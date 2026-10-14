                                         Synthetic Sources?: Auditing Generative Search Engine Citations for Evidence of
                                                                      AI-Generated Sources

                                                                                   Mowafak Allaham, Nicholas Diakopoulos
                                                                                                   Northwestern University




                                                                     Abstract                                    the web is transforming how people seek information on-
arXiv:2605.23684v1 [cs.IR] 22 May 2026




                                                                                                                 line. In this work we refer to these tools, which include pop-
                                           The growing accessibility of Large Language Models via                ular search-enabled LLMs such as ChatGPT or Gemini, as
                                           conversational interfaces capable of responding to users’             generative search engines (GSE). Generative search engines
                                           questions by drawing on, synthesizing, and citing information         simplify the search process for users by shifting their atten-
                                           from the web (i.e., Generative Search Engines) has simpli-
                                           fied the information-seeking process for users. However, with
                                                                                                                 tion away from clicking and visiting multiple links on a tra-
                                           the proliferation of AI-generated content on the web, it is un-       ditional search results page toward consuming a single syn-
                                           clear whether these engines can reliably omit citing synthetic        thesized response substantiated with in-text citation to vari-
                                           sources (i.e., AI-generated sources). Should these engines be         ous sources – a source in this context refers to a unique web
                                           unable to do so, this puts users at risk of harm by treat-            URL that represents an item online (e.g., blog post, an arti-
                                           ing information from AI-generated sources synthesized in re-          cle, image, or video) that is being cited by generative search
                                           sponses of generative search engines as equivalent to infor-          engines.
                                           mation from authoritative or official sources. In a step towards
                                           identifying whether AI-generated sources are being cited by               Experts and journalists have expressed growing concerns
                                           these engines, this work presents an audit of four generative         about the potential of generative search engines in relying
                                           search engines (ChatGPT, Copilot, Gemini, Perplexity) us-             more on AI-generated sources as a means to compensate for
                                           ing a total of 712 real-world human-generated queries span-           gaps in access to authoritative sources of information and to
                                           ning domains of public importance: politics, health, and the          fill information vacuums (i.e., “data voids”) when respond-
                                           environment. Our findings show evidence of AI-generated               ing to users’ queries (Russell et al. 2025a; Alyukov et al.
                                           sources being cited across all four generative search engines         2025; Tripodi and Moeller 2025; Bansal 2025). While the
                                           (∼16% of cited sources) and identifies key source web do-             epistemic quality of AI-generated content could be a con-
                                           mains these sources belong to that are frequently cited across
                                           these engines and topics. In addition, we observed that gen-
                                                                                                                 tentious point of debate, as not all AI-generated content is
                                           erative search engines include a somewhat narrow set of re-           necessarily low quality (Nishal and Diakopoulos 2024), the
                                           peatedly cited domains while predominantly surfacing a large          AI-tools used for generating such content (e.g., large lan-
                                           number of minimally cited domains in responses to users’              guage models) have their biases (Zhang, Mao, and Cambria
                                           queries. These findings contribute to the growing body of             2025; Gallegos et al. 2024) and are susceptible to generat-
                                           work on assessing the risks of generative search engines with         ing hallucinations and inaccurate information (Bommasani
                                           the objective of increasing public awareness of their limita-         et al. 2021; Deng et al. 2025; Luo et al. 2025). This, in
                                           tions and encouraging appropriate measures to improve in-             turn, may affect the information quality of the output pro-
                                           formation quality and governance of these systems.                    duced by these tools. In addition, the sourcing mechanisms
                                                                                                                 of generative search engines for information online and the
                                                                                                                 choices these engines make at the system and information
                                                                 Introduction                                    levels as part of generating the final answer, such as when
                                         People turn to search engines (e.g., Google or Bing) to                 to include sources in responses, what sources to include or
                                         gather and evaluate information, form opinions, and make                exclude, and the quality and credibility of these sources, il-
                                         decisions on a wide range of topics they find important on              lustrate the opaqueness of these engines, which creates ad-
                                         the personal and societal levels (Rieger et al. 2024; Dutton            ditional opportunities for AI-generated sources that may in-
                                         et al. 2017; Ghosh, Rath, and Shah 2018; Moraes, Putra, and             clude false or misleading information to compete with accu-
                                         Hauff 2018; Marchionini 2006). However, the growing ac-                 rate ones (Gregory 2026; Roy 2025; Zihlmann and Euchner
                                         cessibility of search-enabled large language models (LLMs)              2025; NewsGuard Technologies, Inc. 2025). This ambigu-
                                         via conversational interfaces capable of responding to users’           ity in information sourcing mechanism exposes responses
                                         queries by drawing on and synthesizing information from                 of generative search engines to potential manipulation for
                                                                                                                 personal or corporate gains (e.g., brands promoting AI-
                                         Copyright © 2026, Association for the Advancement of Artificial         generated content onlie to rank themselves in first place in
                                         Intelligence (www.aaai.org). All rights reserved.                       “best X” lists) (Allsopp 2025) or get exploited by bad actors,
through knowledge injection or poisoning attacks (Soudani         a significant finding in the context of auditing information
2025; An, Zhang, and Dredze 2025; Deng et al. 2025), to           on such engines, as the AI-generated source content being
amplify sources with low-quality AI-generated content in          cited is prone to be of lower quality, especially given that
the pool of sources on which generative search engines rely       more reputable news websites were reported to disallow AI
on, potentially degrading the quality of generated responses.     crawlers than ones containing misinformation (Steinacker-
   Therefore, if the source content cited and used by gen-        Olsztyn, Gosain, and Dao 2025), which may disproportion-
erative search engines as part of the response generation         ately (or possibly negatively) influence the content produced
process is AI-generated, given the aforementioned issues          by generative search engines that is presented to users in re-
associated with this type of content, users may be at risk        sponses.
of unknowingly consuming low-quality information. This                Our findings contribute to the growing body of research
is particularly consequential for topics of individual (e.g.      investigating information-related risks posed by generative
health) or societal (e.g. politics, environment) importance,      search engines to users and society at large (Luo et al. 2025)
which could misinform beliefs and actions or influence pub-       by presenting evidence of AI-generated sources being cited
lic opinion and upset political processes (Li and Sinnamon        by four popular generative search engines (Union 2025),
2024; Van Der Ven et al. 2025).                                   highlighting limitations in the reliability of these engines es-
   To better characterize the nature and extent of this prob-     pecially when responding to queries on topics of public im-
lem, it is imperative as a first step to identify whether or      portance (politics, health, and the environment). In addition,
not generative search engines cite sources with AI-generated      by mapping and tabulating the frequencies of source web
content. To this end, this research undertakes an audit of        domains cited by these engines, our findings reveal the dis-
the sources cited by four popular generative search en-           proportionate sourcing practices of these engines along with
gines, which include the search-enabled Chatbot interfaces        the subset of source web domains they frequently rely on to
of ChatGPT, Copilot, Gemini, and Perplexity (Union 2025).         substantiate their answers. These findings may inform prac-
We first identify the range of source web domains (i.e., web      titioners, including developers and risk-assessors, about the
domains that sources belong to) these engines rely on to re-      prevalence of AI-generated sources, both across and within
spond to users’ queries, tabulate their frequencies, whether      individual generative search engines, and the source web do-
or not the source content corresponding to cited sources          mains from which they originate. Such insights could inform
from these web domains is AI-generated, and then exam-            governance efforts looking to improve generative search en-
ine the prominence of such content among cited sources.           gines by identifying (and potentially omitting) sources with
To this end, we pursue the following two research ques-           AI-generated content in citations, particularly if found to be
tions: (1) what are the prevalent source web domains              of lower quality. Ultimately our findings may help take steps
generative search engines cite sources from when re-              towards enhancing the overall quality of information used by
sponding to users’ queries? and (2) how prevalent is AI-          these systems to generate responses.
generated sources among those cited sources? We address
these questions by auditing answer engines through a socio-                             Related work
technical lens (Solaiman et al. 2023; Metaxa et al. 2021;         Generative search engines are increasingly becoming the
Allaham, Kieslich, and Diakopoulos 2025) that extends be-         primary systems for information seeking, potentially sur-
yond assessing the technical artifacts of AI systems to reflect   passing traditional search engines (Liu, Zhang, and Liang
real-world users’ queries spanning three topics of public im-     2023; Chapekis and Lieb 2025). However, these systems
portance: politics, health, and the environment (Li and Sin-      largely remain opaque in how they source, synthesize, and
namon 2024; Van Der Ven et al. 2025)                              present information from the web. This lack of transparency,
   Using a closely curated sample of 712 English language         coupled with the rapid deployment of these systems, raises
queries focusing on general knowledge questions spanning          concerns about their potential impacts on individuals and so-
the topics of politics, health, and the environment, we au-       ciety, and particularly on topics of critical importance such
dit the cited sources of the aforementioned four generative       as health and politics (Li and Sinnamon 2024). One estab-
search engines for evidence of AI-generated sources by first      lished strategy for interrogating the inner-workings of AI
submitting each query in our sample through the user in-          and algorithmic systems, such as generative search engines,
terface (UI) of each engine, then (if present) scraping the       and understanding them from the outside in is: algorithmic
cited sources and their respective content in each generated      audits (Metaxa et al. 2021).
response, and finally using an AI-detection tool to identify         The ambiguity in how generative search engines operate
whether the source content in these sources is AI-generated       and sources content from the web have been obscuring infor-
or not.                                                           mation quality issues, which have tremendous negative con-
   To assess whether source content from multiple cited           sequence on users, such as experiencing difficulty in assess-
sources is AI-generated, we use Pangram (Emi and Spero            ing the reliability of generated responses (Venkit et al. 2024;
2024), an AI-generated-text detection tool, and observe           Li and Sinnamon 2024; Yang 2025). As a result, audits have
a considerable share of source contents of cited sources          previously evaluated the quality of citations and responses
(approximately 16% of unique cited sources across all             of generative engines along numerous dimensions, includ-
providers) on GSE to be AI-generated, with responses to           ing information verifiability (Liu, Zhang, and Liang 2023),
environment-related queries exhibiting the highest propor-        response factuality (Venkit et al. 2024), source attribution
tion of cited source content that is AI-generated. This is        (and mis-attribution) (Strauss et al. 2025; Kelly et al. 2023;
Urman and Makhortykh 2025), and political bias (Dai et al.          gap presents an opportunity to leverage emerging computa-
2025; Minici et al. 2025; Rozado 2022). Empirical findings          tional methods, like Pangram, to audit the quality of sources
from these audits consistently reveal clear limitations in the      cited by answer engines as described in subsequent sections.
reliability and safety of these systems (Li and Sinnamon
2024; Kuai et al. 2025; Luo et al. 2025; Roy 2025). For in-                                     Data
stance, studies report that generative answer engines often
respond to questions they cannot accurately answer rather           Curation & Selection for Queries on Politics and
than declining to respond, resulting in incorrect or specula-       Health
tive outputs, fabricated links, inaccurate citations, and the in-   To curate a dataset that reflects the types of queries users
clusion of unsupported or misleading claims (Jaźwińska and        would submit to generative search engines specifically
Chandrasekar 2025; Liu, Zhang, and Liang 2023), which at            (rather than queries they might submit to a traditional search
times could put users at risk of harm as reported on in the         engine), we start by leveraging queries in the English lan-
media in the case of Google AI Overviews putting users at           guage from the Search Arena dataset (Miroyan et al. 2025).
risk of harm by sharing misleading health advice with inac-         This dataset contains 24,069 queries and conversational in-
curate information from AI-generated summaries (Gregory             teractions with generative search engines, collected between
2026). More problematically, other studies have highlighted         March 18, 2025 and May 8, 2025, across 70 languages from
how generative search engines generate citations that are not       11,650 users across 136 countries, capturing a broader range
clickable and consistently present information to users with-       of user search intents and topics. To conduct an in-depth
out conducting live web search, thus relying on the LLM’s           analysis of the queries, the authors of the Search Arena
internal knowledge for answers (Strauss et al. 2025; Liu,           dataset used a mixed annotation approach that involves hu-
Zhang, and Liang 2023). This in turn has its negative impli-        man and GPT-4.1. First, they used 100 queries as a seed to
cations on users being exposed to false or misleading infor-        tune the annotation process for GPT-4.1. Next, they vali-
mation, as LLMs are prone to hallucination (Ji et al. 2023).        dated the agreement between human and GPT-4.1 annota-
   Beyond these risks, studies have also examined the soci-         tions on a sample of 150 multilingual queries, achieving
etal implications of these systems (Memon and West 2024;            a Cohen’s kappa of 0.812 which indicates a strong agree-
Bender et al. 2021), including their potential to influence         ment between model- and human-annotated labels (Miroyan
public opinion (NewsGuard Technologies, Inc. 2025; Dai              et al. 2025). This annotation process groups queries in the
et al. 2025), create “Chat-Chamber” effects (Jacob, Kerri-          dataset into nine intent categories: Factual Lookup, Infor-
gan, and Bastos 2025), engage in forms of information ho-           mation Synthesis, Analysis, Recommendation, Explanation,
mogenization or gate keeping (Lindemann 2025; Brantner,             Creative Generation, Guidance, Text Processing, and an
Karlsson, and Kuai 2025; Vranić et al. 2025), and exposing         Other category (see Appendix A.8 for detailed description
users to information that are “less diverse, more biased, and       of these categories). Seven out of the nine categories are in-
unverifiable—yet expressed in a confident manner” (Memon            formational in nature constituting 87.4% of the dataset. Our
and West 2024). Collectively, these findings characterize           focus in this work is on informational intents and so we ex-
the risks generative search engines may have on individu-           clude the Creative Generation and Other categories as one
als and society as a result of the content and sources they         captures queries requesting original creative outputs, includ-
feature in their responses. One emerging type of content that       ing fictional scenarios and poetry, and the other represents
may further exacerbate the negative impacts of these sys-           queries that are malformed, declarative in nature, or lacking
tems on users and society is the growing proliferation of AI-       in meaningful user intent.
generated content on the web (Russell et al. 2025b; Shaib              Because the dataset includes both single and multi-turn
et al. 2025).                                                       interactions between users and generative search engines,
   Recent work has begun to develop qualitative frame-              we chose to unify the structure of the data by transforming
works and computational tools for characterizing such con-          multi-turn interactions into single-query instances, as some
tent more precisely (Emi and Spero 2024; Shaib et al. 2025).        multi-turn interactions are multilingual (i.e., they involve
For example, Shaib et al. (2025), introduced a taxonomy             queries in English alongside queries in other languages over
of “AI slop”, defined as low-quality AI-generated text, to          the course of an interaction). Accordingly, for each interac-
measure its prevalence, highlighting that existing qualitative      tion session between a user and the system (i.e., the “assis-
judgments of AI content lack consistent operationalization          tant”), we retained only “user” messages that are in English.
(Shaib et al. 2025). Another example that leverages com-            For the remainder of the analysis, we treat each query as an
putational approaches is Pangram(Emi and Spero 2024), a             independent unit of input to the system, rather than consid-
transformer-based classifier that has been trained on exten-        ering the sequence in which queries were submitted, even
sive dataset of human and synthetic texts and shown to ac-          in cases where multi-turn interactions were conducted en-
curately discern AI-generated from human-authored content           tirely in English. This choice enables the retrieval and analy-
(Emi and Spero 2024).                                               sis of the sources generative search engines cite in responses
   Overall, we find that the existing literature on auditing        to individual queries, rather than sources cited in multi-turn
generative search engines has not yet explored the evalua-          conservational interactions between users and the system (a
tion of cited sources for the presence of AI-generated con-         limitation of our study that we highlight the implications of
tent in responses to users queries across topics of public im-      in the limitations section). After de-duplicating queries, this
portance, such as politics, health, and the environment. This       transformation process resulted in a total of 11,185 single-
turn and unique queries in English. Next, to determine which       was not uniformly trivial across all queries, as it required
of these queries are on politics, health, or the environment,      reading each query and attempting to identify keywords that
we first had to determine the topical scope of these queries       might indicate irrelevance. For instance, encountering terms
and then assess their relevance to our topics of interest.         such as “Tesco” (a British multinational grocery store) or
   Using BERTopic (Grootendorst 2022), a topic model-              “Zapatista Army of National Liberation (EZLN)” (a politi-
ing technique that leverages transformer-based embeddings          cal group in Mexico) required additional information lookup
to produce interpretable topics, we followed the open-             by the authors to determine whether the query was rele-
source pipeline developed by the authors of Search Arena           vant. While this presents a limitation to our approach in ex-
for identifying common topics from queries in the dataset          cluding queries, our experience may help inform future re-
(Tang, Angelopoulos, and Chiang 2025). Our decision to             searchers to anticipate the presence of such instances when
use BERTopic stems from its approach, which enables the            dealing with datasets that are multilingual or have been col-
assignment of queries to topics through a zero-shot method         lected from users across multiple nations. For instance, we
while still allowing qualitative evaluation of the generated       excluded queries that primarily focus on regions beyond the
topics. In this pipeline, queries are first transformed to high-   U.S. (e.g., “How does supply chain bifurcation impact Aus-
dimensional vector embeddings, which is then used to iden-         tralia”; “why only germany not embrace Modern Monetary
tify topic clusters. This process resulted in queries being        Theory in rich nation?”), political queries discussing issues
grouped into 76 topics spanning a wide range of domains,           that are not directly relevant to the U.S. (e.g., “Why is Tai-
including sports, music, gaming, financial advice, legal ad-       wan a country?”; “Did the premier of China Xi encourage
vice, and others. To map these topics, and the queries associ-     the youth to forego college and instead go for manufacturing
ated with them, back to the three topic categories of interest     jobs?”), or health related queries or topics specific to other
(politics, health, and the environment) we operationalize the      countries (e.g., “Talk me through the next procedure may see
definition for each topic category based on prior research de-     in UK for pediatric patient”). As a result, 432 queries (∼32%
scribing these topics in the context of online search. Queries     of 1,325 queries) were retained that are on politics (N=257)
on politics involve seeking, monitoring, or evaluating infor-      and health (N=175) that fit our query selection criteria.
mation about political actors, parties, issues, or events. Such
queries are typically motivated by informational needs in-
cluding uncertainty reduction, belief validation, or prepara-
tion for political decision-making (Menchen-Trevino et al.            Queries on health in our sample include one topic clus-
2023; Dutton et al. 2017). Health-related queries are char-        ter focusing on seeking information about supplements (e.g.,
acterized by seeking information, clarification, or guidance       “Which foods Contain all essential amino acids? Protein
concerning health issues, symptoms, diseases, and medica-          Drinks?”), vaccines (e.g., “should children get their second
tions, as well as wellness practices and recommendations           mmr vaccine early among a measles outbreak?”), and medi-
(Jia, Pang, and Liu 2021; Zhu et al. 2025; Swire-Thompson          cations (e.g., “what do you need to do to make the effects
and Lazer 2020). As for queries on the environment, they           of bromantane to last”), including questions about drug-
typically include questions aimed at understanding climate         drug interactions (e.g., “can i use zofran and bisacodyl to-
change, its causes, consequences, and potential mitigation         gether”), and the other topic cluster includes informational
or reversal measures, as well as exploring earth systems and       queries related to mental, physical, or physiological health
alternative energy sources (De La Calzada et al. 2024).            concerns (e.g., “what are the effects of nose breathing and
   Using the definitions described above, authors conducted        mouth taping on face/jaw structure?”; “How to prevent ner-
a manual review of a random sample of five representative          vous tongue scratching against the teeth?”). As for queries
queries from each of the 76 topics produced by the topic           on politics, the topics spanned over U.S. political leadership
modeling pipeline. This review enabled us to identify eight        and governing institutions, with a focus on President Don-
topics (two on health and six on politics) comprising 1,325        ald Trump and his administration (e.g., “Do you think Don-
queries that fall within the domains of politics and health.       ald Trump and his administration members participated in
However, no queries were found to be related to the environ-       insider trading?”), evaluating the consequences of a public
ment other than weather inquires (e.g., “what is weather like      policy (e.g., “Which universities and states will be most im-
today?”) which are not considered relevant under our defi-         pacted by the denial of funds on science?”), U.S. imposed
nition of environment-related topics. Because the dataset in-      tariffs and trade wars (e.g., “What is the effect of the ongo-
cludes queries from users across 136 countries, authors have       ing tariffs enacted by trump”), informational queries about
subsequently discussed and then performed a joint open re-         political actors aimed at uncertainty reduction (e.g., “Who
view of these queries to ensure relevance to U.S. contexts.        is the current U.S. ambassador to Israel, and how might they
We chose to exclude queries that are not relevant to the U.S.      engage in diplomacy?”; “When was the last time a sitting
because (1) all four generative search engines under audit are     president visited Waco, TX?”), queries pertaining to belief
developed primarily in the United States, and (2) the eval-        formation (e.g., “Why the young men shifted towards the
uation of the quality of citations included in responses to        right wing”; “Fascist authors and philosophers that opposed
queries on topics that are relevant to other regions requires      electoralism”; “Authors who claimed that technology could
domain and contextual expertise specific to the information        usher in a communist economy”), and other inquiries con-
ecosystem in these regions, which the authors do not claim         cerning historical political events and outcomes (e.g., “Who
to have the expertise in. It is worth noting that this process     was 1st president in us”).
Curation & Selection for Queries on the                           better reflection of what actual users would see and how they
Environment                                                       could be impacted. To this end, we developed a custom web
Due to the absence of environment-related queries in the          scraper in Python that uses Playwright (Playwright 2026), a
Search Arena dataset we rely on queries from the Climate          framework for web testing and automation, to simulate user
Q&A dataset (De La Calzada et al. 2024) for this topic. This      behavior on generative search engine.
dataset includes 3,425 single-turn queries, collected between        For each generative search engine, the scraper navigates
April and March of 2023, distributed across 16 languages          to the website corresponding to each engine, inserts the
submitted by users mostly from France that are interact-          query in the text area of the search bar, activate the web
ing with an answer engine (i.e, a Chatbot) that responds to       search (if needed as is the case for ChatGPT), and then mon-
environment-related queries regarding users’ actions on na-       itors changes in the HTML source code of the web page
ture (e.g., transportation or food choices) using over 14,000     while the answer is being generated until no more changes
pages of scientific literature sourced from the Intergovern-      are observed in the source code. Once an answer is fully
mental Panel on Climate Change (IPCC) and Intergovern-            generated, the scraper then clicks on the button correspond-
mental Science-Policy Platform on Biodiversity and Ecosys-        ing to the sources (or citations) to view the full list of cited
tem Services (IPBES) reports(Calzada et al. 2024). Queries        sources in the response. Although some engines display re-
in this dataset are distributed over fifteen topic categories     lated sources beyond the cited sources, we only focus on
(see Appendix A.9) ranging from questions about earth sys-        scraping the sources cited by the generative search engine in
tems (e.g., “What will be the sea level rise in 10 years”) to     the response. Accordingly, for each cited source in the re-
inquiries about the potential actions companies could take to     sponse, we scrape the source title, source URL, and source
mitigate climate change (e.g., “what need to be done inside       snippet (i.e., short description of the source, if available).
companies to fight climate change ?”).                               The final dataset collected includes 26,266 unique URLs
   Unlike the Search Arena dataset where the language is an-      (i.e., sources) linking to 7,675 unique web domains featuring
notated and provided by the dataset creators, in this dataset     online content that were cited by the four generative search
we employed Python’s langdetect library on all queries and        engines. In the following section, we describe the procedure
excluded the ones that are not in English. As a result, we re-    used to audit generative search engine citations for evidence
tain 77.9% of all queries (N=2,668) as the sample of queries      of AI-generated content.
in English. Next, we sampled 20% of the queries in English
(N=534) for further analysis. All queries were reviewed for
                                                                  Detecting AI-generated content
regional relevance, following the same procedure applied to       The first step to identify AI-generated content among the
the Search Arena dataset. Accordingly, queries explicitly fo-     26,266 sources cited by generative search engines is to
cusing on environment-related impacts, policies, or mitiga-       scrape the content for each source. To this end, we devel-
tion strategies for countries or regions other than the U.S.      oped a Python script that programmatically visits each of
were excluded (e.g., “what are the top 3 cost effective solu-     the 26,266 source URLs and uses newspaper3k (Newspaper
tions for mitigating climate change in France?”; “What will       Contributors 2018) to extract the main body text from each
be tje sea level in france in 2100?”; “what will be climate im-   webpage. Out of the total URLs in our dataset, we success-
pacts on switzerland?”). Based on this screening criteria, we     fully scraped the content of 19,154 (72.9%) URLs. The re-
retained 52.4% of the queries (N=280) that also preserve the      maining URLs could not be scraped because they linked to
relative distribution of topic categories present in the origi-   other data formats beyond text, including PDFs and images
nal sample, as shown in Appendix A.10.                            (which we report on in the Limitations section). In addition,
   By aggregating queries from Search Arena and Climate           other URLs were not scraped because the content was either
Q&A datasets, our final sample (N=712) encompass queries          inaccessible or had been removed, per the HTML response
on politics (N=175; 24.5%), health (N=257;36.1%), and the         code.
environment (N=280; 39.3%). In the next section we de-               Next, we assess the performance of two prominent
scribe how they are used to audit four generative search en-      AI-detection tools, Pangram (Emi and Spero 2024) and
gines (ChatGPT, Copilot, Gemini, and Perplexity).                 GPTZero (Adam et al. 2026), in detecting AI-generated con-
                                                                  tent. Pangram is built on top of a transformer-based classi-
                      Methodology                                 fier trained on a large corpus of human and AI-generated
                                                                  text, which has been shown to achieve substantially lower
Scraping citations from generative search engines                 false positive and false negative rates than prior detection
Each query in the curated dataset (described in the previous      approaches (Russell et al. 2025a). In comparison, GPTZero
section) was submitted to four generative search engines:         uses a hierarchical classifier architecture that offers a “state-
ChatGPT (with web search enabled), Copilot, Gemini, and           of-the-art industrial AI detection solution, offering reli-
Perplexity using the user interface for each system. While        able discernment between human and LLM-generated text”
these systems each have their own APIs that would make in-        (Adam et al. 2026). Despite the overlapping objective for
formation collection simpler, prior studies have highlighted      both tools in detecting AI-generated content in text, they dif-
differences between responses to API requests and those           fer in their reporting of prediction scores. Pangram classifies
submitted via web interfaces (Schatto-Eckrodt et al. 2025).       text based on its likelihood of being either Highly Likely
We opted to capture the cited sources in the output these en-     AI (i.e., AI-generated), Unlikely AI (i.e., human), or Mixed
gine display to users in response to their queries as this is a   (i.e., AI-assisted text that is possibly or likely to involve the
use of AI) with confidence scores ranging from 0 (least con-        text identified as Mixed and Human-AI Mixed, respectively,
fidence) to 1 (most confident). Whereas GPTZero assigns             to involve the use of AI, we combined the scores of those
percentages that add up to 100 that represent the tool’s con-       instances with the scores of instances classified by Pangram
fidence in the likelihood in the classification of an entire text   and GPTZero as AI-generated for the same input text, and
across all three categories: AI, Human, or AI-Human Mix.            if the combined score exceeds the confidence score assigned
   Based on the objective of this study in detecting AI-            for the respective human category for each tool for that in-
generated content in cited sources by generative search en-         put, then we re-classify each of those instances as “AI”, in-
gines, it is critical to formally assess the performance of         dicating that these instances are AI-generated (or at least
these AI-detection tools based on their false positive (i.e.,       a mix of AI was used), otherwise we re-assign those in-
human-generated content being classified as AI-generated)           stances as “human”. As a result, 14 out of the 17 instances
and false negative (i.e., AI-generated content being classi-        categorized by Pangram as possibly or likely to involve the
fied as human generated) rates. We decided to conduct this          use of AI (i.e, Mixed) were re-categorized as AI-generated
assessment to ensure that we select the AI-detection tool           and only 3 were re-categorized as “human”. In contrast, all
that has the lowest false positive rate in order to avoid mis-      five instances of Human-AI Mixed categorized by GPTZero
classifying human-generated content in our corpus as AI-            were re-categorized as “AI”. Based on the re-categorization
generated, which consequently would inflate our results. At         of these instances, the new total number of AI-generated in-
the same time, and depending which AI-tool we proceed               stances classified by Pangram and GPTZero is 72 and 73
with, it is important to identify the false negative rate so the    with an average confidence score of 97.1% and 91.9%, re-
results are interpreted as a lower bound to the prevalence          spectively. As a result, we observe an 82% agreement be-
of AI-generated content cited by generative search engines.         tween Pangram and GPTZero in the assigned labels to each
It is important to recognize that, given our conservative se-       text being evaluated in our sample of articles. However, both
lection criteria for the AI-detection tool, the reported lower      tools also disagreed on 19 out of 105 articles. GPTZero clas-
bound in the subsequent section of AI-generated content re-         sified 10 out of 19 articles as AI-generated and 9 as human-
mains contingent on the specific tool employed, as discussed        generated (average confidence score=72.8%), whereas Pan-
further in the Limitations section.                                 gram classified 9 articles to be AI-generated and 10 articles
   In our evaluation of both Pangram and GPTZero on                 to be Unlikely AI (average confidence score = 0.91).
a curated dataset of 200 human-authored texts from the                  Assuming that the 105 articles are in fact AI-generated
RAID benchmark (Dugan et al. 2024) and 200 curated                  (a reasonable assumption based on the prior reporting of
AI-generated texts (as further described in A.1 and illus-          the domains producing AI-slop, but one we are not able to
trated in Figure A.13 of the Appendix) spanning the cate-           further validate) these results imply the false negative rate
gories of research abstracts, wikipedia pages, reddit posts,        of Pangram on this benchmark sample is 31.4%, compared
and news articles, we find that Pangram and GPTZero have            to GPTZero (∼30.4%), in correctly detecting AI-generated
100% accuracy in correctly detecting human-authored and             content. While there is still some discrepancy between the
AI-generated texts, respectively. This is relatively consistent     two detectors, we decide to take a conservative approach by
with near zero false positive rates (i.e., roughly 1 in 10,000)     moving our analysis forward using Pangram given its rela-
reported by the providers of these tools (Emi 2025).                tively higher false negative rate, which aligns with the ob-
   To further assess the performance of these tools in the          jective of our evaluation looking to identify the lower bound
wild, we compiled a benchmark dataset from seven web do-            of AI-generated (rather than human curated) source content.
mains spanning the categories of news, lifestyle, entertain-        While we acknowledge and recognize the implications of re-
ment, and technology, that were documented by journalists           lying on a single detector for our findings (see Limitations
and experts as AI-generated per a published report on “AI           section), we see the results we present in the next section
slop” in news media (Paviour 2025). A total of 105 articles         using this tool as a reasonable estimate of a lower bound.
were randomly sampled from the reported web domains by
selecting fifteen articles from the “latest news” section pub-                               Results
lished within the past six months from each of the seven            We collected a total of 2,848 responses by submitting 712
domains. This evaluation step was designed to assess the            queries on politics, health, and the environment to four gen-
robustness of Pangram and GPTZero, especially for false             erative search engines. These responses predominantly in-
negatives. Pangram classified 55.2% (N=58) of the 105 arti-         clude in-text citations (N=2596; 91.2%), but not always
cles as Highly Likely AI (i.e., AI-generated), with an aver-        (N=252; 8.8%). Out of the total number of responses that
age confidence score of 1 (i.e., the maximum level of confi-        do not have citations (N=252), 11.6% of all health-related
dence). Of the remaining articles, 16.2% (N=17) were classi-        queries (N=120) received a response with no citations, com-
fied as Mixed (average confidence score = 0.63), and 28.5%          pared to 8.2% (N=92) of all queries on the environment
(N=30) were classified as Unlikely AI (average confidence           and 5.7% (N=40) of all queries on politics having no ci-
score = 1). In contrast, GPTZero classified 64.7% (N=68)            tations in responses. Although the proportion of responses
out of the 105 articles as AI-generated (average confidence         with no citations is relatively small compared to the total
score = 91.8%), 4.7% (N=5) as Human-AI mix (average                 number of collected responses, it begins to shed light on how
confidence score = 93%), and 30.4% (N=32) as Human (av-             LLMs powering generative search engines occasionally rely
erage confidence score=92%).                                        on internal knowledge versus pulling in external sources to
   However, because both Pangram and GPTZero considers              help generate responses. Despite this infrequent behavior by
                                                                  ChatGPT     Copilot   Perplexity   Gemini
                    Avg. Number of Cited Sources Per Response      14.68       8.44       7.92        7.26
                    Number of Unique Source Web Domains             3,964      3,286      1,750       2,369
                    Number of Unique Cited Sources                 10,453      6,007      5,636       5,168

         Table 1: Descriptive statistics of cited sources per response by each generative search engine (GSE) provider.


GSE, relying on an LLM’s internal knowledge could expose           source web domains). By calculating the Gini index on the
users to outdated information and increase the risk of expo-       overall distribution of frequencies of the cited source web
sure to hallucinated and inaccurate information(Deng et al.        domains in the data, we find that the citations in aggre-
2025; Luo et al. 2025). This is particularly critical in high-     gate for all four generative search engines are unequally
stakes topics such as health, where users may turn to these        distributed over sources (Gini=0.68), indicating that cited
systems to find accurate information. In contrast, responses       sources show some concentration rather than being uni-
that included in-text citations contained an average of 9 ci-      formly drawn from the pool of sources. Moreover, when
tations per response. Among the audited systems, ChatGPT           evaluating the concentration of source web domains among
cited the highest number of unique sources per response, av-       cited sources per provider, we find ChatGPT to have the
eraging 14.7 sources, followed by Copilot (8.4), Perplexity        highest domain concentration amongst its sources (0.648),
(7.9), Gemini (7.3), as reported in Table 1.                       followed by Gemini (0.595), Perplexity (0.563), and then
   Reporting citation patterns at the provider level, we find      Copilot (0.492).
that out of the total number of unique sources in the dataset         To examine which sources are driving the concentration
(N=26,266), ChatGPT with web search accounts for the               of citations across and within each generative search en-
largest share of cited sources (N=10,453; 39.8%), followed         gine, we analyze the distribution of citation frequencies at
by Copilot (N=6,007; 22.9%), Perplexity (N=5,636; 21.5%),          the source web domain level. We find that the 25 most fre-
and then Gemini (N=5,168; 19.7%). At the topic level, we           quently cited source web domains across providers account
find that responses to environment-related queries include         for 23.8% of all citations (i.e., head of the distribution),
on average 10.9 citations, whereas responses to queries on         while the remaining 76.2% are distributed across a highly
health and politics, receive 8.4 and 7.7 citations on average,     skewed set of source web domains. Within this long-tail dis-
respectively (as described in Table 2). Furthermore, when          tribution, the majority of source web domains receive very
examining the proportion of cited sources across generative        few citations (59.1% are cited only once and 16.5% are cited
search engines at the topic–provider level, we divide the total    twice) while a small number of source web domains are
number of unique sources found per topic-provider pair by          cited disproportionately often, as illustrated in Figure 3(b)
the total number of unique sources for that particular topic       in the Appendix (also see Appendix A.4 for breakdown of
from Table 2. We find that ChatGPT accounts for the largest        these proportion by provider). This reflects a concentration
proportion of unique sources cited in responses to environ-        of many source web domains with very few citations (as il-
ment, health, and politics-related queries (0.46, 0.36, and        lustrated by the upper left peak of Figure 3(b)) compared to
0.31, respectively). Also, responses generated by ChatGPT          the cluster of very few source web domains being cited re-
to queries in these topics cite approximately 20, 12, and 10       peatedly, as illustrated in the bottom right corner of Figure
sources on average per response, respectively, which is more       3(b). Upon inspecting this trend among sources with very
than other providers (see Table A.2 in the Appendix).              few citations, we see a large proportion of source web do-
                                                                   mains have very few citations followed by a rapid drop in
                                     Env.   Health Politics        the proportion of source web domains with 3 or more cita-
   Number of Queries                  280   257       175          tions, as illustrated in 3(a) in Appendix A.12. This observed
   Total Unique Domains              3,481 2,958     1,741         long-tail in cited source web domains suggests that gener-
   Total Unique URLs                12,252 8,640     5,375         ative search engines rely on a somewhat narrow set of re-
   Avg. URLs per Query               10.94 8.40       7.68         peatedly cited domains in the head of the distribution while
   Proportion of Total Sources       0.466 0.329     0.205         predominantly surfacing a large number of minimally cited
                                                                   domains.
Table 2: Descriptive statistics of the unique cited source            Specifically, among the top 25 most cited source web do-
web domains and sources by topic category across ChatGPT,          mains across providers, Wikipedia is the single most cited
Copilot, Gemini, and Perplexity.                                   domain, accounting for 15.2% of the total number of ci-
                                                                   tations in the top 25 most cited source web domains. It is
   To measure the concentration of citations across unique         worth noting that when aggregating these most cited source
source web domains, we use the Gini index (Gini 1936)              web domains by category, government websites collectively
which provides a score that ranges from 0 to 1, where 0 indi-      account for 33.0% of citations among the top 25 source web
cates perfect equality (i.e., sources are uniformly distributed    domains, indicating a clear and relatively strong reliance
across all unique source web domains) and 1 indicates per-         on official sources. In contrast, social media websites, in-
fect inequality (i.e., sources are concentrated around a few       cluding Reddit and YouTube, account for 8.8% of citations
                                                                  ley AI” and “Likely AI” categories, we find evidence of
                                                                  a non-negligible share, of approximately 16% (N=3,056)
                                                                  of cited sources that were successfully scraped, to be AI-
                                                                  generated. Moreover, we found that the top 25 source web
                                                                  domains (i.e., head of the distribution) account for 2.9% of
                                                                  AI-generated sources as compared to 97.1% of AI-generated
                                                                  sources that account for the remaining source web domains.
                                                                  This finding further confirms the presence of a very long
                                                                  tail in source web domains that generative search engines
                                                                  source information from when generating responses to users
                                                                  queries.
                                                                     To further analyze the data between the various providers
                                                                  of generative search engines, we examined the proportion
                                                                  of unique sources cited by each provider that we were able
                                                                  to scrape and identify as AI-generated, relative to the total
 Figure 1: Distribution of Pangram prediction categories.         number of sources each provider cites across all responses to
                                                                  queries in our sample. We find Copilot to cite AI-generated
                                                                  sources in 27.8% (N=1,614) of its citations, which translates
among the top 25 source web domains. When combined,               to nearly 3 out of every 10 cited sources being AI-generated.
both government and social media web domains together ac-         Similarly, 14.7% (N=782) of Gemini’s cited sources were
count for a striking 41.8% of all citations within the top 25     found to be AI-generated, followed by Perplexity (N=472;
most frequently cited source web domains. Moreover, we            9.4%), and ChatGPT (N=765; 7.3%).
found that academic and scientific sources, including four           By aggregating the data back at the source web domain
major journal publishers (e.g., Nature, ScienceDirect, Fron-      level, we find that 28.0% (N=1,754 unique source web do-
tiers, MDPI) and websites (e.g., ResearchGate), together ac-      mains) out of all unique source web domains (N=6,258) in
count for 14.6% of citations. However, we observe minimal         the sample used for this analysis to have at least one source
representation of news media outlets among the top 25 most        labeled as AI-generated being cited in generative search en-
cited source web domains. For more details on the top 25          gines responses. Looking at the prominence of such con-
cited source web domains across and within each provider,         tent across source web domains with AI-generated sources
please refer to Table A.3 in the Appendix.                        as identified by Pangram in our sample, we find that 66.2%
                                                                  of the 1,754 source web domains have one AI-generated
Citation of AI-generated Sources                                  source, 17.7% have 2 AI-generated sources, and all remain-
As previously described in the methods section, we success-       ing domains (16.0%) have 3 or more AI-generated sources
fully scraped the content of 19,154 unique sources repre-         (as shown in Figure 2 in A.11). This raises a critical point
senting 72.9% of all unique sources in our dataset linking        with respect to a system-design trade-off between offering
to 6,258 unique source web domains (81.5% of all unique           answers that are substantiated by a diverse set of sources vs.
domains). For each of the 19,154 sources, we submitted the        being able to assess the quality of the long tail of sources in
scraped content to Pangram’s API to assess whether the text       terms of how they use AI in the production of content.
is AI-generated or not and to obtain a prediction score for          We also examined the top 35 source web domains with
each prediction category. The content corresponding to the        the most AI-generated sources cited by generative search
majority of the sources were determined by Pangram to be          engines, and their relative proportions to the total number
unlikely generated by AI (i.e.,“Unlikely AI”) (N=15,815;          of cited sources at the source web domain level (see Ta-
82.5%), followed by “Highly Likely AI” (N=2916; 15.2%),           ble 6 in the Appendix A.5 for details). This set accounts for
“Possibly AI” (N=283; 1.4%), and “Likely AI” (N=140;              24.7% of total AI-generated sources in our sample, suggest-
0.7%), as illustrated in Figure 1.                                ing that responses for generative search engines tend to be
   Based on the the distribution of Pangram scores for each       substantiated with AI-generated sources more from the long
prediction category (as shown in Appendix A.14), we ex-           tail of cited sources. This includes social media sites such as
clude the “Possibly AI” category from further analysis. This      Reddit, government (e.g., pmc.ncbi.nlm.nih.gov, earth.gov)
conservative decision is based primarily on the difficulty        and intergovernmental (e.g., climatepromise.undp.org) sites,
in interpreting this category due to its ambiguity in terms       as well as a number of sites that are narrowly tailored
of whether it represents an instance of content that is co-       niche sites (many using .org domain names) about envi-
authored with an AI system, or whether it reflects the uncer-     ronment and health, and a couple that are news sites (e.g.
tainty in discerning between human and AI-generated con-          m.economictimes.com , timesofindia.indiatimes.com). The
tent. In addition, this decision also helps avoid inflating our   eighth largest source web domain, with 28 sources detected
estimates of AI-generated content in the data given that we       as AI-generated, was www.factually.co, a website which on
have no ground-truth to compare the predictions in this cat-
egory with1 . That said, when combining the “Highly Lik-          Likely AI and manually checked for AI-use disclosure statements,
                                                                  but found, consistent with prior research (Russell et al. 2025b), no
   1
       We sampled 200 URLs classified as Likely AI or Highly      instances where such use was disclosed.
its homepage characterizes itself as an “AI-powered research     health-related queries (about 1 in 9), indicates that gener-
tool” and adds that “Is it perfect? No. Accuracy is hard. Con-   ative “search” engines do rely on their pre-training to an-
sistency is hard. We’re working on it.”                          swer some questions, raising questions about the timeliness
   At the topic level, we find AI-generated sources to be the    of responses and about instances in which these engines may
most present in responses to environment-related queries,        rely on an LLM’s internal knowledge rather than sourcing
constituting 13.3% (N=1,633) of all cited sources in this        information from the web. In addition, we reveal insights
topic category. This is followed by health-related queries       about the disproportionately concentrated sourcing practices
and those on politics where AI-generated sources account         around a handful of source web domains across all four gen-
for 16.3% (N=1,408) and 11.1% (N=592) of all cited sources       erative search engines. Specifically, we show the degree of
in each category, respectively.                                  concentration of cited sources around a few source web do-
   Switching the analysis to be at topic-provider level, and     mains, while a preponderance of source citations derived
as reported in Table A.6, we find Copilot to consistently cite   from a long tail of source web domains the majority of
the highest proportion of AI-generated sources across all        which are cited only once or twice. We find evidence that
three topics. In sources cited in responses to environment-      the content of sources linking to some of these domains
related queries, Copilot cites AI-generated sources the most     to be AI-generated, constituting approximately 16% of all
(N=607; 4.9% of the total citations for this topic category),    sources cited by generative search engines in response to
followed by ChatGPT (N=486; 3.9%), Gemini (N=365,                queries on politics, health, and the environment. In addition,
2.9%) and with Perplexity citing the least number of AI-         the top 35 source web domains with the highest number of
generated sources for this topic category (N=175; 1.4%). A       AI-generated source content accounts for 24.7% of the total
similar pattern is observed for health-related queries, where    AI-generated source content in our sample. This indicates
Copilot leads all four generative search engines in the num-     that answer engines substantiate more sources from the long
ber of cited sources with AI-generated sources (N=655;           tail less or no clear regards to the quality of such content that
7.6% of the total citations for this topic category), followed   users see.
by Gemini (N=316; 3.6%), Perplexity (N=237, 2.7%), and              Our findings raise critical questions about the quality of
ChatGPT (N=200; 2.3%) citing the least number of AI-             the information ecosystem as it evolves with the increas-
generated sources on this topic. As for cited sources on         ing use of generative AI, both by companies using it for
politics, Copilot was also found to cite the highest number      generative search responses, as well as by institutions and
of AI-generated sources (N=352; 6.5%), followed by Gem-          content-creators using it on the broader internet (Kieslich,
ini (N=101; 1.8%), ChatGPT (N=79, 1.4%), and with Per-           Diakopoulos, and Helberger; Kieslich, Helberger, and Di-
plexity citing the least number of sources with AI-generated     akopoulos 2024). While AI-generated content is not neces-
source content (N=60; 1.1%), as described in Table A.6. Fi-      sarily low quality, known issues with the accuracy of content
nally, we report the most frequently cited source web do-        due to hallucination or gaps in human oversight among pro-
mains per provider for each topic in Table A.7 to illus-         fessionals (Nishal and Diakopoulos 2024), the potential for
trate the variability between providers with respect to the      large scale influence operations through pollution of the in-
sources they cite that are AI-generated. For instance, the ta-   formation ecosystem (NewsGuard Technologies, Inc. 2025),
ble shows that Perplexity often leans on Reddit sources that     and emerging demands among end-users for labels to sup-
are AI-generated in responding to health-related queries and     port their agency in opting out of consuming AI-generated
those on politics, whereas Gemini and ChatGPT reference          content (Wittenberg et al. 2024), all suggest that a profu-
AI generated sources on health via the nih.gov website. In       sion of AI generated content being referenced in genera-
contrast, Gemini cites AI-generated sources from Times of        tive search results is a troubling development. Our findings
India (timesofindia.indiatimes.com) in responses related to      draw further attention to the reliance of generative search
queries on politics.                                             engines on social media sources, such as Reddit, and of-
                                                                 ficial sources (e.g., government websites), and that addi-
                        Discussion                               tional work is needed to assess the credibility and qual-
                                                                 ity of information on these websites, not only ones which
This research undertakes an audit of the citations of four       self-disclose their use of AI, but also professional publish-
popular generative search engines (ChatGPT, Copilot, Gem-        ers (e.g. Times of India and Economic Times) who may use
ini, and Perplexity) when responding to users’ queries on        generative AI in production pipelines with (or perhaps with-
three topics of public importance: politics, health, and the     out) appropriate oversight (Russell et al. 2025a). Topic spe-
environment. To do so, we first identified the range of source   cific advocacy sites are proliferating online and finding their
web domains these engines rely on in responding to users’        way into response answers on environmental and health top-
queries, tabulated their prevalence, identified whether or not   ics, while the prevalence of government citations raise ad-
the source content cited from those domains is AI-generated,     ditional questions about the bias of sources cited (Zhang
and then we examined the presence of such content among          et al. 2025). Accordingly, without such assessments focus-
cited sources, topic categories, and providers. Our findings     ing on bias, information quality, and credibility of sources,
highlight ongoing limitations in the reliability of these en-    as well as the contexts in which this type of content is used to
gines, especially when responding to queries on critical         help determine its potential risks to users, AI-generated con-
topics (politics, health, and the environment). For instance     tent may continue to circulate on GSEs without sufficient
the proportion of responses without citations, especially for    scrutiny. Notably, we found that majority of AI-generated
source content from government websites originate from              tual expertise of the information ecosystem in these regions
pmc.ncbi.nlm.nih.gov and earth.gov. However, it is unclear          which the authors do not have. In addition, queries in our
whether these instances reflect high-quality or lower-quality       sample were limited to single-turn interactions with gener-
AI-generated content that has made its way into official web-       ative search engines. Although this has facilitated the audit
sites.                                                              of the four generative search engines through retrieving and
   Overall, this work reflects an initial step towards inform-      analyzing a range of sources that were cited in responses to
ing future risk mitigation and source management strategies         these queries, future audits should expand on this work to
needed to manage information quality in generative search           include a deeper analysis of the composition of sources, the
engines. Our findings can support such efforts to improve the       quality and bias associated with these sources, and how such
reliability of generative search engines by informing risk as-      sources could vary over time in multi-turn conversational
sessors and developers about the sourcing practices of these        flows as various interaction dynamics may yield different
systems through the identification of web domains with AI-          citation patterns by these engines and therefore warrant fur-
generated content, thereby contributing toward enhancing            ther analysis.
the information quality these systems. While our analysis of           Third, prior research suggests that the majority of genera-
AI-generated content is focused on reporting the presence of        tive search engines, including those in our audit, tend to ex-
such content among cited sources, future work focusing on           hibit left-leaning tendencies when responding to questions
analyzing the characteristics of such sources (e.g., accuracy,      on key topics within the categories of politics, health, and
writing style, word selection, or claims included in the text)      the environment (Yang 2025; Rozado 2022; Dai et al. 2025),
and which of these characteristics is influencing how gener-        which limits the generalizability of our findings to systems
ative search engines embed and surface such content in their        with potentially different value alignments (e.g., Grok). Ac-
final responses would complement our findings by helping            cordingly, future audits are encouraged to account for varia-
to reveal the inner processes of generative search engines          tions across regions, languages, and value systems to under-
related to information selection processes which presently          stand how such differences may shape citation patterns of
appear to prioritize the number and range of sources over           sources by generative search engines.
their quality.                                                         Fourth, although this research is concerned with analyz-
                                                                    ing text-based content of sources for the presence of AI-
                        Limitations                                 generated content, we also note that the remaining 7,112
Although our study audits four prominent generative search          sources that we could not scrape from the total number of
engines across topics of public importance, it also has its         unique sources in our sample (N=26,266) reflect formats and
limitations. First, our sample consists of queries from the         modalities beyond text. For instance, 14.2% of the sources
Search Arena dataset (Miroyan et al. 2025) that span the            we could not scrape were URLs linking to PDF files on
domains of politics and health. However, for environment-           various websites. Also, we could not fetch the content of
related queries, this dataset did not include queries that have     16.2% of the overall sources cited by generative search en-
topical scope beyond weather queries (e.g., “what is weather        gines because they appear to be in other modalities, such
like today?”) that fit the definition of this topic, as mentioned   as we observed in links to videos2 and images3 on Face-
earlier in the paper. While this reflects a gap in the Search       book. Such instances were not accounted for in our analysis
Arena dataset, which has motivated us to look for Climate           of AI-generated content and therefore our study falls short
Q&A dataset (De La Calzada et al. 2024) that includes               in analyzing them, though they are surely of interest for fu-
environment-related queries, it does not necessarily indicate       ture information quality research to assess how information
that such queries are not present or prominent among users          across modalities (some of which may be low quality on-
using generative search engines. Rather, it is very plausible       line memes, marketing, or propaganda) is integrated into re-
that the gap in Search Arena is a result of a bias in the sam-      sponses.
ple, which has implications on the range of topics that are            Lastly, our evaluation of AI-detection tools (Pangram and
present in (or absent from) users queries. Therefore, we rec-       GPTZero) in the wild is based on a curated dataset of AI-
ommend for future studies to acknowledge and try to ad-             generated content from news media that have been identi-
dress biases, beyond topical gaps, in any sample used for           fied by journalists. The criteria for selecting which tool to
auditing generative search engines, including the dispropor-        employ in our study was based on assessing the false neg-
tionate representation of users submitting queries from some        ative rate for each tool. However, the lack of availability
regions (e.g., global north) over others (e.g., global south),      to well established benchmarks that facilitate a more robust
and the implications of these biases on the characteristics of      evaluation of these tools across various types of content be-
the sample and interpretability of the results.                     yond news media (e.g., academic blogs or government web-
   Second, we limited queries in our sample to those that are       sites) and across various domains of use presents another
in English language and excluded from them queries that are         limitation to our evaluation of these tools. Therefore, we in-
referring to regions outside of the U.S. All four generative        vite future research to establish a public leaderboard that re-
search engines under audit are developed primarily in the           flects the evaluation criteria for these tools and presents their
United States and the evaluation of cited sources for region-       performance across various content types (e.g., news, aca-
specific queries (e.g., “What are the current poling numbers
                                                                       2
for the czech political party ODS?”) or even in other lan-                 https://tinyurl.com/3f83mpuv
                                                                       3
guages is encouraged but would require domain and contex-                  https://tinyurl.com/mry6f2tm
demic papers) and modalities. Such a resource could help          transparency around the types of sources used, and the qual-
guide researchers in selecting the most performant tool or        ity of their content in generating responses to users’ queries.
model depending on their use case and enhance the trans-          If such mitigation measures are not taken, users of these sys-
parency in this nascent area of research. Moreover, while         tems may be exposed to AI-generated content that may con-
we attempted to contextualize our evaluation of false posi-       tain false or misleading information, potentially resulting in
tives in Pangram’s predictions on our corpus, as articulated      harm particularly in high stakes domains such as health and
in section 4.2, the absence of disclosure statements for the      politics.
use of AI in content online presents a challenge in truly vali-
dating whether content online is AI-generated or is authored
by a human using AI to resolve issues with content (e.g.,
resolving spelling or grammatical mistakes). Accordingly,
the interpretation of our findings is constrained to the use of
Pangram only and that using another AI-detection tool may
yield different proportion of AI-generated content among
cited sources, especially if these tools vary in their false
positive and false negative rates. Thus, we recommend for
researchers to present their results from using AI-detection
tools as a lower-bound, or potentially ensemble results from
various models, especially as these tools continue to evolve
over time.
   Despite the aforementioned limitations, findings pre-
sented in this study highlight a critical and emerging risk:
the presence of AI-generated sources among cited sources
used by generative search engines, with approximately one
in five cited sources on average being AI-generated and used
to synthesize responses to user queries. In addition, by dis-
closing the limitations of this study, we hope future audits
of generative search engines can work towards addressing
and resolving these limitations in order to have better under-
standing about the citation dynamics and the proportion of
AI-generated content being cited and used on these engines.
Lastly, our findings, especially with respect to the presence
of AI-generated content on government websites, establish a
baseline that future research can compare and contrast their
results as they assess the proliferation of AI-generated con-
tent online beyond those cited by generative search engines.

                       Conclusion
This research audits the citations used by four prominent
generative search engines when responding to queries on
topics of public importance: politics, health, and the envi-
ronment. By analyzing the distribution and concentration of
cited sources, we find generative search engines to unequally
cite sources of information, relying on a narrow set of source
web domains some of the time, but more predominantly re-
lying on a long tail of minimally cited source web domains,
the majority of which are cited only once or twice. Upon
inspecting the content of the cited sources we find approxi-
mately 16% of all unique cited sources to be AI-generated.
Through our findings, this work is positioned to serve an ini-
tial step towards informing future risk mitigation and source
management strategies needed to manage the citation of AI-
generated sources in generative search engines.
   As the information ecosystem on the internet continues
to evolve, and considering that AI-generated content is not
necessarily always low in quality, developers of these en-
gines bare partial responsibility in implementing governance
strategies to manage information quality of cited sources on
their systems. One approach to do so is by enhancing the
                                                        A    Appendix

A.1   Evaluating AI-detection tools


To estimate the false positive rate for Pangram and GPTZero, we randomly sampled 200 human written text from the RAID
benchmark, the largest and most challenging benchmark dataset for machine-generated text detectors (Dugan et al. 2024). The
RAID dataset includes human-written text from various sources, including abstracts of published research papers, wikipedia
pages, reddit posts, and news articles. All human text included in the RAID benchmark were published pre-2022 (i.e., prior to
the public release of ChatGPT) and retrieved via the Wayback Machine (Internet Archive n.d.). The 200 human-written texts
in our sample were uniformly distributed across the following categories: research abstracts (N=50), wikipedia pages (N=50),
reddit posts (N=50), and news articles (N=50). Each human-written text in our sample was sent to Pangram and GPTZero via
their respective API to determine whether each content is AI-generated or not. We found that both Pangram and GPTZero have
correctly classified all human-written text as “human”, indicating 100% accuracy and zero false positive rate.
   Next, using the sample of 200 human-written texts, we stratified the dataset by large language model (LLM) and content
category (i.e., research abstracts, wikipedia pages, reddit posts, and news articles). We then prompted three models, GPT-5.3
(N=70 samples), Gemini-3 (N=65 samples), and Claude-Haiku-4.5 (N=65 samples), using the prompt in A.13 to generate text
conditioned on the first four words of the leading sentence from each human-written texts. Our selection of the aforementioned
three LLMs was based on the fact the AI-generated texts in the RAID benchmark were produced using comparatively older
models, whereas our study employs recently deployed frontier models that we leverage for text-generation. Consequently, we
suspected that the capabilities of newer models may generate text that is more difficult for AI-detection tools to identify.
   Accordingly, the final curated dataset includes 200 AI-generated texts spanning the categories of research abstracts, wikipedia
pages, reddit posts, and news articles. We ensured that each LLM generated outputs across all content categories (see Appendix
A.13 for the prompt template), following the approach proposed in RAID and Pangram (Dugan et al. 2024; Emi and Spero
2024). In addition, all generated texts were reviewed by the authors to ensure that they did not relate to or explicitly restate
the original human-written texts from the RAID benchmark. Each AI-generated text was later sent to Pangram and GPTZero
via their respective API for evaluation. Both Pangram and GPTZero detected AI-generated text with 100% accuracy as being
AI-generated.



A.2   Number of unique sources cited by each Generative Search Engine



                                                                                                                     Prop. of
                              Number of      Avg. Sources   Prop. of Unique Sources   Prop. of Unique Sources   All Unique Sources
 Provider     Topic
                            Unique Sources    Per Query              (Topic)                 (Provider)             (N=26,266)
              Environment       5646            20.16                0.46                      0.54                    0.21
 ChatGPT      Health            3121            12.14                0.36                      0.30                    0.12
              Politics          1686             9.63                0.31                      0.16                    0.06
              Politics          1586             9.06                0.30                      0.26                    0.06
 copilot      Health            2072             8.06                0.24                      0.34                    0.08
              Environment       2349             8.39                0.19                      0.39                    0.09
              Environment       2714             9.69                0.22                      0.53                    0.10
 gemini       Politics          1179             6.74                0.22                      0.23                    0.04
              Health            1744             6.79                0.20                      0.34                    0.07
              Health            1972             7.67                0.23                      0.35                    0.08
 perplexity   Politics          1168             6.67                0.22                      0.21                    0.04
              Environment       2028             7.24                0.17                      0.36                    0.08

Table 3: Unique sources cited by each system and topic. To calculate the average number of sources per query, we divide the
number of unique sources for each topic by the number of queries corresponding to that topic in the dataset. As described in
the Data section, the number of queries is 280 for environment, 257 for health, and 175 for politics. In order to calculate the
proportion of unique sources per topic, we divide the total number of unique sources for each provider-topic pair by the total
number of unique sources for each topic (environment is 12,252; health 8640; and politics is 5375).
A.3   Top 25 most cited domains across Generative Search Engines

      Domain                       Number of Citations      Category                      Share of Total Citations(%)
      en.wikipedia.org                      1189            Encyclopedia                              3.6354
      pmc.ncbi.nlm.nih.gov                  1078            Government                                 3.296
      www.sciencedirect.com                  672            Research Publisher                        2.0547
      www.reddit.com                         520            Social Media                              1.5899
      www.epa.gov                            454            Government                                1.3881
      www.un.org                             357            International Organization                1.0915
      www.whitehouse.gov                     304            Government                                0.9295
      www.ipcc.ch                            267            International Organization                0.8164
      www.climate.gov                        249            Government                                0.7613
      science.nasa.gov                       228            Government                                0.6971
      www.theguardian.com                    218            News                                      0.6665
      www.weforum.org                        215            International Organization                0.6574
      www.wri.org                            212            International Organization                0.6482
      www.nature.com                         183            Research Publisher                        0.5595
      www.healthline.com                     170            Information Publisher                     0.5198
      www.youtube.com                        165            Social Media                              0.5045
      www.mdpi.com                           162            Research Publisher                        0.4953
      www.britannica.com                     156            Encyclopedia                               0.477
      www.pbs.org                            150            News                                      0.4586
      www.frontiersin.org                    147            Research Publisher                        0.4495
      www.iea.org                            147            International Organization                0.4495
      www.researchgate.net                   141            Research Platform                         0.4311
      pubmed.ncbi.nlm.nih.gov                138            Government                                0.4219
      my.clevelandclinic.org                 132            Medical Organizations                     0.4036
      www.cdc.gov                            131            Government                                0.4005

Table 4: Top 25 most frequently cited domains across providers and their corresponding share of total citations in the dataset.

A.4   Concentration of cited domains by each Generative Search Engine

        Provider      Top 25 Domains’ Share of Citations (%)        Gini Index     Domains with ≤ 2 Citations (%)
        ChatGPT                        29.89%                          0.648                    82.81%
        Gemini                         27.92%                          0.595                    72.46%
        Perplexity                     31.58%                          0.563                    88.43%
        Copilot                        15.56%                          0.493                    86.93%

                 Table 5: Concentration and inequality of cited domains by provider, ordered by Gini index.
A.5   Domains with AI-generated content

Domain                            Highly Likely AI Likely AI Possibly AI Unlikely AI Total URLs AI-Generated URLs Proportion
www.iere.org                             62            0         0           0         62              62              1
www.reddit.com                           61            0          2        457        520              61            0.12
www.pmc.ncbi.nlm.nih.gov                 40            4         20        1014       1078             44            0.041
www.biologyinsights.com                  41            0          0         0          41              41              1
www.climate.sustainability-              37            0         0           0         37              37              1
directory.com
www.timesofindia.indiatimes.com          30            5         8          35          78             35            0.45
www.greenly.earth                        31            0         2          26          59             31            0.53
www.factually.co                         28            0         0           0         28              28              1
www.numberanalytics.com                  26            0         0           0         26              26              1
www.greenpacks.org                       24            0         0           0         24              24              1
www.earth.org                            24            0         1         103         128             24            0.19
www.maweb.org                            24            0         0           0         24              24              1
www.allaboutamerica.com                  21            0         0           0         21              21              1
www.recovered.org                        19            0         0           1          20             19            0.95
www.pollution.sustainability-            17            0         0           0         17              17              1
directory.com
www.lifestyle.sustainability-            16            0         0          0          16              16              1
directory.com
www.energy.sustainability-               16            0         0          0          16              16              1
directory.com
www.en.wikipedia.org                     14            1         8         1157       1180             15            0.013
www.shunwaste.com                        15            0         0           0         15              15              1
www.theglobalstatistics.com              15            0         0           0         15              15              1
www.thegoodbug.com                       14            1         0           0         15              15              1
www.climatecosmos.com                    13            1         0           0         14              14              1
www.climateimpact.com                    13            0         1           2         16              13            0.81
www.news.sustainability-                 13            0         0           0         13              13              1
directory.com
www.medshun.com                          13            0         0           0         13              13               1
www.sciencenewstoday.org                 13            0         0           0         13              13               1
www.okonrecycling.com                    12            0         0           0         12              12               1
www.globalbioenergy.org                  12            0         0           0         12              12               1
www.solartechonline.com                  12            0         0           0         12              12               1
www.frontiersin.org                      12           0          3         129         144             12            0.083
www.m.economictimes.com                  12           0          1           7          20             12              0.6
www.climatepromise.undp.org               0           12         46         20          78             12             0.15
www.earth.gov                            11           0          0          66          77             11             0.14
www.finance.yahoo.com                     9           2          0          62          73             11             0.15
www.fiveable.me                          11            0         0           0         11              11               1

Table 6: Domain-level distribution of AI-generated content and their respective proportion out of the total sources cited by
generative search engines that were successfully scraped for that domain. The highlighted rows show the domains with 100%
of their cited content to be AI-generated.
A.6   Number of unique AI-generated sources by topic and provider

           Topic Category       Provider      Unique Sources      Total Unique Sources Per Topic         Proportion
           Health               Copilot             655                          8640                        7.6
           Politics             Copilot             352                          5375                        6.5
           Environment          Copilot             607                         12252                        4.9
           Environment          ChatGPT             486                         12252                        3.9
           Health               Gemini              316                          8640                        3.6
           Environment          Gemini              365                         12252                        2.9
           Health               Perplexity          237                          8640                        2.7
           Health               ChatGPT             200                          8640                        2.3
           Politics             Gemini              101                          5375                        1.8
           Politics             ChatGPT              79                          5375                        1.4
           Environment          Perplexity          175                         12252                        1.4
           Politics             Perplexity           60                          5375                        1.1

Table 7: Number of unique sources identified as AI-generated by topic and provider. Values in the table are sorted by the number
of unique sources column from from highest to lowest.

A.7   Most cited domains by Generative Search Engine by topic

                    Topic Category Provider Most Cited Domain                              Citation Count
                    climate          Copilot www.iere.org                                         55
                    climate          Gemini www.climate.sustainability-directory.com              15
                    climate          ChatGPT www.climate.sustainability-directory.com             15
                    climate          Perplexity www.reddit.com                                    16
                    health           Copilot www.biologyinsights.com                              33
                    health           Gemini www.pmc.ncbi.nlm.nih.gov                              13
                    health           ChatGPT www.pmc.ncbi.nlm.nih.gov                             10
                    health           Perplexity www.reddit.com                                    10
                    political        Copilot www.factually.co                                     21
                    political        Gemini www.timesofindia.indiatimes.com                       21
                    political        ChatGPT www.en.wikipedia.org                                  6
                    political        Perplexity www.reddit.com                                    13

                                  Table 8: Most cited domain by provider within each topic.
A.8   Taxonomy of query intent from Search Arena

  Category                     Description
  Text Processing              Users request linguistic tasks such as summarizing, translating, paraphrasing, or refining
                               text.
  Creative Generation          Users request original creative outputs, including fictional scenarios, satire, poetry, story-
                               telling, or other forms of artistic language generation.
  Factual Lookup               Users seek to retrieve a precise, objective fact or specific information (what/who/when-like
                               questions).
  Information Synthesis        Users seek a concise, aggregated summary that combines facts or perspectives from multiple
                               sources. The focus is on integrating factual content without requiring reasoning, subjective
                               interpretation, or personalization.
  Analysis                     Users seek a reasoned judgment or breakdown of a topic, often involving comparison, evalu-
                               ation, weighing different perspectives, and synthesizing material from many sources. Often
                               open-ended.
  Recommendation               Users request suggestions or advice tailored to particular constraints, preferences, or speci-
                               fied criteria. Often implies personalization or ranking.
  Explanation                  Users seek detailed clarifications, educational insights, or thorough elaborations aimed at
                               better understanding a concept, process, or phenomenon. May ask “why” or “how” some-
                               thing works without implying action.
  Guidance                     Users request instructions, procedures, or practical advice intended to accomplish specific
                               tasks, typically involving sequential steps or troubleshooting. Usually framed as “how to”
                               or involving action.
  Other                        Prompts that don’t fit neatly into any of the categories above. Prompts may be malformed,
                               declarative in nature, or lacking in meaningful user intent.

 Table 9: Query intent taxonomy and corresponding descriptions based on the Search Arena dataset (Miroyan et al. 2025).

A.9   Distribution of Climate Q&A queries over 15 categories

                     Topics                                         Number of questions Share of total
                     Climate Change & Greenhouse gas emissions                       1477          43.1%
                     Earth system                                                     416          12.1%
                     Energy                                                           358          10.5%
                     Citizens & behavior                                              173           5.1%
                     Economics                                                        171           5.0%
                     IPCC-related questions                                           170           5.0%
                     Companies & industries                                           153           4.5%
                     Food & Agriculture                                               104           3.0%
                     Feelings                                                         101           2.9%
                     Biodiversity                                                     101           2.9%
                     Politics & Policies                                               70           2.0%
                     Circular economy                                                  67           2.0%
                     Technologies                                                      35           1.0%
                     Social issues                                                     29           0.8%
                     Total                                                           3425           100%

             Table 10: Distribution of Climate Q&A queries (De La Calzada et al. 2024) over 15 topic categories.
A.10   Distribution of sampled categories from Climate Q&A dataset

                                     Topic                  Count % share of total
                                     Earth system              67          25.8%
                                     Citizens & behavior       32          12.3%
                                     Economics                 31          11.9%
                                     IPCC-related questions    19           7.3%
                                     Biodiversity              16           6.2%
                                     Food & Agriculture        16           6.2%
                                     Companies & industries    15           5.8%
                                     Circular economy          14           5.4%
                                     Feelings                  13           5.0%
                                     Politics & Policies       12           4.6%
                                     Technologies              10           3.8%
                                     Social issues              8           3.1%
                                     Companies & Industries     7           2.7%
                                     Total                    260         100.0%

Table 11: Distribution of sampled categories from the Climate Q&A dataset (De La Calzada et al. 2024) including the relative
percentage for each category out of the total sample size.
A.11    Distribution of AI-generated content by domain




                      Figure 2: Distribution of AI-generated sources by number of source web domains.

A.12    Prevalence and concentration of cited sources




    (a) Proportion of Source Web Domains by Citation Count       (b) Distribution of Citation Frequencies Across Source Web Do-
                                                                 mains

Figure 3: Concentration and distribution of citations across source web domains. Figure 1(a) illustrates the high proportion
of source web domains with very few citations and the substantial drop in number of source web domains having 4 or more
citations. Figure (b) illustrates the overall distribution of source web domains and citations in our dataset showing a large
number of domains with one or two citations, representing the long-tail in our distribution.
A.13    Prompt for generating AI-generated text

                         Write <category> starting with the following four words:
                         <the first four words of the leading sentence>.

Figure 4: Prompt template used for to generate text across the categories of “research abstract”, “wiki page”, “reddit post”,
“news article”. The four words used in the prompt were retrieved from the leading sentence of the human text in our sample
from the RAID benchmark.


A.14    Distribution of Pangram scores




                                  Figure 5: Distribution of Pangram prediction categories.
                          References                                    Emi, B. 2025. All About False Positives in AI Detectors. Accessed:
Adam, G. A.; Cui, A.; Thomas, E.; Napier, E.; Shmatko, N.;              2026-03-05.
Schnell, J.; Tian, J. J.; Dronavalli, A.; Tian, E.; and Lee, D.         Emi, B.; and Spero, M. 2024. Technical report on the pangram
2026. GPTZero: Robust Detection of LLM-Generated Texts. arXiv           ai-generated text classifier. arXiv preprint arXiv:2402.14873.
preprint arXiv:2602.13042.                                              Gallegos, I. O.; Rossi, R. A.; Barrow, J.; Tanjim, M. M.; Kim, S.;
Allaham, M.; Kieslich, K.; and Diakopoulos, N. 2025. Informing          Dernoncourt, F.; Yu, T.; Zhang, R.; and Ahmed, N. K. 2024. Bias
AI Risk Assessment with News Media: Analyzing National and              and fairness in large language models: A survey. Computational
Political Variation in the Coverage of AI Risks. In Proceedings of      linguistics, 50(3): 1097–1179.
the AAAI/ACM Conference on AI, Ethics, and Society, volume 8,
90–103.                                                                 Ghosh, S.; Rath, M.; and Shah, C. 2018. Searching as learning: Ex-
                                                                        ploring search behavior and learning outcomes in learning-related
Allsopp, G. 2025. Do Self-Promotional “Best” Lists Boost Chat-          tasks. In Proceedings of the 2018 conference on human informa-
GPT Visibility? Study of 26,283 Source URLs. Ahrefs Blog. Ac-           tion interaction & retrieval, 22–31.
cessed: 2026-03-06.
                                                                        Gini, C. 1936. On the Measure of Concentration with Special Ref-
Alyukov, M.; Makhortykh, M.; Voronovici, A.; and Sydorova, M.
                                                                        erence to Income and Statistics. Colorado College Publication,
2025. LLMs grooming or data voids? LLM-powered chatbot refer-
                                                                        (208): 73–79.
ences to Kremlin disinformation reflect information gaps, not ma-
nipulation. Harvard Kennedy School Misinformation Review.               Gregory, A. 2026. Google AI Overviews put people at risk of harm
An, B.; Zhang, S.; and Dredze, M. 2025. Rag llms are not safer:         with misleading health advice.
A safety analysis of retrieval-augmented generation for large lan-      Grootendorst, M. 2022. BERTopic: Neural topic modeling with a
guage models. In Proceedings of the 2025 Conference of the Na-          class-based TF-IDF procedure. arXiv preprint arXiv:2203.05794.
tions of the Americas Chapter of the Association for Computational      Internet Archive. n.d. Wayback Machine. Accessed: 2026-04-30.
Linguistics: Human Language Technologies (Volume 1: Long Pa-
pers), 5444–5474.                                                       Jacob, C.; Kerrigan, P.; and Bastos, M. 2025. The chat-chamber
                                                                        effect: Trusting the AI hallucination. Big Data & Society, 12(1):
Bansal, V. 2025. What Does It Take To Moderate AI Overviews?
                                                                        20539517241306345.
TechPolicy.Press. Accessed: YYYY-MM-DD.
Bender, E. M.; Gebru, T.; McMillan-Major, A.; and Shmitchell, S.        Jaźwińska, K.; and Chandrasekar, A. 2025. AI Search Has a Cita-
2021. On the dangers of stochastic parrots: Can language mod-           tion Problem: We Compared Eight AI Search Engines. They’re All
els be too big? In Proceedings of the 2021 ACM conference on            Bad at Citing News. https://www.cjr.org/tow center/we-compared-
fairness, accountability, and transparency, 610–623.                    eight-ai-search-engines-theyre-all-bad-at-citing-news.php. Ac-
                                                                        cessed: 2025-01-13.
Bommasani, R.; Hudson, D. A.; Adeli, E.; Altman, R.; Arora, S.;
von Arx, S.; Bernstein, M. S.; Bohg, J.; Bosselut, A.; Brunskill, E.;   Ji, Z.; Lee, N.; Frieske, R.; Yu, T.; Su, D.; Xu, Y.; Ishii, E.; Bang,
et al. 2021. On the opportunities and risks of foundation models.       Y. J.; Madotto, A.; and Fung, P. 2023. Survey of hallucination in
arXiv preprint arXiv:2108.07258.                                        natural language generation. ACM computing surveys, 55(12): 1–
Brantner, C.; Karlsson, M.; and Kuai, J. 2025. Sourcing behavior        38.
and the role of news media in AI-powered search engines in the          Jia, X.; Pang, Y.; and Liu, L. S. 2021. Online health information
digital media ecosystem: Comparing political news retrieval across      seeking behavior: a systematic review. In Healthcare, volume 9,
five languages. Telecommunications Policy, 102952.                      1740. MDPI.
Calzada, N. D. L.; Costa, T. A. D.; Blangero, A.; and Chesneau, N.      Kelly, D.; Chen, Y.; Cornwell, S. E.; Delellis, N. S.; Mayhew, A.;
2024. ClimateQ&A: Bridging the gap between climate scientists           Onaolapo, S.; and Rubin, V. L. 2023. Bing chat: The future of
and the general public. arXiv:2403.14709.                               search engines? Proceedings of the Association for Information
Chapekis, A.; and Lieb, A. 2025. Google users are less likely to        Science and Technology, 60(1): 1007–1009.
click on links when an AI summary appears in the results.               Kieslich, K.; Diakopoulos, N.; and Helberger, N. ???? Anticipating
Dai, S.; Cao, Z.; Wang, W.; Pang, L.; Xu, J.; Ng, S. K.; and Chua,      Impacts: Using Large-Scale Scenario Writing to Explore Diverse
T.-S. 2025. Media source matters more than content: Unveiling po-       Implications of Generative AI in the News Environment.
litical bias in llm-generated citations. In Proceedings of the 2025     Kieslich, K.; Helberger, N.; and Diakopoulos, N. 2024. My Future
Conference on Empirical Methods in Natural Language Process-            with My Chatbot: A Scenario-Driven, User-Centric Approach to
ing, 17267–17287.                                                       Anticipating AI Impacts. Conference on Fairness, Accountability,
De La Calzada, N.; Da Costa, T. A.; Blangero, A.; and Chesneau,         and Transparency, 2071–2085.
N. 2024. ClimateQ&A: Bridging the gap between climate scien-
tists and the general public. arXiv preprint arXiv:2403.14709.          Kuai, J.; Brantner, C.; Karlsson, M.; Van Couvering, E.; and Ro-
                                                                        mano, S. 2025. AI chatbot accountability in the age of algorith-
Deng, B.; Wang, W.; Zhu, F.; Wang, Q.; and Feng, F. 2025. Cram:         mic gatekeeping: Comparing generative search engine political in-
Credibility-aware attention modification in llms for combating mis-     formation retrieval across five languages. new media & society,
information in rag. In Proceedings of the AAAI Conference on Ar-        14614448251321162.
tificial Intelligence, volume 39, 23760–23768.
                                                                        Li, A.; and Sinnamon, L. 2024. Generative ai search engines as
Dugan, L.; Hwang, A.; Trhlı́k, F.; Zhu, A.; Ludan, J. M.; Xu, H.; Ip-
                                                                        arbiters of public knowledge: An audit of bias and authority. Pro-
polito, D.; and Callison-Burch, C. 2024. Raid: A shared benchmark
                                                                        ceedings of the Association for Information Science and Technol-
for robust evaluation of machine-generated text detectors. In Pro-
                                                                        ogy, 61(1): 205–217.
ceedings of the 62nd Annual Meeting of the Association for Com-
putational Linguistics (Volume 1: Long Papers), 12463–12492.            Lindemann, N. F. 2025. Chatbots, search engines, and the sealing
Dutton, W. H.; Reisdorf, B.; Dubois, E.; and Blank, G. 2017.            of knowledges. AI & SOCIETY, 40(6): 5063–5076.
Search and politics: The uses and impacts of search in Britain,         Liu, N. F.; Zhang, T.; and Liang, P. 2023. Evaluating verifiability
France, Germany, Italy, Poland, Spain, and the United States.           in generative search engines. arXiv preprint arXiv:2304.09848.
Luo, Z.; Peng, Z.; Liu, Y.; Sun, Z.; Li, M.; Zheng, J.; and He,         Knor, E. 2025. ChatGPT as a news recommender system: Mea-
X. 2025. Unsafe LLM-Based Search: Quantitative Analysis and             suring source types and diversity across different interfaces.
Mitigation of Safety Risks in AI Web Search. arXiv preprint             Shaib, C.; Chakrabarty, T.; Garcia-Olano, D.; and Wallace,
arXiv:2502.04951.                                                       B. C. 2025. Measuring AI” Slop” in Text. arXiv preprint
Marchionini, G. 2006. Exploratory search: from finding to under-        arXiv:2509.19163.
standing. Communications of the ACM, 49(4): 41–46.                      Solaiman, I.; Talat, Z.; Agnew, W.; Ahmad, L.; Baker, D.; Blodgett,
Memon, S. A.; and West, J. D. 2024. Search engines post-                S. L.; Chen, C.; Daumé III, H.; Dodge, J.; Duan, I.; et al. 2023.
ChatGPT: How generative artificial intelligence could make search       Evaluating the social impact of generative ai systems in systems
less reliable. arXiv preprint arXiv:2402.11707.                         and society. arXiv preprint arXiv:2306.05949.
Menchen-Trevino, E.; Struett, T.; Weeks, B. E.; and Wojcieszak,         Soudani, H. 2025. Enhancing Knowledge Injection in Large Lan-
M. 2023. Searching for politics: Using real-world web search be-        guage Models for Efficient and Trustworthy Responses. In Pro-
havior and surveys to see political information searching in context.   ceedings of the 48th International ACM SIGIR Conference on Re-
The Information Society, 39(2): 98–111.                                 search and Development in Information Retrieval, 4211–4211.
Metaxa, D.; Park, J. S.; Robertson, R. E.; Karahalios, K.; Wilson,      Steinacker-Olsztyn, N.; Gosain, D.; and Dao, H. 2025. Is Misin-
C.; Hancock, J.; Sandvig, C.; et al. 2021. Auditing algorithms: Un-     formation More Open? A Study of robots. txt Gatekeeping on the
derstanding algorithmic systems from the outside in. Foundations        Web. arXiv preprint arXiv:2510.10315.
and Trends® in Human–Computer Interaction, 14(4): 272–344.
                                                                        Strauss, I.; Yang, J.; O’Reilly, T.; Rosenblat, S.; and Moure, I.
Minici, M.; Consonni, C.; Cinus, F.; and Manco, G. 2025. Audit-         2025. The Attribution Crisis in LLM Search Results. arXiv
ing LLM Editorial Bias in News Media Exposure. arXiv preprint           preprint arXiv:2508.00838.
arXiv:2510.27489.
                                                                        Swire-Thompson, B.; and Lazer, D. 2020. Public health and online
Miroyan, M.; Wu, T.-H.; King, L.; Li, T.; Pan, J.; Hu, X.; Chi-         misinformation: challenges and recommendations. Annual review
ang, W.-L.; Angelopoulos, A. N.; Darrell, T.; Norouzi, N.; et al.       of public health, 41: 433–451.
2025. Search Arena: Analyzing Search-Augmented LLMs. arXiv
preprint arXiv:2506.05334.                                              Tang, K.; Angelopoulos, A. N.; and Chiang, W.-L. 2025. Arena
                                                                        Explorer: A Topic Modeling Pipeline for LLM Evals & Analytics.
Moraes, F.; Putra, S. R.; and Hauff, C. 2018. Contrasting search as
                                                                        https://news.lmarena.ai/arena-explorer/?ref=news.lmarena.ai. Ac-
a learning activity with instructor-designed learning. In Proceed-
                                                                        cessed: 2026-01-14.
ings of the 27th ACM international conference on information and
knowledge management, 167–176.                                          Tripodi, F. B.; and Moeller, P. D. 2025. Data Voids and Echo Cham-
NewsGuard Technologies, Inc. 2025. Tracking AI-enabled Misin-           bers: The Transformative Journey of Search and Its Consequences.
formation: 2,089 Undisclosed AI-Generated News Websites (and            NASIG Proceedings, 39.
Counting), Plus the Top False Narratives Generated by Artifi-           Union, E. B. 2025. News Integrity in AI Assistants: An Interna-
cial Intelligence Tools. https://www.newsguardtech.com/special-         tional PSM Study. Technical report, European Broadcasting Union.
reports/ai-tracking-center/. Accessed: 2026-01-13.                      Accessed: 2025-10.
Newspaper Contributors. 2018. Newspaper3k: Article scraping &           Urman, A.; and Makhortykh, M. 2025. The silence of the LLMs:
curation — Documentation. Read the Docs. Online; accessed May           Cross-lingual analysis of guardrail-related political bias and false
25, 2026.                                                               information prevalence in ChatGPT, Google Bard (Gemini), and
Nishal, S.; and Diakopoulos, N. 2024. Envisioning the Applica-          Bing Chat. Telematics and Informatics, 96: 102211.
tions and Implications of Generative AI for News Media. arXiv.          Van Der Ven, H.; Corry, D.; Elnur, R.; Provost, V. J.; Syukron, M.;
Paviour, B. 2025. AI-generated news sites spout viral slop from         and Tappauf, N. 2025. Does artificial intelligence bias percep-
forgotten URLs. Accessed January 14, 2026.                              tions of environmental challenges? Environmental Research Let-
                                                                        ters, 20(1): 014009.
Playwright. 2026. Playwright: Fast and reliable end-to-end testing
for modern web apps. Accessed: 14 Jan 2026.                             Venkit, P. N.; Laban, P.; Zhou, Y.; Mao, Y.; and Wu, C.-S. 2024.
                                                                        Search engines in an ai era: The false promise of factual and veri-
Rieger, A.; Draws, T.; Theune, M.; and Tintarev, N. 2024. Nudges
                                                                        fiable source-cited responses. arXiv preprint arXiv:2410.22349.
to mitigate confirmation bias during web search on debated topics:
Support vs. manipulation. ACM Transactions on the Web, 18(2):           Vranić, A.; Reis, J.; Damião, Í.; Almeida, P.; and Gonçalves-Sá,
1–27.                                                                   J. 2025. Global Claims: A Multilingual Dataset of Fact-Checked
Roy, J.-H. 2025. I used AI chatbots as a source of news for a month,    Claims with Veracity, Topic, and Salience Annotations. In Pro-
and they were unreliable and erroneous. The Conversation. Ac-           ceedings of the 2nd International Workshop on Diffusion of Harm-
cessed 13 Jan 2026.                                                     ful Content on Online Web, 85–94.
Rozado, D. 2022. The political orientation of the ChatGPT AI            Wittenberg, C.; Epstein, Z.; Berinsky, A. J.; and Rand, D. G. 2024.
system. Accessed: 2026-01-13.                                           Labeling AI-generated content: promises, perils, and future direc-
                                                                        tions.
Russell, J.; Karpinska, M.; Akinode, D.; Thai, K.; Emi, B.; Spero,
M.; and Iyyer, M. 2025a. AI use in American newspapers is               Yang, K.-C. 2025. News source citing patterns in ai search systems.
widespread, uneven, and rarely disclosed. arXiv.                        arXiv preprint arXiv:2507.05301.
Russell, J.; Karpinska, M.; Akinode, D.; Thai, K.; Emi, B.;             Zhang, P.; Ye, Q.; Peng, Z.; Garimella, K.; and Tyson, G. 2025.
Spero, M.; and Iyyer, M. 2025b. AI use in American newspa-              Source Coverage and Citation Bias in LLM-based vs. Traditional
pers is widespread, uneven, and rarely disclosed. arXiv preprint        Search Engines. arXiv.
arXiv:2510.18774.                                                       Zhang, X.; Mao, R.; and Cambria, E. 2025. A Systematic
Schatto-Eckrodt, T.; Liebig, L.; Reiss, M.; Geislinger, R.; Schaetz,    Analysis of Biases in Large Language Models. arXiv preprint
N.; Merten, L.; Schröder, J.; Königslöw, K.; Laugwitz, L.; and       arXiv:2512.15792.
Zhu, W. B.; Chen, T.; Lin, C. Y.; Law, J.; Jizzini, M.; Nieva, J. J.;
Liu, R.; and Jia, R. 2025. Cancer-Myth: Evaluating AI Chatbot
on Patient Questions with False Presuppositions. arXiv preprint
arXiv:2504.11373.
Zihlmann, O.; and Euchner, C. 2025. Eine beängstigende Entwick-
lung: Wie KI-Artikel das Internet mit Fake News überfluten. Tages-
Anzeiger. Online; paywall.
