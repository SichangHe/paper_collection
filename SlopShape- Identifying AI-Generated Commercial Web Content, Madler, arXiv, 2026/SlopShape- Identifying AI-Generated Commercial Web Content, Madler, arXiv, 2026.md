                                                SlopShape: Identifying AI-Generated Commercial Web Content


                                                                                      Jochen Madler
                                                                                          Sitefire
                                                                                  jochen@sitefire.ai




                                                               Abstract                         page’s visibility in AI search answers by up to 40
                                             Word-level detectors identify unedited AI-
                                                                                                percent, while traditional tactics like keyword stuff-
arXiv:2609.15369v3 [cs.CL] 28 Sep 2026




                                             generated text almost perfectly, but the liter-    ing yield little to no improvement (Aggarwal et al.,
                                             ature documents their brittleness under reword-    2024), and AI search engines cite systematically
                                             ing, and a word-level score neither charac-        different pages than traditional rankings while re-
                                             terizes a text nor identifies which AI model       ducing clicks to the sources they summarize (Chen
                                             wrote it. We ask whether AI-generated text         et al., 2025; Khosravi and Yoganarasimhan, 2026).
                                             can be identified one level deeper, from struc-    Section 2 examines the literature in more detail.
                                             tural signatures: how information is presented,
                                                                                                   At the same time, LLM adoption has driven the
                                             in what order, with what evidence, and in
                                             what voice. We replicate StoryScope (Russell       marginal cost of producing content toward zero,
                                             et al., 2026a), which showed such patterns for     and low-quality AI-generated text is now so com-
                                             AI-generated fiction, on commercial content:       mon that it has its own term, “slop” (Shaib et al.,
                                             2,250 pre-ChatGPT human blog posts from 268        2025). Academic studies of professional content
                                             company domains against 11,250 AI mirrors          place the share of LLM-assisted text between 9 and
                                             from five frontier models. A 203-feature in-       24 percent: about 9 percent of US newspaper arti-
                                             strument, applied by an LLM and validated
                                                                                                cles and up to 24 percent of corporate press releases
                                             in a human gold-annotation session (human-
                                             human kappa 0.939, human-model 0.951), de-
                                                                                                (Liang et al., 2025). Industry analyses report even
                                             tects AI posts from its 176 structural features    higher numbers: Graphite (2025; 2026) estimates
                                             alone at 97.0 macro-F1 on held-out companies,      that roughly half of newly published English web
                                             nearly unchanged (96.1) when every AI post is      articles are primarily AI-written, and Ahrefs (2025)
                                             reworded by its own model. The signal char-        finds some AI involvement in about three quarters
                                             acterizes and attributes: AI posts share a tidy,   of newly crawled pages. The share of AI-generated
                                             self-announcing shape, 68.6% are attributed to     text is highest in the commercial web, where pages
                                             the correct source against a 16.7% chance rate,
                                                                                                are most directly coupled to traffic and business
                                             and human posts occupy rare structural con-
                                             figurations. All effects replicate StoryScope’s,   incentives. We therefore study AI-generated text
                                             consistent in direction and at least as large in   where it is most prevalent: commercial web pages,
                                             magnitude. We release pipeline, instrument,        in particular company blog posts.
                                             prompts, code, and aggregate artifacts.               For identifying AI-generated content, word-level
                                                                                                detection works well: on our corpus, a fine-tuned
                                         1   Introduction
                                                                                                encoder distinguishes unedited AI-generated posts
                                         In commercial search engines like Google or Bing,      from human writing almost perfectly at near-zero
                                         text carries direct economic value: whether a web      cost (Section 5). Word-level detection has one
                                         page ranks in the top results is directly tied to      weakness, however. Changing words is easy, many
                                         brand visibility and web traffic. With the rise of     free tools automate it, and every word-level detec-
                                         AI search engines like ChatGPT and Google AI           tor family has a documented failure mode under
                                         Mode, web pages are no longer subject to a search      such adversarial rewording (Krishna et al., 2023;
                                         engine’s algorithm alone, but are also assessed by     Weber-Wulff et al., 2023). A commercial ecosys-
                                         an LLM. This additional step has changed the rules     tem of “humanizer” tools has industrialized exactly
                                         of Search Engine Optimization (SEO) and sparked        this attack (Masrour et al., 2025). So we look one
                                         a successor practice, Generative Engine Optimiza-      level deeper, for patterns that are much harder to
                                         tion (GEO): editing web page content can lift a        rewrite. We test this directly: rewording every
AI post in the test split leaves structural detection         strument is an 11-dimension commercial tem-
nearly unchanged (Section 5.4).                               plate schema discovered bottom-up from hu-
   Because word-level detection of reworded AI-               man posts, carrying 203 validated features
generated text is unreliable, policies of platforms           (Section 4). Because the pipeline is LLM-run
like Google have adapted. Google’s policy on                  end to end, we audit it: repeatability runs, a re-
scaled content abuse targets outcomes rather than             liability filter applied before any human/AI la-
methods, sanctioning mass-produced pages “gen-                bels were seen, and a human gold-annotation
erated for the primary purpose of manipulating                session that exceeds the original’s agreement
search rankings and not helping users” whether                numbers (Section 7).
“automation, humans or a combination are involved”
(Google, 2024). And instead of words, YouTube               • Attribution and characterization. The
uses structural signals like account coordination,            shape identifies its author: 68.6 percent of
upload pacing, and templated narrative patterns               posts are attributed to the correct one of the
(Mathur et al., 2026).                                        six sources, against a 16.7 percent chance rate.
   In this paper, we focus on these structural pat-           The shape is also shared: all five AI mod-
terns the platforms observe, and ask whether AI-              els crowd into the same common structural
generated commercial content has a structure, too.            configurations, while human posts occupy dis-
And if it does, what that structure looks like: which         proportionately rare ones (Sections 5-6).
points AI-generated text makes, in what order, with         • Detection performance, via replication.
what evidence, and in what voice - independent of             Structural features alone detect AI-generated
the words being used.                                         commercial blog posts at 97.0 macro-F1 on
   This question has already been answered once,              held-out data from companies never seen in
for fiction. StoryScope (Russell et al., 2026a)               training, consistent with the original study and
showed that AI-generated fiction can be told apart            larger in magnitude (Section 5). The signal
from human fiction by narrative structure alone               is nearly unchanged when every AI post is
(93.2 macro-F1 without stylistic signals), with hu-           reworded by its own model (Section 5.4).
mans occupying statistically rarer regions of nar-
rative space. But fiction is not where AI adoption          • A verifiable release. Our data acquisition
and economic incentives concentrate. We there-                pipeline, the full instrument, all prompts, code,
fore carry their question, alongside the validated            and the aggregate artifacts behind every ex-
pipeline and methodology, to a domain where text              hibit are public, with post-level data available
is tied to revenue: commercial blog content. Our              to researchers on request.
claims are focused on detection of single-pass AI-
generated blog posts from the five studied AI mod-
                                                        2    Related Work
els, both as generated and after rewording (Section
9).                                                     AI search and the economics of AI-generated
   Figure 1a gives an overview of the study design,     content. AI search engines answer user prompts
and Figure 1b previews the central result. The core     with LLM-generated text grounded on retrieved
methodology of the original paper is held fixed: the    web pages. Aggarwal et al. (2024) define the term
same five-stage pipeline (templates, cross-source       GEO and show that modifying web page content
comparison, feature discovery, deduplication, fea-      can lift visibility in AI answers by up to 40 percent
ture application), the same five AI models, the same    while traditional keyword stuffing does not. AI
classifier protocol and metrics. Our methodology        search engines cite systematically different sources
is adapted where the domain demands it, and each        than classic rankings, with top-5 overlap of only 15-
adaptation is declared in a deviation register (Sec-    33% (Chen et al., 2025), and getting cited correctly
tion 4.9). Our contributions are:                       has itself become an optimization target (Tian et al.,
                                                        2026). On the user side, AI-generated summaries
   • The shape of AI-generated commercial               reduce clicks on the pages they cite: exposure to
     writing, and a validated instrument that           Google’s AI Overviews reduced traffic to certain
     reveals it. AI-generated posts share a mea-        Wikipedia articles by about 15 percent (Khosravi
     surable structural signature, and nine features    and Yoganarasimhan, 2026). On the producer side,
     carry most of the signal (Section 6). The in-
       Human corpus                                                      Brief mirroring                           Templates                    Feature discovery                     Scoring
      2,250 posts, 268 domains                                       reverse-engineered briefs             11-dim commercial schema (fixed)      3 runs, 457 candidates           148,500 LLM answers
     pre-2023 archive snapshots                                     5 AI models, 11,250 mirrors                   13,500 extractions             screen 282, dedup 266        alpha 0.89, gold kappa 0.94+




      Instrument floor                                                  Encoding + splits                        Classification                  Rewording test                Validation checks
      outcome-blind exclusions                                      840 columns, domain-disjoint             XGBoost variants, SHAP core        each AI post rewritten by     robustness + validity checks
          203 features final                                         manifest fixed pre-training               headline macro-F1 97.0            its own model, F1 holds             all complete




                                                                                                                         (a)
                                                                                       Human posts occupy the rare regions of structural space
                                                                                0.83                0.33             0.49             0.46         0.54              0.36
                                                                 1.00
                                  Structural rarity percentile




                                                                 0.75


                                                                 0.50


                                                                 0.25


                                                                 0.00
                                                                               Human               GPT-5.4        Claude 4.6        Gemini 3   DeepSeek 3.2        Kimi 2.5

                                                                                                                         (b)

Figure 1. (a) Study pipeline, from corpus construction through template extraction, feature discovery, and scoring
to classification, the rewording test, and validation. (b) The central result previewed: structural rarity percentile by
source. Human posts concentrate in the rarest structural configurations (mean 0.83 vs pooled AI 0.44, Cohen’s d =
1.80), while the five AI models crowd the common ones. Section 6 develops this result.


AI search measurably shifts what content commu-                                                                                weakness is rewording, which is easy and widely
nities publish (Zhang et al., 2026).                                                                                           automated. All four families have documented fail-
   Adoption measurement. Academic studies al-                                                                                  ure modes under adversarial rewording (Sadasivan
ready find a sizeable share of AI-generated text in                                                                            et al., 2023). Likelihood-based zero-shot detectors
professional writing: about 9 percent of new US                                                                                collapse under paraphrasing: DetectGPT falls from
newspaper articles (Russell et al., 2026b), up to 24                                                                           70.3 percent to 4.6 percent detection at 1 percent
percent of corporate press releases (Liang et al.,                                                                             false positives (Krishna et al., 2023). Trained classi-
2025), and more than 5 percent of new English                                                                                  fiers degrade on unseen models, domains, and edits,
Wikipedia articles (Brooks et al., 2024). At web                                                                               with accuracy on AI-paraphrased text as low as 26
scale, a large share of multi-language page transla-                                                                           percent (Weber-Wulff et al., 2023). Lexical-tell
tions is already mass machine translation, skewed                                                                              estimators are defeated by avoiding the tell words
toward low-quality SEO content (Thompson et al.,                                                                               (Kobak et al., 2025). Provider-side watermarks like
2024). Industry measurements report even higher                                                                                the one Anthropic introduced in August 2026 sur-
shares (Section 1).                                                                                                            vive light editing but not a complete rewording, by
   AI-text detection. Word-level detectors are the                                                                             Anthropic’s own account (Anthropic, 2026). The
first choice for AI-text detection, and on unedited                                                                            rewording attacks are heterogeneous and hard to
text they are close to perfect. They span fine-tuned                                                                           anticipate (Dugan et al., 2024), and there is a com-
encoders (ModernBERT; Warner et al., 2024), sty-                                                                               mercial tool ecosystem that exploits them (Mas-
lometric classifiers, TF-IDF baselines, and zero-                                                                              rour et al., 2025; Perkins et al., 2024). The most
shot likelihood methods (DetectGPT, Mitchell                                                                                   rewriting-robust result comes from the study this
et al., 2023; Binoculars, Hans et al., 2024). Their                                                                            paper replicates: StoryScope’s narrative features
lost only 1.6 F1 under span-level style rewriting, us-   feature discovery (Section 4.3) and excluded from
ing the editing protocol of Chakrabarty et al. (2025).   all classifier splits. We call its 600 posts the feature-
We reproduce their word-level baseline suite on our      discovery set. The remaining 2,150 prompts form
data (Section 5) and run their rewording test on         the classification corpus, split 198/32/38 by com-
commercial text (Section 5.4).                           pany domain into train/val/test (Section 4.7).
   Structural analysis of AI writing, with LLMs             The corpus spans seven industry verticals from
as annotators. StoryScope (Russell et al., 2026a)        software/SaaS (26.5%) to edtech (0.6%), with the
built on the NarraBench taxonomy of narrative            full composition by vertical, source frame, and
dimensions (Hamilton et al., 2025) to measure            snapshot year in Appendix A (Table A1). Because
discourse-level differences between human and AI         we collected as much data as possible from just
fiction, and found structural detectability, model-      before ChatGPT’s release, the corpus skews recent:
specific patterns, and a rarity gap. LLM-prose id-       75.5% of post snapshots are from 2020-2022. We
iosyncrasies have also been formalized from the          address this with a publication-year check (Ap-
editing side (the LAMP taxonomy; Chakrabarty             pendix G) and disclose it as a limitation (Section
et al., 2025) and the judging side (Shaib et al.,        9).
2025). This paper is a domain-transfer replica-             Following the original study’s reverse-
tion of StoryScope, and every deviation from the         engineering design, a content brief is inferred
original is disclosed in a register (Section 4.9). Our   from each human post. Like the original’s brief
pipeline uses LLMs for screening, template extrac-       prompt, which asks for key characters or settings
tion, feature discovery, and scoring. We follow the      by name, ours names the publishing company and
original paper’s gold-annotation protocol and ex-        what it sells, so the publisher commissions the post
tend it with a reliability filter that never uses the    rather than being its subject; where a post does not
human/AI labels (Section 4.5) and a human gold-          name its publisher, the brief says “the publisher”.
annotation session (Section 7).                          Analysis-only labels, such as the post’s commercial
                                                         goal, are never passed to the writer. Each brief is
3   Data                                                 then given to the original’s five AI models: gpt-5.4,
Our human writing corpus comprises 2,250 human           claude-sonnet-4.6, gemini-3-flash, deepseek-v3.2,
commercial blog posts from 268 company domains,          and kimi-k2.5, yielding 11,250 AI-generated
captured in pre-ChatGPT Wayback Machine snap-            mirror blog posts. Together, the human posts
shots dated between 2008 and 2022. The posts             and their mirrors form a paired corpus: for every
come from company websites that sell to other            human post there are five AI-generated versions
businesses (B2B) and for which organic search is         written from the same brief. AI mirrors turn out to
a plausible acquisition channel. Table 1 describes       be slightly longer than their human counterparts
the collection pipeline: we assembled a sampling         (per-model means of 1,064 to 1,541 words, length
frame from four public company lists, screened           statistics in Appendix A). To rule out effects driven
the companies for fit, kept domains with enough          by post length, we ran a length check (Appendix
articles archived before ChatGPT’s release, spot-        G) as well as a length-only classifier: given only
checked their genre, applied industry quotas, and        word count, it cannot separate the classes (Section
fetched the qualifying articles through the content      5).
filters (600-2,500 words, English, informational            In the template-extraction, feature-discovery,
genre, near-duplicate removal). Of the 306 selected      and scoring prompts, the web page identity is
domains, 264 yielded usable posts (40 had no fetch-      anonymized. Schema discovery, the stage that de-
able qualifying articles, 2 were emptied by the con-     rives the 11 description dimensions (Section 4.1),
tent filters), and 4 replacement domains drawn from      saw only human posts. Feature discovery, the stage
the same qualification pool during the fetch gave        that derived the 457 candidate features within those
the 268 corpus domains (see Appendix A). Follow-         11 dimensions, saw posts from all six sources with-
ing the original study’s terminology, we define a        out knowing which was which. Nevertheless, a
“prompt” as one human blog post together with its        human post could be recognized for a trivial rea-
brief and the five AI-generated mirror posts derived     son: it might be part of an AI model’s training data.
from it. A seeded, stratified set of 100 prompts,        To rule this out, we ran a memorization check using
spanning 82 of the 268 domains, is set aside for         the 13-gram overlap rule of Brown et al. (2020): if
                                                         a human post and its mirror share even one iden-
    Step                             Rule                                                              Count
    1. Assemble the sampling         Sampling frame assembled from four archived public company        15,075 domains
    frame                            lists: Inc5000 9,979; YC directory 3,448; FT1000 1,129; G2 519
                                     (with an anti-persona prefilter)
    2. Company-fit screen            2 LLM judges assess the company fit from firmographics and        94.3% keep
                                     homepage metadata
    3. Archive-volume check          At least 25 article URLs archived before 2022-11-30 in the        698 qualified
                                     Wayback Machine’s snapshot index
    4. Genre spot-check              5 posts/domain checked for English language, informational        307 keep-eligible
                                     type, and web page length
    5. Industry quotas               Company industry quotas applied (software cap 40%)                306 domains
    6. Fetch and filter              Content filters: 600-2,500 words, English, informational genre,   2,250 posts from
                                     near-duplicate removal                                            268 domains

Table 1 - Data collection pipeline


tical 13-word sequence, the pair is flagged as po-              4.2    Template extraction
tentially contaminated. Only 0.19% of pairs were                For each of the 13,500 posts - the 2,250 human
flagged (against 0.0% for a shuffled-human con-                 posts and their 11,250 AI mirrors, six posts per
trol), no pair was near-verbatim, and excluding all             prompt - we extracted one JSON template that de-
flagged prompts leaves the headline unchanged in                scribes the post along all 11 dimensions of the
substance (97.2). As a final check, we scanned all              schema.
posts for mentions of entities that did not yet exist
at the post’s claimed publication date. Only 0.08%              4.3    Comparison, feature discovery, quality
of posts contain such a mention, and excluding                         gate, deduplication
them leaves the headline numbers unchanged.                     Using the extracted templates, we ran the origi-
                                                                nal study’s cross-source comparison stage over the
4     Measuring Structure
                                                                feature-discovery set: the 100 prompts (600 posts)
The measurement pipeline follows the original’s                 set aside for this purpose and excluded from all clas-
five stages, preceded by one new schema-discovery               sifier training and testing, so that features are never
step. Figure 1a gives the overview.                             discovered on the same posts they are later eval-
                                                                uated on. The feature-discovery set shares some
4.1     Commercial template schema                              company domains with the test split, and a dedi-
Since the original’s template schema is fiction-                cated check covers this overlap (Appendix G). For
shaped (plot, characters, emotion trajectories), we             each of the 100 prompts, gpt-5.6-terra received all
derived a similar schema for commercial content                 six templates - the human post’s and its five AI
bottom-up: three independent runs of the same                   mirrors’ - side by side and noted where the sources
LLM (gpt-5.6-terra) each examined 18 stratified                 diverge. Three independent LLM discovery runs,
human posts and converged on near-identical di-                 each with one specialized prompt per dimension,
mension systems. The consolidated result is a new               then turned these divergence notes into 457 fea-
11-dimension schema: purpose, audience, struc-                  tures, versus the original’s 408. We then applied
ture and flow, explanation, evidence, voices, action-           a quality gate to score each feature on whether it
ability, commercial integration, timeliness, page               can be answered from the text alone, with locatable
format, and writing style. We kept a dedicated                  evidence, in self-explanatory wording, and without
Writing-Style dimension so that style is measured               compound constructs. The gate rejected 38.3% of
on its own and can be excluded. Every structural                candidates (see Appendix C), leaving us with 282
result in this paper is computed with these writing             features. Finally, we removed duplicate features by
style features stripped out, which is what lets us              clustering their embeddings (F2LLM-4B, single-
attribute the detection signal to structure rather than         linkage clustering at cosine 0.85) and keeping only
wording. In Appendix B, we map the NarraBench                   one feature per cluster, which left 266 features. In
fiction dimensions to our commercial ones.                      this embedding step, only 5.7% of our features
                                                                were merged versus the original’s 25.5%, possibly
                                                                because of our quality gate. We include a sweep on
                                                                the deduplication cutoff threshold that shows the
results do not depend on this difference (Appendix        rule was fixed before the samples were scored. It
G).                                                       excluded 11 structural features and no style feature,
                                                          all tied to titles, headings, or lists: where the pay-
4.4   Feature application                                 off and the problem first appear, brand in the title,
To turn features into measurements, every blog post       author identity treatment, heading depth, density,
is scored against every feature. We used gemini-          and workflow, bulleted and numbered lists, num-
3.6-flash, one dimension per call, with the model         bered steps, and numbered main sections. The final
forced to pick exactly one answer from each fea-          instrument therefore has 203 features (versus the
ture’s predefined options. Human posts are scored         original’s 304): 176 structural ones (the original’s
as extracted from the archived pages and normal-          “narrative-strict” analogue) and 27 style. Appendix
ized to plain text, which keeps the page title for        C (Table C1) gives the composition by dimension
some posts and drops it for others. AI posts are          and answer type.
scored as the models produced them: each opens
with a title line, and most carry markdown format-        4.6   Feature space, variants, encoding
ting such as headings, bold text, or lists. Section       Our encoding follows the original paper’s method-
4.5 removes the features that respond to this differ-     ology: one-hot for nominal and binary types, multi-
ence. Before committing to the full corpus, we ran        hot for multi-select, integer position encoding for
two checks on a small sample. First, scoring one          ordinal and scale, NaN for missing (native to XG-
dimension at a time answered 99.97% of items, ver-        Boost; Chen and Guestrin, 2016). The result is a
sus 99.75% for scoring the whole post in a single         matrix of 12,900 posts x 840 columns: each of the
call. Small as the difference is, we kept the per-        2,150 classification prompts contributes six posts,
dimension mode (Appendix C). Second, we scored            and 600 posts from the initial feature-discovery set
60 of the posts five times, and agreement across the      are excluded. As in the original, we train classi-
runs reached a Krippendorff alpha of 0.889 against        fiers on subsets of the instrument: 176 structural
our 0.8 bar (Section 7). We then scored all 13,500        features only, style features only (27), all features
posts against the 266 features. This took 148,500         (203), the nine core features (Section 6), and the
scoring calls (13,500 posts x 11 dimensions).             nine core features plus model-specific features (30
                                                          in total, Section 6).
4.5   Feature reliability filter
An LLM judge can produce unreliable answers:              4.7   Experimental protocol
features whose answer values barely vary, that drift      Before training any classifier, we split the corpus
outside the predefined options, or that randomly          by company domain: 1,566 / 294 / 290 prompts
change from run to run. To remove such features           (198/32/38 domains), so no domain appears in
from further analysis, we ran a reliability filter that   more than one split. This is stricter than the orig-
judges a feature by its result statistics. It excluded    inal’s random prompt split (deviation D6) and
52 features: 11 were degenerate (at least 98% of          prevents a company’s tone of voice from leaking
posts received the same answer), 3 produced an-           across splits. Per the original’s protocol, we grid-
swers outside their predefined options too often          searched hyperparameters on the validation split
(above 2%), and 38 were unstable across the five          and trained the final models on training and vali-
repeat scoring runs.                                      dation data combined (see Appendix D). Our re-
   Because human and AI posts reach the scorer in         sults are, unless stated otherwise, measured only
different formats (Section 4.4), a second filter re-      on the held-out test split: macro-F1 and AUPRC
moves features that answer to the format rather than      for the human-vs-AI task (Section 5.1 explains this
to the post. We rescored three samples from the           choice), and macro-F1 and accuracy for source
training and validation splits with only the format       identification, the task of predicting whether a post
changed: 250 AI posts normalized like the human           was written by a human or, if not, which of the
posts (markdown stripped, title kept as a plain first     five AI models wrote it. Confidence intervals come
line), the same posts without the title line, and 250     from 10,000 bootstrap resamples. Because posts
human posts with their page title added. A fea-           from the same company resemble each other, the
ture is excluded if its answer distribution moves by      primary intervals resample whole company do-
more than twice its run-to-run noise plus 0.05 (total     mains rather than individual prompts.
variation distance) in any of the three samples; the         Hypotheses. We test three hypotheses. The first:
style features outperform structural features, the       written blog posts, and how close they come to the
opposite of the original study’s finding. The ratio-     word-level baselines. Table 3 reports classifiers
nale: commercial writing is persuasion in a brand        trained on each subset of our instrument as well as
voice, so style could plausibly carry more of the        the word-level baselines from the original study, all
signal than it does in fiction. Our data rejects this    evaluated on the same held-out test data.
hypothesis decisively (Section 5.3). The second:            Result: We replicate the original study’s head-
structural detection is robust against rewording, be-    line result at larger magnitude. Structural fea-
cause the features capture what a post says rather       tures alone distinguish AI-generated from human-
than how it formulates it. It holds (Section 5.4).       written commercial blog posts at 97.0 macro-F1.
The third: the gold-annotation session must reach        The ordering of the feature variants replicates,
human-human and human-model agreement of at              too: all features (98.0) above structural only (97.0)
least kappa 0.60. Both bars were cleared at 0.939        above style only (88.1), against the original’s 96.0
and 0.951 (Section 7).                                   > 93.2 > 85.8.
                                                            Word-level detection: the framing of Section 1
4.8    Rewording test                                    holds on this corpus. Unedited single-pass gen-
To test the second hypothesis, every AI post in          eration is near-perfectly detectable at the word
the test split is rewritten by the same AI model         level: the stylometric baseline and ModernBERT
that generated it. The rewriting follows the editing     both reach a perfect score, mirroring the origi-
protocol of Chakrabarty et al. (2025): the model         nal’s 99.9 and 99.8. Part of the stylometric ceil-
edits its own post span by span, targeting the seven     ing comes from formatting rather than wording.
categories of AI-writing artifacts their study identi-   Some human posts are interviews, transcripts, or
fied with professional editors, while keeping every      roundups, formats the AI mirrors almost never pro-
claim, fact, and link. We ensured preservation of        duce. Restricted to the 86.5% of human posts
content after rewording by running a judge on all        that are regular self-contained pages, the structural
1,450 original-rewritten pairs. In the final pairs,      headline remains 96.2. The zero-shot substitute (a
98.2% of blog posts preserve all claims and the          small Qwen2.5-0.5B pair in place of the original’s
rest differ in single details. The rewriting attack is   Falcon-7B Binoculars pair) lands at 78.2 where the
substantial: on average, 73% of a post’s 13-word se-     original’s true Binoculars scored 55.9. Moreover,
quences no longer appear verbatim, and in a seeded       blog post word count by itself cannot separate the
spot check of 20 posts, 16.0% of all feature answers     classes, consistent with the length check (Appendix
change, against 10.9% between two scorings of the        G).
same text (Section 7).                                      As in the original, all feature-based models and
                                                         the stylometric and TF-IDF baselines are trained
4.9    Declared deviations
                                                         on the combined training and validation data. The
Table 2 lists the deviations from the original’s         ModernBERT baseline is an exception: per the
method that most affect how the results should be        original study, we fine-tune it on the training split
read. The full register with all 16 deviations and       alone. Two more baselines, a zero-shot detector
their defenses is in Appendix E.                         substitute and a length-only control, are reported
                                                         in Appendix F, and all values are percentages re-
5     Detection Results                                  ported to one decimal. AUPRC measures ranking
5.1    Binary detection                                  separation rather than thresholded decisions and is
                                                         rounded to three decimals (the structural model’s
We report macro-F1, an accuracy measure balanced
                                                         stored value is 0.9996), so the structural variants’
across two classes: it averages the detection qual-
                                                         remaining test errors are threshold errors, not rank-
ity on human-written and on AI-generated posts
                                                         ing errors. The results are not sensitive to hyperpa-
equally. Naive accuracy would be misleading, be-
                                                         rameter tuning: refitting with the original study’s
cause five of every six posts are AI-generated: a
                                                         published hyperparameters yields only a 0.4 points
detector that answers “AI” for everything already
                                                         difference compared to our tuned configuration on
reaches 83.3% accuracy without catching a single
                                                         both tasks (Appendix D).
human post.
   The first question is how well structural features
alone can distinguish AI-generated from human-
 #       Deviation from the original                                          Defense
 D1      Domain: B2B blog posts                                               The research question
 D6      Domain-disjoint splits, single-unblinding holdout                    Stricter than their random prompt split
 D7      Rarity metric re-implemented from text                               Verified on their data
 D10     Corpus ~1/4.5 of theirs, feature-discovery set 4.4% vs ~1%           Budget, power note in Section 9
 D11     Commercial-native schema discovered from human posts                 Fiction lens misfits the domain
 D13     Evaluation-stage models upgraded within lineage                      The five AI models unchanged
 D14     Rewording test: symmetric self-rewrite by all five models            Removes the original’s single-model
                                                                              asymmetry

Table 2 - Deviation register (condensed to the most consequential rows).

 Variant / baseline                      n feat   Test macro-F1                         AUPRC          Original
 Structural (headline)                     176    97.0 (cluster CI 95.5-98.2, prompt    1.000          93.2 / .959
                                                  CI 95.7-98.1)
 Style-only                                 27    88.1                                  .994           85.8 / .867
 All features (combined)                   203    98.0                                  1.000          96.0 / .982
 Core-only                                   9    90.1                                  .997           30 feat: 84.8 /
                                                                                                       .828
 Core + model-specific                      30    93.7                                  .998           101 feat: 91.1 /
                                                                                                       .934
 ModernBERT-base fine-tune                   -    100.0                                 1.000          99.9 / 1.00
 Stylometric + XGB (144-dim, their         144    100.0                                 1.000          99.8 / .999
 spec)
 TF-IDF (1-2g, their 5,000-feature       5,000    99.3                                  1.000          99.7 / .999
 spec) + XGB

Table 3 - Binary human-vs-AI detection on the held-out test split (macro-F1, original’s Table 2 analogue).


5.2    Distance to the word-level ceiling                      sure two different signals (see Section 8).
The best word-level detectors on this corpus are per-          5.4    Detection survives rewording
fect, but the structural model comes within three
percentage points: 97.0 macro-F1 against their                 The second hypothesis holds. On the test split with
100.0 (the original: 93.2 against near-perfect word-           every AI post replaced by its reworded version, the
level baselines). These word-level detector ceil-              structural classifier scores 96.1 macro-F1, against
ings are measured on unedited text, and there is               97.0 on the original posts (95% CI on the reworded
extensive literature on the brittleness of word-level          split 94.3-97.6). Of 1,450 reworded AI posts, 18
detectors against rewording attacks (Section 2). In            are misclassified as human-written, against 9 of
contrast, our structural feature instrument’s accu-            the same posts before rewording. The result is uni-
racy remains nearly unchanged under rewording                  form across the five AI models (95.3-96.5). Style
attacks (Section 5.4).                                         features, which read how a post is worded, lose
                                                               ground as expected under a wording attack (88.1
5.3    The style-vs-structure direction                        to 87.1), and the combined set changes little (98.0
The first hypothesis (Section 4.7) predicted that              to 97.3). The changed feature answers do not add
style features would beat structural features. The             up to an escape: they are scattered across posts and
data reverses it: the structural model beats the style         features rather than directed toward the structural
model by 8.8 macro-F1 points (95% CI [4.9, 13.2]               profile typical of human posts, and a classifier that
on the primary company-cluster basis, and [6.5,                reads the whole 176-feature signature loses less
11.3] at the prompt level).                                    than a point. The original study observed the same
   Of the 1,740 test posts, the structural model               for its narrative features in fiction, with a 1.6-point
makes 29 errors and the style model 101, and only              drop on a single-model rewording arm. Ours holds
9 posts are misclassified by both. If structural fea-          across all five models. The rewriting protocol and
tures merely re-encoded surface style, the two mod-            verification gates are in Section 4.8 and Appendix
els should fail on the same posts. Instead, their              J.
failure sets are nearly disjoint, which is evidence
that the style features and structural features mea-
        Variant               Original   Reworded                                                 Six-way source attribution (row %)
                                                                            Human            97         1            0             1            1                   0   100
        Structural (176)          97.0         96.1
        Style-only (27)           88.1         87.1
        All features (203)        98.0         97.3                        GPT-5.4           0         82            4             4            1                   8   80


Table 4 - Detection on the original versus reworded test          Claude Sonnet 4.6          5         10           49            12           12                  13   60




                                                                                                                                                                             Row %
                                                           True
split (macro-F1).
                                                                     Gemini 3 Flash          1          2            8            66           11                  12   40

        Class      Ours      Original (without style)               DeepSeek V3.2            1          2           12            14           59                  12   20
        human       .944                         .89
        gpt         .793                         .73                      Kimi K2.5          1         10            8            14            8                  59   0
        gemini      .624                         .60
                                                                                             n       -5.4          4. 6          lash        3. 2                   5
        deepseek    .615                         .57                                       ma                  net                         kV                  K 2.
                                                                                      Hu          GPT                     in i
                                                                                                                               3F
                                                                                                                                        See         K im
                                                                                                                                                           i
        kimi        .579                         .55                                                     e Son          m             ep
                                                                                                       ud            Ge            De
                                                                                                    Cla
        claude      .537                         .77                                                                  Predicted

Table 5 - Per-class F1 for the six-source model (origi-    Figure 2. Row-normalized test confusion of the six-
nal’s Table 11 analogue).                                  source model (accuracy 68.6% vs the 16.7% chance rate,
                                                           macro-F1 68.2). Humans are near-perfectly separated.
                                                           The residual confusion is between AI models, hardest
5.5    Identifying which AI model wrote a post             for Claude Sonnet 4.6.
We also trained a model that identifies each post’s
author among the six sources: the human author
                                                           for 25.6% of the full model’s total feature attribu-
or one of the five AI models. On the test split, it
                                                           tion, and a classifier restricted to them alone still
assigns 68.6% of posts to the correct source (macro-
                                                           tests at 90.1 macro-F1 (the original: 30 features at
F1 68.2, against a 16.7% chance rate), on par with
                                                           84.8). The small-core phenomenon replicates, with
the original’s 68.4%. Table 5 shows the per-class
                                                           a smaller core and a higher accuracy, potentially
scores.
                                                           because of the quality gate in our feature discov-
   Human-written posts are identified almost per-
                                                           ery and because commercial blog posts are more
fectly. The remaining errors are AI posts attributed
                                                           homogeneous than fiction.
to the wrong AI model (Figure 2). Posts by Claude
                                                              Each core value points toward one author class,
Sonnet 4.6 are the hardest to attribute.
                                                           and together the directions form a consistent pat-
6     The Shape of AI Writing                              tern. We interpret only concrete, directly observ-
                                                           able features, within what the validity results of
Figure 3 shows the twenty most important fea-              Section 7 support. The values most commonly pro-
tures, ranked by mean absolute SHAP contribution.          duced by AI models assemble into what we call
SHAP (SHapley Additive exPlanations; Lundberg              the tidy, self-announcing blog post: it states its
and Lee, 2017) assigns each feature its share of           thesis and announces its structure before the first
every prediction the model makes. The most im-             section, presents its subject as the modern answer
portant features describe argument-structure stages,       to a legacy way of working, explains in a confi-
how the reader is addressed, temporal framing, and         dent institutional voice, and closes with a stage that
how sources are disclosed.                                 summarizes or restates the thesis. In a typical AI
   Using the original’s core-selection procedure,          post, the thesis is stated and the flow announced
we then distilled this ranking down to a core: the         before the first section: “In this post, we’ll cover
small set of feature values that carry the signal          why onboarding stalls, three fixes that work, and
most reliably. A value counts as core if it ranks in       how to measure the difference.” The subject is set
the top quartile of SHAP importance, stays impor-          against the old way: “Paper checklists were built
tant when the model is refit 50 times on resampled         for a slower era.” And the close restates the thesis:
data, carries clearly more weight than it would            “In short, structured onboarding saves time.” The
with randomly shuffled labels, and separates hu-           human-leaning values describe posts without those
man from AI answers by a wide margin that is               signposts: no thesis up front, no legacy-versus-
consistent across all five AI models. This yields 10       modern contrast, more references to specific dates
core values on 9 distinct features (the original: 33       and periods, and more short posts. The length-
values on 30 features). These nine features account
                                                    Top-20 structural features separating human from AI posts
               Functional Stage Inventory
                            (STR_STG_001)
                      Conclusion Behavior
                            (STR_STG_008)
           Second-Person Address Density
                           (VOC_ADR_002)
                       Article Length Class
                            (PAG_FUR_011)
            External Participation Pathway
                            (VOC_PRT_005)
              Reader Naming Explicitness
                           (AUD_RDR_001)
                   Thesis Before First Unit
                            (STR_FLW_006)
                Temporal Reference Types
                             (TIM_CUE_003)
             Execution Support Resources
                            (ACT_CHK_025)
                              Effort Framing
                           (ACT_CON_018)
                       Freshness Signaling
                             (TIM_CUE_011)
                      Reader Role Framing
                           (EXP_KNW_004)
                Dominant Credibility Basis
                           (VOC_CRD_001)
           Commercial Solution Placement
                            (PUR_SEC_006)
                    Primary Voice Identity
                           (VOC_VOX_001)
           Legacy-versus-Modern Contrast
                            (STR_FLW_005)
                   Ownership Assignment
                            (EXP_MEC_009)
                      Reader Role Framing
                           (AUD_RDR_009)
            Primary Actor Expected to Act
                             (ACT_STP_008)
                Dominant Definition Form
                             (EXP_DEF_002)

                                           0.00   0.25     0.50      0.75     1.00      1.25     1.50      1.75    2.00
                                                         Mean |SHAP| (50-bootstrap mean, aggregated per feature)

Figure 3. Top-20 features of the structural classifier by mean absolute SHAP contribution across bootstrap refits,
labeled with their plain-language instrument names (feature IDs in parentheses, full question wording in the released
instrument). Dark bars mark the core features (Section 6) that appear among the top 20.


matched check in Section 7 shows the headline                           erence distribution, 146 are human and 2 are AI,
result does not depend on post length.                                  where the original study’s rarest 1% split roughly
   Rarity. Following the original study and the tra-                    evenly (42 vs 41). The gap is equally visible in
dition of Torrance (1966), we measure statistical                       ranking terms: rarity alone separates the classes
rarity as a proxy for originality. Rarity is a per-post                 at AUC 0.898 (original 0.73), and the human post
statistic: for each post, we compute the mean Eu-                       is the rarest of its six-post prompt group in 85.6%
clidean distance to its 25 nearest neighbors in the                     of prompts, against a 16.7% chance rate (original
z-scored structural feature space, and convert it to                    57.8%). Per-model mean rarity orders the AI mod-
a percentile against the pooled train+val distribu-                     els deepseek 0.543 > claude 0.489 > gemini 0.456
tion as reference. A post with a common structure                       > kimi 0.363 > gpt 0.330. DeepSeek sits closest to
sits close to many neighbors and scores low. A                          humans, and the length-matched check (Appendix
post whose structure few others share sits far from                     G) shows this proximity is structural rather than
its neighbors and scores high. We compute these                         length-driven: the per-model ordering is preserved
statistics over all 12,900 posts, and on the origi-                     on the length-matched subset.
nal’s test-only basis the picture is the same (rarest                      The rarity gap also has a geometric reading:
1%: 36 human vs 0 AI, full tail table in Appendix                       human posts are spread out widely in structural
F). Human posts occupy the rarest regions of this                       feature space while AI posts cluster together (Ap-
space and AI posts the densest (Table 7 and Fig-                        pendix F). From the six-source model’s per-class
ure 1b): the mean human rarity percentile is 0.835                      SHAP attributions, we selected 28 model-specific
against 0.436 for AI, a gap of Cohen’s d = 1.80                         features - features whose importance concentrates
(the original: 0.71 vs 0.49, d = 0.83). The con-                        on one source (human 17, gemini 4, gpt 3, deepseek
trast is even sharper in the tail. Among the posts                      2, kimi 2, claude none; the original: 75 features).
whose rarity exceeds the 99th percentile of the ref-                    A classifier on the nine core features plus these 28
       Feature                                         Value                                 Leans   Human-AI gap
       Conclusion Behavior (STR_STG_008)               restated thesis or reframe            AI              0.650
       Functional Stage Inventory (STR_STG_001)        summary or synthesis                  AI              0.609
       External Participation Pathway (VOC_PRT_005)    absent                                AI              0.592
       Legacy-versus-Modern Contrast (STR_FLW_005)     no                                    human           0.497
       Thesis Before First Unit (STR_FLW_006)          no                                    human           0.419
       Freshness Signaling (TIM_CUE_011)               modern or next-generation framing     AI              0.360
       Dominant Credibility Basis (VOC_CRD_001)        confident institutional explanation   AI              0.347
       Functional Stage Inventory (STR_STG_001)        mechanism explanation                 AI              0.285
       Temporal Reference Types (TIM_CUE_003)          historical date or period             human           0.283
       Article Length Class (PAG_FUR_011)              short, under 800 words                human           0.274

Table 6 - All core values, with the class each one points to (original’s Table 15 analogue).


    Statistic                 Ours          Original              The remaining checks close the other declared
 Human mean rarity            0.835         0.71               exposures. Excluding the 0.19% of posts flagged
 percentile                                                    by the memorization check leaves the headline at
 AI mean rarity percentile    0.436         0.49
 Cohen’s d                    1.80          0.83
                                                               97.2, and excluding the 11 company domains that
 Rarity AUC                   0.898         0.73               the feature-discovery set shares with the test split
 Human rarest-of-prompt       85.6%         57.8%              leaves it at 96.5. Varying the deduplication cutoff
 (chance 16.7%)
 Rarest decile share (human   47.3% /       24.7% /            between 0.70 and 0.95 changes the feature count
 / AI)                        3.0%          7.1%               (200 to 282) but not the conclusions. Discovering
                                                               features directly from raw text instead of from tem-
Table 7 - Rarity statistics (all 12,900 posts, percentile      plates yields as many candidates but substantially
reference train+val).                                          different ones (about 23% overlap), so the discov-
                                                               ery pathway shapes which features are found - and
model-specific features (30 distinct features) tests           the template pathway is the one validated end to
at 93.7 macro-F1, and the per-source feature lists             end. Detection strength does not vary significantly
are in Appendix F (Table F3).                                  across industry verticals (p = 0.107, per-vertical
                                                               macro-F1 between 94.8 and 100), consistent with
7      Robustness and Instrument Validity                      the original’s finding of no topic effect. Finally,
                                                               the learning curve reads 95.4, 96.4, 96.4, and 97.0
We ran nine robustness checks, every one under
                                                               at 25, 50, 75, and 100% of the training data (Ap-
the original’s protocol (final models retrained on
                                                               pendix G).
train+val). The rewording test, the tenth robustness
                                                                  Repeatability. We scored the same 60 posts five
result, attacks the input text rather than the pipeline
                                                               independent times with the scoring model. Agree-
and is reported with the detection results (Section
                                                               ment across the five runs is Krippendorff alpha
5.4). Table 8 summarizes them one line each, and
                                                               0.889 (Krippendorff, 2004; our 0.8 bar; original
the full table with complete results and caveats is
                                                               0.90), mean pairwise Cohen kappa 0.888 (Cohen,
Appendix G.
                                                               1960; original 0.89), and pairwise exact agreement
   Two checks target the design confounds declared
                                                               0.891.
in Section 3. On a test subsample in which hu-
                                                                  Human gold validation. To validate that the
man and AI posts are matched on length (1,545
                                                               LLM scorer measures what a careful human reader
posts), detection is unchanged at 96.9 versus 97.0
                                                               would measure, two annotators independently an-
unmatched (the original: 93.2 to 93.2), the rarity
                                                               swered 20 features on 12 posts, scored in the en-
gap survives the matching (d = 1.83), and word
                                                               coded representation on the 19 features that belong
count is nearly uncorrelated with rarity. Structural
                                                               to the final instrument (228 items each). We fixed
features also do not secretly encode when a post
                                                               the acceptance thresholds before annotation began:
was written: predicting a human post’s publica-
                                                               human-human and human-model kappa of at least
tion period from them performs at chance (macro-
                                                               0.60. Table 9 reports the result next to the original’s,
F1 49.1; 187 vs 1,622 posts, where always guess-
                                                               with each kappa computed as Cohen’s kappa on
ing the larger class scores 47.3), and removing the
                                                               the pooled item-level contingency over all scored
most year-associated features leaves the headline
                                                               items. Our human-human kappa is 0.939 against
flat (96.7-97.0).
    #     Check                              One-number result
    1     Length confound                    Headline 96.9 on a length-matched test subsample (vs 97.0 unmatched)
    2     Publication-year check             Predicting a human post’s publication period from structure is at chance
                                             (macro-F1 49.1)
    3     Template-vs-direct discovery       Same candidate yield, only ~23% semantic feature overlap
    4     Deduplication cutoff sweep         200-282 features across cutoffs 0.70-0.95, sensitivity low
    5     Feature-discovery-set domain       Headline 96.5 excluding the 11 overlapping domains
          overlap
    6     Memorization                       0.19% of pairs flagged, filtered headline 97.2
    7     Vertical heterogeneity             No significant variation across verticals (Kruskal-Wallis p = 0.107)
    8     Learning curve                     95.4 / 96.4 / 96.4 / 97.0 at 25 / 50 / 75 / 100% of training data
    9     Format sensitivity                 Rescoring test posts with markdown stripped, title removed, or title added
                                             changes few calls: 249 and 247 of 250 AI posts still detected, 15 vs 18 of
                                             235 human posts called AI

Table 8 - Robustness check summary (full versions in Appendix G).


    Comparison        Agreement    Kappa    Original         no narrative arc, yet the structural signature trans-
    Human-human       94.20%       0.939    76.85% /         fers. Detection performance shows the shape is a
                                            0.739            real signal and not an artifact of our instrument:
    Annotator A vs    95.09%       0.9482   91.67% /
    model                                   0.9056
                                                             structural features alone reach 97.0 macro-F1, and
    Annotator B vs    95.54%       0.9529   79.86% /         every phenomenon of the original study replicates
    model                                   0.7724           in the new domain, consistent in direction and at
    Mean              -            0.951    0.839
    human-model                                              least as large in magnitude.
                                                                The core feature values in Table 6 spell out a
Table 9 - Human gold validation (original’s Table 7,         shape that we call the tidy, self-announcing blog
encoded basis, kappas computed as Cohen’s kappa on           post. AI-generated blog posts state their thesis be-
the pooled item-level contingency).                          fore the first section, announce its flow, set their
                                                             subject against a legacy way of working, close with
their 0.739, and our mean human-model kappa is               a summary, and speak in a confident institutional
0.951 against their 0.839. The LLM scorer agrees             voice. The shape also identifies the author: our
with the human annotators more closely than the              classifier assigns 68.6% of posts to the correct one
original’s did, and more closely than the original’s         of the six sources, far above the 16.7% chance
annotators agreed with each other. Each annota-              rate (Section 5.5). And the distinct shape is shared
tor’s individual agreement with the model clears             across AI models: human posts sit in the rare re-
the 0.60 bar as well. In a separate audit, the anno-         gions of structural space, while the five AI models
tators reviewed the model’s calls on which features          concentrate in common ones (Section 6). Mathur
count as style rather than structure, and endorsed           et al. (2026) observed at platform scale that mass-
that boundary (all kappas above the 0.75 bar, detail         produced generative content can be seen as unique
in Appendix H).                                              variations of functionally identical material. At
   Disclosures. The reliability filter’s 52 exclu-           the level of company blog posts, our measurement
sions and the 11 format-sensitivity exclusions are           confirms this.
itemized in Section 4.5, and the answer distribu-               The shape also goes deeper than the word level.
tions, drift rates, and per-feature stability records        Rewording attacks replace most of the surface
are published in the release. Both annotators are            phrasing, but the structural feature detection accu-
company-affiliated (Section 9).                              racy remains nearly unchanged (Section 5.4). The
                                                             error-overlap result points the same way: the struc-
8       Discussion and Conclusion                            tural and style models fail on almost entirely dif-
                                                             ferent posts, so the two feature sets carry different
We asked whether AI-generated text has a shape:              signals.
a structural signature in how information is pre-               For search engine platforms, the practical read-
sented, in what order, with what evidence, and in            ing is that structural features are a candidate sig-
what voice, independent of the words being used.             nal for detecting AI-generated content that is ro-
Within the studied scope, the answer is yes. Com-            bust against word-level attacks. Google’s policy
mercial blog posts have no plot, no characters, and
on scaled content abuse already targets outcomes         period human-vs-AI comparison remains open.
rather than methods (Section 1), and our structural         Magnitude interpretation. Every effect we re-
instrument fits this reasoning. The instrument also      port is consistent in direction with the original and
reads both ways: the same features that flag the         at least as large in magnitude. The discovery stage
common structural configurations AI posts use also       optimizes features to separate these six sources on
locate the rare configurations of human writing.         the corpus, and a commercial-native schema fitted
   There are three limitations to our instrument.        to the domain probably amplifies the effect. We
First, we cover single-pass generation from the five     therefore do not claim that commercial content is
state-of-the-art AI models. Second, the instrument       intrinsically more separable than fiction, only that
is LLM-run end to end. Like the original study, our      the underlying effect replicates.
validity rests on the validity of Section 7. Third, we      Corpus scale and composition. The corpus has
tested the robustness of our instrument only against     2,250 prompts against the original’s 10,272, and the
rewording attacks, not against the myriad of other,      feature-discovery set is 4.4% of the corpus versus
potentially more sophisticated humanizer and para-       their roughly 1%. Our bootstrap CI widths are
phrase tools. Those attack classes remain an inter-      adjusted accordingly, but per-class attribution and
esting avenue for future research (Section 9).           top-tail rarity statistics are underpowered relative
   To facilitate this research, we release the           to the original. The sampling corpus is software-
pipeline, methodology and code together with the         heavy, US-heavy, and 75.5% of post snapshots date
paper.                                                   from 2020-2022.
                                                            Attack coverage. Our rewording test covers
9   Limitations                                          rewording by the generating models themselves,
Scope of the detection claim. Our design mea-            following an editing protocol of Chakrabarty et al.
sures single-pass generation, both as generated and      (2025). It does not cover a range of humanizer or
after rewording (Section 5.4): every AI post is a        paraphrase tools. Claims about those attack classes
model’s first-shot response to a reverse-engineered      remain open.
brief, optionally rewritten by the model that gener-        Competing interests. The author operates Site-
ated it - not humanized, heavily post-processed, or      fire, a commercial GEO product (formal statement
human-AI collaborative content.                          in the Statements section).
    Brief lossiness. The mirror mechanism is
                                                         Statements
informationally asymmetric: the human author
wrote from full business context, while each AI          Data availability.        The release package is
model conditions only on a reverse-engineered            at https://github.com/pulse-energy-
brief. Some human-AI structural differences may          eu/slopshape. Publicly released: the sampling
therefore reflect what the brief fails to carry rather   ledger with a deterministic fetch pipeline that re-
than how models write. We inherit this limitation        builds the exact human corpus from public archives,
from the original study.                                 the template schema with its NarraBench map-
    Input format. Human posts are scored as ex-          ping, the complete 203-feature instrument, the com-
tracted and normalized, AI posts as generated. The       plete prompt set (including the rewording-attack
format-sensitivity filter removes the features this      prompt), the analysis code (including the fork patch
difference moves beyond scorer noise, and the test-      against the original’s released pipeline and the re-
split check shows the headline classifier is stable to   wording verification gates), and the aggregate arti-
it (Appendix G), but smaller format effects on the       facts and regeneration scripts behind every number
remaining features cannot be ruled out.                  and figure in this paper. Available to researchers on
    Publication-year confound (inherent). Our hu-        request, under a non-commercial research agree-
man posts predate ChatGPT and mirrors were gen-          ment: the per-post feature answers, deterministic
erated in August 2026, so publication period and         refits of the trained models, and the generated briefs
authorship are confounded. The publication-year          and mirrors. We gate these and only these because
check provides evidence that structural features         the ready-to-use scoring assets are the direct sub-
cannot predict when a human post was published,          strate of a commercial product and because the
and removing the most year-associated features           mirrors embed content derived from copyrighted
does not change the headline result. Still, same-        source posts. We do not redistribute the copy-
righted human posts themselves, and everything          T. Chen and C. Guestrin. 2016. XGBoost: A Scalable
needed to audit the paper’s claims can be rebuilt          Tree Boosting System. In Proceedings of the 22nd
                                                           ACM SIGKDD International Conference on Knowl-
with the released pipeline.
                                                           edge Discovery and Data Mining.
   Ethics. Human posts are publicly published mar-
keting content collected from public web archives       J. Cohen. 1960. A coefficient of agreement for nominal
and are not redistributed. No personal data beyond         scales. Educational and Psychological Measurement,
                                                           20(1):37–46.
published bylines is processed.
   Competing interests. The author operates Site-       L. Dugan, A. Hwang, F. Trhlik, J. M. Ludan, A. Zhu,
fire, a commercial GEO product. The study’s meth-          H. Xu, D. Ippolito, and C. Callison-Burch. 2024.
                                                           RAID: A Shared Benchmark for Robust Evaluation
ods, instrument, prompts, code, and aggregate ar-
                                                           of Machine-Generated Text Detectors. In Proceed-
tifacts are publicly released, with post-level data        ings of ACL 2024. arXiv:2405.07940.
available to researchers on request, so that every
claim can be verified independently of that interest.   Google. 2024.     Spam policies for Google web
                                                          search.       https://developers.google.
   AI disclosure. Beyond their role in the method,        com/search/docs/essentials/spam-
AI models and coding agents (Claude Code) were            policies. See also the accompanying March
used to write and test the analysis code, generate        2024 scaled-content-abuse update “New ways we’re
tables and figures, and draft and edit the text. The      tackling spammy, low-quality content on Search”
                                                          (2024-03-05).
author takes full responsibility for the content.
   Acknowledgments. We thank J. Russell for cor-        Graphite. 2025. More Articles Are Now Created by
respondence resolving ambiguities in the original         AI Than Humans. Graphite Five Percent blog.
study’s reported constants.                               https://graphite.io/five-percent/
                                                          more-articles-are-now-created-by-
                                                          ai-than-humans.
References                                              Graphite. 2026. AI Now Writes as Many Online
                                                          Articles as Humans.  Graphite Five Percent
P. Aggarwal, V. Murahari, T. Rajpurohit, A. Kalyan,
                                                          blog.        https://graphite.io/five-
   K. Narasimhan, and A. Deshpande. 2024. GEO:
                                                          percent/ai-now-writes-as-many-
   Generative Engine Optimization. In Proceedings
                                                          online-articles-as-humans-do.
   of the 30th ACM SIGKDD Conference on Knowl-
   edge Discovery and Data Mining (KDD 2024).           S. Hamilton, M. Wilkens, and A. Piper. 2025.
   arXiv:2311.09735.                                      NarraBench: A comprehensive framework for narra-
Ahrefs. 2025. 74% of New Webpages Include AI Con-         tive benchmarking. arXiv:2510.09869.
  tent (Study of 900k Pages). Ahrefs Blog. https:       A. Hans, A. Schwarzschild, V. Cherepanova, H. Kazemi,
  //ahrefs.com/blog/what-percentage-                       A. Saha, M. Goldblum, J. Geiping, and T. Goldstein.
  of-new-content-is-ai-generated/.                         2024. Spotting LLMs With Binoculars: Zero-Shot
Anthropic. 2026. Claude text watermark (product            Detection of Machine-Generated Text. In Proceed-
  announcement). https://www.anthropic.                    ings of the 41st International Conference on Machine
  com/news/claude-text-watermark.                          Learning (ICML 2024). arXiv:2401.12070.

C. Brooks, S. Eggert, and D. Peskoff. 2024. The         M. Khosravi and H. Yoganarasimhan. 2026. Impact
  Rise of AI-Generated Content in Wikipedia. In           of AI Search Summaries on Website Traffic: Evi-
  EMNLP 2024 Workshop on NLP for Wikipedia.               dence from Google AI Overviews and Wikipedia.
  arXiv:2410.08044.                                       arXiv:2602.18455.

T. Brown, B. Mann, N. Ryder, et al. 2020. Language      D. Kobak, R. González-Márquez, E.-Á. Horvát, and
   Models are Few-Shot Learners. In Advances in Neu-      J. Lause. 2025. Delving into LLM-assisted writing in
   ral Information Processing Systems 33 (NeurIPS         biomedical publications through excess vocabulary.
   2020).                                                 Science Advances, 11. arXiv:2406.07016.

T. Chakrabarty, P. Laban, and C.-S. Wu. 2025. Can       K. Krippendorff. 2004. Content Analysis: An Introduc-
   AI writing be salvaged? Mitigating Idiosyncrasies       tion to Its Methodology, 2nd edition. Sage Publica-
   and Improving Human-AI Alignment in the Writing         tions.
   Process through Edits. In Proceedings of the 2025
   CHI Conference on Human Factors in Computing         K. Krishna, Y. Song, M. Karpinska, J. Wieting, and
   Systems. arXiv:2409.14509.                             M. Iyyer. 2023. Paraphrasing evades detectors of AI-
                                                          generated text, but retrieval is an effective defense. In
M. Chen, X. Wang, K. Chen, and N. Koudas. 2025.           Advances in Neural Information Processing Systems
  Generative Engine Optimization: How to Dominate         36 (NeurIPS 2023). arXiv:2303.13408.
  AI Search. arXiv:2509.08919.
                                                                                                             Document length by source
W. Liang et al. 2025. The widespread adoption of large                            3500
  language model-assisted writing across society. Pat-
                                                                                  3000
  terns (Cell Press). arXiv:2502.09747.
                                                                                  2500




                                                             Words per document
S. M. Lundberg and S.-I. Lee. 2017. A Unified Ap-                                 2000
   proach to Interpreting Model Predictions. In Ad-                               1500
   vances in Neural Information Processing Systems 30
                                                                                  1000
   (NeurIPS 2017).
                                                                                   500
E. Masrour, B. Emi, and M. Spero. 2025. DAMAGE:                                      0
   Detecting Adversarially Modified AI Generated Text.                                     Human   GPT-5.4     Claude 4.6   Gemini 3     DeepSeek 3.2   Kimi 2.5

   arXiv:2501.03437.
                                                             Figure A1. Word-count distributions by source (boxes
A. Mathur, C. Liu, K. Tan, and Y. Liu. 2026. Scal-           = IQR, whiskers to 1.5 IQR, outliers hidden). Four
  able Detection of Adversarial Synthetic Slop and           of the five AI models produce longer posts than their
  Coordinated Media Abuse: A LoRA-Enabled                    human sources on average, while kimi-k2.5 runs slightly
  Multimodal Defense System. Google Research.                shorter.
  https://storage.googleapis.com/
  gweb-research2023-media/pubtools/
  1039291.pdf.
                                                                                  Longer: A Modern Bidirectional Encoder for Fast,
E. Mitchell, Y. Lee, A. Khazatsky, C. D. Manning,                                 Memory Efficient, and Long Context Finetuning and
   and C. Finn. 2023. DetectGPT: Zero-Shot Machine-                               Inference. arXiv:2412.13663.
   Generated Text Detection using Probability Cur-
                                                             D. Weber-Wulff et al. 2023. Testing of detection tools
  vature. In Proceedings of the 40th International
                                                               for AI-generated text. International Journal for Edu-
  Conference on Machine Learning (ICML 2023).
                                                               cational Integrity, 19(26).
   arXiv:2301.11305.
                                                             P. Zhang, R. Cui, and D. J. Zhang. 2026. The Impact
M. Perkins, J. Roe, et al. 2024. GenAI Detection Tools,
                                                                of AI Search on the Online Content Ecosystem: Evi-
  Adversarial Techniques and Implications for Inclu-
                                                                dence from Google and Reddit. arXiv:2605.16428.
  sivity in Higher Education. arXiv:2403.19148.
J. Russell, M. Karpinska, D. Akinode, J. Zhou, K. Thai,      A                           Data collection detail
   B. Emi, M. Spero, and M. Iyyer. 2026b. AI use in
   American newspapers is widespread, uneven, and            This appendix carries the corpus composition, mir-
   rarely disclosed. In Proceedings of ACL 2026.             ror coverage, and funnel mechanics summarized in
   arXiv:2510.18774.                                         Section 3.
J. Russell, P. Rajendhran, C. Pham, M. Iyyer, and J. Wi-        Of the 306 selected domains, 264 yielded usable
   eting. 2026a. StoryScope: Investigating idiosyn-          posts (40 had no fetchable qualifying articles, 2
   crasies in AI fiction. arXiv:2604.03136.                  were emptied by the content filters), and 4 replace-
V. S. Sadasivan, A. Kumar, S. Balasubramanian,
                                                             ment domains drawn from the same qualification
  W. Wang, and S. Feizi. 2023. Can AI-Generated              pool during the fetch gave the 268 corpus domains.
  Text be Reliably Detected? arXiv:2303.11156.               A per-domain cap of 20 posts was applied (four do-
                                                             mains reach at most 29). The largest single domain
C. Shaib, T. Chakrabarty, D. Garcia-Olano, and B. C.
  Wallace. 2025. Measuring AI “Slop” in Text.                contributes 1.3% of the corpus.
   arXiv:2509.19163.
                                                             B                           Schema and NarraBench mapping
B. Thompson, M. P. Dhaliwal, P. Frisch, T. Domhan,
   and M. Federico. 2024. A Shocking Amount of the           This appendix maps each NarraBench dimension
  Web is Machine Translated. In Findings of ACL 2024.        (Hamilton et al., 2025) to its counterpart in the
   arXiv:2401.05749.                                         commercial schema of Section 4.1.
Z. Tian, Y. Chen, Y. Tang, J. Liu, and R. Jia. 2026. Diag-
   nosing and Repairing Citation Failures in Generative      C                           Instrument detail
   Engine Optimization. arXiv:2603.09296.
                                                             This appendix carries the final instrument’s com-
E. P. Torrance. 1966. Torrance Tests of Creative Think-      position, the quality-gate detail behind Section 4.3,
   ing. Personnel Press.                                     and the scoring-mode gate behind Section 4.4.
B. Warner, A. Chaffin, B. Clavié, O. Weller, O. Hall-           Quality gate. The gate never sees human/AI
   ström, S. Taghadouini, A. Gallagher, R. Biswas,           labels, and its dominant rejection defect was non-
   F. Ladhak, T. Aarsen, N. Cooper, G. Adams,                exhaustive value lists. The gate prompt and all
  J. Howard, and I. Poli. 2024. Smarter, Better, Faster,     rejection reasons are preserved in the release. The
    Axis                     Shares (%)
    Verticals                software/SaaS 26.5, e-commerce 24.3, services 17.4, fintech 15.7, devtools 11.7, health 3.8,
                             edtech 0.6
    Source frame             YC 57.2, Inc5000 33.7, G2 6.8, FT1000 2.3
    Snapshot years           2008-17: 8.5, 2018-19: 16.0, 2020-21: 41.9, 2022: 33.6

Table A1 - Data composition.


                                            Within 10% of                         LDA projection of the structural feature space
 Source              Posts Mean words                                                                                        Gemini 3 Flash
                                            source length               4                                                    DeepSeek V3.2
                                                                                                                             Kimi K2.5
 human               2,250          1,186                -                                                                   Claude Sonnet 4.6
 gpt-5.4             2,250          1,541              .07                                                                   GPT-5.4
                                                                        2                                                    Human
 deepseek-v3.2       2,250          1,447              .16
 gemini-3-flash      2,250          1,283              .41
 claude-sonnet-4.6   2,250          1,279              .66
                                                                        0
 kimi-k2.5           2,250          1,064              .47




                                                                 LD2
Table A2 - AI mirror coverage and length. The last col-                −2
umn reports, per model, the share of mirrors whose word
count lands within 10 percent of their human source’s                  −4
word count.

                                                                            −4   −2      0        2          4       6        8         10
                                                                                                       LD1
deduplication cutoff sweep is check 4 in Appendix
G.                                                               Figure F2. Two-component LDA projection of the
   Aspect-based application check. Scoring one                   encoded structural feature space (12,900 posts). Human
dimension at a time versus scoring a whole post in               posts separate along LD1, while the five AI models
one call, on 12 posts: 99.97% vs 99.75% of items                 overlap heavily with each other, consistent with the
answered, cross-mode agreement 0.774 (original:                  original’s geometry finding.
95.4% vs 68.4%, with the single-call mode sys-
tematically dropping later dimensions). We kept                  model-specific feature table, and the geometry
per-dimension scoring, per the original.                         numbers.
                                                                    Protocol notes: the feature-variant models and
D    Protocol detail
                                                                 the stylometric, TF-IDF, and length baselines are re-
This appendix records the executed hyperparame-                  trained on train+val per the original’s protocol. The
ter grids and the hyperparameter sensitivity result              ModernBERT row (single seed, their 512-token 3-
behind Section 4.7.                                              epoch configuration) and the Binoculars-style row
   The binary task’s grid comprised 108 configura-               (Qwen2.5-0.5B base/instruct pair in place of their
tions over n_estimators, max_depth, reg_lambda,                  Falcon-7B pair) are single fine-tunes or zero-shot
and scale_pos_weight, and the six-source task ran                substitutes, disclosed.
its own 27-configuration grid, both centered on the                 Cohen’s d uses the unweighted root-mean-
original’s published constants (500/7/1.0). Hyper-               square of the two group SDs (the original pooled
parameter sensitivity: refitting with those constants,           by group size).
untuned, gives binary 96.6 (AUPRC 0.999) and six-                   Selection is by per-class SHAP concentration,
source macro-F1 68.6 (accuracy 69.1) - within 0.4                with the full criteria in the release. The original
points of the tuned configurations on both tasks.                selected 75 features carrying 90 per-source values
                                                                 (counts 32/26/11/11/7/3).
E    Full deviation register                                        Geometry. The average distance from a human
This appendix carries the full deviation register                post to its ten nearest neighbors in the encoded
with each deviation’s defense.                                   structural feature space is 1.42 times larger than for
                                                                 an AI post, the human class as a whole is 1.41 times
F   Additional results                                           more dispersed than the average AI class, and the
                                                                 centers of the human and AI point clouds sit clearly
This appendix carries the additional detection base-
                                                                 apart (centroid distance 11.3 in z-scored units). The
lines, the LDA figure, the rarity tail table, the
 NarraBench dimension     Status              Commercial schema mapping
 Agent                    ADAPTED             Voices and Sources: authors, experts, brands, customers, readers as
                                              discourse roles
 Social Network           REPLACED            Voices and Sources: source arrangements and reader interaction, not
                                              interpersonal plot relations
 Event                    ADAPTED             Audience/Problem/Stakes and Timeliness: business triggers, policy
                                              changes, lifecycle moments
 Plot                     REPLACED            Structure and Flow: movement from problem or context to explanation,
                                              recommendation, resolution
 Structure                ADAPTED             Structure and Flow plus Page Format and Navigation
 Setting                  ADAPTED             Audience/Problem/Stakes: the reader’s professional, market, regulatory,
                                              technical context
 Time                     KEPT                Timeliness: chronology, temporal reference, change, timing relevance
 Revelation               REPLACED            Explanation Depth plus Evidence and Proof: staged explanation and
                                              substantiation
 Perspective              ADAPTED             Voices and Sources: institutional, founder, expert, interviewer, direct-reader
                                              viewpoints
 Style                    KEPT                Writing Style: the single mandated style bucket

Table B1 - NarraBench mapping (kept / adapted / replaced).

 Dimension                 Features     Types                                         Example feature
                                        (categorical/binary/ordinal/scale/multi)
 Actionability                     33   18/5/5/1/4                                    Conditional Logic Presence
 Writing style                     27   14/4/4/4/1                                    Dominant Sentence Complexity
 Audience                          22   8/7/3/4/0                                     Opening Reader Question Invitation
 Explanation                       21   13/4/2/1/1                                    Caveat Presence
 Timeliness                        20   11/1/4/2/2                                    Primary Change Story
 Voices                            20   9/4/4/1/2                                     Primary Reader Role
 Structure and flow                18   10/3/3/1/1                                    Primary Repeated Building Block
 Evidence                          17   5/6/3/1/2                                     Attribution Density
 Commercial integration            14   5/4/3/2/0                                     Proof of Capability Presence
 Purpose                            8   6/2/0/0/0                                     Dominant Communicative Purpose
 Page format                        3   3/0/0/0/0                                     Article Length Class

Table C1 - Final 203-feature instrument composition.


original found the same picture in fiction - humans           exclusions all inside the Writing-Style dimension)
more dispersed, the AI models clustered together              is endorsed by the human annotators.
(+22% dispersion, 1.13x neighbor radius) - and our
version of it is again larger.                                I    Original released-code defects and fixes
                                                              This appendix records the five defects we found
G    Robustness checks, full table
                                                              in the original’s released code. Each is fixed in
This appendix carries the full results and caveats            our fork toward the paper’s stated method, which
behind the check summary of Table 8. Every check              makes the replication more faithful, not less. The
runs under the original’s protocol (final models              unmodified originals and the full defect record are
retrained on train+val).                                      preserved in the release for side-by-side verifica-
                                                              tion.
H    Instrument validity, full detail                            Beyond these fixes and authentication/plumbing
This appendix carries the style-boundary audit be-            changes (provider base URLs and API-key paths,
hind Section 7.                                               a 391-line fork patch over 7 files), no feature, en-
   Style-boundary audit. On 40 sampled fea-                   coding, classifier, or analysis code was modified.
tures, human agreement with the model’s binary
                                                              J    Rewording test detail
style/non-style call: annotator A 90.0% (kappa
0.765), annotator B 97.5% (0.936), against a 0.75             This appendix carries the rewriting protocol, the
bar fixed before the audit. Human-human agree-                verification gates, and the per-model detail behind
ment is 92.5% (0.827). The strict style boundary              Sections 4.8 and 5.4.
(GPT-5.4, 3 runs, 0.989 inter-run agreement, 34
 #       Deviation from the original                                              Defense
 D1      Domain: B2B blog posts                                                   The research question
 D2      Brief extractor gemini-3-flash (their gemini-2.5-flash is deprecated)    Declared
 D3      Brief prompt adapted: names the publisher as commissioner,               Parity: the original’s brief names characters
         anti-quotation clause added                                              and settings
 D4      Dedup cutoff 0.85 retained from the original (not re-selected)           Parity, sweep published (Appendix G, check
                                                                                  4)
 D5      Style audit 3 runs with agreement statistics (theirs: 1 run)             Exceeds the original
 D6      Domain-disjoint splits, single-unblinding holdout (theirs: random        Stricter
         prompt split)
 D7      Rarity metric re-implemented from text                                   Verified on their data, magnitudes disclaimed
 D8      Extraction and discovery via OpenAI direct API                           Provider plumbing
 D9      Encoder fixes (ordinal by taxonomy position, nominal one-hot)            Their released code deviated from their own
                                                                                  paper
 D10     Corpus scale ~2,250 prompts (~1/4.5 of theirs), feature-discovery set    Budget and domain scarcity of archived
         4.4% of corpus vs their ~1%                                              pre-2022 posts, power note in Section 9
 D11     Commercial-native template schema discovered from human posts            Fiction lens misfits commercial content,
         (theirs: NarraBench fiction schema)                                      mechanism unchanged, mapping table
                                                                                  published
 D12     Mirror max_tokens 8,000 (theirs: 128k/65k)                               Matched to commercial target lengths
 D13     Evaluation-stage models upgraded within family lineage, the five AI      Same-variant newer versions for
         models unchanged                                                         non-generating tasks
 D14     Rewording test: each of the five AI models rewrites its own posts, all   Realistic production pattern, removes the
         1,450 test mirrors (theirs: 278 posts, one model as rewriter)            original’s single-model asymmetry, yields a
                                                                                  per-model breakdown
 D15     Rewording prompt is instruction-only (the original’s 25 few-shot         Domain adaptation, declared - not parity
         professional examples are fiction rewrites)
 D16     Content-preservation constraint added (keep claims, facts, links)        Verified by a full claim-preservation census
                                                                                  (Appendix J)

Table E1 - Deviation register (full defenses).

  Variant / baseline                        n feat     Test             AUPRC                          Original
                                                       macro-F1
  Binoculars-STYLE (small-pair              -          78.2             .980                           (their true Binoculars:
  substitute, context only)                                                                            55.9 / .404)
  Length-only logistic                      1          45.5             .871 (prevalence baseline      55.9
                                                                        .833 at the 5:1 ratio)

Table F1 - Additional binary detection baselines (rows not in Table 3).


   Prompt design. The rewriting prompt fol-                       control, and after a two-pass regeneration loop (192
lows the LAMP taxonomy of Chakrabarty et al.                      regenerations) the full census reads 98.2%, with 26
(2025): the seven categories of AI-writing artifacts              single-item residuals disclosed and left in.
their study identified with professional editors, to-                Rescoring and evaluation. The rewritten posts
gether with their editing instructions. The prompt                are scored by the identical frozen stage-5 scorer
is instruction-only (deviation D15). A content-                   and prompts (byte-identity asserted), covering all
preservation clause instructs the model to keep                   15,950 answers (1,450 posts x 11 dimensions) with
every claim, fact, and link and to reword freely                  0 unresolved failures and a rate of answers out-
within them (deviation D16). The full prompt text                 side the predefined options of 0.082% on average
is in the release.                                                (0.089% in our main scoring run). The encoding is
   Verification gates. All gates were fixed before                identical, the classifiers are deterministic refits of
generation, and all passed. Length drift between                  the final models, and nothing is retrained on rewrit-
a rewritten post and its source was bounded to the                ten text. Of the 1,450 reworded AI posts, the struc-
ratio interval [0.6, 1.4], with 0 violations (mean                tural classifier misclassifies 18 as human-written
ratio 0.922, minimum 0.607). Refusals: 0 of 1,450.                (9 before rewording), the style-only classifier 19 (8
Trivial-copy flags: 0 after reruns. For claim preser-             before), and the all-features classifier 10 (3 before).
vation, we judged all 1,450 original-rewritten pairs              Of these, 13, 16, and 8 posts respectively were clas-
in full: 90.3% preserved every claim before quality               sified correctly before rewording. Table J1 gives
 Tail           Human posts           AI posts (five models pooled)    Human share of tail   Original (test basis)
 Rarest 1%      146                   2                                98.7%                 42 human vs 41 AI
 Rarest 5%      586                   85                               87.3%                 -
 Rarest 10%     1,016                 319                              76.1%                 -

Table F2 - Rarity tail composition.

    Source       Model-specific features (up to 5)
    human        Execution Support Resources (ACT_CHK_025); Link and Resource Placement (ACT_CHK_032); False
                 Default Challenged (AUD_PRB_005); Legacy Versus Modern Contrast (AUD_PRB_006); Reader
                 Situation Mirroring (AUD_RDR_006)
    gpt          Numeric Density (EVD_NUM_001); Quantitative Claim Sourcing (EVD_NUM_006); Article Length
                 Class (PAG_FUR_011)
    claude       -
    gemini       Opening Reader Question Invitation (AUD_HOK_006); Self-Reference Frequency (COM_ROL_005);
                 Legacy-to-Modern Commercial Contrast (COM_ROL_011); Evidence Limitation Disclosure
                 (EXP_KNW_009)
    deepseek     Change Requested of Reader (PUR_JOB_004); Conditional Routing Density (STR_UNI_003)
    kimi         Product as Stakes Resolution (AUD_STK_007); Commercial CTA Intensity (VOC_PRT_003)

Table F3 - Model-specific features by source (top features by six-source SHAP concentration). The table lists up to
five features per source, with per-source totals in Section 6.


the attack magnitude and the attacked structural
score per model.
 #      Check                          Result
 1      Length confound (original’s    Length-matched test subsample (1,545 posts, median words human 1,004 vs AI
        Section F)                     1,081): headline 96.9 vs 97.0 unmatched - unchanged, mirroring the original (93.2 to
                                       93.2). Rarity d on the matched subset 1.83, corr(words, rarity) = 0.08. Per-model
                                       matched rarity means preserve the full-corpus ordering (deepseek 0.55 remains
                                       closest to humans)
 2      Publication-year check         Predicting a human post’s publication period from structural features performs at
                                       chance (macro-F1 49.1, grouped CV; 187 vs 1,622 posts, where always guessing the
                                       larger class scores 47.3). Removing the most year-associated features leaves the
                                       headline flat (96.7-97.0). Top-25 year/authorship feature overlap 3/25 - publication
                                       year is not the signal
 3      Template-vs-direct discovery   Same candidate yield (raw-on-text 354 vs template-run mean 356.7, all 11
        (the original’s                dimensions) but only ~23% bidirectional semantic overlap at 0.85 embedding
        template-necessity ablation)   similarity - the discovery pathway substantially shapes which features are found
                                       (original: 6 of top-20 overlap). The raw feature set was not scored at scale (declared)
 4      Deduplication cutoff sweep     Cutoffs 0.70-0.95 published: 200/233/251/266/277/282 features. Silhouette
                                       monotonically decreasing (0.182 at 0.70 to 0.065 at 0.85), so silhouette alone would
                                       prefer lower cutoffs - divergence disclosed. 0.85 retained for parity (merge 5.7% vs
                                       their 25.5%), sensitivity low
 5      Feature-discovery-set          11 of the 82 feature-discovery-set domains land in the test split. Sensitivity excluding
        domain overlap                 them: 96.5
 6      Memorization (original’s       Exact 13-gram rule: 0.19% of the 10,750 human-mirror pairs (the 2,150 classification
        Section E, both rules, exact   prompts x 5 mirrors) share at least one 13-gram (shuffled-human control: 0.0%,
        implementations)               original: 0.70% flagged). Near-verbatim rule (8-gram coverage >= 5%, >= 4 distinct
                                       8-grams, longest common span >= 30 tokens): 0 pairs. Excluding all 16 affected
                                       prompts: headline 97.2 (delta +0.3 points, original’s filtered deltas <= +0.3)
 7      Vertical heterogeneity         H = 9.047, p = 0.107 over the 6 verticals with >= 20 test posts - not significant,
        (Kruskal-Wallis, original’s    consistent with the original’s null (H = 4.69, p = 0.46). Per-vertical macro-F1 ranges
        topic robustness)              from 94.8 (services) to 100 (health). Caveats: grouping uses >= 20 test posts where
                                       the original used >= 20 prompts (the thinnest vertical rests on 5 prompts), and
                                       per-post correctness observations are domain-clustered, an independence violation
                                       the original’s version shares
 8      Learning curve                 Train+val fractions 25/50/75/100%: 95.4 / 96.4 / 96.4 / 97.0 (3 seeds each)
 9      Format sensitivity             The Section 4.5 rescoring repeated on the test split (250 AI posts; 235 human posts)
                                       flags 9 features, all among the 11 excluded. The structural classifier still detects 249
                                       and 247 of 250 AI posts (markdown stripped; title also removed) and calls 15 of 235
                                       human posts AI with the title added (18 as scored)

Table G1 - Robustness checks, full results.




 #      Defect in released code         Symptom                                        Our fix
 B1     Stage config keys passed        Every stage runner crashes on launch           De-duplicated the keyword
        twice to the provider layer                                                    pass-through
 B2     Stage 5 only recognizes a       All human posts silently dropped: the          Source-column handling accepts the
        human_story source column       feature matrix would contain zero human        corpus’s human and mirror columns
                                        rows
 B3     JSON-generation path ignores    The paper states stage 5 runs “minimal         Thinking budget set as a stage
        the thinking configuration      thinking”, but the released code sets no       parameter, matching the paper’s stated
                                        thinking budget and runs full reasoning        method
                                        (83x slower per dimension call)
 B4     Shipped stage-3 prompt does     The prompt asks for a two-template             Prompt rewritten to the paper’s
        not implement the paper’s       quality comparison and contains                specification (all templates together,
        stated method                   {group_a_json}/{group_b_json}                  structured per-source notes,
                                        placeholders the code never fills, while       divergences, executive summary). The
                                        the paper describes all six templates          shipped prompt and the first defective
                                        presented together with cross-source           run are preserved
                                        divergence mining
 B5     Released encoding deviates      Ordinal and nominal features not encoded       Ordinal encoded by taxonomy position,
        from the paper’s stated         as the paper describes                         nominal one-hot, per the paper’s text
        scheme (deviation D9)

Table I1 - Released-code defects and fixes.
                                AI model            Surviving       Attacked
                                                    13-gram share   structural
                                                                    macro-F1
                                gpt-5.4             0.175           96.5
                                claude-sonnet-4.6   0.535           95.3
                                gemini-3-flash      0.003           95.9
                                deepseek-v3.2       0.489           95.9
                                kimi-k2.5           0.141           96.0

Table J1 - Per-model attack magnitude and attacked structural detection. The surviving 13-gram share is the fraction
of a post’s 13-word sequences that still appear verbatim after rewriting (mean 0.269 across models, i.e. 73% of
13-word sequences replaced on average).
