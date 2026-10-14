                                                           Semantic Search over 9 Million Mathematical Theorems


                                         Luke Alexander * 1 2 Eric Leonen * 1 3 Sophie Szeto * 1 2 4 Artemii Remizov 1 5 Ignacio Tejeda 1 2 Jarod Alper 1 2
                                                                               Giovanni Inchiostro 1 2 Vasily Ilin 1 2


                                                                    Abstract                                    These statements serve as the fundamental units of reason-
                                                                                                                ing for both human mathematicians and automated proof
                                             Searching for mathematical results remains dif-                    systems (Polu & Sutskever, 2020; Yang et al., 2023; Wu
                                             ficult: most existing tools retrieve entire pa-                    et al., 2022). A researcher proving a new result must first
arXiv:2602.05216v2 [cs.IR] 7 Mar 2026




                                             pers, while mathematicians and theorem-proving                     determine whether the statement already exists in the liter-
                                             agents often seek a specific theorem, lemma, or                    ature, and similarly, an AI agent generating formal proofs
                                             proposition that answers a query. While semantic                   benefits from retrieving relevant lemmas to guide its search.
                                             search has seen rapid progress, its behavior on                    Yet most existing tools – Google Scholar, arXiv, and even
                                             large, highly technical corpora such as research-                  modern LLMs with web access – operate at the level of
                                             level mathematical theorems remains poorly un-                     entire documents, forcing users to manually scan papers
                                             derstood. In this work, we introduce and study                     when they seek a specific statement.
                                             semantic theorem retrieval at scale over a uni-
                                             fied corpus of 9.2 million theorem statements                      This gap is increasingly significant. arXiv hosts over 2.4
                                             extracted from arXiv and seven other sources,                      million papers, including more than 690,000 in mathemat-
                                             representing the largest publicly available cor-                   ics (Ginsparg, 1994). A study of over 14,000 withdrawn
                                             pus of human-authored, research-level theorems.                    arXiv preprints found that 2.5% were retracted because the
                                             We represent each theorem with a short natural-                    authors’ results already appeared in prior literature (Rao
                                             language description as a retrieval representa-                    et al., 2024). For example, Popescu-Pampu (2007), Zhang
                                             tion and systematically analyze how representa-                    (2012), and Shahryari (2020) were withdrawn after discov-
                                             tion context, language model choice, embedding                     ering their main results had been previously established.
                                             model, and prompting strategy affect retrieval                     AI systems face the same problem: the Erdős Problems
                                             quality. On a curated evaluation set of theorem-                   Project documented cases where AI tools “solved” open
                                             search queries written by professional mathemati-                  problems that had been established decades earlier (Erdős &
                                             cians, our approach substantially improves both                    Newman, 1977; Wirsing & Schwarz, 1961; Klarner, 1966) –
                                             theorem-level and paper-level retrieval compared                   underscoring the need for theorem-level search.
                                             to existing baselines, demonstrating that seman-                   In this work, we construct a corpus of over 9 million theorem
                                             tic theorem search is feasible and effective at                    statements from arXiv, the Stacks Project, ProofWiki, and
                                             web scale. The project page, search tool, dataset,                 five other sources, and study semantic retrieval at scale. We
                                             REST API, and MCP server are available at theo-                    represent each theorem using a natural-language “slogan”
                                             remsearch.com.                                                     generated by an LLM, then embed slogans and queries into
                                                                                                                a shared semantic space. Our main contributions are:

                                        1. Introduction                                                           1. A large-scale theorem corpus. We release over 9
                                        Mathematical knowledge is organized around discrete re-                      million theorem statements with rich metadata, the
                                        sults: theorems, lemmas, propositions, and corollaries.                      largest collection of informal mathematical theorems
                                                                                                                     to date.
                                          *
                                            Equal contribution 1 Math AI Lab, University of Washington,
                                        Seattle, United States 2 Department of Mathematics, University of         2. A systematic study of representation choices. We an-
                                        Washington, Seattle, United States 3 Department of Applied and               alyze how the context, LLM choice, embedding model,
                                        Computational Mathematical Sciences, University of Washington,               and prompting strategy affect retrieval. Notably, we
                                        Seattle, United States 4 Paul G. Allen School of Computer Sci-
                                        ence and Engineering, University of Washington, Seattle, United              find that embedding theorems via natural-language slo-
                                        States 5 Lake Washington High School, Kirkland, United States.               gans significantly outperforms embedding their raw
                                        Correspondence to: Vasily Ilin <vilin@uw.edu>.                               LATEX formulations.

                                        Preprint. March 10, 2026.                                                 3. State-of-the-art retrieval. On 111 queries from pro-

                                                                                                            1
                                                      Theorem Search

     fessional mathematicians, we achieve 45.0% Hit@20              ical knowledge; our work extends informalization-based
     at the theorem level, outperforming ChatGPT 5.2 with           retrieval to millions of LATEX theorem statements.
     search (19.8%) and Gemini 3 Pro (27.0%). For paper-
     level retrieval, we achieve 56.8% Hit@20 compared to           Scientific Literature Search. General academic search
     37.8% for Google Search.                                       engines (Google Scholar, Semantic Scholar) and arXiv pro-
                                                                    vide paper-level retrieval but cannot target individual the-
Our results demonstrate that semantic theorem search is fea-        orems. The zbMATH database (Steinfeldt & Mihaljević,
sible at web scale. The project page is at theoremsearch.com.       2024) offers curated paper-level indexing. Large language
The dataset is available at huggingface.co/datasets/uw-math-        models with web access, such as GPT-4 (Achiam et al.,
ai/theorem-search-dataset. A datasheet for our dataset is           2023) and Gemini (Google DeepMind, 2025), can answer
provided in Appendix A.                                             mathematical questions and sometimes locate relevant pa-
                                                                    pers, but as we show in our experiments, they often provide
                                                                    incorrect theorem references or fail to locate specific state-
2. Related Work                                                     ments. Our work treats theorem statements as first-class
Mathematical Information Retrieval. Early MathIR                    retrieval objects, enabling users to find specific results rather
work focused on formula-level retrieval, with the NTCIR             than papers that might contain them.
Math Tasks (Aizawa et al., 2014; Zanibbi et al., 2016) es-
tablishing benchmarks for formula search over arXiv and             3. Data Collection
Wikipedia. The ARQMath shared tasks (Mansouri et al.,
2022) extended this to mathematical question answering              Figure 1 gives an overview of the pipeline used to parse the-
over Math Stack Exchange. A recent survey (Dadure et al.,           orem statements from source documents, generate natural-
2024) notes that while formula retrieval has progressed, se-        language representations, and embed them for retrieval.
mantic understanding of mathematical statements remains
                                                                          Table 1. Distribution of theorem types in our dataset.
an open challenge – the gap our work addresses.

Dense Retrieval and LLM-Augmented Search. Dense                                       Theorem Type         Count
Passage Retrieval (Karpukhin et al., 2020) showed that dual-
                                                                                      Lemma              3,280,463
encoder architectures can outperform sparse methods like
                                                                                      Theorem            2,864,668
BM25. Sentence-BERT (Reimers & Gurevych, 2019) en-
                                                                                      Proposition        2,067,371
abled efficient semantic similarity via Siamese networks,
                                                                                      Corollary          1,034,259
while E5 (Wang et al., 2022), Qwen3-Embedding (Zhang
et al., 2025), and Gemma Embedding (Vera et al., 2025)
have pushed embedding quality further. ColBERT (Khattab             3.1. Theorem Parsing from arXiv
& Zaharia, 2020) introduced late interaction for fine-grained       We source 99.5% (9.2 million) of our theorems from papers
token matching. Retrieval-augmented generation (RAG)                in the arXiv database tagged with math, stat, cs, physics,
(Lewis et al., 2020) combines retrieval with language model         eess, econ, q-fin, or q-bio. A full breakdown of the
generation, enabling systems to ground responses in re-             statement types and arXiv categories across the dataset are
trieved documents. These advances underpin our approach,            provided in Table 1, Figure 2, and Table 7 in Appendix D.
though mathematical text poses unique challenges due to
symbolic notation.                                                  Our objective in parsing theorems is to extract theorem
                                                                    names and bodies. A theorem name has three components:
Search for Formal Mathematics. LeanSearch (Gao et al.,
2024) provides semantic search over Mathlib4’s 230,000+               1. The theorem type (e.g., Theorem, Proposition, Lemma,
theorems by generating natural-language descriptions and                 or Corollary),
using dense retrieval. ReProver (Yang et al., 2023) uses              2. An optional reference number, and
retrieval-augmented generation to select premises during
proof search, and Numina-Lean-Agent (Liu et al., 2026)                3. An optional note. For example, a theorem name might
integrates multiple search tools, including LeanDex, to re-              look like “Theorem 3.9 (Shokurov reduction)”.
trieve lemmas across libraries. LeanFinder (Lu et al., 2025)
focuses on user intent, while LeanExplore (Asher, 2025)             We define the body as the LATEX content of the theorem,
combines embeddings with BM25+ and PageRank. Jiang                  in which basic author-defined macros are expanded. For
et al. (2023) demonstrate that language models can translate        instance, if an author defines \R as a macro for \mathbb{R}
between formal and natural language mathematics. How-               in the LATEX preamble, we replace all occurrences of \R
ever, formal libraries cover only a fraction of mathemat-           accordingly.

                                                                2
                                                         Theorem Search




Figure 1. Overview of the creation of our database and search engine. Items with a “*” are variable and we tested different methods
during our experiments (Sec. 4).


                                                                       The variety of ways authors define theorem environments
                                                                       makes parsing theorems difficult. Thus, we parse theorems
                                                                       for each paper using three strategies:

                                                                        1. Node Search with plasTeX: We use the Python library
                                                                           plasTeX (Arnold, 2009) to convert LATEX sources into a
                                                                           structured node tree. Every command and environment
                                                                           corresponds to a node. We traverse this tree to find
                                                                           environments corresponding to theorem-like structures.
                                                                           Then, we extract the theorem type, reference number,
                                                                           note, and body from the node metadata. This method
                                                                           successfully parses 422 thousand papers, yielding ap-
                                                                           proximately 6.9 million theorems. However, plasTeX
                                                                           occasionally truncates theorem bodies when a paper’s
                                                                           source relies on LATEX packages unknown to the parser.
                                                                           To remove such malformed extractions, we apply sim-
                                                                           ple heuristics, such as filtering out theorems shorter
                                                                           than 8 characters or ending in “ and” or “ let”.

                                                                        2. TeX Logging: As a fallback to plasTeX, we generate
                                                                           and inject a custom LATEX package that logs theorem
                                                                           data. When a paper’s source is compiled, the package
                                                                           records the theorem type, reference number, note, and
                                                                           body for all theorem environments. We parse 137
                                                                           thousand papers this way, yielding approximately 1.8
Figure 2. Sunburst plot of the distribution of arXiv tags across           million theorems.
theorems in our dataset.
                                                                        3. Regex-based Parsing: As a fallback to TeX logging,
                                                                           we use regular expressions to identify theorem delim-
                                                                           iter tokens such as \begin{...} and \end{...} or
                                                                           \proclaim and \endproclaim. We then parse the
                                                                           content between delimiters to extract the theorem’s

                                                                   3
                                                      Theorem Search

     note and body. Reference numbers are not captured un-          3.3. Theorem Representation
     less they are explicitly stated. We parse 30,000 papers
                                                                    Theorems in our corpus are exclusively represented in LATEX,
     this way, yielding approximately 542,000 theorems.
                                                                    and often lack concise natural-language summaries. To ob-
                                                                    tain searchable textual representations and improve retrieval
                                                                    performance, we generate a short natural language descrip-
                                                                    tion, or slogan, for each theorem using a large language
3.2. Theorem Parsing from Other Sources                             model (LLM). This converts the retrieval task from a sym-
                                                                    metric search over formal notation to an asymmetric task
The remaining 0.5% (38,974) of our theorems come from               where informal queries retrieve formalized content (Wang
a variety of other sources: ProofWiki (ProofWiki Contribu-          et al., 2022). Given the parsed theorem body, we prompt the
tors) (23,871), the Stacks Project (The Stacks Project Au-          DeepSeek V3 model (Liu et al., 2024) to produce a concise,
thors) (12,693), the Open Logic Project (The Open Logic             declarative English description of the theorem’s main result.
Project) (745), the CRing Project (The CRing Project Con-           Prompts instruct the LLM to avoid symbolic notation, proof
tributors) (546), Stacks and Moduli (Alper, 2026) (506), the        details, and references to surrounding document structure in
HoTT Book (The Univalent Foundations Program, 2013)                 the generated slogans. The resulting slogans are stored as
(382), and An Infinitely Large Napkin (Chen) (231). These           the primary textual representation for theorem retrieval.
sources were chosen for their verifiability through open-
source contributions and structured, accessible LATEX files.        To study the effect of additional mathematical context on
We favored graduate-level texts, as their theorems would be         slogan quality and retrieval performance, we evaluate three
useful to a mathematician and are often cited by researchers.       slogan-generation strategies:

The Stacks Project, Open Logic Project, CRing Project,                1. Body Only: The prompt includes only the parsed theo-
HoTT Book, and Infinitely Large Napkin are all hosted                    rem body.
as open-source repositories on GitHub. Theorems from
these sources were exclusively delimited in the source by             2. Body + Abstract: The prompt includes the theorem
\begin{...} and \end{...} tags. This uniform structure                   body together with the paper abstract.
allowed us to build a single regex-based parser, similar to
our regex-based parser for arXiv, that could extract theorems         3. Body + Introduction: The prompt includes the theo-
from all five sources. Our parser first normalizes shorthand             rem body together with the paper introduction.
environment names, then extracts the theorem name, body,
label, and type from each environment. When a theorem               Each strategy uses a similar prompt template as shown in
body begins with a bracketed note, we append it to the the-         11. Their major differences are in the contextual fields
orem name in parentheses for easier identification. Labels          provided to the model. Model temperature is fixed at 0.2,
defined with \label{...} are captured to preserve cross-            and the maximum output tokens is fixed at 1024. Slogans
referencing information from the original text. Since these         are generated independently for each variant and treated as
repositories use GitHub’s file structure, we generate source        separate representations of the same underlying theorem
URLs pointing to the original .tex files, enabling users to         during evaluation. The total cost of building the corpus was
verify theorems against their source material. In addition,         approximately $6,000 USD: $4,000 for LLM API calls to
a custom theorem counter was used to reliably generate              generate slogans across all 9.2 million theorems, and $2,000
reference numbers.                                                  for compute and S3 storage.
ProofWiki required a different approach, as it is a wiki-
                                                                    3.4. Result Retrieval
based encyclopedia built on MediaWiki rather than LATEX.
ProofWiki stores content in wikitext format with mathemat-          We embed theorem slogans and user queries using the
ical expressions enclosed in <math>...</math> tags. We              Qwen3-Embedding-8B model (Zhang et al., 2025), which
developed a separate parser that interfaces with the Medi-          maps natural language inputs to fixed-dimensional vec-
aWiki API to programmatically retrieve pages from relevant          tors. All theorem slogans are embedded offline following
categories. For each page, we extract the theorem statement         their generation by the LLM and stored in a PostgreSQL
by identifying section headers and capturing content up to          database (Stonebraker & Rowe, 1986) with the pgvector
the proof section. The wikitext is then cleaned by removing         extension (pgvector Contributors, 2024). The database em-
MediaWiki-specific markup such as <onlyinclude> tags,               ploys a Hierarchical Navigable Small World (HNSW) index
template calls, and wiki links, while converting <math>             (Malkov & Yashunin, 2020) combined with binary quanti-
blocks to standard delimiters. Since ProofWiki assigns a            zation, enabling fast approximate nearest-neighbor search.
unique URL to each theorem, we preserve these links to              User queries are embedded at inference time using the same
allow direct verification.                                          method. Within this shared embedding space, we retrieve

                                                                4
                                                        Theorem Search

the top-k theorems ranked by their Hamming distance, then             in the top k results:
re-ranked by cosine similarity.
                                                                                                    |Q|
                                                                                             1 X
                                                                                    Hit@k =          max I(ri,j )
3.5. Validation Set                                                                         |Q| i=1 1≤j≤k
Enlisting the help of three research mathematicians, we
                                                                      where Q is the set of queries, ri,j is the j-th result of the
curated a set of 111 distinct math queries across 14 arXiv
                                                                      i-th query, and I(ri,j ) equals 1 if and only if ri,j is an
tags, mainly Algebraic Geometry, Analysis, and PDEs. See
                                                                      exact match. We also use Mean Reciprocal Rank (MRR@k)
Table 6 in the Appendix for a detailed breakdown. These
                                                                      (Craswell, 2009), which takes the reciprocal of the rank at
queries search for distinct theorems, lemmas, corollaries,
                                                                      which an exact match is discovered:
and propositions written by a small number of authors whose
work our subject matter experts are well-acquainted with.                                                 |Q|
                                                                                                     1 X 1
Crucially, queries were written blind: each mathematician                              MRR@k =
                                                                                                    |Q| i=1 ranki
composed natural-language descriptions of theorems they
knew from memory, without access to the corpus or its                 where ranki is the position of the first relevant result.
slogans, to prevent any leakage of retrieval representations
into the evaluation queries. We then asked them to select
                                                                      4.2. Setup
a larger dataset of papers in which they were confident
that the results of the queries they wrote appeared at most           We chose three embedders to use in our experiments:
once; this larger dataset consisted of 7,356 papers. We               Google’s Gemma 0.3B (Vera et al., 2025), and both Qwen3
used this larger dataset to guide our decisions on which              0.6B and 8B (Zhang et al., 2025). Our baseline meth-
embedders to use, which LLM to use for the slogans, how to            ods consist of the following: Filtered Google Search
prompt the embedder, and how much context to give to the              (site:arxiv.org + Query), arXiv advanced search, Chat-
LLM when generating the slogans (body of the result only,             GPT 5.2 w/ Search, and Gemini 3 Pro (Google DeepMind,
body+abstract, body+first section). Every query–theorem               2025); the prompts used for the LLM baselines are provided
pair was subsequently verified in a two-stage quality check:          in Table 12 in the Appendix.
an LLM confirmed that the target theorem exists in the
                                                                      Both Google and arXiv are unable to return specific math
corpus and semantically matches the query, and a second
                                                                      statements, so their performance is graded on their ability
mathematician independently reviewed each pair to ensure
                                                                      to locate the correct paper. Conversely, LLM-based systems
correctness.
                                                                      like ChatGPT and Gemini occasionally return correct results
We remark that while small, this size is typical of mathemat-         with incorrect reference numbers; we grade these as misses
ical information retrieval datasets, such as the query set of         on theorem-level retrieval and treat them as paper matches
LeanSearch for Mathlib4 (Gao et al., 2024) and ARQMath-               for paper-level retrieval.
3 (Mansouri et al., 2022), which contain 50 and 78 queries,
                                                                      We emphasize that these baselines are not designed for
respectively.
                                                                      theorem-level retrieval, but we evaluate them to reflect the
                                                                      tools currently used by LLMs and research mathematicians
4. Experiments                                                        in the absence of specialized theorem-level search systems.
In this section, we report the evaluation performance of exist-
ing retrieval methods against our search engine. We outline           4.3. Main Results
the experiment setup, compare the performance against ex-             Our results are presented in Table 2. We find that the embed-
isting retrieval tools, and perform an ablation study on both         der Qwen3 8B outperforms existing literature review meth-
the context window and the LLM used for slogan genera-                ods across all metrics. In particular, Qwen3 8B achieves
tion.                                                                 substantially higher Hit@10 and Hit@20, indicating that
                                                                      the correct theorem is frequently retrieved within the top
4.1. Metrics                                                          candidate set even when it is not ranked first. This behavior
                                                                      is desirable in large-scale theorem retrieval, where down-
To measure the performance of our search engine against
                                                                      stream reranking or human inspection can refine results once
existing literature review tools, we employ two commonly
                                                                      relevant candidates have been surfaced. We further apply
used information retrieval metrics, following standard prac-
                                                                      a cross-encoder reranker (Qwen3-Reranker-0.6B (Zhang
tice in mathematical retrieval benchmarks (Mansouri et al.,
                                                                      et al., 2025)) to rescore the top-100 candidates retrieved by
2022; Dadure et al., 2024). Hit@k, also known as the hit
                                                                      Qwen3 8B; this improves theorem-level Hit@1 from 17.1%
rate, measures whether the correct result appears anywhere
                                                                      to 18.9% and MRR@20 from 24.3% to 27.0%, confirming
                                                                      that late interaction over full query–slogan pairs captures

                                                                  5
                                                              Theorem Search

Table 2. Results on the validation set, comparing embedder performance against existing literature search tools. Values are reported as
theorem-level / paper-level. Google Search and arXiv search cannot return specific theorem statements, so only paper-level results are
reported. Our corpus was restricted to arXiv papers for evaluation.


                 M ODEL                                 H IT @1            H IT @10          H IT @20       MRR@20
                                                                  BASELINE
                                       †
                 G OOGLE S EARCH                         0.162              0.378             0.378           0.237
                                 †
                 AR X IV S EARCH                         0.009              0.018             0.027           0.011
                 C HAT-GPT 5.2                           0.117              0.180             0.198           0.139
                 G EMINI 3 P RO                          0.171              0.252             0.270           0.196
                                                               O UR M ETHODS
                 G EMMA 0.3B (LAT X)
                                   E                0.027 / 0.054      0.090 / 0.117       0.090 / 0.135   0.041 / 0.070
                 G EMMA 0.3B                        0.081 / 0.108      0.189 / 0.225       0.252 / 0.306   0.118 / 0.154
                 Q WEN 3 0.6B                       0.081 / 0.153      0.234 / 0.342       0.270 / 0.351   0.132 / 0.215
                 Q WEN 3 8B                         0.171 / 0.243      0.387 / 0.505       0.450 / 0.568   0.243 / 0.328
                 Q WEN 3 8B W / R ERANKER           0.189 / 0.324      0.432 / 0.613       0.450 / 0.631   0.270 / 0.416
                 †
                     PAPER - LEVEL ONLY: THESE TOOLS CANNOT RETURN INDIVIDUAL THEOREMS .



fine-grained semantic distinctions that the bi-encoder alone               about the boundary of a KSBA compactification of elliptic
misses.                                                                    surface pairs to Claude (Opus 4.5). Without retrieval aug-
                                                                           mentation, Claude produced a confidently stated but incor-
For search methods at the paper-level, Qwen3 8B continues
                                                                           rect answer, concluding that all boundary pairs must retain
to outperform the baseline models, achieving higher Hit@1
                                                                           a fibration structure. The argument, while superficially plau-
and MRR. The arXiv search is limited in the fields it can
                                                                           sible, relied on incorrect claims about the behavior of slc
search over and does not search within the paper body, so it
                                                                           surface pairs under KSBA compactification.
was only able to locate two papers across the whole query
set in the top-20 results.                                                 When the same question was posed with access to our the-
                                                                           orem database as a RAG tool, Claude retrieved relevant
One notable effect we observed concerns how Chat-GPT
                                                                           results from (Ascher & Bejleri, 2017; Ascher et al., 2018;
and Gemini rank retrieved results. Although both models
                                                                           Inchiostro, 2018; Ascher & Bejleri, 2016) and arrived at the
used web-search-based retrieval, they would often organize
                                                                           correct answer: such boundary pairs do exist, and they are
their outputs primarily at the paper level, returning multiple
                                                                           pseudoelliptic surfaces obtained by contracting the section
theorems from the same paper in consecutive positions be-
                                                                           of an elliptic fibration. The RAG-augmented response cited
fore moving to another paper. This ranking pattern reduces
                                                                           specific theorem numbers and provided a logically valid
result diversity, which lowers Hit@k despite sometimes
                                                                           chain of reasoning grounded in retrieved results. This il-
achieving high early precision. On average, Gemini returns
                                                                           lustrates a key failure mode of LLM reasoning—without
only 10.98 distinct papers per query, compared to 16.89 for
                                                                           access to the relevant literature, the model confabulates
Qwen3 8B, indicating that our retrieval pipeline surfaces a
                                                                           plausible-sounding but incorrect mathematical arguments—
broader cross-section of the literature.
                                                                           and demonstrates that retrieval augmentation over our cor-
Our approach is particularly advantageous for retrieving                   pus can directly address it. The full query, both responses,
auxiliary lemmas and technical results that appear deep                    and detailed citations are reported in Appendix C.
within a paper, far from the title and abstract. Google Search
and LLM-based tools rely heavily on paper-level metadata                   4.5. Ablation Studies
and thus struggle to surface results whose content is not
reflected in the abstract, whereas our system indexes every                In this subsection, we perform ablation studies on the con-
theorem independently via its slogan, making it equally as                 text windows used for slogan generation, the LLMs used to
capable of retrieving a minor lemma in a later section as a                generate slogans, and the document preparation process. For
paper’s headline theorem.                                                  each ablation, we limit the corpus to arXiv papers labeled
                                                                           with the algebraic geometry tag (math.AG) and authored
                                                                           by individuals whose work contains an exact match to one
4.4. Retrieval-Augmented LLM Reasoning
                                                                           of our queries. This filtering reduces the corpus to 7,356
Beyond quantitative retrieval metrics, we investigate                      statements written by 8 primary authors.
whether our theorem corpus can improve LLM reasoning on
research-level mathematical questions. We posed a question


                                                                       6
                                                           Theorem Search

4.5.1. A BLATION OF C ONTEXT W INDOWS                                  Table 4. Comparing LLM slogans in retrieval performance. Em-
                                                                       bedded with prompt using Qwen3 8B (Zhang et al., 2025). Body +
Table 3 presents the effects of context on slogan generation.          Abstract
Increasing or decreasing the amount of context provided
to LLMs when generating math slogans considerably af-
                                                                         M ODEL                H IT @1     H IT @10    H IT @20   MRR@20
fects our search engine’s performance, while holding the
                                                                                                         LLM S
embedder constant. We find that supplying the LLM with
                                                                         D EEPSEEK V3.1        0.316        0.645       0.737      0.429
additional paper context improves the retrieval performance              D EEPSEEK R1          0.276        0.671       0.697      0.388
of its generated slogans. Performance falters when the LLM               G EMINI 3 P RO        0.368        0.750       0.816      0.507
is only given the abstract, but improves significantly with              C LAUDE O PUS 4.5     0.395        0.776       0.842      0.536
the inclusion of the first section of the paper, defined by
\section{}. We attribute this improvement to the LLM                   Table 5. Comparing prompting performance. Slogans generated
                                                                       by DeepSeek V3.1 (Liu et al., 2024) on ‘Body+Abstract’ context
making better sense of the statement with more context,                window.
especially since theorems alone tend to be at most 3–4 sen-
tences long and may reference earlier sections of the paper.
Furthermore, the introduction of most math papers typically              M ODEL          H IT @1         H IT @10     H IT @20    MRR@20
outlines the results and the existing research upon which                                            U NPROMPTED
they build. As a result, context-rich slogans better capture             G EMMA 0.3B         0.303        0.539        0.566       0.376
the semantic intent of the theorem, yielding more reliable               Q WEN 3 0.6B        0.224        0.487        0.526       0.297
and robust retrieval across queries. Results for an expanded             Q WEN 3 8B          0.250        0.553        0.618       0.332
ablation covering additional embedders are reported in Ta-                                            P ROMPTED
ble 8 in Appendix E.                                                     G EMMA 0.3B         0.197        0.434        0.487       0.265
                                                                         Q WEN 3 0.6B        0.237        0.566        0.658       0.346
Table 3. Comparing context window size in retrieval performance.         Q WEN 3 8B          0.316        0.645        0.737       0.496
Embedded with prompt using Qwen3 8B (Zhang et al., 2025).
Slogans generated with DeepSeek V3 (Liu et al., 2024).
                                                                       of the prompts made by (Gao et al., 2024), the details of
                                                                       which are listed in Table 10.
  M ODEL                H IT @1   H IT @10   H IT @20   MRR@20
                        C ONTEXT W INDOWS
                                                                       4.6. Embedding Space Analysis
  B ODY O NLY           0.342      0.658      0.737      0.451
  W / A BSTRACT         0.316      0.645      0.737      0.429         Following (Gao et al., 2024; Jiang et al., 2023), we con-
  W / F IRST S ECTION   0.368      0.737      0.763      0.496
                                                                       vert LATEX theorem statements into natural-language slogans
                                                                       before embedding, since embedders struggle with symbol-
4.5.2. A BLATION OF S LOGAN G ENERATOR                                 heavy notation (Bleckmann & Tschisgale, 2025; Peng et al.,
                                                                       2021) and mathematicians typically query in informal lan-
The LLM used to generate the slogans can also significantly            guage. To verify that sloganization induces semantically
affect our engine’s search performance, as some LLMs are               meaningful structure, we use PCA and UMAP as diagnostic
better trained on mathematical texts than others and thus              tools on a random sample of 10,000 theorems (1,000 from
generate better informal versions of math statements. We               each of the 10 most common arXiv categories).
find that leading proprietary models, such as Claude’s Opus
                                                                       Figure 3 shows PCA projections for three categories: Alge-
4.5 and Gemini 3 Pro (Google DeepMind, 2025), outper-
                                                                       braic Geometry, Probability Theory, and Statistics Theory.
form open-source models such as DeepSeek-V3 (Liu et al.,
                                                                       Conceptually distant fields (Algebraic Geometry vs. Proba-
2024), as summarized in Table 4. A broader comparison
                                                                       bility) are well separated, while closely related fields (Prob-
across additional slogan generators and embedding models
                                                                       ability vs. Statistics) overlap substantially – consistent with
is provided in Table 9 in Appendix E.
                                                                       mathematical intuition. UMAP projections over all ten cate-
                                                                       gories in Figure 4 reveal that Qwen3 8B produces tighter,
4.5.3. A BLATION OF TASK I NSTRUCTION
                                                                       better-separated clusters than Gemma 0.3B, consistent with
We examine the impact of the task instructions used during             the retrieval gap in Table 2.
embeddings on retrieval performance in Table 5. We find
that by providing a math retrieval instruction, both Qwen              5. Search Tool
embedders achieve higher performance than without any
instruction at all. However, this effect is reversed with              The search tool is currently accessible via HuggingFace
Gemma, with empty instruction performing better, though                Spaces (Link). Users can perform semantic searches using
worse than Qwen 8B with instruction. We use a modification             natural language (e.g., “a rational variety is simply con-

                                                                   7
                                                        Theorem Search

nected”). The sidebar interface allows results to be filtered         JSON queries and returns ranked theorem results, enabling
by relevant metadata (e.g., author sets, arXiv category tags,         programmatic integration into research workflows. We
and journal publication status). To optimize retrieval time,          also expose a Model Context Protocol (MCP) server at
the search uses a two-stage retrieval architecture. At in-            api.theoremsearch.com/mcp, allowing AI agents and
ference time, the natural language query is encoded us-               LLM-based tools to use theorem search as a retrieval tool
ing the Qwen3-8B embedding model and binary quantized                 during reasoning and proof generation. The project page,
into 4096 bits. An initial pool of clamp(max(200, 12 ×                including links to the search tool, API, MCP server, and
k), 200, 800) candidates is returned using the HNSW index             dataset, is available at theoremsearch.com.
and Hamming distance, where k is a user-specified number
of results to return. The candidate pool is then filtered by          6. Conclusion
metadata and reranked using cosine similarity on the orig-
inal 4096-dimensional embeddings. When weighting by                   Mathematical knowledge is organized around discrete re-
citations is enabled, the candidates are instead re-ranked            sults – theorems, lemmas, propositions, and corollaries
using the following composite scoring function:                       – yet existing search tools operate at the document level,
                                                                      forcing researchers and AI agents alike to manually locate
  score = cosine similarity + λ · log(max(citations, 1))
                                                                      specific statements within papers. In this work, we ad-
where λ is the user-specified citation-weight parameter. The          dressed this gap by constructing a corpus of over 9.2 million
interface retrieves the top k results, each of which displays         theorem statements extracted from arXiv and seven other
the theorem slogan, the theorem body rendered in LaTeX,               sources, constituting the largest unified collection of human-
any relevant paper metadata, and a link to the paper. Finally,        authored, research-level theorems to date.
a lightweight feedback system allows users to rate each               We showed that representing theorems via natural-language
result’s relevance to their query. The resulting end-to-end           slogans generated by an LLM, rather than embedding raw
latency is approximately 3 seconds per query, compared to             LATEX directly, yields substantially better retrieval perfor-
60+ seconds for LLM-based search tools such as ChatGPT                mance. Our systematic ablations revealed that context mat-
and Gemini, which must perform multiple web searches                  ters: slogans generated with access to the paper’s introduc-
and parse documents at inference time. See Figure 5 for the           tion outperform those generated from the theorem body
interface.                                                            alone, and the choice of both the slogan-generating LLM
Because our slogans are multi-sentence descriptions, the              and the embedding model significantly affects downstream
embedding model produces vectors that are optimized for               retrieval quality. On a curated evaluation set of 111 queries
longer inputs. Short keyword-style queries (e.g., “Landau             written by professional mathematicians, our best configura-
equation”) can therefore be dominated by padding or generic           tion achieves 45.0% Hit@20 at the theorem level and 56.8%
context, leading to poor retrieval. We find that simply repeat-       Hit@20 at the paper level, outperforming ChatGPT 5.2 with
ing a short query (e.g., “Landau equation Landau equation”)           search, Gemini 3 Pro, and Google Search.
substantially improves result quality by strengthening the            By treating theorems as first-class retrieval objects and en-
signal of the key terms in the embedding. The search tool             riching them with natural-language descriptions, we enable
applies this duplication automatically when the query is              new forms of access to mathematical knowledge – whether
below a length threshold.                                             for retrieval-augmented generation by LLMs, for premise
In addition to the web interface, we provide a REST                   selection in formal proof search, or for literature review by
API at api.theoremsearch.com/search that accepts                      expert mathematicians. We have deployed a public search
                                                                      interface described in Appendix 5. Qualitative user feed-
                                                                      back from research mathematicians, reported in Appendix B,
                                                                      further illustrates the practical utility of our system.

                                                                      Acknowledgments
                                                                      We thank Michele Pernice and Dori Bejleri for contributing
                                                                      several entries to the validation set. CPU and GPU com-
                                                                      puting, LLM inference and data storage were in part done
                                                                      using AWS credits from the UW eScience School and UW
                                                                      IT. CPU and GPU computing was in part done using the
                                                                      UW Research Computing Club funded from the UW Stu-
Figure 3. PCA visualizations of theorems in our dataset using
slogan embeddings. Left: Gemma embedding. Right: Qwen3 8B             dent Technology Fee Committee. GPU computing was in
embedding.                                                            part done on UWIT’s GPU cluster Tillicum. GPU comput-

                                                                  8
                                                            Theorem Search




Figure 4. UMAP visualizations of 10,000 theorem slogan embeddings across the ten most common arXiv categories. Gemma 0.3B (left)
and Qwen3 8B (right). Qwen3 8B produces tighter, better-separated clusters.




Figure 5. The interface of the Theorem Search Tool. The main window displays the top results: paper name, paper authors, and theorem
statement, and link to the paper. In the left pane users can filter by paper metadata: type of result (theorem/proposition/lemma/corollary),
author(s), arXiv tag, specific paper, year, and publication status. The thumbs up/down allow for user feedback, used to further improve the
search results.




                                                                     9
                                                    Theorem Search

ing and model inference were in part done using Nebius and        References
TokenFactory.
                                                                  Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I.,
                                                                    Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S.,
                                                                    Anadkat, S., et al. Gpt-4 technical report. arXiv preprint
                                                                    arXiv:2303.08774, 2023.

                                                                  Aizawa, A., Kohlhase, M., Ounis, I., and Schubotz, M.
                                                                    NTCIR-11 Math-2 Task Overview. In Proceedings of the
                                                                    11th NTCIR Conference, pp. 88–98, Tokyo, Japan, 2014.

                                                                  Alper, J. Stacks and moduli. https://sites.math.
                                                                    washington.edu//˜jarod/moduli.pdf, 2026.

                                                                  Arnold, T. Getting started with plasTeX. TUGboat,
                                                                    30(2):180–185, 2009. URL https://www.tug.org/
                                                                    TUGboat/tb30-2/tb95arnold.pdf.

                                                                  Ascher, K. and Bejleri, D. Moduli of fibered surface pairs
                                                                    from twisted stable maps, 2016. URL https://arxiv.
                                                                    org/abs/1612.00792.

                                                                  Ascher, K. and Bejleri, D. Log canonical models of elliptic
                                                                    surfaces, 2017. URL https://arxiv.org/abs/1610.
                                                                    08033.

                                                                  Ascher, K., Bejleri, D., and Inchiostro, G. Moduli of
                                                                    weighted stable elliptic surfaces and invariance of log
                                                                    plurigenera, 2018. URL https://arxiv.org/abs/
                                                                    1702.06107.

                                                                  Asher, J. Leanexplore: A search engine for lean 4 declara-
                                                                    tions. arXiv preprint arXiv:2506.11085, 2025.

                                                                  Bahturin, Y., Mikhalev, A. V., Petrogradsky, V. M., and
                                                                    Zaicev, M. V. Infinite dimensional Lie superalgebras,
                                                                    volume 7. Walter de Gruyter, 2011.

                                                                  Bleckmann, T. and Tschisgale, P. Evaluating nlp embed-
                                                                    ding models for handling science-specific symbolic ex-
                                                                    pressions in student texts, 2025. URL https://arxiv.
                                                                    org/abs/2505.17950.

                                                                  Chen, E. An infinitely large napkin. https://venhance.
                                                                    github.io/napkin/. Accessed 2026-01-25.

                                                                  Craswell, N. Mean Reciprocal Rank, pp. 1703–1703.
                                                                    Springer US, Boston, MA, 2009. doi: 10.1007/
                                                                    978-0-387-39940-9 488.

                                                                  Dadure, P., Pakray, P., and Bandyopadhyay, S. Mathematical
                                                                    information retrieval: A review. ACM Computing Surveys,
                                                                    57(3):1–34, 2024. doi: 10.1145/3699953.

                                                                  Erdős, P. and Newman, D. J. Bases for sets of integers.
                                                                    Journal of Number Theory, 9(4):420–425, 1977.

                                                             10
                                                        Theorem Search

Gao, G., Ju, H., Jiang, J., Qin, Z., and Dong, B. A se-                Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao,
  mantic search engine for mathlib4. In Findings of the                  C., Deng, C., Zhang, C., Ruan, C., et al. Deepseek-v3
 Association for Computational Linguistics: EMNLP 2024.                  technical report. arXiv preprint arXiv:2412.19437, 2024.
  Association for Computational Linguistics, 2024. URL
  https://arxiv.org/abs/2403.13310.                                    Liu, J., Zhou, Z., Zhu, Z., Dos Santos, M., He, W., Liu, J.,
                                                                         Wang, R., Xie, Y., Zhao, J., Wang, Q., Zhi, L., Li, J., and
Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W.,               Li, W. Numina-lean-agent: An open and general agentic
 Wallach, H., Daumé III, H., and Crawford, K. Datasheets                reasoning system for formal mathematics. 2026. URL
  for datasets. Communications of the ACM, 64(12):86–92,                 https://arxiv.org/abs/2601.14027.
  December 2021. doi: 10.1145/3458723.
                                                                       Lu, J., Emond, K., Yang, K., Chaudhuri, S., Sun, W., and
Ginsparg, P. First steps towards electronic research commu-
                                                                         Chen, W. Lean finder: Semantic search for mathlib that
  nication. Computers in Physics, 8(4):390–396, 1994. doi:
                                                                         understands user intents. 2025. URL https://arxiv.
  10.1063/1.4823313.
                                                                         org/abs/2510.15940.
Google DeepMind. Gemini 3: Introducing the latest gem-
  ini AI model from Google. https://blog.google/                       Malkov, Y. A. and Yashunin, D. A. Efficient and robust
  products/gemini/gemini-3/, November 2025. Ac-                         approximate nearest neighbor search using hierarchical
  cessed 2026-01-25.                                                    navigable small world graphs. IEEE Transactions on
                                                                        Pattern Analysis and Machine Intelligence, 42(4):824–
Hu, X., Shan, Z., Zhao, X., Sun, Z., Liu, Z., Li, D., Ye,               836, 2020. doi: 10.1109/TPAMI.2018.2889473.
  S., Wei, X., Chen, Q., Hu, B., Wang, H., Yu, J., and
  Zhang, M. Kalm-embedding: Superior training data                     Mansouri, B., Novotný, V., Agarwal, A., Oard, D. W., and
  brings a stronger embedding model, 2025. URL https:                   Zanibbi, R. Overview of ARQMath-3 (2022): Third
 //arxiv.org/abs/2501.01028.                                            CLEF lab on answer retrieval for questions on math.
                                                                        In Experimental IR Meets Multilinguality, Multimodal-
Inchiostro, G. Moduli of weierstrass fibrations with marked             ity, and Interaction, volume 13390 of Lecture Notes in
  section, 2018. URL https://arxiv.org/abs/1808.                        Computer Science, pp. 286–310. Springer, 2022. doi:
  03539.                                                                10.1007/978-3-031-13643-6 20.
Jiang, A. Q., Li, W., and Jamnik, M. Multilingual mathe-
                                                                       Peng, S., Yuan, K., Gao, L., and Tang, Z. Mathbert: A pre-
   matical autoformalization. 2023. URL https://arxiv.
                                                                         trained model for mathematical formula understanding,
   org/abs/2311.03755.
                                                                         2021. URL https://arxiv.org/abs/2105.00377.
Karpukhin, V., Oğuz, B., Min, S., Lewis, P., Wu, L., Edunov,
  S., Chen, D., and Yih, W.-t. Dense passage retrieval                 pgvector Contributors.      pgvector: Vector similarity
  for open-domain question answering. In Proceedings                     search for Postgres. https://github.com/pgvector/
  of the 2020 Conference on Empirical Methods in Nat-                    pgvector, 2024. Accessed 2026-01-25.
  ural Language Processing (EMNLP), pp. 6769–6781.
                                                                       Polu, S. and Sutskever, I. Generative language model-
  Association for Computational Linguistics, 2020. doi:
                                                                         ing for automated theorem proving. arXiv preprint
 10.18653/v1/2020.emnlp-main.550.
                                                                         arXiv:2009.03393, 2020.
Khattab, O. and Zaharia, M. ColBERT: Efficient and ef-
  fective passage search via contextualized late interaction           Popescu-Pampu, P. Stein or Milnor fillability and cohomol-
  over BERT. In Proceedings of the 43rd International                    ogy, 2007. Withdrawn; merged into arXiv:0712.3484
 ACM SIGIR Conference on Research and Development                        after discovering a theorem had already been proved by
  in Information Retrieval, pp. 39–48. ACM, 2020. doi:                   Durfee and Hain.
 10.1145/3397271.3401075.
                                                                       ProofWiki Contributors. ProofWiki. https://proofwiki.
Klarner, D. A. Representations of n as a sum of distinct ele-            org. Accessed 2026-01-25.
  ments from special sequences. The Fibonacci Quarterly,
  4(4):289–306, 1966.                                                  Rao, D., Young, J., Dietterich, T., and Callison-Burch, C.
                                                                         Withdrarxiv: A large-scale dataset for retraction study.
Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V.,            arXiv preprint arXiv:2412.03775, 2024.
  Goyal, N., Küttler, H., Lewis, M., Yih, W.-t., Rocktäschel,
  T., Riedel, S., and Kiela, D. Retrieval-augmented genera-            Reimers, N. and Gurevych, I. Sentence-BERT: Sentence em-
  tion for knowledge-intensive NLP tasks. In Advances in                 beddings using siamese BERT-networks. In Proceedings
  Neural Information Processing Systems, volume 33, pp.                  of the 2019 Conference on Empirical Methods in Natu-
  9459–9474. Curran Associates, Inc., 2020.                              ral Language Processing and the 9th International Joint

                                                                  11
                                                      Theorem Search

  Conference on Natural Language Processing (EMNLP-                  Wu, Y., Jiang, A. Q., Li, W., Rabe, M., Staats, C., Jam-
  IJCNLP), pp. 3982–3992. Association for Computational               nik, M., and Szegedy, C. Autoformalization with large
  Linguistics, 2019. doi: 10.18653/v1/D19-1410.                       language models. In Advances in Neural Information
                                                                      Processing Systems, volume 35, 2022.
Shahryari, M. A note on surjunctive groups, 2020. With-
  drawn; the main result had already been proved by                  Yang, K., Swope, A. M., Gu, A., Chalamala, R., Song,
  Arzhantseva et al.                                                   P., Yu, S., Godil, S., Prenger, R., and Anandkumar, A.
                                                                       LeanDojo: Theorem proving with retrieval-augmented
Steinfeldt, C. and Mihaljević, H. Evaluation and domain               language models. In Advances in Neural Information
  adaptation of similarity models for short mathematical               Processing Systems, volume 36, 2023.
  texts. In Intelligent Computer Mathematics: 17th In-
  ternational Conference, CICM 2024, Lecture Notes in                Zanibbi, R., Aizawa, A., Kohlhase, M., Ounis, I., Topić, G.,
  Computer Science, pp. 241–260, Montréal, QC, Canada,                and Davila, K. NTCIR-12 MathIR Task Overview. In
  2024. Springer. doi: 10.1007/978-3-031-66997-2 14.                   Proceedings of the 12th NTCIR Conference, pp. 299–308,
                                                                       Tokyo, Japan, 2016.
Stonebraker, M. and Rowe, L. A. The design of POSTGRES.
  In Proceedings of the 1986 ACM SIGMOD International                Zhang, S. On non-congruent numbers with ≡ 3 (mod 8)
  Conference on Management of Data, pp. 340–355, 1986.                 prime factors, 2012. Withdrawn; the result is a corollary
  doi: 10.1145/16894.16888.                                            of a well-known result by Monsky.
                                                                     Zhang, Y., Li, M., Long, D., Zhang, X., Lin, H., Yang,
The CRing Project Contributors. The CRing project. https:
                                                                       B., Xie, P., Yang, A., Liu, D., Lin, J., Huang, F., and
  //math.mit.edu/˜hrm/the_cring_project.pdf.
                                                                       Zhou, J. Qwen3 embedding: Advancing text embedding
  Accessed 2026-01-25.
                                                                       and reranking through foundation models. 2025. URL
The Open Logic Project.  Open logic.    https://                       https://arxiv.org/abs/2506.05176.
  openlogicproject.org. Accessed 2026-01-25.
                                                                     Zhao, X., Hu, X., Shan, Z., Huang, S., Zhou, Y., Zhang,
The Stacks Project Authors. The stacks project. https:                 X., Sun, Z., Liu, Z., Li, D., Wei, X., Pan, Y., Xiang,
  //stacks.math.columbia.edu. Accessed 2026-01-                        Y., Zhang, M., Wang, H., Yu, J., Hu, B., and Zhang, M.
  25.                                                                  Kalm-embedding-v2: Superior training techniques and
                                                                       data inspire a versatile embedding model, 2025. URL
The Univalent Foundations Program. Homotopy Type                       https://arxiv.org/abs/2506.20923.
  Theory: Univalent Foundations of Mathematics. In-
  stitute for Advanced Study, 2013. URL https://
  homotopytypetheory.org/book/.

Usefi, H. Isomorphism invariants of restricted enveloping
  algebras, 2009. URL https://arxiv.org/abs/0804.
  2281.

Vera, H. S., Dua, S., Zhang, B., Salz, D., Mullins, R., Pa-
  nyam, S. R., Smoot, S., Naim, I., Zou, J., Chen, F., et al.
  Embeddinggemma: Powerful and lightweight text repre-
  sentations. arXiv preprint arXiv:2509.20354, 2025.

Wang, L., Yang, N., Huang, X., Jiao, B., Yang, L., Jiang, D.,
 Majumder, R., and Wei, F. Text embeddings by weakly-
 supervised contrastive pre-training. arXiv preprint
 arXiv:2212.03533, 2022. URL https://arxiv.org/
 abs/2212.03533.

Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R.,
 and Wei, F. Multilingual e5 text embeddings: A technical
 report. arXiv preprint arXiv:2402.05672, 2024.

Wirsing, E. and Schwarz, W. Approximation mit algebrais-
 chen zahlen beschränkten grades. 1961.

                                                                12
                                                      Theorem Search

A. Datasheet
This section is based on Datasheets for Datasets by (Gebru et al., 2021).

A.1. Motivation
 1. For what purpose was the dataset created?
        • We created this dataset to create the largest unified corpus of mathematical theorems. We use this dataset ourselves
          to create a theorem search engine.

 2. Who created the dataset?
        • This paper’s co-authors collected theorems. All theorems were written by the authors of the theorems’ papers and
          are cited in our database.

 3. Who funded the creation of the dataset?
        • Self-funded.

A.2. Composition
 1. What do the instances that comprise the dataset represent?
        • Each instance of the dataset represents a mathematical statement derived from a paper, textbook, or repository
          online.

 2. How many instances are there in total?
        • As of writing, there are 9.2 million mathematical statements in the dataset.

 3. Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set?
        • The dataset contains a non-random sample of instances from available math corpora.

 4. What data does each instance consist of?
        • Each instance contains the name of the theorem as displayed in the source document (e.g. Theorem 1.1), the raw
          TeX body, the author-written label inside the body, and the paper it was sourced from (e.g. arXiv’s convention of
          1234.56789v1).
        • In addition, we stored metadata from each source document. This data includes the title, the list of authors, the
          link to the document, the abstract, the journal the document was published in (if it was published), the primary and
          secondary categories, the number of citations (if available), and a tag of which source it came from (e.g. arXiv,
          Stacks Project).

 5. Is there a label or target associated with each instance?
        • Each theorem uses its name derived from the source document, and lists the document it came from, creating a
          distinct method of identification.

 6. Is any information missing from individual instances?
        • No.

 7. Are relationships between individual instances made explicit?
        • Each instance is numbered according to the conventions of the source document. They also contain metadata
          linking them to a specific paper or document.

 8. Are there recommended data splits? (e.g., training, development/validation, testing)
        • Not applicable.

 9. Are there any errors, sources of noise, or redundancies in the dataset?

                                                             13
                                                      Theorem Search

       • Some statement bodies, titles, and labels may be fragmented, as our parsing methods are not applicable to every
         TeX document in our sources.

10. Is the dataset self-contained, or does it link to or otherwise rely on external resources?

       • The data is derived from sources online.

11. Does the dataset contain data that might be considered confidential?

       • No, all data is publicly available online.

12. Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise
    cause anxiety?

       • No.


A.3. Collection Process
 1. How was the data associated with each instance acquired?

       • A LaTeX parser was used to parse all theorem names and bodies from sources.

 2. What mechanisms or procedures were used to collect the data?

       • Our LaTeX theorem parser used the Python library plasTeX to parse LaTeX documents, with a custom TeX logger
         and a pure-regex parser as fallbacks.

 3. If the dataset is a sample from a larger set, what was the sampling strategy?

       • Our dataset is not a sample. To the best of our knowledge, our dataset includes most mathematical theorems in
         arXiv. For the other sources, such as ProofWiki and the Stacks Project, we have included all theorems.

 4. Who was involved in the data collection process, and how were they compensated?

       • This paper’s co-authors were all involved in designing and implementing the pipeline to collect theorems. The
         mathematicians who created the validation set are volunteers.

 5. Over what timeframe was the data collected?

       • Data was collected over five months, from September 2025 to January 2026.

 6. Were any ethical review processes conducted?

       • Not applicable.


A.4. Preprocessing/cleaning/labeling
 1. Was any preprocessing/cleaning/labeling of the data done?

       • We preprocessed theorem bodies by removing unnecessary whitespace and expanding simple author-defined
         macros. We filtered out truncated or corrupted theorem bodies by employing several heuristics.

 2. Was the ”raw” data saved in addition to the preprocessed/cleaned/labeled data?

       • No.

 3. Is the software that was used to preprocess/clean/label the data available?

       • All code used to preprocess, clean, and label our data is available on our GitHub repo (Link).

                                                             14
                                                      Theorem Search

A.5. Uses
 1. Has the dataset been used for any tasks already?
       • The dataset has been used to create a semantic search engine, available on HuggingFace Spaces (Link).

 2. Is there a repository that links to any or all papers or systems that use the dataset?
       • Not applicable.

 3. What (other) tasks could the dataset be used for?
       • Our dataset of theorems is useful for mathematicians and for AI agents for automated theorem proving.

 4. Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that
    might impact future uses?
       • If authors of our theorem sources were to significantly change the content of the papers/textbooks/projects, our
         theorems would be outdated.

 5. Are there tasks for which the dataset should not be used?
       • No.

A.6. Distribution
 1. Will the dataset be distributed to third parties outside of the entity on behalf of which the dataset was created?

 2. How will the dataset be distributed?
       • The dataset is publicly available on Hugging Face at huggingface.co/datasets/uw-math-ai/theorem-search-dataset.
         We release only theorems from arXiv papers that use permissive licenses (CC BY and CC0), as well as theorems
         from the seven other sources (ProofWiki, Stacks Project, Open Logic Project, CRing Project, Stacks and Moduli,
         HoTT Book, and An Infinitely Large Napkin). Theorems from arXiv papers with non-permissive licenses are
         excluded from the public release.

 3. When will the dataset be distributed?
       • The dataset is already publicly available.

 4. Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable
    terms of use (ToU)?
       • The released dataset inherits the licenses of the source materials: CC BY or CC0 for arXiv papers, and the
         respective licenses of the other sources.

 5. Have any third parties imposed IP-based or other restrictions on the data associated with the instances?
       • No.

 6. Do any export controls or other regulatory restrictions apply to the dataset or individual instances?
       • No.

A.7. Maintenance
 1. Who will be supporting/hosting/maintaining the dataset?
       • The co-authors of this paper plan on continuing to build, host, and maintain this dataset.

 2. How can the owner/curator/manager of the dataset be contacted?
       • The co-authors of this paper own this dataset and can be contacted through Vasily Ilin at vilin@uw.edu.

 3. Will the dataset be updated?

                                                             15
                                                         Theorem Search

        • We plan on continuing to improve and grow the dataset in the future. For example, we plan on adding theorems
          from nLab and other open-source textbooks and projects.

  4. If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances (e.g.,
     were the individuals in question told that their data would be retained for a fixed period of time and then deleted)?
        • Not applicable.

  5. Will older versions of the dataset continue to be supported/hosted/maintained?
        • Older versions of the dataset will be available for download indefinitely on Hugging Face. However, all support
          and maintenance efforts will be focused on the latest version of the dataset.

  6. If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?
        • Others can suggest sources to add to the dataset by contacting Vasily Ilin at vilin@uw.edu.

B. User Feedback
In this section, we present feedback from two users on our theorem search engine.

B.1. Feedback One
We will first include a high-level description of the first feedback.
The user wanted to check for a specific reference, which we will call ”Theorem 1”, which the user knew was true. They
thought it follows from another result, which we call “result X,” a bit stronger than Theorem 1. It did, after a small lemma;
in other words, (result X + small lemma) implies what the user wanted. This shifted the user’s attention from finding a
reference for Theorem 1 to finding a reference for the small lemma. The user searched for the small lemma in our tool, and
the first result was a reference for a generalization of the small lemma.
A more detailed description now follows. We advise the non-mathematician reader to skip the next paragraph.
The user wanted to check that a smooth variety over a separably closed field has a k-point. The user thought it follows from
the étale local structure of smooth morphisms, which captured the correct idea but reduced the problem to showing that
k-points are dense in Ank . In essence, the étale local structure theorem translated the original problem of checking that a
smooth variety over a separably closed field has a k-point, to checking that for k separably closed, the set of k-points of An
is dense. The user entered the query “if k is separably closed, the set of k-points of An is dense in An .” The first result was
correct: Tag 056U in the Stacks Project.

B.2. Feedback Two
We now describe a second use case. As before, we first provide a high-level summary.
The user searched for a result known to experts but lacked a specific citable reference; we call this result “Theorem X.”
Many existing references point to similar results, but not exactly to Theorem X. The user queried our tool and found a result,
which we call “Theorem Y,” whose citation list directly referenced Theorem X. By using our tool, the user located the
desired theorem with fewer queries than traditional search methods, which had previously led only to indirect references.
A more detailed description follows. We advise the non-mathematician reader to skip the next two paragraphs.
The user needed a structure theorem for abelian p-Lie algebras, as defined by N. Jacobson. The user conjectured that these
algebras are classified analogously to finite abelian groups, provided the base field is algebraically closed. On MathOverflow,
an answer directed the user to a book that states the desired result. The book explained that the result follows from the
structure theory for modules over a PID, without providing a precise proof, and attributes the technique to Jacobson.
The book Infinite-Dimensional Lie Superalgebras (Bahturin et al., 2011) contains the result the user was looking for, labeled
the 3.2 nil-radical Theorem, attributed to Seligman, 1967. However, the user skimmed through the hundred or so pages of
Seligman’s reference several times without finding where the desired result is proved. When the user queried our tool with
“over an algebraically closed field, any abelian p-Lie algebra splits as a torus and a sum of nilpotent cyclic Lie algebras,” the
first result was the desired statement: Theorem 2.7 in (Usefi, 2009).

                                                                16
                                                       Theorem Search

C. Claude Experiment
We now report the experiment coupling Claude with our theorem search tool as a RAG system. This experiment tests
whether retrieval-augmented generation over our theorem corpus can correct LLM reasoning failures on a research-level
mathematical question. For discussion of this experiment in context, see Section 4.4.


   Query to Claude

   Consider the closure, in the KSBA moduli space, of the moduli space of pairs (S, aB + bF ) where S is an elliptic
   surface, B is a section of the projection S → C which gives the elliptic surface structure to S, the fibers of
   S → C are smooth or nodal, F are some fibers of S → C, and 0 < a, b < 1. The coefficients are chosen so
   that (S, aB + bF ) is KSBA-stable (so don’t need to reprove it). I would like to know if there exist a surface pair
   f : (X ′ , aB ′ + bF ′ ) → C ′ appearing on the boundary of the KSBA-compactification, not admitting a fibration over
   a nodal curve C ′ , with fibers of f that are of dimension one.



Without access to our tool, Claude answered incorrectly:


   Claude’s response without RAG (incorrect)

   No. Every surface pair appearing on the boundary of this KSBA compactification admits a fibration over a (possibly
   nodal) curve with one-dimensional fibers. The fibration structure cannot be lost in the limit.
   Why the fibration persists. The essential point is that the elliptic fibration structure is rigidly encoded in the
   boundary divisor, and this encoding survives in the KSBA limit.
   The fiber class remains nontrivial. In the interior, F is a fiber of S → C, so F 2 = 0 and (KS + aB + bF ) · F > 0
   (since KS · F = 0, B · F = 1, so this equals a > 0). In any flat limit, the limiting divisor F ′ retains F ′2 = 0 and
   (KX ′ + aB ′ + bF ′ ) · F ′ > 0. So F ′ is a nontrivial nef class with zero self-intersection, which defines a fibration
   f : X ′ → C ′.
   Stable reduction preserves the fibered structure. Given a one-parameter degeneration (St , ∆t ) → Ct , after finite
   base change and birational modification one extends the fibration to the central fiber. Each component of the limiting
   surface X ′ either:
      • maps surjectively onto a component of the nodal base curve C ′ with one-dimensional fibers, or

      • maps to a point (a “sprouted” component).
   But a component mapping to a point would be an entire surface sitting over a single point of C ′ , and the slc and
   ampleness conditions prevent this from occurring in the stable model: such a component would need K + ∆ to be
   positive on it, yet its gluing locus with the rest of X ′ is along a single fiber curve, and the combinatorics of the slc
   condition force it to be absorbed (contracted) when passing to the ample model of KX ′ + ∆′ .
   The section prevents collapse. The section B ′ (limit of the section B) meets each fiber in a point, ensuring the
   map X ′ → C ′ has generically one-dimensional fibers throughout. If any component lost the fibration structure,
   B ′ restricted to that component would be a curve not meeting the fiber class transversally, contradicting the
   deformation-invariant intersection number B · F = 1.
   Summary. The divisor data (aB +bF ) is sufficiently rigid that all KSBA-stable limits retain a fibration f : X ′ → C ′
   over a nodal curve C ′ , with all fibers of f being one-dimensional (curves). The boundary pairs differ from interior
   pairs in that C ′ may be nodal, X ′ may be reducible/non-normal (slc), and fibers may be more degenerate—but the
   fibration itself always exists.



When given access to our theorem database, Claude arrived at the correct answer:

                                                              17
                                                   Theorem Search

Claude’s response with RAG (correct)

Yes. Such boundary pairs exist; they are pseudoelliptic surfaces.

   • By Corollary 1.3 of (Ascher & Bejleri, 2017), the log canonical model of an irreducible slc elliptic surface
     (X → C, S + FA ) with KX + S + FA big is either the relative log canonical model (an elliptic surface over
     C), or a pseudoelliptic surface obtained by contracting the section S.

                                                           P is contracted if and only if (C, f∗ FA ) is not a
   • By Corollary 6.10 of (Ascher & Bejleri, 2017), the section
     weighted stable pointed curve; concretely: C ∼
                                                  = P1 with ai ≤ 2, or C has genus 1 with all ai = 0.
   • A pseudoelliptic surface admits no morphism to a curve with one-dimensional fibers: the section (which was
     isomorphic to the base) has been contracted to a point, so all former fibers pass through a single point and
     cannot be separated by a map to a curve.

   • By Proposition 3.22 of (Ascher et al., 2018), an explicit family is provided: for an elliptic surface over P1
     with deg L = 2 and A > 0, the log canonical model is a pseudoelliptic surface (section contracted), which is
     KSBA-stable and lies on the boundary.
   • By Corollary 6.7 of (Inchiostro, 2018), in a stable degeneration of elliptic surface pairs, the special fiber maps
     to a nodal curve C ′ , but pseudoelliptic components map to a point of C ′ , so f does not have all fibers of
     dimension one.
   • Properness of the moduli space of slc fibered surface pairs (Corollary 5.11 of (Ascher & Bejleri, 2016))
     guarantees these pseudoelliptic limits lie in the closure.




                                                          18
                                                          Theorem Search

D. Validation Set arXiv Categories
Table 6 shows the distribution of arXiv categories across the 65 unique papers in our validation set. Out of 32 math tags on
arXiv, the validation set covers 12.

Table 6. Distribution of arXiv categories in the validation set. Each cell reports counts as primary / all, where “primary” counts only
papers whose first-listed arXiv category matches the row, and “all” also includes cross-listed papers.


                                 arXiv Tag    Subject Area                      Theorems      Papers
                                 math.AG      Algebraic Geometry                  70 / 75      47 / 50
                                 math.CA      Classical Analysis and ODEs         26 / 36      9 / 12
                                 math.AP      Analysis of PDEs                    17 / 23       4/7
                                 math.FA      Functional Analysis                  – / 12       –/4
                                 math.MG      Metric Geometry                       7/9         2/3
                                 math.DG      Differential Geometry                 –/9         –/2
                                 math.NT      Number Theory                         2/7         1/4
                                 math.CT      Category Theory                       –/4         –/1
                                 math.CO      Combinatorics                         1/3         1/2
                                 math.RT      Representation Theory                 –/3         –/1
                                 nlin.SI      Exactly Solvable and Int. Sys.        2/2         1/1
                                 math.CV      Complex Variables                     –/1         –/1
                                 math.SG      Symplectic Geometry                   –/1         –/1
                                 hep-th       High Energy Physics – Theory          –/1         –/1




                                                                  19
                                                          Theorem Search

Table 7. Distribution of arXiv categories in the whole dataset. Each cell reports counts as primary / all, where “primary” counts only
papers whose first-listed arXiv category matches the row, and “all” also includes cross-listed papers.

      arXiv Tag                Subject Area                                                  Theorems               Papers
      math.CO                  Combinatorics                                             727514 / 1107979       46929 / 68561
      math.AG                  Algebraic Geometry                                        761230 / 1097654       36350 / 51497
      math.AP                  Analysis of PDEs                                          791867 / 1018652       51176 / 64735
      math.PR                  Probability                                                606057 / 868961       38793 / 55971
      math.NT                  Number Theory                                              550466 / 752812       32235 / 42070
      math.DG                  Differential Geometry                                      499694 / 721447       28901 / 40763
      math.RT                  Representation Theory                                      353605 / 618985       15219 / 26364
      math.DS                  Dynamical Systems                                          374124 / 574125       21561 / 33646
      math.FA                  Functional Analysis                                        333709 / 544882       20193 / 31825
      math-ph                  Mathematical Physics                                       127036 / 533783        8604 / 32239
      math.GR                  Group Theory                                               303021 / 488750       14269 / 22702
      math.OC                  Optimization and Control                                   298096 / 470086       28546 / 43871
      math.GT                  Geometric Topology                                         277653 / 441500       15348 / 22650
      math.RA                  Rings and Algebras                                         202501 / 352448       10783 / 17650
      math.AT                  Algebraic Topology                                         200267 / 348076        8886 / 15601
      cs.LG                    Machine Learning                                           150507 / 323831       16346 / 33522
      math.QA                  Quantum Algebra                                            171100 / 322466        8258 / 15419
      math.CA                  Classical Analysis and ODEs                               194189 / 309145        14237 / 21275
      math.NA                  Numerical Analysis                                         209943 / 285427       23450 / 30763
      math.LO                  Logic                                                      206528 / 285351        9324 / 12952
      stat.ML                  Machine Learning                                            95327 / 281203       10123 / 28137
      math.CV                  Complex Variables                                          148649 / 278361       10203 / 16899
      math.OA                  Operator Algebras                                          170685 / 267922        8033 / 12677
      math.ST                  Statistics Theory                                          153124 / 260628       12979 / 21634
      math.AC                  Commutative Algebra                                        158613 / 253612        8762 / 13462
      math.MG                  Metric Geometry                                            100465 / 207104        6022 / 11402
      math.CT                  Category Theory                                             89204 / 202660         4024 / 8610
      math.SG                  Symplectic Geometry                                        110807 / 191221         4864 / 8954
      math.SP                  Spectral Theory                                             73394 / 162664         4666 / 9798
      math.KT                  K-Theory and Homology                                       57905 / 145433         2441 / 5961
      cs.DM                    Discrete Mathematics                                        35079 / 134746         2246 / 8829
      cs.CC                    Computational Complexity                                    65534 / 127305         4016 / 7808
      cs.DS                    Data Structures and Algorithms                             53579 / 121709         3269 / 7629
      stat.ME                  Methodology                                                 74267 / 117914       10991 / 15438
      cs.IT                    Information Theory                                          42758 / 109029         3422 / 8646
      hep-th                   High Energy Physics – Theory                                17512 / 108924         1753 / 6809
      math.GN                  General Topology                                            60256 / 102259         3223 / 5212
      cs.AI                    Artificial Intelligence                                      24644 / 82598        3072 / 10378
      cs.LO                    Logic in Computer Science                                    30251 / 68125         1772 / 3945
      cs.CG                    Computational Geometry                                       33920 / 59488         2904 / 4755
      quant-ph                 Quantum Physics                                              25484 / 58911         1947 / 4332
      eess.SY                  Systems and Control                                          16997 / 52647         2549 / 7239
      gr-qc                    General Relativity and Quantum Cosmology                    17771 / 43279         1125 / 2721
      cs.CR                    Cryptography and Security                                   16687 / 40367         2204 / 4419
      cs.GT                    Computer Science and Game Theory                            17909 / 36310         1504 / 3096
      nlin.SI                  Exactly Solvable and Integrable Systems                      8253 / 32897          744 / 2414
      math.GM                  General Mathematics                                          27194 / 29265         2224 / 2380
      stat.CO                  Computation                                                   9804 / 28120         1515 / 3830
      econ.TH                  Theoretical Economics                                        19057 / 26467         1582 / 2167
                                                                                                        Continued on next page

                                                                 20
                                             Theorem Search

Table 7 (continued)
arXiv Tag             Subject Area                                       Theorems            Papers
cond-mat.stat-mech    Statistical Mechanics                              2321 / 24482      287 / 1834
q-fin.MF              Mathematical Finance                              14999 / 24160     1273 / 1960
econ.EM               Econometrics                                      14189 / 22632     1479 / 2234
stat.AP               Applications                                       5524 / 20294     1298 / 3778
cs.FL                 Formal Languages and Automata Theory              6655 / 18854      439 / 1192
eess.SP               Signal Processing                                 10708 / 18805     2449 / 3485
q-bio.PE              Populations and Evolution                         7196 / 17583      740 / 1743
cs.DC                 Distributed, Parallel, and Cluster Computing      3689 / 16269      371 / 1669
cs.SC                 Symbolic Computation                              5435 / 14312       395 / 1113
cs.SI                 Social and Information Networks                   3772 / 13795      516 / 1550
cs.CV                 Computer Vision                                    3247 / 12628      703 / 2169
cs.MA                 Multiagent Systems                                 1522 / 12284      208 / 1386
physics.flu-dyn       Fluid Dynamics                                     1836 / 11450      393 / 1335
math.HO               History and Overview                               5067 / 10829       427 / 815
q-fin.CP              Computational Finance                               3495 / 8114       465 / 928
nlin.CD               Chaotic Dynamics                                    1715 / 7802       214 / 834
cs.NE                 Neural and Evolutionary Computing                  2010 / 7620       235 / 884
q-fin.RM              Risk Management                                     2840 / 7611       239 / 677
q-fin.PR              Pricing of Securities                               3634 / 7537       357 / 710
cs.RO                 Robotics                                            1972 / 7091      432 / 1192
q-fin.PM              Portfolio Management                                3474 / 6878       296 / 626
cond-mat.dis-nn       Disordered Systems and Neural Networks              565 / 6180        67 / 504
physics.comp-ph       Computational Physics                               1202 / 6038      313 / 1149
econ.GN               General Economics                                   3402 / 5953       446 / 695
nlin.PS               Pattern Formation and Solitons                     1042 / 5864       121 / 518
physics.soc-ph        Physics and Society                                 1052 / 5639       211 / 819
q-bio.QM              Quantitative Methods                                1417 / 5506       263 / 775
cs.CL                 Computation and Language                            1381 / 5300       277 / 767
cs.NI                 Networking and Internet Architecture               1565 / 5000       222 / 664
q-bio.MN              Molecular Networks                                  1339 / 4549       134 / 408
cs.CE                 Computational Engineering, Finance, and Science    1425 / 4295       280 / 731
cond-mat.str-el       Strongly Correlated Electrons                       580 / 4123        55 / 275
cs.DB                 Databases                                           1521 / 4043       144 / 415
physics.data-an       Data Analysis, Statistics and Probability           583 / 3747       111 / 541
cs.PL                 Programming Languages                               1120 / 3515        83 / 281
physics.class-ph      Classical Physics                                   1082 / 3288       178 / 459
q-fin.ST              Statistical Finance                                 1317 / 3221       197 / 421
nlin.AO               Adaptation and Self-Organizing Systems              558 / 3204        79 / 377
q-bio.NC              Neurons and Cognition                                768 / 3054       102 / 378
cs.PF                 Performance                                          973 / 3019       107 / 320
cond-mat.mes-hall     Mesoscale and Nanoscale Physics                      231 / 2963        15 / 209
cs.CY                 Computers and Society                                405 / 2949        69 / 415
cond-mat.mtrl-sci     Materials Science                                    164 / 2924        29 / 271
q-fin.TR              Trading and Market Microstructure                  1200 / 2919       107 / 269
stat.OT               Other Statistics                                     804 / 2794       111 / 339
cs.IR                 Information Retrieval                                564 / 2488       108 / 387
physics.optics        Optics                                               299 / 2033        40 / 211
nlin.CG               Cellular Automata and Lattice Gases                 229 / 1860        22 / 136
physics.plasm-ph      Plasma Physics                                       265 / 1731        42 / 187
q-fin.GN              General Finance                                      391 / 1730        44 / 156
                                                                                  Continued on next page


                                                   21
                                                  Theorem Search

     Table 7 (continued)
     arXiv Tag             Subject Area                                         Theorems            Papers
     cond-mat.soft         Soft Condensed Matter                                 224 / 1594         39 / 168
     cond-mat.quant-gas    Quantum Gases                                          49 / 1502           6 / 94
     cs.MS                 Mathematical Software                                 174 / 1487         55 / 281
     physics.chem-ph       Chemical Physics                                      188 / 1353         32 / 164
     eess.IV               Image and Video Processing                           349 / 1350         74 / 282
     physics.bio-ph        Biological Physics                                     96 / 1333         25 / 172
     cs.GR                 Graphics                                              254 / 1289         44 / 189
     physics.geo-ph        Geophysics                                             79 / 1258         22 / 139
     physics.ao-ph         Atmospheric and Oceanic Physics                       113 / 1166         28 / 166
     physics.gen-ph        General Physics                                      1010 / 1088        188 / 206
     hep-ph                High Energy Physics – Phenomenology                    31 / 957           6 / 93
     cs.ET                 Emerging Technologies                                  194 / 876         27 / 102
     hep-lat               High Energy Physics – Lattice                           42 / 831           9 / 72
     q-bio.GN              Genomics                                               179 / 811         27 / 125
     cs.HC                 Human-Computer Interaction                             128 / 760        20 / 121
     q-bio.BM              Biomolecules                                           176 / 701          24 / 92
     physics.med-ph        Medical Physics                                        117 / 619          24 / 94
     astro-ph.IM           Instrumentation and Methods for Astrophysics           64 / 586          15 / 83
     q-bio.CB              Cell Behavior                                           99 / 555          17 / 83
     astro-ph.CO           Cosmology and Nongalactic Astrophysics                 82 / 554           4 / 54
     q-bio.TO              Tissues and Organs                                      64 / 482          12 / 73
     cond-mat.other        Other Condensed Matter                                  19 / 441           2 / 39
     cond-mat.supr-con     Superconductivity                                       22 / 434           3 / 26
     physics.app-ph        Applied Physics                                         20 / 431           6 / 64
     cs.SE                 Software Engineering                                   147 / 406          30 / 80
     cond-mat              Condensed Matter                                        83 / 383           9 / 42
     physics.hist-ph       History and Philosophy of Physics                      116 / 380          23 / 54
     cs.SD                 Sound                                                   95 / 373          28 / 74
     astro-ph.EP           Earth and Planetary Astrophysics                      121 / 366          23 / 55
     physics.atom-ph       Atomic Physics                                           4 / 316           1 / 24
     cs.AR                 Hardware Architecture                                   37 / 314           6 / 36
     eess.AS               Audio and Speech Processing                              7 / 299           3 / 66
     astro-ph              Astrophysics                                            38 / 272           4 / 30
     q-bio.SC              Subcellular Processes                                   61 / 257          10 / 33
     cs.OH                 Other Computer Science                                  22 / 246           3 / 22
     nucl-th               Nuclear Theory                                           2 / 232           2 / 24
     cs.MM                 Multimedia                                              18 / 190           7 / 46
     astro-ph.SR           Solar and Stellar Astrophysics                          33 / 150           7 / 26
     cs.DL                 Digital Libraries                                       29 / 104          11 / 21
     physics.acc-ph        Accelerator Physics                                     12 / 104           3 / 16
     physics.space-ph      Space Physics                                             6 / 82           2 / 12
     hep-ex                High Energy Physics – Experiment                         1 / 39            1 / 10
     q-bio.OT              Other Quantitative Biology                                4 / 36            1/8
     cs.OS                 Operating Systems                                        16 / 25            5/7
     physics.pop-ph        Popular Physics                                           3 / 17            2/5
     physics.ins-det       Instrumentation and Detectors                             1 / 15            1/4


E. More Experiments
We ran our experiments with a larger set of embedders, including Multilingual-E5-Large-Instruct (Wang et al., 2024),
zbMath-Bert (Steinfeldt & Mihaljević, 2024), and KaLM-Embedding-V2.5 (Zhao et al., 2025; Hu et al., 2025).

                                                        22
                                                   Theorem Search




  Table 8. Extended results comparing context window size in retrieval performance. Embedded without task instructions.



M ODEL                                                    H IT @1        H IT @10          H IT @20         MRR@20
                                                   B ODY O NLY
ZB M ATH -B ERT 0.3B                                       0.053           0.158             0.237             0.086
G EMMA 0.3B                                                0.184           0.474             0.539             0.290
Q WEN 3 0.6B                                               0.224           0.461             0.513             0.299
Q WEN 3 8B                                                 0.224           0.553             0.632             0.313
K A LM-E MBEDDING -V2.5                                    0.131           0.355             0.434             0.203
M ULTILINGUAL -E5-L ARGE -I NSTRUCT                        0.171           0.395             0.500             0.237
                                                  W / A BSTRACT

ZB M ATH -B ERT 0.3B                                       0.092           0.184             0.237             0.113
G EMMA 0.3B                                                0.303           0.539             0.566             0.376
Q WEN 3 0.6B                                               0.224           0.487             0.526             0.297
Q WEN 3 8B                                                 0.250           0.553             0.618             0.332
K A LM-E MBEDDING -V2.5                                    0.197           0.474             0.513             0.272
M ULTILINGUAL -E5-L ARGE -I NSTRUCT                        0.197           0.421             0.553             0.283
                                               W / F IRST S ECTION

ZB M ATH -B ERT 0.3B                                       0.092           0.184             0.237             0.122
G EMMA 0.3B                                                0.237           0.500             0.566             0.321
Q WEN 3 0.6B                                               0.263           0.526             0.645             0.352
Q WEN 3 8B                                                 0.211           0.605             0.645             0.343
K A LM-E MBEDDING -V2.5                                    0.184           0.447             0.474             0.272
M ULTILINGUAL -E5-L ARGE -I NSTRUCT                        0.224           0.474             0.539             0.304




                                                           23
                                                     Theorem Search




Table 9. Extended results comparing LLM slogans in retrieval performance. Embedded without task instructions. Body+Abstract.



M ODEL                                                      H IT @1        H IT @10         H IT @20        MRR@20
                                                  D EEPSEEK V3.1
ZB M ATH -B ERT 0.3B                                         0.092           0.184            0.237             0.113
G EMMA 0.3B                                                  0.303           0.539            0.566             0.376
Q WEN 3 0.6B                                                 0.224           0.487            0.526             0.297
Q WEN 3 8B                                                   0.250           0.553            0.618             0.332
K A LM-E MBEDDING -V2.5                                      0.197           0.474            0.513             0.272
M ULTILINGUAL -E5-L ARGE -I NSTRUCT                          0.197           0.421            0.553             0.283
                                                    D EEPSEEK R1
ZB M ATH -B ERT 0.3B                                         0.000           0.079            0.105             0.014
G EMMA 0.3B                                                  0.158           0.421            0.474             0.228
Q WEN 3 0.6B                                                 0.132           0.316            0.408             0.199
Q WEN 3 8B                                                   0.118           0.355            0.461             0.195
K A LM-E MBEDDING -V2.5                                      0.066           0.289            0.461             0.140
M ULTILINGUAL -E5-L ARGE -I NSTRUCT                          0.066           0.250            0.355             0.111
                                                   G EMINI 3 P RO
ZB M ATH -B ERT 0.3B                                         0.053           0.171            0.237             0.092
G EMMA 0.3B                                                  0.250           0.553            0.632             0.348
Q WEN 3 0.6B                                                 0.211           0.487            0.539             0.290
Q WEN 3 8B                                                   0.237           0.566            0.684             0.348
K A LM-E MBEDDING -V2.5                                      0.197           0.434            0.553             0.265
M ULTILINGUAL -E5-L ARGE -I NSTRUCT                          0.197           0.513            0.579             0.297
                                                C LAUDE O PUS 4.5
ZB M ATH -B ERT 0.3B                                         0.053           0.184            0.211             0.087
G EMMA 0.3B                                                  0.303           0.553            0.579             0.387
Q WEN 3 0.6B                                                 0.224           0.539            0.605             0.325
Q WEN 3 8B                                                   0.263           0.632            0.737             0.394
K A LM-E MBEDDING -V2.5                                      0.197           0.421            0.526             0.271
M ULTILINGUAL -E5-L ARGE -I NSTRUCT                          0.224           0.526            0.592             0.322




                                                            24
                                                     Theorem Search

F. Prompts
In this section we list the prompts used during slogan generation and retrieval, shown in Tables 10, 11, and 12.

                                          Table 10. Task instructions for embedders


             S IDE            P ROMPT
             T HEOREM         Instruct: Represent the given math statement for retrieving
                              related statement by natural language query.\nQuery:
             U SER Q UERY     Instruct: Given a math search query, retrieve theorems
                              mathematically equivalent to the query.\nQuery:


                                                  Table 11. Slogan prompts


 Context                    Prompt
 Body Only                  You generate summaries of math theorems based on theorem body. Summaries are
                            accurate and at most four sentences. Summaries are plain ASCII sentences with
                            no Unicode. Describe the result without referencing it as ’this theorem’ or
                            similar. Avoid LaTeX and mathematical symbols; use words instead. Output only
                            the final summary sentences, with no reasoning, explanations, or commentary. Do
                            not restate the prompt, input fields, or instructions. Do not include proof
                            steps, motivation, or background discussion.
 Body+Abstract              You generate summaries of math theorems based on theorem body. You also
                            consider paper summary in your summaries. Summaries are accurate and at most
                            four sentences. Summaries are plain ASCII sentences with no Unicode. Describe
                            the result without referencing it as ’this theorem’ or similar. Avoid LaTeX
                            and mathematical symbols; use words instead. Output only the final summary
                            sentences, with no reasoning, explanations, or commentary. Do not restate the
                            prompt, input fields, or instructions. Do not include proof steps, motivation,
                            or background discussion.
 Body+Introduction          You generate summaries of math theorems based on theorem body. You also
                            consider paper summary and the first section of the paper in your summaries.
                            Summaries are accurate and at most four sentences. Summaries are plain ASCII
                            sentences with no Unicode. Describe the result without referencing it as ’this
                            theorem’ or similar. Avoid LaTeX and mathematical symbols; use words instead.
                            Output only the final summary sentences, with no reasoning, explanations, or
                            commentary. Do not restate the prompt, input fields, or instructions. Do not
                            include proof steps, motivation, or background discussion.




                                                             25
                                          Theorem Search




                              Table 12. Retrieval prompts for baselines.


C ONTEXT         P ROMPT
GPT-5.2          {
                    ‘‘role’’: ‘‘system’’,
                    ‘‘content’’: (
                       ‘‘You are an assistant that MUST answer immediately.\n’’
                       ‘‘Do NOT ask the user questions or request permission.\n’’
                       ‘‘Use web search as needed, including opening the latest arXiv PDF(s) to
                 verify statement numbering.\n’’
                       ‘‘If exact numbering cannot be verified for some item, still include it but
                 mark number as ’UNVERIFIED’.\n’’
                       ‘‘Return ONLY the final list|no preamble.’’
                    ),
                 },
                 {
                    ‘‘role’’: ‘‘user’’,
                    ‘‘content’’: (
                       ‘‘Return a list of the top 20 most relevant math statements to the query
                 below.\n’’
                       ‘‘Constraints:\n’’
                       ‘‘- Statements must be from arXiv papers.\n’’
                       ‘‘- For each item include: (1) arXiv id, (2) version used (e.g. v3), ’’
                       ‘‘(3) statement type+number exactly as in that arXiv version (e.g. Theorem
                 1.2 / Lemma 3.4), ’’
                       ‘‘(4) section name/number, (5) statement title/short descriptor, (6) 1{2
                 sentence relevance note.\n’’
                       ‘‘- Use the most recent arXiv version available.\n’’
                       ‘‘Query:\n’’
                       f‘‘{row.query}’’
                    )
                 }
G EMINI 3 P RO   SYSTEM INSTRUCTION = (
                       ‘‘You are an assistant that MUST answer immediately.\n’’
                       ‘‘Do NOT ask the user questions or request permission.\n’’
                       ‘‘Use Google Search grounding as needed, including opening the latest arXiv
                 PDF(s) to verify statement numbering.\n’’
                       ‘‘If exact numbering cannot be verified for some item, still include it but
                 mark number as ’UNVERIFIED’.\n’’
                       ‘‘Return ONLY the final list|no preamble.’’
                 )
                 user prompt = (
                     ‘‘Return a list of the top 20 most relevant math statements to the query
                 below.\n’’
                     ‘‘Constraints:\n’’
                     ‘‘- Statements must be from arXiv papers.\n’’
                     ‘‘- For each item include: (1) arXiv id, (2) version used (e.g. v3), ’’
                     ‘‘(3) statement type+number exactly as in that arXiv version (e.g. Theorem
                 1.2 / Lemma 3.4), ’’
                     ‘‘(4) section name/number, (5) statement title/short descriptor, (6) 1{2
                 sentence relevance note.\n’’
                     ‘‘- Use the most recent arXiv version available.\n’’
                     ‘‘Query:\n’’
                     f‘‘{row.query}’’
                 )




                                                 26
