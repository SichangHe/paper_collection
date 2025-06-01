Contents lists available at ScienceDirect

![](_page_0_Picture_2.jpeg)

# Pattern Recognition Letters

![](_page_0_Picture_4.jpeg)

journal homepage: www.elsevier.com/locate/patrec

# Enhancing the identification of web genres by combining internal and external structures

![](_page_0_Picture_7.jpeg)

## Chaker Jebari<sup>∗</sup>

*University of Technology and Applied Sciences, College of Applied Sciences, IBRI, Oman*

### a r t i c l e i n f o

*Article history:* Received 22 September 2020 Revised 14 January 2021 Accepted 6 March 2021 Available online 13 March 2021

*MSC:* 41A05 41A10 65D05 65D17

*Keywords:* Web genre identification Combination Dempster Shafer theory OWA operators

### **1. Introduction**

With the exponential increase of information on the web, the majority of existing search engines return a huge ranked list of web pages matching a user's query. In front of this huge list of pages returned, it is very difficult to find the desired information quickly and efficiently. For example, searching for the keywords "*machine learning*" will provide a huge list of web pages containing the words "*machine*" and "*learning*". These pages belong to different genres such as *Course page, department page, Conference page, Research group page, blogs*, etc. A user looking for a course about machine learning has to view all web pages returned, which are of different genres. One way to solve this problem is to classify web pages with respect to many aspects such as topic, sentiment, genre, etc. [15]. In the last decade a lot of studies have been conducted to classify web pages and most of them have been focused on topic classification and only few studies have been dedicated to genre classification of web pages. It has been showed that genre classification of web page can improve the retrieval quality of search engines. For example, Stein [21] proposed a new technology called WEGA (Web Genre Analysis) to label Web search results with genre information. This new technology can help user to find

*E-mail address:* chaker.ibr@cas.edu.om

## a b s t r a c t

Automating the identification of the genre of web pages becomes a promising research area in web pages classification, as it can be used to improve the quality of the web search result and to reduce search time. Many studies have been proposed to identify the genre of web pages. These studies differ with respect to three main factors which are the features used, the classification algorithm and the list of genres used for the evaluation. The main idea of this paper is to combine the predictions produced by different classifiers using the internal and external structures of a web page. To combine the predictions of the different classifiers we used different OWA operators and the Dempster-Shafer (DS) combination rule. Moreover, we proposed an improved DS combination method based on the ranks of the predicted genres. The experiments conducted using the two known datasets (KI-04 and SANTINIS), show that our study achieves better results in comparison with other ensemble classifiers and genre identification works as well.

© 2021 Elsevier B.V. All rights reserved.

the desired genres quickly among a huge list of pages returned by a search engine. To filter out conflicting, ambiguous and inconsistent web pages returned by a search engine, Agrawal et al. [2] proposed recently a framework to assess the credibility of the content of a web page based on its genre. Their study shows that the importance of each used credibility parameter varies with the genre of a web page.

So far, many definitions of the concept *genre* have been proposed and no one is considered as a standard definition. According to Shepherd and Watters [20], the genres found in web pages (also called cybergenres) are characterized by the triple < *content*, *f orm*, *f unctionality* >. The content and form attributes are common to non-digital genres and refer respectively to the text and the layout of the web page. The functionality attribute concerns exclusively the digital genres and describes the interaction between the user and the web page. It has been stated by Santini [17], that hybridism and individualization are two important aspects that should be taken in consideration when dealing with web genres. Genre hybridism refers to the existence of multiple genres across the different sections of a web page, while individualization refers to the absence of any recognized genre in a web page, hence the need for a zero-to-multi-genre classification scheme in which a web page can be assigned to zero or multiple genres. Recently Madjarov et al. [10] shows that structuring web genres as a

<sup>∗</sup> Corresponding author.

hierarchy yields best predictive performance across different predictive models and features.

A broad number of studies on genre classification of web documents have been proposed in the literature (See [17]). These studies differ mainly with respect to three factors:1) The feature set used to represent web documents, 2) The classification algorithm and 3) The list of genres used to evaluate the classification performance.

In comparison with the previous studies on genre identification, our paper has made the following contributions:

- We propose to use the terms extracted from the internal and external structures of a web page to identify its genre.
- To achieve better performance, we propose to combine the evidences assigned to all genres by different classifiers using an improved Dempster-Shafer combination method called rankbased evidential combination.
- We compared the proposed combination method with Dempster-Shafer and Murphy combination methods and OWA operators as well.
- We compared the proposed method with other ensemble classifiers.

The remainder of this paper is organized as follows. Section 2 presents the previous works on genre classification of web pages. Section 3 describes the proposed framework. Section 4 explains the different combination techniques used in our framework as well as the new evidential combination technique. Section 5 discusses the evaluation of our approach. Finally, Section 6 summarizes the main points of this paper and suggests some future works.

#### **2. Previous works on web genre identification**

As stated in the previous section, many studies have been proposed to identify the genre of web documents and they differ with respect to the following three factors: 1) The feature set use to represent web documents, 2) The classification algorithm used and 3)The list of genres used to evaluate the classification performance.

The first factor concerns the features used in genre classification, which can be grouped into four main groups: surface features (e. g. genre specific words, punctuation marks, document length, sentence length, etc.), structural features (e. g. Parts Of Speech (POS) tags, tense of verbs, etc.), presentation features (e. g. the number of images, number of links, etc.) and contextual features (e. g. URL, keywords, etc.). For textual documents, other types of features have been used such as discourse relations and markers [5] and semantic features ([4], [23]).

The second factor is the classification algorithm which is often based on single-label classification schema such as Naive Bayes (NB), K-Nearest Neighbour (KNN), Decision Trees (DT), Support Vector Machine (SVM), Neural Networks (NN), etc. [18]. Only few studies have adopted multi-label classification schema such as [8,17,22]. The issue of these studies is the lack of standard multilabel datasets that can be used for comparison and the only available dataset is the MGC dataset[22]. It is also worth noting that most of studies on web genre identification adopted a closedset experimentation setup where a web page should be assigned to one ore more genres from a list of predefined list of genres. To deal with the evolution of web genres, Pritsos and Stamatatos [14] adopted an open-set classification experimentation setup, where it is possible for some web pages not to be assigned to any predefined genre and therefore it can be seen as noise.

The third factor that differentiates the different genre classification studies is the list of genres (also called genre palette) used for the evaluation. Many genre datasets have been compiled to evaluate genre identification task such as KI-04, SANTINIS, MGC, Syracuse, KRYS-I, etc. These datasets differ in terms of the number of web documents, the document format, the set of genre labels and how the web pages were collected and annotated [3]. It is worth mentioning that until now, there is no a standard dataset where the examples are distributed across an exhaustive list of web genres. In order to compare our study with other works, we used in this paper the two most common used datasets KI-04 [6] and SAN-TINIS [17].

Table 1 summarizes the different studies on web genre identification who used KI-04 and/or SANTINIS datasets in their experimentations. For each study we mentioned the different features used, the machine learning algorithm, the datasets used in the evaluation and the results achieved.

Compared to the previous works illustrated in Table 1, this paper propose a framework that combines the terms extracted from the internal and external structures of the web page. To our knowledge, this is the first study that exploits the internal and external structures of a web page to identify its genre. To improve the performance, multiple classifiers are trained with different features and their outputs are combined using an improved DS combination rule.

#### **3. Proposed framework**

The aim of our proposed framework is to identify the genre of a web page using its internal and external structures extracted from the headings and the hyperlinks. This two types of features are used to train multiple classifiers. Our framework has three main modules: 1) Extraction of web page structures, 2) Selection of the best classifiers for each type of web page structure and 3) Combination of the predictions of the selected classifiers to obtain a final and single prediction.

#### *3.1. Extraction of web structures*

A web page is a collection of information displayed to the user through a web browser. This information can be of different types such textual, visual or aural. To be well disseminated, the content of a web page is structured using different HTML elements. We can notice that a web page has two types of structures: internal and external. Oftenly, the internal structure is represented by a set of terms enclosed between headings <Hi>... </Hi> where i=1, ...,6. The external structure represents the links of a given page to other external web pages and it is represented by a set of hyperlinks. We notice that the internal and external structures are different from each genre. Hence, headings and hyperlinks can be used to reveal the genre of the web page. It is also worth noting that in some web pages, the internal structure can be represented by hyperlinks rather than headings, while in other web pages we may found the opposite. In this study, each structure is represented by the set of terms extracted and then processed to remove the stop words and the words that appear in less than 10 web pages. After stemming the remaining words, we applied *TFIDF* weighting scheme to reflect the importance of each term [18].

#### *3.2. Selection of the best classifiers*

To select the best classifiers for each type of web page structure, we trained *N* different base classifiers on the same training dataset. These base classifiers have been used in the previous studies about web genre identification. At the end we will get *N* different classification models from which we can select the best classifier for each type of web page structure.

**Table 1**

Previous works on web genre identification .

| Study | Features                                                                                                         | Algorithm                                                                                           | Dataset                                      | Results                                                                                                  |
|-------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------|----------------------------------------------------------------------------------------------------------|
| [6]   | HTML tag frequencies, classes of words<br>(names, dates, etc.), frequencies of<br>punctuation marks and POS tags | Discriminant Analysis                                                                               | KI-04                                        | accuracy=0.7                                                                                             |
| [7]   | Words extracted from URL, title, headings and<br>anchors                                                         | Centroid-based                                                                                      | KI-04 and WebKB                              | micro-BEP=0.81 using URL,<br>micro-BEP=0.85 using headings,<br>micro-BEP=0.83 using anchors              |
| [9]   | Character n-grams extracted from text and<br>structure                                                           | SVM                                                                                                 | KI-04 and MGC                                | micro-recall=0.55,<br>micro-precision=0.74, micro-F1=0.6                                                 |
| [11]  | character n-grams extracted from the textual<br>content                                                          | Centroid-based                                                                                      | SANTINIS                                     | F-measure=0.84                                                                                           |
| [17]  | Most frequent English words, HTML tags, POS<br>tags, punctuation symbols, genre-specific core<br>vocabulary      | SVM                                                                                                 | SANTINIS and<br>KI-04                        | accuracy=0.86 using SANTINIS,<br>accuracy=0.7 using KI-04.                                               |
| [1]   | character n-grams extracted from URL                                                                             | SVM                                                                                                 | Syracuse and<br>SANTINIS                     | Micro-F1=0.28 using Syracuse and<br>Micro-F1=0.46 using SANTINIS                                         |
| [28]  | On-Page features+information extracted from<br>the neighboring pages                                             | Combined approach                                                                                   | KI-04 and<br>SANTINIS                        | F1 score=0.7 using KI-04, F1<br>score=0.8 using SANTINIS                                                 |
| [13]  | Character 4-grams, Words uni-grams                                                                               | two ensemble classifiers (One-class SVM<br>(OCSVM) and Random Feature Subpacing<br>Ensemble (RFSE)) | KI-04 and<br>SANTINIS                        | F1 score=0.76 using SANTINIS and<br>RFSE classifier                                                      |
| [14]  | Character 4-grams, Word unigrams, Word<br>3-grams, Part-of-speech 3-grams                                        | two ensemble classifiers (One-class SVM<br>(OCSVM) and Random Feature Subpacing<br>Ensemble (RFSE)) | KI-04 and Modified<br>version of<br>SANTINIS | F1 score=0.787 using SANTINIS and<br>RFSE classifier, F1 score=0.643 using<br>KI-04 and OCSVM classifier |

#### *3.3. Combination of classifiers predictions*

Based on the assumption that each source of information provides a different view point, a combination has the potential of providing better results than any single classifier. There are various methods to combine classifiers [16]. These methods can be classified according to the type of classifier output. Generally, classifiers can be combined at different output levels: abstract level, ranking level and measurement level. The measurement level is expected to be the most effective, since it uses all information available. Many techniques have been used to combine classifiers at measurement level such as Fuzzy template, Average bayes combination, Fuzzy integrals, Product of experts, OWA operators, Dempster-Shafer, etc. [16].

#### **4. Combination techniques used**

In this paper we used the most common measurement level combination techniques (OWA operators and Dempster-Shafer). We proposed a new evidential combination technique. The proposed technique is compared with Dempster-Shafer and Murphy combination techniques and OWA operators as well.

#### *4.1. OWA operators*

Ordered Weighted Averaging (OWA) operator is a very common aggregation operator first introduced in [24]. An OWA operator of dimension *n* is a mapping *F* : [0, 1]*<sup>n</sup>* −→ [0, 1] associated with a weighting vector *W* = [*w*1, ... , *wi*, . . ., *wn*], where *wi* ∈ [0, 1] and *n <sup>i</sup>*=<sup>1</sup> *i* = 1. The combination of *n* elements *a*1, . . ., *ai*, . . ., *an* is given as follows:

$$F(a\_1, \ldots, a\_i, \ldots, a\_n) = \sum\_{i=1}^n \mathbf{w}\_j \mathbf{b}\_j \tag{1}$$

Where *bj* is the *j th* larget of the *ai*.

In this paper we used the most common operators which are min, max and average. The min operator is obtained if *wn*=1 and *wi*=0 for *i* = *n*. The max operator is obtained if *w*1=1 and *wi*=0 for *i* = 1. The average operator is obtained if *wi* = <sup>1</sup> *<sup>n</sup>* ∀*<sup>i</sup>* <sup>∈</sup> [1, *<sup>n</sup>*]

#### *4.2. Evidential combination*

*4.2.1. Basics of DS theory of evidence*

In Dempster-Shafer (DS) theory (called also evidential theory), a universe is represented by a finite set 2 of mutually exclusive and exhaustive hypotheses, called frame of discernment [19].

The power set 2 is the set of all possible subsets of including the empty set {Ø} . The theory of evidence assigns a mass value *m* between 0 and 1 to each subset of the power set using a mass function (called also, basic probability assignment) as follows:

$$\{m: 2^{\Theta} \to [0, 1] \,\tag{2}$$

Where *m*(Ø) = 0 and - *A*∈2*m*(*A*) = 1

All subsets *A* ⊆ -, for which *m*(*A*) > 0 are called focal elements. The combination of the two masses *m*<sup>1</sup> and *m*<sup>2</sup> is computed as follows:

$$m\_{12}(\oplus)(\mathcal{X}) = \frac{1}{1 - K} \sum\_{\substack{A, B \in \Theta, A \sqcap B = X}} m\_1(A) \cdot m\_2(B) \tag{3}$$

Where *X* ⊆ and *X* = -

*K* is the degree of conflict between the mass functions and is defined as follows:

$$K = \sum\_{A,B \in \Theta, A \cap B = X} m\_1(A) \cdot m\_2(B) \tag{4}$$

The combination rule can be easily extended to several mass functions by repeating the rule for new mass functions. Thus the combination of *n* mass functions *m*1, *m*2, . . ., *mn*, can be formed as follows:

$$\mathfrak{m} = \mathfrak{m}\_1 \oplus \mathfrak{m}\_2 \oplus \cdots \oplus \mathfrak{m}\_n = [\cdots[[\mathfrak{m}\_1 \oplus \mathfrak{m}\_2] \cdots \cdots \mathfrak{m}\_n]] \tag{5}$$

#### *4.2.2. Rank-based evidential combination*

Despite its wide use in many fields of information fusion, DS combination rule may produce counter-intuitive results when used to combine very conflicting evidences [26]. To solve this problem, several methods have been proposed in the literarture which can be classified into two categories. The first category of methods consists in changing the DS combination rule. This category of methods are not preferred because sometimes they can violate the theoretical properties of DS combination rule like commutativity and

#### **Table 2**

Composition of KI-04 and SANTINIS datasets .

| Genre                 | # of pages | Genre                | # of pages |
|-----------------------|------------|----------------------|------------|
| Article               | 127        | Blog                 | 200        |
| Download              | 152        | Eshop                | 200        |
| Discussion            | 127        | FAQ                  | 200        |
| Portrayal-private     | 131        | Newspaper front page | 200        |
| Portrayal-non-private | 179        | Personal home page   | 200        |
| Link collection       | 208        | Listing              | 200        |
| Help                  | 140        | Search page          | 200        |
| Shop                  | 175        |                      |            |
|                       |            |                      |            |

associativity [27]. The aim of the second category of methods is the modification of original evidences before combination. This kind of methods is the most common and it modify the propositions so that conflict among the evidences are resolved before applying the DS combination rule. Many methods have been proposed [25]. The most common one is Murphy' method [12] which consists in averaging the bodies and then apply DS combination rule on the averages of evidences. In this paper we propose a new DS combination method that uses the rank of each genre to modify the evidences before applying the DS combination method.

Assume we have *n* possible labels {*l*1, . . ., *ln*}. For a given instance *x*, the output of a classifier *hk* is given as follows:

$$h\_k(\mathbf{x}) = \{m\_k^1, \dots, m\_k^i, \dots, m\_k^n\} \tag{6}$$

Where *n <sup>i</sup>*=<sup>1</sup> *m<sup>i</sup> <sup>k</sup>* <sup>=</sup> <sup>1</sup> and *<sup>m</sup><sup>i</sup> <sup>k</sup>* is the evidence associated to the label *i* by the classifier *hk*.

The first step in our new technique is to sort descendingly the evidences produced by each classifier and get their ranks as follows:

$$r\_k(\mathbf{x}) = \{r\_k^1, \dots, r\_k^i, \dots, r\_k^n\} \tag{7}$$

Where *r<sup>i</sup> <sup>k</sup>* <sup>∈</sup> <sup>1</sup>, . . ., *<sup>n</sup>* is the rank of the evidence *<sup>m</sup><sup>i</sup> <sup>k</sup>* assigned to the label *i* by the classifier *hk*.

The second step is to modify each evidence using its rank as follows:

$$h\_k(\mathbf{x}) = \{\frac{m\_k^1}{r\_k^1}, \dots, \frac{m\_k^i}{r\_k^i}, \dots, \frac{m\_k^n}{r\_k^n}\} \tag{8}$$

The main objective of our method is to give more support to higher evidences. So that the highest evidences which have the highest ranks are not affected, whereas small evidences are diminished. Finally, all evidences are normalized and averaged and then the DS combination rule is applied.

### **5. Experimentations**

To discuss our approach in depth, we firstly evaluate the performance of individual classifiers on internal and external structures. Secondly, we evaluate the combination of the best individual classifiers using OWA operators and evidential combination. In addition, a comparison is performed against existing works. To be able to compare our results against existing studies, we used the most common metrics in the previous studies (accuracy, Micro-F1 and Macro-F1) [18].

#### *5.1. Datasets*

In our experimentation, we used the two most common datasets used in genre identification (KI-04 and SANTINIS) modified by [17] (See Table 2). KI-04 dataset is composed of 1239 HTML web pages distribuited across 8 genres. While SANTINIS dataset is composed of 1400 HTML web pages distributed equally over 7 genres.

**Table 3**

Number of terms extracted for each type of structure and for each dataset.

|                              | KI-04 | SANTINIS |  |
|------------------------------|-------|----------|--|
| Internal Structure           | 4225  | 128      |  |
| External Structure           | 2186  | 2396     |  |
| Internal+External Structures | 4777  | 2451     |  |
| Full content                 | 4124  | 5533     |  |
|                              |       |          |  |

![](_page_3_Figure_22.jpeg)

![](_page_3_Figure_23.jpeg)

**Fig. 1.** Performance for different classifiers using the internal structure.

After removing stop words and the words that appear in less than 10 web pages, the remaining words are stemmed and weighted using *TFIDF* scheme. The number of terms obtained for internal and external structures and the complete content of web pages are shown in Table 3.

#### *5.2. Results and discussion*

### *5.2.1. Evaluation of individual classifiers*

In this experimentation we consider the six most common classifiers used in the previous works on genre identifications: Support Vector Machine (SVM), Decision Trees (DT), Naove ˙ Bayes (NB), K-Nearest Neighbour (KNN), Multi-layer Perceptron (MLP), Linear Discriminant Analysis (LDA). To train and test these classifiers we used the Python library sklearn1. These classifiers are used using their default parameter settings. In this experimentation, we adopted 10-fold cross validation to split the datasets for training and testing subsets.

The results achieved using the internal structure are illustrated in Fig. 1 for KI-04 and SANTINIS datasets. We can observe that for KI-04 dataset, MLP achieves the best performance. While for SAN-TINIS dataset, the best results are obtained using DT classifier.

<sup>1</sup> https://scikit-learn.org/

![](_page_4_Figure_1.jpeg)

![](_page_4_Figure_2.jpeg)

**Fig. 2.** Performance for different classifiers using the external structure.

With respect to all individual classifiers, we observe from Fig. 1 that the performances achieved using KI-04 dataset is higher than those achieved using SANTINIS dataset. This can be explained by the fact that the genres contained in KI-04 dataset are mostly traditional genres adapted to the functionality of the web such as "article" genre[17]. For this kind of genres, web pages are usually less connected to other pages and therefore contain less number of hyperlinks and more textual content. In this kind of genres, the structure of a web page is mostly reflected by its headings. This can be also justified by the higher number of terms extracted from the internal structure shown in Table 3.

The results achieved using the external structure are illustrated in Fig. 2 for KI-04 and SANTINIS datasets. We can see that for both KI-04 and SANTINIS datasets, MLP achieves the best performance. With respect to all individual classifiers, we observe from Fig. 2 that the performances achieved using SANTINIS dataset is higher than those achieved using KI-04 dataset. This can be explained by the fact that the genres contained in SANTINIS dataset are either emergent or spontaneous, in the sense that they totally dependent on the new medium and they do not have antecedent in paper genres [17]. The web pages belonging to this kind of genres are usually connected to other pages and therefore their structures are reflected by the hyperlinks that contain. This can be also justified by the higher number of terms extracted from the external structure shown in Table 3.

The performances achieved by combining all terms extracted from the internal and external structures are illustrated in Fig. 3. It is clear that the obtained results are less than those obtained using the terms extracted from each structure separately. Hence, the need to combine the results obtained from each type structure. Moreover, we can observe that the results achieved using KI-04 dataset is higher than using SANTINIS dataset. This is can be explained by the fact that the web pages in KI-04 are more structured than those in SANTINIS.

![](_page_4_Figure_9.jpeg)

![](_page_4_Figure_10.jpeg)

![](_page_4_Figure_11.jpeg)

**Fig. 3.** Performance for different classifiers using internal and external structures.

The results achieved using the full text of the web page are illustrated in Fig. 4 for KI-04 and SANTINIS datasets. We can see that for KI-04 dataset, the results achieved using full text are higher than those obtained using external structure for all classifiers. However, they are lower than those obtained using internal structure for all classifiers. For SANTINIS dataset, the results using full text are much higher than using internal structure for all classifiers. In comparison with the results reported using the external structure, we can say that all classifiers achieve higher results except SVM, NB and KNN classifiers. This result is due to fact that the full textual content of a web page contains terms which are useful to identify topic of the web page rather than its genre. It is also worth mentioning that the terms contained in the internal and external structures are mostly genre oriented terms and can be used to reveal the genre of the web page.

#### *5.2.2. Evaluations of combined classifiers*

In this experimentation we evaluated the different combination techniques explained in Section 4 and compare them against three ensemble classifiers: RFC (Random Forest Classifier), ADA (AdaBoost Classifier) and BAG (Bagging Classifier). These ensemble classifiers are implemented in the Python library sklearn<sup>2</sup> and used with their default parameters. The combination results using KI-04 dataset is illustrated in Fig. 5. It is clear that the best results are achieved using OWA-MAX, followed by DS, then Murphy. For SANTINIS dataset, the best results are achieved using our proposed evidential combination, followed by OWA-MEAN and then OWA-Weighted. We notice also that ensemble classifiers achieves the lowest results for both datasets KI-04 and SANTINIS. In comparison with the previous works on web genre identification shown

<sup>2</sup> https://scikit-learn.org/

![](_page_5_Figure_1.jpeg)

![](_page_5_Figure_2.jpeg)

**Fig. 4.** Performance for different classifiers using full text.

![](_page_5_Figure_6.jpeg)

![](_page_5_Figure_7.jpeg)

**Fig. 5.** Performance for the combination of the two best classifiers using different combination techniques.

in Table 1, we can observe that our results reported by combining internal and external structures are much higher.

#### **6. Conclusion**

In this paper we propose to use the terms extracted from the internal and external structures of a web page to identify its genre. The experimentation study shows that this terms are very effective in capturing the genre of a web page. In addition to that, our approach does not require any complicated natural language processing to extract the terms from the internal and external structures. The main idea of our proposed framework is to combine the outputs of individual classifiers that uses internal and external structures. The combination is done using a new proposed evidential combination method and OWA operators. The experimentations show that the combination of the best selected classifiers achieves the highest results in comparison with three known ensemble classifiers and many previous studies as well. Moreover, the experimentations show that the proposed evidential combination technique achieves better results in comparison with DS and Murphy techniques and OWA operators as well. In the future, we will focus on evaluating the proposed evidential combination technique with more classifiers using different multi-disciplinary datasets. In addition to that, we are planning to validate the usefulness of web genre identification in improving web search.

#### **Declaration of Competing Interest**

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

#### **References**

- [1] M. Abramson, D.W. Aha, What's in a url? genre classification from urls, in: Proceedings of the Workshops at the 26th AAAI Conference on Artificial Intelligence (AAAI'2012), Toronto, Canada, 2012, pp. 1–7.
- [2] S. Agrawal, L.M. Sanagavarapu, Y.R. Reddy, Fact fine grained assessment of web page credibility, in: TENCON, 2019, pp. 1088–1097.
- [3] N.R. Asheghi, S. Sharoff, K. Market, Designing and evaluating a reliable corpus of web genres via crowd-sourcing, in: In Proceedings of the 9th International Conference on Language Resources and Evaluation (LREC'2014), Reykjavik, Iceland, 2014, pp. 1339–1346.
- [4] S.N.B. Bhushan, A. Danti, Classification of text documents based on score level fusion approach, Pattern Recognit. Lett. 94 (2017) 118–126.
- [5] E. Davoodi, L. Kosseim, F. Bachand, M. Laali, E. Argollo, Classification of textual genres using discourse information, in: CICLING, Springer-Verlag, 2016, pp. 636–647.
- [6] S.M. Eissen, On information need and categorizing search, Paderborn University, 2007 Ph.d. thesis.
- [7] C. Jebari, A new centroid-based approach for genre categorization of web pages, Journal for Language Technology and Compotational Linguistics 24 (1) (2009) 73–96.
- [8] C. Jebari, Mlicc: A multi-label and incremental centroid-based classification of web pages by genre, in: In Proceedings of the 17th International Conference on Applications of Natural Language Processing to Information Systems (NLDB'2012), Groningen, Netherlands, 2012, pp. 183–190.
- [9] I. Kanaris, E. Stamatatos, Learning to recognize webpage genres, Information processing and management Journal 45 (5) (2009) 499–512.
- [10] G. Madjarov, V. Vidulin, I. Dimitrovski, D. Kocev, Web genre classification with methods for structured output prediction, Inf. Sci. 503 (2019) 551–573.
- [11] J. Mason, An n-gram Based Approach to the Automatic Classification of Web Pages by Genre, Dalhousie University, 2010 Ph.d. Canada
- [12] C.K. Murphy, Combining belief functions when evidence conflicts, Decis. Support Syst. 29 (2000) 1–9.
- [13] D.A. Pritsos, E. Stamatatos, The impact of noise in web genre identification, in: CLEF, 2015, pp. 268–273.
- [14] D.A. Pritsos, E. Stamatatos, Open set evaluation of web genre identification, Lang. Resour. Evaluation 52 (2018) 949–968.
- [15] X. Qi, B.D. Davison, Web page classification: Features and algorithms, Techincal Report, Lehigh University, 2007.
- [16] D. Ruta, B. Gabrys, An overview of classifier fusion methods, Comput. Inf. Syst. 7 (2000) 1–10.
- [17] M. Santini, Automatic Identification of Genre in Web Pages: A New Perspective, Brighton University, 2011 Phd thesis.
- [18] F. Sebastiani, Machine learning in automated text categorization, ACM Comput. Surv. 34 (2002) 1–47.
- [19] G. Shafer, A Mathematical Theory of Evidence, Princeton University Press, Princeton, NJ, 1976.
- [20] M. Shepherd, C. Watters, Evolution of cybergenre, in: Proceedings of the 31*th* Hawaiian International Conference on System Sciences, 1998, pp. 97–109. Hawai, USA
- [21] B. Stein, S.M. Eissen, N. Lipka, Web genre analysis: Use cases, retrieval models, and implementation issues, in: Genres on the Web, Springer-Verlag, 2011, pp. 167–189.
- [22] V. Vidulin, M. Lustrek, M. Gams, Multi-label approaches to web genre identification, Journal of Language and Computational Linguistics 24 (1) (2009) 97–114.
- [23] J. Worsham, J. Kalita, Genre identification and the compositional effect of genre in literature, in: Proceedings of the 31th Hawaiian International Conference on System Sciences, 2018, pp. 1963–1973. COLING
- [24] R.R. Yager, On ordered weighted averaging aggregation operators in multi-criteria decision making, IEEE Transactions on Systems, Man and Cybernetics 18 (1988) 183–190.
- [25] K. Yuan, F. Xiao, L. Fei, B. Kang, Y. Deng, Conflict management based on belief function entropy in sensor fusion, Springerplus 5 (2016).
- [26] L.A. Zadeh, A simple view of the dempstershafer theory of evidence and its implication for the rule of combination, AI Magazine 7 (1986).
- [27] Z. Zhang, T. Liu, D. Chen, W. Zhang, Novel algorithm for identifying and fusing conflicting data in wireless sensor networks, Sensors 14 (2014) 9562–9581.
- [28] J. Zhu, Q. Xie, S. Yu, W.H. Wong, Exploiting link structure for web page genre identification, Data Min. Knowl. Discov. 30 (2015) 550–575.