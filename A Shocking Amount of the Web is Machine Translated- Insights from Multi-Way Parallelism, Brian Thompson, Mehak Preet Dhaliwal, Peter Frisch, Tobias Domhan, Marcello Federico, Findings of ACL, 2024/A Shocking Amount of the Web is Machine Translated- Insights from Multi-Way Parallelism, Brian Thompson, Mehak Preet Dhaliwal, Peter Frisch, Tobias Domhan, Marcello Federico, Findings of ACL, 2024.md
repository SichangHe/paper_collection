                                                           A Shocking Amount of the Web is Machine Translated:
                                                                   Insights from Multi-Way Parallelism

                                        Brian Thompson,∗ 1 Mehak Preet Dhaliwal,† 2 Peter Frisch,1 Tobias Domhan,3 Marcello Federico1
                                                               1
                                                                 AWS AI Labs 2 UC Santa Barbara 3 Amazon
                                                                           brianjt@amazon.com



                                                                  Abstract                                                                  74.5
                                                                                                                                     75.0




                                                                                                                 CometQE Score ( )
                                               We show that content on the web is often trans-
                                                                                                                                     72.5            72.7
                                               lated into many languages, and the low quality
                                                                                                                                                            70.4
                                               of these multi-way translations indicates they                                        70.0
arXiv:2401.05749v2 [cs.CL] 5 Jun 2024




                                               were likely created using Machine Translation                                                                       68.3
                                               (MT). Multi-way parallel, machine generated                                           67.5
                                               content not only dominates the translations in
                                               lower resource languages; it also constitutes a                                               2        3-4 5-7 8+
                                               large fraction of the total web content in those                                                  Multi-way Parallelism
                                               languages. We also find evidence of a selection
                                               bias in the type of content which is translated            Figure 1: The more languages a sentence has been trans-
                                               into many languages, consistent with low qual-             lated into (“Multi-way Parallelism”), the lower quality
                                               ity English content being translated en masse              the translations are, suggesting a higher prevalence of
                                               into many lower resource languages, via MT.                machine translation. See § 4.4 for more details.
                                               Our work raises serious concerns about train-
                                               ing models such as multilingual large language
                                               models on both monolingual and bilingual data              a large fraction of the total web content in those
                                               scraped from the web.                                      languages. We also find evidence of a selection
                                                                                                          bias in the type of content which is translated into
                                           1    Introduction                                              many languages, and therefore over represented in
                                                                                                          lower resource languages: This content is shorter,
                                           Modern AI is enabled by huge amounts of training               more predictable, and has a different topic distri-
                                           data, typically several hundred billion tokens to a            bution compared to content translated into a single
                                           few trillion tokens (Sun et al., 2021; Chowdhery               language. A limited investigation suggests this se-
                                           et al., 2023; Touvron et al., 2023; Almazrouei et al.,         lection bias is the result of low quality content gen-
                                           2023). Training at this scale is only possible with            erated in English (likely produced to generate ad
                                           web-scraped data.                                              revenue) and translated en masse into many lower
                                              We explore the effects that the long-term avail-            resource languages via MT (again, likely to gener-
                                           ability of low cost Machine Translation (MT) has               ate ad revenue).
                                           had on the web.1 We show that content on the                      Our findings raise numerous concerns for multi-
                                           web is often translated into many languages, and               lingual model builders: Fluency (especially across
                                           the quality of these multi-way translations indi-              sentences) and accuracy are lower for MT data,2
                                           cates they were primarily created using MT: see                which could produce less fluent models with more
                                           Figure 1. Machine generated, multi-way parallel                hallucinations, and the selection bias indicates the
                                           translations not only dominate the total amount of             data may be of lower quality, even before consid-
                                           translated content on the web in lower resource lan-           ering MT errors. Data quality is crucial in Large
                                           guages where MT is available, it also constitutes              Language Model (LLM) training, where high qual-
                                               ∗
                                                 Corresponding author                                     ity corpora like books and Wikipedia articles are
                                               †
                                                 Work conducted during an internship at Amazon.
                                              1                                                              2
                                                Free MT has been available online since late 1997 (Gas-        MT technology has improved dramatically over the last
                                           pari and Hutchins, 2007), around the same time that MT re-     decade, but still falls short of human quality (Freitag et al.,
                                           searchers began scraping the web for training data (Resnik,    2023). MT content has been added to the web over many years
                                           1998), and commercial systems have been available since the    using MT systems available at the time, so much of the MT
                                           1970s (Hutchins, 1995).                                        on the web is likely very low quality by modern standards.
typically upsampled several times (Brown et al.,         3     Corpus Creation: MWccMatrix
2020; Gao et al., 2020; Rae et al., 2021; Le Scao
et al., 2022).                                           We create a multi-way parallel representation of
   Our findings also help to explain why low-            the web, consisting of translation tuples contain-
resource MT (Khan et al., 2017; Duh, 2018; NLLB          ing two or more sentences in different languages
Team et al., 2022) is challenging, and why filtering     which are translations of each other.5 As a trivial
noise (Khayrallah and Koehn, 2018) from web-             example, (“hello”, “hola”) in English-Spanish and
scraped bitext (Junczys-Dowmunt, 2018; Chaud-            (“hello”, “olá”) in English-Portuguese combine to
hary et al., 2019) is beneficial for MT training         make (En:“hello”, Es:“hola”, Pt:“olá”). We denote
(Koehn et al., 2018, 2019, 2020; Sloto et al., 2023).    this corpus Multi-Way ccMatrix (MWccMatrix).
   To enable analysis, we create the largest multi-         We iterate through all bitext in ccMatrix, from
way corpus to date, consisting of 6.4B unique sen-       highest to lowest LASER margin score, adding sen-
tences in 90 languages. We release code to repro-        tence pairs as new tuples in MWccMatrix when
duce our corpus and analysis.3                           neither sentence is already in the new corpus, and
                                                         expanding tuples already in the new corpus when
2       Related Work                                     one sentence or the other (but not both) is already
                                                         present. This deduplicates the corpus (i.e. adds
Our work is inspired by several recent efforts           each unique sentence only once), but allows for
which seek to understand the characteristics of          more than one sentence in the same language to
large scale corpora (Mehmood et al., 2017; Dodge         be added to a given tuple, which tend to differ
et al., 2021; Kreutzer et al., 2022; Brannon et al.,     primarily in punctuation/capitalization (i.e. near
2023). Many works have detected machine transla-         duplicates). Therefore, we remove all but the first
tion (Kurokawa et al., 2009; Arase and Zhou, 2013;       sentence added to each tuple in a given language.
Aharoni et al., 2014), but we are not aware of prior     Deduplication across language pairs brings the total
work using multi-way parallelism to do so. Freitag       number of sentences down from 21.7B total sen-
and Firat (2020) explored multi-way parallelism          tences (10.9B sentence pairs) to 7.9B unique sen-
with the goal of improving multilingual MT.              tences in 2.2B tuples, and near duplicate removal
   Exploring multi-way parallelism on the web re-        brings it down to 6.4B. Pseudocode and a descrip-
quires a curated representation of translated content    tion of the optimizations required to make corpus
from the web. We build upon ccMatrix (Schwenk            creation tractable are provided in Appendix A.
et al., 2021), which is in turn based on Com-
mon Crawl.4 Common Crawl is a long running               4     Analysis
web-scraping project which maintains a free, open
source repository of web-scraped data. ccMatrix is       4.1    Much of the Web is Translated
created by embedding Common Crawl sentences
into a multilingual space using LASER (Artetxe           We compared the total number of unique sentences
and Schwenk, 2019) and then finding bilingual            (before removing near-duplicates) in MWccMatrix
translation pairs using fast approximate nearest         to the total number of unique sentences from the
neighbor search (Johnson et al., 2019). We choose        Common Crawl snapshots that the data is based on,
ccMatrix over a corpus from a traditional bitext         as reported by Schwenk et al. (2021). They only
mining process of document alignment (Resnik             report the number of unique sentences for the 54
and Smith, 2003; Buck and Koehn, 2016; Thomp-            (of 90) largest resource languages, so we cannot
son and Koehn, 2020) followed by sentence align-         compute the fraction of sentences with one or more
ment (Gale and Church, 1993; Sennrich and Volk,          translations in the 36 lowest-resource languages.
2010; Thompson and Koehn, 2019) because it is the        The percentage of unique monolingual sentences
largest corpus available at the time of writing (in      which have at least one translation is quite high,
both number of sentences and language coverage).         even for some high resource languages (e.g. 9.4%
                                                         of English, 17.5% of French): see Figure 2.
    3
      https://github.com/amazon-science/
multi-way-parallel-ccmatrix/.         Corpus creation        5
                                                               Unless otherwise noted, we use the term “translation” to
has been optimized to run in about one day on a single   mean a sentence which appears in a translation tuple – i.e.
i4i.32xlarge AWS instance.                               we do not attempt to distinguish whether that sentence was
    4
      https://commoncrawl.org/                           translated into or out of a given language.
                                50                                                        Parallelism    De      En     Fr      Ja    Zh
  % Sents With 1+ Translation                                                             2             95.2   103.7   96.8   25.2   27.8
                                40                                                        3-4           90.4    86.0   88.7   23.6   24.8
                                                                                          5-7           82.6    71.2   80.5   23.2   22.8
                                                                                          8+            71.6    59.9   70.0   22.3   19.1
                                30
                                                                                   Table 2: Sentence length (in characters) as a function of
                                20                                                 multi-way parallelism, in several languages. Multi-way
                                                                                   parallelism is associated with shorter content.
                                10
                                                                                   in length (see Table 2) and have lower perplexity
                                     1010        109       108       107           (i.e. are easier to predict) as measured by GPT-2
                                            Unique Monolingual Sents               (Radford et al., 2019): see Figure 4.
Figure 2: Fraction of the total monolingual data used to
create ccMatrix with one or more translation, in the 54                            4.4     Multi-way Parallel Translations are
languages for which we can compute it. See Appendix B                                      Lower Quality
for a larger plot with language codes.
                                                                                   We evaluate the quality of translations on the web
     Parallelism                        # tuples    % tuples   # sents   % sents   using Quality Estimation (QE), with the CometQE
                                                                                   model (Rei et al., 2022), across different levels of
     2                                      1,368     62.5%     2,736     42.9%
     3-4                                      573     26.2%     1,895     29.7%    multi-way parallelism. Modern quality estimation
     5-7                                      177      8.1%     1,004     15.7%    methods are nearly on par with reference-based
     8+                                        70      3.2%       745     11.7%
                                                                                   metrics (Freitag et al., 2023) and have been shown
     Total                                  2,188   100.0%      6,379    100.0%    to perform well on noisy web data (Peter et al.,
                                                                                   2023). As QE does not require human annotation
Table 1: MWccMatrix statistics. Numbers in millions.
                                                                                   or human references, it allows us to evaluate a very
37.5% of tuples are multi-way parallel, but 57.1% of all
sentences come from multi-way parallel tuples.                                     large data sample (1M samples per language pair)
                                                                                   and many language pairs.7
                                                                                      We find that highly multi-way parallel transla-
4.2                             Translations on the Web are Highly                 tions are significantly lower quality (6.2 CometQE
                                Multi-way Parallel                                 points worse) than 2-way parallel translations. This
Of the 6.38B sentences in our 2.19B translation                                    trend is consistent across all 8 language pair direc-
tuples, 3.63B (57.1%) are in multi-way parallel6                                   tions we considered: see Table 3. Since length
(3+ languages) tuples: see Table 1. Lower resource                                 could interact with cometQE scores, we verified
languages tend to be more multi-way parallel, with                                 that these results also hold across sentence length:
the 10 highest-resourced languages in ccMatrix                                     see Figure 5.
having an average parallelism of 4.0, and the 10                                      We also investigate how LASER margin score
lowest-resource languages in ccMatrix having an                                    varies with multi-way parallelism. Multi-way par-
average parallelism of 8.6 (see Appendix C for all                                 allel data tends to have higher margin scores: see
languages), and this increase is driven by an in-                                  Figure 6. Further investigation reveals that LASER
crease in highly multi-way parallel (8+) sentences:                                has a strong bias for MT output over human transla-
see Figure 3.                                                                      tions (see Table 4), thus LASER margin scores for
                                                                                   more multi-way parallel content are consistent with
4.3                             Multi-way Parallel Data is Shorter and
                                                                                   multi-way parallel data being MT. LASER’s prefer-
                                Simpler
                                                                                   ence for MT is likely because LASER is based on
We perform monolingual analysis to explore how                                     a small MT model. Similar phenomenon has been
data varies with multi-way parallelism. We find                                    observed (Freitag et al., 2021) in the Prism metric
that more multi-way parallel sentences are shorter                                 (Thompson and Post, 2020a,b), which is also based
           6
     We use “multi-way parallelism” (or simply “parallelism”)                      on an MT model.
to refer to the size of the translation tuple that that sentence
                                                                                      7
is in. For example, a sentence with parallelism of 5 comes                              We select from WMT language pairs as CometQE is
from a tuple of size 5, which contains the given sentence plus                     trained on WMT annotations, thus we expect CometQE to be
translations in 4 other languages.                                                 most accurate in those language pairs.
                  109




                                                                                                                                                                                                        Fraction Multi-Way Parallel
                  108                                                                                                                                                                             0.8
Total Sentences



                  107
                                                                                                                                                                                                  0.6
                  106
                                                                                                                                                                                                  0.4
                  105
                  104                                                                           Parallelism:                                                                                      0.2
                                                                                                       3-4
                                                                                                       5-7
                  103                                                                                  8+
                                                                                                                                                                                                  0.0
                             En Fr Pt Ru Pl Cs Ja Zh Sk El Da Ar Bg Fa Uk Ca Lt Et Bn Ta Gl Eu Mk Si Is Sw Mr Ast Ne Mg Fy Oc Sd Jv Km Su So Yi Ha Yo Ig Or Gd Xh Lg
                               Es De It Nl Sv Tr Id Vi Ro Hu Fi No Ko Sl He Sr Hi Lv Sq Hr Ms Ml Eo Ur Af Tl Be Az Hy La Kk Lb Tt Ka Uz My Am Ilo Ceb Br Ga Cy Om Zu Wo

Figure 3: Fraction of parallel data in each language which is multi-way parallel (bar chart, right y-axis) and number
of unique sentences (solid black line, left y-axis, log scale) by language (x-axis). Low-resource languages exhibit a
dramatic increase in the amount of highly multi-way parallel data (hatched gray bars).

                          Parallelism                     En→De     De→En      Fr→De        De→Fr        En→Ja                               Ja→En         En→Zh            Zh→En       AVG
                          2                                76.5       76.1       73.3        74.6              73.6                            71.9             74.8         75.4   74.5
                          3-4                              74.3       74.2       72.3        73.7              72.0                            70.6             72.1         72.5   72.7 (-1.8)
                          5-7                              71.9       71.8       70.0        71.3              70.5                            69.2             69.1         69.5   70.4 (-4.1)
                          8+                               69.7       69.8       67.5        68.6              69.7                            68.6             66.1         66.6   68.3 (-6.2)

Table 3: Bitext quality (as measured by CometQE) as a function of multi-way parallelism, for random 1M subsets in
various language pairs. Multi-way parallel translations are lower quality. Average scores are visualized in Figure 1.


                                            200                              Parallelism:                                                   1.12 Parallelism:
                                            175                                     2                                                                   2
                                                                                                                  Mean LASER Margin Score
                        Median Perplexity




                                                                                    3-4                                                     1.11        3-4
                                            150                                     5-7                                                                 5-7
                                            125                                     8+                                                                  8+
                                                                                                                                            1.10
                                            100
                                             75                                                                                             1.09
                                             50
                                                   1-38    39-58 59-89 90-139        140+                                                   1.08
                                                           Sentence Length (chars)
                                                                                                                                                   3-38     39-58 59-89 90-139           140+
Figure 4: Median perplexity (measured by GPT-2) vs                                                                                                          Sentence Length (chars)
multi-way parallelism, in English. We stratify by sen-
tence length, as shorter content tends to have higher                                                    Figure 6: LASER margin scores as a function of multi-
perplexity, likely due to GPT-2 having no or little con-                                                 way parallelism and sentence length, in English. Trends
text for predicting the first few words. More multi-way                                                  in other languages that we investigated (French, German,
parallel data has lower perplexity (i.e. easier to predict).                                             Chinese, Japanese) were very similar (not shown).

                                                 Parallelism:                                                                   Langs                     Ref          MT               ∆
                                            0.74        2
                                                        3-4                                                                     En→De                     86.7%        89.5% +/- 0.6%   2.8%
                        CometQE Score ( )




                                            0.72        5-7                                                                     De→En                     87.4%        90.1% +/- 0.4%   2.8%
                                                        8+                                                                      Zh→En                     82.3%        85.3% +/- 0.3%   3.0%
                                            0.70                                                                                En→Zh                     82.6%        85.8% +/- 0.4%   3.1%
                                                                                                                                En→Ja                     78.8%        82.7% +/- 1.1%   3.9%
                                            0.68                                                                                De→Fr                     87.4%        90.1% +/- 0.4%   2.8%
                                                                                                                                Fr→De                     90.5%        91.4% +/- 0.6%   0.9%
                                            0.66
                                                                                                         Table 4: LASER cosine similarity between source and
                                                   1-30    31-43 44-63 64-110        111+                human reference (“Ref”) vs mean and standard devia-
                                                           Sentence Length (chars)
                                                                                                         tion for Online-Y, Online-G, Online-A, Online-W, and
Figure 5: CometQE score vs sentence length (average                                                      Online-B (“MT”) from WMT 2022. In cases where
of source and target, in characters), for Fr-De. Other                                                   there is more than one human reference, we average the
language pairs (not shown) are very similar. Quality dif-                                                cosine similarities. We find that LASER has a bias for
ferences between levels of multi-way parallelism holds                                                   MT output, of about 2.8% on average. Note that Ja→En
across sentence length.                                                                                  was not included among the WMT language pairs.
                                      Parallelism              5   Discussion & Conclusion
  Topic                          2    3-4     5-7    8+
  Autos/Vehicles/Transit        2.2    2.0    1.6    1.6       Experiments with QE (see § 4.4) strongly suggest
  Beauty/Fitness/Health.        6.5    7.2    6.4    6.4       that highly multi-way parallel translations are gen-
  Books/Arts/Entertainment      8.0    7.3    6.3    5.4       erated by MT. In lower resource languages, most
  Business/Industry/Finance    10.6    7.6    6.0    6.6
  Computers/Electronics         3.7    3.4    4.5    3.5       translations are multi-way parallel (see § 4.2), sug-
  Conversation/Opinion         22.5   29.9   33.3   40.1       gesting that MT content dominates translation con-
  Food/Drink                    1.7    1.8    1.7    0.9       tent. Furthermore, a large fraction of the total sen-
  Hobbies/Leisure               0.9    0.9    1.4    1.0
  Home/Garden                   0.9    0.7    0.9    0.5       tences in lower resource languages have at least
  Internet/Telecom              3.2    3.0    2.1    2.6       one translation (see § 4.1), implying that a large
  Jobs/Education                6.6    4.7    5.0    5.0       fraction of the total web in those languages is MT
  Law/Government                7.2    6.0    5.2    4.8
  News/Information             12.2   11.8   10.5    9.5       generated.
  Pets/Animals                  1.2    1.4    1.2    1.0          Several observations point to a selection bias in
  Real Estate                   1.3    0.8    0.5    0.5
  Religion                      3.4    4.7    5.6    5.4
                                                               the type of data which is translated into many lan-
  Shopping                      1.1    1.2    1.2    0.7       guages, compared to data translated into a single
  Sports/Games                  3.2    2.9    3.7    2.2       language: it is shorter and more predictable (see
  Travel                        2.9    2.6    2.5    1.9
  Other/Cannot tell             0.2    0.1    0.5    0.7       § 4.3), and substantially more likely to be from
                                                               the C ONVERSATION & O PINION topic (see § 4.5).
Table 5: Percentage of corpus which human annotators           Since translations of this data constitute a substan-
classified as each topic, for various levels of parallelism.   tial portion of the total data in low-resource lan-
                                                               guages, this bias will also appear in low resource
                                                               languages.
4.5    Multi-way Parallel Data has Topical Bias                   An investigation into the increase in C ONVERSA -
                                                               TION & O PINION data suggests that this selection
We had professional linguists classify8 10,000 ran-            bias is the result of low quality content (likely pro-
domly selected English sentences as one of the 20              duced to generate ad revenue) being translated via
topics given in Table 5, based on the high-level Top-          MT en masse into many lower resource languages
ics API categories.9 We observe a dramatic shift in            (again likely for the purpose of generating ad rev-
the distribution of topics when comparing 2-way                enue). It also suggests that such data originates
to 8+ way parallel data, with C ONVERSATION &                  in English and is translated into other languages.
O PINION increasing from 22.5% to 40.1%.                       Additional investigation would be required to un-
   We manually inspected a random sample of 100                derstand if this finding generalizes to other topics,
highly multi-way parallel sentences from the C ON -            languages, and levels of multi-way parallelism.
VERSATION & O PINION topic and found them hard                    Our findings also suggest some ways to address
to characterize due to the isolated sentences being            the problem of MT output in web-scraped training
very short (typically 5-10 words). However, search-            data: MT detection, which has typically been pro-
ing the web for the sentences was enlightening: the            posed to filter bitext, could also help to filter mono-
vast majority came from articles that we character-            lingual text in lower resource languages. It also
ized as low quality, requiring little or no expertise          suggests that multi-way parallelism is a promising
or advance effort to create, on topics like being              way to detect low quality, machine translated data,
taken more seriously at work, being careful about              especially in lower resource languages, to filter
your choices, six tips for new boat owners, decid-             both bilingual and monolingual data.
ing to be happy, etc. Furthermore, we were un-
                                                               Limitations
able to find any translationese or other errors that
would suggest the articles were being translated               Our study covers 90 of the most common languages
into English (either by human translators or MT),              on the web, where MT tends to be available. We
suggesting it is instead being generated in English            would obviously not expect the trends we observe
and translated to other languages.                             regarding low resource languages to extend into
                                                               the long tail of low-resource languages that are not
   8                                                           currently supported by MT.
    Full annotator guidelines are provided in Appendix D
   9
    https://cloud.google.com/natural-language/                    All our analysis is performed at the sentence
docs/categories                                                level, because ccMatrix is at the sentence level;
this makes some analysis (e.g. topic analysis) diffi-   recall in lower-resource languages (Feng et al.,
cult and/or ambiguous. We would have preferred to       2022) and as we show in this work (Table 4), has a
use a corpus which is aligned at the document level     preference for MT over human translations. ccMa-
to enable document level analysis and evaluation        trix also uses approximate nearest neighbor search
(Läubli et al., 2018; Toral et al., 2018; Vernikos      (Johnson et al., 2019), which trades off some recall
et al., 2022), but no such corpus is publicly avail-    performance in order to make searches computa-
able.                                                   tionally feasible.
   Similarly, our analysis does not take advantage         Our analysis by language / language pair relies
of any cues that might be present in a web page         on automatic language identification (LID). Short-
to indicate its content is MT generated. However,       comings have also been noted in automatic LID, es-
in personal communications with the authors of          pecially in low-resource languages (Caswell et al.,
Paracrawl (Bañón et al., 2020), they note that in       2020; Kreutzer et al., 2022).
low-resource languages supported by popular MT
systems, simple rules10 to remove data from com-        Acknowledgements
mon translation plug-ins filter out most of their       We would like to thank Mohaddeseh Bastan, Anna
scraped bitext. This observation is consistent with     Currey, Kenneth Heafield, Huda Khayrallah, Hieu
our findings.                                           Hoang, Surafel Lakew, Prashant Mathur, Yogesh
   We use CometQE to evaluate translation qual-         Virkar, and the anonymous ACL reviewers for their
ity. CometQE is trained on human annotations            constructive feedback at various stages of drafting.
of translation quality from many years of WMT           We would also like to think Tatyana Badeka and
(Kocmi et al., 2023) evaluations. The web data in       Jenyuan Wang for assistance with the topic analy-
our experiments likely has a very different domain      sis.
distribution than WMT data, and trained metrics
like CometQE have been shown to exhibit a per-
formance drop when moving from WMT to other             References
domains (Zouhar et al., 2024).                          Roee Aharoni, Moshe Koppel, and Yoav Goldberg.
   Our analysis of the web is based on bitext mined       2014. Automatic detection of machine translated text
from the web. As such, shortcomings or biases in          and translation quality estimation. In Proceedings
                                                          of the 52nd Annual Meeting of the Association for
web scraping and bitext mining could affect our           Computational Linguistics (Volume 2: Short Papers),
results. Common Crawl provides only a sample              pages 289–295, Baltimore, Maryland. Association
of the web, and biases have been demonstrated in          for Computational Linguistics.
web scraping (Mehmood et al., 2017; Dodge et al.,
                                                        Ebtesam Almazrouei, Hamza Alobeidli, Abdulaziz Al-
2021). Common Crawl follows links within web              shamsi, Alessandro Cappelli, Ruxandra Cojocaru,
pages to find new pages, and web pages sometimes          Mérouane Debbah, Étienne Goffinet, Daniel Hess-
have links to translations of the same page in an-        low, Julien Launay, Quentin Malartic, et al. 2023.
other language, so Common Crawl may be more               The falcon series of open language models. arXiv
                                                          preprint arXiv:2311.16867.
likely to find web pages which are translations of
pages it has already found than other, new pages.       Yuki Arase and Ming Zhou. 2013. Machine translation
This should be mitigated at least in part by combin-      detection from monolingual web-text. In Proceed-
ing many Common Crawl snapshots, as is done in            ings of the 51st Annual Meeting of the Association for
                                                          Computational Linguistics (Volume 1: Long Papers),
ccMatrix.                                                 pages 1597–1607, Sofia, Bulgaria. Association for
   The 32 snapshots of Common Crawl used in cc-           Computational Linguistics.
Matrix were collected between December 2017 to
                                                        Mikel Artetxe and Holger Schwenk. 2019. Mas-
February 2020 (Schwenk et al., 2021). We are not          sively multilingual sentence embeddings for zero-
aware of a more recent, publicly available corpus         shot cross-lingual transfer and beyond. Transactions
that would enable this kind of analysis.                  of the Association for Computational Linguistics,
   The ccMatrix corpus creation process relies on         7:597–610.
LASER margin scores (as does our process to cre-        Marta Bañón, Pinzhen Chen, Barry Haddow, Kenneth
ate MWccMatrix). LASER is known to have lower            Heafield, Hieu Hoang, Miquel Esplà-Gomis, Mikel L.
                                                         Forcada, Amir Kamran, Faheem Kirefu, Philipp
  10                                                     Koehn, Sergio Ortiz Rojas, Leopoldo Pla Sempere,
     https://github.com/paracrawl/cirrus-scripts/
blob/master/mt-filter-list.annotated                     Gema Ramírez-Sánchez, Elsa Sarrías, Marek Strelec,
  Brian Thompson, William Waites, Dion Wiggins, and          Punta Cana, Dominican Republic. Association for
  Jaume Zaragoza. 2020. ParaCrawl: Web-scale acqui-          Computational Linguistics.
  sition of parallel corpora. In Proceedings of the 58th
  Annual Meeting of the Association for Computational      Kevin Duh. 2018.     The multitarget ted talks
  Linguistics, pages 4555–4567, Online. Association          task.   http://www.cs.jhu.edu/~kevinduh/a/
  for Computational Linguistics.                             multitarget-tedtalks/.
William Brannon, Yogesh Virkar, and Brian Thompson.        Fangxiaoyu Feng, Yinfei Yang, Daniel Cer, Naveen Ari-
  2023. Dubbing in practice: A large scale study of hu-      vazhagan, and Wei Wang. 2022. Language-agnostic
  man localization with insights for automatic dubbing.      BERT sentence embedding. In Proceedings of the
  Transactions of the Association for Computational          60th Annual Meeting of the Association for Compu-
  Linguistics, 11:419–435.                                   tational Linguistics (Volume 1: Long Papers), pages
                                                             878–891, Dublin, Ireland. Association for Computa-
Tom Brown, Benjamin Mann, Nick Ryder, Melanie
                                                             tional Linguistics.
  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,            Markus Freitag and Orhan Firat. 2020. Complete multi-
  Gretchen Krueger, Tom Henighan, Rewon Child,               lingual neural machine translation. In Proceedings of
  Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens         the Fifth Conference on Machine Translation, pages
  Winter, Chris Hesse, Mark Chen, Eric Sigler, Ma-           550–560, Online. Association for Computational Lin-
  teusz Litwin, Scott Gray, Benjamin Chess, Jack             guistics.
  Clark, Christopher Berner, Sam McCandlish, Alec
  Radford, Ilya Sutskever, and Dario Amodei. 2020.         Markus Freitag, Nitika Mathur, Chi-kiu Lo, Elefthe-
  Language models are few-shot learners. In Ad-             rios Avramidis, Ricardo Rei, Brian Thompson, Tom
  vances in Neural Information Processing Systems,          Kocmi, Frederic Blain, Daniel Deutsch, Craig Stew-
  volume 33, pages 1877–1901. Curran Associates,            art, Chrysoula Zerva, Sheila Castilho, Alon Lavie,
  Inc.                                                      and George Foster. 2023. Results of WMT23 metrics
                                                            shared task: Metrics might be guilty but references
Christian Buck and Philipp Koehn. 2016. Quick and           are not innocent. In Proceedings of the Eighth Con-
  reliable document alignment via TF/IDF-weighted           ference on Machine Translation, pages 578–628, Sin-
  cosine distance. In Proceedings of the First Confer-      gapore. Association for Computational Linguistics.
  ence on Machine Translation: Volume 2, Shared Task
  Papers, pages 672–678, Berlin, Germany. Associa-         Markus Freitag, Ricardo Rei, Nitika Mathur, Chi-kiu Lo,
  tion for Computational Linguistics.                        Craig Stewart, George Foster, Alon Lavie, and Ondřej
                                                             Bojar. 2021. Results of the WMT21 metrics shared
Isaac Caswell, Theresa Breiner, Daan van Esch, and           task: Evaluating metrics with expert-based human
   Ankur Bapna. 2020. Language ID in the wild: Unex-         evaluations on TED and news domain. In Proceed-
   pected challenges on the path to a thousand-language      ings of the Sixth Conference on Machine Translation,
   web text corpus. In Proceedings of the 28th Inter-        pages 733–774, Online. Association for Computa-
   national Conference on Computational Linguistics,         tional Linguistics.
   pages 6588–6608, Barcelona, Spain (Online). Inter-
   national Committee on Computational Linguistics.        William A. Gale and Kenneth W. Church. 1993. A
                                                             program for aligning sentences in bilingual corpora.
Vishrav Chaudhary, Yuqing Tang, Francisco Guzmán,           Computational Linguistics, 19(1):75–102.
  Holger Schwenk, and Philipp Koehn. 2019. Low-
  resource corpus filtering using multilingual sentence    Leo Gao, Stella Biderman, Sid Black, Laurence Gold-
  embeddings. In Proceedings of the Fourth Confer-           ing, Travis Hoppe, Charles Foster, Jason Phang, Ho-
  ence on Machine Translation (Volume 3: Shared Task         race He, Anish Thite, Noa Nabeshima, et al. 2020.
  Papers, Day 2), pages 261–266, Florence, Italy. As-        The pile: An 800gb dataset of diverse text for lan-
  sociation for Computational Linguistics.                   guage modeling. arXiv preprint arXiv:2101.00027.
Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
  Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul         Federico Gaspari and John Hutchins. 2007. Online and
  Barham, Hyung Won Chung, Charles Sutton, Sebas-            free! ten years of online machine translation: ori-
  tian Gehrmann, et al. 2023. Palm: Scaling language         gins, developments, current use and future prospects.
  modeling with pathways. Journal of Machine Learn-          In Proceedings of Machine Translation Summit XI:
  ing Research, 24(240):1–113.                               Papers, Copenhagen, Denmark.

Jesse Dodge, Maarten Sap, Ana Marasović, William          W John Hutchins. 1995. Machine translation: A brief
   Agnew, Gabriel Ilharco, Dirk Groeneveld, Margaret         history. In Concise history of the language sciences,
   Mitchell, and Matt Gardner. 2021. Documenting             pages 431–445. Elsevier.
   large webtext corpora: A case study on the colos-
   sal clean crawled corpus. In Proceedings of the         Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019.
   2021 Conference on Empirical Methods in Natural            Billion-scale similarity search with gpus. IEEE
   Language Processing, pages 1286–1305, Online and           Transactions on Big Data, 7(3):535–547.
Marcin Junczys-Dowmunt. 2018. Dual conditional                Muhammad, Nanda Muhammad, Ayanda Mnyak-
 cross-entropy filtering of noisy parallel corpora. In        eni, Jamshidbek Mirzakhalov, Tapiwanashe Matan-
 Proceedings of the Third Conference on Machine               gira, Colin Leong, Nze Lawson, Sneha Kudugunta,
 Translation: Shared Task Papers, pages 888–895,              Yacine Jernite, Mathias Jenny, Orhan Firat, Bonaven-
 Belgium, Brussels. Association for Computational             ture F. P. Dossou, Sakhile Dlamini, Nisansa de Silva,
 Linguistics.                                                 Sakine Çabuk Ballı, Stella Biderman, Alessia Bat-
                                                              tisti, Ahmed Baruwa, Ankur Bapna, Pallavi Baljekar,
Nadeem Jadoon Khan, Waqas Anwar, and Nadir                    Israel Abebe Azime, Ayodele Awokoya, Duygu Ata-
  Durrani. 2017. Machine translation approaches               man, Orevaoghene Ahia, Oghenefego Ahia, Sweta
  and survey for indian languages. arXiv preprint             Agrawal, and Mofetoluwa Adeyemi. 2022. Quality
  arXiv:1701.04290.                                           at a glance: An audit of web-crawled multilingual
Huda Khayrallah and Philipp Koehn. 2018. On the               datasets. Transactions of the Association for Compu-
  impact of various types of noise on neural machine          tational Linguistics, 10:50–72.
  translation. In Proceedings of the 2nd Workshop on        David Kurokawa, Cyril Goutte, and Pierre Isabelle.
  Neural Machine Translation and Generation, pages            2009. Automatic detection of translated text and
  74–83, Melbourne, Australia. Association for Com-           its impact on machine translation. In Proceedings
  putational Linguistics.                                     of Machine Translation Summit XII: Papers, Ottawa,
Tom Kocmi, Eleftherios Avramidis, Rachel Bawden,              Canada.
  Ondřej Bojar, Anton Dvorkovich, Christian Fed-
                                                            Samuel Läubli, Rico Sennrich, and Martin Volk. 2018.
  ermann, Mark Fishel, Markus Freitag, Thamme
                                                              Has machine translation achieved human parity? a
  Gowda, Roman Grundkiewicz, Barry Haddow,
                                                              case for document-level evaluation. In Proceedings
  Philipp Koehn, Benjamin Marie, Christof Monz,
                                                              of the 2018 Conference on Empirical Methods in Nat-
  Makoto Morishita, Kenton Murray, Makoto Nagata,
                                                              ural Language Processing, pages 4791–4796, Brus-
  Toshiaki Nakazawa, Martin Popel, Maja Popović,
                                                              sels, Belgium. Association for Computational Lin-
  and Mariya Shmatova. 2023. Findings of the 2023
                                                              guistics.
  conference on machine translation (WMT23): LLMs
  are here but not quite there yet. In Proceedings of the   Teven Le Scao, Thomas Wang, Daniel Hesslow, Stas
  Eighth Conference on Machine Translation, pages             Bekman, M Saiful Bari, Stella Biderman, Hady Elsa-
  1–42, Singapore. Association for Computational Lin-         har, Niklas Muennighoff, Jason Phang, Ofir Press,
  guistics.                                                   Colin Raffel, Victor Sanh, Sheng Shen, Lintang
Philipp Koehn, Vishrav Chaudhary, Ahmed El-Kishky,            Sutawika, Jaesung Tae, Zheng Xin Yong, Julien Lau-
  Naman Goyal, Peng-Jen Chen, and Francisco                   nay, and Iz Beltagy. 2022. What language model to
  Guzmán. 2020. Findings of the WMT 2020 shared               train if you have one million GPU hours? In Find-
  task on parallel corpus filtering and alignment. In         ings of the Association for Computational Linguistics:
  Proceedings of the Fifth Conference on Machine              EMNLP 2022, pages 765–782, Abu Dhabi, United
  Translation, pages 726–742, Online. Association for         Arab Emirates. Association for Computational Lin-
  Computational Linguistics.                                  guistics.

Philipp Koehn, Francisco Guzmán, Vishrav Chaud-             Muhammad Amir Mehmood, Hafiz Muhammad Shafiq,
  hary, and Juan Pino. 2019. Findings of the WMT             and Abdul Waheed. 2017. Understanding regional
  2019 shared task on parallel corpus filtering for          context of world wide web using common crawl cor-
  low-resource conditions. In Proceedings of the             pus. In 2017 IEEE 13th Malaysia International Con-
  Fourth Conference on Machine Translation (Volume           ference on Communications (MICC), pages 164–169.
  3: Shared Task Papers, Day 2), pages 54–72, Flo-
  rence, Italy. Association for Computational Linguis-      NLLB Team, Marta R. Costa-jussà, James Cross, Onur
  tics.                                                       Çelebi, Maha Elbayad, Kenneth Heafield, Kevin Hef-
                                                              fernan, Elahe Kalbassi, Janice Lam, Daniel Licht,
Philipp Koehn, Huda Khayrallah, Kenneth Heafield, and         Jean Maillard, Anna Sun, Skyler Wang, Guillaume
  Mikel L. Forcada. 2018. Findings of the WMT 2018            Wenzek, Al Youngblood, Bapi Akula, Loic Bar-
  shared task on parallel corpus filtering. In Proceed-       rault, Gabriel Mejia Gonzalez, Prangthip Hansanti,
  ings of the Third Conference on Machine Translation:        John Hoffman, Semarley Jarrett, Kaushik Ram
  Shared Task Papers, pages 726–739, Belgium, Brus-           Sadagopan, Dirk Rowe, Shannon Spruit, Chau
  sels. Association for Computational Linguistics.            Tran, Pierre Andrews, Necip Fazil Ayan, Shruti
                                                              Bhosale, Sergey Edunov, Angela Fan, Cynthia
Julia Kreutzer, Isaac Caswell, Lisa Wang, Ahsan Wahab,        Gao, Vedanuj Goswami, Francisco Guzmán, Philipp
   Daan van Esch, Nasanbayar Ulzii-Orshikh, Allah-            Koehn, Alexandre Mourachko, Christophe Rop-
   sera Tapo, Nishant Subramani, Artem Sokolov, Clay-         ers, Safiyyah Saleem, Holger Schwenk, and Jeff
   tone Sikasote, Monang Setyawan, Supheakmungkol             Wang. 2022. No language left behind: Scaling
   Sarin, Sokhar Samb, Benoît Sagot, Clara Rivera, An-        human-centered machine translation. arXiv preprint
   nette Rios, Isabel Papadimitriou, Salomey Osei, Pe-        arXiv:2207.04672.
   dro Ortiz Suarez, Iroro Orife, Kelechi Ogueji, An-
   dre Niyongabo Rubungo, Toan Q. Nguyen, Math-             Jan-Thorsten Peter, David Vilar, Daniel Deutsch, Mara
   ias Müller, André Müller, Shamsuddeen Hassan                Finkelstein, Juraj Juraska, and Markus Freitag. 2023.
  There’s no data like better data: Using QE metrics      Yu Sun, Shuohuan Wang, Shikun Feng, Siyu Ding,
  for MT data filtering. In Proceedings of the Eighth       Chao Pang, Junyuan Shang, Jiaxiang Liu, Xuyi Chen,
  Conference on Machine Translation, pages 561–577,         Yanbin Zhao, Yuxiang Lu, et al. 2021. Ernie 3.0:
  Singapore. Association for Computational Linguis-         Large-scale knowledge enhanced pre-training for lan-
  tics.                                                     guage understanding and generation. arXiv preprint
                                                            arXiv:2107.02137.
Alec Radford, Jeffrey Wu, Rewon Child, David Luan,
  Dario Amodei, and Ilya Sutskever. 2019. Language        Brian Thompson and Philipp Koehn. 2019. Vecalign:
  models are unsupervised multitask learners. OpenAI        Improved sentence alignment in linear time and space.
  blog, 1(8):9.                                             In Proceedings of the 2019 Conference on Empirical
                                                            Methods in Natural Language Processing and the
Jack W Rae, Sebastian Borgeaud, Trevor Cai, Katie           9th International Joint Conference on Natural Lan-
   Millican, Jordan Hoffmann, Francis Song, John            guage Processing (EMNLP-IJCNLP), pages 1342–
  Aslanides, Sarah Henderson, Roman Ring, Susan-            1348, Hong Kong, China. Association for Computa-
   nah Young, et al. 2021. Scaling language models:         tional Linguistics.
   Methods, analysis & insights from training gopher.
   arXiv preprint arXiv:2112.11446.                       Brian Thompson and Philipp Koehn. 2020. Exploiting
                                                            sentence order in document alignment. In Proceed-
Ricardo Rei, Marcos Treviso, Nuno M. Guerreiro,             ings of the 2020 Conference on Empirical Methods
  Chrysoula Zerva, Ana C Farinha, Christine Maroti,         in Natural Language Processing (EMNLP), pages
  José G. C. de Souza, Taisiya Glushkova, Duarte            5997–6007, Online. Association for Computational
  Alves, Luisa Coheur, Alon Lavie, and André F. T.          Linguistics.
  Martins. 2022. CometKiwi: IST-unbabel 2022 sub-
                                                          Brian Thompson and Matt Post. 2020a. Automatic ma-
  mission for the quality estimation shared task. In
                                                            chine translation evaluation in many languages via
  Proceedings of the Seventh Conference on Machine
                                                            zero-shot paraphrasing. In Proceedings of the 2020
  Translation (WMT), pages 634–645, Abu Dhabi,
                                                            Conference on Empirical Methods in Natural Lan-
  United Arab Emirates (Hybrid). Association for Com-
                                                            guage Processing (EMNLP), pages 90–121, Online.
  putational Linguistics.
                                                            Association for Computational Linguistics.
Philip Resnik. 1998. Parallel strands: a preliminary      Brian Thompson and Matt Post. 2020b. Paraphrase
  investigation into mining the web for bilingual text.     generation as zero-shot multilingual translation: Dis-
  In Proceedings of the Third Conference of the As-         entangling semantic similarity from lexical and syn-
  sociation for Machine Translation in the Americas:        tactic diversity. In Proceedings of the Fifth Confer-
  Technical Papers, pages 72–82, Langhorne, PA, USA.        ence on Machine Translation, pages 561–570, Online.
  Springer.                                                 Association for Computational Linguistics.
Philip Resnik and Noah A. Smith. 2003. The web            Antonio Toral, Sheila Castilho, Ke Hu, and Andy Way.
  as a parallel corpus. Computational Linguistics,          2018. Attaining the unattainable? reassessing claims
  29(3):349–380.                                            of human parity in neural machine translation. In Pro-
                                                            ceedings of the Third Conference on Machine Trans-
Holger Schwenk, Guillaume Wenzek, Sergey Edunov,            lation: Research Papers, pages 113–123, Brussels,
  Edouard Grave, Armand Joulin, and Angela Fan.             Belgium. Association for Computational Linguistics.
  2021. CCMatrix: Mining billions of high-quality
  parallel sentences on the web. In Proceedings of the    Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
  59th Annual Meeting of the Association for Compu-         bert, Amjad Almahairi, Yasmine Babaei, Nikolay
  tational Linguistics and the 11th International Joint     Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
  Conference on Natural Language Processing (Vol-           Bhosale, et al. 2023. Llama 2: Open founda-
  ume 1: Long Papers), pages 6490–6500, Online. As-         tion and fine-tuned chat models. arXiv preprint
  sociation for Computational Linguistics.                  arXiv:2307.09288.

Rico Sennrich and Martin Volk. 2010. MT-based sen-        Giorgos Vernikos, Brian Thompson, Prashant Mathur,
  tence alignment for OCR-generated parallel texts. In      and Marcello Federico. 2022. Embarrassingly easy
  Proceedings of the 9th Conference of the Association      document-level MT metrics: How to convert any
  for Machine Translation in the Americas: Research         pretrained metric into a document-level metric. In
  Papers, Denver, Colorado, USA. Association for Ma-        Proceedings of the Seventh Conference on Machine
  chine Translation in the Americas.                        Translation (WMT), pages 118–128, Abu Dhabi,
                                                            United Arab Emirates (Hybrid). Association for Com-
Steve Sloto, Brian Thompson, Huda Khayrallah, To-           putational Linguistics.
   bias Domhan, Thamme Gowda, and Philipp Koehn.
   2023. Findings of the WMT 2023 shared task on          Vilém Zouhar, Shuoyang Ding, Anna Currey, Tatyana
   parallel data curation. In Proceedings of the Eighth     Badeka, Jenyuan Wang, and Brian Thompson. 2024.
  Conference on Machine Translation, pages 95–102,          Fine-tuned machine translation metrics struggle in
   Singapore. Association for Computational Linguis-        unseen domains. arXiv preprint arXiv:2402.18747.
   tics.
A        MWccMatrix Creation: Additional
         Details
A simplified version of the algorithm used to create
MWccMatrix is provided in algorithm 1.
   In practice, several optimizations were required
to make the process tractable. Instead of attempting
to sort 10.9B sentence pairs by margin score, we
approximate the search by binning margin scores
and sorting the data into buckets corresponding to
the (binned) margin scores, similar to a radix sort.
The sentences are too large to fit in memory, so we
represent the sentences as 64 bit hashes. Addition-
ally, our scripts are written in python but we use
the cykhash11 package, which provides a native C
int64 to int64 hashmap. Conversion from hashes
back to sentences is done in small shards, and the
hash→sent mappings required to reconstruct the
data are sharded such that only the mappings re-
quired for one shard are loaded in memory at one
time. Finally, we make extensive use of paralleliza-
tion (e.g. computing margin score bins, sharding
data by margin score bin, hashing sentence pairs,
etc).

B        Larger Version of Figure 2
A larger version of Figure 2, which includes lan-
guage codes for each language, is provided in Fig-
ure 7. As previously noted, we only have total
data sizes for the 54 highest-resource languages, as
that is what was reported by Schwenk et al. (2021),
so we cannot compute this percentage for the 36
lowest-resource languages used in this study.

C        Multi-way Parallelism by Language
Average parallelism for each language is shown in
Figure 8.




    11
         https://github.com/realead/cykhash
 Algorithm 1: Algorithm (simplified for comprehension) used to create multi-way parallel corpus.
 1 sent2row ← def aultdict(dict)
 2 sort(bitext, key = marginScore, descending = T rue)
 3 numRows ← 0
 4 for srcTxt, srcLang, tgtText, tgtLang, marginScore in bitext do
 5     if srcTxt not in sent2row[srcLang] and tgtText not in sent2row[tgtLang] then
 7          /* add new sentence pair                                                               */
 8          sent2row[srcLang][srcT xt] ← (numRows, marginScore)
 9          sent2row[tgtLang][tgtT xt] ← (numRows, marginScore)
10          numRows ← numRows + 1
11      else if srcTxt in sent2row[srcLang] then
13          /* srcText in table, join on it                                                        */
14          srcRow ← sent2row[srcLang][srcT xt]
15          sent2row[tgtLang][tgtT xt] ← (srcRow, marginScore)
16      else if tgtTxt in sent2row[tgtLang] then
18          /* tgtText in table, join on it                                                        */
19          tgtRow ← sent2row[tgtLang][tgtT xt]
20          sent2row[srcLang][srcT xt] ← (tgtRow, marginScore)
22      /* else both sentences already in table (with higher marginScore), do nothing              */
24   /* Invert sent2row                                                                            */
25 row2sent ← def aultdict(dict)
26 for lang in langs do
27     for sent, (row, marginScore) in sent2row[lang].items() do
28         if row in row2sent[lang] then
29             _, oldM arginScore ← row2sent[lang][row]
30          else
31              oldM arginScore ← −1
33          /* When we find duplicates/paraphrases, keep the sentence with the highest score       */
34          if marginScore > oldMarginScore then
35              row2sent[lang][row] ← (sent, score)

37   /* Coalesce output translation tuples                                                         */
38 output ← []
39 for row in range(numRows) do
40     translations ← dict()
41     for lang in langs do
42         if row in row2sent[lang] then
43              translations[lang] ← row2sent[lang][row]

44      output.append(translations)
                              50
                                                                                                                                                                                  sw


                              40                                                                                                                  gl


                                                                                                                                    et                  eu             af
% Sents With 1+ Translation




                              30                                                                                   bg slsrca
                                                                                                                        lt
                                                                                                                                     lv
                                                                                                              sk                      sq         ms
                                                                                                                                      hr
                                                                                                                                                        si
                                                                                                                   he
                              20                                                                       ro dano
                                                                                             cs        el fi               ta
                                                                                                                             bn
                                                                                                                                            ml
                                                            esfr                                       hu                                              uris mr
                                                                         pt         nlpl    id
                                                                         it
                                                                                    sv            ar     uk
                                                                                                                                                             be
                              10           en              de ru              tr                                                                  tl
                                                                                                  fa
                                                                               vi
                                                                                      ko                                                                          ne
                                                                zhja
                                             1010                                          109                        108                                                   107
                                                                                             Unique Monolingual Sents
        Figure 7: Percentage of unique monolingual sentences which have at least one translation, in each language for
        which we have the data to compute it.




                         109                                                                                                                                                      14
                         108                                                                                                                                                      12
                                                                                                                                                                                      Avg. Parallelism
 Total Sentences




                         107                                                                                                                                                      10
                         106                                                                                                                                                      8
                         105                                                                                                                                                      6
                                                                                                                                                                                  4
                         104
                                                                                                                                                                                  2
                         103
                                                                                                                                                                                  0
                                   En Fr Pt Ru Pl Cs Ja Zh Sk El Da Ar Bg Fa Uk Ca Lt Et Bn Ta Gl Eu Mk Si Is Sw Mr Ast Ne Mg Fy Oc Sd Jv Km Su So Yi Ha Yo Ig Or Gd Xh Lg
                                     Es De It Nl Sv Tr Id Vi Ro Hu Fi No Ko Sl He Sr Hi Lv Sq Hr Ms Ml Eo Ur Af Tl Be Az Hy La Kk Lb Tt Ka Uz My Am Ilo Ceb Br Ga Cy Om Zu Wo

         Figure 8: Average multi-way parallelism (blue bars, right y-axis) and number of unique sentences (gray line, left
         y-axis, log scale) by language (x-axis). Lower-resource languages tend to be more multi-way parallel.
D     Topic Analysis Annotation Guidelines                 2. If needed, please do a quick search of the
                                                              sentence to identify the topic. Do limit the
Task: Please identify the most relevant topic for
                                                              search to a quick scan of search results no
each sentence using the pre-defined list. Assign
                                                              longer than 30 sec.
the correct label to each sentence. Make sure to
familiarize yourself with the list before working on       3. If a sentence fits more than one topic equally
the task.                                                     and you cannot decide between the two, then
                                                              select a primary and a secondary topic. Add
     Index    Topic                                           a comment if needed to explain. Try not to
     1        Autos/Vehicles/Transit                          abuse this option and always try to choose
     2        Beauty/Fitness/Health.                          one.
     3        Books/Arts/Entertainment
     4        Business/Industry/Finance
     5        Computers/Electronics
     6        Conversation/Opinion
     7        Food/Drink
     8        Hobbies/Leisure
     9        Home/Garden
     10       Internet/Telecom
     11       Jobs/Education
     12       Law/Government
     13       News/Information
     14       Pets/Animals
     15       Real Estate
     16       Religion
     17       Shopping
     18       Sports/Games
     19       Travel
     20       Other/Cannot tell


Here is the list of sub-topics that may
help you develop a better idea of what
belongs to each of these topics:   https:
//github.com/patcg-individual-drafts/
topics/blob/main/taxonomy_v2.md

Note:

    1. Do differentiate between a domain and a topic.
       A topic of the sentence is the main idea of the
       sentence. Where this sentence belongs is the
       domain. In this task we are classifying topics.
        (a) “Aiden was once a warrior who placed
            complete faith in his own abilities.” - this
            belongs to literature/creative writing do-
            main, but the topic of the sentence is
            C ONVERSATION & O PINION.
        (b) “i keep telling you to leave me alone, this
            forum is not the right place for hate” - the
            domain is media, but the topic is C ON -
            VERSATION & O PINION .
