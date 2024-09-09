## 10.1145/3009824

Measuring bottleneck bandwidth and round-trip propagation time.

## 10.2 Appendix

### 10.1145/3009824

Measuring bottleneck bandwidth and round-trip propagation time.

By all accounts, today's Internet is not moving data as well as it should. Most of the world's cellular users experience delays of seconds to minutes; public Wi-Fi in airports and conference venues is often worse. Physics and climate researchers need to exchange petabytes of data with global collaborators but find their carefully engineered multi-Gbps infrastructure often delivers at only a few Mbps over intercontinental distances.6

These problems result from a design choice made when TCP congestion control was created in the 1980s--interpreting packet loss as "congestion."13 This equivalence was true at the time but was because of technology limitations, not first principles. As NICs (network interface controllers) evolved from Mbps to Gbps and memory chips from KB to GB, the relationship between packet loss and congestion became more tenuous.

Today TCP's loss-based congestion control--even with the current best of breed, CUBIC11--is the primary cause of these problems. When bottleneck buffers are large, loss-based congestion control keeps them full, causing bufferbloat. When bottleneck buffers are small, loss-based congestion control misinterprets loss as a signal of congestion, leading to low throughput. Fixing these problems requires an alternative to loss-based congestion control. Finding this alternative requires an understanding of where and how network congestion originates.

### 10.3 Congestion and Bottlenecks

At any time, a (full-duplex) TCP connection has exactly one slowest link or _bottleneck_ in each direction. The bottleneck is important because:

* It determines the connection's maximum data-delivery rate. This is a general property of incompressible flow (for example, picture a six-lane freeway at rush hour where an accident has reduced one short section to a single lane. The traffic upstream of the accident moves no faster than the traffic through that lane).
* It is where persistent queues form. Queues shrink only when a link's departure rate exceeds its arrival rate. For a connection running at maximum delivery rate, all links upstream of the bottleneck have a faster departure rate so their queues migrate to the bottleneck.

Regardless of how many links a connection traverses or what their individual speeds are, from TCP's viewpoint an arbitrarily complex path behaves as a single link with the same RTT (round-trip time) and bottleneck rate. Two physical constraints, _RTprop_ (round-trip propagation time) and _BtlBw_ (bottleneck bandwidth), bound transport performance. (If the network path were a physical pipe, _RTprop_ would be its length and _BtlBw_ its minimum diameter.)

Figure 1 shows RTT and delivery rate variation with the amount of data _in flight_ (data sent but not yet acknowledged). Blue lines show the _RTprop_ constraint, green lines the _BtlBw_ constraint, and red lines the bottleneck buffer. Operation in the shaded regions is not possible since it would vilate at least one constraint. Transitions between constraints result in three different regions (app-limited, bandwidth-limited, and buffer-limited) with qualitatively different behavior.

When there isn't enough data in flight to fill the pipe, _RTprop_ determines behavior; otherwise, _BtIbIb_ dominates. Constraint lines intersect at _inflight_ = _BtIbW_ \(\times\)_RTprop_, a.k.a. the pipe's BDP (bandwidth-delay product). Since the pipe is full past this point, the _inflight-BDP_ excess creates a queue at the bottleneck, which results in the linear dependence of RTT on _inflight_ data shown in the upper graph. Packets are dropped when the excess exceeds the buffer capacity. _Congestion_ is just sustained operation to the right of the BDP line, and _congestion control_ is some scheme to bound how far to the right a connection operates on average.

Loss-based congestion control operates at the right edge of the bandwidth-limited region, delivering full bottleneck bandwidth at the cost of high delay and frequent packet loss. When memory was expensive buffer sizes were only slightly larger than the BDP, which minimized loss-based congestion control's excess delay. Subsequent memory price decreases resulted in buffers orders of magnitude larger than ISP link BDPs, and the resulting buffer-budgeted RTTs of seconds instead of milliseconds.9

The left edge of the bandwidth-limited region is a better operating point than the right. In 1979, Leonard Kleinrock16 showed this operating point was optimal, maximizing delivered bandwidth while minimizing delay and loss, both for individual connections and for the network as a whole6. Unfortunately, around the same time Jeffrey M. Jaffe14 proved it was impossible to create a distributed algorithm that converged to this operating point. This result changed the direction of research from finding a distributed algorithm that achieved Kleinrock's optimal operating point to investigating different approaches to congestion control.

Our group at Google spends hours each day examining TCP packet header captures from all over the world, making sense of behavior anomalies and pathologies. Our usual first step is finding the essential path characteristics, _RTprop_ and _BtlBw_. That these can be inferred from traces suggests that delay, and converges with high probability to Kleinrock's optimal operating point. Thus began our three-year quest to create a congestion control based on measuring the two parameters that characterize a path: bottleneck bandwidth and round-trip propagation time, or BBR.

### Characterizing the Bottleneck

A connection runs with the highest throughput and lowest delay when (rate balance) the bottleneck packet arrival rate equals _BtlBw_ and (full pipe) the total data in flight is equal to the BDP (= _BtlBw_ x _RTprop_).

The first condition guarantees that the bottleneck can run at 100% utilization. The second guarantees there is enough data to prevent bottleneck starvation but not overfill the pipe. The rate balance condition alone _does not_ ensure there is no queue, only that it cannot change size (for example, if a connection starts by sending its 10-packet Initial Window into a five-packet BDP, then runs at exactly the bottleneck rate, five of the 10 initial packets fill the pipe so the excess forms a standing queue at the bottleneck that cannot dissipate). Similarly, the full pipe condition does not guarantee there is no queue (for example, a connection sending a BDP in BDP/2 bursts gets full bottleneck utilization, but with an average queue of BDP/4). The only way to minimize the queue at the bottleneck and all along the path is to meet both conditions simultaneously.

_BtlBw_ and _RTprop_ vary over the life of a connection, so they must be continuously estimated. TCP currently tracks RTT (the time interval from sending a data packet until it is acknowledged) since it is required for loss detection. At any time \(t\),

\[\mathit{RTT}_{t} = \mathit{RTprop}_{t} + \eta_{t}\]

where \(\eta \geq 0\) represents the "noise" introduced by queues along the path, the receiver's delayed ack strategy, ack aggregation, and so on. _RTprop_ is a physical property of the connection's path and changes only when the path changes. Since path changes happen on time scales > _RTprop_, an unbiased, efficient estimator at time \(T\) is \(R\widehat{T}\!\!the code in Figure 3. (In Linux, sending uses the efficient FQ/pacing queuing discipline,4 which gives BBR line-rate single-connection performance on multigigabit links and handles thousands of lower-rate paced connections with negligible CPU overhead.)

Footnote 4: [https://github.com/google/pacing-guide/pacing-guide/pacing-guide](https://github.com/google/pacing-guide/pacing-guide/pacing-guide).

**Steady-state behavior.** The rate and amount BBR sends is solely a function of the estimated _BitBw_ and _RTprop_, so the filters control adaptation in addition to estimating the bottleneck constraints. This creates the novel control loop shown in Figure 4, which illustrates the RTT (blue), _inflight_ (green) and delivery rate (red) detail from 700ms of a 10Mbps, 40ms flow. The thick gray line above the delivery-rate data is the state of the _BitBw_ max filter. The triangular structures result from BBR cycling pacing_gain to determine if _BitBw_ has increased. The gain used for each part of the cycle is shown time-aligned with the data it influenced. The gain is applied an RTT earlier, when the data is sent. This is indicated by the horizontal jog in the event sequence description running up the left side.

BBR minimizes delay by spending most of its time with one BDP in flight, paced at the _BitBw_ estimate. This moves the bottleneck to the sender so it cannot observe _BitBw_ increases. Consequently, BBR periodically spends an _RTprop_ interval at a pacing_gain > 1, which increases the sending rate and _inflight_. If _BitBw_ hasn't changed, then a queue is created at the bottleneck, increasing RTT, which keeps deliveryRate constant. (This queue is removed by sending at a compensating pacing_gain < 1 for the next _RTprop_.) If _BitBw_ has increased, deliveryRate increases and the new max immediately increases the _BitBw_ filter output, increasing the base pacing rate. Thus, BBR converges to the new bottleneck rate exponentially fast. Figure 5 shows the effect on a 10Mbps, 40ms flow of _BitBw_ abruptly doubling to 20Mbps after 20 seconds of steady operation (top graph) then dropping to 10Mbps after another 20 seconds of steady operation at 20Mbps (bottom graph).

(BBR is a simple instance of a Max-plus control system, a new approach to control based on nonstandard algebra.12 This approach allows the adaptation rate [controlled by the _max_ gain] to be independent of the queue growth [controlled by the _average_ gain]. Applied to this problem, it results in a simple, implicit control loop where the adaptation to physical constraint changes is automatically handled by the filters representing those constraints. A conventional control system would require multiple loops connected by a complex state machine to accomplish the same result.)

Footnote 4: [https://github.com/google/pacing-guide/pacing-guide/pacing-guide](https://github.com/google/pacing-guide/pacing-guide/pacing-guide).

### Single BBR Flow Startup Behavior

Existing implementations handle events such as startup, shutdown, and loss recovery with event-specific algorithms and many lines of code. BBR uses the code detailed earlier for everything, handling events by sequencing through a set of "states" that are defined by a table containing one or more fixed gains and exit criteria. Most of the time is spent in the ProbeBW state described in the section on Steady-state Behavior.

The Startup and Drain states are used at connection start (Figure 6). To handle Internet link bandwidths spanning 12 orders of magnitude, Startup implements a binary search for _BtlBw_ by using a gain of 2/ln2 to double the sending rate while delivery rate is increasing. This discovers _BtlBw_ in _log3BDP_ RTTs but creates up to _2BDP_ excess queue in the process. Once Startup finds _BtlBw_, BBR transitions to Drain, which uses the inverse of Startup's gain to get rid of the excess queue, then to ProbeBW once the _inflight_ drops to a BDP.

Figure 6 shows the first second of a 10Mbps, 40ms BBR flow. The time/sequence plot shows the sender (green) and receiver (blue) progress vs. time. The red line shows a CUBIC sender under identical conditions. Vertical gray lines mark BBR state transitions. The lower figure shows the RTT of the two connections vs. time. Note that the time reference for this data is ack arrival (blue) so, while they appear to be time shifted, events are shown at the point where BBR learns of them and acts.

The lower graph of Figure 6 contrasts BBR and CUBIC. Their initial behavior is similar, but BBR completely drains its startup queue while CUBIC can't. Without a path model to tell it how much of the _inflight_ is excess, CUBIC makes _inflight_ growth less aggressive, but growth continues until either the bottleneck buffer fills and drops a packet or the receiver's _inflight_ limit (TCP's receive window) is reached.

Figure 7 shows RTT behavior during the first eight seconds of the connections shown in Figure 6. CUBIC (red) fills the available buffer, then cycles from 70% to 100% full every few seconds. After startup, BBR (green) runs with essentially no queue.

### Behavior of Multiple BBR Flows Sharing a Bottleneck

Figure 8 shows how individual throughputs for several BBR flows sharing a 100Mbps/10ms bottleneck converge to a fair share. The downward facing triangular structures are connection ProbeRTT states whose self-synchronization accelerates final convergence.

ProbeBW gain cycling (Figure 4) causes bigger flows to yield bandwidth to smaller flows, resulting in each learning its fair share. This happens fairly quickly (a few ProbeBW cycles), though unfairness can persist when late starters overestimate _RTprop_ as a result of starting when other flows have (temporarily) created a queue.

To learn the true _RTProp_, a flow moves to the left of BDP using | ProbeRTT state: when the _RTProp_ estimate has not been updated (that is, by measuring a lower RTT) for many seconds, BBR enters ProbeRTT, which reduces the _inflight_ to four packets for at least one round trip,then returns to the previous state. Large flows entering ProbeRTT drain many packets from the queue, so several flows see a new \(RTprop\) (new minimum RTT). This makes their \(RTprop\) estimates expire at the same time, so they enter ProbeRTT together, which makes the total queue dip larger and causes more flows to see a new \(RTprop\), and so on. This distributed coordination is the key to both fairness and stability.

BBR synchronizes flows around the desirable event of an empty bottleneck queue. By contrast, loss-based congestion control synchronizes around the undesirable events of periodic queue growth and overflow, amplifying delay and packet loss.

### Google B4 WAN

#### Deployment Experience

Google's B4 network is a high-speed WAN (wide-area network) built using commodity switches.15 Losses on these shallow-buffered switches result mostly from coincident arrivals of small traffic bursts. In 2015, Google started switching B4 production traffic from CUBIC to BBR. No issues or regressions were experienced, and since 2016 all B4 TCP traffic uses BBR. Figure 9 shows one reason for switching. BBR's throughput is consistently 2 to 25 times greater than CUBIC's. We had expected even more improvement but discovered that 75% of BBR connections were limited by the kernel's TCP receive buffer, which the network operations team had deliberately set low (8MB) to prevent CUBIC flooding the network with megabytes of excess _inflight_ (8MB/200ms intercontinental RTT \(\Rightarrow\) 335Mbps max throughput). Manually raising the receive buffer on one U.S.-Europe path caused BBR immediately to reach 2Gbps, while CUBIC remained at 15Mbps--the 133x relative improvement predicted by Mathis et al.17

Figure 9 shows BBR vs. CUBIC relative throughput improvement; the inset shows throughput CDFs (cumulative distribution functions). Measures are from an active proper service that opens persistent BBR and CUBIC connections to remote datacenters, then transfers 8MB of data every minute. Probers communicate via many B4 paths within and between North America, Europe, and Asia.

The huge improvement is a direct consequence of BBR _not_ using loss as a congestion indicator. To achieve full bandwidth, existing loss-based congestion controls require the loss rate to be less than the inverse square of the BDP17 (for example, \(<\) one loss per 30 million packets for a 10Gbps/100ms path). Figure 10 compares measured goodput at various loss rates. CUBIC's loss tolerance is a structural property of the algorithm, while BBR's is a configuration parameter. As BBR's loss rate approaches the ProbeBW peak gain, the probability of measuring a delivery rate of the true _BtBw_ drops sharply, causing the max filter to underestimate.

Figure 10 shows BBR vs. CUBIC goodput for 60-second flows on a 100Mbps/100ms link with 0.001 to 50% random loss. CUBIC's throughput decreases by 10 times at 0.1% loss and totally stalls above 1%. The maximum possible throughput is the link rate times fraction delivered (_=1 - lossRate_). BBR meets this limit up to a 5% loss and is close up to 15%.

### YouTube Edge Deployment Experience

BBR is being deployed on Google.com and YouTube video servers. Google is running small-scale experiments in which a small percentage of users are randomly assigned either BBR or CUBIC. Playbacks using BBR show significant improvement in all of YouTube's quality-of-experience metrics, possibly because BBR's behavior is more consistent and predictable. BBR only slightly improves connection throughput because YouTube already adapts the server's streaming rate to well below _BtBw_ to minimize bufferbloat and rebuffer events. Even so, BBR reduces median RTT by 53% on average globally and by more than 80% in the developing world. Figure 11 shows BBR vs. CUBIC median RTT improvement from more than 200 million YouTube playback connections measured on five continents over a week.

More than half of the world's seven billion mobile Internet subscriptions connect via 8kbps to 114kbps 2.5G systems,5 which suffer well-documented problems because of loss-based congestion control's buffer-filling propensities.3 The bottleneck link for these systems is usually between the SGSN (serving GPRS support node)18 and mobile device. SGSN software runs on a standard PC platform with ample memory, so there are frequently megabytes of buffer between the Internet and mobile device. Figure 12 compares (emulated) SGSN Internet-to-mobile delay for BBR and CUBIC. The horizontal lines mark one of the more serious consequences: TCP adapts to long RTT delay except on the connection initiation SYN packet, which has an OS-dependent fixed timeout. When the mobile device is receiving bulk data (for example, from automatic app updates) via a large-buffered SGSN, the device cannot connect to anything on the Internet until the queue emptipractice

\begin{tabular}{p{128.0pt}|p{128.0pt}}
**Mobile Cellular** \\ **Adaptive Bandwidth** \\  Cellular systems adapt per-subscriber bandwidth based partly on a demand estimate that uses the queue of packets destined for the subscriber. Early versions of BBR were tuned to create very small queues, resulting in connections getting stuck at low rates. Raising the peak ProbeBW pacing_gain to create bigger queues resulted in fewer stuck connections, indicating it is possible to be too nice to some networks. With the current _1.25 \(\times\) BtlBw_ peak gain, no degradation is apparent compared with CUBIC on any network. \\
**Delayed and stretched aks**. Cellular, Wi-Fi, and cable broadband networks often delay and aggregate ACKs.1 When _inflight_ is limited to one BDP, this results in throughput-reducing stalls. Raising ProbeBW's cwnd_gain to two allowed BBR to continue sending smoothly at the estimated delivery rate, even when ACKs are delayed by up to one RTT. This largely avoids stalls. \\
**Token-bucket policers**. BBR's initial YouTube deployment revealed that most of the world's ISPS maple traffic with token-bucket policers.7 The bucket is typically full at connection startup so BBR learns the underlying network's _BtlBw_, but once the bucket empties, all packets sent faster than the (much lower than _BtlBw_) bucket fill rate are dropped. BBR eventually learns this new delivery rate, but the ProbeBW gain cycle results in continuous moderate losses. To minimize the upstream bandwidth waste and application latency increase from these losses, we added policer detection and an explicit policer model to BBR. We are also actively researching better ways to mitigate the policer damage. \\ \end{tabular}

Footnote 1: [https://github.com/google/research/google-research/google](https://github.com/google/research/google-research/google)networks

## Appendix - Detailed Description

A STATE MACHINE FOR SEQUENTIAL PROBING

The pacing_gain controls how fast packets are sent relative to BtlBw and is key to BBR's ability to learn. A pacing_gain > 1 increases inflight and decreases packet inter-arrival time, moving the connection to the right on figure 1. A pacing_gain < 1 has the opposite effect, moving the connection to the left.

BBR uses this pacing_gain to implement a simple sequential probing state machine that alternates between testing for higher bandwidths and then testing for lower round-trip times. [It's not necessary to probe for less bandwidth since that is handled automatically by the BtlBw max filter: new measurements reflect the drop, so BtlBw will correct itself as soon as the last old measurement times out of the filter. The RTprop min filter automatically handles path length increases similarly.]

If the bottleneck bandwidth increases, BBR must send faster to discover this. Likewise, if the actual round-trip propagation delay changes, this changes the BDP, and thus BBR must send slower to get inflight below BDP in order to measure the new RTprop. Thus, the only way to discover these changes is to run experiments, sending faster to check for BtlBw increases or sending slower to check for RTprop decreases. The frequency, magnitude, duration, and structure of these experiments differ depending on what's already known [startup or steady-state] and sending app behavior [intermittent or continuous].

## STEADY-STATE BEHAVIOR

BBR flows spend the vast majority of their time in networks

ProbeBW state, probing for bandwidth using an approach called _gain cycling_, which helps BBR flows reach high throughput, low queuing delay, and convergence to a fair share of bandwidth. With gain cycling, BBR cycles through a sequence of values for the pacing_gain. It uses an eight-phase cycle with the following pacing_gain values: 5/4, 3/4, 1, 1, 1, 1, 1, 1, 1, 1. Each phase normally lasts for the estimated RTprop. This design allows the gain cycle first to probe for more bandwidth with a pacing_gain above 1.0, then drain any resulting queue with a pacing_gain an equal distance below 1.0, and then cruise with a short queue using a pacing_gain of 1.0. The average gain across all phases is 1.0 because ProbeBW aims for its average pacing rate to equal the available bandwidth and thus maintain high utilization, while maintaining a small, well-bounded queue. Note that while gain cycling varies the pacing_gain value, the cwnd_gain stays constant at two, since delayed and stretched acks can strike at any time [see the section on Delayed and Stretched Acks].

Furthermore, to improve mixing and fairness, and to reduce queues when multiple BBR flows share a bottleneck, BBR randomizes the phases of ProbeBW gain cycling by randomly picking an initial phase--from among all but the 3/4 phase--when entering ProbeBW. Why not start cycling with 3/4? The main advantage of the 3/4 pacing_gain is to drain any queue that can be created by running a 5/4 pacing_gain when the pipe is already full. When exiting Drain or ProbeRTT and entering ProbeBW, there is no queue to drain, so the 3/4 gain does not provide that advantage. Using 3/4 in those contexts only has a cost: a link utilization for that round of 3/4 instead of 1.

networks

Since starting with 3/4 would have a cost but no benefit, and since entering ProbeBW happens at the start of any connection long enough to have a Drain, BBR uses this small optimization.

BBR flows cooperate to periodically drain the bottleneck queue using a state called ProbeRTT. In any state other than ProbeRTT itself, if the RTProp estimate has not been updated [i.e., by getting a lower RTT measurement] for more than 10 seconds, then BBR enters ProbeRTT and reduces the cwnd to a very small value [four packets]. After maintaining this minimum number of packets in flight for at least 200 ms and one round trip, BBR leaves ProbeRTT and transitions to either Startup or ProbeBW, depending on whether it estimates the pipe was filled already.

BBR was designed to spend the vast majority of its time [about 98 percent] in ProbeBW and the rest in ProbeRTT, based on a set of tradeoffs. ProbeRTT lasts long enough [at least 200 ms] to allow flows with different RTTs to have overlapping ProbeRTT states, while still being short enough to bound the performance penalty of ProbeRTT's cwnd capping to roughly 2 percent [200 ms?10 seconds]. The RTProp filter window [10 seconds] is short enough to allow quick convergence if traffic levels or routes change, but long enough so that interactive applications [e.g., Web pages, remote procedure calls, video chunks] often have natural silences or low-rate periods within the window where the flow's rate is low enough or long enough to drain its queue in the bottleneck. Then the RTProp filter opportunistically picks up these RTprop measurements, and RTProp refreshes without requiring ProbeRTT. This

## 1 Introduction

The 2010s ofto open up the receive window and for the BBR sender to realize that BtlBw should be higher: in the first round the receive-window autotuning algorithm grows the receive window; in the second round the sender fills the higher receive window; in the third round the sender gets higher delivery-rate samples. This three-round threshold was validated by YouTube experimental data.

In Drain, BBR aims to quickly drain any queue created in Startup by switching to a pacing_gain that is the inverse of the value used during Startup, which drains the queue in one round. When the number of packets in flight matches the estimated BDP, meaning BBR estimates that the queue has been fully drained but the pipe is still full, then BBR leaves Drain and enters ProbeBW.

Note that BBR's Startup and CUBIC's slow start both explore the bottleneck capacity exponentially, doubling their sending rate each round; they differ in major ways, however. First, BBR is more robust in discovering available bandwidth, since it does not exit the search upon packet loss or [as in CUBIC's Hystart10] delay increases. Second, BBR smoothly accelerates its sending rate, while within every round CUBIC [even with pacing] sends a burst of packets and then imposes a gap of silence. Figure 4 demonstrates the number of packets in flight and the RTT observed on each acknowledgment for BBR and CUBIC.

## 5 REACTING TO TRANSITES

The network path and traffic traveling over it can make sudden dramatic changes. To adapt to these smoothly and robustly, and reduce packet losses in such cases, BBR uses a number of strategies to implement the core model. First,networks

BBR treats cwnd_gain x BDP as a target that the current cwnd approaches cautiously from below, increasing cwnd by no more than the amount of data acknowledged at any time. Second, upon a retransmission timeout, meaning the sender thinks all in-flight packets are lost, BBR conservatively reduces cwnd to one packet and sends a single packet [just like loss-based congestion-control algorithms such as CUBIC]. Finally, when the sender detects packet loss but there are still packets in flight, on the first round of the loss-repair process BBR temporarily reduces the sending rate to match the current delivery rate; on second and later rounds of loss repair it ensures the sending rate never exceeds twice the current delivery rate. This significantly reduces transient losses when BBR encounters policers or competes with other flows on a BDP-scale buffer.

The authors are members of Google's make-tcp-fast project, whose goal is to evolve Internet transport via fundamental research and open source software. Project contributions include TFO (TCP Fast Open), TLP (Tail Loss Probe), RACK loss recovery, fqlpacing, and a large fraction of the git commits to the Linux kernel TCP code for the past five years. 


