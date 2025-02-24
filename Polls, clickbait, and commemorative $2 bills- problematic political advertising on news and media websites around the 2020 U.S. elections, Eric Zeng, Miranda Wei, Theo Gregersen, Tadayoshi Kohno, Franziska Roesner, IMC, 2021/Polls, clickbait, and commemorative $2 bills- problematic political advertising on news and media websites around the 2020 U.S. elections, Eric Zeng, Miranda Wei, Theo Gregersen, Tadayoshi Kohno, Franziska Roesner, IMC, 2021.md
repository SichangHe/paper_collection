
## Ccs Concepts

- Information systems → Online advertising; - Social and professional topics → Computing / technology policy; - **Security**
and privacy → **Human and societal aspects of security and**
privacy.

1 INTRODUCTION
The 2020 United States general elections were among the most important and contentious elections in recent history. Issues facing the U.S. included the COVID-19 pandemic and ensuing economic crisis, controversy surrounding President Donald Trump's first term, and renewed movement for racial justice following the murder of George Floyd and other police violence. During this election season, online political advertising was more prominent than ever:

campaigns turned to online ads as the pandemic reduced in-person Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

IMC '21, November 2–4, 2021, Virtual Event, USA
© 2021 Copyright held by the owner/author(s). Publication rights licensed to ACM.

ACM ISBN 978-1-4503-9129-0/21/11. . . $15.00 https://doi.org/10.1145/3487552.3487850

```
         Polls, Clickbait, and Commemorative $2 Bills:
Problematic Political Advertising on News and Media Websites
                Around the 2020 U.S. Elections
       Eric Zeng, Miranda Wei, Theo Gregersen, Tadayoshi Kohno, Franziska Roesner
                                                        
                 Paul G. Allen School of Computer Science & Engineering
                                              
                         University of Washington
                                      
                           Seattle, WA, USA
                                    
                 {ericzeng,weimf,theoag,yoshi,franzi}@cs.washington.edu
                                              
ABSTRACT
Online advertising can be used to mislead, deceive, and manipulate
                              
Internet users, and political advertising is no exception. In this paper, we present a measurement study of online advertising around
                              
the 2020 United States elections, with a focus on identifying dark
                              
patterns and other potentially problematic content in political advertising. We scraped ad content on 745 news and media websites from
                              
six geographic locations in the U.S. from September 2020 to January
                              
2021, collecting 1.4 million ads. We perform a systematic qualitative
                              
analysis of political content in these ads, as well as a quantitative
                              
analysis of the distribution of political ads on different types of
                              
websites. Our findings reveal the widespread use of problematic
                              
tactics in political ads, such as bait-and-switch ads formatted as
                              
opinion polls to entice users to click, the use of political controversy
                              
by content farms for clickbait, and the more frequent occurrence
                              
of political ads on highly partisan news websites. We make policy
                              
recommendations for online political advertising, including greater
                              
scrutiny of non-official political ads and comprehensive standards
                              
across advertising platforms.
             

events and canvassing [89], and spent record sums advertising on
                                                                
Google and Facebook [69]. The misuse of online ads in non-political
                                                                
contexts is a well-known problem, ranging from distasteful clickbait
                                                                
ads to outright scams and malware [47, 58, 95–97]. In this paper, we
                                                                
investigate misleading and manipulative tactics in online political
                                                                
advertising, for purposes such as collecting email addresses and
                                                                
driving traffic to political content websites.
                                          
  We take a broad view of what constitutes a "political" ad in our
                                                                
work, considering any ad with political content, whether or not
                                                                
the ad was placed by an official political campaign committee. In
                                                                
our investigation, we ask: Who ran political ads during this period?
                                                                
What was the content of these ads, and do they use problematic
                                                                
techniques? Did the number of political ads on different types of
                                                                
websites differ?
               
To answer these questions, we conducted measurements of online advertising before, during, and after the Nov. 3rd elections. We
                                                                
collected a daily crawler-based sample of ads from 745 online news
                                                                
and media websites from September 2020 to January 2021, providing insight into the ads people saw while reading news during this
                                                                
period. We continued collecting data through several post-election
                                                                
developments: contested vote counting in multiple states, the Georgia U.S. Senate runoff election on January 5, and the attack on the
                                                                
U.S. Capitol on January 6. Our crawlers collected data from six
                                                                
locations with varying political contestation: Atlanta, GA; Miami,
                                                                
FL; Raleigh, NC; Phoenix, AZ; Salt Lake City, UT; and Seattle, WA.
                                                                
  Using a combination of qualitative and quantitative techniques,
                                                                
we analyze the political ads in our dataset, including identifying
                                                                
examples of misleading and manipulative techniques, the distribution of political ads across websites of different political biases, and
                                                                
political affiliations and organization types of the advertisers.
                                                           

Scope. Our crawler-based dataset provides a complementary perspective to the political ad archives from Google and Facebook.
                                                                    
Though our dataset is not as complete as the political ad archives,
                                                                    
and partially overlaps Google's, our dataset encompasses all ads
on the pages we crawled - including non-political ads, politicalthemed ads were not officially classified as political and thus do not
                                                                    
appear in Google's archive, and ads served via ad networks outside
                                                                    
of Google Ads. Additionally, we capture the URL of the website that
                                                                    
each ad appeared on, allowing us to measure contextual targeting
                                                                    
of political ads on news and media websites.
                                              

```

Contributions. First, we characterize the quantity and content of online advertising longitudinally during the 2020 U.S. Presidential Election and shortly thereafter, and at scale.

```
   - We observe differences in the number of political ads in
     different geographical locations.
                                
   - We observe shifts in the quantity of political ads through the
     election, and the effects of political ad bans.
                                         
   - We characterize the topics of all online advertisements that
     we collected during this time period.
                                    
Through our qualitative analysis, we observed several problematic types of online political advertising, such as:
                                        
   - The use of misleading and manipulative patterns in political
     ads. For example, ads that purport to be political polls, but use
                                                      
     inflammatory framing, and appear to be used for gathering
                                                      
     email addresses.
                   
   - Political topics in clickbait and native advertising. These ads
     imitate the look of links to news articles, but link to external
                                                      
     sites. Headlines often imply controversy about candidates,
                                                      
     and may fuel disinformation.
                             
  We also find that problematic political ads are more common on
                                                      
partisan and low-quality news sites.
                             
   - More partisan websites have more political ads, on both ends
     of the political spectrum.
                          
   - Problematic categories of ads, such as political products and
     polls, appear more frequently on right-leaning sites.
                                                
  We discuss the potential harms from the problematic political ads
                                                      
we observed, and we make recommendations for platform policies,
                                                      
government regulation, and future research. We also release our
                                                      
full dataset of ads and metadata.
                          

```

## 2 Background And Related Work 2.1 The 2020-21 U.S. Elections And Ads

Between September 2020 and January 2021, the U.S. held a presidential election, congressional elections, and numerous state and local elections. In the presidential election, Joe Biden, a Democrat, and his running mate, Kamala Harris, ran against Donald Trump, the incumbent Republican president, and his running mate, Mike Pence [8]. We provide more historical background in Appendix A.

Before the election, tech companies faced mounting pressure to address concerns about political advertising spreading misinformation and causing other harms. Some companies had already banned political ads (Pinterest in 2018 [31], Twitter in 2019 [17]), at least in part due to revelations that Russian organizations had purchased political ads during the 2016 presidential election [41]. Google and Facebook allowed political ads in 2020, but implemented several short-term bans. Our dataset of display ads was likely impacted by Google's bans from Nov. 4 through Dec. 10 [25, 78], and again after the storming of the Capitol between Jan. 14 and Feb. 24 [26].

Still, political ads around the 2020-21 elections set new records for ad spending, with overall spending in the billions. On Facebook and Google alone, the Trump campaign spent $276 million and the Biden campaign spent $213 million [69].

## 2.2 Online Political And Problematic Ads

Prior work studies the online ad ecosystem from various perspectives. In the computer security and privacy community, researchers have often studied the privacy implications of online ads and the tracking enabling them (e.g., [9, 45, 59, 71, 75, 90]). In this work,

```
we focus on the content of ads and contextual targeting that may
                                                                
cause different ads to appear on different types of sites, rather than
                                                               
on the underlying privacy-invasive mechanisms.
                                               
  Recent work in computer science identifies types of problematic
                                                               
content in ads (e.g., clickbait, distasteful ads, misleading content,
                                                                
manipulative techniques) [96, 97], and types explicitly malicious ads
                                                               
(e.g., spreading malware) [47, 58, 67, 93, 95]. Online ads play a role
                                                               
in spreading mis/disinformation (e.g., during the 2016 and 2018 U.S.
                                                                
elections) [14, 21, 79, 80] as well as in monetizing mis/disinformation websites [15, 27, 40, 60]. Other work has shown that ads (e.g., on
                                                               
Facebook) may be targeted in discriminatory ways [2, 43]. Studies of
                                                               
misleading and manipulative patterns (often called "dark patterns")
                                                                
beyond ads also inform our work (e.g., [51, 57]), particularly a recent
                                                               
study of such patterns in political campaign emails [52].
                                                      
Significant work in other fields (e.g., political science and marketing) also studies political ads. Kim et al. identified political ads
                                                               
on Facebook purchased by "suspicious" groups, including Russian
                                                               
groups known for spreading disinformation [41]. Stromer-Galley
                                                                
et al. [85] studied U.S. political ads on Facebook in 2016 and 2020,
                                                                
while Ballard et al. [7] characterized political campaign web display
                                                                
ads during the 2012 U.S. elections. Other work considered deceptive
                                                               
political advertising, (not necessarily online) including deceptively
                                                                
formatted "native" ads (e.g., [18, 55]). Van Steenburg provides a
                                                               
systematic literature review of political advertising research and
                                                               
proposes a research agenda, identifying the study of the impact of
                                                               
technology (i.e., the internet) as one key theme and area for future
                                                               
work (but does not discuss the manipulative patterns or non-official
                                                               
political ads that we see in our dataset) [84].
                                           
  Our work considers ads appearing on websites rather than social
                                                               
media, and we capture all ads (not only those marked as political
                                                               
ads). Prior work has found that Facebook's ad archives are incomplete and use a limited definition of "political" [20, 21, 81]. Indeed,
                                                                
we found many ads that contained political themes but were not
                                                               
placed by an official campaign.
                              

3 METHODOLOGY
In this section, we describe our methodology for measuring ads
                              
throughout the 2020 U.S. elections. In summary, we selected a group
                              
of popular mainstream and alternative news websites and scraped
                              
ads from these sites using crawlers in different locations. We collected 1.4 million ads in total from September 2020 to January 2021.
                              
We analyzed the content of our ads dataset using a combination
                              
of natural language processing, to automate tasks like identifying
                              
which ads were political, and manual qualitative analysis techniques, to provide greater context such as the party affiliation of
                              
the advertiser. See Figure 1 for a summary of our analysis pipeline.
                              

```

## 3.1 Ad Crawling

3.1.1 Seed Websites. To collect ads, we crawled news and media websites that spanned the political spectrum and information ecosystem. We identified 6,144 mainstream news websites in the Tranco Top 1 million [44], using categories provided by the Alexa Web Information Service [4]. These mainstream sites included national newspapers, local newspapers, TV stations, and online digital media. We also compiled a list of 1,344 websites which we refer to as "misinformation websites". Websites in this list were identified as

![2_image_0.png](2_image_0.png)

Figure 1: Overview of our analysis methodology. We used NLP techniques to preprocess and organize our dataset, and then conducted manual content analyses to explore political ads in greater detail, and to validate automated outputs. Blue boxes represent data, green boxes represent automated processes, and red boxes represent manual and qualitative analyses.

| Site Bias                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | # Sites   | Examples   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|------------|
| Mainstream News and Media Websites Left 63 jezebel.com, salon.com Lean Left 57 miamiherald.com, theatlantic.com Center 46 npr.org, realclearpolitics.com Lean Right 18 foxnews.com, nypost.com Right 44 dailysurge.com, thefederalist.com Uncategorized 376 adweek.com, nbc.com News Websites Labeled as Misinformation Left 13 alternet.org, dailykos.com Lean Left 6 greenpeace.org, iflscience.com Center 1 rferl.org Lean right 11 rt.com, newsmax.com Right 60 breitbart.com, infowars.com Uncategorized 50 globalresearch.ca, vaxxter.com |           |            |
| Table 1: Summary of our seed sites, by misinformation label                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |           |            |

```
"fake news", alternative news, mis/disinformation, highly partisan,
                                                                   
propaganda, or conspiracy websites by fact checkers (Politifact [83],
                                                                   
Snopes [42], Media Bias/Fact Check [54], and others [23, 36, 61]).
                                                                 
   To ensure that our crawlers could complete the crawl list in one
                                                                  
day, we truncated the list to 745 sites by picking all sites with a
                                                                  
ranking higher than 5,000 (411 sites), and then sampling from the
                                                                  
remaining tail (334 sites) by choosing 1 site per bucket of 10,000
                                                                  
site rank, to ensure that lower ranked sites were represented. In
                                                                  
Table 1, we show the number of sites in our crawl list by misinformation label and political bias. The political bias of websites were
                                                                  
aggregated from Media Bias/Fact Check [54] and AllSides [3].
                                                              
3.1.2 Crawler Implementation. We built a web crawler to scrape
ads based on Puppeteer [28], a Chromium-based browser automation library. Each crawler node crawls the seed list once per day,
                                                                   
crawling 6 domains in parallel in random order. For each seed domain, the crawler loads the root page and detects ads using CSS
                                                                  
selectors from EasyList [19], a filter list used by ad blockers. Elements smaller than 10 pixels in width or height (like tracking pixels)
                                                                  
were ignored. The crawler scrolls to each ad, takes a screenshot,
                                                                   
and collects the HTML content. Then, the crawler clicks the ad,
                                                                   

and collects the URL and content of the landing page. Because ads
                                                                 
may differ on site homepage vs. subpages, for each seed domain,
                                                                 
the crawler also visits and collects ads from an article on the site.
                                                                
To minimize behavioral ad targeting, we crawled each seed domain using a clean browser profile (similar to prior work [96]). For
                                                                 
each domain we visited, we ran separate browser instances inside
                                                                 
a new Docker container, so that no tracking cookies or other state
                                                                 
persisted across domains (though fingerprinting may be possible).
                                                                 
3.1.3 Crawler Nodes and Locations. We crawled ads using 4 nodes
from geographical locations where we predicted the political landscape could result in different ads.
                                 
    - Sep. 25, 2020 - Nov. 12, 2020: We first crawled from two cities
      in states predicted to be contested (Miami, FL; Raleigh, NC)
                                                                 
      and two uncompetitive (Seattle, WA; Salt Lake City, UT).
                                                              
    - Nov. 13, 2020 - Dec. 8, 2020: Due to contested election results,
      we switched two crawlers to Phoenix, AZ and Atlanta, GA.
                                                                 
      The other two crawlers alternated between the 4 previous
                                                                 
      locations (Seattle, Salt Lake City, Miami, Raleigh).
                                                       
    - Dec. 9, 2020 - Jan. 19, 2021: After the presidential election
      was resolved, we crawled from Atlanta, GA and Seattle, WA
                                                                 
      to observe the Georgia special election. Due to the Capitol
                                                                 
      insurrection, we continued crawling for 2 weeks.
                                                       
  To simulate crawling from these locations, we tunneled our
                                                                 
traffic through the Mullvad VPN service. Mullvad's VPN servers
                                                                 
ran on rented servers in local data centers (100TB, Tzulo, and M247).
                                                                 
We verified that the VPN servers were located in the advertised
                                                                 
locations using commercial IP geolocation services.
                                                   
  In sum, we ran 312 daily crawls, on 4 machines, using Chromium
                                                                 
88.0.4298.0, on a Debian 9 Docker image. The hardware was: Intel
                                                                 
Core i7-4790 3.6GHz 32GB RAM, Intel Core i7-7740X 4.3 GHz 64GB
                                                                 
RAM, and Intel Core i5-6600 3.30GHz, 16GB RAM (2x).
                                                      
3.1.4 Data Collection Errors. No data was collected globally from
10/23–10/27 (VPN subscription lapsed), nor 12/16–12/29 and 1/15–
                                                                 
1/19 in Seattle (VPN server outage). Some individual crawls also
                                                                 
sporadically failed. In total, 33 of 312 daily crawl jobs failed.
                                                           

![2_image_1.png](2_image_1.png)

```

## 3.2 Preprocessing Ad Content

3.2.1 Extracting Text from Ads. To enable large-scale analysis of the content of our dataset, we extracted the text of each ad. For

```
ads where 100% of the visual content is contained in an image,
                                                              
we used the Google Cloud Vision API to perform optical character
                                                             
recognition (OCR). We extracted text from 877,727 image ads (62.6%)
                                                             
using this method. For native ads (i.e., sponsored content headlines),
                                                              
the text is contained in the HTML markup, so we automatically
                                                             
extracted the text from these ads using JavaScript. We extracted
                                                             
text from 524,518 native ads (37.4%) using this method.
                                                   
3.2.2 Ad Deduplication. Many ads in our dataset appeared multiple times, some appearing tens of thousands of times. To reduce
                                                             
redundancy during qualitative coding and the runtime of machine
                                                             
learning tasks, we de-duplicated ads using the extracted text. We
                                                             
grouped our dataset by the domain of the landing page of the ad,
                                                              
and for each group, we used MinHash-Locality Sensitive Hashing1
(LSH) to identify ads with a Jaccard similarity > 0.5. We maintained
                                                             
a mapping of unique ads to their duplicates, which we used later
                                                             
to propagate qualitative labels for unique ads to their duplicates,
                                                              
enabling analysis of the whole dataset. After deduplication, we
                                                             
obtained a subset of 169,751 unique ads.
                                     

3.3 Analyzing Ad Content with Topic Modeling
To help us broadly understand the content of the ads in our dataset,
                                            
we used topic modeling to automatically create groups of semantically similar ads, allowing us to qualitatively analyze those groups.
                                            
We experimented with several topic modeling and text clustering
                                            
algorithms, and selected Gibbs-Sampling Dirichlet Mixture Model
                                            
(GSDMM) [94], which performed best on our dataset (see our experimental methodology in Appendix B). Second, we automatically
                                            
generated qualitative descriptions of each ad cluster, by using c-tfidf to extract the most significant words from the text cluster [33].
                                            
We applied GSDMM & c-tf-idf to describe the topics in our overall
                                            
ads dataset (Sec. 4.3) and political product ads (Sec. 4.7).
                                     

3.4 Analyzing Political Ads In-Depth
Our main focus is the content of political ads in our dataset. We defined a political ad broadly: any ad with political content, whether or
                                             
not the advertiser was a political campaign. This includes ads with
                                             
incidental political content, such as ads for products incorporating
                                             
election imagery or ads promoting political news articles.
                                        
 Our analysis of political ads consisted of three phases. First, we
                                             
used machine learning to automatically identify political ads in our
                                             
overall ads dataset. Second, we manually labeled the attributes of
                                             
each political ad, such as the purpose of the ad, and the advertiser's
                                             
political affiliation. Lastly, we performed quantitative analyses of
                                             
the labeled political ad data.
                   
3.4.1 Political Ads Classifier. To analyze political ads, we first
needed to isolate political ads from the overall ads dataset. We
                                             
implemented a binary text classifier based on the BERT language
                                             
model, to classify our ads as political or non-political.
                                     
We started by generated a training set of political and nonpolitical ads by labeling a random sample of ads in our dataset,
                                              
obtaining 646 political ads and 1,937 non-political ads. We supplemented this data by crawling 1,000 political ads from the Google
                                             
political ad archive [30] to balance the classes. We implemented
                                             
1We used the MinHash LSH implementation from the datasketch Python library:
                                             
http://ekzhu.com/datasketch/lsh.html.
                    

```

the classifier by fine-tuning the DistilBERT model [76] for a binary classification task. We trained our model with a 52.5% / 22.5% / 25%

Train / Validation / Test split. Our model achieved an accuracy of 95.5%, and an 1 score of 0.9. We ran the classifier on our deduplicated dataset (169,751 unique ads) and it classified 8,836 unique ads as political (5.2%).

3.4.2 Qualitative Analysis of Political Ads. Next, we we qualitatively coded the 8,836 unique political ads in our dataset to build a systematic categorization of the ads' content and characteristics [74]. Prior work in computer science and political science has also analyzed ad content using qualitative coding [85, 96]. We describe the development of our qualitative codebook and coding methods in detail in Appendix C.

Codebook Summary. We describe the high level categories of our codebook; a full list of subcodes is presented in Table 2, and a full set of definitions in Appendix C. We identified three mutually exclusive categories at the top level. **(1) Campaigns and Advocacy** ads explicitly addressed a political candidate, election, policy, or call to action. We further coded the Election Level, *Ad Purpose*,
Political Affiliation, and *Organization Type*. We coded Election Level based on the level of government, and Purpose based on the desired action in the ad. We coded Organization Type by first identifying the advertiser, using "Paid for By..." labels and the landing page content, and then looking up the legal registration of the advertiser. We coded Affiliation if the advertiser was officially associated with a political party, or indicated alignment with words such as

"conservative". We were able to attribute an organization type and advertiser affiliation for 96.5% of the campaigns and advocacy ads.

(2) Political News and Media ads promoted political news articles, videos, news sources, or events. We further demarcated two subcategories. *Sponsored Articles / Direct Links to Articles* included ads which promoted a specific article or piece of content. News Outlets, Programs, Events, and Related Media contained all other types of political news and media. **(3) Political Products** ads centered on selling a product or service by using political imagery or content.

We labeled political product ads as either *Political Memorabilia*,
Nonpolitical Products Using Political Topics, or *Political Services*. Ads were labeled as **(4) Malformed/Not Political** if the classifier identified the ad as political, but the content was occluded, incorrectly cropped, or contained multiple ads, in a way that made it impossible to analyze the ad. False positives (ads incorrectly labeled as political by the classifier) were also given this label.

```
3.5 Ethics
Our data collection method had two types of impacts on the web.
                                           
First, our crawler visited web pages and scraped their content. We
                                           
believe this had a minimal impact: all sites we visited were publicfacing content websites, contained no user data, and were visited
                                           
by our crawlers no more than 4 times per day.
                              
 Second, our crawler clicked on ads to scrape the landing page
                                           
of the ads. By clicking on the ads, we may cause the advertiser
                                           
to be charged for the clickthrough (unless our click is detected as
                                           
illegitimate), which is paid to the website and various middlemen.
                                           
 We determined that clicking on ads was necessary because it
                                           
was the only way for us to obtain the content and URL of the

landing page for each ad. Many ads obscure their landing page
                                                             
through nested iframes and redirect chains. This data was needed
                                                             
for automatically determining the identity of the advertiser and for
                                                             
manually investigating the landing pages during qualitative coding
                                                             
(when the ad itself did not have sufficient context).
                                               
  It is difficult to estimate the costs incurred to advertisers as a
                                                             
result of our crawls, but we believe the amount was low enough to
                                                             
be inconsequential. We cannot precisely determine the cost because
                                                             
the bid for each ad is not visible, and we do not know if advertisers
                                                             
pay using a cost-per-impression model or cost-per click model. For
                                                             
advertisers who pay based on impressions, we estimate the amount
                                                             
charged to be $3.00 per thousand impressions [87]. If all advertisers
                                                             
paid by impression, we estimate the total cost to all advertisers to be
approximately $4,200. For the average advertiser, the mean number
                                                             
of ads we crawled was 63, and the median was 3, resulting in a mean
                                                             
cost of $0.19, and median cost of $0.009. If advertisers instead paid
                                                             
per click, we estimate a cost of approximately $0.60 per click [39]: in
                                                             
this case, the the mean advertiser would have been charged $37.80,
                                                             
and the median would have paid $1.80. The outlier advertisers
                                                             
in our dataset who received the most clicks were predominantly
                                                             
intermediary entities, such as Zergnet (36k ads), mysearches.net
                                                             
(26k ads), and comparisons.org (9k ads). These intermediaries place
                                                             
ads on other websites on behalf of advertisers on their platform,
                                                             
meaning that costs incurred for these intermediaries were spread
                                                             
among many individual sub-advertisers.
                                     
  Stepping back, as we discuss further in Section 5, because of the
                                                             
distributed nature of the web ad ecosystem and the complex incentives of different stakeholders, we believe it is critical that external
                                                             
audits investigate the content and practices in this ecosystem, as
                                                             
we do in this study. Towards that end, we believe that the (small)
                                                             
costs of our study were justified. It is only through the process of
                                                             
clicking on ads, and evaluating the resulting landing pages, that can
                                                             
one fully understand the impact to users if they were to click on
                                                             
the ads. This is akin to the observation that malware websites may
                                                             
be linked from ads, potentially requiring search engine companies
                                                             
aiming to develop lists of known malware sites to engineer their
                                                             
crawlers to click on ads [63]. Moreover, similar methodologies have
                                                             
been used in prior works studying ads [67, 93].
                                           

```

## 3.6 Limitations

Our crawling methodology provided an incomplete sample of political advertising on the web. Our crawlers only visited a finite set of news and media websites, excluding other places that political ads appear, e.g., Facebook. Because we only visited each site once, we only saw a fraction of all ad campaigns running at that time. Our crawlers also only see political ad campaigns that were served to them - ongoing political ad campaigns may not have been shown to the crawler e.g. because of targeting parameters. We may have failed to load landing pages for ads because of detection and exclusion of our crawler by ad platforms. Due to VPN outages and crawler bugs, some days are missing from the data (Sec. 3.1.4).

We relied on categorizations from the fact checkers AllSides [3]

and Media Bias/Fact Check [54] to identify the political bias of our input websites. 42% of our input sites had a rating: some uncategorized sites were non-political news websites (e.g., espn.com), while others may not have been popular enough to be rated.

```
  Our automated content analyses were based on text extracted
                                                             
with OCR and did not use visual context from images. Some ads
                                                             
contained text artifacts, which negatively impacted downstream
                                                             
analyses. Based on the sample we labeled, we estimate that 18%
                                                             
ads in our dataset were malformed, i.e., impossible to read the
                                                             
ad's content. This was typically caused by modal dialogs (such as
                                                             
newsletter signup prompts) occluding the ad, which are difficult to
                                                             
automatically and consistently dismiss.
                                    
  For the majority of ads, our data did not allow us to identify
                                                             
the ad networks involved in serving the ads. Though our crawler
                                                             
collected the HTML content of each ad (including iframes), this
                                                             
alone was rarely sufficient to identify ad networks.
                                               
  Despite the above limitations, our dataset presents a unique and
                                                             
large-scale snapshot of political (and other) web ads surrounding
                                                             
the 2020 U.S. election. These include ads that do not appear in
                                                             
Google's (or others') political ad transparency reports. To support
                                                             
future research and auditing of this ecosystem, we will release our
                                                             
full dataset along with the publication of this paper, including ad
                                                             
and landing page screenshots, OCR data, and our qualitative labels.
                                                             

4 RESULTS
In this section, we present an analysis of the ads in our dataset. We
                                  
begin by providing an overview of the dataset as a whole, including:
                                  
How many ads appear overall, and how many of these are political
                                  
ads of different types (Sec. 4.1)? How did the number of ads (political
                                  
and non-political) change over time and location (Sec. 4.2)? Overall,
                                  
what ad topics were common (Sec. 4.3)?
                    
 Then, we dive more deeply into our analysis of political ads. We
                                  
investigate and characterize the sites political advertising appeared
                                  
on (Sec. 4.4), advertisers running official campaign and advocacy
                                  
ads (Sec. 4.5), misleading/manipulative campaign ads (Sec. 4.6), and
                                  
political product ads (Sec. 4.7) and news and media ads (Sec. 4.8).
                                 

4.1 Dataset Overview
Between September 26, 2020 and January 19, 2021, we collected
                                           
1,402,245 ads (169,751 unique ads) from 6 locations: Atlanta, Miami,
                                           
Phoenix, Raleigh, Salt Lake City, and Seattle. Our political ad classifier and qualitative coding, detected 67,501 ads (8,836 unique) with
                                           
political content, or 3.9% of the overall dataset. During our qualitative analysis of political ads, we removed 11,558 false positives and
                                           
malformed ads (3,201 unique), resulting in 55,943 political ads. In
                                           
Tab. 2, we show the number of political ads, across our qualitative
                                           
categories. About a third of ads were from political campaigns and
                                           
advocacy groups; over half advertised political news and media,
                                           
and the remainder political products.
                        

```

## 4.2 Longitudinal And Location Analysis

4.2.1 Ads Overall. We show the quantity of ads collected by location in Fig. 2a. The number of ads per day stayed relatively stable in each location: consistently around 5,000 ads per day. The stability in ad counts indicates that changes in demand for ad space before and after the election had little impact on websites' ad inventory.

We collected about 1,000 fewer ads per crawler day in Atlanta than other locations. We do not know if this was due to differences in location-based targeting or an artifact of our crawling (e.g.,

limitations of the Atlanta VPN provider).

![5_image_0.png](5_image_0.png)

(a) The number of ads collected in each crawler location. We collected a relatively constant number of ads for each location.

![5_image_1.png](5_image_1.png) (b) The number of political ads, classified as political by our text classifier, collected in each crawler location. The number of political ads was higher prior to the elections in November and January, were lower in the period after the elections.
Figure 2: Longitudinal graphs showing the number of total ads and political ads, collected in six locations from Sept. 2020 to Jan.

2021. Salient U.S. political events, as well as ad bans implemented by Google, are superimposed for context. Gaps from mid-Nov.

to mid-Dec. are because we scheduled crawls on nonconsecutive days. Other gaps are due to VPN outages (see Sec. 3.1.4).

```
4.2.2 Political Ads. The amount of political ads over time and
locations is visualized in Fig. 2b. Leading up to the presidential
                                                                 
election on Nov. 3, 2020, the number of ads per day in each location
                                                                 
increases from less than 250 to peaks of 450. After election day,
                                                                 
the number of political ads seen by crawlers sharply decreases, to
                                                                 
below 200 ads/day. This decrease could be a natural consequence
                                                                 
of less political attention following election day; it likely was also
                                                                 
due to Google's first ad ban, from Nov. 4 to Dec. 10. We believe
                                                                 
Google's ad bans help contextualize our results, given Google's
                                                                 
large presence in web ads - but because we did not determine the
                                                                 
ad networks used by each ad, we cannot prove a causal connection.
                                                                 
  During Google's first ban, we collected 18,079 political ads. 76%
                                                                 
of these ads were political news ads and political product ads. In the
                                                                 
4,274 campaign and advocacy ads during this period, 82% were from
                                                                 
nonprofits and unregistered groups, such as Daily Kos, UnitedVoice,
                                                                 
Judicial Watch, and ACLU. The remaining 18% (783 ads) were from
                                                                 
registered committees, some from candidates in special elections
                                                                 
(e.g., Luke Letlow, Raphael Warnock), but others from PAC groups
                                                                 
specifically referencing the contested Presidential election. For example, an ad from the Democratic-affiliated Progressive Turnout
                                                                 
Project PAC reads: "DEMAND TRUMP PEACEFULLY TRANSFER
                                                                 
POWER - SIGN NOW".
                       
  Google lifted their political ad ban on Dec. 11. At this time, we
                                                                 
only collected data from Seattle and Atlanta, and observed a rise
                                                                 
in the number of political ads per day in Atlanta until the Georgia
                                                                 
run-off election on Jan. 5, 2021, but no corresponding rise in Seattle.
                                                                 
The increase in Atlanta came almost entirely from Republicanaffiliated committees - Democratic-affiliated advertisers seem to
                                                                 
have bought very little online advertising for this election (Fig. 3).
                                                                
  Following the Georgia election, we again observed a sharp drop
                                                                 
in ads per day from the Atlanta crawler, matching the Seattle
                                                                 
crawler at less than 200 political ads per day.
                                            

```

Figure 3: Campaign ads observed in Atlanta in Dec 2020–Jan

![5_image_2.png](5_image_2.png)

2021, prior to the Georgia special elections. Almost all ads during this time period were run by Republican groups.
Though we observe that the volume of political advertising generally fell after elections, Google's ban on political advertising did not stop all political ads - other platforms in the display ad ecosystem still served political advertising.

```
4.3 Topics of Ads in Overall Dataset
To provide context before diving into political ads (Sec. 4.4-4.8), we
                                               
present results from a topic model of the entire dataset.
                                        
  Tab. 3 displays the 10 largest topics in the data, each with a
                                               
manually assigned topic description, the top c-TF-IDF terms, and
                                               
the number of ads assigned to the topic.
                            
  The largest topic regarded "enterprise" ads, e.g., a Salesforce ad to
                                               
"empower your partners to accelerate channel growth with external
                                               
apps." The second largest topic included "tabloid" ads, e.g., "the
                                               
untold truth of Arnold Schwarzenegger," as well as many clickbait
                                               
and native advertisements.

```

| Ad Categories                                                      | Count     | %    |
|--------------------------------------------------------------------|-----------|------|
| Political News and Media                                           | 29,409    | 52%  |
| Sponsored Articles                                                 | 25,103    | 45%  |
| News Outlets, Programs, Events                                     | 4,306     | 7%   |
| Campaigns and Advocacy                                             | 22,012    | 39%  |
| Level of Election Presidential                                     | 5,264     | 9%   |
| Federal                                                            | 5,058     | 9%   |
| State/Local (including initiatives/referenda)                      | 2,320     | 4%   |
| No Specific Election                                               | 2,150     | 4%   |
| None                                                               | 7,220     | 13%  |
| Purpose of Ad (not mutually exclusive) Promote Candidate or Policy | 10,923    | 20%  |
| Poll, Petition, or Survey                                          | 7,602     | 14%  |
| Voter Information                                                  | 4,145     | 7%   |
| Attack Opposition                                                  | 3,612     | 6%   |
| Fundraise                                                          | 2,513     | 4%   |
| Advertiser Affiliation Democratic Party                            | 5,108     | 9%   |
| Right/Conservative                                                 | 5,000     | 9%   |
| Republican Party                                                   | 4,626     | 8%   |
| Nonpartisan                                                        | 4,628     | 8%   |
| Liberal/Progressive                                                | 1,673     | 3%   |
| Unknown                                                            | 781       | 1%   |
| Independent                                                        | 172       | <1%  |
| Centrist                                                           | 24        | <1%  |
| Advertiser Organization Type Registered Political Committee        | 12,131    | 22%  |
| News Organization                                                  | 4,249     | 8%   |
| Nonprofit                                                          | 2,736     | 5%   |
| Business                                                           | 931       | 2%   |
| Unregistered Group                                                 | 913       | 2%   |
| Unknown                                                            | 781       | 1%   |
| Government Agency                                                  | 241       | <1%  |
| Polling Organization                                               | 30        | <1%  |
| Political Products                                                 | 4,522     | 8%   |
| Political Memorabilia                                              | 3,186     | 6%   |
| Nonpolitical Products Using Political Topics                       | 1,258     | 2%   |
| Political Services                                                 | 78        | <1%  |
| Political Ads Subtotal                                             | 55,943    | 100% |
| Political Ads - False Positives/Malformed                          | 11,558    |      |
| Non-Political Ads Subtotal                                         | 1,347,810 |      |
| Total                                                              | 1,402,245 |      |
| Table 2: Summary of the types of ads in our dataset.               |           |      |

Polls, Clickbait, and Commemorative $2 Bills: Problematic Political Advertising on News and Media Websites Around the 2020 U.S. Elections IMC '21, November 2–4, 2021, Virtual Event, USA

```
  The model's fourth largest topic, "politics", contained 71,240
                                                                
ads: a 64.8% overlap with the 55,943 political ads identified by our
                                                                
classifier and qualitative coding.
                               
These topics give us a sense of the context within which political ads were embedded. Like the web ad content studied in prior
                                                                
work [96, 97], political ads were surrounded by ordinary or legitimate ads for products and services, as well as low-quality and
                                                                
potentially problematic ads.
                           

```

## 4.4 Distribution Of Political Ads On Sites

Next, we examine how political ads were distributed across sites by political bias, misinformation label, and popularity.

```
   Political Bias of Site. Overall, we find that political ads appeared
more frequently on sites with stronger partisan bias. Fig. 4 shows
                                                                             
the fraction of ads that were political across websites' political
                                                                             
biases for mainstream and misinformation sites.
                                                        
   The percentages we calculate are the number of ads normalized
                                                                             
by the total number of ads collected from sites for each level of bias.
                                                                              
The number of ads collected from sites in each bias level varies, but
                                                                             
no group of sites had overwhelmingly more ads. From Left to Right,
                                                                             
the number of ads collected per site in each group were: 1,888, 1,950,
                                                                             
2,618, 2,092, and 2,172, and 1,676 had unknown bias.
                                                             
Two-sample Pearson Chi-squared tests indicate a significant association between the political bias of the site and the percentage of ads that were political, for both mainstream news sites
                                                                             
(
  
  2
   (5,  = 1150676) = 25393.62,  < .0001) and misinformation
sites (
        
         2
(5,  = 206559) = 8041.43,  < .0001). Pairwise comparisons using Pearson Chi-squared tests, corrected with Holm's
                                                                             
sequential Bonferroni procedure, indicate that all pairs of website
                                                                             
biases were significantly different ( < .0001).
                                                      
   On mainstream news sites, conservative sites had more political
                                                                             
ads than others; 9% and 10.3% of ads on right-leaning and right
                                                                             
sites were political, but only 6.9% and 4.4% of ads on left and leftleaning sites. On misinformation sites, 26% of ads on left sites were
                                                                             
political, substantially more than right leaning sites. In 4 of the 7
                                                                             
left misinformation sites (AlterNet, Daily Kos, Occupy Democrats,
                                                                             
Raw Story) over 19% of ads were political.
                                                 
We also find that political advertisers tend to target sites matching their political affiliation: Democratic and liberal groups ran
                                                                             
the majority of their ads on left-of-center sites, and likewise for
                                                                             
Republican and conservative groups on right-of-center sites (Fig. 5).
                                                                              
In particular, ads for Democratic political candidates and progressive nonprofits and causes ran substantially more on 2 of 7 Left
                                                                             
misinformation sites (Daily Kos and Occupy Democrats).
                                                                   
Two-sample Pearson Chi-squared tests indicate a significant association between the political bias of the site and the number of ads

```

| Topic                                          | c-Tf-IDF Terms                     | Ads       | %        |         |        |     |
|------------------------------------------------|------------------------------------|-----------|----------|---------|--------|-----|
| enterprise                                     | cloud, data, business, software,   | 93,475    | 6.7      |         |        |     |
| marketing                                      |                                    |           |          |         |        |     |
| tabloid                                        | look,                              | photo,    | star,    | upbeat, | 90,596 | 6.5 |
| celebrity, celeb, truth                        |                                    |           |          |         |        |     |
| health                                         | fungus, trick, fat, try, cbd, dog, | 73,240    | 5.2      |         |        |     |
| doctor, knee, tinnitus                         |                                    |           |          |         |        |     |
| politics                                       | vote, trump, biden, president,     | 71,240    | 5.1      |         |        |     |
| election, yes, sure                            |                                    |           |          |         |        |     |
| sponsored                                      | search, senior, yahoo, living,     | 70,613    | 5.0      |         |        |     |
| search                                         | car, might, visa                   |           |          |         |        |     |
| entertainment                                  | stream, original, music, watch,    | 50,248    | 3.6      |         |        |     |
| listen, tv, film                               |                                    |           |          |         |        |     |
| shopping                                       | boot,                              | shipping, | jewelry, | 49,457  | 3.5    |     |
| (goods)                                        | newchic, mattress, rug             |           |          |         |        |     |
| shopping                                       | friday, black, deal, sale, cyber,  | 45,022    | 3.2      |         |        |     |
| (deals/sales)                                  | review, monday                     |           |          |         |        |     |
| shopping                                       | 44,179                             | 3.2       |          |         |        |     |
| suv, luxury, phone, commonsearch, deal, net, auto                                                |                                    |           |          |         |        |     |
| (cars/tech) loans                              | loan, mortgage, payment, rate,     | 43,629    | 3.1      |         |        |     |
| apr, fix, nml                                  |                                    |           |          |         |        |     |
| Table 3: Top Topics in the Overall Ad Dataset. |                                    |           |          |         |        |     |

Figure 4: The percentage of ads, out of all ads on those sites, that were political, by sites' political bias and misinformation label. Higher percentages of ads on partisan sites were political, compared to centrist/uncategorized sites.

```
based on the advertiser's political affiliation, for both mainstream
                                                                    
news sites (
              
              2
               (25,  = 1, 150, 676) = 22575.49,  < .0001) and
misinformation sites (
                        
                        2
                         (20,  = 206, 559) = 22168.50,  < .0001).
Pairwise comparisons using Pearson Chi-squared tests, corrected
                                                                    
the Holm-Bonferroni method, indicate that all pairs of website biases were significantly different ( < .0001) except for the (Lean
                                                                    
Left, Uncategorized) Misinformation Sites.
                                           
Site Popularity. We found little relationship between site popularity and the number of political ads on it (Fig. 6). While sites
                                                                    
hosting many political ads tended to be popular politics sites (e.g.,
                                                                    
dailykos.com, mediaite.com), some popular sites (e.g., nytimes.com,
                                                                    
cnn.com) ran <100 political ads. A linear mixed model analysis of
                                                                    
variance indicates no statistically significant effect of site rank on
                                                                    
the number of political ads ( (1, 744) = 0.805, ..).
At a high level, we find that political ads are seen more on websites that are political and partisan in nature. We hypothesize that
                                                                    
this is either due to contextual targeting (political groups advertising to co-partisans), and/or because neutral news websites choose
                                                                    
to block political advertising on their sites to appear of impartiality.
                                                                    

4.5 Advertisers of Campaign Ads
Next, we analyze the advertisers who ran campaign and advocacy
                                            
ads: their organization type, their affiliations, and how many they
                                            
ran. Fig. 7 shows these ads by organization type and affiliation.
                                          
 Registered Committees. Most campaign ads (12,131, 55.1%) were
purchased by registered committees (FEC or state PACs). These ads
                                            
were roughly evenly split between Republican- and Democraticaffiliated committees, including official candidate committees, like
                                            
Biden for President, as well as Hybrid PACs and party-affiliated
                                            
Super PACs, such as the Progressive Turnout Project and the Trump
                                            
Make America Great Again Committee. These also include candidate committees for other state, local, and federal offices.
                                      
Nonprofits. We observed campaign ads from nonpartisan nonprofits, e.g., AARP (259 ads, 1.2%), ACLU (256 ads, 1.2%), as well
                                            
as explicitly conservative ones, e.g., Judicial Watch (504 ads, 2.3%),
                                            
Pro-Life Alliance (471 ads, 2.1%). Few explicitly liberal nonprofits
                                            
ran ads under our categorization system. However, some may consider self-described nonpartisan organizations as liberal, e.g., issue
                                            
organizations like the ACLU, or voting rights groups like vote.org.
                                            

```

![7_image_0.png](7_image_0.png)

![7_image_1.png](7_image_1.png)

Figure 5: The percentage of ads observed on websites from advertisers of different political affiliations, by the political bias and misinformation label of the website. Advertisers tended to run ads on websites aligned with their politics. ![7_image_2.png](7_image_2.png)

site, by the site's Tranco rank. Though the largest outliers in terms of political ads tend to be popular sites, many popular sites show few if any political ads.
News Organizations. Some news organizations ran explicitly political ads to promote candidates or policies - these were mostly conservative-leaning organizations. The top advertisers in this group are not well-known, e.g., ConservativeBuzz (1,199 ads, 5.4%),
Polls, Clickbait, and Commemorative $2 Bills:

![8_image_0.png](8_image_0.png) Problematic Political Advertising on News and Media Websites Around the 2020 U.S. Elections IMC '21, November 2–4, 2021, Virtual Event, USA

Figure 7: Campaign and advocacy ads by organization type of the advertiser, color-coded by the political affiliation of the advertiser. Ads from registered committees dominated, roughly evenly divided between Democratic and Republican ads, but ads from news organizations and nonprofits were more heavily conservative and nonpartisan respectively.

```
UnitedVoice.com (800 ads, 3.6%), and rightwing.org (393 ads, 1.8%).
                                                                   
ConservativeBuzz does not have a website, despite claiming to be a
                                                                  
news source on their landing page; UnitedVoice and rightwing.org
                                                                  
are ranked 248,997 and 539,506 on the Tranco Top 1m.
                                                       
  Other advertisers in this category are more well-known, e.g.,
                                                                  
Daily Kos, a liberal blog (690 ads, 3.1%, site rank 3,218); Human
                                                                  
Events, a conservative newspaper (390 ads, 1.8%, rank 19,311); Newsmax, a conservative news network (117 ads, 0.5%, rank 2,441).
                                                              
  Unregistered Groups. Unregistered groups ran a small number
of ads. The top advertiser was "Gone2Shit", a campaign from the
                                                                  
marketing firm MullenLowe, which ran 228 ads for a humorous
                                                                  
voter turnout campaign. The U.S. Concealed Carry Association ran
                                                                  
162 ads. Beyond these top two, a number of "astroturfing" groups or
                                                                  
other industry interest groups ran ads, such as "A Healthy Future"
                                                                   
(lobbying against price controls on Rx drugs), "Clean Fuel Washington", and "Texans for Affordable Rx" (a front for the Pharmaceutical
                                                                  
Care Management Association, based on investigating their website). Other top ads came from unregistered, left-leaning groups,
                                                                  
such as "Progress North" and "Opportunity Wisconsin", which describe themselves as grassroots movements. We also saw a small
                                                                  
number of groups consisting of coalitions of registered nonprofits, who collectively fund an ad campaign, such as "No Surprises:
                                                                   
People Against Unfair Medical Bills" and "votewith.us".
                                                        
  Businesses and Government Agencies. Some businesses, e.g., Levi's,
Absolut Vodka, ran political ads: mostly nonpartisan ads for voter
                                                                  
registration. State/local election boards also ran voter information
                                                                  
ads, e.g. the NYC Board of Elections.
                                    

```

## 4.6 Misleading Political Polls

Focusing now on the content of ads in our campaign and advocacy category, rather than the advertisers, we highlight the use of polls, petitions, and surveys, many of which appear to contain misleading content, and manipulate users into providing their email addresses.

The purpose of many online political petitions and polls are to allow political actors to harvest personal details like email addresses, so that they can solicit donations, canvas, or advertise to those people in the future [66]. This phenomenon is present in our dataset.

In a few cases (30 ads), ads we labeled as polls or petitions linked to nonpartisan public opinion polling firms such as YouGov and Civiqs, but most ads were from political groups, and had landing pages asking people to provide their email addresses.

Figure 8: The political affiliation and organization types of

![8_image_1.png](8_image_1.png)

poll/petition advertisers. These ads were primarily run by unaffiliated conservative advertisers, mostly news organizations and nonprofits.

```
  We observe that poll and petition ads are more common from
                                                            
politically conservative advertisers. In Fig. 8, we visualize the number of poll ads by the political affiliation of their advertisers. Nonaffiliated conservative groups (mostly news organizations and nonprofits) ran the highest number of poll and petition ads (3,960
                                                            
ads, 52% of total), followed by Republican party committees (1,389,
                                                            
18.2%). Democratic committees ran fewer poll ads than their Republican counterparts (1,027 ads, 13.5%), while non-partisans and
                                                            
nonaffiliated liberals rarely use poll ads (458 ads, 6%; 53 ads, 0.6%).
                                                            
  Poll ads also made up a greater proportion of ads on right-leaning
                                                            
websites than other sites: 2.2% on Right and 1.1% on right-leaning
                                                            
websites were polls and petitions, compared to 1.1% on Left, 0.2%
                                                            
on left-leaning, and 0.2% on center sites.
                                     
  Next, we describe several topics and manipulative tactics used
                                                            
by poll ads, which differ across political affiliations.
                                               
  Democratic-Affiliated Groups. Most poll or petition ads from
Democratic-affiliated groups were for highly partisan issue-based
                                                            
petitions, e.g., "Stand with Obama: Demand Congress Pass a Voteby-Mail Option", "Official Petition: Demand Amy Coney Barrett
                                                            
Resign - Add Your Name". However, some petitions used even more
                                                            
contrived scenarios, such as posing as a "thank you card" for important politicians (Fig. 9a). These ads were run by affiliated PACs
                                                            
rather than party or candidate committees, such as the National
                                                            
Democratic Training Committee (290 ads), Progressive Turnout
                                                            
Project (282 ads), and Democratic Strategy Institute (215 ads).

```

![9_image_0.png](9_image_0.png)

![9_image_1.png](9_image_1.png)

(a) (b) (c) (d)
Figure 9: Examples of political ads purporting to be polls, including from: a Democratic-aligned PAC (a), the Trump campaign
(b), a conservative news organization/email harvesting scheme (c), and a Republican-aligned PAC (d).

```
   Republican-Affiliated Groups. The Trump campaign ran 906 ads
with positive and neutral polls promoting President Trump and
                                                                   
479 ads with polls that attacked their opponent (e.g., Fig. 9b). Other
                                                                   
Republican committees, such as the NRCC, used the LockerDome ad
                                                                   
platform to run generic-looking polls not clearly labeled as political
                                                                   
(e.g., Fig. 9d). Moreover, Lockerdome was also used by unaffiliated
                                                                   
advertisers, e.g., "All Sears MD", rawconservativeopinions.com, to
                                                                   
run nearly identical-looking ads that were used to sell political
                                                                   
products; this homogenization makes it difficult for users to discern
                                                                   
the nature of such ads. We also found 5 Lockerdome ads from the
                                                                   
"Keep America Great Committee," whose operators turned out to
                                                                   
be using it to commit fraud and pocket donations [50].
                                                       

Conservative News Organizations. The largest subgroup of advertisers that used polls were right-leaning news organizations, such
                                                                
as such as ConservativeBuzz, UnitedVoice, and rightwing.org. Some
                                                                
polls use neutral language, e.g., "Who Won the First Presidential
                                                                
Debate?", while others used more provocative language, e.g., "Do
                                                                
Illegal Immigrants Deserve Unemployment Benefits?" (Fig. 9c).
                                                              
Journalistic investigations have found that advertisers like ConservativeBuzz purport to be conservative news organizations but
                                                                
are actually run by Republican-linked digital marketing firms. Appearing as news, many of their stories are plagiarized and/or serve
                                                                
a political agenda. Their misleading poll ads are an entry point for
                                                                
harvesting email addresses for their mailing lists. They profit from
                                                                
these mailing lists by sending ads to their subscribers, including
                                                                
ads from political campaigns [6, 49].
                                   
  Our data backs up these findings. We inspected poll ads from
                                                                
ConservativeBuzz, UnitedVoice, and rightwing.org, who comprise
                                                                
55% of poll ads from Right/Conservative advertisers, and 29% of
                                                                
poll ads overall. The landing pages of their ads often asked for an
                                                                
email address to submit poll responses (Appendix E). We looked
                                                                
up these advertisers in the Archive of Political Emails to see the
                                                                
content of the emails that they send to subscribers 2. We found that
                                                                
their emails often contained a mix of spam for various products
                                                                
(Subject: "This Toxic Vegetable Is The #1 Danger In Your Diet"),
                                                                 
biased or inaccurate political news (Subject: "Fauci-Obama-Wuhan
                                                                
Connection Exposed in This Bombshell Report"), or a combination
                                                                
of the two (Subject: "URGENT - Think Trump Won? You need to
                                                                
see this...", selling a Trump mug).
                                

```

2https://politicalemails.org/

```
4.7 Political Product Ads
We now consider ads in our dataset that used political content to
                                             
sell products, divided into three categories.
                             
4.7.1 Ads for Memorabilia. We observed 3,186 ads for political
memorabilia, including clothing with slogans, collectibles, and novelty items. These ads were placed by commercial businesses - none
                                             
were affiliated with political parties. Our GSDMM model produced
                                             
45 topics for political memorabilia ads; Tab. 4 shows the top seven.
                                             
 We observe that the majority of memorabilia ads are targeted
                                             
towards conservative consumers. 2,175 advertisements (68.3% of
                                             
memorabilia ads) contained "Donald" and/or "Trump". Seven of the
                                             
top ten topics are directly related to Trump, selling items such as
                                             
special edition $2 bills (Fig. 10a), electric lighters, garden gnomes,
                                             
and trading cards.
            
 Some memorabilia ads targeting conservatives used potentially
                                             
misleading practices. While some ads clearly advertised themselves
                                             
as products, others disguised the memorabilia as "free" items, but
                                             
requires payment to cover shipping and handling. Many ads did
                                             
not clearly disclose the name of the advertiser. Some straddled the
                                             
line between product ads and clickbait by making claims that the
                                             
product "angered Democrats" or would "melt snowflakes." We also
                                             
observed many collectible bills and coins, advertised as "Legal U.S.
                                             
Tender", by sellers such as Patriot Depot, making dramatic claims
                                             
like "Trump Supporters Get a Free $1000 Bill."
                               
 We observed far fewer ads for left-leaning consumers; the first
                                             
topic containing left-leaning products was the 15th largest at 71
                                             
ads. Ads targeting liberals include a pin for "flaming feminists" or
                                             
a deck of cards themed around the 2020 Senate Impeachment Trial
                                             
of former President Trump (Fig. 10b).
                         
4.7.2 Ads Using Political Context To Sell Something Else. We observed 1,258 ads that leveraged the political climate for their own
                                             
marketing. Some of these ads were from legitimate companies,
                                             
such as Capitol One advertising their alliance with the Black Economic Alliance to close opportunity gaps, or the Wall Street Journal promoting their market insight tools. However, many others
                                             
were from relatively unknown advertisers peddling get-quick-rich
                                             
schemes, like stocks that would "soar" from Biden winning the
                                             
election (Fig. 10c) or election-proof security in buying gold.
                                         
Our GSDMM model found 29 topics for ads categorized as nonpolitical products using political context. Tab. 5 details the largest 7
                                             
topics. The most prominent political contexts used for these topics
                                             
were Congress (e.g., legislation related to the product) and the 2020

```

Polls, Clickbait, and Commemorative $2 Bills: Problematic Political Advertising on News and Media Websites Around the 2020 U.S. Elections IMC '21, November 2–4, 2021, Virtual Event, USA

| Topic                                                        | Weighted c-TF-IDF Terms             | Ads     |        |        |     |
|--------------------------------------------------------------|-------------------------------------|---------|--------|--------|-----|
| Trump wristbands and                                         | America, charger, USB, butane,      | 643     |        |        |     |
| lighters                                                     | require, vote, include              |         |        |        |     |
| "free" Trump flags                                           | dems, hate, give, foxworthynews,    | 300     |        |        |     |
| away, claim, flag                                            |                                     |         |        |        |     |
| Trump electric lighters                                      | spark, instantly, generate, one,    | 253     |        |        |     |
| and garden deco                                              | click, open, light, garden          |         |        |        |     |
| $2 bills and "currency"                                      | legal, tender, authentic, official, | 186     |        |        |     |
| Donald, USA, make                                            | 172                                 |         |        |        |     |
| Israel support pins                                          | Israel, request, pin, Jew, fellowship, Christian                                     |         |        |        |     |
| Trump camo hats,                                             | camo, gray, anywhere, discreet,     | 156     |        |        |     |
| bracelets, and coolers                                       | go, sale, way, bracelet             |         |        |        |     |
| Trump coins and bills                                        | left, gold, coin, Democrat, upset,  | 133     |        |        |     |
| hat, supporter, value                                        |                                     |         |        |        |     |
| Table 4: Top Topics in Political Memorabilia Ads             |                                     |         |        |        |     |
| Topic (Context)                                              | Weighted c-TF-IDF Terms             | Ads     |        |        |     |
| Hearing devices (congress                                    | hearing,                            | aidion, | slash, | price, | 266 |
| action)                                                      | health, hear, act, sign, Trump      |         |        |        |     |
| Retirement finance                                           | sucker, punch, law, pension, even,  | 205     |        |        |     |
| (congress action)                                            | rob, retire, IRA                    |         |        |        |     |
| Investing (election-time)                                    | former, presidential, Stansberry,   | 123     |        |        |     |
| congressional, veteran                                       |                                     |         |        |        |     |
| Seniors' mortgage                                            | 97                                  |         |        |        |     |
| amount, reverse, senior, Steve, calculate, tap, age                                                              |                                     |         |        |        |     |
| (congress action) Banking (racial justice)                   | JPMorgan, Chase, advance, co,       | 66      |        |        |     |
| racial, important, equality                                  |                                     |         |        |        |     |
| Portfolio finance                                            | inauguration, money, Jan, wonder,   | 63      |        |        |     |
| (election-time)                                              | oxford, communique                  |         |        |        |     |
| Dating sites (for                                            | Republican, single, date, woman,    | 54      |        |        |     |
| Republicans)                                                 | wait, profile, view                 |         |        |        |     |
| Table 5: Top Topics in Ads About Nonpolitical Products Using |                                     |         |        |        |     |

Table 5: Top Topics in Ads About Nonpolitical Products Using

Political Context

election. Finance related topics in particular often cited market uncertainty around the election, e.g., referencing how a certain outcome might affect stocks and promoting their product as a hedge or chance to capitalize. Notably, three of the top four topics targeted older audiences: "hearing devices," "retirement finance," and

"seniors' mortgage."

4.7.3 Where did political product ads appear? We find that political product ads appeared much more frequently on right-of-center websites (Fig. 11). This finding aligns with the qualitative content that we observed in these ads - a large amount of Trump memorabilia, and "scare" headlines about the election outcome. Two-sample Pearson Chi-Squared tests indicate a statistically significant association between the political bias of the site and the number of political product ads observed, both for mainstream news sites

(

2
(10,  = 1, 150, 676) = 4871.97,  < .0001) and misinformation sites (

2
(8,  = 206, 559) = 414.75,  < .0001). Pairwise comparisons using Pearson Chi-squared tests, corrected with the HolmBonferroni method, indicate that all pairs of website biases were significantly different ( < .0001), except for the following pairs on misinformation sites: (Lean Left, Lean Right), (Lean Left, Left), and

(Lean Left, Uncategorized).

![10_image_0.png](10_image_0.png)

(c)
Figure 10: Examples of political product ads, including those

![10_image_1.png](10_image_1.png)

selling memorabilia (a-b) and those using the political context to sell something else (c).
Figure 11: The percentage of ads observed that were for political products, by the political bias of the site. Right sites more frequently hosted ads for political products, both on misinformation and mainstream sites, and both for memorabilia or nonpolitical products using political contexts.

```
4.8 Political News and Media Ads
We observed 29,409 ads that were related to political news and media content. At 52.0% of all political ads, this was the most populous
                                            
category and accounted for more than either of the other two categories. Unlike the product ads primarily selling goods or services,
                                            
these ads advertised information or information-related services.
                                            
We categorize these news and media ads into two groups: those that
                                            
advertised specific political news articles, and those that advertised
                                            
political outlets, events, or related media. Article ads contained a
                                            
range of sensationalized, vacuous, or otherwise misleading content,
                                            
especially with "clickbait-y" language that enticed people to click.
                                            
4.8.1 Sponsored Content / Direct Article Links. Overall, we find
that most political news and media ads were sponsored content
                                            
or links to articles (25,103 ads, 85.4%). Some of these ads reported
                                            
substantive content, e.g., linking to a review of a documentary:
                                            
"'All In: The Fight for Democracy' Tackles the Myth of Widespread
                                            
Voter Fraud." Others were clickbait only using political themes for
                                            
attention, e.g., "Tech Guru Makes Massive 2020 Election Prediction."
                                            
  Misleading Ads and Headlines. Given that our ads were primarily
scraped from news and media websites, many appeared as native

```

Figure 12: Number of ads including first and last names of the 2020 presidential and VP candidates.

```
ads that blend into the other content, albeit with an inconspicuous
                                                                   
"Sponsored content" or similar label. Further, the headline shown
                                                                   
in a political article ad did not always align with the actual content
                                                                   
on the clickthrough page. For example, the ad shown in Fig. 13a
                                                                   
links (via a Zergnet aggregation page) to an article3that recounts
                                                                   
Vanessa Trump's life before marrying Donald Trump Jr., instead
                                                                   
of after, as the title suggests. Many Zergnet ads with headlines
                                                                   
implying controversy were unsubstantiated by the linked article.
                                                                  
   Ads Mentioning Top Politicians. Overall, Trump and Biden were
referenced in ads much more often than Pence and Harris (Fig. 12).
                                                                   
Within political news and media ads, "Trump" is referenced in ads
                                                                   
2.5x more than "Biden" (11,956 ads vs. 4,691, or 40.7% vs. 16.0%),
                                                                   
even even after the election. Eight of the top ten ads mentioning
                                                                   
Trump actually involve his family: e.g., "Trump's Bizarre Comment
                                                                   
About Son Barron is Turning Heads" (1,377 ads, 4.7%), or "Eric
                                                                   
Trump Deletes Tweet After Savage Reminder About His Father"
                                                                   
(415 ads, 1.4%). The top 10 ads mentioning Biden imply scandals
                                                                   
with his wife, e.g., Fig. 13b (1,267 ads, 4.3%), and his health, e.g., "ExWhite House Physician Makes Bold Claim About Biden's Health"
                                                                   
(423 ads, 1.4%).
               
Looking at the VP candidates, Pence is referenced in ads frequently during the run up to the election and immediately following the insurrection at the Capital, while a spike in the mentions of
                                                                   
Harris occurs in late November and early December. Some of the
                                                                   
top 10 ads mentioning Pence connect him to high-profile events, including the VP debate ("The Pence Quote from the VP Debate That
                                                                   
Has People Talking," 143 ads, 0.5%) and the U.S. Capitol storming
                                                                   
(Fig. 13c). Some of the top 10 ads mentioning Harris highlight her
                                                                   
ex ("Why Kamala Harris' Ex Doesn't Think She Should Be Biden's
                                                                   
VP," 246 ads, 0.8%) as well as her gender ("Women's Groups Are
                                                                   
Already Reacting Strongly to Kamala," 51 ads, 0.2%).
                                                     
   Frequent Re-Appearances of Sponsored Content. Out of 25,103
political article ads, we counted only 2,313 unique ads, meaning
                                                                   
that many political article ads were shown to our crawler multiple
                                                                   
times. On average, a single (unique) political article ad appeared
                                                                   
to our crawlers 9.9 times, compared to 9.3 times for campaign
                                                                   
ads and 5.1 times for product ads. The frequent re-appearance of
                                                                   
political article ads is likely an artifact of content farms' practice of
                                                                   
3https://www.thelist.com/161249/the-stunning-transformation-of-vanessa-trump/
                                                                 

```

![11_image_1.png](11_image_1.png)

![11_image_0.png](11_image_0.png)

Figure 13: Political news and media articles.

```
producing high quantities of low-quality articles solely for revenue
                                                                    
from clicks [12]. 79.4% of all political news articles were run by
                                                                    
Zergnet, which accounted for 19,690 ads and only 1,388 unique
                                                                    
ads. Other top ad platforms for political news articles were Taboola
                                                                    
(10.0%), Revcontent (5.7%), and Content.ad (1.8%).
                                                   
4.8.2 Political Outlets, Programs, Events, and Related Media. A
small portion of political ads, just 4,306 (7%), advertised a political news outlet, event, or other media content. This includes ads
                                                                    
run by well-known news organizations, e.g., Fox News, The Wall
                                                                    
Street Journal, The Washington Post, that advertised their organizations at large, as well as highlighting specific events, such as
                                                                    
CBS's coverage of the "Assault on the Capitol" (Appendix E), or
                                                                    
special programs about the presidential election. Ads were also run
                                                                    
by less-well known news organizations advertising themselves or
                                                                    
their events, e.g., The Daily Caller, a right-wing news and opinion
                                                                    
site, or advocacy groups and nonprofits, e.g., Faith and Freedom
                                                                    
Coalition (Appendix E), a conservative 501(c)(4). We also observed
                                                                    
ads about books, podcasts, movies, and more.
                                               
4.8.3 Where did political news and media ads appear? Political
news and media ads appeared more often on right-of-center sites,
                                                                    
compared to center and left-of-center sites (Fig. 14). Two-sample
                                                                    
Pearson Chi-Squared tests indicate a statistically significant association between the political bias of the site and the number
                                                                    
of political news and media ads, both for mainstream news sites
                                                                    
(
  
  2
(10,  = 1, 150, 676) = 16729.34,  < .0001) and misinformation sites (
            
             2
              (8,  = 206, 559) = 3985.43,  < .0001). Pairwise
comparisons using Pearson Chi-squared tests, corrected with the
                                                                    
Holm-Bonferroni method, indicate that all pairs of website biases
                                                                    
were significantly different ( < .0001). Nearly 5% of ads on both
                                                                    
Right and Lean-Right sites are sponsored content, but only 3.9%,
                                                                    
2.2%, and 0.8% on Left, Lean Left, and Center sites.
                                                    

```

## 5 Discussion 5.1 Concerns About Problematic Political Ads

Our investigation adds to a growing body of work studying potentially problematic content in online ads, political and otherwise

(see Sec. 2). Here, we discuss further the potential harms from the problematic political ads we found.

Manipulative Polls. The most common manipulative pattern we observed in our political ads was the poll-style ad. We view these ads as problematic for two reasons. First, they manipulate people into

![12_image_0.png](12_image_0.png)

Figure 14: The number of political news ads observed per site, by the political bias of the site. Right sites more frequently host political news ads than others.

```
clicking on ads by appealing to political motivations with (seemingly) clickable user interface elements. Second, once users click,
                                                                                                                                  
they often ask users to provide personal information for further manipulation, e.g., to put them on manipulative email newsletters [52].
                                                                                                                                   
     Political Clickbait. We observed attention-grabbing news and
media ads that were not official political ads and thus do not appear in political ad transparency libraries. However, these ads are
                                                                                                                                  
misleading: they are often designed to looks like real news articles, but the political controversies they imply (e.g., "Viral Video
                                                                                                                                  
Exposes Something Fishy in Biden's Speeches," Figs. 13a-13c) are
                                                                                                                                  
not usually substantiated by the underlying articles. Though we
                                                                                                                                  
believe these ads' goal is to entice clicks for ad revenue, we worry
                                                                                                                                  
that the provocative political "headlines" contribute to a climate
                                                                                                                                  
of hyper-partisan political communication and muddy the information ecosystem to which voters are exposed. We argue that this
                                                                                                                                  
type of political-adjacent advertising requires additional scrutiny
                                                                                                                                  
from ad platforms and the public.
                                                                  
     Exploitative Product Ads. Most ads aiming to make money through
the sales of products and services are legitimate, identifiable as ads,
                                                                                                                                  
and meet expectations of appropriateness [97]. However, we identified product ads that we would consider exploitative, e.g., that
                                                                                                                                  
promise "free" products that turn out to not to be. Though such
                                                                                                                                  
ads are not unique to political contexts, we observed many that
                                                                                                                                  
leverage political controversy to attract potential buyers.
                                                                                                                
Misleading Political Organizations. Online ads (particularly native ads) have been criticized for being potentially hard to identify
                                                                                                                                  
as ads, and thus regulated to require disclosure [11, 24]. We observe
                                                                                                                                  
that these issues are compounded in a political context, where the
                                                                                                                                  
advertiser's identity - e.g., political leaning, official (or not) political
                                                                                                                                  
organization - is (or should be) key to a user's assessment of the ad.
                                                                                                                                   
Being mistaken for a legitimate, official political organization can
                                                                                                                                  
benefit problematic advertisers (e.g., exploitative product sellers or
                                                                                                                                  
the fraudulent "Keep America Great Committee" [50]).
                                                                                                            
     Partisan Ad Targeting. We observed more political ads, and more
of the problematic ads that we discussed above, on more partisan
                                                                                                                                  
websites, particularly right-leaning sites, as well as on low-quality
                                                                                                                                  
and misinformation sites. Ad targeting in itself is not problematic,
                                                                                                                                  
and naturally, political advertisers would wish to reach people with
                                                                                                                                  
partisan alignments most likely to click on a given ad. However,
                                                                                                                                  

we raise two concerns: first, the continued polarization of U.S. political discourse, reinforced by online ads; second, the risk that
                                                                                                                                    
more vulnerable people are targeted with more manipulative and
                                                                                                                                    
exploitative political ads.
                                                  

```

## 5.2 Recommendations And Future Work

Recommendations for Ad Platforms and Policymakers. Political ads are already strongly regulated due to its sensitivity. We argue that ad platforms (which make and enforce ad policies) and policymakers (e.g., the FTC or FEC) should also consider the potential harms from ads not currently violating of existing policies. Many of the problematic ads that we saw were not official political ads but leveraged political themes and could have political ramifications

(e.g., spreading misinformation via clickbait headlines). Ad platforms and regulators should consider these ads alongside official political ads in transparency and regulation efforts.

It is worth noting that there were types of problematic political ads that we did not observe. In a preliminary qualitative analysis, we did not find ads providing false voter information, e.g., incorrect election dates, polling places, or voting methods. While that does not mean they did not exist, it nevertheless suggests that ad platforms are regulating the most egregiously harmful ads.

The extreme decentralization of the online ad ecosystem poses additional challenges for ad moderation. Though Google periodically banned political ads during our data collection, we continued to see political ads, including problematic political ads, placed by other ad platforms. Thus, we call for more comprehensive ad moderation standards (and perhaps regulation) across advertising platforms - while recognizing the complex financial and political incentives that may hamper the clear-cut adoption of regulation [34].

```
  Future Research. Future research should continue to audit ad
content and targeting. While our study has focused on web ads
                                                                
appearing on news and media websites, the online ad ecosystem is
                                                                
large and requires analysis with different data collection and analysis methods. Future work should (continue to) consider political
                                                                
and other ads across various platforms - social media, mobile web
                                                                
and apps - and sites. Moreover, we focused on U.S. political ads,
                                                                
but future research should also critically study the role of online
                                                                
ads in non-U.S. political contexts or around other historical events.
                                                                
  Future work should also directly study people who view these
                                                                
ads, to better understand the actual impact of potentially problematic ads and for different user populations.
                                         
  To enable other researchers to further analyze our collected
                                                                
ads, our dataset and codebook are available at: https://badads.cs.
                                                                
washington.edu/political.html.
                             

6 CONCLUSION
We collected ads from 745 news and media sites around the time
                                
of the 2020 U.S. elections, including 55,943 political ads, which we
                                
analyzed using quantitative and qualitative methods. We identified
                                
the use of manipulative techniques and misleading content in both
                                
official and non-official political-themed ads, and we highlight the
                                
need for greater scrutiny by ad platforms and regulators, as well as
                                
further external study and auditing of the online ad ecosystem.

ACKNOWLEDGEMENTS
We thank our shepherd, Zakir Durumeric, as well as our anonymous
                               
reviewers, for helping improve this paper. We thank Kentrell Owens
                               
and Sudheesh Singanamalla for providing feedback on an earlier
                               
draft. This work was supported in part by the National Science
                              
Foundation under grant CNS-2041894, and by the UW Center for
                               
an Informed Public and the John S. and James L. Knight Foundation.
                               

REFERENCES
[1] Albalawi, R., Yeap, T. H., and Benyoucef, M. Using Topic Modeling Methods
                                  
  for Short-Text Data: A Comparative Analysis. Frontiers in Artificial Intelligence
  (2020).
    
[2] Ali, M., Sapiezynski, P., Bogen, M., Korolova, A., Mislove, A., and Rieke, A.
                                  
  Discrimination through Optimization: How Facebook's Ad Delivery Can Lead to
                                  
  Biased Outcomes. Proc. ACM Hum.-Comput. Interact. 3, CSCW (Nov. 2019).
[3] AllSides. Balanced news via media bias ratings for an unbiased news perspective.
                                  
  https://www.allsides.com/unbiased-balanced-news.
                       
[4] Amazon. Alexa Web Information Service API. https://awis.alexa.com/.
                               
[5] Arthur, D., and Vassilvitskii, S. k-means++: The Advantages of Careful
                                  
  Seeding. In Proceedings of the Eighteenth Annual ACM-SIAM Symposium on
  Discrete Algorithms (USA, 2007), SODA '07, Society for Industrial and Applied
  Mathematics, p. 1027–1035.
             
[6] Baker, S. How GOP-linked PR firms use Google's ad platform to harvest email
                                  
  addresses. Engadget, November 2019. https://www.engadget.com/2019-11-11-
                                  
  google-political-ads-polls-email-collection.html.
                      
[7] Ballard, A. O., Hillygus, D. S., and Konitzer, T. Campaigning Online: Web
                                  
  Display Ads in the 2012 Presidential Campaign. PS: Political Science & Politics 49,
  3 (2016), 414–419.
         
[8] Ballotpedia. Presidential election, 2020. https://ballotpedia.org/Presidential_
                                  
  election,_2020.
        
[9] Bashir, M. A., Arshad, S., Robertson, W., and Wilson, C. Tracing Information Flows between Ad Exchanges Using Retargeted Ads. In Proceedings of the
  25th USENIX Conference on Security Symposium (USA, 2016), SEC'16, USENIX
  Association, p. 481–496.
            
[10] Blei, D. M., Ng, A. Y., and Jordan, M. I. Latent Dirichlet Allocation. Journal of
  Machine Learning Research 3 (2003), 993–1022.
[11] Campbell, C., and Grimm, P. E. The Challenges Native Advertising Poses: Exploring Potential Federal Trade Commission Responses and Identifying Research
                                  
  Needs. Journal of Public Policy & Marketing 38, 1 (2019), 110–123.
[12] Carr, A. Low quality websites: Content farms: What is a content farm?, 2021.
                                  
  https://researchguides.austincc.edu/contentfarms.
                      
[13] Cillizza, C. Why the delayed election results prove the system is actually
                                  
  working, Nov. 2020. https://www.cnn.com/2020/11/04/politics/donald-trumpjoe-biden-2020-election-results/index.html.
                    
[14] Crain, M., and Nadler, A. Political Manipulation and Internet Advertising
                                  
  Infrastructure. Journal of Information Policy 9 (2019), 370–410.
[15] Crovitz, L. G. How Amazon, Geico and Walmart fund propaganda. The New
                                  
  York Times, Jan. 2020. https://www.nytimes.com/2020/01/21/opinion/fake-newsrussia-ads.html.
        
[16] Curiskis, S. A., Drake, B., Osborn, T. R., and Kennedy, P. J. An evaluation of
                                  
  document clustering and topic modelling in two online social networks: Twitter
                                  
  and Reddit. Information Processing & Management 57, 2 (2020), 102034.
[17] Dorsey, J. We've made the decision to stop all political advertising on Twitter
                                  
  globally, 2019.
        
[18] Dykhne, I. Persuasive or Deceptive - Native Advertising in Political Campaigns.
                                  
  Southern California Law Review 91 (2018), 339.
[19] Easylist Filter List Project. Easylist. https://easylist.to.
                          
[20] Edelson, L., Lauinger, T., and McCoy, D. A Security Analysis of the Facebook
                                  
  Ad Library. In IEEE Symposium on Security and Privacy (Oakland) (2020).
[21] Edelson, L., Sakhuja, S., Dey, R., and McCoy, D. An Analysis of United States
                                  
  Online Political Advertising Transparency. arXiv:1902.04385, Feb. 2019.
                               
[22] Evelyn, K. Capitol attack: the five people who died, 2021. https:
                                  
  //www.theguardian.com/us-news/2021/jan/08/capitol-attack-police-officerfive-deaths.
       
[23] FactCheck.org. Misinformation directory. https://www.factcheck.org/2017/07/
                                  
  websites-post-fake-satirical-stories/.
                 
[24] Federal Trade Commission. .com Disclosures: How to Make Effective
                                  
  Disclosures in Digital Advertising, Mar. 2013. https://www.ftc.gov/system/files/
                                  
  documents/plain-language/bus41-dot-com-disclosures-information-aboutonline-advertising.pdf.
           
[25] Fischer, S. Scoop: Google to block election ads after election day,
                                  
  2021. https://www.axios.com/google-to-block-election-ads-after-election-day4b60650d-b5c2-4fb4-a856-70e30e19af17.html.
                    

[26] Fischer, S. Scoop: Google to lift political ad ban put in place following capitol siege, 2021. https://www.axios.com/capitol-siege-google-political-ad-ban5000245d-35d6-4448-b7b2-daa7ccfe816a.html.
                                                   
[27] Global Disinformation Index. The Quarter Billion Dollar Question: How is
                                                                                    
     Disinformation Gaming Ad Tech?, Sept. 2019. https://disinformationindex.org/
                                                                                    
     wp-content/uploads/2019/09/GDI_Ad-tech_Report_Screen_AW16.pdf.
                                                                           
[28] Google. Puppeteer. https://developers.google.com/web/tools/puppeteer/.
                                                                               
[29] Google. Adwords API - Verticals. Google Developers, 2021. https://developers.
                                                                                    
     google.com/adwords/api/docs/appendix/verticals.
                                                      
[30] Google. Political advertising in the United States. https://transparencyreport.
                                                                                    
     google.com/political-ads/region/US, 2021. Google Transparency Report.
                                                                             
[31] Graham, M. Pinterest says it will no longer allow ads on elections-related
                                                                                    
     content, employees get time off to vote, 2020.
                                                  
[32] Grootendorst, M. BERTopic: Leveraging BERT and c-TF-IDF to create easily
                                                                                    
     interpretable topics, 2020.
                               
[33] Grootendorst, M. Creating a class-based TF-IDF with Scikit-Learn.
                                                                                    
     https://towardsdatascience.com/creating-a-class-based-tf-idf-with-scikitlearn-caea7b15b858, October 2020. Towards Data Science.
                                                               
[34] Haenschen, K., and Wolf, J. Disclaiming responsibility: How platforms deadlocked the Federal Election Commission's efforts to regulate digital political
                                                                                    
     advertising. Telecommunications Policy 43, 8 (2019), 101824.
[35] Hao, S., Chen, L., Zhou, S., Liu, W., and Zheng, Y. Multi-layer multi-view topic
                                                                                    
     model for classifying advertising video. Pattern Recognition 68 (2017), 66–81.
[36] Herbert, C. The Fake News Codex. http://www.fakenewscodex.com, December
                                                                                    
     2018.
          
[37] Hoffman, M., Bach, F., and Blei, D. Online Learning for Latent Dirichlet
                                                                                    
     Allocation. In Advances in Neural Information Processing Systems (2010), J. Lafferty,
     C. Williams, J. Shawe-Taylor, R. Zemel, and A. Culotta, Eds., vol. 23, Curran
                                                                                    
     Associates, Inc.
                    
[38] Hubert, L., and Arabie, P. Comparing partitions. Journal of Classification 2
     (dec 1985), 193–218.
                         
[39] Irvine, M. Google ads benchmarks for your industry. https://www.wordstream.
                                                                                    
     com/blog/ws/2016/02/29/google-adwords-industry-benchmarks, 2021. Wordstream: Online Advertising Made Easy.
                                            
[40] Joshua Gillin. The more outrageous, the better: How clickbait ads make money
                                                                                    
     for fake news sites. https://www.politifact.com/punditfact/article/2017/oct/04/
                                                                                    
     more-outrageous-better-how-clickbait-ads-make-mone/, October 2017.
                                                                             
[41] Kim, Y. M., Hsu, J., Neiman, D., Kou, C., Bankston, L., Kim, S. Y., Heinrich, R.,
                                                                                    
     Baragwanath, R., and Raskutti, G. The Stealth Media? Groups and Targets
                                                                                    
     behind Divisive Issue Campaigns on Facebook. Political Communication 35, 4
     (2018), 515–541.
                     
[42] Kim LaCapria. Snopes' field guide to fake news sites and hoax purveyors. Snopes,
                                                                                    
     January 2016. https://www.snopes.com/news/2016/01/14/fake-news-sites/.
                                                                                
[43] Kingsley, S., Wang, C., Mikhalenko, A., Sinha, P., and Kulkarni, C. Auditing
                                                                                    
     Digital Platforms for Discrimination in Economic Opportunity Advertising. ArXiv
     2008.09656 (2020).
[44] Le Pochat, V., Van Goethem, T., Tajalizadehkhoob, S., Korczyński, M., and
                                                                                    
     Joosen, W. Tranco: A Research-Oriented Top Sites Ranking Hardened Against
                                                                                    
     Manipulation. In 26th Network and Distributed System Security Symposium (NDSS)
     (2019).
           
[45] Lécuyer, M., Spahn, R., Spiliopolous, Y., Chaintreau, A., Geambasu, R., and
                                                                                    
     Hsu, D. Sunlight: Fine-grained Targeting Detection at Scale with Statistical
                                                                                    
     Confidence. In ACM Conference on Computer and Communications Security (CCS)
     (2015).
           
[46] Lemire, J., Miller, Z., and Weissert, W. Biden defeats Trump for White House,
                                                                                    
     says 'time to heal', 2021. https://apnews.com/article/joe-biden-wins-whitehouse-ap-fd58df73aa677acb74fce2a69adb71f9.
                                                   
[47] Li, Z., Zhang, K., Xie, Y., Yu, F., and Wang, X. Knowing Your Enemy: Understanding and Detecting Malicious Web Advertising. In ACM Conference on
     Computer and Communications Security (CCS) (2012).
[48] Looper, E., and Bird, S. NLTK: The Natural Language Toolkit. ArXiv
     https://arxiv.org/abs/cs/0205028 (2002).
[49] Markay, L. Pro-trump 'news sites' are harvesting your emails to sell to the campaign. https://www.thedailybeast.com/pro-trump-news-sites-are-harvestingyour-emails-to-sell-to-the-campaign, August 2020. The Daily Beast.
                                                                          
[50] Markay, L. Pro-Trump scam PAC operator hit with wire fraud charge. Axios,
                                                                                    
     April 2021. https://www.axios.com/pro-trump-scam-pac-operator-wire-fraudcharge-d888876f-680c-4b47-83d8-d72da709ce8b.html.
                                                           
[51] Mathur, A., Narayanan, A., and Chetty, M. Endorsements on Social Media:
                                                                                    
     An Empirical Study of Affiliate Marketing Disclosures on YouTube and Pinterest.
                                                                                    
     Proceedings of the ACM on Human-Computer Interaction (CSCW) 2 (Nov. 2018).
[52] Mathur, A., Wang, A., Schwemmer, C., Hamin, M., Stewart, B. M., and
                                                                                    
     Narayanan, A. Manipulative tactics are the norm in political emails: Evidence
                                                                                    
     from 100K emails from the 2020 U.S. election cycle. https://electionemails2020.org,
                                                                                    
     2020.
          
[53] McHugh, M. L. Interrater reliability: the kappa statistic. Biochem Med (Zagreb)
     22, 3 (October 2012), 276–82.

```

Polls, Clickbait, and Commemorative $2 Bills: Problematic Political Advertising on News and Media Websites Around the 2020 U.S. Elections IMC '21, November 2–4, 2021, Virtual Event, USA

```
[54] Media Bias/Fact Check Team. Media Bias/Fact Check: The Most Comprehensive Media Bias Resource. https://mediabiasfactcheck.com/fake-news/.
                                                                           
[55] Misra, S. Deceptive political advertising: Some new dimensions. Journal of Legal,
     Ethical and Regulatory Issues 18 (2015), 71–80.
[56] Muller, M. Ways of Knowing. Springer, 2014, ch. Curiosity, Creativity, and
     Surprise as Analytic Tools: Grounded Theory Method.
                                                           
[57] Narayanan, A., Mathur, A., Chetty, M., and Kshirsagar, M. Dark patterns:
                                                                                    
     Past, present, and future. Communications of the ACM 63, 9 (Aug. 2020), 42–47.
[58] Nelms, T., Perdisci, R., Antonakakis, M., and Ahamad, M. Towards Measuring
                                                                                    
     and Mitigating Social Engineering Software Download Attacks. In Proceedings of
     the 25th USENIX Conference on Security Symposium (USA, 2016), SEC'16, USENIX
     Association, p. 773–789.
                             
[59] Nikiforakis, N., Kapravelos, A., Joosen, W., Krügel, C., Piessens, F., and
                                                                                    
     Vigna, G. Cookieless Monster: Exploring the Ecosystem of Web-Based Device
                                                                                    
     Fingerprinting. IEEE Symposium on Security and Privacy (2013), 541–555.
[60] Ohlheiser, A. This is how Facebook's fake-news writers make money. Washington Post, Nov. 2016. https://www.washingtonpost.com/news/the-intersect/
                                                                                    
     wp/2016/11/18/this-is-how-the-internets-fake-news-writers-make-money/.
                                                                                 
[61] OpenSources Contributors. Opensources. https://github.com/
                                                                                    
     OpenSourcesGroup/opensources, April 2017.
                                                  
[62] Pedregosa, F., Varoqaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel,
                                                                                    
     O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J.,
                                                                                    
     Passos, A., Cournapeau, D., Brucher, M., Perrot, M., and Duchesnay, E.
                                                                                    
     Scikit-learn: Machine learning in Python. Journal of Machine Learning Research
     12 (2011), 2825–2830.
[63] Provos, N., Mavrommatis, P., Rajab, M. A., and Monrose, F. All your iframes
                                                                                    
     point to us. In Proceedings of the 17th Conference on Security Symposium (USA,
     2008), SS'08, USENIX Association, p. 1–15.
                                               
[64] Qi, P., Zhang, Y., Zhang, Y., Bolton, J., and Manning, C. D. Stanza: A Python
                                                                                    
     Natural Language Processing Toolkit for Many Human Languages. Association
     for Computational Linguistics System Demonstrations (2020).
[65] Qiang, J., Qian, Z., Li, Y., Yuan, Y., and Wu, X. Short Text Topic
                                                                                    
     Modeling Techniques, Applications and Performance: A Survey. ArXiv
     https://arxiv.org/abs/1904.07695 (2019).
[66] Rakoczy, C. The sneaky reason you should never sign petitions or answer
                                                                                    
     surveys online. Mic.com, May 2017. https://www.mic.com/articles/175333/wantto-save-money-heres-the-surprising-reason-why-you-should-never-sign-anonline-petition.
                     
[67] Rastogi, V., Shao, R., Chen, Y., Pan, X., Zou, S., and Riley, R. Are these Ads Safe:
                                                                                    
     Detecting Hidden Attacks through the Mobile App-Web Interfaces. In Network
     and Distributed System Security Symposium (NDSS) (2016).
[68] Řehůřek, R., and Sojka, P. Software Framework for Topic Modelling with
                                                                                    
     Large Corpora. In Proceedings of the LREC 2010 Workshop on New Challenges for
     NLP Frameworks (Valletta, Malta, May 2010), ELRA, pp. 45–50. http://is.muni.cz/
     publication/884893/en.
                            
[69] Ridout, T. N., Fowler, E. F., and Franz, M. M. Spending Fast and Furious:
                                                                                    
     Political Advertising in 2020. The Forum 18, 4 (2021). https://www.degruyter.
     com/document/doi/10.1515/for-2020-2109/html.
                                                     
[70] Röder, M., Both, A., and Hinneburg, A. Exploring the Space of Topic Coherence
                                                                                    
     Measures. In Proceedings of the Eighth ACM International Conference on Web
     Search and Data Mining (New York, NY, USA, 2015), WSDM '15, Association for
     Computing Machinery, p. 399–408.
                                        
[71] Roesner, F., Kohno, T., and Wetherall, D. Detecting and Defending Against
                                                                                    
     Third-Party Tracking on the Web. In USENIX Symposium on Networked Systems
     Design and Implementation (NSDI) (2012).
[72] Romano, S., Vinh, N. X., Bailey, J., and Verspoor, K. Adjusting for Chance
                                                                                    
     Clustering Comparison Measures, 2015.
                                             
[73] Rosenberg, A., and Hirschberg, J. V-measure: A conditional entropy-based
                                                                                    
     external cluster evaluation measure. In Proceedings of the 2007 Joint Conference
     on Empirical Methods in Natural Language Processing and Computational Natural Language Learning (EMNLP-CoNLL) (Prague, Czech Republic, June 2007),
     Association for Computational Linguistics, pp. 410–420.
                                                             
[74] Saldana, J. The Coding Manual for Qualitative Researchers. SAGE Publications,
     2012.
          
[75] Sanchez-Rola, I., Dell'Amico, M., Balzarotti, D., Vervier, P.-A., and Bilge,
                                                                                    
     L. Journey to the Center of the Cookie Ecosystem: Unraveling Actors' Roles and
                                                                                    
     Relationships. In IEEE Symposium on Security and Privacy (2021).
[76] Sanh, V., Debut, L., Chaumond, J., and Wolf, T. Distilbert, a distilled version of
                                                                                    
     bert: smaller, faster, cheaper and lighter. ArXiv https://arxiv.org/abs/1910.01108v4
     (2020).
           
[77] Schmidt, M. S., and Broadwater, L. Officers' Injuries, Including Concussions,
                                                                                    
     Show Scope of Violence at Capitol Riot, 2021. https://www.nytimes.com/2021/
                                                                                    
     02/11/us/politics/capitol-riot-police-officer-injuries.html.
                                                              
[78] Schneider, E. Google will end political ad ban this week, 2021. https://www.
                                                                                    
     politico.com/news/2020/12/09/google-end-political-ad-ban-443882.
                                                                        
[79] Silverman, C., and Alexander, L. How Teens In The Balkans
                                                                                    
     Are Duping Trump Supporters With Fake News, Nov. 2016. https:
                                                                                    

       //www.buzzfeednews.com/article/craigsilverman/how-macedonia-became-aglobal-hub-for-pro-trump-misinfo#.tcR3aZa5r.
                                                                          
[80] Smith, A., and Banic, V. Fake News: How a Partying Macedonian Teen Earns Thousands Publishing Lies. NBC News, December 2016. https://www.nbcnews.com/news/world/fake-news-how-partyingmacedonian-teen-earns-thousands-publishing-lies-n692451.
                                                                                             
[81] Sosnovik, V., and Goga, O. Understanding the Complexity of Detecting Political
                                                                                                                       
       Ads. In The Web Conference (WWW) (2021).
[82] Spring, M. 'Stop the steal': The deep roots of Trump's 'voter fraud' strategy,
                                                                                                                        
       2021. https://www.bbc.com/news/blogs-trending-55009950.
                                                                                            
[83] staff, P. Politifact's guide to fake news websites and what they peddle. Politifact, April 2017. https://www.politifact.com/article/2017/apr/20/politifacts-guidefake-news-websites-and-what-they/.
                                                            
[84] Steenburg, E. V. Areas of research in political advertising: a review and research
                                                                                                                       
       agenda. International Journal of Advertising 34, 2 (2015), 195–231.
[85] Stromer-Galley, J., Hemsley, J., Rossini, P., McKernan, B., McCracken, N.,
                                                                                                                        
       Bolden, S., Korsunska, A., Gupta, S., Kachhadia, J., Zhang, W., and Zhang,
                                                                                                                        
       F. The Illuminating Project: Helping Journalists Cover Social Media in the
                                                                                                                       
       Presidential Campaign, 2020. https://illuminating.ischool.syr.edu/.
                                                                                                     
[86] Surian, D., Nguyen, D. Q., Kennedy, G., Johnson, M., Coiera, E., and Dunn,
                                                                                                                        
       A. G. Characterizing Twitter Discussions About HPV Vaccines Using Topic
                                                                                                                       
       Modeling and Community Detection". J Med Internet Res 18, 8 (Aug 2016), e232.
[87] Team, A. Google Display Ads CPM, CPC, & CTR Benchmarks in Q1 2018. https:
                                                                                                                        
       //blog.adstage.io/google-display-ads-cpm-cpc-ctr-benchmarks-in-q1-2018, 2018.
                                                                                                                        
       AdStage.
                    
[88] Team, B. V. J. Capitol riots: A visual guide to the storming of Congress, 2021.
                                                                                                                        
       https://www.bbc.com/news/world-us-canada-55575260.
                                                                                       
[89] Trish, B. From recording videos in a closet to Zoom meditating, 2020's political
                                                                                                                       
       campaigns adjust to the pandemic. https://theconversation.com/from-recordingvideos-in-a-closet-to-zoom-meditating-2020s-political-campaigns-adjust-tothe-pandemic-145788, 2020. The Conversation.
                                                                          
[90] Venkatadri, G., Andreou, A., Liu, Y., Mislove, A., Gummadi, K. P., Loiseau, P.,
                                                                                                                        
       and Goga, O. Privacy Risks with Facebook's PII-Based Targeting: Auditing a
                                                                                                                       
       Data Broker's Advertising Interface. In IEEE Symposium on Security and Privacy
       (2018).
                
[91] Vinh, N. X., Epps, J., and Bailey, J. Information Theoretic Measures for Clusterings Comparison: Variants, Properties, Normalization and Correction for Chance.
                                                                                                                        
       Journal of Machine Learning Research 11, 95 (2010), 2837–2854.
[92] Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue, C., Moi, A., Cistac, P.,
                                                                                                                        
       Rault, T., Louf, R., Funtowicz, M., Davison, J., Shleifer, S., von Platen, P.,
                                                                                                                        
       Ma, C., Jernite, Y., Plu, J., Xu, C., Scao, T. L., Gugger, S., Drame, M., Lhoest, Q.,
                                                                                                                        
       and Rush, A. M. HuggingFace's Transformers: State-of-the-art Natural Language
                                                                                                                       
       Processing, 2020.
                               
[93] Xing, X., Meng, W., Lee, B., Weinsberg, U., Sheth, A., Perdisci, R., and Lee, W.
                                                                                                                        
       Understanding Malvertising Through Ad-Injecting Browser Extensions. In 24th
       International Conference on World Wide Web (WWW) (2015).
[94] Yin, J., and Wang, J. A Dirichlet Multinomial Mixture Model-Based Approach
                                                                                                                       
       for Short Text Clustering. In Proceedings of the 20th ACM SIGKDD International
       Conference on Knowledge Discovery and Data Mining (New York, NY, USA, 2014),
       KDD '14, Association for Computing Machinery, p. 233–242.
                                                                                             
[95] Zarras, A., Kapravelos, A., Stringhini, G., Holz, T., Kruegel, C., and Vigna,
                                                                                                                        
       G. The dark alleys of Madison Avenue: Understanding malicious advertisements.
                                                                                                                        
       In ACM Internet Measurement Conference (2014).
[96] Zeng, E., Kohno, T., and Roesner, F. Bad News: Clickbait and Deceptive Ads on
                                                                                                                       
       News and Misinformation Websites. In Workshop on Technology and Consumer
       Protection (2020).
[97] Zeng, E., Kohno, T., and Roesner, F. What Makes a "Bad" Ad? User Perceptions
                                                                                                                       
       of Problematic Online Advertising. In Proceedings of the 2021 CHI Conference
       on Human Factors in Computing Systems (New York, NY, USA, 2021), CHI '21,
       Association for Computing Machinery.
                                                              

A HISTORICAL BACKGROUND
Election day was November 3, 2020, but the results of the election
                                 
were significantly delayed due to the COVID-19 pandemic as states
                                 
continued to receive mail-in votes and count ballots in subsequent
                                 
days [13]. During this time, Trump and his campaign maintained
                                 
that there was widespread voter fraud [82]. Most major news outlets
                                 
declared the results - that Biden had obtained enough electoral
                                 
votes to defeat Trump - on November 7 [46]. Sparked by a speech
                                 
from Donald Trump on January 6, 2021 in which he continued
                                 
to falsely claim that he had won the election, thousands of his
                                 
supporters marched to the U.S. Capitol complex, where Congress

had assembled to certify the electoral result [88]. The storming
                                                                
of the Capitol resulted in over 140 injuries [77] and 5 deaths [22].
                                                                
The certification was completed the next day and President Biden's
                                                                
inauguration was held on January 20, 2021.
                                          
  On November 3, elections were also held for seats in the Senate
                                                                
and House of Representatives. In state and local politics, elections
                                                                
were held for 13 governorships in 11 states and 2 territories, as well
                                                                
as for state legislative chambers, attorneys generals, state supreme
                                                                
court seats, and various referendums and ballot measures. In the
                                                                
state of Georgia, no Senate candidates received a majority of the
                                                                
vote during the first round, leading to a run-off election on January
                                                                
5, 2021.
       

B TEXT CLUSTERING EXPERIMENTS
To qualitatively categorize the overall dataset, we used topic modeling and text clustering algorithms to group ads with similar content, and then created qualitative descriptions for each grouping
                                   
via term frequency evaluation and manual labeling. The shortcontent, low-context nature of many of ads in the dataset most
                                   
closely aligns with short-text topic modeling problems [1, 16, 65],
                                   
however prior work on topic modeling advertisement text specifically is minimal [35]. As such, we pursued several diverse approaches to the NLP pipeline. For tokenization and lemmatization,
                                   
we experimented with three pre-processing models: NLTK [48],
                                   
Stanford NLP Group's Stanza [64], and DistilBERT [76]. Our preprocessing filtered on NLTK's english stopword corpus 4along
                                   
with several OCR artifacts such as "sponsoredsponsored." For topic
                                   
generation, we experimented with several models and techniques:
                                   
Latent Dirichlet Allocation (LDA) [10, 37], Gibbs-Sampling Dirichlet
                                   
Mixture Model (GSDMM) 5[94], DistilBERT + K-means Clustering [5, 76], and BERTopic [32]. We tested two implementations of
                                   
LDA: Scikit-learn [62] and Gensim [68] with both Stanza and NLTK
                                   
pre-processing. The selection of LDA parameter values to evaluate
                                   
was based on results from Hoffman et al. [37]. The GSDMM model
                                   
was tested on parameter values following suggestions from Yin and
                                   
Wang [94] for both Stanza and GSDMM pre-processing as well. The
                                   
DistilBERT model and DistilBERT pre-processing, implemented via
                                   
Huggingface [92], were used to generate feature vectors for use
                                   
by K-means clustering via Sklearn [62], which was tested on topic
                                   
count. Lastly, BERTopic was tested on topic count as well.
                               
To establish an approximate baseline for topic cardinality tuning and evaluation on the full deduplicated dataset, we manually
                                   
labeled 2,583 unique randomly-sampled advertisements from the
                                   
dataset (1.52% of the deduplicated ads), using a list of verticals that
                                   
Google Adwords provides to publishers for targeting purposes [29]
                                   
(e.g. "/Shopping", "/Shopping/Apparel", "/Shopping/Apparel/Men's
                                   
Clothing"). For each ad we used the most descriptive label, but later
                                   
collapsed the hierarchies to the second level to form larger groups.
                                   
This process produced 171 unique label groups in the sample, which
                                   
served as reference for topic count selection and as test data for
                                   
evaluation. After generating topics for the full deduplicated dataset,
                                   
the subset of ads corresponding to those labeled manually were isolated for similarity evaluation, assuming that a good model would
                                   
roughly place ads in the same product sector in the same group.
                                  
4https://www.nltk.org/book/ch02.html
                
5https://github.com/rwalk/gsdmm
              

```

IMC '21, November 2–4, 2021, Virtual Event, USA Eric Zeng, Miranda Wei, Theo Gregersen, Tadayoshi Kohno, Franziska Roesner

| Model                                        | Preprocessor   | 𝛼   | 𝛽   | K   | n_iters   |
|----------------------------------------------|----------------|------|------|-----|-----------|
| Stanza                                       | 0.1            | 0.05 | 180  | 40  |           |
| Full                                         | Dedupli                |      |      |     |           |
| cated Dataset                                | NLTK           | 0.1  | 0.1  | 75  | 40        |
| Political Memorabilia                                              | NLTK           | 0.1  | 0.1  | 30  | 40        |
| Nonpolitical Products Using Political Topics |                |      |      |     |           |

| Model                                                  | Topics   |
|--------------------------------------------------------|----------|
| Full Deduplicated Dataset                              | 180      |
| Political Memorabilia                                  | 45       |
| Nonpolitical Products Using Political Topics           | 29       |
| Table 8: Selected GSDMM Model Topic Count by Data Subs | et       |

| Model        | ARI    | AMI    | H      | C      | 𝐶𝑣   |
|--------------|--------|--------|--------|--------|--------|
| BERT+K-means | 0.0119 | 0.0337 | 0.3243 | 0.3119 | 0.5333 |
| BERTopic     | 0.0109 | 0.1411 | 0.3424 | 0.4524 | 0.5590 |
| LDA          | 0.2616 | 0.2306 | 0.5343 | 0.4696 | 0.4198 |
| GSDMM        | 0.4743 | 0.4438 | 0.5297 | 0.6328 | 0.5457 |

Table 7: Selected GSDMM Model Parameters by Data Subset

```
  To evaluate similarity to our training clusters we used Adjusted
                                                                  
Rand Index () [38] and Adjusted Mutual Index () [91] metrics implemented via Scikit-learn, accounting for possible imbalanced or balanced cluster sizes [72]. For evaluating intra-topic
                                                                  
similarity, we measured Homogeneity () and for inter-topic similarity, we measured Completeness () [73], both via Scikit-learn.
                                                                   
As a general measure of topic quality, we recorded  coherence
via Gensim, based on Röder et al [70].
                                      
  Table 6 details the best performances by model during tuning and
                                                                  
testing. GSDMM performed the best (likely because it is designed
                                                                  
specifically for short text documents), with an  = 0.4743,  =
0.4438,  = 0.5297,  = 0.6328, and  Coherence= 0.5457, and
thus was selected. These values are comparable to other GSDMM
                                                                  
results on Twitter data [16, 65, 86]. We ran the model on the top
                                                                  
parameters 8 more times and selected the best iteration for use in
                                                                  
our final results. The final GSDMM model produced 180 clusters
                                                                  
on the full deduplicated dataset.
                                
Labels for topics were designated after reviewing random samples of ads from within the topic and incorporating term results
                                                                  
from c-TF-IDF, which utilizes a modified term frequency - inverse
                                                                  
document frequency (TF-IDF) algorithm to select important terms
                                                                  
from a given topic cluster [33].
                               
  Based on the performance of GSDMM on the overall dataset,
                                                                   
we further used GSDMM for topic modeling on the political ad
                                                                  
subsets of "political memorabilia" and "nonpolitical products using
                                                                  
political topics." To evaluate performance in the absence of a ground
                                                                  
truth, we measured  coherence. For both subsets, we tuned parameters of topic count, alpha, and beta. After identifying the best

```

Polls, Clickbait, and Commemorative $2 Bills: Problematic Political Advertising on News and Media Websites Around the 2020 U.S. Elections IMC '21, November 2–4, 2021, Virtual Event, USA
performing parameters, we ran the models 10 additional times each before selecting the best iteration. The top "political memorabilia" model achieved a  coherence of 0.7109 with 45 topics, and the top "nonpolitical products using political topics" model achieved a  coherence of 0.6777 with 29 topics. As before, we manually labeled the largest topics after reviewing random samples of ads from within the topic. However, due to the smaller topic sizes in the political subsets as compared to the full dataset, we weighted ads by their duplicate counts when generating c-TF-IDF results (e.g.

an ad with 10 duplicates would have its text weighted 10x).

Table 7 contains the GSDMM parameters used in our selected GSDMM models by dataset subset, and table 8 details the topic count by the end of each model's runtime. For all three models, topic labels were scaled up from the deduplicated subsets to the full dataset.

```
C QUALITATIVE CODEBOOK
C.1 Methodology
We generated a qualitative codebook using grounded theory [56],
                                 
an approach for generating themes categories via observation of the
                                 
ground-level data. First, three researchers conducted a preliminary
                                 
analysis of around 100 political ads each, creating open codes describing the characteristics of ads. We met to discuss and organized
                                 
them into axial codes (i.e., multiple choice categories for different
                                 
concepts) that best addressed our research questions.
                           
 Using these codes, three researchers coded the 8,836 ads, meeting
                                 
multiple times during the process to iteratively refine the codebook
                                 
based on new data. To assess the consistency of the coding, all
                                 
coders coded a random subset of 200 ads, and we calculated Fleiss'
                                 
 (a statistical measure of intercoder agreement,  = 0 indicates
zero,  = 1.0 indicates perfect) on this subset. We achieved an
average  = 0.771 across our 10 categories ( = 0.09), indicating
moderate-strong agreement [53].
                 
 Supplementing our qualitative codes, one researcher also labeled
                                 
each campaign-related ad with the advertisers' name and legal
                                 
classification (e.g., 501(c)(4) nonprofit), using information such as
                                 
the "paid for" box in the ad, or the organization's website.
                             

```

## C.2 Codebook Contents

Our codeboook included three mutually exclusive high-level themes:

(1) campaigns and advocacy ads, **(2) political product ads**,
and **(3) political news and media ads**. To account for technical errors in crawling and classification, ads were classified as **Malformed/not political** if the extracted text and/or image content was incomplete or non-political, e.g., if screenshots failed to capture the whole ad, pop-ups or other material covered the ad, multiple ads were captured, incorrect model classification.

## C.3 Campaigns And Advocacy Ads

We define campaign and advocacy ads as those that explicitly addressed or promoted a political candidate, election, policy, or call to action. Within this category, we further define the level of election, the purpose of the ad, and advertiser-related information.

C.3.1 Level of Election. Election level refers to candidate's jurisdiction, e.g., Senate elections were classified as federal. Specific

```
codes of election level are: presidential, federal, state / local, no
                                                                     
specific election, none. These codes are mutually exclusive. Note
                                                                     
that "state / local" encompasses ballot initiatives and referenda as
                                                                     
well as candidates.
                   
C.3.2 Purpose of Ad. Ad purpose is mutually inclusive, meaning
one campaign and advocacy ad can be assigned multiple purposes,
                                                                     
e.g. voter information coupled with promoting a candidate. We
                                                                     
coded for five purposes: promote candidate or policy; poll, petition,
                                                                     
or survey; voter information; attack opposition; fundraise.
                                                             
C.3.3 Advertiser Affiliation and Organization Type. To facilitate
insights into the advertisers, we identified their political affiliation
                                                                     
and type of organization (both mutually exclusive). First, we labeled
                                                                     
each advertiser by name, using information from the ad content
                                                                     
and/or the landing page (e.g., disclosures that say "Paid for By...").
                                                                    
  Then, for each advertiser, we investigated their legal organization
                                                                     
status, based on criteria developed by Kim et al. [41]. Organizations
                                                                     
listed on the Federal Election Commission website, or state elections
                                                                     
boards were labeled as Registered Committees. 501(c)(3), 501(c)(4),
                                                                     
and 501(c)(6) tax-exempt nonprofits, and legitimate foreign nonprofits that were visible in the Propublica Nonprofit Explorer or
                                                                     
Guidestar were labeled as Nonprofit organizations. Advertisers
                                                                     
whose websites' home pages were news front pages were labeled
                                                                     
as news organizations (regardless of their legitimacy). Elections
                                                                     
boards, state Secretaries of State, or any other state or local government institutions were labeled as Government Agencies. Advertisers who ran poll ads, and were listed FiveThirtyEight's Pollster
                                                                     
Ratings were labeled as poll organizations. Ads from corporations
                                                                     
and other commercial ventures were listed as businesses. Any ads
                                                                     
where the advertiser was not identifiable was listed as unknown.
                                                                    
  We also attempted to determine the political affiliation of the
                                                                     
advertiser. We coded affiliations as Democratic party, Republican
                                                                     
party, or independent if the advertiser was officially associated
                                                                     
with those political parties (local or national branches), or a candidate running under that party's ticket. Codes of right/conservative,
                                                                     
liberal/progressive, and centrist apply to advertisers not officially
                                                                     
associated with a party, but that explicitly indicate their political
                                                                     
alignment with words like "conservative" or "progressive", either in
                                                                     
the ad itself or on their websites. Nonpartisan affiliation refers to
                                                                     
explicitly nonpartisan advertisers or nonpartisan election positions,
                                                                     
e.g. some local sheriff offices.
                              

```

## C.4 Political Product Ads

We define political products ads as those centered on selling a product or service, using political imagery or content. This is further delineated into three mutually exclusive subcategories: political memorabilia, nonpolitical products using political topics, and political services.

C.4.1 Political Memorabilia. Political memorabilia includes all ads marketing products with some form of political design, e.g. 2ndamendment-themed apparel, keepsakes such as election trading cards, and merchandise such as Trump flags. This encompasses products sold for profit and those marketed as free or giveaways.

C.4.2 Nonpolitical Products Using Political Topics. We coded ads as nonpolitical products using political topics if they used political messaging or context to advertise products ordinarily unrelated to politics. For instance, this covers investment firms marketing their stock reports in the context of election uncertainty.

C.4.3 Political Services. Political services includes ads promoting services directly involved in political industry such as lobbying or election prediction sites.

```
C.5 Political News and Media Ads
We define political news and media ads as those advertising a
                                            
specific political news article, video, program, or event, regardless
                                            
of the content style or quality. This categorization encompasses
                                            
political clickbait and tabloid-style coverage of political figures as
                                            
well as traditional news and media. We further define two mutually
                                            
exclusive subcategories: sponsored articles / direct links to stores,
                                            
and news outlets, programs, and events.
                           
C.5.1 Sponsored Articles / Direct Links to Stories. We coded ads
as sponsored articles / direct links to stories if they advertised a
                                            
specific news article or media piece, e.g. an authored story or video
                                            
regarding a current event. We automatically assigned 1,038 ads to
                                            
this category from Zergnet, a well-known content recommendation
                                            
company, as we determined via their advertisement methods that
                                            
all ads from their domain fit this category.
                            
C.5.2 News Outlets, Programs, Events, And Related Media. News
outlets, programs, and events ads are distinguished from sponsored
                                            
articles / direct links to stories in specificity, longevity, or reference.
                                            
This category includes ads for political news outlets (as opposed
                                            
to individual news pieces), lasting programs such as NBC election
                                            
shows (in contrast to a single media clip), or future events such as
                                            
panels or livestreams (rather than already existing news). We also
                                            
included ads that were related media, such as podcasts, books, and
                                            
interviews.
       

D WORD FREQUENCY ANALYSIS OF
  POLITICAL NEWS ADS
 Unique Word Frequency Analysis. We looked at the most common
words in political article ads by first deduplicating ads (Sec. 3.2.2),
                                   
then tokenizing and lemmatizing the ad text. The top 10 words and
                                   
their frequencies, as well as a word cloud of the top 50 words, is
                                  
shown in Fig. 15. Among the top 50, we find frequent mentions of
                                   
"trump" (1,050 times, more than double the next most common word,
                                   
"biden"), as well as other politically relevant terms and names. Many
                                   
of top 50 words reveal the general tone of these article ads, which
                                  
often emphasize urgency, e.g., "new," "top," or scandal, e.g., "just,"
                                   
"claim," "reveal," "watch." The colloquialism "turn heads" was particularly common, e.g., "What Michigan's Governor Just Revealed
                                  
May Turn Some Heads."
            

```

| Word   | Freq.   |
|--------|---------|
| trump  | 1,050   |
| biden  | 415     |
| elect  | 314     |
| read   | 235     |
| new    | 219     |
| top    | 215     |
| articl | 196     |
| presid | 176     |
| thi    | 170     |
| video  | 162     |

![17_image_0.png](17_image_0.png)

Figure 15: Frequencies of the top 10 words in political news article ads, and a word cloud showing the top 50. Ad text was deduplicated by ad, and then tokenized and lemmatized.

Polls, Clickbait, and Commemorative $2 Bills:

![18_image_0.png](18_image_0.png) Problematic Political Advertising on News and Media Websites Around the 2020 U.S. Elections IMC '21, November 2–4, 2021, Virtual Event, USA
(a) (b)
Figure 16: Other misleading campaign ads: an RNC ad imitates a system popup (a), and a Trump campaign meme-style ad attacking Biden (b).

```
E ADDITIONAL AD SCREENSHOTS
 Other Misleading Campaign Ads: Phishing Ads and Memes. Though
many campaign and advocacy ads in the dataset were potentially
                                  
misleading or factually incorrect, we highlight two types that appeared particularly egregious.
               
 In December, the Republican National Committee ran ads that
                                  
imitate a system alert popup, like an impersonation attack (Figure 16a). We found 162 ads of this style in our dataset. Though the
                                  
popup's style is outdated, it is generally misleading for ads and
                                  
websites to imitate operating system dialogues or other programs.
                                   
 Before the general election, the Trump Make America Great
                                  
Again Campaign launched several attack ads in the style of an
                                  
"image macro" meme. They featured
                   
 (obviously) doctored photos of Joe Biden, holding Chinese flags,
                                   
handfuls of cash, or depicting him approving of rioting (Fig. 16b).
                                   
We found 119 meme-style ads in our dataset. Though attack ads and
                                  
smears are fairly normalized, we did not observe the use of memes
                                  
for attacks by any other campaigns. These ads contrast with more
                                  
polished ads placed by other campaigns, and could be misleading if
                                  
users assume meme-style ads are placed by other
                          
 users, not an official political campaign.
                      

```

Figure 17: Landing page of the poll from Figure 9c. Viewers

![18_image_3.png](18_image_3.png) are asked to submit an email address to vote in the poll, and are signed up a newsletter. Prior reporting has shown this is typically a scheme to generate mailing lists and audiences for political campaigns to advertise to. © **rightwing.org**
Misleading Political Polls. Figure 17 shows the landing page of

![18_image_1.png](18_image_1.png)

the misleading political poll depicted in Figure 9c.

Political News and Media. .

![18_image_2.png](18_image_2.png)

Figure 18: Examples of political news and media ads about political outlets and events.

Figures 18a and 18b show examples of political news ads in the outlets, events, and programs subcategory. These ads, rather than advertising a sponsored link to a news article, instead advertise the outlet as a whole, or a larger event or program hosted by the outlet.