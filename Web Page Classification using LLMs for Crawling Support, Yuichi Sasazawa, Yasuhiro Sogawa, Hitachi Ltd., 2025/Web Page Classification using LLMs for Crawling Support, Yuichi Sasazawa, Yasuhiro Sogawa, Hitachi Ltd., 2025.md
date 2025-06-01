# Web Page Classification using LLMs for Crawling Support

Yuichi Sasazawa and Yasuhiro Sogawa Hitachi, Ltd. Research and Development Group {yuichi.sasazawa.bj, yasuhiro.sogawa.tp}@hitachi.com

### Abstract

A web crawler is a system designed to collect web pages, and efficient crawling of new pages requires appropriate algorithms. While website features such as XML sitemaps and the frequency of past page updates provide important clues for accessing new pages, their universal application across diverse conditions is challenging. In this study, we propose a method to efficiently collect new pages by classifying web pages into two types, "Index Pages" and "Content Pages," using a large language model (LLM), and leveraging the classification results to select index pages as starting points for accessing new pages. We construct a dataset with automatically annotated web page types and evaluate our approach from two perspectives: the page type classification performance and coverage of new pages. Experimental results demonstrate that the LLM-based method outperformed baseline methods in both evaluation metrics. [1](#page-0-0)

### 1 Introduction

A web crawler is a system designed to collect web pages, primarily used to register web pages in search engines [\(Olston and Najork](#page-6-0) , [2010\)](#page-6-0). As the number of web pages grows daily, efficient crawling of new pages requires the use of appropriate algorithms [\(Heydon and Najork](#page-6-1) , [1999](#page-6-1) ; [Boldi et al.](#page-5-0) , [2004](#page-5-0) ; [Pant et al.](#page-6-2) , [2004\)](#page-6-2). Commercial crawlers generally rely on features provided by websites, such as XML sitemaps and RSS feeds, to gather updated information [\(Schonfeld and Shivakumar](#page-6-3) , [2009\)](#page-6-3). However, there are websites that lack such features. When accessing new pages without relying on site-specific features, it is efficient to inspect only a few pages, such as the home page, but this approach often misses many new pages. Conversely, by revisiting most pages within a website,

<span id="page-0-1"></span>![](_page_0_Picture_7.jpeg)

Figure 1: Examples of "Index Pages" [\(Space.com](#page-6-4) , [2025a\)](#page-6-4), which aim to contain hyperlinks to other pages within the website, and "Content Pages," [\(Space.com](#page-6-5) , [2025b\)](#page-6-5) which contain content such as news articles and columns.

including outdated ones, it is possible to maintain the freshness of pages within the site and comprehensively collect URLs of new pages, but doing so frequently is impractical due to network and computational resource limitations [\(Edwards et al.](#page-5-1) , [2001](#page-5-1) ; [Cho and Garcia-Molina](#page-5-2) , [2003\)](#page-5-2). Additionally, the frequency of past page updates can serve as a crucial indicator for determining the appropriate crawling frequency [\(Fetterly et al.,](#page-5-3) [2003\)](#page-5-3), but this approach encounters a cold-start problem that cannot handle new pages that have no crawl history [\(Han et al.](#page-6-6) , [2019\)](#page-6-6).

One way to improve the efficiency of web page collection is to utilize page types. There are many different types of web pages [\(Chen and Choi](#page-5-4) , [2008](#page-5-4) ; [Qi and Davison](#page-6-7) , [2009\)](#page-6-7), and from the perspective of crawling new pages, it is highly likely that the URLs of new pages can be efficiently collected by identifying web pages intended to provide links to other pages within the website, such as home pages or feed pages, and then concentrating on

<span id="page-0-0"></span><sup>1</sup>The code used in the experiments is available at [https:](https://github.com/ckdjrkffz/web-page-classifier) [//github.com/ckdjrkffz/web-page-classifier](https://github.com/ckdjrkffz/web-page-classifier) .

accessing those pages. However, due to the significant variations in web page structures [\(Crescenzi](#page-5-5) [et al.,](#page-5-5) [2001;](#page-5-5) [Qi and Davison,](#page-6-7) [2009\)](#page-6-7), it is difficult to automatically identify these pages using heuristic rules.

In this study, we propose a method to enhance crawling efficiency by classifying web page types using large language models (LLMs) and leveraging the classification results. Specifically, as shown in Figure [1,](#page-0-1) we broadly categorize web pages into two types: Index Pages, which aim to contain links to other pages, and Content Pages, which aim to present content such as news articles and columns.[2](#page-1-0) We then perform binary classification using GPT-4o-mini and GPT-4o [\(OpenAI et al.,](#page-6-8) [2024\)](#page-6-8), taking the title and body of web pages as input. LLMs trained on large-scale datasets possess advanced language processing capabilities and are expected to accurately classify even previously unseen web pages. While existing studies have explored topic classification of web pages [\(Voros et al.,](#page-6-9) [2023\)](#page-6-9), filtering harmful pages [\(Rashid et al.,](#page-6-10) [2025\)](#page-6-10), and analyzing HTML [\(Gur et al.,](#page-6-11) [2023;](#page-6-11) [Huang et al.,](#page-6-12) [2024\)](#page-6-12) using LLMs, to our knowledge, no prior work has investigated methods for classifying page types using LLMs for crawling support.

In our experiments, we construct a dataset by applying an automatic annotation method to label page types. Using the constructed dataset, we evaluate the page type classification performance and demonstrate that LLMs can classify page types effectively compared to the baseline method. Furthermore, we evaluate the coverage of new pages when using the index pages identified by each method as starting points and show that the LLM-based method can improve performance.

### 2 Method

The overall framework of the proposed method and evaluation approach is illustrated in Figure [2.](#page-2-0) This study has two main objectives: first, to evaluate the performance of page classification using LLMs, and second, to verify whether classifying page types with LLMs improves the efficiency of retrieving new pages during crawling. In this study, we construct a new dataset annotated with page types. The creation process for this dataset is described in Section [2.1.](#page-1-1) Subsequently, the method

for page classification using LLMs is presented in Section [2.2.](#page-2-1)

#### <span id="page-1-1"></span>2.1 Dataset Construction

To evaluate the page type classification performance, a dataset labeled with page types is required. However, such a dataset currently does not exist. Therefore, we construct a new dataset for experimental purposes. Since manually annotating each page would incur high costs, we employ an automated annotation method proposed in this study. The statistics of the constructed dataset are shown in Table [1.](#page-3-0)

Page Type Annotation Method Some websites comprehensively list hyperlinks to nearly all content pages on the site across multiple pages, either in the form of XML sitemaps or HTML pages with titles such as "Latest News" or "All Content Archive." We refer to these pages as "Content Listing Pages." By classifying the web pages listed on content listing pages as content pages and the pages not listed on content listing pages as index pages, annotation can be performed at a lower cost than manual annotation and potentially closer to human judgment. However, since annotation errors are frequent depending on the website, we perform a simple manual review of the annotation results and retain only those websites deemed to be of sufficient quality.

Detailed Procedure We construct the dataset targeting English news websites across multiple domains. First, we select websites that include content listing pages. From these websites, we download 10,000 web pages per site using breadth-first search starting from the home page. Since pages are collected on a site-by-site basis, only internal links are used. Additionally, non-HTML formats such as PDFs are excluded. Next, for each website, we create a script to collect the URLs of content pages linked from the content listing pages, and use these URLs to annotate the type of each page. Finally, we conduct a manual review to retain only websites that meet the quality criteria, and split them into development and test sets on a site-bysite basis.

Construction of the Noisy-Test Set For websites with content listing pages, it is expected that the coverage of new pages will be higher than average, as it is easier to access each content page from content listing pages. Therefore, we also download pages from websites that do not have content listing pages using the same procedure and use this as a

<span id="page-1-0"></span><sup>2</sup>While there are other types of pages, such as login pages and error pages, we assume they are relatively few in number. Thus, in this study, pages other than index pages are collectively treated as content pages.

<span id="page-2-0"></span>![](_page_2_Figure_0.jpeg)

Figure 2: Overview of the proposed method and evaluation approach. Each web page is classified as either an index page or a content page, and new pages are efficiently retrieved starting from index pages. The experiments evaluate two aspects: the page type classification performance and the coverage of new pages.

"Noisy-Test" set for evaluation experiments. While this set cannot be annotated with page types and hence is not used for the evaluation of classification performance, it serves as a challenging dataset to evaluate the generality of our method for new page coverage performance.

New Pages Annotation The dataset we construct simply captures static snapshots of websites and does not dynamically capture changes to web pages to obtain newly posted pages. Therefore, we treat web pages published within a certain number of days prior to the latest date found among the collected pages of that site as new pages. To assess the performance under multiple crawling frequencies, evaluations are conducted under two scenarios based on the duration prior to this latest date: one using pages published within the latest 1 day as new pages, and the other using pages published within the latest 30 days as new pages.

#### <span id="page-2-1"></span>2.2 Page Type Classification using LLMs

A prompt containing the target web page's information and a description of the task is provided to an LLM, which then classifies the input web page as either an index page or a content page. We compare two LLMs offered via the OpenAI API: GPT-4o-mini (gpt-4o-mini-2024-07-18) and GPT-4o (gpt-4o-2024-08-06).

We evaluate two types of input to the LLM: using only the title of the web page, and using both the title and body text of the web page. The body

text of web pages is extracted from HTML content using heuristic rules.[3](#page-2-2) The title succinctly represents the page's content and serves as a crucial clue for classification. The body text provides more information than the title, and if the LLM can interpret its content sufficiently, it can serve as strong grounds for judgment. However, the extracted body text also carries the risk of including noise, such as titles or summaries from related pages, potentially leading to misclassifications. To determine the optimal input for the LLM, we conduct a comparison of these two approaches.

### <span id="page-2-3"></span>3 Experiments

#### 3.1 Evaluation Methods

Evaluation of Page Classification Performance The predictions of each method are evaluated by directly comparing them with the gold labels obtained through automated annotation. Treating index pages as positive, we calculate the classification precision, recall, and F1 score for each site and report the average values.

Evaluation of New Page Coverage We evaluate how comprehensively new pages can be collected by starting from the pages identified as index pages by each method. Coverage is defined as the proportion of new pages that can be reached either directly through links on index pages or indirectly

<span id="page-2-2"></span><sup>3</sup>We use a script modified from ExtractContent3 ([https:](https://github.com/kanjirz50/python-extractcontent3) [//github.com/kanjirz50/python-extractcontent3](https://github.com/kanjirz50/python-extractcontent3)).

<span id="page-3-0"></span>Table 1: Data statistics: The number of index pages, content pages, the total number of collected pages (fixed at 10,000 pages), the number of pages published within latest 1 day, and the number of pages published within latest 30 days for each site.

| Category   | Site Name            | #Index | #Content | #Total | #Latest 1 Day | #Latest 30 Days |
|------------|----------------------|--------|----------|--------|---------------|-----------------|
| Dev        | CNN                  | 2,811  | 7,189    | 10,000 | 165           | 1,470           |
|            | Variety              | 3,924  | 6,076    | 10,000 | 177           | 1,429           |
| Test       | TechCrunch           | 3,721  | 6,279    | 10,000 | 44            | 763             |
|            | Mongabay             | 3,911  | 6,089    | 10,000 | 13            | 150             |
|            | Space.com            | 1,964  | 8,036    | 10,000 | 19            | 316             |
| Noisy-Test | Entertainment Weekly | –      | –        | 10,000 | 74            | 722             |
|            | The New York Times   | –      | –        | 10,000 | 419           | 2,073           |
|            | MedicalNewsToday     | –      | –        | 10,000 | 11            | 128             |
|            | Healthline           | –      | –        | 10,000 | 21            | 247             |

<span id="page-3-2"></span>Table 2: Evaluation results of the page type classification performance on the test set. Reports precision, recall, and F1 score, considering index pages as positive.

| Method      | Input        | Precision | Recall | F1    |
|-------------|--------------|-----------|--------|-------|
| All Pages   | –            | 0.320     | 1.000  | 0.478 |
| Rule-based  | –            | 0.699     | 0.910  | 0.787 |
|             | Title        | 0.989     | 0.643  | 0.777 |
| GPT-4o-mini | Title + Body | 0.992     | 0.570  | 0.697 |
|             | Title        | 0.980     | 0.734  | 0.836 |
| GPT-4o      | Title + Body | 0.984     | 0.820  | 0.894 |

via other new pages, divided by the total number of new pages. For example, if a website has 100 new pages and 80 of them can be reached from the index pages, the coverage is 0.80. The reason why pages that can be reached via new pages are also considered "reachable" is that in actual crawling scenarios, the HTML content of newly accessed pages is also analyzed, and if they contain links to new pages, those pages can also be accessed. The coverage is calculated for each website, and the average value is reported.

Additionally, to evaluate coverage under the same resource constraints for each method, we report the coverage when starting from a fixed number of shallow hierarchy index pages determined by each method.[4](#page-3-1) We report the coverage for five cases of 10, 30, 100, 300, and 1,000 fixed index pages used. In cases where the number of index pages is fewer than the fixed number of pages used for evaluation, shallow hierarchy content pages are added to maintain consistency in evaluation.

### 3.2 Comparison Methods

We compare the performance of the following methods:

- All Pages: All pages are treated as index pages. For the coverage evaluation, a fixed number of the shallowest hierarchy pages are used as starting points.
- Rule-Based: Pages with 9 or fewer words in their titles are treated as index pages.
- LLM: The types of pages are classified using LLMs. We evaluate four combinations using two types of LLMs (GPT-4o-mini and GPT-4o) with two types of inputs (title only and title + body).

The following methods are evaluated only for new page coverage:

- LLM + All Pages: We evaluate a hybrid method where, for a fixed number of access starting points, half are selected from the pages determined to be index pages by LLM and half are selected from the shallow hierarchy pages regardless of their type.
- Gold Labels: Annotations created using content listing pages are used.

#### 3.3 Results

Table [2](#page-3-2) shows the results of the page type classification evaluation. GPT-4o with Title + Body achieves the highest F1 score, outperforming the baseline methods (All Pages and Rule-Based). While all methods using LLMs exhibit high precision, there are significant differences in their recall scores. In other words, LLM-based methods rarely misclassify content pages as index pages, but they tend to misclassify index pages as content pages. Furthermore, while GPT-4o improves its performance

<span id="page-3-1"></span><sup>4</sup> Shallow hierarchy pages mean pages that can be accessed with fewer transitions from the home page.

<span id="page-4-0"></span>Table 3: Evaluation results of coverage for new pages on the test set. Reports the coverage and their averages for 10 combinations: two settings for new pages (pages published within latest 1 day and pages published within latest 30 days) and five settings for the number of index pages at shallow hierarchy levels used as starting points (top 10, 30, 100, 300, and 1,000 pages).

|                         |              | Latest 1 Day |       |       |             | Latest 30 Days |       |       |                         |       |        |         |
|-------------------------|--------------|--------------|-------|-------|-------------|----------------|-------|-------|-------------------------|-------|--------|---------|
| Method                  | Input        | 10P          | 30P   | 100P  | 300P        | 1,000P         | 10P   | 30P   | 100P                    | 300P  | 1,000P | Average |
| All Pages               | –            | 0.920        | 0.927 | 0.935 | 0.942       | 0.967          | 0.542 | 0.613 | 0.718                   | 0.929 | 0.986  | 0.848   |
| Rule-based              | –            | 0.920        | 0.927 | 0.935 | 0.935       | 0.970          | 0.542 | 0.626 | 0.883                   | 0.934 | 0.992  | 0.866   |
|                         | Title        | 0.920        | 0.927 |       | 0.935 0.970 | 0.970          |       |       | 0.542 0.668 0.900 0.980 |       | 0.988  | 0.880   |
| GPT-4o-mini             | Title + Body | 0.594        | 0.601 | 0.601 | 0.842       | 0.842          | 0.428 | 0.562 | 0.820                   | 0.931 | 0.948  | 0.717   |
|                         | Title        | 0.920        | 0.927 |       | 0.935 0.970 | 0.970          | 0.542 |       | 0.643 0.919 0.963       |       | 0.989  | 0.877   |
| GPT-4o                  | Title + Body | 0.920        | 0.927 | 0.935 | 0.952       | 0.970          | 0.542 | 0.640 | 0.914                   | 0.964 | 0.989  | 0.875   |
| GPT-4o-mini + All Pages | Title        | 0.920        | 0.927 | 0.935 | 0.952       | 0.977          | 0.542 | 0.633 | 0.880                   | 0.952 | 0.993  | 0.871   |
| GPT-4o + All Pages      | Title + Body | 0.920        | 0.927 | 0.935 | 0.952       | 0.977          | 0.542 | 0.628 | 0.885                   | 0.934 | 0.993  | 0.869   |
| Gold Labels             | –            | 0.920        | 0.927 | 0.935 | 0.960       | 0.985          | 0.551 | 0.665 | 0.895                   | 0.939 | 0.994  | 0.877   |

<span id="page-4-1"></span>Table 4: Evaluation results of coverage for new pages on the noisy-test set. The evaluation method is the same as that described in Table [3.](#page-4-0)

|                         |              | Latest 1 Day |             |                   |             |        | Latest 30 Days |       |                   |             |        |         |
|-------------------------|--------------|--------------|-------------|-------------------|-------------|--------|----------------|-------|-------------------|-------------|--------|---------|
| Method                  | Input        | 10P          | 30P         | 100P              | 300P        | 1,000P | 10P            | 30P   | 100P              | 300P        | 1,000P | Average |
| All Pages               | –            | 0.413        | 0.468       |                   | 0.570 0.895 | 1.000  | 0.393          | 0.445 |                   | 0.593 0.869 | 0.992  | 0.664   |
| Rule-based              | –            | 0.390        | 0.464       | 0.563             | 0.833       | 0.925  | 0.390          | 0.448 | 0.593             | 0.851       | 0.943  | 0.640   |
|                         | Title        | 0.413        | 0.468       | 0.700             | 0.792       | 0.968  | 0.424          |       | 0.499 0.750       | 0.831       | 0.941  | 0.678   |
| GPT-4o-mini             | Title + Body | 0.216        | 0.317       | 0.626             | 0.656       | 0.963  | 0.362          | 0.445 | 0.704             | 0.722       | 0.953  | 0.596   |
|                         | Title        | 0.413        |             | 0.445 0.728 0.833 |             | 0.972  | 0.381          | 0.466 | 0.759             | 0.823       | 0.938  | 0.676   |
| GPT-4o                  | Title + Body |              | 0.413 0.472 |                   | 0.728 0.819 | 0.970  | 0.394          | 0.454 | 0.758             | 0.824       | 0.948  | 0.678   |
| GPT-4o-mini + All Pages | Title        | 0.413        | 0.456       | 0.725             | 0.874       | 0.977  | 0.393          |       | 0.488 0.760 0.848 |             | 0.956  | 0.689   |
| GPT-4o + All Pages      | Title + Body |              | 0.413 0.472 |                   | 0.728 0.866 | 0.977  | 0.393          |       | 0.453 0.760 0.842 |             | 0.962  | 0.687   |

using the web page body, GPT-4o-mini's performance deteriorates when the body is included. This is likely because the body text, automatically extracted from HTML, includes noise that is difficult for GPT-4o-mini to process appropriately, such as titles or summaries of related pages, and GPT-4omini may lack the capability to effectively interpret the body text.

Next, Table [3](#page-4-0) presents the results of the new page coverage evaluation on the test set. The results confirm that LLM-based methods generally perform better than baseline methods. Regarding the overall average, there is no significant difference among LLM-based methods (except for GPT-4o-mini with Title + Body, which performs poorly), and the results are nearly equivalent to those obtained using gold labels. This suggests that once classification performance reaches a certain threshold, its correlation with coverage becomes low, and further improvements in coverage would require improvements in other elements such as the crawl algorithm.

When comparing the number of index pages used as starting points, there is no notable difference in coverage among methods for smaller page

numbers. However, when using pages published within the latest 1 day as new pages, differences emerge when using 300 or more index pages, and when using pages published within the latest 30 days as new pages, differences are observed when using 30 or more index pages. This is likely because shallow hierarchy pages, especially the home page and pages directly linked from the home page, are often index pages, and when using a small number of index pages as starting points, all methods tend to select the same set of pages around the home page, leading to similar coverage. On the other hand, as the number of index pages used as starting points increases, the page sets selected by each method become different, and the quality of page selection becomes more impactful, resulting in performance differences.

The evaluation results for the noisy-test set, shown in Table [4,](#page-4-1) indicate that LLMs achieve higher coverage than baseline methods, particularly when using 100 index pages. However, for 300 or more pages, the All Pages method achieves higher coverage. This is likely because, on the noisy-test set, it is difficult to comprehensively cover new pages using only index pages. When

starting from a large number of pages, sequentially accessing from shallow hierarchy pages regardless of their type can be more effective in collecting new pages. While each method has its strengths and weaknesses, hybrid methods consistently achieve high coverage under the evaluated conditions. Notably, GPT-4o-mini + All Pages with Title achieves the best results in terms of the average coverage on the noisy-test set. Furthermore, to reinforce the validity of the experimental results, the results of additional experiments using a dataset reconstructed at a different time from the same websites are shown in Appendix [A.](#page-6-13)

## 4 Conclusion

In this study, we proposed a method to improve crawling efficiency by classifying web pages into two types, index pages and content pages, using LLMs, and then using the classification results to crawl web pages by starting from index pages. In the experiments, we constructed a dataset with labeled page types and evaluated the method from two perspectives: page type classification performance and coverage for new pages. The results confirmed that LLMs achieve high performance in both evaluation criteria. Future challenges include the following:

- Subdividing Web Page Types: In this study, pages were classified simply into index pages and content pages, but it may be possible to improve the efficiency of page crawling by further subdividing them. For example, index pages could be divided into pages that contain links to new pages and pages that contain links to old pages, allowing access to be concentrated on the former to retrieve new pages.
- Revisiting Content Pages: This study focused on collecting new pages, but it is also important to revisit important content pages during crawling to maintain the freshness of collected web pages. Existing studies have proposed importance measurement by PageRank [\(Page et al.,](#page-6-14) [1998\)](#page-6-14) or estimated future update frequencies based on each page's update frequency [\(Fetterly et al.,](#page-5-3) [2003\)](#page-5-3), but these approaches encounter a cold-start problem where it is difficult for them to handle new pages. A potential approach is to initially estimate the importance or future update frequencies of new pages using LLMs, and then adjust these estimates using PageRank or ac-

tual update frequencies after a certain period of time.

- Validation of Computational Cost: Since page classification with LLMs incurs a certain computational cost, it is necessary to verify whether the improvement in collection efficiency justifies the increase in computational costs.
- Lightweight LLMs: Further improvements in classification performance may not directly enhance coverage performance. Therefore, achieving sufficient classification performance with lightweight LLMs will be a key challenge.
- Practical evaluation: The evaluation in this study is limited to a small number of news websites, so it is necessary to conduct evaluations targeting a wider variety of websites. In addition, rather than evaluations using static snapshots of websites as in this study, evaluations in actual environments where website structures gradually change are also necessary.

### References

- <span id="page-5-0"></span>Paolo Boldi, Bruno Codenotti, Massimo Santini, and Sebastiano Vigna. 2004. [UbiCrawler: a scalable](https://doi.org/10.1002/spe.587) [fully distributed web crawler.](https://doi.org/10.1002/spe.587) *Softw. Pract. Exper.*, 34(8):711–726.
- <span id="page-5-4"></span>Guangyu Chen and Ben Choi. 2008. [Web page genre](https://doi.org/10.1145/1363686.1364247) [classification.](https://doi.org/10.1145/1363686.1364247) In *Proceedings of the 2008 ACM Symposium on Applied Computing*, SAC '08, page 2353–2357. Association for Computing Machinery.
- <span id="page-5-2"></span>Junghoo Cho and Hector Garcia-Molina. 2003. [Ef](https://doi.org/10.1145/958942.958945)[fective page refresh policies for web crawlers.](https://doi.org/10.1145/958942.958945) 28(4):390–426.
- <span id="page-5-5"></span>Valter Crescenzi, Giansalvatore Mecca, and Paolo Merialdo. 2001. [RoadRunner: Towards Automatic Data](https://dl.acm.org/doi/10.5555/645927.672370) [Extraction from Large Web Sites.](https://dl.acm.org/doi/10.5555/645927.672370) In *Proceedings of the 27th International Conference on Very Large Data Bases*, VLDB '01, page 109–118. Morgan Kaufmann Publishers Inc.
- <span id="page-5-1"></span>Jenny Edwards, Kevin McCurley, and John Tomlin. 2001. [An adaptive model for optimizing performance](https://doi.org/10.1145/371920.371960) [of an incremental web crawler.](https://doi.org/10.1145/371920.371960) In *Proceedings of the 10th International Conference on World Wide Web*, WWW '01, page 106–113. Association for Computing Machinery.
- <span id="page-5-3"></span>Dennis Fetterly, Mark Manasse, Marc Najork, and Janet Wiener. 2003. [A large-scale study of the evolution of](https://doi.org/10.1145/775152.775246) [web pages.](https://doi.org/10.1145/775152.775246) In *Proceedings of the 12th International Conference on World Wide Web*, WWW '03, page 669–678. Association for Computing Machinery.
- <span id="page-6-11"></span>Izzeddin Gur, Ofir Nachum, Yingjie Miao, Mustafa Safdari, Austin Huang, Aakanksha Chowdhery, Sharan Narang, Noah Fiedel, and Aleksandra Faust. 2023. [Understanding HTML with Large Language Mod](https://doi.org/10.18653/v1/2023.findings-emnlp.185)[els.](https://doi.org/10.18653/v1/2023.findings-emnlp.185) In *Findings of the Association for Computational Linguistics: EMNLP 2023*, pages 2803–2821. Association for Computational Linguistics.
- <span id="page-6-6"></span>Shuguang Han, Bernhard Brodowsky, Przemek Gajda, Sergey Novikov, Mike Bendersky, Marc Najork, Robin Dua, and Alexandrin Popescul. 2019. [Pre](https://doi.org/10.1145/3308558.3313694)[dictive Crawling for Commercial Web Content.](https://doi.org/10.1145/3308558.3313694) In *The World Wide Web Conference*, WWW '19, page 627–637. Association for Computing Machinery.
- <span id="page-6-1"></span>Allan Heydon and Marc Najork. 1999. [Mercator: A](https://doi.org/10.1023/A:1019213109274) [scalable, extensible Web crawler.](https://doi.org/10.1023/A:1019213109274) *World Wide Web*, 2(4):219–229.
- <span id="page-6-12"></span>Wenhao Huang, Zhouhong Gu, Chenghao Peng, Jiaqing Liang, Zhixu Li, Yanghua Xiao, Liqian Wen, and Zulong Chen. 2024. [AutoScraper: A Progressive Un](https://doi.org/10.18653/v1/2024.emnlp-main.141)[derstanding Web Agent for Web Scraper Generation.](https://doi.org/10.18653/v1/2024.emnlp-main.141) In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, pages 2371–2389. Association for Computational Linguistics.
- <span id="page-6-0"></span>Christopher Olston and Marc Najork. 2010. [Web Crawl](https://doi.org/10.1561/1500000017)[ing.](https://doi.org/10.1561/1500000017) *Foundations and Trends in Information Retrieval*, 4(3):175–246.
- <span id="page-6-8"></span>OpenAI, :, Aaron Hurst, Adam Lerer, Adam P. Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, and 1 others. 2024. [GPT-4o System Card.](https://arxiv.org/abs/2410.21276) *Preprint*, arXiv:2410.21276.
- <span id="page-6-14"></span>Lawrence Page, Sergey Brin, Rajeev Motwani, and Terry Winograd. 1998. [The PageRank Citation Rank](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.31.1768)[ing: Bringing Order to the Web.](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.31.1768) Technical report, Stanford Digital Library Technologies Project.
- <span id="page-6-2"></span>Gautam Pant, Padmini Srinivasan, and Filippo Menczer. 2004. [Crawling the Web.](https://doi.org/10.1007/978-3-662-10874-1_7) In *Web Dynamics: Adapting to Change in Content, Size, Topology and Use*, pages 153–177. Springer Berlin Heidelberg.
- <span id="page-6-7"></span>Xiaoguang Qi and Brian D. Davison. 2009. [Web page](https://doi.org/10.1145/1459352.1459357) [classification: Features and algorithms.](https://doi.org/10.1145/1459352.1459357) *ACM Comput. Surv.*, 41(2).
- <span id="page-6-10"></span>Fariza Rashid, Nishavi Ranaweera, Ben Doyle, and Suranga Seneviratne. 2025. [LLMs are one-shot URL](https://doi.org/10.1016/j.comnet.2024.111004) [classifiers and explainers.](https://doi.org/10.1016/j.comnet.2024.111004) *Comput. Netw.*, 258(C).
- <span id="page-6-3"></span>Uri Schonfeld and Narayanan Shivakumar. 2009. [Sitemaps: above and beyond the crawl of duty.](https://doi.org/10.1145/1526709.1526842) In *Proceedings of the 18th International Conference on World Wide Web*, WWW '09, page 991–1000. Association for Computing Machinery.
- <span id="page-6-4"></span>Space.com. 2025a. [NASA's Orion crew capsule had](https://www.space.com/space-exploration/nasa-orion-crew-capsule-had-heat-shield-issues-during-artemis-1-an-aerospace-expert-weighs-in-op-ed) [heat shield issues during Artemis 1 - an aerospace](https://www.space.com/space-exploration/nasa-orion-crew-capsule-had-heat-shield-issues-during-artemis-1-an-aerospace-expert-weighs-in-op-ed) [expert weighs in \(op-ed\).](https://www.space.com/space-exploration/nasa-orion-crew-capsule-had-heat-shield-issues-during-artemis-1-an-aerospace-expert-weighs-in-op-ed)

<span id="page-6-5"></span>Space.com. 2025b. [Technology.](https://www.space.com/technology)

<span id="page-6-9"></span>Tamas Voros, Sean Paul Bergeron, and Konstantin Berlin. 2023. [Web Content Filtering Through Knowl](https://doi.org/10.1109/WI-IAT59888.2023.00058)[edge Distillation of Large Language Models.](https://doi.org/10.1109/WI-IAT59888.2023.00058) In *2023 IEEE International Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT)*, pages 357–361. IEEE Computer Society.

# <span id="page-6-13"></span>A Experiments with the reconstructed dataset

The experimental results reported in this study were obtained using web pages collected around January 2025. To reinforce the validity of our experimental results, we recollected web pages from the same websites using breadth-first search starting from the home page around March 2025 and conducted the same experiments using the same procedures. Table [5](#page-7-0) shows the statistics of the reconstructed dataset, and Tables [6,](#page-7-1) [7,](#page-7-2) and [8](#page-7-3) show the experimental results. These results exhibit the same trends as the results reported in Section [3,](#page-2-3) indicating that our method is robust against changes in site structure and web page content over a certain period of time.

<span id="page-7-0"></span>

| Category   | Site Name            | #Index | #Content | #Total | #Latest 1 Day | #Latest 30 Days |
|------------|----------------------|--------|----------|--------|---------------|-----------------|
| Dev        | CNN                  | 2,216  | 7,784    | 10,000 | 171           | 1,709           |
|            | Variety              | 3,925  | 6,075    | 10,000 | 153           | 1,662           |
| Test       | TechCrunch           | 3,230  | 6,770    | 10,000 | 69            | 911             |
|            | Mongabay             | 3,918  | 6,082    | 10,000 | 16            | 217             |
|            | Space.com            | 2,549  | 7,451    | 10,000 | 19            | 307             |
| Noisy-Test | Entertainment Weekly | –      | –        | 10,000 | 75            | 942             |
|            | The New York Times   | –      | –        | 10,000 | 438           | 2,301           |
|            | MedicalNewsToday     | –      | –        | 10,000 | 14            | 144             |
|            | Healthline           | –      | –        | 10,000 | 19            | 307             |

Table 5: Data statistics of the reconstructed dataset.

<span id="page-7-1"></span>Table 6: Evaluation results of the page type classification performance on the reconstructed test set.

| Method      | Input        | Precision | Recall | F1    |
|-------------|--------------|-----------|--------|-------|
| All Pages   | –            | 0.323     | 1.000  | 0.486 |
| Rule-based  | –            | 0.680     | 0.834  | 0.749 |
|             | Title        | 0.989     | 0.561  | 0.716 |
| GPT-4o-mini | Title + Body | 0.991     | 0.513  | 0.649 |
|             | Title        | 0.977     | 0.652  | 0.777 |
| GPT-4o      | Title + Body | 0.982     | 0.734  | 0.837 |

Table 7: Evaluation results of coverage for new pages on the reconstructed test set.

<span id="page-7-2"></span>

| Method                  | Input        | Latest 1 Day |                   |             |       |        | Latest 30 Days |             |                         |       |        |         |
|-------------------------|--------------|--------------|-------------------|-------------|-------|--------|----------------|-------------|-------------------------|-------|--------|---------|
|                         |              | 10P          | 30P               | 100P        | 300P  | 1,000P | 10P            | 30P         | 100P                    | 300P  | 1,000P | Average |
| All Pages               | –            | 0.835        |                   | 0.844 0.864 | 0.931 | 0.968  | 0.461          | 0.551       | 0.685                   | 0.953 | 0.986  | 0.808   |
| Rule-based              | –            | 0.801        | 0.811             | 0.867       | 0.912 | 0.966  | 0.461          | 0.612       | 0.898                   | 0.978 | 0.995  | 0.830   |
| GPT-4o-mini             | Title        | 0.801        | 0.811             | 0.867       | 0.923 | 0.942  |                |             | 0.459 0.630 0.927 0.991 |       | 0.995  | 0.834   |
|                         | Title + Body | 0.702        | 0.702             | 0.888       | 0.923 | 0.942  | 0.418          |             | 0.552 0.941 0.974       |       | 0.994  | 0.803   |
| GPT-4o                  | Title        | 0.801        | 0.811             | 0.867       | 0.923 | 0.942  | 0.461          | 0.614       | 0.937                   | 0.988 | 0.995  | 0.834   |
|                         | Title + Body | 0.801        | 0.811             | 0.867       | 0.923 | 0.942  |                | 0.511 0.624 | 0.938                   | 0.988 | 0.995  | 0.840   |
| GPT-4o-mini + All Pages | Title        |              | 0.801 0.844       | 0.901       | 0.966 | 0.986  | 0.469          | 0.619       | 0.882                   | 0.974 | 0.995  | 0.844   |
| GPT-4o + All Pages      | Title + Body |              | 0.801 0.844 0.859 |             | 0.949 | 0.986  |                | 0.511 0.619 | 0.843                   | 0.984 | 0.995  | 0.839   |
| Gold Labels             | –            | 0.835        | 0.844             | 0.859       | 0.931 | 0.986  | 0.450          | 0.546       | 0.827                   | 0.985 | 0.996  | 0.826   |

Table 8: Evaluation results of coverage for new pages on the reconstructed noisy-test set.

<span id="page-7-3"></span>

| Method                  | Input        | Latest 1 Day |                   |                   |             |        | Latest 30 Days |                   |                   |       |        |         |
|-------------------------|--------------|--------------|-------------------|-------------------|-------------|--------|----------------|-------------------|-------------------|-------|--------|---------|
|                         |              | 10P          | 30P               | 100P              | 300P        | 1,000P | 10P            | 30P               | 100P              | 300P  | 1,000P | Average |
| All Pages               | –            | 0.374        | 0.398             |                   | 0.544 0.879 | 0.982  | 0.385          | 0.420             | 0.582 0.866       |       | 0.984  | 0.642   |
| Rule-based              | –            | 0.350        | 0.391             | 0.523             | 0.790       | 0.912  | 0.389 0.420    |                   | 0.585             | 0.844 | 0.938  | 0.614   |
| GPT-4o-mini             | Title        | 0.254        | 0.372             | 0.668             | 0.746       | 0.940  | 0.320          | 0.360             | 0.654             | 0.733 | 0.934  | 0.598   |
|                         | Title + Body | 0.253        | 0.340             | 0.671             | 0.699       | 0.954  | 0.379          | 0.452             | 0.738             | 0.768 | 0.939  | 0.619   |
| GPT-4o                  | Title        | 0.374        |                   | 0.398 0.689 0.784 |             | 0.958  |                | 0.385 0.470 0.742 |                   | 0.816 | 0.936  | 0.655   |
|                         | Title + Body | 0.374        | 0.398             | 0.671             | 0.766       | 0.961  | 0.385          |                   | 0.421 0.744 0.822 |       | 0.945  | 0.649   |
| GPT-4o-mini + All Pages | Title        |              | 0.374 0.406 0.687 |                   | 0.829       | 0.964  | 0.385          | 0.427             | 0.741             | 0.841 | 0.954  | 0.661   |
| GPT-4o + All Pages      | Title + Body | 0.374        |                   | 0.398 0.689 0.844 |             | 0.964  | 0.385          | 0.421             | 0.742             | 0.842 | 0.953  | 0.661   |