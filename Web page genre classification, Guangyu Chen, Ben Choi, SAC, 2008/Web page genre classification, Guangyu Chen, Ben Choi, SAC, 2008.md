# **Web Page Genre Classification**

**Guangyu Chen & Ben Choi**

Computer Science Louisiana Tech University, LA 71272, USA pro@BenChoi.org

**Abstract:** In this paper we present an automatic genre-based Web page classification system. Unlike subject or topic based classifications, genre-based classifications focus on functional purposes and classify web pages into categories such as online shopping, technical paper, or discussion forum. Until now, the genre classifications are not well developed due to the subjectivities and difficulties to define the genre, the features, and even the categories. In this paper, we define five top-level genre categories, each of which has several subcategories, and develop new methods to extract 31 features from Web pages to identify the categories. We analyze not only the contents of the Web pages, but also the URLs, HTML tags, Java scripts, and VB scripts. We developed a genre classification system that achieved average accuracy of 93%. In addition, we combined this genre classification with our subject-based classification to produce a comprehensive Web page classification system.

**Categories and Subject Descriptors:** H.3.3 [**Information Search and Retrieval**]: *Information filtering, Relevance feedback.*

**General Terms:** Algorithms, Design, Experimentation.

**Keywords:** Web Ontology, Semantic Web, Knowledge Classification, Web Mining, Information Retrieval.

## **1. Introduction**

There are two main types of Web page classifications. In subject-based classification (also known as topic-based classification), Web pages are classified according to their contents or subjects [2,3]. Alternatively, some classifications are genre [1,4,6,8,9] or style based focusing on genre related factors, such as document structure or format, purpose of the page, and intended audience.

Genre based classifications are not widely adopted. One reason is that the genre of the Web pages is highly subjective; different people define their own genre differently, making it much harder for a researcher to choose the right approach. Good genre based approaches that can fulfill most users' search requirements are still in development. Most existing approaches have their own deficiencies. For instance, in [1], there are only three categories defined, therefore users cannot find an appropriate category to match the search requirements in most cases. In [9], they concentrate only on organizational member's communication actions like the business or technical report which is not an approach suitable for everyone's needs.

*SAC'08*, March 16-20, 2008, Fortaleza, Ceará, Brazil. Copyright 2008 ACM 978-1-59593-753-7/08/0003…\$5.00.

In this paper, we define "genre" as the Web page's functional purpose provided to Web users. For example, online shopping is the kind of Web pages whose purpose is to allow users to make purchases online. Google's product search is an example of the applications of this type of genre classification. The reason for defining genre in this way is that we care about users' multi-facet search demands for the Web pages. The categories defined in this paper are in a hierarchical structure and are determined by their own functional type. Every category is distinguished from each other by its unique functionality. We also introduce new categories, such as resource download, specialized information search. All the categories and their functional purposes will be discussed in detail in Section 3.1. We also define new features to categorize Web pages. Features such as JavaScript and VBScript methods have not been used in other classification systems. The entire feature set will be introduced in detail in Section 3.2. In addition, we proposed new process to associate features to each defined category. As the results, our proposed system can achieve average classification accuracy of 93% and performed better than related works.

# **2. Related Research**

Structural information of a Web page can help identifying its genre. This approach relies on the features that are apart from text content and classifies Web pages to a particular category that contains Web pages having "common layout". The features affecting the structure include textual features, such as the number and placement of links, image features, such as the histogram of the image's distinct colors, and other features, such as video or other multimedia contents [1]. In [1] a structure based approach is used. There are only three categories defined in the paper: information pages, research pages, and personal home pages. The approach in [7] is very similar to [1]. The Web pages are classified according to the structural characteristics. The categories in [7] are online shopping, product catalog, advertisement, call for paper, links, frequently asked questions, glossary, home page, and bulletin board. The features used in the paper include URL, keyword, image, link, OCR, structure, and plugin [7].

The communicative actions type of Web pages is another kind of genre been used. Paper [9] defines genre as "a type of communication recognized and enacted by organizational members". They provided six questions: why (purpose of communicative action), what (contents of a genre or genre system), who/whom (participants in genre or genre system), when (timing of genre or genre system use), where (place of

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee.

communicative action), and how (the form of genre and genre system) [9]. By answering these questions a category can be described.

Paper [4] defined genre as the dimensions such as the degree of expertise, the amount of detail presented and whether it reports facts or opinions. The expertise dimension is estimated as a function of the frequency and length of document's words [4]. The detail dimension is estimated as a function of the document's physical size, number of lines, and the frequency of long words [4]. The subjective dimension involves the use of shallow linguistics features such as the part-of-speech tags. These dimensions can be very helpful when users care about the degree of expertise.

Some other approaches combined multiple ideas. For example, in [5], Web pages are classified based on the following characteristics: the purpose or function of the page, its intended audience, its surface content or format (e.g. words, tables, sounds, tools, etc.), the type of links it contains, and its relationship to the pages to which it provides the links (e.g. cover page, index, etc.) [5]. The categories in the paper include organizational pages, documentation, text, homepage, multimedia, database entry, and tools.

# **3. Our Genre Classification System**

In this section, we propose a new classification system based on Web page genre. First, we define a hierarchy of genre categories. We also define features that are to be extracted from Web pages. Then, we describe how to use the features to specify each of the categories. We finally describe how to assign a category to a Web page.

### **3.1 Definition of categories**

In our approach, we define the genre according to the functionality of the Web page. Each category is defined based on the functional role it plays to the users. After selecting and analyzing hundreds of popular Web pages and considering user's requirements to these pages, we defined five top-level categories, plus several subcategories under the top-level categories.

**Homepage** is the starting page or portal page to other Web pages. It usually has a menu bar on the top that lets users enter other locations of the Website, and often has some or even abundant images and classified links. According to the different proprietors of homepages, we defined five subcategories: portal Website homepage, university or institute homepage, government or organization homepage, company homepage, and personal homepage.

**Information search page** has the main purpose of letting users search the Web, which includes general purpose search engine and specialized search engine. The general purpose search engines have no content limitation, such as the well-known search site www.google.com. The specialization search engines have their intended scope, for example, www.froogle.com is a search engine for commercial products. An information search page should have a text input area for users to input the query and a submit button.

**Information and resource page** has the common motive of providing certain information or resource to users, which includes subcategories: resource download, pure information page, news report, term paper, frequently asked questions (FAQ). Each subcategory has its own functional purpose and characteristics. For example, a FAQ page gathers a number of frequently asked questions about certain topic and usually organizes all the questions in lists. Most of the questions can be detected by matching the interrogative at the beginning of the sentence and the question mark at the end of the question. In many cases, each question follows "Q:", and each answer follows "A:".

**Table 1.** Weights of each HTML file feature in each category

|          | Feature                                |              | Online       | Discus.    | Univ.      |                     |
|----------|----------------------------------------|--------------|--------------|------------|------------|---------------------|
| No.      | Name                                   | Type         | shopping     | forum      | home       | FAQ                 |
|          |                                        |              |              |            | page       |                     |
| 1        | Price                                  | Text         | 5            | -0.5       | 0          | -0.5                |
| 2        | Tel. No.                               | Text         | -0.5         | 0.875      | 0.5        | 0.375               |
| 3        | Email link                             | Text         | -0.375       | -0.5       | -0.45      | -<br>0.625          |
| 4        | Copyright                              | Text         | -0.25        | 0.125      | 0.9        | -<br>0.125          |
| 5        | Alert                                  | JavaScript   | -0.1         | 0.1        | -0.9       | -0.9                |
| 6        | Confirm                                | JavaScript   | -1           | -0.875     | -1         | -1                  |
| 7        | Open<br>window                         | VBScript     | -0.625       | -0.625     | -<br>0.875 | -<br>0.875          |
| 8        | Prompt                                 | VBScript     | -1           | -1         | -1         | -<br>0.875          |
| 9        | Input box                              | HTML         | -0.2         | 0.1        | 0.05       | -0.1                |
| 10       | Message box                            | HTML         | 0.3          | 0.5        | -0.9       | 0.2                 |
| 11       | Checkbox;<br>select; ratio<br>button   | HTML         | 0.2          | 0.525      | 0.125      | -<br>0.625          |
| 12       | Submit;<br>custom<br>submit            | HTML         | 0.25         | 0.525      | 1          | -0.8                |
| 13       | Email                                  | HTML         | -0.875       | -0.5       | -0.75      | -0.5                |
| 14       | Frame                                  | HTML         | -0.875       | -1         | -1         | -1                  |
| 15       | Hyperlink                              | HTML         | 0.005        | 0.004      | 0.005      | 0.005               |
| 16       | Link to ftp                            | HTML         | -1           | -1         | -1         | -<br>0.875          |
| 17       | List                                   | HTML         | -0.675       | -0.99      | -0.1       | 1                   |
| 18       | Password                               | HTML         | -1           | -0.625     | -1         | -1                  |
| 19       | Reset                                  | HTML         | 0.1          | -0.9       | -1         | -0.5                |
| 20       | Style sheet                            | HTML         | -0.375       | -0.5       | 0.125      | -0.5                |
| 21       | Table                                  | HTML         | 0.875        | 0.875      | 0.625      | 0.6                 |
| 22       | Text area                              | HTML         | -1           | -0.75      | -1         | -1                  |
| 23       | Text input                             | HTML         | 0            | 0          | 1          | -0.65               |
|          |                                        |              |              |            |            |                     |
| 24       | Image link                             | HTML         | 0.325        | 0.65       | 0.625      | 0.475               |
| 25<br>26 | Image<br>Date                          | HTML<br>Text | 0.1<br>-0.25 | 0.088<br>5 | 0.1<br>0.3 | 0.063<br>-<br>0.625 |
| 27       | Time                                   | Text         | 0            | 1          | 0          | 0                   |
| 28       | Question<br>sentence                   | Text         | 0            | 0          | 0          | 5                   |
| 29       | Postfix:<br>.edu;<br>.ac.uk;<br>.ac.jp | URL          | 0            | 0          | 100        | 0                   |
| 30       | Directory:<br>forums;<br>forum         | URL          | 0            | 100        | 0          | 0                   |
| 31       | Directory:<br>FAQ; faqs                | URL          | 0            | 0          | 0          | 100                 |

For another example, the Web pages of news report also tend to have some common characters. The title of the news should appear in the top, probably in a bigger font, and then followed by the author's name and the date/time it was released. Images are sometimes embedded in the content. After the news, there are several links to other related news.

**Online shopping** is quite popular today, and the functions are very clear: show products to users, let them search the products they want, select the products they like, calculate the cost, and finally let them submit their order. To achieve all the functions, typical online shopping Web pages have several common traits. There are plenty of price information and clickable images which can show some larger images or link to a specific product page. And there are also some submit buttons or customized submit buttons which let users add the product to shopping cart or submit the order by just clicking it. Some powerful online shopping Web pages also include a simple search engine.

**Discussing forum** is also very popular today. This type of Web pages let users exchange opinions on variety of topics by reading others opinion and posting their own. It often arranged in a table format, and each row for one topic which has the date and time of the last post and the link which links to all the posts of the topic. Some pages have a place for quick reply, which consists of several text input areas and at least two submit buttons, one for submitting the input and one for clearing the text.

#### **3.2 Feature Extraction from Web Pages**

We develop new methods to extract features from Web pages to identify the categories. We analyze not only the contents of the Web pages, but also the URLs, HTML tags, Java scripts, and VB scripts. The following are several principles we used to select features: (1) The features should be detectable; (2) The computational cost of detecting each feature should be inexpensive. (3) The features should bring some benefit for classification purpose. (4)The features should follow the idea of Web page genre classification, and not involve the features that used for subject-based

![](_page_2_Figure_5.jpeg)

**Fig. 1.** Estimation of feature weights and threshold

approach. This principle is useful when we combine the genre classification with subject-based approach.

Following these principles, we determined the whole feature set by gathering hundreds of Web pages of various categories and analyzing the URLs, the HTML files, and the embedded scripts. We developed methods to extract 31 features from text, HTML, scripts, and URLs (see Table 1).

**URL:** two types of features extracted from URLs are the postfix and the directory. The general format of a postfix feature is *dot abbreviation* or *dot abbreviation dot abbreviation.* For example, the postfixes ".edu", ".ac.uk", and ".ac.jp" indicate Web pages belong to university or academic Websites. The common format for a directory feature is *word (abbreviation) slash.* The directory name, such as FAQ or forum, can give clues to the categories of the Web pages.

**Text:** we use regular expressions to extract features, such as price, phone number, date, and time from text portions of the Web pages. For example, price is composed of dollar sign or other currency sign followed by digits.

**HTML:** since it is a tagged language, the first thing of HTML feature extraction is to recognize the HTML tags. We extract features, such as input box, table, submit button, and image link.

**Script language:** the primary script languages embedded in HTML are JavaScript and VBScript. We selected some methods of the script languages as the script features. A script in HTML is defined with the <script> tag, and the type language attribute specifies the script language, such as <script type="text/javascript">. Once we locate the scripts in one HTML file, the next thing is to extract the scripts features in them by matching the method names and the parameters format. For example, the alert function can be recognized by the name "alert" and followed by the alert message.

#### **3.3 Association of features to each category**

To build the genre classification system, we first need to determine how to specify each category using the given features. There are two major stages: (1) estimation of feature weights and threshold and (2) fine tuning the feature weights and threshold.

The first stage is to get the approximate value of parameters including threshold and feature weights. The process in this stage is shown in Fig. 1. First, we select Web pages to be used as the training dataset and create a file containing the list of these Web page URLs. Then, a Web page download module reads the URLs in that file and downloads the HTML files. After getting all HTML files, the average file size is calculated. Based on the average file size, we estimate an original value of threshold. Then the HTML files are passed to an HTML feature extraction module, by which each feature's occurrence frequency in each category is calculated. The initial value of each feature's weight in each category was defined by the occurrence frequency in the category. The formula to calculate the initial weights is:

Weight (C<sup>i</sup> , Fj) = ( 2 Freq(C<sup>i</sup> , Fj) – N(Ci) ) / N(Ci)

- Weight (C<sup>i</sup> , Fj) is the feature Fj's weight in category Ci.
- Freq (C<sup>i</sup> , Fj) is the occurrence frequency of the feature F<sup>j</sup> in the category C<sup>i</sup> .

 N (Ci) is the number of Web pages of category C<sup>i</sup> in the training set.

The second stage for associating features to each category is to fine tuning the initial values of threshold and features weights produced from the first stage. Fig. 2 shows the process. The URLs of Web pages in training dataset are first provided to both the Web page download module and URL feature extraction module. The Web page download module takes the URL and downloads the HTML file and then passes the file to a HTML feature extraction module, which analyzes HTML file and detects the feature frequencies. Meanwhile, the URL feature extraction module takes the URL as input and detects the URL features. Both the HTML and the URL feature frequencies are passed to the sum generation module, which takes all the feature frequencies and receives the feature weights according to each category. Then two things will be done in this module, first is to calculate the sums of the feature weights in each category, then the highest one will be selected and passed to the result processing module, which receives the highest score, normalizes it, and then compares the normalized score to the threshold. If the score is not higher the threshold, then the Web page will be considered not belonging to any of the existing categories and labeled as "other"; otherwise the page will be classified to the category which has the highest score.

We then manually check the final classification results and adjust the threshold and features weights to optimize the classification system. The weights initially are all ranging from -1.0 to 1.0, where negative indicates negative contribution to the category. For the fine tuning, we choose one key feature from each category and increase the weight to 5. This is based on an assumption that most of the

![](_page_3_Figure_3.jpeg)

categories have their unique feature that may represent themselves best and distinguish from other categories. Then we ran the classification system on the training dataset to check the likely value. The classification results were checked, and the errors were analyzed and used as the feedback to modify the weights again. It is necessary to repeat the whole fine tuning process many times in order to achieve the best performance.

The results of one of our experiments are shown in Table 1. In the experiment, we chose four categories for testing and evaluation purpose. These four categories are online shopping, discussion forum, university homepage, and frequently asked questions. The actual values of the weights for each feature in each category are showed in Table 1. Considering the uniqueness and importance of the features in URL, we assigned a weight of 100 to each of them. The high weight will not offset the balance of the URL feature with other features in Table 1, since the other weights usually are multiplied with high frequency of occurrences.

Besides fine tuning the feature weights, we also need to fine tune the threshold, which is used to distinguish whether a Web page belongs to the defined genre categories or not. The value of the threshold is very important since it will significantly influence the performance of the classification system. We use the precision, recall, and F-measure to describe the performance [3]:

$$\begin{array}{l} \text{Precision} = \text{a} \land (\text{a} + \text{b})\\ \text{Recall} = \text{a} \land (\text{a} + \text{c}) \end{array}$$

a: the number of testing examples correctly assigned to the category; b: the number of testing examples incorrectly assigned to the category; c: the number of testing examples incorrectly rejected to the category

F = 2 \* (recall \* precision) / (recall + precision) For our experiments, when the value of the threshold increases, the precision will increase, but the recall will decrease. To keep a balance between the precision and recall, the threshold can not be too high or too low. Fmeasure combines precision and recall, and allow us to keep a balance between them by adjusting the threshold to maximize the value of F-measure. For our training dataset, the best performance happens when the threshold is set to 15, using which the average of the F-measure is high, and the distributing of the F-measure does not result in any category having a significantly low F-measure.

#### **3.4 Genre Classification of Web Pages**

After we associated features to each category and fine tuning the feature weights and the threshold, we are now ready to classify new Web pages. The classification process is shown in Fig. 3. This process is similar to the fine tuning process except we do not modify the weights and the threshold. The URL of the Web page to be classified is first given. The features of the Web page is extracted and weighted. The total weight for each category is calculated and the highest one is selected. The highest weight is then **Fig. 2.** Fine tuning feature weights and threshold normalized by the size of the HTML file of the Web page. If

![](_page_4_Figure_0.jpeg)

**Fig. 3.** Process for classifying new Web pages

this normalized weight is larger than the threshold, then the Web page is classified to the category that has the high weight; otherwise it is considered not belonging to any defined genre categories.

## **4. Evaluation and Test Results**

To evaluate our genre classification system, we performed experiments and compared our results to two related papers. To insure accuracy, the testing dataset is completely different from the training dataset. We gathered 1000 testing Web pages, from the Internet, chosen from four categories: online shopping, discussion forum, university homepage, and frequently asked questions. In order to show the fullscale performance of the system, we also mixed a number of Web pages that do not belong to any of the four categories. The results of training and fine tuning of the feature weights are shown in Table 1. The classification accuracy of our system is shown in Fig. 4. The results for comparing our approach to two related works [1, 7], is shown in Table 2 and 3. Based on the results, we can draw two conclusions. One is our approach is proved to be practical; the whole system achieves a good performance. Another is our system is more accurate than the work in [1] and [7], which shows our approach is viable.

![](_page_4_Figure_5.jpeg)

**Fig. 4.** Classification accuracy using F-measure

| Table 2. Comparison | with results in [1] |  |
|---------------------|---------------------|--|
|                     |                     |  |

|                  | Results in [1] | Our results | Difference |
|------------------|----------------|-------------|------------|
| Average accuracy | 87.83%         | 93.25%      | + 5.42%    |

| Table 3. | Comparison with results in [7] |  |  |
|----------|--------------------------------|--|--|
|          |                                |  |  |

|                   | Results in | Our     | Difference |
|-------------------|------------|---------|------------|
|                   | [12]       | results |            |
| Highest precision | 90%        | 97.4%   | +7.4%      |
| Lowest precision  | 72%        | 75%     | +3%        |
| Average precision | 81%        | 90.6%   | +9.6%      |
| Highest recall    | 100%       | 96%     | -4%        |
| Lowest recall     | 79%        | 89%     | +10%       |
| Average recall    | 89.5%      | 93.25%  | +3.75%     |
| Highest F-measure | 84%        | 94%     | +10%       |
| Lowest F-measure  | 67%        | 84%     | +17%       |
| Average F-measure | 75.5%      | 91%     | +15.5%     |

## **5. Conclusion and Future Research**

This paper proposes a new automatic genre-based Web page classification system, which can work either independently or in conjunction with other topic-based Web page classification systems. New categories and features are introduced. The proposed system can achieve average classification accuracy of 93% and performed better than related works.

To achieve the high accuracy, the system currently requires considerable manual fine tuning of the feature weights and the threshold during the training phase. Since the Web is dynamically changing, new features will appears and new categories need to be defined. When new features and new categories are added into the system, in addition to determining the weights of the new features, the existing feature weights and the threshold should also be modified. To keep up the changes, future research should seek to develop more automated training and fine tuning process.

# **References**

- 1. Asirvatham, A.and Ravi, K. "Web page classification based on document structure," IEEE National Convention, Dec 2001.
- 2. Choi, B. and Peng, X. "Dynamic and Hierarchical Classification of Web Pages," *Online Information Review,* Vol.28, No.2, pp. 139-147, 2004.
- 3. Choi, B. and Yao, Z. "Web page classification," book chapter in "*Foundations and Advances in Data Mining*," Springer-Verag 2005.
- 4. Dimitrova, M., Finn, A, Kushmerick, N. and Smyth, B. "Web genre visualization," Smart Media Institute, Proc. conference on Human Factors in Computing Systems, Minneapolis, 2002.
- 5. Haas, S. and Grams, E. "Page and link classifications: connecting diverse resources," ACM DL, 99-107, 1998.
- 6. Kwanik, B. and Crowston, K. "Genres of digital documents: Introduction to the Special Issue" Information, Technology & People, 18(2), 76-88, 2005.
- 7. Matsuda, K., Toshikazu, and Fukushima "Task-oriented world wide web retrieval by document type classification," in Proceedings of the 8th international conference on Information and knowledge management, 109-113, 1999.
- 8. Stamatatos, E., Fakotakis, N. and Kokkinakis, G. "Automatic text categorization in terms of genre and author," Computational Linguistics, Vol. 26, Issue 4, 471-495, Dec 2000.
- 9. Yoshioka, T. and Herman, G. "Genre taxonomy: a knowledge repository of communicative actions," ACM transactions on information system, v. 19, n. 4, 431-456, 2001.