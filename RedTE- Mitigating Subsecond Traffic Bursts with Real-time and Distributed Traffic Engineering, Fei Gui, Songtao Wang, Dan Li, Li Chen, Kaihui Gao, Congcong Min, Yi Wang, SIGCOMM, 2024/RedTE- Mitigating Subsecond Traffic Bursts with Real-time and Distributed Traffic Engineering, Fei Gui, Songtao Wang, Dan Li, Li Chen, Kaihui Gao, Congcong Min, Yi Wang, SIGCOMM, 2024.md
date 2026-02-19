![](_page_0_Picture_0.jpeg)

.

![](_page_0_Picture_1.jpeg)

![](_page_0_Picture_2.jpeg)

![](_page_0_Picture_3.jpeg)

![](_page_0_Picture_4.jpeg)

Latest updates: [hps://dl.acm.org/doi/10.1145/3651890.3672231](https://dl.acm.org/doi/10.1145/3651890.3672231)

RESEARCH-ARTICLE

# RedTE: Mitigating Subsecond Traffic Bursts with Real-time and Distributed Traffic Engineering

FEI [GUI](https://dl.acm.org/doi/10.1145/contrib-99661282087), Tsinghua [University,](https://dl.acm.org/doi/10.1145/institution-60025278) Beijing, China

[SONGTAO](https://dl.acm.org/doi/10.1145/contrib-99661282138) WANG, Beijing Institute of [Technology,](https://dl.acm.org/doi/10.1145/institution-60016835) Beijing, China

[DAN](https://dl.acm.org/doi/10.1145/contrib-81100476304) LI, Tsinghua [University,](https://dl.acm.org/doi/10.1145/institution-60025278) Beijing, China

LI [CHEN](https://dl.acm.org/doi/10.1145/contrib-99660555710), Beijing Institute of [Technology,](https://dl.acm.org/doi/10.1145/institution-60016835) Beijing, China

[KAIHUI](https://dl.acm.org/doi/10.1145/contrib-99660024702) GAO, Beijing Institute of [Technology,](https://dl.acm.org/doi/10.1145/institution-60016835) Beijing, China

[CONGCONG](https://dl.acm.org/doi/10.1145/contrib-99661280691) MIN, Guangdong [Communications](https://dl.acm.org/doi/10.1145/institution-60274020) & Networks Institute, Guangzhou, [Guangdong,](https://dl.acm.org/doi/10.1145/institution-60274020) China

[View](https://dl.acm.org/doi/10.1145/3651890.3672231) all

Open Access [Support](https://libraries.acm.org/acmopen) provided by:

Beijing Institute of [Technology](https://dl.acm.org/doi/10.1145/institution-60016835)

Tsinghua [University](https://dl.acm.org/doi/10.1145/institution-60025278)

Guangdong [Communications](https://dl.acm.org/doi/10.1145/institution-60274020) & Networks Institute

Southern University of Science and [Technology](https://dl.acm.org/doi/10.1145/institution-60105683)

![](_page_0_Picture_20.jpeg)

PDF Download 3651890.3672231.pdf 13 January 2026 Total Citations: 19 Total Downloads: 4024

Published: 04 August 2024

[Citation](https://dl.acm.org/action/exportCiteProcCitation?dois=10.1145%2F3651890.3672231&targetFile=custom-bibtex&format=bibtex) in BibTeX format

ACM [SIGCOMM](https://dl.acm.org/conference/comm) '24: ACM SIGCOMM 2024 [Conference](https://dl.acm.org/conference/comm)

*August 4 - 8, 2024 NSW, Sydney, Australia*

Conference Sponsors:

[SIGCOMM](https://dl.acm.org/sig/sigcomm)

# RedTE: Mitigating Subsecond Traffic Bursts with Real-time and Distributed Traffic Engineering

Fei Gui\*°, Songtao Wang<sup>‡</sup>, Dan Li\*, Li Chen<sup>‡</sup>, Kaihui Gao<sup>‡</sup>, Congcong Min<sup>†</sup>, Yi Wang<sup>\$</sup>
\*Tsinghua University <sup>‡</sup>Zhongguancun Laboratory <sup>°</sup>BNRist <sup>†</sup>Guangdong Communications & Networks Institute
<sup>\$\$</sup>Institute of Future Networks in Southern University of Science and Technology

#### **Abstract**

Internet traffic bursts usually happen within a second, thus conventional burst mitigation methods ignore the potential of Traffic Engineering (TE). However, our experiments indicate that a TE system, with a sub-second control loop latency, can effectively alleviate burst-induced congestion. TE-based methods can leverage network-wide tunnel-level information to make globally informed decisions (e.g., balancing traffic bursts among multiple paths). Our insight in reducing control loop latency is to let each router make local TE decisions, but this introduces the key challenge of minimizing performance loss compared to centralized TE systems.

In this paper, we present RedTE, a novel distributed TE system with a control loop latency of < 100ms, while achieving performance comparable to centralized TE systems. RedTE's innovation is the modeling of TE as a distributed cooperative multi-agent problem, and we design a novel multi-agent deep reinforcement learning algorithm to solve it, which enables each agent to make globally informed decisions solely based on local information. We implement real RedTE routers and deploy them on a WAN spanning six city datacenters. Evaluation reveals notable improvements compared to existing solutions: < 100ms of control loop latency, a 37.4% reduction in maximum link utilization, and a 78.9% reduction in average queue length.

#### **CCS Concepts**

 $\bullet$  Networks  $\to$  Traffic engineering algorithms;  $\bullet$  Computing methodologies  $\to$  Reinforcement learning.

#### **Keywords**

Traffic Engineering, Network Optimization, Machine Learning

#### **ACM Reference Format:**

Fei Gui, Songtao Wang, Dan Li, Li Chen, Kaihui Gao, Congcong Min, Yi Wang. 2024. RedTE: Mitigating Subsecond Traffic Bursts with Real-time and Distributed Traffic Engineering. In ACM SIGCOMM 2024 Conference (ACM SIGCOMM '24), August 4–8, 2024, Sydney, NSW, Australia. ACM, New York, NY, USA, 15 pages. https://doi.org/10.1145/3651890.3672231

#### 1 Introduction

Internet traffic is known to be bursty [19, 29, 33], and it can lead to long tail latency or even packet loss for users. Mitigating the

![](_page_1_Picture_13.jpeg)

This work is licensed under a Creative Commons Attribution International 4.0 License. ACM SIGCOMM '24, August 4–8, 2024, Sydney, NSW, Australia © 2024 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-0614-1/24/08 https://doi.org/10.1145/3651890.3672231 burstiness of Internet traffic in a cost-efficient manner is a priority for Internet service providers (ISPs). To reduce the occurrence of bursts, ISPs typically overprovision the bandwidth of their wide area networks (WANs), which significantly increases their costs, because the common practice is to double the capacity when the average utilization is greater than 50% [15]. The strategy is coarsegrained and inflexible.

Mitigating bursty traffic in the WAN can improve user experience and reduce capital expenses. However, it is challenging because traffic bursts are unpredictable and instantaneous (a burst typically lasts milliseconds). Conventional burst mitigation methods are either source-based or router-based. The former attempts to prevent bursts at the source, such as in end-host applications [39] or in the transport layer [9, 14, 32], and thus these methods cannot be enforced by ISPs. The latter uses traffic managers [1, 3] to perform dynamic load balancing within a router. They mitigate bursts with only local information, and thus encounter difficulties in achieving network-wide performance goals.

In contrast, traffic engineering (TE) mechanisms usually have global information when making a decision, but are ignored as potential mitigation methods for traffic bursts. This is because current TE controllers are typically centralized [8, 42, 45, 53], and operate on a much larger timescale (minutes or hours) than traffic bursts (hundreds of milliseconds). However, we believe that TE is uniquely equipped to handle bursts for WANs. A TE-based burst mitigation approach can leverage tunnel-level information at global scale and make informed decisions on all devices. This approach has the potential to address temporary congestion in a more fundamental manner while remaining transparent to the upper layers, and thus is more friendly for ISP deployments.

Can TE help to mitigate traffic bursts? We perform extensive experiments (§2.2) to confirm this. The results show that this approach is crucially dependent on the decision-making speed of the TE controller. If the control loop latency of the TE system is less than one second, the maximum link utilization (MLU) of the network can be reduced by 39.0% to 47.8%, greatly reducing the possibility of temporary congestion due to bursts. We conclude that, to be effective, the TE control loop latency—information collection, computation, and decision deployment—must be close to the time scale of traffic bursts.

Reducing the latency of TE systems is challenging. We find that although there have been continuous efforts to accelerate the TE system, all current TE systems have control loop latency in seconds or minutes [8, 42, 45, 53]. This is because, even if we can reduce the centralized computation time, much time is still spent waiting for information collection from remote routers and deploying TE decisions to remote routers. To effectively mitigate bursts using TE, we believe that routers need to make TE decisions solely based

<span id="page-2-1"></span>![](_page_2_Figure_2.jpeg)

Figure 1: The control loop of a TE controller.

on local information—a practice known as distributed TE (dTE). However, we find that existing dTE solutions [16, 30, 40] cannot mitigate traffic bursts. dTE solutions suffer from the slow multiround adjustment process to converge, and the convergence time is at least seconds.

The goal of this paper is to reduce the control loop latency while maintaining performance comparable to centralized TE systems. Our key insight is that, without access to up-to-date global information, a router can still learn from past experience and attempt to make the best decision with locally available information. Past experience includes locally measured traffic statistics, the history of past decisions of a centralized controller, and the historical contexts in which the decisions were made. In other words, if a similar situation has happened before, the routers can learn from past experience to approximate optimal TE decisions.

This motivates us to model dTE as a cooperative multi-agent system (CMAS) [18], and following this model, this paper presents the design and implementation of a Real-time dTE (RedTE), which is a novel dTE system with a control loop latency of less than 100ms, while achieving network performance comparable to centralized TE systems. With RedTE, we make the following contributions:

- We find that the control loop latency is the key factor in applying TE to burst mitigation. Our experiments demonstrate that reducing latency from 25s to 50ms results in a significant improvement in the practical performance of TE systems (a reduction of 47.8% in MLU).
- We model TE as a CMAS problem and solve it with a novel multiagent deep reinforcement learning algorithm. Specifically, we present a training technique called circular traffic matrix (TM) replay, which reduces the convergence time of agents' neural networks by up to 61.2%. For a WAN with 754 routers, the training job can be completed in about half a day on only an NVIDIA A6000 GPU.
- We implement RedTE, which includes a centralized training system and RedTE routers that are built on P4-capable switch platforms. We make several optimizations to further reduce control loop latency, such as an efficient data collection mechanism and a fine-grained rule table update technique that prevents up to 87.2% unnecessary table entry updates.
- We deploy the RedTE routers on a real WAN testbed that spans 6 datacenters in 6 cities. Furthermore, we evaluate RedTE on a large-scale WAN with 754 routers using NS3 simulations. Evaluation results reveal notable improvements compared to existing solutions: less than 100ms control loop latency, a 37.4% reduction in MLU, and a 78.9% reduction in the average queue length. We also demonstrate that RedTE is robust to network failures.

This work does not raise any ethical issues.

## 2 Background

In this section, we first describe how to mitigate bursty traffic by traditional methods and TE. Then we analyze the limitations of current TE methods, which motivates our design.

## 2.1 Bursty Traffic and Mitigation Mechanisms

The sending rate of a flow may increase sharply due to many factors, such as application's bursty nature, TCP self-clocking as well as the batch operation of the network stack [29, 43]. When multiple bursty flows compete for a path (or a link) due to load imbalance, which will cause a violent burst in the network [19, 29, 33], and its time scale is very short (e.g., 10-100s of milliseconds). Bursty traffic causes queue buildup in routers [50], and can easily hurt delaysensitive applications [22, 49], such as high frequency trading [43], VR/AR, etc.

There exist two types of traditional burst mitigation mechanisms: end-host mechanisms and device-local traffic managers, but both of them are not effective for ISPs [34]. End-host mechanisms work in the transport or application layers, such as BBR [14], QUIC [32] and DCTCP [9]. They resort to adjusting the sending rate for end hosts in advance before path congestion. Device-local traffic managers [1, 3] can distribute traffic among multiple paths to prevent links from being heavily loaded. However, they are not aware of global traffic patterns and can be stuck at a local optimum. For ISPs, it is appealing to design a burst mitigation scheme with global awareness of traffic information, while being transparent to the transport and application layers. TE is uniquely equipped for this, because it works in the network layer and is able to obtain network-wide tunnel-level information.

Next, we overview the current three classes of TE methods in terms of burst mitigation, and motivate RedTE's design.

## <span id="page-2-0"></span>2.2 Existing LP-based TE Systems

The TE problem is usually formulated as a multi-commodity flow (MCF) problem [26, 27, 31], in which the input is the traffic demand  $r_{o,d}$  between every edge router pair (o,d), and the output is the fraction of traffic  $w_p$  allocated to each pre-configured path p between an (o,d) pair. The performance of a TE algorithm can be measured by the MLU under a specified traffic demand [31, 42]. The classic TE solution uses a global linear programming (LP) solver such as Gurobi[2] to calculate the optimal decision, e.g., the optimal splitting ratio of traffic among multiple pre-configured paths.

Impact of control loop latency. While the global LP algorithm exhibits strong theoretical TE performance, the control loop latency in a practical TE system cannot be ignored. As shown in Figure 1, the control loop of a TE decision includes collecting input information to make TE decisions, computation, and updating the route rule table. The global LP has control loop latency on the order of minutes, since the computation (*i.e.*, solving an LP problem) can be computationally intractable for large networks [42]. Given that traffic bursts usually occur on a millisecond time scale, a long control loop latency will significantly degrade the practical TE performance.

We conduct experiments to confirm that reducing the control loop latency of TE to the millisecond scale can lead to a sizable

<span id="page-3-0"></span>![](_page_3_Figure_2.jpeg)

Figure 2: The bursty ratio of traffic collected from a collector point on WIDE, a Japanese backbone network.

improvement in the network performance, significantly reducing the possibility of temporary congestion due to bursts.

In the experiments, we use public packet traces from WIDE [5], a major backbone network in Japan. The traffic in the traces is bursty, as shown in Figure 2. Concretely, more than 20.0% of the periods are experiencing a burst ratio greater than 200%. The burst ratio is defined as the change ratio of traffic volume between two adjacent 50ms. That not only includes the expanding ratio, but the shrink ratio on top of the previous time duration. NCFlow [8] also revealed similar bursty phenomena, but it analyzed data at the granularity of minutes, whereas our analysis focuses on a finer granularity, specifically at the millisecond level. Experiments (§6.3) indicate that bursts can cause routers to build up a queue of over 20kpackets, resulting in an end-to-end queuing delay of up to 39.2ms. Additionally, bursts can cause the network to exceed the capacity upgrade threshold (MLU >50%) in up to 82.3% of the time. Even using the state-of-the-art TE method [45, 53], the average maximal queue length is over 10k packets. Further, the end-to-end queuing delay is 21.3ms and the events where MLU exceeds the capacity upgrade threshold is 41.5% of the total.

We also conduct experiments of three scenarios in a private WAN (APW), which detail is seen in (§6.1). In Figure 3, the y-axis represents the normalized MLU, which is compared to the ideal performance (*i.e.*, the network's MLU when the control loop latency of the TE system is zero). The results indicate that when reducing the control loop latency (x) from 25s to 50ms, the effectiveness of the TE system is increased by 39.0% to 47.8%. Further, the path queuing delay is reduced by up to 75.9% and the number of events where MLU exceeds the capacity upgrade threshold is reduced by up to 38.3% (§6.3).

Tradeoff between decision-making speed and solution quality. Existing TE systems cannot achieve sub-second control loop latency. In general, they fall in different tradeoff points between solution quality and decision-making speed, as shown in Figure 4.

Specifically, POP [42] generates congruent replicas of the network topology, each possessing a proportion of the network's capacities. It subsequently allocates demands across these replicas and concatenates the solutions of each sub-problem to recover the solution for the original problem in a heuristic manner. Although the solution quality of POP is lower than that of the global LP, the improvements gained from a shorter control loop latency lead to better practical TE performance. However, POP also has significant control loop latency due to its centralized nature.

#### 2.3 Distributed TE

In prior dTE solutions [16, 30, 40], routers, constrained by their lack of access to global information, need to progressively refine

<span id="page-3-1"></span>![](_page_3_Figure_11.jpeg)

(a) Public packet trace replay on two dif-(b) Different traffic scenario on a real priferent networks. vate WAN.

Figure 3: Performance degrades with increasing control loop latency. Gurobi is used as the LP solver.

![](_page_3_Figure_14.jpeg)

Figure 4: An illustrative comparison between RedTE and prior works. RedTE maintains comparable performance with much lower control loop latency.

their operations based on feedback related to the network's state, which is influenced by the decisions of other routers. The multi-step convergence is slow and costs at least seconds, resulting in a longer control loop latency than POP.

#### 2.4 Existing ML-based TE Systems

Reinforcement learning (RL) has shown potential in making decisions in complex and uncertain systems. And deep learning provides an end-to-end learning paradigm, obviating the need for feature engineering. They have led to increased attention in recent years regarding its application to TE. Despite significant progress, we identify two main problems with existing machine learning-based TE solutions.

**1. The learning instability problem.** TE can be modeled as a CMAS task. If each agent is cooperatively trained using deep reinforcement learning (DRL) (*e.g.*, multi-agent reinforcement learning (MARL) [25]), an agent can make optimal global decisions with locally available information, through a learning procedure using past experience. That means routers can approximate the best TE action based on a similar scenario happening in training.

However, in practical deployments, we find that the learning instability problem can cause agents to not cooperate. The reason is that existing MARL algorithms cannot accurately evaluate the contribution of an agent's action to the global goal, e.g., minimizing the MLU of the entire network. For example, DATE [24] uses a straightforward combination of global reward (with the MLU of the global network) and local reward (with MLU in candidate paths) to train each router, but the two goals may conflict. In other words, it may encourage individual agents to sacrifice the global goal for the local goal, leading to the opposite of global cooperation. It remains an open question to design a MARL algorithm that enables all routers to cooperate.

2. Ignoring the latencies of information collection and rule table update. The computation process in machine learning has

two phases, namely, the model training phase and the model inference phase. Although the model training is time-consuming, it is carried out offline. By contrast, the model inference in the TE control loop is very fast. For example, in DOTE [\[45\]](#page-13-12) and TEAL [\[53\]](#page-14-0), a central controller not only trains the model but also infers the model online. Compared with global LP, model inference significantly reduces the computation time of the algorithm. However, with the reduction of the algorithm computation time, the other two stages (i.e., input information collection and the rule table updating) become the new bottleneck (>83% in our evaluation).

Motivations for RedTE. These problems are crucial to our goal of achieving low control loop latency and high TE performance. To address them, our idea is to model TE as a CMAS problem and tackle it using a novel multi-agent deep reinforcement learning algorithm. Before RedTE, TEAL [\[53\]](#page-14-0) has already applied MARL into TE. However, TEAL still uses MARL to tackle centralized TE whereas RedTE targets distributed TE. Moreover, RedTE introduces a novel circular traffic replay mechanism to overcome the challenges associated with training convergence, a common issue when directly applying traditional RL techniques to TE scenarios. We opt for RL over imitation Learning (IL) [\[11\]](#page-13-28), because IL requires expert demonstrations of desired behavior, but for our task of improving both solution quality and rule table updating speed, desired demonstrations are not available. In contrast, RL can learn with only feedback from the environment, and does not need labeled data.

RedTE advances dTE because RedTE introduces a global critic network [\[18,](#page-13-16) [37\]](#page-13-29) during training to distinguish the contribution of each agent to the global reward, enabling them to cooperate to achieve performance comparable to centralized TE with no need for the multi-iteration converge. The critic network is only used during training, while the agent's neural network is solely needed during TE execution. RedTE is superior to previous ML-based TE methods because RedTE optimizes the entire loop holistically to reduce latency with a novel reward function design. In contrast, other ML-based systems focus solely on the computation stage. Finally, using the P4-capable switch platform, we develop highly efficient data collection and rule table update facilities for RedTE.

# 3 Design Overview

In this section, we overview the design of RedTE.

## 3.1 Assumptions

We make three assumptions in the design of RedTE.

- We target ISPs that have control over their WAN routers, and we do not control end hosts. This means that the inputs to RedTE are traffic counters collected from the data plane of routers (§[5.2.2\)](#page-7-0).
- RedTE is orthogonal to other protocols (BGP, RSVP, etc.) in the control plane. We follow the same assumption as the prior TE systems [\[30,](#page-13-14) [42,](#page-13-11) [45,](#page-13-12) [53\]](#page-14-0) that candidate paths (tunnels) are given, so the TE system only needs to decide traffic split ratios for the candidate paths.
- RedTE assumes that for each origin-destination pair, there are candidate paths (≥1), which is true for real WAN networks [\[26,](#page-13-21) [28\]](#page-13-30) due to fault tolerance requirements. We discuss how RedTE handles failures in §[6.3.](#page-11-0)

<span id="page-4-0"></span>![](_page_4_Figure_12.jpeg)

Figure 5: Architecture of RedTE.

## 3.2 Architecture and Workflow

Figure [5](#page-4-0) shows the overall architecture of RedTE. RedTE has two types of entities, namely the RedTE routers and the RedTE controller. We describe the implementation of RedTE routers in §[6.2.](#page-9-0) RedTE routers must be deployed at the edge of the network.

RedTE router workflow. Each RedTE router continuously reports the traffic demand vector to the RedTE controller and periodically downloads the RL model from the RedTE controller. There is no interaction between the agents and the controller during the model inference phase.

Each RedTE router makes TE decisions by its unique local RL model, based on local input information. Local RL models for different RedTE routers can be different. For each RedTE router, the local input information includes the utilization of local links, the bandwidth of local links, and the current traffic demand sourced at this router and towards every edge router. The output of the RL model is the traffic splitting ratio among multiple alternate paths, which is pre-calculated based on the network topology. Tunnelbased mechanisms [\[10,](#page-13-31) [17\]](#page-13-32) can be used for intermediate routers to follow the pre-configured end-to-end paths, which guarantees that RedTE does not cause a routing loop. Deployments for traffic split decisions are required only at the edge routers, rather than at every router along the path, which avoids the transit loop.

RedTE controller workflow. Based on the historical traffic demand matrices, as well as the network topology information, the controller replays the traffic in a simulation environment and runs an RL algorithm to train the RL model for each RedTE router. The model training process runs periodically to address model degradation.

## 4 RedTE Core Algorithms

In this section, we describe the core algorithms of RedTE.

RedTE can achieve decentralized globally informed decisionmaking by not only local input information but also global information, which is gained from the centralized training phase. In the training phase, the learning instability problem can cause RL agents to not cooperate toward global optimization. Meanwhile, the standard training replay strategy leaves RedTE models hard to converge. Additionally, other ML-based methods adjust the split ratio typically in a manner that ignores the rule table updating

time cost. That enables the time of the rule table updating as the bottleneck in control loop latency.

To address the above problems, we first borrow the idea from the cooperative game theory and apply multi-agent deep deterministic policy gradient (MADDPG) [37] algorithm with a global critic network to train the RL models. Furthermore, within the training framework of RedTE, we employ a circular TM replay mechanism to accelerate the convergence speed of RL models, thus improving the overall training efficiency. Finally, we design a novel reward function considering the time required for updating rule tables. This enables RedTE to adjust traffic split ratios in a time-saving manner, without performance sacrifice.

## 4.1 Stable MARL Algorithm with MADDPG

In the CMAS task, to enable all agents to learn towards global optimization, a naive approach is to directly apply traditional single-agent RL methods [36, 41, 51] in the multi-agent setting, where the global-optimization-oriented objective function is used as the reward function for each agent. However, in TE scenarios, the environment would be non-stationary from the view of any single agent, since the state of the global optimization objective is the result of the joint action of all agents, and it is difficult for each agent to distinguish its own contribution. It violates the Markov assumptions in RL methods and will result in the learning instability problem, resulting in poor cooperation results [18].

To address this problem, RedTE borrows the idea from the cooperative game theory and applies the MADDPG algorithm [37] to train the RL models. As a multi-agent actor-critic algorithm, MADDPG aggregates the policies of all agents into a global critic model and distinguishes each agent's contribution to the global reward. Consequently, the TE policies of all agents are visible to every agent, making the environment stationary for each agent. In this way, RedTE can train each agent based on the local information and the feedback from the global critic, towards the goal of global optimization.

Next, we present how the RedTE controller uses MADDPG to train each agent, as illustrated in Figure 6.

**State space.** For each agent i, state  $s_i$  is the combination of the corresponding edge router's traffic demand vector  $m_i$ , local link utilization set  $u_i$ , and local link bandwidth set  $b_i$ .

**Action space.** The action for each agent is fractionally splitting traffic among multiple pre-configured paths towards edge routers. **Training with global critic.** We leverage MADDPG algorithm to address the learning instability problem. As shown in Figure 6, MADDPG is an actor-critic algorithm. It has N actor networks  $(\mu=\{\mu_1,...,\mu_N\})$ , each represents the model in each RedTE agent, as well as a global critic network.

The global critic network criticizes all agents' actions, making them trained toward global optimization. The global critic takes the global information as input and then outputs the global Q value, *i.e.*, the expected reward brought by the actions of all agents. The global information includes the actions of all agents ( $\mathbf{a}=(a_1,...,a_N)$ ), the local states of all agents ( $\mathbf{s}=(s_1,...,s_N)$ ), as well as parts of the state ( $\mathbf{s_0}$ ) that are not observed by these agents.  $\mathbf{s_0}$  can be the link utilization of some intermediate regular routers, it enables the agents to train towards minimizing the network's MLU, and the

<span id="page-5-0"></span>![](_page_5_Figure_11.jpeg)

Figure 6: Training with MADDPG algorithm in RedTE controller.

<span id="page-5-1"></span>![](_page_5_Figure_13.jpeg)

Figure 7: The rule table updating time against the number of updated entries on a Barefoot switch.

information can be easily obtained in the simulation environment. By introducing the global critic network, the actions of all the agents become visible to each other, and some hidden states also become visible to all agents. Each agent can thus stably train its model towards a common global optimization goal, under a stationary environment.

Next, we explain why we cannot simply take MLU as the reward and must design a new one instead.

## 4.2 Reward Function Design

RedTE conducts TE through traffic splitting per edge-router pair, not through per-flow scheduling [34, 35]. In current TE systems [26, 31, 55], the traffic splitting ratio among multiple candidate paths is implemented by hashing and indexing on the TE rule table, the entry number of which is proportional to the number of edge routers, which is

When the TE system generates a decision, the traffic splitting ratio will change and the rule table will also be updated, which takes time, increasing with the number of updated entries. Figure 7 shows the rule table updating time against the number of updated entries, which is obtained by running experiments on a Barefoot switch. We can see that the rule table updating time can be several hundreds of milliseconds.

<span id="page-6-2"></span><span id="page-6-1"></span><span id="page-6-0"></span>![](_page_6_Figure_2.jpeg)

Figure 8: Two examples to show that avoiding unnecessary path adjustment can reduce the rule table updating time. The bandwidth of all links is equal to 100Gbps.

![](_page_6_Figure_4.jpeg)

Figure 9: State transition process in TE scenario.

In traditional LP-based TE systems, the bottleneck of the control loop latency is the computation time. Hence, previous works primarily focus on how to reduce the computation time. However, in machine learning-based TE, both the computation time and the data collection time are significantly shortened, and thus the update time of the rule table becomes the bottleneck. In a network with 153 nodes and 354 edges, the rule table updating time can reach up to 123 ms and accounts for more than 83% in the total latency of the control loop (§6). Consequently, to further reduce the control loop latency, we need to reduce the rule table updating time.

Our solution in RedTE is to avoid unnecessary path adjustments without sacrificing performance. Figure 8 uses two examples to show some unnecessary path adjustments. In Figure 8(a), the traffic demands of  $A \rightarrow E$  and  $B \rightarrow E$  are both 20Gbps at t. Then the traffic demand for  $A \rightarrow E$  increases to 40Gbps. In this case, no matter what the TE paths are for the two demands at t, it is unnecessary to change the TE paths at t+1. Because the bottleneck link is DE, any path change at t+1 cannot reduce MLU.

Figure 8(b) shows the second example. At t, the traffic demands of  $A \rightarrow C$  and  $A \rightarrow D$  are 20Gbps. Demand  $A \rightarrow C$  takes the path of AC and demand  $A \rightarrow D$  takes the path of ABD. At t+1, the traffic demand of  $A \rightarrow D$  increases to 40Gbps. The best path adjustment policy is to move 10Gbps of  $A \rightarrow D$  traffic from path ABD to path ACD. It only requires router A to update 1/4 of the rule table entries to achieve the optimal MLU. However, the traditional TE methods only focus on MLU optimization, not the updating time cost. As a result, they may choose to evenly split the two traffic demands between the two candidate paths, more rule table updates will be required to achieve the same MLU.

Previous RL-based TE solutions cannot distinguish between the alternative path adjustment policies above, since they only focus on the resultant MLU. To address this issue, RedTE introduces a penalty in the reward function, which represents the cost of updating the rule table. The reward function is thus formulated as follows:

$$r_i = -u_{\max} - \alpha * \max_{i \in (1,N)} \left\{ \sum_{j=1}^{N} f(d_{i,j}) \right\},$$
 (1)

where  $d_{i,j}$  is the number of updated rule table entries for the edge pair of (i,j),  $f(\cdot)$  is a function that converts  $d_{i,j}$  into time, and  $\alpha$  is a discounting parameter. By carefully tuning  $\alpha$ , RedTE can avoid many unnecessary path adjustments and does not sacrifice TE performance.

<span id="page-6-3"></span>![](_page_6_Figure_12.jpeg)

(a) Training with naive sequential TM replay.

<span id="page-6-4"></span>![](_page_6_Figure_14.jpeg)

(b) Training with circular TM replay in RedTE

Figure 10: Standard training strategy and RedTE's training strategy. Each rectangle with a kind of color is a TM.

## 4.3 RL Training with Circular TM Replay

In TE scenarios, traffic is continuously injected into the network, which is called an input-driven environment [38], and its state transition process is not only driven by the agent's action but the arrival process of network traffic, which is shown in Figure 9. In every training step, each agent takes an action  $a_2$  for the current state  $s_1$ , and however the reward  $r_2$  for evaluating  $a_2$  is also influenced by the incoming  $TM_2$ . That means a good action (e.g., balancing current load) may receive a bad reward if a new TM with a high load has arrived.

Standard RL training strategy [48] performs poorly in this environment. Specifically, the standard strategy is to replay all TMs sequentially and train them over again and again, as shown in Figure 10(a). In this way, each TM will occur only once in a training epoch, which means, a particular state will occur only once. The memory range[46] of RL training is limited due to the discounting parameter  $\gamma$ . Thus, the RL model cannot optimize policies multiple times for the same state within the memory range. As a result, it is difficult for the RL model to converge, as shown in Figure 11, the TE performance of the RL model wildly fluctuates all the time.

To address the problem, one naive method is to replay a single TM repeatedly until model convergences, and then switch to the next TM. This approach can stabilize the training process by preventing the influence of new incoming TMs. However, it disrupts the data and loses traffic pattern information in training data, ultimately converging to a sub-optimal solution. To strike a balance between training stability and preserving traffic pattern information, we design a novel training strategy that involves circular TM replay.

Specifically, we first divide a long integrated TM sequence into n TM subsequences, each of which is composed of several consecutive TMs. We each time fix a TM subsequence and replay it multiple times repeatedly. When agent models are trained effectively, RedTE switches to the next TM subsequence and conducts the same procedure again and again, till convergence, as shown in Figure 10(b). In this way, agents would experience the same TM multiple times in the short term, and the effect of the new incoming TMs can be mitigated. Meanwhile, because multiple TMs are trained in each round, the traffic pattern information in TMs [21] can be reserved as much as possible. As shown in Figure 11, the normalized MLU performance of RedTE is approaching the optimal gradually, which

<span id="page-7-1"></span>![](_page_7_Figure_2.jpeg)

Figure 11: The convergence trend of training under dynamic TM in A major ISP WAN.

means the quality of the agent policy is getting better and can be trained to convergence.

## 5 Implementation

In this section, we describe our implementation effort, including RedTE controller (§5.1) and RedTE router (§5.2). Besides, implementations in NS3 are described in Appendix A.1.

## <span id="page-7-2"></span>5.1 RedTE Controller Implementation

The RedTE controller manages the lifecycles of RedTE models, including training data collection, training, and distribution of trained models. The controller persistently collects the TM data and periodically performs offline training (*e.g.*, once per week). Upon completion of model training, all agent models are pushed to each router through gRPC [6].

**TM data collection.** The RedTE controller establishes gRPC channels with each RedTE router to collect training data. In each cycle (or a control loop), routers push traffic demand data, which the controller processes and formats for algorithm training, sorting by timestamps and node sequence, and stores in a Postgres database. Data not received integrally within three cycles is considered lost and excluded from storage.

Training RL agents of RedTE in simulator. The RedTE controller centrally trains RL agents on routers using traffic matrices from networks, replayed in a numerical simulation that computes link utilization based on topology, candidate paths, and TMs for RL model training. This process, typically completed within about half a day from scratch for large networks, concludes with model deployment to RedTE routers. Additionally, models can be incrementally retrained within 1 hour based on previously trained ones.

**Hyperparameters of RL models.** The actor network in RedTE has three layers, with the number of neurons in each layer being 64, 32, and 64 respectively. The critic network employs a three-layer fully connected network, with the neuron counts for each layer being 128, 32, and 64 respectively. We selected this architecture due to its empirical superiority over other settings that were examined. The Adam optimizer is used for stochastic gradient descent, with a learning rate of  $10^{-4}$  for the actor and  $10^{-3}$  for the critic.

## <span id="page-7-3"></span>5.2 RedTE Router Implementation

We implement RedTE router prototype based on Barefoot Wedge100BF-32X switch, with Tofino ASIC chip, D-1517 8-core 1.6GHz Intel Pentium CPU, 8GB memory, and PCIe 3.0. Figure 12 shows the implementation architecture. It is composed of 6 core modules, namely, forwarding engine module, data collection module, measurement module, interaction module, inference module, and table update module. Among them, the former two modules run in the data plane (with Tofino ASIC chip), while the latter four modules

<span id="page-7-4"></span>![](_page_7_Figure_14.jpeg)

Figure 12: Architecture of RedTE router prototype.

run in the control plane (with Intel Pentium CPU). The control plane reads data from the data plane and updates the rule table in the data plane by PCIe calls.

5.2.1 Control Plane Implementation. We perform two optimizations to reduce the time cost in the control plane, resulting in a speedup on the TE decision. First, we move the time-consuming consistency operation of SONiC out of the critical path, which saves 100ms. Specifically, after making the TE decision, SONiC conducts a default consistency operation, which stores the action (i.e., traffic split ratio) into Redis, to prevent the loss of the last action when the router restarts. We believe this overhead is only justifiable for centralized TE systems with much lower rule update frequency than RedTE. For RedTE, since split ratios are changed frequently, we bypass the consistency operation and directly step into the rule table update. The consistency operation is done asynchronously using an in-memory write-ahead log.

The second optimization is to remove the interference of process scheduling because RedTE needs a stable execution timing for the measurement module, the inference module, and the table update module. Thus, we bind each process of these modules to specific CPU cores to mitigate the negative effect of resource contention. As a result, the execution timing of these modules becomes stable.

<span id="page-7-0"></span>5.2.2 Data Plane Implementation. The hardware resources of the data plane are mainly consumed in data collection and traffic split. **Data collection.** RedTE routers measure traffic demands by filtering out self-originated packets and determining the destination edge router using a flow table that maps node IDs to register addresses. Packet origin is checked through Segment Routing over IPv6 (SRv6) encapsulation, and the destination node ID is identified from the SRv6 header's final Segment ID (SID), updating the corresponding register with payload length. The measurement of local link utilization is similar and simpler. This data collection process is completed within 11.1ms in networks of up to 754 nodes. The default measurement interval of both the traffic demand and the utilization is 50ms.

The memory overhead of the data collection. The time for the control plane to read data from the data plane depends on the data size, while the time to change the write location of a register is negligible. Therefore, to achieve punctual and periodic data collection, we implement an alternating read-write strategy using two groups of registers, one for writing and the other for reading. In each cycle, the measurement module in the control plane first issues a command to switch the writing address from the

<span id="page-8-2"></span>![](_page_8_Figure_2.jpeg)

![](_page_8_Figure_3.jpeg)

(a) Testbed topology.

(b) RedTE router (above) and controller (below).

Figure 13: Topology, RedTE router and controller in testbed.

previous group of writing registers to the other group of registers, and then issues a data read from the previous group of writing registers. Regardless of whether it is storing the utilization of a local link or the traffic demand of an edge router pair, 16 bytes (8+8) are required.

Typically, routers have fewer than 50 links, leading to a maximum link utilization data size of 800 bytes. Meanwhile, the size of the traffic demand vector is proportional to the number of edge routers in the network. For a network with 754 edge routers, traffic demand data needs around 12 KB of storage. In summary, 12 KB of hardware memory is required in the data plane to collect the input information for TE decision, which is negligible compared with tens of MB register resources in the switch data plane.

Traffic split. We enforce traffic splitting among multiple paths using Segment Routing over IPv6 (SRv6) tunnels. We note that RedTE can be compatible with any implementation of any underlying forwarding methods, such as SRv6 and Multiprotocol Label Switching (MPLS). We opt for SRv6 to be compatible with the network architecture of the datacenters where we deploy the RedTE routers. In addition to a rule table required to split traffic, an SRv6 path table is needed to store end-to-end paths. For a network with N edge routers, M\*(N-1) entries are required to store the rule table in every RedTE router. M is set to 100, which is the maximum value supported by our P4 switch. Experiments show that the bigger M leads to better TE performance due to the finer split granularity and higher split accuracy. Since each entry consists of the match field (i.e., index) with 4 bytes and the action field (i.e., path identifier) with 4 bytes, 8\*(N-1) bytes are needed in total for the rule table. The SRv6 path table maps path identifiers to end-to-end paths consisting of L SID, L is determined by the maximal path length, which can be reduced by SRv6 compression. For instance, for the KDL network with 754 nodes, a SID can be represented in 16 bits and L is about 50. The total memory cost for traffic splitting in RedTE is approximately 61 KB, which is also small compared with the hardware resources that modern switches can provide. Note that an MPLS-based implementation could further save hardware costs owing to its smaller header size.

#### <span id="page-8-1"></span>6 Evaluation

We evaluate the TE performance, latency, and robustness of RedTE in a real WAN testbed and large-scale simulations with public network topology and TMs.

#### Key Results.

 Performance in a real WAN: We deploy physical RedTE routers and video streams in a real WAN comprising 6 city nodes, with the greatest distance between nodes exceeding 600 kilometers. Compared to the state-of-the-art, RedTE achieves a reduction of up to 31.8% in MLU and 57.7% in MOL.

- Performance in large-scale networks: We evaluate RedTE under large-scale networks using NS3 simulator. Compared to the state-of-the-art, RedTE reduces the average MLU by up to 37.4%, and decreases the average queue length by up to 78.9%. Further, the path queuing delay is reduced by up to 75.9% and the number of events where MLU exceeds the capacity upgrade threshold is reduced by up to 38.3%.
- Control loop latency: We evaluate the control loop latency
  of RedTE on the Barefoot switch. RedTE can complete a TE
  decision in millisecond timescale. For a network with 754 nodes
  and 1790 links, RedTE can finish the control loop within 100ms.
- Robustness: RedTE is robust against device failures. Concretely, when 4.0% of the links fail, RedTE experiences a performance loss of only 3.0% and still achieves a 20.7% normalized MLU reduction compared with the LP-based TE method.

#### <span id="page-8-0"></span>6.1 Evaluation Setting

Evaluation setting in real WAN testbed. We deployed RedTE in a real WAN, subsequently called a private WAN (APW), which consists of 6 city nodes and spans 6 datacenters, as depicted in Figure 13(a). The furthest distance between these nodes exceeds 600 kilometers. To ensure the uninterrupted operation of existing services, we employ a customized cutting technique using Virtual Extensible LAN (VxLAN) to establish 10G links between nodes. This approach allowed us to create an isolated virtual network over the existing infrastructure without disrupting current services. Each router is a RedTE router implemented on the Barefoot switch, which independently runs the entire TE control loop. 6 servers, each with 2 10-Gigabit NICs, are used to generate traffic and cause congestion. Additionally, there is a RedTE controller, equipped with 2 NVIDIA A6000 GPUs, and 2 16-core E5-2630-V3 @2.4GHz CPUs.

We set up three different traffic scenarios in the real WAN: (1) WIDE packet trace replay: Packet traces from a collector point of the real backbone network, WIDE [5] were concurrently replayed among all node pairs. Thirty segments of packet traces, each lasting 15 minutes, were employed. Each segment represented the traffic of a specific node pair.

- (2) All to all iPerf: All servers engage in periodic streaming in an all-to-all mode, with each period lasting 200ms. The traffic demands come from the CERNET2 TM dataset. Each pair of nodes simultaneously sends up to more than 100 iPerf flows, each flow's rate is 25Mbps, and the number of flows is proportional to the loads in the TM.
- (3) All to all video streams: All servers send videos to each other via FFmpeg. The rate of a single video stream itself is dynamic, resulting in millisecond-level rate jitter. It is found that for the same type of video, the rate of adjacent 50ms intervals can differ by more than three times. Then, each pair of nodes randomly selects one type of video to send and randomly selects a TM from the CERNET2 TM dataset, then determines the number of video streams sent simultaneously.

**Evaluation setting in large-scale simulation.** We run the packet-level simulation [7, 20] and these TE methods on a server, with the same configuration as the RedTE controller.

<span id="page-9-1"></span>Table 1: Control loop latency (ms) in the form of (input collection time / computation time / rule table updating time) on various network topologies.

| topology<br>(#nodes, #edge) | Colt<br>(153, 354)   | AMIW<br>(291, 2248)  | KDL<br>(754, 1790)    |
|-----------------------------|----------------------|----------------------|-----------------------|
| global LP                   | - / 2120.75 / 120.70 | - / 4803.46 / 200.17 | - / 32022.00 / 519.30 |
| POP                         | - / 68.98 / 113.00   | - / 228.00 / 193.05  | - / 1427.03 / 452.10  |
| DOTE                        | - / 50.50 / 105.85   | - / 150.15 / 198.10  | — / 563.40 / 504.30   |
| TEAL                        | - / 24.95 / 123.27   | - / 69.42 / 223.56   | - / 476.73 / 563.38   |
| RedTE                       | 3.45 / 5.26 / 29.60  | 5.19 / 7.69 / 47.10  | 11.09 / 12.57 / 71.90 |

In NS3 [7], we use a backbone WAN topology from a major ISP, called AMIW with 291 nodes and 2248 edges. We also use 3 public WAN topologies [4], *i.e.*, Viatel with 88 nodes and 184 edges, Colt with 153 nodes and 354 edges, as well as KDL with 754 nodes and 1790 edges.

The experiment uses 2k 15-minute packet trace segments from collectors G and F of WIDE [5], collected from January 2018 to December 2023. The aggregated average traffic rate for these segments can range from hundreds to thousands of Mbps. We randomly selected 10% of node pairs, assigning each a unique packet trace for simultaneous traffic replay, which conforms the NCFlow's observation, in which on average, 16% of the node pairs account for 75% of the total demand. Due to limited traces, some node pairs shared identical traces for AMIW and KDL topology. The link bandwidth and packet buffer size in routers are set to 100Gbps and 30k packets. **Comparables** to RedTE include:

- (1) Both **global LP** and **POP** [42] are *LP-based* solutions. In POP, there exists a tradeoff between the TE performance and the computation time, dependent on the number of sub-problems and the size of the network topology. We test POP's performance under different numbers of sub-problems and choose the maximal one that falls within 20% of the optimal solution, namely, 1 for APW, 8 for Viatel, 16 for ION, 24 for Colt and AMIW, and 128 for KDL. Both global LP and POP use Gurobi[2] as the LP solver.
- (2) Both **TEAL** [53] and **DOTE** [45] are *machine learning-based* methods, which make decisions centrally based on observed global information. TEAL is based on RL, whereas DOTE harnesses supervised learning. Both of them utilize PyTorch [44] to implement deep neural network modules.
- (3) **TeXCP** [30] is a *dTE* solution, which adapts to a dynamically changing network environment by multi-iteration fine-tuning. According to TeXCP, the probe and decision interval are set to 100*ms* and 500*ms*, respectively.

Note that all the above methods use the same set of candidate paths. Paths are chosen by using the *K*-shortest path algorithm. Paths are preferred to be edge-disjoint and K is 3 in the real WAN testbed and 4 in large-scale simulation.

**Metrics.** The metric is the MLU of the network normalized by the theoretical optimal value, obtained by the global LP without control loop latency. That is always  $\geq 1$ , with lower values signifying less congestion. And the burst mitigation capability is evaluated by monitoring the maximum queue length (MQL) in routers.

## <span id="page-9-0"></span>6.2 Evaluation on a Real WAN Testbed

We conduct extensive experiments to compare the control loop latency, solution quality, and practical TE performance among these TE solutions.

**Control loop latency.** As shown in Table 1, the control loop latency consists of the input collection time, the computation time,

<span id="page-9-2"></span>![](_page_9_Figure_14.jpeg)

Figure 14: The number of updated entries in the rule table. The candlesticks depict results across thousands of TMs. The boxes represent the interquartile range, spanning from the 25th percentile to the 75th percentile. The whiskers extend from the minimum to the maximum value of the data

and the rule table updating time. And the full table is seen in Table 4 and Table 5 in Appendix B.1.

**1. the input collection time.** The time of APW is directly measured in the real WAN testbed. For other topologies, we calculate the size of the data structure for storing link utilization and traffic demand and then conduct switch experiments to determine the time to read this data from the data plane.

The collection time of RedTE router falls between 1.5ms to 11.1ms. In other centralized methods, the controller needs to collect traffic demands from the entire network; there is a round trip time (RTT) between the router and controller. The collection time may be up to the maximum RTT of the network, denoted as '–'. For subsequent evaluations, that is set to 20 ms, which will be larger in large networks.

**2. the computation time.** We evaluate the computation time of the RedTE model on P4 switches and the computation time of other alternatives on a server with same configuration as the RedTE controller across all topologies.

The experimental results show that: 1) Global LP is the slowest due to its super-linear complexity. 2) RedTE can achieve up to several orders of magnitude lower computation time compared with global LP and POP because it only requires a few matrix multiplications. 3) RedTE is faster than DOTE and TEAL due to its distributed decision-making.

3. the rule table updating time. Time measurements for APW were taken directly from WAN testbeds, while for other topologies, we inferred time from the number of updated entries per TE solution, as depicted in Figure 7. We observed that RedTE reduces the Maximum Number of Updates (MNU) across routers by 64.9% to 87.2%, 64.0% to 83.4%, and 66.5% to 82.2% for the mean, P95, and P99, respectively, indicating the lowest rule table updating time (Figure 14). This contrasts with traditional global LP, where updating time is much less than computation time, emphasizing the need to focus on reducing rule table updating time in ML-based TE solutions.

In summary, since RedTE reduces the control loop latency from all the three parts, it speeds up the control loop by up to  $341.1\times$ ,  $19.0\times$ ,  $11.2\times$ , and  $10.9\times$ , compared with global LP, POP, DOTE, and TEAL, respectively. In all experiments, RedTE can finish the control loop within 100ms.

**Solution quality.** We conduct experiments on a numerical simulator to show the solution quality (ignoring the control loop latency) of these TE solutions on the four topologies. As shown in Figure 15, we take normalized MLU as the metric and the global LP results as

<span id="page-10-1"></span>![](_page_10_Figure_2.jpeg)

Figure 15: The solution quality. The candlesticks depict results across thousands of TMs. RedTE with AGR represents RedTE which uses a global reward instead of MADDPG. RedTE with NR represents RedTE which uses normal TM replay instead of circular TM replay.

<span id="page-10-2"></span>![](_page_10_Figure_4.jpeg)

(a) Normalized Maximum Link Utilization (MLU).

![](_page_10_Figure_6.jpeg)

(b) Maximum Queue Length (MQL). A cell is equal to 80 bytes.

Figure 16: Performance comparison in 3 different traffic scenarios in a private WAN when setting the control loop latency equal to AMIW data.

the normalized baseline. POP shows faster computation through parallelization, while has lower solution quality, its normalized MLU is between 1 and 1.2. ML-based TE solutions (RedTE, TEAL, and DOTE) outperform POP. Although RedTE makes distributed decisions based on local information, by using the MADDPG algorithm and the circular TE replay in model training, RedTE can achieve comparable performance to the centralized methods, i.e., TEAL and DOTE. Performance breakdown on RedTE shows that, compared to RedTE with AGR and RedTE with NR, RedTE can achieve a reduction of 14.1% and 8.3% on average normalized MLU, respectively.

Practical TE performance. The control loop latency of all TE methods matched AMIW and KDL topologies data (see Table [1\)](#page-9-1), reflecting real-world scale. Global LP's performance, the same as POP's under real WAN topology, was omitted. Figure [16](#page-10-2) shows the experiment result of setting the control loop latency equal to AMIW topology data. It indicates that RedTE outperforms alternatives in three traffic scenarios by reducing average normalized MLU by 11.2% to 30.3% and MQL by 24.5% to 54.7%. The full table about the control loop latency is seen in Table [4](#page-15-2) and Table [5.](#page-15-3)

In Figure [17,](#page-10-3) the control loop latency is set consistent with KDL's data. RedTE demonstrated superior and stable network performance, outperforming alternatives in three traffic scenarios by

<span id="page-10-3"></span>![](_page_10_Figure_12.jpeg)

(a) Normalized Maximum Link Utilization (MLU).

![](_page_10_Figure_14.jpeg)

(b) Maximum Queue Length (MQL). A cell is equal to 80 bytes.

Figure 17: Performance comparison in 3 different traffic scenarios on a private WAN when setting the control loop latency equal to KDL data..

reducing average normalized MLU by 12.0% to 31.8% and MQL by 24.2% to 57.7%. RedTE shows even greater advantages in the 95th and 99th percentile metrics compared to other methods.

## <span id="page-10-0"></span>6.3 Large-scale Evaluation in Simulator

We use NS3 to run simulations based on three public network topologies and a topology from a major ISP WAN.

TE performance. Figure [18\(a\)](#page-11-1) reveals that, compared to all alternatives on the four topologies, RedTE can reduce the average normalized MLU by 14.6% to 37.4%. As a result, Figure [19](#page-11-2) shows RedTE can reduce 15.8% to 38.3% of the events where MLU exceeds the threshold of capacity upgrading (50%). Compared to other machine learning-based work, the performance gain of RedTE mainly comes from the control loop latency reduction.

Figure [18\(b\)](#page-11-3) shows that, compared with all alternatives in four topologies, RedTE can reduce the average MQL by 44.1% to 78.9%. For P95 and P99 of these metrics, compared to other methods, RedTE has an even greater performance advantage. This means RedTE is more stable than other methods. As shown in Figure [20,](#page-11-2) compared to other methods, RedTE can reduce 53.3% to 75.9% average queuing delay, because the reduction of the end-to-end control loop latency can bring about lower router queue lengths. The result shows that, compared to TeXCP, RedTE can reduce the average normalized MLU by 25.9% to 32.4% and the average MQL by 70.0% to 77.2%. That is because when traffic bursts occur, TeXCP requires tens of iterations, often >10s, to converge to a competitive performance. As a result, bursts are gone before TeXCP takes effect.

MLU and MQL under a burst. To demonstrate the ability of RedTE to mitigate bursts on a millisecond timescale, we create a burst lasting 500 on one router and monitor the trend of MLU and MQL over time on AMIW. As shown in Figure [21\(a\),](#page-11-4) the MLU for all TE solutions increases rapidly during the burst, but RedTE is the first to make a TE decision thanks to its short control loop latency. By redirecting burst flows to under-utilized paths, RedTE can limit the rising trend of MLU. Consequently, RedTE exhibits the lowest

<span id="page-11-1"></span>![](_page_11_Figure_2.jpeg)

Figure 18: Performance comparison across various topologies in large-scale simulation.

<span id="page-11-2"></span>![](_page_11_Figure_4.jpeg)

Figure 19: MLU in large-scale simulation.

![](_page_11_Figure_6.jpeg)

Figure 20: Queuing delay in large-scale simulation.

<span id="page-11-4"></span><span id="page-11-0"></span>![](_page_11_Figure_8.jpeg)

<span id="page-11-5"></span>Figure 21: MLU and MQL under a burst on AMIW.

MLU among all TE solutions during the burst. Figure [21\(b\)](#page-11-5) reveals that RedTE also has the lowest queue length due to the shortest control loop latency. The MQL during the burst is 30000 (packets), 29106, 26337, 19100, and 7, for global LP, TeXCP, POP, DOTE, and RedTE, respectively.

Robustness against network failure. In the event of a router or link failure, the corresponding RedTE router sets the failed paths in an extremely congested state. Specifically, the utilization of the failed paths is set to a relatively high value, such as 1000%. This proactive measure informs the agents to avoid allocating traffic to these paths. As illustrated in Figure [22,](#page-11-6) 0.5% to 3.0% of randomly chosen links are set failed. The results indicate that RedTE experiences a maximum performance loss of only 3.0% and still achieves a 20.2% and 20.7% normalized MLU reduction compared with POP on AMIW and KDL, respectively. Thus, RedTE demonstrates significant robustness against link failures. In the event of a network router, all the directed connected links are failed. As illustrated in Figure [23,](#page-11-7) we introduced random node failures ranging from 0.1%

<span id="page-11-6"></span><span id="page-11-3"></span>![](_page_11_Figure_12.jpeg)

Figure 22: Performance comparison between RedTE and POP under link failure.

<span id="page-11-7"></span>![](_page_11_Figure_14.jpeg)

Figure 23: Performance comparison between RedTE and POP under router failure.

<span id="page-11-8"></span>![](_page_11_Figure_16.jpeg)

Figure 24: RedTE performance under traffic noise.

to 0.5% into two networks, AMIW and KDL. The results indicate that RedTE experiences a maximum performance loss of only 5.1% and still achieves a 17.1% and 18.8% normalized MLU reduction compared with POP in AMIW and KDL, respectively. Thus, our approach demonstrates significant robustness in the face of network link failures.

Robustness against drifts in spatial traffic patterns. To assess the impact of unforeseen traffic fluctuations, we introduce variability into the test dataset. This is achieved by independently scaling each traffic demand with a randomly chosen multiplier, uniformly drawn from the interval:

$$[1-\alpha,1+\alpha]$$
 for  $\alpha \in 0.1,0.2,0.3$ . (2)

The experiment results in Figure [24](#page-11-8) show that the RedTE only downgrades 0.5%-2.8% with the growing .

Robustness against drifts in temporal traffic patterns. We study how much RedTE's TE performance decreases when it is not

<span id="page-12-0"></span>Table 2: The performance of RedTE over time on APW.

|                        | 3days | 4 weeks | 8weeks |
|------------------------|-------|---------|--------|
| Average Normalized MLU | 1.05  | 1.08    | 1.10   |

<span id="page-12-1"></span>Table 3: TE Performance of RedTE on AMIW with varied neural network structures.

|                           | Number of neurons in hidden layers |          |            |          |
|---------------------------|------------------------------------|----------|------------|----------|
| Actor network             | (64,32,32)                         | (64,32)  | (64,32)    | (64, 64) |
| Critic network            | (128,64,32)                        | (128,64) | (64,32,32) | (32, 32) |
| Average<br>Normalized MLU | 1.063                              | 1.067    | 1.061      | 1.073    |

trained often. In the test phase of the RedTE model, We use the data that passes 3 days to 8 weeks since the model is trained. Our results in Table [2](#page-12-0) show that while the performance degradation increases over time, in general, RedTE remains close to the optimum (within 10% and 8% for maximizing MLU.

#### Robustness against neural network (NN) structures.

To validate the robustness of RedTE against the DNN model, we evaluate its performance under varied neural network structures in AMIW. For both the actor network and the critic network, we experimented with varying the number of hidden layers and the number of neurons in each layer. The settings and the resulting average normalized MLU are presented in Table [3.](#page-12-1) For instance, (64, 32, 32) indicates three hidden layers with 64, 32, and 32 neurons in each layer, respectively. The performance differences among all these configurations are less than 1.2% under different TE objectives. This suggests that RedTE is insensitive to neural network architecture. Consequently, network operators have flexibility in configuring the DNN model when deploying RedTE, as it does not significantly impact performance.

# 7 Related Work

Traditional burst mitigation schemes. There are two kinds of burst mitigation mechanisms: endhost mechanisms and devicelocal traffic managers. End-host mechanisms, such as BBR [\[14\]](#page-13-6), QUIC [\[32\]](#page-13-7), DCTCP [\[9\]](#page-13-5) work in transport and application layers. They resort to adjusting the sending rate for end hosts in advance before path congestion. Device-local traffic manager-based schemes [\[1,](#page-13-8) [3\]](#page-13-9) can distribute packets among multiple paths to prevent links from being heavily loaded. However, they cannot be aware of global traffic patterns and can be stuck at a local optimum. TE based on global LP. TE based on global LP [\[26,](#page-13-21) [27,](#page-13-22) [31\]](#page-13-23) is widely used in operational networks. These solutions collect global TMs and network topology, resort to a global LP algorithm to solve the MCF problem, and perform global decision deployment, incurring high computation costs, particularly in large-scale networks. The high control loop latency results in a slow response to traffic bursts with short timescales.

TE by accelerating control loop. By realizing the impact of the control loop latency on practical TE performance, some TE solutions with fast computation are proposed. NCFlow [\[8\]](#page-13-10) divides the topology into disjoint clusters and solves sub-problems per cluster in parallel, significantly shortening the algorithm run time. POP [\[42\]](#page-13-11) creates identical copies of the network topology (each

with a fraction of the network capacity) and distributes demands randomly.

Machine learning-based TE. ML-based TE methods [\[12,](#page-13-45) [23,](#page-13-46) [24,](#page-13-27) [45,](#page-13-12) [47,](#page-13-47) [48,](#page-13-37) [52–](#page-14-4)[54\]](#page-14-5) optimize the control loop latency by fast ML model inference. For example, DOTE [\[45\]](#page-13-12) models TE as an end-toend stochastic optimization problem and utilizes the DNN model to make TE decisions. TEAL [\[53\]](#page-14-0) uses GNN and MARL to optimize the allocation of network traffic. However, unlike RedTE, both TEAL and DOTE operate TE in a centralized manner, which incurs a long control loop.

Both Q-routing [\[13\]](#page-13-48) and DATE [\[24\]](#page-13-27) propose a distributed RLbased method. Q-routing attempts to generate a hop-by-hop route configuration by tabular-based RL. But it requires per-packet TE decision, rendering it difficult to implement at line rate. Like RedTE, DATE learns to split traffic among the candidate paths by deep RL. To deduce each agent's contribution to the global TE objective, DATE develops a simple combination of local and global reward functions, which may incur a conflict between the local and global. Besides, DATE does not consider reducing the rule table updating time, which can be a dominant factor in the control loop latency of distributed machine-based TE solutions. Moreover, all previous machine learning-based TE methods ignore the time cost of rule table updates, significantly slowing down decision deployment. Traditional distributed TE. Prior dTE solutions [\[16,](#page-13-13) [30,](#page-13-14) [40\]](#page-13-15), need a multi-step convergence process due to the lack of access to global information. In contrast, leveraging a global critic network for

learning complex patterns during the centralized training phase, RedTE routers can make globally informed decisions from local data in a singular, often iterative-free step during real-time operations.

## 8 Conclusion

In this paper, we design RedTE, a new distributed RL-based TE solution that takes advantage of MARL to optimize practical TE performance. We have implemented the prototype of the RedTE router on a Barefoot switch and deployed the RedTE routers within a real wide area network (WAN) testbed, encompassing six datacenters distributed across six distinct cities. The evaluation results indicate significant enhancements relative to current solutions, including a control loop latency of less than 100, a reduction in average maximum link utilization (MLU) by 37.4%, a decrease in average maximum queue length by 78.9%, a decrease in average path queuing delay by 75.9% and a reduction in the number of events where MLU exceeds the capacity upgrade threshold is reduced by 38.3%. Furthermore, we provide evidence of RedTE's robustness in the face of network link and router failures. RedTE is also robust against drifts in spatial and temporal traffic patterns, and the neural network structure.

# ACKNOWLEDGEMENT

We thank our shepherd Dr. Michael Schapira and the anonymous SIGCOMM reviewers for their constructive comments. Prof. Dan Li is the corresponding author. This work was supported by the National Key R&D Program of China under Grant 2019YFB1802600, the National Natural Science Foundation of China under Grant U23B2001.

## References

- <span id="page-13-8"></span>[1] 2022. cisco dynamic load balance. [https://community.cisco.com/t5/routing/](https://community.cisco.com/t5/routing/dynamic-load-balancing/td-p/646603) [dynamic-load-balancing/td-p/646603.](https://community.cisco.com/t5/routing/dynamic-load-balancing/td-p/646603)
- <span id="page-13-24"></span>[2] 2022. Gurobi. [https://www.gurobi.com.](https://www.gurobi.com)
- <span id="page-13-9"></span>[3] 2022. huawei dynamic load balance. [https://support.huawei.com/enterprise/en/](https://support.huawei.com/enterprise/en/doc/EDOC1100169990/75e82656/configuring-dynamic-load-balancing) [doc/EDOC1100169990/75e82656/configuring-dynamic-load-balancing.](https://support.huawei.com/enterprise/en/doc/EDOC1100169990/75e82656/configuring-dynamic-load-balancing)
- <span id="page-13-43"></span>[4] 2022. Internet Topology Zoo. [http://www.topology-zoo.org/dataset.html.](http://www.topology-zoo.org/dataset.html)
- <span id="page-13-25"></span>[5] 2022. MAWI Working Group Traffic Archive. [https://mawi.wide.ad.jp/mawi/.](https://mawi.wide.ad.jp/mawi/)
- <span id="page-13-40"></span>[6] 2024. gRPC. [https://grpc.io.](https://grpc.io)
- <span id="page-13-41"></span>[7] 2024. Network Simulator 3. [EB/OL]. [https://www.nsnam.org/.](https://www.nsnam.org/)
- <span id="page-13-10"></span>[8] Firas Abuzaid, Srikanth Kandula, Behnaz Arzani, Ishai Menache, Matei Zaharia, and Peter Bailis. 2021. Contracting Wide-area Network Topologies to Solve Flow Problems Quickly. In 18th {USENIX} Symposium on Networked Systems Design and Implementation ({NSDI} 21). 175–200.
- <span id="page-13-5"></span>[9] Mohammad Alizadeh, Albert Greenberg, David A Maltz, Jitendra Padhye, Parveen Patel, Balaji Prabhakar, Sudipta Sengupta, and Murari Sridharan. 2010. Data center tcp (dctcp). In Proceedings of the ACM SIGCOMM 2010 Conference. 63–74.
- <span id="page-13-31"></span>[10] Petri Aukia, Murali Kodialam, Pramod VN Koppol, TV Lakshman, Helena Sarin, and Bernhard Suter. 2000. RATES: A server for MPLS traffic engineering. IEEE Network 14, 2 (2000), 34–41.
- <span id="page-13-28"></span>[11] Michael Bain and Claude Sammut. 1995. A Framework for Behavioural Cloning.. In Machine Intelligence 15. 103–129.
- <span id="page-13-45"></span>[12] Guillermo Bernárdez, José Suárez-Varela, Albert López, Bo Wu, Shihan Xiao, Xiangle Cheng, Pere Barlet-Ros, and Albert Cabellos-Aparicio. 2021. Is Machine Learning Ready for Traffic Engineering Optimization? arXiv preprint arXiv:2109.01445 (2021).
- <span id="page-13-48"></span>[13] Justin A Boyan and Michael L Littman. 1994. Packet routing in dynamically changing networks: A reinforcement learning approach. In Advances in neural information processing systems. 671–678.
- <span id="page-13-6"></span>[14] Neal Cardwell, Yuchung Cheng, C Stephen Gunn, Soheil Hassas Yeganeh, and Van Jacobson. 2016. Bbr: Congestion-based congestion control: Measuring bottleneck bandwidth and round-trip propagation time. Queue 14, 5 (2016), 20–53.
- <span id="page-13-3"></span>[15] Cisco. 2020. Best Practices in Core Network Capacity Planning White Paper. [https://www.cisco.com/c/en/us/products/collateral/routers/wan](https://www.cisco.com/c/en/us/products/collateral/routers/wan-automation-engine/white_paper_c11-728551.html)[automation-engine/white\\_paper\\_c11-728551.html.](https://www.cisco.com/c/en/us/products/collateral/routers/wan-automation-engine/white_paper_c11-728551.html)
- <span id="page-13-13"></span>[16] Anwar Elwalid, Cheng Jin, Steven Low, and Indra Widjaja. 2001. MATE: MPLS adaptive traffic engineering. In Proceedings IEEE INFOCOM 2001. Conference on Computer Communications. Twentieth Annual Joint Conference of the IEEE Computer and Communications Society (Cat. No. 01CH37213), Vol. 3. IEEE, 1300– 1309.
- <span id="page-13-32"></span>[17] Clarence Filsfils, Nagendra Kumar Nainar, Carlos Pignataro, Juan Camilo Cardona, and Pierre Francois. 2015. The segment routing architecture. In 2015 IEEE Global Communications Conference (GLOBECOM). IEEE, 1–6.
- <span id="page-13-16"></span>[18] Jakob Foerster, Gregory Farquhar, Triantafyllos Afouras, Nantas Nardelli, and Shimon Whiteson. 2018. Counterfactual multi-agent policy gradients. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 32.
- <span id="page-13-0"></span>[19] Romain Fontugne, Patrice Abry, Kensuke Fukuda, Darryl Veitch, Kenjiro Cho, Pierre Borgnat, and Herwig Wendt. 2017. Scaling in internet traffic: a 14 year and 3 day longitudinal study, with multiscale analyses and random projections. IEEE/ACM Transactions on Networking 25, 4 (2017), 2152–2165.
- <span id="page-13-42"></span>[20] Kaihui Gao, Li Chen, Dan Li, Vincent Liu, Xizheng Wang, Ran Zhang, and Lu Lu. 2023. Dons: Fast and affordable discrete event network simulation with automatic parallelization. In Proceedings of the ACM SIGCOMM 2023 Conference. 167–181.
- <span id="page-13-39"></span>[21] Kaihui Gao, Dan Li, Li Chen, Jinkun Geng, Fei Gui, Yang Cheng, and Yue Gu. 2020. Incorporating intra-flow dependencies and inter-flow correlations for traffic matrix prediction. In 2020 IEEE/ACM 28th IWQoS.
- <span id="page-13-18"></span>[22] Kaihui Gao, Chen Sun, Shuai Wang, Dan Li, Yu Zhou, Hongqiang Harry Liu, Lingjun Zhu, and Ming Zhang. 2022. Buffer-based end-to-end request event monitoring in the cloud. In 19th USENIX Symposium on Networked Systems Design and Implementation (NSDI 22). 829–843.
- <span id="page-13-46"></span>[23] Nan Geng, Mingwei Xu, Yuan Yang, Enhuan Dong, and Chenyi Liu. 2020. Adaptive and Low-cost Traffic Engineering based on Traffic Matrix Classification. In 2020 29th International Conference on Computer Communications and Networks (ICCCN). IEEE, 1–9.
- <span id="page-13-27"></span>[24] Nan Geng, Mingwei Xu, Yuan Yang, Chenyi Liu, Jiahai Yang, Qi Li, and Shize Zhang. 2021. Distributed and Adaptive Traffic Engineering with Deep Reinforcement Learning. In 2021 IEEE/ACM 29th International Symposium on Quality of Service (IWQOS). IEEE, 1–10.
- <span id="page-13-26"></span>[25] Pablo Hernandez-Leal, Bilal Kartal, and Matthew E Taylor. 2019. A survey and critique of multiagent deep reinforcement learning. Autonomous Agents and Multi-Agent Systems 33, 6 (2019), 750–797.
- <span id="page-13-21"></span>[26] Chi-Yao Hong, Srikanth Kandula, Ratul Mahajan, Ming Zhang, Vijay Gill, Mohan Nanduri, and Roger Wattenhofer. 2013. Achieving high utilization with softwaredriven WAN. In ACM SIGCOMM Computer Communication Review, Vol. 43. ACM, 15–26.
- <span id="page-13-22"></span>[27] Chi-Yao Hong, Subhasree Mandal, Mohammad Al-Fares, Min Zhu, Richard Alimi, Chandan Bhagat, Sourabh Jain, Jay Kaimal, Shiyu Liang, Kirill Mendelev, et al.

- 2018. B4 and after: managing hierarchy, partitioning, and asymmetry for availability and scale in google's software-defined WAN. In Proceedings of the 2018 Conference of the ACM Special Interest Group on Data Communication. 74–87.
- <span id="page-13-30"></span>[28] Sushant Jain, Alok Kumar, Subhasree Mandal, Joon Ong, Leon Poutievski, Arjun Singh, Subbaiah Venkata, Jim Wanderer, Junlan Zhou, Min Zhu, et al. 2013. B4: Experience with a globally-deployed software defined WAN. ACM SIGCOMM Computer Communication Review 43, 4 (2013), 3–14.
- <span id="page-13-1"></span>[29] Hao Jiang and Constantinos Dovrolis. 2005. Why is the internet traffic bursty in short time scales?. In Proceedings of the 2005 ACM SIGMETRICS international Conference on Measurement and Modeling of Computer Systems. 241–252.
- <span id="page-13-14"></span>[30] Srikanth Kandula, Dina Katabi, Bruce Davie, and Anna Charny. 2005. Walking the tightrope: Responsive yet stable traffic engineering. ACM SIGCOMM Computer Communication Review 35, 4 (2005), 253–264.
- <span id="page-13-23"></span>[31] Praveen Kumar, Yang Yuan, Chris Yu, Nate Foster, Robert Kleinberg, Petr Lapukhov, Chiun Lin Lim, and Robert Soulé. 2018. Semi-oblivious traffic engineering: The road not taken. In 15th {USENIX} Symposium on Networked Systems Design and Implementation ({NSDI} 18). USENIX.
- <span id="page-13-7"></span>[32] Adam Langley, Alistair Riddoch, Alyssa Wilk, Antonio Vicente, Charles Krasic, Dan Zhang, Fan Yang, Fedor Kouranov, Ian Swett, Janardhan Iyengar, et al. 2017. The quic transport protocol: Design and internet-scale deployment. In Proceedings of the conference of the ACM special interest group on data communication. 183– 196.
- <span id="page-13-2"></span>[33] Georgios Y Lazarou, Julie Baca, Victor S Frost, and Joseph B Evans. 2009. Describing network traffic using the index of variability. IEEE/ACM Transactions On Networking 17, 5 (2009), 1672–1683.
- <span id="page-13-20"></span>[34] Dan Li, Yunfei Shang, Wu He, and Congjie Chen. 2014. EXR: Greening data center network with software defined exclusive routing. IEEE Trans. Comput. 64, 9 (2014), 2534–2544.
- <span id="page-13-35"></span>[35] Dan Li, Yirong Yu, Wu He, Kai Zheng, and Bingsheng He. 2014. Willow: Saving data center network energy for network-limited flows. IEEE Transactions on Parallel and Distributed Systems 26, 9 (2014), 2610–2620.
- <span id="page-13-33"></span>[36] Timothy P Lillicrap, Jonathan J Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, and Daan Wierstra. 2015. Continuous control with deep reinforcement learning. arXiv preprint arXiv:1509.02971 (2015).
- <span id="page-13-29"></span>[37] Ryan Lowe, Jean Harb, Aviv Tamar, Pieter Abbeel, and Igor Mordatch. 2018. Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments. In 31st Conference on Neural Information Processing Systems (NIPS.
- <span id="page-13-36"></span>[38] Hongzi Mao, Malte Schwarzkopf, Shaileshh Bojja Venkatakrishnan, Zili Meng, and Mohammad Alizadeh. 2019. Learning scheduling algorithms for data processing clusters. In Proceedings of the ACM Special Interest Group on Data Communication. 270–288.
- <span id="page-13-4"></span>[39] Rui Miao, Lingjun Zhu, Shu Ma, Kun Qian, Shujun Zhuang, Bo Li, Shuguang Cheng, Jiaqi Gao, Yan Zhuang, Pengcheng Zhang, et al. 2022. From luna to solar: the evolutions of the compute-to-storage networks in Alibaba cloud. In Proceedings of the ACM SIGCOMM 2022 Conference. 753–766.
- <span id="page-13-15"></span>[40] Nithin Michael and Ao Tang. 2014. Halo: Hop-by-hop adaptive link-state optimal routing. IEEE/ACM Transactions on Networking 23, 6 (2014), 1862–1875.
- <span id="page-13-34"></span>[41] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al. 2015. Human-level control through deep reinforcement learning. nature 518, 7540 (2015), 529–533.
- <span id="page-13-11"></span>[42] Deepak Narayanan, Fiodar Kazhamiaka, Firas Abuzaid, Peter Kraft, Akshay Agrawal, Srikanth Kandula, Stephen Boyd, and Matei Zaharia. 2021. Solving Large-Scale Granular Resource Allocation Problems Efficiently with POP. In Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles. 521–537.
- <span id="page-13-17"></span>[43] Xena network. 2009. White paper: Is your network prepared for microbursts? [https://www.xenanetworks.com/wp-content/ uploads/2019/11/](https://www.xenanetworks.com/wp-content/uploads/2019/11/Microburst_WP.pdf) [Microburst\\_WP.pdf](https://www.xenanetworks.com/wp-content/uploads/2019/11/Microburst_WP.pdf) (2009).
- <span id="page-13-44"></span>[44] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, et al. 2019. Pytorch: An imperative style, high-performance deep learning library. Advances in neural information processing systems 32 (2019).
- <span id="page-13-12"></span>[45] Yarin Perry, Felipe Vieira Frujeri, Chaim Hoch, Srikanth Kandula, Ishai Menache, Michael Schapira, and Aviv Tamar. 2023. DOTE: Rethinking (Predictive) WAN Traffic Engineering. In 20th USENIX Symposium on Networked Systems Design and Implementation (NSDI 23). USENIX Association, Boston, MA, 1557–1581.
- <span id="page-13-38"></span>[46] Richard S Sutton and Andrew G Barto. 2018. Reinforcement learning: An introduction. MIT press.
- <span id="page-13-47"></span>[47] Ying Tian, Zhiliang Wang, Xia Yin, Xingang Shi, Yingya Guo, Haijun Geng, and Jiahai Yang. 2020. Traffic Engineering in Partially Deployed Segment Routing Over IPv6 Network With Deep Reinforcement Learning. IEEE/ACM Transactions on Networking 28, 4 (2020), 1573–1586.
- <span id="page-13-37"></span>[48] Asaf Valadarsky, Michael Schapira, Dafna Shahaf, and Aviv Tamar. 2017. Learning to route with deep rl. In NIPS Deep Reinforcement Learning Symposium.
- <span id="page-13-19"></span>[49] Shuai Wang, Kaihui Gao, Kun Qian, Dan Li, Rui Miao, Bo Li, Yu Zhou, Ennan Zhai, Chen Sun, Jiaqi Gao, et al. 2022. Predictable vFabric on informative data plane. In Proceedings of the ACM SIGCOMM 2022 Conference. 615–632.

- <span id="page-14-1"></span>[50] Yanshu Wang, Dan Li, Yuanwei Lu, Jianping Wu, Hua Shao, and Yutian Wang. 2022. Elixir: A High-performance and Low-cost Approach to Managing {Hardware/Software} Hybrid Flow Tables Considering Flow Burstiness. In 19th USENIX Symposium on Networked Systems Design and Implementation (NSDI 22). 535–550.
- <span id="page-14-2"></span>[51] Christopher JCH Watkins and Peter Dayan. 1992. Q-learning. Machine learning 8, 3-4 (1992), 279–292.
- <span id="page-14-4"></span>[52] Zhiyuan Xu, Jian Tang, Jingsong Meng, et al. 2018. Experience-driven networking: A deep reinforcement learning based approach. In IEEE INFOCOM 2018-IEEE Conference on Computer Communications. IEEE, 1871–1879.
- <span id="page-14-0"></span>[53] Zhiying Xu, Francis Y. Yan, Rachee Singh, Justin T. Chiu, Alexander M. Rush, and Minlan Yu. 2023. Teal: Learning-Accelerated Optimization of WAN Traffic Engineering. In Proceedings of the ACM SIGCOMM 2023 Conference (New York, NY, USA) (ACM SIGCOMM '23). 378–393.
- <span id="page-14-5"></span>[54] Junjie Zhang, Minghao Ye, Zehua Guo, Chen-Yu Yen, and H Jonathan Chao. 2020. CFR-RL: Traffic engineering with reinforcement learning in SDN. IEEE Journal on Selected Areas in Communications 38, 10 (2020), 2249–2259.
- <span id="page-14-3"></span>[55] Junlan Zhou, Malveeka Tewari, Min Zhu, Abdul Kabbani, Leon Poutievski, Arjun Singh, and Amin Vahdat. 2014. WCMP: Weighted cost multipathing for improved fairness in data centers. In Proceedings of the Ninth European Conference on Computer Systems. 1–14.

## <span id="page-15-0"></span>Appendix

Appendices are supporting material that has not been peer-reviewed.

## A RedTE Implementation

# <span id="page-15-1"></span>A.1 RedTE Implementation in NS3 Simulator

As shown in Figure [25,](#page-15-5) in order to simulate the traffic splitting in RedTE, we maintain two core structures, including a global split table and a global flow table. Meanwhile, in the packet forwarding phase, we hijack the layer 2 and 3 forwarding logic in NS3. The hijack mechanism can guarantee that we take control over every packet following the desired path in an explicit and end-to-end manner.

In the split table, each node pair has candidate explicit paths, each of which is with specified weight (or traffic splitting ratio) and identified by node ip along the path. As noted the split table is globally shared among all edge pairs. The flow table stores the map between the flow id and its allocated path.

Upon a coming flow arrival, the system first takes a lookup in the flow table using the packet's 5-tuple information. if matches, the system finds the next hop ip based on its current location in the explicit path and inserts it into the payload field (we allocate the beginning fixed 4 bytes for holding the next hop ip). In the forwarding phase, the forwarding function is hijacked to extract the next hop information in this packet payload field and drop it into the corresponding next-hop link. And if not, NS3 simulator would allocate a path to the flow using its 5-tuple in a weighted random manner and store the map in the global flow table.

## B Evaluation

## <span id="page-15-4"></span>B.1 The experiment Results in a Real WAN

The full table for the control loop latency is seen in Table [4](#page-15-2) and Table [5.](#page-15-3)

<span id="page-15-5"></span>

| global split table    |                                     |             | global flow table  |                                     |
|-----------------------|-------------------------------------|-------------|--------------------|-------------------------------------|
| edge router<br>pair   | explicit path identifier            | split ratio | flow id (5 tuples) | explicit path identifier            |
| edge router<br>pair 1 | path 1 <ip1, ip2,="" ip3=""></ip1,> | 40%         | flow 1             | path 2 <ip4, ip5,="" ip6=""></ip4,> |
|                       | path 2 <ip4, ip5,="" ip6=""></ip4,> | 40%         | flow 2             | path 1 <ip1, ip2,="" ip3=""></ip1,> |
|                       |                                     | 40%         | flow 3             | path 3 <ip7, ip8,="" ip9=""></ip7,> |
|                       | path 3 <ip7, ip8,="" ip9=""></ip7,> | 20%         | flow 4             | path 2 <ip4, ip5,="" ip6=""></ip4,> |
| edge router<br>pair 2 |                                     |             |                    |                                     |

Figure 25: Two core structures to simulate the traffic split in RedTE NS3 implementation.

<span id="page-15-2"></span>Table 4: Control loop latency (ms) in the form of (input collection time/computation time/rule table updating time) under the objective of minimizing MLU on various network topologies (Part 1).

| topology        | APW                | Viatel              | Ion                 |
|-----------------|--------------------|---------------------|---------------------|
| (#nodes, #edge) | (6, 16)            | (88, 184)           | (125, 292)          |
| global LP       | − / 3.45 / 7.92    | − / 690.00 / 75.30  | − / 1045.50 / 97.30 |
| POP             | − / 1.64 / 6.91    | − / 23.40 / 92.12   | − / 56.49 / 99.00   |
| DOTE            | − / 0.15 / 4.47    | − / 39.28 / 60.30   | − / 59.07 / 93.15   |
| TEAL            | − / 0.18 / 6.91    | − / 8.11 / 75.30    | − / 12.30 / 95.08   |
| RedTE           | 1.50 / 0.21 / 1.24 | 2.61 / 3.15 / 21.40 | 3.17 / 4.13 / 25.00 |

<span id="page-15-3"></span>Table 5: Control loop latency (ms) in the form of (input collection time/computation time/rule table updating time) under the objective of minimizing MLU on various network topologies (Part 2).

| topology        | Colt                 | AMIW                 | KDL                   |
|-----------------|----------------------|----------------------|-----------------------|
| (#nodes, #edge) | (153, 354)           | (291, 2248)          | (754, 1790)           |
| global LP       | − / 2120.75 / 120.70 | − / 4803.46 / 200.17 | − / 32022.00 / 519.30 |
| POP             | − / 68.98 / 113.00   | − / 228.00 / 193.05  | − / 1427.03 / 452.10  |
| DOTE            | − / 50.50 / 105.85   | − / 150.15 / 198.10  | − / 563.40 / 504.17   |
| TEAL            | − / 24.95 / 123.27   | − / 69.42 / 233.56   | − / 476.73 / 563.38   |
| RedTE           | 3.45 / 5.26 / 29.60  | 5.19 / 7.69 / 47.10  | 11.09 / 12.57 / 71.90 |