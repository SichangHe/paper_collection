![](_page_0_Picture_0.jpeg)

.

![](_page_0_Picture_1.jpeg)

![](_page_0_Picture_2.jpeg)

![](_page_0_Picture_3.jpeg)

![](_page_0_Picture_4.jpeg)

Latest updates: [hps://dl.acm.org/doi/10.1145/3646547.3689683](https://dl.acm.org/doi/10.1145/3646547.3689683)

POSTER

## Poster: Web Dependency Analyzer to Identify Resource Dependencies and their Impact on Rendering

YASIN [ALHAMWY](https://dl.acm.org/doi/10.1145/contrib-99661394463), [University](https://dl.acm.org/doi/10.1145/institution-60018123) of Kassel, Kassel, Hessen, Germany PAUL [MERTENS](https://dl.acm.org/doi/10.1145/contrib-99661394240), [University](https://dl.acm.org/doi/10.1145/institution-60018123) of Kassel, Kassel, Hessen, Germany OLIVER [HOHLFELD](https://dl.acm.org/doi/10.1145/contrib-81444608269), [University](https://dl.acm.org/doi/10.1145/institution-60018123) of Kassel, Kassel, Hessen, Germany

Open Access [Support](https://libraries.acm.org/acmopen) provided by: [University](https://dl.acm.org/doi/10.1145/institution-60018123) of Kassel

![](_page_0_Picture_10.jpeg)

PDF Download 3646547.3689683.pdf 27 January 2026 Total Citations: 0 Total Downloads: 458

Published: 04 November 2024

[Citation](https://dl.acm.org/action/exportCiteProcCitation?dois=10.1145%2F3646547.3689683&targetFile=custom-bibtex&format=bibtex) in BibTeX format

IMC '24: ACM Internet [Measurement](https://dl.acm.org/conference/imc) [Conference](https://dl.acm.org/conference/imc) *November 4 - 6, 2024*

Conference Sponsors: [SIGCOMM](https://dl.acm.org/sig/sigcomm) [SIGMETRICS](https://dl.acm.org/sig/sigmetrics)

*Madrid, Spain*

# Poster: Web Dependency Analyzer to Identify Resource Dependencies and their Impact on Rendering

[Yasin Alhamwy](https://orcid.org/0000-0003-4412-581X) alhamwy@uni-kassel.de University of Kassel Germany

[Paul Mertens](https://orcid.org/0009-0004-1586-0633) paul@uni-kassel.de University of Kassel Germany

[Oliver Hohlfeld](https://orcid.org/0000-0002-7557-1081) oliver.hohlfeld@uni-kassel.de University of Kassel Germany

#### ABSTRACT

Modern websites are complex and fetch content from a multitude of different servers or domains. When measuring the complexity of the modern web, an open question is how content that is fetched from these domains contribute to the rendered output of the website. In this poster, we present the Web Dependency Analyzer, a tool that is designed to automatically infer the domains that a website depends on and further analyze the impact of each domain on the rendered output of the site. Our Web Dependency Analyzer instructs a headless web browser to infer the resource dependencies from a large set of input domains and outputs the visual impact of the unavailability of each domain.

#### ACM Reference Format:

Yasin Alhamwy, Paul Mertens, and Oliver Hohlfeld. 2024. Poster: Web Dependency Analyzer to Identify Resource Dependencies and their Impact on Rendering. In Proceedings of the 2024 ACM Internet Measurement Conference (IMC '24), November 4–6, 2024, Madrid, Spain. ACM, New York, NY, USA, [2](#page-2-0) pages.<https://doi.org/10.1145/3646547.3689683>

#### 1 INTRODUCTION

With the rapid growth of smart city initiatives globally, city dashboards, such as the one in Darmstadt [\[1\]](#page-2-1), are gaining popularity and are anticipated to play a crucial role in future decision-making processes [\[7\]](#page-2-2). Additionally, citizens in both developed and developing countries increasingly rely on the internet for entertainment (e.g., social media, streaming) and essential services such as banking. These services are typically websites that incorporate third-party service dependencies and use CDNs (Content Delivery Networks) to enhance design (e.g., Google Fonts) and improve performance [\[5\]](#page-2-3).

However, these online services can become unreachable for various reasons, including cyber-attacks, maintenance, or server overload. This raises several key questions: What visual effects emerge when these services are disrupted? Are these changes noticeable to users, and which version do they prefer? Furthermore, how many websites are impacted if certain services become unreachable? To address these questions, we propose a tool that can retrieve and selectively block dependencies for a list of websites. This tool will generate screenshots and videos for each blocked dependency, facilitating future data analysis. Understanding human perception is crucial in this context; therefore, we will explore methods that align

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s).

IMC '24, November 4–6, 2024, Madrid, Spain © 2024 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-0592-2/24/11 <https://doi.org/10.1145/3646547.3689683>

<span id="page-1-0"></span>![](_page_1_Figure_13.jpeg)

Figure 1: Goal: instruct a headless browser to infer i) the set of domains that a rendering web page depends on and ii) the visual impact of each domain by analyzing the visual impact of the unavailability of each domain.

with how humans discern differences in images when comparing the appearance of the website with blocked dependencies to its original appearance.

#### 2 WEB DEPENDENCY ANALYZER

Goal. Our Web Dependency Analyzer is designed to instruct a headless browser to automatically visit a web page, monitor the domains from which content is being fetched (step 1), and then subsequently test the visual and performance impact of each domain (step 2). It takes a (large) set of domains as input that are visited in parallel to facilitate large-scale Internet measurement studies to study the complexity of the web.

Step 1: Scraping. To scrape the website's content, the tool starts a headless chrome browser instance, opens listeners for all HTTP requests and records them, and then waits for the website to load (or until a certain timeout is reached). After the loading process, the tool downloads the website as one big HTML file including hyperlinks to its resources. Figure [1](#page-1-0) visualises what the tool retrieves.

The tool considers all of these resources as dependencies as they are required for the website to look and function as expected. A dependency can either be internal (Hyperlinks to same domain) or external (Hyperlinks to external domains). When recording website dependencies, a distinction is made between two types: Dynamic – All requests made during navigation to the website and Static – All HTML elements statically present in the HTML page that have src or href attributes. If a network request is sent to a host and this hostname is also found as a static dependency in the HTML page, the dependency type is set to dynamic: dynamic overrides static. The list of dependencies (including the hostnames and IPs) for each website is stored in JSON format.

Validation. To test the tool, a website with known dependencies is created. The tool is able to retrieve all of the dependencies correctly.

<span id="page-2-8"></span><span id="page-2-0"></span>![](_page_2_Picture_2.jpeg)

![](_page_2_Picture_3.jpeg)

![](_page_2_Picture_4.jpeg)

![](_page_2_Picture_5.jpeg)

(a) netflix.com (b) netflix.com with assets.nflxext.com blocked

(c) instagram.com (d) instagram.com with static.cdninstagram.com blocked

Figure 2: Comparison of Netflix and Instagram websites when certain dependencies are blocked

Step 2: visual impact of each dependency. After retrieving all the dependencies and their IPs, the tool blocks each one separately by blocking the request to the given dependency (i.e. the dependency is no longer fetched). The tool observes the website's loading behaviour and generates the Lighthouse [\[2\]](#page-2-4) report (which includes the speed index and other timing metrics), a .webp screenshot and a .webm video of the process, which will be used for further analysis. As this is a time consuming process, a cluster of Node.js processes is created and instead of worker threads, isolated child processes are instantiated that communicate via server ports. The separation of the processes is necessary because Lighthouse is based on singleton instances, which influence each other through parallelization using worker threads in the same Node.js process.

It is important to note that the tool is also able to block multiple dependencies at once; however, to simplify the analysis for now, only one dependency is blocked at a time. Despite that, sensible groupings of dependencies are being considered for future work. Configuration. Using configurations, we can specify which types the tool should analyze. The configuration significantly affects the tool's runtime, as a Puppeteer [\[3\]](#page-2-5) instance, along with a Lighthouse report and possibly a video and screenshot, must be created for each dependency that needs to be blocked.

#### 3 CURRENT RESULTS AND NEXT STEPS

Tranco Top 2000. To employ the Web Dependency Analyzer in the wild, we initially launched it on the Tranco top 2000 [\[6\]](#page-2-6) websites. We then computed perceptual hashes to compare all screenshots of each blocked dependency with the original screenshot of the website. As websites are often designed to be visually appealing to humans, perceptual hashing was used as it allows us to mimic human perception [\[4\]](#page-2-7).

Figure [2](#page-2-8) shows two examples of how Netflix and Instagram look when a certain dependency is blocked. For Netflix (Figures [2a](#page-2-8) and [2b\)](#page-2-8), blocking assets.nflxext.com clearly effects the visual appeal of the website and removes the baked in self advertisements. For Instagram (Figure [2c](#page-2-8) and [2d\)](#page-2-8), blocking static.cdninstagram.com not only visually changes the website but also makes it unusable. While these examples represent extreme cases, there are instances where blocking certain dependencies, such as Google Fonts, results in minimal but noticeable design changes.

Survey. With that in mind, a survey will be conducted to explore how humans perceive visual changes, both extreme and subtle, when certain dependencies are blocked. Some changes might be

so subtle that users barely notice them (e.g., a font change), while others could be extreme, resulting in significant layout shifts or missing elements. The survey would capture how users react to these visual changes and see whether the users prefer the "intended" look (fully loaded with all dependencies) to the "unintended" look (partial or broken due to blocked dependencies).

Tranco Top 1M. While the survey is being conducted, the tool will be ran for the Tranco top 1 million list[1](#page-2-9) [\[6\]](#page-2-6) generated on 2 August 2024 to give us an understanding of how the most popular websites are designed and what percentage of these websites will be impacted if certain services are no longer available or reachable. Of course, the websites will change over time and therefore the tool will be ran at fixed time intervals to explore the changes over time for the foreseeable future.

Ethics. Our data collection methods involve scraping publicly available websites. We ensured that all data collected were publicly accessible and did not involve any personally identifiable information. No private or sensitive information is accessed, stored, or analyzed during our research.

### A ACKNOWLEDGEMENTS

This work has been funded by the LOEWE initiative (Hesse, Germany) within the emergenCITY center [LOEWE/1/12/519/03/05.001(0016)/72].

Many thanks to Thomas Falk for the initial implementation of the Web Dependency Analyzer.

#### REFERENCES

- <span id="page-2-1"></span>[1] [n. d.]. .<https://datenplattform.darmstadt.de>
- <span id="page-2-4"></span>[2] [n. d.]. .<https://developer.chrome.com/docs/lighthouse>
- <span id="page-2-5"></span>[3] [n. d.]. .<https://pptr.dev/>
- <span id="page-2-7"></span>[4] Qingying Hao, Licheng Luo, Steve TK Jan, and Gang Wang. 2021. It's not what it looks like: Manipulating perceptual hashing based applications. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security. 69–85.
- <span id="page-2-3"></span>[5] Aqsa Kashaf, Vyas Sekar, and Yuvraj Agarwal. 2020. Analyzing third party service dependencies in modern web services: Have we learned from the mirai-dyn incident?. In ACM IMC.
- <span id="page-2-6"></span>[6] Victor Le Pochat, Tom Van Goethem, Samaneh Tajalizadehkhoob, Maciej Korczyński, and Wouter Joosen. 2019. Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation. In Proceedings of the 26th Annual Network and Distributed System Security Symposium (NDSS 2019). [https://doi.org/10.14722/](https://doi.org/10.14722/ndss.2019.23386) [ndss.2019.23386](https://doi.org/10.14722/ndss.2019.23386)
- <span id="page-2-2"></span>[7] Meiyi Ma, Sarah M Preum, Mohsin Y Ahmed, William Tärneberg, Abdeltawab Hendawi, and John A Stankovic. 2019. Data sets, modeling, and decision making in smart cities: A survey. ACM Transactions on Cyber-Physical Systems 4, 2 (2019), 1–28.

<span id="page-2-9"></span><sup>1</sup>Available at:<https://tranco-list.eu/list/66W5X>