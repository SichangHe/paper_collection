                                                 The Pile: An 800GB Dataset of Diverse Text for Language Modeling
                                                    Leo Gao                 Stella Biderman                  Sid Black               Laurence Golding

                                             Travis Hoppe                    Charles Foster                Jason Phang                   Horace He

                                                 Anish Thite                Noa Nabeshima                 Shawn Presser                Connor Leahy

                                                                                          EleutherAI
                                                                                    contact@eleuther.ai

                                                                  Abstract                             versity leads to better downstream generalization
                                                                                                       capability (Rosset, 2019). Additionally, large-scale
                                                 Recent work has demonstrated that increased
                                                 training dataset diversity improves general           language models have been shown to effectively
                                                 cross-domain knowledge and downstream gen-            acquire knowledge in a novel domain with only
arXiv:2101.00027v1 [cs.CL] 31 Dec 2020




                                                 eralization capability for large-scale language       relatively small amounts of training data from that
                                                 models. With this in mind, we present the             domain (Rosset, 2019; Brown et al., 2020; Carlini
                                                 Pile: an 825 GiB English text corpus tar-             et al., 2020). These results suggest that by mix-
                                                 geted at training large-scale language mod-           ing together a large number of smaller, high qual-
                                                 els. The Pile is constructed from 22 diverse          ity, diverse datasets, we can improve the general
                                                 high-quality subsets—both existing and newly
                                                 constructed—many of which derive from aca-
                                                                                                       cross-domain knowledge and downstream general-
                                                 demic or professional sources. Our evalua-            ization capabilities of the model compared to mod-
                                                 tion of the untuned performance of GPT-2 and          els trained on only a handful of data sources.
                                                 GPT-3 on the Pile shows that these models
                                                 struggle on many of its components, such as           To address this need, we introduce the Pile: a
                                                 academic writing. Conversely, models trained          825.18 GiB English text dataset designed for train-
                                                 on the Pile improve significantly over both           ing large scale language models. The Pile is com-
                                                 Raw CC and CC-100 on all components of the            posed of 22 diverse and high-quality datasets, in-
                                                 Pile, while improving performance on down-            cluding both established natural language process-
                                                 stream evaluations. Through an in-depth ex-
                                                                                                       ing datasets and several newly introduced ones.
                                                 ploratory analysis, we document potentially
                                                 concerning aspects of the data for prospective        In addition to its utility in training large language
                                                 users. We make publicly available the code            models, the Pile can also serve as a broad-coverage
                                                 used in its construction.1                            benchmark for cross-domain knowledge and gener-
                                                                                                       alization ability of language models.
                                         1       Introduction
                                                                                                       We introduce new datasets derived from the fol-
                                         Recent breakthroughs in general-purpose language              lowing sources: PubMed Central, ArXiv, GitHub,
                                         modeling have demonstrated the effectiveness of               the FreeLaw Project, Stack Exchange, the US
                                         training massive models on large text corpora for             Patent and Trademark Office, PubMed, Ubuntu
                                         downstream applications (Radford et al., 2019;                IRC, HackerNews, YouTube, PhilPapers, and NIH
                                         Shoeybi et al., 2019; Raffel et al., 2019; Rosset,            ExPorter. We also introduce OpenWebText2 and
                                         2019; Brown et al., 2020; Lepikhin et al., 2020). As          BookCorpus2, which are extensions of the original
                                         the field continues to scale up language model train-         OpenWebText (Gokaslan and Cohen, 2019) and
                                         ing, the demand for high-quality massive text data            BookCorpus (Zhu et al., 2015; Kobayashi, 2018)
                                         will continue to grow (Kaplan et al., 2020).                  datasets, respectively.
                                         The growing need for data in language modeling
                                                                                                       In addition, we incorporate several existing high-
                                         has caused most existing large-scale language mod-
                                                                                                       quality datasets: Books3 (Presser, 2020), Project
                                         els to turn to the Common Crawl for most or all of
                                                                                                       Gutenberg (PG-19) (Rae et al., 2019), Open-
                                         their data (Brown et al., 2020; Raffel et al., 2019).
                                                                                                       Subtitles (Tiedemann, 2016), English Wikipedia,
                                         While training on the Common Crawl has been
                                                                                                       DM Mathematics (Saxton et al., 2019), EuroParl
                                         effective, recent work has shown that dataset di-
                                                                                                       (Koehn, 2005), and the Enron Emails corpus (Klimt
                                             1
                                                 https://pile.eleuther.ai/                             and Yang, 2004). To supplement these, we also in-

                                                                                                   1
                           Figure 1: Treemap of Pile components by effective size.


troduce a new filtered subset of Common Crawl,              1.1    Contributions
Pile-CC, with improved extraction quality.                  The core contributions of this paper are:
Through our analyses, we confirm that the Pile is               1. The introduction of a 825.18 GiB english-
significantly distinct from pure Common Crawl                      language dataset for language modeling com-
data. Additionally, our evaluations show that the                  bining 22 diverse sources.
existing GPT-2 and GPT-3 models perform poorly
on many components of the Pile, and that models                 2. The introduction of 14 new language model-
trained on the Pile significantly outperform both                  ing datasets, which we expect to be of inde-
raw and filtered Common Crawl models. To com-                      pendent interest to researchers.
plement the performance evaluations, we also per-               3. Evaluations demonstrating significant im-
form an exploratory analysis of the text within the                provements across many domains by GPT-2-
Pile to provide a detailed picture of the data. We                 sized models trained on this new dataset, com-
hope that our extensive documentation of the con-                  pared to training on CC-100 and raw Common
struction and characteristics of the Pile will help                Crawl.
researchers make informed decisions about poten-
tial downstream applications.                                   4. The investigation and documentation of this
                                                                   dataset, which we hope will better inform re-
Finally, we make publicly available the preprocess-                searchers about how to use it as well as moti-
ing code for the constituent datasets of the Pile and              vate them to undertake similar investigations
the code for constructing alternative versions2 . In               of their own data.
the interest of reproducibility, we also document
all processing performed on each dataset (and the           2     The Pile Datasets
Pile as a whole) in as much detail as possible. For
further details about the processing of each dataset,       The Pile is composed of 22 constituent sub-datasets,
see Section 2 and Appendix C.                               as shown in Table 1. Following Brown et al. (2020),
                                                            we increase the weights of higher quality compo-
  2
    https://github.com/EleutherAI/                          nents, with certain high-quality datasets such as
the-pile                                                    Wikipedia being seen up to 3 times (“epochs”) for

                                                        2
  Component                   Raw Size      Weight     Epochs       Effective Size   Mean Document Size
  Pile-CC                   227.12 GiB      18.11%           1.0       227.12 GiB                  4.33 KiB
  PubMed Central             90.27 GiB      14.40%           2.0       180.55 GiB                 30.55 KiB
  Books3†                   100.96 GiB      12.07%           1.5       151.44 GiB                538.36 KiB
  OpenWebText2               62.77 GiB      10.01%           2.0       125.54 GiB                  3.85 KiB
  ArXiv                      56.21 GiB       8.96%           2.0       112.42 GiB                 46.61 KiB
  Github                     95.16 GiB       7.59%           1.0        95.16 GiB                  5.25 KiB
  FreeLaw                    51.15 GiB       6.12%           1.5        76.73 GiB                 15.06 KiB
  Stack Exchange             32.20 GiB       5.13%           2.0        64.39 GiB                  2.16 KiB
  USPTO Backgrounds          22.90 GiB       3.65%           2.0        45.81 GiB                  4.08 KiB
  PubMed Abstracts           19.26 GiB       3.07%           2.0        38.53 GiB                  1.30 KiB
  Gutenberg (PG-19)†         10.88 GiB       2.17%           2.5        27.19 GiB                398.73 KiB
  OpenSubtitles†             12.98 GiB       1.55%           1.5        19.47 GiB                 30.48 KiB
  Wikipedia (en)†             6.38 GiB       1.53%           3.0        19.13 GiB                  1.11 KiB
  DM Mathematics†             7.75 GiB       1.24%           2.0        15.49 GiB                  8.00 KiB
  Ubuntu IRC                  5.52 GiB       0.88%           2.0        11.03 GiB                545.48 KiB
  BookCorpus2                 6.30 GiB       0.75%           1.5         9.45 GiB                369.87 KiB
  EuroParl†                   4.59 GiB       0.73%           2.0         9.17 GiB                 68.87 KiB
  HackerNews                  3.90 GiB       0.62%           2.0         7.80 GiB                  4.92 KiB
  YoutubeSubtitles            3.73 GiB       0.60%           2.0         7.47 GiB                 22.55 KiB
  PhilPapers                  2.38 GiB       0.38%           2.0         4.76 GiB                 73.37 KiB
  NIH ExPorter                1.89 GiB       0.30%           2.0         3.79 GiB                  2.11 KiB
  Enron Emails†               0.88 GiB       0.14%           2.0         1.76 GiB                  1.78 KiB
  The Pile                  825.18 GiB                               1254.20 GiB                   5.91 KiB

Table 1: Overview of datasets in the Pile before creating the held out sets. Raw Size is the size before any
up- or down-sampling. Weight is the percentage of bytes in the final dataset occupied by each dataset. Epochs
is the number of passes over each constituent dataset during a full epoch over the Pile. Effective Size is the
approximate number of bytes in the Pile occupied by each dataset. Datasets marked with a † are used with minimal
preprocessing from prior work.


each full epoch over the Pile. Detailed information        2.2     PubMed Central
about the construction of each dataset is available
                                                           PubMed Central (PMC) is a subset of the PubMed
in Appendix C.
                                                           online repository for biomedical articles run by
                                                           the United States of America’s National Center
2.1   Pile-CC                                              for Biotechnology Information (NCBI), providing
                                                           open, full-text access to nearly five million publi-
Common Crawl is a collection of website crawls
                                                           cations. Most publications indexed by PMC are
from 2008 onwards, including raw web pages,
                                                           recent, and their inclusion is mandated for all NIH
metadata and text extractions. Due to the raw na-
                                                           funded research starting from 2008 by the NIH
ture of the dataset, Common Crawl has the ad-
                                                           Public Access Policy. We included PMC in the
vantage of including text from diverse domains,
                                                           hopes that it will benefit potential downstream ap-
but at the cost of varying quality data. Due to
                                                           plications to the medical domain.
this, use of Common Crawl typically necessi-
tates well-designed extraction and filtering. Our
                                                           2.3     Books3
Common Crawl-based dataset, Pile-CC, uses jus-
Text (Endrédy and Novák, 2013) on Web Archive              Books3 is a dataset of books derived from a copy
files (raw HTTP responses including page HTML)             of the contents of the Bibliotik private tracker
for extraction, which yields higher quality output         made available by Shawn Presser (Presser, 2020).
than directly using the WET files (extracted plain-        Bibliotik consists of a mix of fiction and nonfic-
text).                                                     tion books and is almost an order of magnitude

                                                       3
larger than our next largest book dataset (BookCor-         and other metadata, we focused specifically on
pus2).We included Bibliotik because books are in-           court opinions due to an abundance of full-text
valuable for long-range context modeling research           entries. This data is entirely within the public do-
and coherent storytelling.                                  main.
2.4     OpenWebText2                                        2.8    Stack Exchange
OpenWebText2 (OWT2) is a generalized web
                                                            The Stack Exchange Data Dump4 contains an
scrape dataset inspired by WebText (Radford et al.,
                                                            anonymized set of all user-contributed content on
2019) and OpenWebTextCorpus (Gokaslan and Co-
                                                            the Stack Exchange network, a popular collection
hen, 2019). Similar to the original WebText, we
                                                            of websites centered around user-contributed ques-
use net upvotes on Reddit submissions as a proxy
                                                            tions and answers. It is one of the largest publicly
for outgoing link quality. OpenWebText2 includes
                                                            available repositories of question-answer pairs, and
more recent content from Reddit submissions up
                                                            covers a wide range of subjects—from program-
until 2020, content from multiple languages, docu-
                                                            ming, to gardening, to Buddhism. We included
ment metadata, multiple dataset versions, and open
                                                            Stack Exchange in the hopes that it will improve
source replication code. We included OWT2 as a
                                                            the question answering capabilities of downstream
high quality general purpose dataset.
                                                            models on diverse domains.
2.5     ArXiv
                                                            2.9    USPTO Backgrounds
ArXiv is a preprint server for research papers that
has operated since 1991. As shown in fig. 10, arXiv         USPTO Backgrounds is a dataset of background
papers are predominantly in the fields of Math,             sections from patents granted by the United States
Computer Science, and Physics. We included arXiv            Patent and Trademark Office, derived from its pub-
in the hopes that it will be a source of high qual-         lished bulk archives5 . A typical patent background
ity text and math knowledge, and benefit potential          lays out the general context of the invention, gives
downstream applications to research in these ar-            an overview of the technical field, and sets up the
eas. ArXiv papers are written in LaTeX, a common            framing of the problem space. We included USPTO
typesetting language for mathematics, computer              Backgrounds because it contains a large volume of
science, physics, and some adjacent fields. Train-          technical writing on applied subjects, aimed at a
ing a language model to be able to generate papers          non-technical audience.
written in LaTeX could be a huge boon to the re-
search community.                                           2.10    Wikipedia (English)

2.6     GitHub                                              Wikipedia is a standard source of high-quality text
                                                            for language modeling. In addition to being a
GitHub is a large corpus of open-source code repos-
                                                            source of high quality, clean English text, it is also
itories. Motivated by the ability of GPT-3 (Brown
                                                            valuable as it is written in expository prose, and
et al., 2020) to generate plausible code completions
                                                            spans many domains.
despite its training data not containing any explic-
itly gathered code datasets, we included GitHub in          2.11    PubMed Abstracts
the hopes that it would enable better downstream
performance on code-related tasks.                          PubMed Abstracts consists of the abstracts from 30
                                                            million publications in PubMed, the online repos-
2.7     FreeLaw                                             itory for biomedical articles run by the National
The Free Law Project is a US-registered non-profit          Library of Medicine. While the PMC (see Section
that provides access to and analytical tools for aca-       2.2) provides full-text access, the subset of cover-
demic studies in the legal realm. CourtListener,3           age is significantly limited and biased towards re-
part of the Free Law Project, provides bulk down-           cent publications. PubMed also incorporates MED-
loads for millions of legal opinions from federal           LINE, which expands the coverage of biomedical
and state courts. While the full dataset provides           abstracts from 1946 to present day.
multiple modalities of legal proceedings, includ-
                                                               4
ing dockets, bibliographic information on judges,               https://archive.org/details/
                                                            stackexchange
   3                                                          5
       https://www.courtlistener.com/                           https://bulkdata.uspto.gov/


                                                        4
2.12     Project Gutenberg                                  provides an opportunity to model real-time human
Project Gutenberg is a dataset of classic Western           interactions, which feature a level of spontaneity
literature. The specific Project Gutenberg derived          not typically found in other modes of social me-
dataset we used, PG-19, consists of Project Guten-          dia.
berg books from before 1919 (Rae et al., 2019),             2.17   EuroParl
which represent distinct styles from the more mod-
ern Books3 and BookCorpus. Additionally, the PG-            EuroParl (Koehn, 2005) is a multilingual parallel
19 dataset is already being used for long-distance          corpus originally introduced for machine transla-
context modeling.                                           tion but which has also seen use in several other
                                                            fields of NLP (Groves and Way, 2006; Van Hal-
2.13     OpenSubtitles                                      teren, 2008; Ciobanu et al., 2017). We use the most
The OpenSubtitles dataset is an English language            current version at time of writing, which consists of
dataset of subtitles from movies and television             the proceedings of the European Parliament in 21
shows gathered by Tiedemann (2016). Subtitles               European languages from 1996 until 2012.
provide an important source of natural dialog, as           2.18   YouTube Subtitles
well as an understanding of fictional formats other
than prose, which may prove useful for creative             The YouTube Subtitles dataset is a parallel cor-
writing generation tasks such as screenwriting,             pus of text gathered from human generated closed-
speechwriting, and interactive storytelling.                captions on YouTube. In addition to providing mul-
                                                            tilingual data, Youtube Subtitles is also a source of
2.14     DeepMind Mathematics                               educational content, popular culture, and natural
                                                            dialog.
The DeepMind Mathematics dataset consists of a
collection of mathematical problems from topics             2.19   PhilPapers
such as algebra, arithmetic, calculus, number the-
                                                            The PhilPapers7 dataset consists of open-access
ory, and probability, formatted as natural language
                                                            philosophy publications from an international
prompts (Saxton et al., 2019). One major weakness
                                                            database maintained by the Center for Digital Phi-
of large language models has been performance
                                                            losophy at the University of Western Ontario. We
on mathematical tasks (Brown et al., 2020), which
                                                            included PhilPapers because it spans a wide body
may be due in part to a lack of math problems in
                                                            of abstract, conceptual discourse, and its articles
the training set. By explicitly including a dataset
                                                            contain high quality academic writing.
of mathematical problems, we hope to improve the
mathematical ability of language models trained on          2.20   NIH Grant Abstracts:
the Pile.                                                          ExPORTER
2.15     BookCorpus2                                        The NIH Grant abstracts provides a bulk-data repos-
                                                            itory for awarded applications through the Ex-
BookCorpus2 is an expanded version of the origi-
                                                            PORTER8 service covering the fiscal years 1985-
nal BookCorpus (Zhu et al., 2015), a widely used
                                                            present. We included the dataset because it contains
language modeling corpus consisting of books writ-
                                                            examples of high-quality scientific writing.
ten by “as of yet unpublished authors.” BookCor-
pus is therefore unlikely to have significant overlap       2.21   Hacker News
with Project Gutenberg and Books3, which consist
                                                            Hacker News9 is a link aggregator operated by Y
of published books. BookCorpus is also commonly
                                                            Combinator, a startup incubator and investment
used as dataset for training language models (Rad-
                                                            fund. Users submit articles defined as “anything
ford et al., 2018; Devlin et al., 2019; Liu et al.,
                                                            that gratifies one’s intellectual curiosity,” but sub-
2019).
                                                            mitted articles tend to focus on topics in computer
2.16     Ubuntu IRC                                         science and entrepreneurship. Users can comment
                                                            on submitted stories, resulting in comment trees
The Ubuntu IRC dataset is derived from the pub-
                                                            discussing and critiquing submitted stories. We
licly available chatlogs6 of all Ubuntu-related chan-
                                                               7
nels on the Freenode IRC chat server. Chatlog data               https://philpapers.org/
                                                               8
                                                                 https://exporter.nih.gov/
   6                                                           9
       https://irclogs.ubuntu.com/                               https://news.ycombinator.com


                                                        5
scrape, parse, and include these comment trees              2019) and GPT-3 (Brown et al., 2020), shown in
since we believe they provide high quality dialogue         Figure 2. We use all available versions of GPT-2,
and debate on niche topics.                                 and all four versions of GPT-3 available via the
                                                            OpenAI API. Because of the cost associated with
2.22    Enron Emails                                        using the OpenAI API, we evaluate on one-tenth of
The Enron Emails dataset (Klimt and Yang, 2004)             the respective test sets for most of the constituent
is a valuable corpus commonly used for research             datasets. We report the perplexity converted to bits
about the usage patterns of email. We included              per UTF-8 encoded byte (BPB). Importantly, we
Enron Emails to aid in understanding the modality           compute perplexity by evaluating each document
of email communications, which is typically not             independently within each dataset, as opposed to
found in any of our other datasets.                         concatenating all documents as is common practice
                                                            for computing perplexity on large corpora.
3     Benchmarking Language Models with
      the Pile                                              Full details of the perplexity computation can be
                                                            found in Appendix E.2.
While the Pile was conceived as a training dataset
for large-scale language models, its coverage of            Unsurprisingly, larger language models generally
multiple disparate domains makes it also suitable           attain lower perplexity compared to smaller models.
as an evaluation dataset. In this section, we de-           Recent work has shown an increased focus on the
scribe how the Pile can be used as a broad-coverage         empirical scaling laws of language models (Kaplan
dataset for benchmarking language models.                   et al., 2020; Henighan et al., 2020). As such, we
                                                            investigate the scaling law for the GPT-2 and GPT-
3.1    Benchmarking Guidelines                              3 families of models on perplexity evaluation on
The Pile is provided as train, validation, and test-        the Pile. The scaling law relation for the GPT-3
ing splits. The validation and testing components           family of models is shown in Figure 2.10 The line
each contain 0.1% of the data, sampled uniformly            of best fit shown in the figure has a coefficient of
at random. While this is a far smaller percentage           -0.1674 and an intercept of 2.5516.
than most datasets, the sheer size of the dataset
results in over 1 GiB of validation and testing data
each. We highlight that while we have made ef-
forts to deduplicate documents within the Pile (See:
Section D.2), it is still possible that some docu-
ments are duplicated across the train/validation/test
splits.
Our preferred metric is bits per UTF-8 encoded
byte (BPB). Bits per byte is preferred over bits per
character or perplexity when using Pile as a met-
ric due to its invariance to different tokenization
schemes and the ambiguity of measuring charac-
ters in Unicode. To compute bits per byte from a
                                                            Figure 2: Scaling law for performance of GPT-2/3 mod-
given negative log likelihood loss `, we compute
                                                            els. ‘Zero-shot’ refers to the fact that none of the mod-
BPB = (LT /LB ) log2 (e` ) = (LT /LB )`/ ln(2),
                                                            els have been fine-tuned on data from the Pile.
where LT is the length of the dataset in tokens and
LB is the length of the dataset in UTF-8 encoded            Interestingly, while GPT-2 and GPT-3 were not
bytes. We find that LT /LB is 0.29335 GPT-2-                trained on the Pile, there still appears to be a clear
tokens/byte across the Pile; dataset-specific values        scaling law without diminishing returns. We hy-
of LT /LB can be found in Table 7.                          pothesize that this is due to the inherent generaliza-
3.2    Test Perplexity with GPT-2 and                       tion capability of these models. We leave a more
       GPT-3                                                  10
                                                                 While the sizes of GPT-3 models on the OpenAI API have
                                                            not been publicized, we assume here that ada, babbage,
We compute the test perplexity of the constituent           curie and davinci models correspond to 2.7B, 6.7B, 13B
datasets of the Pile using GPT-2 (Radford et al.,           and 175B parameter models respectively.


                                                        6
rigorous analysis of zero-shot scaling laws to future         GPT-3 appears to perform poorly on datasets
work.                                                         pertaining to research or academic writing like
                                                              PubMed Central, PubMed Abstracts, and ArXiv;
3.3   Relative Componentwise GPT-3 Pile                       domain-specific datasets like FreeLaw, Hack-
      Performance                                             erNews, and USPTO Backgrounds; and on datasets
Determining which components GPT-3 underper-                  containing predominantly text distinct from natu-
forms on provides information about which Pile                ral language, like GitHub and DM Mathematics.
components are most dissimilar to the distribution            In addition, the majority of datasets see less of an
of text (web pages and books) that GPT-3 was                  improvement than OpenWebText2. As such, we ex-
trained on. These components would thus make es-              pect a GPT-3 sized model trained on Pile to perform
pecially good candidates for supplementing GPT-3              significantly better on research related tasks, soft-
training data. These results are also valuable for            ware tasks, and symbol manipulation tasks than the
determining which types of datasets to emphasize              base model. Additionally, this experiment provides
for future iterations of the Pile.                            evidence that the majority of Pile components are
                                                              not redundant with the predominantly web-based
Due to the difference in entropy of different
                                                              GPT-3 training data.
datasets, directly comparing perplexity of GPT-3
on different Pile components is not an accurate in-
                                                              We note that this metric is only a proxy for similar-
dication of relative performance. Ideally we would
                                                              ity, and that it could be confounded by dataset spe-
train a GPT-3 model from scratch on the Pile and
                                                              cific scaling effects. Although our results largely
compare the difference in loss per dataset with
                                                              accord with expectations, there are some puzzling
that of the original GPT-3. Because of resource
                                                              results, like the datasets on which GPT-3 outper-
constraints, we instead use a GPT-2 model trained
                                                              formed GPT-2 Pile. We hypothesize that GPT-3
from scratch on the Pile (see Section 4) to con-
                                                              learns to be so good at these datasets that train-
struct a proxy measure. To construct our proxy,
                                                              ing on them explicitly does not notably benefit the
we first measure the improvement from the GPT-
                                                              model’s performance. We leave a more rigorous
2-Pile model to GPT-3 on each component. Then,
                                                              analysis of these effects for future work.
we normalize our results by setting the change on
OpenWebText2 to be zero. This computation is
shown in the equation below:                                  4     Evaluation

                                                              To confirm the effectiveness of the Pile for im-
        ∆set = LGPT3 − LGPT3
                                                             proving language modeling quality, we train
                set      owt2
                                                            architecturally-identical 1.3 billion parameter mod-
             − LGPT2Pile
                set      − L GPT2Pile
                             owt2                             els based on those in Brown et al. (2020) on dif-
                                                              ferent datasets and evaluate on the WikiText and
Since GPT2-Pile was trained on both OWT2 and                  LAMBADA tasks as benchmarks of language mod-
the dataset we are evaluating, we expect the second           eling ability. We also report results on the Pile
term in ∆set to reflect the difference in the intrinsic       as a measure of more cross-domain generaliza-
difficulty of the two datasets. Thus the total value          tion.
of ∆set reflects how much harder the dataset we are
evaluating was for GPT-3 than OWT2, minus the                 4.1    Methodology
relative difficulty of the two tasks. As GPT-3 was
                                                              To ensure a fair comparison across datasets of dif-
trained on data very similar to OWT2, this gives us
                                                              ferent sizes, we decontaminate any instances of the
a proxy for how much better GPT-3 would do if it
                                                              evaluation sets using the same 13-gram overlap fil-
were trained on the Pile.
                                                              tering as in Brown et al. (2020) and downsample
The results are shown in Figure 3. As a san-                  to 40GB to control for dataset size. As we control
ity check, we observe that datasets that are con-             for dataset size, we emphasize that our evaluation
tained in, or are extremely similar to, GPT-3’s               is generous to CC-100 (en), which is about 1/3 the
training set (Books3, Wikipedia (en), Pile-CC and             size of the Pile in reality.
Project Gutenberg) score close to zero on our met-
ric.                                                          We compare the following datasets: the Pile, the En-

                                                          7
 Component                                GPT-2                                          GPT-3
                           small    medium        large           xl      ada      babbage     curie    davinci
 Pile-CC                  1.0878     0.9992     0.9582         0.9355    0.9212     0.8483    0.7849     0.7070
 PubMed Central           1.0759     0.9788     0.9334         0.9044    0.8633     0.7792    0.7150     0.6544
 Books3                   1.1959     1.1063     1.0588         1.0287    0.9778     0.9005    0.8284     0.7052
 OpenWebText2             1.1111     1.0073     0.9539         0.9171    0.8727     0.7921    0.7199     0.6242
 ArXiv                    1.3548     1.2305     1.1778         1.1381    1.0304     0.9259    0.8453     0.7702
 Github                   1.7912     1.3180     1.7909         1.6486    0.8761     0.7335    0.6415     0.5635
 FreeLaw                  1.0512     0.9321     0.9017         0.8747    0.8226     0.7381    0.6667     0.6006
 Stack Exchange           1.2981     1.1075     1.0806         1.0504    1.0096     0.8839    0.8004     0.7321
 USPTO Backgrounds        0.8288     0.7564     0.7202         0.6969    0.6799     0.6230    0.5752     0.5280
 PubMed Abstracts         0.9524     0.8579     0.8108         0.7810    0.8130     0.7382    0.6773     0.6201
 Gutenberg (PG-19)        1.2655     1.1140     1.0820         1.0829    0.9776     0.8749    0.7930     0.7115
 OpenSubtitles            1.2465     1.1657     1.1324         1.1129    1.1116     1.0488    0.9875     0.9130
 Wikipedia (en)           1.1285     1.0213     0.9795         0.9655    0.8757     0.7863    0.7047     0.5953
 DM Mathematics           2.6911     2.5448     2.4833         2.4377    2.3249     2.2015    2.1067     2.0228
 Ubuntu IRC               1.8466     1.7187     1.6427         1.6024    1.3139     1.1968    1.0995     0.9915
 BookCorpus2              1.1295     1.0498     1.0061         0.9783    0.9754     0.9041    0.8435     0.7788
 EuroParl                 2.3177     2.0204     1.8770         1.7650    1.0475     0.9363    0.8415     0.7519
 HackerNews               1.4433     1.2794     1.3143         1.3361    1.1736     1.0875    1.0175     0.9457
 YoutubeSubtitles         2.0387     1.8412     1.7355         1.6694    1.3407     1.1876    1.0639     0.9469
 PhilPapers               1.3203     1.2163     1.1688         1.1327    1.0362     0.9530    0.8802     0.8059
 NIH ExPorter             0.9099     0.8323     0.7946         0.7694    0.7974     0.7326    0.6784     0.6239
 Enron Emails             1.5888     1.4119     1.4535         1.4222    1.2634     1.1685    1.0990     1.0201
 The Pile                 1.2253     1.0928     1.0828         1.0468    0.9631     0.8718    0.7980     0.7177

Table 2: Test perplexity of the Pile using GPT-2 and GPT-3, converted to bits per UTF-8 encoded byte (BPB).
Evaluation is performed on one-tenth of the test data of the Pile, on a per-document basis. Bold indicates the
best-performing model in each row.


glish component of the CC-100 dataset11 (Wenzek               cantly on programming-related datasets like Github
et al., 2019; Conneau et al., 2020), and a sample of          and StackExchange, on EuroParl, due to the lack of
raw CC WET files filtered for English-only.                   multilingual text in either other dataset, and on DM
                                                              Mathematics, indicating a significant improvement
4.2   Results                                                 in mathematical ability.
On traditional language modeling benchmarks, the
                                                              Surprisingly, raw Common Crawl performs better
Pile improves significantly on WikiText and shows
                                                              on the Pile BPB than CC-100, despite losing by a
negligible changes in LAMBADA. However, mod-
                                                              significant margin on LAMBADA and WikiText.
els trained on Pile improve significantly over both
                                                              We hypothesize that this is due to the perplexity
Raw CC and CC-100 on all components of the
                                                              based filtering used in CC-100, where a language
Pile, as shown in Table 4. This indicates that mod-
                                                              model is trained on Wikipedia and all data with a
els trained on the Pile have greater cross-domain
                                                              perplexity too high or too low is discarded. This
generalization capabilities without compromising
                                                              effectively discards any data too similar to or too
performance on traditional benchmarks.
                                                              different from Wikipedia, which severely limits
The magnitude of improvement over CC-100 per                  the diversity of the collected data. This result
set is shown in Figure 4. Unsurprisingly, there               suggests that future work using Common Crawl
is almost no improvement on Pile-CC. However,                 should take caution with filtering to preserve its
the model trained on the Pile performs signifi-               diversity.
cantly better than either of the other models on
academic datasets such as ArXiv, Pubmed Central,              5   Structural Statistics
FreeLaw, and PhilPapers. It also improves signifi-            In this section, we cover the Structural Statistics
  11
     The data was obtained from http://data.statmt.           of the dataset, which provide more coarse-grained
org/cc-100/.                                                  and statistical information about the Pile. In Sec-

                                                          8
Figure 3: Change in BPB from GPT-2 trained on Pile to GPT-3 zero-shot, relative to OpenWebText2 BPB change.
Dotted line indicates overall Pile change. Lower indicates better relative performance by GPT-3.

                      Dataset Size     Pile (val)   Pile (test)    WikiText    LAMBADA          LAMBADA
                                        (BPB)         (BPB)         (PPL)        (PPL)            (ACC)
      The Pile           825 GiB         0.9281        0.9433           5.59           12.78             50.1
      CC-100 (en)        300 GiB         1.3143        1.3293           8.27           11.78             49.7
      Raw CC           45927 GiB†        1.1180        1.1275          11.75           19.84             43.8

Table 3: Size-controlled evaluation results. Each dataset is deduplicated against all evaluation metrics and subsam-
pled to approximately 40GB to control for the effects of dataset size. For LAMBADA, we use the variant of the
data introduced in Radford et al. (2019) and only evaluate the perplexity on the final token rather than the final
word. For WikiText, we report the perplexity per GPT-2 token. † indicates that the size is an estimate.


tion 6, we provide a closer investigation and doc-           consist largely of ordinary text in a similar distri-
umentation of the textual content within the Pile            bution to WebText, which is reflected in a greater
datasets.                                                    number of bytes per token. On the other hand,
                                                             many of the sets with the lowest bytes per token
5.1   Document Lengths and                                   are those which consist in large part of non-text
      Tokenization                                           content (Github, ArXiv, Stack Exchange, and DM
Each dataset consists of a large number of docu-             Mathematics) or languages other than English (Eu-
ments. We analyze the distribution of document               roParl).
lengths, as well as the number of bytes-per-token
using the GPT-2 tokenizer in order to put our abla-          5.2   Language and Dialects
tions in context.                                            While only 13% of the world’s population speaks
                                                             English, the vast majority of NLP research is done
While the majority of documents in the Pile are
                                                             on English. For the Pile, we took a similar ap-
short, there is a long tail of very long documents
                                                             proach to the dataset used by Brown et al. (2020)
(Figure 5).
                                                             and focused predominantly on English, while also
Since the GPT-2 BPE tokenizer is trained on Web-             not explicitly filtering out other languages when
Text, the mean bytes per token is also a very rough          collecting our own data. When evaluating a multi-
indicator of how syntactically different each Pile           lingual dataset, our main criteria for inclusion was
component is from WebText. For instance, datasets            whether the English component of the dataset mer-
like NIH ExPorter, OpenWebText2 and Books3                   ited inclusion alone. We plan to create a fully multi-

                                                         9
           Figure 4: Magnitude of BPB improvement of Pile model over CC-100 model on each test set.


 Dataset              The Pile   CC-100 (en)   Raw CC (en)
 Pile-CC               0.9989        1.0873         1.0287
 PubMed Central        0.6332        1.1311         0.9120
 Books3                1.0734        1.2264         1.1366
 OpenWebText2          0.9938        1.2222         1.0732
 ArXiv                 0.7945        1.8159         1.2642
 Github                0.5597        1.6509         0.9301
 FreeLaw               0.6978        1.0221         0.9468
 Stack Exchange        0.8152        1.5414         1.1292
 USPTO Backgrounds     0.6731        0.8772         0.8455
 PubMed Abstracts      0.7313        1.0193         0.9718
 Gutenberg (PG-19)     1.1426        1.2780         1.2235
 OpenSubtitles         1.0909        1.1827         1.2139
 Wikipedia (en)        0.8961        1.1807         1.0252
 DM Mathematics        1.5206        3.1774         2.6229
 Ubuntu IRC            1.4085        2.1243         1.5691
 BookCorpus2           1.0613        1.1346         1.0914
 EuroParl              1.1202        2.7141         1.4917
 HackerNews            1.0968        1.4352         1.2305        Figure 5: Distribution of document lengths in Pile. The
 YoutubeSubtitles      1.4269        2.3287         1.5607
 PhilPapers            1.1256        1.4269         1.2090        highest 1 percentile of document length are considered
 NIH ExPorter          0.7347        0.9713         0.9225        to be outliers and excluded from this plot.
 Enron Emails          0.8301        1.3300         1.0483

Table 4: Breakdown of BPB on Pile heldout test set.               6   Investigating and Documenting the
Columns indicate the dataset each model is trained on;                Datasets
rows indicate the evaluation dataset. Bold indicates the
best performing model in each row.                                As the scale of machine learning research has
                                                                  grown, scrutiny has been placed on the ever
                                                                  larger datasets that models are trained on (Prabhu
lingual expansion of the Pile as future work.                     and Birhane, 2020; Biderman and Scheirer,
                                                                  2020)
Using fasttext (Suárez et al., 2019a), we deter-                  While this issue has been raised within AI ethics
mine that the Pile is 97.4% English. We note that                 and bias research (Hovy and Spruit, 2016; Hutchin-
due to issues with language identification, partic-               son et al., 2020; Blodgett et al., 2020), it has not
ularly with rare languages Caswell et al. (2020),                 been a focal point of concern within the language
this methodology provides only a rough estimate                   modeling community. Despite the proliferation
for English content and no reliable conclusions for               of work exploring and documenting issues with
low-resource languages can be drawn.                              datasets (Gebru et al., 2018; Bender and Friedman,

                                                             10
                                                                      tives (Seck et al., 2018; Costa-jussà et al., 2020;
                                                                      Thieme et al., 2020). The second, the data state-
                                                                      ments methodology (Bender and Friedman, 2018),
                                                                      was proposed specifically for natural language pro-
                                                                      cessing and has been well received by the NLP
                                                                      community. Our datasheet and data statement will
                                                                      be featured in the GitHub repository where the
                                                                      code for the Pile is stored and will also be available
                                                                      as separate documents on arXiv (Biderman et al.,
                                                                      2021; Biderman, 2021).
                                                                      In addition to the datasheet and data statement,
                                                                      there is additional information that may be helpful
                                                                      to people training language models that these doc-
                                                                      uments do not cover. In the rest of this section we
                                                                      investigate and document in greater detail some of
Figure 6: Mean bytes per GPT-2-token for each dataset
                                                                      this additional contextual information.
in the Pile. Error bars indicate standard deviation.
                                                                      6.2   Topical Distribution
2018; Jo and Gebru, 2020), no dataset intended                        In order to better understand the specific subject
to train massive language models has been seri-                       matter covered by the Pile, we performed a topic
ously documented by its creators12 . Therefore, our                   modeling analysis on its components. Using Gen-
analyses serve two goals: to address ethical con-                     sim (Rehurek et al., 2011), we trained 16-topic La-
cerns about the Pile, and to promote and normalize                    tent Dirichlet Allocation (Blei et al., 2003) models
the practice of engaging with the AI ethics litera-                   on each component of the validation set of the Pile
ture.                                                                 concurrently, in an online fashion (Hoffman et al.,
                                                                      2010). We filtered the Pile for English only for this
Natural language processing technologies are
                                                                      analysis. Afterwards, we computed the perplex-
widely applicable and can be used in extremely
                                                                      ity of the Common Crawl-derived (Pile-CC) topic
different contexts. What is and is not appropriate
                                                                      model on the document sets of the other compo-
data to train on can therefore vary wildly with the
                                                                      nents. In this way, we provide a rough measure of
application context. In our view, the best approach
                                                                      the degree to which parts of the Pile contain topics
is to document rather than eliminate potentially con-
                                                                      not well covered within Common Crawl.
cerning aspects of datasets13 , particularly since the
purpose of the Pile is to train general-purpose lan-                  In Figure 7, these cross-component perplexities are
guage models. The primary goal of our documen-                        shown, with a vertical line indicating the perplexity
tation, therefore, is to empower NLP researchers to                   of the Pile-CC topic model evaluated on the doc-
make informed decisions.                                              uments of OpenWebText2. This component was
                                                                      chosen as a baseline of comparison for similar rea-
6.1    Documenting Methods                                            sons as in the previous evaluation: it is derived in a
To document the Pile, we chose to implement two                       similar manner (filtered crawls of the open web) as
frameworks that have been proposed by method-                         the Common Crawl, and thus is expected to contain
ologists and ethics researchers. The first, the                       a similar distribution of topics. Although Pile-CC
datasheets methodology (Gebru et al., 2018), is a                     is somewhat diverse in its content, several of the
general purpose methodology that is recommended                       Pile’s other components deviate from it strongly in
by several methodologists (Raji and Yang, 2019;                       their topical focus, as evidenced by higher perplex-
Biderman and Scheirer, 2020) and appears to be                        ity on Github, PhilPapers, and EuroParl.
used more frequently by practitioners than alterna-
                                                                      We also documented the topical clusters inferred
  12
      Brown et al. (2020) discusses ethical issues surrounding        from our LDA models for each component, which
their model, but do not discuss those surrounding the training        we provide in Appendix C. As expected, though
dataset itself.
   13
      That said, we did exclude several datasets, see Appendix        the larger CC-derived component itself represents a
B for details.                                                        diversity of content—including politics, education,

                                                                 11
sports and entertainment—the content clusters it              model. We primarily focus on co-occurrence tests,
misses become apparent when compared qualita-                 where we analyzed what words occur in the same
tively to other components of the Pile. Notably, the          sentence as other specific words. Using this infor-
data modes covering programming, logic, physics,              mation, we can estimate what words strongly bias
and legal knowledge appear largely absent.                    towards a category word, as well as calculate the
                                                              general sentiment of surrounding words.
6.3   Pejorative Content
Due to the wide diversity in origins, it is possible          We focused our analysis on gender, religion, and
for the Pile to contain pejorative, sexually explicit,        race. Our goal is to provide users of this dataset
or otherwise objectionable content. As this content           with preliminary guidance on how the different
may not be desirable for some use cases, we break             components are biased so that they can make deci-
down profanity on a per-dataset level.                        sions on which components to train on.

We used the profanity-checker Python                          All tables and figures in this section can be found
package (Zhou, 2019). This package includes a                 in the Appendix.
“toxicity model” trained on multiple profanity lists
                                                              6.4.1   Gender
as well as the Wikidetox Toxic Comment Dataset
(Wulczyn et al., 2016) and classifies a given string          We computed gender associations by computing co-
as being profane or not profane.                              occurrences for binary pronouns. For each word,
                                                              we computed the difference in the rate it co-occurs
We considered only the English sentences in                   with "he" and "she"14 and weighed it by the square
each dataset using the same language classi-                  root of its frequency. We report the top 15 most
fier from Section 3.7.        We did this since               biased adjectives or adverbs (Loper and Bird, 2002)
profanity-checker is built for English and                    for each in Table 10. We see that words like “mil-
other languages may improperly impact the results.            itary”, “criminal”, and “offensive” strongly bias
For instance, the German nominative/accusative                towards men, while “little”, “married”, “sexual”,
feminine/plural definite article "die" is flagged as          and “happy” bias towards women.
being profane regardless of context. We split each
sentence into words and computed the percentage               In addition, we computed the average senti-
of words that are flagged as profane for each com-            ment (Baccianella et al., 2010) of words co-
ponent of the Pile. We emphasize that this method-            occurring with the gendered pronouns across each
ology is only a proxy for profanity, given the com-           dataset in Figure 13. Generally, we find no sig-
plexity of determining whether a given word or                nificant sentiment bias towards men or women.
phrase is profane in context.                                 This, of course, does not mean that the dataset
                                                              is free of gender bias (as our co-occurrence tests
As shown in Figure 8, the Pile as a whole appears             show).
less profane than Pile-CC. Further, the majority of
Pile components appear less profane than Pile-CC              6.4.2   Religion
as well.                                                      We computed a similar co-occurrence analysis for
We also broke each dataset down on a sentence                 religion, which can be found in Table 11. Like gen-
level, to allow profanity-checker to check                    der, we find that these co-occurrences reflect how
entire sentences. Splitting datasets by sentence              these terms are used in pockets of online discourse.
allows for additional context to be considered when           For example, “radical” co-occurs with “muslim” at
determining whether content is pejorative. Our                a high rate, while “rational” often co-occurs with
results are shown in Figure 12.                               “atheist”. This analysis also demonstrates some
                                                              of the limitations of a purely co-occurrence based
6.4   Bias and Sentiment Co-occurrence                        analysis. For example, “religious” often co-occurs
As language models may pick up unexpected biases              with “atheist”, which likely reflects the type of con-
from the training data, we performed a preliminary            versations in which the word “atheist” is likely to
analysis of the different components that make up             occur as opposed to a descriptor of “atheist”.
the Pile. Because models with different charac-                 14
                                                                   We chose to only study male and female pronouns as a
teristics may be trained on the Pile, we aimed to             simplifying assumption. Studying “they” would require us to
document the biases of the data and not a specific            isolate its usage as a singular noun.


                                                         12
Figure 7: Log perplexity of 16-topic LDA trained on Pile-CC, on other Pile components. Dotted line indicates log
perplexity of the topic model on OpenWebText2. Higher indicates a larger topical divergence from Pile-CC.


                                                              occurences with phrases like “black man” or “white
                                                              woman”.
                                                              We show the top 15 most biased words for each
                                                              demographic in Table 12. Once again, we found
                                                              that the co-occurrences reflect the context in which
                                                              these terms are used. For example, the 4 most
                                                              biased words for “black” are “unarmed”, “civil”,
                                                              “criminal”, and “scary”.
                                                              Similar to above, we compute the average senti-
                                                              ment of co-occurring words. We report the average
                                                              sentiment numbers in Table 13. We find that “his-
                                                              panic/latino” narrowly edges out “asian” for the
                                                              highest sentiment, followed by “white”. On the
                                                              other hand, “black” had the lowest sentiment, at
Figure 8: Percentage of words classified as profane in
                                                              -0.15.
the Pile. The percentage of the CC component and the
weighted mean of the Pile as a whole are shown as hor-        We note that for all demographics, the average sen-
izontal lines.                                                timent is negative. We hypothesize that this is due
                                                              to the specific context for which the phrases we use
In addition, we computed the average sentiment                to compute co-occurrences appear. For example, it
of co-occurrences across each of the constituent              is often quite common for news articles to describe
datasets in Figure 14. Over the entire dataset,               suspects as an “asian man”.
we find that “Buddhist” has the highest sentiment,            6.5   Author Consent and Public Data
followed by “Hindu”, “Christian”, “Atheist”, and
“Muslim”. Notably, “Jew” is the lowest, perhaps               Another issue with the use of texts in natural lan-
reflecting its historical use as a pejorative.                guage processing research is consent. Although
                                                              one is typically not legally obligated to receive the
6.4.3   Race                                                  permission of an author to train a NLP algorithm on
Finally, we ran the same analysis for racial groups.          their work15 , many consider doing so a moral obli-
Here, as identifiers like “black” or “white” of-                15
                                                                   Laws vary by country. For a discussion of US law, see
ten do not indicate race, we instead compute co-              Section 7.1


                                                         13
gation or a good measure to guard against misuse                authorized to post the data online by the parties
(Obar, 2020; Prabhu and Birhane, 2020). On the                  that own it. The Enron Emails dataset was not
other hand, there is significant disagreement sur-              collected with the permission of the authors, but
rounding the ethics of repurposing data protected               was collected by the U.S. government as part of
by terms of service in research contexts (Vitak et al.,         a criminal investigation. While the people whose
2016; Fiesler et al., 2020), particularly given the             emails are in the Enron dataset are aware of this
power asymmetries inherent in digital platforms,                fact, they were not given the ability to consent to
which often close off independent researchers from              its inclusion in any way.
investigating public data while simultaneously com-
                                                                There are five datasets included in the Pile that were
pelling users to consent to its private use (Halavais,
                                                                not collected and distributed in a ToS compliant
2019).
                                                                fashion and for which the authors had no ability
While much of the Pile’s data comes from sources                to consent to their data being used. Each of these
that have expressly consented to its wider dissemi-             datasets are widely used, both in the NLP litera-
nation and use in research, researchers often fail to           ture and the world at large. With the exception
clearly document where their data came from and                 of the YouTube Subtitles dataset, each of these
under what terms its use was consented to. In light             datasets were published by researchers and are
of this, we felt it appropriate to release the Pile with        passed around freely on the internet. The YouTube
transparency around how the authors of its data                 Subtitles dataset was created by us for this project,
have indicated that that data can be used.                      using a very popular unofficial API that is both
                                                                widely used and easily obtainable on Pip, Conda,
To provide needed nuance to our discussion of con-              and GitHub, among other places. Given the pro-
sent, we identified three tiers of availability for             cessing applied and the difficulty of identifying par-
public use. Public data is data which is freely and             ticular files in the Pile, we feel that our use of these
readily available on the internet. This primarily               datasets does not constitute significantly increased
excludes data which is pay-walled (regardless of                harm beyond that which has already been done by
how easy that paywall is to bypass) and data which              the widespread publication of these datasets.
cannot be easily obtained but can be obtained, e.g.
through a torrent or on the dark web. Terms of                  7     Implications and Broader
Service (ToS) compliant data is data which is ob-                     Impacts
tained and used in a fashion that is known to be
consistent with the terms of service of the data host.          The Pile represents yet another stepping stone
Data with authorial consent is data for which the               along the path of scaling models and datasets to
original authors of the work consented to the use               ever larger sizes and capabilities. There are many
of their data, or where a reasonable person could               serious concerns about how the emergence of pro-
not assume that their data would not be used for                gressively stronger AI systems will influence the
purposes such as research. ToS compliant data and               wider world (Brundage et al., 2018; Amodei et al.,
authorial consented data differ in two main ways:               2016; Bostrom and Yudkowsky, 2014; Bostrom,
It is important to keep in mind that people typically           2014; Critch and Krueger, 2020), and we believe
do not read Terms of Service, and additionally that             that they merit serious thought. In this section
being ToS-compliant does not entail authorial con-              we discuss the legal ramifications of the Pile, and
sent. We adopted a strict model of consent, where               then consider the impact of the Pile to AI align-
ambiguous or unknown consent is treated as non-                 ment from two angles: accelerating AI timelines
consensual.                                                     and the dangers posed by unaligned language mod-
                                                                els.
Table 5 summarizes our understanding of the status
of each of the datasets within the Pile. Datasets               7.1    Legality of Content
marked with a 3are compliant in the relevant re-                While the machine learning community has be-
spects, though a couple datasets are worth remark-              gun to discuss the issue of the legality of training
ing on in particular. Book3 and OpenSubtitles are               models on copyright data, there is little acknowl-
being used in a fashion that is consistent with the             edgment of the fact that the processing and dis-
terms of service of the data host. However, this is             tribution of data owned by others may also be a
somewhat misleading in that the data host is not                violation of copyright law. As a step in that direc-

                                                           14
 Component                Public       ToS      Author                    additional restrictions on some of these works in
 Pile-CC                     3          3                                 particular jurisdictions. To enable easier compli-
 PMC                         3          3           3                     ance with local laws, the Pile reproduction code is
 Books3                      3                                            available and can be used to exclude certain com-
 OWT2                        3                                            ponents of the Pile which are inappropriate for
 ArXiv                       3          3           3                     the user. Unfortunately, we do not have the meta-
 Github                      3          3                                 data necessary to determine exactly which texts are
 FreeLaw                     3          3           3                     copyrighted, and so this can only be undertaken at
 Stack Exchange              3          3           3                     the component level. Thus, this should be be taken
 USPTO                       3          3           3                     to be a heuristic rather than a precise determina-
 PubMed                      3          3           3                     tion.
 PG-19                       3          3
                                                                          7.2   Acceleration of AI Timelines
 OpenSubtitles               3
 Wikipedia                   3          3           3                     There is serious concern that AI systems may soon
 DM Math                     3          3           3                     be meaningfully more capable than humans in all
 Ubuntu IRC                  3          3           3                     relevant economic tasks (Grace et al., 2018; Yud-
 BookCorpus2                 3                                            kowsky, 2013). Relatedly, there are serious unre-
 EuroParl                    3          3           3                     solved questions surrounding how to properly align
 HackerNews                  3          3                                 such powerful AI systems with human interests
 YTSubtitles                 3                                            (Bostrom and Yudkowsky, 2014; Russell, 2019;
 PhilPapers                  3          3           3                     Bostrom, 2014; Amodei et al., 2016) and generally
 NIH                         3          3           3                     avoid morally catastrophic outcomes (Sotala and
 Enron Emails                3          3                                 Gloor, 2017; Shulman and Bostrom, 2020). As
                                                                          such, it has been argued that accelerating the de-
       Table 5: Types of consent for each dataset                         velopment of such powerful AI systems may be
                                                                          undesirable before these concerns have been more
tion, we discuss the reasons we believe that our                          adequately addressed (Bostrom, 2014).
use of copyright data is in compliance with US
                                                                          There are several pragmatic responses to this
copyright law.16
                                                                          view:
Under pre (1984) (and affirmed in subsequent
                                                                            1. Due to human competition, curiosity, and cul-
rulings such as aff (2013); Google (2015)), non-
                                                                               tural diversity, halting technological develop-
commercial, not-for-profit use of copyright media
                                                                               ment is incredibly difficult, if not impossible.
is preemptively fair use. Additionally, our use is
                                                                               (Russell, 2019) (Critch and Krueger, 2020)
transformative, in the sense that the original form
of the data is ineffective for our purposes and our                         2. AI development is experimental in nature:
form of the data is ineffective for the purposes of                            The alignment problem can only be solved
the original documents. Although we use the full                               through development, testing and (hopefully
text of copyright works, this is not necessarily dis-                          non-existential) failure.
qualifying when the full work is necessary (ful,
2003). In our case, the long-term dependencies in                           3. High powered language models, along with
natural language require that the full text be used in                         their more general successors, must be capa-
order to produce the best results (Dai et al., 2019;                           ble of viewing morally problematic content
Rae et al., 2019; Henighan et al., 2020; Liu et al.,                           without adopting it in their output. We elabo-
2018).                                                                         rate on this in the following section.
Copyright law varies by country, and there may be                         With this in mind, we accept the reality that the Pile
   16
      This discussion does not, and is not intended to, constitute        could potentially accelerate AI timelines. However,
legal advice; rather, it is a general discussion of law. Only your        we hope our efforts to establish best practices, such
attorney can provide assurances that the information contained            as thoroughly documenting the contents of our data,
herein is applicable or appropriate to a particular situation. If
in doubt, it is always advisable to speak to an intellectual              will help encourage diligence for downstream re-
property attorney.                                                        searchers on alignment problems.

                                                                     15
7.3    Negative LM Output                                    Rosset, 2019; Shoeybi et al., 2019) and masked lan-
There has been much discussion about the possi-              guage models (Devlin et al., 2019; Liu et al., 2019;
ble negative effects of powerful language models             Raffel et al., 2019) have been trained on datasets
in the world (Brown et al., 2020; Brundage et al.,           such as Wikipedia, BookCorpus (Zhu et al., 2015),
2018). Some of these possible problems, such as              RealNews (Zellers et al., 2019), CC-Stories (Trinh
the ability to mass produce low quality content              and Le, 2018), and other Internet scrape-derived
for the purpose of Search Engine Optimization,               datasets discussed below. Other datasets such as
are inherent problems to the way online content              WikiText (Stephen et al., 2016) have also been used
is distributed, and cannot be stopped by those de-           in similar self-supervised training.
veloping language models alone. Directly solving             As data requirements for language modeling have
these problems would require sweeping changes                grown, the field has turned towards Internet scrapes
to the architecture of the Internet, such as vastly          for large-scale datasets (Gokaslan and Cohen,
expanded Public Key Infrastructure and distributed           2019), with Common Crawl being particularly
authentication of identity (Ferguson and Schneier,           prevalent. Works such as Brown et al. (2020); Wen-
2003).                                                       zek et al. (2019); Suárez et al. (2019b); Raffel et al.
                                                             (2019) have relied on Common Crawl to build train-
Another concern is that training such models on
                                                             ing datasets for large-scale models. However, these
huge datasets will almost inevitably require them to
                                                             works often highlight the difficulty of cleaning and
have undesirable content in their training sets, such
                                                             filtering the Common Crawl data, and often high-
as that promoting hateful stereotypes (Christian,
                                                             light the resulting data quality as a determining
2020). Having models output undesirable content
                                                             factor of model capability.
is, by definition, undesirable, but we believe that
attacking this problem from the training set side            It has also been increasingly common practice
is unproductive and ultimately leads us away from            to combine multiple datasets when training lan-
optimal solutions. If a person reads a racist piece          guage models. For instance, GPT (Radford et al.,
of content, they do not then immediately adopt its           2018) was trained on Wikipedia and BookCorpus,
racist views—they may be capable of doing so, but            whereas GPT-3 (Brown et al., 2020) was trained
can decide not to. This capacity to understand un-           on Wikipedia, two fiction datasets, and two web-
desirable content and then decide to ignore it is an         scraped datasets. The Pile continues the trend of
essential future research direction. Not only would          combining large-scale web-scrapes with smaller,
this allow models to use “dirtier" data with less            higher-quality datasets that capture knowledge we
concern, but also to use their gained knowledge              believe would be most beneficial to training lan-
to better understand what not to do. We recognize            guage models.
that, despite recent progress in human-guided learn-
                                                             The two most comparable publicly available
ing (Stiennon et al., 2020), the technology is not
                                                             datasets to the Pile are CC-100 (Wenzek et al.,
yet at this stage, and have thus made a number of
                                                             2019) and C4/mC4 (Raffel et al., 2019). C4 is
editorial decisions as described in this paper. How-
                                                             comparably-sized to the Pile, while mC4 and CC-
ever, this approach seems essential to the future
                                                             100 are larger, multilingual datasets. However,
of these models and AI more broadly, and more
                                                             C4/mC4 require immense computational resources
research is needed.
                                                             to preprocess the data, with its maintainers even rec-
                                                             ommending the use of a distributed cloud service,17
8     Related Work
                                                             setting a high bar of entry to using these datasets.
Self-supervised training of natural language pro-            CC-100 is directly downloadable and pre-cleaned;
cessing models on large, unlabeled text corpora,             however, its English portion is much smaller than
has seen widespread adoption in the field. Word              the Pile. Importantly, these three datasets are all de-
representation models such as GloVe (Pennington              rived entirely from Common Crawl—as discussed
et al., 2014) and word2vec (Mikolov et al., 2013)            above, the current best practice in training large-
were trained on datasets such as Wikipedia, Giga-            scale language models involve using both large web
word (Graff et al., 2003), or a non-public Google            scrapes and more targeted, higher-quality datasets,
News corpus. More recently, language models                    17
                                                                  https://www.tensorflow.org/datasets/
(Radford et al., 2018, 2019; Brown et al., 2020;             catalog/c4


                                                        16
which the Pile directly addresses.                            Tom B Brown, Benjamin Mann, Nick Ryder, Melanie
                                                              Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Nee-
9   Acknowledgments                                           lakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
                                                              et al. 2020. Language models are few-shot learners.
The authors would like to thank TensorFlow Re-                arXiv preprint arXiv:2005.14165.
search Cloud for providing the computational re-              Miles Brundage, Shahar Avin, Jack Clark, Helen
sources for the evaluation and OpenAI for provid-             Toner, Peter Eckersley, Ben Garfinkel, Allan Dafoe,
ing access and credits for the OpenAI API for GPT-            Paul Scharre, Thomas Zeitzoff, Bobby Filar, et al.
                                                              2018. The malicious use of artificial intelligence: Fore-
3 evaluation.
                                                              casting, prevention, and mitigation. arXiv preprint
We would also like to thank Farrukh Raman, JR                 arXiv:1802.07228.
Smith, and Michelle Schmitz for reviewing the                 Nicholas Carlini, Florian Tramer, Eric Wallace,
manuscript.                                                   Matthew Jagielski, Ariel Herbert-Voss, Katherine Lee,
                                                              Adam Roberts, Tom Brown, Dawn Song, Ulfar Erlings-
                                                              son, Alina Oprea, and Colin Raffel. 2020. Extracting
                                                              training data from large language models.
References
                                                              Isaac Caswell, Theresa Breiner, Daan van Esch, and
1984. Sony corp. of america v. universal city studios,        Ankur Bapna. 2020. Language id in the wild: Unex-
inc.                                                          pected challenges on the path to a thousand-language
2003. Kelly v. arriba soft corp.                              web text corpus. arXiv preprint arXiv:2010.14571.

2013. Righthaven llc v. hoehn.                                Brian Christian. 2020. The Alignment Problem: Ma-
                                                              chine Learning and Human Values. WW Norton &
Dario Amodei, Chris Olah, Jacob Steinhardt, Paul              Company.
Christiano, John Schulman, and Dan Mané. 2016.
Concrete problems in AI safety.  arXiv preprint               Alina Maria Ciobanu, Liviu P Dinu, and Andrea Sgarro.
arXiv:1606.06565.                                             2017. Towards a map of the syntactic similarity of lan-
                                                              guages. In International Conference on Computational
Stefano Baccianella, Andrea Esuli, and Fabrizio Sebas-        Linguistics and Intelligent Text Processing, pages 576–
tiani. 2010. Sentiwordnet 3.0: An enhanced lexical re-        590. Springer.
source for sentiment analysis and opinion mining. In
LREC. European Language Resources Association.                Alexis Conneau, Kartikay Khandelwal, Naman Goyal,
                                                              Vishrav Chaudhary, Guillaume Wenzek, Francisco
Emily M Bender and Batya Friedman. 2018. Data                 Guzmán, Edouard Grave, Myle Ott, Luke Zettlemoyer,
statements for natural language processing: Toward            and Veselin Stoyanov. 2020. Unsupervised cross-
mitigating system bias and enabling better science.           lingual representation learning at scale. In Proceedings
Transactions of the Association for Computational Lin-        of the 58th Annual Meeting of the Association for Com-
guistics, 6:587–604.                                          putational Linguistics, pages 8440–8451, Online. As-
                                                              sociation for Computational Linguistics.
Stella Biderman. 2021. Data statement for the Pile.
arXiv preprint arXiv.                                         Marta R Costa-jussà, Roger Creus, Oriol Domingo,
                                                              Albert Domínguez, Miquel Escobar, Cayetana López,
Stella Biderman, Kieran Bicheno, and Leo Gao. 2021.           Marina Garcia, and Margarita Geleta. 2020. Mt-
Datasheet for the Pile. arXiv preprint arXiv.                 adapted datasheets for datasets: Template and reposi-
Stella Biderman and Walter J. Scheirer. 2020. Pitfalls        tory. arXiv preprint arXiv:2005.13156.
in machine learning research: Reexamining the devel-          Andrew Critch and David Krueger. 2020. AI Re-
opment cycle. NeurIPS “I Can’t Believe It’s Not Bet-          search Considerations for Human Existential Safety
ter!” Workshop.                                               (ARCHES). Preprint at acritch.com/arches.
David M Blei, Andrew Y Ng, and Michael I Jordan.              Zihang Dai, Zhilin Yang, Yiming Yang, Jaime
2003. Latent dirichlet allocation. Journal of machine         Carbonell, Quoc V Le, and Ruslan Salakhutdinov.
Learning research, 3(Jan):993–1022.                           2019.    Transformer-xl: Attentive language mod-
Su Lin Blodgett, Solon Barocas, Hal Daumé III, and            els beyond a fixed-length context. arXiv preprint
Hanna Wallach. 2020. Language (technology) is                 arXiv:1901.02860.
power: A critical survey of “bias” in NLP. arXiv              Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
preprint arXiv:2005.14050.                                    Kristina Toutanova. 2019. BERT: Pre-training of deep
Nick Bostrom. 2014. Superintelligence: Paths, Dan-            bidirectional transformers for language understanding.
gers, Strategies. Oxford University Press, Inc.               In Proceedings of the 2019 Conference of the North
                                                              American Chapter of the Association for Computa-
Nick Bostrom and Eliezer Yudkowsky. 2014. The                 tional Linguistics: Human Language Technologies,
ethics of artificial intelligence. The Cambridge hand-        Volume 1 (Long and Short Papers). Association for
book of artificial intelligence, 1:316–334.                   Computational Linguistics.

                                                         17
István Endrédy and Attila Novák. 2013. More effec-               Eun Seo Jo and Timnit Gebru. 2020. Lessons from
tive boilerplate removal – the GoldMiner algorithm. In           archives: Strategies for collecting sociocultural data in
Polibits.                                                        machine learning. In Proceedings of the 2020 Con-
                                                                 ference on Fairness, Accountability, and Transparency,
Niels Ferguson and Bruce Schneier. 2003. Practical               pages 306–316.
Cryptography. John Wiley & Sons.
                                                                 Jared Kaplan, Sam McCandlish, Tom Henighan,
Casey Fiesler, Nathan Beard, and Brian C Keegan.                 Tom B Brown, Benjamin Chess, Rewon Child, Scott
2020. No robots, spiders, or scrapers: Legal and ethical         Gray, Alec Radford, Jeffrey Wu, and Dario Amodei.
regulation of data collection methods in social media            2020. Scaling laws for neural language models. arXiv
terms of service. In Proceedings of the International            preprint arXiv:2001.08361.
AAAI Conference on Web and Social Media, volume 14,
pages 187–196.                                                   Bryan Klimt and Yiming Yang. 2004. The Enron cor-
                                                                 pus: A new dataset for email classification research.
Timnit Gebru, Jamie Morgenstern, Briana Vecchione,               In European Conference on Machine Learning, pages
Jennifer Wortman Vaughan, Hanna Wallach, Hal                     217–226. Springer.
Daumé III, and Kate Crawford. 2018. Datasheets for
datasets. arXiv preprint arXiv:1803.09010.                       Sosuke Kobayashi. 2018. Homemade bookcor-
                                                                 pus.     https://github.com/BIGBALLON/
Aaron Gokaslan and Vanya Cohen. 2019. Openweb-                   cifar-10-cnn.
text corpus. http://Skylion007.github.io/
OpenWebTextCorpus.                                               Philipp Koehn. 2005. Europarl: A parallel corpus for
                                                                 statistical machine translation. In MT summit, vol-
Authors Guild v. Google. 2015. . Docket No. 13-4829-             ume 5, pages 79–86. Citeseer.
cv, 804:202.
                                                                 Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu,
Katja Grace, John Salvatier, Allan Dafoe, Baobao
                                                                 Dehao Chen, Orhan Firat, Yanping Huang, Maxim
Zhang, and Owain Evans. 2018. When will AI exceed
                                                                 Krikun, Noam Shazeer, and Zhifeng Chen. 2020.
human performance? evidence from AI experts. Jour-
                                                                 Gshard: Scaling giant models with conditional com-
nal of Artificial Intelligence Research, 62:729–754.
                                                                 putation and automatic sharding.    arXiv preprint
David Graff, Junbo Kong, Ke Chen, and Kazuaki                    arXiv:2006.16668.
Maeda. 2003. English gigaword. Linguistic Data Con-
                                                                 Peter J Liu, Mohammad Saleh, Etienne Pot, Ben
sortium, Philadelphia, 4(1):34.
                                                                 Goodrich, Ryan Sepassi, Lukasz Kaiser, and Noam
Declan Groves and Andy Way. 2006. Hybridity in mt:               Shazeer. 2018. Generating wikipedia by summarizing
Experiments on the Europarl corpus. In Proceeedings              long sequences. arXiv preprint arXiv:1801.10198.
of the 11th Annual conference of the European Associ-
                                                                 Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Man-
ation for Machine Translation (EAMT 2006).
                                                                 dar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke
Alexander Halavais. 2019. Overcoming terms of ser-               Zettlemoyer, and Veselin Stoyanov. 2019. RoBERTa:
vice: a proposal for ethical distributed research. Infor-        A robustly optimized BERT pretraining approach.
mation, Communication & Society, 22(11):1567–1581.               arXiv preprint arXiv:1907.11692.

Chris Hardin. 2018. How to shuffle a big dataset.                Edward Loper and Steven Bird. 2002. NLTK: The Nat-
                                                                 ural Language Toolkit. In Proceedings of the ACL
Tom Henighan, Jared Kaplan, Mor Katz, Mark Chen,                 Workshop on Effective Tools and Methodologies for
Christopher Hesse, Jacob Jackson, Heewoo Jun, Tom B              Teaching Natural Language Processing and Computa-
Brown, Prafulla Dhariwal, Scott Gray, et al. 2020. Scal-         tional Linguistics, pages 62–69. Somerset, NJ: Associa-
ing laws for autoregressive generative modeling. arXiv           tion for Computational Linguistics. http://arXiv.
preprint arXiv:2010.14701.                                       org/abs/cs/0205028.
Matthew Hoffman, Francis Bach, and David Blei.                   John MacFarlane. 2006–2020. Pandoc: a universal
2010. Online learning for latent dirichlet allocation.           document converter.
advances in neural information processing systems,
23:856–864.                                                      Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S Cor-
                                                                 rado, and Jeff Dean. 2013. Distributed representations
Dirk Hovy and Shannon L Spruit. 2016. The social im-             of words and phrases and their compositionality. In Ad-
pact of natural language processing. In Proceedings of           vances in Neural Information Processing Systems, vol-
the 54th Annual Meeting of the Association for Com-              ume 26, pages 3111–3119. Curran Associates, Inc.
putational Linguistics (Volume 2: Short Papers), pages
591–598.                                                         Jonathan A Obar. 2020. Sunlight alone is not a disin-
                                                                 fectant: Consent and the futility of opening big data
Ben Hutchinson, Vinodkumar Prabhakaran, Emily                    black boxes (without assistance). Big Data & Society,
Denton, Kellie Webster, Yu Zhong, and Stephen De-                7(1):2053951720935615.
nuyl. 2020. Social biases in NLP models as bar-
riers for persons with disabilities. arXiv preprint              Jeffrey Pennington, Richard Socher, and Christopher D.
arXiv:2005.00813.                                                Manning. 2014. Glove: Global vectors for word repre-


                                                            18
sentation. In Empirical Methods in Natural Language               Carl Shulman and Nick Bostrom. 2020. Sharing the
Processing (EMNLP), pages 1532–1543.                              world with digital minds. preprint.
Vinay Uday Prabhu and Abeba Birhane. 2020. Large                  Kaj Sotala and Lukas Gloor. 2017. Superintelligence
image datasets: A pyrrhic win for computer vision?                as a cause or cure for risks of astronomical suffering.
arXiv preprint arXiv:2006.16923.                                  Informatica, 41(4).
Shawn Presser. 2020. Books3.    https:                            Robyn Speer. 2019. ftfy. Zenodo. Version 5.5.
//twitter.com/theshawwn/status/
1320282149329784833.                                              Merity Stephen, Xiong Caiming, Bradbury James, and
                                                                  Richard Socher. 2016.
Alec Radford, Karthik Narasimhan, Time Salimans,
and Ilya Sutskever. 2018. Improving language under-               Nisan Stiennon, Long Ouyang, Jeffrey Wu, Daniel
standing with unsupervised learning. Technical report,            Ziegler, Ryan Lowe, Chelsea Voss, Alec Radford,
OpenAI.                                                           Dario Amodei, and Paul F Christiano. 2020. Learn-
                                                                  ing to summarize with human feedback. Advances in
Alec Radford, Jeffrey Wu, Rewon Child, David Luan,                Neural Information Processing Systems, 33.
Dario Amodei, and Ilya Sutskever. 2019. Language
models are unsupervised multitask learners. OpenAI                Pedro Javier Ortiz Suárez, Benoît Sagot, and Laurent
Blog, 1(8):9.                                                     Romary. 2019a. Asynchronous pipeline for process-
                                                                  ing huge corpora on medium to low resource infrastruc-
Jack W Rae, Anna Potapenko, Siddhant M Jayakumar,                 tures. In 7th Workshop on the Challenges in the Man-
Chloe Hillier, and Timothy P Lillicrap. 2019. Compres-            agement of Large Corpora (CMLC-7). Leibniz-Institut
sive transformers for long-range sequence modelling.              für Deutsche Sprache.
arXiv preprint.
                                                                  Pedro Javier Ortiz Suárez, Benoît Sagot, and Laurent
Colin Raffel, Noam Shazeer, Adam Roberts, Kather-                 Romary. 2019b. Asynchronous pipeline for process-
ine Lee, Sharan Narang, Michael Matena, Yanqi Zhou,               ing huge corpora on medium to low resource infrastruc-
Wei Li, and Peter J Liu. 2019. Exploring the limits of            tures. In 7th Workshop on the Challenges in the Man-
transfer learning with a unified text-to-text transformer.        agement of Large Corpora (CMLC-7). Leibniz-Institut
arXiv preprint arXiv:1910.10683.                                  für Deutsche Sprache.

Inioluwa Deborah Raji and Jingying Yang. 2019.                    Anja Thieme, Danielle Belgrave, and Gavin Doherty.
ABOUT ML: Annotation and benchmarking on under-                   2020. Machine learning in mental health: A system-
standing and transparency of machine learning lifecy-             atic review of the HCI literature to support the devel-
cles. arXiv preprint arXiv:1912.06166.                            opment of effective and implementable ML systems.
                                                                  ACM Transactions on Computer-Human Interaction
C. Radhakrishna Rao. 1961. Generation of random per-              (TOCHI), 27(5):1–53.
mutations of given number of elements using random
sampling numbers. Sankhyā: The Indian Journal of                 J. Tiedemann. 2016. Finding alternative translations in
Statistics, Series A (1961-2002), 23(3):305–307.                  a large corpus of movie subtitles. Proceedings of the
                                                                  10th International Conference on Language Resources
Radim Rehurek, Petr Sojka, et al. 2011.         Gen-              and Evaluation (LREC 2016).
sim—statistical semantics in python. NLP Centre, Fac-
ulty of Informatics, Masaryk University.                          Trieu H. Trinh and Quoc V. Le. 2018. A simple method
                                                                  for commonsense reasoning. CoRR, abs/1806.02847.
C Rosset. 2019. Turing-NLG: A 17-billion-parameter
language model by Microsoft. Microsoft Blog.                      Hans Van Halteren. 2008. Source language markers in
                                                                  Europarl translations. In Proceedings of the 22nd In-
S. Russell. 2019. Human Compatible: Artificial Intelli-           ternational Conference on Computational Linguistics
gence and the Problem of Control. Penguin Publishing              (Coling 2008), pages 937–944.
Group.
                                                                  Jessica Vitak, Katie Shilton, and Zahra Ashktorab.
David Saxton, Edward Grefenstette, Felix Hill, and                2016. Beyond the Belmont principles: Ethical chal-
Pushmeet Kohli. 2019. Analysing mathematical rea-                 lenges, practices, and beliefs in the online data research
soning abilities of neural models. arXiv preprint                 community. In Proceedings of the 19th ACM Confer-
arXiv:1904.01557.                                                 ence on Computer-Supported Cooperative Work & So-
                                                                  cial Computing, pages 941–953.
Ismaïla Seck, Khouloud Dahmane, Pierre Duthon,
and Gaëlle Loosli. 2018. Baselines and a datasheet                Guillaume Wenzek, Marie-Anne Lachaux, Alexis Con-
for the Cerema AWP dataset.        arXiv preprint                 neau, Vishrav Chaudhary, Francisco Guzmán, Armand
arXiv:1806.04016.                                                 Joulin, and Edouard Grave. 2019. CCNet: Extracting
                                                                  high quality monolingual datasets from web crawl data.
Mohammad Shoeybi, Mostofa Patwary, Raul Puri,                     arXiv preprint arXiv:1911.00359.
Patrick LeGresley, Jared Casper, and Bryan Catanzaro.
2019. Megatron-LM: Training multi-billion parameter               Thomas Wolf, Lysandre Debut, Victor Sanh, Julien
language models using gpu model parallelism. arXiv                Chaumond, Clement Delangue, Anthony Moi, Pierric
preprint arXiv:1909.08053.                                        Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe


                                                             19
Davison, Sam Shleifer, Patrick von Platen, Clara Ma,
Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao,
Sylvain Gugger, Mariama Drame, Quentin Lhoest, and
Alexander M. Rush. 2020. Transformers: State-of-
the-art natural language processing. In Proceedings of
the 2020 Conference on Empirical Methods in Natural
Language Processing: System Demonstrations, pages
38–45, Online. Association for Computational Linguis-
tics.
Ellery Wulczyn, Nithum Thain, and Lucas Dixon. 2016.
Wikipedia detox.
Eliezer Yudkowsky. 2013. Intelligence explosion mi-
croeconomics. Machine Intelligence Research Insti-
tute, accessed online October, 23:2015.
Rowan Zellers, Ari Holtzman, Hannah Rashkin,
Yonatan Bisk, Ali Farhadi, Franziska Roesner, and
Yejin Choi. 2019. Defending against neural fake
news. In H. Wallach, H. Larochelle, A. Beygelzimer,
F. dÁlché-Buc, E. Fox, and R. Garnett, editors, Ad-
vances in Neural Information Processing Systems 32,
pages 9054–9065. Curran Associates, Inc.
Victor Zhou. 2019. Building a better profanity detec-
tion library with scikit-learn.
Yukun Zhu, Ryan Kiros, Rich Zemel, Ruslan Salakhut-
dinov, Raquel Urtasun, Antonio Torralba, and Sanja Fi-
dler. 2015. Aligning books and movies: Towards story-
like visual explanations by watching movies and read-
ing books. In Proceedings of the IEEE international
conference on computer vision, pages 19–27.




                                                         20
Appendices                                                    transparency:
                                                                  1. US Congressional Record. The official
                                                                     record of the United States Congress (1800
A    Contributions
                                                                     – today) records important points of debate at
All authors contributed to the design of the research                the highest levels of American government. It
project and the writing of the paper. Additionally,                  reflects the opinions and biases of the polit-
authors contributed as follows:                                      ical class over the past 200 years, including
                                                                     segregationism and xenophobia. In particular,
Leo Gao led the project, implemented the main                        we found a large quantity of extremely racist
Pile codebase, contributed to the model training                     content that we did not feel appropriate for a
code, performed the evaluations and the language                     dataset intended for general-purpose language
analysis, interpreted the perplexity analysis results,               modeling.
implemented the processing to create the final data,
and processed Pile-CC, PubMed Central, ArXiv,                     2. Fanfiction. Hundreds of GiB of fanfiction
and Ubuntu IRC.                                                      has been written and put online, primarily
Stella Biderman led the data analysis, the broader                   on the websites www.fanfiction.net
impact analysis, and the data documentation, and                     and www.https://archiveofourown.
coordinated the project. She also wrote the anal-                    org/. This represents a significant untapped
ysis of structural statistics, authorial consent, and                resource for language modeling as it is al-
copyright law.                                                       most exclusively short-form fiction, a writing
Sid Black implemented the model training and                         style that is not represented in most language
evaluation code and processed YouTube Subtitles,                     modeling datasets. We ultimately decided to
Stack Exchange, and GitHub.                                          exclude fanfiction on logistical grounds: we
Laurence Golding implemented deduplication,                          found other sources of data that were easier to
performed the n-gram analysis, and processed                         obtain.
OpenWebText2.                                                     3. Literotica. Literotica is a website where users
Travis Hoppe processed FreeLaw, Pubmed Ab-                           can upload short-form erotic fiction. We had
stracts, ExPorter, and PhilPapers.                                   originally planned on including it in the Pile
Charles Foster performed the topic modeling anal-                    and even went as far as scraping and process-
ysis, contributed to the discussion of authorial con-                ing it. However we decided to not include it
sent, and processed USPTO Backgrounds.                               for several reasons. Firstly, once we decided
Jason Phang implemented and performed the GPT-                       to exclude fanfiction, Literotica represented
2/3 perplexity analysis and advised the project.                     our sole source of short-form fiction, which
Horace He performed the bias and sentiment anal-                     would likely lead to undesirable biases in the
ysis.                                                                trained model. Secondly, Literotica would
Anish Thite implemented and performed the pro-                       require significantly more investigation, as-
fanity analysis and processed Hacker News.                           sessment, and care than we spent on the other
Noa Nabeshima processed GitHub.                                      datasets. Thirdly, Literotica contains a signifi-
Shawn Presser processed BookCorpus2.                                 cant amount of stereotyping, including racial
Connor Leahy wrote the alignment implication                         fetishes. While Literotica is likely usable for
analysis and the model training code.                                some tasks, we are not comfortable including
                                                                     it in the Pile.
B   Excluded Datasets
                                                              C     Dataset Details
In the course of building the Pile, we considered
including and ultimately decided to not use sev-              This section contains additional information about
eral datasets. We excluded several datasets on the            each dataset listed in Section 2, including how it
grounds that they were too small to be worth spend-           was obtained, how it was processed, and any other
ing time on or because the English component of               details relevant for replication. The intent of this
the data did not merit inclusion on its own. How-             section is to provide as much detail as possible,
ever we also decided to exclude several data sets             so that Pile can be replicated in the future if nec-
for other reasons, which we document here for                 essary, and so that any future processing of these

                                                         21
and similar datasets can use or improve on our                  jusText’s intended application for text corpora cre-
methods. As such, all code created for processing               ation. In contrast, trafilatura is, for instance, better
has been made publicly available under permissive               at preserving the structure of the website faithfully,
open source licenses and is referenced in footnotes             often correctly extracting elements such as tables,
where applicable.                                               but it kept too much unnecessary boilerplate. Had
                                                                we used trafilatura, we would have required an addi-
C.1   Pile-CC                                                   tional intra-page filtering step to remove boilerplate
We extract Common Crawl using jusText (Endrédy                  from the page.
and Novák, 2013). Our filtering implementation
uses a classifier trained against the OpenWebText2              C.1.3    Languages
dataset. We process only a small fraction of the                While jusText does technically support several
available Common Crawl data; we break the list                  other languages, the quality on those languages
of urls to individual WARC files from 2013 to                   is worse than on English as many constants in the
2020 into 3679 chunks and process 22 random                     algorithm are specifically tuned for English. Ad-
chunks.                                                         ditionally, jusText is completely unable to handle
                                                                languages such as Chinese and Japanese, which do
C.1.1 WARC vs WET
                                                                not use spaces to delimit words.
CommonCrawl data is available in two main for-
mats: Web ARChive (WARC) files, which contain                   Due to the difficulty of maintaining an acceptable
a full record of the crawl as well as the raw HTML              level of extraction quality across all languages, we
of the webpage, and WET files, which contain pre-               decided to restrict the scope of the CC dataset to
extracted versions of the contents of the WARC                  only English and leave a high-quality, fully multi-
files. The WET files have poor quality, often con-              lingual, WARC-based CC-based dataset to future
taining large amounts of boilerplate text like menus            work. To filter for only English, we use the py-
and page footers, but due to the lower bandwidth                cld2 library and only attempt to extract text from
and computation requirements necessary to use                   documents where English is the most common lan-
WET files, prior work based on CC have mainly                   guage.
focused on using WET files while applying clean-
ing such as document level filtering (Brown et al.,             We use pycld2 instead of fasttext because it is ca-
2020; Wenzek et al., 2019), or n-sentence level                 pable of classifying the language from the HTML
deduplication with very aggressive heuristics (Raf-             directly, and since jusText requires knowledge of
fel et al., 2019).                                              the language of the webpage before extraction. Ad-
                                                                ditionally, pycld2 was significantly faster than jus-
We do not believe that document level filtering                 Text, and by only processing with jusText doc-
is sufficient for WET files because many of the                 uments classified as English by pycld2, we re-
issues with WET files stem from intra-document                  duced the required computation by approximately
boilerplate. We also find many of the heuristics                half.
used in Raffel et al. (2019), such as the removal
of all lines without terminal punctuation, the word             Extracting text from websites for language model-
"javascript", and 3-sentence deduplication to be too            ing, especially for multilingual corpora, is highly
aggressive.                                                     nontrivial, and we leave the refinement of such
                                                                extraction to future work.
C.1.2 Extraction
In addition to jusText, we also considered Trafi-               C.1.4    Filtering
latura, Newspaper, Goose3, and DragNet. While                   To filter CC for quality, we follow Brown et al.
we were originally intending on creating an extrac-             (2020) in training a classifier to classify between a
tion benchmark, this proved infeasible given our                known high quality dataset and CC. We use fasttext
available resources, and we chose jusText based on              with an n-gram size of 2. We ran experiments us-
visual inspection of the output. In inspection, we              ing both the entire Pile and just OpenWebText2 as
noticed that jusText has the characteristic that it dis-        the positive examples, with score distributions on
cards more data than many other extractors, which               unseen CC data as shown in Figure 9. We decided
is not a major drawback given the large volume                  to use only OpenWebText2 for positive examples
of CC data available. This was as expected, given               for our final CC data because of the low sensitivity

                                                           22
                  α    Filtering Ratio                            C.4.1 Extractor Choice
                                                                  We chose to use Newspaper instead of jusText for
                  1        0.5894
                                                                  OpenWebText2 for consistency with OpenWeb-
                  2        0.3649
                                                                  TextCorpus. Additionally, by using multiple differ-
                  3        0.2390
                                                                  ent html extractors for different components of the
                  4        0.1671
                                                                  Pile, we reduce the potential impact of systematic
                  5        0.1239
                                                                  biases from any one extractor negatively impacting
                  6        0.0974
                                                                  the dataset.
                  7        0.0802
                  8        0.0685                                 C.5      ArXiv
                  9        0.0602
                                                                  We downloaded the TEX sources of all
                                                                  papers on arXiv up to the July 2020
Table 6: Filtering Ratios (kept:total) of various settings
                                                                  dump (the last file included in our data is
                                                                  arXiv_src_2007_068.tar) via arXiv’s S3
of using the full Pile. We use the same Pareto-                   Bulk Source File Access18 , and used pandoc
distribution thresholding as Brown et al. (2020),                 1.19.2.4 to convert these source files to
with α = 3. Our choice of α targets the filtering                 Markdown, discarding any papers which had errors
ratio necessary to filter our subset of CC to the size            during the conversion process. This yielded a total
we needed. The impact of α on the filtering ratio is              of 1,264,405 papers.
shown in Table 6.                                                 We remove any line beginning with :::, which is
                                                                  used by pandoc to indicate html classes in mark-
C.2    Pubmed Central                                             down.
We use pandoc 1.19.2.4 (MacFarlane, 2006–
                                                                  C.6      GitHub
2020) to convert the JATS format data provided by
PMC to markdown. Afterwards, we remove any                        We separate the data gathering process into two
line beginning with :::, which is used by pandoc                  steps:
to indicate html classes in markdown.                               1. Gathering a list of the desired repositories and
                                                                       their metadata
C.3    Books3
                                                                    2. Extracting all text data useful for language
No additional details.                                                 modeling from each repository

C.4    OpenWebText2                                               For the first step, mirroring the approach of the
                                                                  WebText dataset, we use GitHub ‘stars’ as a proxy
To produce the dataset, URLs and their associated                 for quality, and choose to gather only repositories
metadata were first extracted from all Reddit sub-                with more than 100 stars. For practical reasons, we
missions up to April 2020. URLs were dedupli-                     also limit the list of repositories gathered to reposi-
cated, with each unique URL featuring a list of                   tories with less than 1GB of files. Since Github’s
associated submissions metadata, and an aggre-                    API limits the number of search results to 1000, in
gate score. URLs with an aggregate score of less                  order to comprehensively gather all repositories we
then 3 were removed. The links were then scraped                  need to create many small queries that each return
and processed with Newspaper scraper. Dedupli-                    fewer than 1000 results in such a way that every
cation was performed at the document level using                  repository of interest will be returned by at least
in memory MinHashLSH through the DataSketch                       one of our queries. To achieve this, we bound our
library.                                                          initial search by size to return only repositories be-
                                                                  tween a lower bound of 0 and 5 bytes. At the time
Both filtered and raw versions were produced, with
                                                                  of writing, this returns 965 results. For the next
the raw version only deduplicated by URL. The fil-
                                                                  step, we set our lower bound one above our previ-
tered version contains 65.86 GB of uncompressed
                                                                  ous upper bound, and decide on a new upper bound
text across 17,103,059 documents. The raw version
                                                                  that should also return fewer than 1000 results by
is much larger, at 193.89GB of uncompressed text
                                                                    18
across 69,547,149 documents.                                             https://arxiv.org/help/bulk_data_s3


                                                             23
                       (a) OpenWebText2                                       (b) Full Pile

     Figure 9: Score distribution of documents from Common Crawl given different classifier training data.


                                                              Because we wanted to limit the size of the overall
                                                              Pile, we randomly sampled 95.0 GiB of the 630.64
                                                              GiB of Github data we collected in total and leave
                                                              quality filtering to future work.
                                                              However, we believe code generation will be an in-
                                                              creasingly important component of language mod-
                                                              els as they continue to scale up and increase in their
Figure 10: Left: number of new submissions/year
                                                              ability to generalize. As such, we hope to extend
to arXiv grouped by domain over time.         Right:          this dataset in future work.
fractional submission rates for each of the domains.
Figure     from     https://arxiv.org/help/                   C.7   FreeLaw
stats/2019_by_area/                                           We download the court opinions data in bulk from
                                                              CourtListener,19 and extract the raw text using
                                                              BeautifulSoup.
using the results from our last query to estimate our
new upper bound as (lowerbound+(1000/(n/r)),                  C.8   Stack Exchange
where n is the number of previous results and r is
                                                              To construct the dataset, we download and parse
the range of bounds in the previous step.
                                                              every Stack Exchange database dump to plaintext
This tends not to overshoot, because Github repos-            files. We opt to extract the top three answers
itories follow a power distribution with respect to           with at least three upvotes, discarding all other
size, but if it does, we simply use the amount of             responses. We only include the plain text ques-
repositories our new query returned in order to con-          tion and response and do not incorporate any meta-
struct a new upper bound estimate.                            data. Motivated by large-scale language models’
                                                              few-shot ability (Brown et al., 2020), we provide
Using the gathered list of repositories, we clone             context by prepending all questions and answers
each one, extract any text-based files, and discard           with Q:\n\n and A:\n\n respectively.
the rest. Because some repositories took an imprac-
tical amount of time to clone and/or extract, we set          The resulting dataset contains a total of 15,622,475
a hard time limit of 300 seconds for both the git             documents across a total of 365 Stack Exchanges
cloning and text extraction steps. As such, some              and Meta-Stack Exchanges, the bulk of which is
larger repositories may only be partially extracted.          from StackOverflow.
We also impose a file size limit of 100kB on ex-              C.9   USPTO Backgrounds
tracted files, as we found that the majority of files
over that size were typically very repetitive auto-           The United States Patent and Trademark Office
generated source files or data files, and that setting        (USPTO) has published bulk archives of the full
this file size limit was an effective cleaning step to          19
                                                                   https://www.courtlistener.com/api/
limit the data to code.                                       bulk-info/


                                                         24
text of all patents granted in the US from 1976 to            C.15      Ubuntu IRC
September 2020. From these archives, we extract               We processed all logs from July 5, 2004 through
the Background sections, along with key grant-                September 1, 2020.
specific metadata, such as the inventor, assignee,
and classification information.                               To process the data, all system messages, such
                                                              as joins, disconnects, nick changes, etc. were
The file format used for storing bulk text US patents         discarded, but actions (i.e using /me) were kept.
has changed over time. Prior to 2002, all of the              Timestamps were removed, and all logs for the
datasets are in a specialized format called APS               same channel in a given week were concatenated
(Automated Patent System). Since 2002, the data               into a single document, with each the logs for each
is XML encoded. Partially as a function of this               day prepended with the date if that day’s log is
change, the location of the "Background" section              non-empty.
has also shifted. Our converter accounts for these
structural shifts and extracts the raw text from each         C.16      BookCorpus2
patent’s Background.
                                                              The original BookCorpus consists of 11,038 books.
C.10    PubMed Abstracts                                      However, due to issues with availability of the
                                                              original BookCorpus, as well as the possibility of
About one-third of the articles in the dataset were           collecting a larger version, we decided to collect
missing or contained a malformed title or abstract            our own version of BookCorpus using a similar
and were excluded. Additionally, PubMed Cen-                  methodology as Kobayashi (2018). Our version of
tral (see Section 2.2) contains full-text resources to        BookCorpus contains 17,868 books instead.
many recent publications; any publications which
already appear in PMC are excluded from this set.             We create and use a modified version of the epub-
To process the data, we concatenated the title and            to-text converter in Kobayashi (2018) that:
abstract and removed any copyright information.
The remaining dataset contains 15,518,009 titles                 • Correctly preserves the document structure
and abstracts.                                                     across chapters, matching the table of contents
                                                                   very closely;
C.11    Project Gutenberg
                                                                 • Correctly renders tables of data, whereas by
No additional details.                                             default html2txt produces poor-quality re-
                                                                   sults for tables,
C.12    OpenSubtitles
To create the text dataset, we simply extract the                • Correctly preserves code structure, so that
subtitle text from each XML file in the English                    source code is visually coherent,
language dataset provided by Tiedemann (2016),                   • Converts numbered lists from “1\.” to “1.”
discarding any provided metadata.
                                                                 • Runs         the     full      text     through
C.13    Wikipedia (English)                                        ftfy.fix_text()               (Speer,     2019),
We use the wikipedia/20200301.en dataset                           replacing Unicode apostrophes with ascii
from TensorFlow Datasets.20 We prepend the ti-                     apostrophes and expanding Unicode ellipses
tle to the body of each article, separated by two                  to “...” (three separate ascii characters).
newlines.
                                                              C.17      EuroParl
C.14    DeepMind Mathematics                                  We download the data in bulk from 21 . We re-
We include instances from the Easy, Medium,                   move all basic tag information and only retain
and Hard components of DeepMind Mathemat-                     the name of each document as a title. For ex-
ics, breaking each curriculum item (such as                   ample, <SPEAKER ID=77 LANGUAGE="NL"
algebra__polynomial_roots) into 8 KiB                         NAME="Pronk"> becomes Pronk, and then ex-
chunks.                                                       tract the body of each document, discarding those
                                                              that are shorter than 200 characters.
  20
     https://www.tensorflow.org/datasets/
                                                                21
catalog/wikipedia#wikipedia20200301en                                http://www.statmt.org/europarl/


                                                         25
C.18   HackerNews                                                    educational topics.
We first use the Hackernews BigQuery dataset to                 2. We use requests-html to gather a list of 1000
obtain a list of all story ids in our date range. For              Youtube video IDs for each search term, and
the Pile we use the first Hacker News post (1) to                  deduplicate the resulting video ids across
post number 24531712. This corresponds to a date                   search terms.
range of approximately 10/09/2006 to 09/20/2020.
We use the BigQuery dataset to gather story ids                 3. We use YoutubeTranscriptApi22 to
for efficiency purposes. However, the BigQuery                     gather all human generated closed captions
dataset was lacking some information for stories,                  for every available language for each video.
so we used the official Hacker News API for story                  To align each language in parallel, we split
and comment text retrieval.                                        the captions for each language into parallel
                                                                   minute-long sections by timestamp, and ar-
Hacker News displays and stores comments in a                      range each language in a random order within
tree-like manner, with children comments replying                  these sections, appending the language as a
to parent comments. However, most language mod-                    header to each minute-long section to provide
els require input data to be in a sequential form.                 context. If only a single language is available,
Considering each path through the comment tree                     the output is just the subtitles, with no header
as a sequence could be detrimental, since there will               appended.
be a large amount of near-duplicate comment se-
quences. In addition, only taking one path through            In total, subtitles for 173,651 videos were gath-
the comment tree for each story leaves out a large            ered.
portion of the comment data. Therefore, we parsed
                                                              C.20     PhilPapers
comments in a hybrid form. For every top-level
comment (comments that have no parent comment),               The PhilPapers (PP) are indexed using OAI-MPH,
we create a sequence of comments by traversing                the Open Archives Initiative Protocol for Metadata
down the comment tree from the top-level com-                 Harvesting. As such, the first step to collect the
ment. We choose the next comment by taking the                data is to get the XML for all links. This was done
child comment with the highest number of children             using pyoaiharvester.23
comments (a cheap attempt at taking a long path               From that, each publication is downloaded. Some
through the comment tree, note that it does not take          entries do not exist, or have been removed by
the longest possible path).                                   the authors. Papers with text are extracted using
We consider all stories that have at least one com-           pdfbox, and papers with non-machine readable
ment and are not flagged by the moderators for                text are ignored. Non-English language publica-
potential conduct violations. Since comments are              tions are kept, and the metadata reflects the lan-
stored in HTML, we use the html2text package                  guage reported by the OAI-MPH XML. The text is
to extract the text from the post.                            filtered with pdf_filter.py from PDFextract,
                                                              and we discard any papers with less than 1000 char-
We order each document by listing the title, url,             acters.24
sub-title, and author at the top. Top-level comments
are delimited by "\n----\n" and sub-comment                   C.21     NIH Grant abstracts:
chains are delimited by "\n~~~\n". We include                          ExPORTER
author and extracted text for each comment.                   The NIH provides a bulk-data repository for
                                                              awarded applications through the ExPORTER ser-
C.19   YouTube Subtitles                                      vice covering the fiscal years 1985–present. These
We construct the dataset in three stages:                     data come from the NIH, but also other other Health
                                                              and Human Services agencies (ACF, AHRQ, CDC,
  1. We build a large list of search terms by
                                                              HRSA, FDA), and the VA. Additionally, the NIH
     prompting a GPT-3 model with a manually
                                                                22
     selected list of queries, manually filtering the              https://github.com/jdepoix/
                                                              youtube-transcript-api
     responses, and repeating this process itera-               23
                                                                   https://github.com/vphill/
     tively until a suitable size is reached. The list        pyoaiharvester/
                                                                24
     of terms is centred around, but not limited to,               https://github.com/sdtblck/PDFextract


                                                         26
provides a legacy data format named CRISP for               elements that are also present verbatim in any of
awarded applications during the fiscal years 1970–          the held out data, to prevent leakage.
2009.
                                                            D.1     Weights
We merged both the ExPORTER and CRISP data
to form a consolidated dataset of awarded appli-            Similar to Brown et al. (2020), we increase the
cations. Entries were deduplicated based off their          weight of certain components such that the number
application ID, and excluded if their abstract text         of epochs elapsed on data we consider high quality
was missing or too short. Small grants, especially          is greater than one. Our choice of weights was
administrative ones, consisted solely of short boil-        primarily informed by the source of the data and
erplate. For this reason, we further deduplicated on        the size of the dataset; we attempted to upweight
abstract text. All grants types were considered, in-        academic texts the most, which we felt provided the
cluding new applications (Application Type Code             highest quality data, as well as smaller sets, such
1) and renewals (Application Type Code 2) as the            that they would have a more pronounced impact on
text differed enough to provide novel input. The            the data. We strictly disallowed any data more than
text was then minimally parsed to remove admin-             3 epochs and avoided having any data with more
istrative boilerplate, (ex. most old awards contain         than 2 epochs.
some variation of “description: (provided by appli-
cant)"). In total, there were 939,668 grant applica-        D.2     Deduplication
tion abstracts added.
                                                            Due to memory constraints we did not perform
C.22   Enron Emails                                         Pile wide de-duplication. Instead, de-duplication
To extract the data, we used the mailparser                 was performed at the document level within Open-
package25 to extract the body of each email as a            WebText2 and Pile-CC as those sets were the most
document.                                                   likely to contain duplicate documents.

D    General Data Processing                                The same technique was used for both OpenWeb-
                                                            Text2 and Common Crawl—MinHashLSH with
This section discusses any processes applied across         the Python Datasketch library.26 We used 10 hash
multiple datasets.                                          functions for each Minhash and an approximate
                                                            Jaccard similarity of 0.5. This produced a dupli-
To combine the constituent datasets, we iterate
                                                            cate rate of 28% in OpenWebText2 and 26% for
until the size of the output dataset is the desired
                                                            Common Crawl.
size, drawing documents from datasets at random,
weighted by the number of documents in each                 The main challenge here was computational, lead-
dataset times the number of epochs desired on               ing us on a journey through the various LSH per-
that dataset. Because the number of documents               sistence options. A simple quadratic Minhash com-
involved is high, by the law of large numbers, the          parison of all documents would have taken several
number of copies of each dataset present in the Pile        hundred thousand years, motivating the use of LSH.
is approximately equal to its epoch count.                  Initially, we did not have sufficient RAM for in-
Shuffling a dataset posed a major problem due to            memory LSH and chose to use the Cassandra back-
our limited memory and computational budget. We             end when de-duplicating OpenWebText2. This was
follow Hardin (2018), a method descended from               reasonably fast, but the same method resulted in a
Rao (1961), and interleave our output to produce            corrupted database about 34 of the way through pro-
30 output piles.                                            cessing Common Crawl. After the Cassandra cor-
                                                            ruption, we briefly tested the experimental Mongo
We hold out approximately 10GiB of data from                implementation; however this was quite slow due
the Pile, of which 2GiB are used to create the val-         to the nature of Mongo itself. In the end, we ran
idation and test splits, and the remainder is held          in-memory LSH on a machine with enough RAM
in reserve. From the training set, we remove any            for Common Crawl, taking several days.
  25
     https://github.com/SpamScope/
                                                              26
mail-parser                                                        https://github.com/ekzhu/datasketch


                                                       27
D.3    Downstream Validation Leakage                              Component                 Tokens per byte
To avoid leakage of data from downstream evalu-                                                  (LT /LB )
ations, recent work (Radford et al., 2019; Brown                  Pile-CC                             0.2291
et al., 2020; Shoeybi et al., 2019) has removed any               PubMed Central                      0.3103
data in the training set that may overlap with the                Books3                              0.2477
evaluation metrics. We decided not to perform any                 OpenWebText2                        0.2434
such removal, because it is impossible to antici-                 Arxiv                               0.3532
pate all potential downstream evaluation metrics,                 Github                              0.4412
and so any particular selection of metrics would                  FreeLaw                             0.2622
inevitably either become obsolete as the choice of                StackExchange                       0.3436
benchmarks in the field changes, or potentially hin-              USPTO Backgrounds                   0.2116
der the development of new benchmarks for models                  PubMed Abstracts                    0.2183
trained on Pile.                                                  Gutenberg (PG-19)                   0.2677
For models trained on Pile and evaluated on metrics               OpenSubtitles                       0.2765
other than Pile’s own validation and test sets, we                Wikipedia (en)                      0.2373
encourage authors to remove overlaps between Pile                 DM Mathematics                      0.8137
and the validation data of these additional down-                 Ubuntu IRC                          0.3651
stream evaluations. We do not anticipate that such                BookCorpus2                         0.2430
leakage removal will hurt model performance, as                   EuroParl                            0.3879
the validation sets of most benchmarks are very                   HackerNews                          0.2627
small in relation to the size of the Pile, and so                 YoutubeSubtitles                    0.4349
choosing to evaluate on more metrics will not be a                PhilPapers                          0.2688
disadvantage for any model.                                       NIH ExPorter                        0.1987
                                                                  Enron Emails                        0.3103
E     Investigating data
                                                                  Table 7: Tokens per byte for Pile components
E.1    13-Gram Analysis
As part of our exploratory analysis, we calcu-
lated the counts of all 13-grams across Common              TripAdvisor, SimplyHired, Associated Press, Post-
Crawl. We chose n = 13 due to its use in prior              Media, The FCC etc. PHP error messages and
work (Brown et al., 2020). There were a total of            password login prompts also made an appearance.
40,216,231,078 different 13-grams in this dataset.          It may be of interest to fans of Portal that repeti-
The 1000 most common range from 11 million                  tions of “the cake is a lie .” achieved a
occurrences down to 20k.                                    high count.

The most frequently occurring 13-grams were                 E.2    Benchmark Perplexity
character repetitions used for styling such as                     Computation
“-- --”, “* * * *”, “! ! ! !”, at 11
                                                            To compute the perplexity for a given dataset, we
million, 5.8 million and 1.1 million respectively.
                                                            tokenize each document separately, divide the docu-
Other characters used in this manner include the
                                                            ment into segments of up to the maximum sequence
following: “# . > ?”. In the 264k count
                                                            length of the model (1024 tokens for GPT-2, 2048
range, we see repetitions of badly formatted
                                                            for GPT-3), and predict the logits of the each seg-
HTML escape characters “; &nbsp”, “; amp”.
                                                            ment. The inputs to the model are the immediate
Boilerplate from standard forum software appears
                                                            prior tokens the e.g. for scoring tokens 1 to 1024,
around the 180k occurrences range, such as the
                                                            we provide tokens 0 to 1023 at the input context.
following: “select the forum that you
                                                            The respective language model implementations
want to visit from the selection
                                                            handle the causal attention masking. This ensures
below”.
                                                            that every token in the dataset is scored exactly
Overall, a large amount of common HTML and                  once. This also means that some tokens will have
CSS is included in the top 1000, along with boil-           more input context than others. We then aggregate
erplate text from Amazon Affiliate Advertising,             over the whole dataset and compute the final per-

                                                       28
plexity score. The perplexity for the whole Pile
is computed by aggregating over the constituent
datasets (i.e. weighted by dataset size, not a simple
average of dataset perplexities). Both GPT-2 and
GPT-3 share the same tokenizer and vocabulary,
making the perplexity scores directly comparable.
We use the Hugging Face (Wolf et al., 2020) im-
plementation of GPT-2, and the OpenAI API for
GPT-3. The davinci model in the OpenAI API
is presumed to correspond to a 175B parameter
version of GPT-3.
In Table 8 we show the test set perplexities (i.e. not
normalized by UTF-8 length, as in Table 2). Be-
cause of the costs associated with using the OpenAI
API, we compute test perplexities on only one-tenth                            Figure 12: Percentage of sentences classified as pro-
of the test set in Tables 8 and Table 2. Specifically,                         fane in the Pile. The percentage of the CC component
we randomly sample one-tenth of the documents of                               and the weighted mean of the Pile as a whole are shown
each dataset except for three: Ubuntu IRC, Book-                               as horizontal lines
Corpus2, and PhilPapers. In Table 9, we show
test perplexity computed on the full test set on all
GPT-2 models.                                                                  to catch all the instances of pejorative content, since
                                                                               purposeful misspellings of words could evade the

                7
                         Test loss vs. Log sequence position                   censor and still have the intended effect. Further-
                                                        GPT-2 (small)
                                                                               more, words and their intents are always evolving,
                6                                       GPT-2 (medium)         therefore any list created would likely be always
                                                        GPT-2 (large)
                                                        GPT-2 (xl)             outdated. Another issue pertains to sorting the
                5                                       GPT-3 (ada)
  Loss (nats)




                                                        GPT-3 (babbage)        words into the categories. Words are highly de-
                                                        GPT-3 (curie)
                4                                       GPT-3 (davinci)        pendent on their context, so a word would change
                                                                               categories with different contexts.
                3

                2                                                              F     Data Samples
                     0       2        4        6       8        10             The following consists of two random, non-
                              Sequence Position Log2 (tokens)
                                                                               cherrypicked 512-byte samples from each con-
Figure 11: Test loss (log perplexity) over the Pile, buck-                     stituent dataset of the Pile, sampled from the vali-
eted by position in the input sequence based on the                            dation split.
model’s maximum sequence length. To smooth out the
lines, we bucket 4 positions per plotted datapoint. (e.g.                      F.1    Pile-CC
positions 0–3, positions 2044–2047). Later tokens are
predicted with more context and thus see lower perplex-                              pot trending topics and the coverage around them. First up, there’s a bit of
ities.                                                                               a visual redesign. Previously, clicking on a trending topic would highlight
                                                                                     a story from one publication, and you’d have to scroll down past a live
                                                                                     video section to view related stories. Facebook is replacing that system
                                                                                     with a simple carousel, which does a better job of showing you different
                                                                                     coverage options. To be clear, the change doesn’t affect how stories are
E.3                 Pejorative Content                                               sourced, according to Facebook. It’s still the same algorithm pickin

Initially we decided on separating pejorative con-
tent into 4 groups: sex-related terminology, slurs,                                  e public safety. He said the bridge saves commuters two or three minutes
                                                                                     when trains pass – and those minutes could be vital.
neither of these categories, and both of these cate-
                                                                                     “Two to three minutes may not mean much if you’re just driving
gories. We adapted a public "naughty words" list                                     home from work, but if you’re the one waiting for an ambulance to get to
                                                                                     your home, if you’re the one waiting for a fire truck to get to your home,
and broke them into these categories with the in-                                    if you’re the one waiting for a police car to get to your home, those two
                                                                                     to three minutes could mean the difference between life or death,” Sharp
tern of looking at the proportion of each category                                   said. “That’s what this pro

in each dataset. However, this provided many is-
sues.
                                                                               F.2    PubMed Central
First, any blacklist of words would be hard-pressed

                                                                          29
      d a suitable substitute for the advice of a qualified health care                            \mbox{ if } 2\leq x\leq 3
      professional. Do not disregard or avoid professional medical advice due                      \end{array}\right.$$ is lower semicontinuous and the nonemptiness
      to content published within Cureus.                                                          of ${\operatorname{fix}}\Phi$ is guaranteed by Corollary \[cor:fixed
                                                                                                   point\]. Notice that ${\operatorname{fix}}\Phi=[1,2]$. Nevertheless
      Introduction                                                                                 the Kakutani fixed point Theorem does not apply since ${\operator-
      ============                                                                                 name{gph}}\Phi$ is not closed.

      Total knee arthroplasty (TKA) is a promising treatment for end-                              On the converse, the set-valued map $\Phi:[0,3]\rightrightarrows
      stage osteoarthritis (OA) of the knee for alleviating pain and restoring                     [0,3]$ $$\Phi(x):=\left\{\begin{array}{ll}
      the function of the knee. Some of the cases with bilateral TKA are                           \{1\} & \mbox{ if } 0\leq x<1\\
      symptomatic, necessitating revision arthroplasty in both the knees. A                        {}[1,2] & \mbox{ if } 1\leq x\leq 2\\
      bilateral revision TKA can be done ei                                                        \{2\} &



      ent\’s ability to make judgements and decisions about their work                             .eps){width="6.5cm"}
      experiences and learning that will position them as future critical
      thinkers, life longer enquirers and learners.                                                ![Gamma-ray spectrum at Mt. Norikura (2.77 km a.s.l). The vertical axis
                                                                                                   is Flux$\times Eˆ2$. Our data is at $<$ 100 GeV. Data above 300 GeV is
      Conclusion {#jmrs290-sec-0014}                                                               from emulsion chamber experiments. For the latter, see Sec.\[discuss\]
      ==========                                                                                   []{data-label="norispec"}](norikura.eps){width="7.5cm"}

      Identification of the core capabilities that our stakeholder com-                            ![The altitude variation of the flux integrated over 6 GeV. The
      munity rate highly has proved informative in assisting us to describe a                      dpmjet3.03 and fritiof7.02 give almost the same feature consistent with
      "work ready *plus"* medical imaging graduate for the New Zealand                             the observation while the deviation of fritiof1.6 from the data is obvious.
      context. The results have provided data to the curriculum development                        \[trans
      team allowing them




F.3    Books3                                                                                F.6    Github

                                                                                                   "enabled", out.enabled);
      cept of _forçage_ , ’a forcing of language enacted by the advent of an                       }
      "other" language that is at once immanent and created’, 44as Badiou puts
      it: this opens up vistas of a truly syntactic analysis of the poem, in which,                std::string      SMTPServerInfoJSONStringSerializer::serialize(const
      again, Badiou would be close to his philosophical other, Deleuze, who,                       SMTPServerInfo &in,
      as we just saw, defines style through a-grammaticality and who tries to                      const SecurityContext &sc)
      define what he calls an ’intensive line of syntax’.45                                        {
                                                                                                   return SMTPServerInfoJSONSerializer::serialize(in, sc).dump(4);
      Nevertheless, the insistence on syntax as guarantee involves a                               }
      _seventh paradox_ , the parad
                                                                                                   void                               SMTPServerInfoJSONStringSerial-
                                                                                                   izer::unserialize(SMTPServerInfo &out,
                                                                                                   const std::string &in,
      rnment, before the Second World War there were 5,300 communities                             const SecurityContext &sc)
      and two million burakumin. The BLL thinks there must be at least three                       {
      million burakumin living in Japan today.                                                     retur
      We visited a hall in Osaka where a taiko drum group, made up
      exclusively of young burakumin, were about to start their weekly
      rehearsal. The small gymnasium was filled with taiko drums of all sizes.
                                                                                                   lose">
      The smallest was about the size of a snare drum, the largest about the
                                                                                                   <at-form state="vm.form" autocomplete="off" id="external_test_form">
      size of a compact car. The Japanese drum group Kodo have made th
                                                                                                   <at-input-group col="12" tab="20" state="vm.form.inputs" form-
                                                                                                   id="external_test"></at-input-group>
                                                                                                   <at-action-group col="12" pos="right">
                                                                                                   <at-action-button
                                                                                                   variant="tertiary"
F.4    OpenWebText2                                                                                ng-click="vm.onClose()"
                                                                                                   >
                                                                                                   {{::vm.strings.get(’CLOSE’)}}
      prime minister to repatriate all the police sent to Catalonia before the                     </at-action-button>
      referendum.                                                                                  <at-action-button
                                                                                                   variant="primary"
      What were the results?                                                                       n

      With nearly all votes counted, the pro-independence parties To-
      gether for Catalonia (JxCat), Republican Left of Catalonia (ERC) and
      Popular Unity (CUP) were on course to win a total of 70 seats in total,
      giving them a majority in the new parliament.                                          F.7    FreeLaw
      Citizens (Cs) had 25.3% of the vote, winning 37 seats in the
      135-seat chamber.
                                                                                                   ssible, and further, that the weight of the evidence, the credibility of the
      Its leader told the BBC her party had been "victorious".                   Ms                witnesses and the persuasive effect of the testimony is for the sole deter-
      Inés Arrima                                                                                  mination of the trier of fact.
                                                                                                   This Court thus uses the same interpretation of V.R.C.P. 52(a) as it did
                                                                                                   *487 under the previous statutory requirement found in 12 V.S.A. § 2385.
                                                                                                   In essense, the defendants urge that this Court should reconsider the case
      so accommodate Stablecoins.                                                                  of Green Mountain Marble Co. v. Highway Board, supra, and follow the
                                                                                                   Federal practice of looking to the evide
      While some analysts opined that Stablecoins are created to bring
      growth into the crypto space, they are becoming a solid way to reduce
      crypto volatility due to the fact that their value are pegged to fiat currency.
                                                                                                   ng to the fact that
      For Low Cost and Almost Instant Across Border Remittance                                     the relevant Arkansas statutes and rules provide for criminal sanctions
                                                                                                   against school
      When Stellar-based Wirex stablecoins finally launches, they are                              officials who fail to enforce the immunization requirements, the Morn-
      going to be used to perfect low-cost and all most immediately                                ingstar and
      cross-border remittance, just like the IBM Stablecoin which has received                     Lake Hamilton School Districts characterized themselves as disinterested
      support fr                                                                                   bystanders
                                                                                                   caught in the crossfire between the Schoolchildren and the Officials. See
                                                                                                   Ark. Code
                                                                                                   Ann. § 6-18-702(c)(2)(B) (2000) (“Any school official, parent, or
                                                                                                   guardian violating
F.5    ArXiv                                                                                       the regulations shall be subject to the penalties imposed herein.”); Id




                                                                                        30
F.8     Stack Exchange                                                                       F.11      PubMed Abstracts

       ooks like a fancy wheel, When resetting rotation from 360deg to 0 deg, It                    ent (REM) latency were found to be significantly worse in Group 1 as
       animating the wheel in anti-clockwise direction, How to Avoid this???                        compared with Group 2. Cognitive and executive parameters were signif-
       HTML                                                                                         icantly impaired in Group 1. Shorter total sleep time, poorer sleep effi-
       <ul class="cm">                                                                              ciency, and prolonged sleep latencies were observed to be associated with
       <li><span>01</span></li>                                                                     poor memory and executive function in patients with refractory epilepsy.
       <li><span>02</span></li>                                                                     Our study strongly suggests that sleep disturbances, mainly shorter total
       <li><span>03</span></li>                                                                     sleep time, poor sleep efficiency, and prolonged sleep latencies, are asso-
       <li><span>04</span></li>                                                                     ciated
       <li><span>05</span></li>
       <li><span>06</span></li>
       <li><span>07</span></li>
       <li><span>08</span></li>                                                                     neurons in vesicular GABA transporter (VGAT)-venus transgenic mouse.
       </ul>                                                                                        Inhibitory neurons play important roles in a number of brain functions.
                                                                                                    They are composed of GABAergic neurons and glycinergic neurons, and
       SCSS                                                                                         vesicular GABA transporter (VGAT) is specifically expressed in these
       $Brdr: #7d868c;                                                                              neurons. Since the inhibitory neurons are scattered around in the CNS,
       *{                                                                                           it is difficult to identify these cells in living brain preparations. The glu-
       -webkit-box-sizing: border-box;                                                              tamate decarboxylase (GAD) 67-GFP knock-in mouse has been widely
       -moz-box-sizing: border-box;                                                                 used for the identif
       box-sizing: border-box;



       w can I solve it?                                                                     F.12      Gutenberg (PG-19)
       Yesterday I added Google ReCAPTCHA v3 in one of my
       client’s Shopify website, but I don’t think that it is working because he is
       still reporting to receive several spam e-mails.                                             s he met with as a novelist, he was anxious to prosecute his
       I’ve followed Google’s guide, but I don’t know what to do for "Verifying                     original profession of medicine; and having procured from a foreign
       user response" part of the guide. I’m not an expert in coding.                               university the degree of M.D., he commenced to practise physic in
       Basically I’ve added this code to the theme.liquid file                                      Chelsea, but without success. He wrote, however, an essay "On the
       <script src="https://www.google.com/recaptcha/api.js?render=*site key                        External Use of Water," in which he seems to have partly anticipated
       provided by google*"></script>                                                               the method of the cold-water cure. In 1753 he published his
                                                                                                    "Adventures of Count Fathom;" and, two years later, encouraged by a
       And then I’ve added th                                                                       liberal subscription, he issued a translation of "Don



                                                                                                    Yearn;
F.9     Wikipedia (en)                                                                              Its Advertising brought us such Renown,
                                                                                                    We jumped Three Hundred Thousand, on that Turn!"


       and the third son of John Bland and Elizabeth née Birch, daughter of                         XXXVI
       Robert Birch, Bland was educated at Trinity College, Cambridge, where
       he graduated as a Bachelor of Arts in 1825, and a Master of Arts in                          I think the man exaggerated some
       1829. He was called to the Irish Bar in 1829, becoming a member of the                       His increased Circulation,–but, I vum!
       Queen’s Counsel in 1854.                                                                     If I could get Two Thousand for one Tale,
                                                                                                    I’d write him Something that would simply Hum!
       In 1840, he married Charlotte Elizabeth Grove Annesley, daugh-
       ter of Arthur Grove Annesley and Elizabeth née Mahon, and they had at
       least one child: John Loftus Bland (1841–1908). After Charlotte’s death                      XXXVII
       in 18
                                                                                                    For I remember, shopping by the way,
                                                                                                    I saw a Novel writ by Bertha Clay;
                                                                                                    And there was scrawled across its Title-Page,
       heart of the University campus, a meeting-place for all academic                             "This is the Stuff that Sells–so People say!"
       disciplines, improving its opportunities to co-operate across traditional
       academic boundaries. It also gives USBE-students an opportunity to take
       an active part of student environment created for the 37 000 students at                     XXXVIII
       Umeå University.
                                                                                                    Listen–a moment listen!–Of the same
       Organization                                                                                 Wood-pulp on wh

       Umeå School of Business, Economics and Statistics has three
       departments:   the Department of Business Administration, the
       Department of Economics and the Department of Statistics.

       USBE Career Cent
                                                                                             F.13      OpenSubtitles

                                                                                                    ad for you." " Too bad for me?" "How about too bad for you?" "Oh
                                                                                                    no!" "Luckily I keep a spare." "Look everyone!" "My winky was a key!"
F.10      USPTO Backgrounds                                                                         "Oh dear, bloody Dutchman." "Foxxy, I’m coming!" "Don’t do anything
                                                                                                    stupid or the shooting begins." "Austin, take Ducky I’ll stay here and
                                                                                                    be your backup." "Ducky, what do we do?" "I’m not really a "hands-on-
                                                                                                    evil-genius"." "Think you were always the smart one." "I could re-write
       nductivity types), it is necessary that at least some process is steps differ-               the output capacity to the tractorbeam from one of the conduit boxes up
       entiate between p-type and n-type transistors. Separate implant steps, for                   there." "Come on, let’s
       example, are needed to define n-well and p-well structures and to dope
       the source/drain regions of n-channel and p-channel transistors. When-
       ever possible, however, it is generally desirable to use a single process
       step to define transistor features regardless of the transistor type. Single                 ." "this calls for... four people." "Yes!" "we got it." "guys." "We got it."
       process steps imply a single mask step, which is always desirable to                         " Got what?" " Our sub." " Did he say sub?" " Mm-hmm." "Only private
                                                                                                    sub on the Florida coast rated for 300 fathoms." "Sub as in submarine?"
                                                                                                    "Following up on your haloclines." "so we’re going to have to drive all
                                                                                                    night... if we’re going to be there by morning." "Anybody have trouble
       enser further comprising a means of identifying the user by voice recog-                     sleeping in a car?" "whoa." "Wait a minute." "What happened to the nice
       nition. Also, an object is dispenser further comprising a means of identi-                   offices in Canaveral City?" "Mr. Benirall expects you to take ’em." "we
       fying a supervisor by voice recognition.                                                     just go
       Furthermore, an object is a dispenser further comprising a means of cus-
       tomizing the plurality of aural messages for instructing the user during
       each of the plurality of washing steps.
       An object of the invention is a dispenser for metering a liquid cleanser to
       a user and prompting the user in compliance with a recommended wash
                                                                                             F.14      DM Mathematics


                                                                                        31
       3651*w**2 + 519*w + 1                                                                    e notebook didn’t have lines for me to write with like some notebooks
       Find the second derivative of -91419126*m**2 - 162128943*m.                              have. I hated that notebook and I hated writing into it. I was glad to
       -182838252                                                                               throw that damn thing out even if it was unfinished. Ugh.
       Find the third derivative of 5*l*u*y**3 + l*u*y - 5*l*y**2 -
       4621073*u*y**3 - 1755838*u*y**2 + u wrt y.                                               I was urged by voice "You to go take your pills and eat food."
       30*l*u - 27726438*u                                                                      but I refused on calling mom.
       Find the third derivative of 317297018*s**3 + 3136*s**2 - 30884*s wrt
       s.                                                                                       I should have listened to the voice’s suggestion because mom
       1903782108                                                                               picked up the phone at eight forty five in the morning and hogged me to
       What is the third derivative of -16525*f*r**3 + 20*f*r + 356*r**3 +                      ten o’clock is when she finally quit. Ugh hence voice picking onto me
       1425730*r**2 wrt r?                                                                      when I got off
       -99150*f + 2136
       What is the second derivative of 199836725*j**2 - 443399*j - 462 wrt j?
       399673450
       What is the derivative of
                                                                                         F.17      EuroParl
       the nearest integer?
       5                                                                                        račun prometne varnosti in visokih cen? Danes želimo izvedeti, kako in
       What is 783451 to the power of 1/3, to the nearest integer?                              kdaj bomo integrirali razvrščanje zgornjega zračnega prostora ter kako
       92                                                                                       bomo skupaj upravljali spodnji zračni prostor v prihodnosti. Ali se lahko
       What is the fourth root of 6322907 to the nearest integer?                               odkrito določijo ovire za vzpostavitev funkcionalnih blokov nad evrop-
       50                                                                                       skim ozemljem? Ali je mogoče osvetliti politično voljo držav članic, da
       What is the ninth root of 4723626 to the nearest integer?                                izpolnijo svoje obveznosti? Prav tako nas skrbi, da pristop od spodaj navz-
       6                                                                                        gor ne bo uspel, ker v treh letih države članice niso razvile funkcionalnih
       What is 4954939 to the power of 1/2, to the nearest integer?                             blok
       2226
       What is 625583 to the power of 1/3, to the nearest integer?
       86
                                                                                                om ekonomisk styrning som vi debatterar inom kort kommer att vara my-
       What is 1105849 to the power of 1/3, to the nearest integer?
                                                                                                cket viktigt. Vi vet mycket väl att det är på gång i vårt lagstiftningsför-
       103
                                                                                                farande, och vi hoppas att vi kommer att vara klara så snabbt som möjligt.
       What is the fourth root of 4820344 to the nearest integer?
                                                                                                Vad kan jag sammanfattningsvis säga? Hela paketet som vi undertecknar
       47
                                                                                                i dag kommer att börja gälla i Europeiska unionen från och med den 1
       What is the seventh root of 243476 to the neare
                                                                                                januari 2011, alltså mycket snart. Det är viktigt för oss alla, såväl för
                                                                                                marknaderna som för våra medborgare, att förstå att avsikten med paketet
                                                                                                är att hj


F.15       HackerNews
                                                                                         F.18      YoutubeSubtitles
       ced lists I email don’t get formatted correctly. It’s
       slightly annoying for such an otherwise beautifully designed layout.
                                                                                                science term
       ——                                                                                       for a mixture of things
       ajcronk                                                                                  that don’t usually mix.
       There is a typo in the url at the end of the How did your day go? email.                 The things in this case
       Should be ohlife.com/today, not ohlife.come/today                                        are water and fats.
                                                                                                Under normal circumstances,
       ~~~                                                                                      fats and water repel each other,
       sgupta                                                                                   but milk also contains complex
       Thanks for the heads up!                                                                 protein chains called caseins
                                                                                                that are made up of both
       ——                                                                                       hydrophilic, or water loving,
       a3_nm                                                                                    and lipophilic, or fat loving, particles.
       How exactly is this service better than, say, a simple text file on my own               When presented with both water and fats,
       machine with a daily reminder set up through some other means?                           caseins grab bits of fat and cluster up
                                                                                                into globules called micelles,
       Why would I want to use some third-party website for some-                               with the fat on the inside
       thi                                                                                      and the hydrophilic bits on the outside.
                                                                                                The hydr


       or Amazon EC2 and Amazon SQS. The bandwidth tier in which you will
       be                                                                                       SE WE KIND OF ARE MORE,
       charged each month will be calculated based on your use of each of these                 HIPPY, I GUESS MAYBE IN SOME OF
       services separately, and could therefore vary across services."                          THE THINGS THAT WE DO.
                                                                                                AND THEY WERE JOKING AND THEY
       ——                                                                                       WERE LIKE, "OH WE HEARD ABOUT
       yaacovtp                                                                                 THIS TOWN IT’S LIKE THIS
       Can anyone tell me what bandwidth costs a month once you need over a                     SUSTAINABLE CITY THERE’S SOLAR
       terabyte                                                                                 PANELS, YOU GUYS WOULD LOVE IT."
       a month? How would you host a 5-10 mb movie that may be viewed                           AND I LOOKED IT UP AND I WAS
       millions of                                                                              LIKE I REALLY ACTUALLY DO LOVE
       times without using a 3rd party video host like youtube etc?                             THIS TOWN.
                                                                                                >> Sreenivasan: JOSHUA, A
       ~~~                                                                                      PHYSICAL THERAPIST, GOT A JOB AT
       especkman                                                                                THE LOCAL HEALTH CENTER IN THE
       Lots of dedicated hosts will include a 2-5 TB of transfer a                              TOWN’S COMMERCIAL HUB BEFORE
                                                                                                THEY MOVED IN.
                                                                                                IT’S WHERE THE FIRST BUILDINGS
                                                                                                WENT UP.
                                                                                                THERE’S ALSO A RESTAURANT AND
F.16       BookCorpus2                                                                          COFFEE SH



       considerate of me, you’re right. I apologize." Kate smiled in what she
       hoped was a winning way. She teetered over to the counter on heels that
       were too high and put down her things with a sigh of relief.
                                                                                         F.19      Ubuntu IRC
       Althea, who would not reveal her age but was probably some-
       where in her late sixties, patted her dark-dyed helmet of hair and                       emingly wlan related) <Snappy:New> <linux-raspi2 (Ubuntu):New for p-
       straightened the flowing turquoise silk jacket she was wearing over white                pisati> <https://launchpad.net/bugs/1627643>
       capris and a white tank. "Well. It just seems to me that as the _owner_ ,                <ppisati> ogra_: or we punch a hole in the dev image so we can login via
       you should try to set some sort of                                                       the serial console and check what’s really going on
                                                                                                <ppisati> ogra_: yes
                                                                                                <ogra_> well, i wanted to play with systemd console but didnt have time




                                                                                    32
       for that yet
       <ogra_> \o/                                                                                Carol, I
       <ogra_> something at least ... that kernel looks fine
       <ppisati> ogra_: good to know
       <ogra_> do you have an SRU bug that i can tag verification-done ?
       <ogra_                                                                                     —-Original Message—–
                                                                                                  From: "Prakash Narayanan" <pnarayan@andrew.cmu.edu>@ENRON
                                                                                                  Sent: Sunday, December 02, 2001 9:28 PM
                                                                                                  To: Kaminski, Vince J
       problem with this? Like, if teenage boy wants to have nekkid lady wall-                    Cc: Crenshaw, Shirley
       papers, maybe he don’t want it to come up on family computer... Dunno,                     Subject: Talk on Friday
       maybe it’s not an issue?"
       <swilson> hi there! yes, i believe that a bug has been created which raises                Dear Vince
       this same issue - about embarrassing or confidentiality issues with this                   How are you? I understand that things are extremely hectic for you right
       <swilson> this seems to be a bit of an edge case, but it may be significant                now
       enough to warrant giving some careful thought                                              but I was wondering if we are going ahead as schedulef on friday. It
       <imnichol> Or if you have bank info on your screen before it’s locked                      would
       #ub                                                                                        be great to hear from you.
                                                                                                  Best Regards
                                                                                                  Prakash

                                                                                                  Prakash Narayanan
F.20      PhilPapers                                                                              412-422-3287 (Home)
                                                                                                  412-607-5321 (Mobile)
                                                                                                  6315 Forbes Avenue
                                                                                                  Apartment # 809
       intersubjectivity and self-consciousness was already emphasized by                         Pittsburg
       Sartre. Forthcoming in Grazer Philosophische Studien 84 (2012), p. 75-
       101 15 Thus, to use Rochat’s terminology, from this point onwards, the
       child has "others in mind" (Rochat 2009). The child now begins to un-
       derstand that she is a subject that can be observed by others, just like she
       can observe the behavior of others, and she can begin to consider others’
       perspectives on herself. It is at this point that the child begins to fully                              StackExchange
       apprecia
                                                                                                                OpenWebText2

       d an entire chapter detailing the remarkable achievements of Ashkenazi                                          Pile-CC
       Jews and hold them up as exhibit A in the argument that human evolution
       has been, in Wade’s words, recent, copious, and regional. The example                                          FreeLaw
       of Ashkenazi evolution is supposed to show the absurdity of the view,
       held by authors like Jared Diamond and Stephen Jay Gould, that human                                            Books3
       evolution either stopped one hundred thousand years ago or that natural
       selection has somehow continued to sculpt the bodies but not the brains
       of different gro                                                                                         Wikipedia (en)
                                                                                                                                                             0.10
                                                                                                                  HackerNews
                                                                                                                 OpenSubtitles
F.21      NIH ExPorter
                                                                                                               PubMed Central                                0.05
       rapies that can inhibit the EMT, but few assays for EMT inhibitors in                                 PubMed Abstracts
       high throughput screens (HTS) have developed. A change in fibroblast
       growth factor receptor 2 (FGFR2) splicing occurs during the EMT and
       using an innovative luciferase-based splicing reporter assay we previously
                                                                                                                  Enron Emails                               0.00
       carried out a genome-wide high throughput cDNA expression screen for
       regulators of this splicing switch. This screen identified the epithelial cell                             BookCorpus2
       type specific splicing regulators ESRP1 and ESRP2 demonstrating the
       feasibility of                                                                                    USPTO Backgrounds
                                                                                                                                                               0.05
                                                                                                                         ArXiv
       l and behavioral research projects utilizing primates residing in a semi-
       natural habitat. This population has the most extensive computerized de-                               YoutubeSubtitles
       mographic and genetics database available to researchers anywhere in the
       world. The population management program for CS has been designed to                                            Github                                  0.10
       optimize the health and well-being of the monkeys, to enhance the value
       of the colony for research. In addition, the goal is to provide healthy ani-
       mals to the scientific community for biomedical research, including AIDS                                     PhilPapers
       and Sl
                                                                                                             Gutenberg (PG-19)
                                                                                                                      EuroParl
F.22      Enron Emails                                                                                             Ubuntu IRC
                                                                                                                  NIH ExPorter
       want to make sure that my vacation time gets paid at 100%
       before I go down to the 90% level. Thanks for taking care of this. As you
       can see, I now have access to my e-mail so when I’m not pumping,
                                                                                                              DM Mathematics
       feeding,
       changing diapers, etc... I acn be checking up on things!!!
                                                                                                                                   male      female

       Carol St. Clair
       EB 3892                                                                               Figure 13: The average sentiment co-occurrence with
       713-853-3989 (Phone)
       713-646-3393 (Fax)                                                                    each gender across all datasets.
       carol.st.clair@enron.com



       Suzanne Adams
       07/18/00 05:22 PM

       To: Carol St Clair/HOU/ECT@ECT
       cc: Taffy Milligan/HOU/ECT@ECT
       Subject: Re: Carol St. Clair




                                                                                        33
                                                                              34




                                                                      1.00
     StackExchange
     OpenWebText2
            Pile-CC                                                   0.75
           FreeLaw
            Books3
     Wikipedia (en)                                                   0.50
       HackerNews
      OpenSubtitles
    PubMed Central                                                    0.25

  PubMed Abstracts
       Enron Emails
                                                                      0.00
       BookCorpus2
 USPTO Backgrounds
              ArXiv                                                    0.25
   YoutubeSubtitles
            Github
         PhilPapers                                                    0.50
  Gutenberg (PG-19)
           EuroParl
        Ubuntu IRC                                                     0.75

       NIH ExPorter
   DM Mathematics
                                                                       1.00
                      Muslim Christian Atheist Buddhist Hindu   Jew


Figure 14: The average sentiment co-occurrence with
each religious word across all datasets. Each dataset’s
sentiments have been normalized by the maximum
norm sentiment for that dataset.
                                                                                                              35




 Component                                GPT-2                                        GPT-3
                           small    medium        large      xl         ada     babbage        curie   davinci
 Pile-CC                 26.8894    20.5671    18.1656    16.9572    16.2430    13.0270    10.7532      8.4929
 PubMed Central          11.0626     8.9052     8.0454     7.5404     6.8800     5.7006     4.9390      4.3143
 Books3                  28.3889    22.0958    19.3424    17.7833    15.4209    12.4220    10.1526      7.1927
 OpenWebText2            23.6764    17.6175    15.1314    13.6267    12.0063     9.5439     7.7706      5.9163
 ArXiv                   14.2804    11.1896    10.0904     9.3330     7.5551     6.1541     5.2537      4.5341
 Github                  16.6814     7.9322    16.6742    13.3337     3.9614     3.1660     2.7398      2.4240
 FreeLaw                 16.1000    11.7518    10.8427    10.0965     8.7976     7.0366     5.8256      4.8926
 Stack Exchange          13.7202     9.3405     8.8467     8.3238     7.6652     5.9486     5.0267      4.3796
 USPTO Backgrounds       15.1141    11.9232    10.5878     9.8095     9.2775     7.7000     6.5849      5.6411
 PubMed Abstracts        20.5642    15.2379    13.1190    11.9355    13.2112    10.4188     8.5861      7.1604
 Gutenberg (PG-19)       26.4947    17.8975    16.4722    16.5112    12.5709     9.6349     7.7940      6.3112
 OpenSubtitles           22.7418    18.5724    17.0868    16.2709    16.2174    13.8561    11.8836      9.8578
 Wikipedia (en)          27.0237    19.7570    17.4856    16.7849    12.9112     9.9453     7.8363      5.6915
 DM Mathematics           9.8990     8.7389     8.2928     7.9772     7.2458     6.5231     6.0171      5.6020
 Ubuntu IRC              33.3028    26.1203    22.6128    20.9461    12.1138     9.6995     8.0628      6.5679
 BookCorpus2             25.0743    19.9725    17.6343    16.2905    16.1530    13.1796    11.0885      9.2205
 EuroParl                62.8981    36.9757    28.6198    23.4294     6.4996     5.3282     4.4982      3.8327
 HackerNews              45.0915    29.2599    32.0796    33.9774    22.1295    17.6314    14.6582     12.1283
 YoutubeSubtitles        25.7794    18.8173    15.9002    14.3104     8.4740     6.6394     5.4510      4.5235
 PhilPapers              30.1129    23.0288    20.3755    18.5649    14.4730    11.6785     9.6797      7.9915
 NIH ExPorter            23.9004    18.2298    15.9850    14.6371    16.1417    12.8744    10.6573      8.8110
 Enron Emails            34.7954    23.4353    25.7138    23.9791    16.8190    13.6043    11.6473      9.7655
 The Pile                18.0878    13.2253    12.9177    11.8633     9.7355      7.8456     6.5904     5.4508

Table 8: Test perplexity of the Pile using GPT-2 and GPT-3. Evaluation is performed on one-tenth of the test data
of the Pile, on a per-document basis.
                                                                                                36
        Component                                               GPT-2
                                               small     medium            large    xl
        Pile-CC                                26.5            20.3         17.9   16.7
        PubMed Central                         10.3             8.3          7.6    7.1
        Books3                                 27.9            21.3         18.5   17.0
        OpenWebText2                           23.5            17.5         15.1   13.6
        ArXiv                                  13.7            10.7          9.7    9.0
        Github                                 16.5             8.1         16.7   13.5
        FreeLaw                                15.9            11.6         10.8   10.1
        Stack Exchange                         13.7             9.4          9.0    8.4
        USPTO Backgrounds                      16.6            13.0         11.5   10.6
        PubMed Abstracts                       20.9            15.4         13.3   12.1
        Gutenberg (PG-19)                      37.8            24.9         22.8   24.3
        OpenSubtitles                          22.1            18.1         16.6   15.8
        Wikipedia (en)                         27.0            19.8         17.5   16.8
        DM Mathematics                          9.9             8.7          8.3    7.9
        Ubuntu IRC                             33.3            26.1         22.6   20.9
        BookCorpus2                            25.1            20.0         17.6   16.3
        EuroParl                               63.9            41.9         33.5   27.7
        HackerNews                             43.7            28.3         30.9   32.4
        YoutubeSubtitles                       25.3            18.8         16.2   14.8
        PhilPapers                             30.1            23.0         20.4   18.6
        NIH ExPorter                           23.2            17.7         15.5   14.2
        Enron Emails                           22.0            15.4         18.6   18.1
        the Pile                               18.4            13.3         13.1   12.0

                Table 9: Full Test Perplexity of the Pile using GPT-2.

                                Male               Female
                                general            little
                                military           married
                                united             sexual
                                political          happy
                                federal            young
                                great              soft
                                national           hot
                                guilty             tiny
                                criminal           older
                                former             black
                                republican         emotional
                                american           worried
                                major              nice
                                such               live
                                offensive          lesbian


    Table 10: Top 15 most biased adjectives/adverbs for each gender

Muslim             Christian    Atheist            Buddhist          Hindu         Jew
islamic            adrian       religious          static            indian        little
international      available    agnostic           final             single        white
new                great        such               private           free          natal
american           high         liberal            interested        asian         common
black              bible        likely             central           more          false
western            good         much               chinese           united        poor
best               old          less               japanese          real          demonic
radical            same         least              noble             other         german
regional           harmonious   political          complete          british       romantic
entire             third        moral              full              cultural      unlicensed
national           special      scientific         fundamental       social        stupid
own                hispanic     rational           udisplaycontext   lower         nuclear
syrian             biblical     skeptic            familiar          local         african
bad                original     skeptical          beneficial        general       hard
guilty             happy        intellectual       native            most          criminal


    Table 11: Top 15 most biased adjectives/adverbs for each religion
                                                                                                                                                                     37
                                           White             Black               Asian                 Hispanic
                                           indian            unarmed             international         likely
                                           rich              civil               western               african
                                           aboriginal        scary               chinese               american
                                           great             federal             japanese              mexican
                                           old               diary               best                  united
                                           superior          political           european              cervical
                                           good              amish               foreign               spanish
                                           little            nigerian            eastern               potential
                                           same              concerned           secondary             better
                                           red               urban               dietary               medical
                                           stupid            historical          open                  more
                                           live              literary            grand                 new
                                           equal             criminal            vietnamese            educational
                                           eternal           worst               russian               young


                         Table 12: Top 15 most biased adjectives/adverbs for each demographic



                                            White             Black              Asian                 Hispanic
                                            -0.114            -0.148             -0.028                -0.024

                              Table 13: Average sentiment co-occurence of each demographic


Component           Topic #1          Topic #2          Topic #3           Topic #4              Topic #5            Topic #6        Topic #7        Topic #8
Pile-CC             Generic           Politics          Generic            Technical             Leisure             Generic         Plants          Entertainment
PubMed Central      Cells             Cells             Cells              Cells                 Cells               Cells           Cells           Cells
Books3              Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
OpenWebText2        US Politics       Law               Sports             Education             Business            Tech            US Religion     Generic
ArXiv               Data              Math              Modeling           Math                  Physics             Physics         Math            Dynamics
Github              Unknown           Programming       Unknown            Java                  C/C++               Unknown         Go              Unknown
FreeLaw             Appeals           Appeals           Legal              Legal                 Appeals             Legal           Legal           Appeals
Stack Exchange      Software          Unknown           Server             Programming           Applications        File System     Programming     Users
USPTO Backgrounds   Data              Electronics       Devices            Unknown               Data                Unknown         Chemistry       Data
PubMed Abstracts    Organ Trans-      Nervous           Animal Study       Animal Study          Ophthalmology       Bacteria        Pulmonology     Fluids
                    plant             System
Gutenberg (PG-19)   Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknowne
OpenSubtitles       Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
Wikipedia (en)      Education         International     Sports             Sports                Entertainment       Entertainment   Logistics       Science
                                      Politics
DM Mathematics      Calculation       Probability       Calculation        Solving               Calculation         Calculation     Probability     Calculation
Ubuntu IRC          Bugs              Pull Requests     Bugs               Bugs                  Bugs                Bugs            Bugs            Pull Requests
BookCorpus2         Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
EuroParl            International     International     International      International         International       International   International   International
                    Politics          Politics          Politics           Politics              Politics            Politics        Politics        Politics
HackerNews          Generic           Software          Generic            Generic               Software            Generic         Generic         Generic
YoutubeSubtitles    Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknowne
PhilPapers          Logic             Science           Science            Mind                  Science             Epistemology    Logic           Science
NIH ExPorter        Cells             Disease           Cells              Cells                 Clinical            Clinical        Unknown         Clinical
Enron Emails        Email             Email             Email              Email                 Email               Email           Email           Business


                                                        Table 14: Topic Summaries


Component           Topic #9          Topic #10         Topic #11          Topic #12             Topic #13           Topic #14       Topic $15       Topic #16
Pile-CC             Education         Politics          Home               Business              Geography           Sports          Medicine        Generic
PubMed Central      Cells             Cells             Cells              Cells                 Cells               Cells           Cells           Cells
Books3              Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
OpenWebText2        Drugs             Sports            Geogrpahy          Crime                 Military            Unknown         Research        Sports
ArXiv               Dynamics          Math              Physics            Physics               Physics             Physics         Math            Modeling
Github              Unknown           HTML/CSS          HTML/CSS           C/C++                 Java                C/C++           Unknown         HTML/CSS
FreeLaw             Legal             Legal             Legal              Legal                 Legal               Legal           Legal           Appeals
Stack Exchange      Programming       HTML/CSS          Programming        Programming           HTML/CSS            Java            SQL             Java
USPTO Backgrounds   Imaging           Electronics       Unknown            Unknown               Data                Imaging         Imaging         Chemistry
PubMed Abstracts    Human      Dis-   Research          Human       Dis-   Clinical              Clinical            Medical Imag-   Cells           Cells
                    ease                                ease                                                         ing
Gutenberg (PG-19)   Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
OpenSubtitles       Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
Wikipedia (en)      Sports            Geography         Entertainment      Unknown               Geography           Sports          History         Law
DM Mathematics      Calculation       Differentiation   Differentiation    Solving               Simplification      Calculation     Units           Unknown
Ubuntu IRC          Software          Software          Software           Bugs                  Software            Pull Requests   Software        Bugs
BookCorpus2         Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
EuroParl            International     International     International      International         International       International   International   International
                    Politics          Politics          Politics           Politics              Politics            Politics        Politics        Politics
HackerNews          Generic           Generic           Generic            Software              Software            Generic         Generic         Generic
YoutubeSubtitles    Unknown           Unknown           Unknown            Unknown               Unknown             Unknown         Unknown         Unknown
PhilPapers          Epistemology      Science           Logic              Science               Epistemology        Science         Logic           Logic
NIH ExPorter        Cells             Cells             Disease            Disease               Disease             Disease         Disease         Clinical
Enron Emails        Energy            Email             Email              Email                 Email               Email           Computer        Computer


                                                 Table 15: Topic Summaries (continued)
Component           Topic #1          Topic #2      Topic #3      Topic #4       Topic #5      Topic #6      Topic #7      Topic #8
Pile-CC             like              people        said          system         new           like          water         music
                    time              said          like          surface        dating        time          plants        like
                    good              government    time          x              art           game          food          book
                    use               war           got           high           day           good          climate       new
                    want              right         going         second         city          food          plant         film
PubMed Central      cells             cells         study         study          data          patients      patients      cells
                    data              cell          cells         data           study         cells         study         data
                    study             data          c             patients       patients      study         data          cell
                    cell              figure        data          cells          cells         cell          cells         analysis
                    results           et            group         analysis       c             analysis      analysis      patients
Books3              time              like          like          said           said          said          said          said
                    said              said          said          like           like          like          like          new
                    like              time          time          time           time          time          way           like
                    new               man           new           know           new           new           new           time
                    know              way           right         new            way           good          time          man
OpenWebText2        said              said          team          people         said          data          people        like
                    trump             court         season        like           government    use           law           world
                    president         law           game          said           year          google        american      time
                    house             case          said          school         market        system        god           people
                    state             state         players       life           business      new           world         day
ArXiv               case              let           function      let            phys          let           let           time
                    given             function      case          set            data          model         given         case
                    time              case          let           following      energy        field         case          let
                    let               given         state         number         field         system        number        set
                    data              order         model         x              b             energy        theorem       given
Github              y                 return        void          return         const         fa            err           import
                    d                 function      f             public         typename      var           return        msgstr
                    b                 div           license       int            return        span          nil           msgid
                    abbr              var           v             case           void          file          func          insert
                    j                 value         countries     null           template      key           error         license
FreeLaw             court             court         court         court          court         court         court         court
                    trial             state         defendant     district       trial         defendant     defendant     state
                    evidence          case          state         plaintiff      evidence      trial         case          evidence
                    case              trial         states        defendant      defendant     evidence      law           defendant
                    state             evidence      trial         motion         united        states        motion        district
Stack Exchange      run               data          function      array          device        file          file          q
                    q                 option        server        int            spring        image         line          like
                    server            pdf           use           value          android       files         error         use
                    project           q             thread        like           app           echo          import        user
                    use               rails         client        code           boot          path          python        set
USPTO Backgrounds   signal            invention     invention     pressure       data          high          al            invention
                    system            data          surface       system         system        air           et            circuit
                    invention         power         having        invention      memory        light         invention     data
                    memory            voltage       present       cells          information   invention     present       present
                    line              frequency     liquid        use            devices       temperature   water         signal
PubMed Abstracts    liver             activity      species       dose           retinal       strains       p             activity
                    group             nerve         study         mg             eye           isolates      levels        acid
                    acute             stimulation   studies       rats           lens          resistance    patients      high
                    transplantation   induced       associated    effects        corneal       resistant     blood         water
                    renal             muscle        risk          effect         laser         bacteria      increased     concentration
Gutenberg (PG-19)   said              said          said          said           said          said          said          man
                    time              time          man           time           great         man           man           said
                    little            little        time          great          like          time          time          like
                    man               like          great         man            man           like          little        time
                    great             man           men           little         little        day           like          little
OpenSubtitles       know              like          know          know           know          know          know          know
                    right             know          oh            like           right         like          right         got
                    come              come          right         oh             like          right         yeah          right
                    got               right         yeah          got            oh            got           got           like
                    like              want          like          right          want          come          let           oh
Wikipedia (en)      category          people        category      championship   film          category      category      system
                    university        government    players       category       category      music         railway       category
                    school            category      people        driver         films         album         station       energy
                    american          political     football      cars           new           song          line          work
                    college           chinese       born          car            television    released      new           systems
DM Mathematics      let               letters       collect       let            let           let           factors       solve
                    pm                let           terms         suppose        common        solve         prime         remainder
                    minutes           replacement   positive      solve          calculate     suppose       replacement   divided
                    factor            sequence      assuming      nearest        suppose       base          letters       calculate
                    divided           prob          simplify      c              highest       calculate     list          true
Ubuntu IRC          ubuntu            ubuntu        like          ubuntu         ubuntu        like          ubuntu        ubuntu
                    like              bug           ubuntu        like           like          ubuntu        like          good
                    think             like          know          think          think         think         bug           snap
                    bug               think         created       need           yeah          good          use           use
                    need              snap          ok            yeah           know          yeah          know          like
BookCorpus2         said              said          said          said           said          said          said          said
                    like              like          know          like           like          like          like          know
                    time              know          like          time           time          know          time          time
                    know              way           time          know           know          time          know          like
                    eyes              eyes          right         going          going         head          going         going
EuroParl            european          european      mr            european       european      commission    european      european
                    mr                president     european      mr             mr            president     commission    commission
                    commission        commission    president     president      commission    european      mr            mr
                    president         mr            commission    commission     president     mr            president     union
                    europe            union         parliament    energy         parliament    parliament    council       parliament
HackerNews          like              like          like          people         people        like          like          people
                    people            people        people        time           like          people        people        like
                    work              work          work          like           time          work          time          work
                    time              time          time          way            think         time          think         good
                    use               use           think         work           use           think         work          use
YoutubeSubtitles    like              know          like          like           like          like          like          like
                    know              like          going         going          think         know          know          people
                    going             going         right         guest          people        going         think         know
                    think             people        time          people         know          look          right         going
                    right             time          know          think          going         host          going         time
PhilPapers          theory            philosophy    case          self           theory        case          derivation    case
                    case              case          science       case           science       theory        reduction     de
                    φ                 moore         theory        science        physical      science       φ             set
                    reduction         physical      set           theory         de            s             paradox       science
                    paradox           theory        world         analysis       case          epistemic     ψ             theory
NIH ExPorter        cells             cell          cell          research       cells         studies       research      study
                    cell              studies       research      determine      specific      development   study         research
                    studies           research      gene          health         cell          patients      development   clinical
                    research          cells         development   specific       study         analysis      specific      studies
                    study             study         study         cells          aim           clinical      use           development
Enron Emails        subject           pm            pm            enron          subject       subject       hou           final
                    pm                subject       new           e              enron         pm            pm            enron
                    new               enron         enron         mail           said          enron         subject       schedule
                    time              cc            time          new            sent          database      e             energy
                    energy            know          image         subject        image         sent          time          information


                                                        Table 16: Topic Terms
Component           Topic #9     Topic #10       Topic #11    Topic #12     Topic #13     Topic #14    Topic $15    Topic #16
Pile-CC             students     said            home         use           said          game         health       people
                    school       state           room         business      new           team         medical      like
                    work         government      house        data          city          season       care         know
                    university   law             hotel        information   years         year         treatment    think
                    research     court           area         new           police        said         body         life
PubMed Central      cells        data            cells        study         study         cells        patients     study
                    expression   cells           study        data          p             study        study        cells
                    patients     patients        cell         p             cells         data         cells        patients
                    cell         study           data         fig           c             time         et           cancer
                    study        c               figure       cells         patients      group        data         figure
Books3              said         said            said         said          said          said         said         said
                    like         like            like         like          like          like         time         time
                    time         time            time         time          time          new          like         new
                    man          know            way          new           people        people       man          people
                    good         way             new          know          man           man          new          like
OpenWebText2        drug         like            city         said          game          flight       study        v
                    cannabis     time            new          police        war           caption      research     granada
                    drugs        new             unlockable   people        party         aircraft     time         club
                    marijuana    game            building     man           military      add          climate      m
                    women        way             said         old           said          water        found        cent
ArXiv               time         let             let          let           model         let          x            let
                    function     number          set          theorem       order         phys         let          model
                    r            model           space        given         energy        order        time         data
                    model        system          model        case          let           model        field        set
                    al           theorem         given        x             phys          case         set          function
Github              string       x               end          define        void          int          return       var
                    license      z               values       software      value         struct       self         assert
                    def          divide          list         copyright     public        return       size         text
                    public       var             color        include       return        case         long         label
                    import       y               table        endif         class         static       string       check
FreeLaw             court        court           court        court         court         court        court        court
                    defendant    â               plaintiff    defendant     district      plaintiff    trial        states
                    state        law             state        states        states        state        state        district
                    trial        case            case         plaintiff     case          case         defendant    united
                    plaintiff    state           evidence     case          united        district     case         trial
Stack Exchange      x            text            code         b             div           string       table        android
                    y            color           n            q             page          return       select       new
                    q            width           use          class         function      public       question     public
                    d            font            int          n             var           new          like         import
                    c            height          include      k             form          class        q            void
USPTO Backgrounds   image        device          invention    invention     data          optical      image        invention
                    light        invention       material     present       network       surface      light        layer
                    data         layer           light        device        system        device       device       substituted
                    optical      film            method       object        user          invention    sheet        et
                    system       power           high         provide       information   system       display      group
PubMed Abstracts    women        health          bone         patients      patients      method       cells        binding
                    patients     data            asthma       treatment     disease       artery       cell         protein
                    positive     care            vaccine      group         study         surface      expression   receptor
                    hiv          based           study        clinical      cases         energy       gene         dna
                    cancer       study           sperm        patient       age           optical      protein      beta
Gutenberg (PG-19)   said         said            said         said          tr            said         time         tr
                    little       man             man          great         said          man          said         said
                    time         little          little       little        man           great        men          man
                    man          like            time         man           time          time         man          time
                    old          time            great        like          little        like         like         little
OpenSubtitles       know         like            know         know          know          know         know         know
                    right        know            like         come          right         right        right        like
                    got          right           come         got           like          oh           like         right
                    like         think           right        oh            yeah          like         think        want
                    oh           oh              good         right         come          come         come         got
Wikipedia (en)      align        category        category     category      category      season       category     category
                    season       new             game         population    county        team         century      new
                    points       state           film         species       district      league       war          states
                    game         united          series       age           references    player       new          law
                    right        states          video        oil           village       nfl          de           american
DM Mathematics      common       let             derivative   let           let           base         digit        let
                    let          derivative      wrt          suppose       suppose       c            terms        suppose
                    divided      wrt             find         solve         value         common       collect      derivative
                    calculate    second          express      b             b             picked       thousands    c
                    factor       find            rearrange    c             simplify      b            let          determine
Ubuntu IRC          ubuntu       ubuntu          ubuntu       like          ubuntu        ubuntu       ubuntu       like
                    like         like            think        ubuntu        like          like         like         ubuntu
                    time         need            like         think         think         think        think        need
                    think        use             yeah         use           work          yeah         good         ok
                    snap         snap            use          need          time          yes          à            juju
BookCorpus2         said         said            said         said          said          said         said         said
                    like         like            like         like          like          like         like         like
                    know         know            know         time          know          eyes         know         know
                    right        time            eyes         know          going         time         time         looked
                    time         going           time         going         time          going        going        going
EuroParl            mr           european        mr           european      european      european     european     european
                    commission   mr              european     mr            commission    mr           mr           mr
                    president    president       commission   commission    mr            commission   commission   parliament
                    european     commission      parliament   president     parliament    parliament   parliament   commission
                    iran         parliament      president    parliament    president     president    president    president
HackerNews          people       like            people       use           like          people       like         like
                    like         people          like         like          people        time         people       time
                    think        time            data         work          time          like         time         people
                    time         think           time         time          work          work         use          think
                    use          use             work         think         data          good         think        use
YoutubeSubtitles    like         like            like         like          like          like         like         like
                    know         time            host         think         think         know         know         know
                    people       know            guest        know          right         want         going        people
                    going        going           know         people        know          going        people       think
                    time         think           look         going         people        right        look         going
PhilPapers          theory       theory          φ            theory        epistemic     theory       φ            case
                    s            science         reduction    case          science       case         derivation   φ
                    case         set             theory       order         belief        science      reduction    s
                    belief       de              paradox      space         theory        physics      t            derivation
                    experience   philosophy      derivation   new           system        theories     paradox      theory
NIH ExPorter        cells        research        disease      cells         cells         research     cell         research
                    research     cells           research     cell          specific      cells        research     studies
                    specific     cell            study        study         development   studies      cells        clinical
                    studies      studies         cells        disease       studies       cell         specific     determine
                    role         study           cell         human         research      project      studies      cancer
Enron Emails        time         subject         hou          image         subject       hou          space        hou
                    new          pm              enron        enron         message       enron        alias        disk
                    enron        friday          subject      pm            pm            subject      disk         space
                    power        sent            cc           hou           know          cc           enron        alias
                    subject      october         na           subject       cc            gas          said         e


                                              Table 17: Topic Terms (continued)
