                                        Impact of AI Search Summaries on Website Traffic: Evidence from
                                                                 Google AI Overviews and Wikipedia
                                                                Mehrzad Khosravi *                      Hema Yoganarasimhan
                                                              University of Washington                 University of Washington

                                                                                       September 4, 2026
arXiv:2602.18455v6 [cs.CY] 2 Sep 2026




                                                                                             Abstract

                                                 Search engines increasingly display AI-generated answers above organic links, potentially
                                             displacing traffic to upstream publishers. We estimate the impact of Google’s AI Overviews
                                             (AIO) on Wikipedia’s search traffic using AIO’s staggered geographic rollout and Wikipedia’s
                                             multilingual structure. Our difference-in-differences design compares monthly external-search
                                             referrals to English Wikipedia articles with referrals to the same articles in German and French,
                                             and finds that default AIO availability reduced English search traffic by 5.45% and 4.82% ,
                                             respectively. Our results suggest that answer-producing digital intermediaries can materially real-
                                             locate attention away from informational publishers, with implications for content monetization,
                                             search platform design, and policy.

                                        Keywords: Generative AI, Search Engines, Digital Economy, Artificial Intelligence, Wikipedia, Google




                                          * Please address all correspondence to: mehrzad@uw.edu and hemay@uw.edu.



                                                                                                 1
1   Introduction
Digital information intermediaries, such as search engines and content aggregators, have traditionally created
value by organizing third-party content, lowering search costs, and directing users to relevant publishers.
Generative AI changes this role by allowing search engines and information intermediaries to synthesize
information from multiple upstream publishers and present a self-contained response within their own
interfaces. Rather than merely helping users locate relevant content, these intermediaries can now satisfy
part of users’ information demand before they visit the underlying source. This shift can improve access to
information and further reduce search costs, but it may also divert attention and economic value from the
publishers whose content supports the generated response. Because many publishers rely heavily on search
referrals, even modest reductions in referral traffic can affect advertising revenue, subscription acquisition,
and ultimately the incentives to produce and maintain content (Nielsen and Fletcher 2022). Whether answer-
producing information intermediaries complement or substitute for upstream content producers is therefore
an important question for the digital economy.
    Google’s AI Overviews (AIO) provides a prominent setting to study this question. Google’s AIO feature
presents a synthesized answer prominently on the search-results page, before the traditional organic links,
and includes links to a limited set of cited sources (Reid 2023, 2024b); see Web Appendix §A for an example.
Google made AIO part of the default search experience for U.S. users in May 2024, (Reid 2024b), and
then expanded AI Overviews internationally in subsequent months, reaching more than 100 countries by
early 2025 (Venkatachary 2024). The change is economically consequential because Google accounts for
approximately 90% of the global search market (Statista 2025).
    There is substantial disagreement over the effect of AIO on upstream publisher traffic. Publishers argue
that by placing a synthesized answer above the organic results, AIO may satisfy users’ information needs
without an external click and push source pages farther down the search-results page. In this view, AIO
acts as a substitute for publisher content and cannibalizes traffic, even when it cites the underlying sources
(Davies 2025; Miller 2025). Google counters that AIO is complementary: it lowers search costs, improves
user satisfaction, and sends users to helpful pages through included links, potentially expanding overall search
activity and traffic to publishers (Reid 2024b, 2025).
    The economic and policy stakes of this disagreement are substantial. U.S. search advertising generated
$102.9 billion in revenue in 2024, accounting for nearly 40% of all U.S. internet advertising revenue
(Interactive Advertising Bureau (IAB) 2025). Google has also steadily integrated advertising into AIO,
expanding these placements across devices and geographies by late 2025 (Google 2025). These developments
increase the economic importance of where users consume information: when AIO satisfies a query within
the search interface, the platform can retain and monetize the user’s attention while the underlying publishers
may lose visits and associated revenue opportunities. If AIO systematically diverts traffic from source pages,
it could shift advertising revenue, user-interaction data, bargaining power, and ultimately market power
from upstream publishers toward large search platforms. Over time, lower traffic and monetization could
weaken publishers’ incentives to create and maintain the content on which generative search relies, potentially


                                                         2
generating a negative feedback loop in content supply. If, instead, AIO lowers search costs and directs users
toward more relevant or higher-quality sources, it may improve the efficiency of information search and
generate more valuable visits for publishers. Distinguishing between these possibilities is therefore central
to understanding how generative search redistributes attention and economic value, and how it shapes the
long-run incentives to produce the content on which it depends.
    At a high-level, this debate echoes prior work on news aggregators, which asks whether aggregators
cannibalize publisher demand (substitution) or expand it by improving discovery and lowering search costs
(complementarity). Empirical evidence largely supports complementarity: removing Associated Press content
from Google News reduced traffic to other publishers (Chiou and Tucker 2017), and the unavailability of
Google News in Spain decreased traffic to Spanish publishers (Calzada and Gil 2020; Athey et al. 2021).
However, AIO changes the mechanism in a way that makes direct extrapolation difficult. Unlike an aggregator
that primarily routes users to linked pages, AIO presents a synthesized answer before organic links and can
satisfy informational queries without a click. Whether this shift from routing demand to fulfilling it turns the
intermediary from a complement into a substitute is therefore an empirical question.
    We estimate the causal effect of Google’s AI Overviews on publisher search traffic, using Wikipedia as
a large, transparent, and economically important empirical setting. Wikipedia is particularly well suited to
this analysis for three reasons. First, it is one of the world’s most visited websites and a major source of
informational content, receiving more than 130 billion page views per year (Wikipedia 2025a,b). Search
engines also play a central role in directing users to Wikipedia.1 Second, Wikimedia’s public clickstream data
report article-level referrals from external search engines, allowing us to measure directly the traffic channel
most closely tied to AIO (Wikimedia Foundation 2026). Third, Wikipedia’s multilingual structure allows us
to observe traffic to different language versions of the same underlying article. This structure, together with
the staggered geographic rollout of AIO, supports a within-article, difference-in-differences design.
    A priori, the effect of AIO on Wikipedia traffic is ambiguous. On the one hand, Wikipedia’s concise
factual content resembles the information that AIO can synthesize and present directly, making visits to
Wikipedia potentially easy to replace. On the other hand, Wikipedia ranks prominently in organic search and
is among the sources most frequently cited in AI-generated summaries (Harsel et al. 2025). These citations
could increase Wikipedia’s visibility and direct users to its pages. AIO could therefore either substitute for
Wikipedia visits by satisfying users’ information needs directly or complement them by increasing exposure
to Wikipedia’s content.
    We construct article–language–month panels from Wikimedia’s public clickstream data covering Decem-
ber 2023 through December 2024. Our main samples contain 499,927 matched English–German article pairs
and 530,873 matched English–French article pairs. We use English Wikipedia as the treated edition because
a substantial share of its readership comes from the United States, where AIO became part of the default
search experience in May 2024. We use the German and French editions as controls because their readership
is concentrated in European markets where AIO did not become part of the default search experience during
1According to industry reports, 70-80% of Wikipedia’s traffic originates from organic search (Similarweb 2025; SemRush 2025).




                                                              3
our sample period (Reid 2024b; Schwartz 2025). We then estimate a PPML difference-in-differences model
that compares each English article’s monthly search traffic with that of its corresponding German or French
version, controlling for article–language and calendar-month fixed effects to absorb persistent cross-language
differences in baseline traffic and common monthly shocks.
    We find that the introduction of AIO led to a substantial relative decline in English Wikipedia search
traffic. Monthly traffic to English articles fell by approximately 5.45% relative to their German counterparts
and by 4.82% relative to their French counterparts. Translating the estimates into traffic levels, we obtain a
back-of-the-envelope reduction of approximately 100.27 million direct search-originated visits to English
Wikipedia per month.
    We interpret these estimates as reduced-form effects of moving the U.S. search environment into a
default-AIO regime, rather than as effects conditional on an individual AIO display. Actual exposure was
incomplete: only a portion of English Wikipedia traffic originates in the United States, the clickstream data
combine Google with other search engines, and Google displayed AIO for only a subset of queries while
continuing to revise its triggering rules during the post-treatment period (Reid 2024a; BrightEdge 2024;
Khromova and Ivanna 2024). The estimates therefore average across users, queries, search engines, and
months with varying exposure. Under sign-consistent effects, this incomplete exposure would attenuate the
reduced-form estimates relative to the effect among Google searches that actually displayed an AIO.
    Two related papers following ours provide complimentary evidence on the consequences of AIO in
different settings. Agarwal and Sen (2026) run a field experiment involving 1,000 users over a two-week
period and find that AIO substantially reduces outbound organic clicks and increases zero-click searches.
Their study provides direct user-level evidence over a short experimental window, while our analysis
documents publisher-side traffic effects from the real-world rollout across hundreds of thousands of articles
and millions of visits.2 Relatedly, Zhang et al. (2026) study downstream activity in Reddit communities
and find increases in comments and unique commenting users following AIO exposure. This positive effect
on Reddit engagement contrasts with our findings, and may reflect Reddit’s distinctive position in the AIO
ecosystem. Although Reddit does not typically rank among the top organic results for many searches, it is
one of the sources most frequently cited and linked in AIO summaries, following its data-sharing agreement
with Google (Edmonds 2025). Taken together, these studies suggest that the effects of AIO and similar
answer-first generative features can crucially depend on how it changes a publisher’s visibility in the search
ecosystem. Our study contributes to this emerging evidence by documenting how the rollout of AIO affected
search-referral traffic to a major informational publisher, Wikipedia.
    More broadly, our findings show how generative AI can change the role of digital intermediaries. When
an intermediary moves from organizing links to producing answers, it may lower users’ search costs while
reducing visits to the upstream sources on which those answers rely. The results therefore have implications
2 Our findings are consistent with theirs in direction, although the estimated effects in our setting are considerably smaller. This

 difference may reflect the nature of the publisher (Wikipedia versus generic publishers that may experience larger declines in traffic),
 the opt-in design of their experiment (which recruited relatively active and knowledgeable users), or differences in AIO exposure
 arising from the study periods and queries used.



                                                                   4
not only for search-engine design, but also for attribution, platform governance, and the long-run sustainability
of the content ecosystem that generative intermediaries depend on.
2   Setting and Data
AIO rollout and analysis period.          Google’s rollout of AI Overviews was staggered across countries and
regions. First, Google announced nationwide U.S. availability of AIO on May 15, 2024 (Reid 2024b). At this
time, in the U.S. AIO was introduced directly into the default search experience, without requiring users to
opt in. In contrast, AIO was not part of the default search experience in the European markets corresponding
to our control-language editions during our analysis period; Google began rolling out AIO by default in
European Union regions only in early 2025 (Schwartz 2025).
    This geographic staggering motivates our difference-in-differences design. We treat May 2024 as the
onset of the U.S. availability regime. The estimation panel contains five pre-treatment months from December
2023 through April 2024 and eight post-treatment months from May through December 2024.
Treatment and control languages.            The Wikimedia clickstream data report search traffic by language
edition and article, but not by the reader’s country. We therefore proxy geographic exposure to AIO using
Wikipedia language editions. We designate the English-language edition (en.wikipedia.org) as the
treated group because approximately 40% of its traffic originates in the United States, where AIO became
part of the default search experience during our treatment period. For the same underlying articles, we use
the German- and French-language editions (de.wikipedia.org and fr.wikipedia.org) as control
groups. These editions are among the largest Wikipedia language editions by page views (Wikipedia 2024),
and their readership is concentrated in European markets where AIO was not part of the default search
experience during our estimation window.3 Moreover, prior research documents meaningful similarities in
online information discovery and consumption behaviors across users in the United States, Germany, and
France (Stier et al. 2020; Miz et al. 2020; Lemmerich et al. 2019; Fletcher and Nielsen 2018), supporting the
use of German and French editions as comparison groups.
    Spanish provides a less suitable comparison because it is widely used across multiple countries, including
the United States, making its language edition a less precise proxy for geographic exposure. We also exclude
Russian and Chinese editions due to censoring concerns. As an additional robustness check, we report
English–Japanese comparisons separately in Web Appendix §E.
Search referrals traffic data.      We obtain article-level clickstream data from Wikimedia’s publicly available
data sets (Wikimedia Foundation 2026). Among the available traffic sources, we use other-search,
which records monthly human referrals from external search engines as our traffic metric. Because Google
accounts for approximately 90% of the global search market (Statistics 2026), this measure provides a close
proxy for Google search referrals to Wikipedia. Our outcome, Ri,l,m , is therefore the monthly number of
3According to Similarweb (2026), approximately 77% of German Wikipedia traffic comes from Germany, 8% from Austria, and

 5% from Switzerland, while approximately 77% of French Wikipedia traffic comes from France, 5% from Belgium, and 5% from
 Canada.




                                                           5
external-search referrals received by article i in language edition l during month m.4
Article selection and panel construction. We construct separate English–German and English–French
article samples by matching the same underlying Wikipedia articles across language editions. Wikimedia
does not report monthly other-search counts below 10; these observations are therefore censored in the
clickstream data. To ensure that our main analysis is based on reliably measured search-referral counts, we
retain articles that exist since November 2023, and for which both editions have a reported other-search
count of at least 10 in every pre-treatment month (December 2023 through April 2024). This restriction
ensures that sample membership is determined using only pre-treatment information and gives us 499,927
and 530,873 matched articles in the English–German and English–French samples, respectively.
    For post-treatment observations that are censored by Wikimedia’s reporting threshold, we assign a
value of 10 to English counts and a value of 0 to control-language counts. This directional assignment is
conservative for detecting a negative English effect because it reduces the measured decline in English search
referrals relative to the control editions.5
           Table 1: Summary statistics of monthly search traffic for the English–German and English–French samples.


                                        Pre-treatment months (Dec. 2023–Apr. 2024)
                    Statistic          English (EN–DE)         German       English (EN–FR)          French
                    Mean                    4,222.13           624.45            4,305.29             577.76
                    Std.                   26,615.55          4,061.18          26,872.24           3,842.78
                    Min.                     10.00               10.00             10.00               10.00
                    25%                      159.00              38.00            188.00               36.00
                    50%                      628.00             102.00            721.00               92.00
                    75%                     2,438.00           358.00            2,625.00             312.00
                    Max.                 12,503,258.00      3,061,107.00      12,503,258.00       2,386,870.00
                    Articles (QIDs)         499,927            499,927           530,873             530,873
                                        Post-treatment months (May 2024–Dec. 2024)
                    Statistic          English (EN–DE)         German       English (EN–FR)          French
                    Mean                    3,559.10           556.75            3,624.94             511.09
                    Std.                   21,816.49          3,224.70          22,062.84           4,070.44
                    Min.                     10.00              0.00               10.00                0.00
                    25%                      136.00             32.00             159.00               28.00
                    50%                      541.00             89.00             614.00               75.00
                    75%                     2,101.00           315.00            2,247.00             262.00
                    Max.                 11,251,661.00      1,242,785.00      11,251,661.00       2,286,315.00
                    Articles (QIDs)         499,927            499,927           530,873             530,873


4We do not use traffic from other websites as an untreated comparison outcome because AIO may also affect traffic to those websites

 and, consequently, their outbound referrals to Wikipedia. Non-search referrals therefore cannot be treated as a clean control
 outcome.
5Alternative assignments of censored post-treatment observations do not meaningfully affect the results. Specifically, reversing the 0

 and 10 assignment, assigning censored observations a value of 10 in both the English and control editions, or assigning a value of 0
 in both editions, produces estimates that are nearly identical to the baseline results; Web Appendix §C for details.



                                                                  6
Summary Statistics Table 1 reports summary statistics of monthly search traffic for each sample, separately
for the pre-treatment period (December 2023 to April 2024) and the post-treatment period (May 2024 to
December 2024). Because we independently construct the English–German and English–French samples, we
summarize English search traffic separately for the two comparison samples. We observe three broad patterns
in the data. First, English Wikipedia articles receive substantially more search traffic than their German
and French counterparts. As we discuss in the empirical analysis section, this difference in scale motivates
our use of PPML rather than a log-linear specification. Second, search traffic is highly right-skewed across
languages: the mean exceeds the median, reflecting a small number of high-traffic articles. Third, average
monthly search traffic declines from the pre- to post-treatment period across all language editions. In the
empirical analysis below, we examine whether English search traffic declined more than the corresponding
control editions following the AIO rollout.
3     Empirical Analysis
3.1    Model-Free Analysis
We now present a model-free comparison of the English and control-language traffic paths before and after
the introduction of Google AIO in the United States.

                      English–German                                                  English–French




Figure 1: Demeaned log of total monthly search traffic through December 2024 for the English–German and English–French samples.
Each series is demeaned using December 2023–April 2024; the dashed line marks May 2024.


      Figure 1 plots these comparisons over the entire analysis period. For each language and month, we
sum Ri,l,m across all the articles in corresponding sample, transform the aggregate using log(1 + R), and
demean each series by its own pre-treatment (December 2023–April 2024) average. The log transformation
emphasizes proportional rather than absolute changes, while demeaning places the English and control series
on a common pre-treatment baseline.
      Before May 2024, the English and control-language series move closely together. After the AIO rollout,
English search traffic shifts downward relative to both German and French and generally remains below the
control series through the end of the sample. These patterns provide initial evidence of a negative post-AIO
change in English search traffic, which we estimate formally in the next subsection using a PPML difference-
in-differences model. Because the figure aggregates traffic across articles and applies a log transformation,
                                                    7
it does not correspond one-for-one to the article-level PPML estimand. Nevertheless, both approaches
characterize proportional changes, so the figure provides a useful descriptive preview of the regression results.
3.2    PPML Difference-in-Differences Specification and Main Results
We next quantify the post-AIO divergence shown in Figure 1 using a PPML difference-in-differences model
at the article–language–month level.
      We use PPML rather than an OLS difference-in-differences model with logged search traffic for three
reasons. First, when the treated and control outcome distributions differ substantially in scale, a log-linear
specification can produce a treatment effect with the opposite sign from the aggregate effect of interest
(McConnell 2024). This concern is especially relevant in our setting because English articles receive
substantially more traffic than their German and French counterparts. Second, OLS on logged traffic gives
similar weight to a proportional change on a low-traffic article and the same proportional change on a
high-traffic article, so its estimand more closely reflects the response of a typical article. Our primary
interest instead lies in total traffic to Wikipedia, for which changes on high-traffic articles should contribute
more. By modeling the conditional mean of traffic directly in levels, PPML aligns more closely with this
aggregate-traffic estimand while retaining a multiplicative, proportional interpretation (Wooldridge 2010).
Third, PPML accommodates observations with zero traffic directly, without requiring us to drop them or
apply a transformation such as log(1 + R).
      We estimate the following PPML difference-in-differences specification separately for each control
language c ∈ {DE, FR}:
                                                                                         
                          E[Ri,l,m | αi,l , δm ] = exp αi,l + δm + βc Englishl × Postm        ,               (1)

where i indexes the underlying article, l indexes the language edition, and m indexes the month. The indicator
Englishl equals one for the treated English edition, and Postm equals one beginning in May 2024, the month
in which AIO became part of the default U.S. search experience. Article×language fixed effects, αi,l , absorb
persistent differences in article popularity and audience size across language editions, while month fixed
effects, δm , absorb temporal shocks common to both editions in a comparison.
      Under the parallel-trends assumption, βc identifies the average post-AIO change in English search traffic
relative to control language c. This assumption requires that, absent AIO, search traffic to the English and
control-language versions of the same articles would have continued to evolve proportionally in parallel. The
coefficient’s exact percentage interpretation is 100 × [exp(βc ) − 1]. We assess the parallel-trends assumption
and the sensitivity of our conclusions to deviations from it in Section 3.3 and Web Appendix §B. Further,
we two-way cluster standard errors by article and month. Clustering by article allows for correlated shocks
across language editions and over time within an article, while clustering by month allows for common
shocks across articles in a given month (Bertrand et al. 2004; Cameron et al. 2011).
      Table 2 reports the estimates. The English–German coefficient of −0.0561 implies that monthly English
Wikipedia search traffic declined by approximately 5.45% relative to German following the AIO rollout. The


                                                         8
                                               Table 2: PPML DiD estimates

                                                                German       French
                                    English × post           −0.0561∗∗∗ −0.0494∗∗∗
                                                              (0.0117)   (0.0136)
                                    No. observations         12,998,102 13,802,698
                                    Articles (QIDs)           499,927    530,873
                                    Article × language FE        Yes          Yes
                                    Month FE                     Yes          Yes
                                    Robust standard errors in parentheses are two-way
                                   clustered by article and month.
                                    Significance: ∗∗∗ p < 0.001, ∗∗ p < 0.01, ∗ p <
                                   0.05.


English–French coefficient of −0.0494 implies a corresponding decline of approximately 4.82% relative to
French. The similarity in the signs and magnitudes of the estimates across two separately constructed control
samples reduce the likelihood that a shock unique to either control edition drives the results.
      We interpret these coefficients as reduced-form effects of making AIO part of the default U.S. search
experience, analogous to intent-to-treat effects. They do not identify the effect of an individual AIO display
because realized exposure varied along several dimensions, e.g., only a portion of English Wikipedia traffic
originates in the United States, and Google displayed AIO for only a subset of queries (Reid 2024b). Google
also continued to revise AIO’s triggering rules and technical implementation after the May 2024 rollout,
changing both the prevalence of AIO and the composition of queries for which it appeared (Reid 2024a;
BrightEdge 2024; Khromova and Ivanna 2024).6 Our estimates therefore average across users, queries, and
months with different levels of realized AIO exposure. Because we do not observe query-level AIO displays,
we cannot recover the effect conditional on an AIO display. Under sign-consistent effects, the inclusion of
unexposed traffic likely attenuates the reduced-form estimates relative to the effect among Google searches
that actually displayed an AIO.
3.3     Robustness Checks
We next evaluate the robustness of our main estimates by examining whether alternative data choices,
treatment timing, or control groups change our conclusions. We first assess the parallel-trends assumption
using complementary diagnostics and then summarize the remaining robustness checks; the corresponding
Web Appendix reports the full specifications, tables, and figures.
 • Parallel trends. A key assumption of the DiD model is that, absent AIO, English search traffic would
      have followed the same trend as control-language search traffic (Angrist and Pischke 2009). We assess
      this assumption in four ways and confirm that there are no significant violations that threaten the main
      takeaways. First, a parametric linear pre-treatment test finds no statistically significant pre-treatment drift.
6 Third-party audits suggest that AIOs now appear on approximately 18% of Google searches (Tabuena 2025; Chapekis and Lieb

 2025), though this number varies by query type and measurement timeframe.



                                                            9
    Second, monthly event studies show some pre-treatment differences, but the German estimates fluctuate
    around zero, the French estimates move opposite the post-AIO decline, and both are small relative to
    the post-treatment estimates. Next, we use Honest DiD to examine how large departures from parallel
    trends must be to overturn the result; the confidence intervals remain below zero when post-treatment
    changes are allowed to reach 40% of the largest pre-treatment change for German and 35% for French.
    Finally, both equal-weighted and precision-weighted linear extrapolations of the pre-treatment event-study
    coefficients place observed post-treatment search traffic significantly below its counterfactual for both
    controls. See Web Appendix §B for the detailed analyses.
 • Sensitivity to post-treatment censoring assignment. Wikimedia suppresses monthly article-level search
    counts below 10. In the main analysis, we address this missing data issue by assigning unpublished
    post-treatment counts a value of 10 for English and 0 for the control language, which works against
    finding a negative English effect. We test whether the findings depend on this treatment by reversing the
    assignment—0 for English and 10 for the control—while leaving all published counts and the estimation
    samples unchanged. Under this opposite assignment, the estimates imply a 5.5% decline in English
    search traffic relative to German and a 4.9% decline relative to French; both estimates remain statistically
    significant and are nearly identical to the main results. Thus, the estimated effect is not driven by how we
    assign censored post-treatment observations. Please see Web Appendix §C for the detailed analysis.
 • Pre-treatment timing placebo. We also run placebo tests to check whether the main estimates reflect
    a relative decline in English traffic that began before AIO rather than a break following its rollout.
    Accordingly, we re-estimate the PPML DiD model using only pre-treatment period’s data (December
    2023–April 2024) and designate March–April 2024 as an artificial post-treatment period. The placebo
    estimates are not statistically significant for either German or French. The absence of a negative English-
    relative-control shift before May supports the interpretation that the main estimates capture a post-AIO
    divergence. Please see Web Appendix §D for details.
 • Alternative control language. As an additional comparison, we construct a sample of 315,054 matched
    English–Japanese article pairs and end the analysis before August 2024, when Google expanded AIO
    to Japan (Budaraju 2024). The PPML estimate implies a 16.53% decline in English search traffic
    relative to Japanese. Because the Japanese edition differs substantially from the main controls in
    audience composition and because this comparison uses a shorter post-treatment window, we treat it
    as corroborating evidence on the direction of the effect rather than pool it with the German and French
    estimates. Please see Web Appendix §E for details.
4   Discussion and Implications
We now place our empirical findings in a broader economic context. We first discuss the magnitude and scope
of the measured traffic effect, and then consider the implications for publisher monetization, content supply,
intermediary design, welfare, and policy.




                                                      10
Economic magnitude. We first translate the proportional estimates into traffic levels to illustrate their
economic scale. We first take the arithmetic mean of the English–German and English–French PPML
coefficients, which corresponds to an average decline of approximately 5.14%. We then apply this average
effect to the arithmetic mean of monthly post-treatment English search traffic in the two comparison samples.
Because the observed post-treatment traffic already reflects the estimated decline, we use the multiplicative
structure of the PPML model to recover the corresponding counterfactual traffic level absent AIO. This
calculation implies approximately 100.27 million fewer direct search-originated visits to English Wikipedia
per month. If the estimated monthly effect persisted for one year, it would correspond to approximately 1.20
billion fewer direct search visits. Web Appendix §F reports the complete calculation and assumptions.
Scope of the estimates. We next clarify what our estimates capture. Our outcome measures visits that
arrive directly from external search engines. We therefore interpret the estimates as the first-order effect of
AIO on search-originated traffic to Wikipedia, rather than as the overall effect on Wikipedia traffic across all
referral channels.
    AIO may generate additional downstream effects within Wikipedia. For example, a user who enters
Wikipedia through a search engine may visit an initial article and then follow links to several other Wikipedia
pages.7 If AIO eliminates the initial search visit, Wikipedia may lose both the entry-page view and the internal
navigation that would have followed it. The public clickstream data identify only the immediate referrer for
each article transition; they do not link an internal click to the external source that initiated the user’s session
(Wikimedia Foundation 2026). We therefore cannot determine how much internal traffic originates from
search-referred sessions or quantify the resulting downstream effect. Accordingly, our estimates capture the
direct effect of AIO on traffic referred by external search engines. The total effect on Wikipedia traffic could
be larger if lost search visits also result in fewer internal referrals.
Publisher monetization and content supply. Wikipedia does not monetize its traffic through advertising
or subscriptions, but many publishers rely directly on search-originated visits for advertising impressions,
subscription acquisition, lead generation, and commerce. For these publishers, a decline in search traffic
reduces both immediate monetization opportunities and the number of users entering the top of the conversion
funnel.
    To illustrate the potential advertising implications, we assume that each foregone search visit corresponds
to one foregone landing-page view and apply a page-revenue range of approximately $8.99–$30.81 per
thousand page views. We derive this range using an average of 5.22 display-ad opportunities per page, fill rates
of 75–90%, a 70% publisher revenue share, and CPMs of $3.28–$9.37 (Zeng et al. 2020; Google Ad Manager
Help n.d.; Playwire 2026; Association of National Advertisers (ANA) 2025). Applying these benchmarks to
the estimated traffic reduction yields an illustrative advertising-revenue equivalent of approximately $0.901M–
$3.090M per month, or $10.82M–$37.08M per year if the estimated monthly effect persisted. These figures
illustrate the potential monetization consequences for an ad-supported publisher experiencing a traffic decline
of the estimated magnitude. Web Appendix §F reports the complete calculation and assumptions.
7 Internal article-to-article referrals account for roughly 40% of the overall Wikipedia traffic (Piccardi et al. 2023).




                                                                   11
    Traffic displacement may also affect the long-run supply of content even when a publisher does not
monetize visits directly. Prior research on Wikipedia suggests that greater audience reach and article popularity
can influence contributors’ incentives to produce and maintain content (Zhang and Zhu 2011; Champion
and Hill 2025). By reducing the audience reaching source pages, answer engines may weaken the visibility,
recognition, and other benefits that motivate content production. This creates a potential feedback loop:
search platforms use publisher content to generate answers, but those answers may reduce the traffic and
incentives that support the production and maintenance of that content. Our analysis does not estimate this
longer-run response, but the traffic displacement that we document identifies an important first step in that
mechanism.
Intermediary design and welfare. Our findings highlight a fundamental difference between link-based
aggregation and answer-producing intermediation. Traditional search engines and news aggregators primarily
lower discovery costs and route users to upstream content. Consistent with this mechanism, prior research
often finds that link-based aggregation complements publisher consumption (Chiou and Tucker 2017;
Calzada and Gil 2020; Athey et al. 2021). AIO changes the intermediary’s role by synthesizing the underlying
information and presenting an answer before the organic links. By satisfying some users’ information needs
directly, the intermediary can substitute for a visit to the source rather than merely facilitate it.
    The negative effects that we estimate are particularly notable because Wikipedia is among the sources
most frequently cited in AI-generated summaries (Harsel et al. 2025). These citations may direct some
users to Wikipedia, but our estimates indicate that any resulting traffic did not offset the average decline
associated with the introduction of AIO. More generally, the results suggest that an intermediary can shift
from complementing upstream content to substituting for source-page visits when it moves from organizing
links to producing answers.
    The observed traffic displacement does not, by itself, imply that AIO reduces overall welfare. Answer-first
search may lower users’ search costs, provide faster access to information, and direct users who do click to
more relevant pages (Reid 2024b, 2025). Our design measures publisher traffic rather than consumer surplus,
answer quality, or the value of users’ time. The results thus highlight an ecosystem level tradeoff: the same
interface that improves the immediate efficiency of information retrieval may shift attention away from the
publishers that produce and maintain the underlying information. The long-run welfare effects therefore
depend not only on users’ short-run benefits but also on how reduced traffic changes publishers’ incentives to
supply high-quality content.
Platform and policy implications. Our findings also raise broader questions about market power, attribu-
tion, and the governance of AI-mediated information markets. Search platforms control the interface through
which users discover content and can reallocate traffic through product-design changes that publishers cannot
directly control.8 As more discovery and consumption take place within search and AI platforms, these
8 Beyond search, evidence from standalone AI chatbots points to a similar, although heterogeneous, reallocation of attention: LLM

 adoption reduces traditional search and disproportionately reduces browsing to smaller websites (Padilla et al. 2025), while ChatGPT
 reduced participation and question production on Stack Overflow (Burtch et al. 2024; del Rio-Chanona et al. 2024).



                                                                12
platforms also retain a larger share of user-interaction data, measurement feedback, and monetization oppor-
tunities. These changes can deepen publishers’ dependence on platform-controlled ranking, advertising, and
attribution systems, reinforcing longstanding concerns about digital gatekeepers (Greenstein 2010; Goldfarb
and Tucker 2019).
    Our results highlight the value of greater transparency about AIO exposure, source attribution, and
downstream traffic effects. They also motivate the design of mechanisms that preserve incentives to produce
content while allowing users to benefit from AI-generated summaries. Potential approaches include effective
publisher controls, auditable traffic reporting, compensation or revenue-sharing arrangements, and attribution
systems that value individual sources’ contributions to generated answers, e.g., through Shapley-based
attribution systems (Ye and Yoganarasimhan 2025). Recent regulatory debates over publisher opt-outs and
litigation concerning the use of publisher content in AI summaries reflect these broader tensions (Davies and
Guaglione 2026; Reuters 2026). As search platforms increasingly produce answers rather than merely rank
links, the design of these mechanisms will become central to sustaining both efficient information access and
the upstream content on which it depends.
5   Conclusion
Generative AI is changing search engines from intermediaries that organize links into systems that answer
users’ questions within the search interface. We study the publisher-side consequences of this shift by
combining Google’s staggered rollout of AI Overviews with Wikimedia’s article-level clickstream data.
Comparing English Wikipedia articles with the same articles in German and French, we find that default AIO
availability reduced monthly English search traffic by approximately 5.45% relative to German and 4.82%
relative to French.
    Our findings imply that generative-answer features such as AIO in search engines can materially reallocate
attention away from publisher pages, even when it cites and links to that content. Although this shift may
lower users’ search costs and improve access to information, it can also reduce publishers’ monetization
opportunities and weaken the incentives that sustain the underlying content ecosystem. As digital interme-
diaries increasingly produce answers rather than merely organize links, preserving the incentives to create
and maintain the content on which those answers rely will become central to the economics of AI-mediated
information.




                                                     13
References
S. Agarwal and A. Sen. The impact of google ai overviews on publisher traffic and user experience: Evidence from a
   field experiment. 2026.
J. D. Angrist and J.-S. Pischke. Mostly Harmless Econometrics: An Empiricist’s Companion. Princeton University
   Press, 2009.
Association of National Advertisers (ANA). Programmatic transparency benchmark report (q1 2025). https:
   //tinyurl.com/4jc4r2pm, 2025.
S. Athey, M. Mobius, and J. Pal. The impact of aggregators on internet news consumption. Technical report, National
   Bureau of Economic Research, 2021.
M. Bertrand, E. Duflo, and S. Mullainathan. How much should we trust differences-in-differences estimates? The
   Quarterly Journal of Economics, 119(1):249–275, 2004.
BrightEdge. 10 observations about AI overviews after a full month. https://www.brightedge.com/blog/
   10-observations-AI-Overviews-June2024, 2024.
H. Budaraju. New ways to connect to the web with AI overviews. https://tinyurl.com/mr2zme39, August
   2024. Accessed: 2025-12-19.
G. Burtch, D. Lee, and Z. Chen. The consequences of generative ai for online knowledge communities. Scientific
   Reports, 14(1):10413, 2024.
J. Calzada and R. Gil. What do news aggregators do? evidence from google news in spain and germany. Marketing
   Science, 39(1):134–167, 2020.
A. C. Cameron, J. B. Gelbach, and D. L. Miller. Robust inference with multiway clustering. Journal of Business &
   Economic Statistics, 29(2):238–249, 2011.
K. Champion and B. M. Hill. Countering underproduction of peer produced goods. New Media & Society, 27(9):
   5132–5150, 2025.
A. Chapekis and A. Lieb. Google users are less likely to click on links when an AI summary appears in the results. Pew
   Research Center, July 2025.
L. Chiou and C. Tucker. Content aggregation by platforms: The case of the news media. Journal of Economics &
   Management Strategy, 26(4):782–805, 2017.
J. Davies. Google ai overviews linked to 25% drop in publisher referral traffic, new data shows. https://tinyurl.
   com/4t7bfs99, August 2025.
J.      Davies      and     S.      Guaglione.                 Google’s       AI      opt-out     leaves    publishers
   with      a     choice      they     can’t    safely       use.                https://digiday.com/media/
   googles-ai-opt-out-leaves-publishers-with-a-choice-they-cant-safely-use/,
   June 2026.
R. M. del Rio-Chanona, N. Laurentsyeva, and J. Wachs. Large language models reduce public knowledge sharing on
   online q&a platforms. PNAS nexus, 3(9):pgae400, 2024.
L. Edmonds. Reddit Is the 2nd Most-Cited Source in Google AI Overviews, but That Might Not Mean Much for
   Its Bottom Line. https://tinyurl.com/4b78f2mu, June 2025. Yahoo Finance; originally published by
   Business Insider. Accessed July 18, 2026.
R. Fletcher and R. K. Nielsen. Automated serendipity: The effect of using search engines on news repertoire balance
   and diversity. Digital Journalism, 6(8):976–989, 2018.
A. Goldfarb and C. Tucker. Digital economics. Journal of economic literature, 57(1):3–43, 2019.
Google. More opportunities for your business on google search. https://tinyurl.com/2snbhp7x, May 2025.


                                                         14
   Accessed: 2026-01-15.
Google Ad Manager Help. Ad manager report metrics. https://tinyurl.com/5s38x8my, n.d. Defines total
   fill rate as total impressions divided by total ad requests. Accessed July 15, 2026.
S. Greenstein. Gatekeeping economics. IEEE Micro, 30(5):102–104, 2010.
L. Harsel, A. Drozdov, and C. Skopec. The most-cited domains in ai: A 3-month study. https://tinyurl.com/
   463t7evc, 2025. Semrush blog post, published November 10, 2025.
Interactive Advertising Bureau (IAB). Digital ad revenue surges 15% yoy in 2024, climbing to $259b, according to iab.
   IAB news release (conducted by PwC), April 2025. Accessed 2025-12-20.
Y. Khromova and V. Ivanna. AI overviews research: Comparing pre and post-rollout results on 100k keywords.
   https://tinyurl.com/3z59d95a, 2024.
F. Lemmerich, D. Sáez-Trumper, R. West, and L. Zia. Why the world reads wikipedia: Beyond english speakers. In
   Proceedings of the twelfth ACM international conference on web search and data mining, pages 618–626, 2019.
B. McConnell. Can’t see the forest for the logs: on the perils of using difference-in-differences with a log-dependent
   variable, 2024.
M. Miller. New user trends on wikipedia. https://tinyurl.com/3r8k9ysa, October 2025.
V. Miz, J. Hanna, N. Aspert, B. Ricaud, and P. Vandergheynst. What is trending on wikipedia? capturing trends and
   language biases across wikipedia editions. In Companion proceedings of the Web conference 2020, pages 794–801,
   2020.
R. K. Nielsen and R. Fletcher. Concentration of online news traffic and publishers’ reliance on platform referrals:
   Evidence from passive tracking data in the uk. Journal of Quantitative Description: Digital Media, 2, 2022.
N. Padilla, H. T. Lam, A. Lambrecht, and B. Hollenbeck. The impact of llm adoption on online user behavior. Available
   at SSRN, 2025.
T. Piccardi, M. Gerlach, A. Arora, and R. West. A large-scale characterization of how readers browse wikipedia. ACM
   Transactions on the Web, 17(2):1–22, 2023.
Playwire. State of publisher ad revenue 2026: Insights and opportunities. Technical report, Playwire, 2026. URL
   https://tinyurl.com/2s32r2rd.
E. Reid. Supercharging search with generative AI. https://tinyurl.com/yc5xkbm3, May 2023.
E. Reid. AI overviews: About last week. https://blog.google/products-and-platforms/
   products/search/ai-overviews-update-may-2024/, May 2024a.
E. Reid. Generative AI in search: Let Google do the searching for you. https://tinyurl.com/4y3ehssc,
   May 2024b.
E. Reid. AI in search: Driving more queries and higher quality clicks. https://tinyurl.com/ykk2ucf2,
   August 2025.
Reuters. Google defends ai search summaries against publishers’ lawsuit. https://tinyurl.com/43zy2abk,
   Jan. 2026. Reuters Legal, accessed January 2026.
B. Schwartz. Google Rolls Out AI Overviews In EU Regions. https://searchengineland.com/
   google-rolls-out-ai-overviews-in-eu-regions-453595, Mar. 2025. Search Engine Land. Ac-
   cessed August 22, 2026.
SemRush. Wikipedia traffic stats. https://www.semrush.com/website/wikipedia.org/overview/,
   2025.
Similarweb. Wikipedia website performance. https://www.similarweb.com/website/wikipedia.
   org/, 2025.



                                                         15
Similarweb, 2026.
Statista. Market share of leading search engines worldwide from january 2015 to december 2025. https://
   tinyurl.com/f46smwst, 2025. Accessed: 2026-01-19.
Statistics.           Distribution   of    search     engine     referrals    share    worldwide     from    january
   2015       to     june      2026.                https://www.statista.com/statistics/1381664/
   worldwide-all-devices-market-share-of-search-engines/?srsltid=
   AfmBOoqaLLZ-L0fBrBd0tOF4gVFl4rCKI1Ce4OfnQVGCavUDlS7IFLJR, 2026.
S. Stier, N. Kirkizh, C. Froio, and R. Schroeder. Populist attitudes and selective exposure to online news: A cross-
   country analysis combining web tracking and surveys. The International Journal of Press/Politics, 25(3):426–446,
   2020.
E. J. Tabuena. New ahrefs data outline how to optimize for ai overviews. https://tinyurl.com/2kwfy95z,
   2025. DesignRush News. Accessed: 2026-01-19.
S. Venkatachary. AI overviews in search are coming to more places around the world. https://tinyurl.com/
   mrx9xfkc, Octobor 2024.
Wikimedia Foundation. Wikipedia Clickstream. https://meta.wikimedia.org/wiki/Research:
   Wikipedia_clickstream, 2026. Documentation for the monthly public clickstream releases. Accessed July
   31, 2026.
Wikipedia. Languages used on the internet. https://tinyurl.com/ynwy2ajc, 2024.
Wikipedia. List of most-visited websites. https://tinyurl.com/4css9t5x, 2025a. Accessed: 22 January
   2026.
Wikipedia. Wikipedia:statistics. https://tinyurl.com/y32j75p6, 2025b. Accessed: 22 January 2026.
J. M. Wooldridge. Econometric analysis of cross section and panel data. MIT press, 2010.
Z. Ye and H. Yoganarasimhan. Fair document valuation in llm summaries via shapley values. arXiv preprint
   arXiv:2505.23842, 2025.
E. Zeng, T. Kohno, and F. Roesner. Bad news: Clickbait and deceptive ads on news and misinformation websites. In
   Workshop on Technology and Consumer Protection (ConPro ’20), 2020. Accessed: 2026-01-19.
P. Zhang, R. Cui, and D. J. Zhang. The impact of ai search on the online content ecosystem: Evidence from google and
   reddit. arXiv preprint arXiv:2605.16428, 2026.
X. Zhang and F. Zhu. Group size and incentives to contribute: A natural experiment at chinese wikipedia. American
   Economic Review, 101(4):1601–1615, 2011.




                                                        16
Appendix
A   Search Results Pages with and without AIO
In this section, we present two examples of Google’s search engine results (SERPs) without and with AIO.
As we can see in Figures A1 and A2, AIO pushes the top search results (including Wikipedia in this example)
down in the SERP.




                     Figure A1: A Google search result page without AIO for the query “e=mc2.”




                                                         i
Figure A2: A Google search result page with AIO for the query “e=mc2.”




                                  ii
B     Parallel Pre-Treatment Trends
The main assumption in our difference-in-difference specification is that the treatment and control articles
would have parallel trends absent the AIO treatment. In this section, we examine this parallel-trends assump-
tion for the pairwise samples of English vs. German and French control languages using linear pre-treatment
tests, dynamic event studies, Honest DiD sensitivity analysis, and linear counterfactual extrapolations.
B.1    Linear Pre-Treatment Tests
As a simple parametric check, we estimate a PPML differential-trend model using the set of five pre-treatment
months, denoted as Mpre , for estimation, December 2023–April 2024. For each sample, we estimate:

                                                                              m ∈ Mpre .
                                                                          
                 E[Ri,l,m | αi,l , δm ] = exp αi,l + δm + ηc Englishl × tm ,                             (A1)

Here, tm is a linear month index within the pre-treatment estimation period. Similar to our main two-way
fixed-effects (TWFE) specification, αi,l and δm denote article-language and month fixed effects, respectively.
For control c, the coefficient ηc captures whether English search traffic was already drifting linearly relative
to that control-language edition before treatment. Under the parallel-trends benchmark, we expect ηc ≈ 0.
Table A1 reports the results of this test.

                                   Table A1: PPML linear pre-treatment trend tests

                                                               German     French
                                  English ×tm                  −0.0014 0.0028
                                                                (0.0035) (0.0076)
                                  No. observations             4,999,270 5,308,730
                                  Articles (QIDs)               499,927 530,873
                                  Article × language FE          Yes       Yes
                                  Month FE                       Yes       Yes
                                   Robust standard errors in parentheses are two-
                                  way clustered by article and month.
                                   Significance: ∗∗∗ p < 0.001, ∗∗ p < 0.01, ∗ p <
                                  0.05.

    The estimated monthly differential slopes are −0.0014 for German and 0.0028 for French. Neither
is statistically different from zero under the two-way-clustered inference. We next use the event-study
specification to assess dynamic deviations that a single linear slope can miss.
B.2    PPML Event Studies
The DiD specification summarizes the post-treatment period with a single average effect. We also estimate a
pooled event-study that replaces Postm with event-month interactions:
                                                                                         !
                                                                                       
               E[Ri,l,m | αi,l , δm ] = exp αi,l + δm + ∑ βc,r Englishl × 1{m = r} ,                  (A2)
                                                         r∈M \{m0 }

where M is the set of event months and m0 = −1 is the omitted reference month (April 2024), and May
2024 is the event month. For control c, each βc,r measures the English-versus-control difference in event
month r relative to April. Figure A3 reports the German and French estimates through December 2024.


                                                         iii
                                           English–German                                           English–French
                          .05                                                       .05
Event-study coefficient


                            0                                                        0


                          -.05                                                  -.05


                           -.1                                                      -.1


                          -.15                                                  -.15
                                 −5   −3     −1 0   1        3   5         7              −5   −3   −1    0   1        3   5    7
                                               Event Month                                               Event Month

Figure A3: Monthly PPML event-study estimates through December 2024 for the English–German and English–French samples.
April 2024 is the omitted reference month and May 2024 is event month zero. Pointwise 95% confidence intervals use two-way-
clustered standard errors.


    Figure A3 shows pre-treatment fluctuations that the linear tests do not capture. Although some of the
pre-treatment coefficients have 95% confidence intervals that do not include zero, three observations make the
violations less concerning. In the English-German sample, the violations are more fluctuations around zero,
which do not represent a negative pre-treatment trend. In the English-French sample, the violations exhibit
a pre-treatment positive trend that runs counter to our estimated negative treatment effect. This makes our
estimation a lower bound for the effect’s magnitude. Finally, the magnitude of the pre-treatment violations is
much smaller than the magnitude of the post-treatment coefficient, making the overall results less sensitive to
these deviations from the parallel pre-treatment trends. Nevertheless, we use Honest DiD in the next section
to report how sensitive the average post-treatment conclusion is to deviations calibrated from the observed
pre-period.
B.3                         Honest DiD Sensitivity under Relative-Magnitude Restrictions
As we discussed in the previous section, several pre-treatment event-study coefficients are close to, but
statistically different from, zero. We therefore use the Honest DiD framework of Rambachan and Roth (2023)
to examine the sensitivity of our conclusions to violations of the parallel-trends assumption. Following their
notation, we decompose each sample event-study coefficient as

                                                                     βc,r = τc,r + δc,r ,                                      (A3)

where τc,r is the causal effect in event month r and δc,r is the differential trend between English and control
language c that would have occurred absent treatment. Under no anticipation, τc,r = 0 in the pre-treatment
period, so the pre-treatment coefficients identify the corresponding differential trends. The omitted reference
month, April, 2024 here, is m0 = −1, with δc,m0 = 0 by normalization.
    We use the relative-magnitude restriction, ∆RM (M̄), as the observed pre-treatment deviations appear
primarily as fluctuations around zero rather than as a stable, negative differential trend. A restriction
calibrated to the magnitude of adjacent pre-treatment changes is therefore more natural in this setting. Let




                                                                               iv
Mpre
 0 =M
      pre ∪ {m0 }. The relative-magnitude restriction requires

                                                |δc,r − δc,r−1 | ≤ M̄ max |δc,s − δc,s−1 | ,          r ∈ Mpost .                      (A4)
                                                                         0
                                                                     s∈Mpre
                                                                           0
                                                                    s−1∈Mpre


Thus, M̄ bounds each adjacent post-treatment change in the counterfactual differential trend relative to
the largest adjacent pre-treatment change, including the change into the normalized reference month. For
instance, M̄ = 0.3 allows each post-treatment change to be at most 30% as large as the largest corresponding
pre-treatment change. In this way, Honest DiD constructs confidence intervals for the equally weighted
May–December 2024 average, accounting for sampling uncertainty in both the pre-treatment differential
trends and the post-treatment event-study estimates. Figure A4 reports the relative-magnitude ∆RM intervals.

                                       English–German                                                  English–French
      95% robust CI




                        0                                                                 0
                      -.05                                                            -.05
                                                                                        -.1
                       -.1                                                            -.15
                        Original 0         .1       .2      .3     .4        .5          Original 0     .1      .2      .3        .4   .5
                                                   Mbar                                                        Mbar

Figure A4: Honest DiD sensitivity intervals under relative-magnitude (∆RM ) restrictions for German and French controls. The target
is the equally weighted average post-treatment effect over May–December 2024, using the original PPML event-study covariance
matrices.

    For the German comparison, the robust interval remains below zero through M̄ = 0.40, and for the French
comparison, it remains below zero through M̄ = 0.35. Considering eight post-treatment periods, each with
the possibility of deviating by 0.4 or 0.35 or the largest pre-treatment deviation, these M̄ values represent
considerable robustness in our results.
B.4                   Linear Extrapolation of Pre-Treatment Event-Study Coefficients
As a complementary diagnostic, we utilize a linear extrapolation method in this section. In our linear
extrapolation method, we fit a straight line to the pre-treatment event-study coefficients using OLS and WLS
methods, extrapolate it to the post-treatment period as the counterfactual trend, and compare the resulting
post-treatment mean with the post-treatment event-study coefficients’ mean. Let β̂c,r denote the estimated
English-control event-study coefficient for control language c in event month r. Using only the pre-treatment
event months, we fit
                               β̂c,r = ωc (r − m0 ) + uc,r ,   r ∈ Mpre \ {m0 },                         (A5)
where Mpre is the set of pre-treatment event months, m0 = −1 is the omitted April 2024 reference month, ωc
is the pre-treatment slope in PPML log points per event month for control c, and uc,r is the corresponding
fitting residual. Because the event-study normalization implies β̂c,m0 = 0, Equation (A5) has no free intercept:
the line is anchored at (m0 , 0). We estimate the equation separately for the German and French controls.
     The fitted counterfactual path in a post-treatment event month r ∈ Mpost is β̂c,r  cf = ω̂ (r − m ). We
                                                                                               c        0
therefore report three post-treatment quantities

                                         1                            cf      1                                              cf
                             βb̄ c =              ∑ β̂c,r ,
                                       |Mpost | r∈M
                                                                  βb̄ c =              ∑ ω̂c (r − m0 ),
                                                                            |Mpost | r∈M
                                                                                                               bc = βb̄ − βb̄ .
                                                                                                               ∆       c     c         (A6)
                                                   post                                 post




                                                                                  v
                                                   cf
Here βb̄ c is the factual post-treatment mean, βb̄ c is the counterfactual mean by extrapolating the fitted pre-
treatment line, and ∆ bc is their difference. We report two estimators of Equation (A5): ordinary least squares
(OLS), which weights the pre-treatment coefficients equally, and weighted least squares (WLS), which uses
                                                                                          cf
inverse marginal-variance weights. For each estimator, Table A2 reports ω̂c , βb̄ c , βb̄ c , and ∆
                                                                                                  bc .
    For both controls and both fitting methods, the factual post-treatment mean is significantly below the
extrapolated counterfactual mean. The estimated differences are −0.0510 (German, OLS), −0.0505 (German,
WLS), −0.1163 (French, OLS), and −0.1100 (French, WLS). This diagnostic is consistent with a negative
post-AIO shift under a linear continuation of the pre-treatment differential.
    Figures A5 and A6 plot the monthly event-study estimates together with the fitted OLS and WLS
pre-treatment paths and their post-treatment counterfactual continuations.

                                               English-German                                                     English-French
                                                                     Pre-treatment line
                                                                     Counterfactual line        .05
   Event study coefficient




                               0

                                                                                                  0
                             -.04

                                                                                                -.05
                             -.08
                                                                                                 -.1

                             -.12
                                    −5   −3   −1    0   1        3           5         7               −5   −3   −1    0   1        3   5   7
                                                   Event Month                                                        Event Month


Figure A5: OLS linear extrapolations of the pre-treatment event-study coefficients. Black points and blue whiskers report the monthly
PPML estimates and 95% confidence intervals. The solid red line is fitted to the four nonreference pre-treatment coefficients and
anchored at the omitted April 2024 coefficient; the dashed red line is its May–December counterfactual continuation. The dotted
gray line marks May 2024.




                                                                                           vi
                                                 English-German                                                         English-French
                                                                         Pre-treatment line
                                                                         Counterfactual line      .05
   Event study coefficient


                               0

                                                                                                    0
                             -.04
                                                                                                  -.05

                             -.08
                                                                                                   -.1

                             -.12
                                    −5    −3    −1    0    1         3           5         7             −5    −3     −1    0   1        3   5    7
                                                     Event Month                                                           Event Month


Figure A6: WLS linear extrapolations of the pre-treatment event-study coefficients. Black points and blue whiskers report the
monthly PPML estimates and 95% confidence intervals. The solid red line uses inverse marginal-variance weights for the four
nonreference pre-treatment coefficients and is anchored at the omitted April 2024 coefficient; the dashed red line is its May–December
counterfactual continuation. The dotted gray line marks May 2024.


                                                Table A2: Linear extrapolations of pre-treatment event-study coefficients

                                Control   Method     Pre-trend slope          Factual post mean          Counterfactual post mean    Difference
                                German    OLS             −0.0009                    −0.0552∗∗∗                 −0.0042             −0.0510∗∗∗
                                                          (0.0013)                    (0.0039)                  (0.0057)             (0.0079)
                                          WLS             −0.0010                    −0.0552∗∗∗                 −0.0046             −0.0505∗∗∗
                                                          (0.0013)                    (0.0039)                  (0.0057)             (0.0078)
                                French    OLS             0.0092∗∗∗                  −0.0748∗∗∗                 0.0414∗∗∗           −0.1163∗∗∗
                                                           (0.0012)                   (0.0040)                   (0.0052)            (0.0072)
                                          WLS             0.0078∗∗∗                  −0.0748∗∗∗                 0.0352∗∗∗           −0.1100∗∗∗
                                                           (0.0011)                   (0.0040)                   (0.0049)            (0.0070)
 Notes: Estimates are PPML log coefficients. OLS gives equal weight to the four nonreference pre-treatment
 coefficients, and WLS uses inverse marginal-variance weights. The fitted line is anchored at the omitted April 2024
 reference month. “Difference” is the factual May–December 2024 mean minus the extrapolated counterfactual
 mean. Standard errors computed using the unaltered event-study covariance matrix are in parentheses. ∗∗∗ p < 0.001,
 ∗∗ p < 0.01, ∗ p < 0.05.




                                                                                           vii
C    Sensitivity to Post-Treatment Censoring Assignment
The main analysis addresses unpublished post-treatment counts by setting an unpublished English count to
10, and an unpublished control count to 0. This assignment moves censored outcomes against a negative
English effect. To assess how strongly the estimates depend on that choice, we run the PPML regression
in Equation (1) on three alternative imputation procedures: we first reverse the assignment for censored
post-treatment observations, setting an unpublished English count to 0 and an unpublished control count to
10. Alternatively, we assign censored observations a value of 10 in both the English and control editions, or
assign a value of 0 in both editions. Table A3 reports the main and alternative assignment estimates.

                  Table A3: PPML DiD estimates under alternative post-treatment censoring assignments

                                             German                        French
                  Panel A: Main assignment: unpublished English count 10; control count 0
                  English × post        −0.0561∗∗∗                −0.0494∗∗∗
                                         (0.0117)                   (0.0136)
                  Panel B: Opposite assignment: unpublished English count 0; control count 10
                  English × post         −0.0566∗∗∗                −0.0502∗∗∗
                                          (0.0117)                   (0.0136)
                  Panel C: Symmetric zero assignment: unpublished counts 0 in both languages
                  English × post         −0.0561∗∗∗                −0.0494∗∗∗
                                          (0.0117)                  (0.0136)
                  Panel D: Symmetric ten assignment: unpublished counts 10 in both languages
                  English × post         −0.0566∗∗∗                −0.0502∗∗∗
                                          (0.0117)                  (0.0136)
                  No. observations          12,998,102                   13,802,698
                  Articles (QIDs)            499,927                      530,873
                  Article × language FE         Yes                          Yes
                  Month FE                      Yes                          Yes
                   Published counts are unchanged under both assignments. Robust standard errors
                  in parentheses are two-way clustered by article and month.
                   Significance: ∗∗∗ p < 0.001, ∗∗ p < 0.01, ∗ p < 0.05.

    Under every assignment, the estimates imply a near 5.5% decline relative to German and a near 4.9%
decline relative to French. All estimates are statistically significant. The negative direction therefore does not
depend on which of the two directional assignments we use.




                                                         viii
D   Pre-Treatment Timing Placebo
In this section, we run a placebo analysis to check whether moving the treatment date to two months earlier
and using only the pre-treatment period (December 2023–April 2024) yields similar negative estimates. We
define PlaceboPostm to equal one in March and April 2024 (placebo post-treatment period) and zero from
December 2023 through February 2024 (placebo pre-treatment period). We then estimate

                     E[Ri,l,m | αi,l , δm ] = exp αi,l + δm + βcP Englishl × PlaceboPostm ,
                                                                                         
                                                                                                      (A7)

separately for each c ∈ {DE, FR}. The article–language and month fixed effects are identical to those in
Equation (1). The coefficient βcP measures whether English search traffic changed relative to control c after
the placebo March onset.
    If the main estimates capture a post-AIO shift rather than an existing English–control divergence, βcP
should be close to zero. A negative placebo estimate would instead indicate that the relative decline had
already begun before May. Because sample membership requires published counts in all five months, this
exercise tests timing within the retained sample. Table A4 reports the placebo estimates.

                                Table A4: Pre-treatment timing-placebo PPML DiD
                                estimates

                                                           German     French
                                 English × placebo post −0.0026 0.0162
                                                         (0.0094) (0.0179)
                                 No. observations       4,999,270 5,308,730
                                 Articles (QIDs)         499,927 530,873
                                 Article × language FE      Yes         Yes
                                 Month FE                   Yes         Yes
                                The placebo pre-period is December 2023–
                                February 2024, and the placebo post-period is
                                March–April 2024. Robust standard errors in
                                parentheses are two-way clustered by article
                                and month.
                                 Significance: ∗∗∗ p < 0.001, ∗∗ p < 0.01, ∗ p <
                                0.05.

   The placebo estimates imply a 0.26% decline relative to German and a 1.6% increase relative to French.
Neither estimate is statistically significant. Thus, the timing falsification provides no evidence that the
negative English-relative-control shift began before the actual treatment period.




                                                      ix
E     English–Japanese Analysis Through July 2024
In this section, we report the English–Japanese comparison separately from the two main control comparisons.
Japan entered Google’s public AIO expansion in August 2024 (Budaraju 2024); ending the outcome window
in July therefore keeps this comparison entirely before that expansion. The sample-membership and post-
treatment censoring rules are otherwise identical to the main analysis: both editions must have published
counts in every pre-treatment month, and post-treatment publication does not affect eligibility. All descriptive
outcomes, model-free series, and estimates reported below use December 2023–July 2024. The resulting
sample contains 315,054 matched English–Japanese article pairs.
E.1    Summary Statistics and Model-Free Series
Table A5 reports the pre-treatment (December 2023–April 2024) and post-treatment (May–July 2024)
distributions of monthly article-level search traffic in the English–Japanese sample.

         Table A5: Summary statistics of monthly search traffic for the English–Japanese sample through July 2024.


                                    Pre-treatment months (Dec. 2023–Apr. 2024)
                                   Statistic         English (EN–JA)       Japanese
                                   Mean               5,836.47       926.30
                                   Std.              31,743.35     5,530.86
                                   Min.                 10.00         10.00
                                   25%                 253.00         45.00
                                   50%                1,034.00       133.00
                                   75%                3,865.00       503.00
                                   Max.            12,503,258.00 1,580,324.00
                                   Articles (QIDs)    315,054       315,054
                                    Post-treatment months (May 2024–Jul. 2024)
                                   Statistic         English (EN–JA)       Japanese
                                   Mean                   4,946.87          940.54
                                   Std.                  24,905.92        4,835.75
                                   Min.                     10.00             0.00
                                   25%                     215.00            48.00
                                   50%                     885.00           145.00
                                   75%                    3,310.00          547.00
                                   Max.                8,113,164.00     1,039,675.00
                                   Articles (QIDs)        315,054          315,054

    Figure A7 applies the same model-free transformation as Figure 1: total search traffic in each language is
transformed using log(1 + R) and demeaned by the language-specific December 2023–April 2024 mean.




                                                            x
                                                       English–Japanese




Figure A7: Demeaned log of total monthly search traffic through July 2024 for the English–Japanese sample. Each series is demeaned
using December 2023–April 2024; the dashed line marks May 2024.


E.2    PPML Difference-in-Differences Estimate
We estimate Equation (1) on the English–Japanese sample through July 2024. The coefficient of −0.1806
implies that monthly English Wikipedia search traffic declined by approximately 16.53% relative to Japanese
beginning in May 2024. Table A6 reports the coefficient and two-way-clustered standard error.

                                            Table A6: English–Japanese PPML DiD
                                            estimate through July 2024

                                                                         Japanese
                                             English × post            −0.1806∗∗∗
                                                                        (0.0110)
                                             No. observations          5,040,864
                                             Articles (QIDs)            315,054
                                             Article × language FE          Yes
                                             Month FE                       Yes
                                             Robust standard errors in parenthe-
                                            ses are two-way clustered by article
                                            and month.
                                             Significance: ∗∗∗ p < 0.001, ∗∗ p <
                                            0.01, ∗ p < 0.05.

E.3    Parallel-Trends and Sensitivity Diagnostics
In this section, we apply the same sequence of diagnostics as in Web Appendix §B to assess the parallel
trends assumption on the English-Japanese sample.
Linear pre-treatment test. Table A7 reports the PPML differential linear trend over the five pre-treatment
months. The estimated coefficient is negative but statistically insignificant, representing no differential trend
over time between the search traffic to English and Japanese articles.


                                                               xi
                                                              Table A7: English–Japanese PPML lin-
                                                              ear pre-treatment trend test

                                                                                       Japanese
                                                              English ×tm             −0.0020
                                                                                       (0.0049)
                                                              No. observations        3,150,540
                                                              Articles (QIDs)          315,054
                                                              Article × language FE        Yes
                                                              Month FE                     Yes
                                                               Robust standard errors in parenthe-
                                                              ses are two-way clustered by article
                                                              and month.
                                                               Significance: ∗∗∗ p < 0.001, ∗∗ p <
                                                              0.01, ∗ p < 0.05.


Event-study analysis. Figure A8 reports the monthly event-study coefficients through July 2024, with
April 2024 omitted and May 2024 defined as event month zero. The estimated coefficients are close to
zero, and in cases where the 95% confidence intervals do not include zero, the deviations are much smaller
compared to the post-treatment effect. Next, we present the relative-magnitude Honest DiD results to assess
the sensitivity of the English-Japanese PPML difference-in-differences result to deviations from pre-treatment
parallel trends.
                                                                      English–Japanese
                                                   .1
                         Event-study coefficient




                                                    0


                                                   -.1


                                                   -.2


                                                   -.3
                                                         −5   −4      −3      −2      −1         0   1   2
                                                                            Event Month
Figure A8: Monthly PPML event-study estimates through July 2024 for the English–Japanese sample. April 2024 is the omitted
reference month and May 2024 is event month zero. Pointwise 95% confidence intervals use two-way-clustered standard errors.


Honest DiD. Figure A9 reports Honest DiD intervals under the relative-magnitude restriction in Equa-
tion (A4). The target is the equally weighted May–July 2024 average. All the 95% confidence intervals are
below zero, showing the relative robustness of the negative result in Table A6



                                                                              xii
                                                                                            English–Japanese
                                                                         0




                                                     95% robust CI
                                                                     -.05
                                                                       -.1
                                                                     -.15
                                                                       -.2
                                                                         Original 0               .1                  .2                             .3        .4       .5
                                                                                                               Mbar
Figure A9: Honest DiD sensitivity intervals under relative-magnitude (∆RM ) restrictions for the Japanese control. The target is the
equally weighted average post-treatment effect over May–July 2024, using the original PPML event-study covariance matrix.


Linear Counterfactual Extrapolation Figures A10a and A10b report the corresponding OLS and WLS
pre-treatment paths and their May–July counterfactual continuations for the English–Japanese comparison.

                                                  English-Japanese                                                                                                   English-Japanese
                            .06                                                   Pre-treatment line                                     .06                                                Pre-treatment line
                                                                                  Counterfactual line                                                                                       Counterfactual line
  Event study coefficient




                                                                                                               Event study coefficient
                              0                                                                                                            0


                            -.06                                                                                                         -.06


                            -.12                                                                                                         -.12


                            -.18                                                                                                         -.18

                                   −5   −4   −3      −2                −1     0         1         2                                             −5        −4    −3      −2     −1       0         1         2
                                                    Event Month                                                                                                        Event Month

                                                  (a) OLS                                                                                                            (b) WLS

Figure A10: Linear extrapolations for the English–Japanese comparison through July 2024. Black points and blue whiskers report the
monthly PPML estimates and 95% confidence intervals. The solid red line is fitted to the four nonreference pre-treatment coefficients
and anchored at the omitted April 2024 coefficient, using equal weights in panel (a) and inverse marginal-variance weights in panel
(b); the dashed red line is its May–July counterfactual continuation. The dotted gray line marks May 2024.

    Finally, Table A8 fits the pre-treatment event-study coefficients using the anchored OLS and WLS
specifications in Equations (A5)–(A6) and compares the factual May–July average with the extrapolated
counterfactual average.
    For both fitting methods, the factual post-treatment mean is significantly below the extrapolated coun-
terfactual mean. The estimated differences are −0.1577 (OLS) and −0.1541 (WLS). This diagnostic is
consistent with a negative post-AIO shift under a linear continuation of the pre-treatment differential.




                                                                                                        xiii
                        Table A8: Linear extrapolations of pre-treatment event-study coefficients

       Control    Method     Pre-trend slope    Factual post mean      Counterfactual post mean     Difference
       Japanese   OLS          −0.0049∗             −0.1675∗∗∗                  −0.0098∗            −0.1577∗∗∗
                               (0.0022)              (0.0059)                   (0.0044)             (0.0085)
                  WLS         −0.0067∗∗∗            −0.1675∗∗∗                 −0.0134∗∗∗           −0.1541∗∗∗
                               (0.0018)              (0.0059)                   (0.0036)             (0.0073)
Notes: Estimates are PPML log coefficients. OLS gives equal weight to the four nonreference pre-treatment
coefficients, and WLS uses inverse marginal-variance weights. The fitted line is anchored at the omitted April
2024 reference month. “Difference” is the factual May–July 2024 mean minus the extrapolated counterfactual
mean. Standard errors computed using the unaltered event-study covariance matrix are in parentheses. ∗∗∗ p < 0.001,
∗∗ p < 0.01, ∗ p < 0.05.




                                                          xiv
F     Traffic and Advertising-Revenue Calculations
This section provides the calculations underlying the traffic and advertising-revenue benchmarks discussed
in Section 4. We use these calculations to illustrate the economic scale of the main estimates. Because we
estimate the English–German and English–French specifications on separately constructed article samples,
the calculations do not constitute a separate pooled causal estimate.
F.1   Implied Reduction in Direct Search Traffic
Table 2 reports the English–German and English–French PPML coefficients, β̂DE = −0.0561 and β̂FR =
−0.0494. To construct a single back-of-the-envelope benchmark, we take their arithmetic mean:

                                            1             
                                     β̂avg =   β̂DE + β̂FR = −0.0527.                                 (A8)
                                            2
    This coefficient corresponds to an average proportional decline of approximately 5.14%. We match this
                                                                     EN,DE      EN,FR
average coefficient with a corresponding average traffic base. Let T post and T post denote average monthly
English search traffic from May through December 2024 in the English–German and English–French samples,
respectively. We define

                      EN            1  EN,DE        EN,FR
                                                           
                     T post,avg =        T post + T post      ≈ 1.852 billion visits per month.    (A9)
                                    2
    The observed post-treatment traffic already incorporates the estimated decline. Under the multi-
plicative PPML model, the corresponding counterfactual traffic level absent the estimated effect equals
  EN
T post,avg exp(−β̂avg ). We therefore calculate the implied monthly traffic loss as
                                         h                 i
                    bmonth = T EN
                    L           post,avg  exp   −β̂avg   − 1   ≈ 100.27 million visits per month. (A10)

    Thus, the average of the two main estimates implies approximately 100.27 million fewer direct search-
originated visits to English Wikipedia each month. If the estimated monthly rate persisted for one year, the
corresponding annualized reduction would be

                                L         bmonth ≈ 1.20 billion visits per year.
                                byear = 12L                                                             (A11)
    The annualized value is an illustrative scenario rather than an estimate over an observed twelve-month
treatment period. It assumes that the average post-treatment effect persists despite subsequent changes
in AIO exposure, user behavior, and publisher responses. Moreover, the calculation includes only visits
referred directly by external search engines; it does not include any associated changes in subsequent internal
navigation within Wikipedia.
F.2   Illustrative Advertising-Revenue Equivalent
Wikipedia does not display advertising, so the estimated traffic reduction does not imply an advertising-
revenue loss for Wikipedia itself. To illustrate the potential scale for an otherwise comparable ad-supported
publisher, we assume that each foregone search referral corresponds to one foregone landing-page view and
apply benchmark display-ad revenues per page.
    Zeng et al. (2020) report an average of 5.22 display advertisements on mainstream news article pages,
which we use as an illustrative measure of ad opportunities per page. We assume a fill rate between 75% and
90%, where the fill rate denotes the share of ad requests that result in an impression (Google Ad Manager
Help n.d.). The upper portion of this range is consistent with benchmarks for publishers with relatively
strong advertising monetization (Playwire 2026). We further assume that publishers retain 70% of advertiser

                                                      xv
spending, close to the 73.9% seller-revenue share reported in the ANA programmatic-advertising benchmark
(Association of National Advertisers (ANA) 2025).
    The ANA benchmark reports median CPMs of $3.28 in the open marketplace and $9.37 in private
marketplaces (Association of National Advertisers (ANA) 2025). Because the benchmark covers multiple
delivery environments, including connected television, we treat these values as illustrative low and high
inputs rather than as general bounds for web-display CPMs.
    Combining the lower CPM with a 75% fill rate and the higher CPM with a 90% fill rate gives the
following publisher revenue per thousand page views:


                           Low page RPM = 5.22 × 0.75 × 0.70 × $3.28 ≈ $8.99,                               (A12)
                          High page RPM = 5.22 × 0.90 × 0.70 × $9.37 ≈ $30.81.                              (A13)

    For a page-RPM benchmark r, we calculate the monthly advertising-revenue equivalent as

                                                             L
                                                             bmonth
                                           d month (r) =
                                          ∆Rev                      × r.                                    (A14)
                                                             1,000
    Applying the low and high page-RPM benchmarks to the estimated monthly traffic loss yields

                                 d month ≈ $0.901M to $3.090M per month.
                                ∆Rev                                                                        (A15)
    If these monthly values persisted for one year, the corresponding annualized revenue equivalent would be

                                   d year ≈ $10.82M to $37.08M per year.
                                  ∆Rev                                                                      (A16)
    These calculations require several strong assumptions. In particular, we treat each foregone search referral
as one foregone page view, apply advertising benchmarks from other publishers to Wikipedia-scale traffic, and
assume that the estimated monthly traffic effect persists when we annualize the result. We also omit potential
effects on subscriptions, lead generation, commerce, and subsequent internal navigation. The resulting figures
should therefore be interpreted as illustrative advertising-revenue equivalents, not as estimates of Wikipedia’s
lost revenue or of revenue transferred from publishers to Google.
References
Association of National Advertisers (ANA). Programmatic transparency benchmark report (q1 2025). https:
   //tinyurl.com/4jc4r2pm, 2025.
H. Budaraju. New ways to connect to the web with AI overviews. https://tinyurl.com/mr2zme39, August
   2024. Accessed: 2025-12-19.
Google Ad Manager Help. Ad manager report metrics. https://tinyurl.com/5s38x8my, n.d. Defines total
   fill rate as total impressions divided by total ad requests. Accessed July 15, 2026.
Playwire. State of publisher ad revenue 2026: Insights and opportunities. Technical report, Playwire, 2026. URL
   https://tinyurl.com/2s32r2rd.
A. Rambachan and J. Roth. A more credible approach to parallel trends. Review of Economic Studies, 90(5):2555–2591,
   2023.
E. Zeng, T. Kohno, and F. Roesner. Bad news: Clickbait and deceptive ads on news and misinformation websites. In
   Workshop on Technology and Consumer Protection (ConPro ’20), 2020. Accessed: 2026-01-19.




                                                       xvi
