# Vl2: A Scalable And Flexible Data Center Network

Albert Greenberg James R. Hamilton Navendu Jain Srikanth Kandula Changhoon Kim Parantap Lahiri David A. Maltz Parveen Patel Sudipta Sengupta Microsoft Research

## Abstract

To be agile and cost eective, data centers should allow dynamic resource allocation across large server pools. In particular, the data center network should enable any server to be assigned to any **service. To meet these goals, we present VL, a practical network architecture that scales to support huge data centers with uniform high**
capacity between servers, performance isolation between services, and Ethernet layer- semantics. VL uses () at addressing **to allow**
service instances to be placed anywhere in the network, () Valiant Load Balancing to spread trac uniformly across network paths, and () end-system based address resolution to scale to large server pools, without introducing complexity to the network control plane. VL's design is driven by detailed measurements of trac and **fault**
data from a large operational cloud service provider. VL's implementation leverages proven network technologies, already **available**
at low cost in high-speed hardware implementations, to build a scalable and reliable network architecture. As a result, VL networks can be deployed today, and we have built a working prototype. We evaluate the merits of the VL design using measurement, analysis, and experiments. Our VL prototype shues . TB of data among servers in  seconds - sustaining a rate that is  of the **maximum possible.**
Categories and Subject Descriptors: **C.. [Computer-Communication Network]: Network Architecture and Design**
General Terms: **Design, Performance, Reliability** Keywords: **Data center network, commoditization**

## 1. Introduction

Cloud services are driving the creation of data centers that **hold**
tens to hundreds of thousands of servers and that concurrently support a large number of distinct services (e.g., search, email, mapreduce computations, and utility computing). e motivations for building such shared data centers are both economic and technical:
to leverage the economies of scale available to bulk deployments and to benet from the ability to dynamically reallocate servers among services as workload changes or equipment fails [, **]. e cost is**
also large - upwards of  million per month for a , server data center - with the servers themselves comprising the largest cost component. To be protable, these data centers must achieve high utilization, and key to this is the property of agility **— the capacity to assign any server to any service.**
Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, to republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. SIGCOMM'09, **August 17–21, 2009, Barcelona, Spain.** Copyright 2009 ACM 978-1-60558-594-9/09/08 ...$10.00.

Agility promises improved risk management and cost savings.

Without agility, each service must pre-allocate enough servers to meet dicult to predict demand spikes, or risk failure at the **brink**
of success. With agility, the data center operator can meet the uctuating demands of individual services from a large shared server pool, resulting in higher server utilization and lower costs.

Unfortunately, the designs for today's data center network **prevent agility in several ways. First, existing architectures do not**
provide enough capacity between the servers they interconnect. Conventional architectures rely on tree-like network congurations built from high-cost hardware. Due to the cost of the equipment, the capacity between dierent branches of the tree is typically oversubscribed by factors of : or more, with paths through the highest levels of the tree oversubscribed by factors of : to :. is limits communication between servers to the point that it fragments the server pool - congestion and computation hot-spots are prevalent even when spare capacity is available elsewhere. Second, while data centers host multiple services, the network does little to prevent a trac ood in one service from aecting the other services around it - when one service experiences a trac ood,it is common for all those sharing the same network sub-tree to suer collateral **damage.**
ird, the routing design in conventional networks achievesscale by assigning servers topologically signicant IP addresses and dividing servers among VLANs. Such fragmentation of the address space limits the utility of virtual machines, which cannot migrate out of their original VLAN while keeping the same IP address. Further, the fragmentation of address space creates an enormous conguration burden when servers must be reassigned among services, and the human involvement typically required in these recongurations limits the speed of deployment.

To overcome these limitations in today's design and achieve agility, we arrange for the network to implement a familiar and concrete model: give each service the illusion that all the servers assigned to it, and only those servers, are connected by a single non-interfering Ethernet switch—a Virtual Layer **— and maintain**
this illusion even as the size of each service varies from  server to
,. Realizing this vision concretely translates into **building a**
network that meets the following three objectives:
- Uniform high capacity**: e maximum rate of a server-to-server**
trac ow should be limited only by the available capacity on the network-interface cards of the sending and receiving servers, and assigning servers to a service should be independent of network topology.

- Performance isolation**: Trac of one service should not be affected by the trac of any other service, just as if each service was**
connected by a separate physical switch.

- Layer- semantics**: Just as if the servers were on a LAN—where**
any IP address can be connected to any port of an Ethernet switch due to at addressing—data-center management so
ware should be able to easily assign any server to any service and congure that server with whatever IP address the service expects. Virtual machines should be able to migrate to any server while keeping the same IP address, and the network conguration of each server should be identical to what it would be if connected via a LAN.

Finally, features like link-local broadcast, on which many **legacy** applications depend, should work.

In this paper we design, implement and evaluate VL, a network architecture for data centers that meets these three objectives and thereby provides agility. In creating VL, a goal was to investigate whether we could create a network architecture that could be deployed today, so we limit ourselves from making any changes to the hardware of the switches or servers, and we require that legacy applications work unmodied. However, the so
ware and operating systems on data-center servers are already extensively **modied**
(e.g., to create hypervisors for virtualization or blob le-systems to store data). erefore, VL's design explores a new split in the responsibilities between host and network - using a layer . shim in servers' network stack to work around limitations of the network devices. No new switch so
ware or APIs are needed.

VL consists of a network built from low-cost switch ASICs arranged into a Clos topology [] that provides extensive path diversity between servers. Our measurements show data centers have tremendous volatility in their workload, their trac, and their failure patterns. To cope with this volatility, we adopt Valiant **Load**
Balancing (VLB) [, **] to spread trac across all available paths**
without any centralized coordination or trac engineering. Using VLB, each server independently picks a path at random through the network for each of the ows it sends to other servers in the data center. Common concerns with VLB, such as the extra latency and the consumption of extra network capacity caused by path stretch, are overcome by a combination of our environment (propagation delay is very small inside a data center) and our topology (which includes an extra layer of switches that packets bounce o of). Our experiments verify that our choice of using VLB achieves both the uniform capacity and performance isolation objectives.

e switches that make up the network operate as layerrouters with routing tables calculated by OSPF, thereby enabling the use of multiple paths (unlike Spanning Tree Protocol) while **using a** well-trusted protocol. However, the IP addresses used by services running in the data center cannot be tied to particular switches in the network, or the agility to reassign servers between services would be lost. Leveraging a trick used in many systems [], VL
assigns servers IP addresses that act as names alone, with no **topological signicance. When a server sends a packet, the shim-layer**
on the server invokes a directory system to learn the actual location of the destination and then tunnels the original packet there. e shim-layer also helps eliminate the scalability problems created by ARP in layer- networks, and the tunneling improves our ability to implement VLB. ese aspects of the design enable VL to provide layer- semantics, while eliminating the fragmentation and waste of server pool capacity that the binding between addresses and **locations causes in the existing architecture.**
Taken together, VL's choices of topology, routing design, and so
ware architecture create a huge shared pool of network capacity that each pair of servers can draw from when communicating. We implement VLB by causing the trac between any pair of servers to bounce o a randomly chosen switch in the top level of the Clos topology and leverage the features of layer- routers, such **as EqualCost MultiPath (ECMP), to spread the trac along multiple subpaths for these two path segments. Further, we use anycast addresses**
and an implementation of Paxos [] in a way that simplies the design of the Directory System and, when failures occur, provides consistency properties that are on par with existing protocols.

![1_image_0.png](1_image_0.png)

 

 

 

	 	

!"#

•$%&'$%() •%&'**++%()
•&,)*- •&,)*-
345 •.%&./010%*2,)*-
Figure : A conventional network architecture for data centers (adapted from gure by Cisco []).

e feasibility of our design rests on several questions that we experimentally evaluate. First, the theory behind Valiant **Load Balancing, which proves that the network will be hot-spot free,requires**
that (a) randomization is performed at the granularity of small packets, and (b) the trac sent into the network conforms to the hose model []. For practical reasons, however, VL picks a dierent path for each ow **rather than packet (falling short of (a)), and it** also relies on TCP to police the oered trac to the hose model
(falling short of (b), as TCP needs multiple RTTs to conform trafc to the hose model). Nonetheless, our experiments show that for data-center trac, the VL design choices are sucient to oer the desired hot-spot free properties in real deployments. Second, the directory system that provides the routing information needed to reach servers in the data center must be able to handle heavy workloads at very low latency. We show that designing and implementing such a directory system is achievable.

In the remainder of this paper we will make the following contributions, in roughly this order.

- **We make a rst of its kind study of the trac patterns in a production data center, and nd that there is tremendous volatility in the**
trac, cycling among - dierent patterns during a day and spending less than  s in each pattern at the th percentile.

- **We design, build, and deploy every component of VL in an -**
server cluster. Using the cluster, we experimentally validate that VL has the properties set out as objectives, such as uniform **capacity and performance isolation. We also demonstrate the speed**
of the network, such as its ability to shue . TB of data among servers in  s.

- We apply Valiant Load Balancing in a new context, the interswitch fabric of a data center, and show that ow-level trac **splitting achieves almost identical split ratios (within  of optimal**
fairness index) on realistic data center trac, and it smoothes utilization while eliminating persistent congestion.

- **We justify the design trade-os made in VL by comparing the**
cost of a VL network with that of an equivalent network based on existing designs.

## 2. Background

In this section, we rst explain the dominant design pattern for data-center architecture today []. We then discuss why this architecture is insucient to serve large cloud-service data centers.

As shown in Figure **, the network is a hierarchy reaching from**
a layer of servers in racks at the bottom to a layer of core routers at the top. ere are typically  to  servers per rack, each singly connected to a Top of Rack (ToR) switch with a  Gbps link. ToRs connect to two aggregation switches for redundancy, and these switches aggregate further connecting to access routers. At the top of the hierarchy, core routers carry trac between access routers and manage trac into and out of the data center. All links use Ethernet as a physical-layer protocol, with a mix of copper and ber cabling. All switches below each pair of access routers form a single layerdomain, typically connecting several thousand servers. To limit overheads (e.g., packet ooding and ARP broadcasts) and to isolate dierent services or logical server groups (e.g., email, search, web front ends, web back ends), servers are partitioned into **virtual LANs (VLANs). Unfortunately, this conventional design suers**
from three fundamental limitations:
Limited server-to-server capacity**: As we go up the hierarchy, we are confronted with steep technical and nancial barriers**
in sustaining high bandwidth. us, as trac moves up through the layers of switches and routers, the over-subscription ratio increases rapidly. For example, servers typically have : over-subscription to other servers in the same rack - that is, they can communicate at the full rate of their interfaces (e.g.,  Gbps). We found that up-links from ToRs are typically : to : oversubscribed (i.e.,  to  Gbps of up-link for  servers), and paths through the highest layer of the tree can be : oversubscribed. is large over-subscription factor fragments the server pool by preventing idle serversfrom being assigned to overloaded services, and it severely limits **the entire**
data-center's performance.

Fragmentation of resources**: As the cost and performance of**
communication depends on distance in the hierarchy, the conventional design encourages service planners to cluster servers nearby in the hierarchy. Moreover, spreading a service outside a single layer- domain frequently requires reconguring IP addresses and VLAN trunks, since the IP addresses used by servers are topologically determined by the access routers above them. e result is a high turnaround time for such reconguration. Today's designs avoid this reconguration lag by wasting resources; the plentiful spare capacity throughout the data center is o
en eectively reserved by individual services (and not shared), so that each **service**
can scale out to nearby servers to respond rapidly to demand spikes or to failures. Despite this, we have observed instances when the growing resource needs of one service have forced data center operations to evict other services from nearby servers, incurring significant cost and disruption.

Poor reliability and utilization: Above the ToR, the basic resilience model is :, i.e., the network is provisioned such **that if an**
aggregation switch or access router fails, there must be sucient remaining idle capacity on a counterpart device to carry the load. is forces each device and link to be run up to at most  of its maximum utilization. Further, multiple paths either do not exist or aren't eectively utilized. Within a layer- domain, the Spanning **Tree Protocol causes only a single path to be used even when multiple paths**
between switches exist. In the layer- portion, Equal Cost Multipath
(ECMP) when turned on, can use multiple paths to a destination if paths of the same cost are available. However, the conventional topology oers at most two paths.

## 3. Measurements & Implications

To design VL, we rst needed to understand the data center environment in which it would operate. Interviews with architects, developers, and operators led to the objectives described in Section **, but developing the mechanisms on which to build the**
network requires a quantitative understanding of the trac **matrix** (who sends how much data to whom and when?) and churn (how o
en does the state of the network change due to changes in demand or switch/link failures and recoveries, etc.?). We analyze **these aspects by studying production data centers of a large cloud service**
provider and use the results to justify our design choices as **well as**
the workloads used to stress the VL testbed.

![2_image_0.png](2_image_0.png)

Figure : Mice are numerous;  of ows are smaller than MB. However, more than  of bytes are in ows between MB and  GB.
Our measurement studies found two key results with implications for the network design. First, the trac patterns inside a data center are highly divergent (as even over  representative **trac**
matrices only loosely cover the actual trac matrices seen),and they change rapidly and unpredictably. Second, the hierarchical topology is intrinsically unreliable—even with huge eort and expense to increase the reliability of the network devices close to the top of the hierarchy, we still see failures on those devices resulting **in signi-** cant downtimes.

## 3.1 Data-Center Traffic Analysis

Analysis of Netow and SNMP data from our data centers reveals several macroscopic trends. First, the ratio of trac **volume**
between servers in our data centers to trac entering/leaving our data centers is currently around : (excluding CDN applications).

Second, data-center computation is focused where high speed access to data on memory or disk is fast and cheap. Although data is distributed across multiple data centers, intense computation and communication on data does not straddle data centers due to the cost of long-haul links. ird, the demand for bandwidth between servers inside a data center is growing faster than the demand for bandwidth to external hosts. Fourth, the network is a bottleneck to computation. We frequently see ToR switches whose uplinks are above  utilization.

To uncover the exact nature of trac inside a data center, we instrumented a highly utilized , node cluster in a data center that supports data mining on petabytes of data. e servers are distributed roughly evenly across  ToR switches, which are connected hierarchically as shown in Figure **.We collected socket-level**
event logs from all machines over two months.

## 3.2 Flow Distribution Analysis

Distribution of ow sizes: Figure  **illustrates the nature of**
ows within the monitored data center. e ow size statistics (marked as '+'s) show that the majority of ows are small (a few KB); most of these small ows are hellos and meta-data requests to the distributed le system. To examine longer ows, we compute a statistic termed total bytes **(marked as 'o's) by weighting each ow** size by its number of bytes. Total bytes tells us, for a random **byte,** the distribution of the ow size it belongs to. Almost all the **bytes** in the data center are transported in ows whose lengths vary **from** about  MB to about  GB. e mode at around  MB springs from the fact that the distributed le system breaks long les into
-MB size chunks. Importantly, ows over a few GB are rare.

![3_image_0.png](3_image_0.png)

![3_image_1.png](3_image_1.png)

Figure : Number of concurrent connections has two modes: () ows per node more than  of the time and ()  ows per node for at least  of the time.

Similar to Internet ow characteristics [],we nd that there are myriad small ows (mice). On the other hand, as compared with Internet ows, the distribution is simpler and more uniform. e reason is that in data centers, internal ows arise in an engineered environment driven by careful design decisions (e.g., the -MB chunk size is driven by the need to amortize disk-seek times over read times) and by strong incentives to use storage and analytic tools with well understood resilience and performance.

Number of Concurrent Flows: Figure  **shows the probability**
density function (as a fraction of time) for the number of concurrent ows going in and out of a machine, computed over all ,
monitored machines for a representative day's worth of ow data.

ere are two modes. More than  of the time, an average machine has about ten concurrent ows, but at least  of the time it has greater than  concurrent ows. We almost never see more than  concurrent ows.

e distributions of ow size and number of concurrent ows both imply that VLB will perform well on this trac. Since even big ows are only  MB ( s of transmit time at  Gbps), randomizing at ow granularity (rather than packet) will not cause perpetual congestion if there is unlucky placement of a few ows. Moreover, adaptive routing schemes may be dicult to implement in the data center, since any reactive trac engineering will need to run at least once a second if it wants to react to individual ows.

## 3.3 Traffic Matrix Analysis

Poor summarizability of trac patterns: **Next, we ask the**
question: **Is there regularity in the trac that might be exploited**
through careful measurement and trac engineering? **If trac in the**
DC were to follow a few simple patterns, then the network could be easily optimized to be capacity-ecient for most trac. To answer, we examine how the Trac Matrix(TM) of the , server cluster changes over time. For computational tractability, we compute the ToR-to-ToR TM - the entry TM(t)i,j **is the number of bytes sent**
from servers in ToR i to servers in ToR j **during the  s beginning**
at time t**. We compute one TM for every  s interval, and servers**
outside the cluster are treated as belonging to a single "ToR".

Given the timeseries of TMs, we nd clusters of similar TMs using a technique due to Zhang et al. []. In short, the technique recursively collapses the trac matrices that are most similar to each other into a cluster, where the distance (i.e., similarity) **reects how** much trac needs to be shued to make one TM look like the other. We then choose a representative TM for each cluster, such that any routing that can deal with the representative TM performs no worse on every TM in the cluster. Using a single representative TM per cluster yields a tting error (quantied by the distances between each representative TMs and the actual TMs they represent),
which will decrease as the number of clusters increases. Finally, if there is a knee point (i.e., a small number of clusters that reduces the tting error considerably), the resulting set of clusters and their representative TMs at that knee corresponds to a succinct number of distinct trac matrices that summarize all TMs in the set.

![3_image_2.png](3_image_2.png)

![3_image_3.png](3_image_3.png)

a trac matrix belongs, i.e., the type of trac mix in the TM, changes quickly and randomly.
Surprisingly, the number of representative trac matrices in our data center is quite large. On a timeseries of  TMs, indicating a day's worth of trac in the datacenter, even when approximating with 50 − 60 **clusters, the tting error remains high () and**
only decreases moderately beyond that point. is indicatesthat the variability in datacenter trac is not amenable to concise summarization and hence engineering routes for just a few trac matrices is unlikely to work well for the trac encountered in practice.

Instability of trac patterns: Next we ask **how predictable is**
the trac in the next interval given the current trac? Trac predictability enhances the ability of an operator to engineer **routing**
as trac demand changes. To analyze the predictability of trac in the network, we nd the  best TM clusters using the technique above and classify the trac matrix for each  s interval to the best tting cluster. Figure **(a) shows that the trac pattern changes**
nearly constantly, with no periodicity that could help predict the future. Figure **(b) shows the distribution of run lengths - how many**
intervals does the network trac pattern spend in one cluster before shi
ing to the next. e run length is  to the th percentile.

Figure **(c) shows the time between intervals where the trac maps** to the same cluster. But for the mode at s caused by transitions within a run, there is no structure to when a trac pattern will next appear.

e lack of predictability stems from the use of randomness to improve the performance of data-center applications. For example, the distributed le system spreads data chunks randomly across servers for load distribution and redundancy. e volatility implies that it is unlikely that other routing strategies will outperform VLB.

## 3.4 Failure Characteristics

To design VL to tolerate the failures and churn found in data centers, we collected failure logs for over a year from eight **production data centers that comprise hundreds of thousands of servers,**
host over a hundred cloud services and serve millions of users. We analyzed hardware and so
ware failures of switches, routers, load balancers, rewalls, links and servers using SNMP polling/traps, syslogs, server alarms, and transaction monitoring frameworks. In all, we looked at M error events from over K alarm tickets.

What is the pattern of networking equipment failures? We dene a failure as the event that occurs when a system or component is unable to perform its required function for more than  s.

As expected, most failures are small in size (e.g.,  of network device failures involve <  devices and  of network device failures involve <  **devices) while large correlated failures are rare**
(e.g., the largest correlated failure involved  switches). However, downtimes can be signicant:  of failures are resolved in  **min,**
 in <  hr, . in <  day, but . last >  **days.**
What is the impact of networking equipment failure? As discussed in Section , conventional data center networks apply : re-

![4_image_0.png](4_image_0.png)

Figure : An example Clos network between Aggregation and Intermediate switches provides a richly-connected backbone **wellsuited for VLB. e network is built with two separate address**
families - topologically signicant Locator Addresses (LAs) and at Application Addresses (AAs).
dundancy to improve reliability at higher layers of the hierarchical tree. Despite these techniques, we nd that in . of failures all redundant components in a network device group became unavailable (e.g., the pair of switches that comprise each node in the conventional network (Figure **) or both the uplinks from a switch). In**
one incident, the failure of a core switch (due to a faulty supervisor card) aected ten million users for about four hours. We found the main causes of these downtimes are network miscongurations, rmware bugs, and faulty components (e.g., ports). With no obvious way to eliminate all failures from the top of the hierarchy, VL's approach is to broaden the topmost levels of the network so that the impact of failures is muted and performance degrades gracefully, moving from : redundancy to n:m redundancy.

## 4. Virtual Layer Two Networking

Before detailing our solution, we briey discuss our design **principles and preview how they will be used in the VL design.**
Randomizing to Cope with Volatility**: VL copes with**
the high divergence and unpredictability of data-center trac matrices by using Valiant Load Balancing to do destinationindependent (e.g., random) trac spreading across multiple intermediate nodes. We introduce our network topology suited for VLB
in §., and the corresponding ow spreading mechanism in §..

VLB, in theory, ensures a non-interfering packet switched network [], the counterpart of a non-blocking circuit switched network, as long as (a) trac spreading ratios are uniform, and (b**) the**
oered trac patterns do not violate edge constraints (i.e., line card speeds). To meet the latter condition, we rely on TCP's end-to-end congestion control mechanism. While our mechanisms to realize VLB do not perfectly meet either of these conditions, we show in §. **that our scheme's performance is close to the optimum.**
Building on proven networking technology**: VL is based on**
IP routing and forwarding technologies that are already available in commodity switches: link-state routing, equal-cost multi-path
(ECMP) forwarding, IP anycasting, and IP multicasting. VL **uses** a link-state routing protocol to maintain the switch-level **topology,** but not to disseminate end hosts' information. is strategy **protects** switches from needing to learn voluminous, frequently-changing host information. Furthermore, the routing design uses ECMP forwarding along with anycast addresses to enable VLB with minimal control plane messaging or churn.

Separating names from locators**: e data center network**
must support agility, which means, in particular, support for hosting any service on any server, for rapid growing and shrinking of **server**
pools, and for rapid virtual machine migration. In turn, this calls for separating names from locations. VL's addressing scheme separates server names, termed application-specic addresses (AAs),
from their locations, termed location-specic addresses (LAs). VL uses a scalable, reliable directory system to maintain the mappings between names and locators. A shim layer running in the network stack on every server, called the VL agent, invokes the directory system's resolution service. We evaluate the performance of the directory system in §..

Embracing End Systems**: e rich and homogeneous programmability available at data-center hosts provides a mechanism**
to rapidly realize new functionality. For example, the VL agent enables ne-grained path control by adjusting the randomization used in VLB. e agent also replaces Ethernet's ARP functionality **with**
queries to the VL directory system. e directory system itself is also realized on servers, rather than switches, and thus oers exibility, such as ne-grained, context-aware server access control and dynamic service re-provisioning.

We next describe each aspect of the VL system and how they work together to implement a virtual layer- network. ese aspects include the network topology, the addressing and routing design, and the directory that manages name-locator mappings.

## 4.1 Scale-Out Topologies

As described in §., conventional hierarchical data-center topologies have poor bisection bandwidth and are also susceptible to major disruptions due to device failures at the highest levels.

Rather than scale up individual network devices with more capacity and features, we scale out **the devices - build a broad network**
oering huge aggregate capacity using a large number of simple, inexpensive devices, as shown in Figure **. is is an example of a**
folded Clos network [] where the links between the Intermediate switches and the Aggregation switches form a complete bipartite graph. As in the conventional topology, ToRs connect to two Aggregation switches, but the large number of paths between every two Aggregation switches means that if there are n **Intermediate switches, the failure of any one of them reduces the bisection**
bandwidth by only 1/n–a desirable graceful degradation of bandwidth **that we evaluate in §.. Further, it is easy and less expensive to build a Clos network for which there is no over-subscription**
(further discussion on cost is in §). For example, in Figure **, we**
use DA-port Aggregation and DI **-port Intermediate switches, and**
connect these switches such that the capacity between each layer is DIDA/2 **times the link capacity.**
e Clos topology is exceptionally well suited for VLB in that by indirectly forwarding trac through an Intermediate switch at the top tier or "spine" of the network, the network can provide bandwidth guarantees for any trac matrices subject to the hose model.

Meanwhile, routing is extremely simple and resilient on this topology - take a random path up to a random intermediate switch and a random path down to a destination ToR switch.

VL leverages the fact that at every generation of technology, switch-to-switch links are typically faster than server-to-switch links, and trends suggest that this gap will remain. Our current design uses G server links and G switch links, and the next design point will probably be G server links with G switch links. By leveraging this gap, we reduce the number of cables required **to implement the Clos (as compared with a fat-tree []), and we simplify**
the task of spreading load over the links (§.).

![5_image_0.png](5_image_0.png) 

Figure : VLB in an example VL network. Sender S sends packets to destination D **via a randomly-chosen intermediate switch**
using IP-in-IP encapsulation. AAs are from 20/8, and LAs are from 10/8. H(ft**) denotes a hash of the ve tuple.**

## 4.2 Vl2 Addressing And Routing

is section explains how packets ow through a VL network, and how the topology, routing design, VL agent, and directory system combine to virtualize the underlying network fabric - creating the illusion that hosts are connected to a big, non-interfering datacenter-wide layer- switch.

## 4.2.1 Address Resolution And Packet Forwarding

VL uses two dierent IP-address families, as illustrated in Figure **. e network infrastructure operates using location-specic**
IP addresses (LAs); all switches and interfaces are assigned LAs, and switches run an IP-based (layer-) link-state routing protocol that disseminates only these LAs. is allows switches to obtain the complete switch-level topology, as well as forward packets encapsulated with LAs along shortest paths. On the other hand, applications use application-specic IP addresses (AAs), which remain unaltered no matter how servers' locations change due to virtual-machine migration or re-provisioning. Each AA (server) is associated with an LA,
the identier of the ToR switch to which the server is connected. e VL directory system stores the mapping of AAs to LAs, and this mapping is created when application servers are provisioned to a service and assigned AA addresses.

e crux of oering layer- semantics is having servers believe they share a single large IP subnet (i.e., the entire AA space) with other servers in the same service, while eliminating the ARP and DHCP scaling bottlenecks that plague large Ethernets.

Packet forwarding: **To route trac between servers, which use**
AA addresses, on an underlying network that knows routes for LA addresses, the VL agent at each server traps packets from the host and encapsulates the packet with the LA address of the ToR of the destination as shown in Figure **. Once the packet arrives at the**
LA (the destination ToR), the switch decapsulates the packet and delivers it to the destination AA carried in the inner header.

Address resolution: **Servers in each service are congured to**
believe that they all belong to the same IP subnet. Hence, when an application sends a packet to an AA for the rst time, the networking stack on the host generates a broadcast ARP request for the destination AA. e VL agent running on the host intercepts this ARP request and converts it to a unicast query to the VL directory system.

e directory system answers the query with the LA of the ToR to which packets should be tunneled. e VL agent caches this mapping from AA to LA addresses, similar to a host's ARP cache, such that subsequent communication need not entail a directory lookup.

Access control via the directory service: **A server cannot send**
packets to an AA if the directory service refuses to provide it with an LA through which it can route its packets. is means that the directory service can enforce access-control policies. Further, since the directory system knows which server is making the request when handling a lookup, it can enforce ne-grained isolation policies. For example, it could enforce the policy that only servers belonging to the same service can communicate with each other. An advantage of VL is that, when inter-service communication is allowed, packets ow directly from a source to a destination, without being detoured to an IP gateway as is required to connect two VLANs in the conventional architecture.

ese addressing and forwarding mechanisms were chosen for two reasons. First, they make it possible to use low-cost switches, which o
en have small routing tables (typically just 16**K entries)**
that can hold only LA routes, without concern for the huge number of AAs. Second, they reduce overhead in the network control plane by preventing it from seeing the churn in host state, tasking **it to the** more scalable directory system instead.

## 4.2.2 Random Traffic Spreading Over Multiple Paths

To oer hot-spot-free performance for arbitrary trac matrices, VL uses two related mechanisms: VLB and ECMP. e goals of both are similar - VLB distributes trac across a set of intermediate nodes and ECMP distributes across equal-cost paths **— but**
each is needed to overcome limitations in the other. VL uses ows, rather than packets, as the basic unit of trac spreading and **thus** avoids out-of-order delivery.

Figure  **illustrates how the VL agent uses encapsulation to implement VLB by sending trac through a randomly-chosen Intermediate switch. e packet is rst delivered to one of the Intermediate switches, decapsulated by the switch, delivered to the ToR's LA,**
decapsulated again, and nally sent to the destination.

While encapsulating packets to a specic, but randomly chosen, Intermediate switch correctly realizes VLB, it would require updating a potentially huge number of VL agents whenever an Intermediate switch's availability changes due to switch/link failures. Instead, we assign the same LA address to all Intermediate switches, and the directory system returns this anycast address **to agents upon** lookup. Since all Intermediate switches are exactly three hops away from a source host, ECMP takes care of delivering packets encapsulated with the anycast address to any one of the active Intermediate switches. Upon switch or link failures, ECMP will react, eliminating the need to notify agents and ensuring scalability.

In practice, however, the use of ECMP leads to two problems.

First, switches today only support up to -way ECMP, with - way ECMP being released by some vendors this year. If there are more paths available than ECMP can use, then VL denes several anycast addresses, each associated with only as many Intermediate switches as ECMP can accommodate. When an Intermediate switch fails, VL reassigns the anycast addresses from that switch **to other**
Intermediate switches so that all anycast addresses remain **live, and**
servers can remain unaware of the network churn. Second, some inexpensive switches cannot correctly retrieve the ve-tuple values (e.g., the TCP ports) when a packet is encapsulated with multiple IP
headers. us, the agent at the source computes a hash of the vetuple values and writes that value into the source IP address **eld,**
which all switches do **use in making ECMP forwarding decisions.**
e greatest concern with both ECMP and VLB is that if "elephant ows" are present, then the random placement of ows could lead to persistent congestion on some links while others are **underutilized. Our evaluation did not nd this to be a problem on datacenter workloads (§.). Should it occur, initial results show the VL**
agent can detect and deal with such situations with simple mechanisms, such as re-hashing to change the path of large ows when TCP detects a severe congestion event (e.g., a full window loss).

BCD

TOW
NTUXONV

![6_image_0.png](6_image_0.png)

BCD

BCD

KKK KKK LMNOPQRNS
TONUONV 

## 4.2.3 Backwards Compatibility

is section describes how a VL network handles external trafc, as well as general layer- broadcast trac.

Interaction with hosts in the Internet: 20 **of the trac handled in our cloud-computing data centers is to or from the Internet,**
so the network must be able to handle these large volumes. Since VL employs a layer- routing fabric to implement a virtual layernetwork, the external trac can directly ow across the highspeed silicon of the switches that make up VL, without being **forced**
through gateway servers to have their headers rewritten, asrequired by some designs (e.g., Monsoon []).

Servers that need to be directly reachable from the Internet(e.g.,
front-end web servers) are assigned two addresses: an LA in addition to the AA used for intra-data-center communication with backend servers. is LA is drawn from a pool that is announced via BGP and is externally reachable. Trac from the Internet can **then**
directly reach the server, and trac from the server to external destinations will exit toward the Internet from the Intermediate **switches,**
while being spread across the egress links by ECMP.

Handling Broadcast: **VL provides layer- semantics to applications for backwards compatibility, and that includes supporting**
broadcast and multicast. VL completely eliminates the most common sources of broadcast: ARP and DHCP. ARP is replaced by the directory system, and DHCP messages are intercepted at the ToR using conventional DHCP relay agents and unicast forwarded to DHCP servers. To handle other general layer- broadcast trac, every service is assigned an IP multicast address, and all broadcast trac in that service is handled via IP multicast using the servicespecic multicast address. e VL agent rate-limits broadcast trafc to prevent storms.

## 4.3 Maintaining Host Information Using The Vl2 Directory System

e VL directory provides three key functions: ()lookups and
() updates **for AA-to-LA mappings; and () a reactive cache update** mechanism so that latency-sensitive updates (e.g., updating the AA to LA mapping for a virtual machine undergoing live migration)
happen quickly. Our design goals are to provide scalability, reliability and high performance.

## 4.3.1 Characterizing Requirements

We expect the lookup workload for the directory system to be frequent and bursty. As discussed in Section **., servers can communicate with up to hundreds of other servers in a short time period**
with each ow generating a lookup for an AA-to-LA mapping. For updates, the workload is driven by failures and server startup events. As discussed in Section **., most failures are small in size and large** correlated failures are rare.

Performance requirements: e bursty nature of workload implies that lookups require high throughput and low response **time.**
Hence, we choose  ms as the maximum acceptable response time.

For updates, however, the key requirement is reliability, and response time is less critical. Further, for updates that are scheduled ahead of time, as is typical of planned outages and upgrades, **high**
throughput can be achieved by batching updates.

Consistency requirements**: Conventional L networks provide**
eventual consistency for the IP to MAC address mapping, as hosts will use a stale MAC address to send packets until the ARP cache times out and a new ARP request is sent. VL aims for a similar goal, eventual consistency of AA-to-LA mappings coupled with a reliable update mechanism.

## 4.3.2 Directory System Design

e diering performance requirements and workload patterns of lookups and updates led us to a two-tiered directory system architecture. Our design consists of () a modest number (-
servers for K servers) of read-optimized, replicated **directory** servers**that cache AA-to-LA mappings and handle queriesfrom VL** agents, and () a small number (- servers) of write-optimized, asynchronous replicated state machine (RSM) servers **that oer a**
strongly consistent, reliable store of AA-to-LA mappings. **e directory servers ensure low latency, high throughput, and high availability for a high lookup rate. Meanwhile, the RSM servers ensure**
strong consistency and durability, using the Paxos [] consensus algorithm, for a modest rate of updates.

Each directory server caches all the AA-to-LA mappings stored at the RSM servers and independently replies to lookupsfrom **agents**
using the cached state. Since strong consistency is not required, a directory server lazily synchronizes its local mappings with the RSM
every  seconds. To achieve high availability and low latency, an agent sends a lookup to k **(two in our prototype) randomly-chosen**
directory servers. If multiple replies are received, the agent simply chooses the fastest reply and stores it in its cache.

e network provisioning system sends directory updates to a randomly-chosen directory server, which then forwards the **update**
to a RSM server. e RSM reliably replicates the update to every RSM server and then replies with an acknowledgment to the directory server, which in turn forwards the acknowledgment back **to the**
originating client. As an optimization to enhance consistency, the directory server can optionally disseminate the acknowledged updates to a few other directory servers. If the originating client does not receive an acknowledgment within a timeout (e.g., s), the client sends the same update to another directory server, trading response time for reliability and availability.

Updating caches reactively**: Since AA-to-LA mappings are**
cached at directory servers and in VL agents' caches, an update can lead to inconsistency. To resolve inconsistency without wasting server and network resources, our design employs a reactive cacheupdate mechanism. e cache-update protocol leverages this **observation: a stale host mapping needs to be corrected only when that**
mapping is used to deliver trac. Specically, when a stale mapping is used, some packets arrive at a stale LA—a ToR which does not host the destination server anymore. e ToR may forward a sample of such non-deliverable packets to a directory server, triggering the directory server to gratuitously correct the stale mapping in the source's cache via unicast.

## 5. Evaluation

In this section we evaluate VL using a prototype running on an  server testbed and  commodity switches (Figure **). Our** goals are rst to show that VL can be built from components that are available today, and second, that our implementation meets the objectives described in Section .

Figure : VL testbed comprising  servers and  switches.

![7_image_0.png](7_image_0.png)

e testbed is built using the Clos network topology of Figure **, consisting of  Intermediate switches,  Aggregation switches**
and  ToRs. e Aggregation and Intermediate switches have Gbps Ethernet ports, of which  ports are used on each Aggregation switch and  ports on each Intermediate switch. e ToRs switches have  Gbps ports and  Gbps ports. Each ToR is connected to two Aggregation switches via Gbps links, and to servers via Gbps links. Internally, the switches use commodity ASICs - the Broadcom  and  - although any switch that supports line rate L forwarding, OSPF, ECMP, and IPinIP decapsulation will work. To enable detailed analysis of the TCP behavior seen during experiments, the servers' kernels are instrumented to log TCP extended statistics [] (e.g., congestion window (cwnd) and smoothed RTT) a
er each socket buer is sent (typically KB in our experiments). is logging only marginally aects **goodput**, i.e., useful information delivered per second to the application layer.

We rst investigate VL's ability to provide high and uniform network bandwidth between servers. en, we analyze performance isolation and fairness between trac ows, measure convergence a
er link failures, and nally, quantify the performance of **address**
resolution. Overall, our evaluation shows that VL provides an effective substrate for a scalable data center network; VL achieves ()
 optimal network capacity, () a TCP fairness index of ., ()
graceful degradation under failures with fast reconvergence, and ()
K lookups/sec under ms for fast address resolution.

## 5.1 Vl2 Provides Uniform High Capacity

A central objective of VL is uniform high capacity between any two servers in the data center. How closely does the performance and eciency of a VL network match that of a Layer  switch with : over-subscription?

To answer this question, we consider an all-to-all **data shue**
stress test: all servers simultaneously initiate TCP transfers to all other servers. is data shue pattern arises in large scale sorts, merges and join operations in the data center. We chose this test because, in our interactions with application developers, **we learned** that many use such operations with caution, because the operations are highly expensive in today's data center network. However, data shues are required, and, if data shues can be eciently supported, it could have large impact on the overall algorithmic and data storage strategy.

We create an all-to-all data shue trac matrix involving servers. Each of  servers must deliver MB of data to each of the  other servers - a shue of . TB from memory to memory.

Figure  **shows how the sum of the goodput over all ows varies**
with time during a typical run of the . TB data shue. All data is carried over TCP connections, all of which attempt to connect be-

![7_image_1.png](7_image_1.png)

Figure : Aggregate goodput during a .TB shue among servers.
ginning at time  (some ows start late due to a bug in our trac generator). VL completes the shue in  s. During the run, the sustained utilization of the core links in the Clos network is about . For the majority of the run, VL achieves an aggregate goodput of . Gbps. e goodput is evenly divided among the ows for most of the run, with a fairness index between the ows of . [], where . indicates perfect fairness (mean goodput per ow . Mbps, standard deviation . Mbps). is goodput is more than x what the network in our current data centers can achieve with the same investment (see §).

How close is VL to the maximum achievable throughput in this environment? **To answer this question, we compute the goodput ef-**
ciency for this data transfer. e goodput eciency of the network for any interval of time is dened as the ratio of the sent goodput summed over all interfaces divided by the sum of the interface capacities. An eciency of 1 **would mean that all the capacity on all**
the interfaces is entirely used carrying useful bytes from the time the rst ow starts to when the last ow ends.

To calculate the goodput eciency, two sources of ineciency must be accounted for. First, to achieve a performance eciency of 1, the server network interface cards must be completely fullduplex: able to both send and receive  Gbps simultaneously. **Measurements show our interfaces are able to support a sustained rate**
of . Gbps (summing the sent and received capacity), introducing an ineciency of 1 −
1.8 2 = 10%**. e source of this ineciency is**
largely the device driver implementation. Second, for every two fullsize data packets there is a TCP ACK, and these three frames have B of unavoidable overhead from Ethernet, IP and TCP headers for every  B sent over the network. is results in an ineciency of . erefore, our current testbed has an intrinsic ineciency of resulting in a maximum achievable goodput for our testbed of
(75∗.83) = 62.3 **Gbps. We derive this number by noting that every**
unit of trac has to sink at a server, of which there are  instances and each has a Gbps link. Taking this into consideration, the VL
network sustains an eciency of 58.8/62.3 = 94% **with the difference from perfect due to the encapsulation headers (.), TCP**
congestion control dynamics, and TCP retransmissions.

To put this number in perspective, we note that a conventional hierarchical design with  servers per rack and : **oversubscription at the rst level switch would take x longer to shuf-**
e the same amount of data as trac from each server not in the rack () to each server within the rack () needs to ow through the Gbps downlink from rst level switch to the ToR switch.

e  eciency combined with the fairness index of .

demonstrates that VL promises to achieve uniform high bandwidth across all servers in the data center.

## 5.2 Vl2 Provides Vlb Fairness

Due to its use of an anycast address on the intermediate switches, VL relies on ECMP to split trac in equal ratios among the intermediate switches. Because ECMP does ow-level splitting, coexisting elephant and mice ows might be split unevenly at **small**
time scales. To evaluate the eectiveness of VL's implementation

![8_image_0.png](8_image_0.png)

Figure : Fairness measures how evenly ows are split to intermediate switches from aggregation switches.
of Valiant Load Balancing in splitting trac evenly across the network, we created an experiment on our -node testbed with trac characteristics extracted from the DC workload of Section **. Each**
server initially picks a value from the distribution of number of concurrent ows and maintains this number of ows throughout the experiment. At the start, or a
er a ow completes, it picks a new ow size from the associated distribution and starts the ow(s). Because all ows pass through the Aggregation switches, it is sucient to check at each Aggregation switch for the split ratio among the links to the Intermediate switches. We do so by collecting SNMP
counters at  second intervals for all links from Aggregation to Intermediate switches.

Before proceeding further, we note that, unlike the eciency experiment above, the trac mix here is indicative of actual **data**
center workload. We mimic the ow size distribution and the number of concurrent ows observed by measurements in §.

In Figure **, for each Aggregation switch, we plot Jain's fairness index [] for the trac to Intermediate switches as a time series. e average utilization of links was between  and . As**
shown in the gure, the VLB split ratio fairness index averages more than . for all Aggregation switches over the duration of this experiment. VL achieves such high fairness because there are **enough**
ows at the Aggregation switches that randomization benets from statistical multiplexing. is evaluation validates that our implementation of VLB is an eective mechanism for preventing hotspots in a data center network.

Our randomization-based trac splitting in Valiant Load Balancing takes advantage of the 10**x gap in speed between server line**
cards and core network links. If the core network were built out of links with the same speed as the server line cards, then only one fullrate ow will t on each link, and the spreading of ows has to be perfect in order to prevent two long-lived ows from traversing the same link and causing congestion. However, splitting at a sub-ow granularity (for example, owlet switching []) might alleviate this problem.

## 5.3 Vl2 Provides Performance Isolation

One of the primary objectives of VL is agility**, which we dene**
as the ability to assign any server, anywhere in the data center, to any service (§). Achieving agility critically depends on providing sufcient performance isolation between services so that if one service comes under attack or a bug causes it to spray packets, it does not adversely impact the performance of other services.

Performance isolation in VL rests on the mathematics of VLB
- that any trac matrix that obeys the hose model is routed by splitting to intermediate nodes in equal ratios (through randomization)
to prevent any persistent hot spots. Rather than have VL perform admission control or rate shaping to ensure the trac oered **to the**
network conforms to the hose model, we instead rely on TCP to ensure that each ow oered to the network is rate-limited to its fair share of its bottleneck.

![8_image_1.png](8_image_1.png)

Figure : Aggregate goodput of two services with servers intermingled on the ToRs. Service one's goodput is unaected as service two ramps trac up and down.

![8_image_2.png](8_image_2.png)

Figure : Aggregate goodput of service one as service two creates bursts containing successively more short TCP connections.
A key question we need to validate for performance isolation is whether TCP reacts suciently quickly to control the oered **rate**
of ows within services. TCP works with packets and adjusts their sending rate at the time-scale of RTTs. Conformance to the hose model, however, requires instantaneous feedback to avoid oversubscription of trac ingress/egress bounds. Our next set of experiments shows that TCP is "fast enough" to enforce the hose model for trac in each service so as to provide the desired performance isolation across services.

In this experiment, we add two services to the network. e rst service has  servers allocated to it and each server starts **a single** TCP transfer to one other server at time  and these ows last for the duration of the experiment. e second service starts with one server at  seconds and a new server is assigned to it every  seconds for a total of  servers. Every server in service two starts an GB transfer over TCP as soon as it starts up. Both the services' servers are intermingled among the  ToRs to demonstrate agile assignment of servers.

Figure  **shows the aggregate goodput of both services as a**
function of time. As seen in the gure, there is no perceptible change to the aggregate goodput of service one as the ows in service two start or complete, demonstrating performance isolation when the trac consists of large long-lived ows. rough extended TCP
statistics, we inspected the congestion window size (cwnd) **of service one's TCP ows, and found that the ows uctuate around their**
fair share briey due to service two's activity but stabilize quickly.

We would expect that a service sending unlimited rates of UDP
trac might violate the hose model and hence performance isolation. We do not observe such UDP trac in our data centers, although techniques such as STCP to make UDP "TCP friendly" are well known if needed []. However, large numbers of short TCP connections (mice), which are common in DCs (Section **), have the**
potential to cause problems similar to UDP as each ow can transmit small bursts of packets during slow start.

To evaluate this aspect, we conduct a second experiment with service one sending long-lived TCP ows, as in experiment one. Servers in service two create bursts of short TCP connections ( to KB), each burst containing progressively more connections. Figure  **shows the aggregate goodput of service one's ows along with**
the total number of TCP connections created by service two. Again,

![9_image_0.png](9_image_0.png)

Figure : Aggregate goodput as all links to switches Intermediate and Intermediate are unplugged in succession and then reconnected in succession. Approximate times of link manipulation marked with vertical lines. Network re-converges in < 1s a
er each failure and demonstrates graceful degradation.
service one's goodput is unaected by service two's activity. We inspected the cwnd of service one's TCP ows and found only brief uctuations due to service two's activity.

e two experiments above demonstrate TCP's natural enforcement of the hose model combined with VLB and a network with no oversubscription is sucient to provide performance isolation between services.

## 5.4 Vl2 Convergence After Link Failures

In this section, we evaluate VL's response to a link or a switch failure, which could be caused by a physical failure or due to the routing protocol converting a link ap to a link failure. We begin an all-to-all data shue and then disconnect links between Intermediate and Aggregation switches until only one Intermediate **switch**
remains connected and the removal of one additional link would partition the network. According to our study of failures, this type of mass link failure has never occurred in our data centers, but we use it as an illustrative stress test.

Figure  **shows a time series of the aggregate goodput achieved**
by the ows in the data shue, with the times at which links were disconnected and then reconnected marked by vertical lines. e gure shows that OSPF re-converges quickly (sub-second) a
er each failure. Both Valiant Load Balancing and ECMP work as expected, and the maximum capacity of the network gracefully degrades. Restoration, however, is delayed by the conservative defaults for OSPF timers that are slow to act on link restoration. Hence, VL fully uses a link roughly s a
er it is restored. We note, however, that restoration does not interfere with trac and, the aggregate goodput eventually returns to its previous level.

is experiment also demonstrates the behavior of VL when the network is structurally oversubscribed,i.e., the Clos **network has**
less capacity than the capacity of the links from the ToRs. For the over-subscription ratios between : and : created during this experiment, VL continues to carry the all-to-all trac at roughly of maximum eciency, indicating that the trac spreading in VL fully utilizes the available capacity.

## 5.5 Directory-System Performance

Finally, we evaluate the performance of the VL directory system through macro- and micro-benchmark experiments. We run our prototype on up to  machines with - RSM nodes, - directory server nodes, and the rest emulating multiple instances of VL agents that generate lookups and updates. In all experiments, the system is congured such that an agent sends a lookup request to two directory servers chosen at random and accepts the rst response. An update request is sent to a directory server chosen at random. e response timeout for lookups and updates is set to s to measure the worst-case latency. To stress test the directory system, the VL agent instances generate lookups and updates following a bursty random process, emulating storms of lookups and updates. Each directory server refreshes all mappings (K) from the RSM
once every  seconds.

Our evaluation supports four main conclusions. First, the directory system provides high throughput and fast response time for lookups; three directory servers can handle K lookups/sec with latency under ms (th percentile latency). Second, the directory system can handle updates at rates signicantly higherthan expected churn rate in typical environments: three directory **servers**
can handle K updates/sec within ms (th **percentile latency).**
ird, our system is incrementally scalable; each directory **server** increases the processing rate by about K for lookups and K for updates. Finally, the directory system is robust to component (directory or RSM servers) failures and oers high availability under network churns.

roughput: **In the rst micro-benchmark, we vary the lookup and**
update rate and observe the response latencies (st, th **and** th percentile). We observe that a directory system with three directory servers handles K lookups/sec within ms, which we set as the maximum acceptable latency for an "ARP request". Up to K
lookups/sec, the system oers a median response time of < ms.

Updates, however, are more expensive, as they require executing a consensus protocol [] to ensure that all RSM replicas are mutually consistent. Since high throughput is more important than latency for updates, we batch updates over a short time interval (i.e.,
ms). We nd that three directory servers backed by three RSM
servers can handle K updates/sec within ms and about K updates/sec within s.

Scalability: **To understand the incremental scalability of the directory system, we measured the maximum lookup rates (ensuring sub-ms latency for  requests) with , , and  directory**
servers. e result conrmed that the maximum lookup rates increases linearly with the number of directory servers (with **each**
server oering a capacity of 17**K lookups/sec). Based on this result,**
we estimate the worst case number of directory servers needed for a K server data center. From the concurrent ow measurements (Figure **), we select as a baseline the median of  correspondents**
per server. In the worst case, all K servers may perform  **simultaneous lookups at the same time resulting in a million simultaneous lookups per second. As noted above, each directory server can**
handle about K lookups/sec under ms at the th **percentile.**
erefore, handling this worst case requires a modest-sized directory system of about  servers (0.06 **of the entire servers).**
Resilience and availability: **We examine the eect of directory** server failures on latency. We vary the number of directory servers while keeping the workload constant at a rate of K lookups/sec and K updates/sec (a higher load than expected for three directory servers). In Figure **(a), the lines for one directory server show that**
it can handle  of the lookup load (K) within ms. e spike at two seconds is due to the timeout value of s in our prototype. e entire load is handled by two directory servers, demonstrating the system's fault tolerance. Additionally, the lossy network **curve shows** the latency of three directory servers under severe () packet losses between directory servers and clients (either requests or responses), showing the system ensures availability under network churns. For updates, however, the performance impact of the number of directory servers is higher than updates because each **update**
is sent to a single directory server to ensure correctness. Figure (b) shows that failures of individual directory servers do not collapse the entire system's processing capacity to handle updates. **e step**
pattern on the curves is due to a batching of updates (occurring every ms). We also nd that the primary RSM server's failure leads

![10_image_0.png](10_image_0.png)

ïêé ïéêé ïééêé ïéééêé ÿ
Figure : e directory system provides high throughput and **fast response time for lookups and updates**
to only about s delay for updates until a new primary is elected, while a primary's recovery or non-primary's failures/recoveries do not aect the update latency at all.

Fast reconvergence and robustness: **Finally, we evaluate the**
convergence latency of updates, i.e., the time between when an update occurs until a lookup response reects that update. As described in Section **., we minimize convergence latency by having each directory server pro-actively send its committed updates**
to other directory servers. Figure **(c) shows that the convergence** latency is within ms for  of the updates and  of updates have convergence latency within  ms.

## 6. Discussion

In this section, we address several remaining concerns about the VL architecture, including whether other trac engineering mechanisms might be better suited to the data center than Valiant Load Balancing, and the cost of a VL network.

Optimality of VLB: **As noted in §.., VLB uses randomization to cope with volatility, potentially sacricing some performance**
for a best-case trac pattern by turning all trac patterns (including both best-case and worst-case) into the average case. is performance loss will manifest itself as the utilization of some links being higher than they would under a more optimal trac engineering system. To quantify the increase in link utilization VLB will suer, we compare VLB's maximum link utilization with that achieved by other routing strategies on the VL topology for a full day's **trac**
matrices (TMs) (at min intervals) from the data center trac data reported in Section ..

We rst compare to adaptive routing **(e.g., TeXCP []), which**
routes each TM separately so as to minimize the maximum link utilization for that TM - essentially upper-bounding the best performance that real-time adaptive trac engineering could achieve.

Second, we compare to best oblivious routing **over all TMs so as to** minimize the maximum link utilization. (Note that VLB is just one among many oblivious routing strategies.) For adaptive and **best**
oblivious routing, the routings are computed using linear programs in cplex**. e overall utilization for a link in all schemes is computed as the maximum utilization over all routed TMs.**
In Figure **, we plot the CDF for link utilizations for the three**
schemes. We normalized the link utilization numbers so that the maximum utilization on any link for adaptive routing is 1.0. e results show that for the median utilization link in each scheme, VLB performs about the same as the other two schemes. For the most heavily loaded link in each scheme, VLB's link capacity **usage**
is about  higher than that of the other two schemes. us, evaluations on actual data center workloads show that the simplicity and universality of VLB costs relatively little capacity when compared to much more complex trac engineering schemes.

Cost and Scale: **With the range of low-cost commodity devices**
currently available, the VL topology can scale to create networks

![10_image_1.png](10_image_1.png) 

!"#$%&"'"()&"*#+ ,-*./)'"(012
Figure : CDF of normalized link utilizations for VLB, adaptive, and best oblivious routing schemes, showing that VLB (and best oblivious routing) comes close to matching the link utilization performance of adaptive routing.
with no over-subscription between all the servers of even the largest data centers. For example, switches with  ports (D = 144**) are**
available today for K, enabling a network that connects K
servers using the topology in Figure  **and up to K servers using a slight variation. Using switches with** D = 24 **ports (which**
are available today for K each), we can connect about K servers.

Comparing the cost of a VL network for K servers with a typical one found in our data centers shows that a VL network with no over-subscription can be built for the same cost as the current network that has : over-subscription. Building a conventional network with no over-subscription would cost roughly x the cost of a equivalent VL network with no over-subscription. We nd the same factor of - cost dierence holds across a range of over-subscription ratios from : to :. (We use street prices for switches in both architectures and leave out ToR and cabling **costs.)** Building an oversubscribed VL network does save money (e.g., a VL network with : over-subscription costs  less than **a nonoversubscribed VL network), but the savings is probably not worth**
the loss in performance.

## 7. Related Work

Data-center network designs: **Monsoon [] and Fat-tree []**
also propose building a data center network using commodity **switches and a Clos topology. Monsoon is designed on top of layer**
 and reinvents fault-tolerant routing mechanisms already **established at layer . Fat-tree relies on a customized routing primitive**
that does not yet exist in commodity switches. VL, in contrast, achieves hot-spot-free routing and scalable layer- semantics using forwarding primitives available today and minor, applicationcompatible modications to host operating systems. Further, our experiments using trac patterns from a real data center show that random ow spreading leads to a network utilization fairly close to the optimum, obviating the need for a complicated and expensive optimization scheme suggested by Fat-tree. We cannot empirically compare with these approaches because they do not provide results on communication-intensive operations (e.g., data shue) that stress the network; they require special hardware []; and they do not support agility and performance isolation.

DCell [] proposes a dense interconnection network built by adding multiple network interfaces to servers and having the servers forward packets. VL also leverages the programmability of **servers,** however, it uses servers only to control the way trac is routed as switch ASICs are much better at forwarding. Furthermore, DCell incurs signicant cabling complexity that may prevent large deployments. BCube [] builds on DCell, incorporating switches for faster processing and active probing for load-spreading.

Valiant Load Balancing: **Valiant introduced VLB as a randomized scheme for communication among parallel processors interconnected in a hypercube topology []. Among its recent applications, VLB has been used inside the switching fabric of a packet**
switch []. VLB has also been proposed, with modications and generalizations [, **], for oblivious routing of variable trac on**
the Internet under the hose trac model [].

Scalable routing: **e Locator/ID Separation Protocol [] proposes "map-and-encap" as a key principle to achieve scalability and**
mobility in Internet routing. VL's control-plane takes a similar approach (i.e., demand-driven host-information resolution and caching) but adapted to the data center environment and implemented on end hosts. SEATTLE [] proposes a distributed hostinformation resolution system running on switches to enhance Ethernet's scalability. VL takes an end host based approach to **this**
problem, which allows its solution to be implemented today, **independent of the switches being used. Furthermore, SEATTLE**
does not provide scalable data plane primitives, such as multi-path, which are critical for scalability and increasing utilization of network resources.

Commercial Networks: **Data Center Ethernet (DCE) [] by**
Cisco and other switch manufacturers shares VL's goal of increasing network capacity through multi-path. However, these industry eorts are primarily focused on consolidation of IP and storage area network (SAN) trac, which is rare in cloud-service data centers. Due to the requirement to support loss-less trac, their switches need much bigger buers (tens of MBs) than commodity Ethernet switches do (tens of KBs), hence driving their cost higher.

## 8. Summary

VL is a new network architecture that puts an end to the need for oversubscription in the data center network, a result that would be prohibitively expensive with the existing architecture.

VL benets the cloud service programmer. Today, programmers have to be aware of network bandwidth constraints and constrain server to server communications accordingly. VL instead provides programmers the simpler abstraction that all servers assigned to them are plugged into a single layer  switch, with hotspot free performance regardless of where the servers are actually connected in the topology. VL also benets the data center operator as today's bandwidth and control plane constraints fragment the server pool, leaving servers (which account for the lion's share of data center cost) under-utilized even while demand elsewhere in the **data**
center is unmet. Instead, VL enables agility: any service can be assigned to any server, while the network maintains uniform **high** bandwidth and performance isolation between services.

VL is a simple design that can be realized today with available networking technologies, and without changes to switch control and data plane capabilities. e key enablers are an addition to the endsystem networking stack, through well-established and public APIs, and a at addressing scheme, supported by a directory service.

VL is ecient. Our working prototype, built using commodity switches, approaches in practice the high level of performance that the theory predicts. Experiments with two data-centerservices showed that churn (e.g., dynamic re-provisioning of servers, change of link capacity, and micro-bursts of ows) has little impact on TCP goodput. VL's implementation of Valiant Load Balancing splits ows evenly and VL achieves high TCP fairness. On all-to-all data shue communications, the prototype sustains an eciency of with a TCP fairness index of ..

## Acknowledgements

e many comments from our shepherd David Andersen and the anonymous reviewers greatly improved the nal version of this paper. John Dunagan provided invaluable help implementing the Directory System.

## 9. References

[] M. Al-Fares, A. Loukissas, and A. Vahdat. A scalable, commodity data center network architecture. In SIGCOMM, .

[] M. Armbrust, A. Fox, R. Grith, et al. **Above the Clouds: A**
Berkeley View of Cloud Computing UC Berkeley TR UCB/EECS--.

[] C. Chang, D. Lee, and Y. Jou. Load balanced Birkho-von Neumann switches, part I: one-stage buering. IEEE HPSR, .

[] Cisco. Data center Ethernet. http://www.cisco.com/go/dce. [] Cisco: Data center: Load balancing data center services, . [] K. C. Clay, H. werner Braun, and G. C. Polyzos. A parameterizable methodology for Internet trac ow proling. JSAC**, , .**
[] W. J. Dally and B. Towles. **Principles and Practices of Interconnection**
Networks**. Morgan Kaufmann Publishers, .**
[] N. G. Dueld, P. Goyal, A. G. Greenberg, P. P. Mishra, K. K.

Ramakrishnan, and J. E. van der Merwe. A exible model for resource management in virtual private network. In **SIGCOMM**, .

[] D. Farinacci, V. Fuller, D. Oran, D. Meyer, and S. Brim. Locator/ID
Separation Protocol (LISP). Internet-dra
, Dec. .

[] A. Greenberg, J. R. Hamilton, D. A. Maltz, P. Patel. e cost of a cloud: research problems in data center networks CCR**, (), .**
[] A. Greenberg, P. Lahiri, D. A. Maltz, P. Patel, and S. Sengupta.

Towards a next generation data center architecture: Scalability and commoditization. In PRESTO Workshop at SIGCOMM, .

[] C. Guo, H. Wu, K. Tan, L. Shiy, Y. Zhang, and S. Lu. Dcell: A
scalable and fault-tolerant network structure for data centers. In SIGCOMM, .

[] C. Guo, H. Wu, K. Tan, L. Shiy, Y. Zhang, and S. Lu. Bcube: A **high**
performance, server-centric network architecture for modular data centers. In SIGCOMM, .

[] M. Handley, S. Floyd, J. Padhye, and J. Widmer. TCP friendly rate control (TFRC): Protocol specication. RFC , .

[] R. Jain. e Art of Computer Systems Performance Analysis**. John**
Wiley and Sons, Inc., .

[] S. Kandula, D. Katabi, B. Davie, and A. Charny. Walking the Tightrope: Responsive yet Stable Trac Engineering. In SIGCOMM, .

[] C. Kim, M. Caesar, and J. Rexford. Floodless in SEATTLE: **a scalable**
ethernet architecture for large enterprises. In SIGCOMM, .

[] M. Kodialam, T. V. Lakshman, and S. Sengupta. Ecient and Robust Routing of Highly Variable Trac. In HotNets, .

[] L. Lamport. e part-time parliament. **ACM Transactions on**
Computer Systems**, :–, .**
[] M. Mathis, J. Hener, and R. Raghunarayan. TCP extended statistics MIB. RFC , .

[] S. Sinha, S. Kandula, and D. Katabi. Harnessing TCP's burstiness with owlet switching. In HotNets, .

[] Y. Zhang and Z. Ge. Finding critical trac matrices. In DSN**, June**
.

[] R. Zhang-Shen and N. McKeown. Designing a Predictable Internet Backbone Network. In HotNets, .