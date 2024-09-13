# Self-Similarity In World Wide Web Traffic: Evidence And Possible Causes

Mark E. Crovella, Member, *IEEE,* and Azer Bestavros, *Member, IEEE* 
Abstract-Recently, the notion *of self-similari~* **has been shown** 
to apply to wide-area and local-area network traffic. In this paper, we show evidence that the subset of network traffic that is due to World Wide Web (WWW) transfers can show characteristics that are consistent with self-similarity, and we present a hypothesized explanation for that self4milarity. Using a set of traces of actual user executions of NCSA Mosaic, we examine the dependence structure of WWW traffic. First, we show evidence that WWW 
traffic exhibits behavior that is consistent with self-similar traftic models. Then we show that the self-shnilarity in such traftic can be explained based an the underlying distributions of WWW 
document sizes, the effects of caching and user preference in tile transfer, the effect of user "think time," and the superimposition of many such transfers in a local-area network. To do this, we rely on empirically measured distributions both from client traces and from data independently collected at WWW servers. 

Zndex Terms--File **sizes, heavy tails, Internet, self-similarity,** 
World Wide Web. 

I. INTRODUCTION 
U NDERSTANDING the nature of network traffic is critical in order to properly design and implement computer networks and network services like the World wide Web. Recent examinations of LAN traffic [14] and wide-area network traffic [20] have challenged the commonly assumed models for network traffic, e.g., the Poisson process. Were traffic to follow a Poisson or Mark&an arrival process, it would have a characteristic burst length which would tend to be smoothed by averaging over a long enough time scale. Rather, measurements of real traffic indicate that significant traffic variance (burstiness) is present on a wide range of time scales. 

Traffic that is bursty on **many** or all time scales can be described statistically using *the* notion of *self-similarity.* Selfsimilarity is the property we associate with one type of fractal-an object whose appearance is unchanged regardless of the scale at which it is viewed. In the case of stochastic objects like time series, self-similarity is used in the distributional sense: when viewed at varying scales, the object's correlational structure remains unchanged. As a result, such a time series exhibits bursts-extended periods above the mean-at a wide range of time scales. 

Since a self-similar process has observable bursts at a wide range of time scales, it can exhibit *long-range dependence;* 

Manuscript received September 18. 1996; rexised June 4. 1997; approved by **IEEEfACM** TRAN~AC~ONS ON NETWORKING Editor C. Partridge. **This** work was supported in part by the National Science Foundation under Grant CCR9501822 and Grant CCR-9308344. 

The authors are with the Department of Computer Science, Boston University, Boston, MA 02215 USA (e-mail: crovella@cs.bu-edu; best@cs.bu.edu). 

Publisher Item Identifier S 1063~6692(97)08782-7. 
values at any instant are typically nonnegligibly positively correlated with values at all future instants. Surprisingly (given the counterintuitive aspects of long-range dependence), the self-similarity of Ethernet network traffic has been rigorously established [14]. The importance of long-range dependence in network traffic is beginuing to be observed in studies such as 
[S], [13], [18], which show that packet loss and delay behavior are radically different when simulations use either real traffic data or synthetic data that incorporate **long-range dependence.** 
However, the reasons behind self-similarity in Internet traffic have not been clearly identified. In this paper, we show that in some cases, self-similarity in network traffic can be explained in terms of file system characteristics and user behavior. In the process, we trace the genesis of self-similarity in network traffic back from the traffic itself, through the actions of file transmission, caching systems, and user choice, to the high-level distributions of file sizes and user event interarrivals. 

To bridge the gap between studying network traffic on the one hand and high-level system **characteristics on the other, we** 
make use of two essential tools. First, to explain self-similar network traffic in terms of individual transmission lengths, we employ the mechanism described in [30] (based on earlier work in [15] and [14]). Those papers point out that self-similar traffic can be constructed by multiplexing a large number of ON/OFF sources that have ON and OFF period lengths that are heavy-tailed, as defined in Section II-C. Such a mechanism could correspond to a network of workstations, each of which is either silent or transferring data at a constant rate. 

Our second tool in bridging **the gap** between **transmission** 
times and high-IeveI system characteristics is our use of the World Wide Web (or Web) as an object of study. The Web provides a special opportunity for studying network traffic because its traffic arises as the result of tile transfers from an easily studied set, and user activity is easily monitored. 

To study the traffic patterns of the Web, we collected reference data reflecting actual Web use at our site. We instrumented NCSA Mosaic [lo] to capture user access patterns to the Web. Since, at the time of our data collection, Mosaic was by far the dominant Web browser at our site, we were able to capture a **fairly complete** picture of Web **traffic on our local** 
network, our dataset consists of more than half a million user requests for document transfers and includes detailed timing of requests and transfer Iengths. In addition, we surveyed a number of Web servers to capture document size information that we used to compare the access patterns of clients with the access patterns seen at servers. 

The paper takes two parts. First, we consider the possibility of self-similarity of Web t&tic for the busiest hours we measured. To do so, we use analyses very sirniIar to those performed in [14]. These analyses support the notion that Web traffic may show self-similar characteristics, at least when demand is high enough. This result in itself has implications for designers of systems that attempt to improve performance characteristics of the Web. 

Second, using our Web traffic, user preference, and file size data, we comment on reasons why the transmission times and quiet times for any particular Web session are heavytailed, which is an essential characteristic of the proposed mechanism for the self-similarity of traffic. In particular, we argue that many characteristics of Web **use** can be modeled using heavy-tailed distributions, including the distribution of transfer times, the distribution of user requests for documents, and the underlying distribution of documents sizes avaiIable in the Web. In addition, using our measnrements of user interrequest times, we explore reasons for the heavy-tailed distribution of quiet times. 

## Ii. Background A. Dejnition Of Serf-Similarity

For a detailed discussion of self-similarity in time series data and the accompanying statistical tests, see [2], [29]. Our discussion in this subsection and the next cIosely follows those sources. 

Given a zero-mean, stationary time series X = (Xt; t = 
1, 2, 3, -*>, we define the m-aggregated series X(") = 
(X~m1;k=1,2,3,--)by summing the original series X 
over nonoverlapping blocks of size m. Then we say that X 
is *H-self-similar,* if for all positive m, Xc") has the same distribution as X resealed by mH. That is, 

$$X_{t}\stackrel{d}{=}m^{-H}\sum_{i=(t-1)m+1}^{t m}X_{i},\qquad{\mathrm{for~all~}}m\in N.$$

If X is H-self-similar, it has the same autocorrelation function y(k) = E[(Xt - p)(Xt+k - p)]/02 as the series X(m) for all m. Note that this means that the series is *distributionaffy* selfsimilar: the distribution of the aggregated series is the same 
(except for a change in scale) as .that of the original. 

As a result, self-simiIar processes can show long-range dependence. A process with long-range dependence has an autocorrelation function r(k) N L-p as k 4 m, where 0 c /? < 1. Thus, the autocorrelation function of such a process follows a power law, as compared to the exponential decay exhibited by traditional traffic models. Power-law decay is slower than exponential decay, and since /3 < 1, the sum of the autocorrelation values of such a series approaches intinlty. This has a number of implications. First, the variance of the mean of n samples from such a series does not decrease proportionally to l/n (as predicted by basic statistics for uncorrelated datasets), bui rather decreases proportionally to n-p. Second, the power spectrum of such a series is hyperbolic, rising to infinity at frequency zero-reflecting the 
"infinite" influence of *long-range* dependence in the data. 

One of the attractive features of using setf-similar models for time series, when appropriate, is that the degree of self-similarity of a series is expressed using only a single parameter. The parameter expresses the speed of decay of the series' autocorrelation function. For historical reasons, the parameter used is the Hurst parameter H = 1 -j3/2. Thus, for seIf-similar series with long-range dependence, l/2 < II < 1. 

As H t 1, the degree of both self-similarity **and** long-range dependence increases. 

## 3. Statisticpf Tests For Self-Similarity

In this paper, we use four methods to test for self-similarity, These methods are described fully in [2], and are the same methods described and used in [14]. A summary of the relative accuracy of these methods on synthetic datasets Is presented in [273. 

The *first* method, *the variance-timeplot,* relies on the slowly decaying variance of a self-sisnihu series. The variance of X("') is plotted against m on a log-log plot; a straight line with slope (-p) greater than - 1 is indicative of self-similarity, and the parameter H is given by *H = I- p/2. The* second method, the R/S plot, uses the fact that for a self-similnr dataset, the resculed range or *R/S* statistic grows according to a power iaw with exponent H as a function of the number of points included (n). Thus, the plot of *R/S* against 12 on a log-log plot has a slope which is an estimate of H. The thiid approach, the *periudogram* method, uses the slope of the power spectrum of the series as frequency approaches zero. 

On a log-log plot, the periodogram slope is a straight line with slope p - 1 = 1 - *2H close to the* origin. 

While the preceding three graphical methods are useful for exposing faulty assumptions (such as nonstationarity in the dataset), they do not provide confidence intervals, and ns developed in [27], they may be biased for Iarge *H. The* fourth method, called the WhiffZe esrimaror, does provide a confidence interval, but has the drawback that the form of the underlying stochastic process must be supplied. The two forms thnt nre most commonly used are fractional Gaussian noise (FGN) with parameter l/2 < H < 1, and fractional ARIMA (p$ rl, r7) with 0 < d < l/2 (for details, see [2], [4]). These two models differ in their assumptions about the short-range dependences in the datasets; FGN assumes no short-range dependence, while fractionaI ARMA can assume a fixed degree of short-range dependence. 

Since we are concerned only with the long-range dependence in our datasets, we employ the Whittle estimator ns follows. Each hourly dataset is aggregated at increasing levels m, and the Whittle estimator is applied to each m-aggregated dataset using *the* FGN modeI. This approach expIoits the property that any Iong-range dependent process approaches FGN when aggregated to a sufficient level, and so should be coupled with a test of the marginal distribution of the aggregated observations. to ensure that it has converged to the normal distribution. As m increases, short-range dependences are averaged out of the dataset; if the value of H remains relatively constant, we can be confident that it measures a true underlying level of self-similarity. Since aggregating the series shortens it, confidence intervals will tend to grow as the aggregation level increases; however, if the estimates of H appear stable as the aggregation level increases, then we consider the confidence intervals for the unaggregated dataset to be representative. 

## C. Heavy-Tailed Distributions

The distributions we use in this paper have the property of being *heavy-tailed.* A distribution is heavy-tailed if 

$$P[X>x]\sim x^{-\alpha},\qquad\mathrm{as}\quad x\rightarrow\infty,\quad0<\alpha<2.$$

That is, regardless of the behavior of the distribution for small values of the random variable, if the asymptotic shape of the distribution is hyperbolic, it is heavy-tailed. 

The simplest heavy-taiIed distribution is *the Pareto* distribution. The Pareto distribution is hyperbolic over its entire range; its probability mass function is 

$$p(x)=\alpha k^{\alpha}x^{-\alpha-1},\qquad\alpha,k>0,\quad x\geq k$$

and its cumulative distribution function is given by 

$$F(x)=P[X\leq x]=1-(k/x)^{\alpha}.$$

The parameter L represents the smallest possible value of the random variable. 

Heavy-tailed distributions have a number of properties that are qualitatively different from distributions more commonly encountered such as the exponential, normal, or Poisson distributions. If a! 5 2, then the distribution has infinite variance; if a < 1, then the distribution has infinite mean. Thus, as a decreases, an arbitrarily large portion of the probability mass may be present in the tail of the distribution. In practical terms, a random variable that follows a heavy-tailed distribution can give rise to extremely large values with nonnegligible probability (see [20] and [16] for details and examples). 

To assess the presence of heavy tails in our data, we employ log-Zag complementary *distribution* (LLCD) plots. These are plots of the complementary cumulative distribution P(z) = 
1 - F(z) = P[X > z] on log-log axes. Plotted in this way, heavy-tailed distributions have the property that 

$$\frac{d\log\bar{F}(x)}{d\log x}=-\alpha,\qquad x>\theta$$

for some 0. To check for the presence of heavy tails in practice, we form the LLCD plot, and look for approximately linear behavior over a significant range (three orders of magnitude or more) in the tail. 

It is possible to form rough estimates of the shape parameter Q from the LLCD plot as well. First, we inspect the LLCD 
plot, and choose a value for B above which the plot appears to be linear. Then we select equally spaced points from among the LLCD points larger than 8, and estimate the sIope using least squares regression.' The proper choice of 0 is made based on inspecting the LLCD plot; in this paper, we identify the B 
'Equally spaced points are used because the point density varies over the range used, and the preponderance of data points at small values would otherwise unduly influence the least squares regression. 

used in each case, and show the resulting fitted line used to estimate cr. 

Another approach we used to estimating tail weight is the Hill estimator (described in detail in [30])= The Hill estimator uses the k: largest values from a dataset to estimate the value of Q for the dataset. In practice, one plots the Hill estimator for increasing values of k, using only the portion of the tail that appears to exhibit power-law behavior; if the estimator settles to a consistent value, this value provides an estimate of (Y. 

## M. Blated Work

The first step in understanding WWW traftic is the collection of trace data. Previous measurement studies of the Web have focused on reference patterns established based on logs of proxies [ll], [25] or servers 1213. The authors in 
[5] captured client traces, but they concentrated on events at the *user* interface'level in order to study browser and page design. In contrast, our goal in data collection was to acquire a complete picture of the reference behavior and timing of user accesses to the WWW. As a result, we collected a large dataset of client-based traces. A full description of our traces (which are avaiIabIe for anonymous FTP) is given in [6]. 

Previous wide-area traffic studies have studied PIP, TELICI', &fNTP, and SMTP traffic [19], [20]. Our data complement those studies by providing a view of WWW (I-I'ITP) 
trafftc at a "stub" network. Since WWW traffic accounts for a large fraction of the traftic on the Internet? understanding the nature of WWW traftic is important. 

The benchmark study of self-similarity in network trafhc is 
[14], and our study uses many of the same methods used in that work. However, the goal of that study was to demonstrate the self-similarity of network traffic; to do that, many large datasets taken from a multiyear span were used. Our focus is not on establishing self-similarity of network traffic (although we do so for the interesting subset of network traffic that is Web-related); instead, we concentrate on examining the reasons behind self-similarity of network traflic. As a result of this different focus, we do not analyze traftic datasets for low, normal, and busy hours. Instead, we focus on the four busiest hours in our logs. While these four hours are well described as self-similar, many Iess busy hours in our logs do not show self-similar characteristics. We feel that this is only the result of the traffic demand present in our logs, which is much lower than that used in [14]; this belief is supported by the findings in that study, which showed that the intensity of sellXmilarity increases as the aggregate traffic level increases. 

Our work is most similar m intent to 1301. That paper looked at network traffic at the packet level, identified the flows between individual source/destination pairs, and showed that transmission and idle times for those flows were heavytailed. In contrast, our paper is based on data collected at the application 1eveI rather than the network level. As a result, we are able to examine the relationship between transmission times and file sizes, and are able to assess the effects of caching and user preference on these distributions. These observations allow us to build on the conclusions presented 
'See,for example.data athttp://~~~.nlanr.net/INFO/. 

in [3OJ, and confirm observations made in [20] by showing that the heavy-tailed nature of transmission and idle times is not primariIy a result of network protocols or user preference, but rather stems from more basic properties of information storage and processing: both fiIe sizes and user "think times" are themselves strongly heavy-tailed. 

## Iv. Examnng Web Traffic Self-Sdjilanty

In this section, we show evidence fiat WNW fraffic can be self-similar. To do so, we first describe how we measured WWW traffic; then we apply the statistical methods described in *Section* II to assess self-similarity. 

In order to reIate traffic patterns to higher level effects, we needed to capture aspects of user behavior as well as network demand. The approach we took to capturing both types of data simultaneously was to modify a WWW browser so as to log a11 user accessed to the Web. The browser we used was Mosaic since its source was publicly available and permission has been granted for using and modifying the code for research purposes. A complete description of our data cohection methods and the format of the log files is given in [6]; here, we onIy give a high-level summary. 

We modified Mosaic to record the uniform *resource* locator 
(UFtL) [33 of each file accessed by the Mosaic user, as well as the time the file was accessed and the time required to transfer the file from its server (if necessary). For completeness, we record all URLs accessed whether they were served from Mosaic's cache or via a file transfer; however, the traffic time series we analyze in this section consist only of actual network transfers. 

At the time of our study (January and February 19953, Mosaic was the WWW browser preferred by nearly all users at our site. Hence, our data consist of nearly all of the WWW 
traffic at our site. Since the time of OUT study, users have come to prefer commericial browsers which are not available 
'in sonrce form. As a result, capturing an equivalent set of WWW user traces at the current time would be more difficult, The data captured consist of the sequence of WWW file requests performed during each session, where a session is one execution of NCSA Mosaic. Each file request is identified by its URL, and session, user, and workstation ID; associated with the request is the time stamp when the request was made, the size of the document (inchtding the overhead of the protocol), and the object retrieval time. Time stamps were accurate to 10 ms. Thus, to provide three significant digits in our results, we limited *our* analysis to time intervals greater than or equal to 1 s. To convert OUT logs to traffic time series, it was necessary to allocate the bytes trausferred in each request equalIy into bins spanning the transfer duration. Although this process smooths out short-term variations in the traffic flow of each transfer, our restriction to time series with gramiIarity of 1 s or more-combined with the fact that most file transfers are short [6]-means that such smoothing has little effect on our results. 

| TABLE I                                                                                                                                |                               |
|----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| SUMMARY STATETICS FOR                                                                                                                  | TRACE DATA USED IN THIS STUDY |
| Sessions  Users  URLs Requested  files Transferred  Unique Files Requested  Bytes Requested  Bytes Transferred  Unique Bytes Requested |                               |

4700 

591 

515,775 

130,140 

46,830 

2713 MB 

1849 MB 

maa MB 

To collect our data, we installed our instrumented version of Mosaic in the general computing environment at Boston University's Department of Computer Science. This environment consists principally of 37 SparcStation-2 workstations connected in a local network. Each workstation has its own local disk; logs were written to the local disk, and subsequently transferred to a central repository. Although we collected data from November 21, 1994 through May 8, 1995, the data used in this paper are only from the period January 17, 1995 'to February 28, 1995. This period was chosen because departmental WWW *usage was* distinctly lower (and the pool of users less diverse) before the start of classes in early January, and because by early March 1995, Mosaic had ceased to be the dominant browser at our site. A statistical summary of the trace data used in this study is shown in Table I. 

## B. Self-Similarity Of Www **Trafj**

Using the ?VWW traffic data we obtained as described in the previous section, we show evidence consistent wilh the conclusion that WWW traffic is self-similar on time scales of 1 s and above. To do so, we show that for four busy hours from our traffic logs, the Hurst parameter H for our datasets is significantly different from l/2. 

We used the four methods for assessing self-similarity described in Section II: the variance-time plot, the resealed range (or R/S) plot, the periodogram plot, and the Whittle estimator. We concentrated on individual hours from our traffic series, so as to provide as nearly a stationary dataset as possible. 

To provide an example of these approaches, analysis of a single hour (4-5 P.M., Thursday, February 5,1995) is shown in Fig. 1. The figure shows plots for the three graphical methods: 
variance-time (upper left), resealed range (upper right), and periodogram (Iower center). The variance-time pIot is linear, and shows a slope that is distinctly different from -1 {which is shown for comparison); the slope is estimated using regression as -0.48, yielding an estimate for H of *0.76. The R/S* plot shows an asymptotic sIope that is different from 0.5 and from 1.0 (shown for comparision); it is estimated using regression as 0.75, which is also the corresponding estimate of H. The periodogram plot shows a slope of -0.66 (the regression line is shown), yiekling an estimate of H as 0.83. Finally, the Whittle estimator for this dataset (not a graphical method) yields an estimate of H = 0.82 with a 95% confidence interval of (0.77, 0.87). 

As discussed in Section II-B, the Whittle estimator is the only method that yields confidence intervals on H, but it 

CROVELLA AND BESTAVROS: SELF-SIMILARITY IN ?4WW TRAFFIC 839 

![4_image_0.png](4_image_0.png)

- -- 
l 
requires that the form of the undedying time series be provided. We used the fractional Gaussian noise model, so it is important to verify that the underlying series behaves lie FGN, namely, that is has a normal marginal distribution, and that additional short-range dependence is not present. We can test whether lack of normahty or short-range dependence is biasing the Whittle estimator by m-aggregating the time series for successively large values of m, and determiuing whether the Whittle estimator remains stable since aggregating the series will disrupt short-range correlations and tend to make the marginal distribution closer to the normal. 

The results of this method for four busy hours are shown in Fig. 2. Each hour is shown in one plot, from the busiest hour (largest amount of total traffic) in the upper left to the least busy hour in the lower right. In these figures, the solid line is the value of the Whittle estimate of H as a function of the aggregation level rn of the dataset. The upper and lower dotted lines are the limits of the 95% confidence interval on H. The three level lines represent the estimate of H for the unaggregated dataset as given by the variance&me, R-S, and periodogram methods. 

The figure shows that for each dataset, the estimate of H 
stays relatively consistent as the aggregation level is increased, and that the estimates given by the three graphical methods fall well within the range of H estimates given by the Whittle estimator. The estimates of H given by these plots are in the range 0.748, consistent with the values for a lightly loaded network measured in [ 141. Moving from the busier hours to the less busy hours, the estimates of H seem to decline somewhat, and the variance in the estimate of H increases, which are also conclusions consistent with previous research. 

Thus, the results in this section show evidence that WWW 
traffic at stub networks might be self-similar when traffic demand is high enough. We expect this to be even more pronounced on backbone links, where traftic from a multitude of sources is aggregated. In addition, WWW traffic in stub networks is likely to become more self-similar as the demand for, and utilization of, the WWW increase in the future. 

## V. Explaining Web Traffic Self-Similarmy

While the previous section showed evidence that Web traffic can show self-similar characteristics, it provides no explanation for this result. This section provides a possible explanation, based on measured characteristics of the Web. 

## A. Superimposing Heavy-Tailed Renewal Processes

Our starting point is the method of constructing self-similar processes described in [30], which is a refinement of work done by Mandelbrot [15] and Taqqu and Levy [28]. A selfsimilar process may be constructed by superimposing many simple renewal reward processes, in which the rewards are restricted to the values 0 and 1, and in which the interrenewal times are heavy-tailed. As described in Section II, a heavy- 

![5_image_0.png](5_image_0.png)

tailed distribution has infinite variance, and the weight of its tail is determined by the parameter & < 2. 

This construction can be visualized as follows. Consider a large number of concurrent processes that are each either ON or OFF. The ON and **OFF** periods for each process strictly alternate, and either the distribution of ON times is heavy-tailed with parameter (~1, or the distribution of **OFF** times is heavy-tailed with parameter CYZ, or both. At any point in time, the value of the time series is the number of processes in the ON state. Such a model could correspond to a network of workstations, each of which is either silent or transferring data at a constant rate. 

For this model, it has been shown that the result of aggregating many such sources is a self-similar fractional Gaussian noise process, with H = (3 - min(crl, a~))/2 [30]. 

Adopting this model to explain the self-similar& of Web traffic *requires* an explanation for the heavy-tailed distribution of either ON or **OFF** times. h~ our system, ON t&es correspond to the transmission durations of individual Web files (although this is not an exact fit since the model assumes *constant trans-*mission rate during the ON times), and **OFF** times correspond to the intervals between transmissions. So we need to ask whether Web file transmission times or quiet times are heavy-taiIed, and if so, *why.* 
Unlike traffic studies that concentrate on network-level and transport-level data transfer rates, we have availabIe application-level information such as the names and sizes of files being transferred, as weU as their transmission times. 

![5_image_1.png](5_image_1.png) 
Thus, to answer these questions, we can analyze the characteristics of onr client logs. 

## B. Examining Transmission Emes

I) Tke DisA-in'bufion of *Web Transmission i%tes:* Our first observation is that the distribution of Web file transmission times shows nonnegligible probabilities over a wide range of file sizes. Fig. 3(a) shows the LLCD plot of the durations of all 130 140 transfers that occurred during the measurement period. The shape 'of the upper tail on this plot, while not strictly linear, shows only a sIight downward trend over almost four orders of magnitude. This is evidence of very high variance (although perhaps not infinite) in the underlying distribution. 

From this plot, it is not clear whether actual ON times in the Web would show heavy tails because our assumption equating file transfer durations with actual ON limes is an oversimplification (e.g., the pattern of packet arrivals during fiIe transfers may show large gaps). However, if we hypothesize that the underlying distribution is heavy-tailed, then this property wouId seem to be present for values greater fhan about 0.5, which corresponds roughly to largest 10% of all transmissions (log,,(P[X > 2)) < -1). 

A least squares tit to evenly spaced data points grenter than -0.5 (B" = 0.98) has a slope of -1.21, which yields 
& = 1.21. Fig. 3(b) shows the value of the Hill estimator for varying k, again restricted to the upper 10% tail. The Hill plot 

![6_image_1.png](6_image_1.png)

transmission times of Web files. 
shows that the estimator seems to settle to a relatively constant estimate, consistent with & M 1.2. 

Thus, although this dataset does not show conclusive evidence of infinite variance, it is suggestive of a very high or infinite variance condition in the underlying distribution of ON 
times. Note that the result of aggregating a large number of ON/OFF processes in which the distribution of ON times is heavy-tailed with a = 1.2 should yield a self-similar process with H = 0.9, while our data generally show values of H in the range 0.7-0.8. 

2) Why Are Web Transmission Emes Highly Variable?: To understand why transmission times exhibit high variance, we now examine size distributions of Web files themselves. First, we present the distribution of sizes for file transfers in our logs. The results for all 130 140 transfers are shown in Fig. 4, which is a plot of the LLCD and the Hi11 estimator for the set of transfer sizes in bytes. Again, choosing the point at which power-law behavior begins is difficult, but the figure shows that for file sizes greater than about 10 000 bytes, transfer size distribution seems reasonably well modeled by a heavy-tailed distribution. This is the range over which the Hill estimator is shown in the figure. 

A linear fit to the points for which file size is greater than 10 000 yields & = 1.15 (R2 = 0.99). The Hill estimator shows some variability in the interval between 1 and 1.2, but its estimates seem consistent with d x 1.1. 

![6_image_0.png](6_image_0.png)

Fig. 4. LLCD and Hill estimator for sizes of Web file transfers. 
Interestingly, the authors in [20] found that the upper tail of the distribution of data bytes in FTP bursts was well fit to a Pareto distribution with 0.9 5 Q 2 1.1. Thus, our results indicate that with respect to the upper tail distribution of file sizes, Web transfers do not differ significantly from FI'P traffic; however, our data also allow us to comment on the reasons behind the heavy-tailed distribution of transmitted files. 

An important question then is: Why do file transfers show a heavy-tailed distribution? On the one hand, it is clear that the set of files requested constitutes user "input" to the system. It is natural to assume that file requests therefore might be the primary determiner of heavy-tailed file transfers. If this were the case, then perhaps changes in user behavior might affect the heavy-tailed nature of file transfers, and by implication, the self-similar properties of network traftic. 

In fact, in this section, we argue that the set of file requests made by users is nor the primary determiner of the heavy-tailed nature of file transfers. Rather, file transfers seem to be more stongly determined by *the* set of files *available* in the Web. 

To support this conclusion, we present characteristics of two more datasets. First, we present the distribution of the set of all requests made by users. This sei consists of 575 775 files, and contains both the requests that were satisfied via the network and the requests that were satisfied from Mosaic's cache. Second, we present the distribution of the set of *unique* files that were transferred. This set consists of 46 830 files, all different. These two distributions are shown in Fig. 5. 

![7_image_1.png](7_image_1.png)

Fig. 5. LLCD of {a) file requests and (b) unique files. 
The figure shows that both distributions appear to be heavytailed. For the set of file requests, we estimated the tail to start at approximately sizes of 10000 bytes; over @is range, the slope of the LLCD plot yields an 8 of about 1.22 (B2 = 0.99>, 
while the Hill estimator varies between approximately 1.0 and 1.3. For the set of unique files, we estimated the tail to start at approximately 30000 bytes. The slope estimate over this range is 8 of about I.12 (R' = 0.99>, and the Hill estimator over this range varies between 1.0 and 1.15. 

The relationship between the three sets can be seen more clearly in Fig. 6, which plots all three distributions on the same axes. This figure shows that the set of file transfers is intennediare in characteristics between the set of file requests and the set of unique files. For example, the median size of the set of file transfers lies between the median sizes for the sets of file requests and unique files. 

The reason for this effect can be seen as the natural result of caching. If caches were infinite in size-and shared by all users, the set of file transfers would be identical to the set of unique files since each tie would miss in the cache only once. If finite caches are performing well, we can expect that they are attempting to approximate the effects of an infinite cache. Thus, the effect of caching (when it is effective) 
is to adjust the distributional characteristics of the set of transfers to approximate those of the set of unique files. In the case of our data, it seems that NCSA Mosaic was able to achieve a reasonable approximation of the performance of 

![7_image_0.png](7_image_0.png)

Fig. 6. LLCD plots of the different distributions. 
0 1 2 3 4 5 6 7 8 0 1 2 3 4 5 6 7 8 LoglO(FiIe Size in Bytes) LoglO(File Size in Bytes) 

![7_image_2.png](7_image_2.png)

Fig. 7. LLCD plots of the unique files and available files. 
an infinite cache, despite its finite resources: from Table I, 
we can calculate that NCSA Mosaic achieved a 77% hit rate 
(l-130 1401575 7751, while a cache of infinite size (shared by all users) would achieve a 92% hit rate (1 - 46 830/575 775). 

What, then, determines the distribution of the set of unique files? To help answer this question, we surveyed 32 Web servers scattered throughout North America. These servers were chosen because they provided a usage report based on www-stat 1.0 1231. These usage reports provide information sufficient to determine the distribution of file sizes on the server (for files accessed during the reporting period). In each case, we obtained the most recent usage reports (as of July 1995), for an entire month if possible. While this method is not a random sample of files available in the Web, it sufficed for the purpose of comparing distributional characteristics. 

In fact, the distribution of all of the available files present on the 32 Web servers closely matches the distribution of the set of unique files in our client traces. The two distributions are shown on the same axes in Fig. 7. Although these two distributions appear very similar, they are based on completely different datasets. That is, it appears that the set of unique files can be considered, with respect to sizes, to be a sample from the set of all files available on the Web.. 

This argument is based on the assumption that cache mnnagenient policies do not specifically exclude or include files based on their size; and that unique files are sampled without respect to size from the set of available files. While these assumptions may not hoId in other contexts, the data shown 

![8_image_0.png](8_image_0.png)

Fig, 8. LLCD of file sizes available on 32 Web sites, by file type. 
in Figs. 6 and 7 seem to support them in this case. Thus, we conclude that as long as caching is effective, the set of files available in the Web is likely to be the primary determiner of the heavy-tailed characteristics of tiles transferred-and that the set of requests made by users is relatively less important. 

This suggests that available files are of primary importance in determining actual traffic composition, and that changes in user request patterns are unlikely to result in significant changes to the self-similar nature of Web traftic. 

3) Why Are Avaiiabie Files Heavy-Taifed?: If available files in the Web are, in fact, heavy-tailed, one possible explanation might be that the explicit support for multimedia formats may encourage larger file sizes, thereby increasing the tail weight of distribution sizes. While we find that multimedia does increase tail weight to some degree, in fact, it is not the root cause of the heavy tails. This can be seen in Fig. 8. 

Fig. 8 was constructed by categorizing all server files into one of seven categories, based on file extension. The categories we used were: *images, text, audio, video, aichives, prefermatted text,* and *compressed* jles. This simple categorization was able to encompass 85% of all files. From this set, the categories *images, text, audio,* and *video* accounted for 97%. 

The cumulative distribution of these four categories, expressed as a fraction of the total set of files, is shown in Fig. 8. In the figure, the upper line is the distribution of all accessed files, which is the same as the available fiIes line shown in Fig, 7. The three intermediate lines are the components of that distribution attributable to images, audio, and video. The lowest line (at the extreme right-hand point) is the component attributable to text (I-ITML) alone. 

The figure shows that the effect of adding multimedia files to the set of text files serves to translate the tail to the right. 

However, it also suggests that the distribution of text files may itself be heavy-tailed. Using Ieast squares fitting for the portions of the distributions in which log,,,(~) > 4, we find that for all files available & = 1.27, but that for the text files only, d = 1.59. The effects of the vat-ions multimedia types are also evident from the figure. In the approximate range. 

of 1000-30000 bytes, tail weight is primarily increased by images. In the approximate range of 30 000-300 000 bytes, tail weight is increased mainly by audio files. Beyond 300 000 bytes, tail weight is increased mainly by video tiles. 

![8_image_1.png](8_image_1.png)

Fig. 9. Comparison of Unix tile sizes with Web file sizes. 
The fact that file size distributions have very long tails has been noted-before, particularly in tile-system studies [l], 
[9], [17], 1221, 1241, [2151; however, they have not explicitly examined the tails for power-law behavior, and measurements of Q! values have been absent. As an example, we compare the distribution of Web tiles found in our logs with an overall distribution of files found in a survey of Unix file systems. 

While there is no truly "typical" Unix file system, an aggregate picture of file sizes on over 1000 different Unix file systems was collected by Irlam in 1993? In Fig. 9, we compare the distribution of document sizes we found in the Web with those data. The figure plots the two histograms on the same log-log scale. 

Surprisingly, Fig. 9 shows that in-our Web data, there is a sfronger preference for small files than in Unix file systemsP The Web favors documents in the 256-512 byte range, while Unix files are more commonly in the l-4 kbyte range. More importantly, the tail of the distribution of Web files is not nearly as heavy as the tail of the distribution of Unix files. 

Thus, despite the emphasis on multimedia in the Web, we conclude that Web file systems are currently more biased toward smalI files than are typical Unix file systems. 

In conclusion, these observations seem to show that heavytailed size distributions are not uncommon in various data storage systems. It seems that the possibility of very large file sizes may be nonnegligible in a wide range of contexts, and that in particular, this effect is of central importance in understanding the genesis of self-similar traffic in the Web. 

## C. Examining Quiet Emes

In Section V-A, we attributed tbe self-similarity of Web traffic to the superimposition of heavy-tailed **ON/OFF** processes, where the ON times correspond to the transmission durations of individual Web files and **OFF** times correspond to periods when a workstation is not receiving Web data. while ON times are the result of a positive event (transmission), **OFF** times are 3Tbese data are available from http: //www.base.com/gordoni/ 
ufs93.html 4However; not shown in tbe figure is the fact that while there are virtually no Web files smaller tbao 100 bytes, there is a significant number of Unix= 
files smaller than 100 bytes, including many zero- and one-byte files. 

![9_image_1.png](9_image_1.png)

0 
. 

Fig. **10. LLCD** plot of OFF times showing active and inactive regimes. 
a negative event that could occur for a number of reasons. 

The workstation may *not* be receiving data because it has just finished receiving one component of a Web page (say, text containing an inlined image), and is busy interpreting, formatting, and dispraying it before requesting the next component (say, the inlined image). Or, the workstation may not be receiving data because the user is inspecting the results of the **last transfer, or** *not* actively *using* the Web at all. We wiI1 call these two conditions "active **OFF"** time and "'inactive OFF" time. The difference between active **OFF** time and inactive OFF time is important in und&tanding the distribution of **OFF** 
times considered in this section. 

In contrast to the other distributions we study in this paper, Fig. 10 shows that the distribution of **OFF** times is not well modeled by a distribution with constant Q. Instead, there seem to be two regimes for o. The region from 1 ms to 1 s forms one regime; *the* region from 30 to 3000 s forms another regime; in between the two regions, the curve is in transition. 

The difference between the two regimes in Fig. 10 can be explained in terms of active **OFF** time versus inactive **OFF** 
time. Active OFF times represent the time needed by the client machine to process transmitted files (e.g., interpret, format, and display a document component). It seems reasonable that OFF times in the range of 1 ms-1 s are not primarily due to users examining data, but are more likely fo be strongly determined by machine processing and display time for data items that are retrieved as part of a multipart document. This distinction is illustrated in Fig. 11. For *this* reason, Fig. 10 shows the 1 ms-1 s region as active **OFF** time. On the other hand, it seems reasonable that very few e&e&d components would require 30 s or more to interpret, format, and display. 

Thus, we assume that **OFF** times greater than 30 s are primarily user-determined, inactive **OFF** times. 

![9_image_0.png](9_image_0.png)

![9_image_2.png](9_image_2.png)

Fig. 12. Histogram of interarrival time of URL requests, 
indicates that the heavy-tailed nature of *OFF* times is primarily due to inactive *OFF* times that resuIt from user-induced delays, rather than from machine-induced delays or processing. 

To extract **OFF** times from our traces, we adopt the following definitions. Within each Mosaic session, let a; be the absolute arrival time of IJRL request i. Let q be thi: absolute compleriun time of the transmission resulting from URL request i. 

It folIows that (Q - ai) is the random variable of ON times 
(whose distribution was shown in Fig. 3), whereas (ci+l - cr) 
is the random *variable* of **OFF** times. Fig. 10 shows the LLCD 
plot of (&i+1 - r$. 

Another way of characterizing these two regimes is through the examination of the interarrival times of URL 
requests-namely, the distribution of a;+1 - ai. Fig. 12 shows that distribution. 

The "dip" in the distribution in Fig. I2 reflects the presence of two underlying distributions. The first is the interarrival of URL requests generated in response to a single user request 
(or-user dick). The second is the interarrival of URL requests generated in response to two consecutive user **requests,** The difference between these distributions is that the former is affected by the distribution of ON times and the distribution of active OFF times, whereas. the latter is affected by the distribution of ON times, active *OFF* times, and inactive OFF 
times. A recent study 173 confirmed this observation by annlyzing and characterizing the distribution of document request arrivals at access links. This study, which was based on two datasets different from ours,s concluded that the two regimes exhibited in Fig. 10 could be emphically modeled using a Weibull distribution for the interanival of URL requests during the active regime, and a Pareto distribution for the inactive OFF times. 

For self-similarity via aggregation of heavy-tailed renewal processes, *the* important part of the distribution of *OFF* times is its tail. Measuring the vahre of 01 for the tail of the distribution 
(OFF times greater than 30 s) via the slope method yields 
& = 1.50 (R* = 0.99). Thus, we see that the OFF times measured in our traces may be heavy-tailed, but with lighter taiIs than the distribution of ON times. In addition, we argue 

This delineation between active and inactive OFF times explains the two notable slopes in Fig. 10; furthermore, it SNamely, the Web traffic monitored at a corporate firewall during two **2-h** 
sessions. 
that any heavy-tailed nature of OFF times is a result of user rKrzk *rime* rather than machine-induced delays. 

Since we saw in the previous section that ON times were heavy&ted with Q = 1.0-1.3, and we see in this section that OFF times are heavy tailed with Q N" 1.5, we conclude that ON 
times (and, consequently, the distribution of available files in the Web) are more likely responsibIe for the observed level of traffic self-similarity, rather than **OFF** times. 

## Vi. Conclusion

In this paper, we have shown evidence that tmftic due to World Wide Web transfers shows characteristics that are consistent with seIf-similarity. More importantly, we have traced the genesis of Web traffic self-similarity aIong two threads: first, we have shown that transmission times may be heavy-tailed, primarily due to the distribution of available file sizes in the Web. Second, we have shown that silent times also may be heavy-tailed, primarily due to the influence of user "think time." 
Comparing the distributions of ON and **OFF** times, we find that the ON time distribution is heavier tailed than the **OFF** time distribution. The model presented in [30] indicates that when comparing the ON and **OFF** times, the distribution with the heavier tail is the determiner of actual trafIic self-similarity levels. Thus, we feel that the distribution of file sizes in the Web (which determine ON times) is likely the primary determiner of Web traffic self-simihuity. In fact, the work presented in [18] has shown that the transfer of files whose sizes are drawn from a heavy-tailed distribution is sufficient to generate self-similarity in network traffic. 

These results seem to trace the causes of Web traffic self-similarity back to basic characteristics of information organization and retrieval. The heavy-tailed distribution of file sizes we have observed seems similar in spirit to Pareto distributions noted in the social sciences, such as the distribution of lengths of books on library shelves, and the distribution of word lengths in sample texts (for a discussion of these effects, see [16] and citations therein). In fact, in other work 
[6], we show that the rule known as Zipf s law (the degree of popularity is exactly inversely proportional to the rank of popularity) applies quite strongly to Web documents. The heavy-tailed distribution of user think times also seems to be a feature of human information processing (e.g., [21]). 

These results suggest that the self-similarity of Web trafhc is not a machine-induced artifact; in particular, changes in protocol processing and document display are not likely to fundamentally remove the seIf-similarity of Web traffic (although some designs may reduce or increase the intensity of self-similarity for a given level of traffic demand). 

A number of questions are raised by this study. First, the generalization from Web traftic to aggregated wide-area traffic is not obvious. While other authors have noted the heavy-tailed distribution of FTP transfers [20], extending our approach to wide-area traffic in general is difficult because of the many sources of traffic and **determiners** of traffic demand. 

A second question concerns the amount of demand required to observe self-similarity in a traffic series. As the number of sources increases, the statistical confidence in judging selfsimilarity increases; however, it is not clear whether the important effects of self-similarity (burstiness at a wide range of scales and the resulting impact on buffering, for example) 
remain even at low levels of tic demand. 

## Acknowledgment

The authors thank M. Taqqu and V. Teverovsky of the Department of Mathematics, Boston University, for many helpful discussions concerning long-range dependence. The authors also thank V. Paxson and an anonymous referee whose comments substantially improved the paper. C. **Cunha** 
instrumented Mosaic, collected the trace logs, and extracted some of the data used in this study. Finally, the authors also thank the other members of the Oceans Research Group at Boston University for many thoughtful discussions. 

[1] M. G. Baker, 3. H. Hartman, M. D. Kupfer, K W. Shhriff, and J. K. 

Ousterhout, "Measurements of a distributed file system," in *Proc.* **13th** 
ACM Symp. Open Syst. *Principles,* **Pacific Grove, CA, Oct. 1991. pp.** 
198-212. 

121 _ _ J. Beran, *Statisics for Lon.e-Memory Processes Nonouavhs on* **Statistics and Applied Kobabiliiy). London: Chap&t andHaIl. 1994.** 
[3] T. Berners-Lee, L. Masinter, and M. McCabill, UniJbrm Resortme 
.Lmurors, RFC 1738. Dec. 1994. 

141 - _ P. J. Bmckwell and R. A. Davis. *lime Series: Theorv and Methods* 
(Springer Series in Statistics), 2nd ed. New York: Springer-Verlag. 

1991. 

[5] L. D. Catledge and J. E. Pitkow, "Characterizing browsing strategies in the World-Wide Web," in *Proc 3rd WWW Con/..* **1994.** 
[6] C. R. Cunha, A. Bestavms, and M. E. Crovella, "Characteristics of WWV client-based traces," Dept. Comput. Sci.. Boston Univ., Boston, MA, Tech. Rep. BU-CS-95-010, 1995. 

[7] S. Deng, "Empirical model of WWV document arivals at access links." 
in *Proc. 1996 IEEE ht. Con& Conunun.,* **June 1996.** 
[S] A. Ermmiili, 0. Narayan, and IV. Willinger. 'Experimental queueing analysis with long-range dependent packet *traffic," IEEELACM Trans.* Ne&orking, **vol. 4, no. 2. pp. 209-2!?3. Apr. 1996.** 
[9] R A. Floyd. 'Short-term tile reference patterns in a UNIX environment,' 
Dept. Comput. Sci.. Univ. Rochester,Rochester, NY, Tech. Rep. 177, 1986. 

[lo] Mosaic software, National Center for Supercomputing Applications, Univ. Illinois Urbma-Cbampaigu. 

[ll] S. Glassman, 'A caching relay for the world wide web," in Proc. 1st hr. 

Conf: World-mde Web, CERN, Geneva, Switzerland, Elsevier Science, May 1994. 

[12] B. M. Hill, "A simple general approach to inference about the tail of a distribution," *Ann Srurist.. vol. 3.* pp. 1163-l 174. 1975. 

[13] W. E. Leland and D. V. Wilson. "High time-resolution measurement and analysis of LAN traflic: Implications for LAN interconnection," in Proc. IEEE NFOCOM'91. **Bal Harbour, FL, 1991. pp. 1360-1366.** 
[14] W. E. Lcland. M. S. Taqqu. W. Wtllinger, and D. V. Wilson. "On the self-simitar nature of Ethernet traffic" (extended version). IEEE/ACM 
Truns. Nenvorking, **vol. 2. no. 1, pp. 1%. 1994. .-** 
1151 _ _ B. B. Mandelbmt, "'Long-tun lincatitv. locallv Gaussian urocesses. H-spectra and infinite va&nces," Int. &on. *Rx, vol. 16.* pp. 82-113, 1969. 

Ml *-, The Frucful Geometry ofNurure. San* **Francisco, CA: Freeman,** 
1983. 

1171 J. K. Ousterhout, H. Da Costa, D. Harrison, J. A. Kunze. M. Kupfer, and J. G. Thompson, "A trace-driven analysis of the UNIK 4.2 BSD file system," in *Proc. 10th ACM Symp. Oper. Syst. PrincipIes, Orcas* **Island.** 
WA, Dec. 1985, pp. 15-24. 

[18] K. Park, G. T. Kim, and M. E. Cmvella. "On the relationship between file sizes. transport protocols. and self-similar network traffic." in *Proc.* 
4th ht. Cant *fier&rk Protocols (ICNP'96). Oct. 1996.* pp. i71-180. 

Cl91 _ _ **V. Paxson. 'Emairicallv-derived an&tic models of wide-area TCP** 
connections." *IE&LACh Trans. Nefivoiking,* vol. 2. pp. 316-336, Aug. 

1994. 

[2O] V. Paxson and S. Floyd, "Wide-area traffic: The failure of Poisson modeling," *IEEELACM Trans. fiehvorkng,* vol. -3. pp. 226-244, June 1995. 

{2I] I. E. Pitkow and M. M. Reeker, "A simple yet robust caching algorithm based on dynamic access patterns," in Efecfron. Pruc. 2nd WWW Co@, 
1994. 

mrllel computers and nclworks. 

--- -- _.*- ----.. 1 .-_ ---.. r.~, cct which has produced over 20 rerformance measurement, annlysis, and redesign of the World [24] M. Satyanarayanan, "A study of file sizes and functional lifetimes," in Proc. 8th ACM Symp. Oper. Sysr. Princ$tes, Dec. 1981. papers on the i rs.r, 1 n.>-~ ~~ LI.II..--- ..I .~.I1 ~._~~ IL., .-.. . - ~~. . . -.-P *'tlide* Web and 1~21 J. aeaayao, ~- -1v10sanz w*n ml my n~wor~t -+ruoymg neovor~ oamc oatterns of Mosaic use," *in Eiectnm. Proc. 2nd World Wide Web* related issues in wide area networking. 

Dr. Croveha is a **member** of ACM. 

'conJI'94: Mosaic and the Web, Chicago, IL, Oct. 1994. 

1261 A. J. Smith, "Analysis of long term file reference oatterns for aoolication to file migration aigori~hms,"JEEE Trans. *sofnvk? Eng., voLLk-7,* pp. 

403-410. JuIy 1981. 

[27] M. S. Taqqu, V. Tevemvsky, and W. Willinger, "Estimators for Iongrange dependence: Au empirical study," *Frucials. vol. 3,* no. 4, pp. 

785-798, 1995. 

[2X] M. S. Taqqu and J. B. Levy. 'Using renewal processes to generate longrange dependence and high variability," in *Dependence in Prubabiiity* and Sfaristics, E. Eberlein and M. S. Taqqu, Eds. Birkhauser, 1986, pp. 73-90, 1986. 

[29] W. WiIIinger, M. S. Taqqu, W. E. Leland, and D. V. Wilson, "Selfsimilarity in high-speed packet &a&: Analysis and modeling of Ethernet traffic measurements," *Statist. Sci.,* vol. IO, no. 1, pp. 67-85. 

199s. 

Mark E. Crovella (M'95) received the T&S, dcgree fmm Cornell University, Ithaca, NY, the MS, 
degree fmm SUNY Buffalo, and the PhD, degree From the University of Rochester, Rochcstcr, NY, 
in 1994. 

From 1984 IO 1994 he was a Senior Camputcr 
[22] K. K. Ramakrishnan, P. Biswas. and R. Karedia. "Analysis of file 

![11_image_0.png](11_image_0.png)

I/O traces in commercial computing environments," in Proc. SfGME'F- f "3i RICS'92, June 1992, pp. 78-90. A! 

[23] WWW-stat 1.0 software, Regents of the University of California, available from Dept. Inform. Comput. Sci., Univ. California, Irvine, 1 ..---.- ..- r- ___.. 

CA 92697:3425. and evaluation of pr He is a c&u&r nf the flwnns rewnn-h nrnit Scientist at Calspan Corporation. Since 1994 he hns been Assistant Professor in the Computer ScIencc Department at Boston University. His research In-
Azer Beshvros (M'87) received the **SM.** nnd Ph.D. 

![11_image_1.png](11_image_1.png) degrees from Harvard University. Cambridge, MA, 
He is a Computer Science faculty member at Boston University, where he conducts research on real-time computation and communication systems and on large-scale networked information systems, He has authored in excess of 60 refereed publicnlions. 

[30] W. WiIlinger, M. S. Taqqu, R. Sherman, and D. V. Wilson, "Self- Dr. Bestavms is a member of ACM, He Is cursimilarity through high-variability: Statistica analysis of Ethernet LAN 
traffic at the source IeveI," IEEElACM Trans. *Nehvorking,* vol. 5, pp. 

rentIy tbe Editor-in-Chief of the Newsletter of ~lrc 
' 
71-86, Feb. 1997. 

IEEE-CS TC on Real-lime Systems and the PC 
Chair of the IEEE Real-Time Technology and Applications Symposium. 