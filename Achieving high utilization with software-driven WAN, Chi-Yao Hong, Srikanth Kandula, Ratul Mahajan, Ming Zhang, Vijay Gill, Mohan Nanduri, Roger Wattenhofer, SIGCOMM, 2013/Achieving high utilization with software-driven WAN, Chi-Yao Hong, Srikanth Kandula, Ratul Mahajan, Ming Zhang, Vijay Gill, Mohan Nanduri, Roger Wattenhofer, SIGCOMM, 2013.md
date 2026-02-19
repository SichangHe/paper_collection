![](_page_0_Picture_0.jpeg)

.

![](_page_0_Picture_1.jpeg)

![](_page_0_Picture_2.jpeg)

![](_page_0_Picture_3.jpeg)

![](_page_0_Picture_4.jpeg)

Latest updates: [hps://dl.acm.org/doi/10.1145/2486001.2486012](https://dl.acm.org/doi/10.1145/2486001.2486012)

RESEARCH-ARTICLE

### Achieving high utilization with soware-driven WAN

[CHIYAO](https://dl.acm.org/doi/10.1145/contrib-99659579759) HONG, University of Illinois [Urbana-Champaign,](https://dl.acm.org/doi/10.1145/institution-60000745) Urbana, IL, United States [SRIKANTH](https://dl.acm.org/doi/10.1145/contrib-81100358227) KANDULA, Microso [Corporation,](https://dl.acm.org/doi/10.1145/institution-60026532) Redmond, WA, United States RATUL [MAHAJAN](https://dl.acm.org/doi/10.1145/contrib-81100330255), Microso [Corporation,](https://dl.acm.org/doi/10.1145/institution-60026532) Redmond, WA, United States MING [ZHANG](https://dl.acm.org/doi/10.1145/contrib-81452604633), Microso [Corporation,](https://dl.acm.org/doi/10.1145/institution-60026532) Redmond, WA, United States [VIJAY](https://dl.acm.org/doi/10.1145/contrib-81418594696) GILL, Microso [Corporation,](https://dl.acm.org/doi/10.1145/institution-60026532) Redmond, WA, United States MOHAN [NANDURI](https://dl.acm.org/doi/10.1145/contrib-82659107657), Microso [Corporation,](https://dl.acm.org/doi/10.1145/institution-60026532) Redmond, WA, United States [View](https://dl.acm.org/doi/10.1145/2486001.2486012) all

Open Access [Support](https://libraries.acm.org/acmopen) provided by: Swiss Federal Institute of [Technology,](https://dl.acm.org/doi/10.1145/institution-60025858) Zurich Microso [Corporation](https://dl.acm.org/doi/10.1145/institution-60026532) University of Illinois [Urbana-Champaign](https://dl.acm.org/doi/10.1145/institution-60000745)

![](_page_0_Picture_10.jpeg)

PDF Download 2486001.2486012.pdf 13 January 2026 Total Citations: 998 Total Downloads: 6250

Published: 27 August 2013

[Citation](https://dl.acm.org/action/exportCiteProcCitation?dois=10.1145%2F2486001.2486012&targetFile=custom-bibtex&format=bibtex) in BibTeX format

[SIGCOMM'13:](https://dl.acm.org/conference/comm) ACM SIGCOMM 2013 [Conference](https://dl.acm.org/conference/comm)

*August 12 - 16, 2013 Hong Kong, China*

Conference Sponsors: [SIGCOMM](https://dl.acm.org/sig/sigcomm)

# **Achieving High Utilization with Software-Driven WAN**

## Chi-Yao Hong (UIUC) Srikanth Kandula Ratul Mahajan Ming Zhang Vijay Gill Mohan Nanduri Roger Wattenhofer (ETH)

Microsoft

Abstract— We present SWAN, a system that boosts the utilization of inter-datacenter networks by centrally controlling when and how much traffic each service sends and frequently re-configuring the network's data plane to match current traffic demand. But done simplistically, these reconfigurations can also cause severe, transient congestion because different switches may apply updates at different times. We develop a novel technique that leverages a small amount of scratch capacity on links to apply updates in a provably congestion-free manner, without making any assumptions about the order and timing of updates at individual switches. Further, to scale to large networks in the face of limited forwarding table capacity, SWAN greedily selects a small set of entries that can best satisfy current demand. It updates this set without disrupting traffic by leveraging a small amount of scratch capacity in forwarding tables. Experiments using a testbed prototype and data-driven simulations of two production networks show that SWAN carries 60% more traffic than the current practice.

Categories and Subject Descriptors: C.2.1 [Computer-Communication Networks]: Network Architecture and Design Keywords: Inter-DC WAN; software-defined networking

### 1. INTRODUCTION

The wide area network (WAN) that connects the datacenters (DC) is critical infrastructure for providers of online services such as Amazon, Google, and Microsoft. Many services rely on low-latency inter-DC communication for good user experience and on high-throughput transfers for reliability (e.g., when replicating updates). Given the need for high capacity—inter-DC traffic is a significant fraction of Internet traffic and rapidly growing [\[20\]](#page-12-0)—and unique traffic characteristics, the inter-DC WAN is often a dedicated network, distinct from the WAN that connects with ISPs to reach end users [\[15\]](#page-12-1). It is an expensive resource, with amortized annual cost of 100s of millions of dollars, as it provides 100s of Gbps to Tbps of capacity over long distances.

However, providers are unable to fully leverage this investment today. Inter-DC WANs have extremely poor efficiency; the average utilization of even the busier links is 40-60%. One culprit is the lack of coordination among the services that use the network. Barring coarse, static limits

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

*SIGCOMM'13,* August 12–16, 2013, Hong Kong, China. Copyright 2013 ACM 978-1-4503-2056-6/13/08 ...\$15.00. in some cases, services send traffic whenever they want and however much they want. As a result, the network cycles through periods of peaks and troughs. Since it must be provisioned for peak usage to avoid congestion, the network is under-subscribed on average. Observe that network usage does not have to be this way if we can exploit the characteristics of inter-DC traffic. Some inter-DC services are delay-tolerant. We can tamp the cyclical behavior if such traffic is sent when the demand from other traffic is low. This coordination will boost average utilization and enable the network to either carry more traffic with the same capacity or use less capacity to carry the same traffic.[1](#page-1-0)

Another culprit behind poor efficiency is the distributed resource allocation model of today, typically implemented using MPLS TE (Multiprotocol Label Switching Traffic Engineering) [\[4,](#page-12-2) [24\]](#page-12-3). In this model, no entity has a global view and ingress routers greedily select paths for their traffic. As a result, the network can get stuck in locally optimal routing patterns that are globally suboptimal [\[27\]](#page-12-4).

We present SWAN (Software-driven WAN), a system that enables inter-DC WANs to carry significantly more traffic. By itself, carrying more traffic is straightforward—we can let loose bandwidth-hungry services. SWAN achieves high efficiency while meeting policy goals such as preferential treatment for higher-priority services and fairness among similar services. Per observations above, its two key aspects are i) globally coordinating the sending rates of services; and ii) centrally allocating network paths. Based on current service demands and network topology, SWAN decides how much traffic each service can send and configures the network's data plane to carry that traffic.

Maintaining high utilization requires frequent updates to the network's data plane, as traffic demand or network topology changes. A key challenge is to implement these updates without causing transient congestion that can hurt latencysensitive traffic. The underlying problem is that the updates are not atomic as they require changes to multiple switches. Even if the before and after states are not congested, congestion can occur during updates if traffic that a link is supposed to carry after the update arrives before the traffic that is supposed to leave has left. The extent and duration of such congestion is worse when the network is busier and has larger RTTs (which lead to greater temporal disparity in the application of updates). Both these conditions hold

<span id="page-1-0"></span><sup>1</sup> In some networks, fault tolerance is another reason for low utilization; the network is provisioned such that there is ample capacity even after (common) failures. However, in inter-DC WANs, traffic that needs strong protection is a small subset of the overall traffic, and existing technologies can tag and protect such traffic in the face of failures (§[2\)](#page-2-0).

for our setting, and we find that uncoordinated updates lead to severe congestion and heavy packet loss.

This challenge recurs in every centralized resource allocation scheme. MPLS TE's distributed resource allocation can make only a smaller class of "safe" changes; it cannot make coordinated changes that require one flow to move in order to free a link for use by another flow. Further, recent work on atomic updates, to ensure that no packet experiences a mix of old and new forwarding rules [\[23,](#page-12-5) [29\]](#page-12-6), does not address our challenge. It does not consider capacity limits and treats each flow independently; congestion can still occur due to uncoordinated flow movements.

We address this challenge by first observing that it is impossible to update the network's data plane without creating congestion if all links are full. SWAN thus leaves "scratch" capacity s (e.g., 10%) at each link. We prove that this enables a congestion-free plan to update the network in at most d1/se–1 steps. Each step involves a set of changes to forwarding rules at switches, with the property that there will be no congestion independent of the order and timing of those changes. We then develop an algorithm to find a congestion-free plan with the minimum number of steps. Further, SWAN does not waste the scratch capacity. Some inter-DC traffic is tolerant to small amounts of congestion (e.g., data replication with long deadlines). We extend our basic approach to use all link capacity while guaranteeing bounded-congestion updates for tolerant traffic and congestion-free updates for the rest.

Another challenge that we face is that fully using network capacity requires many forwarding rules at switches, to exploit many alternative paths through the network, but commodity switches support a limited number of forwarding rules.[2](#page-2-1) Analysis of a production inter-DC WAN shows that the number of rules required to fully use its capacity exceeds the limits of even next generation SDN switches. We address this challenge by dynamically changing, based on traffic demand, the set of paths available in the network. On the same WAN, our technique can fully use network capacity with an order of magnitude fewer rules.

We develop a prototype of SWAN, and evaluate our approach through testbed experiments and simulations using traffic and topology data from two production inter-DC WANs. We find that SWAN carries 60% more traffic than MPLS TE and it comes within 2% of the traffic carried by an optimal method that assumes infinite rule capacity and incurs no update overhead. We also show that changes to network updates are quick, requiring only 1-3 steps.

While our work focuses on inter-DC WANs, many of its underlying techniques are useful for other WANs as well (e.g., ISP networks). We show that even without controlling how much traffic enters the network, an ability that is unique to the inter-DC context, our techniques for global resource and change management allow the network to carry 16-25% more traffic than MPLS TE.

### <span id="page-2-0"></span>2. BACKGROUND AND MOTIVATION

Inter-DC WANs carry traffic from a range of services, where a service is an activity across multiple hosts. Externally visible functionality is usually enabled by multiple internal services (e.g., search may use Web-crawler, indexbuilder, and query-responder services). Prior work [\[6\]](#page-12-8) and our conversations with operators reveal that services fall into three broad types, based on their performance requirements.

Interactive services are in the critical path of end user experience. An example is when one DC contacts another in the process of responding to a user request because not all information is available in the first DC. Interactive traffic is highly sensitive to loss and delay; even small increases in response time (100 ms) degrade user experience [\[35\]](#page-12-9).

Elastic services are not in the critical path of user experience but still require timely delivery. An example is replicating a data update to another DC. Elastic traffic requires delivery within a few seconds or minutes. The consequences of delay vary with the service. In the replication example, the risk is loss of data if a failure occurs or that a user will observe data inconsistency.

Background services conduct maintenance and provisioning activities. An example is copying all the data of a service to another DC for long-term storage or as a precursor to running the service there. Such traffic tends to be bandwidth hungry. While it has no explicit deadline or a long deadline, it is still desirable to complete transfers as soon as possible—delays lower business agility and tie up expensive server resources.

In terms of overall volumes, interactive traffic is the smallest subset and background traffic is the largest.

### 2.1 Current traffic engineering practice

Many WANs are operated using MPLS TE today. To effectively use network capacity, MPLS TE spreads traffic across a number of tunnels between ingress-egress router pairs. Ingress routers split traffic, typically equally using equal cost multipath routing (ECMP), across the tunnels to the same egress. They also estimate the traffic demand for each tunnel and find network paths for it using the constrained shortest path first (CSPF) algorithm, which identifies the shortest path that can accommodate the tunnel's traffic (subject to priorities; see below).

With MPLS TE, service differentiation can be provided using two mechanisms. First, tunnels are assigned priorities and different types of services are mapped to different tunnels. Higher priority tunnels can displace lower priority tunnels and thus obtain shorter paths; the ingress routers of displaced tunnels must then find new paths. Second, packets carry differentiated services code point (DSCP) bits in the IP header. Switches map different bits to different priority queues, which ensures that packets are not delayed or dropped due to lower-priority traffic; they may still be delayed or dropped due to equal or higher priority traffic. Switches typically have only a few priority queues (4–8).

### 2.2 Problems of MPLS TE

Inter-DC WANs suffer from two key problems today.

Poor efficiency: The amount of traffic the WAN carries tends to be low compared to capacity. For a production inter-DC WAN, which we call IDN (§[6.1\)](#page-9-0), we find that the average utilization of half the links is under 30% and of three in four links is under 50%.

Two factors lead to poor efficiency. First, services send whenever and however much traffic they want, without regard to the current state of the network or other services. This lack of coordination leads to network swinging between

<span id="page-2-1"></span><sup>2</sup>The limit stems from the amount of fast, expensive memory in switches. It is not unique to OpenFlow switches; number of tunnels that MPLS routers support is also limited [\[2\]](#page-12-7).

<span id="page-3-1"></span><span id="page-3-0"></span>![](_page_3_Figure_0.jpeg)

<span id="page-3-2"></span>Figure 1: Illustration of poor utilization. (a) Daily traffic pattern on a busy link in a production inter-DC WAN. (b) Breakdown based on traffic type. (c) Reduction in peak usage if background traffic is dynamically adapted.

<span id="page-3-4"></span><span id="page-3-3"></span>![](_page_3_Figure_2.jpeg)

<span id="page-3-5"></span>Figure 2: Inefficient routing due to local allocation.

over- and under-subscription. Figure 1a shows the load over a day on a busy link in IDN. Assuming capacity matches peak usage (a common provisioning model to avoid congestion), the average utilization on this link is under 50%. Thus, half the provisioned capacity is wasted. This inefficiency is not fundamental but can be remedied by exploiting traffic characteristics. As a simple illustration, Figure 1b separates background traffic. Figure 1c shows that the same total traffic can fit in half the capacity if background traffic is adapted to use capacity left unused by other traffic.

Second, the local, greedy resource allocation model of MPLS TE is inefficient. Consider Figure 2 in which each link can carry at most one flow. If the flows arrive in the order  $F_A$ ,  $F_B$ , and  $F_C$ , Figure 2a shows the path assignment with MPLS TE:  $F_A$  is assigned to the top path which is one of the shortest paths; when  $F_B$  arrives, it is assigned to the shortest path with available capacity (CSPF); and the same happens with  $F_C$ . Figure 2b shows a more efficient routing pattern with shorter paths and many links freed up to carry more traffic. Such an allocation requires non-local changes, e.g., moving  $F_A$  to the lower path when  $F_B$  arrives.

Partial solutions for such inefficiency exist. Flows can be split across two tunnels, which would divide  $F_A$  across the top and bottom paths, allowing half of  $F_B$  and  $F_C$  to use direct paths; a preemption strategy that prefers shorter paths can also help. But such strategies do not address the fundamental problem of local allocation decisions [27].

Poor sharing: Inter-DC WANs have limited support for flexible resource allocation. For instance, it is difficult to be fair across services or favor some services over certain paths. When services compete today, they typically obtain throughput proportional to their sending rate, an undesirable outcome (e.g., it creates perverse incentives for service developers). Mapping each service onto its own queue at routers can alleviate problems but the number of services (100s) far exceeds the number of available router queues. Even if we had infinite queues and could ensure fairness on the data plane, network-wide fairness is not possible without

<span id="page-3-6"></span>![](_page_3_Figure_8.jpeg)

Figure 3: Link-level fairness  $\neq$  network-wide fairness.

controlling which flows have access to which paths. Consider Figure 3 in which each link has unit capacity and each service  $(S_i \rightarrow D_i)$  has unit demand. With link-level fairness,  $S_2 \rightarrow D_2$  gets twice the throughput of other services. As we show, flexible sharing can be implemented with a limited number of queues by carefully allocating paths to traffic and control the sending rate of services.

### 3. SWAN OVERVIEW AND CHALLENGES

Our goal is to carry more traffic and support flexible network-wide sharing. Driven by inter-DC traffic characteristics, SWAN supports two types of sharing policies. First, it supports a small number of priority classes (e.g., Interactive > Elastic > Background) and allocates bandwidth in strict precedence across these classes, while preferring shorter paths for higher classes. Second, within a class, SWAN allocates bandwidth in a max-min fair manner.

SWAN has two basic components that address the fundamental shortcomings of the current practice. It coordinates the network activity of services and uses centralized resource allocation. Abstractly, it works as:

- All services, except interactive ones, inform the SWAN controller of their demand between pairs of DCs. Interactive traffic is sent like today, without permission from the controller, so there is no delay.
- 2. The controller, which has an up-to-date, global view of the network topology and traffic demands, computes how much each service can send and the network paths that can accommodate the traffic.
- 3. Per SDN paradigm, the controller directly updates the forwarding state of the switches. We use OpenFlow switches, though any switch that permits direct programming of forwarding state (e.g., MPLS Explicit Route Objects [3]) may be used.

While the architecture is conceptually simple, we must address three challenges to realize this design. First, we need a scalable algorithm for global allocation that maximizes network utilization subject to constraints on service priority and fairness. Best known solutions are computationally intensive as they solve long sequences of linear programs (LP) [9, 26]. Instead, SWAN uses a more practical approach that is approximately fair with provable bounds and close to optimal in practical scenarios (§6).

Second, atomic reconfiguration of a distributed system of switches is hard to engineer. Network forwarding state needs updating in response to changes in the traffic demand or network topology. Lacking WAN-wide atomic changes, the network can drop many packets due to transient congestion even if both the initial and final configurations are uncongested. Consider Figure 4 in which each flow is 1 unit and each link's capacity is 1.5 units. Suppose we want to change the network's forwarding state from Figure 4a to 4b, perhaps to accommodate a new flow from  $R_2$  to  $R_4$ . This change requires changes to at least two switches. Depending on the

<span id="page-4-4"></span><span id="page-4-2"></span><span id="page-4-1"></span><span id="page-4-0"></span>![](_page_4_Figure_0.jpeg)

<span id="page-4-5"></span>Figure 4: Illustration of congestion-free updates. Each flow's size is 1 unit and each link's capacity is 1.5 units. Changing from state (a) to (b) may lead to congested states (c) or (d). A congestion-free update sequence is (a)❀(e)❀(f)❀(b).

order in which the switch-level changes occur, the network reaches the states in Figures [4c](#page-4-3) or [4d,](#page-4-4) which have a heavily congested link and can significantly hurt TCP flows as many packets may be lost in a burst.

To avoid congestion during network updates, SWAN computes a multi-step congestion-free transition plan. Each step involves one or more changes to the state of one or more switches, but irrespective of the order in which the changes are applied, there will be no congestion. For the reconfiguration in Figure [4,](#page-4-0) a possible congestion-free plan is: i) move half of F<sup>A</sup> to the lower path (Figure [4e\)](#page-4-5); ii) move F<sup>B</sup> to the upper path (Figure [4f\)](#page-4-6); and iii) move the remaining half of F<sup>A</sup> to the lower path (Figure [4b\)](#page-4-2).

A congestion-free plan may not always exist, and even if it does, it may be hard to find or involve a large number of steps. SWAN leaves scratch capacity of s ∈ [0, 50%] on each link, which guarantees that a transition plan exists with at most d1/se−1 steps (which is 9 if s=10%). We then develop a method to find a plan with the minimal number of steps. In practice, it finds a plan with 1-3 steps when s=10%.

Further, instead of wasting scratch capacity, SWAN allocates it to background traffic. Overall, it guarantees that non-background traffic experiences no congestion during transitions, and the congestion for background traffic is bounded (configurable).

Third, switch hardware supports a limited number of forwarding rules, which makes it hard to fully use network capacity. For instance, if a switch has six distinct paths to a destination but supports only four rules, a third of paths cannot be used. Our analysis of a production inter-DC WAN illustrates the challenge. If we use k-shortest paths between each pair of switches (as in MPLS), fully using this network's capacity requires k=15. Installing these many tunnels needs up to 20K rules at switches (§[6.5\)](#page-10-0), which is beyond the capabilities of even next-generation SDN switches; the Broadcom Trident2 chipset will support 16K OpenFlow rules [\[33\]](#page-12-13). The current-generation switches in our testbed support 750 rules.

To fully exploit network capacity with a limited number of rules, we are motivated by how the working set of a process is often a lot smaller than the total memory it uses. Similarly, not all tunnels are needed at all times. Instead, as traffic demand changes, different sets of tunnels are most suitable. SWAN dynamically identifies and installs these tunnels. Our dynamic tunnel allocation method, which uses an LP, is effective because the number of non-zero variables in a basic solution for any LP is fewer than the number of constraints [\[25\]](#page-12-14). In our case, we will see that variables include the fraction of a DC-pair's traffic that is carried over a

<span id="page-4-7"></span><span id="page-4-3"></span>![](_page_4_Picture_8.jpeg)

Figure 5: Architecture of SWAN.

<span id="page-4-6"></span>tunnel and the number of constraints is roughly the number of priority classes times the number of DC pairs. Because SWAN supports three priority classes, we obtain three tunnels with non-zero traffic per DC pair on average, which is much less than the 15 required for a non-dynamic solution.

Dynamically changing rules introduces another wrinkle for network reconfiguration. To not disrupt traffic, new rules must be added before the old rules are deleted; otherwise, the traffic that is using the to-be-deleted rules will be disrupted. Doing so requires some rule capacity to be kept vacant at switches to accommodate the new rules; done simplistically, up to half of the rule capacity must be kept vacant [\[29\]](#page-12-6), which is wasteful. SWAN sets aside a small amount of scratch space (e.g., 10%) and uses a multi-stage approach to change the set of rules in the network.

### 4. SWAN DESIGN

Figure [5](#page-4-7) shows the architecture of SWAN. A logically centralized controller orchestrates all activity. Each noninteractive service has a broker that aggregates demands from the hosts and apportions the allocated rate to them. One or more network agents intermediate between the controller and the switches. This architecture provides scale by providing parallelism where needed—and choice—each service can implement a rate allocation strategy that fits.

Service hosts and brokers collectively estimate the service's current demand and limit it to the rate allocated by the controller. Our current implementation draws on distributed rate limiting [\[5\]](#page-12-15). A shim in the host OS estimates its demand to each remote DC for the next Th=10 seconds and asks the broker for an allocation. It uses a token bucket per remote DC to enforce the allocated rate and tags packets with DSCP bits to indicate the service's priority class.

The service broker aggregates demand from hosts and updates the controller every Ts=5 minutes. It apportions its allocation from the controller piecemeal, in time units of Th, to hosts in a proportionally fair manner. This way, T<sup>h</sup> is the maximum time that a newly arriving host has to wait before starting to transmit. It is also the maximum time a service takes to change its sending rate to a new allocation. Brokers that suddenly experience radically larger demands can ask for more any time; the controller does a lightweight computation to determine how much of the additional demand can be carried without altering network configuration.

Network agents track topology and traffic with the aid of switches. They relay news about topology changes to the controller right away and collect and report information about traffic, at the granularity of OpenFlow rules, every Ta=5 minutes. They are also responsible for reliably updating switch rules as requested by the controller. Before returning success, an agent reads the relevant part of the switch rule table to ensure that the changes have been successfully applied.

Controller uses the information on service demands and network topology to do the following every  $T_c=5$  minutes.

- 1. Compute the service allocations and forwarding plane configuration for the network (§4.1, §4.2).
- 2. Signal new allocations to services whose allocation has decreased. Wait for  $T_h$  seconds for the service to lower its sending rate.
- 3. Change the forwarding state (§4.3) and then signal the new allocations to services whose allocation has increased.

#### <span id="page-5-0"></span>Forwarding plane configuration

SWAN uses label-based forwarding. Doing so reduces forwarding complexity; the complex classification that may be required to assign a label to traffic is done just once, at the source switch. Remaining switches simply read the label and forward the packet based on the rules for that label. We use VLAN IDs as labels.

Ingress switches split traffic across multiple tunnels (labels). We propose to implement unequal splitting, which leads to more efficient allocation [13], using group tables in the OpenFlow pipeline. The first table maps the packet, based on its destination and other characteristics (e.g., DSCP bits), to a group table. Each group table consists of the set of tunnels available and a weight assignment that reflects the ratio of traffic to be sent to each tunnel. Conversations with switch vendors indicate that most will roll out support for unequal splitting. When such support is unavailable, SWAN uses traffic profiles to pick boundaries in the range of IP addresses belonging to a DC such that splitting traffic to that DC at these boundaries will lead to the desired split. Then, SWAN configures rules at the source switch to map IP destination spaces to tunnels. Our experiments with traffic from a production WAN show that implementing unequal splits in this way leads to a small amount of error (less than 2%).

#### <span id="page-5-1"></span>4.2 Computing service allocations

When computing allocated rate for services, our goal is to maximize network utilization subject to service priorities and approximate max-min fairness among same-priority services. The allocation process must be scalable enough to handle WANs with 100s of switches.

**Inputs:** The allocation uses as input the service demands  $d_i$  between pairs of DCs. While brokers report the demand for non-interactive services, SWAN estimates the demand of interactive services (see below). We also use as input the paths (tunnels) available between a DC pair. Running an unconstrained multi-commodity problem could result in allocations that require many rules at switches. Since a DC pair's traffic could flow through any link, every switch may need rules to split every pair's traffic across its outgoing ports. Constraining usable paths avoids this possibility and also simplifies data plane updates ( $\S4.3$ ). But it may lead to lower overall throughput. For our two production inter-DC WANs, we find that using the 15 shortest paths between each pair of DCs results in negligible loss of throughput.

**Allocation LP:** Figure 6 shows the LP used in SWAN. At the core is the MCF (multi-commodity flow) function that maximizes the overall throughput while preferring shorter paths;  $\epsilon$  is a small constant and tunnel weights  $w_j$  are proportional to latency.  $s_{Pri}$  is the fraction of scratch link capacity that enables congestion-managed network updates;

```
Inputs:
                 flow demands for source destination pair i
        d_i:
                 weight of tunnel j (e.g., latency)
       w_j:
                 capacity of link l
        c_l:
                scratch capacity ([0, 50\%]) for class Pri
    s_{Pri}:
                1 if tunnel j uses link l and 0 otherwise
      I_{j,l}:
  Outputs:
     b_i = \sum_i b_{i,j}: b_i is allocation to flow i; b_{i,j} over tunnel j
  Func: SWAN Allocation:
  \forall links l: c_l^{\text{remain}} \leftarrow c_l; // remaining link capacity
  for Pri = Interactive, Elastic, \dots, Background do
                     Throughput Maximization
        \{b_i\} \leftarrow \begin{array}{ll} {\rm Inroughput Max-Min Fairness} \end{array}
                                                                (Pri, \{c_i^{\text{remain}}\}):
        c_{i}^{\mathrm{remain}} \leftarrow c_{l}^{\mathrm{remain}} - \sum_{i,j} b_{i,j} \cdot I_{j,l};
  Func: Throughput Maximization(Pri, \{c_l^{remain}\}):
  return MCF(Pri, \{c_l^{remain}\}, 0, \infty, \emptyset);
  Func: Approx. Max-Min Fairness(Pri, \{c_i^{\text{remain}}\}):
  // Parameters \alpha and U trade-off unfairness for runtime
  //\alpha > 1 and 0 < U \le \min(\text{fairrate}_i)
 T \leftarrow \lceil \log_{\alpha} \frac{\max(d_i)}{U} \rceil; F \leftarrow \emptyset; for k = 1 \dots T do
        foreach b_i \in MCF(Pri, \{c_l^{remain}\}, \alpha^{k-1}U, \alpha^kU, F) do
             if i \notin F and b_i < \min(d_i, \alpha^k U) then F \leftarrow F + \{i\}; f_i \leftarrow b_i; // flow saturated
  return \{f_i : i \in F\};
  Func: MCF(Pri, \{c_l^{remain}\}, b_{Low}, b_{High}, F):
  //Allocate rate b_i for flows in priority class Pri
                        \begin{array}{l} \sum_{i} b_{i} - \epsilon(\sum_{i,j} w_{j} \cdot b_{i,j}) \\ \forall i \notin F : b_{Low} \leq b_{i} \leq \min(d_{i}, b_{High}); \\ \forall i \in F : b_{i} = f_{i}; \end{array}
    maximize
    subject to
                        \begin{array}{l} \forall l: \sum_{i,j} b_{i,j} \cdot \tilde{I}_{j,l} \leq \min\{c_l^{\mathrm{remain}}, (1-s_{Pri})c_l\}; \\ \forall (i,j): b_{i,j} \geq 0. \end{array}
Figure 6: Computing allocations over a set of tunnels.
```

it can be different for different priority classes (§4.3). The SWAN Allocation function allocates rate by invoking MCF separately for classes in priority order. After a class is allocated, its allocation is removed from remaining link capacity.

It is easy to see that our allocation respects traffic priorities. By allocating demands in priority order, SWAN also ensures that higher priority traffic is likelier to use shorter paths. This keeps the computation simple because MCF's time complexity increases manifold with the number of constraints. While, in general, it may reduce overall utilization, in practice, SWAN achieves nearly optimal utilization (§6).

Max-min fairness can be achieved iteratively: maximize the minimal flow rate allocation, freeze the minimal flows and repeat with just the other flows [26]. However, solving such a long sequence of LPs is rather costly in practice, so we devised an approximate solution instead. SWAN provides approximated max-min fairness for services in the same class by invoking MCF in T steps, with the constraint that at step k, flows are allocated rates in the range  $[\alpha^{k-1}U, \alpha^kU]$ , but no more than their demand. See Fig. 6, function APPROX. MAX-MIN FAIR. A flow's allocation is frozen at step k when it is allocated its full demand  $d_i$  at that step or it receives a rate smaller than  $\alpha^k U$  due to capacity constraints. If  $r_i$  and  $b_i$  are the max-min fair rate and the rate allocated to flow i, we can prove that this is an  $\alpha$ -approximation algorithm, i.e.,  $b_i \in \left[\frac{r_i}{\alpha}, \alpha r_i\right]$  (Theorem 1 in [14]<sup>3</sup>).

Many proposals exist to combine network-wide max-min

<span id="page-5-3"></span><sup>&</sup>lt;sup>3</sup>All proofs are included in a separate technical report [14].

fairness with high throughput. A recent one offers a search function that is shown to empirically reduce the number of LPs that need to be solved [9]. Our contribution is showing that one can trade-off the number of LP calls and the degree of unfairness. The number of LPs we solve per priority is T; with max  $d_i$ =10Gbps, U=10Mbps and  $\alpha$ =2, we get T=10. We find that SWAN's allocations are highly fair and take less than a second combined for all priorities (§6). In contrast, Danna et al. report running times of over a minute [9].

Finally, our approach can be easily extended to other policy goals such as virtually dedicating capacity to a flow over certain paths and weighted max-min fairness.

Interactive service demands: SWAN estimates an interactive service's demand based on its average usage in the last five minutes. To account for prediction errors, we inflate the demand based on the error in past estimates (mean plus two standard deviations). This ensures that enough capacity is set aside for interactive traffic. So that inflated estimates do not let capacity go unused, when allocating rates to background traffic, SWAN adjusts available link capacities as if there was no inflation. If resource contention does occur, priority queueing at switches protects interactive traffic.

**Post-processing:** The solution produced by the LP may not be feasible to implement; while it obeys link capacity concerns, it disregards rule count limits on switches. Directly including these limits in the LP would turn the LP into an Integer LP making it intractably complex. Hence, SWAN post-processes the output of the LP to fit into the number of rules available.

Finding the set of tunnels with a given size that carries the most traffic is NP-complete [13]. SWAN uses the following heuristic: first pick at least the smallest latency tunnel for each DC pair, prefer tunnels that carry more traffic (as per the LP's solution) and repeat as long as more tunnels can be added without violating rule count constraint  $m_j$  at switch j. If  $M_j$  is the number of tunnels that switch j can store and  $\lambda \in [0,50\%]$  is the scratch space needed for rule updates (§4.3.2),  $m_j = (1 - \lambda)M_j$ . In practice, we found that  $\{m_j\}$  is large enough to ensure at least two tunnels per DC pair (§6.5). However, the original allocation of the LP is no longer valid since only a subset of the tunnels are selected due to rule limit constraints. We thus re-run the LP with only the chosen tunnels as input. The output of this run has both high utilization and is implementable in the network.

To further speed-up allocation computation to work with large WANs, SWAN uses two strategies. First, it runs the LP at the granularity of DCs instead of switches. DCs have at least 2 WAN switches, so a DC-level LP has at least 4x fewer variables and constraints (and the complexity of an LP is at least quadratic in this number). To map DC-level allocations to switches, we leverage the symmetry of inter-DC WANs. Each WAN switch in a DC gets equal traffic from inside the DC as border routers use ECMP for outgoing traffic. Similarly, equal traffic arrives from neighboring DCs because switches in a DC have similar fan-out patterns to neighboring DCs. This symmetry allows traffic on each DClevel link (computed by the LP) to be spread equally among the switch-level links between two DCs. However, symmetry may be lost during failures; we describe how SWAN handles failures in  $\S 4.4$ .

Second, during allocation computation, SWAN aggregates the demands from all services in the same priority class between a pair of DCs. This reduces the number of flows that

```
 \begin{aligned} & \textbf{Inputs:} \left\{ \begin{array}{ll} q, & \text{sequence length} \\ b_{i,j}^0 = b_{i,j}, & \text{initial configuration} \\ b_{i,j}^q = b_{i,j}', & \text{final configuration} \\ c_l, & \text{capacity of link } l \\ I_{jl}, & \text{indicates if tunnel } j \text{ using link } l \\ \end{aligned} \right. \\ & \textbf{Outputs:} \left\{ b_{i,j}^a \right\} \ \forall a \in \{1, \dots q\} \text{ if feasible} \\ & \text{maximize} & c_{\text{margin}} \ / / \text{ remaining capacity margin} \\ & \text{subject to} & \forall i, a : \sum_j b_{i,j}^a = b_i; \\ & \forall l, a : c_l \geq \sum_{i,j} \max(b_{i,j}^a, b_{i,j}^{a+1}) \cdot I_{j,l} + c_{\text{margin}}; \\ & \forall (i,j,a) : b_{i,j}^a \geq 0; \ c_{\text{margin}} \geq 0; \end{aligned}
```

Figure 7: LP to find if a congestion-free update sequence of length  $\,q\,$  exists.

the LP has to allocate by a factor that equals the number of services, which can run into 100s. Given the per DC-pair allocation, we divide it among individual services in a max-min fair manner.

#### <span id="page-6-0"></span>4.3 Updating forwarding state

To keep the network highly utilized, its forwarding state must be updated as traffic demand and network topology change. Our goal is to enable forwarding state updates that are not only congestion-free but also quick; the more agile the updates the better one can utilize the network. One can meet these goals trivially, by simply pausing all data movement on the network during a configuration change. Hence, an added goal is that the network continue to carry significant traffic during updates.<sup>4</sup>

Forwarding state updates are of two types: changing the distribution of traffic across available tunnels and changing the set of tunnels available in the network. We describe below how we make each type of change.

#### 4.3.1 Updating traffic distribution across tunnels

Given two congestion-free configurations with different traffic distributions, we want to update the network from the first configuration to the second in a congestion-free manner. More precisely, let the current network configuration be  $C=\{b_{ij}: \forall (i,j)\}$ , where  $b_{ij}$  is the traffic of flow i over tunnel j. We want to update the network's configuration to  $C'=\{b'_{ij}: \forall (i,j)\}$ . This update can involve moving many flows, and when an update is applied, the individual switches may apply the changes in any order. Hence, many transient configurations emerge, and in some, a link's load may be much higher than its capacity. We want to find a sequence of configurations  $(C=C_0,\ldots,C_k=C')$  such that no link is overloaded in any configuration. Further, no link should be overloaded when moving from  $C_i$  to  $C_{i+1}$  regardless of the order in which individual switches apply their updates.

In arbitrary cases congestion-free update sequences do not exist; when all links are full, any first move will congest at least one link. However, given the scratch capacity that we engineered on each link  $(s_{Pri}; \S4.2)$ , we show that there exists a congestion-free sequence of updates of length no more than  $\lceil 1/s \rceil - 1$  steps (Theorem 2 in [14]). The constructive proof of this theorem yields an update sequence with exactly  $\lceil 1/s \rceil - 1$  steps. But shorter sequences may exist and are desirable because they will lead to faster updates.

We use an LP-based algorithm to find the sequence with the minimal number of steps. Figure 7 shows how to exam-

<span id="page-6-1"></span><sup>&</sup>lt;sup>4</sup>Network updates can cause packet re-ordering. In this work, we assume that switch-level (e.g., FLARE [18]) or host-level mechanisms (e.g., reordering robust TCP [36]) are in place to ensure that applications are not hurt.

ine whether a feasible sequence of q steps exists. We vary q from 1 to  $\lceil 1/s \rceil - 1$  in increments of 1. The key part in the LP is the constraint that limits the worst case load on a link during an update to be below link capacity. This load is  $\sum_{i,j} \max(b^a_{i,j}, b^{a+1}_{i,j}) I_{j,l}$  at step a; it happens when none of the flows that will decrease their contribution have done so, but all flows that will increase their contribution have already done so. If q is feasible, the LP outputs  $C_a = \{b^a_{i,j}\}$ , for  $a = (1, \ldots, q-1)$ , which represent the intermediate configurations that form a congestion-free update sequence.

From congestion-free to bounded-congestion: showed above that leaving scratch capacity on each link facilitates congestion-free updates. If there exists a class of traffic that is tolerant to moderate congestion (e.g., background traffic), then scratch capacity need not be left idle; we can fully use link capacities with the caveat that transient congestion will only be experienced by traffic in this class. To realize this, when computing flow allocations (§4.2), we use  $s_{Pri} = s > 0$  for interactive and elastic traffic, but set  $s_{Pri} = 0$  for background traffic (which is allocated last). Thus, link capacity can be fully used, but no more than (1-s) fraction is used by non-background traffic. Just this, however, is not enough: since links are no longer guaranteed to have slack there may not be a congestion-free solution within  $\lceil \frac{1}{2} \rceil - 1$  steps. To remedy this, we replace the perlink capacity constraint in Figure 7 with two constraints, one to ensure that the worst-case traffic on a link from all classes is no more than  $(1 + \eta)$  of link capacity  $(\eta \in [0, 50\%])$  and another to ensure that the worst-case traffic due to the nonbackground traffic is below link capacity. In this case, we prove that i) there is a feasible solution within  $\max(\lceil 1/s \rceil -$ 1,  $\lceil 1/\eta \rceil$ ) steps (Theorem 3 in [14]) such that ii) the nonbackground traffic never encounters loss and iii) the background traffic experiences no more than an  $\eta$  fraction loss. Based on this result, we set  $\eta = \frac{s}{1-s}$  in SWAN, which ensures the same  $\lceil \frac{1}{s} \rceil - 1$  bound on steps as before.

#### <span id="page-7-0"></span>4.3.2 Updating tunnels

To update the set of tunnels in the network from Pto P', SWAN first computes a sequence of tunnel-sets  $(P=P_0,\ldots,P_k=P')$  that each fit within rule limits of switches. Second, for each set, it computes how much traffic from each service can be carried (§4.2). Third, it signals services to send at a rate that is minimum across all tunnel-sets. Fourth, after  $T_h=10$  seconds when services have changed their sending rate, it starts executing tunnel changes as follows. To go from set  $P_i$  to  $P_{i+1}$ : i) add tunnels that are in  $P_{i+1}$  but not in  $P_i$ —the computation of tunnel-sets (described below) guarantees that this will not violate rule count limits; ii) change traffic distribution, using boundedcongestion updates, to what is supported by  $P_{i+1}$ , which frees up the tunnels that are in  $P_i$  but not in  $P_{i+1}$ ; iii) delete these tunnels. Finally, SWAN signals to services to start sending at the rate that corresponds to P'.

We compute the interim tunnel-sets as follows. Let  $P_i^{add}$  and  $P_i^{rem}$  be the set of tunnels that remain be added and removed, respectively, at step i. Initially,  $P_0^{add} = P' - P$  and  $P_0^{rem} = P - P'$ . At each step i, we first pick a subset  $p_i^a \subseteq P_i^{add}$  to add and a subset  $p_i^r \subseteq P_i^{rem}$  to remove. We then update the tunnel sets as:  $P_{i+1} = (P_i \cup p_i^a) - p_i^r$ ,  $P_{i+1}^{add} = P_i^{add} - p_i^a$ , and  $P_{i+1}^{rem} = P_i^{rem} - p_i^r$ . The process ends when  $P_i^{add}$  and  $P_i^{rem}$  are empty (at which point  $P_i$  will be P').

At each step, we also maintain the invariant that  $P_{i+1}$ ,

which is the next set of tunnels that will be installed in the network, leaves  $\lambda M_j$  rule space free at every switch j. We achieve this by picking the maximal set  $p_i^a$  such that the tunnels in  $p_0^a \cup \cdots \cup p_i^a$  fit within  $t_i^{add}$  rules and the minimal set  $p_i^r$  such that the tunnels that remain to be removed  $(P_i^{rem} - p_i^r)$  fit within  $t_i^{rem}$  rules. The value of  $t_i^{add}$  increases with i and that of  $t_i^{rem}$  decreases with i; they are defined more precisely in Theorem 4 in [14]. Within the size constraint, when selecting  $p_i^a$ , SWAN prefers tunnels that will carry more traffic in the final configuration (P') and those that transit through fewer switches. When selecting  $p_i^r$ , it prefers tunnels that carry less traffic in  $P_i$  and those that transit through more switches. This biases SWAN towards finding interim tunnel-sets that carry more traffic and use fewer rules.

We show that the algorithm above requires at most  $\lceil 1/\lambda \rceil - 1$  steps and satisfies the rule count constraints (Theorem 4 in [14]). At interim steps, some services may get an allocation that is lower than that in P or P'. The problem of finding interim tunnel-sets in which no service's allocation is lower than the initial and final set, given link capacity constraints, is NP-hard. (Even much simpler problems related to rule-limits are NP-hard [13]). In practice, however, services rarely experience short-term reductions (§6.6). Also, since both P and P' contain a common core in which there is at least one common tunnel between each DC-pair (per our tunnel selection algorithm; §4.2), basic connectivity is always maintained during transitions, which in practice suffices to carry at least all of the interactive traffic.

### <span id="page-7-1"></span>4.4 Handling failures

Gracefully handling failures is an important part of a global resource controller. We outline how SWAN handles failures. Link and switch failures are detected and communicated to the controller by network agents, in response to which the controller immediately computes new allocations. Some failures can break the symmetry in topology that SWAN leverages for scalable computation of allocation. When computing allocations over an asymmetric topology, the controller expands the topology of impacted DCs and computes allocations at the switch level directly.

Network agents, service brokers, and the controller have backup instances that take over when the primary fails. For simplicity, the backups do not maintain state but acquire what is needed upon taking over. Network agents query the switches for topology, traffic, and current rules. Service brokers wait for  $T_h$  (10 seconds), by which time all hosts would have contacted them. The controller queries the network agents for topology, traffic, and current rule set, and service brokers for current demand. Further, hosts stop sending traffic when they are unable to contact the (primary and secondary) service broker. Service brokers retain their current allocation when they cannot contact the controller. In the period between the primary controller failing and the backup taking over, the network continues to forward traffic as last configured.

#### 4.5 Prototype implementation

We have developed a SWAN prototype that implements all the elements described above. The controller, service brokers and hosts, and network agents communicate with each other using RESTful APIs. We implemented network agents using the Floodlight OpenFlow controller [11], which

<span id="page-8-1"></span>![](_page_8_Figure_0.jpeg)

Figure 8: Our testbed. (a) Partial view of the equipment. (b) Emulated DC-level topology. (c) Closer look at physical connectivity for a pair of DC.

allows SWAN to work with commodity OpenFlow switches. We use the QoS features in Windows Server 2012 to mark DSCP bits in outgoing packets and rate limit traffic using token buckets. We configure priority queues per class in switches. Based on our experiments (§6), we set s=10% and  $\lambda=10\%$  in our prototype.

#### 5. TESTBED-BASED EVALUATION

We evaluate SWAN on a modest-sized testbed. We examine the efficiency and the value of congestion-controlled updates using today's OpenFlow switches and under TCP dynamics. The results of several other testbed experiments, such as failure recovery time, are in [14]. We will extend our evaluation to the scale of today's inter-DC WANs in §6.

#### 5.1 Testbed and workload

Our testbed emulates an inter-DC WAN with 5 DCs spread across three continents (Figure 8). Each DC has: i) two WAN-facing switches; ii) 5 servers per DC, where each server has a 1G Ethernet NIC and acts as 25 virtual hosts; and iii) an internal router that splits traffic from the hosts over the WAN switches. A logical link between DCs is two physical links between their WAN switches. WAN switches are a mix of Arista 7050Ts and IBM Blade G8264s, and routers are a mix of Cisco N3Ks and Juniper MX960s. The SWAN controller is in New York, and we emulate control message delays based on geographic distances.

In our experiment, every DC pair has a demand in each priority class. The demand of the Background class is infinite, whereas Interactive and Elastic demands vary with a period of 3-minutes as per the patterns shown in Figure 9. Each DC pair has a different phase, i.e., their demands are not synchronized. We picked these demands because they have sudden changes in quantity and spatial characteristics to stress SWAN. The actual traffic per {DC-pair, class} consists of 100s of TCP flows. Our switches do not support unequal splitting, so we insert appropriate rules into the switches to split traffic as needed based on IP headers.

We set  $T_s$  and  $T_c$ , the service demand and network update frequencies, to one minute, instead of five, to stress-test SWAN's dynamic behavior.

#### **5.2** Experimental results

Efficiency: Figure 10 shows that SWAN closely approximates the throughput of an optimal method. For each 1-min interval, this method computes service rates using a multiclass, multi-commodity flow problem that is not constrained

<span id="page-8-2"></span>![](_page_8_Figure_11.jpeg)

Figure 9: Demand patterns for testbed experiments.

<span id="page-8-3"></span>![](_page_8_Figure_13.jpeg)

Figure 10: SWAN achieves near-optimal throughput.

<span id="page-8-4"></span>![](_page_8_Figure_15.jpeg)

<span id="page-8-6"></span><span id="page-8-5"></span>Figure 11: Updates in SWAN do not cause congestion.

by the set of available tunnels or rule count limits. It's prediction of interactive traffic is perfect, it has no overhead due to network updates, and it can modify service rates instantaneously.

Overall, we see that SWAN closely approximates the optimal method. The dips in traffic occur during updates because we ask services whose new allocations are lower to reduce their rates, wait for  $T_h{=}10$  seconds, and then ask services with higher allocations to increase their rate. The impact of these dips is low in practice when there are more flows and the update frequency is 5 minutes (§6.6).

Congestion-controlled updates: Figure 11a zooms in on an example update. A new epoch starts at zero and the throughput of each class is shown relative to its maximal allocation before and after the update. We see that with SWAN there is no adverse impact on the throughput in any class when the forwarding plane update is executed at  $t\!=\!10$ s.

To contrast, Figure 11b shows what happens without congestion-controlled updates. Here, as in SWAN, 10% of scratch capacity is kept with respect to non-background traffic, but all update commands are issued to switches in one step. We see that Elastic and Background classes suffer transient throughput degradation due to congestion induced losses followed by TCP backoffs. Interactive traffic is protected due to priority queuing in this example but that does not hold for updates that move a lot of interactive traffic across paths. During updates, the throughput degradation across all traffic in a class is 20%, but as Figure 11c shows, it is as high as 40% for some of the flows.

### <span id="page-8-0"></span>6. DATA-DRIVEN EVALUATION

To evaluate SWAN at scale, we conduct data-driven simulations with topologies and traffic from two production inter-DC WANs of large cloud service providers (§6.1). We show that SWAN can carry 60% more traffic than MPLS TE (§6.2) and is fairer than MPLS TE (§6.3). We also show

that SWAN enables congestion-controlled updates (§6.4) using bounded switch state (§6.5).

#### <span id="page-9-0"></span>6.1 Datasets and methodology

We consider two inter-DC WANs:

**IDN:** A large, well-connected inter-DC WAN with more than 40 DCs. We have accurate topology, capacity, and traffic information for this network. Each DC is connected to 2-16 other DCs, and inter-DC capacities range from tens of Gbps to Tbps. Major DCs have more neighbors and higher capacity connectivity. Each DC has two WAN routers for fault tolerance, and each router connects to both routers in the neighboring DC. We obtain flow-level traffic on this network using sFlow logs collected by routers.

**G-Scale:** Google's inter-DC WAN with 12 DCs and 19 inter-DC links [15]. We do not have traffic and capacity information for it. We simulate traffic on this network using logs from another production inter-DC WAN (different from IDN) with a similar number of DCs. In particular, we randomly map nodes from this other network to **G-Scale**. This mapping retains the burstiness and skew of inter-DC traffic, but not any spatial relationships between the nodes.

We estimate capacity based on the gravity model [30]. Reflecting common provisioning practices, we also round capacity up to the nearest multiple of 80 Gbps. We obtained qualitatively similar results (omitted from the paper) with three other capacity assignment methods: i) capacity is based on 5-minute peak usage across a week when the traffic is carried over shortest paths using ECMP (we cannot use MPLS TE as that requires capacity information); ii) capacity between each pair of DCs is 320 Gbps; iii) capacity between a pair of DCs is 320 or 160 Gbps with equal probability.

With the help of network operators, we classify traffic into individual services and map each service to Interactive, Elastic, or Background class.

We conduct experiments using a flow-level simulator that implements a complete version of SWAN. The demand of the services is derived based on the traffic information from a week-long network log. If the full demand of a service is not allocated in an interval, it carries over to the next interval. We place the SWAN controller at a central DC and simulate control plane latency between the controller and entities in other DCs (service brokers, network agents). This latency is based on shortest paths, where the latency of each hop is based on speed of light in fiber and great circle distance.

#### <span id="page-9-1"></span>6.2 Network utilization

To evaluate how well SWAN utilizes the network, we compare it to an optimal method that can offer 100% utilization. This method computes how much traffic can be carried in each 5-min interval by solving a multi-class, multi-commodity flow problem. It is restricted only by link capacities, not by rule count limits. The changes to service rates are instantaneous, and rate limiting and interactive traffic prediction is perfect.

We also compare SWAN to the current practice, MPLS TE (§2). Our MPLS TE implementation has the advanced features that IDN uses [4, 24]. Priorities for packets and tunnels protect higher-priority packets and ensure shorter paths for higher-priority services. Per re-optimization, CSPF is invoked periodically (5 minutes) to search for better path assignments. Per auto-bandwidth, tunnel bandwidth is periodically (5 minutes) adjusted based on the current traffic

<span id="page-9-3"></span>![](_page_9_Figure_11.jpeg)

Figure 12: SWAN carries more traffic than MPLS TE.

demand, estimated by the maximum of the average (across 5-minute intervals) demand in the past 15 minutes.

Figure 12 shows the traffic that different methods can carry compared to the optimal. To quantify the traffic that a method can carry, we scale service demands by the same factor and use binary search to derive the maximum admissible traffic. We define admissibility as carrying at least 99.9% of service demands. Using a threshold less than 100% makes results robust to demand spikes.

We see that MPLS TE carries only around 60% of the optimal amount of traffic. SWAN, on the other hand, can carry 98% for both WANs. This difference means that SWAN carries over 60% more traffic that MPLS TE, which is a significant gain in the value extracted from the inter-DC WAN.

To decouple gains of SWAN from its two main components—coordination across services and global network configuration—we also simulated a variant of SWAN where the former is absent. Here, instead of getting demand requests from services, we estimate it from their throughput in a manner similar to MPLS TE. We also do not control the rate at which services send. Figure 12 shows that this variant of SWAN improves utilization by 10–12% over MPLS TE, i.e., it carries 15–20% more traffic. Even this level of increase in efficiency translates to savings of millions of dollars in the cost of carrying wide-area traffic. By studying a (hypothetical) version of MPLS that perfectly knows future traffic demand (instead of estimating it based on history), we find that most of SWAN's gain over MPLS stems from its ability to find better path assignments.

We draw two conclusions from this result. First, both components of SWAN are needed to fully achieve its gains. Second, even in networks where incoming traffic cannot be controlled (e.g., ISP network), worthwhile utilization improvements can be obtained through the centralized resource allocation offered by SWAN.

In the rest of the paper, we present results only for IDN. The results for G-Scale are qualitatively similar and are deferred to [14] due to space constraints.

#### <span id="page-9-2"></span>6.3 Fairness

SWAN improves not only efficiency but also fairness. To study fairness, we scale demands such that background traffic is 50% higher than what a mechanism admits; fairness is of interest only when traffic demands cannot be fully met. Scaling relative to traffic admitted by a mechanism ensures that oversubscription level is the same. If we used an identical demand for SWAN and MPLS TE, the oversubscription for MPLS TE would be higher as it carries less traffic.

For an exemplary 5-minute window, Figure 13a shows the throughput that individual flows get relative to their maxmin fair share. We focus on background traffic as the higher priority for other traffic means that its demands are often

<span id="page-10-2"></span>![](_page_10_Figure_0.jpeg)

<span id="page-10-3"></span>Figure 13: SWAN is fairer than MPLS TE.

<span id="page-10-4"></span>![](_page_10_Figure_2.jpeg)

Figure 14: Number of stages and loss in network throughput as a function of scratch capacity.

met. We compute max-min fair shares using a precise but computationally-complex method (which is unsuitable for online use) [26]. We see that SWAN well approximates maxmin fair sharing. In contrast, the greedy, local allocation of MPLS TE is significantly unfair.

Figure 13b shows aggregated results. In SWAN, only 4% of the flows deviate over 5% from their fair share. In MPLS TE, 20% of the flows deviate by that much, and the worst-case deviation is much higher. As Figure 13a shows, the flows that deviate are not necessarily high- or low-demand, but are spread across the board.

#### <span id="page-10-1"></span>**6.4** Congestion-controlled updates

We now study congestion-controlled updates, first the tradeoff regarding the amount of scratch capacity and then their benefit. Higher levels of scratch capacity lead to fewer stages, and thus faster transitions; but they lower the amount of non-background traffic that the network can carry and can waste capacity if background traffic demand is low. Figure 14 shows this tradeoff in practice. The left graph plots the maximum number of stages and loss in network throughput as a function of scratch capacity. At the s=0%extreme, throughput loss is zero but more stages—infinitely many in the worst case—are needed to transition safely. At the s=50% extreme, only one stage is needed, but the network delivers 25-36\% less traffic. The right graph shows the PDF of the number of stages for three values of s. Based on these results, we use s=10%, where the throughput loss is negligible and updates need only 1-3 steps (which is much lower than the theoretical worst case of 9).

To evaluate the benefit of congestion-controlled updates, we compare with a method that applies updates in one shot. This method is identical in every other way, including the amount of scratch capacity left on links. Both methods send updates in a step to the switches in parallel. Each switch applies its updates sequentially and takes 2 ms per update [8].

For each method, during each reconfiguration, we compute the maximum over-subscription (i.e., load relative to capacity), at each link. Short-lived oversubscription will be absorbed by switch queues. Hence, we also compute the

<span id="page-10-5"></span>![](_page_10_Figure_10.jpeg)

Figure 15: Link oversubscription during updates.

<span id="page-10-6"></span>![](_page_10_Figure_12.jpeg)

Figure 16: SWAN needs fewer rules to fully exploit network capacity (left). The number of stages needed for rule changes is small (right).

maximal buffering required at each link for it to not drop any packet, i.e., total excess bytes that arrive during oversubscribed periods. If this number is higher than the size of the physical queue, packets will be dropped. Per priority queuing, we compute oversubscription separately for each traffic class; the computation for non-background traffic ignores background traffic but that for background traffic considers all traffic.

Figure 15 shows oversubscription ratios on the left. We see heavy oversubscription with one-shot updates, especially for background traffic. Links can be oversubscribed by up to 60% of their capacity. The right graph plots extra bytes on the links. Today's top-of-line switches, which we use in our testbed, have queue sizes of 9-16 MB. But we see that oversubscription can bring 100s of MB of excess packets and hence, most of these will be dropped. Note that we did not model TCP backoffs which would reduce the load on a link after packet loss starts happening, but regardless, those flows would see significant slowdown. With SWAN, the worst-case oversubscription is only 11% ( $=\frac{s}{1-s}$ ) as configured for bounded-congestion updates, which presents a significantly better experience for background traffic.

We also see that despite 10% slack, one-shot updates fail to protect even the non-background traffic which is sensitive to loss and delay. Oversubscription can be up to 20%, which can bring over 50 MB of extra bytes during reconfigurations. SWAN fully protects non-background traffic and hence that curve is omitted.

Since routes are updated very frequently even a small likelihood of severe packet loss due to updates can lead to frequent user-visible network incidents. For e.g., when updates happen every minute, a  $\frac{1}{1000}$  likelihood of severe packet loss due to route updates leads to an interruption, on average, once every 7 minutes on the IDN network.

#### <span id="page-10-0"></span>6.5 Rule management

We now study rule management in SWAN. A primary measure of interest here is the amount of network capacity that can be used given a switch rule count limit. Figure 16 (left) shows this measure for SWAN and an alternative that installs rules for the k-shortest paths between DC-pairs; k is chosen such that the rule count limit is not violated for any switch. We see that k-shortest path routing requires 20K rules to fully use network capacity. As mentioned before, this requirement is beyond what will be offered by next-

<span id="page-11-1"></span>![](_page_11_Figure_0.jpeg)

<span id="page-11-3"></span>Figure 17: Time for network update.

<span id="page-11-2"></span>![](_page_11_Figure_2.jpeg)

Figure 18: (a) SWAN carries close to optimal traffic even during updates. (b) Frequent updates lead to higher throughput.

generation switches. The natural progression towards faster link speeds and larger WANs means that future switches may need even more rules. If switches support 1K rules, k-shortest path routing is unable to use 10% of the network capacity. In contrast, SWAN's dynamic tunnels approach enables it to fully use network capacity with an order of magnitude fewer rules. This fits within the capabilities of current-generation switches.

Figure 16 (right) shows the number of stages needed to dynamically change tunnels. It assumes a limit of 750 Open-Flow rules, which is what our testbed switches support. With 10% slack only two stages are needed 95% of the time. This nimbleness stems from 1) the efficiency of dynamic tunnels—a small set of rules are needed per interval, and 2) temporal locality in demand matrices—this set changes slowly across adjacent intervals.

#### <span id="page-11-0"></span>6.6 Other microbenchmarks

We close our evaluation of SWAN by reporting on some key microbenchmarks.

**Update time:** Figure 17 shows the time to update IDN from the start of a new epoch. Our controller uses a PC with a 2.8GHz CPU and runs unoptimized code. The left graph shows a CDF across all updates. The right graph depicts a timeline of the average time spent in various parts. Most updates finish in 22s; most of this time goes into waiting for service rate limits to take effect, 10s each to wait for services to reduce their rate  $(t_1 \text{ to } t_3)$  and then for those whose rate increases ( $t_4$  to  $t_5$ ). SWAN computes the congestion-controlled plan in parallel with the first of these. The network's data plane is in flux for only 600 ms on average  $(t_3 \text{ to } t_4)$ . This includes communication delay from controller to switches and the time to update rules at switches, multiplied by the number of stages required to bound congestion. If SWAN were used in a network without explicit resource signaling. the average update time would only be this 600 ms.

Traffic carried during updates: During updates, SWAN ensures that the network continues to maintain high utilization. That the overall network utilization of SWAN comes close to optimal (§6.2) is an evidence of this behavior. More directly, Figure 18a shows the %-age of traffic that SWAN

carries during updates compared to an optimal method with instantaneous updates. The median value is 96%.

**Update frequency:** Figure 18b shows that frequent updates to the network's data plane lead to higher efficiency. It plots the drop in throughput as the update duration is increased. The service demands still change every 5 minutes but the network data plane updates at the slower rate (x-axis) and the controller allocates as much traffic as the current data plane can carry. We see that an update frequency of 10 (100) minutes reduces throughput by 5% (30%).

Prediction error for interactive traffic: The error in predicting interactive traffic demand is small. For only 1% of the time, the actual amount of interactive traffic on a link differs from the predicted amount by over 1%.

#### 7. DISCUSSION

This section discusses several issues that, for conciseness, were not mentioned in the main body of the paper.

Non-conforming traffic: Sometimes services may (e.g., due to bugs) send more than what is allocated. SWAN can detect these situations using traffic logs that are collected from switches every 5 minutes. It can then notify the owners of the service and protect other traffic by re-marking the DSCP bits of non-confirming traffic to a class that is even lower than background traffic, so that it's carried only if there is any spare capacity.

**Truthful declaration:** Services may declare their lower-priority traffic as higher priority or ask for more bandwidth than they can consume. SWAN discourages this behavior through appropriate pricing: services pay more for higher priority and pay for all allocated resources. (Even within a single organization, services pay for the infrastructure resources they consume.)

Richer service-network interface: Our current design has a simple interface between the services and network, based on current bandwidth demand. In future work, we will consider a richer interface such as letting services reserve resources ahead of time and letting them express their needs in terms of total bytes and a deadline by which they must be transmitted. Better knowledge of such needs can further boost efficiency, for instance, by enabling store-and-forward transfers through intermediate DCs [21]. The key challenge here is the design of scalable and fair allocation mechanisms that composes the diversity of service needs.

#### 8. RELATED WORK

SWAN builds upon several themes in prior work.

Intra-DC traffic management: Many recent works manage intra-DC traffic to better balance load [1, 7, 8] or share among selfish parties [16, 28, 31]. SWAN is similar to the former in using centralized TE and to the latter in providing fairness. But the *intra*-DC case has constraints and opportunities that do not translate to the WAN. For example, EyeQ [16] assumes that the network has a full bisection bandwidth core and hence only paths to or from the core can be congested; this need not hold for a WAN. Seawall [31] uses TCP-like adaptation to converge to fair share, but high RTTs on the WAN would mean slow convergence. Faircloud [28] identifies strategy-proof sharing mechanisms, i.e., resilient to the choices of individual actors. SWAN uses explicit resource signaling to disallow such greedy actions.

Signaling also helps it avoid estimating demands which other centralized TE schemes have to do [\[1,](#page-12-24) [8\]](#page-12-22).

WAN TE & SDN: As in SWAN, B4 uses SDNs in the context of inter-DC WANs [\[15\]](#page-12-1). Although this parallel work shares a similar high-level architecture, it addresses different challenges. While B4 develops custom switches and mechanisms to integrate existing routing protocols in an SDN environment, SWAN develops mechanisms for congestionfree data plane updates and for effectively using the limited forwarding table capacity of commodity switches.

Optimizing WAN efficiency has rich literature including tuning ECMP weights [\[12\]](#page-12-29), adapting allocations across preestablished tunnels [\[10,](#page-12-30) [17\]](#page-12-31), storing and re-routing bulk data at relay nodes [\[21\]](#page-12-23), caching at application-layer [\[32\]](#page-12-32) and leveraging reconfigurable optical networks [\[22\]](#page-12-33). While such bandwidth efficiency is one of the design goals, SWAN also addresses performance and bandwidth requirements of different traffic classes. In fact, SWAN can help many of these systems by providing available bandwidth information and by offering routes through the WAN that may not be discovered by application-layer overlays.

Guarantees during network update: Some recent work provides guarantees during network updates either on connectivity, or loop-free paths or that a packet will see a consistent set of SDN rules [\[19,](#page-12-34) [23,](#page-12-5) [29,](#page-12-6) [34\]](#page-12-35). SWAN offers a stronger guarantee that the network remains uncongested during forwarding rule changes. Vanbever et. al. [\[34\]](#page-12-35) suggest finding an ordering of updates to individual switches that is guaranteed to be congestion free; however, we see that such ordering may not exist (§[6.4\)](#page-10-1) and is unlikely to exist when the network operates at high utilization.

### 9. CONCLUSIONS

SWAN enables a highly efficient and flexible inter-DC WAN by coordinating the sending rates of services and centrally configuring the network data plane. Frequent network updates are needed for high efficiency, and we showed how, by leaving a small amount of scratch capacity on the links and switch rule memory, these updates can be implemented quickly and without congestion or disruption. Testbed experiments and data-driven simulations show that SWAN can carry 60% more traffic than the current practice.

Acknowledgements. We thank Rich Groves, Parantap Lahiri, Dave Maltz, and Lihua Yuan for feedback on the design of SWAN. We also thank Matthew Caesar, Brighten Godfrey, Nikolaos Laoutaris, John Zahorjan, and the SIG-COMM reviewers for feedback on earlier drafts of the paper.

### 10. REFERENCES

- <span id="page-12-24"></span>[1] M. Al-Fares, S. Radhakrishnan, B. Raghavan, N. Huang, and A. Vahdat. Hedera: Dynamic flow scheduling for data center networks. In NSDI, 2010.
- <span id="page-12-7"></span>[2] D. Applegate and M. Thorup. Load optimal MPLS routing with N+M labels. In INFOCOM, 2003.
- <span id="page-12-10"></span>[3] D. Awduche, L. Berger, D. Gan, T. Li, V. Srinivasan, and G. Swallow. RSVP-TE: Extensions to RSVP for LSP tunnels. RFC 3209, 2001.
- <span id="page-12-2"></span>[4] D. Awduche, J. Malcolm, J. Agogbua, M. O'Dell, and J. McManus. Requirements for traffic engineering over MPLS. RFC 2702, 1999.
- <span id="page-12-15"></span>[5] H. Ballani, P. Costa, T. Karagiannis, and A. Rowstron. Towards predictable datacenter networks. In SIGCOMM, 2011.
- <span id="page-12-8"></span>[6] Y. Chen, S. Jain, V. K. Adhikari, Z.-L. Zhang, and K. Xu. A first look at inter-data center traffic characteristics via Yahoo! datasets. In INFOCOM, 2011.

- <span id="page-12-25"></span>[7] M. Chowdhury, M. Zaharia, J. Ma, M. I. Jordan, and I. Stoica. Managing data transfers in computer clusters with Orchestra. In SIGCOMM, 2011.
- <span id="page-12-22"></span>[8] A. R. Curtis, J. C. Mogul, J. Tourrilhes, P. Yalagandula, P. Sharma, and S. Banerjee. DevoFlow: Scaling flow management for high-performance networks. In SIGCOMM, 2011.
- <span id="page-12-11"></span>[9] E. Danna, S. Mandal, and A. Singh. A practical algorithm for balancing the max-min fairness and throughput objectives in traffic engineering. In INFOCOM, 2012.
- <span id="page-12-30"></span>[10] A. Elwalid, C. Jin, S. Low, and I. Widjaja. MATE: MPLS adaptive traffic engineering. In INFOCOM, 2001.
- <span id="page-12-20"></span>[11] Project Floodlight. <http://www.projectfloodlight.org/>.
- <span id="page-12-29"></span>[12] B. Fortz, J. Rexford, and M. Thorup. Traffic engineering with traditional IP routing protocols. IEEE Comm. Mag., 2002.
- <span id="page-12-16"></span>[13] T. Hartman, A. Hassidim, H. Kaplan, D. Raz, and M. Segalov. How to split a flow? In INFOCOM, 2012.
- <span id="page-12-17"></span>[14] C.-Y. Hong, S. Kandula, R. Mahajan, M. Zhang, V. Gill, M. Nanduri, and R. Wattenhofer. Achieving high utilization with software-driven WAN (extended version). Microsoft Research Technical Report 2013-54, 2013.
- <span id="page-12-1"></span>[15] S. Jain et al. B4: Experience with a globally-deployed software defined WAN. In SIGCOMM, 2013.
- <span id="page-12-26"></span>[16] V. Jeyakumar, M. Alizadeh, D. Mazi`eres, B. Prabhakar, and C. Kim. EyeQ: Practical network performance isolation for the multi-tenant cloud. In HotCloud, 2012.
- <span id="page-12-31"></span>[17] S. Kandula, D. Katabi, B. Davie, and A. Charny. Walking the tightrope: Responsive yet stable traffic engineering. In SIGCOMM, 2005.
- <span id="page-12-18"></span>[18] S. Kandula, D. Katabi, S. Sinha, and A. Berger. Dynamic load balancing without packet reordering. SIGCOMM CCR, 2007.
- <span id="page-12-34"></span>[19] N. Kushman, S. Kandula, D. Katabi, and B. M. Maggs. R-BGP: Staying connected in a connected world. In NSDI, 2007.
- <span id="page-12-0"></span>[20] C. Labovitz, S. Iekel-Johnson, D. McPherson, J. Oberheide, and F. Jahanian. Internet inter-domain traffic. SIGCOMM Comput. Commun. Rev., 2010.
- <span id="page-12-23"></span>[21] N. Laoutaris, M. Sirivianos, X. Yang, and P. Rodriguez. Inter-datacenter bulk transfers with NetStitcher. In SIGCOMM, 2011.
- <span id="page-12-33"></span>[22] A. Mahimkar, A. Chiu, R. Doverspike, M. D. Feuer, P. Magill, E. Mavrogiorgis, J. Pastor, S. L. Woodward, and J. Yates. Bandwidth on demand for inter-data center communication. In HotNets, 2011.
- <span id="page-12-5"></span>[23] R. McGeer. A safe, efficient update protocol for OpenFlow networks. In HotSDN, 2012.
- <span id="page-12-3"></span>[24] M. Meyer and J. Vasseur. MPLS traffic engineering soft preemption. RFC 5712, 2010.
- <span id="page-12-14"></span>[25] V. S. Mirrokni, M. Thottan, H. Uzunalioglu, and S. Paul. A simple polynomial time framework for reduced-path decomposition in multi-path routing. In INFOCOM, 2004.
- <span id="page-12-12"></span>[26] D. Nace, N.-L. Doan, E. Gourdin, and B. Liau. Computing optimal max-min fair resource allocation for elastic flows. IEEE/ACM Trans. Netw., 2006.
- <span id="page-12-4"></span>[27] A. Pathak, M. Zhang, Y. C. Hu, R. Mahajan, and D. Maltz. Latency inflation with MPLS-based traffic engineering. In IMC, 2011.
- <span id="page-12-27"></span>[28] L. Popa, G. Kumar, M. Chowdhury, A. Krishnamurthy, S. Ratnasamy, and I. Stoica. FairCloud: Sharing the network in cloud computing. In SIGCOMM, 2012.
- <span id="page-12-6"></span>[29] M. Reitblatt, N. Foster, J. Rexford, C. Schlesinger, and D. Walker. Abstractions for network update. In SIGCOMM, 2012.
- <span id="page-12-21"></span>[30] M. Roughan, A. Greenberg, C. Kalmanek, M. Rumsewicz, J. Yates, and Y. Zhang. Experience in measuring backbone traffic variability: Models, metrics, measurements and meaning. In Internet Measurement Workshop, 2002.
- <span id="page-12-28"></span>[31] A. Shieh, S. Kandula, A. Greenberg, C. Kim, and B. Saha. Sharing the data center network. In NSDI, 2011.
- <span id="page-12-32"></span>[32] S. Traverso, K. Huguenin, I. Trestian, V. Erramilli, N. Laoutaris, and K. Papagiannaki. Tailgate: handling long-tail content with a little help from friends. In WWW, 2012.
- <span id="page-12-13"></span>[33] Broadcom Trident II series. [http://www.broadcom.com/docs/](http://www.broadcom.com/docs/features/StrataXGS_Trident_II_presentation.pdf) [features/StrataXGS\\_Trident\\_II\\_presentation.pdf](http://www.broadcom.com/docs/features/StrataXGS_Trident_II_presentation.pdf), 2012.
- <span id="page-12-35"></span>[34] L. Vanbever, S. Vissicchio, C. Pelsser, P. Francois, and O. Bonaventure. Seamless network-wide IGP migrations. In SIGCOMM, 2011.
- <span id="page-12-9"></span>[35] C. Wilson, H. Ballani, T. Karagiannis, and A. Rowstron. Better never than late: Meeting deadlines in datacenter networks. In SIGCOMM, 2011.
- <span id="page-12-19"></span>[36] M. Zhang, B. Karp, S. Floyd, and L. Peterson. RR-TCP: A reordering-robust TCP with DSACK. In ICNP, 2003.