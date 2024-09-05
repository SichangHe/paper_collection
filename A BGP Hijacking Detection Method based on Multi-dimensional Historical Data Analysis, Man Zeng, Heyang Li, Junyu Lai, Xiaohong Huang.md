# A BGP Hijacking Detection Method based on Multi-dimensional Historical Data Analysis

\({}^{\ast}\)Man Zeng, \({}^{\dagger}\)Heyang Li, \({}^{\ast}\)Junyu Lai, \({}^{\ast}\)Xiaohong Huang

\({}^{\ast}\)_School of Computer Science (National Pilot Software Engineering School), Beijing University of Posts and Telecommunications, Beijing, China_

\({}^{\dagger}\)_Meituan Beijing, China,_

Email: \({}^{\ast}\){zengman, 2017212655, huangxh}@bupt.edu.cn, \({}^{\dagger}\)li_hy54@163.com

###### Abstract

BGP prefix hijacking is one of the top threats on the Internet. The traditional approaches are mainly to analyze the prefix changes of the control plane, or to use the active measurement detection method to obtain the reachability of the prefix to determine whether there is prefix hijacking. These approaches rely on extensive infrastructures, wide coverage of measurement points, and long-term continuous detection. In this paper, we propose a BGP prefix hijacking detection method based on multi-dimensional historical data analysis, which can avoid the high deployment cost and long detection delay of active measurement methods. We test the proposed method on 1487 prefix hijacking events identified by BGPStream, from which more than 99% (1475/1487) prefix hijacking events are detected. The results show that the proposed method can effectively and accurately detect prefix hijacking.

 BGP, Prefix hijacking detection, Multi-dimensional data. +
Footnote †: publicationid: pubid: 978-1-7281-9401-1/21/$31.00 ©2021 IEEE

## I Introduction

There exist more than 70,000 Autonomous Systems (ASes) on the Internet. Every AS possesses its Autonomous System Number (ASN) and declares one or more owned IP prefixes to other ASes. The Border Gateway Protocol (BGP) is a standard interdomain routing Protocol that allows ASes to obtain network reachability information by exchanging BGP update messages. However, BGP remains security vulnerabilities due to the lack of security authentication mechanisms. For example, ASes completely believe the routing messages announced by their neighbors, which makes them easy to accept malicious routes.

The prefix hijacking is a common type of BGP anomaly event, in which ASes illegally declare prefixes owned by other ASes to misdirect or drop the legal traffic. In recent years, Internet security incidents caused by prefix hijacking have emerged one after another. In particular hijacking attacks launched against electronic money pose a serious threat to the property security of network users [1, 2]. The root cause of prefix hijacking is that the AS does not verify the validity of the IP prefix ownership in the received BGP announcements. Ideally, the Regional Internet Registries (RIRs) and Internet Routing Registries (IRRs) have the prefix allocation records, which can be used to validate the prefix ownership. However, in actual applications, the registration data in RIR/IRR may be outdated, incomplete, and inconsistent [3]. Therefore, how to more accurately determine the legality of prefix declaration is the first problem to be solved by prefix hijacking detection.

The existing detection methods for prefix hijacking can be categorized into three types according to the attack characteristics of different planes: control-plane detection, data-plane detection, and comprehensive detection including control and data plane [4]. Control-plane detection methods [5, 6, 7, 8] usually collect original BGP update messages from Route Views Project [9] and RIPE RIS [10] to detect anomalies. The data-plane detection methods [11, 12, 13, 14] use the active measurement technology to obtain the prefix reachability and utilize this information to determine whether there is prefix hijacking. The comprehensive detection methods [15, 16, 17] use information from both control and data plane to improve the accuracy of the detection. However, these methods have their limits. The control-plane detection has a low detection accuracy due to the single-dimensional data. The data-plane detection relies on the deployment of measurement points and requires a high detection cost. Moreover, with the exponential growth of the Internet [18], the required cost will continue to increase. The comprehensive detection improves the detection accuracy but it also has the same shortcomings of the data-plane detection.

There are plenty of different dimensional data that can reflect the BGP routing information on the Internet, such as historical BGP routing tables, registry information, and geographical location data. These data contain valuable information about the attribution of IP prefixes. Therefore, instead of using single-dimensional data like BGP update messages, we argue that a combination of multi-dimensional data can better determine the credibility of prefix ownership.

In this paper, we propose a prefix hijacking detection method based on multi-dimensional historical data and use this method to build a detection framework. The key of the proposed method is to establish a reliable mapping relationship between the prefix and origin AS using multi-dimensional public data. Through the analysis results of the above dimensions, we can quantify the credibility of each dimension and integrate the credibility of these dimensions to get a final mapping relationship of the prefix and origin AS. Using the mapping relationship to jointly evaluate the possibility of the prefix hijacking can make the detection results more credible.

The rest of the paper is organized as follows. Section II gives a brief overview of the detection framework and introduces the core of the detection, namely the qualitative analysis of multi-dimensional data. Section III presents experiment results of the method and the conclusion is shown in Section IV.

## II Methodology

We first give a brief overview of the detection framework, and then present more details about the quantitative analysis method in the Data Analysis module.

### _Detection framework_

The detection framework is shown in Figure 1, which consists of four modules including the Data acquisition module, Data analysis Module, Data storage module, and Anomaly Detection module.

Data Acquisitionthe Data Acquisition module collects and parses data from different sources. For example, it acquires historical BGP routing data from RIPE RIS and RouteViews. The registry information is collected from RIR/IRR, and the IP geographical location data are collected from IP2Location database [19].

Data Analysisthe Data Analysis module is the core of the framework. It is used to obtain the credibility of prefix and origin AS pairs (denoted as prefix-AS pairs) from the collected data. First, it analyzes the data in three dimensions and establishes linear correlations to describe the credibility of these dimensions respectively. Second, it uses Analytic Hierarchy Process (AHP) [20] to integrate these dimensions.

Data Storagethe Data Storage module uses the quantitative analysis results obtained from the Data Analysis module to construct a knowledge repository. This knowledge repository provides the final credibility of prefix-AS pairs to help with the hijacking detection. Through storing and retrieving data in the knowledge repository, the Data Storage module can improve the speed of the detection.

Anomaly Detectionthe Anomaly Detection module utilizes the data in the knowledge repository to detect whether the received BGP message is prefix hijacking. The process of the detection is shown in Algorithm 1. If the credibility of the prefix-AS pair in the mapping table is lower than or equal to the threshold \(l\), it is regarded as prefix hijacking. Otherwise, it is regarded as a legal event.

```
Input: 1) prefix-AS mapping table prefix_map,
2) prefix \(p\) and its origin AS \(s\) extracted from the received BGP message, 3) threshold \(l\). Output: True (hijacking) / False (legal event). if\(p\) in prefix_mapthen \(Y_{p}\) =prefix_map(\(p\)) if\(s\) in \(Y_{p}\)then \(x\gets Y_{p}(s)\) // \(x\) is the credibility of pair \((p,s)\) return\((x\leq l)\) else return True endif endif return False
```

**Algorithm 1** Anomaly detection

### _Quantitative analysis of historical routing table data_

The historical BGP routing tables collected from RIPE RIS and CAIDA [21] are used to help decide the credibility of prefix-AS pairs. RIPE RIS has 24 collectors providing every 8 hours routing snapshots. CAIDA extracts the routing data collected from RouteViews and provides a daily updated mapping relationship between IPv4/IPv6 prefix and origin AS.

We count the frequency of occurrence and the last occurrence time of each prefix-AS pair during the collection period. If the frequency of occurrence is higher and the last occurrence time is closer to the end time of collection, the credibility will be higher. Thus, the following equation can be built:

\[C_{rib}=a*\frac{t_{l}-t_{s}}{t_{e}-t_{s}}+b*\frac{n}{N} \tag{1}\]

where \(C_{rib}\) represents the credibility measured by historical BGP routing tables, \(t_{l}\) is the last occurrence time of prefix-AS pair, \(t_{s}\) is the start time of the collection and \(t_{e}\) is the end

Fig. 1: Detection framework time of the collection. \(n\) denotes the occurrence frequency of prefix-AS pair and \(N\) is the total number of the routes. The coefficient \(a\) and \(b\) are weights determined by AHP.

### _Quantitative analysis of historical registration information_

We have collected a total of 2.2 million registration records from 22 registration databases in IRR and filtered out 820,000 active registration records with a total of 1.1 million prefixes. Due to the large span of registration time in the database, it is impossible to distinguish the reliability of these registrations. Therefore, we only focus on the last modification time of the registration. If the last modification time of the registration is closer to the end time of the collection, the registration is more reliable. Thus, the correlation equation can be established:

\[C_{regis}=\frac{t-t_{min}}{t_{max}-t_{min}} \tag{2}\]

where \(C_{regis}\) represents the credibility measured by registration information, \(t\) is the last modification time of the prefix-AS pair's registration, \(t_{min}\) is the earliest modification time of the prefix's registration, and \(t_{max}\) is the final modification time of the prefix's registration.

### _Quantitative analysis of AS geographical information_

An AS usually manages plenty of IP prefixes and routers with geographical information. Thus, the geographical location of the AS can be derived from the geographical location of its owned IP prefixes. The following is the process for acquiring the geographical location of an AS:

* First, record the set of prefixes (\(P_{origin}\)) declared by each AS according to the historical BGP routing data, where \(origin\) is the AS and \(p_{n}\) denotes the prefix.
* \[P_{origin}=\{p_{1},p_{2},p_{3},...,p_{n}\}\] (3)
* Second, randomly select \(m\) IP addresses for each prefix to construct a set of IP addresses (\(IP_{as}\)), where \(ip_{m}\) is the IP address. \[IP_{origin}=\{ip_{1},ip_{2},ip_{3},...,ip_{m}\}\] (4)
* Third, query the latitude and longitude of the IP address from IP2Location database to construct a set of (latitude, longitude) \(AL_{origin}\) for each AS \(origin\). \[AL_{origin}=\{(lng_{1},lat_{1}),...,(lng_{n},lat_{n})\}\] (5)
* Finally, use density-based clustering algorithm DBSCAN [22] to cluster the locations in \(AL_{origin}\). Then, select the class with the most elements to get a latitude and longitude interval, which can be used to determine which country the AS belongs to.

After the above process, we can obtain all origin ASes of each prefix \(p\) and their corresponding country information, which can be denoted as:

\[C_{p}=\{(ASN_{1},country_{1}),...,(ASN_{n},country_{n})\} \tag{6}\]

Then, we count the proportion of each country illustrated in \(C_{p}\) as the credibility for the country dimension. Thus, the final prefix-AS-country-credibility mapping table can be obtained.

### _Integration of multi-dimensional historical data_

The AHP is a combination of qualitative and quantitative decision-making analysis methods and can reflect the difference in the relative importance of different dimensions. It is used to calculate weights for the above three dimensions and the detail is shown below:

* First, the three dimensions are combined into pairs. Compare the relative importance of the pairs, and construct pairwise comparison matrix \(A\) according to the relative scale. \[A=(a_{ij})_{n*n}\] (7)
* Then, a consistency check is carried out on the constructed pairwise comparison matrix. If the matrix passes the check, find the maximum eigenvalue \(\lambda_{max}\) of the matrix and eigenvector \(W=(w_{1},...,w_{n})^{T}\) whose element is the weight of every dimension. If the matrix does not pass the check, the pairwise comparison matrix needs to be reconstructed.

After the above process, we can obtain the weight for each dimension and the final credibility table of each prefix-AS pair.

## III Experiment results

In this section, the test results of the proposed method for the prefix hijacking detection are illustrated. The results mainly include two parts, the quantitative analysis results of multi-dimensional historical data and the detection results of prefix hijacking detection.

Before introducing the results, the detail of the data used in the experiment is presented. The prefix hijacking events used in the experiment are collected by BGPstream ranging from March 2019 to December 2019. The time of the collected routing data is from May 2018 to February 2019. The IRR registration data, IP address geographical location data, and BGP routing table data are all selected before March 2019.

### _Quantitative analysis results of multi-dimensional historical data_

Table I shows partial analysis results of the historical routing data. For every prefix-AS pair, the _frequency_ is the number of occurrences of the prefix-AS pair in the collection period, and the _fscore_ is the credibility of the _frequency_. The _last_appear_ is the last occurrence time of the prefix-AS pair and _lscore_ is the credibility of the _last_appear_. The _rib_score_ is the total score calculated by using the (1). From the results we can see, the prefix-AS pair (153.94.32.0/21, 25394) only appeared once in the collection period and its total score is lower than others, so the prefix 153.94.32.0/21 has a higher probability of being hijacked by AS 25394.

Table II shows partial analysis results of the historical registration data. The _last_modified_ is the last modification time of prefix-AS pair in the registration records. The _reg_score_ is the credibility of the _last_modified_ calculated by (2). When the _reg_score_ of the prefix-AS pair is 1, it indicates the pair has registered in IRR database and the _last_modified_ of the prefix-AS pair is the final registration time of the prefix. Table

III shows the analysis results of the prefix-AS geographical information. The _geo_score_ is the credibility of the prefix-AS in geographical dimension. When the _geo_score_ is 1, it indicates that in the historical data, there is only one country corresponding to the prefix.

After obtaining the above scores from different dimensions, the integration results can be obtained by using the method in Section II-E. Table IV shows partial analysis results after the integration. In the integration, the credibility weight of the routing data, historical registration data, geographical information are 0.639, 0.274, and 0.087 respectively. The _total score_ is the final credibility of the prefix-AS pair. The prefix-AS pair (165.118.0.0/16, 1221) has a _total score_ of 0, which suggests it has a high probability of being a prefix hijacking event.

### _Prefix Hijacking Detection Results_

The prefix hijacking events collected from BGPstream are used to evaluate the accuracy of the proposed hijacking detection method. These hijacking events are from February 28, 2019 to December 25, 2019, with a total of 1487 pieces. We use the credibility of 0.5 as the threshold to determine whether it is prefix hijacking. Thus, if the credibility of the prefix-AS pair is less than or equal to 0.5, it is regarded as a prefix hijacking. Otherwise, it is regarded as a legal event. The results show that among the 1487 events, 99% of the events are detected as hijacking, and only 12 events are different. For the inconsistent detection results, a reasonable analysis is given below.

Table V illustrates the 12 events. These events are determined as prefix hijacking by BGPstream while the proposed method classifies them as legal events. The columns of fields in Table V from left to right are IP prefix (_prefix_), victim AS determined by BGPStream (_origin ASN_), credibility of victim's history routing data (_origin_rib_), credibility of victim's historical registration data (_origin_reg_), credibility of victim's geographic location (_origin_geo_), victim's total credibility (_origin_total_), hijack AS determined by BGPStream (_hijacker ASN_), credibility of hijacker's history routing data (_hijack_rib_), credibility of hijacker's historical registration data (_hijack_reg_), credibility of hijacker's geographic location (_hijack_geo_), and hijacker's total credibility (_hijack_total_).

By comparing the scores in Table V, it can be seen that the score of the hijacker AS determined by BGPStream, is all above 0.66 in the dimension of historical routing data, which indicates that the prefix-AS pairs appear several times in historical routing data and the last occurrence time is close to the end collection time. In addition, there are four pairs of prefix-hijacker AS scored 1 in the dimension of historical registration information, indicating that these pairs have been recorded in IRR. Moreover, from _origin_total_ column in the Table V, there are 7 origin ASes that have a score of 0, and only one origin AS has a total score of more than 0.5. In the dimension of the historical routing data, there are 9 origin ASes with a score of 0, which means that these origin ASes have never announced the corresponding prefixes during the statistical period. However, the score of the hijacker AS in the historical routing data dimension is all greater than 0.7. In the dimension of historical registration information, there are 10 ASes with a score of 0, which suggests that there is no registration information for these prefix-AS pairs during the collection period.

For example, in the first event, BGP Stream determines the legal origin AS of prefix 85.235.68.0/2 is AS 42831, and the hijacker AS is 206751. The three scores of AS 42831 are all 0, which means that AS 42831 has never announced the prefix 85.235.68.0/22 during the collection period and there are no related registration records in the IRR registration database. From the above analysis, it can be concluded that the prefix-AS pair (85.235.68.0/22, 206751) have a high degree of credibility and low possibility of prefix hijacking, so this may be a false alarm of BGPStream.

As shown in the above analysis, the detection result of the proposed method has a high overlap with the result of the commercial BGP anomaly detection agency BGPStream and can provide reliable performance in prefix hijacking detection.

## IV Conclusions

In this paper, we propose a novel prefix hijacking detection method based on multi-dimensional historical data analysis and implement a detection framework based on the method. It quantifies three dimensions of historical data to obtain the credibility of prefix-AS pairs and uses this credibility to detect prefix hijacking. Compared with existing methods, the proposed method avoids the high cost of using active measurement technology and the low accuracy by using single dimension routing data. The results show that the proposed method has high accuracy (99%) in detecting prefix hijacking compared with BGPStream.

## Acknowledgment

This work is supported by the National Key R&D Program of China (No. 2018YFB1800404).

## References

* [1]_BGP Hijacking Attacks Target US Payment Processors_, 2018. [Online]. Available: [https://www.securityweek.com/bgp-hijacking-attacks-target-us-payment-processors](https://www.securityweek.com/bgp-hijacking-attacks-target-us-payment-processors)
* [2]_Russian-controlled telecom hijacks financial services: Internet traffic_, 2017. [Online]. Available: [https://arstechnica.com/information-technology/2017/04/trussian-controlled-telecom-hijacks-financial-services-internet-traffic/](https://arstechnica.com/information-technology/2017/04/trussian-controlled-telecom-hijacks-financial-services-internet-traffic/)
* [3] K. Sriram, O. Borchert, O. Kim, P. Gleichmann, and D. Montgomery, "A comparative analysis of bgp anomaly detection and robustness algorithms," in _2009 Cybersecurity Applications & Technology Conference for Homeland Security_. IEEE, 2009, pp. 25-38.
* [4] A. Mitseva, A. Panchenko, and T. Engel, "The state of affairs in bgp security: A survey of attacks and defenses," _Computer Communications_, vol. 124, pp. 45-60, 2018.
* [5] M. Lad, D. Massey, D. Pei, Y. Wu, B. Zhang, and L. Zhang, "Phas: A prefix hijack alert system." in _USENIX Security symposium_, vol. 1, no. 2, 2006, p. 3.
* [6] P. Sermpezis, V. Kotronis, P. Gigis, X. Dimitropoulos, D. Cicalese, A. King, and A. Dainotti, "Artemis: Neutralizing bgp hijacking within a minute," _IEEE/ACM Transactions on Networking_, vol. 26, no. 6, pp. 2471-2486, 2018.
* [7] J. Karlin, S. Forrest, and J. Rexford, "Petty good bgp: Improving bgp by cautiously adopting routes," in _Proceedings of the 2006 IEEE International Conference on Network Protocols_. IEEE, 2006, pp. 290-299.
* [8] G. Theodoridis, O. Tsigkas, and D. Tzovaras, "A novel unsupervised method for securing bgp against routing hijacks," in _Computer and Information Sciences III_. Springer, 2013, pp. 21-29.
* [9]_The route views project_. [Online]. Available: [http://www.routeviews.org/](http://www.routeviews.org/)
* [10]_The RIPE Routing Information Service_. [Online]. Available: [https://www.ripe.net/analyse/internet-measurements/routing-information-service-its](https://www.ripe.net/analyse/internet-measurements/routing-information-service-its)
* [11] M. Tahara, N. Tateishi, T. Oimatsu, and S. Majima, "A method to detect prefix hijacking by using bmg tests," in _Asia-Pacific Network Operations and Management Symposium_. Springer, 2008, pp. 390-398.
* [12] Z. Zhang, Y. Zhang, Y. C. Hu, Z. M. Mao, and R. Bush, "ispy: Detecting ip prefix hijacking on my own," in _Proceedings of the ACM SIGCOMM 2008 conference on Data Communication_, 2008, pp. 327-338.
* [13] C. Zheng, L. Ji, D. Pei, J. Wang, and P. Francis, "A light-weight distributed scheme for detecting ip prefix hijacks in real-time," _ACM SIGCOMM Computer Communication Review_, vol. 37, no. 4, pp. 277-288, 2007.
* [14] M. Chiesa, A. Kamisifiski, J. Rak, G. Retvari, and S. Schmid, "A survey of fast recovery mechanisms in the data plane," 2020.
* [15] G. Siganos and M. Faloutsos, "A blueprint for improving the robustness of internet routing," 2005.
* [16] G. Siganos and M. Faloutsos, "Analyzing bgp policies: Methodology and tool," in _IEEE INFOCOM 2004_, vol. 3. IEEE, 2004, pp. 1640-1651.
* [17] X. Hu and Z. M. Mao, "Accurate real-time identification of ip prefix hijacking," in _2007 IEEE Symposium on Security and Privacy (SP'07)_. IEEE, 2007, pp. 3-17.
* [18] M. A. Kumar and S. Karthikeyan, "Security model for tcp/ip protocol suite," _Journal of Advances in Information Technology_, vol. 2, no. 2, pp. 87-91, 2011.
* [19]_IP2Location_, _db6-ip-country-region-city-latitude-longitude-isp_. [Online]. Available: [https://www.ip2location.com/database/db6-ip-country-region-city-latitude-longitude-isp](https://www.ip2location.com/database/db6-ip-country-region-city-latitude-longitude-isp)
* [20] E. W. Cheng and H. Li, "Analytic hierarchy process," _Measuring business excellence_, 2001.
* [21]_CAIDA Routerives Prefix to AS mappings Dataset(p/2x3) for IPv4 and IPv6_. [Online]. Available: [https://www.caida.org/data/routing/routeviews-prefix2x3.xml](https://www.caida.org/data/routing/routeviews-prefix2x3.xml)
* [22] M. Parimala, D. Lopez, and N. Senthilkumar, "A survey on density based clustering algorithms for mining large spatial databases," _International Journal of Advanced Science and Technology_, vol. 31, no. 1, pp. 59-66, 2011. 


