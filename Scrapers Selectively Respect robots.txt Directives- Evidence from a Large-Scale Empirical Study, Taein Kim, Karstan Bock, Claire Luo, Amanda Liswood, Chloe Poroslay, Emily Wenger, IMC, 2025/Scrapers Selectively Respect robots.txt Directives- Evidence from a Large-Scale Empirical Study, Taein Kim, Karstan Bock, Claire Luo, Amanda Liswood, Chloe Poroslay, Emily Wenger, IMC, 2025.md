                                                            Scrapers Selectively Respect robots.txt Directives:
                                                               Evidence From a Large-Scale Empirical Study
                                                               Taein Kim                                              Karstan Bock                                    Claire Luo
                                                   Department of Electrical and                              Department of Electrical and                   Department of Electrical and
                                                     Computer Engineering                                      Computer Engineering                           Computer Engineering
                                                        Duke University                                           Duke University                                Duke University
                                                       Durham, NC, USA                                           Durham, NC, USA                                Durham, NC, USA

                                                         Amanda Liswood                                             Chloe Poroslay                                 Emily Wenger∗
                                                   Department of Electrical and                          Office of Information Technology                   Department of Electrical and
arXiv:2505.21733v2 [cs.NI] 23 Oct 2025




                                                     Computer Engineering                                         Duke University                             Computer Engineering
                                                        Duke University                                          Durham, NC, USA                                 Duke University
                                                       Durham, NC, USA                                                                                          Durham, NC, USA
                                         Abstract                                                                                1    Introduction
                                         Online data scraping has taken on new dimensions in recent years,                       Web scraping, the process of systematically extracting and down-
                                         as traditional scrapers have been joined by new AI-specific bots.                       loading information from websites, has been a part of the internet
                                         To counteract unwanted scraping, many sites use tools like the                          ecosystem since its early days [24]. Scraping is now a critical part
                                         Robots Exclusion Protocol (REP), which places a robots.txt file                         of many companies’ business models, allowing search engines to
                                         at the site root to dictate scraper behavior. Yet, the efficacy of the                  optimize results and shopping sites to compare deals, among other
                                         REP is not well-understood. Anecdotal evidence suggests some bots                       purposes. In recent years, scraping has gained new importance as
                                         comply poorly with it, but no rigorous study exists to support (or                      vast troves of internet data are tapped for a novel purpose: train-
                                         refute) this claim. To understand the merits and limits of the REP,                     ing and operating large-scale AI models. Today’s large-scale AI
                                         we conduct the first large-scale study of web scraper compliance                        models require terabytes of training data [30, 33], for which the
                                         with robots.txt directives using anonymized web logs from our                           internet is an obvious and cheap source. Whitepapers documenting
                                         institution. We analyze the behavior of 130 self-declared bots (and                     many of today’s biggest models, from GPT to Llama and beyond,
                                         many anonymous ones) over 40 days, using a series of controlled                         openly acknowledge the use of web scraping to create training
                                         robots.txt experiments. We find that bots are less likely to comply                     data [5, 11, 14, 19, 44, 45].
                                         with stricter robots.txt directives, and that certain categories of                        The AI demand for web scraping extends beyond training data.
                                         bots, including AI search crawlers, rarely check robots.txt at                          AI models for text generation have a pesky tendency to halluci-
                                         all. Our findings suggest that relying on robots.txt to prevent                         nate, confidently stating incorrect information [29, 41]. To make
                                         unwanted scraping is risky and highlight the need for alternatives.                     AI-generated text more reliable, AI developers proposed Retrieval-
                                                                                                                                 Augmented Generation (RAG), in which large vectorized databases
                                         CCS Concepts                                                                            of web content are used to ground AI responses [26, 28, 34]. These
                                         • Information systems → Web log analysis; • Security and                                databases are collated via large-scale web scraping and, unlike train-
                                         privacy → Access control.                                                               ing datasets, are continuously updated. Additionally, AI “agents,”
                                                                                                                                 generative models with additional capabilities, can deploy bots to
                                         Keywords                                                                                fetch web content as part of their workflow [6, 8, 22].
                                                                                                                                    Beyond well-documented copyright and privacy concerns, wide-
                                         web scraping; content controls; bots
                                                                                                                                 spread scraping for any purpose—including for AI training data,
                                         ACM Reference Format:                                                                   RAG, and agent use—can destabilize public, data-rich websites.
                                         Taein Kim, Karstan Bock, Claire Luo, Amanda Liswood, Chloe Poroslay,                    Numerous writings from the “grey” (non-academic) literature de-
                                         and Emily Wenger. 2025. Scrapers Selectively Respect robots.txt Direc-                  scribe sites being taken offline in recent months due to thousands
                                         tives: Evidence From a Large-Scale Empirical Study. In Proceedings of the
                                                                                                                                 of download requests from scrapers associated with AI compa-
                                         2025 ACM Internet Measurement Conference (IMC ’25), October 28–31, 2025,
                                         Madison, WI, USA. ACM, New York, NY, USA, 17 pages. https://doi.org/10.
                                                                                                                                 nies [15, 27, 38]. These scraping-induced problems have prompted
                                         1145/3730567.3764471                                                                    an escalating tactical war, as content-rich websites attempt to mod-
                                                                                                                                 erate or prevent unwanted web scraping [10, 36, 37].
                                         ∗ Corresponding author: emily.wenger@duke.edu
                                                                                                                                    Among the most widely used anti-scraping solution is the Robots
                                                                                                                                 Exclusion Protocol (REP), implemented via a robots.txt file lo-
                                                                                                                                 cated at the site root. The REP lets site owners set rules that specify
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   which bots can scrape information from the site, which sub-domains
                                         IMC ’25, Madison, WI, USA                                                               those bots can access, and how long bots must wait between suc-
                                         © 2025 Copyright held by the owner/author(s).                                           cessive page accesses [2]. Recent work [37] showed a significant
                                         ACM ISBN 979-8-4007-1860-1/2025/10
                                         https://doi.org/10.1145/3730567.3764471                                                 uptick in the use of and restrictions in robots.txt files after the
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                    Taein Kim et al.


rise of generative AI models around 2022, purportedly in reaction         2     Context: Web Scraping and Bot Deterrence
to increased scraping for training data. The REP was codified in          Prior work has studied web scraping in general, as well as the
2022, but it is not legally binding, so compliance requires scraper       prevalence and properties of robots.txt files. In this section, we
goodwill.                                                                 position our work in the broader landscape of research on data
   Although robots.txt is widely used, little hard evidence exists        scraping and scraper deterrence.
to prove its efficacy in preventing scraping. Some gray literature
suggests that many crawlers, including AI-specific bots, do not
respect robots.txt [15]. Other articles claim that certain crawlers       2.1    Web scraping: a history
ignore robots.txt files altogether [10, 38], while still others ob-
serve that bots disallowed by robots.txt sometimes pretend to be          Early days. Web scrapers and crawlers are nearly as old as the in-
other, sanctioned bots to circumvent restrictions [27]. Despite this,     ternet. In this work, crawling refers to the process of systematically
a recent work [35] conducted a study of 7 crawlers and observed           accessing links on the web, while scraping is the act of downloading
that all AI bots that promised to respect robots.txt did so.              information from each link. The first known web crawler was the
   Given the dearth of options for deterring unwanted web scraping        World Wide Web Wanderer, created in 1993 by an MIT undergrad-
and widespread belief that robots.txt can help, there is urgent           uate student to measure web growth [24]. Shortly after this, the
need for a large-scale, controlled experiment evaluating this belief.     first crawler-based search engine, JumpStation, premiered, paving
Such a study will allow content hosts to make informed decisions          the way for future crawler-fueled search engines like Google [39].
about whether robots.txt will provide their desired level of pro-         The creation of tools such as APIs has allowed for simultaneous
tection or if alternative deterrence mechanisms are needed.               scraping and crawling, since APIs enable easy data downloads [20].
                                                                          Web crawling and scraping now power a number of useful appli-
Our contribution. We conduct the first controlled study of scraper
                                                                          cations, such as search engines, price comparison, and real-time
compliance with robots.txt at scale. To do this, we collect anonymized
                                                                          system monitoring.
web traffic data from a set of 36 websites we control over 40 days.
During this period, we conduct two empirical measurement studies          Web scraping in the AI era. Interest in data scraping has only
on sites’ robots.txt files to determine if or to what extent web          increased as AI models have grown in size and scope. The operating
bots, AI and otherwise, comply with robots.txt directives.                principle for many AI model trainers is that more training data
   The first study, conducted on a single site in our dataset with        produces better models [30], and the internet is a free and expansive
significant web traffic, deployed three versions of a robots.txt file     source of data. To collect data at scale, model trainers can either
with increasingly strict bot directives, each for two weeks. By ana-      scrape the data themselves or rely on pre-collected datasets like
lyzing how bot behavior changes in response to different robots.txt di-   Common Crawl [3]. Additionally, there are some datasets, like
rectives, we can determine which directives, if any, effectively de-      LAION 5B, which only provide URLs, requiring prospective users
ter bot behavior and which bots are more or less respectful of            to scrape the data from the links [42]. Since this practice has become
robots.txt . The second study, conducted via passive observation          so common, large AI companies have developed new user agents
of bot behavior on sites with fixed robots.txt files, broadens the        to identify bots scraping data on their behalf [4].
perspective on the analysis, determining the frequency with which            In recent years, other types of AI-related scraping have emerged:
robots.txt files are accessed. Along the way, we make observa-            retrieval-augmented generation (RAG) and AI web accesses. RAG [26,
tions about bot and scraper behavior in general that we believe the       28, 34] allows large language models (LLMs) to supplement their
community will find interesting. Our key findings are as follows:         outputs with current online information, since their training datasets
                                                                          struggle to produce factual information on recent events and can
                                                                          “hallucinate” information in their responses [29]. RAG relies on a
• Bots are less likely to respect robots.txt that employ strict           database of continuously updated web links that models can quickly
  directives, such as denying access to certain pages. Across our         search. Recent innovations enable generative AI “agents” to access
  three versions of robots.txt , we see compliance decrease as            websites while completing a user-requested task [6, 8, 22]. Such
  directives become stricter.                                             web accesses—which range from information lookup to inputting
• SEO bots are most respectful of robots.txt , while search               or downloading data—typically involve deputizing a scraper bot to
  engine crawlers are among the least. AI-specific bots like AI           perform the task.
  assistants and AI data scrapers, fall in between.
• Observed non-compliance with robots.txt among other-
  wise respectful bots can sometimes be attributed to spoof-              2.2    Bot deterrence
  ing, in which malicious bots present a false user agent to avoid        Although certain types of web scraping can benefit site owners
  detection.                                                              (e.g. search engine optimization), other types can be harmful. For
                                                                          example, unfettered scraping can scoop up data that, while publicly
   The rest of the paper is organized as follows. §2 situates our         available, may have copyright or privacy concerns [37]. Further-
work in the broader landscape of data scraping. §3 describes our          more, numerous blog posts and other articles from recent years
data collection process and gives a dataset overview. §4 outlines         have documented how high-intensity scraping by presumed AI
our robots.txt experiments and results. §5 discusses possible             crawlers have caused site instability [10, 27, 38]. In light of these
confounding variables in our experiments. §6 lists limitations and        downsides, many techniques have been proposed to prevent un-
future work.                                                              wanted scraping.
                                                                                                                                IMC ’25, October 28–31, 2025, Madison, WI, USA



                           robots.txt field                                                  Description
                              user-agent                  Refers to a bot with self-declared user agent string (e.g. Googlebot).
                                  allow                   Subset of site pages that bot with specific user-agent can access.
                                disallow                   Subset of site pages bot with specific user-agent cannot access.
                             crawl-delay             Minimum required time between successive page accesses by specific bot.
                                 sitemap                              Provides an overview of subdomains on the site.
               Table 1. Common fields in robots.txt files. robots.txt files constructed using these fields specify how bots can interact with a site, see Figure 1.




User-agent: Googlebot                                                                        while recent advances in AI (and human skill) make CAPTCHA
Allow: /                                                                                     solving easy [7, 12, 25, 49], both of which make CAPTCHAs less
Crawl-delay: 15                                                                              useful. Companies like Cloudflare market proprietary bot detection
                                                                                             and deterrence methods, which can be purchased [16]. As a last
User-agent: *                                                                                resort, companies can outright block the IP addresses of troublesome
Allow: /allowed-data/                                                                        bots. However, since many bots run on VPNs, IP addresses can
Disallow: /restricted-data/                                                                  be easily recycled, circumventing this approach. Several academic
Crawl-delay: 30                                                                              works suggest using reverse proxies to better regulate traffic to a
                                                                                             site [17, 35]. Finally, other articles suggest novel methods like em-
Sitemap: https://X.X.X/sitemap/sitemap-0.xml                                                 ploying a proof of work [27] or even a tarpit [10], which creates
                                                                                             unending fake content for scrapers.
Figure 1. Example robots.txt file. This site allows bots with user-agent Googlebot
to access all subdomains with a crawl-delay of 15 seconds. All other bots are given
a crawl-delay of 30 seconds and can only access data under the /allowed-data/
subdomain.



The Robots Exclusion Protocol emerged in 1994 as a possible                                  2.3      Prior work on scraping and robots.txt
solution to unwanted bot activity. As crawlers became prominent on                           Numerous studies have considered behaviors of web scrapers [32,
the early web, it became clear that a mechanism was needed to allow                          40], but limited work has studied the relationship between scrap-
“friendly” scrapers and disallow poorly-behaved ones [31]. The                               ers and robots.txt . Longpre et al. [37] performed a longitudi-
Robots Exclusion Protocol (REP) [2] was proposed to fill this gap.                           nal analysis of robots.txt files on websites often scraped for AI
The REP asks developers to place a file called robots.txt at their                           data and found that robots.txt restrictions tightened after the
site root, specifying restrictions on certain bots and bot behaviors                         rise of generative AI models like ChatGPT. Restrictions in these
on their site. Possible bot directives include restricting subdomain                         robots.txt files vary among AI bots, with large, well-known com-
access, enforcing a crawl delay, and allowing only bots with certain                         panies like OpenAI having the most restrictions. Longpre et al.
user-agent strings—see Table 1 and Figure 1. The REP was codified                            argue that tight controls in robots.txt may degrade the quality
as RFC 9309 by the Internet Engineering Task Force (IETF) [21] and                           of open-source AI training datasets. Concurrent work from [18]
is widely used [37, 43].                                                                     similarly observed tightening in robots.txt restrictions since the
    Despite its prominence, the REP has significant drawbacks. First,                        advent of generative AI tools.
robots.txt is not a legally binding document, so requires the good-                          Do AI bots respect robots.txt ? Limited work has focused on
will of the parties involved for compliance [1]. Second, it requires                         whether AI scrapers specifically respect robots.txt . One small-
web hosts to maintain extensive knowledge of user agents and                                 scale study explored whether a robots.txt file was respected by
entities that they wish to exclude from scraping [37]. This places a                         AI bots and found that, of the 7 AI bots that visited their site, 6
heavy burden on hosts to maintain awareness of the ever-changing                             promised to respect robots.txt and did so [35]. One (Bytespider
web landscape. Third, since compliance is optional, some crawlers                            from Bytedance) did not promise to respect robots.txt and did not.
simply ignore robots.txt . Finally, limited work [35] has studied                            While interesting, the scale of this study prevents it from providing
bot compliance with robots.txt , and none have done so at scale,                             a holistic picture of how bots in general interact with robots.txt .
making its efficacy unknown.                                                                    Evidence from grey literature further suggests that noncom-
Other bot-blocking methods. Other methods to block unwanted                                  pliance with robots.txt is widespread [38]. Again, however, no
scraping behavior vary from mildly intrusive to very disruptive.                             large-scale empirical study has considered this question. We hy-
CAPTCHAs, which ask site visitors to solve a hard (e.g. computation-                         pothesize this literature gap is primarily due to data access limi-
ally difficult) problem before viewing or retrieving page content,                           tations, since to make statistically meaningful statements about
have historically been effective in deterring bots [47, 48]. However,                        robots.txt (non)compliance, one must have access to millions of
they add significant friction to user interactions with webpages [13],                       web logs.
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                                                     Taein Kim et al.


                              Unique               Unique                Avg. bytes                 Unique          Total bytes           Total            Unique
        Data subset
                            IP addresses         user agents         scraped per session             ASNs            scraped            page visits       page visits
        All data                231,859              19,250                   82,306                  8,841       62,713,813,720           761,956             31,665
       Known bots               11,291                405                     52,612                   179        16,706,054,178           317,532             6,347
          Table 2. Overview of our dataset. The top row corresponds to the entire dataset, while the bottom row documents activity associated with well-recognized bots.



3  Our dataset for analyzing                                                                                                     Total        % of all      GB of data
                                                                                                    Bot name
   robots.txt compliance at scale                                                                                                hits         traffic       scraped
3.1 Dataset Preparation                                                                             YisouSpider                  121495       15.95         8.23
To study scraper compliance with robots.txt files at scale, we                                      Applebot                     118258       15.52         0.21
collect and analyze a large dataset composed of network access                                      Baiduspider                  15132        1.99          0.05
data from website endpoints managed by our institution, a large                                     bingbot                      12900        1.69          0.80
private US university. The sites host information about a variety of                                meta-externalagent           12837        1.68          0.87
university functions, from the IT department to campus dining to                                    Googlebot                    9103         1.19          0.85
a personnel directory and beyond. The dataset contains approxi-                                     HeadlessChrome               8365         1.1           1.22
mately 3.9 million external web requests made to a set of 36 websites                               ChatGPT-User                 3029         0.4           0.98
from February 12 - March 29, 2025 and includes the following fields:                                yandex.com/bots              2179         0.29          0.28
                                                                                                    SemrushBot                   2111         0.28          0.06
• Useragent: A self-reported string identifying the entity access-                                  GPTBot                       1225         0.16          0.25
  ing a website that often includes the browser, operating system,                                  dotbot                       1066         0.14          0.01
  hardware, and version information of the origin of the request.                                   Amazonbot                    1009         0.13          0.07
  Well-known bots often provide a simpler identifying string in                                     AhrefsBot                    862          0.11          0.02
  this field (e.g. Googlebot).                                                                      SkypeUriPreview              831          0.11          0.09
• Timestamp: The ISO-8601 formatted time of the request.                                            facebookexternalhit          785          0.1           0.05
• IP Hash: A one-way cryptographic hash of the web visitor’s IP                                     BrightEdge Crawler           736          0.1           0.06
  address. This anonymizes IPs for IRB compliance.                                                  Scrapy                       726          0.1           0.19
• Autonomous System Number (ASN): A number assigned by                                              ClaudeBot                    684          0.09          0.09
  the American Registry of Internet Numbers (ARIN) to the entity                                    Bytespider                   561          0.07          0.08
  controlling web visitor’s IP.                                                              Table 3. Over 40% of web accesses in our dataset are attributable to just 20 bots.
• Sitename: The base website accessed.                                                       We document the number of unique web accesses for each bot, the proportion of web
                                                                                             traffic they compose, and the amount of data each scraped during the 40 day period.
• URI path: The requested resource. The sitename and URI path
  combined form the whole URL.
• Status code: Code site returned in response to request.                                    including the declared entity name and description. We also stan-
• Bytes: Amount of data, in bytes, transmitted by the web server                             dardize bot names via fuzzy string matching with a public dataset
  during site interaction (e.g. amount of downloaded content).                               of common useragent strings and the corresponding bot names2 .
• Referer: Site from which web visitor was redirected (if applica-                           Using these standardized names, we add an additional column to
  ble.)                                                                                      our dataset that maps bots to bot categories proposed by Dark Vis-
                                                                                             itors, an industry website that keeps an up-to-date list of known
Each row of the dataset corresponds to one page access by a web                              scrapers3 —AI Agents (bots from AI companies with “agent” in their
visitor at a given time.                                                                     name, presumed to operate as part of an agent pipeline), AI As-
Data preprocessing. Data from any institution-hosted networks                                sistants (bots that retrieve content to supplement AI queries), AI
or logged-in institutional users is filtered out before it reaches our                       Data Scrapers (bots that scrape AI training data), Archivers, De-
servers to protect user privacy. We inspect data after collection and                        veloper Helpers, Fetchers, Headless Agents, Intelligence Gatherers
remove several IP hashes associated with vulnerability scanning                              (data collection for non-SEO or AI purposes), Scrapers, Search En-
tools and similar entities that are not relevant to our analysis. We                         gine Crawlers, SEO Crawlers, Uncategorized, and Undocumented
screen out 3 IP hashes associated with 294, 362 web accesses through                         AI Agents. This categorization allows us to analyze collective bot
this approach. Then, we map ASNs to ARIN info and standardize bot                            behaviors.
names to enhance the data and simplify analysis.                                             Ethical considerations. Data collection and analysis adhered to a
   To map ASNs to ARIN info, we leverage the external library                                study protocol approved by our local Institutional Review Board
whoisit1 to poll for whois information for all unique ASNs in our                            (IRB)4 . We followed all IRB guidelines for anonymizing and storing
incoming dataset. The returned whois information contains infor-                             this dataset, including making significant efforts to exclude non-bot
mation held by ARIN about the registered user behind the ASN,
                                                                                             2 https://github.com/monperrus/crawler-user-agents
                                                                                             3 https://darkvisitors.com/
1 https://pypi.org/project/python-whois/                                                     4 IRB information redacted for anonymous submission
                                                                                                                                                       IMC ’25, October 28–31, 2025, Madison, WI, USA


                                                                                                         1.0
                    105                                                                                                Search Engine Crawlers
                                                                                                         0.8           AI Data Scrapers




                                                                                          CDF of bytes
     (log) number




                                                                                          downloaded
                    104                                                                                                Headless Browsers
      of sessions


                                                                                                         0.6           AI Assistants
                    103                                                                                                AI Search Crawlers
                                                                                                         0.4
                    102                                                                                  0.2
                    101                                                                                  0.0
                          s s s s s s s s s s
                       ler ler per ser ler ant her rer ver per                                                             -15            -22            -01             -08            -15         3-2
                                                                                                                                                                                                       2
                  C raw Craw Scra Brow Craw ssist Fetc athe Archi r Hel                                              5 -02          5 -02          5 -03           5 -03          5 -03          5-0
               ine ch ta ss EO AI A                         eG           pe                                       202            202            202             202            202            202
           E ng I Sear AI Da eadle S                 ig enc      e v elo
                                                                                                                                                               Date
         ch A               H                    ell           D
     Sear                                    Int
  Figure 2. Traditional and AI search, as well as AI data scrapers, are the                Figure 3. Most bots in the top 5 categories in terms of data scraped collect data steadily,
  most active bot types in our dataset. Headless browsers—a browser running                but search engine crawlers buck the trend, driven by YisouSpider’s mid-March activity.
  sans GUI, commonly used by scrapers—are fourth.                                          AI assistants scrape much data relative to session count (Fig 2).


            20000           Search Engine Crawlers
# of scraper




                            AI Search Crawlers
  sessions




            15000           AI Data Scrapers
            10000           Headless Browsers
                            SEO Crawlers
             5000
                0
                             2025-02-15               2025-02-22              2025-03-01                       2025-03-08               2025-03-15                     2025-03-22
                                                                                                          Date
  Figure 4. Traditional and AI search crawlers exhibit the most volatility in scraping patterns during the date range encompassed by our dataset. The volatility in these
  two categories corresponds directly with high scraping activity of YisouSpider (a search engine crawler) and AppleBot (an AI search crawler). We plot the behaviors of the top 5 categories of
  bots by session count for simplicity.


  behavior from the dataset and preserve user privacy. We removed                                         match either a user agent string format from our Github dataset
  sessions originating from logged-in users from our institution or                                       using regular expression pattern matching, or one recorded by Dark
  from institution-hosted networks, and anonymized IP addresses by                                        Visitors. The low number of known bots relative to the total unique
  hashing them. All data was stored and analyzed on secure servers                                        user agents in our dataset presages the difficulty of determining bot
  only accessible by the research team.                                                                   compliance with robots.txt , since many operate anonymously
                                                                                                          or with generic user agents.
  3.2          Dataset overview                                                                           Most active bots. Now, we focus specifically on known bots, e.g.
 First, we present an overview of our dataset, examining both basic                                       bots with self-declared user agents that are well-documented by
 dataset statistics and bot behaviors of interest. Such an overview,                                      several web sources. Table 3 gives details about the behavior of
 independent of our work on robots.txt compliance, is valuable.                                           the 20 most active bots (as measured by number of web accesses)
 Little academic work has documented the contours of web scraper                                          seen in our dataset. Together, these 20 bots make up over 40%
 behavior in the AI age—and none have done so at scale. For our                                           of the observed web traffic. YisouSpider and AppleBot dominate,
 analysis, we aggregate dataset rows, each of which describes a                                           collectively driving 30% of all traffic and scraping over 8 GB of data
 single page access, into time-based “sessions” associated with the                                       during the 40 day period. YisouSpider is associated with the Chinese
 same web agent. To do this, we identify accesses by a particular en-                                     search engine Yisou and appears to be used to index web pages [46],
 tity/user agent to a set of related pages at contiguous time steps and                                   specifically focusing on educational and job related webpages [4].
 collapse them into one row, retaining information about individual                                       We found that the vast majority of the YisouSpider’s accesses were
 subdomains visited in a session. We say a session “ends" after 5                                         to our institution’s people directory. AppleBot is a generic bot
 minutes of inactivity from an entity. This reduces our dataset from                                      associated with Apple and is “used by Apple to index search results
 3,914,096 rows to 761,956 rows.                                                                          that allow the Siri AI Assistant to answer user questions” [9].
                                                                                                             We also investigate which categories of bots most frequently visit
 High-level statistics. Table 2 gives an overview of our dataset,
                                                                                                          our sites, using the categories defined by Dark Visitors (see §3.1).
 distinguishing between two subsets of data: data associated with
                                                                                                          Figure 2 plots the relative frequency of different types of known
 any user agent (including generic ones), and data associated with
                                                                                                          bots in our dataset, separated into the categories defined by Dark
 known user agents with defined bot purposes. As the table shows,
                                                                                                          Visitors. Search-related bots, either for traditional or AI-powered
 our dataset contains thousands of unique IP addresses and user
                                                                                                          search, are the most frequent visitors, followed by AI data scrapers.
 agents, but only a handful are associated with known user agents.
                                                                                                          Headless browsers, a category assigned to entities observed running
 We define “known bots” as those with self-declared user agents that
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                                Taein Kim et al.


a browser without a GUI, come in forth. This category is mostly           • Version 1 (Fig. 6): All bots retain the same level of access as
composed of likely scraper bots that do not identify themselves              in the base version, but a 30 second crawl delay is requested
with a known user agent string. Bots used for other applications,            between successive page requests.
like SEO and archivers, are less common.                                  • Version 2 (Fig. 7): Most bots are allowed to access only the
Cumulative bot behaviors. Finally, we explore how bots behave               /page-data/* endpoint, which we observed experimentally to
over time. Figure 3 plots the CDF of data collected by the top 5             be a common target for scrapers, but are disallowed from all
categories of bots in terms of bytes scraped. From this, we see              other sites. Eight search engine optimization (SEO) bots5 are
that most bots collect data at a steady rate, with search engine             exempt from these restrictions per our institution’s request, to
crawlers as a notable exception. These have a significant spike              ensure the sites remain easily findable online.
in data collection towards the end of our data collection period.         • Version 3 (Fig. 8): Most bots are denied access to all page content.
Furthermore, we observe that AI assistants, though ranked sixth in           The same eight SEO bots as before are exempt.
of number of total scraping sessions (Figure 2) are ranked fourth         We validated that each robots.txt file was formatted correctly via
in terms of data scraped (Figure 3), indicating that they collect a       the Google robots.txt parser6 . Data collection associated with
relatively large amount of data per session.                              each of these files was conducted mostly in parallel with the data
   Figure 4 shows the number of sessions per day for the five cate-       collection process described in the previous section. The one ex-
gories of bots with the most total sessions. As with the data CDF         ception was the baseline robots.txt data, which was collected
plot, most categories of bots exhibit relatively stable behavior over     in January 2025 before the full dataset collection started. Table 4
time, with the exception of search engine crawlers and AI search          summarizes data collected under each robots.txt version. Similar
crawlers. Upon further inspection, we find these spikes in activity       numbers of site visits and unique bots are observed across all four
correspond directly with high scraping activity from YisouSpider          robots.txt deployments.
(a search engine crawler) and AppleBot (an AI search crawler).
                                                                                         robots.txt         unique site        unique bot
4     Measuring scraper compliance with                                                    version            visits            visitors
      robots.txt                                                                         Base (Fig. 5)            113, 601           78
Now, we turn our attention to our central question: understanding                        v1 (Fig. 6)              111, 206           87
the extent to which scraper bots comply with robots.txt directives.                      v2 (Fig. 7)              119, 399           77
We first describe our methodology, then analyze the results of our                       v3 (Fig. 8)              113, 060           75
experiments.                                                              Table 4. Summary statistics of web traffic captured under all four
                                                                          robots.txt versions. Site traffic and number of unique bot visitors (bots with known
                                                                          user agents) remains consistent across all robots.txt deployments.
4.1     Methodology
Over a period of 8 weeks, we deployed four versions of robots.txt files   Data preparation. We performed basic preprocessing on our
on one of the 36 institution-controlled sites we were monitoring.         datasets after collection to aid analysis. Much of our preprocessing
Data from this site was also part of the dataset in §3. This site         pipeline for the robots.txt experiments mirrored that described
was chosen because of its observed high bot traffic, making it a          in §3. However, for our analysis of compliance with robots.txt we
rich source of data on scraper behavior. Each robots.txt file was         also filter out bots that accessed the site less than 5 times under
deployed for two weeks, then swapped out by support staff for             any robots.txt version. Finally, we also eliminated any bots that
the next version. The four versions of the robots.txt files have          appeared to have spoofed their user-agent. We determine potential
increasingly strict directives, ranging from no meaningful restric-       spoofing by looking at bots for which > 90% of traffic originates
tions to full denial of access for certain bots. The restrictions were    from a single ASN, and flag as possibly spoofed instances any re-
chosen to represent a steady gradient of robots.txt behaviors,            quests originating from another ASN (e.g. not the 90% majority
ranging from permissive to strict while only changing one con-            ASN). A deeper exploration of this spoofing metric can be found in
dition at a time, allowing us to assess how bot behaviors change          §5.
in response to incremental robots.txt updates. We believe such
controlled experimentation is the best approach, ensuring that con-
                                                                          4.2     Metrics for robots.txt compliance
founding variables are not introduced by the modification of too          For each version of robots.txt with some restrictions (v1, v2,
many robots.txt properties at once. Using these related but dis-          v3), we develop novel metrics to determine if a bot complies with
tinct versions of robots.txt allowed us to achieve two distinct           the directive(s), then use traditional statistical methods to measure
goals: measuring whether certain robots.txt directives were more          whether such compliance is statistically significant relative to the
or less respected by scrapers, and measuring how quickly scrapers         bot’s default behaviors. Here, we describe our compliance metrics.
adapted to new robots.txt restrictions. The files are described           Baseline robots.txt . We use web accesses associated with this
below and shown in Figures 5-8.                                           version of robots.txt as a control group to determine how/if bot
                                                                          behavior changes in response to stricter directives.
• Base version (Fig. 5): All bots can access all but three pages          5 Googlebot, Slurp, bingbot, Yandexbot, DuckDuckBot, BaiduSpider, DuckAssistBot,
  (/404, /dev-404-page, /secure/*). This was our institution’s            ia_archiver
  standard robots.txt setup.                                              6 https://github.com/google/robotstxt
                                                                                                                                       IMC ’25, October 28–31, 2025, Madison, WI, USA



User-agent: *                                                                                          User-agent: *
Allow: /                                                                                               Allow: /
Disallow: /404                                                                                         Disallow: /404
Disallow: /dev-404-page                                                                                Disallow: /dev-404-page
Disallow: /secure/*                                                                                    Disallow: /secure/*
                                                                                                       Crawl-delay: 30
Figure 5. Original robots.txt file. Sitename and host fields are in all
robots.txt versions but were removed for anonymous submission.                                         Figure 6. Version 1 robots.txt file requires a 30 second crawl delay from
                                                                                                       all bots.

User-agent: Googlebot
Allow: /                                                                                         User-agent: Googlebot
Disallow: /404                                                                                   Allow: /
Disallow: /dev-404-page                                                                          Disallow: /404
Disallow: /secure/*                                                                              Disallow: /dev-404-page
                                                                                                 Disallow: /secure/*
[above block repeated for user agents: Slurp,
bingbot, Yandexbot, DuckDuckBot, BaiduSpider,                                                    [above block repeated for user agents Slurp,
DuckAssistBot, ia_archiver]                                                                      bingbot, Yandexbot, DuckDuckBot, BaiduSpider,
                                                                                                 DuckAssistBot, ia_archiver]
User-agent: *
Allow: /page-data/*                                                                              User-agent: *
Disallow: /                                                                                      Disallow: /

    Figure 7. Version 2 robots.txt file disallows page-data for most bots.                             Figure 8. Version 3 robots.txt file disallows all pages for most bots.


                          Bot category                         Crawl delay          Endpoint access             Disallow all          Category average
                          AI Assistants                        0.910 (2077)         0.131 (2154)                1.000 (1126)                   0.616
                          AI Data Scrapers                     0.560 (1857)         0.352 (1824)                0.766 (1818)                   0.559
                          AI Search Crawlers                   0.895 (1157)         0.623 (974)                 0.348 (1056)                   0.631
                          Fetchers                             0.925 (249)          0.283 (250)                 0.377 (235)                    0.531
                          Headless Browsers                    0.036 (2777)         0.278 (4207)                0.011 (1282)                   0.155
                          Intelligence Gatherers               0.809 (1120)         0.372 (549)                 0.094 (1008)                   0.450
                          Other                                0.486 (5685)         0.139 (3801)                0.019 (3688)                   0.255
                          SEO Crawlers                         0.635 (1564)         0.831 (1215)                0.639 (1268)                   0.695
                          Search Engine Crawlers               0.780 (6345)         0.366 (5925)                0.189 (6314)                   0.447
                          Directive average                    0.609                0.310                       0.307                           0.420
Table 5. Bots are most likely to comply with the crawl delay directives, and SEO Crawlers are the most compliant bots overall. We measure this by computing weighted
averages of compliance ratios, weighted by number of bot accesses, for all bots in a particular category. We bold the highest compliance value in each row to show directive-level trends in
compliance and also bold the highest row and column averages (last row/column).



Crawl delay compliance (v1). This robots.txt version imple-                                       In other words, we compute the ratio of access time deltas greater
ments a 30 second crawl delay, the minimum time bots must wait                                    than or equal to 30 seconds to total time deltas for tuple 𝜏𝑖 . If
between successive page accesses. To determine compliance with                                    𝐶𝜏𝑖 = 1, all access time deltas complied with the 30 second crawl
this directive, we first stratified our dataset into sets of accesses                             delay directive, and if 𝐶𝜏𝑖 = 0, none did. If there was only one
associated with a unique triple 𝜏𝑖 = (ASN, IP hash, user-agent),                                  access instance associated with a given 𝜏𝑖 triple, we count this as
𝑖 ∈ [0, 𝐾], where 𝐾 is the total number of 𝜏 tuples in our dataset.                               an instance of compliance, so 𝐶𝜏𝑖 = 1.
This ensured we were correctly matching access logs with their                                        After computing 𝐶𝜏𝑖 for the crawl-delay dataset, we run the same
unique requesting entity. We then sort each set of accesses by time                               compliance ratio calculation on all access time deltas for 𝜏 triples
and compute the time elapsed between each successive access.                                      in the baseline robots.txt dataset, 𝐶𝜏 𝑗
                                                                                                                                            𝑑𝑒 𝑓 𝑎𝑢𝑙𝑡
                                                                                                                                                      , to determine the base
   We denote 𝛿𝜏𝑖 = {𝛿𝜏𝑗𝑖 | 𝑗 ∈ [0, 𝑛𝑖 ]} as the set of access time deltas                         rate of compliance with the 30 second crawl delay directive. We
associated with tuple 𝜏𝑖 , 𝑛𝑖 accesses total. Then, the compliance ratio                          then use a paired z-test for difference in proportions to determine
for tuple 𝜏𝑖 , 𝐶𝜏𝑖 is defined as                                                                  if there is a statistically significant shift in the rate of compliance
                                                                                                  with the crawl delay directive for bots before/after the crawl-delay
                                      |{𝛿𝜏𝑗𝑖 |𝛿𝜏𝑗𝑖 ≥ 30}|                                         in robots.txt is enforced. Since a single user agent (a term we
                             𝐶𝜏𝑖 =                        .
                                                𝑛
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                       Taein Kim et al.


use synonymously with bot) can be associated with multiple 𝑡𝑎𝑢𝑖
                                                                              Answer to RQ1: Bots comply most with the crawl delay direc-
tuples—for example, multiple IP addresses declare the same user-
                                                                              tive and least with the disallow all directive. This indicates that
agent—we first group tuples based on user agent name, then analyze
                                                                              bots are less likely to comply with stricter robots.txt di-
behavior across all 𝜏𝑖 tuples associated with this user agent.
                                                                              rectives.
Endpoint access compliance (v2). This robots.txt version re-
stricts bots (except for a group of SEO bots, see §4.1) to only access-       To answer RQ2, we compute the average compliance rate across
ing subpages under a single endpoint, /page-data, on the site. Com-       all directives for each category and list this in the rightmost column
puting the ratio of compliance with this directive is more straight-      of Table 5. From this, we see that:
forward. For each unique user-agent, we count its accesses to either
the robots.txt file (which is always allowed) or /page-data sub-
pages and compute the ratio of this to the user agent’s total page            Answer to RQ2: SEO Crawlers exhibit the highest rate of
accesses. This compliance ratio 𝐶𝜏𝑖 is 1 if the user-agent only ac-           compliance with robots.txt directives, followed closely by
cesses the allowed pages, robots.txt and page-data, and is near               AI Assistants and AI Search Crawlers.
0 if it consistently accesses many other pages. We then compute
an identical compliance metric for user agents under our default             SEO Crawlers rely heavily on robots.txt files to guide their
robots.txt and use this as the baseline for a paired z-test for differ-   actions, so their high compliance rate makes sense. The high com-
ences in proportions between the two datasets. Ideally, we should         pliance rates of AI Assistants and AI Search Crawlers are more
see a significant uptick in compliance under the endpoint directive.      surprisingly, especially given articles in the grey literature about AI
Disallow compliance (v3). The final robots.txt version pre-               bot non-compliance with robots.txt [27, 38]. Further exploration
vents most bots (again, see exceptions in §4.1) from accessing any        of this disconnect is interesting future work. The least respectful
endpoint on the page, although robots.txt is always allowed.              bots, in contrast, are Headless Browsers and "Other." Since both
“Compliance” in this setting is therefore the ratio of robots.txt ac-     these categories serve somewhat as a catchall, bots in this category
cesses to total page accesses. If the bot behaves, all page accesses      are more obscure, making noncompliance unsurprising.
should be to robots.txt , resulting in a compliance ratio of 1.              Finally, we consider individual bot behavior in answering RQ3.
Again, we compute this metric for both the dataset of disallow ac-        Figure 9 shows the change in compliance ratio from baseline for
cesses and the baseline dataset and use a paired z-test for differences   each directive across the 26 bots with ≥ 5 web accesses under
in proportion to measure change in compliance.                            each directive, denoting statistically significant shifts with a red
                                                                          dotted line. Table 6 breaks out these bots by their category and in-
                                                                          cludes information about their sponsoring organization and public
4.3     Results and Discussion                                            promises made to respect robots.txt. From Figure 9 we see a de-
                                                                          creasing trend in baseline compliance with robots.txt directives
In our analysis of robots.txt compliance, we consider three main
                                                                          as we move from crawl delay to disallow all. This indicates that
research questions:
                                                                          a number of bots complied by default with our 30 second crawl
                                                                          delay. Additionally, several bots make notable efforts to comply
• RQ1: With which directive are bots most likely to comply?               with each directive—Amazonbot, ClaudeBot, and GPTBot in partic-
• RQ2: Which category of bots have the highest rate of overall            ular. Finally, several bots (such as PerplexityBot) explicitly stated
  compliance?                                                             they will not respect robots.txt (see Table 6) but have somewhat
• RQ3: Do any individual bots exhibit interesting trends?                 high compliance. This indicates either that they comply by default
                                                                          (which happened frequently for crawl delay) or are more respectful
   To answer RQ1 and RQ2, we group bots by their Dark Visitors            than they claim. There are also bots like BrightEdge that claim to
category and compute the weighted average of bot compliance with          respect robots.txt but have low compliance.
the 3 directives for category. We weight the average by number
of accesses from a particular bot, so the category average is more            Answer to RQ3: There is significant variation in individual
heavily weighted towards more common bots. We made this choice                bot responses to robots.txt directives.
due to observed uneven distributions of bot accesses in our dataset.
For example, some bots never comply with the directive but appear
less than 10 times, while others comply at a much higher rate
and appear hundreds of times. A weighted average captures this
                                                                          5     Exploring possible confounding variables in
nuanced behavior. Table 5 displays these results.                               robots.txt analysis
   We begin with RQ1. In Table 5, we bold the directive with the          While the prior section shows that some bots respect robots.txt ,
highest compliance rate for each bot. From this, we see that 5 cate-      there are still several issues with relying on robots.txt for restrict-
gories of bots comply the most with crawl delay, while 2 categories       ing bot behavior. First, bots may simply not check robots.txt fre-
of bots each have highest compliance with endpoint access and dis-        quently enough for changes in robots.txt to be effective pre-
allow all. Furthermore, we compute the average compliance rate for        ventative measures. Second, bots may “spoof” their user agent,
each directive, the last row in the table, and find the highest average   pretending to be a bot with high permissions in robots.txt (e.g.
compliance with crawl-delay—nearly 2x that of the next-highest,           Googlebot in our situation) to access otherwise-restricted content.
endpoint access. Based on this analysis, we conclude that:                In this section, we investigate how likely these two scenarios are in
                                                                                                                                    IMC ’25, October 28–31, 2025, Madison, WI, USA


                                         Crawl Delay                                   Endpoint Access                                         Disallow All
                                         Default robots.txt
      Academicbotrtu                     Experiment robots.txt
                                         Not significant
           AhrefsBot                     Statistically significant
          Amazonbot
   Apache-httpclient
             Applebot
                  Axios
  Brightedge crawler
          Bytespider
        Chatgpt-user
           ClaudeBot
                Coccoc
       Dataforseobot
                Dotbot
 Facebookexternalhit
        Go-http-client
                Gptbot
    Headlesschrome
              Iframely
    MicrosoftPreview
        PerplexityBot
              Petalbot
     Python-requests
 Semanticscholarbot
         SemrushBot
          Seznambot
     Skypeuripreview
      Slack-imgproxy
    Yandex.com-bots

                           0.0     0.2     0.4      0.6       0.8    1.0      0.0     0.2     0.4     0.6      0.8     1.0       0.0     0.2     0.4      0.6     0.8     1.0
                                    Compliance ratio                                   Compliance ratio                                   Compliance ratio
Figure 9. Many bots comply by default with the 30 second crawl delay (leftmost graph), but the rate of compliance decreases overall as robots.txt restrictions
tighten. We exclude results for exempted SEO bots and highlight statistically significant (𝑝 ≤ 0.05) shifts with red dotted lines. We also exclude results for bots that appear to have
spoofed their user agent. Results for only putative spoofed bots are in Appendix A.2, and additional analysis of observed spoofing behavior is in §5.


practice, to help practitioners understand practical limits of relying                         settings, both points are impossible to verify experimentally. We
on robots.txt to restrict bot behavior.                                                        speculate that when bots comply with the crawl-delay directive
                                                                                               without checking, compliance may have occurred naturally. It is
                                                                                               unclear how compliance with stricter directives regarding page
5.1     Frequency of robots.txt updates                                                        access could occur by chance, but investigation of the possibility of
Motivation. There were several bots that simply never checked                                  robots.txt caching is out of scope for this paper.
robots.txt during our experiments: 9/34 for the crawl delay ex-                                   The other interesting pattern in Table 7 is that some bots check
periment, and 15/47 for both the endpoint access and the disallow-                             robots.txt under some conditions but not others (e.g. DuckDuck-
all experiments. Some of these bots still complied at least some-                              Bot, Bytespider). This raises the question of whether some bots
what with the directives, but others did not comply at all. Table 7                            simply check robots.txt infrequently. The standard set forth by
lists all bots that did not check at least one of our experimental                             Google (which other bots often follow) is that bots should check
robots.txt versions and their rates of compliance for each version.                            robots.txt every 24 hours [23] but some bots may not follow
    The case where bots never check robots.txt but still com-                                  this. Knowing which bots check robots.txt less frequently on
ply (e.g. Slackbot, Googlebot-Image, Brightedge Crawler) raises                                average could help web hosts determine how long they should
some interesting questions. Do the bots comply without checking                                expect to wait before bots adjust behavior based on their deployed
robots.txt because (1) compliance happens naturally (e.g. direc-                               robots.txt and/or know if changing the robots.txt file is the
tive is permissive enough) or (2) they retrieve robots.txt from                                right approach for deterring a particular bot.
some other cached source? Without knowledge of crawler internal
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                                               Taein Kim et al.



                                                                                        Promise to           Crawl delay            Endpoint              Disallow
                                 Sponsoring                 Bot
 Bot Name                                                                                 respect            robots.txt            robots.txt            robots.txt
                                   entity                category
                                                                                        robots.txt           compliance            compliance            compliance
 Academicbotrtu                  Riga Technical           Other                           Unknown                  0.939                 0.032                0.045
 AhrefsBot                       Ahrefs                   SEO                               Yes                    0.697                 1.000                1.000
 Amazonbot                       Amazon                   AI Search                         Yes                    0.973                 1.000                1.000
 Apache-httpclient               Apache                   Other                           Unknown                  0.091                 0.043                0.000
 Applebot                        Apple                    AI Search                         Yes                    0.841                 0.444                0.043
 Axios                           Open Source              Other                             No                     0.060                 0.000                0.000
 BrightEdge                      BrightEdge               SEO                               Yes                    1.000                 0.284                0.000
 Bytespider                      ByteDance                AI Data Scraper                   No                     0.398                 0.000                0.000
 ChatGPT-User                    OpenAI                   AI Assistant                        Yes                  0.910                 0.131                1.000
 ClaudeBot                       Anthropic                AI Data Scraper                     Yes                  0.480                 1.000                1.000
 Coccoc                          Coc Coc                  Search Engine                       Yes                  0.704                 0.941                0.929
 DataForSEOBot                   DataForSEO               SEO                               Yes                    0.573                 0.667                0.024
 Dotbot                          Moz                      SEO                               Yes                    0.615                 1.000                0.988
 Facebookexternalhit             Meta                     Fetcher                           No                     0.920                 0.281                0.375
 Go-http-client                  Open Source              Other                           Unknown                  0.474                 0.167                0.012
 GPTBot                          OpenAI                   AI Data Scraper                   Yes                    0.634                 0.305                1.000
 Headlesschrome                  Open Source              Headless Browser                Unknown                  0.036                 0.278                0.011
 Iframely                        Itteco                   Other                             Yes                    0.254                 0.000                0.000
 MicrosoftPreview                Microsoft                Other                             Yes                    0.294                 0.000                0.000
 PerplexityBot                   Perplexity               AI Search                         No                     0.933                 0.897                0.202
 PetalBot                        Huawei                   Search Engine                     Yes                    0.812                 0.643                1.000
 Python-requests                 Open Source              Other                           Unknown                  0.462                 0.051                0.000
 SemanticScholarBot              Allen AI                 Search Engine                     Yes                    0.663                 1.000                1.000
 SemrushBot                      Semrush                  SEO                                 Yes                  0.521                 0.986                0.993
 SeznamBot                       Seznam.cz                Search Engine                       Yes                  0.565                 0.833                1.000
 SkypeUriPreview                 Microsoft                Other                               Yes                  0.726                 0.000                0.000
 Slack-imgproxy                  Salesforce               Other                               No                   0.917                 0.000                0.000
 Yandex.com/bots                 Yandex                   Search Engine                       Yes                  0.992                 0.361                0.363
Table 6. Individual bots respond differently to our robots.txt directives. We plot the top 26 bots with ≥ 5 accesses under each of our robots.txt directives. For user agents
associated with scraping libraries, we list “open source” as the sponsoring entity.



Methodology. To understand the frequency with which bots check                            time window length, we then counted the number of windows in
robots.txt , we first find additional sites in our dataset for which                      which the bot accessed robots.txt throughout our 40 day dataset.
robots.txt were deployed with meaningful restrictions (e.g. con-                          We report a bot as “complying” with a particular time window
tained at least one directive designed to change bot behavior)                            access length if every time window of that length in the dataset
and were publicly available. Three out of the 36 total sites had                          contains a robots.txt access. Using the variable length time win-
robots.txt that met this criteria. All three files were identical and                     dows allows us to see the bounds on robots.txt frequency—do
implemented simple restrictions on /404 and /secure endpoints                             bots access it every 12 hours? Every 24? Every 168?
on their respective sites. Through dataset inspection, we found that                         We then grouped these results by bot category (e.g. Dark Visitors
all bots respected these restrictions.                                                    categories used previously), to give a better sense of aggregate bot
    To then analyze the frequency with which bots checked these                           behavior, and report the proportion of bots in each category that
files, we segmented the access logs for each bot into variable length                     check robots.txt within each of the 5 time windows in Figure 10.
time windows (12hrs, 24hrs, 48hrs, 72hrs, 168hrs) starting from                           Results. Some categories of bots (scrapers, archivers, and intelli-
when the bot first accessed any of these robots.txt files. For each                       gence gatherers) consistently re-check robots.txt within 12 hours
                                                                                                                                       IMC ’25, October 28–31, 2025, Madison, WI, USA


                                                 Crawl delay robots.txt                      Endpoint access robots.txt                        Disallow all robots.txt
                       Bot
                                           Checked robots.txt            Compliance      Checked robots.txt            Compliance       Checked robots.txt                 Compliance
 Apache-HttpClient                                    No                      0.10                  Yes                    0.05                     No                           0.0
         Axios                                        No                      0.0                   No                      0.0                     No                           0.0
     BaiduSpider                                      No                       1.0                  No                     0.51∗                    No                          0.0∗
 BrightEdge Crawler                                   No                       1.0                  No                     0.28                     No                           0.0
      Bytespider                                      Yes                     0.35                  No                      0.0                     Yes                         0.02
    DuckDuckBot                                       Yes                     0.07                  No                      0.0∗                    Yes                         0.02∗
  Googlebot-Image                                     No                      0.98                  No                     0.0∗                     No                          0.0∗
       Iframely                                       No                      0.17                  No                      0.0                     No                           0.0
 Microsoft-Preview                                    No                      0.13                  No                      0.0                     No                           0.0
  SkypeURIPreview                                     No                      0.67                  No                     0.01                     No                           0.0
   Slack-ImgProxy                                     No                      0.98                  No                      0.0                     No                           0.0
Table 7. Bots that skipped robots.txt check during one or more robots.txt experiments but still complied. ∗ = bot excluded from endpoint and disallow-all robots.txt at
institution’s request.




                                                          Frequency of robots.txt checks across bot types
                            0.6
    re-checked robots.txt
      Prop. of bots that




                            0.5
                                           Within 168 hours
                            0.4            Within 48 hours
                            0.3            Within 24 hours
                                           Within 12 hours
                            0.2
                                         per
                                             s
                                                      ver
                                                          s
                                                                       ncers Dataers                       e      s
                                                                                                       gins adlessers tcher
                                                                                                                            s                  er                 nts           rchrs
                                     r a          h i              g e                    O s
                                                                                       SE wler       n                                     Oth              sis
                                                                                                                                                                ta          e a
                                                                                                                                                                           S le
                                  Sc           Arc             elli ere ASI crap                  h E er e w
                                                                                       Cra earc rawl H Bro
                                                                                                                      Fe                                  As            AI Craw
                                                            IntGath                                                                                  AI
                                                                                               S C
                                   Figure 10. Some bots do not check robots.txt very frequently. AI assistants and AI search crawlers check robots.txt the least.


if they check it at all. Other categories exhibit more variable behav-                               themselves, potentially circumventing certain robots.txt restric-
ior, but increasing the window of time between robots.txt checks                                     tions. Some bots, like Googlebot, have elevated privileges in many
typically leads to a higher re-check rate. AI-related bots (AI As-                                   robots.txt files (including our experiments). By spoofing Google-
sistants and AI search crawlers) have the lowest re-check rates                                      bot’s user agent, a bot could fly under the radar for longer before
with less than 40% of bots checking robots.txt within a 168 hour                                     being banned. They could eventually be detected via IP address
window. Thus, frequent updates to robots.txt may not effectively                                     checks and behavioral patterns, but spoofing could help them avoid
prevent scraping, particularly for AI bots.                                                          early flagging.
                                                                                                        Since a spoofing agent may not necessarily abide by the same
                                                                                                     rules as the benevolent bot, it may not, for example, respect robots.txt .
5.2            User agent spoofing                                                                   This could plausibly explain the partial non-compliance we saw
Motivation. Our analysis of §4 included checks for user agent                                        with some of our robots.txt directives. The grey literature gives
“spoofing.” Here, we describe additional details of our methods for                                  some evidence of such spoofing in practice, particularly for large-
detecting spoofing and results. A key motivation for this investiga-                                 scale AI bots [27].
tion was our observation that a few bots had high-but-not perfect                                    Methods. We analyzed web traffic data for known bots and ob-
compliance rates. For example, Googlebot had a 0.65 compliance                                       served empirically that most bots are overwhelmingly associated
rate with the 30 second crawl delay in robots.txt , despite check-                                   with a particular ASN. For example, 99.62% of Googlebot’s traf-
ing robots.txt several times during this experiment. Similarly,                                      fic comes from the GOOGLE-CLOUD-PLATFORM ASN, while 99.76%
Amazonbot had a 0.96 compliance rate, even though it regularly                                       of GPT-Bot’s traffic is from MICROSOFT-CORP. Based on this, we
checked robots.txt . Several other popular bots like GPT-Bot and                                     develop an empirical heuristic that if a bot’s traffic is associated
bingbot had similar trends.                                                                          90% of the time with one ASN, other ASNs associated with this
   This led us consider how much bot “spoofing” affected measured                                    user agent are likely spoofed. Using this heuristic, we analyze web
compliance rate for certain well-known bots. The useragent field                                     accesses from our dataset and flag any bots associated with more
in a web access request is manually set by the requesting agent,                                     than 1 ASN for which one ASN has over 90% of the traffic. Here, we
so malicious bots can easily manipulate this field to misrepresent
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                  Taein Kim et al.


focus specifically on well-known bots, for which spoofing is more       bots may behave differently on different types of sites (e.g. sites
interesting.                                                            not affiliated with a large, well-resourced university). The second
Results. Overall, we identify 18 bots for which spoofing may            robots.txt study was conducted on a single website, raising the
have occurred. In Table 8, we show the flagged bots, the domi-          possibility that bots behaved differently on this site than elsewhere.
nant ASN (making up ≥ 90% of bot traffic), and the suspicious           Both studies only capture a snapshot of bot behavior during a 45
ASNs (≤ 1% of traffic). Although many flagged bots are only asso-       day time window. Bot behavior will likely evolve over time, making
ciated with two ASNs, some popular bots such as Googlebot are           it difficult to draw permanent lessons from our findings. Finally, in
associated with up to 24. Our analysis cannot prove that these in-      the first study, bot behavior was not static over time, which could
frequent ASNs belong to spoofers (maybe Google contracts with           impact findings from the second study.
Telefonica_de_Espana?), but it strongly suggests this is the case.      Future work. Numerous threads of future work can build on this
   There are, on average, less than 5 web accesses associated with      study. First, continued work is needed to find low-cost solutions
these infrequent ASNs for most of the flagged bots. Notable excep-      to unwanted data scraping. This could take the form of a legally
tions are Baiduspider, with 381 potentially spoofed accesses out        enforceable standard, a novel technical tool, or another new ap-
of 15, 132; Googlebot, with 33 out of 9103; and SkypeURIPreview,        proach. Second, understanding needs of mid-size web hosts who
with 26 out of 831. This means that spoofed bots may cause some,        might be exceptionally targeted by AI scraping (such as libraries
but not all, of the noncompliance with robots.txt observed in §4.       and archives) through a user study could surface new, more tar-
We believe this relatively low spoofing rate could be due to tools      geted ways to provide more controlled access to this valuable data.
deployed by our institution to filter out potential spoofers using      Finally, additional work could dive into the spoofing analysis of
whitelists of known IP addresses for common bots. Since these           §5, determining more robust anti-spoofing methods that catch bots
tools prevent certain suspicious bots from accessing institutional      who slip through other enforcement mechanisms.
content a priori, we will not observe their traffic in our dataset.
Nevertheless, the presence of potential spoofed bots that evade this
analytical dragnet is interesting.
Limitations. The study of spoofing presented here has several
limitations. First, our threshold of 90% of traffic originating from
a single ASN is somewhat arbitrary. Future work could explore
whether adjusting this threshold surfaces other interesting behav-
iors. Second, our analysis does not allow us to definitively state
whether a bot is spoofing its user agent. Future work could con-
sider alternative means, such as honeypots, that could enable more
confident conclusions about which bot instances are spoofed.

6    Discussion
From this large-scale study, we note several limitations of using
robots.txt as a deterrent for web scrapers, particularly AI scrap-
ers. First, we observe that bots are less likely to comply with more
restrictive robots.txt directives, such as denying access to certain
subpages, but are friendlier about respecting crawl delay. This im-
plies that leveraging robots.txt alone to prevent unwanted scrap-
ing could be ineffective. Second, we observed that many bots with
known user agents in our data never checked the robots.txt file
or check it infrequently. This means that any changes made to
robots.txt to prevent unwanted scraping (e.g. [37]) would not be
noticed by the scraper for significant time (if they are respected at
all). Finally, we observe numerous instances of potential spoofing of
well-known bots, indicating that malicious user-agents may attempt
to evade robots.txt restrictions by masquerading as bots with
higher privileges. Together, these suggest that robots.txt does
not provide a universally respected signal for bot behavior, high-
lighting the need for more strongly-enforceable methods to prevent
unwanted scraping.
Limitations of our study. This study has several drawbacks
that may limit the generalizability of its findings. The first study
only considered traffic from 36 websites owned by our institution.
While these websites saw significant traffic during the course of
data collection, they represent a small subset of sites online, and
                                                                                                                                   IMC ’25, October 28–31, 2025, Madison, WI, USA


                Bot                        Main ASN (> 90% of accesses)                                   Possible spoofing ASNs (< 5% of accesses)
         AdsBot-Google                                    GOOGLE                                                               DMZHOST
            AhrefsBot                                       OVH                                                             AHREFS-AS-AP
           Amazonbot                                  AMAZON-AES                                                CONTABO, DIGITALOCEAN-ASN
                                                                                             CHINAMOBILE-CN, CHINANET-BACKBONE, CHINANET-IDC-BJ-AP,
           Baiduspider                            CHINA169-Backbone                                   CHINATELECOM-JIANGSU-NANJING-IDC,
                                                                                                  CHINATELECOM-ZHEJIANG-WENZHOU-IDC, HINET
                                                                                                           Clouvider, HOL-GR,MICROSOFT-CORP-AS,
             bingbot                   MICROSOFT-CORP-MSN-AS-BLOCK
                                                                                                           ORG-TNL2-AFRINIC, ORG-VNL1-AFRINIC
            ClaudeBot                                  AMAZON-02                                                   GOOGLE-CLOUD-PLATFORM
         DuckDuckBot                   MICROSOFT-CORP-MSN-AS-BLOCK                                             DIGITALOCEAN-ASN31, INTERQ31
                                                                                                                   AMAZON-02, AMAZON-AES,
      facebookexternalhit                               FACEBOOK
                                                                                                                     KAKAO-AS-KR-KR51
             GPTBot                    MICROSOFT-CORP-MSN-AS-BLOCK                                                     BORUSANTELEKOM-AS
     Google Web Preview                                   GOOGLE                                                              AMAZON-02
       Googlebot-Image                                    GOOGLE                                                              AMAZON-02
                                                                                                     52468, ASN-SATELLITE, ASN270353, CDNEXT,
                                                                                                    CHINANET-BACKBONE, Clouvider, DATACLUB,
                                                                                              HOL-GR, HWCLOUDS-AS-AP, IT7NET, LIMESTONENETWORKS,
           Googlebot/                                     GOOGLE                                    M247, ORG-RTL1-AFRINIC, ORG-TNL2-AFRINIC,
                                                                                                        P4NET, PROSPERO-AS, RELIABLESITE,
                                                                                                RELIANCEJIO-IN, ROSTELECOM-AS, ROUTERHOSTING,
                                                                                                 TENCENT-NET-AP-CN, Telefonica_de_Espana, VCG-AS
      meta-externalagent                                FACEBOOK                                                        DIGITALOCEAN-ASN
       SkypeUriPreview                 MICROSOFT-CORP-MSN-AS-BLOCK                                                       AMAZON-AES, M247
 Snap URL Preview Service                             AMAZON-AES                                                              AMAZON-02
            Twitterbot                                   TWITTER                                                      PROSPERO-AS, Telegram
                                                                                                                   AMAZON-02, AMAZON-AES,
       yandex.com/bots                                    YANDEX
                                                                                                                       PROSPERO-AS
                          Table 8. Popular bots with one dominant ASN and several infreqently-appearing ASNs—a possible sign of spoofing.



References                                                                                      [12] Elie Bursztein, Jonathan Aigrain, Angelika Moscicki, and John C Mitchell. 2014.
 [1] 2007. Can a /robots.txt be used in a court of law? https://www.robotstxt.org/                   The end is nigh: Generic solving of text-based { CAPTCHAs } . In 8th USENIX
     faq/legal.html.                                                                                 Workshop on Offensive Technologies (WOOT 14).
 [2] 2022. RFC 9309: Robots Exclusion Protocol. https://www.rfc-editor.org/rfc/                 [13] Elie Bursztein, Steven Bethard, Celine Fabry, John C Mitchell, and Dan Jurafsky.
     rfc9309.html.                                                                                   2010. How good are humans at solving CAPTCHAs? A large scale evaluation. In
 [3] 2025. Common Crawl. https://commoncrawl.org/.                                                   IEEE Security & Privacy (SP).
 [4] 2025. Dark Visitors. https://darkvisitors.com/.                                            [14] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav
 [5] Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad                           Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Se-
     Awan, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat Behl,                    bastian Gehrmann, et al. 2023. Palm: Scaling language modeling with pathways.
     et al. 2024. Phi-3 technical report: A highly capable language model locally on                 Journal of Machine Learning Research 24, 240 (2023), 1–113.
     your phone. arXiv preprint arXiv:2404.14219 (2024).                                        [15] Thomas Claburn. 2024. Automation needed to fight army of AI content harvesters
 [6] Open AI. 2025. Introducing Operator. https://openai.com/index/introducing-                      stalking the web. https://www.theregister.com/2024/07/30/taming_ai_content_
     operator/.                                                                                      crawlers/.
 [7] Babak Amin Azad, Oleksii Starov, Pierre Laperdrix, and Nick Nikiforakis. 2020.             [16] Cloudflare. 2024. https://www.cloudflare.com/application-services/products/bot-
     Web runner 2049: Evaluating third-party anti-bot services. In International Con-                management/.
     ference on Detection of Intrusions and Malware, and Vulnerability Assessment.              [17] Hoang Dai Nguyen, Karthika Subramani, Bhupendra Acharya, Roberto Perdisci,
     Springer, 135–159.                                                                              and Phani Vadrevu. 2024. C-Frame: Characterizing and measuring in-the-wild
 [8] Anthropic. 2025. Claude can now search the web. https://www.anthropic.com/                      CAPTCHA attacks. In IEEE Security & Privacy (SP).
     news/web-search.                                                                           [18] Michael Dinzinger and Michael Granitzer. 2024. A longitudinal study of content
 [9] Apple. 2025. About Applebot. https://support.apple.com/en-us/119829.                            control mechanisms. In Companion Proceedings of the ACM Web Conference 2024.
[10] Ashley Belanger. 2025. AI haters build tarpits to trap and trick AI scrapers that ig-           1382–1387.
     nore robots.txt. Ars Technica (2025). https://arstechnica.com/tech-policy/2025/01/         [19] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
     ai-haters-build-tarpits-to-trap-and-trick-ai-scrapers-that-ignore-robots-txt/.                  Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan,
[11] Tom B Brown. 2020. Language models are few-shot learners. arXiv preprint                        et al. 2024. The llama 3 herd of models. arXiv preprint arXiv:2407.21783 (2024).
     arXiv:2005.14165 (2020).                                                                   [20] Roy Thomas Fielding. 2000. Architectural Styles and the Design of Network-
                                                                                                     based Software Architectures. https://ics.uci.edu/~fielding/pubs/dissertation/top.
                                                                                                     htm?deviceId=c9100f78-4e17-449f-b247-5f55bf2b13bc.
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                                                  Taein Kim et al.


[21] Internet Engineering Task Force. 2022. RFC 9309. https://datatracker.ietf.org/      [36] Shayne Longpre. 2025. AI crawler wars threaten to make the web more closed
     doc/html/rfc9309.                                                                        for everyone. MIT Tech Review (2025). https://www.technologyreview.com/2025/
[22] Google. 2025. Gemini Deep Research. https://gemini.google/overview/deep-                 02/11/1111518/ai-crawler-wars-closed-web/.
     research/?hl=en.                                                                    [37] Shayne Longpre, Robert Mahari, Ariel Lee, Campbell Lund, Hamidah Oderinwale,
[23] Google. 2025. How Google interprets the robots.txt specification. https://               William Brannon, Nayan Saxena, Naana Obeng-Marnu, Tobin South, Cole Hunter,
     developers.google.com/search/docs/crawling-indexing/robots/robots_txt.                   et al. 2025. Consent in crisis: the rapid decline of the AI data commons. Proc. of
[24] Matthew Gray. 1995. Measuring the Growth of the Web. https://www.mit.edu/                NeurIPS (2025).
     people/mkgray/growth/.                                                              [38] Dhruv Mehrotra and Tim Marchman. 2024. Perplexity is a Bullshit Machine.
[25] Meriem Guerar, Luca Verderame, Mauro Migliardi, Francesco Palmieri, and                  Wired (2024). https://www.wired.com/story/perplexity-is-a-bullshit-machine/.
     Alessio Merlo. 2021. Gotta captcha em all: A survey of 20 years of the human-or-    [39] Joe Miller. 2013. Jonathon Fletcher: forgotten father of the search engine. BBC
     computer dilemma. ACM Computing Surveys (CSUR) (2021).                                   News (2013). https://www.bbc.com/news/technology-23945326.
[26] Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang.             [40] Kien Pham, Aécio Santos, and Juliana Freire. 2016. Understanding website
     2020. Retrieval augmented language model pre-training. In Proc. of ICML.                 behavior based on user agent. In Proceedings of the 39th International ACM SIGIR
[27] Xe Iaso. 2025. Amazon’s AI Crawler is Making my Git Server Unstable. https:              conference on Research and Development in Information Retrieval.
     //xeiaso.net/notes/2025/amazon-crawler/.                                            [41] Vikas Raunak, Arul Menezes, and Marcin Junczys-Dowmunt. 2021. The cu-
[28] Gautier Izacard and Edouard Grave. 2020. Leveraging passage retrieval with               rious case of hallucinations in neural machine translation. arXiv preprint
     generative models for open domain question answering. arXiv preprint                     arXiv:2104.06683 (2021).
     arXiv:2007.01282 (2020).                                                            [42] Christoph Schuhmann, Romain Beaumont, Richard Vencu, Cade Gordon, Ross
[29] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii,           Wightman, Mehdi Cherti, Theo Coombes, Aarush Katta, Clayton Mullis, Mitchell
     Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of hallucination in          Wortsman, et al. 2022. Laion-5b: An open large-scale dataset for training next
     natural language generation. ACM computing surveys 55, 12 (2023).                        generation image-text models. Proc. of NeurIPS (2022).
[30] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess,            [43] Yang Sun, Ziming Zhuang, and C Lee Giles. 2007. A large-scale study of robots. txt.
     Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. 2020.               In Proceedings of the 16th international conference on World Wide Web. 1123–1124.
     Scaling laws for neural language models. arXiv preprint arXiv:2001.08361 (2020).    [44] Jamba Team, Barak Lenz, Alan Arazi, Amir Bergman, Avshalom Manevich, Barak
[31] Martijn Koster. 1994.        Important: Spiders, Robots and Web Wander-                  Peleg, Ben Aviram, Chen Almagor, Clara Fridman, Dan Padnos, et al. 2024. Jamba-
     ers. https://web.archive.org/web/20131029200350/http://inkdroid.org/tmp/www-             1.5: Hybrid Transformer-Mamba Models at Scale. arXiv preprint arXiv:2408.12570
     talk/4113.html.                                                                          (2024).
[32] Junsup Lee, Sungdeok Cha, Dongkun Lee, and Hyungkyu Lee. 2009. Classification       [45] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne
     of web robots: an empirical study based on over one billion requests. Computers          Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
     & Security 28, 8 (2009).                                                                 Azhar, et al. 2023. Llama: Open and efficient foundation language models. arXiv
[33] Christopher Lehane. 2025. [OpenAI Response] OSTP/NSF RFI: Notice Request                 preprint arXiv:2302.13971 (2023).
     for Information on the Development of an Artificial Intelligence (AI) Action        [46] Udger. 2025. YisouSpider Details. https://udger.com/resources/ua-list/bot-
     Plan. https://cdn.openai.com/global-affairs/ostp-rfi/ec680b75-d539-4653-b297-            detail?bot=YisouSpider.
     8bcf6e5f7686/openai-response-ostp-nsf-rfi-notice-request-for-information-           [47] Luis Von Ahn, Manuel Blum, Nicholas J Hopper, and John Langford. 2003.
     on-the-development-of-an-artificial-intelligence-ai-action-plan.pdf.                     CAPTCHA: Using hard AI problems for security. In International conference
[34] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,        on the theory and applications of cryptographic techniques. Springer.
     Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al.     [48] Luis Von Ahn, Benjamin Maurer, Colin McMillen, David Abraham, and Manuel
     2020. Retrieval-augmented generation for knowledge-intensive nlp tasks. Proc.            Blum. 2008. Recaptcha: Human-based character recognition via web security
     of NeurIPS (2020).                                                                       measures. Science 321, 5895 (2008).
[35] Enze Liu, Elisa Luo, Shawn Shan, Geoffrey M Voelker, Ben Y Zhao, and Stefan         [49] Guixin Ye, Zhanyong Tang, Dingyi Fang, Zhanxing Zhu, Yansong Feng, Pengfei
     Savage. 2024. Somesite I Used To Crawl: Awareness, Agency and Efficacy in                Xu, Xiaojiang Chen, and Zheng Wang. 2018. Yet another text captcha solver: A
     Protecting Content Creators From AI Crawlers. arXiv preprint arXiv:2411.15091            generative adversarial network based approach. In ACM Conference on Computer
     (2024).                                                                                  and Communications Security (CCS).
                                                                                                     IMC ’25, October 28–31, 2025, Madison, WI, USA


A Appendix                                                                 Overall, there were few instances of potentially spoofed requests
                                                                        flagged by our heuristic—see Table 9. However, for the spoofed
A.1 Ethics
                                                                        bots we did observe, there was little respect for robots.txt direc-
This paper raises few ethical concerns, besides those associated with   tives. Particularly for the endpoint access and disallow all directives,
potentially private data included in our user study. As specified in    spoofed bot behaviors typically did not change before/after the di-
the paper, data collection and analysis adhered to a study protocol     rective was implemented. The two notable exceptions to this were
approved by our local Institutional Review Board (IRB). We followed     PerplexityBot under the endpoint access directive and Bytespider
all IRB guidelines for anonymizing and storing this dataset, includ-    under the disallow all directive. Both bots significantly changed
ing making significant efforts to exclude non-bot behavior from the     their behavior, echoing the behavior seen in presumably true in-
dataset and preserve user privacy. We removed sessions originating      stances of the bots in Figure 9. This perhaps indicates that these
from logged-in users from our institution or from institution-hosted    were not spoofed instances, but rather instances of the true bot
WiFi networks, and anonymized IP addresses by hashing them. All         leveraging a different ASN than typically seen. Future work is
data was stored and analyzed on secure servers only accessible by       needed to be able to definitively identify bots with spoofed user
the research team.                                                      agents and avoid such ambiguity.
A.2    Spoofing analysis from §4.3                                      A.3     Statistical tests for change in bot
Our §4.3 analysis of bot compliance with robots.txt excluded bots               compliance
with apparently spoofed user agents. We used the methodology
                                                                        In Table 10, we report z-scores and p-values for the observed
presented in §5 to identify potential spoofing bots: we look at bots
                                                                        changes in compliance from the most common 26 bots in our
for which > 90% of traffic originates from a single ASN, and flag as
                                                                        robots.txt experiments. As is evident, many bots exhibit statis-
possibly spoofed instances any requests with the same useragent
                                                                        tically significant changes in behavior in response to the various
originating from another ASN. In Figure 11, we present parallel
                                                                        robots.txt versions we deploy, indicating some level of awareness
results to Figure 9 but for putative spoofed bots.
                                                                        of the robots.txt protocol and/or willingness to comply.
IMC ’25, October 28–31, 2025, Madison, WI, USA                                                                                                                                          Taein Kim et al.


                                                          Directive                 Crawl delay              Endpoint access                 Disallow all
                                             Legitimate requests                            10333                        11397                    8859
                                         Potentially spoofed requests                        60                           36                      247
Table 9. Potentially spoofed requests account for less than 0.1% of all traffic under our three crawl delay directives. We report the number of perceived legitimate and
potentially spoofed requests recorded during each of the three robots.txt experiments.



                                    Crawl Delay                                                     Endpoint Access                                                     Disallow All
                                    Default robots.txt                                                  Default robots.txt                                              Default robots.txt
   Apache-httpclient                Experiment robots.txt                      AhrefsBot                Experiment robots.txt                  Bytespider               Experiment robots.txt
                                    Not significant                                                     Not significant                                                 Not significant
                                    Statistically significant                                           Statistically significant                                       Statistically significant

         Baiduspider                                                             Aiohttp

             Bingbot
                                                                                   Axios

 Facebookexternalhit
                                                                                 Bingbot
          Googlebot
                                                                      Facebookexternalhit                                                      Googlebot
   Googlebot-image
                                                                               Googlebot
              Gptbot

                                                                                  Okhttp
        SemrushBot


           Twitterbot                                                       PerplexityBot


    Yandex.com-bots                                                      Skypeuripreview                                                  Python-requests

                        0.0   0.2     0.4      0.6       0.8    1.0                         0.0   0.2     0.4      0.6       0.8    1.0                     0.0   0.2    0.4        0.6       0.8   1.0
                              Compliance ratio                                                      Compliance ratio                                               Compliance ratio
Figure 11. The majority of potentially spoofed bots respond less—if at all—to robots.txt changes than their non-spoofed counterparts (see Figure 9). The two
exceptions are PerplexityBot and Bytedance bots under the Endpoint Access and Disallow All directives, which may be misidentified by our spoofing detection heuristic. We highlight
statistically significant (𝑝 ≤ 0.05) shifts with red dotted lines.
                                                                                                                           IMC ’25, October 28–31, 2025, Madison, WI, USA


                                 Bot Name                       Crawl delay                Endpoint                   Disallow
                                                             z-score p-value           z-score p-value            z-score p-value
                                 AcademicBotRTU               -0.74      4.59e-01         0.18     8.59e-01         0.48      6.29e-01
                                 Amazonbot                     0.61      5.44e-01        10.71     0.00e+00        11.43      0.00e+00
                                 Apache-httpclient             0.42      6.73e-01         0.99     3.21e-01        N/A          N/A
                                 Applebot                     -0.45      6.49e-01        -0.20     8.45e-01        -0.04      9.66e-01
                                 Axios                        -0.77      4.39e-01        N/A         N/A           N/A          N/A
                                 BrightEdge                    2.12      3.42e-02         1.21     2.25e-01        N/A          N/A
                                 Bytespider                   -1.96      5.00e-02        -5.04     4.74e-07        -1.30      1.93e-01
                                 ChatGPT-User                 -2.07      3.86e-02        -0.18     8.60e-01        20.62      0.00e+00
                                 Claudebot                     0.44      6.62e-01         8.95     0.00e+00         8.24      2.22e-16
                                 Coccoc                        0.27      7.84e-01         2.67     7.51e-03         2.34      1.91e-02
                                 DataForSEOBot                 2.41      1.62e-02         6.35     2.14e-10        -1.11      2.68e-01
                                 Dotbot                       -0.17      8.63e-01         4.28     1.85e-05         4.66      3.12e-06
                                 Facebookexternalhit           0.95      3.43e-01         2.49     1.27e-02         3.98      6.97e-05
                                 Go-http-client               14.05      0.00e+00        19.24     0.00e+00         5.23      1.72e-07
                                 GPTBot                       11.54      0.00e+00         7.43     1.09e-13        24.20      0.00e+00
                                 HeadlessChrome               -3.15      1.63e-03        -5.15     2.67e-07         0.87      3.83e-01
                                 Iframely                      0.26      7.97e-01        -2.49     1.26e-02        N/A          N/A
                                 MicrosoftPreview             -1.00      3.15e-01        N/A         N/A           N/A          N/A
                                 PerplexityBot                -0.36      7.20e-01         6.86     7.01e-12        -0.90      3.69e-01
                                 PetalBot                      0.58      5.64e-01        -0.27     7.86e-01         2.81      4.94e-03
                                 Python-requests              11.46      0.00e+00         5.04     4.64e-07         1.83      6.71e-02
                                 SemanticScholarBot           10.39      0.00e+00         6.86     6.99e-12         7.36      1.81e-13
                                 SemrushBot                    0.91      3.62e-01         9.90     0.00e+00        10.18      0.00e+00
                                 SeznamBot                    -0.49      6.26e-01         1.65     9.91e-02         2.83      4.65e-03
                                 SkypeUriPreview               0.95      3.44e-01         1.66     9.61e-02        N/A          N/A
                                 Slack-imgProxy                0.35      7.24e-01        N/A         N/A           N/A          N/A
                                 Yandex.com/bots              -1.77      7.64e-02        -0.81     4.21e-01        -0.74      4.58e-01
Table 10. Statistical significance of changes in compliance in response to each robots.txt version. We report z-scores and p-values for the 26 most common bots across all
experiments.
