                                         AI use in American newspapers is widespread, uneven, and rarely disclosed
                                              Jenna Russell            Marzena Karpinska              Destiny Akinode               James Zhou
                                                    Katherine Thai                 Bradley Emi       Max Spero             Mohit Iyyer
                                             University of Maryland, College Park        Simon Fraser University                        UMass Amherst
                                                                                   Pangram Labs
                                                                    {jennarus,miyyer}@umd.edu, karpinsk@sfu.ca
                                                                              ainewsaudit.github.io

                                                               Abstract                             D ISCLAIMER
                                                                                                    All findings in this paper rely on the outputs of
arXiv:2510.18774v4 [cs.CL] 26 Apr 2026




                                             AI is rapidly transforming journalism, but the
                                                                                                    an automated AI detector and should be inter-
                                             extent of its use in published newspaper ar-
                                             ticles remains unclear. We address this gap
                                                                                                    preted accordingly. We do not assert definitive
                                             by auditing a large-scale dataset of 186K ar-          authorship attributions for any article. We do
                                             ticles from online editions of 1.5K American           not draw conclusions about the intent, conduct,
                                             newspapers published in the summer of 2025.            or practices of individual journalists, outlets, or
                                             Using Pangram, a state-of-the-art AI detector,         companies. Results should not be interpreted as
                                             we discover that approximately 9% of newly-            rankings, qualitative judgments, or accusations
                                             published articles are detected as either par-         of wrongdoing. See §6 for further discussion.
                                             tially or fully AI-generated. This AI use is un-
                                             evenly distributed, appearing more frequently
                                             in smaller, local outlets, in specific topics such
                                             as weather and technology, and within certain
                                             ownership groups. We also analyze 45K opin-          published U.S. newspaper articles are detected as
                                             ion pieces from Washington Post, New York            either partially or fully AI-generated.
                                             Times, and Wall Street Journal, finding that
                                             they are 6.4 times more likely to contain AI-        Why does this matter? Our audit is largely mo-
                                             generated content than news articles from the        tivated by concerns of transparency and factual-
                                             same publications, with many AI-flagged op-          ity. We do not claim that all AI use is inherently
                                             eds authored by prominent public figures. De-
                                                                                                  harmful; in fact, limited applications like gram-
                                             spite this prevalence, we find that AI use is
                                             rarely disclosed: a manual audit of 200 AI-
                                                                                                  mar / style checking and template-driven article
                                             flagged articles, 96.5% of authors and 94.0% of      creation (e.g., weather reports) can improve article
                                             publishers did not disclose AI use. A factuality     quality and accessibility (Medill Local News Ini-
                                             analysis shows articles flagged as AI-generated      tiative, 2024; Radcliffe, 2025). However, LLMs
                                             are 8.2 times more likely to contain halluci-        often hallucinate (Maynez et al., 2020a; Ji et al.,
                                             nated claims than human-labeled news. Over-          2023a; Su et al., 2024) and inherit social biases
                                             all, our audit highlights the immediate need for     from their training data (Gallegos et al., 2024; Hu
                                             greater transparency and updated editorial stan-
                                                                                                  et al., 2025); thus, public opinion is highly sensitive
                                             dards regarding the use of AI in journalism to
                                             maintain public trust.                               to undisclosed AI use.1 We manually analyze 200
                                                                                                  articles flagged for AI use by Pangram and find that
                                         1   Introduction                                         only 7 of them disclose AI use, while only 12 of
                                                                                                  the newspapers have any public policies on AI use,
                                         How much AI-generated content is being published         leaving readers largely unable to determine the role
                                         in newspapers across America? To answer this             AI plays in article authorship.
                                         question, we conduct a large-scale audit of recently-
                                                                                                     1
                                         published articles using Pangram (Emi and Spero,              Recent studies from Pew Research show that (1) 49% of
                                                                                                  Americans who get news directly from AI assistants report
                                         2024), a high-precision AI detector that has previ-      encountering inaccurate information (Lipka and Eddy, 2025);
                                         ously been used to audit consumer reviews (Cava-         (2) 56% of Americans would feel less confident about a news
                                         zos and Sterling, 2024), research papers (Evanko         article if they knew an AI wrote it (Yam and Kennedy, 2025);
                                                                                                  and (3) 76% believe it is extremely important for them to know
                                         and Natale, 2025), and Medium articles (Knibbs,          if the text they are reading is AI-generated (Kennedy et al.,
                                         2024). Our analysis reveals that ∼9% of newly-           2025).
Audit design: We collect and audit two large-                        I N THIS PAPER ...
scale datasets of American newspapers:                               AI USE : We use the term AI use throughout
 \ recent_news contains 186K articles pub-                           this paper to denote articles labeled by Pangram
   lished online by 1.5K local and national news-                    as either M IXED or AI-G ENERATED .
   papers from June to September 2025.                                EXAMPLES : Each article discussed in this
                                                                     paper is associated with a      icon that links to
 × opinions contains 45K opinion articles pub-
                                                                     an AI prediction dashboard and a        icon that
   lished by the New York Times, Washington
                                                                     links to the original news article.
   Post, and Wall Street Journal between August
   2022 and September 2025.
   We feed each article in both datasets
                                                                 leaving readers in the dark about the true sources
through Pangram’s API to obtain both an
                                                                 of information. At the same time, we find that 41%
AI likelihood (from 0-100%) and a categor-
                                                                 of articles labeled as AI-generated contain hallu-
ical label in { H UMAN - WRITTEN , M IXED ,
                                                                 cinations, showing that AI-generated information
 AI-G ENERATED }. Pangram has a reported
                                                                 is often inaccurate and not corrected by human
false positive rate (FPR) of ∼0.001% on news
                                                                 revision.
text (Emi, 2025) and Jabarian and Imas (2025)
verified Pangram’s high accuracy, finding an FPR                 AI use is concentrated in opinion articles at top
of 0.08%, substantially below the rates of AI                    newspapers. Opinion articles published at the
use we observe. Importantly, for articles labeled                NYT, WaPo, and WSJ are 6.4 times more likely to
 M IXED , we cannot infer the role that AI played                be flagged for AI use than contemporaneous news
in the authorship process: we only know that                     articles from the same three newspapers (4.5% vs.
some parts of a M IXED article are classified as                 0.7%). Many opinion articles flagged for AI use are
human-written while other parts are classified as                written by prominent guest contributors, including
AI-generated.                                                    Nobel prize winners, US Senators and Governors,
                                                                 Pulitzer Prize-winning journalists, and CEOs (see
AI use in published articles is increasingly
                                                                 Table 12 for examples). Analysis of both opinions
common. In our recent_news dataset, 9.1%
                                                                 and ai_reporters show AI usage rising over time,
of articles are labeled by Pangram as either
                                                                 with reporters in the latter dataset increasing their
 AI-G ENERATED or M IXED , and disclosure of
                                                                 AI use from ∼ 0% prior to 2023 to over 40% in
AI use is rare in our manual sample. Digging
                                                                 2025 on average (Figure 8).
deeper, we observe that AI usage is unevenly dis-
tributed: it is much higher in smaller local outlets             Contributions: We release our datasets,3 analy-
than nationally-circulated papers; it occurs more                sis code, and an interactive dashboard to facilitate
frequently in topics such as weather, science / tech-            further exploration of AI use in newspapers. 4 We
nology, and health (Figure 13); it varies across                 also commit to periodically updating our dashboard
ownership group, with Boone Newsmedia and Ad-                    with new articles and annotations (i.e., disclosure
vance Publications among the heaviest AI adopters                audits) to measure future changes to AI adoption.
(Figure 14); and it is higher in languages other than
English (Figure 2).2                                             2        Collecting newspaper articles

Undisclosed AI use compounds risks of factual                    We collect two datasets of published newspaper
hallucinations. While AI use is becoming more                    articles (Table 1): recent_news and opinions. 5
common, we find it is rarely disclosed and often                 The datasets vary significantly in terms of cover-
factually unreliable. When investigating whether                 age, diversity, and publication date, which allows
AI use is disclosed, only 4% of articles were trans-             us to analyze differences in AI use across local vs.
parent about writing articles with the help of AI,               national papers, staff reporters vs. guest contrib-
    2
                                                                 utors, and articles written pre- vs. post-ChatGPT.
      Example articles linked within this paper are solely for
                                                                      3
illustrative purposes. Their inclusion does not attribute any          We release links to the articles involved in our study (not
intent or misconduct on part of any reporters: Pangram has       full texts).
a small but non-zero FPR, and we also emphasize that it is           4
                                                                       ainewsaudit.github.io
infeasible to tease apart exactly how AI is used in M IXED           5
                                                                       We collect a third dataset, ai_reporters, which is de-
authorship cases.                                                tailed and analyzed in §D.3.
                           \ recent_news         × opinions          article into one of 19 topics, and we use an existing
 Temporal coverage                                                   database to match about half of the newspapers in
 Years                                  2025       2022–2025         our recent_news with print circulation statistics.
 Dataset statistics                                                  Detecting AI use: Emi and Spero (2024) intro-
 # Articles                          186,507            44,803
                                                                     duce Pangram; a robust AI-generated text detec-
 # Authors                            34,608             9,863
 # Newspapers                          1,528                 3       tion tool. On news articles, it achieves a false
 Avg. tokens                           787.4            1078.4       positive rate of 0.001% (Emi, 2025), consistent
 AI use statistics                                                   with other studies that have also reported low FPR
 H UMAN - WRITTEN                    90.85%            99.04%        (Russell et al., 2025; Jabarian and Imas, 2025;
 M IXED                               3.98%             0.85%        Dugan et al., 2025). Using Pangram’s inference
 AI-G ENERATED                        5.24%             0.11%        API9 , we collect (1) the likelihood (from 0-100%)
                                                                     that a text is AI-generated and (2) a text label
Table 1: Dataset and AI use statistics for recent_news               that is one of H UMAN - WRITTEN , M IXED , or
and opinions. The token counts are reported as per
                                                                      AI-G ENERATED .10 Pangram predicts M IXED
tiktoken tokenizer (o200k_base).
                                                                     when there is a high confidence of both AI and
                                                                     human writing present in the document; specifi-
This section outlines our dataset creation process,                  cally, where some segments are predicted as AI,
in which the full text and metadata for each article                 and some segments are predicted as human. While
is paired with a label indicating whether the article                prior studies have validated Pangram’s high accu-
was generated via AI.                                                racy, we also experiment with another commercial
                                                                     detector, GPTZero (Tian and Cui, 2023), and ob-
2.1    recent_news                                                   serve a high cross-detector agreement of 88.2%
To examine AI use in present-day newspaper jour-                     (Cohen’s κ = 0.764).11
nalism, we form the recent_news dataset by col-
                                                                     Topic classification: To analyze AI use across
lecting 186,507 articles6 published online by 1,528
                                                                     article topics, we further augment our datasets
unique newspapers between June 15th, 2025 and
                                                                     with topic labels for each article using the Inter-
September 15th, 2025, accessed via url RSS feeds.7
                                                                     national Press Telecommunications Council Media
2.2    opinions                                                      Topics taxonomy, which comprises 17 top-level top-
While recent_news contains a broad sample                            ics (IPTC, 2025). We prompt Q WEN 3-8B (Qwen
across many different American newspapers, top-                      Team, 2025) in a zero-shot setting to assign a topic
ics, and journalists, another object of our study                    (full prompt and details in §A).12 To assess the re-
is AI use in opinion articles written by prominent                   liability of these topic labels, two of the authors
people in highly-reputable newspapers. To facili-                    independently reclassified a random subset of 100
tate this, we also collect a dataset of opinions ar-                 model outputs,13 with model–human agreement
ticles published by The New York Times, Wall                         averaging 77%, indicating moderately strong align-
Street Journal, and Washington Post between Au-                      ment between the classifier and human judgments.
gust 2022 and September 2025. The full text and                         9
                                                                           API documentation available here.
                                                                        10
metadata of these articles were accessed via Pro-                          We simplify the fine-grained labels produced by the Pan-
Quest Recent Newspapers. In total, we collected                      gram API in the following way: H UMAN - WRITTEN = {Hu-
                                                                     man, Unlikely AI}; M IXED = {Mixed, Possibly AI, Likely
44,803 articles during this time period: 16,964 from
                                                                     AI}; AI-G ENERATED = {Highly Likely AI, AI}. See §B for
WSJ, 15,977 from WP, and 11,862 from NYT.                            details on how labels are combined.
                                                                        11
                                                                           This experiment was conducted on a balanced binary held-
2.3    Labeling the datasets                                         out set of 1K news articles, 500 of which are marked by Pan-
                                                                     gram as H UMAN - WRITTEN and 500 as AI-G ENERATED .
For each of the 251,442 total articles across all                    Agreement on the human subset is 98.4% while agreement
datasets, we use Pangram (v2.0) to obtain an AI                      on the AI subset is 78.4%, and discrepancies on the latter
detection label and score.8 We also classify each                    label are likely due to each detector’s differing treatment of
                                                                      M IXED text (see §B for more).
   6                                                                    12
      Each instance in our datasets includes the full article text         In addition to the 17 IPTC topics, we include two auxiliary
along with title, author, publication date, newspaper, and URL.      categories—Other and Obituary—for items that fall outside
    7
      See §A for additional collection details.                      the taxonomy or are obituaries.
    8                                                                   13
      All Pangram links display v3.2 predictions, and had con-             Inter-annotator agreement between the two human raters
sistent labels with Pangram v2.0.                                    was 87% (Cohen’s κ = 0.85).
Figure 1: Heatmap of AI use by publication owner and article topic in recent_news. Some owners disclose AI
use for specific content, such as Advance Publications for weather reports, but the biggest adopters, such as Boone
Newsmedia, use AI broadly across many topics. Note that only 87% of recent_news has ownership information,
and only topics that have at least 5 articles per owner are visualized in the heatmap.


Linking newspapers to circulation and own-                       between M IXED and AI-G ENERATED articles,
ership information: We link newspapers to                        factual details, and disclosure.
print circulation data from the U.S. News Deserts
Database (UNC Center for Innovation & Sustain-                   3.1    How often is AI used in American
ability in Local Media, 2020) and ownership in-                         newspapers?
formation from the Local News Initiative (Medill                 We find that 9.1% of the 186K articles in
Local News Initiative, 2024). Because circulation                recent_news are labeled by Pangram as ei-
figures are based on historical AAM audits and                   ther AI-G ENERATED (5.2%) or M IXED (3.9%),
self-reports (primarily from 2019), we treat them                while the remaining 90.9% of articles are classified
as a proxy for print scale rather than current to-               as H UMAN - WRITTEN . The rest of this section
tal audience.14 40.3% of articles come from small                goes beyond these aggregate numbers to examine
publications with daily circulation between 1-7K                 AI use as a function of different fine-grained as-
and another 36.3% comes from publications with a                 pects like topic and ownership.
circulation of 10-50K. Only 20.1% of articles come
from very large nationally-circulated publications               AI use is higher in local newspapers. Local
with average circulations over 50K.15                            outlets, often operating in "news deserts," places
                                                                 with little to no access to credible reporting due
3        Analyzing AI use in newspapers                          to limited resources (Metzger, 2024), rely on AI
                                                                 more than national newspapers. Only 1.7% of arti-
How much of recent news contains AI-generated                    cles at papers with circulation >100K are labeled
content, and when and how do journalists use AI?                 as AI-G ENERATED or M IXED , versus 9.3% at
Using our recent_news dataset, we investigate                    papers below 100K (see Figure 15),16 suggesting
where AI-generated content appears across circu-                 that large national newspapers enforce stricter edi-
lation, ownership, language, and article topic. We               torial constraints on automation than local papers.
also explore how it is used, looking at differences
                                                                   16
                                                                      At the article level, this difference is highly significant
    14
     See §A for details and limitations. 54.6% of the articles   (χ2 (1) = 1175.6, p < 10−250 ). At the newspaper level,
and 49.7% of newspapers in recent_news were matched to           smaller outlets averaged 8.5% AI content vs. 5.0% among
publications in the News Desert Database.                        very large outlets (Welch’s t(≈ 23) = 2.24, p = 0.032,
  15
     Circulation distribution is depicted in Figure 6.           d = 0.22).
AI use also varies geographically, peaking in the                  English                   Other Languages
mid-Atlantic and southern US, Maryland (16.5%),
Tennessee (13.6%), Alabama (13.9%), and lowest                          8.0%
                                                                                                                31.0%
in the Northeast, including New Hampshire (2.9%)
and Massachusetts (3.4%) (Figure 11).
                                                                                                 69.0%
AI use varies with topic. Prior work has shown                     92.0%
that factual, data-heavy content (e.g., reports about
weather, finance, or sports) is particularly amenable         Total: 177,478 articles             Total: 9,034 articles
to automation (Medill Local News Initiative, 2024).                      Human-written       AI-generated or Mixed
Consistent with this, weather articles in our dataset
exhibit the highest average AI likelihood (27.7%),         Figure 2: AI use in recent_news is more frequent in
as shown in Figure 13. However, we also observe            languages other than English. The most prominent such
                                                           languages include Spanish, Portuguese, Vietnamese,
high AI use in other topics, such as science and
                                                           French, and Polish.
technology (16.1%) and health (11.7%), while con-
tent on more sensitive issues such as conflict and
war (4.3%), crime, law, and justice (5.2%), and            non-English news articles.18 As shown in Fig-
religion (5.3%) exhibit lower rates.                       ure 2, only 8.0% of English-language articles in
                                                           recent_news are classified as AI-G ENERATED
AI use varies with ownership. Many newspa-                 or M IXED ; this share rises to 31.0% for articles
pers in recent_news share ownership: for ex-               in other languages.19 Most non-English AI use
ample, Advance Publications owns widely-read               (≈ 80%) comes from U.S.-based Spanish-language
outlets like pennlive.com, cleveland.com, and              reporting (7.2K articles), 20 suggesting that local
al.com and often syndicates articles among them.           bilingual outlets rely more heavily on translation
While some ownership groups view AI use as a               and other automation. High non-English AI use is
reputational risk, others emphasize cost reduction         observed across many states (Figure 12).
and efficiency gains (Medill Local News Initiative,
2024). Boone News Media and CherryRoad Media               Exploring the role of machine translation in
both have detected AI use rates over 15%, while            AI detection To understand if the higher rate
Nash Holdings and Hearst Corporation have AI use           of detected AI use in non-English languages is
rates under 1% (Figure 14). We note the irony of           an artifact of machine translation (MT), we trans-
several prominent media groups suing AI compa-             late a sample of 300 English articles into 12 lan-
nies over training language models on their content        guages and re-evaluate them using the same detec-
(e.g., Advance Local Media v. Cohere)17 even as            tion pipeline.21 Translated articles receive lower
they churn out LLM-generated articles.                     AI-likelihood scores than their English counter-
                                                           parts, with an average decrease of 13%. Under the
AI use varies by topic across ownership groups.            binary AI use versus human, translated texts agree
Figure 14 shows how different ownership groups             with English in 83.2% of cases, and disagreements
use AI. Advance Publications, for instance, relies         are asymmetric: in our sample, translation is far
heavily on AI for weather reporting (81% AI Use).          more likely to suppress AI use predictions than
Boone Media exhibits the broadest adoption, with           to introduce them.22 The magnitude of this effect
especially high rates in science and technology            varies by language: Vietnamese translations show
(67.7%) as well as lifestyle and leisure (55.7%).
                                                             18
Other chains show narrower topical patterns, such                Pangram FPR’s range from 0.0% to 0.10% across the
                                                           languages in this study (Pangram, 2024).
as CherryRoad Media in sports (37.8%) and Lee                 19
                                                                 Machine-translated articles may be misclassified, but our
Enterprises in foreign policy coverage (15.4%).            small-scale verification suggests human-written articles are
These results show that AI integration is vastly           still correctly identified after translation.
                                                              20
                                                                 Other major languages include: Portuguese (468), Viet-
uneven across both topic and ownership groups.             namese (403), French (343), and Polish (314).
                                                              21
                                                                 We sample 100 AI-G ENERATED , 100 M IXED , and
AI use is higher in languages other than En-               100 H UMAN - WRITTEN articles. Articles are translated using
glish. AI-generated content is more prevalent in           GPT-4.1. We note that results may differ with other MT
                                                           methods or models; see §D.1 for details.
  17                                                          22
    Advance Local Media LLC v. Cohere Inc., No. 1:25-cv-         McNemar’s exact test, FDR-corrected p < 0.001 for all
01305, S.D.N.Y. filed Feb. 13, 2025.                       but one language (Japanese).
      P OLICY C ATEGORY           F REQ   E XAMPLE P UBLICATIONS / OWNERS                       I LLUSTRATIVE D ISCLOSURE T EXT
¥ AI A LLOWED                 12          Ionia Sentinel-Standard, Ams-              “If AI-assisted content is approved for publication, journalists
                                          terdam News, Penn Live                     must disclose the use of AI and its limitations to their audi-
                                                                                     ence. AI-generated content must be verified for accuracy and
                                                                                     factuality before being used in reporting.”
; AI P ROHIBITED              2           New York Post, Michigan Daily              “The use of generative artificial intelligence for content pro-
                                                                                     duction (including written, visual and auditory content) is
                                                                                     unacceptable in all circumstances. Any staffer found to have
                                                                                     used generative AI to produce content for The Daily can be
                                                                                     fired by their section editor or the Editor in Chief.”
® N O P UBLIC P OLICY         186         Daily Register, Hudson Reporter,           No disclosure found on website.
                                          LA Opinion


                          Table 2: AI disclosure policies among 200 sampled U.S. news outlets.


the largest score decrease (∆ = −0.21) and lowest                            The majority (54.8%) primarily publish mixed ar-
agreement (74.7%), while Portuguese and Spanish                              ticles, while 36.1% rely mostly on AI-generated
retain high agreement (≥88%) with minimal score                              text. These findings resonate with survey evidence
shifts (see Table 10). While these results suggest                           from Radcliffe (2025), who report that over half
that MT is unlikely to be the primary driver of the                          of journalists use AI to edit their work, while only
higher AI detection rates in non-English content,                            about a third employ it to generate text directly.
especially given the observed ∼31% AI use rate,
this analysis does not account for the influence of                          AI use is largely undisclosed. Disclosure of AI
human translation or alternative MT methods. Mul-                            use (e.g., exactly how and where AI was used
tilingual AI detection is an evolving field; factors                         in the construction of the article) is important to
like language-specific writing conventions, varied                           maintain audience trust. Readers might be okay
editorial workflows, and regional AI tool availabil-                         with small AI edits for style in articles labeled
ity likely contribute to these discrepancies.                                as M IXED but they require proper disclosure to
                                                                             make these judgments.cUnfortunately, in a sample
3.2    Characterizing AI use in American                                     of 200 AI-flagged articles from unique newspapers
       newspapers                                                            in recent_news, 96.5% of authors and 94.0% of
                                                                             publishers did not disclose AI use (Table 2).23
Our analysis establishes that (1) many published
newspaper articles today are written partially or                            Notable individual cases of AI use. We iden-
entirely by AI, and (2) AI use varies across factors                         tify several unique cases of AI-generated writing
like ownership, topic, and language. We investigate                          in recent_news, snippets of which are shown in
important questions about authorship, transparency,                          Table 3. One outlet, Argonaut, turned out to be an
and public trust, revealing that journalists often                           entirely AI-generated newspaper with AI reporter
use AI in conjunction with their own writing rather                          personas who “write” exclusively articles labeled
than as a full replacement; that prestigious outlets                         as AI-G ENERATED (e.g.,                 ). Another re-
rely more on M IXED authorship; articles with AI                             porter appears to have revisited and republished
use are more likely to contain hallucinations; and                           their older work, producing updated AI-assisted
that disclosure of AI involvement is strikingly rare.                        versions of previously H UMAN - WRITTEN stories
These findings show not only how AI is chang-                                (e.g., edited (2025):     ,     ; original (2021):    ,
ing journalistic practices, but also why it matters                              ).24
whether readers are informed about its role.                                    More concerningly, we also found AI-generated
Many articles have mixed authorship. While                                   responses in a popular advice column, Dear An-
 M IXED authorship articles include at least some                            nie, a practice that risks betraying the trust readers
human writing, it is difficult to tease apart the con-                       place in such personal guidance (e.g., Reader:        ,
                                                                             Annie:       ,    ).25
tributions of the reporter compared to AI (Thai
et al., 2025). Mixed authorship is common: of the                              23
                                                                                  95% Wilson score CIs: 193/200 (96.5%; [93.0%, 98.3%])
17,059 articles we detect as using AI, 42.7% are                             and 188/200 (94.0%; [89.8%, 96.5%]).
                                                                               24
predicted as M IXED , while 57.3% are classified as                               Earlier versions were retrieved via the Internet Archive’s
                                                                             Wayback Machine.
 AI-G ENERATED . At the author level, 1,453 out                                25
                                                                                  We were unable to scrape the Dear Annie column to
of 34,608 writers produce at least some AI content.                          quantify AI use because its publication across many different
    N EWSPAPER    P REDICTION                        A RTICLE E XCERPT                                        O BSERVATIONS

    ARGONAUT     AI-G ENERATED      “...The forms of commerce have drastically changed,    Fully AI-generated text with a very generic conclusion.
                                    with constant evolution to meet consumer needs and     No details about the author exist online, and when we
                                    market dynamics . From brick-and-mortar stores, e-     further investigated the site, no details could be found
                                    commerce, and omnichannel strategies to pop-up shops   about any of its staff.
                                    and outdoor commerce, businesses need to remain
                                    adaptable to thrive in this ever-changing commercial
                                    landscape ...”

    CALEXICO     H UMAN - WRITTEN   “...This    grant     represents    an     important   While this article is detected as human-written, it in-
    CHRONI-                         step forward in our     efforts to create healthier,   cludes an AI-generated quote that was likely provided to
    CLE                             more sustainable    learning environments for our      the reporter    . Reporters who write their own articles
                                    students. By increasing shade and greenery across      may not be aware that the people they quote in their
                                    our campuses, we’ re not only improving outdoor        articles used AI to create their response.
                                    comfort and air quality, but also setting an example
                                    of environmental responsibility for our students and
                                    community...”

    WASHINGTON   M IXED             “...Finally, focus on who and where else you can       AI use often occurs even in high circulation papers like
    POST                            seek support from. Is there even one family member     Washington Post. In this advice column, a person writes
                                    or community member you can turn to and tap in for     in feeling lonely, only to receive partially AI-generated
                                    support and allyship as you navigate these familial    advice.
                                    struggles?


Table 3: Notable cases of AI use in the recent_news dataset. Words and phrases identified as indicative of AI use
by Pangram are highlighted in red. AI use takes many forms, from completely made-up news sites to AI responses
to advice columns (e.g., Dear Annie), legitimate articles that happen to quote AI-generated text from other sources,
and highly-templated topics like weather and sports reports.


AI-generated news often contains hallucina-                              As LLMs are often more persuasive than humans
tions. Hallucinations are defined as outputs that                        (Salvi et al., 2025; Schoenegger et al., 2025), AI-
are fluent and coherent but factually incorrect or                       assisted opinion writing raises concerns of misin-
unfaithful to the source material (Maynez et al.,                        formation and ideological amplification (Weidinger
2020b; Ji et al., 2023b). The widespread halluci-                        et al., 2022; Nehring et al., 2024). To assess these
nations in news media risks the spread of inaccu-                        risks, we examine opinion articles written from
rate information and reputational damage (BBC                            2022-2025 in three of the most highly circulated
News and European Broadcasting Union, 2025).                             national newspapers (New York Times, Washing-
To understand if news detected as AI-generated                           ton Post, and Wall Street Journal). While AI use in
is as verifiable as human-written reporting, we                          opinions remains low relative to recent_news, it
manually reviewed 100 AI-G ENERATED and                                  has risen sharply following mainstream LLM adop-
100 H UMAN - WRITTEN articles, finding that AI-                          tion and is also almost completely undisclosed.
labeled articles are 8.2x more likely to contain hal-
lucinations:26 41% of AI-labeled news contained                          AI use in opinion articles published at reputable
at least one hallucinated claim, whereas only 5%                         newspapers has increased by 25x over the past
of articles predicted as human-written had halluci-                      three years. To see whether AI-generated mate-
nations.27 Typical factual errors include fabricated                     rial has risen over time, we measure the share of
quotes, incorrect statistics, and misdated events                        opinions flagged as AI between September 2022
(example hallucinations in Table 8).                                     and September 2025. AI use increases from 0.1%
                                                                         in 2022 to 3.4% in 2025, about a 25× rise, consis-
4     Opinions                                                           tent across the three outlets.28 By outlet, the AI
                                                                         use share grows from 0.1% to 3.4% at the Wall
Opinion articles play a large role in shaping public                     Street Journal, 0.2% to 4.3% at the Washington
attitudes, especially those authored by trusted fig-                     Post, and 0.0% to 2.6% at the New York Times
ures such as Nobel laureates, elected officials, and                     (Figure 3). As a pre-ChatGPT sanity check, only 5
journalists. Even a single op-ed can significantly                       of 5,029 opinion articles published before Decem-
shift beliefs (Coppock et al., 2018; Bai et al., 2025).                  ber 2022 are flagged under our AI-use definition
websites made it difficult to access archival content.                   ( AI-G ENERATED or M IXED ), implying an em-
   26
      Fisher’s exact test, p = 2.3 × 10−9 .                              pirical false-positive rate of 0.10% (95% Wilson
   27
      A BBC/EBU study found around 55% of AI-generated
                                                                           28
responses had accuracy issues (BBC News and European                        Across all opinion pieces in our sample, 0.1% are labeled
Broadcasting Union, 2025).                                               AI-G ENERATED and 0.8% M IXED ; see Figure 18.
                                                                    AI Use in Opinion Pieces: Year over Year Comparison
                                                                Environment
                                                                      Culture                               2023
                                                                     Opinion                                2024
                                                                        Labor
                                                                   Education
                                                                                                            2025
                                                                      Politics
                                                                      Human




                                                          Topic
                                                                    Lifestyle
                                                                        Crime
                                                                    Economy
                                                                        Sport
                                                                       Health
                                                                     Religion
                                                                Social Issues
                                                               Foreign Policy
                                                                  Technology
                                                                                 0   2   4       6      8
Figure 3: Monthly proportion of opinions articles                                        AI Use (%)
flagged for AI use (Sep. 2022 -Sep. 2025). AI use
                                                           Figure 4: Changes in AI use in opinions articles year
in opinion pieces has dramatically increased over time.
                                                           over year (2025 only includes January 1 - September 15).
                                                           AI likelihood increased across all topics, with especially
CI: 0.04%–0.23%).                                          large gains in opinion articles about Science & Technol-
                                                           ogy, consistent with topic trends in recent_news.
Opinions exhibit higher AI use than other sec-
tions (June–September 2025). Across the three
                                                           Topical differences in AI use between opinions
outlets, AI use is 6.4 times more likely to occur
                                                           and recent_news. Setting aside AI use, the
in opinion pieces than non-opinion news articles
                                                           majority of opinion articles in our dataset focus
published by those same outlets29 between June-
                                                           on politics and government (56.9%), far more
September 2025 (4.56% vs. 0.71%; n=3,420 opin-
                                                           than in recent_news (15.0%). In Figure 4, sev-
ions, n=10,129 all articles). By outlet, the gap is
                                                           eral categories show large increases since early
largest at The Washington Post (5.51% vs. 0.55%),
                                                           2025: crime and law (about 31x higher)„ reli-
followed by The Wall Street Journal (4.99% vs.
                                                           gion (16x), and economy and business (14x) stand
0.74%), and smaller at The New York Times (2.94%
                                                           out as the fastest-growing. Science and technol-
vs. 1.80%). Looking at how AI is used, M IXED
                                                           ogy continues to lead in absolute terms, roughly
dominates in both settings (86.5% of AI use in
                                                           9× higher (1.2%→9.0%), mirroring its position in
opinions and 86.1% of AI use in non-opinion ar-
                                                           recent_news as the topic most likely to contain AI
ticles at the same outlets). Without clear disclo-
                                                           use. Substantial gains also appear in conflict, war
sure standards, readers cannot discern whether AI
                                                           and peace (12×), human interest (10x), and politics
contributed merely to editing or to greater content
                                                           and government (9×). These patterns indicate that
generation, restricting readers’ ability to judge the
                                                           AI use in opinion writing extends well beyond sci-
appropriateness of AI in specific articles.
                                                           entific domains and into political, economic, and
Guest contributors are much more likely to use             broadly human-centered discourse.
AI in opinion pieces than full-time reporters.
We observe that the majority of the 219 unique au-         5      Related work
thors in opinions with at least one article detected       AI use in news media. Recent scholarship maps
as having AI use are infrequent contributors rather        how generative AI is impacting newsroom prac-
than full-time journalists. Categorizing authors by        tices. Recent case studies document both benefits
occupation reveals clear occupational divides: po-         and frictions caused by AI within news organiza-
litical figures, executives, and scientists exhibit the    tions (Brigham et al., 2024; Jones and Jones, 2025;
highest AI use, with many using AI for all of their        Ansari et al., 2025), while industry policies study
articles in opinions V̇eteran opinion columnists           the adoption, governance, and platform–publisher
show near-zero AI incidence (<0.5%). This pat-             dynamics (Simon, 2024; Brown and Jaźwińska,
tern intuitively makes sense, as guests generally          2025; Simon et al., 2025; Meir, 2023).
lack established editorial processes and newsroom
support (Washington Post Staff, 2022).                     Effects of disclosing AI in news. Disclosure re-
   29
                                                           liably changes how readers judge identical con-
      These non-opinion articles are extracted from
recent_news, which includes WSJ, WaPo, and NYT;            tent (Longoni et al., 2022). In recent surveys,
see Table 11 for more details.                             comfort reading AI-generated material was low
( AI-G ENERATED : 19%; M IXED : 30%) (New-                    with disclosure (e.g., summarization, more
man et al., 2025). Disclosing machine author-                 in-depth rewrites), and not permitted at all
ship reduces perceived credibility (Toff and Simon,           (e.g., full article generation). Reporters should
2025; Lee et al., 2025), yet readers rarely detect AI         record notes and/or log their AI use during the
without cues and experience (Brown et al., 2020;              writing process, as these can be useful for
Clark et al., 2021; Russell et al., 2025). Moreover,          more informative disclosure.
disclosure labels often fail to reduce persuasive im-
pact (Gallegos et al., 2025). Despite these mixed          2. Explicit AI policies for external contribu-
effects on perceived credibility, transparency in AI          tors: Since opinion pieces exhibit high rates
use is important: ethically, newsroom standards               of detected AI use at top papers, particularly
emphasize being accountable to the reader (Meir,              those written by guest contributors, we pro-
2023; Viner and Bateson, 2023) and practically,               pose that author attestations about AI use
would enhance trust between readers and news out-             are collected along with article submissions.
lets using AI (Newman et al., 2025).                          Editors may additionally want to check sub-
                                                              missions (automatically or manually) for AI
Measuring AI content in other domains. Prior                  cues (Russell et al., 2025) and publish stan-
studies audit the growing presence of LLM-                    dards on what they deem acceptable AI use in
generated text across academic and creative do-               opinion pieces.
mains. In scholarly settings, the influence of AI is
measured in peer reviews (Liang et al., 2024a; Zhou      Limitations
et al., 2025) and academic papers (Liang et al.,         Our study focuses primarily on AI use in the U.S.
2024b; Luo et al., 2025; Kobak et al., 2025). Gupta      press in English-language publications. While we
and Pruthi (2025) use AI detection to identify pat-      connect our work to prior studies about hallucina-
terns of plagiarism in generated research. Similar       tion and factual errors in language model genera-
detection efforts in creative domains examine AI-        tions, we do not perform a large-scale evaluation of
generated media on art platforms, Wikipedia, social      the factuality of AI-G ENERATED articles in our
networks, and news websites (Matatov et al., 2025;       dataset beyond studying the authenticity of quo-
Brooks et al., 2024; Sun et al., 2025; Hanley and        tations. Furthermore, although articles in other
Durumeric, 2024). Other studies trace the adop-          languages are included in our datasets, they are
tion of AI in public communication and consumer          comparatively much fewer in number; as such, we
complaints (Liang et al., 2025; Shin et al., 2025).      do not claim that this sample captures the diversity
                                                         of AI use in journalism globally.
6     Conclusion
                                                            Our machine translation experiment uses a single
Our analysis provides the first audit of AI use          MT model (GPT-4.1) and does not account for hu-
across 250k articles of U.S. newspaper articles.         man translation or other MT methods, which may
We find that AI use is both widespread and uneven:       affect AI detection differently. Additionally, while
roughly 9% of recent articles are flagged as either      Pangram reports low false positive rates across lan-
partially or completely AI-generated, with partic-       guages, detection performance may vary in ways
ularly high rates in smaller local papers, specific      not fully captured by aggregate metrics; we there-
topics, ownership groups, and languages other than       fore treat our cross-lingual findings as exploratory.
English. In highly-reputed national newspapers,             recent_news focuses on regional and local
we observe AI use in opinion pieces is rapidly in-       newspapers (although national outlets like NYT
creasing (from 0% in 2022 to 3-4% in 2025), much         and WSJ are included), which may bias results to-
more so than in other news articles published by the     wards the journalistic practices of smaller outlets.
same papers. Based on our audit, we suggest some         The inclusion or exclusion of particular newspa-
disclosure policies that newspapers could consider       pers is partially due to data accessibility constraints.
adopting to improve public trust regarding AI use:       Specifically, we are unable to obtain articles from
                                                         most sites without active RSS feeds, and we are
    1. Guidance for mixed authorship: editorial          not able to include print-only newspapers. Finally,
       standards should publicly outline what kind of    the data contains inevitable noise. Despite exten-
       AI use is acceptable without disclosure if any    sive data-cleaning efforts, metadata occasionally
       (e.g., grammar checks, style edits), acceptable   appears within article text, which may marginally
affect AI detection and topic classification results.    Adrien Barbaresi. 2021. Trafilatura: A Web Scrap-
                                                           ing Library and Command-Line Tool for Text Dis-
Ethical Considerations                                     covery and Extraction. In Proceedings of the Joint
                                                           Conference of the 59th Annual Meeting of the Asso-
Our data was collected from publicly accessible            ciation for Computational Linguistics and the 11th
                                                           International Joint Conference on Natural Language
newspaper sites, either through RSS feeds or avail-        Processing: System Demonstrations, pages 122–131.
able archives. Given the sensitivity of large-scale        Association for Computational Linguistics.
text collection, we do not release the complete
article texts, but instead provide metadata to re-       BBC News and European Broadcasting Union. 2025.
                                                           News integrity in ai assistants. Technical report, BBC
spect the rights of content owners. We identify            Media Centre. Accessed: 2025-10-21.
AI-generated text using Pangram, an AI detection
model. While Pangram does exhibit very low false-        Natalie Grace Brigham, Chongjiu Gao, Tadayoshi
positive rates in benchmark testing, it is not in-         Kohno, Franziska Roesner, and Niloofar Mireshghal-
                                                           lah. 2024.     Developing story: Case studies
fallible, and all findings should be interpreted as        of generative ai’s use in journalism. Preprint,
detector outputs rather than definitive authorship         arXiv:2406.13706.
attributions. We do not attribute any intent, mis-
                                                         Creston Brooks, Samuel Eggert, and Denis Peskoff.
conduct, or ethical lapses to the individual jour-
                                                           2024. The rise of AI-generated content in Wikipedia.
nalists and newspapers flagged by the model. We            In Proceedings of the First Workshop on Advancing
do not draw conclusions about the intent, conduct,         Natural Language Processing for Wikipedia, pages
or practices of individual journalists, outlets, or        67–79, Miami, Florida, USA. Association for Com-
companies. Results should not be interpreted as            putational Linguistics.
rankings, qualitative judgments, or accusations of       Peter Brown and Klaudia Jaźwińska. 2025. Journalism
wrongdoing. Rather, we purposely use large-scale           zero: How platforms and publishers are navigating ai.
data collection to understand AI use trends at an          Report, Tow Center for Digital Journalism, Columbia
                                                           University.
aggregate level. We aim to understand what trends
in AI use appear across the industry rather than         Tom Brown, Benjamin Mann, Nick Ryder, Melanie
making judgments about specific cases.                     Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
                                                           Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Acknowledgments                                            Askell, Sandhini Agarwal, Ariel Herbert-Voss,
                                                           Gretchen Krueger, Tom Henighan, Rewon Child,
We thank the University of Maryland Compu-                 Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens
                                                           Winter, Chris Hesse, Mark Chen, Eric Sigler, Ma-
tational Linguistics and Information Processing            teusz Litwin, Scott Gray, Benjamin Chess, Jack
(CLIP) Lab for their feedback and support. We are          Clark, Christopher Berner, Sam McCandlish, Alec
grateful to the University of Maryland Howard Cen-         Radford, Ilya Sutskever, and Dario Amodei. 2020.
ter for Investigative Reporting, especially Derek          Language models are few-shot learners. In Ad-
                                                           vances in Neural Information Processing Systems,
Willis and Daniel Trielli, for their guidance. This        volume 33, pages 1877–1901. Curran Associates,
project was partially supported by awards IIS-             Inc.
2046248 and IIS-2312949 from the National Sci-
ence Foundation (NSF) as well as an award from           Roberto Cavazos and Greg Sterling. 2024. The high
                                                           cost of review fraud: An economic analysis of con-
Open Philanthropy.                                         sumer harm. https://askfortransparency.com/
                                                           research/high-cost-of-review-fraud/. Ac-
                                                           cessed: 2025-10-17.
References
                                                         Elizabeth Clark, Tal August, Sofia Serrano, Nikita
Abolfazl Ansari, Delvin Ce Zhang, Nafis Irtiza Tripto,      Haduong, Suchin Gururangan, and Noah A. Smith.
  and Dongwon Lee. 2025. Echoes of automation: The          2021. All that‘s ‘human’ is not gold: Evaluating
  increasing use of llms in newsmaking. In Social,          human evaluation of generated text. In Proceedings
  Cultural, and Behavioral Modeling: 18th Interna-          of the 59th Annual Meeting of the Association for
  tional Conference, SBP-BRiMS 2025, Pittsburgh, PA,        Computational Linguistics and the 11th International
  USA, October 14–17, 2025, Proceedings, page 3–13,         Joint Conference on Natural Language Processing
  Berlin, Heidelberg. Springer-Verlag.                     (Volume 1: Long Papers), pages 7282–7296, Online.
                                                            Association for Computational Linguistics.
Hui Bai, Jan G. Voelkel, Shane Muldowney, Johannes C.
  Eichstaedt, and Robb Willer. 2025. Llm-generated       Jim Conaghan. 2017. Young, old and in-between:
  messages can persuade humans on policy issues. Na-        Newspaper platform readers ages are well-
  ture Communications, 16:6037.                             distributed. https://www.newsmediaalliance.
  org/age-newspaper-readers-platforms/.                     Brian Jabarian and Alex Imas. 2025. Artificial writing
  Highlights Nielsen Scarborough USA+ 2016                    and automated detection.
  Release 2 finding that the median age of daily
  print-newspaper readers is 57.9 years.                    Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan
                                                              Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea
Alexander Coppock, Emily Ekins, and David Kirby.              Madotto, and Pascale Fung. 2023a. Survey of halluci-
  2018. The long-lasting effects of newspaper op-eds          nation in natural language generation. ACM Comput.
  on public opinion. Quarterly Journal of Political           Surv., 55(12).
  Science, 13(1):59–87.
                                                            Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan
Liam Dugan, Andrew Zhu, Firoj Alam, Preslav Nakov,            Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea
  Marianna Apidianaki, and Chris Callison-Burch.              Madotto, and Pascale Fung. 2023b. Survey of halluci-
  2025. GenAI content detection task 3: Cross-domain          nation in natural language generation. ACM Comput.
  machine generated text detection challenge. In Pro-         Surv., 55(12).
  ceedings of the 1stWorkshop on GenAI Content De-
  tection (GenAIDetect), pages 377–388, Abu Dhabi,          Bethany Jones and Richard Jones. 2025. Action re-
  UAE. International Conference on Computational              search at the BBC: Interrogating artificial intelligence
  Linguistics.                                                with journalists to generate actionable insights for the
                                                              newsroom. Journalism, 26(8):1708–1725. Original
Bradley Emi. 2025. All about false positives in
                                                              work published 2025.
  ai detectors. https://www.pangram.com/blog/
  all-about-false-positives-in-ai-detectors.                Brian Kennedy, Eileen Yam, Emma Kikuchi, Isabelle
  Pangram Labs blog.                                          Pula, and Javier Fuentes. 2025. How americans view
Bradley Emi and Max Spero. 2024. Technical Report on          AI and its impact on people and society. Pew Re-
  the Pangram AI-Generated Text Classifier. Preprint,         search Center, Report.
  arXiv:2402.14873.
                                                            Kate Knibbs. 2024. Ai slop is flooding medium. Wired.
Daniel S. Evanko and Michael Di Natale. 2025. Quanti-         Accessed: 2025-10-17.
  fying and assessing the use of generative ai by authors
  and reviewers in the cancer research field. In Peer       Dmitry Kobak, Rocío González-Márquez, Éva A.
  Review Congress. Accessed 2025-10-17.                      Horvát, and Jana Lause. 2025. Delving into
                                                             llm-assisted writing in biomedical publications
Isabel O. Gallegos, Ryan A. Rossi, Joe Barrow,               through excess vocabulary. Science Advances,
   Md Mehrab Tanjim, Sungchul Kim, Franck Dernon-            11(27):eadt3813.    PMID: 40601754; PMCID:
   court, Tong Yu, Ruiyi Zhang, and Nesreen K. Ahmed.        PMC12219543.
   2024. Bias and fairness in large language models:
   A survey. Computational Linguistics, 50(3):1097–         Daniel Chaein Lee, Jihoon Jhang, and Tae Hyun Baek.
   1179.                                                      2025. Ai-generated news content: The impact of AI
                                                              writer identity and perceived AI human-likeness. In-
Isabel O. Gallegos, Chen Shani, Weiyan Shi, Federico          ternational Journal of Human-Computer Interaction,
   Bianchi, Robb Willer, and Dan Jurafsky. 2025. AI-          pages 1–13. Published online 2025-03-24; Taylor &
   generated content and public persuasion: The lim-          Francis.
   ited effect of AI authorship labels. In NeurIPS 2024
   Workshop on Regulatable ML.                              Weixin Liang, Zachary Izzo, Yaohui Zhang, Haley Lepp,
                                                              Hancheng Cao, Xuandong Zhao, Lingjiao Chen, Hao-
Tarun Gupta and Danish Pruthi. 2025. All that glitters        tian Ye, Sheng Liu, Zhi Huang, Daniel A. McFarland,
  is not novel: Plagiarism in AI generated research.          and James Y. Zou. 2024a. Monitoring ai-modified
  In Proceedings of the 63rd Annual Meeting of the            content at scale: a case study on the impact of chatgpt
  Association for Computational Linguistics (Volume 1:        on ai conference peer reviews. In Proceedings of the
  Long Papers), pages 25721–25738, Vienna, Austria.           41st International Conference on Machine Learning,
  Association for Computational Linguistics.                  ICML’24. JMLR.org.
Hans W. A. Hanley and Zakir Durumeric. 2024.
  Machine-made media: Monitoring the mobilization           Weixin Liang, Yaohui Zhang, Mihai Codreanu,
  of machine-generated articles on misinformation and        Jiayu Wang, Hancheng Cao, and James Zou.
  mainstream news websites. Proceedings of the Inter-        2025. The widespread adoption of large language
  national AAAI Conference on Web and Social Media,          model-assisted writing across society. Preprint,
  18(1):542–556. ICWSM 2024.                                 arXiv:2502.09747.

Tony Hu, Yuliya Kyrychenko, Steve Rathje, et al. 2025.      Weixin Liang, Yaohui Zhang, Zhengxuan Wu, Haley
  Generative language models exhibit social identity         Lepp, Wenlong Ji, Xuandong Zhao, Hancheng Cao,
  biases. Nature Computational Science, 5:65–75.             Sheng Liu, Siyu He, Zhi Huang, Diyi Yang, Christo-
                                                             pher Potts, Christopher D Manning, and James Y.
IPTC. 2025. Media topics. https://iptc.org/                  Zou. 2024b. Mapping the increasing use of LLMs in
  standards/media-topics/. Accessed: 2025-09-                scientific papers. In First Conference on Language
  29.                                                        Modeling.
Michael Lipka and Kirsten Eddy. 2025. Relatively few      OpenAI. 2024. Gpt-4.1. https://platform.openai.
  americans are getting news from AI chatbots like          com/docs/models/gpt-4.1. Accessed 2025.
  ChatGPT. Pew Research Center, Short Reads.
                                                          Pangram. 2024.   Pangram multilingual v2: Ex-
Chiara Longoni, Andrey Fradkin, Luca Cian, and Gor-         pansion of ai content detection into multiple
  don Pennycook. 2022. News from generative arti-           languages.   https://www.pangram.com/blog/
  ficial intelligence is believed less. In Proceedings      pangram-multilingual-v2. Pangram Labs blog.
  of the 2022 ACM Conference on Fairness, Account-
  ability, and Transparency, FAccT ’22, page 97–106,      Pew Research Center. 2025.        News plat-
  New York, NY, USA. Association for Computing              forms (news & information) – american
  Machinery.                                                trends panel wave 177:      Topline results.
                                                            https://www.pewresearch.org/wp-content/
Ziming Luo, Zonglin Yang, Zexin Xu, Wei Yang,               uploads/sites/20/2025/09/PJ_2025.09.25_
  and Xinya Du. 2025. Llm4sr: A survey on large             news-information-fact-sheets_topline.pdf.
  language models for scientific research. Preprint,
  arXiv:2501.04306.                                       Qwen Team. 2025. Qwen3 technical report. Preprint,
                                                           arXiv:2505.09388.
Hana Matatov, Marianne Aubin Le Quéré, Ofra Amir,
  and Mor Naaman. 2025. Examining the prevalence          Damian Radcliffe. 2025. Journalism in the AI era: Op-
  and dynamics of ai-generated media in art subreddits.     portunities and challenges in the global south and
  Preprint, arXiv:2410.07302.                               emerging economies. Trf insights report, Thomson
                                                            Reuters Foundation. Survey of 200+ journalists from
Joshua Maynez, Shashi Narayan, Bernd Bohnet, and            70+ countries.
  Ryan McDonald. 2020a. On faithfulness and factu-
  ality in abstractive summarization. In Proceedings      Jenna Russell, Marzena Karpinska, and Mohit Iyyer.
  of the 58th Annual Meeting of the Association for         2025. People who frequently use ChatGPT for writ-
  Computational Linguistics, pages 1906–1919, On-           ing tasks are accurate and robust detectors of AI-
  line. Association for Computational Linguistics.          generated text. In Proceedings of the 63rd Annual
                                                            Meeting of the Association for Computational Lin-
Joshua Maynez, Shashi Narayan, Bernd Bohnet, and            guistics (Volume 1: Long Papers), pages 5342–5373,
  Ryan McDonald. 2020b. On faithfulness and factu-          Vienna, Austria. Association for Computational Lin-
  ality in abstractive summarization. In Proceedings        guistics.
  of the 58th Annual Meeting of the Association for
  Computational Linguistics, pages 1906–1919, On-         Fabio Salvi, Manoel Horta Ribeiro, Riccardo Gallotti,
  line. Association for Computational Linguistics.          et al. 2025. On the conversational persuasiveness of
                                                            gpt-4. Nature Human Behaviour, 9(10):1645–1653.
Medill Local News Initiative. 2024. Ai and local news:
 Report 2024. Technical report, Northwestern Univer-      Philipp Schoenegger, Francesco Salvi, Jiacheng Liu, Xi-
 sity. Accessed: 2025-10-01.                                aoli Nan, Ramit Debnath, Barbara Fasolo, Evelina
                                                            Leivada, Gabriel Recchia, Fritz Günther, Ali
Nicole Meir. 2023. Standards around generative ai. The
                                                            Zarifhonarvar, Joe Kwon, Zahoor Ul Islam, Marco
  Definitive Source: Behind the News, The Associated
                                                            Dehnert, Daryl Y. H. Lee, Madeline G. Reinecke,
  Press. Accessed on 2025-10-15.
                                                            David G. Kamper, Mert Kobaş, Adam Sandford,
Zachary Metzger. 2024. The state of local news 2024.        Jonas Kgomo, Luke Hewitt, Shreya Kapoor, Kerem
  Technical report, Northwestern University. Accessed:      Oktar, Eyup Engin Kucuk, Bo Feng, Cameron R.
  2025-10-01.                                               Jones, Izzy Gainsburg, Sebastian Olschewski, Nora
                                                            Heinzelmann, Francisco Cruz, Ben M. Tappin, Tao
Jan Nehring, Aleksandra Gabryszak, Pascal Jür-              Ma, Peter S. Park, Rayan Onyonka, Arthur Hjorth,
  gens, Aljoscha Burchardt, Stefan Schaffer, Matthias       Peter Slattery, Qingcheng Zeng, Lennart Finke, Igor
  Spielkamp, and Birgit Stark. 2024. Large language         Grossmann, Alessandro Salatiello, and Ezra Karger.
  models are echo chambers. In Proceedings of the           2025. Large language models are more persua-
  2024 Joint International Conference on Computa-           sive than incentivized human persuaders. Preprint,
  tional Linguistics, Language Resources and Evalu-         arXiv:2505.09662.
  ation (LREC-COLING 2024), pages 10117–10123,
  Torino, Italia. ELRA and ICCL.                          Minkyu Shin, Jin Kim, and Jiwoong Shin. 2025. The
                                                            adoption and efficacy of large language models: Ev-
Nic Newman, Amy Ross Arguedas, Craig T.                     idence from consumer complaints in the financial
  Robertson, Rasmus Kleis Nielsen, and Richard              industry. Preprint, arXiv:2311.16466.
  Fletcher. 2025.   Digital news report 2025.
  https://reutersinstitute.politics.ox.ac.                Felix M. Simon. 2024. Artificial intelligence in the
  uk/sites/default/files/2025-06/Digital_                   news: How ai retools, rationalizes, and reshapes jour-
  News-Report_2025.pdf. Accessed: 2025-09-30.               nalism and the public arena. Report, Tow Center for
                                                            Digital Journalism, Columbia University.
OpenAI. 2022. Introducing ChatGPT. https://
  openai.com/blog/chatgpt. Accessed: 2025-10-             Felix M. Simon, Rasmus Kleis Nielsen, and Richard
  06.                                                       Fletcher. 2025. Generative ai and news report 2025:
  How people think about ai’s role in journalism and      Li Zhou, Ruijie Zhang, Xunlian Dai, Daniel Hersh-
  society. Report, Reuters Institute for the Study of       covich, and Haizhou Li. 2025. Large language mod-
  Journalism, University of Oxford.                         els penetration in scholarly writing and peer review.
                                                            Preprint, arXiv:2502.11193.
Jinyan Su, Claire Cardie, and Preslav Nakov. 2024.
   Adapting fake news detection to the era of large
   language models. In Findings of the Association        A        Dataset
   for Computational Linguistics: NAACL 2024, pages
   1473–1490, Mexico City, Mexico. Association for        In this section of the appendix we provide more
   Computational Linguistics.                             details on our data collection process.

Zhen Sun, Zongmin Zhang, Xinyue Shen, Ziyi Zhang,         recent_news additional collection details. To
  Yule Liu, Michael Backes, Yang Zhang, and Xinlei        facilitate automatic data collection, we first obtain a
  He. 2025. Are we in the AI-generated text world
  already? quantifying and monitoring AIGT on social
                                                          list of 6,175 URLs for American newspapers30 and
  media. In Proceedings of the 63rd Annual Meeting of     filter out those that are unreachable and/or do not
  the Association for Computational Linguistics (Vol-     have active RSS feeds, which yielded 1,528 URLs.
  ume 1: Long Papers), pages 22975–23005, Vienna,         Roughly twice a week, from June 15 to September
  Austria. Association for Computational Linguistics.     15, we automatically accessed each RSS feed and
Katherine Thai, Bradley Emi, Elyas Masrour, and Mohit     downloaded the full text and metadata for up to 50
  Iyyer. 2025. Editlens: Quantifying the extent of ai     recently-published articles from each paper.31 Each
  editing in text. Preprint, arXiv:2510.03154.            full text article was then preprocessed using the
Edward Tian and Alexander Cui. 2023. GPTZero: To-         Trafilatura (Barbaresi, 2021) and Newspaper4K32
  wards detection of AI-generated text using zero-shot    libraries to strip headers/footers, advertisements,
  and supervised methods. https://gptzero.me.             and HTML artifacts from the text.
  Accessed: 2025-10-09.
                                                   Topic classification. Each instance was pre-
Benjamin Toff and Felix M. Simon. 2025. “Or They
                                                   sented to the Q WEN 3-8B model with the full ar-
  Could Just Not Use It?”: The Dilemma of AI Disclo-
                                                   ticle text and an instruction to select the single
  sure for Audience Trust in News. The International
  Journal of Press/Politics, 30(4):881–903.        most semantically appropriate topic from the IPTC
UNC Center for Innovation & Sustainability in Lo-  taxonomy. The complete prompt is shown in Fig-
  cal Media. 2020. Newspapers 2020 — active u.s.   ure 5. To verify, we randomly sampled 100 articles
  newspapers as of 2020. https://usnewsdeserts. from the recent_news set. Two of the authors in-
  cislm.org/. Accessed: 2025-09-29.                dependently re-labeled these samples according to
Katharine Viner and Anna Bateson. 2023. The        the same IPTC taxonomy. Inter-annotator agree-
  guardian’s approach to generative ai. Accessed:  ment between the two human raters was 87% (Co-
  2025-10-17.                                      hen’s κ = 0.85), reflecting strong consistency
Washington Post Staff. 2022.       The washington  in human judgments. Agreement between the
  post guide to writing an opinion article. https: Q WEN 3-8B predictions and the majority human
  //www.washingtonpost.com/opinions/2022/          label averaged 77%, indicating moderately strong
  op-ed-writing-guide-washington-post-examples/.   alignment between the classifier and human anno-
  Updated June 23, 2022; accessed 2025-10-16.
                                                   tations.
Laura Weidinger, Jonathan Uesato, Maribeth Rauh,
  Conor Griffin, Po-Sen Huang, John Mellor, Amelia        Topics present in datasets. The classification
  Glaese, Myra Cheng, Borja Balle, Atoosa Kasirzadeh,     scheme in this work builds on the 17 top-level cate-
  Courtney Biles, Sasha Brown, Zac Kenton, Will           gories defined in the International Press Telecom-
  Hawkins, Tom Stepleton, Abeba Birhane, Lisa Anne
  Hendricks, Laura Rimell, William Isaac, Julia Haas,     munications Council (IPTC) “Media Topics” tax-
  Sean Legassick, Geoffrey Irving, and Iason Gabriel.     onomy. We map each article to one of the 17 top-
  2022. Taxonomy of risks posed by language models.       level topics. In addition to those categories, we
  In Proceedings of the 2022 ACM Conference on Fair-      include two supplementary labels — “Obituary”
  ness, Accountability, and Transparency, FAccT ’22,
  page 214–229, New York, NY, USA. Association for            30
                                                                https://onlinenewspapers.com/usstate/
  Computing Machinery.                                    usatable.shtml
                                                             31
                                                                While the majority of recent_news is obtained from RSS
Eileen Yam and Brian Kennedy. 2025. From political        feeds, articles from some newspapers (e.g., Washington Post,
   speeches to songs, how would americans react if they   Wall Street Journal) were accessed via ProQuest Recent News-
   found out AI was involved? Pew Research Center,        papers.
   Short Reads.                                              32
                                                                https://github.com/AndyTheFactory/newspaper4k
   Prompt for classifying topic of articles

   Classify the following article into the most appropriate primary topic from the IPTC taxonomy.

   IPTC Primary Topics:
   {taxonomy_text}

   Article to classify:
   Title: {article.title}
   Text: {article_text}

   Instructions:
   1. Carefully read the article content and identify the main focus
   2. Choose the most appropriate primary topic from the taxonomy above
   3. Base your decision on the primary subject matter and content focus
   4. Consider the description of each category when making your choice
   5. If the article truly doesn't fit well into any of the listed categories, choose "Other"
   6. Be specific and accurate - don't force a category if it's not a good fit
   7. Respond ONLY with the classification in this exact format:

   <classification>
   Primary Topic: [exact primary topic name]
   </classification>



                               Figure 5: Prompt for classifying topic of articles


and “Other” — to capture content that does not
cleanly fall into the predefined classes. Definitions
of topics are displayed in Table 4 and the distribu-
tion of topics across the three datasets are shown
in Table 5.

Circulation definition and data source. In the
U.S. News Deserts Database, circulation refers ex-
clusively to the average number of printed copies
distributed per publishing day, excluding any dig-
ital readership metrics. These figures are com-
                                                          Figure 6: Distribution of circulations of articles in the
piled primarily from Alliance for Audited Me-             recent_news dataset.
dia (AAM) audits when available, and supple-
mented with publisher self-reports, state press as-
sociation directories, and industry trade sources         main dataset contains 1560 unique newspapers, of
for unaudited outlets. As noted in the database’s         which 776 (49.74 %) report any circulation figure.
section “Dealing with Circulation Limitations”            Unless otherwise noted, all circulation–AI likeli-
on https://www.usnewsdeserts.com/methodology/,            hood correlations are computed on this overlapping
many small newspapers rely on self-reported or            set to avoid missing-data biases.
infrequently updated numbers, which are treated
as approximate indicators of print scale rather than
precise measures of audience size. The distribution       Ownership Details Our ownership information
of newspapers by circulation amounts is depicted          comes from the Northwestern Local News Initia-
in Figure 6.                                              tive (Medill Local News Initiative, 2024). We
                                                          collect ownership information for 162,342 arti-
Data coverage and overlap. Our correlation                cles (87.04% of recent_news) and 1,259 unique
analysis uses the subset of articles for which both       newspapers (82.40% of unique newspapers in
AI-likelihood and circulation are observed. Out of        recent_news). Since ownership of newspapers
186 507 articles in total print circulation is avail-     is transferred frequently, this database shows own-
able for 101 799 (54.58 %). At the outlet level, the      ership information current as of November 2025.
Topic                                        Definition (IPTC summary)
arts, culture, entertainment and media       All forms of arts, entertainment, cultural heritage and media
conflict, war and peace                      Acts of socially or politically motivated protest or violence, military activities,
                                             geopolitical conflicts, as well as resolution efforts
crime, law and justice                       The establishment and/or statement of the rules of behavior in society, the enforce-
                                             ment of these rules, breaches of the rules, the punishment of offenders and the
                                             organizations and bodies involved in these activities
disaster, accident and emergency incident    Man made or natural event resulting in loss of life or injury to living creatures
                                             and/or damage to inanimate objects or property
economy, business and finance                All matters concerning the planning, production and exchange of wealth.
education                                    All aspects of furthering knowledge, formally or informally
environment                                  The protection, damage, and condition of the ecosystem of the planet Earth and its
                                             surroundings
health                                       All aspects of physical and mental well-being
human interest                               Item that discusses individuals, groups, animals, plants or other objects in an
                                             emotional way
labor                                        Social aspects, organizations, rules and conditions affecting the employment of
                                             human effort for the generation of wealth or provision of services and the economic
                                             support of the unemployed.
lifestyle and leisure                        Activities undertaken for pleasure, relaxation or recreation outside paid employ-
                                             ment, including eating and travel.
politics and government                      Local, regional, national and international exercise of power, the day-to-day running
                                             of government, and the relationships between governing bodies and states.
religion                                     Belief systems, institutions and people who provide moral guidance to followers
science and technology                       All aspects pertaining to human understanding of, as well as methodical study and
                                             research of natural, formal and social sciences, such as astronomy, linguistics or
                                             economics
society                                      The concerns, issues, affairs and institutions relevant to human social interactions,
                                             problems and welfare, such as poverty, human rights and family planning
sport                                        Competitive activity or skill that involves physical and/or mental effort and organi-
                                             zations and bodies involved in these activities
weather                                      The study, prediction and reporting of meteorological phenomena
Additional labels used in our classification
Obituary                                     Memorial and death-notice content about individuals.
Other                                        Articles that do not clearly align with any IPTC top-level topic.

           Table 4: Top-level topics from the IPTC Media Topics taxonomy and definitions (IPTC, 2025).

              Topic                                   recent_news (%)       opinions (%)       ai_reporters (%)
              Politics and government                           15.02              56.86                  19.55
              Economy, business and finance                     10.53                9.77                   2.30
              Arts, culture, entertainment & media              20.55                4.87                   6.55
              Opinion                                             0.40               4.65                   0.75
              Health                                              3.75               4.47                 12.92
              Human interest                                      3.61               2.91                   6.09
              Crime, law and justice                            10.91                2.80                   7.41
              Environment                                         4.22               2.77                   4.36
              Education                                           3.72               2.06                 10.27
              Science and technology                              0.98               1.97                   0.72
              Society                                             1.29               1.86                   3.71
              Conflict, war and peace                             0.54               1.72                   0.35
              Labor                                               1.54               0.96                   1.45
              Religion                                            0.74               0.94                   0.69
              Sport                                             11.24                0.69                   5.28
              Lifestyle and leisure                               1.70               0.42                   0.50
              Disaster, accident, emergency                       3.69               0.23                   1.25
              Obituary                                            2.48               0.04                   1.49
              Weather                                             0.76               0.01                   0.37
              Other                                                  –                  –                 14.00

          Table 5: Comparison of topic distributions between recent_news, opinions, and ai_reporters.


Lengths of datasets.      We see that all datasets                recent news which has an average of 787.4 tokens.
are similar lengths, with opinions being slightly                 Comparison of lengths shown in Figure 7.
longer at an average of 1078.4 tokens, compared to
                                                            reporters who “authored” multiple AI articles
                                                            in recent_news. Each reporter in this dataset
                                                            published articles written both before and af-
                                                            ter the release of ChatGPT (November 2022),
                                                            enabling longitudinal analysis.

                                                         Additionally, we analyze ai_reporters, a lon-
                                                      gitudinal dataset for 10 veteran reporters (5 male
                                                      and 5 female) who published articles both before
Figure 7: Comparison of the lengths of articles in    and after ChatGPT’s release (November 2022) and
recent_news, opinions, and ai_reporters               had at least three articles in recent_news labeled
                                                      as either AI-G ENERATED or M IXED .33 For
B   AI Detection                                      each reporter, we scrape all of their available online
                                                      articles and run the same detection pipeline detailed
In this section of the appendix we discuss details    in §2 . We note that since the reporters selected for
of how we used AI Detection models.                   this analysis have multiple articles flagged for AI
Pangram prediction API details. Pangram is a          use in recent_news, they are not representative of
highly accurate AI detection language model (Emi      all reporters. Nevertheless, they give us valuable
and Spero, 2024). To detect AI, Pangram divides       insight into some of the heaviest adopters of AI in
the text into segments, with each segment assigned    modern American journalism.
an AI probability score before an overall confi-
dence score and final label are produced We use       ai_reporters Several                reporters        in
Pangram v2 for all results in this study. However,    recent_news published articles both before
examples may reflect newer versions of Pangram        and after the release of ChatGPT, making them
likelihood.                                           good candidates for a longitudinal analysis to
                                                      explore when and how they started using AI.
Condensing the Pangram API labeling scope.            We identify a set of 10 veteran reporters from
To standardize categories across Pangram’s short-     recent_news who meet two criteria: (1) they have
text (single pass) and long-text (sliding-window)     published articles prior to November 2022,34 and
endpoints, we collapse the vendor’s granular labels   (2) at least three of their articles were identified as
into three meta-labels used throughout our analy-      M IXED or AI-G ENERATED . We then write ten
sis: H UMAN - WRITTEN = {Human, Unlikely AI};         custom scrapers, one for each reporter, to collect
 M IXED = {Mixed, Possibly AI, Likely AI}; and        a corpus of all of their published articles that are
 AI-G ENERATED = {Highly Likely AI, AI}.              available online, resulting in a final dataset of
Comparison to GPTZero. We drew a balanced             20,132 articles from 14 newspapers.35
sample of 1,000 articles from Pangram: 500 la-
                                                      AI use by these reporters rises from 0% pre-
beled AI / Highly Likely AI and 500 labeled Human
                                                      ChatGPT to 40% in 2025. Figure 8 shows a
/ Unlikely AI. We then ran GPTZero on the same
                                                      near-absence in AI use prior to November 2022
texts; GPTZero returns human, mixed, or ai. For
                                                      before rising sharply to 15.7% in 2023, 36.1% in
evaluation, we binarized the GPTZero outputs by
                                                      2024, and then 40.4% in 2025. This result also
counting mixed as AI and compared the two de-
tectors on this binary task. Under this protocol,        33
                                                            All but one reporter are veteran reporters, often with
we observed 88.2% raw agreement and Cohen’s           decades of experience. However, due to technical difficul-
                                                      ties associated with scraping specific websites, we could not
κ = 0.764 (118/1,000 disagreements).                  obtain all of their older articles. The one early-career reporter
                                                      started their career in 2021, and thus had less exposure to
      Pangram\GPTZero Human AI                        the profession prior to the release of ChatGPT. The reporters
           Human       490   10                       collectively cover a variety of topics ranging from local gov-
                                                      ernment, public safety, and environmental justice to national
             AI        108  392                       politics, racial equity, LGBTQ+ rights, Caribbean-American
                                                      culture, economic development, and community sports.
C   Tracking reporter adoption of AI                     34
                                                            This cutoff was selected because the public release
                                                      of ChatGPT in November 2022 (OpenAI, 2022) made AI-
     ai_reporters is a historical dataset of 20K      assisted writing tools widely accessible.
                                                         35
     articles published by a subset of 10 veteran           One journalist published in multiple newspapers.
                                                             AI use over time (%)                                                 D     Additional Results
                                                                                                                        40.4%
          AI Article Percentage (%)
                                  40                                                                               36.1%
                                                                                                                                  D.1    recent_news
                                  30

                                  20
                                                                                                                                  In this section, we report more results about
                                                                                                            15.7%
                                  10
                                                                                                                                  recent_news, a collection of over 185k articles
                                                                 0.1% 0.1% 0.2%      0.2% 0.1% 0.3%                               collected between June 15th and September 15th,
                                      0 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025
                                                                            Year                                                  2025.
                                                             Article count by year
                                                                                                                    3082          Overall       AI     usage      in   recent_news.
                    3000                       Human-written                                                2843
                                                                                                     2653
                                                                                                                                  recent_news has 90.9% H UMAN - WRITTEN
Number of Articles




                    2500                       AI-generated or Mixed
                                                                                                                           2196
                    2000
                                                                                    1629 1546 1556                                articles, with a total of 9.1% having AI Use. 5.2%
                    1500
                                                                        1191 1209
                    1000                                                                                                          is detected as AI-G ENERATED and 3.9% is
                                                                  753
                                                            550
                           500                291 321 217                                                                          M IXED as shown in Figure 9. The distribution
                                         94
                                      0 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025                of AI likelihoods per each of the three labels is
                                                                            Year
                                                                                                                                  shown in Figure 10. Data by state is displayed
    Figure 8: AI adoption takes off after ChatGPT’s release                                                                       in Figure 11 and Figure 12 Band by topic in
    in late 2022 with the ten reporters in our ai_reporters                                                                       Figure 13.
    sample.



   serves as a sanity check on Pangram’s reliabil-
   ity: as all of these reporters published articles pre-
   ChatGPT that were correctly detected as human-
   written, it is unlikely that their unique writing styles
   are a source of false positives.

   While AI use varies across this cohort of re-
   porters, none discloses their use. We observe
   high variance in AI use across these ten reporters.
   While some show a negligible increase in arti-
                                                                                                                                  Figure 9: Distribution of AI Use predictions in
   cles flagged with AI use (from 0% in 2022 to                                                                                   recent_news.
   about 2.3% in 2025), others are far more recep-
   tive. For instance, 90.1% of the most prolific au-
   thor’s 2025 articles were classified as M IXED or
    AI-G ENERATED , up from 0% in 2022 (see indi-
   vidual plots in §D.3). Importantly, none of the ten
   reporters disclose use of AI to their readership.36

   AI traces are visible in the articles. Perhaps not
   surprisingly, we observe qualitative differences be-
   tween the articles marked for AI use and the human-
   written ones. For instance, AI-assisted articles in
   this subset have up to 11.53× more em dashes than
   those authored entirely by humans (Table 6, Re-                                                                                Figure 10: Distribution of AI Likelihoods per each AI
   porter 3). Furthermore, human-written articles tend                                                                            Use category in recent_news.
   to be more concrete, naming specific people and
   locations ( Reporter 1) and focus more on factual
                                                                                                                                  Newspaper-level test (below 100K vs. 100K+ cir-
   knowledge than vague statements ( Reporter 2).
                                                                                                                                  culation). We collapse to one observation per out-
                                                                                                                                  let (share of AI-labeled articles) and compare news-
                           36
        We reached out to each reporter in this cohort with a                                                                     papers below 100K circulation to those at 100K+.
    publicly-available email address in an effort to learn more
    about their AI use, but (perhaps unsurprisingly) we received                                                                  The below-100K group (n=750) averages 8.47% AI
    no responses.                                                                                                                 articles (median 2.93%, SD 16.08, range 0–100),
R EPORTER    H UMAN - WRITTEN                                    AI-G ENERATED or M IXED                           O BSERVATION

  1         “Problems associated with the past California       “The State of California has established the       The human-written article names specific rele-
            administration seem to have dissipated as the       Salton Sea Conservancy under the Salton Sea        vant people, times, and pinpoints the main point
            IID and Newsome government officials are on         Conservancy Act, a comprehensive initiative        of the article, the restoration of the Salton Sea.
            the verge of agreeing to a plan restoring the       to reverse decades of ecological damage and        In the AI article, the conservancy act is tied to
            lower part of the Salton Sea as reported by Wa-                                                        lofty statements such as ’decades of ecological
                                                                promote sustainable development in the Salton
            ter Manager Tina Shields during the April 30                                                           damage’.
                                                                Sea region. This new state agency, housed within
            meeting. ...”
                                                                the Natural Resources Agency, is poised to
            (2019-05-06)                                        lead the charge ..."
                                                                (2024-11-18)

  2         “One shouldn’t need a reason to buy Black, it       “The spending power of the Black dollar            In the human-written article, the reporter uses
            should be a way of life. Such is the thought        stands at a staggering $1.7 trillion, reflecting   unique phrases like ’hang their hat’ and ’mom-
            process for several Black business owners and       immense potential for community growth and         and-pop shops’, focusing on specific ways the
            individuals who hang their hat on the idea of       economic empowerment. This financial strength,     reader could buy from Black businesses. In
            supporting within to keep the Black dollar circu-   however, is underutilized, prompting a crucial     the latter, the “author” makes sweeping claims
            lating longer in local neighborhoods, mom-and-      need for increased and unconditional support       about the financial state of Black businesses in
            pop shops, and places that need it most...”         within the African American community...”          a more general manner.
            (2023-02-15)                                        (2023-11-29)

  3         “The UN General Assembly met on Tuesday af-         “The Government of Guyana has expressed its        In the human-written article, the author refer-
            ternoon in Emergency Special Session on the         support for the United States’ call for a cease-   ences the time (Tuesday) and setting (Emer-
            decades long Israel-Palestine conflict and as       fire in the ongoing conflict between Israel and    gency Special Setting). In the AI-generated arti-
            the ongoing crisis in Gaza shows no signs of        Gaza.     In a recent statement , the Guyanese     cle, the author uses more fluff words and more
            abating. Member States adopted a resolution,        government acknowledged the three-phase plan       vague time placement (i.e. ongoing, recent).
            demanding an “immediate humanitarian cease-         proposed by U.S. President Joseph Biden on
            fire”, the immediate and unconditional release      May 31, 2024, aimed at ending Israel’s war on
            of all hostages ...”                                Gaza...”
            (2024-06-20)                                        (2025-03-21)


Table 6: Excerpts from passages of newspaper articles written by reporters in the ai_reporters dataset. Words
and phrases identified as indicative of AI use by Pangram are highlighted in red. In the left H UMAN - WRITTEN
column, excerpts of older, human-written articles are displayed, while the AI-G ENERATED or M IXED column
shows newer articles by the same author detected as AI-generated or assisted. When AI use is present, articles by
these reporters include fewer specific details, broader time markers, and loftier language.


while the 100K+ group (n=24) averages 4.95% (me-                                                     Table 7: Language distribution
dian 1.75%, SD 7.14, range 0–24.74). The differ-
                                                                                                      Language                             % (n)
ence in means is +3.52 percentage points (Cohen’s
d = 0.22). A Welch t-test indicates a statistically                                                   English             95.16% (177,478)
                                                                                                      Spanish                3.88% (7,235)
significant gap (t = 2.24, p = 0.032), whereas                                                        Portuguese               0.25% (468)
a Mann–Whitney U test does not (U = 9506,                                                             Vietnamese               0.22% (403)
p = 0.634). The divergence reflects heavy right-                                                      French                   0.18% (343)
                                                                                                      Polish                   0.17% (314)
skew and zero-inflation in the outlet-level shares:                                                   Other                    0.15% (271)
mean-based tests are more sensitive to a few high-
AI smaller outlets, while rank-based tests empha-                                    Other includes: Russian (163), German (37), Yiddish (27),
                                                                                    Indonesian (25), Turkish (10), Dutch (5), Latin (2), Ukrainian
size the bulk of the distribution. In other words,                                           (1), Chinese (1). Total: 186,512 articles.
higher AI usage is not uniform across smaller out-
lets; it is concentrated in a subset of them, while
many smaller outlets have low (often zero) AI                                       older demographic less likely to be technologically
shares. Overall, we read this as modest evidence                                    savvy, with a median age of 57.9 (Conaghan, 2017).
that smaller-circulation newspapers exhibit higher                                  We further note that readers of print newspapers
AI usage on average. In Figure 15, the rate of news-                                face higher barriers to verifying content, in contrast
papers labeled as AI-G ENERATED or M IXED is                                        to digital readers who can simply copy and paste
much lower in papers with cirulation above 100k.                                    text into search engines. Thus, newspapers that
                                                                                    only appear in print are much harder to audit using
AI use in print. Many AI-G ENERATED articles                                        our methodology.
in recent_news appear in print in addition to the
online editions. According to a 2025 Pew study, the                                 Detecting     Hallucinated     Content We
print audience still includes an estimated 65 mil-                                  manually reviewed 200 articles:       100 ar-
lion Americans who read physical newspapers “of-                                    ticles predicted as      AI-G ENERATED and
ten” or “sometimes” (Pew Research Center, 2025).                                    100    predicted    as     H UMAN - WRITTEN .
Critically, this group is heavily skewed towards an                                 41%     of    AI-G ENERATED and      5%   of
Figure 11: Map of the United States showing the AI use (%), number of articles, and number of unique newspapers
for each state. States in the mid-Atlantic and southern US exhibit markedly higher AI use than other states. Note
that this plot only considers articles written in English (see Figure 12 for others).




Figure 12: AI use in articles written in languages other than English. The most common language are Spanish,
Portuguese, and Vietnamese.


 H UMAN - WRITTEN contained factual inaccuracies          ticles contain at least one AI-generated quote, and
refered to as hallucinations. Some examples of            403 articles contain both AI-generated narrative
hallucinations found in AI-G ENERATED articles            and AI-generated quotes. To test whether length
are depicted in Table 8.                                  influences detection, we also compare long quotes
                                                          (≥ 120 words, n = 870) to short quotes, finding no
Detecting AI in quoted speech We analyze                  significant difference in AI likelihood (two-sample
30,462 articles with available quote-level pre-           t-test, p = 0.96).
dictions. Each quote is evaluated with an AI-
likelihood classifier, restricted to spans of at least    Many AI-generated articles contain authentic
50 tokens to reduce false positives on very short         quotes. To examine whether articles labeled as
fragments. We treat quotes labeled as Unlikely AI          M IXED and AI-G ENERATED include fabricated
or Human as human-written, and all others (Highly         information, we analyze the authorship of quota-
Likely AI, AI, Likely AI, Mixed, Possibly AI) as          tions in these articles. Specifically, we extract all
AI-generated. At the article level, we compare the        quotes in the dataset longer than 50 words, and
incidence of AI quotes in AI-flagged versus human-        run each of them through Pangram individually.
flagged articles, yielding P (AI quote|AI article) =      Note that Pangram’s reliability degrades on shorter
0.239 and P (AI quote|human article) = 0.034.             texts, and so we are unable to perform this anal-
Conversely, the probability that an article is AI-        ysis on all quotes. Within the subset of articles
generated given the presence of an AI quote is            that include at least one quote >50 words long,
P (AI article|AI quote) = 0.293. In total, 1,376 ar-      76.1% of articles flagged with AI use contain at
    N EWSPAPER                          A RTICLE E XCERPT                                                      H ALLUCINATION
    LA SENTINEL    “We know that 52 percent of adult women across this country          The percent of woman on medicaid is 19%, not 52% (Source).
                   are on Medicaid, and that number is exponentially higher in Los      The article also contains other hallucinations such as referring to
                   Angeles”                                                             ’former President Trump’ in 2025, when he is the current U.S.
                                                                                        president.
    SANTA FE RE-   “The program is currently set to expire in June 2030 under the       The program is set to expire in 2027, not 2030 as reported in the
    PORTER         reconciliation bill, though advocates continue pushing for longer    article (Source).
                   extensions and inclusion of additional affected communities.”
    SUNCOAST       “”We’re not trying to silence anyone,” Koulianos said. “We’re        Most of the quotes in this article, including the excerpt here,
    NEWS           trying to conduct the people’s business in a reasonable time-        cannot be found in the transcript of the Board of Commissioners
                   frame.” ‘’                                                           meeting (Source). Most quotes are paraphrases or similar quotes,
                                                                                        but do not have the same wording.
   THE             “It still shows up, five days a week in print and daily online, to   In an article detailing the history of their own paper, they incor-
   ADVOCATE-       deliver what no outside media outlet ever could: the truth of this   rectly state the paper is printed 5 times a week, when in reality it
   MESSENGER       town, in this moment, for these people.”                             is printed twice a week. (Source).


               Table 8: Examples of hallucinations found in articles predicted as AI-G ENERATED .


                                                                               size = 4.16). The Associated Press appears most
                                                                               frequently, in 1664 clusters and 4030 redistributed
                                                                               articles, consistent with syndication as the domi-
                                                                               nant driver of redistribution. Across all duplicates,
                                                                               6.7 % are labeled AI-generated, with a lower rate
                                                                               for exact duplicates (3.1 %) and a markedly higher
                                                                               rate for semantically similar duplicates (14.3 %).
                                                                               Figure 16 summarize the resulting cluster-size dis-
                                                                               tribution; Table 9 lists the top content providers
                                                                               present in duplicate coverage.
                                                                                            Rank      Author                               Count
                                                                                               1      Assoicated Press                     4,011
                                                                                               2      Unknown                              1,204
                                                                                               3      Staff Reports                          701
                                                                                               4      Advance Local Weather Alerts           404
                                                                                               5      USA Today Network                      264
                                                                                               6      Myedmondnews                           104
                                                                                               7      Teresa Wippel                          101
                                                                                               8      WP Block Co-Authors                     98
                                                                                               9      Cascade PBS Staff                       82
                                                                                              10      Grace Gilson                            81

Figure 13: AI use by topic in recent_news. Weather,                            Table 9: Top 10 authors by frequency of appearances in
science/technology, and health exhibit higher AI use                           duplicate articles.
than topics like conflict, crime/justice, and religion.

                                                                               Effects of machine translation on AI-text detec-
least one human-written quote. This suggests that                              tion. As depicted in Figure 2, AI-use is more
many stories written with AI use rely on authenti-                             frequent in languages other than English. To
cally sourced material. However, it remains unclear                            better understand if this is due to Pangram pick-
whether journalists are choosing these quotes and                              ing up on texts that were automatically translated
feeding them into a prompt for AI generation, or                               into other languages from English or written in-
if the AI is also doing quote selection (see Table 3                           part or fully using AI, we take a sample of 300
for examples).                                                                 English detects with the following distribution:
                                                                               100 H UMAN - WRITTEN , 100 M IXED , and 100
Effects of republishing articles. We examine                                    AI-G ENERATED . The articles are translated us-
how AI-generated content propagates via redistri-                              ing GPT4.1 (OpenAI, 2024) in chunks of 2000
bution. Using recent_news, we cluster articles                                 tokens. The translation prompt is displayed in Fig-
by cosine similarity and define exact duplicates                               ure 17. If the article is less than 2000 tokens, the
for scores ≥ 0.95 and semantically similar for                                 whole article is translated at once. If it is longer,
0.85 ≤ score < 0.95. In total, 16 580 articles                                 the article is chunked into chunks of 2000 tokens
meet these criteria, forming 6413 clusters (mean                               or less, respecting paragraph boundaries, and then
Figure 14: Heatmap of AI use by publication owner and article topic in recent_news. Some owners disclose AI
use for specific content, such as Advance Publications for weather reports, but the biggest adopters, such as Boone
Newsmedia, use AI broadly across many topics. Note that only 87% of recent_news has ownership information,
and only topics that have at least 5 articles per owner are visualized in the heatmap.


                                                           translated. We translate the articles into the 12
                                                           languages: Arabic, Chinese (Simplified), Dutch,
                                                           French, German, Italian, Japanese, Polish, Por-
                                                           tuguese, Russian, Spanish, and Vietnamese. Af-
                                                           ter translation, we find the average AI-likelihood
                                                           decreases by an average of 0.13, with Japanese hav-
                                                           ing the smallest decrease of 0.08 (Table 10). We
                                                           see that agreement using Pangram is high but im-
                                                           perfect, ranging between 74.7% (Vietnamese) to
                                                           88.7% (Portuguese). All languages have a McNe-
Figure 15:     Distribution of AI Categories in            mar P lower than 0.01 except Japanese, indicating
recent_news articles between papers with circulations      that translation suppresses some AI-use. We note
below 100k (left) and above 100k (right).                  that this experiment uses a single MT model (GPT-
                                                           4.1); results may differ with other translation meth-
                                                           ods or models, and the effects of human translation
                                                           on AI detection remain an open question.

                                                           Topic-level variation is unlikely to be driven by
                                                           detector bias alone. One concern is that the un-
                                                           even distribution of AI labels across topics could
                                                           reflect differences in detector performance rather
                                                           than differences in AI adoption. We use opinions
                                                           to test whether topic-level uniformity differs in
                                                           2022, before widespread LLM-assisted writing,
Figure 16: Distribution of duplicate-cluster sizes in      versus 2025. If detector bias were the main driver
recent_news. Most clusters are small, with a minority      of topic-level differences, we would expect to ob-
of large clusters driving redistribution volume.           serve similar topic variance in both years. In 2022,
                                                           across 4,344 articles, only 5 were flagged (0.12%).
                  Language           ∆ AI Likelihood   Binary Match (%)   FP   FN   McNemar p
                  Arabic                 −0.12               82.0         11   43     < 0.001
                  Chinese (Simpl.)       −0.12               82.0         14   37      0.002
                  Dutch                  −0.17               82.0          4   50     < 0.001
                  French                 −0.11               83.0          9   35     < 0.001
                  German                 −0.16               82.3          5   48     < 0.001
                  Italian                −0.13               83.3         4    36     < 0.001
                  Japanese               −0.08               82.3         28   25       0.78
                  Polish                 −0.19               82.0          9   49     < 0.001
                  Portuguese             −0.10               88.7          7   27      0.001
                  Russian                −0.14               82.3          6   45     < 0.001
                  Spanish                −0.09               88.0          4   32     < 0.001
                  Vietnamese             −0.21               74.7         10   66     < 0.001
                  Mean                   −0.13               83.2

Table 10: Binary effects of machine translation on AI-use detection. ∆ AI likelihood denotes the mean change in
predicted AI likelihood (translated minus English). Binary match reports agreement with English labels under a
human vs. AI-use formulation. FP and FN denote false positives and false negatives relative to English. McNemar’s
exact test evaluates directional asymmetry in disagreements (FDR-corrected).


   Prompt for translating langauge of articles             as AI-G ENERATED and 0.85% is M IXED as
                                                           shown in Figure 18. The distribution of AI like-
   Translate the following English text to {               lihoods per each of the three labels is shown in
    TARGET LANGUAGE}.                                      Figure 19.
   Preserve the original meaning, tone, and
    style as much as possible.
   Only return the translated text, without
    any explanations or additional comments.

   Text to translate:
   {TEXT}



Figure 17: Prompt for translating articles to other lan-
guages


A permutation chi-squared test with 10,000 sam-
ples yielded a non-significant result (p = 0.1101),
indicating no significant topic-level divergence.          Figure 18: Distribution of AI Use predictions in
In 2025, across 7,932 articles, 267 were flagged           opinions.
(3.37%). The same permutation chi-squared test
was significant (p = 0.0002), showing strong topic-
level divergence. We use a permutation chi-squared         D.3      ai_reporters
test because expected flagged counts in most topics        In section §C, we talk about the aggregated trends
are near zero in 2022, violating the large-sample          for the 10 reporters identified as using AI in our
assumptions of the standard asymptotic test. Taken         data set, whose data we analyzed longitudinally.
together, topic uniformity in 2022 and topic diver-        Here we present more details about the reporters,
gence in 2025 support the interpretation that the          label distribution, and patterns observed in individ-
detector is capturing real differential AI adoption        ual reporters.
across topics rather than fixed topic-specific detec-
tor artifacts.                                             Reporter Profile. Figure 8 shows reporter statis-
                                                           tics. We have anonymized the data, as we want to
D.2   opinions                                             show only the diversity of expertise the reporters in
Overall AI usage in opinions. opinions has                 ai_reporters have rather than highlight specific
99% H UMAN - WRITTEN articles, with a total                reporters. Nine out of ten reporters in this data had
of 1% having AI Use.      0.11% is detected                at least 10 years of experience.
                                                                 Outlet               Opinions (AI+mixed)                         recent_news (AI+mixed)   Ratio
                                                                 WSJ                                   4.99%                              0.74%             6.8×
                                                                 WaPo                                  5.51%                              0.55%            10.1×
                                                                 NYT                                   2.94%                              1.80%             1.6×
                                                                 Pooled                               4.56%                               0.71%             6.4×

                                                            Table 11: Opinion vs. recent_news AI rates, 2025-06-01–2025-09-15.




     Figure 19: Distribution of AI Likelihoods per each AI
     Use category in opinions.
                                                                                                                                    Figure 21: Distribution of AI Use predictions in
                                                                                                                                    ai_reporters.
                            Article label distribution per year (counts)
                     3500                                                                                                Label
                                                                                                           2              HUMAN
                                                                                                      08
                     3000                                                                      4   33                     MIXED
                                                                                           28                             AI
                                                                                       653
Number of articles




                                                                                      2
                     2500                                                                                            6
                                                                                                               219
                     2000
                                                                         9
                                                                      162 1546 1556
                     1500                                      1 9
                                                            119 120
                     1000
                                                      753
                     500                        550
                                     1
                               291 32 217
                            94
                       0
                       11
                             12
                                  13
                                       14
                                            15
                                                  16
                                                        17
                                                              18
                                                                   19
                                                                        20
                                                                             21
                                                                                  22
                                                                                          23
                                                                                                24
                                                                                                       25
                      20
                            20
                                 20
                                      20
                                           20
                                                20
                                                      20
                                                            20
                                                                 20
                                                                       20
                                                                            20
                                                                                 20
                                                                                          20
                                                                                               20
                                                                                                     20




                                                               Year

     Figure 20: Distribution of AI use predictions in
     ai_reporters by year.                                                                                                          Figure 22: Distribution of AI Likelihoods per each AI
                                                                                                                                    Use category in ai_reporters.

    Label       distribution     in     ai_reporters.
    ai_reporters has 86.6% H UMAN - WRITTEN                                                                                         ery reporter. We did, however, ensure we gathered
    articles, with a total of 13.3% having AI Use.                                                                                  most of their recent articles and as many as possible
    10.7% is detected as AI-G ENERATED and                                                                                          from before November 2022 (the ChatGPT release
    2.6% is M IXED as shown in Figure 21. The                                                                                       date).
    distribution of AI likelihoods per each of the three
    labels is shown in Figure 22. More importantly, all
     AI-G ENERATED labels and almost all M IXED
    are concentrated in the last three years (i.e.,
    2023–2025; see Figure 20)

    AI use by reporter. We report AI use by reporter
    in Figure 23 and Figure 24. We note a limitation in
    our data collection: reporters often write for mul-
    tiple outlets, and accessing historical articles from
    some of these sources is difficult. Consequently,
    we could not retrieve all possible articles for ev-
Publication   Label            Author role                      Title
U.S. Politics & Governance
WaPo          AI-G ENERATED    Political writer and former con- MAGA Maoism is spreading through the populist right.
                               gressional speechwriter
WaPo          M IXED           Former U.S. Senator                My fellow Republicans, the responsibility to speak out
                                                                  rests with you.
WaPo          M IXED           Urban warfare scholar              As the border wall goes up, the underground threat will
                                                                  grow.
WSJ           M IXED           Legal activist and think tank fel- The Gates Foundation Put Its Tax Exemption at Risk.
                               low
Public Health
NYT           M IXED           Immunologist                  America Is Abandoning One of the Greatest Medical
                                                             Breakthroughs.
WSJ           M IXED           Health-longevity      company A Chatbot Can Be Part of Your Medical Team.
                               founder
WSJ           AI-G ENERATED    Physician, Fox News commen- The Madness in RFK Jr.’s Autism Method
                               tator
War & National Security
WSJ           AI-G ENERATED    Former Canadian international Canada Is the Best Friend America’s Got.
                               trade minister
NYT           AI-G ENERATED    Retired U.S. Army general     Be Not Afraid.
WaPo          M IXED           Space research CEO            Nuclear-powered rockets will win the new space race.

Cybersecurity
WaPo          M IXED           U.S. Representative & CEO of Cyber warfare has arrived. Here’s the United States’ best
                               TFG Asset Management         defense.
WaPo       M IXED              AI data-center CEO               AI extremists are peddling science fiction.
NYT        M IXED              Principal Product Manager        Ye and the Limits of Free Speech
Technology
WSJ           M IXED           Former Intel CEO                 A Sovereign-Wealth Fund to Keep America’s
                                                                Technological Edge;
NYT         M IXED             Therapist                        I’m a Therapist. ChatGPT Is Eerily Effective.
WSJ         M IXED             Investment firm founder          The AI Boom May Be Too Good to Be True.
Law & Justice
NYT           AI-G ENERATED    Journalist, ex–Navy SEAL       What the ‘Rust’ Shooting Case Is Really About.
WSJ           AI-G ENERATED    Governor and sociology profes- Utah Hands Parents the Keys to the App Store.
                               sor

Table 12: A sample of op-eds labeled as either M IXED or AI-G ENERATED from WSJ, WaPo, and NYT. Author
names are omitted and replaced with professional roles. These op-eds often address polarizing topics such as
politics, war, and public health, making the disclosure of AI imperative. All examples included produced the same
labels on Pangram v2 and v3.2.
 R EPORTER     Y EARS ACTIVE     AI USE IN 2025 (%)     T OPIC COVERAGE
   1           25+ years         90.1%519/576           National politics, civil rights, racial justice, Black affairs
   2           20+ years         84.6%11/13             Regional news, agriculture, water policy, environment
   3           10+ years         78.3%90/115            Caribbean-American news, culture, health, diaspora
   4           40+ years         72.7%8/11              Opinion on policy, education, creativity, technology
   5           20+ years         38.1%48/126            Local news, public safety, city government, environment
   6           30+ years         30.4%157/517           Environmental justice, racial equity, misinformation (opinion)
   7           50+ years         11.7%19/162            Hyper-local news, history, community affairs
   8           10+ years         6.9%27/393             LGBTQ+ news, politics, legal issues, culture
   9           <5 years          3.3%5/153              Business, Black entrepreneurship, economic development
   10          ~10 years         2.3%3/130              Local sports, high school athletics, youth leagues

Table 13: Reporter Profiles: Years active, aggregate AI use in 2025 (%ai_f lag/total ), and topic coverage. Reporters
are arranged from most to least prolific AI user.
        (a) Reporter   1                                                (b) Reporter   2




        (c) Reporter   3                                                (d) Reporter   4




        (e) Reporter   5                                                (f) Reporter   6

Figure 23: AI content patterns in 2025 by reporters (part 1). See Table 13 for profile alignment.
        (a) Reporter   7                                                (b) Reporter   8




        (c) Reporter   9                                               (d) Reporter    10

Figure 24: AI content patterns in 2025 by reporters (part 2). See Table 13 for profile alignment.
