                                             Somesite I Used To Crawl: Awareness, Agency and Efficacy in
                                                   Protecting Content Creators From AI Crawlers
                                                                Enze Liu∗                                               Elisa Luo∗                                  Shawn Shan
                                                            e7liu@ucsd.edu                                          e4luo@ucsd.edu                         shansixiong@cs.uchicago.edu
                                                             UC San Diego                                            UC San Diego                             University of Chicago
                                                           La Jolla, CA, USA                                        La Jolla, CA, USA                            Chicago, IL, USA

                                                      Geoffrey M. Voelker                                             Ben Y. Zhao                                  Stefan Savage
                                                          voelker@ucsd.edu                                   ravenben@cs.uchicago.edu                             ssavage@ucsd.edu
arXiv:2411.15091v2 [cs.HC] 7 May 2025




                                                            UC San Diego                                        University of Chicago                               UC San Diego
                                                          La Jolla, CA, USA                                       Chicago, IL, USA                                 La Jolla, CA, USA

                                        Abstract                                                                                1    Introduction
                                        The success of generative AI relies heavily on training on data                         The success of generative AI relies heavily on training on data
                                        scraped through extensive crawling of the Internet, a practice                          scraped through extensive crawling of the Internet, a practice
                                        that has raised significant copyright, privacy, and ethical concerns.                   that has raised significant copyright, privacy, and ethical concerns.
                                        While few measures are designed to resist a resource-rich adversary                     Today, AI model trainers have unleashed large numbers of data
                                        determined to scrape a site, crawlers can be impacted by a range of                     crawlers on the Internet. By many reports, these crawlers now
                                        existing tools such as robots.txt, NoAI meta tags, and active crawler                   dwarf the volume of human traffic on the Internet, partly because
                                        blocking by reverse proxies.                                                            human users consume content at a much lower rate than crawlers.
                                           In this work, we seek to understand the ability and efficacy of                      For example, analysis by Akamai and Imperva suggest that roughly
                                        today’s networking tools to protect content creators against AI-                        50–70% of website traffic is due to automated crawlers [48, 109].
                                        related crawling. For targeted populations like human artists, do                       Other anecdotal evidence suggests that AI crawlers are effectively
                                        they have the technical knowledge and agency to utilize crawler-                        producing DDoS attacks on smaller websites [25, 26].
                                        blocking tools such as robots.txt, and can such tools be effective?                        While Internet crawling is well-studied, the widespread adoption
                                        Using large scale measurements and a targeted user study of 203 pro-                    of generative AI and its intensive data scraping has significantly
                                        fessional artists, we find strong demand for tools like robots.txt, but                 changed the landscape. Data creators and hosting platforms, who
                                        significantly constrained by critical hurdles in technical awareness,                   were generally ambivalent about having their content crawled in
                                        agency in deploying them, and limited efficacy against unrespon-                        the past, are now raising serious concerns about AI-related crawl-
                                        sive crawlers. We further test and evaluate network level crawler                       ing, particularly regarding copyright, privacy, and ethical practices.
                                        blockers provided by reverse proxies. Despite relatively limited de-                    Indeed, these concerns have manifested in over thirty ongoing
                                        ployment today, they offer stronger protections against AI crawlers,                    copyright lawsuits [68, 69, 112], multiple data strikes [34, 118], and
                                        but still come with their own set of limitations.                                       a surge in the adoption of anti-crawling tools [70].
                                                                                                                                   Given this new tension between AI training companies seeking
                                        CCS Concepts                                                                            training data and content creators who consider unauthorized AI
                                        • Information systems → Web crawling.                                                   training an existential threat to their livelihoods [31], a natural
                                                                                                                                question arises: What tools, if any, can content creators use to prevent
                                        Keywords                                                                                their content from being crawled for AI training? Answering this
                                                                                                                                question requires a more thorough understanding of the needs of
                                        Robots.txt; AI Crawlers; Web Content Control; Content Creators;
                                                                                                                                content creators; their awareness of, accessibility to, and agency
                                        ACM Reference Format:                                                                   over anti-crawling mechanisms; and ultimately, the availability and
                                        Enze Liu, Elisa Luo, Shawn Shan, Geoffrey M. Voelker, Ben Y. Zhao, and Ste-             efficacy of current tools.
                                        fan Savage. 2025. Somesite I Used To Crawl: Awareness, Agency and Ef-
                                                                                                                                   This paper presents our efforts to address these issues from
                                        ficacy in Protecting Content Creators From AI Crawlers. In Proceedings
                                                                                                                                several complementary perspectives. In terms of representative
                                        of the 2025 ACM Internet Measurement Conference (IMC ’25), October 28–
                                        31, 2025, Madison, WI, USA. ACM, New York, NY, USA, 22 pages. https:                    content creators, we focus on visual artists as the most vulnerable
                                        //doi.org/10.1145/3730567.3732913                                                       population being targeted by AI crawlers. In terms of anti-crawling
                                                                                                                                mechanisms, we focus on two tools at different ends of the spectrum.
                                        ∗ Equal contribution.
                                                                                                                                The most prominent and popular tool is robots.txt, a voluntary
                                                                                                                                (and non-enforceable) protocol that enables site owners to specify
                                                                                                                                crawling restrictions. We also consider crawler blocking by reverse
                                        This work is licensed under a Creative Commons Attribution 4.0 International License.   proxies (e.g., Cloudflare), an active approach that enforces blocking
                                        IMC ’25, Madison, WI, USA.                                                              but has seen limited deployment.
                                        © 2025 Copyright held by the owner/author(s).                                              We begin with a longitudinal analysis of robots.txt files across
                                        ACM ISBN 979-8-4007-1860-1/2025/10
                                        https://doi.org/10.1145/3730567.3732913                                                 the Web. Utilizing data from Common Crawl [24], we analyze the
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                                Enze Liu et al.


inclusion of directives that specifically target AI crawlers over        Some companies have developed their own crawlers for such pur-
time. This effort serves as broader context on how the arrival of        poses, and others rely upon third-party crawlers (e.g., Common
AI crawlers has changed views across the Web towards crawling.           Crawl [24]).
We then turn our attention to visual artists, and perform a user            Crawlers for augmenting AI-backed assistants (AI assistant crawlers).
study to understand their attitudes towards AI crawlers, and their       The second significant use of crawlers is to enhance AI-backed as-
awareness of and accessibility to defensive tools like robots.txt. We    sistants with additional information by fetching Web content in real
complement these results with measurements of 1100+ professional         time. For instance, ChatGPT-User is a crawler that can visit web-
artist websites to examine the hosting services artists use and levels   sites to fetch additional information when a user poses a question
of control these services provide. Next, we use sites under our          beyond ChatGPT training data. In such cases, the crawler retrieves
control to determine which AI crawlers respect robots.txt. Finally,      relevant content from the site and delivers it to the user. While some
we consider active crawler blocking techniques, and measure their        companies, like OpenAI, state that website content accessed by AI
deployment as well as their efficacy across different AI crawlers.       assistants is not directly used for training, it could inadvertently
   Results from our study highlight critical hurdles that limit or       contribute if the company trains models on user interaction logs,
prevent the effective utilization of protective tools by individual      as seen with ChatGPT [82].
creators, leaving these key stakeholders in the data ecosystem vul-         Crawlers for facilitating AI-backed search engines (AI search crawlers).
nerable and often unable to safeguard their work from unauthorized       A third major use of crawlers is to facilitate AI-backed search en-
AI-driven use. More specifically, our analysis produces a number         gines. For example, OpenAI-SearchBot is a crawler that indexes
of interesting findings:                                                 websites, which in turn is used by AI-backed search engines. While
                                                                         companies claim that the content of a website retrieved by AI search
• We measured the inclusion of AI crawlers in robots.txt of large,
                                                                         crawlers is not directly used for training, the user or owner of a
  popular sites, and found an initial surge followed by a slow in-
                                                                         website cannot enforce nor verify this claim.
  crease. A small but growing number of websites also explicitly
  invite AI crawlers to crawl their content.
                                                                         2.2     Mechanisms against Crawling
• We conducted a survey with 203 professional artists, and found
  that individual artists often do not have the knowledge (59%           Next we discuss current mechanisms for controlling crawling. We
  have never heard about robots.txt) and technological means to          focus specifically and exclusively on data transfer-centric mecha-
  include AI crawlers in their robots.txt. Once presented with more      nisms designed to prevent the acquisition of content for the purpose
  information, many artists indicated that they would like to use        of training AI models, rather than content-centric mechanisms such
  robots.txt to disallow AI crawling. At the same time, the majority     as Glaze [100] that focus on limiting the value of the acquired data.
  of the artists do not trust that AI companies will respect it.         Robots.txt. The Robots Exclusion Protocol (RFC9309 [61]) de-
• Testing on our own sites, most large AI companies currently do         fines robots.txt, allowing website owners to signal which URLs
  respect robots.txt. However, a number of AI-powered apps and           crawlers should access. Originally designed to reduce server load,
  crawlers do not respect it (including crawlers from ByteDance).        it is now widely used to manage content access. As an honor-based
• We measure the adoption and operation of active blocking mecha-        system, compliant crawlers follow its directives, but adherence is
  nisms. While they offer stronger protection, they still suffer from    not mandatory. Note that this approach is distinct (and indeed op-
  limitations such as an incomplete list of AI crawlers blocked, and     posite) from browser-oriented mechanisms, such as Global Privacy
  inability to stop AI training for Meta, Google, and Webzio.            Control (GPC) [116] and Global Privacy Platform (GPP) [63], which
                                                                         are designed to let browsers signal privacy preferences to websites
Altogether, our work highlights the need for better mechanisms that      (e.g., if they permit their user data to be sold to third-parties).1
account for the diverse range of use cases, that make mechanisms             Figure 1 shows an example robots.txt file. The first two lines
more accessible to a broader range of content creators, and that         allow Googlebot to crawl all URLs, while the next three disallow
more clearly convey the implications and limitations of using them.      ChatGPT-User and GPTBot from crawling any. The final lines block
                                                                         all other crawlers from accessing the /secret/ directory. Robots.txt
2     Background and Related Work                                        can also include sitemaps (URL lists for indexing).
We start by providing a brief overview of AI-related crawling, and           In this paper, we categorize the levels of restriction imposed by
then discuss existing mechanisms that sites can use to prevent it.       robots.txt on a given crawler into four distinct groups. The first
                                                                         category, no robots.txt, applies to sites that do not have a robots.txt
2.1     Data Scraping of Commercial AI                                   file. The second, no restrictions, refers to cases where the user
                                                                         agent is fully allowed to access the website as specified by robots.txt.
Crawlers are automated programs that visit websites and download
                                                                         The third category, partially disallowed, indicates that the user
their content. In the era of AI, companies use crawlers for a variety
                                                                         agent is permitted to access some paths but not all. Finally, fully
of purposes. At the time of writing, there exist three main types of
                                                                         disallowed describes instances where the user agent is prohibited
AI-related crawlers: (1) crawlers for collecting training data (e.g.,
                                                                         from accessing any paths on the website.
OpenAI’s GPTBot), (2) crawlers for augmenting AI-backed assis-
tants (e.g., OpenAI’s ChatGPT-User), and (3) crawlers for facilitating   1 Both the GPC and GPP systems were built in response to affirmative consumer privacy

AI-backed search engines (e.g., OpenAI’s SearchBot).                     obligations, such as provided in Europe’s General Data Privacy Regulation (GDPR)
                                                                         and California’s Consumer Privacy Act (CCPA). As of yet the statutory legal landscape
   Crawlers for collecting training data (AI data crawlers). One sig-    for protecting content creator interests has not had similarly crisp rules — perhaps
nificant use of crawlers is to collect data for training AI models.      explaining the absence of standardized AI-use permission signaling.
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers           IMC ’25, October 28–31, 2025, Madison, WI, USA.


# An example robots.txt file                                                           Web content control mechanisms. Robots.txt, arguably the
User-agent: Googlebot                                                                  most widely-used web content control mechanism, has been ex-
Allow: /                                                                               tensively studied. Sun et al. [108] performed a large-scale analysis,
                                                                                       identifying errors and the increased use of the now-deprecated
User-agent: ChatGPT-User                                                               “Crawl-Delay” field. Studies by Sun et al. [107] and Kolay et al. [60]
User-agent: GPTBot                                                                     revealed biases favoring major search engines. Non-technical as-
Disallow: /                                                                            pects, such as legal implications of violating robots.txt [97] and its
                                                                                       use for expressing copyright authorization [119], have also been
User-agent: *                                                                          explored. Similar protocols, like security.txt [89] and ads.txt [11],
Disallow: /secret/                                                                     have been examined for purposes beyond Web content control.
                                                                                          More recently, studies have revisited robots.txt in the context
Figure 1: In this example robots.txt file, Googlebot is al-                            of generative AI. Dinzinger and Granitzer surveyed web content
lowed to crawl all URLs on the website, ChatGPT-User and                               control mechanisms [29], and empirical studies [28, 70] found a
GPTBot are disallowed from crawling any URLs, and all                                  sharp increase in robots.txt adoption post-generative AI, with other
other crawlers are disallowed from crawling URLs under                                 mechanisms like the noai meta tag remaining rare. Fletcher [32] re-
the /secret/ directory.                                                                cently conducted a case study on the adoption of robots.txt by news
                                                                                       websites. Several blog posts have examined the use of robots.txt
                                                                                       at small scales (e.g., hundreds of websites) [16, 37, 74, 85]. These
                                                                                       studies focus on broad trends, while our work mainly examines the
   More recently, companies have provided managed services for                         perspective of individual creators and the unique challenges they
robots.txt. These managers simplify maintenance by offering auto-                      face.
mated updates and interfaces. Dark Visitors [114] syncs with an AI
                                                                                       Detection and blocking of Web crawlers. Research on Web
crawler database, while tools like YoastSEO [99] and AIOSEO [2]
                                                                                       crawler detection and blocking has explored various techniques,
provide more intuitive features for configuring rules.
                                                                                       including web traffic analysis [46, 49, 71], server access logs [45,
Active blocking. Active blocking prevents crawlers from ac-                            95, 103], user behavior [20, 45], pattern matching [62], machine
cessing a website using various methods for detecting and reacting                     learning [50, 105], and browser fingerprinting [5, 54, 111]. Studies
to crawlers. Detection methods range from simple IP address or                         have also differentiated crawler behaviors, such as good versus bad
user agent rules to more sophisticated techniques like browser                         bots [67], bogus bots [9], and human versus bot access patterns [4,
fingerprinting. Once detected, a website can block the crawler by                      65]. Websites use blocking methods like 403 errors, CAPTCHAs, or
returning an error HTTP status (e.g., 403 Forbidden), displaying an                    altered pages [5, 88]. Our work builds on analyses of website and
alternative page (e.g., a CAPTCHA), or even serving fake content                       anti-bot service behavior, including studies by Pham et al. [88] on
(e.g., Cloudflare’s Labyrinth [110]). Active blocking can be imple-                    user agents, Azad et al. [5] on anti-bot service effectiveness, and
mented directly on a web server (e.g., via Apache or Nginx rules)                      Jones et al. [53] on automated detection of block pages.
or through third-party services like Cloudflare’s reverse proxy.
                                                                                       Impact of generative AI on content creators. A third area of
NoAI meta tag. First proposed by DeviantArt, NoAI and NoIm-                            research investigates the impact of generative AI on content cre-
ageAI are meta tags [33] a site can insert into HTML content to                        ators. The work closest to ours focuses on the impact of generative
indicate to crawlers that content should not be used for AI training:                  AI on artists and art. For example, the blog posts by Ortiz [83] and
    <meta name="robots" content="noai, noimageai">                                     Zhou [122] highlighted two specific harms created by AI art: plagia-
                                                                                       rism and loss of jobs. Jiang et al. [51] comprehensively categorize
Previous work [28] found that the adoption of these tags is low. We
                                                                                       different types of issues raised by generative AI. More empirically,
confirm this result by checking the top 10k domains in the Tranco
                                                                                       Kawakami et al. [55], Shi et al. [102], Lovato et al. [72], Ali and
ranking from October 2024, with only 17 sites having noai and 16
                                                                                       Breazeal [3], and various reports [27, 73] have identified similar
having noimageai tags.
                                                                                       kinds of concerns by summarizing online discussions or survey-
ai.txt. Introduced by Spawning AI, ai.txt allows content owners                        ing artists. Huang et al. [44] conducted a field experiment and
to specify whether AI crawlers can use their data for training [77].                   found that the adoption of generative AI could adversely impact
Unlike robots.txt, ai.txt is read when an AI model attempts to down-                   the activities of artists on digital art platforms. Zhou and Lee [121]
load media, enabling real-time updates to preferences, even for                        measured the amount and impact of AI-assisted art activities. Shan
previously collected data. Its creators argue it offers a legally en-                  et al. [100] highlighted the specific concern of style mimicry (using
forceable standard, referencing the EU TDM Article 4 exception [56],                   AI to generate a specific style of art). Lastly, others have discussed
though its enforcement differences from robots.txt remain unclear.                     the benefits and harms of generative AI art [19, 30, 35, 80, 86] as
                                                                                       well as studied the attitudes and sentiment toward generative AI
2.3     Related Work                                                                   art [12, 42, 52, 64, 76, 92]. Our work contributes to this strand of
                                                                                       research by examining the technical needs and challenges artists
Given the broad scope of our work, we survey a variety of related
                                                                                       face in protecting their online presence.
work in the areas of Web content control mechanisms, crawler
                                                                                          Also related, but orthogonal to our work, is the study of the im-
detection and blocking, and the impact of generative AI on content
                                                                                       pact of generative AI on other communities, such as user experience
creators.
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                     Enze Liu et al.


           User Agent                    Category          Company          Publish IP     Claim Respect       Respect in Practice
           Amazonbot                     AI Search         Amazon               Yes              Yes                    Yes
           AI2Bot                        AI Data           Ai2                  No                -                      -
           anthropic-ai                  Undocumented AI   Anthropic            No                -                      -
           Applebot                      AI Search         Apple                Yes              Yes                    Yes
           Applebot-Extended*            AI Data           Apple                 -               Yes                     -
           Bytespider                    AI Data           ByteDance            No                -                     No
           CCBot                         AI Data           Common Crawl         Yes              Yes                    Yes
           ChatGPT-User                  AI Assistant      OpenAI               Yes              Yes                    Yes
           Claude-Web                    Undocumented AI   Anthropic            No                -                      -
           ClaudeBot                     AI Data           Anthropic            No               Yes                    Yes
           cohere-ai                     Undocumented AI   Cohere               No                -                      -
           Diffbot                       AI Data           Diffbot              No                -                      -
           FacebookBot                   AI Data           Meta                 Yes              Yes                     -
           Google-Extended*              AI Data           Google                -               Yes                     -
           GPTBot                        AI Data           OpenAI               Yes              Yes                    Yes
           Kangaroo Bot                  AI Data           Kangaroo LLM         No               Yes                     -
           Meta-ExternalAgent            AI Data           Meta                 Yes               -                     Yes
           Meta-ExternalFetcher          AI Assistant      Meta                 Yes              No                      -
           OAI-SearchBot                 AI Search         OpenAI               Yes              Yes                     -
           omgili                        AI Data           Webz.io              No               Yes                     -
           PerplexityBot                 AI Search         Perplexity           No               Yes                     -
           Timpibot                      AI Data           Timpi                No                -                      -
           Webzio-Extended*              AI Data           Webz.io               -               Yes                     -
           YouBot                        AI Search         You.com              No                -                      -
Table 1: Summary of AI user agents studied and the companies associated with them. We derive the category from the Dark
Visitors list [113] and note whether companies publish the IP addresses they use when crawling with a particular user agent,
whether their documentation claims to respect robots.txt, and whether they respect robots.txt in practice (Section 5). If we
cannot find documentation associated with a user agent or the documentation does not mention whether they respect robots.txt,
we mark it as ‘-’. If we cannot test whether a user agent respects robots.txt (because the crawler did not visit our website), we
mark it as ‘-’. *These three user agents are not used by real crawlers, but instead are special user agents site owners can use to
control crawler behavior (Section 6.2). As a result, we mark their IP address as ‘-’.


design professionals [66], early-career game developers [14], come-       3.1    Data and Methodology
dians [78], Jewish Americans [90], professional playwrights [39],         To explore historic trends in the use of robots.txt to control AI
creative writers [40, 47], and online communities such as Stack-          crawlers, we compile a comprehensive list of user agents for AI
overflow and Reddit [17].                                                 crawlers and a longitudinal dataset of robots.txt files for sites that
                                                                          are consistently popular over time.
3    How Well-resourced Websites Reacted                                  AI user agents. We compile a comprehensive list of AI user
To provide a broader context on how the arrival of AI crawlers            agents based on Dark Visitors, an industry blog that maintains an
changed views across the Web towards crawlers, we start by revisit-       up-to-date list of AI user agents [113]. Since Dark Visitors also
ing how well-resourced websites reacted. These websites are more          lists other crawler user agents, we only consider the AI-related
likely to react swiftly, as they have substantial content to protect      user agents belonging to the following categories: AI Assistant
and the technical capability and domain knowledge to do so.               (AI Assistant Crawler in this paper), AI Data Scraper (AI Data
    In this section, using a corpus of popular domains, we investigate    Crawler in this paper), AI Search Crawler, and Undocumented
the extent to which well-resourced websites adopt robots.txt to           AI Agents. We also cross-validated the list with a prior study that
restrict AI-related crawlers. Among these popular sites, many are         collected popular user agents in robots.txt files [70] and confirmed
quick to add restrictions to AI crawlers in robots.txt: over 10% of       that our list is a superset of the AI user agents in this prior study.
the domains explicitly disallowed AI crawlers in their robots.txt         In total, we use 24 unique AI-related user agents, listed in Table 1.
file after AI crawler user agents were announced. While there have        We focus exclusively on these user agents for the rest of the paper
been many different incentives and efforts (e.g., the recent EU AI        unless otherwise noted.
Act) to use robots.txt to restrict AI crawlers, we also observe a
                                                                          Historic robots.txt data from Common Crawl. We compile a
small yet noticeable reverse trend: some sites recently removed
                                                                          list of sites that are consistently popular over time to represent a
restrictions on AI crawlers, likely due to reasons such as entering
                                                                          stable set of well-resourced websites that have substantial valuable
into data licensing agreements with AI companies.
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers                                   IMC ’25, October 28–31, 2025, Madison, WI, USA.


content, and the knowledge and resources to control AI crawler                                               14            Stable Top 5k
access to it. In particular, we focus on popular sites whose domains                                                       Other Sites
                                                                                                             12
appear in the Tranco Top 100k lists every month for two years,
                                                                                                             10




                                                                                          Percent of Sites
from October 2022 through October 2024. We restrict the list to
sites that appear in all of the top 100k lists over this period to avoid                                      8
having our results affected by list churn [96]. There are 51,605 sites
                                                                                                              6
whose domains consistently appear in the top 100k lists over these
two years.                                                                                                    4
   For each of these sites, we look for historic robots.txt files served                                      2
by the sites in Common Crawl [24] snapshots covering the October                                              0




                                                                                                                   022
                                                                                                                                 022
                                                                                                                                 023
                                                                                                                                 023
                                                                                                                                  023
                                                                                                                                 023
                                                                                                                                 023
                                                                                                                                 023
                                                                                                                                 024
                                                                                                                                 024
                                                                                                                                  024
                                                                                                                                 024
                                                                                                                                 024
2022–2024 period. All snapshots crawled each site at least once;




                                                                                                                  Oct 2
                                                                                                                          Dec 2
                                                                                                                           Feb 2
                                                                                                                           Apr 2
                                                                                                                            Jun 2
                                                                                                                           Aug 2
                                                                                                                           Oct 2
                                                                                                                           Dec 2
                                                                                                                           Feb 2
                                                                                                                           Apr 2
                                                                                                                            Jun 2
                                                                                                                           Aug 2
                                                                                                                           Oct 2
if a snapshot crawled a site more than once, we use the most-
recent robots.txt in that snapshot. Table 3 in Appendix B.1 lists each
                                                                                                                                                  Date
Common Crawl snapshot, the months it covers, and the number of
sites with a robots.txt file.
                                                                                           Figure 2: Percent of sites that fully disallow at least one AI
   We exclude sites that did not have robots.txt files, as well as
                                                                                           crawler user agent for the Stable Top 5k (2,551 sites) and the
sites where Common Crawl encountered an error when requesting
                                                                                           remaining sites in the Stable Top 100k (37,904 sites).
robots.txt from them.2 Of the 51,605 longitudinally popular sites,
40,455 of them have a robots.txt file in every snapshot of the Com-
mon Crawl data. We refer to these 40,455 sites as the Stable Top
                                                                                           User-agent: *), we do not consider such sites to express an intent
100k, and these are the sites we use in our analyses. Each Stable
                                                                                           to specifically disallow AI crawlers. The code for categorizing AI
Top 100k site appears in all top 100k rankings over time and has a
                                                                                           user agents in robots.txt files is publicly available at https://github.
robots.txt file in every Common Crawl snapshot.
                                                                                           com/ucsdsysnet/ai-crawler-imc-25.
   We validated that the Common Crawl data is accurate by manu-
ally comparing robots.txt files retrieved by Common Crawl with
the temporally closest version available in the Internet Archive                           3.2                      Increasing Drive to Protect Data
for a random sample of ten robots.txt files in each Common Crawl                          Figure 2 shows the trend of restrictions on AI crawlers over time
snapshot. We also validated the last snapshot of the Common Crawl                         with curves for two categories of sites: the Stable Top 5k sites, and
data by conducting our own crawl of robots.txt of the top 10k sites                       all other sites in the Stable Top 100k. The Stable Top 5k sites are
of the Stable Top 100k. There was no disagreement between the                             the 2,551 sites consistently ranked in the top 5k in every Tranco
robots.txt files collected by Common Crawl and Internet Archive.                          list throughout October 2022–2024. While all sites in the Stable Top
We found minimal (<1%) disagreements between our own crawl                                100k have popular content and significant resources to manage it,
and Common Crawl, which we attribute to websites changing the                             the Stable Top 5k represent the very largest sites on the Web. Each
contents of robots.txt in the time between the two crawls (the day                        point shows the percent of sites in a category that fully disallow
we performed our crawl could be up to multiple weeks later than                           at least one AI crawler user agent in a particular Common Crawl
when the site appeared in the last Common Crawl snapshot).                                snapshot. For snapshots that span multiple months, we use the
Parsing and interpreting robots.txt. We parse robots.txt files                            most recent month of the snapshot to represent it (e.g., points
using Google’s robots.txt parser [38]. We rely on Google’s parser as                      at December 2022 correspond to the “November/December 2022”
robots.txt is a complex standard and our experience suggested that                        snapshot).
home-grown parsers are error-prone.3 We randomly selected a set                               While both categories of sites have an initial surge disallowing
of 100 robots.txt files, and manually verified that Google’s parser                       AI crawlers in their robots.txt after October 2023 (around the an-
correctly interpreted all of them. We also verified that the parser                       nouncement of OpenAI’s GPTBot and ChatGPT-User user agents
correctly interpreted a variety of edge cases not captured by other                       that identify their crawlers), the most popular websites are notice-
parsers, as shown in Appendix B.2.                                                        ably quicker to add restrictions in robots.txt. Likely since they value
    We built a wrapper around Google’s parser to categorize whether                       their content so highly, a larger proportion of the most popular
a given user agent is fully disallowed (for all content on the site), is                  sites have restrictions on at least one AI crawler (12–14%) when
partially disallowed (for a portion of the site), or has no restrictions.                 compared to the rest of the Stable Top 100k sites (8–10%). We also
In our analyses, we only consider a site to disallow an AI crawler                        looked at other popularity tiers below the Stable Top 5k. In those
if the site’s robot.txt file has an explicit rule for the crawler’s user                  tiers the proportions of sites that fully disallow AI user agents are
agent. While less than 2% of the domains in the Stable Top 100k have                      all very similar to each other, so we combine them together into the
robots.txt files with a wildcard rule that disallows all crawlers (e.g.,                  “Other Sites” curve for clarity to avoid many overlapping curves.
                                                                                              Figure 3 shows historical site robots.txt behavior for specific AI
2 For instance, if a site implemented active blocking on automated requests (like those   user agents. Each curve shows the percent of Stable Top 100k sites
of the CC crawler), then Common Crawl may record a 403 Forbidden HTTP status              that either fully or partially disallow the corresponding AI user
code for those sites.                                                                     agent over time. The most frequently restricted user agents are
3 An example is the parser developed by [70], which we estimate to have a 10% error
rate in parsing robots.txt. We notified the authors about this issue, and it has since    GPTBot (OpenAI) and CCBot (Common Crawl). While Common
been corrected.                                                                           Crawl merely collects the data (and does not use it for any AI-related
 IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                                    Enze Liu et al.



                               GPTBot                                                                       Explicitly Allowed
                               CCBot                                                         300            Removed Restrictions
                   8           Google-Extended                                                              Condé Nast deal
                               ChatGPT-User                                                  250            Stack Exchange, Dotdash Meredith deal




                                                                           Number of Sites
                                                                                                            Vox Media deal
Percent of Sites




                   6           anthropic-ai                                                  200
                               ClaudeBot
                               Claude-Web                                                    150
                   4           PerplexityBot
                               Bytespider                                                    100
                   2           omgili
                                                                                              50

                   0                                                                           0




                                                                                                    022
                                                                                                                  022
                                                                                                                  023
                                                                                                                  023
                                                                                                                   023
                                                                                                                  023
                                                                                                                  023
                                                                                                                  023
                                                                                                                  024
                                                                                                                  024
                                                                                                                   024
                                                                                                                  024
                                                                                                                  024
                              022
                              022
                              023
                              023
                              023
                              023
                              023
                              023
                              024
                              024
                              024
                              024
                              024




                                                                                                   Oct 2
                                                                                                           Dec 2
                                                                                                            Feb 2
                                                                                                            Apr 2
                                                                                                             Jun 2
                                                                                                            Aug 2
                                                                                                            Oct 2
                                                                                                            Dec 2
                                                                                                            Feb 2
                                                                                                            Apr 2
                                                                                                             Jun 2
                                                                                                            Aug 2
                                                                                                            Oct 2
                       Oct 2
                        Dec 2
                        Feb 2
                        Apr 2
                         Jun 2
                        Aug 2
                        Oct 2
                        Dec 2
                        Feb 2
                        Apr 2
                         Jun 2
                        Aug 2
                        Oct 2
                                                 Date                                                                                  Date


 Figure 3: Percent of Stable Top 100k sites that partially or               Figure 4: Number of sites that explicitly allow at least one
 fully disallow an AI crawler user agent in robots.txt over                 AI crawler in their robots.txt over time, and number of sites
 time. The vertical line indicates the release of the EU AI Act.            that removed restrictions on AI crawlers in each time period.
                                                                            The vertical lines indicate public data deals between major
                                                                            publishers (who control 40+ domains) and OpenAI.

 purpose itself), Common Crawl is a very frequent data source for
 AI training [8].                                                           traffic to their website. The full list of such websites is in Table 4 in
    After August 2024 there appears a secondary distinct uptick of re-      Appendix B.3.
 strictions for all user agents. This uptick correlates with the release    Possible private deals. In the case of major American publisher
 of the EU Artificial Intelligence Act, which aims to impose legal          Future PLC, more than 10 of their sites (including techradar.com,
 regulations on general-purpose AI. Critically, the draft version of        tomsguide.com, and cyclingnews.com) removed restrictions on
 the Act’s “Code of Practice” explicitly requires signatories to respect    GPTBot in May 2024, while the rest of the robots.txt file remained
 the directives of robots.txt (Sub-Measure 4.1) to avail themselves of      unchanged. However, in an August 2024 podcast, the CEO of Future
 statutory “Text and Data Mining” copyright carve-outs [22].                PLC stated that they did not have a partnership with OpenAI [10].
                                                                            A few other smaller publishers and news sites also removed restric-
 3.3                      Recent Decrease in Restrictions                   tions on GPTBot, which could indicate possible private deals.
 Among the Stable Top 5k sites, we surprisingly not only see the
 trend of adding restrictions to AI crawlers in robots.txt level off,       3.4                     Recent Increase in Allowing AI Crawlers
 but also some decreases at the end of the time period. This latest         To our surprise, a growing number of sites explicitly allowed AI
 behavior is in contrast to predictions in [70] of strictly increasing      crawlers in their robots.txt, welcoming AI crawlers to scrape their
 observable intent to disallow AI crawling.                                 content. While a small number of sites fall into this unique cate-
 Public data licensing deals. One reason why a site will remove             gory, the overall number of sites that explicitly allow AI crawlers is
 an AI crawler from their robots.txt is when the site owner has             increasing over time as shown in Figure 4.
 entered into a data licensing agreement with an AI company. A blog            In total, 79 sites not only had no restrictions on GPTBot in their
 post from early October 2024 confirmed that such partnerships were         robots.txt, but also included a rule that explicitly allowed the GPT-
 indeed the reason for the removal of GPTBot from the robots.txt            Bot user agent. The data licensing agreements between OpenAI
 files from the websites of several major publishers, including The         and publishers mentioned previously explain part of this increase
 Atlantic and Vox Media [58]. These deals often involve a publisher         (especially in mid-2024), but there are also other reasons.
 who controls dozens of domains; e.g., Newscorp owns more than                 Among the sites that explicitly allow AI crawlers are popular
 10 news and media companies, each having its own set of domains.           right-wing misinformation sites, which may be motivated to spread
     In our data, between August 2023 (the announcement of Ope-             misinformation to LLMs. Other cases are shopping sites that poten-
 nAI’s GPTBot and ChatGPT-User user agents) and October 2024 (the           tially seek to use LLMs to increase traffic to their site. Appendix B.3
 end of our dataset), 484 sites removed explicit restrictions on GPT-       shows the full list of sites where we observe this reverse intent
 Bot from their robots.txt (Figure 4). Many of these sites are owned        toward GPTBot. This case study highlights that sites have a variety
 by publishers who have struck publicly-announced data licensing            of motives for allowing AI companies to crawl their data.
 agreements with OpenAI, such as Dotdash Meredith [91] (e.g., in-
 vestopedia.com, people.com, allrecipes.com), Stack Exchange [84]           4                  Sentiments and Actions of Individual Artists
 (e.g., superuser.com, stackoverflow.com), and Conde Nast [57] (e.g.,       Section 3 showed that many well-resourced websites swiftly adopted
 newyorker.com, vanityfair.com, wired.com). Some of these data              robots.txt to protect their content. In this section, we explore the
 usage agreements require OpenAI to place direct links to the sites         question of what individual artists think about AI-related crawling
 when ChatGPT generates content based on their data, driving more           and what actions they have taken in response to such crawling, if
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers                  IMC ’25, October 28–31, 2025, Madison, WI, USA.


any. Compared to large organizations, individual artists have sig-                      4.2     Sentiment Towards AI-related Crawling
nificantly more direct risk yet are comparatively under-resourced.                      Echoing previous studies [3, 27, 72, 73], surveyed artists express a
   We first present a user study, comprised of 203 professional                         strong sentiment against AI-related crawling and a strong desire
artists, to understand their sentiments, actions, and challenges they                   for effective tools to stop it.
face when dealing with AI-related crawling. While many artists
                                                                                       Artists are worried and have taken actions against AI. Over
are extremely concerned about AI, they lack the awareness (59% of
                                                                                       79% of all artists express concerns that AI-generated art will have
artists have never heard about the term “robots.txt”), technical abil-
                                                                                       at least moderate impact on their job security, with more than 54%
ity (not knowing how to use robots.txt), and agency (unable to edit
                                                                                       anticipating that AI art will have a significant or severe effect on
robots.txt) to utilize existing technical approaches like robots.txt.
                                                                                       their careers. A notable majority (169, 83%) reported taking proac-
   Informed by our user study, we follow up with a measurement
                                                                                       tive measures to address these concerns. Among these 169 artists,
study of over 1,100 artist websites to further examine the hosting
                                                                                       71% use Glaze [100], a tool that employs adversarial machine learn-
services artists use and levels of control these services provide. The
                                                                                       ing to protect artwork. Other common actions selected by artists
majority of these artists use third-party hosting services that do
                                                                                       include reducing the volume of work shared online and sharing
not allow for modification of robots.txt. Among the few that do,
                                                                                       lower-resolution images to mitigate potential misuse. Besides Glaze,
those artists do not exercise their control, with fewer than 17% of
                                                                                       artists mentioned alternative approaches to modify their art, such
such artists disallowing AI-related crawlers in their robots.txt.
                                                                                       as applying watermarks or using Nightshade [101]. Another com-
                                                                                       mon action is changing to platforms that offer better protection
                                                                                       against AI-related crawlers and withdrawing from platforms that
4.1     User Study Methodology                                                         do not provide such protection (e.g., switching from Instagram to
                                                                                       Cara). Lastly, a few artists mentioned that AI-generated art has
In this section we provide details on our user study, including
                                                                                       impacted their career choices, with one artist stating, “I left school
the recruitment process, survey protocol, analysis methods, and
                                                                                       and taking a gap year to reevaluate my life.”
participant demographics.
   Recruitment. We conduct a user study, approved by our uni-                          Artists would like to prevent AI crawling. When presented
versity’s institutional review board, with professional artists. We                    with the option of a mechanism for blocking crawlers from access-
draw participants from professional artists informed via their social                  ing their sites, over 97% of the artists expressed a desire to use such
circles and professional networks (e.g., internal discord channels                     a mechanism. A significant majority (185, 93%) indicated that they
and social media groups). We also ask participants to help distribute                  were “very likely” to adopt it. The most-commonly cited reasons
our survey to other artists whom they are in contact with.                             included their desire to protect their work, not consenting to hav-
   Survey Protocol. We start by gathering basic information for                        ing their art crawled, and not being compensated for their work.
each participant. Since our main concern is whether the artists                        Interestingly, five artists noted that such mechanisms could provide
whom we survey represent the community, we focus primarily on                          potential legal benefits (e.g., used as evidence in legal cases). The
their artistic background (e.g., their years of experience). Then, we                  few artists who are neutral or unlikely to adopt such a mechanism
ask them about their perceptions of AI-generated art, concerns                         cited concerns about its efficacy and trustworthiness.
regarding its impact on their job security, and actions taken in re-                      We observed similar but less pronounced results when we asked
sponse to AI-generated art. Next, we inquire about their knowledge                     artists who were not familiar with robots.txt about their willingness
and use of robots.txt, as well as their willingness to adopt robots.txt                to adopt it in the future. Concretely, 59% of the artists (119) had
in the future. We compensate participants at a rate of $15/hour, and                   not heard about robots.txt prior to our study. After reading a brief
the median time to complete the survey is 12 minutes. We provide                       explanation of robots.txt (Appendix D.1), almost all (113 out of 119)
our list of survey questions in Appendix D.1.                                          of the artists gained a basic understanding.4 Among these artists,
   Analysis. The first author conducted iterative open coding on                       75% indicated that they would likely or very likely adopt robots.txt
the open-ended survey questions following the thematic analysis                        in the future. For those who indicated neutral or unlikely, the most
approach [15]. The segment of analysis is the entire response, which                   common reasons cited were concerns regarding its efficacy (that
mostly consists of a few sentences. Multiple codes could be applied.                   robots.txt does not fully stop crawling), usability (whether it is easy
At the end, the first author created a master codebook and re-labeled                  to use), and the need for more information.
the responses. Appendix D.3 presents our codebook.                                     Artists do not trust AI crawlers to respect robots.txt. When
   Participants. After removing low quality answers (overly short                      asked about their trust in AI companies, 77% of participants who had
or off-topic answers, straight-line answers, and incomplete an-                        not heard of robots.txt before the study expressed skepticism about
swers), we obtained 203 valid responses from artists who share their                   AI companies respecting robots.txt. Artists cited several reasons for
artwork online. Around two thirds (136, 67%) of the participants                       this distrust, including the monetary incentives for AI companies
consider themselves as professional artists. 87% of all participants                   to scrape data, poor track records of AI companies so far, the lack of
are making money from their art, over half of whom have been                           legal enforcement, and that they perceive AI companies negatively.
doing so for at least five years. Geographically, over 50% of our                      One participant remarked, “[AI companies] feel they have a right
participants are based in North America, with 80% of them in the                       to everything for free, and if things like copyright don’t stop them,
United States. 25% of the participants are in Europe, and the rest
are in Asia, South America, Africa, and Oceania. We provide more                        4 That said, we caution that many artists use terms such as “block” or “stop”, while
details on the demographics of our participants in Appendix D.2.                        robots.txt is a voluntary mechanism.
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                      Enze Liu et al.


why would a polite notice on a website?”. Experiments in Section 5            Hosting Provider       % Sites    Edit?       % Disallow AI
with sites we control present a more complicated picture. Consistent
                                                                              Squarespace                20.7   No𝐴𝐼,𝑆𝐸                   17
with artist expectations, the majority of AI assistant crawlers do
                                                                              Artstation                 20.4   No                         0
not respect robots.txt. Perhaps surprisingly, though, only one major
                                                                              Wix (Paid)                  9.3   Yes                        0
AI data crawler (Bytespider) does not respect it.
                                                                              Adobe Portfolio             4.8   No𝑆𝐸                       0
   Despite a strong level of distrust, 47% of all artists remain inter-
                                                                              Wix (Free)                  3.5   No                         0
ested in adopting, or have already adopted, robots.txt. This result
demonstrates a willingness among artists to explore measures they             Weebly                      3.1   No𝑆𝐸                       0
perceive as imperfect, perhaps viewing them as necessary steps                Shopify                     1.7   No                         0
toward protecting their work even if not completely effective.                Carbonmade                  1.5   No                       100

                                                                          Table 2: The top eight web hosting providers used by artists,
4.3     Challenges in Adopting Technical Measures                         usage percentage, and their options for modifying robots.txt.
We identify three main challenges for artists to utilize technical        𝐴𝐼 : option available to disallow AI crawlers; 𝑆𝐸: option avail-
measures such as robots.txt: lack of awareness, ability, and agency.      able to disallow search engine crawlers.
   The most significant challenge is the lack of awareness among
artists: as previously mentioned, around 59% of the artists have
never heard about robots.txt prior to our study. Among the 41%            other services (e.g., Squarespace), the domain’s DNS record points to
who had heard of robots.txt, 90% of them demonstrated a basic             the service’s infrastructure. For sites hosted on Wix, their domains
understanding of its purpose, describing it as a way of “blocking”        allow for straightforward differentiation between free and paid
or “stopping” crawlers.                                                   versions: sites hosted using the free version of Wix use subdomains
   Another major challenge is the lack of technical ability to utilize    of wix.com, whereas sites using the paid version have a registered
robots.txt. Among the 38 artists who maintain personal websites           domain whose DNS record points to Wix’s infrastructure.
and were aware of robots.txt before the study, 27 of them have not
utilized robots.txt on their personal websites. When prompted why,        Limited control and information available. Hosting providers
the single most-cited reason was not knowing how to do it.                give limited control and information to artists. Table 2 shows the
   Lastly, artists reported that they do not have agency to utilize       services used by artists, usage percentage, and percentage of web-
robots.txt: out of the aforementioned 38 artists, nine report having      sites that disallow any AI crawlers (Table 1) in their robots.txt. The
no control over the content of robots.txt. Another five note the          contents of robots.txt files are identical for all artists who host with
additional challenge that even though they have control over their        a particular hosting provider except artists who use Squarespace.
personal website, they post on multiple platforms and can only                To better understand the agency these hosting providers give
modify the robots.txt of their personal website.                          their users, we registered accounts with each of them. Four do not
                                                                          provide any method for users to modify the robots.txt file, which the
                                                                          provider sets with a default configuration. Out of these four, only
4.4     Artist Website Use of Robots.txt
                                                                          Carbonmade disallows AI crawlers (GPTBot and CCBot) in their
Guided by the findings from our user study, we performed a mea-           default robots.txt file. Two providers (Adobe Portfolio and Weebly)
surement study on over 1,100 artist websites to better understand         offer users the option to disallow search engine crawlers through
the services used by artists and the level of control these ser-          their robots.txt file; however, none of the sites in our dataset have
vices provide. The majority of these artists use third-party hosting      this option enabled. Only one provider, the paid version of Wix,
providers that do not allow for modification of robots.txt. Among         allows users to directly modify the content of the robots.txt file.
the few providers that do, most artists do not exercise the option to         Squarespace is the only provider that gives the user the option to
disallow AI crawlers.                                                     disallow AI crawlers in robots.txt. This option adds full restrictions
Artist websites and their service provider. We identified                 on ten AI user agents, including GPTBot and anthropic-ai (the full
the personal websites of artists using directories of two top artist      list is available in Appendix C.1).
associations in the U.S., Concept Art Association and Animation               We also investigated if any of these providers actively block
Union. Both organizations published their member lists along with         AI crawlers in addition to disallowing them in robots.txt. (For a
each artist’s personal website. In total, we collected a list of 1,182    detailed methodology for detecting active blocking, see Section 6.1.)
sites. The majority of these artists (over 78%) use one of eight          Weebly does specifically block requests that have the user agent set
hosting providers, such as Squarespace and ArtStation, to host their      to Claudebot and Bytespider, whereas Artstation and Carbonmade
websites, followed by a long tail of small providers, self-hosted         implement captcha-like challenges for all automated requests.
websites, and social media platforms. As such, we focus on the top            As a last step, we checked whether any of the Terms of Service
eight hosting providers in our analysis. Most of these platforms          (ToS) of these hosting providers mention AI training on user con-
provide drag-and-drop tools, allowing artists to easily upload their      tent. While all providers state that they do not claim ownership
portfolios and personal information. As well, many artists obtain         over user content, only Adobe [1] and Artstation [7] explicitly men-
custom domain names through these services for an additional fee.         tion in their terms of service that they do not use or license user
   To determine which hosting provider an artist’s website uses, we       content for generative AI training. On the other hand, Wix can
rely on DNS. In some cases (e.g., Carbonmade), the artist sites are       use user content to train their AI tools, but only for the purpose of
subdomains of their provider (e.g., example.carbonmade.com). For          “maintain[ing] and improv[ing] the Services” [117]. Finally, while
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers            IMC ’25, October 28–31, 2025, Madison, WI, USA.




Figure 5: Squarespace provides a user-friendly option for                               Figure 6: Example of a GPT app (WebG) that can retrieve
controlling whether AI-related crawlers are disallowed in a                             information from the Web. Upon clicking “Allow”, WebG
site’s robots.txt.                                                                      can retrieve information via mixerbox.com.

                                                                                        5.1     Methodology
Carbonmade does not mention AI training in their terms of ser-                         In this section, we describe how we setup our website, followed by
vice, they have a clause prohibiting crawling content on their site:                   how we conducted our measurements.
“obtain[ing] or attempt[ing] to obtain any materials, documents                            Experiment setup. To determine whether crawlers respect
or information through any means not purposely made available                          robots.txt, we created two websites with different robots.txt files.
through the website” is prohibited [18].                                               The first website has a robots.txt file that disallows all crawlers using
Artists do not exercise their control. We next examine to                              the wildcard rule “User-agent: *; Disallow: /”. The second website
what extent artists actively utilize these options. For Wix’s paid ver-                has a robots.txt file that disallows AI crawlers by listing every
sion, which provides the highest level of control over the robots.txt                  user agent individually (e.g., “User-agent: Amazonbot; Disallow: /”).
file, none of the 1,100 websites in our dataset had edited their                       Both websites contain basic text, images, and links to other pages.
robots.txt file. When attempting to modify the file through our                        We host them on a cloud provider with the same IP address, create
paid Wix account, we discover that the interface is confusing and                      valid certificates, and log all requests. We link to both websites from
found it difficult to determine how to make changes. In contrast,                      various pages under our control (e.g., personal websites) to increase
Squarespace offers a very straightforward option: a single button                      the chances of crawlers visiting them.
that allows users to disallow AI access. However, only 49 (17%) of                         Passive measurement. Using these sites we conduct a passive
the 293 artists who use Squarespace had enabled this option — a                        measurement study for six months from September 2024 to March
figure significantly lower than the 75% of artists who, in our user                    2025. Concretely, we passively wait for crawlers to visit our website.
study, expressed a desire to disallow AI crawlers when given the                       Later, we use user agent and IP addresses (if available) to identify
choice.                                                                                individual AI crawlers. For AI crawlers that do not document the
    We hypothesize that the significant gap between the large per-                     list of IP addresses they use, we search the Internet to make sure
centage of artists desiring to take action and the small percentage                    that the IP addresses we observe are commonly associated with the
who actually do so is due to two main reasons. First, many artists                     crawlers (e.g., others have observed traffic from the same /24 with
lack awareness of these tools or an understanding of their function-                   the same user agent).
ality. This issue is evident from the low number of respondents who                        Active measurement. We also conduct an active measurement
had ever heard of robots.txt. Second, the current tools are poorly de-                 study in November 2024. We actively request AI assistant crawlers
signed and inadequately communicated. For example, Squarespace                         to visit our websites and observe if they respect the robots.txt file. To
provides no transparency about how its AI-blocking feature works                       this end, we compile a list of AI assistant crawlers for which we can
when enabled. Figure 5 shows a screenshot of the information pro-                      trigger visits to our website. This list includes built-in AI assistant
vided to users, which lacks any mention of robots.txt or details                       crawlers that are part of ChatGPT and Meta’s LLAMA. In addition,
on which AI crawlers are included. It states, “your site won’t be                      apps in ChatGPT’s store (also known as GPT apps) can also retrieve
scanned to train AI models” — an ambiguous claim, as the feature                       information from the Web using crawlers operated by third parties.
only modifies the robots.txt file and does not prevent all scanning                    We consider these third-party crawlers as AI assistant crawlers, too.
or data usage by AI.                                                                   Figure 6 shows an example of a GPT app (WebG) that can retrieve
                                                                                       information through the crawler operated by mixerbox.com.
                                                                                           To create a list of such crawlers, we start by examining a list of
5    Do AI Crawlers Respect Robots.txt?                                                the top 5k GPT apps listed on GPTStore (a popular website cited in
Since robots.txt is a voluntary mechanism, Web crawlers do not                         various prior efforts that study GPT apps [43, 104, 120]). We then
have to respect it. Indeed, anecdotal evidence has suggested that                      interact with each GPT app in an automated manner to determine
some crawlers appear to ignore robots.txt [36, 59, 93, 106]. Fur-                      whether it can retrieve information from the Web by asking it to
ther complicating the issue is the recent emergence of AI assistant                    visit a website we control. We use two different prompts: (a) “Start
crawlers that fetch pages for generative models — these crawlers                       action, fetch page: [url]”; and (b) “Get web page content: [url].”
are triggered by user queries, a use case not clearly covered by                       We check that a request is made to our website by examining the
the robots.txt standard. In this section, we explore the question                      server logs. Next, we identify individual crawlers that make these
of whether AI crawlers respect robots.txt files. The results are nu-                   requests using a combination of domain and IP address information.
anced: the majority of the AI crawlers operated by big companies                       Concretely, we examine the domain contacted by each GPT app (e.g.,
do respect robots.txt, while the majority of AI assistant crawlers                     WebG contacts mixerbox.com in Figure 6) and the IP address that
do not.                                                                                each crawler uses to visit our website. We merge any crawlers that
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                                           Enze Liu et al.


share at least one IP address or has the same registered domain name.             proficiency to configure properly. Then, as a case study we compre-
This process yields 23 distinct third-party AI assistant crawlers.                hensively evaluate the AI-specific active blocking option provided
                                                                                  by Cloudflare. While its deployment does not require technical
5.2     Results                                                                   sophistication, it does have coverage limitations.
We start by presenting the results of our passive measurement,
followed by the results of our active measurement.                                6.1     Methodology
                                                                                  Active blocking is largely overlooked as a content access control
5.2.1 Passive Measurement. Most of the crawlers that visited our
                                                                                  mechanism in prior work [28, 29, 32, 70], so its adoption for this
websites respect the robots.txt file (Table 1). During our six-month
                                                                                  purpose is relatively unknown. Hence, we first explore its use by
measurement period, nine AI crawlers visited our websites without
                                                                                  estimating the proportion of popular websites that actively block
our request: Amazonbot, Applebot, Bytespider, CCBot, ChatGPT-
                                                                                  AI crawlers. In particular, we estimate the use of active blocking
User, ClaudeBot, GPTBot, Meta-ExternalAgent, and OAI-SearchBot,
                                                                                  on the top 10k websites in the most-recent Tranco ranking in our
most of which are AI data crawlers. Seven crawlers (Amazonbot,
                                                                                  dataset (October 2024).
Applebot, CCBot, ClaudeBot, GPTBot, Meta-ExternalAgent, and
                                                                                     For simplicity, we opted for a user-agent based approach (in-
OAI-SearchBot) respected the robots.txt file. One crawler (Bytespi-
                                                                                  spired by [88]) to detect active blocking. With this approach we
der) fetched the robots.txt file but did not respect it. ChatGPT-User
                                                                                  visit sites with different user agents (a common default user agent
visited our website once and did not fetch the robots.txt file, which
                                                                                  vs. AI crawlers) and compare the results. A site that actively blocks
contradicts its behavior in our active measurement. Given that it is
                                                                                  based on an AI user agent will return very different content com-
a user-triggered crawler and we did not trigger it, it is unclear why
                                                                                  pared to accessing the site with a common user agent. We acknowl-
this crawler visited our website.5
                                                                                  edge that many advanced bot detection methods exist (e.g., through
5.2.2 Active Measurement. Both ChatGPT’s and Facebook’s built-                    fingerprinting or behavioral analysis), and consider our results a
in AI assistant crawlers respected the robots.txt file. ChatGPT’s                 conservative estimate of the overall number of sites that actively
crawler can be identified with the user agent “ChatGPT-User” while                block AI crawlers. Following [88], for each website we perform the
Meta uses a mix of “FacebookExternalHit” and “Meta-ExternalAgent”                 following steps:
as the user agent. Both ChatGPT and Meta start by requesting                         Control case: We first identify sites that inherently block our
robots.txt from a website. If the robots.txt file disallows the crawler,          automation tool, regardless of the user agent. In these cases, we
the crawler will not fetch content on the website.                                cannot distinguish whether a site is blocking our tool, or is blocking
    Interestingly, according to both the official documentation [75]              based on a particular user agent. We visit the site with a headless
and Dark Visitors [113], Meta’s AI assistant crawler should use                   browser (Chromium automated by Selenium) and set its user agent
the user agent “Meta-ExternalFetcher”. However, we do not ob-                     to a typical Chrome user with the OS matching the machine the
serve any crawler with this user agent in either our passive or                   browser runs on. If a site returns a non-200 HTTP status code (after
active measurements. Instead, our observation is that Meta uses                   any potential redirections), we make no inferences on its use of
“FacebookExternalHit” or “Meta-ExternalAgent” for both AI data                    active blocking of AI crawlers. Among the top 10k popular sites in
crawling (training) and AI assistant crawling (user-triggered).                   October 2024, 1,487 (15%) of them inherently block our crawler. By
    For the 23 third-party crawlers, most of them did not respect the             excluding these sites, we again consider our measurement of the
robots.txt file: one crawler fetched and respected robots.txt files;              active blocking adoption rate to be a lower bound.
one has a bug in its implementation that caused it to incorrectly                    AI case: Holding all else constant, we then revisit all sites that
fetch the robots.txt file; one did not fetch the robots.txt file most of          do not block our tool with two Anthropic user agents: Claudebot
the time; and the remaining 20 crawlers did not fetch the robots.txt              and anthropic-ai. We use just these two AI user agents because,
file at all (and hence do not respect it).                                        according to Dark Visitors [113], these are the two most-frequently
                                                                                  restricted AI user agents that do not have published IP address
6     Active Blocking of AI Crawlers                                              origins. Since Anthropic does not publish the IP address ranges it
The effectiveness of a mechanism like robots.txt depends both on                  uses for crawling, site operators would more likely actively block
the ability of content owners to express their intent to prevent                  them based on user agent. The companies associated with the other
crawling, as well as the willingness of AI companies to respect the               AI user agents do publish IP address ranges, and sites could actively
prohibitions that content creators have expressed. Instead, content               block based solely on the IP address of the crawler — a form of
owners can take matters into their own hands and actively block                   active blocking that we cannot measure.
crawlers by refusing to return content when HTTP requests include                    Detecting blocking behavior based on user agent: To iden-
AI crawler user agents.                                                           tify active blocking, we check the HTTP status code, any excep-
   In this section we explore active blocking as another option for               tions that occur, and whether there are significant differences in the
protecting content from AI crawling. We first measure the preva-                  HTTP content length returned (inspired by [53]).6 Any differences
lence of active blocking on popular sites. While the extent of active             in these features between the “Control” and “AI” crawls indicate
blocking is similar to the use of robots.txt, our results indicate that           active blocking based on the AI user agent. For example, if in the
there are still several limitations to active blocking: it does not offer         6 For sites where we observed a difference in HTTP content length (but the same
a perfect replacement for robots.txt, and it can require technical                HTTP status code) between the “Control” and “AI” crawls, we manually validated that
                                                                                  these were in fact cases where the site returned a “block” page instead of some trivial
5We also verified that the IP and user-agent are indeed associated with OpenAI.   difference.
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers                   IMC ’25, October 28–31, 2025, Madison, WI, USA.


“Control” crawl a site returned an HTTP status code of 200 and un-                                                                              Test Block AI:
der the “AI” crawl the site returned a status code of 403 (Forbidden),                                                                      ClaudeBot, anthropic-ai
then we decide the site has blocked the latter request.
                                                                                                                                             Block
                                                                                                                               Test Definitely
                                                                                                                                                             200
6.2     Sites Using Active Blocking                                                                                             Automated:
Using this methodology, we infer that 1,433 (14%) of the top 10k                                                              HeadlessChrome,                 Block AI OFF
October 2024 sites actively block two of Anthropic’s AI crawlers,                                                               Libwww-perl                     (87.01%)
indicating that active blocking, like robots.txt, is a relatively estab-                                        Block         Challenge            200
lished content access-control mechanism.                                                  Inconclusive: could be
                                                                                            blocked by definitely                 Block AI ON                  Block AI ON
    Many sites use active blocking instead of robots.txt. Only
                                                                                          automated or AI (7.19%)                   (1.64%)                      (4.16%)
35 (2%) of the 1,433 top 10k sites that actively block anthropic-ai
and Claudebot also have explicit restrictions on these user agents
in robots.txt. The very limited use of robots.txt among these sites                     Figure 7: Flowchart for inferring the Block AI Bots setting
indicates that many sites indeed use active blocking as their sole                      on websites hosted by Cloudflare.
form of restriction on AI crawling.
                                                                                          Grey-box evaluation. To evaluate its operation, we created an
    However, active blocking cannot replace robots.txt for
                                                                                       account with Cloudflare and configured their reverse proxy service
all AI crawlers. While active blocking may seem like a strictly
                                                                                       on a website we control. While Cloudflare states that its Block AI
better alternative, it inherently cannot replace some directives in
                                                                                       Bots feature is available for all payment tiers, for validation we
robots.txt. Specifically, in the case where companies use the same
                                                                                       tested both the free and “Pro” tiers. We use our web server logs and
crawler to collect content for both AI training as well as for other
                                                                                       Cloudflare’s internal dashboard as a source of ground truth.
purposes (e.g., indexing for Web search), active blocking is an all-or-
                                                                                          Inferring the list of AI user agents covered. Cloudflare does
nothing approach that can have unwanted side-effects. Examples of
                                                                                       not document the list of AI crawlers they block under this new
these mixed-use crawlers include Google’s Googlebot and Apple’s
                                                                                       feature. Thus, to infer its coverage, we send requests to our own
Applebot: blocking them completely can have severe consequences
                                                                                       website with the AI user agents in Table 1 and an additional 590 user
on a site’s visibility in search indexes. The only way for users to
                                                                                       agents from a public list of crawlers [79].7 We first make a request
allow crawling for search indexing and opt out of AI training for
                                                                                       with the Block AI Bots option turned off, and another with it on.
these companies is to add a disallow directive for a special “dummy”
                                                                                       For these paired requests, we determine whether or not a given
user agent (Google-Extended and Applebot-Extended) to robots.txt.
                                                                                       user agent was blocked using the HTTP response codes and the
This mechanism, while ad-hoc, highlights that robots.txt is indeed
                                                                                       dashboard for our Cloudflare account. In all, Cloudflare’s feature
still necessary even with active blocking measures in place.
                                                                                       blocks 17 AI user agents, as shown in Appendix C.3.
    Active blocking can be a black box for the user. While some
                                                                                          Inferring the adoption of Cloudflare’s Block AI Bots op-
active blocking configurations require the user to manually input
                                                                                       tion. Figure 7 shows the logic we used to infer whether a website
the blocking rules (e.g., through Apache’s .htaccess), other active
                                                                                       using Cloudflare has turned on the Block AI Bots setting. Cloudflare
blocking tools (such as third-party bot-detection platforms) act as
                                                                                       also has another managed ruleset, called Definitely Automated, that
black boxes for users, leaving them unaware of its exact behavior
                                                                                       covers all the unverified8 AI crawlers shown in Appendix C.2.
(e.g., which user agents are blocked). If the list of AI user agents
                                                                                          As with the popular sites, we used the ClaudeBot and anthropic-
is incomplete, for example, it can mislead the user into believing
                                                                                       ai user agents as they are not Cloudflare verified bots and do not
their content is fully protected.
                                                                                       publish or document their IP address origins, so it is unlikely that
    We end by noting that for a comprehensive approach to prevent
                                                                                       Cloudflare uses IP addresses to check for requests from these two
AI crawling, it is important for site owners to still use robots.txt
                                                                                       crawlers. As for inferring the Definitely Automated option, we chose
in conjunction with active blocking and verify that their active
                                                                                       the user agents of two less popular web automation libraries that are
blocking configuration matches their expectations.
                                                                                       blocked by the managed rule (HeadlessChrome and libwww-perl),
                                                                                       reducing the chance that a website has configured some custom
6.3     Third-party Active Blocking                                                    blocking rule against one of them.
As a case study of third-party active blocking, we examine Cloud-                         For the set of websites that use Cloudflare, we visit them with
flare’s recently-launched Block AI Bots feature [13]. It is a com-                     a headless browser and modify the user-agent strings as shown
pelling feature to evaluate because Cloudflare is currently the only                   in Figure 7. We inspect the HTTP response code and the returned
third-party service that offers any AI-specific active blocking mech-                  HTML content to detect whether a Cloudflare Block or Challenge
anism, it is a highly popular service [115], and this feature is clearly               page was returned, or if the site content was returned (indicating
targeted toward a less technically-proficient user base. While the                     the user agent was not blocked).
feature is designed to be user-friendly (a “single click”), its oper-
ation is unfortunately a black box to the user. We therefore first                      7 The GitHub repository we used includes the full user-agent string, which is important
experimentally infer the behavior of the Block AI Bots feature on a                    to note in case a service uses specific pattern matching.
                                                                                       8 The verified AI bots include Amazonbot, Applebot (which is not blocked), GPT-
website we control. Based on this understanding, we then estimate
                                                                                       Bot, OAI-SearchBot (not blocked), ChatGPT-User, ICC Crawler (not blocked), and
its adoption among the 2,018 (20%) sites of the Tranco top 10k that                    DuckAssistbot (not blocked). For more details on the operation of this setting, see
are hosted on Cloudflare in October 2024.                                              Appendix C.2.
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                                                 Enze Liu et al.


   We conclusively determined the setting for 1,875 (93%)9 of the                     it is accessible. While such rights are typically explicit in copyright
2,018 top 10k sites using Cloudflare. Of these 1,875 sites, only 107                  law, they are not readily expressible, let alone enforceable in today’s
(5.7%) sites enable Cloudflare’s Block AI Bots option. Yet, these sites               Internet. Instead, a series of ad hoc controls have emerged based on
also disallow AI-related crawlers in their robots.txt files at a much                 repurposing existing Web norms and firewall capabilities, none of
higher rate than average: 24% as opposed to 12% among the other                       which match the specificity, usability, or level of enforcement that
Cloudflare sites that do not enable the Block AI Bots option. These                   is, in fact, desired by content creators. We believe there exist four
107 sites show a strong intent to block AI crawlers.                                  kinds of issues that limit the value of these protections in practice:
   To sum up, while the active blocking feature provided by Cloud-                    ambiguity, respect for signal, user control, and legal uncertainty.
flare may not be widely used yet, but it is an encouraging new
option. It is user-friendly and actively blocks content from being                    8.1      Issues of Ambiguity
returned to crawlers. However, given the need to coordinate active                    Perhaps unsurprisingly, robots.txt is an imperfect mechanism for
blocking together with robots.txt, we strongly encourage platforms                    this purpose and introduces a range of ambiguities — even for the
providing such features to transparently document which user-                         purpose of measurement — around what robots.txt means and how
agent strings they block so that sites can continue to be indexed by                  it is honored.
search crawlers while achieving their goals of blocking AI crawlers.                      Syntactic ambiguity. One source of such ambiguity is the syn-
                                                                                      tactic and lexical structure of robots.txt, which is unintuitively
7    Limitations                                                                      complex. As a result, different parsers interpret the same set of
Like all measurement studies, ours has limitations in scope, method-                  directives differently. For example, the parser used in [70] misinter-
ology and generalizability.                                                           prets grouping rules and also mistakenly treats the User-agent line
Scope of participants. The user study included 203 professional                       as case-sensitive, leading to large numbers of disallow directives
artists, which does not fully represent the entire population of con-                 being ignored. Similarly, robots.txt authors themselves can misun-
tent creators. In particular, most participants were based in North                   derstand the syntactic requirements of the protocol. Approximately
America, which limits the coverage of creators from other countries.                  1% of sites we studied have mistakes in their robots.txt (e.g., such
For example, European-based artists might be more familiar with                       as not starting a path with a “/” or using non-existent directives).
robots.txt due to the implications of the AI Act.                                         Naming ambiguity. However, a more significant problem is
                                                                                      that robots.txt’s ability to specify that LLM-training crawlers are
Blocked data collection requests. In our dataset, robots.txt files
                                                                                      unwelcome is predicated on the notion that the purpose of a crawler
were collected by Common Crawl or our own custom crawler. A
                                                                                      is clearly and uniquely identified via the user agent string. Thus,
percentage of sites returned non-200 responses and were excluded
                                                                                      an LLM crawler that does not self-identify as such will not provoke
from our analysis. These sites likely employed active blocking mea-
                                                                                      the creation of a robots.txt rule. Moreover, keeping track of the
sures against CCBot or our crawler in addition to robots.txt blocks
                                                                                      current user agent mapping for all such crawlers is a burden placed
to prevent our requests. Excluding this data might lead to us under-
                                                                                      on each site administrator. Lastly, a number of crawlers serve dual
reporting the adoption of robots.txt.
                                                                                      purposes: gathering data that is used both for updating search
Automation tools can be inherently blocked. Our estimation                            indexes and for training AI models. Thus, a site owner wishing to
of the adoption rate of active blocking presented in Section 6.2 is a                 prevent their content being acquired for AI training may be faced
conservative lower bound since or 15% of the sites tested, we could                   with a difficult tradeoff as their desire to block a crawler may also
not determine their active blocking behavior due to our crawler                       force them to forgo the benefits of appearing in a popular search
being blocked independent of the user agent used.                                     index.10 Some such “dual-purpose” organizations have documented
Custom active blocking configurations are possible. In Sec-                           particular AI-specific “tokens” (e.g., Applebot-Extended and Google-
tion 6.3, we assume that a site does not configure any custom active                  Extended) that may be included in robots.txt as a signal for sites
blocking rules against the user agents we use. For example, for a                     to indicate that the content gathered by their crawlers should not
small proportion of sites we determined they were using an addi-                      be used for training by the associated organization. However, this
tional active blocking service (e.g., PerimeterX). We excluded those                  “opt-out” signal is far from standard and operates at the discretion
sites from our analysis.                                                              of the crawling organization (i.e., it does not stop the acquisition
Single measurement. Finally, our study represents measure-                            of content, but only signals the site’s preference for its use). Thus,
ments from both a point in time and with a particular methodology.                    any subsequent changes in policy or interpretation are at the sole
Thus, the behaviors that we document may have been different in                       discretion of the crawling organization.11
the past, may yet change in the future, and may even vary based                           Mode of access ambiguity. The Robots Exclusion Protocol
on factors such as country of origin.                                                 does not make clear what a “robot” is, and each organization can
                                                                                      make its own interpretation. For example, Google’s documented
8    Discussion and Conclusion                                                        policy is that robots.txt is not applicable to crawlers controlled by
                                                                                      users (for example, feed subscriptions). Indeed, there are few norms
At the core of the conflict in this paper is the notion that content
creators now wish to control how their content is used, not simply if                 10 This is similar to the ambiguity problem that arises in the use of IP blocklisting — a
                                                                                      single server may host benign and offending content.
9 For the remaining sites, we were unable to determine the setting as they may have   11 Indeed, there is some evidence that the original version of the Googlebot-Extended
been using third-party blocking mechanisms, or have some custom, non-standard         signal did not exclude the use of content in training Google’s Search Generative
Cloudflare Web Application Firewall configuration.                                    Experience search results [98].
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers           IMC ’25, October 28–31, 2025, Madison, WI, USA.


about whether user-triggered fetches should be exempt from the                         and integrated into AI models without their consent. This situation
protocol, even when such fetches may themselves be driven by a                         is complicated by a landscape that differs across geographic regions.
generative AI. For example, Meta’s user-triggered crawler Meta-                        In the US, this question is being litigated in the courts, primarily
ExternalFetcher and Perplexity’s recently-announced Perplexity-                        around the extent that the models trained on copyrighted data are
User [87] both claim to ignore robots.txt. In contrast, OpenAI takes                   derived works and if commercial AI companies can avail them-
the opposite approach with ChatGPT-User, which obeys robots.txt.                       selves of the “first use” doctrine to bypass traditional obligations
                                                                                       to copyright holders for derived works. By contrast, the EU has no
8.2     Respect for Signal                                                             general-purpose fair use exception, and while there are text and
Even if all of these other ambiguities are successfully managed,                       data-mining exceptions, the EU’s recent AI Act makes clear (via
the underlying signaling protocol is voluntary — crawlers must                         Recital 105) that “where the rights to opt out has been expressly
abide by the directives of robots.txt. As we have shown in Section 5,                  reserved in an appropriate manner, providers of general-purpose
not all crawlers respect robots.txt (e.g., ByteDance’s Bytespider                      AI models need to obtain an authorization from rightsholders if
ignores robots.txt directives) and others, while they abide, may                       they want to carry out text and data mining over such works” [23].
cache robots.txt and may continue to fetch content even after it                       Yet other countries have instead liberalized their copyright policies
has changed. At the extreme, some crawlers may pretend to be                           specifically to support the AI industry. For example, Singapore’s
regular user browsers, thus necessitating the use of advanced active                   copyright law now includes an exception for the purpose of “com-
blocking techniques such as fingerprinting [13].                                       putational data analysis” (Section 244 [81]) and Japan’s law has
   In comparison, active blocking (e.g., as offered by Cloudflare)                     also been amended to allow exploitation of copyrighted works in
allows better enforcement of an access policy, but still suffers from                  which “it is not a person’s purpose to personally enjoy or cause
issues such as dual-purpose crawlers and fetches laundered via a                       another person to enjoy” the work (Article 30-4 [94]). However,
third-party infrastructure. In addition, some LLM crawlers do not                      even in these more permissive legal environments the precise line
use identifiable ranges of IP addresses and thus IP-level blocking is                  for when such activity crosses into unprotected use is unclear.
not technically feasible (e.g., Anthropic [6]).                                            Indeed, there is reason to believe that confusion around the
                                                                                       availability of legal remedies will only further focus attention on
8.3     User Control                                                                   technical access controls such as those we have discussed. For
                                                                                       example, the “in an appropriate manner” opt-out provisions of the
Both robots.txt and active blocking (i.e., via firewall rules) presup-
                                                                                       EU’s AI Act are not prescriptive and will inevitably engage with the
pose that the content creator has the capability to change this state
                                                                                       challenges we have discussed in this work. Similarly to the extent
on the Web server hosting their content and that they have the
                                                                                       that any US court finds an affirmative “fair use” defense for AI
technical capability and domain knowledge to do so correctly.
                                                                                       model builders, this weakening of remedies on use will inevitably
    However, most content creators are not also system administra-
                                                                                       create an even stronger demand to enforce controls on access.
tors, nor do they run their own Web servers. Thus, these mech-
                                                                                           In summary, our work highlights the challenges for today’s con-
anisms are of most utility to larger organizations whose policy
                                                                                       tent creators with respect to AI use. First, there are no existing
interests can be aligned with their use of technical controls. Indeed,
                                                                                       standard mechanisms for explicitly controlling whether publicly-
in our data, we observed that multiple large publishers have re-
                                                                                       accessible Web content is used in training AI models. Second, the
moved restrictions in robots.txt for the sites they own after striking
                                                                                       existing mechanisms that have been brought to bear for this purpose
data usage deals with AI companies. This reversal shows that large
                                                                                       are poor fits for the task, lack appropriate specificity, comprehen-
content owners are willing to let their data be used for AI training,
                                                                                       siveness or verifiability. Third, these mechanisms are generally not
but only if they receive monetary compensation and/or site traffic 12
                                                                                       readily available to individual content creators and more serve the
in exchange for the usage of their data.
                                                                                       interests of large organizations. Last but not least, uncertainty and
    Since few creators maintain their own Web server, they must rely
                                                                                       differences exist around the legal protections for content creators.
on their website hoster to provide an interface to such capabilities
that creators can understand and is technically effective. However,
                                                                                        9    Acknowledgements
few hosters export robots.txt directly to their customers and most
do not provide any separate mechanism to express a desire to block                     We thank our shepherd Alessandro Finamore and the reviewers
AI bots. Finally, if a third party copies a creator’s content (e.g., posts             for their insightful and constructive suggestions and feedback. We
it on social media) no anti-crawler protections follow this content                    are also grateful to Kristen Vaccaro, Weijia He, and Lu Sun for
to its new host. Thus, to the extent creator control is possible, it                   providing feedback on our user study and drafts of our paper, artist
may be limited to direct accesses by AI crawlers.                                      Karla Ortiz for her input and help with the user study, and our
                                                                                       participants who took the survey. Many thanks also to Cindy Moore
8.4     Legal Uncertainty                                                              and Jennifer Folkestad for operational and administrative support
                                                                                       of our research. Funding for this work was provided in part by NSF
While this paper has focused on technical data access restrictions, it
                                                                                       grant SaTC-2241303 and ONR project #N00014-24-1-2669, the Irwin
is within a larger legal context about the extent to which copyright
                                                                                       Mark and Joan Klein Jacobs Chair in Information and Computer
holders will have an effective remedy if their content is accessed
                                                                                       Science, the CSE Professorship in Internet Privacy and/or Internet
12 For example, in the deal between OpenAI and Dotdash Meredith, one contract term     Data Security, and operational support from the UCSD Center for
requires that OpenAI must link to their site when displaying information relevant to   Networked Systems.
one of their subsidiaries [91].
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                                                 Enze Liu et al.


References                                                                                     29 pages.
  [1] Adobe. 2024. Adobe General Terms of Use. https://www.adobe.com/legal/terms.         [28] Michael Dinzinger and Michael Granitzer. 2024. A Longitudinal Study of Content
      html.                                                                                    Control Mechanisms. In Proc. of the ACM Web Conference. 1382–1387.
  [2] AIOSEO. 2025. The Best WordPress SEO Plugin and Toolkit. https://aioseo.com/        [29] Michael Dinzinger, Florian Heß, and Michael Granitzer. 2024. A Survey of Web
  [3] Safinah Ali and Cynthia Breazeal. 2023. Studying Artist Sentiments around                Content Control for Generative AI. (2024), 12 pages. arXiv:2404.02309 [cs.IR]
      AI-generated Artwork. (2023), 13 pages. arXiv:2311.13725 [cs.HC] https:                  https://arxiv.org/abs/2404.02309
      //arxiv.org/abs/2311.13725                                                          [30] Ziv Epstein, Aaron Hertzmann, Memo Akten, Hany Farid, Jessica Fjeld, Mor-
  [4] Yasmin AlNoamany, Michele C. Weigle, and Michael L. Nelson. 2013. Access                 gan R. Frank, Matthew Groh, Laura Herman, Neil Leach, Robert Mahari,
      Patterns for Robots and Humans in Web Archives. In Proc. of the 13th ACM/IEEE-           Alex “Sandy” Pentland, Olga Russakovsky, Hope Schroeder, and Amy Smith.
      CS Joint Conference on Digital Libraries. 339–348.                                       2023. Art and the science of generative AI. Science 380, 6650 (2023), 1110–1111.
  [5] Babak Amin Azad, Oleksii Starov, Pierre Laperdrix, and Nick Nikiforakis. 2020.      [31] Fairly Trained. 2024. Statement on AI training. https://www.aitrainingstatement.
      Web runner 2049: Evaluating third-party anti-bot services. In Proc. of 17th              org/.
      Detection of Intrusions and Malware, and Vulnerability Assessment. Springer,        [32] Richard Fletcher. 2024. How many news websites block AI crawlers? Reuters
      135–159.                                                                                 Institute Factsheets (2024), 7 pages.
  [6] Anthropic. 2024. Does Anthropic crawl data from the web, and how can site           [33] Foundation Web Design & Development. 2022. What is DeviantArt’s new "noai"
      owners block the crawler? https://support.anthropic.com/en/articles/8896518-             and "noimageai" meta tag and how to install it. https://www.foundationwebdev.
      does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-                    com/2022/11/noai-noimageai-meta-tag-how-to-install/.
      the-crawler                                                                         [34] Sheera Frenkel and Stuart A. Thompson. 2023. Not for Machines to Harvest: Data
  [7] ArtStation. 2025. ArtStation Terms of Service. https://www.artstation.com/tos.           Revolts Break Out Against A.I. — The New York Times. https://www.nytimes.
  [8] Stefan Baak. 2024. Training Data for the Price of a Sandwich. https://foundation.        com/2023/07/15/technology/artificial-intelligence-models-chat-data.html
      mozilla.org/en/research/library/generative-ai-training-data/common-crawl/.          [35] Manuel B. Garcia. 2024. The Paradox of Artificial Creativity: Challenges and
  [9] Quan Bai, Gang Xiong, Yong Zhao, and Longtao He. 2014. Analysis and De-                  Opportunities of Generative AI Artistry. Creativity Research Journal (2024),
      tection of Bogus Behavior in Web Crawler Measurement. Procedia Computer                  1–14.
      Science 31 (2014), 1084–1091.                                                       [36] generosus. 2023. PSA | Bytedance and Bytespider Bots | Recommend Block-
 [10] Kayleigh Barber. 2024. Future’s Jon Steinberg shares his philosophy on AI                ing. https://wordpress.org/support/topic/psa-bytedance-and-bytespider-bots-
      content licensing deals — Digiday. https://digiday.com/podcasts/futures-jon-             recommend-blocking/
      steinberg-shares-his-philosophy-on-ai-content-licensing-deals/.                     [37] Jonathan Gillham. 2024. Block AI Bots from Crawling Websites Using Robots.txt
 [11] Muhammad Ahmad Bashir, Sajjad Arshad, Engin Kirda, William Robertson, and                — Originality.ai. https://originality.ai/ai-bot-blocking
      Christo Wilson. 2019. A Longitudinal Analysis of the ads.txt Standard. In Proc.     [38] Google. 2024. Google Robots.txt Parser and Matcher Library. https://github.
      ACM Internet Measurement Conference 2019. 294–307.                                       com/google/robotstxt.
 [12] Lucas Bellaiche, Rohin Shahi, Martin Harry Turpin, Anya Ragnhildstveit, Shawn       [39] Paolo Grigis and Antonella De Angeli. 2024. Playwriting with Large Language
      Sprockett, Nathaniel Barr, Alexander Christensen, and Paul Seli. 2023. Humans            Models: Perceived Features, Interaction Strategies and Outcomes. In Proc. the
      versus AI: whether and why we prefer human-created compared to AI-created                International Conference on Advanced Visual Interfaces 2024. 1–9.
      artwork. Cognitive Research: Principles and Implications 8, 42 (2023), 22 pages.    [40] Alicia Guo, Shreya Sathyanarayanan, Leijie Wang, Jeffrey Heer, and Amy Zhang.
 [13] Alex Bocharov, Santiago Varagas, Adam Martinetti, Reid Tatoris,                          2025. From Pen to Prompt: How Creative Writers Integrate AI into their Writing
      and Carlos Azevedo. 2024.               Declare your AIndependence: block                Practice. (2025), 23 pages. arXiv:2411.03137 [cs.HC] https://arxiv.org/abs/2411.
      AI bots, scrapers and crawlers with a single click — Cloudflare.                         03137
      https://blog.cloudflare.com/declaring-your-aindependence-block-ai-bots-             [41] Eszter Hargittai. 2009. An Update on Survey Measures of Web-Oriented Digital
      scrapers-and-crawlers-with-a-single-click/.                                              Literacy. Social Science Computer Review 27, 1 (2009), 130–137.
 [14] Josiah D Boucher, Gillian Smith, and Yunus Doğan Telliel. 2024. Is Resistance       [42] Joo-Wha Hong and Nathaniel Ming Curran. 2019. Artificial Intelligence, Artists,
      Futile?: Early Career Game Developers, Generative AI, and Ethical Skepticism.            and Art: Attitudes Toward Artwork Produced by Humans vs. Artificial Intel-
      In Proc. of CHI Conference on Human Factors in Computing Systems 2024. 1–13.             ligence. ACM Transactions on Multimedia Computing, Communications, and
 [15] Virginia Braun and Victoria Clarke. 2006. Using thematic analysis in psychology.         Applications 15, 2s (2019), 1–16.
      Qualitative Research in Psychology 3, 2 (2006), 77–101.                             [43] Xinyi Hou, Yanjie Zhao, and Haoyu Wang. 2024. On the (In)Security of LLM
 [16] Jack Brewster, Zach Fishman, and Isaiah Glick. 2024. AI Chatbots Are Blocked             App Stores. (2024), 17 pages. arXiv:2407.08422 [cs.CR] https://arxiv.org/abs/
      by 67% of Top News Sites, Relying Instead on Low-Quality Sources — News                  2407.08422
      Guard. https://www.newsguardtech.com/special-reports/67-percent-of-top-             [44] Hongxian Huang, Runshan Fu, and Anindya Ghose. 2023. Generative AI and
      news-sites-block-ai-chatbots/.                                                           Content Creators: Evidence from Digital Art Platforms. SSRN (2023), 41 pages.
 [17] Gordon Burtch, Dokyun Lee, and Zhichen Chen. 2023. The consequences                 [45] Christos Iliou, Theodoros Kostoulas, Theodora Tsikrika, Vasilis Katos, Stefanos
      of generative AI for UGC and online community engagement. SSRN (2023),                   Vrochidis, and Ioannis Kompatsiaris. 2021. Detection of Advanced Web Bots
      26 pages.                                                                                by Combining Web Logs with Mouse Behavioural Biometrics. Digital Threats:
 [18] Carbonmade. 2024. Terms and Conditions of Use. https://carbonmade.com/                   Research and Practice 2, 3 (2021), 1–26.
      terms.                                                                              [46] Christos Iliou, Theodoros Kostoulas, Theodora Tsikrika, Vasilis Katos, Stefanos
 [19] Eva Cetinic and James She. 2022. Understanding and Creating Art with AI:                 Vrochidis, and Yiannis Kompatsiaris. 2019. Towards a framework for detecting
      Review and Outlook. ACM Transactions on Multimedia Computing, Communi-                   advanced web bots. In Proc. of 14th International Conference on Availability,
      cations, and Applications 18, 2 (2022), 1–22.                                            Reliability and Security. 1–10.
 [20] Zi Chu, Steven Gianvecchio, and Haining Wang. 2018. Bot or Human? A                 [47] Katy Ilonka Gero, Meera Desai, Carly Schnitzler, Nayun Eom, Jack Cushman,
      Behavior-Based Online Bot Detection System. From Database to Cyber Security:             and Elena L. Glassman. 2024. Creative Writers’ Attitudes on Writing as Training
      Essays Dedicated to Sushil Jajodia on the Occasion of His 70th Birthday (2018),          Data for Large Language Models. In Proc. of CHI Conference on Human Factors
      432–449.                                                                                 in Computing Systems 2025. 1–16.
 [21] Cloudflare. 2024. Verified Bots. https://radar.cloudflare.com/traffic/verified-     [48] Imperva. 2024. 2024 Bad Bot Report. https://www.imperva.com/resources/
      bots.                                                                                    resource-library/reports/2024-bad-bot-report/.
 [22] European Commission. 2024.               First Draft of the General-Purpose         [49] Gregoire Jacob, Engin Kirda, Christopher Kruegel, and Giovanni Vigna. 2012.
      AI Code of Practice published, written by independent experts.                           PUBCRAWL: Protecting Users and Businesses from CRAWLers. In Proc. of 21st
      https://digital-strategy.ec.europa.eu/en/library/first-draft-general-purpose-            USENIX Security Symposium. 507–522.
      ai-code-practice-published-written-independent-experts                              [50] Steve TK Jan, Qingying Hao, Tianrui Hu, Jiameng Pu, Sonal Oswal, Gang Wang,
 [23] European Commission. 2024.                 The AI Act Explorer.            https:        and Bimal Viswanath. 2020. Throwing Darts in the Dark? Detecting Bots with
      //artificialintelligenceact.eu/ai-act-explorer/.                                         Limited Data using Neural Data Augmentation. In Proc. of 2020 IEEE Symposium
 [24] Common Crawl. 2025. Common Crawl — Open Repository of Web Crawl Data.                    on Security and Privacy. IEEE, 1190–1206.
      https://commoncrawl.org/                                                            [51] Harry H Jiang, Lauren Brown, Jessica Cheng, Mehtab Khan, Abhishek Gupta,
 [25] davepattern. 2024. DDoS from Anthropic AI. https://www.linode.com/                       Deja Workman, Alex Hanna, Johnathan Flowers, and Timnit Gebru. 2023. AI
      community/questions/24842/ddos-from-anthropic-ai.                                        Art and its Impact on Artists. In Proc. of AAAI ACM Conference on AI, Ethics,
 [26] deninho32. 2024. Claudebot attack. https://www.phpbb.com/community/                      and Society 2023. 363–374.
      viewtopic.php?t=2652265.                                                            [52] Hannah Johnston and David Thue. 2024. Understanding Visual Artists’ Values
 [27] Design and Artists Copyright Society (DACS). 2024. Artificial Intelligence               and Attitudes towards Collaboration, Technology, and AI. In Proc. 50th Graphics
      and Artists’ Work: A survey of artists on AI. https://cdn.dacs.org.uk/uploads/           Interface Conference. 1–9.
      documents/News/Artificial-Intelligence-and-Artists-Work-DACS.pdf. (2024),           [53] Ben Jones, Tzu-Wen Lee, Nick Feamster, and Phillipa Gill. 2014. Automated
                                                                                               Detection and Fingerprinting of Censorship Block Pages. In Proc. of ACM Internet
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers                     IMC ’25, October 28–31, 2025, Madison, WI, USA.


      Measurement Conference 2014. 299–304.                                                [77] Cullen Miller. 2023. ai.txt: A new way for websites to set permissions for AI —
 [54] Hugo Jonker, Benjamin Krumnow, and Gabry Vlot. 2019. Fingerprint Surface-                 Spawning. https://spawning.substack.com/p/aitxt-a-new-way-for-websites-to-
      Based Detection of Web Bot Detectors. In Proc. of 24th European Symposium on              set.
      Research in Computer Security. Springer, 586–605.                                    [78] Piotr Mirowski, Juliette Love, Kory Mathewson, and Shakir Mohamed. 2024. A
 [55] Reishiro Kawakami and Sukrit Venkatagiri. 2024. The Impact of Generative AI               Robot Walks into a Bar: Can Language Models Serve as Creativity Support Tools
      on Artists. In Proc. of 16th Conference on Creativity & Cognition. 79–82.                 for Comedy? An Evaluation of LLMs’ Humour Alignment with Comedians. In
 [56] Paul Keller. 2023.          Protecting Creatives or Impeding Progress? Ma-                Proc. of the ACM Conference on Fairness, Accountability, and Transparency 2024.
      chine learning and the EU copyright framework — Open Future.                              1622–1636.
      https://openfuture.eu/blog/protecting-creatives-or-impeding-progress/.               [79] Martin Monperrus. 2024. crawler-user-agents. https://github.com/monperrus/
 [57] Kate Knibbs. 2024. Condé Nast Signs Deal With OpenAI — Wired. https:                      crawler-user-agents.
      //www.wired.com/story/conde-nast-openai-deal/.                                       [80] Alexis Newton and Kaustubh Dhole. 2023. Is AI Art Another Industrial Rev-
 [58] Kate Knibbs. 2024. The Race to Block OpenAI’s Scraping Bots Is Slowing Down —             olution in the Making? (2023), 6 pages. arXiv:2301.05133 [cs.AI] https:
      Wired. https://www.wired.com/story/open-ai-publisher-deals-scraping-bots/.                //arxiv.org/abs/2301.05133
 [59] Robb Knight. 2024. Perplexity AI Is Lying about Their User Agent. https:             [81] Republic of Singapore. 2021. Singapore Copyright Act of 2021: Section 244
      //rknight.me/blog/perplexity-ai-is-lying-about-its-user-agent/                            (English Translation). https://sso.agc.gov.sg/Acts-Supp/22-2021/Published/
 [60] Santanu Kolay, Paolo D’Alberto, Ali Dasdan, and Arnab Bhattacharjee. 2008. A              ?ProvIds=pr244-.
      Larger Scale Study of Robots.txt. In Proc. of 17th World Wide Web Conference.        [82] OpenAI. 2023. Our approach to AI safety. https://openai.com/index/our-
      1171–1172.                                                                                approach-to-ai-safety/
 [61] Martijn Koster, Gary Illyes, Henner Zeller, and Lizzi Sassman. 2022. Robots          [83] Karla Ortiz. 2024. Why AI Models are not inspired like humans.              https:
      Exclusion Protocol. RFC 9309. https://doi.org/10.17487/RFC9309                            //www.kortizblog.com/blog/why-ai-models-are-not-inspired-like-humans
 [62] Shinil Kwon, Young-Gab Kim, and Sungdeok Cha. 2012. Web robot detection              [84] Stack Overflow. 2024. Stack Overflow and OpenAI Partner to Strengthen
      based on pattern-matching technique. Journal of Information Science 38, 2 (2012),         the World’s Most Popular Large Language Models. https://stackoverflow.co/
      118–126.                                                                                  company/press/archive/openai-partnership.
 [63] IAB Tech Lab. 2025. Global Privacy Protocol. https://iabtechlab.com/gpp/             [85] palewire. 2025. Who blocks OpenAI, Google AI and Common Crawl? https:
 [64] Rita Latikka, Jenna Bergdahl, Nina Savela, and Atte Oksanen. 2023. AI as                  //palewi.re/docs/news-homepages/openai-gptbot-robotstxt.html
      an Artist? A Two-Wave Survey Study on Attitudes Toward Using Artificial              [86] Sungjin Park. 2024. The work of art in the age of generative AI: aura, liberation,
      Intelligence in Art. Poetics 101 (2023), 11 pages.                                        and democratization. AI & Society (2024), 1–10.
 [65] Junsup Lee, Sungdeok Cha, Dongkun Lee, and Hyungkyu Lee. 2009. Classi-               [87] Perplexity. 2025. Perplexity Crawlers. https://docs.perplexity.ai/guides/bots.
      fication of web robots: an empirical study based on over one billion requests.       [88] Kien Pham, Aécio Santos, and Juliana Freire. 2016. Understanding Website
      Computers & Security 28, 8 (2009), 795–802.                                               Behavior based on User Agent. In Proc. of 39th ACM SIGIR Conference on Research
 [66] Jie Li, Hancheng Cao, Laura Lin, Youyang Hou, Ruihao Zhu, and Abdallah El                 and Development in Information Retrieval. 1053–1056.
      Ali. 2024. User Experience Design Professionals’ Perceptions of Generative           [89] Tara Poteat and Frank Li. 2021. Who You Gonna Call? An Empirical Evaluation
      Artificial Intelligence. In Proc. of CHI Conference on Human Factors in Computing         of Website security.txt Deployment. In Proc. of ACM Internet Measurement
      Systems 2024. 1–18.                                                                       Conference 2021. 526–532.
 [67] Xigao Li, Babak Amin Azad, Amir Rahmati, and Nick Nikiforakis. 2021. Good            [90] Heila Precel, Allison McDonald, Brent Hecht, and Nicholas Vincent. 2024. A
      Bot, Bad Bot: Characterizing Automated Browsing Activity. In Proc. of 2021 IEEE           Canary in the AI Coal Mine: American Jews May Be Disproportionately Harmed
      Symposium on Security and Privacy. IEEE, 1589–1605.                                       by Intellectual Property Dispossession in Large Language Model Training. In
 [68] Baker & Hostetler LLP. 2024. Case Tracker: Artificial Intelligence, Copyrights            Proc. of CHI Conference on Human Factors in Computing Systems 2024. 1–17.
      and Class Actions. https://www.bakerlaw.com/services/artificial-intelligence-        [91] PRNewswire. 2024. Dotdash Meredith Announces Strategic Partnership
      ai/case-tracker-artificial-intelligence-copyrights-and-class-actions/                     with OpenAI, Bringing Iconic Brands and Trusted Content to ChatGPT.
 [69] Joseph Saveri Law Firm LLP. 2023.                   Class Action Filed Against            https://dotdashmeredith.mediaroom.com/2024-05-07-Dotdash-Meredith-
      Stability AI, Midjourney, and DeviantArt for DMCA Violations,                             Announces-Strategic-Partnership-with-OpenAI,-Bringing-Iconic-Brands-
      Right of Publicity Violations, Unlawful Competition, Breach of TOS.                       and-Trusted-Content-to-ChatGPT.
      https://www.prnewswire.com/news-releases/class-action-filed-against-                 [92] Gayatri Raman and Erin Brady. 2024. Exploring Use and Perceptions of Genera-
      stability-ai-midjourney-and-deviantart-for-dmca-violations-right-of-                      tive AI Art Tools by Blind Artists. (2024), 4 pages. arXiv:2409.08226 [cs.HC]
      publicity-violations-unlawful-competition-breach-of-tos-301721869.html                    https://arxiv.org/abs/2409.08226
 [70] Shayne Longpre, Robert Mahari, Ariel Lee, Campbell Lund, Hamidah Oderin-             [93] rejeptai. 2024.       Why doesn’t ClaudeBot/Anthropic obey robots.txt?
      wale, William Brannon, Nayan Saxena, Naana Obeng-Marnu, Tobin South, Cole                 https://www.reddit.com/r/Anthropic/comments/1c8tu5u/why_doesnt_
      Hunter, Kevin Klyman, Christopher Klamm, Hailey Schoelkopf, Nikhil Singh,                 claudebot_anthropic_obey_robotstxt/
      Manuel Cherep, Ahmad Anis, An Dinh, Caroline Chitongo, Da Yin, Damien Sileo,         [94] Copyright Research and Information Center. 2019. Copyright Law of Japan:
      Deividas Mataciunas, Diganta Misra, Emad Alghamdi, Enrico Shippole, Jianguo               Chapter II Rights of Authors (English Translation). https://www.cric.or.jp/
      Zhang, Joanna Materzynska, Kun Qian, Kush Tiwary, Lester Miranda, Manan                   english/clj/cl2.html.
      Dey, Minnie Liang, Mohammed Hamdy, Niklas Muennighoff, Seonghyeon Ye,                [95] Stefano Rovetta, Alberto Cabri, Francesco Masulli, and Grażyna Suchacka. 2019.
      Seungone Kim, Shrestha Mohanty, Vipul Gupta, Vivek Sharma, Vu Minh Chien,                 Bot or Not? A Case Study on Bot Recognition from Web Session Logs. Quanti-
      Xuhui Zhou, Yizhi Li, Caiming Xiong, Luis Villa, Stella Biderman, Hanlin Li,              fying and Processing Biomedical and Behavioral Signals (2019), 197–206.
      Daphne Ippolito, Sara Hooker, Jad Kabbara, and Sandy Pentland. 2024. Con-            [96] Quirin Scheitle, Oliver Hohlfeld, Julien Gamba, Jonas Jelten, Torsten Zimmer-
      sent in Crisis: The Rapid Decline of the AI Data Commons. (2024), 41 pages.               mann, Stephen D. Strowes, and Narseo Vallina-Rodriguez. 2018. A Long Way to
      arXiv:2407.14933 [cs.CL] https://arxiv.org/abs/2407.14933                                 the Top: Significance, Structure, and Stability of Internet Top Lists. In Proc. of
 [71] Anália G. Lourenço and Orlando O. Belo. 2006. Catching Web Crawlers in the                ACM Internet Measurement Conference 2018. 478–493.
      Act. In Proc. of 6th International Conference on Web Engineering. 265–272.           [97] M. H. M. Schellekens. 2013. Robot.txt: balancing interests of content producers
 [72] Juniper Lovato, Julia Witte Zimmerman, Isabelle Smith, Peter Dodds, and Jen-              and content users. Bridging Distances in Technology and Regulation (2013),
      nifer L. Karson. 2024. Foregrounding Artist Opinions: A Survey Study on                   173–187.
      Transparency, Ownership, and Fairness in AI Generative Art. In Proc. of AAAI         [98] Barry Schwartz. 2023. Google-Extended does not stop Google Search Generative
      ACM Conference on AI, Ethics, and Society 2024. 905–916.                                  Experience from using your site’s content. https://searchengineland.com/google-
 [73] Abhijeeth Madhu. 2023. Survey Reveals 9 out of 10 Artists Believe Current                 extended-does-not-stop-google-search-generative-experience-from-using-
      Copyright Laws are Outdated in the Age of Generative AI Technology —                      your-sites-content-433058.
      Book An Artist Blog. https://bookanartist.co/blog/2023-artists-survey-on-ai-         [99] Yoast SEO. 2025. SEO starts with Yoast. https://yoast.com/
      technology/                                                                         [100] Shawn Shan, Jenna Cryan, Emily Wenger, Haitao Zheng, Rana Hanocka, and
 [74] Bron Maher. 2024. Revealed: Which of the top 100 UK and US news websites                  Ben Y Zhao. 2023. Glaze: Protecting Artists from Style Mimicry by Text-to-Image
      are blocking AI crawlers — PressGazette. https://pressgazette.co.uk/platforms/            Models. In Proc. of 32nd USENIX Security Symposium. 2187–2204.
      news-sites-block-ai-web-crawlers-chatgpt-google/                                    [101] Shawn Shan, Wenxin Ding, Josephine Passananti, Stanley Wu, Haitao Zheng,
 [75] Meta. 2024. Meta Web Crawlers. https://developers.facebook.com/docs/sharing/              and Ben Y. Zhao. 2024. Nightshade: Prompt-Specific Poisoning Attacks on
      webmasters/web-crawlers/.                                                                 Text-to-Image Generative Models. In Proc. of IEEE Symposium on Security and
 [76] Elzė Sigutė Mikalonytė and Markus Kneer. 2022. Can Artificial Intelligence             Privacy 2024. 807–825.
      Make Art?: Folk Intuitions as to whether AI-driven Robots Can Be Viewed as          [102] Jingyu Shi, Rahul Jain, Runlin Duan, and Karthik Ramani. 2023. Understanding
      Artists and Produce Art. ACM Transactions on Human-Robot Interaction 11, 4                Generative AI in Art: An Interview Study with Artists on G-AI from an HCI
      (2022), 1–19.                                                                             Perspective. (2023), 15 pages. arXiv:2310.13149 [cs.HC] https://arxiv.org/abs/
                                                                                                2310.13149
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                                    Enze Liu et al.


[103] Dusan Stevanovic, Aijun An, and Natalija Vlajic. 2012. Feature evaluation                  Snapshot          Month      # Sites   + robots.txt
      for web crawler detection with data mining techniques. Expert Systems with
      Applications 39, 10 (2012), 8707–8717.                                                       2022-05    Sep/Oct 2022    40177        31494
[104] Dongxun Su, Yanjie Zhao, Xinyi Hou, Shenao Wang, and Haoyu Wang. 2024.                       2022-21   Nov/Dec 2022     40614        31536
      GPT Store Mining and Analysis. (2024), 16 pages. arXiv:2405.10210 [cs.LG]                    2022-40    Jan/Feb 2023    39080        30063
      https://arxiv.org/abs/2405.10210
[105] Grażyna Suchacka, Alberto Cabri, Stefano Rovetta, and Francesco Masulli. 2021.               2023-06   Mar/Apr 2023     39216        29963
      Efficient on-the-fly Web bot detection. Knowledge-Based Systems 223 (2021),                  2023-14   May/Jun 2023     39212        30107
      16 pages.                                                                                    2023-23    Sep/Oct 2023    39033        29721
[106] Mark Sullivan. 2024. AI Companies Ignoring Robots.txt. https://mjtsai.com/                   2023-40   Nov/Dec 2023     39722        30060
      blog/2024/06/24/ai-companies-ignoring-robots-txt/
[107] Yang Sun, Ziming Zhuang, Isaac G. Councill, and C. Lee Giles. 2007. Deter-                   2023-50   Feb/Mar 2024     41446        31282
      mining Bias to Search Engines from Robots.txt. In Proc. of IEEE WIC ACM Web                  2024-10        Apr 2024    41640        31010
      Intelligence and Intelligent Agent Technology 2007. 149–155.                                 2024-18       May 2024     41004        30763
[108] Yang Sun, Ziming Zhuang, and C. Lee Giles. 2007. A Large-Scale Study of                      2024-22        Jun 2024    41047        30661
      Robots.txt. In Proc. of 16th World Wide Web Conference. 1123–1124.
[109] David Sénécal. 2024. The Web Scraping Problem: Part 1 — Akamai. https:                       2024-26         Jul 2024   40927        30526
      //www.akamai.com/blog/security/the-web-scraping-problem-part-1.                              2024-33       Aug 2024     40455        29922
[110] Reid Tatoris, Harsh Saxena, and Luis Miglietti. 2025. Trapping misbehaving                   2024-38        Sep 2024    40444        29806
      bots in an AI Labyrinth — Cloudflare. https://blog.cloudflare.com/ai-labyrinth/              2024-42        Oct 2024    40420        29867
[111] Antoine Vastel, Walter Rudametkin, Romain Rouvoy, and Xavier Blanc. 2020. FP-
      Crawlers: Studying the Resilience of Browser Fingerprinting to Block Crawlers.
      In Proc. of NDSS Workshop on Measurements, Attacks, and Defenses for the Web.
                                                                                        Table 3: Snapshots used in the historic AI crawler analysis:
      13 pages.                                                                         the months they cover, the number of sites in the Stable Top
[112] James Vincent. 2023. Getty Images is suing the creators of AI art tool Stable     100k in each snapshot, and the number of those sites that
      Diffusion for scraping its content — The Verge. https://www.theverge.com/
      2023/1/17/23558516/ai-art-copyright-stable-diffusion-getty-images-lawsuit         have a robots.txt file in the snapshot.
[113] Dark Visitors. 2024. Agents. https://darkvisitors.com/agents.
[114] Dark Visitors. 2025. Track the AI Agents and Bots Crawling Your Website.
      https://darkvisitors.com/
[115] W3Techs. 2024. Usage statistics and market shares of reverse proxy services.
                                                                                        robots.txt files by taking the most recent non-errored crawl in
      https://w3techs.com/technologies/overview/proxy.                                  the snapshot. The Common Crawl crawler also does not follow
[116] Wikipedia contributors. 2020. Global Privacy Control — Wikipedia. https:          redirects. To improve our coverage, for domains that returned a non-
      //en.wikipedia.org/wiki/Global_Privacy_Control
[117] Wix. 2025. Wix.com Terms of Use. https://www.wix.com/about/terms-of-use.          200 HTTP status code to Common Crawl (such as 301 Redirect), we
[118] Chloe Xiang. 2022. Artists Are Revolting Against AI Art on ArtStation —           also checked Common Crawl for the robots.txt file for the domain
      Vice. https://www.vice.com/en/article/ake9me/artists-are-revolt-against-ai-       prepended with “www.” (if not already) and without (if already
      art-on-artstation
[119] Chyan Yang and Hsien-Jyh Liao. 2010. Using the Robots. txt and Robots Meta        prepended).
      tags to implement online copyright and a related amendment. Library Hi Tech
      28, 1 (2010), 94–106.
[120] Zejun Zhang, Li Zhang, Xin Yuan, Anlan Zhang, Mengwei Xu, and Feng Qian.
                                                                                        B.2    Robots.txt edge cases
      2024. A First Look at GPT Apps: Landscape and Vulnerability. (2024), 11 pages.    When experimenting with robots.txt parsers from both Google
      arXiv:2402.15105 [cs.CR] https://arxiv.org/abs/2402.15105
[121] Eric Zhou and Dokyun Lee. 2024. Generative artificial intelligence, human         and [70], we discovered three edge cases that can lead to very
      creativity, and art. PNAS Nexus 3, 3 (2024), 8 pages.                             different interpretations of a robots.txt file depending on whether
[122] Viola Zhou. 2023. AI is already taking video game illustrators’ jobs in China     a parser is fully compliant with RFC 9309.
      — Rest of World. https://restofworld.org/2023/ai-china-video-game-layoffs-
      illustrators/                                                                     Case 1. For the following robots.txt, a compliant parser will
                                                                                        ignore comments or newlines after the “User-agent” line and re-
A     Ethics                                                                            spect the “Disallow” directives. If a parser does not handle such
We believe our work has very low ethical risk. Our user study is                        comments or newlines correctly, the parser may skip and ignore
approved by the IRB at our institution. Our longitudinal analysis                       the “Disallow” directives:
leverages common crawl data, which is publicly available and does
not contain any personal information, and our active blocking                                      User-agent: *
experiments are conducted at a responsible rate. We also make our                                  # Blog restrictions
data and code available to the community at https://github.com/                                    Disallow: /blog/latest/*
ucsdsysnet/ai-crawler-imc-25.                                                                      Disallow: /blogs/*

B Historic Use of Robots.txt                                                            Case 2. RFC 9309 allows “User-agent” directives to be grouped
B.1 Common Crawl Snapshots                                                              as shown below. A non-compliant parser, however, can ignore all
For our historic robots.txt analysis (Section 3), we used data from                     such grouped “User-agent” lines except for the last when parsing
15 consecutive snapshots from Common Crawl from October 2022                            robots.txt:
to October 2024. Table 3 lists each Common Crawl snapshot, the
months it covers (as reported by Common Crawl’s website), and the                                  User-agent: GPTBot
number of sites that are in the Stable Top 100k and have a robots.txt                              User-agent: anthropic-ai
file in each particular snapshot. For each snapshot, Common Crawl                                  User-agent: Claudebot
may crawl a site several times over the period in which the data                                   Disallow: /
for the snapshot was collected. In these cases, we deduplicate the
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers                   IMC ’25, October 28–31, 2025, Madison, WI, USA.


Case 3. Using unsupported directives can have unintended con-                               Site                         Snapshot   Site                        Snapshot

sequences. For example, “Crawl-delay” is a non-standard extension                           nfhs.org                     2023-40    bleedcubbieblue.com         2024-42
                                                                                            10best.com                   2023-40    popsugar.com                2024-42
supported by some crawlers and ignored by others, a situation that                          ground.news                  2023-40    voxmedia.com                2024-42
can lead to unexpected results depending on the parser used by                              opindia.com                  2024-42    patspulpit.com              2024-42
                                                                                            tarleton.edu                 2023-50    barcablaugranes.com         2024-42
the crawler. Google’s compliant robots.txt parser will ignore the                           alldatasheet.com             2024-42    eater.com                   2024-42
“Crawl-delay” directive and effectively treat it as a blank line. As a                      bestproductsreviews.com      2024-42    popsugar.co.uk              2024-42
                                                                                            network54.com                2023-50    prideofdetroit.com          2024-42
result, in the following robots.txt the “User-agent: *” directive will                      care.com                     2024-42    royalsreview.com            2024-42
                                                                                            kbs.co.kr                    2024-42    truebluela.com              2024-42
be combined with the “User-agent: GoogleBot” directive due to the                           brit.co                      2024-42    thrillist.com               2024-42
grouping rule (ignoring “Crawl-delay” and effectively grouping the                          lonza.com                    2024-42    sbnation.com                2024-42
                                                                                            millersville.edu             2024-42    arrowheadpride.com          2024-42
two “User-agent” lines together):                                                           icelandair.com               2024-42    theringer.com               2024-42
                                                                                            customink.com                2024-42    adslzone.net                2024-42
                                                                                            celebmafia.com               2024-18    milehighreport.com          2024-42
              User-agent: *                                                                 credit-agricole.fr           2024-42    polygon.com                 2024-42
                                                                                            adelaidenow.com.au           2024-42    racked.com                  2024-42
              Disallow: /                                                                   dailytelegraph.com.au        2024-42    behindthesteelcurtain.com   2024-42
                                                                                            walkhighlands.co.uk          2024-42    bavarianfootballworks.com   2024-42
                                                                                            softonic-ar.com              2024-22    bleedinggreennation.com     2024-42
              User-agent: *                                                                 heraldsun.com.au             2024-42    silverscreenandroll.com     2024-42
              Crawl-delay: 5                                                                royalsocietypublishing.org   2024-22    gnc.com                     2024-42
                                                                                            softonic.com                 2024-42    cagesideseats.com           2024-42
                                                                                            shopstyle.com                2024-42    blazersedge.com             2024-42
              User-agent: GoogleBot                                                         couriermail.com.au
                                                                                            theaustralian.com.au
                                                                                                                         2024-42
                                                                                                                         2024-42
                                                                                                                                    badlefthook.com
                                                                                                                                    cincyjungle.com
                                                                                                                                                                2024-42
                                                                                                                                                                2024-42
              Allow: /                                                                      news.com.au                  2024-42    hogshaven.com               2024-42
                                                                                            kaufland.de                  2024-42    bigblueview.com             2024-42
              Disallow: /z/                                                                 sendpulse.com                2024-26    ninersnation.com            2024-42
                                                                                            washingtonexaminer.com       2024-33    pinstripealley.com          2024-42
                                                                                            thedodo.com                  2024-42    bloggingtheboys.com         2024-42
   In contrast, a parser that obeys the non-standard “Crawl-delay”                          g2a.com                      2024-42    quickbase.com               2024-42
                                                                                            fieldgulls.com               2024-42    embluemail.com              2024-42
directive will not group together the two “User-agent” lines (only                          recode.net                   2024-42    softonic.com.br             2024-42
the GoogleBot user agent will be associated with the two “Al-                               novartis.com                 2024-38    stimulustech.com            2024-42
                                                                                            mmafighting.com              2024-42    searchenginejournal.com     2024-42
low/Disallow” rules).                                                                       vox.com                      2024-42    giant-bicycles.com          2024-42
                                                                                            mmamania.com                 2024-42    realself.com                2024-42

B.3     Domains that explicitly allow GPTBot                                           Table 4: Domains that explicitly and fully allow GPTBot in
Table 4 shows the list of domains that explicitly and fully allow                      their robots.txt, and the Common Crawl snapshot in which
GPTBot in their robots.txt with a directive such as:                                   we first observed this behavior.
              User-agent: GPTBot
              Allow: /
                                                                                        C.2        Cloudflare “Definitely Automated”
as well as the Common Crawl snapshot in which we first ob-
                                                                                       The following list shows the user agents we inferred Cloudflare’s
served this behavior. We note that five sites (nfhs.org, 10best.com,
                                                                                       “Definitely Automated” setting to block:
ground.news, network54.com, and tarleton.edu) have persistently
allowed GPTBot since around the time of its release to our latest                                      360Spider                      libwww-perl
snapshot.                                                                                              AHC                            magpie-crawler
                                                                                                       aiohttp                        MeltwaterNews
C Active Blocking                                                                                      anthropic-ai                   node-fetch
                                                                                                       Apache-HttpClient              Nutch
C.1 Squarespace Restricted AI Bots                                                                     axios                          omgili
The following directives are added to the robots.txt file for a Squares-                               binlar                         PerplexityBot
pace site when a customer turns off the “Artificial Intelligence                                       Bytespider                     PhantomJS
Crawlers” option:                                                                                      CCBot                          PHP-Curl-Class
              User-agent: GPTBot                                                                       centurybot                     PiplBot
              User-agent: ChatGPT-User                                                                 Claudebot                      python-requests
              User-agent: CCBot                                                                        curl                           Python-urllib
              User-agent: anthropic-ai                                                                 Diffbot                        Scrapy
              User-agent: Google-Extended                                                              Go-http-client                 serpstatbot
              User-agent: FacebookBot                                                                  grub.org                       Teoma
              User-agent: Claude-Web                                                                   HeadlessChrome                 W3C-checklink
              User-agent: cohere-ai                                                                    httpx                          wget
              User-agent: PerplexityBot                                                    We note that IP address likely plays a role in the operation of
              User-agent: Applebot-Extended                                             this setting to block “fake” verified bots (e.g., a request that claims
              Disallow: /                                                               to be a particular Cloudflare Verified Bot, but does not come from
                                                                                        a documented IP address). We exclude these user agents from the
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                        Enze Liu et al.


list, but note that the list of Cloudflare verified bots is publicly          Q9. How do you host your personal website?
available [21].                                                                   • I have my own server • Free service (e.g., free server with AWS)
                                                                                  • Paid service (e.g., Squarespace with a custom domain)
C.3     Cloudflare’s “Block AI Scrapers and                                       • Other (please specify)
                                                                              Q10. What is the name of the service you use?
        Crawlers”                                                                 Answer:
The following user agents are blocked by Cloudflare’s “Block AI               Q11. Why did you choose the service?
Scrapers and Crawlers” option:                                                    Answer:
             Amazonbot                Diffbot/                                Q12. [Optional] If you’re comfortable, please share a link to your
                                                                            personal website.
             AwarioRssBot             GPTBot/
                                                                                  Answer:
             AwarioSmartBot           magpie-crawler
             Bytespider               MeltwaterNews                         Questions about impressions of AI art and their actions
             CCBot/                   omgili/                                  Q13. How familiar are you with AI-generated art?
             ChatGPT-User             PerplexityBot                                 • Not familiar at all
             Claude-Web               PiplBot                                       • Slightly familiar
             ClaudeBot                YouBot                                        • Somewhat familiar
             cohere-ai                                                              • Moderately familiar
                                                                                    • Very familiar
Note that AwarioRssBot, AwarioSmartBot, magpie-crawler, and
                                                                               Q14. Do you use AI in your artistic process?
MeltwaterNews are not in the Dark Visitors list of AI user agents.                  • Never • Rarely • Sometimes • Often • Always
                                                                               Q15. Please briefly describe your general impression of AI-generated
D Artist Survey                                                             art.
D.1 Survey Questions                                                                Answer:
                                                                               Q16. How much impact do you expect AI-generated art to have
In this section, we provide the list of questions that we asked in the      on your job security?
artist survey. We omit the questions related to contact information                 • No impact • Minor impact • Moderate impact
and compensation. Our study was approved by our university’s                        • Significant impact • Severe impact
Institutional Review Board (IRB).                                              Q17. Have you taken any actions because of the increasing use of
                                                                            AI-generated art in recent years?
Questions about artistic background                                                 • Yes • No
  Q1. Do you consider yourself a professional artist?                          Q18. What actions have you taken? (Select all that apply)
        • Yes • No                                                                  • Reducing the amount of my artwork that I share online
  Q2. What portion of your income comes from your art?                              • Actively removing my old artwork from the Internet
        • I haven’t made any money from my art                                      • Posting lower resolution versions of my artwork online
        • I make some income from my art but it’s not the main source               • Learning about AI art tools and possibly using them
        • My art is my main source of income                                        • Preventing my websites from being scraped
  Q3. How long have you been making money from your art?                            • Using Glaze to protect my art before posting
        • Less than 1 year • 1–5 years • 5–10 years • 10 years or more              • Other (please specify)
  Q4. What type of art do you do? (Select all that apply)                      Q19. Please elaborate on how you prevent your websites from
        • Concept Art • Traditional Painting and Drawing • Photography      being scraped.
        • Abstract • Illustration • Game Art • Anime and Manga Art                  Answer:
        • Digital 2D • Digital 3D • Traditional Sculpting • Environmental      Q20. Do you plan to take any actions because of the increasing
       • Character and Creature Design • Comicbook Art • Matte Painting     use of AI-generated art in recent years?
        • Items Props • Other (please specify)                                      • Yes • No
  Q5. Which country do you live in?                                            Q21. What actions do you plan to take? (Select all that apply)
        • Australia • Brazil • Canada • China • France • Germany • India            • Reducing the amount of my artwork that I share online
        • Italy • Japan • Mexico • Russia • South Africa • Spain                    • Actively removing my old artwork from the Internet
        • United Kingdom • United States • Other (please specify)                   • Posting lower resolution versions of my artwork online
                                                                                    • Learning about AI art tools and possibly using them
Questions about technical background                                                • Using Glaze to protect my art before posting
  Q6. How familiar are you with the following computer and inter-
                                                                                    • Preventing my websites from being scraped
net items? (1-5; 1 = no understanding, 5 = full understanding.)                     • Other (please specify)
        • Website • Generative AI • Search engine                              Q22. If your website hosting platform offers a mechanism (e.g. by
        • Nearest diffusion tree • Robots.txt                               clicking a button) to tell AI companies that you would like them not
  Q7. Do you post your art online?                                          to scrape your website, how likely will you enable this mechanism?
        • Yes • No                                                                  • Not likely at all • Unlikely • Neutral / Undecided
  Q8. Where do you post art online? (Select all that apply)                         • Likely • Very likely
        • Social Media (Instagram, LinkedIn, . . . )                            Why or why not? Answer:
        • Art Platforms (ArtStation, DeviantArt, . . . )                       Q23. If your website hosting platform offers a mechanism (e.g. by
        • Personal Website                                                  clicking a button) to block AI companies from scraping your website,
        • Art Seller Websites (Artsy, Artrepreneur, . . . )                 how likely will you enable this mechanism?
        • Other (please specify)
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers                IMC ’25, October 28–31, 2025, Madison, WI, USA.


      • Not likely at all • Unlikely • Neutral / Undecided                                      • I find it hard to write the robots.txt
      • Likely • Very likely                                                                    • I don’t know how to use it
    Why or why not? Answer:                                                                     • Other (please specify)

Questions about knowledge of robots.txt
    Q24. Have you heard about robots.txt before today?
         • Yes • No                                                                     D.2     Demographics
    Description of robots.txt for artists who select “no” in Q24. This                 This section presents the demographics of the participants in our
description is generated with the help of ChatGPT.
                                                                                       survey. As previously mentioned, we focus on their artistic back-
         Do you know that over 90% of artists don’t realize they can use a
simple tool called robots.txt to stop automated programs (also known as
                                                                                       ground, as it is the most relevant to our study.
bots) from downloading content from their websites? Think of robots.txt
as a “Do Not Enter” sign for automated programs that browse the internet.                                      Duration                Count
When placed on a website, it tells these automated programs which parts
of the site they’re not allowed to access. While it won’t stop every bot, it                                   Less than 1 year             17
works like a polite request to keep things like personal galleries or portfolios                               1–5 years                    68
hidden from search engines or unwanted bots. This is an easy way for artists                                   5–10 years                   44
to protect their work and control how it appears online, without needing to                                    10 years or more             47
dive into complicated tech or legal steps. Adding a robots.txt file can be a
                                                                                                               Total                       176
quick win for maintaining privacy and keeping unwanted eyes off your art.
        That being said, it is important to note that not all companies respect        Table 5: How long participants have been making money
robots.txt—some may ignore it entirely if they choose to.                              from their art.
    Q25. Briefly describe what you think robots.txt does.
         Answer:
                                                                                          Table 5 presents a breakdown of how long participants have
    Q26. Would you consider adopting robots.txt in the future?
         • Not likely at all • Unlikely • Neutral / Undecided
                                                                                       been making money from their art. The majority of respondents
         • Likely • Very likely                                                        (68) have been doing so for 1–5 years, whereas only 17 have been
     Why or why not? (Open-ended)                                                      making money from their art for less than a year. Over half of the
    Q27. Robots.txt is a standardized way to declare “do not crawl,” and               respondents (91) have been making money from their art for at
most companies respect it. How likely do you think AI companies                        least 5 years.
will respect robots.txt?
         • Not likely at all • Unlikely • Neutral / Undecided
                                                                                                                Continent             Count
         • Likely • Very likely
     Why or why not? Answer:                                                                                    North America              109
    Q28. Have you checked the robots.txt of websites where you post                                             Europe                      52
your work?                                                                                                      Asia                        21
         • Yes • No                                                                                             South America               18
    Q29. Can you control (edit or modify) the content of the robots.txt
                                                                                                                Africa                       2
of websites where you post your work?
                                                                                                                Oceania                      1
         • I have full control over the full content of robots.txt
         • I can click some buttons to switch between a few presets                                             Total                      203
         • I have no control over the content
         • I am not sure
                                                                                                Table 6: Continent of residence of participants.
         • Other (please specify)
    Q30. How did you get the current content of robots.txt?                                Table 6 presents a breakdown of the continent of residence of par-
         • Provided by my website hosting platform                                     ticipants. The majority of participants (109) are from North America,
         • Copied from the Internet (e.g., a blog)                                     with 89 of them from the United States. The second largest group
         • Created my own robots.txt                                                   is from Europe (52), with 18 from the United Kingdom, five from
         • Other (please specify)                                                      Poland, and another five from Germany. The third largest group is
    Q31. Do you currently use robots.txt to disallow bots from AI
                                                                                       from Asia (21), with nine from The Philippines. The remaining par-
companies from scraping websites where you post your art?
         • Yes • No                                                                    ticipants are from South America (18), Africa (2), and Oceania (1).
     Why? Answer:                                                                          Table 7 presents a breakdown of the top five types of art partici-
     Why not?                                                                          pants do. Each participant can select every type of art they do, so
         • I am concerned it will impact the discoverability of my website             the total number of responses is greater than the number of partici-
online                                                                                 pants. The most common type of art is illustration (163), followed
         • I don’t mind AI training on my art                                          by digital 2D (143), character and creature design (99), traditional
         • I don’t know how to do it                                                   painting and drawing (78), and concept art (68).
         • Other (please specify)                                                          Table 8 presents our participant’s average familiarity with var-
     Q32. [Optional] Do you face any obstacles in adopting robots.txt?                 ious terms. This question is designed to assess our participants’s
(Select all that apply)
                                                                                       digital literacy. The average is on a scale from 1 to 5, where 1
         • I have trouble finding how to edit the robots.txt
                                                                                       represents no understanding and 5 represents full understanding.
IMC ’25, October 28–31, 2025, Madison, WI, USA.                            Enze Liu et al.


             Art Type                               Count
             Illustration                               163
             Digital 2D                                 143
             Character and Creature Design               99
             Traditional Painting and Drawing            78
             Concept Art                                 68
             Total                                     551
         Table 7: Top five types of art participants do.

            Term                        Average Familiarity
            Website                                     4.60
            Search Engine                               4.35
            Generative AI                               3.89
            Robots.txt                                  1.99
            Nearest diffusion tree                      1.56

Table 8: Participant’s average familiarity with various terms.
The average is on a scale from 1 to 5, where 1 represents no
understanding and 5 represents full understanding. Follow-
ing the work of Hargittai [41], we also include a bogus item
“Nearest diffusion tree”, indicated in italics.


Following the work of Hargittai [41], we also include a bogus item
“Nearest diffusion tree”, indicated in italics. The most familiar term
is “website” (4.60), followed by “search engine” (4.35), “generative
AI” (3.89), and “robots.txt” (1.99). The least familiar term is “nearest
diffusion tree” (1.56). Given that this bogus term was rated as the
lowest compared to the other four terms, we conclude that our
participants do not select randomly. This data also suggests that
our participants are relatively familiar with general terms such
as “website”, “search engine”, and “generative AI”, but much less
familiar with “robots.txt”. This result is consistent with our other
findings in Section 4.
Somesite I Used To Crawl: Awareness, Agency and Efficacy in Protecting Content Creators From AI Crawlers          IMC ’25, October 28–31, 2025, Madison, WI, USA.


D.3     Codebook
This section details the codebook we used to analyze the qualitative data collected from artists. Specifically, Table 9 lists other actions taken
by artists in response to AI-generated art; Table 10 lists reasons why artists would not adopt robots.txt; Table 11 lists reasons why artists
would enable a mechanism that blocks AI crawlers; and Table 12 lists reasons why artists do not trust AI companies to respect robots.txt.

     Theme                       Description                                      Example
     Modify post                 Artists alter the content or format of           “Overlaying watermarks or art filters to modify the artwork”
                                 the artwork they share online.
     Switch platforms            Artists migrate to alternative sites or          “Use Cara instead of Instagram”
                                 remove their work from certain plat-
                                 forms.
     Raise awareness             Artists publicly highlight issues affect-        “Spreading awareness about the damage AI-generated art does”
                                 ing them or the community.
     Unionize                    Artists organize collectively to negoti-         “Connecting with groups of professional artists being impacted to
                                 ate or advocate for shared interests.            search for collective solutions for our field”
     Change career path          Artists pivot to a different professional        “I left school and am taking a gap year to reevaluate my life”
                                 direction.
     Miscellaneous               Additional strategies not covered                “Using block lists to block AI art accounts”
                                 above.
                           Table 9: Codebook for other actions taken by artists in response to AI-generated art.



     Theme                       Description                                      Example
     Efficacy                    Artists are concerned about the effi-            “if the companies can ignore it why would they respect it consider-
                                 cacy of robots.txt given its voluntary           ing what they already do”
                                 nature.
     Usability                   Artists are concerned about the com-             “It sounds like something difficult to use”
                                 plexity of implementing or using
                                 robots.txt.
     More information            Artists want to gather more informa-             “Not informed enough about it”
                                 tion about robots.txt before making a
                                 decision.
     No personal website         Artists do not have a personal website.          “I do not have a personal website”
     Search results              Artists are concerned about robots.txt           “If it hides things from *search engines* then how will people find
                                 impacting the search results of their            my work?...”
                                 websites.
                                         Table 10: Codebook for why artists would not adopt robots.txt.
IMC ’25, October 28–31, 2025, Madison, WI, USA.                                                                                         Enze Liu et al.


     Theme                       Description                               Example
     Protection                  Artists want to protect their work.       “To protect my original concepts and visual brand (aka original
                                                                           character designs and artstyle)”
     Consent                     Artists do not want their work to be      “I havent given AI companies permission to use my work”
                                 crawled and do not consent to crawl-
                                 ing.
     Compensation                Artists are not compensated while AI “..., and I do not want other companies to profit off of it without my
                                 companies profit from their work.     knowledge, permission, or without fair compensation towards the
                                                                       source.”
     Useful mechanism            Artists see this mechanism as useful “Adds a sense of security and ease of use.”
                                 and reassuring.
     Legal benefit               Artists believe such mechanisms could “..., it is a measure to reinforce a statement that we do not condone
                                 be potentially useful in legal cases. with these practices and will probably benefit in a possible lawsuit
                                                                       in the future.”
     Misc                        Additional reasons not covered above. “At this point if the option is presented I’ll do my research on it and
                                                                       if it seems legitimate I’ll do it on principle.”
                         Table 11: Codebook for why artists would enable a mechanism that blocks AI crawlers.

     Theme                       Description                               Example
     Track record                AI companies have a history of con-       “Based on the attitudes I have seen from AI companies and the way
                                 ducting operations that maybe unau-       AI companies have already used data without consent, I’m unsure
                                 thorized and unethical.                   if they will respect robot.txt”
     Profit                      AI companies have monetary interests      “Money before morals.”
                                 in scraping artists’ work.
     Perception                  Artists perceive AI companies nega-       “AI companies are morally bankrupt.”
                                 tively (e.g., as greedy or unethical).
     Loophole                    AI companies might find loopholes or      “They might start loopholes to get around it or something ”
                                 workarounds to bypass robots.txt.
     Legal enforcement           The need and lack of legislation or le-   “Generative AI is built on top of copyright infringement-they can’t
                                 gal enforcement.                          be profitable without it, so they will argue against any thing that
                                                                           prevents them from scrapping. They have to be forced to respect it
                                                                           by law, we can’t trust their good faith.”
     Voluntary nature            Robots.txt is a voluntary mechanism.      “At best it seems that robot.txt is just a warning sign, and will not
                                                                           entirely stop AI companies from deciding to scrape any particular
                                                                           content.”
     Misc                        Additional reasons not covered above.     “I think, unfortunately, a lot of companies will not respect and will
                                                                           do it anyway.”
                            Table 12: Codebook for why artists do not trust AI companies to respect robots.txt.
