# A Bgp Hijacking Detection Method Based On Multi-Dimensional Historical Data Analysis

*Man Zeng, †Heyang Li, *Junyu Lai, *Xiaohong Huang
*School of Computer Science (National Pilot Software Engineering School),
Beijing University of Posts and Telecommunications, Beijing, China
†*Meituan Beijing, China*,
Email: *{zengman, 2017212655, huangxh}@bupt.edu.cn, †li hy54@163.com Abstract**—BGP prefix hijacking is one of the top threats on**
the Internet. The traditional approaches are mainly to analyze the prefix changes of the control plane, or to use the active measurement detection method to obtain the reachability of the prefix to determine whether there is prefix hijacking. These approaches rely on extensive infrastructures, wide coverage of measurement points, and long-term continuous detection. In this paper, we propose a BGP prefix hijacking detection method based on multi-dimensional historical data analysis, which can avoid the high deployment cost and long detection delay of active measurement methods. We test the proposed method on 1487 prefix hijacking events identified by BGPStream, from which more than 99% (1475/1487) prefix hijacking events are detected.

The results show that the proposed method can effectively and accurately detect prefix hijacking.

Index Terms**—BGP, Prefix hijacking detection, Multidimensional data.**

## I. Introduction

There exist more than 70,000 Autonomous Systems (ASes)
on the Internet. Every AS possesses its Autonomous System Number (ASN) and declares one or more owned IP prefixes to other ASes. The Border Gateway Protocol (BGP) is a standard interdomain routing Protocol that allows ASes to obtain network reachability information by exchanging BGP
update messages. However, BGP remains security vulnerabilities due to the lack of security authentication mechanisms.

For example, ASes completely believe the routing messages announced by their neighbors, which makes them easy to accept malicious routes.

The prefix hijacking is a common type of BGP anomaly event, in which ASes illegally declare prefixes owned by other ASes to misdirect or drop the legal traffic. In recent years, Internet security incidents caused by prefix hijacking have emerged one after another. In particular hijacking attacks launched against electronic money pose a serious threat to the property security of network users [1], [2]. The root cause of prefix hijacking is that the AS does not verify the validity of the IP prefix ownership in the received BGP announcements.

Ideally, the Regional Internet Registries (RIRs) and Internet Routing Registries (IRRs) have the prefix allocation records, which can be used to validate the prefix ownership. However, in actual applications, the registration data in RIR/IRR may be outdated, incomplete, and inconsistent [3]. Therefore, how to more accurately determine the legality of prefix declaration is the first problem to be solved by prefix hijacking detection.

The existing detection methods for prefix hijacking can be categorized into three types according to the attack characteristics of different planes: control-plane detection, dataplane detection, and comprehensive detection including control and data plane [4]. Control-plane detection methods [5]–[8]
usually collect original BGP update messages from Route Views Project [9] and RIPE RIS [10] to detect anomalies.

The data-plane detection methods [11]–[14] use the active measurement technology to obtain the prefix reachability and utilize this information to determine whether there is prefix hijacking. The comprehensive detection methods [15]–[17] use information from both control and data plane to improve the accuracy of the detection. However, these methods have their limits. The control-plane detection has a low detection accuracy due to the single-dimensional data. The data-plane detection relies on the deployment of measurement points and requires a high detection cost. Moreover, with the exponential growth of the Internet [18], the required cost will continue to increase. The comprehensive detection improves the detection accuracy but it also has the same shortcomings of the dataplane detection.

There are plenty of different dimensional data that can reflect the BGP routing information on the Internet, such as historical BGP routing tables, registry information, and geographical location data. These data contain valuable information about the attribution of IP prefixes. Therefore, instead of using single-dimensional data like BGP update messages, we argue that a combination of multi-dimensional data can better determine the credibility of prefix ownership.

In this paper, we propose a prefix hijacking detection method based on multi-dimensional historical data and use this method to build a detection framework. The key of the proposed method is to establish a reliable mapping relationship between the prefix and origin AS using multi-dimensional public data. Through the analysis results of the above dimensions, we can quantify the credibility of each dimension and integrate the credibility of these dimensions to get a final mapping relationship of the prefix and origin AS. Using the mapping relationship to jointly evaluate the possibility of the prefix hijacking can make the detection results more credible.

2021 International Conference on Computer Communication and Artificial Intelligence (CCAI) | 978-1-7281-9401-1/20/$31.00 ©2021 IEEE | DOI: 10.1109/CCAI50917.2021.9447530

![1_image_0.png](1_image_0.png)

Fig. 1. Detection framework
The rest of the paper is organized as follows. Section II gives a brief overview of the detection framework and introduces the core of the detection, namely the qualitative analysis of multidimensional data. Section III presents experiment results of the method and the conclusion is shown in Section IV.

## Ii. Methodology

We first give a brief overview of the detection framework, and then present more details about the quantitative analysis method in the Data Analysis module.

## A. Detection Framework

The detection framework is shown in Figure 1, which consists of four modules including the Data acquisition module, Data analysis Module, Data storage module, and Anomaly Detection module.

a) Data Acquisition: the Data Acquisition module collects and parses data from different sources. For example, it acquires historical BGP routing data from RIPE RIS and RouteViews. The registry information is collected from RIR/IRR, and the IP geographical location data are collected from IP2Location database [19].

b) Data Analysis: the Data Analysis module is the core of the framework. It is used to obtain the credibility of prefix and origin AS pairs (denoted as prefix-AS pairs) from the collected data. First, it analyzes the data in three dimensions and establishes linear correlations to describe the credibility of these dimensions respectively. Second, it uses Analytic Hierarchy Process (AHP) [20] to integrate these dimensions.

c) Data Storage: the Data Storage module uses the quantitative analysis results obtained from the Data Analysis module to construct a knowledge repository. This knowledge repository provides the final credibility of prefix-AS pairs to help with the hijacking detection. Through storing and retrieving data in the knowledge repository, the Data Storage module can improve the speed of the detection.

d) Anomaly Detection: the Anomaly Detection module utilizes the data in the knowledge repository to detect whether the received BGP message is prefix hijacking. The process of the detection is shown in Algorithm 1. If the credibility of the prefix-AS pair in the mapping table is lower than or equal to the threshold l, it is regarded as prefix hijacking. Otherwise, it is regarded as a legal event.

Algorithm 1 Anomaly detection Input: 1) prefix-AS mapping table prefix map, 2) prefix p and its origin AS s extracted from the received BGP message, 3) threshold l.

Output: True (hijacking) / False (legal event).

if p in prefix map **then**
Yp =prefix map(p) if s in Yp **then**
x ← Yp(s) // x is the credibility of pair (*p, s*)
return (x ≤ l)
else return True end if else if the parent prefix f of p in prefix map **then**
Yf =prefix map(f)
if s in Yf **then**
x ← Yf (s) // x is the credibility of pair (*f, s*)
return (x ≤ l)
else return True end if end if return False B. Quantitative analysis of historical routing table data The historical BGP routing tables collected from RIPE
RIS and CAIDA [21] are used to help decide the credibility of prefix-AS pairs. RIPE RIS has 24 collectors providing every 8 hours routing snapshots. CAIDA extracts the routing data collected from RouteViews and provides a daily updated mapping relationship between IPv4/IPv6 prefix and origin AS.

We count the frequency of occurrence and the last occurrence time of each prefix-AS pair during the collection period.

If the frequency of occurrence is higher and the last occurrence time is closer to the end time of collection, the credibility will be higher. Thus, the following equation can be built:

$$C_{r i b}=a*{\frac{t_{l}-t_{s}}{t_{e}-t_{s}}}+b*{\frac{n}{N}}$$
$$(1)$$

where Crib represents the credibility measured by historical BGP routing tables, tlis the last occurrence time of prefixAS pair, ts is the start time of the collection and te is the end time of the collection. n denotes the occurrence frequency of prefix-AS pair and N is the total number of the routes. The coefficient a and b are weights determined by AHP.

C. Quantitative analysis of historical registration information We have collected a total of 2.2 million registration records from 22 registration databases in IRR and filtered out 820,000 active registration records with a total of 1.1 million prefixes. Due to the large span of registration time in the database, it is impossible to distinguish the reliability of these registrations.

Therefore, we only focus on the last modification time of the registration. If the last modification time of the registration is closer to the end time of the collection, the registration is more reliable. Thus, the correlation equation can be established:

$$C_{r e g i s}={\frac{t-t_{m i n}}{t_{m a x}-t_{m i n}}}$$

tmax − tmin(2)
where C*regis* represents the credibility measured by registration information, t is the last modification time of the prefixAS pair's registration, tmin is the earliest modification time of the prefix's registration, and tmax is the final modification time of the prefix's registration.

D. Quantitative analysis of AS geographical information An AS usually manages plenty of IP prefixes and routers with geographical information. Thus, the geographical location of the AS can be derived from the geographical location of its owned IP prefixes. The following is the process for acquiring the geographical location of an AS:
- First, record the set of prefixes (P*origin*) declared by each AS according to the historical BGP routing data, where origin is the AS and pn denotes the prefix.

Porigin = {p1, p2, p3*, ..., p*n} (3)
- Second, randomly select m IP addresses for each prefix to construct a set of IP addresses (IPas), where ipm is the IP address.

IPorigin = {ip1, ip2, ip3*, ..., ip*m} (4)
- Third, query the latitude and longitude of the IP address from IP2Location database to construct a set of (latitude, longitude) LAL*origin* for each AS origin.

LALorigin = {(lng1, lat1), ...,(lngn*, lat*n)} (5)
- Finally, use density-based clustering algorithm DBSCAN
[22] to cluster the locations in LAL*origin*. Then, select the class with the most elements to get a latitude and longitude interval, which can be used to determine which country the AS belongs to.

After the above process, we can obtain all origin ASes of each prefix p and their corresponding country information, which can be denoted as:

$$C_{p}=\{(A S N_{1},c o u n t r y_{1}),...,(A S N_{n},c o u n t r y_{n})\}$$

Then, we count the proportion of each country illustrated in Cp as the credibility for the country dimension. Thus, the final prefix-AS-country-credibility mapping table can be obtained.

## E. Integration Of Multi-Dimensional Historical Data

The AHP is a combination of qualitative and quantitative decision-making analysis methods and can reflect the difference in the relative importance of different dimensions. It is used to calculate weights for the above three dimensions and the detail is shown below:
- First, the three dimensions are combined into pairs. Compare the relative importance of the pairs, and construct pairwise comparison matrix A according to the relative scale.

A = (aij )n∗n (7)
- Then, a consistency check is carried out on the constructed pairwise comparison matrix. If the matrix passes the check, find the maximum eigenvalue λmax of the matrix and eigenvector W = (w1*, ..., w*n)
T whose element is the weight of every dimension. If the matrix does not pass the check, the pairwise comparison matrix needs to be reconstructed.

After the above process, we can obtain the weight for each dimension and the final credibility table of each prefix-AS pair.

## Iii. Experiment Results

In this section, the test results of the proposed method for the prefix hijacking detection are illustrated. The results mainly include two parts, the quantitative analysis results of multidimensional historical data and the detection results of prefix hijacking detection.

Before introducing the results, the detail of the data used in the experiment is presented. The prefix hijacking events used in the experiment are collected by BGPstream ranging from March 2019 to December 2019. The time of the collected routing data is from May 2018 to February 2019. The IRR
registration data, IP address geographical location data, and BGP routing table data are all selected before March 2019.

$\mathbf{l}$
A. Quantitative analysis results of multi-dimensional historical data Table I shows partial analysis results of the historical routing data. For every prefix-AS pair, the *frequency* is the number of occurrences of the prefix-AS pair in the collection period, and the *fscore* is the credibility of the *frequency*. The last *appear* is the last occurrence time of the prefix-AS pair and *lscore* is the credibility of the last *appear*. The rib *score* is the total score calculated by using the (1). From the results we can see, the prefix-AS pair (153.94.32.0/21, 25394) only appeared once in the collection period and its total score is lower than others, so the prefix 153.94.32.0/21 has a higher probability of being hijacked by AS 25394.

Table II shows partial analysis results of the historical registration data. The last *modified* is the last modification time of prefix-AS pair in the registration records. The reg *score* is the credibility of the last *modified* calculated by (2). When the reg *score* of the prefix-AS pair is 1, it indicates the pair has registered in IRR database and the last *modified* of the prefix-AS pair is the final registration time of the prefix. Table

| prefix          | ASN    | last modified       | reg score   |
|-----------------|--------|---------------------|-------------|
| 91.242.136.0/22 | 48427  | 2016-06-02 00:00:00 | 1           |
| 202.65.52.0/24  | 10131  | 2016-08-11 00:00:00 | 1           |
| 213.5.200.0/21  | 196858 | 2010-02-02 00:00:00 | 1           |
| 121,244.20.0/23 | 10199  | 2011-11-16 00:00:00 | 1           |
| 117.2.60.0/23   | 7552   | 2012-10-19 00:00:00 | 1           |

| prefix          | ASN    | #frequency   | fscore   | last appear      | lscore   | rib score   |
|-----------------|--------|--------------|----------|------------------|----------|-------------|
| 88.151.115.0/24 | 39596  | 117          | 0.9915   | 2019-02-28 00:00 | 1        | 0.9932      |
| 91.242.136.0/22 | 48427  | 118          | 1        | 2019-02-28 00:00 | 1        | 1           |
| 213.5.200.0/21  | 196858 | 118          | 1        | 2019-02-28 00:00 | 1        | 1           |
| 8.26.230.0/23   | 23089  | 118          | 1        | 2019-02-28 00:00 | 1        | 1           |
| 153.94.32.0/21  | 25394  | 1            | 0.0085   | 2019-02-28 00:00 | 1        | 0.2068      |
| 103.205.78.0/24 | 135009 | 72           | 0.6102   | 2019-01-12 00:00 | 0.605    | 0.60916     |
| 103.205.78.0/24 | 135002 | 33           | 0.2797   | 2019-02-28 00:00 | 1        | 0.42376     |

TABLE III

PARTIAL ANALYSIS RESULTS OF GEOGRAPHICAL LOCATION INFORMATION

prefix ASN country geo score

88.151.115.0/24 39596 RU 1

91.242.136.0/22 48427 ES 1

213.5.200.0/21 196858 PL 1

8.26.230.0/23 23089 US 1

180.98.0.0/16 4134 CN 1

III shows the analysis results of the prefix-AS geographical information. The geo *score* is the credibility of the prefixAS in geographical dimension. When the geo *score* is 1, it indicates that in the historical data, there is only one country corresponding to the prefix.

After obtaining the above scores from different dimensions, the integration results can be obtained by using the method in Section II-E. Table IV shows partial analysis results after the integration. In the integration, the credibility weight of the routing data, historical registration data, geographical information are 0.639, 0.274, and 0.087 respectively. The *total* score is the final credibility of the prefix-AS pair. The prefixAS pair (165.118.0.0/16, 1221) has a *total score* of 0, which suggests it has a high probability of being a prefix hijacking event.

## B. Prefix Hijacking Detection Results

The prefix hijacking events collected from BGPstream are used to evaluate the accuracy of the proposed hijacking

TABLE IV

PARTIAL ANALYSIS RESULTS OF MULTI-DIMENSIONAL HISTORICAL DATA

INTEGRATION

prefix ASN rib score reg score geo score total score

51.252.159.0/24 39891 1 0 1 0.726

101.127.0.0/17 38861 0 1 0 0.274

103.233.95.0/24 137166 0.42568 0 1 0.359

194.71.244.0/24 3301 1 1 1 1

165.118.0.0/16 1221 0 0 0 0

detection method. These hijacking events are from February 28, 2019 to December 25, 2019, with a total of 1487 pieces. We use the credibility of 0.5 as the threshold to determine whether it is prefix hijacking. Thus, if the credibility of the prefix-AS pair is less than or equal to 0.5, it is regarded as a prefix hijacking. Otherwise, it is regarded as a legal event. The results show that among the 1487 events, 99% of the events are detected as hijacking, and only 12 events are different.

For the inconsistent detection results, a reasonable analysis is given below.

Table V illustrates the 12 events. These events are determined as prefix hijacking by BGPstream while the proposed method classifies them as legal events. The columns of fields in Table V from left to right are IP prefix (*prefix*),
victim AS determined by BGPStream (*origin ASN*), credibility of victim's history routing data (origin rib), credibility of victim's historical registration data (origin reg), credibility of victim's geographic location (origin geo), victim's total credibility (origin *total*), hijack AS determined by BGPStream
(*hijacker ASN*), credibility of hijacker's history routing data
(hijack rib), credibility of hijacker's historical registration data (hijack reg), credibility of hijacker's geographic location
(hijack geo), and hijacker's total credibility (hijack *total*).

By comparing the scores in Table V, it can be seen that the score of the hijacker AS determined by BGPStream, is all above 0.66 in the dimension of historical routing data, which indicates that the prefix-AS pairs appear several times in historical routing data and the last occurrence time is close to the end collection time. In addition, there are four pairs of prefix-hijacker AS scored 1 in the dimension of historical registration information, indicating that these pairs have been recorded in IRR. Moreover, from origin *total* column in the Table V, there are 7 origin ASes that have a score of 0, and only one origin AS has a total score of more than 0.5. In the dimension of the historical routing data, there are 9 origin ASes with a score of 0, which means that these origin ASes have never announced the corresponding prefixes during the statistical period. However, the score of the hijacker AS in the historical routing data dimension is all greater than 0.7. In the dimension of historical registration information, there are 10 ASes with a score of 0, which suggests that there is no registration information for these prefix-AS pairs during the collection period.

For example, in the first event, BGP Stream determines the legal origin AS of prefix 85.235.68.0/2 is AS 42831, and the

| prefix           | origin ASN   | origin rib   | origin reg   | origin geo   | origin total   | hijacker ASN   | hijack rib   | hijack reg   | hijack geo   | hijack total   |
|------------------|--------------|--------------|--------------|--------------|----------------|----------------|--------------|--------------|--------------|----------------|
| 85.235.68.0/22   | 42831        | 0            | 0            | 0            | 0              | 206751         | 1            | 1            | 1            | 1              |
| 86.107.110.0/24  | 12874        | 0            | 0            | 0            | 0              | 44220          | 1            | 1            | 1            | 1              |
| 194.61.119.0/24  | 208425       | 0            | 0            | 0            | 0              | 201978         | 1            | 1            | 1            | 1              |
| 91.200.59.0/24   | 29405        | 0            | 0            | 0            | 0              | 43789          | 1            | 1            | 1            | 1              |
| 212.28.65.0/24   | 208671       | 0            | 0            | 0            | 0              | 51408          | 1            | 0            | 1            | 0.726          |
| 45.164.20.0/22   | 45382        | 0            | 0            | 1            | 0.087          | 174            | 1            | 0            | 0            | 0.639          |
| 93.120.94.0/24   | 50835        | 0.2068       | 1            | 1            | 0.4931         | 201636         | 0.99152      | 0            | 0            | 0.6336         |
| 77.73.20.0/22    | 15440        | 0.26776      | 1            | 1            | 0.5321         | 42366          | 0.91544      | 0            | 0            | 0.585          |
| 194.32.250.0/24  | 49392        | 0            | 0            | 0            | 0              | 31198          | 0.76272      | 0            | 1            | 0.5744         |
| 23.151.96.0/24   | 20119        | 0.35592      | 0            | 0            | 0.2274         | 395559         | 0.7484       | 0            | 1            | 0.5652         |
| 212.19.211.0/24  | 31122        | 0            | 0            | 0.5          | 0.0435         | 39855          | 0.75294      | 0            | 0.5          | 0.5246         |
| 198.240.112.0/24 | 132335       | 0            | 0            | 0            | 0              | 31863          | 0.66776      | 0            | 1            | 0.5137         |

hijacker AS is 206751. The three scores of AS 42831 are all 0, which means that AS 42831 has never announced the prefix 85.235.68.0/22 during the collection period and there are no related registration records in the IRR registration database.

From the above analysis, it can be concluded that the prefix-AS
pair (85.235.68.0/22, 206751) have a high degree of credibility and low possibility of prefix hijacking, so this may be a false alarm of BGPStream.

As shown in the above analysis, the detection result of the proposed method has a high overlap with the result of the commercial BGP anomaly detection agency BGPStream and can provide reliable performance in prefix hijacking detection.

## Iv. Conclusions

In this paper, we propose a novel prefix hijacking detection method based on multi-dimensional historical data analysis and implement a detection framework based on the method.

It quantifies three dimensions of historical data to obtain the credibility of prefix-AS pairs and uses this credibility to detect prefix hijacking. Compared with existing methods, the proposed method avoids the high cost of using active measurement technology and the low accuracy by using single dimension routing data. The results show that the proposed method has high accuracy (99%) in detecting prefix hijacking compared with BGPstream.

## Acknowledgment

This work is supported by the National Key R&D Program of China (No. 2018YFB1800404).

## References

[1] *BGP Hijacking Attacks Target US Payment Processors*, 2018. [Online].

Available: https://www.securityweek.com/bgp-hijacking-attacks-targetus-payment-processors
[2] *Russian-controlled telecom hijacks financial services' Internet traffic*, 2017. [Online]. Available: https://arstechnica.com/information-technology/2017/04/russiancontrolled-telecom-hijacks-financial-services-internet-traffic/
[3] K. Sriram, O. Borchert, O. Kim, P. Gleichmann, and D. Montgomery,
"A comparative analysis of bgp anomaly detection and robustness algorithms," in *2009 Cybersecurity Applications & Technology Conference* for Homeland Security. IEEE, 2009, pp. 25–38.

[4] A. Mitseva, A. Panchenko, and T. Engel, "The state of affairs in bgp security: A survey of attacks and defenses," *Computer Communications*,
vol. 124, pp. 45–60, 2018.

[5] M. Lad, D. Massey, D. Pei, Y. Wu, B. Zhang, and L. Zhang, "Phas:
A prefix hijack alert system." in *USENIX Security symposium*, vol. 1, no. 2, 2006, p. 3.

[6] P. Sermpezis, V. Kotronis, P. Gigis, X. Dimitropoulos, D. Cicalese, A. King, and A. Dainotti, "Artemis: Neutralizing bgp hijacking within a minute," *IEEE/ACM Transactions on Networking*, vol. 26, no. 6, pp.

2471–2486, 2018.

[7] J. Karlin, S. Forrest, and J. Rexford, "Pretty good bgp: Improving bgp by cautiously adopting routes," in *Proceedings of the 2006 IEEE*
International Conference on Network Protocols. IEEE, 2006, pp. 290–
299.

[8] G. Theodoridis, O. Tsigkas, and D. Tzovaras, "A novel unsupervised method for securing bgp against routing hijacks," in Computer and Information Sciences III. Springer, 2013, pp. 21–29.

[9] *The route views project*. [Online]. Available: http://www.routeviews.org/
[10] *The RIPE Routing Information Service*. [Online].

Available: https://www.ripe.net/analyse/internet-measurements/routinginformation-service-ris
[11] M. Tahara, N. Tateishi, T. Oimatsu, and S. Majima, "A method to detect prefix hijacking by using ping tests," in *Asia-Pacific Network Operations* and Management Symposium. Springer, 2008, pp. 390–398.

[12] Z. Zhang, Y. Zhang, Y. C. Hu, Z. M. Mao, and R. Bush, "ispy: Detecting ip prefix hijacking on my own," in *Proceedings of the ACM SIGCOMM* 2008 conference on Data Communication, 2008, pp. 327–338.

[13] C. Zheng, L. Ji, D. Pei, J. Wang, and P. Francis, "A light-weight distributed scheme for detecting ip prefix hijacks in real-time," ACM SIGCOMM Computer Communication Review, vol. 37, no. 4, pp. 277–
288, 2007.

[14] M. Chiesa, A. Kamisinski, J. Rak, G. R ´ etv ´ ari, and S. Schmid, "A survey ´
of fast recovery mechanisms in the data plane," 2020.

[15] G. Siganos and M. Faloutsos, "A blueprint for improving the robustness of internet routing," 2005.

[16] G. Siganos and M. Faloutsos, "Analyzing bgp policies: Methodology and tool," in *IEEE INFOCOM 2004*, vol. 3. IEEE, 2004, pp. 1640–1651.

[17] X. Hu and Z. M. Mao, "Accurate real-time identification of ip prefix hijacking," in *2007 IEEE Symposium on Security and Privacy (SP'07)*.

IEEE, 2007, pp. 3–17.

[18] M. A. Kumar and S. Karthikeyan, "Security model for tcp/ip protocol suite," *Journal of Advances in Information Technology*, vol. 2, no. 2, pp.

87–91, 2011.

[19] *IP2Location, db6-ip-country-region-city-latitude-longitude-isp*. [Online]. Available: https://www.ip2location.com/database/db6-ip-countryregion-city-latitude-longitude-isp
[20] E. W. Cheng and H. Li, "Analytic hierarchy process," *Measuring* business excellence, 2001.

[21] *CAIDA Routeviews Prefix to AS mappings* Dataset(pfx2as) for IPv4 and IPv6. [Online]. Available:
https://www.caida.org/data/routing/routeviews-prefix2as.xml
[22] M. Parimala, D. Lopez, and N. Senthilkumar, "A survey on density based clustering algorithms for mining large spatial databases," International Journal of Advanced Science and Technology, vol. 31, no. 1, pp. 59–66, 2011.