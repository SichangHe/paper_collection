# On The Self-Similar Nature Of Ethernet Traffic (Extended Version)

Will E. Leland, Member, *IEEE,* Murad S. Taqqu, Member, *IEEE,* Walter Willinger, and Daniel V. Wilson, Member, *IEEE*
Abstrac(-We demonstrate that Ethernet LAN traffic is **statistically** *se~-simi/ar,* that none of the commonly used traffic **models**
is able to capture **this** *fra([al-like* behavior, that such **behavior**
has serious implications for the design, control, and analysis of high-speed, cell-based networks, and that aggregating **streams** of such traffic typically intensifies the self-similarity **("burstiness")**
instead of smoothing it. Our conclusions are **supported** by a rigorous statistical analysis of hundreds of millions of high **quality**
Ethernet traffic measurements colleeted between 1999 and **1992,**
coupled with a discussion of tbe underlying mathematical and statistical properties of self-similarity and their relationship **with**
actual network behavior. We also present traffic models **based**
on self-similar stochastic processes that provide simple, **accurate,**
and realistic descriptions of traffic scenarios expected during B-ISDN **deployment.**

## 1. **Introduction**

I
N THIS PAPER 1. we use the LAN traffic data collected by Leland and Wilson [ 14] who were able to record hundreds of millions of Ethernet packets without loss (irrespective of the traffic load) and with recorded time-stamps accurate to within 100 ps, The data were collected between August 1989 and February 1992 on several Ethernet LAN's at the Bellcore Morristown Research and Engineering Center. Leland and Wilson [ 14] present a preliminary statistical analysis of this unique high-quality data and comment in detail on the presence of 'Sburstiness" across an extremely wide range of time scales: traffic "spikes" ride on longer-term "ripples," that in turn ride on still longer term "swells," etc. This *self-similar* or fractal-like behavior of aggregate Ethernet LAN traffic is very different both from conventional telephone traffic and from currently considered formal models for packet traffic (e.g.,
pure Poisson or Poisson-related models such as Poisson-batch or Markov-Modulated Poisson processes (see [11]), packettrain models (see [13]), fluid flow models (see [1]), etc. and requires a new look at modeling traffic and performance of broadband networks.

The main objective of this paper is to establish in a statistically rigorous manner the *self-similarity* characteristic of the very high quality, high time-resolution Ethernet LAN

Manuscript received July 1, 1993; revised January 15, 1994; approved by IEEE/ACM TRANSACTIONS(m **NETWORKING**Editor Jonathan Smith. This work was supported in part by Boston University, under ONR Grant NOOO14-90-J1287, W. E. t-eland, W. Willinger, and D. V. Wilson am with Bellco~, Morristown, NJ 07962-1910 (email: wel@%ellcote, corn, waltet@ellcore, corn, dv wttjlbellcom.to m),.

M. S. Taqqu is with the Dept.of Mathematics, Boston University, Boston, MA 02215-2411 (email: murad@bu-ma.bu.edu).

IEEE Log Number 9300098.

'An abbreviated version of this paper appeared in [15].
traffic measurements presented in [ 14]. Moreover, we illustrate some of the most striking differences between self-similar models and the standard models for packet traffic currently considered in the literature. For example, our analysis of the Ethernet data shows that the generally accepted argument for the "Poisson-like" nature of aggregate traffic, namely, that aggregate traffic becomes smoother (less bursty) as the number of traffic sources increases, has very little to do with reality. In fact, using the degree of self-similarity (which typically depends on the utilization level of the Ethernet and can be defined via the Hurst *parameter)* as a measure of "burstiness,"
we show that the burstiness of LAN traffic typically intensifies as the number of active traffic sources increases, contrary to commonly held views.

The term "self-similar" was coined by Mandelbrot. He and his co-workers (e.g., see [21 ]–[23]) brought self-similar processes to the attention of statisticians, mainly through applications in such areas as hydrology and geophysics. For further applications and references on the probability theory of self-similar processes, see the extensive bibliography in
[27]. For an early application of the self-similarity concept to communications systems, see the seminal paper by Mandelbrot
[18].

The paper is organized as follows. In Section 11,we describe the available Ethernet traffic measurements and comment on the changes of the Ethernet population, applications, and environment during the measurement period from August 1989 to February 1992. In Section III, we give the mathematical definition of self-similarity, identify classes of stochastic models which are capable of accurately describing the self-similar behavior of the traffic measurements at hand, and illustrate statistical methods for analyzing self-similar data sets. Section IV describes our statistical analysis of the Ethernet data, with emphasis on testing for self-similarity. Finally, in Section V we discuss the significance of self-similarity for traffic engineering, and for operation, design, and control of B-ISDN
environments.

## 11. Traffic Measurements 2.1, The Trafic Monitor

The monitoring system used to collect the data for the present study was custom-built by one of the authors (Wilson) in 1987/88 and has been in use to the present day with one upgrade. For each packet seen on the Ethernet under study, the monitor records a timestamp (accurate to within 100p-to within 20 /Ls in the updated version of the monitor), the packet

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | TABLE   | I   |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|-----|
| QUASJTATSVEDESCRIPTIONOF SETS OF ETHERNEXTRAFFIC MEASUREMENTSUSED rN THE ANALYSISIN SECITONIV Traces of Ethe Measurement Period ToM (27.45 h) AUGUST 1989 Low Hour Start of Trace: (6:25 anr-7:25 am) Aug. 29, 11:25 am Normal Hour End of Trace: (2:25 pm-3:25 pm) Aug. 30, 3:10 pm Bmy Hour 4:25 pm-5:25 pm) Told (20,86 h) OCTOBER 1989 Low Hour Start of Trace: (2:00 am-3:tM am) Get. 5, 11:(NIam Normal Hour End of Trace: (5:00 pm-6:00 pm) Get. 6, 7:51 pm Busy Hour (1 I:oo am-12:ou am) Total (40.16 h) JANUARY 1990 Low Hour Start of Trace: (Jan. 11, 8:32 pm-9:32 pm) JWI.10, 6:07 am Normal Hour End of Trace: (Jan. 10,9:32 arn-10:32 am) Jan. 11, 1017 pm Busy Hour (1032 am-l I :32 am) Totat (47.91 h) FEBRUARY 1992 Low Hour Start of Trace: (Feb. 20, 1:21 arn-2:21 am) Feb. 18, 5:22 am Normal Hour End of Trace: (Feb. 18, 8:21 pm-9:21 pm) Feb. 20, 5:16 ~ Busy Hour (Feb. 18, 11:21 am-12:21 am. ;t Traffic Measurements Total Number Total Number Ethernet Data Set of Bytes of Packets Utilization 11448753134 27901984 9.3'?4 AUG89.LB 224315439 AUG89.LP 652909 5.0'% AUG89.MB 3S0889404 AUG89.MP 968631 8.5% AUG89.HB 677715381 AUG89.HP 1404444 15.l% 14774694236 27915376 15.7% OCT89.LB 468355006 0CT89.LP 978911 10.4% ocT89.h4B 827287174 0CT89.MP 1359656 18.4% OCT89.HB 1382483551 0CT89.HP 2141245 30.7% 7122417589 27954961 3.9% JAN90.LB 87299639 JAN90.LP 310038 1.9'% JAN90.MB 182636845 JAN90.MP 643451 4.l% JAN90.HB 711529370 JAN90.HP 1391718 15.8% 6585355731 27674814 3.1%1 FEB92.LB 56811435 FEB92.LP 231823 1.3% FEB92.MB 154626159 FEB92.MP 524458 3.4% FEB92.HB 225066741 FEB92.HP 947662 5.0'% |         |     |

The network environment at the Bellcore Morns Research

and Engineering Center (MRE) where the traffic measurements

used for the analysis presented later were collected is probably

typical of a research or software development environment

where workstations are the primary machines on people's desks. It is also typical in that much of the original installation

was well thought out and planned but then grew haphazardly. For the purposes of this study, this haphazard growth is not necessarily a liability, as we are able to study the traffic on a

network that is evolving over time. Table I gives a summary description of the traffic data analyzed later in the paper. We consider four sets of traffic measurements, each representing between 20 and 40 consecutive hours of Ethernet traffic and each consisting of tens of millions of Ethernet packets. The data were collected on different intracompany LAN networks at different times over the course of approximately four years

(August 1989, October 1989, January 1990, and February

1992).

2.2.1. Workgroup Network Traflc *Data:* Four data sets will

be considered in this paper. A summary description of these

;t Traffic Measurements

Total Number Total Number Ethernet

Data Set of Bytes of Packets Utilization

11448753134 27901984 9.3'?4

AUG89.LB 224315439

AUG89.LP 652909 5.0'%

AUG89.MB 3S0889404

AUG89.MP 968631 **8.5%**

AUG89.HB 677715381

AUG89.HP 1404444 15.l%

14774694236 27915376 15.7%

OCT89.LB 468355006

0CT89.LP 978911 10.4%

ocT89.h4B 827287174

0CT89.MP 1359656 18.4%

OCT89.HB 1382483551

0CT89.HP 2141245 30.7%

7122417589 27954961 3.9%

JAN90.LB 87299639

JAN90.LP 310038 1.9'%

JAN90.MB 182636845

JAN90.MP 643451 4.l%

JAN90.HB 711529370

JAN90.HP 1391718 15.8%

6585355731 27674814 3.1%1

FEB92.LB 56811435

FEB92.LP 231823 1.3%

FEB92.MB 154626159

FEB92.MP 524458 3.4%

FEB92.HB 225066741

FEB92.HP 947662 **5.0'%**

length, the status of the Ethernet interface and the first 60 bytes of data in each packet (header information). As we will show in Section IV, the high-accuracy timestamps of the Ethernet packets produced by this monitor are crucial for our statistical analyses of the data. A detailed discussion of the capabilities of the original monitoring system, including extensive testing of its capacity and accuracy can be found in [14].

## 2.2. The Network Environment At Bellcore

data sets is given in Table I. The first two sets of traffic measurements, taken in August and October of 1989 (see first two rows in Table I), were from an Ethernet network serving a laboratory of researchers engaged in everything from software development to prototyping new services for the telephone system. The traffic was mostly from services that used the Internet Protocol (1P) suite for such capabilities as remote Iogin or electronic mail, and the Network File System (NFS)
protocol for file service from servers to workstations. There were some unique services, though; for example, the audio of a local radio station was p-law encoded and distributed over the network during portions of the day. While it is not our intent to provide here a detailed description of the particular MRE network segments under study, some words about the types of traffic on them are appropriate.

A snapshot of the network configuration at the time of collection of the earliest data set being used (August 1989)
is given in Fig. 1: there were about 140 hosts and routers comected to this intra-laboratory network at that time, of which 121 spoke up during the 27 h monitoring period. This network consisted of two cable segments connected by a bridge, implying that not all the traffic on the network as a whole was visible from our monitoring point. During the period this data was collected, among the 25 most active hosts were two DEC 3100 fileservers, one Sun-4 fileserver, six Sun3 fileservers, two VAX 8650 minicomputers, and one CCI
Power 6 minicomputer. At that time, the less active hosts were mainly diskless Sun-3 machines and a smattering of Sun-4 's, DEC 3 100's, personal computers, and printers.

![2_image_0.png](2_image_0.png)

Fig. 1, Network from which the August 1989 and October 1989 measurements were taken.
During the latter part of 1989 when the first two data sets were collected, a revolution was taking place on this network.

The older Sun-3 class workstations were rapidly replaced with RISC-based workstations such as the SPARC station-1 and DEC **3100.** Many of the new workstations were "dataless"
(where the operating system is stored on a local disk but user data on a server) instead of "diskless" (where all tiles for the user and for the operating system are stored on a remote server). Because of the increased computing power of the machines connected to this segment, the network load increased appreciably, in spite of the trend towards dataless workstations. Note, for example, that the "busy hour" from the October 1989 data set is indeed busy: 30. 7y0 utilization as compared to 15. l?lo during the August 1989 busy hour; similar increases can also be observed for the low and normal hours. Not long after this data was taken, this logical Ethernet segment was again segmented by adding yet a third cable and a bridge, and moving some user workstations and their fileserver to that new cable. The above network has always been isolated from the rest of the Bellcore world by one or more routers. The other sides of these routers were connected to a large corporate intemet consisting at that time of many Ethernet segments and T-1 point-to-point links connected together with bridges. Less than 5% of the total traffic cm this workgroup network during either of the traces went out to either the rest of Bellcore or outside of the company.

?.2,2. W[>rkgr(>upand External *Trafl(:* The third data set, taken in January 1990 (row 3 in Table I), came from an Ethernet cable that linked the two wings of the MRE facility that were occupied by a second laboratory (see Fig. 2). At the time this data set was collected, this second laboratory comprised about 160 people, engaged in work similar to the first laboratory. This particular segment was unique in that it was also the segment serving Bellcore's link to the outside Internet world. Thus the traffic on this cable was from several sources: (i) two very active file servers directly connected to the segment; (ii) traffic (file service and remote Iogin) between the two wings of this laboratory; (iii) traffic between the laboratory and the rest of Bellcore; and (iv) traffic between Bellcore as a whole and the larger Internet world. This last type of traffic we term *exfermd* traffic, and in 1990 could come from conversations between machines in any part of Bellcore and the outside world. This Ethernet segment was specifically monitored to capture this external traffic. In Section IV, we

![2_image_1.png](2_image_1.png)

Network for second laboratory from which the Jarruary 1990 measurements were taken.
Fig. 2.

![2_image_2.png](2_image_2.png)

Fig. 3. Backbone network for MRE facility from which the Febrmry 1990 measurements were taken.
will be considering the aggregate and external traffic from this data set separately. This segment was separated from both the Bellcore intemet and the two wings of the laboratory by bridges, and from the outside world by a vendor-controlled router programmed to pass anything with a Bellcore address as source or destination. In contrast to the two earlier data sets, over 1200 hosts spoke up during the 40 h monitoring period on this segment.

The last data set, from February 1992 (see row 4 in Table I), was taken from the building-wide Ethernet backbone in MRE after security measures mandated by the "Morris worm"
(described in detail in [26]) had been put into place (see Fig.

3). This cable carried all traffic going between laboratories within MRE, traffic from other Bellcore buildings destined for MRE, and all traffic destined for locations outside of Bellcore.

![3_image_0.png](3_image_0.png)

h-m an appropriately chosen compound Poisson model on the same five different time scales (a')-(e').
Some hosts were still directly connected to this companywide network in early 1992, but the trend to move them from the Bellcore intemet to workgroup cables comected to the Bellcore intemet via routers continues to the present. Because this cable had very little host to file server traffic, the overall traffic levels were much lower than for the other three sets. On the other hand, the percentage of remote login and mail traffic was higher. This cable also carried the digitized radio traffic between the two laboratories under discussion. The most radical difference bet ween this data set and the others is that the traffic is primarily router to router rather than host to host.

In fact, about 600 hosts spoke up during the measurement period (down from about 1200 active hosts during the January
'90 measurement period), and the five most active hosts were routers.

## Iii. Self-Simflarstochastic **Processes** 3.1. A Picture Is Worth A Thousand Words

For 27 consecutive hours of monitored Ethernet traffic from the August 1989 measurements (first row in Table I), Fig.

4 (a)-(e) depicts a sequence of simple plots of the packet counts (i.e., number of packets per time unit) for five different choices of time units. Starting with a time unit of 100 s (Fig.

4(a)), each subsequent plot is obtained from the previous one by increasing the time resolution by a factor of 10 and by concentrating on a randomly chosen subinterval (indicated by a darker shade).

The time unit corresponding to the finest time scale (e) is 10 ms. In order to avoid the visually irritating quantization effect associated with the finest resolution level, plot (e)
depicts a "jittered" version of the number of packets per 10 ms, i.e., a small amount of noise has been added to the actual arrival rate. Observe that with the possible exception of plot (a) which suggests the presence of a daily cycle, all plots are intuitively very "similar" to one another (in a dkributional sense), that is, Ethernet traffic seems to look the same in the large (rein, h) as in the small (s, ins). In particular, notice the absence of a natural length of a "burst:"
at every time scale ranging from milliseconds to minutes and hours, bursts consist of bursty subperiods separated by less bursty subperiods. This scale-invariant or "self-similar" feature of Ethernet traffic is drastically different from both conventional telephone traffic and from stochastic models for packet traffic currently considered in the literature. The latter typically produce plots of packet counts which are indistinguishable from white noise after aggregating over a few hundred milliseconds, as illustrated in Fig. 4 with the sequence of plots (a')–(e'); this sequence was obtained in the same way as the sequence (a)–(e), except that it depicts synthetic traffic generated from a comparable (in terms of average packet size and arrival rate) compound Poisson process. (Note that while the choice of a compound Poisson process is admittedly not very sophisticated, even more complicated Markovian arrival processes would produce plots indistinguishable from Fig. 4(a')–(e'). ) Fig. 4 provides a surprisingly simple method for distinguishing clearly between our measured data and traffic generated by currently used models and strongly suggests the use of self-similar stochastic processes for traffic modeling purposes. Below. we give a brief description of the concept of self-similar processes, discuss their most important mathematical and statistical properties, mention some modeling approaches, and outline statistical methods for analyzing self-similar data. For a more detailed presentation andreferences, see 117], [4], or [2].

## 3..?. Definitions And Propertic,~

Let .Y = (.Yt : / = ('l.1. 2....) be a *f{~t'uriar2ce.Yrarionary* stochastic process with mean I(, variance rJ2 and autocorrelation function r(k). k > 0. In particular, we assume that X has an autocorrelation function of the foml

$r(k)\sim k^{-1}L(t)$, as $k\sim\infty$.  
where () < ~i < I and 1. is slowly varying at infinity, i.e.,
liltlt-+w L(l.r)/ l,(t) = 1, for all .r > (). (For our discussion below, we assume for simplicity that L is asym totically constant. ) For each ))t = 1.2.3... .. let .Y['") =r
(x,,~') :/$=
1.'2.3. ..) denote the new covariance stationary time series
(with corresponding autocorrelation function r('n )) obtained by averaging the original series Y over non-overlapping blocks of size ~rl, That is. for each II) = 1.2. :\. . . .. .l-('") is given by ~j,lll ] = l//n(.Yk.,,, --,1,+] + . . + .Y~,,,).k > 1. The process .Y is called (e.u/[t/y) second-order *self-similar* with self-similarity parameter 11 = 1 - ~J/2 if for all m = 1, 2 . . . ..

var(.~~'"~) = ~zr,,-'i and

$$r^{(m)}(k)=r(k),k\geq0.$$

'r~'''~(k)= r(k), k > (). (2)
.\- is called (u.symptoticallyj se(wtd-order *self-similar* with selt-similarity parameter }1 = 1– ~~/2 if for ail k large enough,
,"'J'(A"') - r(k). as ?t] - x (3)
with r(k) given by ( I ). In other words. .Y is exactly or asymptotically second-order self-similar if the corresponding aggregated processe~ .1-I1,1J are the same as X or become indistinguishable from .Y—at least with respect to their autocorrelation functions.

Mathematically. self-similarity manifests itself in a number of equivalent ways: (i) the variance of the sample mean decreases more slowly than the reciprocal of the sample size
(slowly dccqvin,g *l,ariances),* i.e.. var( .Y('")) N a2?n-i?, as rt}+ x, with () < ;) < I (here and below, a,z. as, . . .

denote finite positive constants): (ii) the autocorrelations decay hyperbolically rather than exponentially fast. implying a nonsummable autocorrelation function ~k. r(k) = K (long-range *depende~r[e).* i.e., r(k) satisfies relation ( 1); and (iii)
the spectral density ~(.) obeys a power-law near the origin
(1/~–rroise), i.e., ~(~) - *a3A-7,* as A ~ O, with O < ~ <1 and~=l–~.

Intuitively, the most striking feature of (exactly or asymptotically) second-order self-similar processes is that their aggregated processes X(m) possess a nondegenerate correlation structure, as m ~ w. This intuition is best illustrated with the sequence of plots in Fig. 4: if X **represents** the number of Ethernet packets per 10 ms (plot (e)), then plots (d)-(a) depict segments of the time series *rrLX(m* ), m = 10, 100, 1000.10000"
(i.e., number of Ethernet packets per 0.1, 1, 10, 100 s),
respectively. Note that all plots look "similar" and distinctively different from pure noise. The existence of a nondegenerate correlation structure for the processes X(m), as m + ,x, is in stark contrast to typical packet traffic models currently considered in the literature, all of which have the property that their aggregated processes X ('n) tend to second-order pure noise, i.e., for all k > 1,

$$r^{(m)}(k)\to0,\mathrm{~as~}m\to\infty.$$
$$(4)$$
$$(\mathbb{I})$$

Equivalently, packet traffic models currently considered in the literature can be characterized by (i) a variance of the sample mean that decreases like the reciprocal of the sample mean, i.e., Va(x("l) )- *rQTn* –1, as 77L + x, (ii) an autocorrelation function that decreases exponentially fast (i.e.,
T-(k) - pk. O < p < 1), implying a summable autocorrelation function ~k r(k) < cc (short-range *dependence),* or (iii) a spectral density that is bounded at the origin.

Historically, the importance of self-similar processes lies in the fact that they provide an elegant explanation and interpretation of an empirical law that is commonly referred to the Hurst *effect.* Briefly, for a given set of observations (Xk :
k = 1.2, . . . . n) with sample mean **~(rt)** and sample variance S2(7L), the resealed adjusted range *statistic* (or RIS *statistic)* is given by R(n)/S(n) = l/S(n)[ max(O, W'l, W2, . . . . Wn) –
min (O, Wl$WZ, . . . . *W.)],* with wk = (Xl + X2 + . . +
Xk ) - k~(n)(,k ~ 1). While many naturally Occurnng time series appear to be well represented by the relation E[z?(7/)/s(7L)] ~ **rzsn~.** as n --+ x, with Hurst *parameter* H "typically" about ().7, observations xk from a shortrange $~pendent model are known to satisfy **~[l?(7L)** /S(71)]
- (l(j?) , as 71-+ X. This discrepancy is generally referred to as the Hurst *effect,*

$$(2)$$
$$\mathbf{\partial}\times\mathbf{\partial}$$
$\downarrow$ ? 

## 3.3. Modeling Of Self-Similar Phenomena

Since in practice we are always dealing with finite data sets, it is in principle not possible to decide whether the above asymptotic relationships (e.g., ( I)-(4)) hold or not.

For processes that are not self-similar in the sense that their aggregated series converge to second-order pure noise (see
(4)), the correlations will eventually decrease exponentially, continuity of the spectral density function at the origin will eventually show up, the variances of the aggregated processes will eventually decrease as *m-1,* and the resealed adjusted range will eventually increase as no's. For finite sample sizes, distinguishing between these asymptotic and the ones corresponding to self-similar processes is, in general, problematic. In the present context of Ethernet measurements, we typically deal with time series with hundreds of thousands of observations and are therefore able to employ statistical and data analytic techniques that are impractical for small data sets. Moreover, with such sample sizes, parsimonious modeling becomes a necessity due to the large number of parameters needed when trying to fit a conventional process to a "truly" self-similar model. Modeling, for example, longrange dependence with the help of short-range dependent processes is equivalent to approximating a hyperbolically decaying autocomelation function by a sum of exponential.

Although always possible, the number of parameters needed will tend to infinity as the sample size increases, and giving physically meaningful interpretations for the parameters becomes more and more difficult. In contrast, the long-range dependence component of the process can be modeled (by a self-similar process) with only one parameter. Moreover, from a modeling perspective, it would be very unsatisfactory to use for a single empirical time series two different models, one for a short sequence, another one for a long sequence.

Two formal mathematical models that yield elegant representations of the self-similarity phenomenon but do not provide any physical explanation of self-similarity are fracfbud Gaussian *noise* and the class of fractional autoregressive integrated moving-average (ARIMA) processes. Fractional Gaussian noise X = (X~ : k 2 O) with parameter H G (O, 1)
has been introduced in [22] and is a stationary Gaussian process with mean p, variance Oz, and autocorrdation function r-(k) = l/2(lk + 112* - IIc12H+ Ik - 112H), k > 0. Simple calculations show that fractional Gaussian noise is exactly second-order self-similar with self-similarity parameter If, as long as 1/2 < If < 1. Methods for estimating the three unknown parameters IL,u*, and H are known and will be addressed below. Fractional ARIMA(p, d, q) processes are a natural generalization of the widely used class of Box–Jenkins models [3] by allowing the parameter d to take non-integer values. They wem introduced by Granger and Joyeux [10]
and Hosking [12] who showed that fractional ARIMA(P, d, q)
processes are asymptotically second-order self-similar with self-similarity parameter d + 1/2, as long as O < d < 1/2.

Fractional ARIMA processes are much more flexible with regard to the simultaneous modeling of the short-term and long-term behavior of a time series than fractional Gaussian noise, mainly because the latter, having only the three parameter u, az, and H, has a very rigid correlation structure and is not capable of capturing the wide range of low-lag correlation structures encountered in practice. This flexibility can already be observed when considering the simplest processes of the fractional ARIMA(P, d, q) family, namely the two-parameter models ARIMA(l, d, O) and ARIMA(O, d, 1).

Finally, we briefly mention a construction of self-similti processes (due to Mandelbrot [19] and later extended by Taqqu and Levy [28]), based on aggregating many simple renewal reward processes exhibiting inter-renewal times with infinite variances. Although the construction was originally cast in an economic framework involving commodhy prices, it is particularly appealing in the context of high-speed packet traffic, and we will return to this construction in Section V when attempting to provide a "phenomenological" explanation for the observed self-similar nature of aggregate Ethernet traffic.

In its simplest form, this construction requires a sequence of i.i.d. integer valued random variables UO, UI, U2, . . . ("inter renewal times") with "heavy tails," i.e., with the property

$$P[U\geq u]\sim u^{-\alpha}h(u),\ \mathrm{as}u\rightarrow\infty,$$
$\left(\mathfrak{S}\right)_{\mathbb{R}}$
where h is slowly varying at infinity and O < a < 2.

For example, the stable (Pareto) distribution with parameter 1< a <2 satisfies the "heavy-tail" property (5). Furthermore, let WO, WI, Wz, . . . be an i.i.d. sequence ("rewards") with mean zero and finite variance, independent of the b"s. Next, let Sk = SO + **~$=1** Uj, k 2 0 denote the delayed renewal sequence derived from (Uj *)j20* where SO is chosen such that the sequence (Sk *)k20* is stationary. The renewal reward process W = (W(t) : t = *0,1,2,..* .) is then defined by W(t) = ~~=o wk~(.s,.,,s,l(t), with *1A(")* denoting the indicator function of the set A. By aggregating Zt4 i.i.d.

copies W(l), W(2), . . . . *Wfkf)* of W, we obtain the model of interest, namely the process W* given by W* (T, M) =
ZF=l Zti=l w(m)(~) with *W"(O,* M) = O. In [19] and [28]
it is shown that for T and M both large with T << M,
W* behaves like fractional *Brownian* motion; in other words, properly normalized, *W'(T,* M) converges to the integrated version of fractional Gaussian noise, i.e., to a mean-zero Gaussian process BH = *(B~(s)* : s ~ O), 1/2 < H <1, with correlation function R(s, t) = l/2(s2H + t2H– Is– t12H).For more details concerning fractional Brownian motion, see [22]
and [21 ]. As an immediate consequence of Taqqu and Levy's result, we have that for T and M both large with T << M,
the increment process of W* behaves like fractional Gaussian noise.

## 3.4. Inference For Self-Similar Processes

Since slowly decaying variances, long-range dependence, and a spectral density obeying a power-law are different manifestations of one and the same property of the underlying covariance stationary process X, namely that X is asymptotically or exactly second-order self-similar, we can approach the problem of testing for and estimating the degree of selfsimilarity from three different angles: (1) time-domain analysis based on the MS-statistic, (2) analysis of the variances of the aggregated processes X(m), and (3) periodogram-based analysis in the frequency-domain. The following gives a brief description of the corresponding statistical and graphical tools.

For an engineering-based graphical tool that is related to the variance property of the aggregated processes, see Section 5.2.

The objective of the R/S analysis of an empirical record is to infer the degree of self-simihwit y H (Hurst parameter+via the Hurst effect-for the self-similar process that presumably generated the record under consideration. Graphical R/S
analysis consists of taking logarithmically spaced values of n (starting with n x 10), and plotting log(R(n)/S(n))
versus log(n) results in the resealed adjusted range *plot* (also called the pox diagram of *R/S).* When l-l is well defined, a typical resealed adjusted range plot starts with a transient zone representing the nature of short-range dependence in the sample, but eventually settles down and fluctuates in a straight "street" of a certain slope. Graphical R/S analysis is used to determine whether such asymptotic behavior appears supported by the data. In the affirmative, an estimate fi of H is given by the street's asymptotic slope which can take any value between 1/2 and 1. For practical purposes, the most useful and attractive feature of the R/S analysis is its relative robustness against changes of the marginal distribution. This feature allows for practical] y separate investigations of the self-similarity property of a given data set and of its distributional characteristics.

We have observed that for second-order self-similar processes, the variances of the aggregated processes X("'). m >—
1. decrease linearly (for large m) in log-log plots against m with slopes arbitrarily flatter than —1. The so-called tlariancefirne *plots* are obtained by plotting log(var( X(m))) against log( 7n) **(''time")** and by fitting a simple least squares line through the resulting points in the plane, ignoring the small values for m. Values of the estimate ~ of the asymptotic slope between - 1 and O suggest self-similarity, and an estimate for the degree of setf-simik-wity is given by A = 1 - ~/2.

The absence of any limit law results for the statistics corresponding to the R/S analysis or the variance-time plot makes them inadequate for a more refined data analysis
(e.g.. confidence intervals for H). In contrast, a more refined data analysis is possible for maximum likelihood-type estimates (MLE) and related methods based on the per-i0dOgrUf7? I(r) = (2'T?L)-1 \ ~J=~ *Xjt'i;J12,* () ~ J; < fl Of
.%" = (Xl, .~2, . . . . X,, ) and its distributional properties. In particular, for Gaussian or approximately Gaussian processes, Whittle's approximate MLE has been studied extensively and has been shown to have desirable statistical properties.

Combined, Whittle's approximate MLE approach and the aggregation method discussed earlier give rise to an operational procedure for obtaining confidence intervals for the self-similarity parameter H. Briefly, for a given time series, consider the corresponding aggregated processes X(m) with
/r/ = 100,"'200. 300, . . .. For each of the aggregated series, estimate the self-similarity parameter H(m) via Whittle's method. This procedure results in point estimates fi(n') of H( "iJ and corresponding %5%,-confidence intervals of the form
~(lrl) + l,gfj~ ~, ,,,~, where ti~(,,, , is given by a known central limit theorem result (for references, see [17 ]). Plots of fi(m' )
(together with their 95%-confidence intervals) versus 711 **will** typically vary for small aggregation levels, but will stabilize after a while and fluctuate around a constant value, our final estimate of the self-similarity parameter }{.

## Iv. Ethernet Traffic 1S Self-Similar

While Fig. 4 gives a pictorial "proof' of the self-similar nature of the traffic measurements described in Section II,
using the statistical and graphical tools presented above, we establish in this section the self-similar nature of Ethernet traffic (and some of its major components, such as external traffic or external TCP traffic) in a statistically more rigorous manner. For each of the four measurement periods described in Table I, we identified typical low-, medium-, and high-activity hours. With the resulting data sets, we are able to investigate features of the observed traffic that persist across the network as well as across time, irrespective of the utilization level of the Ethernet. Only one LAN could be monitored at any one time (making it impossible to study correlations in the activity on different LAN's) and all data were collected from LAN's in the same company (making it not representative for all LAN traffic). For a similar analysis that uses different data sets from Table I, see [ 16].

## 4,1. Ethernet Trajjic Over A 27-Hour Period

In order to check for the possible self-similarity of the August 1989 Ethernet traffic data, we apply the graphical tools described in the previous section, namely, variancetime plots, pox plots of R/S, and periodogram plots, to the three subsets AUG89.LB, AUG89.MB, and AUG89.HB of the August '89 trace that correspond to a typical "low hour," "normal hour," and "busy hour" traffic scenario, respectively
(see Table I). Each sequence contains 360000 observations, and each observation represents the number of bytes sent over the Ethernet per 10 ms. As an illustration of the usefulness of the graphical tools for detecting self-similarity in an empirical record, Fig. 5 depicts the variance-time curve (a), the pox plot of R/S (b), and the periodogram plot (c) corresponding to the sequence AUG89.MB. The variance-time curve, which has been normalized by the corresponding sample variance, shows an asymptotic slope that is distinctly different from
- 1 (dotted line) and is easily estimated to be about - ,40, resulting in an estimate fi of the Hurst parameter H of about fi x .80. Estimating the Hurst parameter directly from the corresponding pox plot of R/S leads to a practically identical estimate; the value of the asymptotic slope of the R/S plot is clearly between 1/2 and 1 (lower and upper dotted line, respectively), with a simple least-squares fit resulting in H x .79. Finally, looking at the periodogram plot, we observe that although there are some pronounced peaks in the high-frequency domain of the periodogram, the low-frequency part is characteristic for a power-law behavior of the spectral density around zero. In fact, by fitting a simple least-squares line using only the lowest 10~ of all frequencies, we obtain a slope estimate ~ x .64 which results in a Hurst parameter estimate P of about .82. Thus, together the three graphical methods suggest that the sequence AUG89.MB is self-similar with self-similarity parameter H x *.80.* Moreover, Fig. 5(d) indicates that the normal hour Ethernet traffic of the August 1989 data is, for practical **purposes,** exactly self-similar: it shows the estimates of the Hurst parameter H for selected aggregated time series derived from the sequence AUG89.MB,
as a function of the aggregation level m. For aggregation levels m = 1,5.10.50, 100,500, 1000, we plot the Hurst parameter estimate fi(m') (based on the pox plots of IUS
("*"), the variance-time curves ("o"), and the periodogram plots ("0")) for the aggregated time series X('") against the logarithm of the aggregation level m. Notice that the estimates are extremely stable and practically constant over the depicted range of aggregation levels 1 s wi. s 1000. Because the range includes small values of m, the sequence AUG89.MB

![7_image_0.png](7_image_0.png)

"'"'"':'''"-
Fig, 5. Graphical methods for checking the self-similarity property of the sequence AUG89.MB.
can be regarded as exactly self-similar. Similar results are obtained for the sequences AUG89.LB and AUG89.HB, and for the corresponding packet count processes AUG89.LP,
AUG89.MP, and AUG89.HP. Together, these observations show that Ethernet traffic over approximately a 24-hour period is self-similar, with the degree of self-similarity increasing as the utilization of the Ethernet increases.

## 4.2. Ethernet Trajj4C Over A Four-Year Period

In order to examine in detail the nature of Ethernet traffic across time as well as across the network under consideration, we now consider the remaining data sets described in Table I.

In contrast to Section 4.1, our analysis below results in estimates of the self-similarity parameter H together with their respective 95%-confidence intervals. As discussed in Section 3.4, such a refined analysis is possible if maximum likelihood type estimates (MLE) or related estimates based on the periodogram are used instead of the mostly heuristic graphical estimation methods illustrated in the previous section. Plots
(a)-(d) of Fig. 6 show the result of the MLE-based estimation method when combined with the method of aggregation. For each of the four sets of traffic measurements described in Table I, we use the time series representing the packet counts during normal traffic conditions (i.e., AUG89.MP in Fig. 6(a),
0CT89.MP in (b), JAN90.MP in (c), and FEB92.MP in (d)), and consider the corresponding aggregated time series X(m)
with m = 100, 200, 300,. ... 1900, 2000 (representing the packet counts per 1,2,..., 19,20 s, respectively). We plot the Hurst parameter estimates llfm) of H(m) obtained from the aggregated series X(m), together with their 95%-confidence intervals, against the aggregation level m. Fig. 6 shows that for the packet counts during normal traffic loads (irrespective of the measurement period), the values of fi(m) are quite stable and fluctuate only slightly in the 0.85 to 0.95 range throughout the aggregation levels considered. The same holds for the 95%-confidence interval bands indicating strong statistical evidence for self-similarity of these four time series with degrees of self-similarity ranging from about 0.85 to about 0.95. The relatively stable behavior of the estimates fi(m) for the different aggregation levels m also confirms our earlier finding that Ethernet traffic during normal traffic hours can be considered to be exactly self-similar rather than asymptotically self-similar. For exactly self-similar time series, determining a single point estimate for H and the corresponding 9570confidence interval is straightforward and can be done by visual inspection of plots such as the ones in Fig. 6 (see below).

Notice that in each of the four plots in Fig. 6, we added two lines corresponding to the Hurst parameter estimates obtained from the pox diagrams of R/S and the variance-time plots, respectively. Typically, these lines fall well within the 95~0confidence interval bands which confirms our earlier argument that for these long time series considered here, graphical estimation methods based on R/S or variance-time plots can be expected to be very accurate.

In addition to the four normal hour packet data time series, we also appliedthe combined MLE/aggregation method to the other traffic data sets described in Table 1. Fig. 7(a)
depicts all Hurst parameter estimates (together with the 95%- confidence interval corresponding to the choice of m discussed earlier) for each of the 12 packet data time series, while Fig. 7(b) summarizes the same information for the time series representing the number of bytes. We also include in these summary plots the Hurst parameter estimates obtained via the variance-time plots ("o") and R/S analysis ("*") in order to indicate the accuracy of these essentially heuristic estimators when compared to the statistically more rigorous Whittle estimator ("o").

Concentrating first on the packet data, i.e., Fig. 7(a),we see that despite the transition from mostly host-to-host workgroup traffic during the August 1989 and October 1989 measurement

![8_image_1.png](8_image_1.png)

Fig. 6. Penodogram-based MLE/aggregation melhod for the sequences AUG89.MP, 0CT89.MP. JAN90,MP, and FEB92,MP.
periods, to a mixture of host-to-host and router-to-router traffic during the January 1990 measurement period, to the predominantly router-to-router traffic of the February 1992 data set, the Hurst parameter corresponding to the typical normal and busy hours, respectively, are comparable, with slightly higher H-values for the busy hours than for the normal traffic hours, This latter observation might be surprising in light of conventional traffic modeling where it is commonly assumed that as the number of sources (Ethernet users) increases, the resulting aggregate traffic becomes smoother and smoother. In contrast to this generally accepted argument for the "Poissonlike" nature of aggregate traffic, our analysis of the Ethernet data shows that, in fact, the aggregate traffic tends to become less smooth (or, more bursty ) as the number of active sources increases (see also our discussion in Section 5.1 ). While

![8_image_0.png](8_image_0.png)

Fig. 7. Summary plot of Hursl parameter estimates for all da)a sets in Table I.
there were about 120 hosts that spoke up during the August 1989 or October 1989 busy hour, we heard from an order of magnitude more hosts (about 1200) during the January 1990 high traffic houq the comparable number of active hosts during the February '92 busy hour was around 600. The major difference between the early (pre-1990) measurements and the later ones (post- 1990) can be seen during the low traffic hours.

Intuitively, low period router-to-router traffic consists mostly of machine-generated packets which tend to form a much smoother arrival process than low period host-to-host traffic which is typically produced by a smaller than average number of actual Ethernet users, e.g., researchers working late hours. Next, turning our attention to Fig. 7(b), we observe that as in the case of the packet data, H increases as we move from low to normal to high traffic hours. Moreover, while there is practical y no difference between the two post- 1990 data sets, the two pre-1990 sets clearly differ from one another but follow a similar pattern as the post-1990 ones. The difference between the August 1989 and October 1989 measurements can be explained by the transition from diskless to "dataless" workstations that occurred during the latter part of 1989 (see Section 2,2). Except during the low hours, the increased computing power of many of the Ethernet hosts causes H to increase and gives rise to a bit rate that closely matches the self-similar feature of the corresponding packet process.

Also note that the 95%-confidence intervals corresponding to the Hurst parameter estimates for the low traffic hours are typically wider than those corresponding to the estimates of H for the normal and high traffic hours. This widening indicates

| QUALITATIVE DESCRIFITONOF THE SETS OF EXTERNAL ETHERNETTRAFFtC MEASUREMENTSUSED IN THE A   | NALYSISIN SECTION4.3        |            |           |          |
|--------------------------------------------------------------------------------------------|-----------------------------|------------|-----------|----------|
| Traces of Ethernet Traffic Measurements I Total                                            | Total                       | Percentage | of        |          |
| Measurement                                                                                | [ntemal Traffic             |            |           |          |
| Period                                                                                     | Data (see Table I) JAN90.LB |            |           |          |
| JANUARY                                                                                    | 1990                        |            |           |          |
| Start of Trace:                                                                            | JAN90.LP                    |            |           |          |
| Jan. 10,6:07                                                                               | am                          | JAN9CLMB   |           |          |
| End of Trace:                                                                              | JAN90.MP                    |            |           |          |
| JarL 11, 10:17 pm                                                                          | JAN9CLHB JAN90MP FEB92.LB   |            |           |          |
| FEBRUARY                                                                                   | 1992                        |            |           |          |
| Start of Trace:                                                                            | FEB92.LP                    |            |           |          |
| Feb. 18, 5:22 am                                                                           | FEB92.MB                    |            |           |          |
| End of Trace:                                                                              | FEB92.MP                    |            |           |          |
| Feb. 20, 5:16 am                                                                           | FEB92.HB FEB92.HP           | Number of  | NumLux of | Internal |
| Data Set                                                                                   | Bytes                       | Packets    | Traffic   |          |
| JAN90E.LB                                                                                  | 1105876                     | 1.27%      |           |          |
| JAN90E.LP                                                                                  | 9369                        | 3.02%      |           |          |
| JAN90E.MB                                                                                  | 16536148                    | 9.05%      |           |          |
| JAN90E.MP                                                                                  | 87307                       | 13.57%     |           |          |
| JAN90E.HB                                                                                  | 13023016                    | 2.00%      |           |          |
| JAN90E.HP                                                                                  | 68405                       | 4.96%,     |           |          |
| FEB92E.LB                                                                                  | 2319881                     | 4.08%      |           |          |
| FEB92E.LP                                                                                  | 25247                       | 10.89%,    |           |          |
| FEB92E.MB                                                                                  | 86283283                    | 55.80%     |           |          |
| FEB92E.MP                                                                                  | 270636                      | 51.60%     |           |          |
| FEB92E.HB                                                                                  | 55154789                    | 24.50%     |           |          |
| FEB92E.HP                                                                                  | 202367                      | 21.35%     |           |          |

that Ethernet traffic during low traffic periods is asymptotically self-similar rather than exactly self-similar.

We also notice in Fig. 7 that some of the analyzed time series result in estimated Hurst parameters close to 1, i.e., their corresponding 95%-confidence intervals include the value H = 1.

When finding an H-estimate close to 1, it is advisable to analyze the time series further to ensure that the observed high degree of self-similarity is genuine and cannot be explained by elementary arguments (see for example [21]). To illustrate, we consider the sequences JAN90.HP and FEB92.HP; visual inspection of both time series and comparisons with traces of fractional Gaussian noise with H = 0.9 (see, for example, the plots in [23] and [21]) show no obvious signs of nonstationarity; the mean seems to be changing with time but the overall mean appears constant and although, locally, there clearIy exist spurious trends and cycles of varying frequencies, these "typical" features of nonstationarity are characteristic of stationary long-range dependent processes. Moreover, the variance-time plots as well as the pox diagrams of the adjusted range R (without resealing by S) of the two time series yield slope estimates (not shown) that are consistent with the observed high H-values. As discussed in [2] this consistency is a strong indication that the given time series cannot be regarded as nonstationary due to a lack of differencing. Further tests for non-stationarity (e.g., due to nonhomogeneities of H) can be found in [17].

## 4.3. External Ethernet Traflic

The Ethernet traffic analyzed so far is also called iruernal trdlic and consists of all packets on a LAN. An important component of internal Ethernet traffic is the so-called *remote* or *external* Ethernet traffic, consisting of all those Ethernet packets that originate on one LAN but are routed to another LAN. That is, for the traffic measurements at hand, an *external* packet is defined to be an 1P (Internet protocol) packet with a source or destination address that is not on any of the Bellcote networks. This external traffic can be viewed as representative for LAN interconnection services, which are expected to contribute significantly to future broadband traffic.

Table 11 summarizes the external Ethernet traffic data analyzed in the process of this study. We consider the two most reeent measurement traces i.e., the January 1990 and February 1992 data sets, and for ease of comparison, we analyze for both measurement periods the time series consisting of the number of external packets (bytes) per 10 ms during the same low-, normal-, and high-hours of (internal) Ethernet traffic as considered in Table I. The last column in Table II shows that external traffic (in terms of packets or bytes) makes up between 1– 10~0 of the internal traffic during the low hours in January 1990 and February 1992, about 2–2570 during the corresponding busy hours, and up to 56% during the February 1992 normal hour. As a result, it is reasonable to expect external traffic to behave very similarly to the overall traffic analyzed earlier in this section. Differences (if any) between the internal and external traffic can, in general, be attributed to NFS traffic between workstations and file servers which is missing completely in the external traffic.

Repeating the same laborious analysis of Section 4.2 for the data sets described in Table II, we find that in terms of its selfsimilar nature, external traffic does not differ from the internal traffic studied earlier. More specifically, the Hurst parameters for the external traffic during normal and high (internal) traffic hours (or during previously identified stationary parts of the corresponding data sets) are only slightly smaller than the ones depicted in Fig. 7. For instance, even though the portion of external packets during the high (internal) traffic hour of the January 1990 data is only 2% of all the packets seen during this period, the data set JAN90E.HP seems to be well described by an H-value that changes from H = 0.82 for the first 30 min to H = 0.94 for the second 30 rein; recall that the corresponding data set of internal traffic, i.e., the sequence JAN90.HP, has an estimated Hurst parameter of 0.98. A more significant change in the Hurst parameter occurs during the low traffic hours. While the internal traffic data (JAN90.LB, JAN90.LP, FEB92.LB, and FEB92.LP) yield a Hurst parameter of about 0.70, the sequences JAN90E.LB, JAN90E.LP, FEB92E.LB,
and FEB92E.LP have H x 0.55, and the corresponding 95 intervals contain the value H = 0.5. These are the only cases in all the data sets considered in this paper, where an H-value of 0.5 (i.e., conventionally used short-range dependent models such as Poisson, batch-Poisson, or Markov-Modulated Poisson Processes) seems to describe the data accurately. For all other data sets described in Tables I and 11, the 95%-confidence intervals for the Hurst parameter estimates do not even come close to covering the value H = 0.5. As already mentioned in our discussion of Fig. 7, the low hour traffic in the January 199(I and February 1992 data is mostly machine-generated and produces traffic that is typically smoother (i.e., less bursty)
than traffic that is generated during the normal and busy hours by humans using their workstations. This argument applies even more when considering low hour external traffic.

We also looked at the portion of external traffic using the Transmission Control Protocol (TCP) and 1P. There were two main **reasons** for this. First, the traditional services offered by the Internet are for the most part based around TCP, which offers reliable delivery of data and protection against data loss due to lost or corrupted packets. These services include remote Iogin, file transfer (including anonymous file transfer for making information and programs publicly available to any lntemet user), electronic mail. and more recently the delivery of the electronic bulletin board known as Netnews. The second reason is that application programs using the TCP protocol have significantly less control over how their data is actually sent than do applications using the User Datagram Protocol
(LJDP) or their own protocol. The TCP protocol has significant control over how the user data is segmented and a great deal of control over the spacing of the packets as they are sent out. When investigating the external TCP traffic, we found that there was little point in doing a separate analysis. For instance, in the heavy traffic hour from the MRE backbone taken in 1992 (FEB92E. HP), 87% of the packets were TCP packets, and a plot of the external TCP traffic is practically indistinguishable from the corresponding plot of the entire external traffic. Of those TCP packets of the FEB92E.HP data set. about (;(;(~ of the packets were for file transfer, 9~o for remote login~ELNET. 11% for electronic mail, and 13~o for netnews delivery. The 12% of non-TCP traffic simply had no effect on the results of our analysis for this data set; external TC'P traffic is practically identical to the external traffic, and our findings for the external traffic apply directly to external TCP traffic,

## V. Engineering For Self-Similar Network Trafftc

The fact that one can distinguish clearly—with respect to second-order statistical properties-between the existing models for Ethernet traffic and our measured data is surprising and clearly challenges some of the modeling assumptions that have been made in the past. While this distinction is obvious from a statistical perspective, potential traffic engineering implications of this distinction are currently under intense scrutiny. Below, we concentrate on three implications of self-similar network trdftic for traffic engineering purposes: mOdeling individual sources such as Ethernet hosts, inadequacy of conventional notions of "burstiness," and the generation of synthetic traces of self-similar traffic. For a simulation study of the effects of self-similar packet traffic on congestion control and management for B-ISDN, we refer to [7].

## I. 1. On T)Lt, Natl{T-T~Of Tra/Ji( Generated Bt' [Ndi\'Idual . .Ethernet H[~.Sts

In Section IV, we showed that irrespective of when and where the Ethernet measurements were collected, the traffic is self-similar, with different degrees of self-similarity depending on the load on the network. We did so without first studying and modeling the behavior of individual Ethernet users
(sources). Although historically, accurate source modeling has been considered a prerequisite for successful modeling of aggregale traffic, we show here that in the case of self-similar packet traffic, knowledge of fundamental characteristics of the aggregate traffic can provide new insight into the nature of traffic generated by an individual user. Thus, in this section we attempt to give a phenomenological explanation for the visually obvious (see Fig. 4) and statistically significant (see Fig. 7) self-similarity property of aggregate Ethernet LAN
traffic in terms of the behavior of individual Ethernet users.

TO this end, we recall Mandelbrot's construction of fractional Brownian motion (see Section 3.3) and interpret the renewal reward process W('") = (W(m)(t) : t = 0, 1,2, . . .)
introduced in Section 3.3 as the amount of information (in bits, bytes, or packets) generated by Ethernet host m at time t
(1 s m < M, t > O). In fact, if bits or bytes are the prefemed units, the renewal reward process source model resembles the popular class of fluid models (see [1]). On the other hand, if we think of packets as the underlying unit of information, the renewal reward process is basically a packet train model in the sense of [13]. For ease of presentation, we can assume that the "rewards" WO, WI, WZ, . . . *take* only the values 1 and O
(or, to keep E[W] = O, +1 and - 1), with equal probabilities, where the value 1/0 during a renewal interval indicates an active/inactive period during which the source sends 1/0 unit(s)
of information every time unit. The crucial property that distinguishes the renewal reward process source model from the above mentioned models is that the inter-renewal intervals
(i.e., the lengths of the active/inactive periods) are heavy-*tailed* in the sense of (5) or, using Mandelbrot's terminology, exhibit the injinire variance *syndrome.* Intuitively, (5) states that with relatively high probability, the active/inactive periods are very long, i.e., each Wm can assume the same value for a long period of time. While this heavy-tailed property of the activefinactive periods seems plausible in light of tbe way a typical workstation user contributes to the overall traffic on the Ethernet, we have not yet analyzed the traffic generated by individual Ethernet users in order to validate the simple renewal reward source model assumption.

However, evidence in support of the infinite variance syndrome in packet traffic measurements already exists. For example, in a recent study of traffic measurements from an ISDN office automation application, Meier-Hellstem et al.

[24] observed that the extreme variability in the data (e.g., interarrival times of packets, number of successive packet arrivals in certain states) cannot be adequately captured using traditional packet traffic models but, instead, seems to be best described with the help of heavy-tailed distributions of the form (5). These authors subsequently propose an elaborate and highly parametenzed model for the measured traffic. In contrast, the renewal reward source model for the traffic generated by an individual workstation user is extremely simple; moreover, we have seen in Section 3.3 that when aggregating the traffic of many such source models, the resulting superposition process is a fractional Brownian motion with self-similarity parameter H = (3 - 0)/2, where a is given in (5), and that the time series representing, for example, the total number of bytes or Ethernet packets every 10 ms, behaves like fractional Gaussian noise with the same If-value. In this sense, our analysis in Section IV suggests that a simple renewal reward process is an adequate traffic source model for an individual Ethernet user and that often, a more detailed source modeling might not be needed since the convergence result in Section 3.3 shows that many of the details disappear during the process of aggregating the traffic of many sources and only property (5) is required for the fractional Brownian motion behavior of the superposition process to hold. Note that we have reached this conclusion by treating the Ethernet packets essentially as black boxes, i.e., we did not look into the packet header fields or distinguish packets based on their source or destination. Further work on extracting the relevant source-destination addresses from our measurements and on statistically validating the infinite variance property of the inter-renewal periods of a single source is currently in progress.

## 5.2. On Measuring "Burstiness" For Self-Similar Network Trajjic

On an intuitive level, the results of our statistical analysis of the Ethernet traffic measurements in Section IV can be summarized by saying that typically, the higher the load on the Ethernet the higher the estimated Hurst parameter If, i.e.,
the degree of self-similarity in the arrival rate process (in terms of packets or bytes). Visual comparisons between the different traces also suggest that the larger H, the "burstier" the corresponding trace appears. Trying to capture the intuitive notion of "burstiness" with the help of the Hurst parameter l-l becomes particularly appealing in light of the relation H =
(3 - a)/2 mentioned in the previous section between the selfsimikirity parameter H and the parameter a that characterizes the "thickness" (see (5)) of the tail of the inter-renewal time distribution (i.e., of the lengths of the active/inactive periods).

Clearly, the heavier the tail in (5) *(i.e.,* the closer ~ gets to 1), the greater the variability of the active/inactive periods and hence, the burstier the traffic generated by an individual source.

Going from a to H relates burstiness of an individual source to burstiness of the aggregate traffic: the higher the H, the burstier the aggregate traffic. The fact that the Hurst parameter H seems to capture the intuitive notion of burstiness through the concept of self-similarity and, at the same time, also seems to agree well with the visual assessment of bursty behavior challenges the feasibility of some of the most commonly used measures of "burstiness." The latter include the index of dispersion ('Jor *counts),* the peak-to-mean *ratio,* and the coefficient of **variation** (of inter-renewal *times).*
A commonly used measure for capturing the variability of traffic over different time scales is provided by the index of dispersion (for *counts)* and has recently attracted considerable attention (see for example [11 ]). For a given time interval of length L, the index of dispersion for counts (IDC) is given by the variance of the number of arrivals during the interval of length L divided by the expected value of that same quantity. Fig. 8 depicts the IDC as a function of L in log-log

![11_image_0.png](11_image_0.png)

Fig. 8. Index of dispersion for counts (IDC) as a function of the length L of the time interval over which the IDC is calculated, for the high traffic hours of the January 1990 and February 1992 data sets.
coordinates; it shows the IDC for both internal (solid lines)
and external (dashed lines) traffic from the high traffic hour of the January 1990 (Fig. 8(a)) and February 1992 data (b).

Note in particular that the IDC increases monotonically throughout a time span that covers 4-5 orders of magnitude. This behavior is in stark contrast to conventional traffic models such as Poisson or Poisson-like processes and the popular Markov-modulated Poisson processes where the IDC is either constant or converges to a fixed value quite rapidly. On the other hand, self-similar traffic models are easily shown to produce a monotonically increasing IDC. In fact, assume for simplicity that the process X representing the total number of packets seen in every 10 ms interval, is fractional Gaussian noise (with positive drift) with self-similarity parameter H.

CL2H-1 (where c is a finite positi~e constant th~t does not depend on L), and plotting *log(lDC(L))* against *log(L)*
results in an asymptotic straight line with slope 2H - 1. The dotted lines in Figure 5.1 represent the IDC curves predicted by self-similar traffic models with H x 0.94 (JAN90.HP)
and H = 0.96 (FEB92.HP), respectively. Similarly striking agreement between the empirical and theoretical IDC curves can be observed for the corresponding external traffic data sets.

Notice that plotting the IDC curve and estimating its slope provides a quick and simple engineering-based approach to testing for self-similarity of a set of traffic measurements.

Leland and Wilson [ 14] have pointed out the problem with using the peak-to-mean *ratio* as a measure for "bttrstiness" in the presence of self-similar traffic. The observed ratio of peak bandwidth (i.e., peak arrival rate of, say, bytes) to mean bandwidth depends critically on the time interval over which the peak and mean bandwidth is determined, i.e., essentially any peak-to-mean ratio is possible, depending on the length of the measurement interval. For a two-week long trace of the October 1989 measurements, they show that the peak rate in bytes for the external traffic observed in any 5 s interval is about 150 times the mean arrival rate, while the peak rate observed in any 5 ms interval is about 710 times the mean. The dependence of this burstiness measure on the choice of the time interval is clearly undesirable.

Final] y, we remark that the use of the coefficient of *}wriation* (for interarrival times), i.e., the ratio of the standard deviation of the interarrival time to the expected number of the interarrival time, as a measure of "burstiness" becomes questionable because of the potential "heavy-tailedness" (in the sense of (5)) of the interarrival times and the implied infinite variance property. Although the empirical standard deviation can always be calculated, it will depend crucially on the sample size and can attain practically any value as the sample size increases.

## 5.-?. On Generutin<Q .Tynthetic Traces Of Self Similar Trafic

As we have noted in Section IV, exactly self-similar models such as fractional Gaussian noise, or some nonlinew transformation of fractional Gaussian noise (in order to ensure for example that the process takes only positive values) or asymptotically self-similar models such as fractional ARIMA
processes can be used to fit hour-long traces of Ethernet traffic very well. Parameter estimation techniques for these models are known but they often turn out to be computationally too intensive in order to work for large data sets. However, we have illustrated in Section W how to estimate the Hurst parameter H for large data sets, and methods to adapt the existing parameter estimation techniques and to apply them to long time series are currently being studied (for references, see [17]).

Notice also **that** our analysis of the measured data has shown that the Hurst parameter can be expected to change during a measurement period of an hour or more and that refinements such as modeling the change points of H may be needed in the future in order to produce more realistic traffic models. For other approaches to modeling self-similar packet traffic, see the recent articles by Erramilli and Singh [6] who use deterministic nonlinear chaotic maps in order to mimic the fractal-like properties of Ethernet traffic, and Veitch [29] whose work is motivated by the early paper of Mandelbrot [18].

An important requirement of practical traffic modeling is to generate synthetic data sequences that exhibit similar features as the measured traffic. While exact methods for generating synthetic traces from fractional Gaussian noise and fractional ARIMA models exist (see for example [ 12]), they are, in general, only appropriate for short traces (about 1000 observations). For longer time series, short memory approximations have been proposed such as the fast fractional Gaussian
~ujise by Mandelbrot [20]. However, such approximations also become often inappropriate when the sample size becomes exceedingly large. Here, we briefly discuss two methods for generating asymptotically self-similar observations. The tirst method simulates the buffer occupancy in an Al/G/cc queue. where the service time distribution G satisfies the heavy-tail condition (5), i.e., G has infinite variance. Cox l-l] showed that an infinite variance service time distribution results in an asymptotically self-similar buffer occupancy process, and he relates the tail-behavior of the former to the degree of self-similarity of the latter. Generating a time series of length 100000 this way requires about 2 h of CPUtime on a Sun SPARCstation 2. The second method exploits a convergence result obtained by Granger [9] who showed that when aggregating many simple AR( 1)-processes, where the AR(1) parameters are chosen from a beta-distribution on
[0, 1] with shape parameters p and q, then the superposition process is asymptotically self-similau Granger also showed that the Hurst parameter H depends linearly on the shape parameter q of the beta-distribution. This method is well- -suited for parallel computers, and producing a synthetic trace of length 100000 on a MasPar MP- 1216, a massively parallel computer with 16384 processors, takes only a few minutes. In contrast, Hosking's method to produce 100000 observations from a fractional ARIMA(O, d. 0) model requires about 10 h of CPU time on a Sun SPARCstation 2. Implementations of and experimentations with these and some other methods are currently under way.

## Vi. Discussion

Understanding the nature of traffic in high-speed, highbandwidth communications systems such as B-ISDN is essential for engineering, operations, and performance evaluation of these networks. In a first step toward this goal, it is important to know the traffic behavior of some of the expeeted major contributors to future high-speed network traffic. In this paper, we analyze LAN traffic offered to a high-speed public network supporting LAN interconnection, an important and rapidly growing B-ISDN service. The main findings of our statistical analysis of hundreds of millions of high quality, high timeresolution Ethernet LAN traffic measurements are that (i)
Ethernet LAN traffic is statistically self-similar, irrespective of when during the four-year data collection period 1989–1 992 the data were collected and where they were collected in the network, (ii) the degree of self- simihuit y measured in terms of the Hurst parameter H is typically a function of the overall utilization of the Ethernet and can be used for measuring the
"burstiness" of the traffic (namely, the burstier the traffic the higher H), (iii) major components of Ethernet LAN traffic such as external LAN traffic or external TCP traffic share the same self-similar characteristics as the overall LAN traffic, and (iv)
the packet traffic models currently considered in the literature are not able to capture the self-similarity property and can therefore be clearly distinguished from our measured data.

For the purpose of modeling this self-similar or fractal-like nature of the Ethernet traffic data, we introduce novel methods based on self-similar stochastic processes. The motivation for these methods is the desire for an accurate and relatively simple (i.e., parsimonious) description of the complex packet traffic generation process. These modeling approaches typically yield a single parameter (i.e., the Hurst parameter)
that describes the fractal nature of the measured traffic and appears to capture the intuitive notion of "burstiness" where conventional measures of burstiness no longer apply. From the point of view of queueing/performance analysis, the proposed modeling approaches pose new and challenging problems which are likely to require new sets of mathematical tools.

Ultimately, in the context of traffic engineering, it is the predieted performance of appropriately chosen queueing systems that will decide the relevance of self-similar traffic models.

However, indications of the impact of the self-similar nature of packet traffic for engineering, operations, and performance evahtation of high-speed networks are already ample: (i)
source models for individual Ethernet users are expeeted to show extreme variability in terms of interarrival times of packets (i.e., the infinite variance syndrome), (ii) commonly used measures for "burstiness" such as the index of dispersion (for counts), the peak-to-mean-ratio, or the coefficient of variation (for interarrival times) are no longer meaningful for self-similar traffic but can be replaced by the Hurst parameter, (iii) the nature of congestion produced by selfsimilar network traffic models differs drastically from that predicted by standard formal models and displays a far more complicated picture than has been typically assumed in the past, and (iv) first analytic results show a clear distinction between predicted performance of certain queueing models with traditional input streams and the same queueing models with self-similar inputs (see for example [25] and [5]). Finally, in light of the same fractrd-like behavior recently observed in VBR video traffic (see [2] and [8])-another major contributor to future high-speed network traffic-the more complicated nature of congestion due to the self-similar traffic behavior can be expected to persist even when we move toward a more heterogeneous B-ISDN environment. Thus, we believe based on our measured traffic data that the success or failure of, for example, a proposed congestion control scheme for B-ISDN
will depend on how well it performs under a self-similar rather than under one of the standard formal traffic scenarios.

## Acknowledgment

This work could not have been done without the help of J. Beran and R. Sherman who provided the S-functions that made the statistical analysis of an abundance of data possible.

The authors also acknowledge many helpful discussions with A. Erramilli about his dynamical systems approach to packet traffic modeling.

## References

[1]
[9]
D. Anick, D. Mitra, and M. M. SondM, "Stochastic theory of a datahandlin~ svstem with multinle sources." Bell Svstern Tech. J. *vol.* 61.

pP. 187~-i694, 1982. "
J. Bemn. R. Sherman. M. S. Taaau. and W. Wlllinger,"Variable-bit- .-
rate video traffic and long-rangedependence,"acceptedfor publication in IEEE Trans. Commun., 1993.

G. E. P. Box and G. M. Jenkins, Time Series Analysis: Forecasting and Control, 2nd ed. San Francisco, CA: Holden Day, 1976. D. R. Cox, "Long-range dependence: A review," in Skztisrics: An Appraisal, H. A. David and H. T. David, eds. Ames, 1A: The Iowa State University Press, 1984, pp. 55-74.

N. G. Duffield and N. O'Cotrnell, "Large deviations and overflow probabilities for the general single-server queue, with applications,"
preprint, 1993.

A.ErramilliandR.P. Singh, "Chaotic maps as models of packet trafficv in Proc. 14fh *fTC,* Antibes Juan-ies-Pins, France, 1994 (to appear).

H. J. Fowler and W. E. Lekmd, "Locaf area network traffic chamcteristics, with implications for broadband network congestion management,"
IEEE J. Se/ect. Areas Commun. *vol.* 9, pp. 1139–1 149, 1991.

M. W. Garrett and W. WMinger, "Analysis, modelling, and generation of self-similar VBR video traffic," preprint, 1994.

C. W. J. Grarrger, "Long memory relationships and the aggregation of dynamic models," J. Economerr. vol. 14, pp. 227-238, 1980.

[2]
[3] [4] [5]
[6]
[7]
[8]
[29]
C. W. J. Granger and R. Joyeux, "ASSintroduction to long-memory time series models aod fractional dlfferencing," J. Time Series *Anal,* vol. 1, pp. 15-29, 1980. H. Heffes and D. M. Lucsmtoni, "A Markov modulated characterisation of packetized voice and &ta traffic and related statistical multiplexer pxformance," IEEE J. *Select.* Areas Conrnrun., vol. SAC-4, pp. 856-868, 1986.

J. R. M. Hosking, "Fractional differencing," Biometri&a, vol. 68, pp.

16.%176. **1981**
R. Jain and S. A. Routbier, "Packet trains: Measurements and a new model for computer network traffic," fEEE J. Selecr. Areas *Commun.,* vol. SAC-4, pp. 986-995, 1986. W, E. I-eland and D. V. Wilson, "High time-resolution measurement and analysis of LAN traflic: Implications for LAN irrtcrcormcction," in Proc. JEE.ElNFOCOM *'91,* Bal Harbotsr, FL, 1991, pp. 1360-1366. W. E. L-eland, M. S. Taqqu, W. WNinger, and D. V. Wilson, "Orr the self-similar nature of Ethernet traffic," in Proc. ACM *Sigcomm* '93, San Fmocisco, CA, 1993, pp. 183-193.

—, "Statistical analysis of high time-resolution Ethernet LAN traffic measurements," in Proc. 25fh lnre~ace, San Diego, CA, 1993.

—, "Self-similarity in high-speed packet traffic: Analysis and modeling of Ethernet traffic measurements,"Statistical Science, *1994* (to am=).

B. B. Maodelbrot, "Self-similar error clusters in communication systems and the concept of conditional stationarity," IEEE Trans. *Corrrmun.*
Techn,, *vol.* COM- 13, pp. 71-90, 1965.

- "Lmng-rurr linearity, locafly Gaussian processes, H-spectra and infiti'te variances," Intern. Econom. *Rev.,* vol. 10, pp. 82–1 13, 1969. - "A fast fractional Gaussian noise generator," Wafer *Resources* Rese~rch, vol. 7, pp. 543-553, 1971. B. B. Mandelbrnt and M. S. Taqqu, "Robust R/S analysis of long run serial correlation," in *Proc.* 42mi Session 1S1, 1979, pp. 69–99.

B. B. Marrdelbrot and J. W. Van Ness, "Fractional Bruwnian motions, fractional noises and applications," SIAM Rev., *vol.* 10, pp. 422437, 1968.

B. B. Mandelbrot and J. R. Wallis, "Computer experiments witfs fractional Gaussism noises," Water Resources Research, *vol.* 5, pp. 22$267, 1969.

K. Meier-Hellstem, P. E. Wkth, Y.-L. Yan, and D. A. Hoeflin, "Tmf6c models for ISDN data users: Office automation application," in Te/etrufjic and Datatrafic in a Period of Change (Proc. 13th fTC, *Copenhagen,*
1991), A. Jensen and V. B, Iversen, eds. Amsterdam, The Netherlands:
North-Holland, 1991, pp. 167-172.

I. Norros, "Studies on a model for connectionless traffic, based on fractional Brownian motion," COST24TD(92)041, 1992.

E. H. Spafford, "The Internet worm incident," in Proc. *ESEC* 89 and Lecture Notes in Computer Science 87. New York: Springer-Verlag, 1989.

M. S. Taqqu, "A bibliographical guide to self-similar processes and long-range dependence," in Dependence in Probability and *Statistics,* E.

Eberlein and M. S. Taqqu, eds. Base]: Birkhauser, 1985, pp. 137-165.

M. S. Taqqu and J, B. Levy, "Using renewaf processes to generate long-range dependence and high variability," in Dependence in Probobiliry and *Statistics,* E. Ebcrlein and M. S. Taqqu, eds. Boston, MA:
Birkhauser, 1986, vol. 11, pp. *73H9.* D. Veitch, "Novel models of broadband traffic," in Proc, 7th *Australian* Teletraflc Research *Seminar,* Murray River, Australia, 1992.

10]
II]
12]
[13]
[14]
[15]
[16]
[17]
[18]
[19]
[20] [21]
[22]
[23]
[24] [25]
[26]
[27]
[28]
WW Letand (M'82/ACM'77) received the Ph. D.

![13_image_0.png](13_image_0.png)

degree in computer science from the University of Wisconsin, Madison.

He is a Member of Technical Staff at Bellcorc, where he works in the Network Systems Research Department.

Murad Taqqu **(M'92)** received the B. A. degree in mathematics and physics in 1%6 from the Universit.4 de Lausanne-Ecole Polytechnique and the Ph. D. degree in statistics in 1972 from Columbia University, New York.

Since 1985, hehasbeen Professor in the Department of Mathematics al Boston University.

Dr. Taqqu is a Guggenheim Fellow and a Fellow of the Institute of Mathematical Statistics. He is currently an Associate Editor for Skxhsric Pro-
Walter Wilfinger received the Diplom (Dipl.

![14_image_1.png](14_image_1.png)

Math. ) in 1980 from the ETH Zurich, Switzerland, and the M. S. and Ph. D. degrees in 1984 and 1987, respectively, from the School of ORIE, Cornell University, Ithacaj NY.

He k a Memberof TechnicalStaff at Bellcore, where he works in the Computing and Communications Research Department.

Dr. Wlllinger is currently an Associate Editor for The Annals of Applied *ProbabiIiry.*
cesses and fheir *App/icarioris* and coauthor of the book Sksble Non-Gaussian Random Processes: Stochastic Models with *Infinite* Vanunce (Chapman and Hall, 1994).

Daniel V. Wllaon (M'85/ACM'85) received the M,

![14_image_0.png](14_image_0.png)

![14_image_2.png](14_image_2.png)

S. degree in electrical engineering from Stanford University in 1983 and the B. S. degree in physics and mathematics fmm Southwest Missouri State University in 1977.

He is a Member of Technical Staff at Bellcotv where he works on network monitoring and analysis.