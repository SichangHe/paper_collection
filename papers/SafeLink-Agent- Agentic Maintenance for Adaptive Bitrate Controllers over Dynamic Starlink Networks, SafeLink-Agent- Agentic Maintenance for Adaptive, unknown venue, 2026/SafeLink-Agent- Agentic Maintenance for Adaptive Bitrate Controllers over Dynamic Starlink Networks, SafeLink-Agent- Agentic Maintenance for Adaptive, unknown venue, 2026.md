                                                                                                                                                                                               1




                                           SafeLink-Agent: Agentic Maintenance for Adaptive
                                           Bitrate Controllers over Dynamic Starlink Networks
                                                                             Hongjun Xie, Bowen Zhang, Genke Yang, and Pengcheng Luo




                                              Abstract—Low Earth orbit (LEO) satellite broadband, repre-                     strong, but it can quickly drain the buffer and cause rebuffering
                                           sented by Starlink, is making high-resolution video streaming                     when the available capacity drops.
                                           feasible beyond fixed terrestrial coverage. However, Starlink                        This bitrate–buffer tradeoff becomes harder over Starlink
                                           access links change across time and regions, exposing adaptive
arXiv:2608.28194v1 [eess.SY] 28 Aug 2026




                                           bitrate (ABR) streaming to shifting throughput tails, latency,                    because the access link is not a fixed terrestrial path. LEO con-
                                           volatility, and handover conditions. Existing ABR controllers                     stellations exhibit time-varying topologies and rapidly chang-
                                           are usually designed, tuned, or trained for specific network                      ing access conditions under high satellite mobility [4], [5].
                                           conditions, making it difficult to handle newly exposed hard                      Their service continuity also depends on frequent handovers
                                           Starlink profiles. This paper proposes SafeLink-Agent, an agen-                   as satellites and users move across coverage regions [6], [7].
                                           tic maintenance framework for ABR controllers over dynamic
                                           Starlink networks. SafeLink-Agent summarizes exposed failures                     In operational Starlink networks, satellite mobility, serving-
                                           and uses a large language model (LLM)-based agentic patch                         satellite handovers, obstruction, regional coverage differences,
                                           proposer to generate candidate patches, while replay verification                 traffic load, and gateway association can therefore change
                                           determines whether each patch can be safely committed. The                        the throughput tail, volatility, and latency experienced by
                                           framework supports both rule-based controllers and learned                        users [8], [9]. As these conditions change after deployment,
                                           controllers under the same maintenance workflow. Experiments
                                           on real Starlink networks show that SafeLink-Agent reduces                        an ABR controller may encounter Starlink profiles that differ
                                           the severe-session ratio of RobustMPC from 2.60% to 0.40%                         substantially from the conditions used for its original design or
                                           and reduces cumulative severe sessions from 45 to 7 in rolling                    training. A configuration or policy that is suitable under stable
                                           maintenance. For learned controllers, verified adaptive auditing                  access conditions may produce buffer depletion and severe
                                           lowers the average severe-session ratio from 39.01% to 9.79%.                     session-level stalls under low-tail, high-volatility, high-latency,
                                           These results demonstrate that agentic maintenance can improve
                                           ABR robustness under dynamic Starlink access conditions.                          or handover-heavy Starlink profiles.
                                                                                                                                Most existing ABR studies still follow a static-controller
                                             Index Terms—Adaptive bitrate streaming, Starlink, agentic                       design paradigm. Rule-based controllers such as BOLA and
                                           maintenance, large language model
                                                                                                                             RobustMPC encode expert-designed control rules and fixed
                                                                                                                             parameter settings [10], [11], while learned controllers such
                                                                      I. I NTRODUCTION                                       as Pensieve and Comyco fix their policy parameters after
                                           A. Background and Motivation                                                      training [12], [13]. Recent learned ABR methods further
                                                                                                                             improve adaptation and generalization through curriculum
                                                TARLINK and other low Earth orbit (LEO) satellite
                                           S    broadband systems are making high-bitrate video stream-
                                           ing feasible in rural, maritime, airborne, emergency, and other
                                                                                                                             learning, offline reinforcement learning, meta-learning, and
                                                                                                                             bitrate guidance [14]–[19]. However, once deployed, both rule-
                                                                                                                             based and learned controllers are difficult to adjust when newly
                                           scenarios where terrestrial broadband is unavailable [1], [2].
                                                                                                                             observed Starlink profiles expose new failure modes: rule-
                                           Beyond basic connectivity, large-scale LEO systems are also
                                                                                                                             based controllers often require manual redesign or retuning,
                                           being developed to support low-latency computing and trans-
                                                                                                                             and learned controllers often require additional data collection
                                           mission services in remote areas [3]. In such services, adaptive
                                                                                                                             and retraining.
                                           bitrate (ABR) control is the client-side mechanism that selects
                                                                                                                                This deployment gap leaves two unsatisfactory choices.
                                           each video chunk bitrate according to the observed network
                                                                                                                             Keeping the originally designed or trained controller as a
                                           condition, playback buffer, and chunk-size information. A
                                                                                                                             Static default may preserve high average Quality of Experience
                                           higher bitrate improves visual quality when the link remains
                                                                                                                             (QoE) on common profiles, but it can leave severe stalls on
                                             This work was supported by the National Science and Technology Major            newly exposed hard profiles. Applying a Static conservative
                                           Project of China under Grant 2025ZD1602400. (Corresponding author:                configuration or safety rule can reduce such stalls, but it may
                                           Pengcheng Luo.)                                                                   unnecessarily lower video resolution on stable profiles where
                                             Hongjun Xie, Bowen Zhang, Genke Yang, and Pengcheng Luo are with
                                           Ningbo Artificial Intelligence Institute, Shanghai Jiao Tong University, Ningbo   the original controller already works well. Fig. 1 illustrates
                                           315000, China, and also with the School of Automation and Intelligent             the Starlink ABR scenario and the resulting deployment gap.
                                           Sensing, Shanghai Jiao Tong University, Shanghai 200240, China, and the Key       Therefore, dynamic Starlink ABR requires a maintenance
                                           Laboratory of System Control and Information Processing, Ministry of Ed-
                                           ucation of China, Shanghai 200240, China (e-mail: xiehongjun@sjtu.edu.cn,         view: the controller should be locally repaired for profiles
                                           bwz96sco@sjtu.edu.cn, gkyang@sjtu.edu.cn, luopeng69131@sjtu.edu.cn).              where it fails, while regression checks should prevent the
                                             Hongjun Xie and Pengcheng Luo are also with Shanghai i-Space Orbital            repair from damaging profiles where the controller already
                                           Computing Infrastructure Technology Co., Ltd., Shanghai 200235, China.
                                             The source code will be available at: https://github.com/luopeng69131/          behaves well.
                                           SafeLink-Agent.                                                                      Such a maintenance view requires the ability to read re-
                                                                                                                                                              2




Fig. 1. Deployment gap of ABR streaming over dynamic Starlink access links. (a) A Starlink video client selects chunk bitrate or resolution according to
network and buffer states. (b) Starlink access conditions vary across regions, time, latency, and handovers, producing stable, low-tail, high-volatility, high-
latency, and handover-heavy profiles. (c) A Static high-QoE ABR controller can drain the playback buffer and cause severe session-level stalls on hard profiles,
whereas Static conservative control avoids rebuffering by sacrificing resolution on stable profiles.



play evidence, reason about failure causes, propose localized
controller changes, and use verification feedback. This require-
ment matches the emerging strengths of large language models
(LLMs) and coding agents, whose reasoning, repository-level
code editing, and tool-use capabilities have been demonstrated
in general reasoning models, networking tasks, and software-
engineering agents [20]–[24]. These capabilities make LLMs
and coding agents suitable for maintenance tasks that involve
diagnosis, repair proposal, self-improvement, and auditing, and
allow their outputs to be organized as structured and auditable
                                                                                 Fig. 2. From conventional ABR controller design to agentic controller
maintenance candidates [25]–[28].                                                maintenance. (a) Conventional ABR design builds a static controller from
   Motivated by this observation, this paper proposes SafeLink-                  historical trace data, but future Starlink profiles may expose severe stalls
Agent, an agentic maintenance framework for ABR controllers                      and QoE regression. (b) SafeLink-Agent treats new profiles as maintenance
                                                                                 evidence: it diagnoses replay failures, uses an LLM-based agentic patch
over dynamic Starlink networks. SafeLink-Agent mines Star-                       proposer to generate candidate patches, and updates the controller only after
link profiles and ABR replay logs, summarizes newly exposed                      replay verification.
failure patterns, uses an agentic patch proposer to generate
a candidate patch, and commits the patch only after target-
profile replay and regression-memory replay confirm that it                         • We propose SafeLink-Agent, an agentic maintenance
reduces severe-session risk without introducing unacceptable                          framework for ABR controllers over dynamic Starlink
QoE regression. Fig. 2 summarizes this shift from static-                             networks. SafeLink-Agent mines profile and failure ev-
controller design to agentic controller maintenance.                                  idence from Starlink replay logs, uses an LLM-based
                                                                                      agentic patch proposer to generate candidate patches, and
                                                                                      commits a patch only after replay verification confirms
B. Contributions
                                                                                      target-profile improvement without unacceptable regres-
   The main contributions of this paper are summarized as                             sion.
follows:                                                                            • We instantiate SafeLink-Agent for both rule-based and
   • We formulate dynamic ABR controller maintenance                                  learned ABR controllers. For BOLA and RobustMPC,
     over Starlink networks. Instead of treating ABR as a                             it produces profile-conditioned configuration patches;
     static-controller design problem, the formulation models                         for SABR, Pensieve, and Comyco, it produces verified
     controller updates, Starlink profiles, candidate patches,                        runtime-auditing patches. This demonstrates that hetero-
     severe-session risk metrics, and verifier constraints.                           geneous ABR controllers can be maintained through a
                                                                                                                                   3



      unified patch-and-verify interface.                          studies over Starlink and LEO networks further indicate that
  •   We build a dynamic Starlink ABR evaluation work-             such variation can affect real-time and streaming applica-
      flow from real Starlink traces. The experiments evaluate     tions [32], [33]. However, existing ABR research mainly
      SafeLink-Agent across diverse controller types and newly     asks how to design, train, or generalize a controller before
      observed Starlink profile scenarios. The results show that   deployment. Even when a controller adapts online at the chunk
      agentic maintenance can reduce severe-session failures       level, its rule set, policy, or safety mechanism is typically not
      while avoiding QoE loss.                                     repaired after new hard profiles are discovered.
                                                                      These limitations leave a gap between ABR controller
C. Organization                                                    design and controller maintenance under dynamic Starlink
                                                                   access. Existing ABR studies mainly optimize the controller
   The remainder of this paper is organized as follows. Section    before deployment or adapt bitrate decisions online at the
II reviews related work on ABR control under dynamic               chunk level, but they rarely study how an already deployed
network conditions and LLM-based system maintenance. Sec-          controller should be diagnosed, repaired, and regression-tested
tion III formulates dynamic Starlink ABR as a controller-          when newly observed profiles expose severe stalls or QoE
maintenance problem. Section IV presents the SafeLink-Agent        regression. This gap motivates treating ABR controllers as
maintenance framework, including profile mining, candidate         maintainable artifacts after deployment, rather than as fixed
patch generation, patch schema validation, and patch commit-       outputs of an offline design process.
ment. Section V describes the experimental setting and evalu-
ates SafeLink-Agent across newly observed Starlink profiles.
Finally, Section VI concludes the paper.                           B. LLM Agents for System Maintenance and Program Repair
                                                                      Recent progress in LLM-based software engineering shows
                     II. R ELATED W ORK                            that language models can operate on real repositories rather
   The related literature is organized along two lines. We first   than isolated code snippets. SWE-bench evaluates models
review ABR control under dynamic network conditions, which         on GitHub issue resolution tasks that require repository-level
is the application domain of this paper. We then discuss LLM       understanding and patch generation [25]. SWE-agent further
agents for system maintenance and program repair, which            demonstrates that agent-computer interfaces, repository nav-
motivate the agentic maintenance of SafeLink-Agent.                igation, file editing, and test execution can substantially im-
                                                                   prove automated software engineering performance [23]. Au-
                                                                   toCodeRover combines LLMs with program-structure-aware
A. ABR Control under Dynamic Network Conditions                    code search and test feedback for autonomous program im-
   ABR control has long been studied as the client-side mech-      provement [24]. Meanwhile, Agentless shows that careful
anism for adapting video quality to network dynamics. Clas-        localization, localized repair, and patch validation can be as
sical online methods select chunk bitrates using throughput        important as complex agent scaffolding [26]. These studies
prediction, buffer occupancy, or short-horizon optimization.       support the use of LLMs as maintenance assistants, but
Model Predictive Control (MPC)-style ABR explicitly plans          they also emphasize that generated patches require external
bitrate decisions over a future horizon [10], while BOLA for-      validation.
mulates bitrate selection as a buffer-based utility maximization      LLM agents have also begun to appear in system op-
problem [11]. Prediction-assisted systems such as Lumos and        eration and networking contexts. LLexus uses LLM agents
Starnet further show that more accurate throughput prediction      to convert troubleshooting guides into executable incident-
can improve mobile video QoE [9], [29], [30]. These methods        management plans [27]. LogGPT explores generative pre-
can react to short-term network variation, but their control       trained transformer (GPT)-based log anomaly detection for
rules and parameters are usually fixed once deployed.              system diagnosis [34]. NetLLM adapts LLMs for networking
   Learning-based ABR controllers improve this design space        tasks and shows the potential of LLM reasoning in networked
by learning policies from QoE feedback. Pensieve trains a          systems [22]. These works are relevant because ABR con-
neural ABR policy with reinforcement learning [12], and            troller maintenance also involves logs, configuration choices,
Comyco combines imitation learning and reinforcement learn-        and network-dependent behavior. However, a latency-sensitive
ing to improve ABR decisions [13]. SABR further follows            ABR controller cannot simply trust a generated action or patch
a pretraining and fine-tuning design for satellite ABR [31].       because the consequence is measured in playback stalls and
More recent studies focus on adaptation and generalization         QoE regression.
across heterogeneous traces. Genet uses automatic curriculum          These works indicate that LLM and coding agents can
generation to expose a policy to diverse network condi-            support the maintenance of deployed systems, but the vali-
tions [14]. Offline reinforcement learning and meta-learning       dation target in ABR control differs from those in existing
improve ABR policies across traces or tasks [15], [16], while      settings. In software repair, correctness is commonly evaluated
bitrate guidance, MetaABR, and Merina+ explore additional          by functional tests; in artificial intelligence for IT operations
mechanisms for cross-condition adaptation [17]–[19].               (AIOps), the output is often assessed as a diagnosis or exe-
   Starlink access makes this post-deployment question more        cution plan. For an ABR controller, a maintenance proposal
important because measured links show temporal, regional,          affects playback behavior over measured network traces: a
and handover-related performance variation [8], [9]. Video         change that mitigates failures on a newly observed profile
                                                                                                                                  4



may also reduce QoE or introduce stalls on profiles that           where Smem denotes representative sessions retained from
were previously stable. Therefore, LLM-based agentic ABR           earlier replays. The regression memory stores previously ac-
maintenance requires a way to generate constrained controller      ceptable playback behavior, so that later maintenance decisions
changes and judge their effect on both newly exposed failures      can be checked against profiles and sessions that should remain
and previously acceptable playback behavior.                       stable.

    III. DYNAMIC ABR C ONTROLLER M AINTENANCE                      B. Replay-Based Controller Evaluation
                   F ORMULATION
                                                                      After the profile sequence is defined, the next step is
   This section formulates ABR control over dynamic Starlink       to specify how a controller is evaluated on each profile.
access as a maintenance problem. We first define Starlink          Controller maintenance requires a behavioral interface that can
profiles as the operating units on which new failures are          compare the original and patched controllers under the same
observed. We then define replay-based evaluation to measure        measured network conditions. Replay evaluation provides this
how a controller behaves on each profile. With the measure-        interface: it exposes not only aggregate QoE, but also the logs
ment interface specified, we introduce the controller update to    needed for failure mining and regression checking. Given a
describe what SafeLink-Agent can change. Finally, we define        controller 𝐶 and a measured Starlink streaming session 𝜏,
the verifier constraints that determine whether a candidate        the replay simulator executes the controller over the measured
patch should be committed.                                         throughput sequence and returns session-level outcomes:
                                                                            (𝑄(𝐶, 𝜏), 𝐵(𝐶, 𝜏), ℓ(𝐶, 𝜏)) = Replay(𝐶, 𝜏),         (5)
A. Starlink Profiles
                                                                   where 𝑄(𝐶, 𝜏) is the session-level QoE, 𝐵(𝐶, 𝜏) is the cumu-
   Starlink measurements are first converted into replay traces,
                                                                   lative rebuffering, and ℓ(𝐶, 𝜏) is the replay log that records
each of which represents one streaming session under a
                                                                   actions, buffer states, rebuffering events, and other diagnostic
measured throughput and latency trajectory. Controller main-
                                                                   signals. This replay interface is the basic object maintained
tenance, however, should not react to an isolated trace alone;
                                                                   by SafeLink-Agent: a patch is judged by how the patched
it should react when a group of traces exposes a recurring
                                                                   controller behaves under trace replay.
operating condition or failure mode. We call such a group a
                                                                      The QoE used in replay follows the standard ABR form that
Starlink profile. A profile may correspond to a deployment
                                                                   combines video quality, rebuffering penalty, and smoothness
stage, such as a newly collected calibration batch, or to a hard
                                                                   penalty. For a session with 𝑇 chunks, we write it as
access condition, such as low throughput tail, high volatility,
high latency, or frequent satellite changes.                                                 𝑇 h
                                                                                            ∑︁
   As new profiles are exposed to the deployed system, the                      𝑄(𝐶, 𝜏) =          𝑢(𝑎 𝑡 ) − 𝜇𝜌𝑡
access environment is represented as a sequence                                             𝑡=1
                                                                                                                       i
                                                                                              − 𝜂|𝑢(𝑎 𝑡 ) − 𝑢(𝑎 𝑡 −1 )| ,       (6)
                       𝐷1, 𝐷2, . . . , 𝐷 𝑘 , . . . ,         (1)
                                                                                             𝑇
                                                                                            ∑︁
where 𝐷 𝑘 denotes the 𝑘th profile exposed to the maintenance                    𝐵(𝐶, 𝜏) =         𝜌𝑡 .
workflow. Formally, 𝐷 𝑘 is a set of measured replay sessions:                               𝑡=1

                 𝐷 𝑘 = {𝜏𝑘,1 , 𝜏𝑘,2 , . . . , 𝜏𝑘,𝑛𝑘 },       (2)   Here 𝑢(𝑎 𝑡 ) is the utility of the selected bitrate action, 𝜌𝑡
                                                                   is the rebuffering duration of chunk 𝑡, and 𝜇 and 𝜂 are
where each 𝜏𝑘, 𝑗 is one replay trace in this profile and 𝑛 𝑘       the rebuffering and smoothness penalty weights. The exact
is the number of sessions. To characterize the profile for         simulator computes 𝜌𝑡 from the measured throughput, chunk
maintenance, we summarize 𝐷 𝑘 by metadata                          size, and buffer evolution.
                             tp                     ⊤               For a profile 𝐷, replay outcomes are aggregated over the
            𝑧(𝐷 𝑘 ) = 𝜇tp , 𝑞 0.05 , 𝜎tp , 𝜇lat , 𝐻ho ,  (3)       sessions in that profile:
where 𝑧(𝐷 𝑘 ) is the compact description of profile 𝐷 𝑘 , 𝜇tp is                    ¯
                                                                                    𝑄(𝐶, 𝐷) = E 𝜏∼𝐷 [𝑄(𝐶, 𝜏)],
                         tp                                                                                                     (7)
the mean throughput, 𝑞 0.05 is the 5th-percentile throughput,                       ¯
                                                                                    𝐵(𝐶, 𝐷) = E 𝜏∼𝐷 [𝐵(𝐶, 𝜏)].
𝜎tp is throughput volatility, 𝜇lat is mean latency, and 𝐻ho
represents handover or serving-satellite change intensity. These   These profile-level quantities provide the playback measure-
metadata describe the environment in which a controller is         ments used by later maintenance decisions. In particular, they
replayed and help SafeLink-Agent distinguish, for example,         allow SafeLink-Agent to compare controller behavior on both
a low-tail profile from a high-volatility or handover-heavy        the newly exposed profile and the regression memory.
profile.
   The profile sequence also defines what should be protected      C. Controller Update
during maintenance. When the current profile is 𝐷 𝑘 , the re-
gression memory is formed from previously validated profiles          Profiles and replay evaluation define where controller be-
and representative sessions:                                       havior is observed and how playback outcomes are measured.
                                                                   The maintenance formulation also needs to specify how an
         M 𝑘 = {𝐷 𝑖 : 𝑖 < 𝑘, 𝐷 𝑖 is validated} ∪ Smem ,      (4)   already deployed controller may be updated. We model this
                                                                                                                                              5



update as a versioned patch operation: the current controller        third inequality limits the QoE cost on that profile. The fourth
remains the reference controller, and any proposed change            and fifth inequalities implement regression memory: a patch
must belong to an admissible patch space.                            should not introduce new severe-session risk or excessive
   Let 𝐶𝑣 denote the current deployed ABR controller ver-            QoE loss on previously stable profiles. The final inequality
sion. The controller can be rule-based, learned, or risk-aware.      limits patch complexity. This formulation separates proposal
When a new Starlink profile exposes severe-session failures,         generation from patch acceptance: the proposer may generate
SafeLink-Agent searches for a candidate patch from the ad-           a candidate patch, but the patch is committed only if replay
missible patch space and applies it to obtain the next controller    verification confirms that 𝑝 satisfies Γ.
version:
                  𝐶𝑣+1 = 𝐶𝑣 ⊕ 𝑝, 𝑝 ∈ P.                       (8)               IV. S AFE L INK -AGENT M AINTENANCE
Here ⊕ denotes applying a patch to the current controller.              SafeLink-Agent realizes controller maintenance as a se-
A patch is the maintenance decision made for the controller          quence of failure summarization, candidate patch generation,
version. The patch 𝑝 may change a finite configuration, add          and verified patch commitment. When a newly observed
a profile-conditioned rule, enable a runtime auditor, introduce      Starlink profile exposes a maintenance trigger, the framework
a fallback condition, or update a constrained training config-       first summarizes where the current controller fails. Using this
uration. Its complexity is denoted by Ω( 𝑝) and is limited to        summary, the agentic patch proposer then generates a candi-
keep the repair interpretable and verifiable.                        date patch. Patch schema validation checks whether the patch
                                                                     follows the required patch schema, and replay verification
                                                                     finally decides whether it should be committed to produce the
D. Risk Metrics and Verifier Constraints
                                                                     new controller. Fig. 3 summarizes this maintenance workflow.
   After a controller update is represented as a patch opera-
tion, SafeLink-Agent needs criteria for deciding whether the         A. Profile and Failure Mining
patched controller is acceptable. The verifier first measures
severe-session risk and worst-tail rebuffering on replayed              Profile and failure mining converts replay evidence into
profiles, and then checks whether the patch improves the newly       the structured maintenance context used by the agentic patch
exposed profile without causing unacceptable regression.             proposer. It has two roles. First, it checks whether the newly
   We first define the severe-session ratio of controller 𝐶 on       observed profile 𝐷 𝑘 actually requires maintenance. Second, if
profile 𝐷 as                                                         maintenance is triggered, it summarizes the Starlink profile,
                                                                     the observed playback failure, representative hard sessions,
           𝑅sev (𝐶, 𝐷) = E 𝜏∼𝐷 [1{𝐵(𝐶, 𝜏) > 𝑏 sev }] ,        (9)    and the behavior that should be preserved.
where 1{·} is the indicator function and 𝑏 sev is the severe-stall      The trigger check is performed after the current controller
threshold. We further define the worst-tail rebuffering metric       𝐶𝑣 is replayed on 𝐷 𝑘 using the interface in Section III-B. The
                                                                     regression memory M 𝑘 provides the reference behavior for
             𝑇𝛼 (𝐶, 𝐷) = E 𝜏 ∈Tail 𝛼 (𝐶,𝐷) [𝐵(𝐶, 𝜏)] ,       (10)    identifying unacceptable regression. For the two quantitative
where Tail 𝛼 (𝐶, 𝐷) denotes the worst 𝛼 fraction of sessions in      risk triggers, we define
profile 𝐷 ranked by cumulative rebuffering under controller           Itrig (𝐶𝑣 , 𝐷 𝑘 ) = 1[𝑅sev (𝐶𝑣 , 𝐷 𝑘 ) > 𝛽sev ∨ 𝑇𝛼 (𝐶𝑣 , 𝐷 𝑘 ) > 𝛽tail ] ,
𝐶.                                                                                                                                       (12)
   These replay metrics become the quantities checked by the         where 𝛽sev and 𝛽tail are the trigger thresholds for severe-
verifier. On the newly exposed profile, the patched controller       session ratio and worst-tail rebuffering, respectively. Visible
should repair the observed failure without an excessive QoE          QoE regression relative to regression memory can be used as
cost. Because such a local repair may also affect profiles that      auxiliary trigger evidence. When Itrig (𝐶𝑣 , 𝐷 𝑘 ) = 1, the miner
were previously acceptable, the verifier checks the same patch       builds the maintenance context described below.
on regression memory and requires the preserved behavior to              The context first records what kind of Starlink profile is
remain within tolerance. Accordingly, for a current controller       being handled. For the current profile 𝐷 𝑘 , the profile-side sum-
𝐶𝑣 , a newly exposed profile 𝐷 new , and regression memory           mary is the metadata vector 𝑧(𝐷 𝑘 ) defined in (3). It records
M, we collect the acceptance requirements as the verifier            network-side properties such as throughput tail, volatility, la-
constraints Γ:                                                       tency, and handover intensity, which distinguish, for example,
      Γ : 𝑝 ∈ P,                                                     a low-tail profile from a high-volatility or handover-heavy
           𝑅sev (𝐶𝑣 ⊕ 𝑝, 𝐷 new ) ≤ 𝑅sev (𝐶𝑣 , 𝐷 new ) − 𝛿,           profile.
                                                                         The second part of the context describes how the current
           𝑇𝛼 (𝐶𝑣 ⊕ 𝑝, 𝐷 new ) ≤ 𝑇𝛼 (𝐶𝑣 , 𝐷 new ) − 𝛾,               controller behaves on this profile. The miner uses the replay
            ¯ 𝑣 ⊕ 𝑝, 𝐷 new ) ≥ 𝑄(𝐶
           𝑄(𝐶                   ¯ 𝑣 , 𝐷 new ) − 𝜖,          (11)    outputs of 𝐶𝑣 on 𝐷 𝑘 to form an aggregate failure summary:
           𝑅sev (𝐶𝑣 ⊕ 𝑝, M) ≤ 𝑅sev (𝐶𝑣 , M) + 𝜁,                                                 
                                                                                  𝑠(𝐶𝑣 , 𝐷 𝑘 ) = 𝑄,¯ 𝐵,¯ 𝑅sev , 𝑇𝛼 , 𝑁sev , 𝜌audit ⊤ ,
                                                                                                                                  
                                                                                                                                         (13)
           ¯ 𝑣 ⊕ 𝑝, M) ≥ 𝑄(𝐶
           𝑄(𝐶              ¯ 𝑣 , M) − 𝜖 reg ,
                                                                     where 𝑁sev is the number of severe sessions and 𝜌audit is
           Ω( 𝑝) ≤ 𝜅.                                                the audit-intervention rate when applicable. This summary
The first two inequalities require the patch to reduce severe-       gives the agentic patch proposer aggregate evidence of QoE,
session risk and worst-tail rebuffering on the target profile. The   rebuffering, tail risk, and auditing behavior.
                                                                                                                                                          6




Fig. 3. Overall framework of SafeLink-Agent. The current ABR controller, a newly observed Starlink profile, and regression memory are first summarized
by profile and failure mining. The agentic patch proposer generates a candidate patch for rule-based or learned ABR controllers, but patch commitment is
decided by the replay verifier using target-profile replay, regression-memory replay, QoE cost, regression risk, and patch-complexity checks. The online ABR
loop remains separate from the agentic maintenance workflow.



   Aggregate metrics alone do not show which sessions caused                   which parameters of the current controller are maintainable
the failure. The miner therefore uses the detailed replay log                  and which profile or failure features can be used to condition
ℓ(𝐶𝑣 , 𝜏) to identify representative hard sessions:                            a maintenance action. Table I presents the detailed controller
                                                                               metadata settings used in this paper.
           Fsev (𝐶𝑣 , 𝐷 𝑘 ) = {𝜏 ∈ 𝐷 𝑘 | 𝐵(𝐶𝑣 , 𝜏) > 𝑏 sev },
                                                                       (14)       The output 𝑝 is represented as a structured candidate patch
           Ftail (𝐶𝑣 , 𝐷 𝑘 ) = Tail 𝛼 (𝐶𝑣 , 𝐷 𝑘 ).                             rather than free-form code. It specifies the target controller
Fsev contains sessions whose cumulative rebuffering exceeds                    version, patch type, activation condition, maintenance oper-
the severe-stall threshold, and Ftail contains the worst-tail                  ation, and bounded parameter values. The operation forms
sessions ranked by cumulative rebuffering. These sets connect                  considered in this paper are configuration selection, profile-
the profile-level failure to concrete replay sessions that can be              conditioned configuration rules, and runtime auditor attach-
inspected by the agentic patch proposer and later checked by                   ment or tuning for learned ABR policies.
the verifier.
   Finally, the profile summary, aggregate failure summary,                    C. Patch Schema Validation
representative hard sessions, and regression-memory summary                       The agentic proposer may return an unsupported patch type,
are combined into the maintenance context:                                     unknown fields, invalid activation conditions, or parameter
      X𝑘 = (𝑧(𝐷 𝑘 ), 𝑠(𝐶𝑣 , 𝐷 𝑘 ), Fsev , Ftail , 𝑠(𝐶𝑣 , M 𝑘 )) ,      (15)    values outside the allowed range. A candidate patch is schema-
                                                                               valid only if it conforms to this controller-specific schema and
where 𝑠(𝐶𝑣 , M 𝑘 ) summarizes the playback behavior recorded                   satisfies the patch-complexity bound.
in regression memory. Thus, X𝑘 tells the agentic patch pro-                       The admissible patch space can therefore be written as
poser what kind of profile is being handled, how the current
controller fails on that profile, which sessions represent the                               P = {𝑝 | Schema𝐶𝑣 ( 𝑝) = 1, Ω( 𝑝) ≤ 𝜅}.                  (17)
failure, and what behavior should be preserved.                                Here, Schema𝐶𝑣 ( 𝑝) = 1 means that the candidate patch
                                                                               matches the patch schema selected for 𝐶𝑣 , including the con-
B. Agentic Patch Proposer                                                      troller type, allowed operation, approved activation-condition
   The agentic patch proposer uses an LLM assistant to gen-                    fields, and admissible parameter ranges.
erate a candidate repair for the ABR controller. After profile                    If a candidate patch satisfies (17), patch schema validation
and failure mining, it maps the structured maintenance inputs                  outputs it as a schema-valid patch and sends it to replay
to a candidate patch:                                                          verification. If the candidate patch fails validation, the module
                                                                               outputs a schema-violation record and stores it in Patch
                  𝑝 = 𝐺 𝜃 (X𝑘 , H𝑣 , meta(𝐶𝑣 ), Γ) ,                   (16)    History before replay begins.
where 𝐺 𝜃 denotes the proposer, which can be implemented
by an LLM assistant; H𝑣 denotes Patch History for controller                   D. Replay Verification and Patch Commit
version 𝑣; and meta(𝐶𝑣 ) denotes the controller metadata.                         Replay verification is the commit gate between a schema-
  The controller metadata gives the proposer controller-                       valid patch and a new controller version. The verification
specific information before a patch is generated. It describes                 is organized into two checks: target-profile replay examines
                                                                                                                                                                 7



                                                                   TABLE I
                                            C ONTROLLER METADATA SETTINGS USED BY S AFE L INK -AGENT.

  Controller                 Maintainable Parameters                                      Available Profile/Failure Features
  BOLA                       Buffer-threshold candidates, e.g., (10, 30) s or (15, 45)    Throughput tail, volatility, buffer pressure, and severe-session
                             s.                                                           evidence.
  RobustMPC                  Prediction horizon, safety margin, and bitrate-cap candi-    Tail throughput, latency, volatility, handover intensity, and replay
                             dates, e.g., horizon 5/6 and margin 1.00/0.85.               failure summaries.
  Learned ABR                Policy identity and admissible runtime auditor parameters    Buffer state, safe capacity, requested bitrate risk, and severe-
                             such as safe-capacity margin, low-buffer threshold, and      session examples.
                             buffer guard.



                                                                               severe-session risk on M. The verifier therefore checks the
                                                                               regression-memory block of Γ:
                                                                                         Γmem :    𝑅sev (𝐶𝑣 ⊕ 𝑝, M) ≤ 𝑅sev (𝐶𝑣 , M) + 𝜁,
                                                                                                                                                           (19)
                                                                                                   ¯ 𝑣 ⊕ 𝑝, M) ≥ 𝑄(𝐶
                                                                                                   𝑄(𝐶              ¯ 𝑣 , M) − 𝜖 reg .
                                                                               Here, the first inequality limits severe-session risk increase
                                                                               on profiles in regression memory, and the second limits QoE
                                                                               regression.
                                                                                  3) Patch Commit and Patch History: The verifier converts
                                                                               the target-profile replay and regression-memory replay reports
                                                                               into an accept-or-reject decision. A patch is accepted only
                                                                               when patch schema validation and these checks confirm that
Fig. 4. Replay verification for schema-valid patches. The verifier evaluates
each patch on the challenging target profile and on previously validated       𝑝 satisfies Γ. Rejected patches are stored in the Patch His-
profiles in regression memory.                                                 tory H𝑣 , and a machine-readable reason, such as insufficient
                                                                               target-risk reduction, excessive QoE cost, regression-memory
                                                                               constraint violation, or patch-complexity violation.
whether the patch repairs the newly exposed failure, and
                                                                                  The committed controller update is therefore
regression-memory replay examines whether it preserves pre-                                           (
viously validated behavior. It reuses the replay-based evalu-                                           𝐶𝑣 ⊕ 𝑝, if 𝑝 satisfies Γ,
ation in Section III-B to compare the current controller and                                 𝐶𝑣+1 =                                      (20)
                                                                                                        𝐶𝑣 ,     otherwise.
the patched controller under measured Starlink profiles. Fig. 4
summarizes the verification flow.                                                Algorithm 1 summarizes the SafeLink-Agent maintenance
   1) Target-Profile Replay: Target-profile replay checks                      procedure.
whether a candidate patch actually addresses the failure that
triggered maintenance. For efficiency, a lightweight probe                                        V. E XPERIMENTAL E VALUATION
replay may first evaluate the patch on a small subset of 𝐷 𝑘 to                A. Experimental Setting and Starlink Profiles
screen clearly ineffective proposals. Passing this probe does                     1) Starlink Trace Processing and ABR Task: We build
not certify the patch and does not check regression memory;                    the evaluation traces from the raw Starlink measurement
it only sends the patch to full target-profile replay.                         dataset [9]. The raw measurements contain downlink through-
   In the full replay, the current controller 𝐶𝑣 and the patched               put, latency, satellite candidate information, and terminal-side
controller 𝐶𝑣 ⊕ 𝑝 are evaluated on the same target profile 𝐷 𝑘 ,               status logs from multiple regions. To make the traces directly
so any behavioral difference can be attributed to the patch                    replayable by ABR controllers, we convert each continuous
rather than to a change in traces. The verifier then checks                    measurement segment into a 600-s trace with 1-s throughput
the target-profile block of Γ, obtained from (11) by setting                   samples. Traces with insufficient duration, missing throughput,
𝐷 new = 𝐷 𝑘 :                                                                  or invalid replay rows are discarded. Table II summarizes
          Γtar :   𝑅sev (𝐶𝑣 ⊕ 𝑝, 𝐷 𝑘 ) ≤ 𝑅sev (𝐶𝑣 , 𝐷 𝑘 ) − 𝛿,                 the resulting valid ABR traces. The table uses the location
                   𝑇𝛼 (𝐶𝑣 ⊕ 𝑝, 𝐷 𝑘 ) ≤ 𝑇𝛼 (𝐶𝑣 , 𝐷 𝑘 ) − 𝛾,             (18)    labels US, OSN, and VIC, corresponding to the United States,
                                                                               Germany, and Victoria, Canada, respectively. In the table, TP
                    ¯ 𝑣 ⊕ 𝑝, 𝐷 𝑘 ) ≥ 𝑄(𝐶
                   𝑄(𝐶                 ¯ 𝑣, 𝐷𝑘) − 𝜖 .
                                                                               denotes throughput; P05, P50, and P95 denote the 5th-, 50th-
Here, the first two inequalities require reductions in severe-                 , and 95th-percentile throughput, respectively; and the trace
session risk and worst-tail rebuffering on 𝐷 𝑘 , while the third               split is reported in the order of train/calibration/test.
limits the QoE cost of the repair.                                                All ABR experiments use the same high-bitrate video set-
   2) Regression-Memory Replay: Regression-memory replay                       ting. The bitrate ladder is [3, 8, 15, 30, 60, 120] Mbps, repre-
evaluates the same candidate patch on profiles whose playback                  senting a 4K/8K-style streaming service over high-capacity
behavior should be preserved. This step distinguishes a local                  satellite access. Each video contains 48 chunks, and each
repair from a global retuning: a patch may reduce stalls                       chunk has a playback duration of 4 s [12], [13]. The maximum
on 𝐷 𝑘 but still be rejected if it lowers QoE or increases                     playback buffer is 60 s. The replay reward follows the standard
                                                                                                                                           8



                                                                    TABLE II
                                                         S TARLINK ABR TRACE INVENTORY.

         Item                                 US                      OSN                     VIC                     Total
         Measurement period          2024-04-26–2024-05-28    2024-07-13–2024-07-31   2024-07-11–2024-07-28   2024-04-26–2024-07-31
         Raw measurement runs                  16                      118                     188                      322
         Raw throughput samples            24,912,647                615,777                 148,283                25,676,707
         Raw latency samples               26,120,046                728,950                 174,962                27,023,958
         Primary satellite changes           23,291                   7,982                   1,746                   33,019
         Candidate 600-s traces              1,955                    1,026                    246                    3,227
         Valid 600-s traces                  1,954                    1,024                    243                    3,221
         Filtered invalid traces               1                        2                       3                       6
         Trace split                     1,368/293/293             717/154/153              170/37/36             2,255/484/482
         Replay rows                       1,172,400                 614,400                 145,800                1,932,600
         Replay duration (h)                 325.7                    170.7                    40.5                   536.8
         Mean TP (Mbps)                      210.1                    216.6                   171.7                   209.3
         Mean P05 TP (Mbps)                   84.7                    138.0                    98.4                   102.7
         Mean P50 TP (Mbps)                  223.2                    203.1                   171.5                   212.9
         Mean P95 TP (Mbps)                  282.1                    308.8                   243.8                   287.7



Algorithm 1 SafeLink-Agent Maintenance Procedure                         from the valid trace inventory, we construct profile batches
 1: Input: current controller 𝐶𝑣 , new profile 𝐷 𝑘 , regres-             according to region, time split, low-percentile throughput,
    sion memory M 𝑘 , Patch History H𝑣 , controller metadata             volatility, latency, and satellite-change metadata. Table III
    meta(𝐶𝑣 ), verifier constraints Γ                                    summarizes the main Starlink profiles used by the replay
 2: Replay 𝐶𝑣 on 𝐷 𝑘 using (5).                                          verifier. The initial, calibration, and future-test profiles model
 3: Compute the maintenance trigger Itrig (𝐶𝑣 , 𝐷 𝑘 ) by (12).           profile arrival over time. The high-volatility, low-tail, and high-
 4: if Itrig (𝐶𝑣 , 𝐷 𝑘 ) = 0 then                                        latency profiles expose different failure patterns. The regres-
 5:    Keep 𝐶𝑣+1 ← 𝐶𝑣 and store 𝐷 𝑘 as validated replay                  sion memory profile is selected from comparatively stable
       evidence.                                                         traces and is used only to check whether a patch damages
 6:    return 𝐶𝑣+1 and the replay report.                                previously safe operating conditions.
 7: end if                                                                   3) Controllers, Variants, and Implementation: We eval-
 8: Mine 𝑧(𝐷 𝑘 ), 𝑠(𝐶𝑣 , 𝐷 𝑘 ), Fsev , and Ftail from replay out-        uate SafeLink-Agent on both rule-based and learned ABR
    puts.                                                                controllers. The rule-based branch includes BOLA and Ro-
 9: Build maintenance context X𝑘 using (15).                             bustMPC. BOLA is controlled by buffer thresholds, and Ro-
10: Generate candidate patch 𝑝 with the agentic patch pro-               bustMPC is controlled by the prediction horizon and safety
    poser using (16).                                                    margin. The Static default variant uses one default configura-
11: Perform patch schema validation for 𝑝 using (17).                    tion for all profiles. The Static conservative variant applies one
12: if 𝑝 is not schema-valid then                                        safer configuration globally. SafeLink-Agent instead selects a
13:    Store the schema-violation reason in Patch History H𝑣 .           verified profile-conditioned patch, so that safer configurations
14:    Keep 𝐶𝑣+1 ← 𝐶𝑣 .                                                  are used only on profiles where replay evidence indicates a
15: else                                                                 severe-risk reduction without unacceptable regression.
16:    Run target-profile replay for 𝐶𝑣 ⊕ 𝑝 on 𝐷 𝑘 and check                 For BOLA, the default configuration uses a 10-s minimum
       Γtar .                                                            buffer and a 30-s target buffer, while the conservative config-
17:    Run regression-memory replay for 𝐶𝑣 ⊕ 𝑝 on M 𝑘 and                uration uses a 15-s minimum buffer and a 45-s target buffer.
       check Γmem .                                                      For RobustMPC, the default configuration uses a five-chunk
18:    if 𝑝 satisfies Γ then                                             planning horizon with safety margin 1.00. The main conserva-
19:        Commit patch 𝑝 and set 𝐶𝑣+1 ← 𝐶𝑣 ⊕ 𝑝.                         tive configuration uses a six-chunk horizon with safety margin
20:    else                                                              0.85; additional horizon and margin candidates are used only
21:        Store patch 𝑝 in Patch History H𝑣 .                           when constructing verifier upper bound or ablation variants.
22:        Keep 𝐶𝑣+1 ← 𝐶𝑣 .                                                  The learned controller branch includes SABR, Pensieve,
23:    end if                                                            and Comyco. For these controllers, SafeLink-Agent attaches
24: end if
                                                                         a policy-agnostic runtime auditor after the learned policy.
25: Output: updated controller version 𝐶𝑣+1 and replay-
                                                                         We compare three variants: No auditor, Static auditor, and
    verifier report.                                                     Adaptive auditor.
                                                                             In our implementation, SafeLink-Agent uses DeepSeek-V4-
                                                                         Pro [35] as the LLM in the agentic patch proposer. The verifier
ABR form in (6), with rebuffering penalty 𝜇 = 40 and                     constraints Γ are instantiated with the severe-session threshold
smoothness penalty 𝜂 = 1.                                                𝑏 sev = 10 s and tail fraction 𝛼 = 0.05. For the maintenance
  2) Starlink Profile Construction: The central experimental             trigger in (12), we set 𝛽sev = 1% and 𝛽tail = 10 s.
unit is a Starlink profile rather than an isolated trace. Starting           For rule-based controller patches, target-profile replay in-
                                                                                                                                                 9



                                                                     TABLE III
                                         S UMMARY OF S TARLINK PROFILES USED FOR CONTROLLER MAINTENANCE .

                    Profile                 Traces    Region Mix (US/OSN/VIC)     Mean TP      Mean P05 TP        Volatility   Latency
                                                                                   (Mbps)        (Mbps)            (Mbps)       (ms)
                    Initial deployment       192                 64/64/64           190.9            91.7           195.1           38.8
                    New calibration          484               293/154/37           200.4            88.7           205.3           29.7
                    High volatility          192                 173/18/1           197.4            54.7           251.1           30.2
                    Low tail                 192                126/50/16           123.1            18.9           211.3           38.8
                    High latency             192                106/47/39           123.1            28.2           199.1           41.0
                    Future test              482               293/153/36           192.7            85.9           198.4           30.7
                    Regression memory        192                 64/64/64           277.3           195.9           155.9           28.1



                            TABLE IV
             M AIN CONTROLLER MAINTENANCE VARIANTS .

   Variant                    Description
   Static default             Original controller configuration or policy
                              used for all profiles.
   Static conservative        One globally safer configuration used for all
                              profiles.
   SafeLink-Agent             Profile-conditioned patch accepted by target-
                              profile replay and regression-memory replay.
   Verifier upper bound       Best feasible profile-wise configuration se-
                              lected with replay evidence; used only for
                              analysis.
   Static auditor             Fixed runtime safety layer attached to a
                              learned ABR policy.
   Adaptive auditor           Runtime safety layer whose guard changes
                              with profile or failure context.



stantiates the target block Γtar in (18): the selected config-
uration must keep 𝑅sev (𝐶𝑣 ⊕ 𝑝, 𝐷 𝑘 ) ≤ 1%, reduce at least
one target-profile risk metric, i.e., 𝑅sev or 𝑇𝛼 , and keep the               Fig. 5. Rule-based controller maintenance tradeoff.
target-profile QoE loss within 𝜖 = 8%. Regression-memory
replay instantiates Γmem in (19) with 𝜖reg = 2% and 𝜁 = 0.5
percentage points; it also applies a worst-5% rebuffering-                    we additionally report QoE loss relative to the Static default
increase tolerance of 1 s.                                                    controller, QoE loss on regression memory, audit rate for
    For learned controller auditor patches, target-profile replay             learned controller auditors, and verifier acceptance or rejection.
uses 𝛿 = 0.5 percentage points for severe-session reduction,
requires non-increasing 𝑇𝛼 , and checks that more severe                      B. Rule-Based Controller Maintenance
sessions are fixed than newly introduced. The QoE-cost bound
                                                                                 This experiment evaluates whether SafeLink-Agent can
𝜖 is set to 3% for SABR and 5% for Pensieve and Comyco;
                                                                              maintain rule-based ABR controllers across newly observed
the corresponding audit-rate increase limits are 15% and 35%,
                                                                              Starlink profiles. The comparison is designed around the de-
respectively. Regression-memory replay uses the same QoE
                                                                              ployment choices faced by a fixed controller. The Static default
and audit limits, requires no severe-session increase, i.e.,
                                                                              controller preserves its original QoE-oriented configuration on
𝜁 = 0, and allows only 0.1 s tolerance in worst-5% rebuffering.
                                                                              every profile. The Static conservative controller applies one
    4) Evaluation Metrics: For a profile 𝐷 with |𝐷 | replay
                                                                              safer configuration globally. SafeLink-Agent applies a profile-
sessions, we report the average QoE and mean cumulative
                                                                              conditioned patch only when replay verification indicates that
rebuffering:
                                                                              the target-profile risk reduction does not introduce regression
  ¯            1 ∑︁                 ¯           1 ∑︁                          on profiles in regression memory.
 𝑄(𝐶,   𝐷) =            𝑄(𝐶, 𝜏), 𝐵(𝐶,   𝐷) =             𝐵(𝐶, 𝜏).
              |𝐷 | 𝜏 ∈𝐷                        |𝐷 | 𝜏 ∈𝐷                         Fig. 5 visualizes the rule-based result as a QoE loss versus
                                                             (21)             severe-risk tradeoff. In each panel, the lower-left direction
To quantify severe session-level risk, we report the fraction of              is preferred: a good maintenance outcome should reduce
sessions whose cumulative rebuffering exceeds 10 s:                           severe-session risk while keeping target-profile QoE loss or
                            1 ∑︁                                              QoE loss on regression memory small. Table V reports the
            𝑆 >10 (𝐶, 𝐷) =           1{𝐵(𝐶, 𝜏) > 10}.        (22)             corresponding exact values over all non-regression Starlink
                           |𝐷 | 𝜏 ∈𝐷
                                                                              profiles, including initial, calibration, high-volatility, low-tail,
We also report worst-5% session rebuffering, denoted by                       high-latency, and future-test profiles.
𝐵worst5 , which is the average cumulative rebuffering of the 5%                  Fig. 5 shows that Static conservative tuning and SafeLink-
sessions with the largest 𝐵(𝐶, 𝜏). For maintenance analysis,                  Agent move in the same risk reduction direction from the
                                                                                                                                                   10



                                                              TABLE V
                                    RULE - BASED CONTROLLER MAINTENANCE ACROSS S TARLINK PROFILES .

          Controller   Method                QoE     QoE Loss   Mean Rebuf      Worst-5% Rebuf        Session > 10s      Reg. QoE Loss
                                                       (%)          (s)               (s)                  (%)                (%)
          BOLA         Static default        87.42     0.00          0.70              7.23                0.63                0.00
          BOLA         Static conservative   80.57     7.84          0.55              4.26                0.23                8.05
          BOLA         SafeLink-Agent        86.34     1.24          0.62              5.63                0.40                0.00
          RobustMPC    Static default        96.58     0.00          1.08             11.77                2.60                0.00
          RobustMPC    Static conservative   94.31     2.35          0.61              4.97                0.23                0.60
          RobustMPC    SafeLink-Agent        94.95     1.68          0.66             5.70                 0.40                0.00



Static default point, but with different side effects. In the
BOLA panels, the Static conservative point is far to the right,
indicating a large QoE cost for a relatively small additional
reduction in severe-session risk. SafeLink-Agent stays closer
to the low-loss side of the plot while still moving below
the default severe-risk level. The exact values in Table V
show that Static conservative tuning reduces the BOLA severe-
session ratio from 0.63% to 0.23%, but causes 7.84% target-
profile QoE loss and 8.05% QoE loss on regression memory.
SafeLink-Agent reaches a 0.40% severe-session ratio with
only 1.24% target-profile QoE loss and zero QoE loss on
                                                                       Fig. 6. Learned controller tail-risk reduction with verified runtime auditors.
regression memory.
   The RobustMPC panels make the same tradeoff more visible
because the Static default controller has a clearer severe-               In Fig. 6, the No auditor learned controllers expose a pro-
session tail. In Fig. 5, SafeLink-Agent moves the operating            nounced severe-session tail on hard Starlink profiles. SABR,
point close to the low-risk side reached by Static conserva-           Pensieve, and Comyco have severe-session ratios of 38.47%,
tive tuning, but with smaller target-profile QoE loss and no           44.49%, and 34.07%, respectively. Their worst-5% session
QoE loss on regression memory. Numerically, SafeLink-Agent             rebuffering is also large, especially for Pensieve, whose worst-
reduces the RobustMPC severe-session ratio from 2.60% to               5% rebuffering reaches 161.05 s. After SafeLink-Agent at-
0.40%, an 84.6% reduction over the Static default. Compared            taches a verified Static auditor, the severe-session ratio de-
with Static conservative tuning, it obtains 92.8% of the severe-       creases to 12.33%, 12.33%, and 11.31% for SABR, Pensieve,
risk reduction while lowering the target QoE loss from 2.35%           and Comyco, respectively. The Adaptive auditor further re-
to 1.68% and eliminating QoE loss on regression memory from            duces the corresponding ratios to 11.01%, 10.13%, and 8.22%.
0.60% to 0.00%. These results show that SafeLink-Agent is                 Adaptive auditing usually gives the lowest severe-session
not a Static conservative fallback; it uses profile-conditioned        risk and mean rebuffering, but it increases the audit rate and
patches accepted by replay verification to reduce severe risk          can reduce QoE compared with the Static auditor. For exam-
while controlling QoE loss and avoiding regression on memory           ple, on SABR, the Adaptive auditor reduces severe sessions
profiles.                                                              from 12.33% to 11.01% compared with the Static auditor, but
                                                                       QoE decreases from 4311.30 to 4271.32, and the audit rate
                                                                       increases from 11.26% to 12.48%. On Pensieve, the auditor
C. Learned Controller Maintenance
                                                                       improves both QoE and severe risk relative to the No auditor
   This experiment evaluates whether SafeLink-Agent can                baseline, because avoiding long stalls outweighs the bitrate
maintain learned ABR controllers without retraining them               corrections. These differences support the SafeLink-Agent
from scratch. SafeLink-Agent uses a policy-agnostic runtime            design: the proposer generates a candidate auditor patch, while
auditor as the patch type: the learned policy still proposes the       replay verification determines whether the resulting QoE–risk
bitrate, and the auditor modifies only requests that violate the       operating point is acceptable for deployment.
verified safety rule.
   We compare SABR, Pensieve, and Comyco under three
operating modes. The No auditor mode evaluates the original            D. Rolling Maintenance Across Newly Observed Starlink Pro-
learned controller. The Static auditor mode attaches one ver-          files
ified safety rule to all evaluated traces. The Adaptive auditor           This experiment evaluates the maintenance process when
mode further conditions the guard on failure context, such as          Starlink profiles arrive sequentially. The evaluated sequence
low buffer or high-risk link states. Fig. 6 visualizes the severe-     is initial deployment, new calibration traces, high-volatility
session and worst-tail rebuffering trends, while Table VI              traces, low-tail traces, high-latency traces, and future-test
reports the exact values under the default severe-stall threshold      traces. At each step, the Static default controller keeps its
of 10 s and the worst-5% tail metric.                                  original configuration, the Static conservative controller keeps
                                                                                                                                              11



                                                               TABLE VI
                                     L EARNED CONTROLLER MAINTENANCE WITH VERIFIED RUNTIME AUDITORS .

                    Controller    Method                 QoE       Mean Rebuf      Worst-5% Rebuf        Session > 10s      Audit Rate
                                                                       (s)               (s)                  (%)              (%)
                    SABR          No auditor           4372.95         12.91              62.31               38.47             0.00
                    SABR          Static auditor       4311.30          3.19              23.43               12.33            11.26
                    SABR          Adaptive auditor     4271.32          2.65              21.58               11.01            12.48
                    Pensieve      No auditor           4129.85         30.39             161.05               44.49             0.00
                    Pensieve      Static auditor       4290.27          3.26              22.22               12.33            21.39
                    Pensieve      Adaptive auditor     4234.21          2.52              19.64               10.13            21.93
                    Comyco        No auditor           4427.39         10.08              51.77               34.07            0.00
                    Comyco        Static auditor       4339.09          2.81              20.04               11.31            8.11
                    Comyco        Adaptive auditor     4290.84          2.33              19.09                8.22            9.55




                                                                               Fig. 8. Stress test on handover-heavy Starlink profiles.


                                                                               the change.

                                                                               E. Handover-Heavy Starlink Stress Test
Fig. 7. Rolling maintenance across newly observed Starlink profiles.              This experiment evaluates whether the maintenance need
                                                                               is connected to Starlink-specific mobility. We use candidate-
                                                                               satellite change metadata as a serving-satellite-change proxy.
one global safe configuration, and SafeLink-Agent uses only                    Among all non-regression dynamic sessions, the top 30%
verifier-accepted profile-conditioned patches.                                 by primary candidate-satellite changes are labeled handover-
   Fig. 7 plots the cumulative number of severe sessions as                    heavy, and the remaining sessions are labeled normal. This
profiles arrive. The terminal labels report the final cumulative               split produces 521 handover-heavy sessions and 1213 normal
severe-session counts, and the verifier upper bound is included                sessions. The handover-heavy group has many more primary
only as an analysis reference; it selects the best risk-feasible               candidate-satellite changes on average, 1924.71 versus 758.52,
configuration from the existing replay sweep and is not treated                and also has a lower mean P05 throughput, 63.83 Mbps versus
as a deployable controller.                                                    72.77 Mbps. Thus, the stress set captures sessions with more
   The Static default controller accumulates severe sessions                   frequent satellite-association changes and a weaker throughput
quickly once low-tail and high-latency profiles arrive. Its                    tail.
cumulative severe-session count increases from 19 after the                       Fig. 8 summarizes the RobustMPC result. Panel (a) com-
high-volatility profile to 32 after the low-tail profile and to 42             pares the severe-session ratio on normal and handover-heavy
after the high-latency profile, ending with 45 severe sessions.                sessions, while panel (b) shows the handover-heavy QoE–
This trend shows why a one-time controller configuration can                   risk operating points. The Static default controller is sensitive
become unsafe under later Starlink profiles even if it preserves               to the mobility-heavy split: its severe-session ratio increases
high average QoE.                                                              from 1.90% on normal sessions to 4.22% on handover-heavy
   The Static conservative controller ends with only four                      sessions. This confirms that handover-heavy Starlink periods
severe sessions, but it reaches this point by applying one safe                are not merely another random subset; they amplify the severe-
configuration to every profile. SafeLink-Agent ends with seven                 session tail of a high-QoE rule-based controller.
severe sessions, reducing 38 severe sessions relative to the                      SafeLink-Agent reduces the handover-heavy severe-session
Static default controller while remaining close to the verifier                ratio from 4.22% to 0.96%. The Static conservative baseline
upper bound of nine severe sessions. The rolling trend supports                gives the lowest severe-session ratio, 0.58%, but panel (b)
the central maintenance view of this paper: the controller                     shows that it occupies a lower-QoE operating point than
should not be globally frozen or statically conservative, but                  SafeLink-Agent on the handover-heavy split, 92.84 versus
should be patched only when new profile evidence justifies                     93.39. In the rule-based main result, the Static conservative
                                                                                                                                         12



                            TABLE VII
 V ERIFIER ABLATION FOR A PROBE - ACCEPTED ROBUST MPC PROPOSAL .

   Metric              High Lat.   High Vol.   Low Tail   Initial
   Probe pass             Yes         Yes         Yes      Yes
   Full pass              No          Yes         No       Yes
   Session > 10s (%)     2.60        0.00        2.60      0.52
   QoE delta (%)         -1.37       -1.73       -1.45    -1.80
   Reject reason        Severe         –        Severe       –



configuration introduces QoE loss on regression memory,
whereas SafeLink-Agent keeps this loss at zero. The handover-
heavy result therefore supports the maintenance: when mobil-
ity changes expose a hard profile, a verified patch can reduce
severe stalls without turning the entire controller into a Static
conservative version.

F. Patch Verification and Regression Memory Analysis
   This experiment examines the acceptance logic behind
SafeLink-Agent. Since candidate patches may look reasonable
on a small number of traces, the key question is whether
SafeLink-Agent can reject proposals that fail under full re-
play or create regressions on previously stable profiles. We        Fig. 9. Mechanism case study on a hard learned controller session.
therefore analyze two mechanisms: replay verification, which
tests whether a candidate patch satisfies the target-profile
constraints, and regression memory, which prevents a patch          replay can lead to unsafe or unnecessarily regressive patch
from improving the current profile at the cost of previously        acceptance.
validated behavior.
   1) Verifier Ablation: This ablation tests whether a small
probe check can replace full replay verification. The probe         G. Hard Trace Mechanism Case Study
check runs a candidate RobustMPC patch on a small trace                This experiment inspects one hard learned controller session
subset, while the full verifier replays the same patch on the       to explain the mechanism behind the aggregate severe-risk
complete target profile. As shown in Table VII, the candidate       reduction. The selected session comes from a low-tail OSN
passes the probe on all four profiles. Full replay changes the      profile where the original learned policy produces repeated
decision: the patch is rejected on the high-latency and low-tail    large rebuffering events. We compare the same replay trace
profiles because their severe-session ratios remain above the       under three variants: the original learned controller without
verifier constraint. Therefore, a probe can screen proposals,       auditing, a verified Static auditor, and the Adaptive auditor
but it cannot decide patch commitment.                              accepted by SafeLink-Agent. Fig. 9 visualizes the chunk-level
   2) Regression Memory Ablation: The regression memory             behavior, and Table IX reports the corresponding session-level
analysis evaluates whether a target-profile repair creates unac-    outcome.
ceptable side effects on previously stable profiles. Table VIII        Fig. 9 shows how the accepted auditor patch changes the
compares the default controller, a target-only safe patch, and      session trajectory. Panel (a) first shows the safe-capacity esti-
the SafeLink-Agent patch accepted with regression memory.           mates used by the Static and Adaptive auditors. Both estimates
For BOLA, the target-only patch reduces the target severe-          expose a long low-capacity interval in the middle of the session
session ratio from 0.63% to 0.23%, but it introduces an 8.05%       and a second capacity drop near the end, which creates the
QoE regression on the memory set. SafeLink-Agent accepts            conditions for severe rebuffering if high bitrates are admitted.
a less aggressive memory-aware patch: it still reduces target       Panel (b) then shows the requested and audited bitrates. The
risk relative to the default controller, while keeping QoE loss     No auditor rollout keeps several high-bitrate requests during
on regression memory at zero. RobustMPC shows the same              the hard intervals, whereas the Static and Adaptive auditors
pattern with a smaller loss on regression memory. These results     replace part of these requests with lower audited bitrates.
indicate that regression memory changes the accepted patch,            The playback consequence appears in panels (c) and (d).
rather than only adding an after-the-fact report.                   Panel (c) shows that the No auditor rollout stays close to
   Together, these results show that both checks affect the final   the startup-buffer level during the early hard interval, which
maintenance decision. Full replay rejects patches that pass         corresponds to the sharp cumulative-rebuffering increase in
a small probe but still violate severe-risk constraints, while      panel (d). The audited rollouts build more buffer before this
regression memory changes an over-conservative target-only          early stall period, so their cumulative rebuffering remains
patch into a lower-regression patch. This ablation confirms that    much lower at the same chunks. The Static auditor, however,
removing either full replay verification or regression-memory       later suffers a pronounced buffer drop near the end of the
                                                                                                                                                       13



                                                                  TABLE VIII
                                             R EGRESSION MEMORY ANALYSIS FOR TARGET- PROFILE REPAIR .

                   Controller    Variant                          Target QoE     Worst-5% Rebuf       Session > 10s     Reg. QoE Loss
                                                                                       (s)                 (%)               (%)
                   BOLA          Static default                     87.42               7.23               0.63               0.00
                   BOLA          Target-only safe patch             80.57               4.26               0.23               8.05
                   BOLA          SafeLink-Agent with memory         86.34               5.63               0.40               0.00
                   RobustMPC     Static default                     96.58              11.77               2.60               0.00
                   RobustMPC     Target-only safe patch             94.31               4.97               0.23               0.60
                   RobustMPC     SafeLink-Agent with memory         94.95               5.70               0.40               0.00



                           TABLE IX                                               The absolute severe-session ratio changes with the thresh-
   H ARD TRACE CASE STUDY FOR A LEARNED CONTROLLER AUDITOR                     old, as expected, but the ordering remains stable. For Ro-
                            PATCH .
                                                                               bustMPC, SafeLink-Agent reduces the severe-session ratio
Variant                QoE      Rebuf      Max Chunk    Bitrate     Audit      from 4.73% to 1.90% at the 5-s threshold, from 2.60% to
                                 (s)          (s)       (Mbps)       (%)       0.40% at the 10-s threshold, and from 1.04% to 0.29% at
No auditor           1518.96    44.85        17.00       79.98       0.00      the 15-s threshold. The worst-tail metric shows the same
Static auditor       1969.76    13.26         7.25       65.71      29.17      trend under different tail fractions. For the learned controllers,
Adaptive auditor     2224.30     4.19         2.59       63.69      33.33
                                                                               the Adaptive auditor reduces the average severe-session ratio
                                                                               from 39.01% to 9.79% at the default 10-s threshold, and
                                                                               the reduction remains visible under both stricter and looser
session; the Adaptive auditor also loses buffer near the end,                  thresholds. These results show that the maintenance gain is
but the added stall is smaller. Panel (d) summarizes this differ-              robust to reasonable choices of severe-stall threshold and tail-
ence. The No auditor rollout crosses the 10-s severe-session                   risk fraction.
threshold early and reaches 44.85 s cumulative rebuffering.
The Static auditor delays and reduces the stall, but still ends
above the threshold at 13.26 s. The Adaptive auditor remains                                            VI. C ONCLUSION
below the threshold and ends at 4.19 s, turning the same hard                     This paper presented SafeLink-Agent, an agentic mainte-
trace into a non-severe session.                                               nance framework for adaptive bitrate controllers over dy-
   Table IX reports the corresponding session-level outcome.                   namic Starlink networks. We formulated Starlink ABR as a
Compared with the Static auditor, the Adaptive auditor in-                     controller-maintenance problem, where newly observed pro-
creases the intervention rate from 29.17% to 33.33%, reduces                   files expose failures that should be repaired through controller
total rebuffering from 13.26 s to 4.19 s, reduces the maximum                  updates under severe-risk, QoE cost, and regression con-
single-chunk rebuffering from 7.25 s to 2.59 s, and improves                   straints. SafeLink-Agent realizes this formulation by mining
QoE from 1969.76 to 2224.30. These values support the                          replay evidence, using an agentic patch proposer to generate
visual observation that a small increase in verified auditing                  candidate patches, and committing only the patches that pass
can materially change the stall outcome on a hard learned                      target-profile replay and regression-memory replay. This turns
controller session.                                                            newly observed Starlink failures into verifiable maintenance
   The case study shows that the learned controller patch acts                 actions that keep ABR controllers robust as the access envi-
as a targeted runtime auditor. It preserves the original policy                ronment changes. Experiments on real Starlink traces show
as the bitrate proposer, but uses the maintenance context to                   that SafeLink-Agent reduces the RobustMPC severe-session
identify requests that become risky under low buffer or low                    ratio from 2.60% to 0.40%, lowers cumulative severe sessions
safe capacity. The behavior explains the aggregate learned                     from 45 to 7 in rolling maintenance, and reduces the learned
controller result: verified auditor patches can reduce severe-                 controller average severe-session ratio from 39.01% to 9.79%.
session tails by correcting a small set of high-risk decisions                 These results show that SafeLink-Agent can combine LLM-
rather than replacing the underlying ABR policy.                               assisted patch generation with replay verification for auto-
                                                                               mated maintenance and localized repair of ABR controllers,
H. Sensitivity Analysis                                                        reducing severe-session failures without repeated manual re-
                                                                               tuning or retraining under dynamic Starlink access. Future
   This experiment evaluates whether the maintenance con-
                                                                               work will investigate broader agentic maintenance across pre-
clusion depends on a single severe-stall threshold or tail
                                                                               diction, control, and application-layer optimization modules in
fraction. We vary the severe-session threshold from 5 s to
                                                                               satellite networking systems.
15 s and the worst-tail fraction from 1% to 10%. Table X
reports a compact summary. For rule-based controllers, we
use RobustMPC because it is the clearest rule-based case in                                                 R EFERENCES
the main result. For learned controllers, we report the average
                                                                                [1] F. Michel, M. Trevisan, D. Giordano, and O. Bonaventure, “A first look
over SABR, Pensieve, and Comyco to summarize the effect                             at Starlink performance,” in Proceedings of the 22nd ACM Internet
of the verified Adaptive auditor.                                                   Measurement Conference, 2022, pp. 130–136.
                                                                                                                                                             14



                                                                        TABLE X
                                         S ENSITIVITY TO SEVERE - STALL THRESHOLD AND WORST- TAIL FRACTION .

                          Branch           Method               > 5s     > 10s    > 15s     Worst-1%       Worst-5%      Worst-10%
                                                                (%)       (%)      (%)         (s)            (s)           (s)
                          RobustMPC        Static default       4.73      2.60     1.04        22.17         11.77           7.32
                          RobustMPC        SafeLink-Agent       1.90      0.40     0.29        12.69         5.70            3.59
                          Learned avg.     No auditor           48.60    39.01    32.65       117.52         91.71           78.29
                          Learned avg.     Adaptive auditor     13.80     9.79     4.16        26.71         20.10           16.03



 [2] M. M. Kassem, A. Raman, D. Perino, and N. Sastry, “A browser-side                 information-theoretic meta-reinforcement learning,” IEEE Transactions
     view of starlink connectivity,” in Proceedings of the 22nd ACM Internet           on Circuits and Systems for Video Technology, pp. 1–17, 2025.
     Measurement Conference, 2022, pp. 151–158.                                   [20] OpenAI, “GPT-4 technical report,” arXiv preprint arXiv:2303.08774,
 [3] B. Guo, Z. Zhang, S. Atapattu, M. Pan, Y. Yan, Z. Xiong, and H. Li,               2023.
     “Enabling real-time computing and transmission services in large-scale       [21] ——, “OpenAI o1 system card,” 2024. [Online]. Available: https:
     LEO satellite networks,” IEEE Transactions on Vehicular Technology,               //arxiv.org/abs/2412.16720
     vol. 74, no. 8, pp. 12 813–12 828, 2025.                                     [22] D. Wu, X. Wang, Y. Qiao, Z. Wang, J. Jiang, S. Cui, and F. Wang,
 [4] Z. Han, C. Xu, G. Zhao, S. Wang, K. Cheng, and S. Yu, “Time-varying               “NetLLM: Adapting large language models for networking,” in Pro-
     topology model for dynamic routing in LEO satellite constellation                 ceedings of the ACM SIGCOMM 2024 Conference, 2024, pp. 661–678.
     networks,” IEEE Transactions on Vehicular Technology, vol. 72, no. 3,        [23] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan,
     pp. 3440–3454, 2023.                                                              and O. Press, “SWE-agent: Agent-computer interfaces enable automated
 [5] S. Li, G. Lu, L. Zhen, D. Feng, K. Yu, and D. W. K. Ng, “Block-cyclic             software engineering,” in Advances in Neural Information Processing
     zadoff–chu sequences-based preamble design and detection for OTFS-                Systems, vol. 37, 2024.
     enabled LEO satellite random access systems,” IEEE Transactions on           [24] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury, “AutoCodeRover:
     Vehicular Technology, vol. 75, no. 3, pp. 5179–5184, 2026.                        Autonomous program improvement,” in Proceedings of the 33rd ACM
 [6] Y. Wang, T. Ma, X. Qin, X. Zhang, Z. Zhang, and H. Zhou, “Satellite–              SIGSOFT International Symposium on Software Testing and Analysis,
     aircraft handover in ultra-dense LEO satellite networks,” IEEE Trans-             2024, pp. 1592–1604.
     actions on Vehicular Technology, vol. 74, no. 3, pp. 4946–4961, 2025.        [25] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and
                                                                                       K. Narasimhan, “SWE-bench: Can language models resolve real-world
 [7] Y. Huang, J. Li, M. Zhang, Y. Wu, W. Fan, and D. Wang, “A dual
                                                                                       GitHub issues?” in International Conference on Learning Representa-
     threshold handover scheme for improved service stability in large-scale
                                                                                       tions, 2024.
     optical satellite networks,” IEEE Transactions on Vehicular Technology,
                                                                                  [26] C. S. Xia, Y. Deng, S. Dunn, and L. Zhang, “Agentless: Demystifying
     vol. 75, no. 1, pp. 1398–1411, 2026.
                                                                                       LLM-based software engineering agents,” Proceedings of the ACM on
 [8] J. Garcia, S. Sundberg, G. Caso, and A. Brunstrom, “Multi-timescale
                                                                                       Software Engineering, vol. 2, no. FSE, pp. 1–24, 2025.
     evaluation of starlink throughput,” in Proceedings of the 1st ACM
                                                                                  [27] P. Las-Casas, A. G. Kumbhare, R. Fonseca, and S. Agarwal, “LLexus:
     Workshop on LEO Networking and Communication, 2023, pp. 31–36.
                                                                                       An AI agent system for incident management,” ACM SIGOPS Operating
 [9] Z. Liu, F.-X. G. Reidys, S. Tanveer, and D. Vasisht, “Vivisecting starlink        Systems Review, vol. 58, no. 1, pp. 23–36, 2024.
     throughput: Measurement and prediction,” Proceedings of the ACM on           [28] J. Weng, “Learning beyond gradients,” https://trinkle23897.github.io/
     Networking, vol. 3, no. CoNEXT4, pp. 1–23, 2025.                                  learning-beyond-gradients/, may 2026, blog post.
[10] X. Yin, A. Jindal, V. Sekar, and B. Sinopoli, “A control-theoretic           [29] G. Lv, Q. Wu, W. Wang, Z. Li, and G. Xie, “Lumos: Towards better
     approach for dynamic adaptive video streaming over HTTP,” in Pro-                 video streaming QoE through accurate throughput prediction,” in IEEE
     ceedings of the 2015 ACM Conference on Special Interest Group on                  INFOCOM 2022 - IEEE Conference on Computer Communications.
     Data Communication, 2015, pp. 325–338.                                            IEEE, 2022, pp. 650–659.
[11] K. Spiteri, R. Urgaonkar, and R. K. Sitaraman, “BOLA: Near-optimal           [30] G. Lv, Q. Wu, Q. Tan, W. Wang, Z. Li, and G. Xie, “Accurate throughput
     bitrate adaptation for online videos,” IEEE/ACM Transactions on Net-              prediction for improving QoE in mobile adaptive streaming,” IEEE
     working, vol. 28, no. 4, pp. 1698–1711, 2020.                                     Transactions on Mobile Computing, vol. 23, no. 5, pp. 5799–5817, 2024.
[12] H. Mao, R. Netravali, and M. Alizadeh, “Neural adaptive video stream-        [31] P. Luo, Y. Zhao, B. Zhang, G. Yang, B.-H. Soong, and C. Yuen, “Sabr:
     ing with pensieve,” in Proceedings of the Conference of the ACM Special           A stable adaptive bitrate framework using behavior cloning pretraining
     Interest Group on Data Communication, 2017, pp. 197–210.                          and reinforcement learning fine-tuning,” in 2026 IEEE Wireless Com-
[13] T. Huang, C. Zhou, R.-X. Zhang, C. Wu, X. Yao, and L. Sun, “Comyco:               munications and Networking Conference (WCNC). IEEE, 2026, pp.
     Quality-aware adaptive video streaming via imitation learning,” in                1–6.
     Proceedings of the 27th ACM International Conference on Multimedia,          [32] H. Zhao, H. Fang, F. Wang, and J. Liu, “Realtime multimedia services
     2019, pp. 429–437.                                                                over starlink: A reality check,” in Proceedings of the 33rd Workshop on
[14] Z. Xia, Y. Zhou, F. Y. Yan, and J. Jiang, “Genet: Automatic curriculum            Network and Operating System Support for Digital Audio and Video,
     generation for learning adaptation in networking,” in Proceedings of the          2023, pp. 43–49.
     ACM SIGCOMM 2022 Conference, 2022, pp. 397–413.                              [33] J. Zhao and J. Pan, “Low-latency live video streaming over a low-earth-
[15] L. Yi, Y. Qin, and R. Huang, “Optimizing adaptive video streaming:                orbit satellite network with DASH,” in Proceedings of the 15th ACM
     Offline reinforcement learning and meta-learning in diverse networks,”            Multimedia Systems Conference, 2024, pp. 109–120.
     IEEE Transactions on Multimedia, vol. 27, pp. 8185–8198, 2025.               [34] X. Han, S. Yuan, and M. Trabelsi, “LogGPT: Log anomaly detection via
     [Online]. Available: https://jglobal.jst.go.jp/en/detail?JGLOBAL_ID=              GPT,” in 2023 IEEE International Conference on Big Data (BigData),
     202502299348451593                                                                2023, pp. 1117–1122.
[16] A. Bentaleb, M. Lim, M. N. Akcay, A. C. Begen, and R. Zimmermann,            [35] DeepSeek-AI, “DeepSeek-V4: Towards highly efficient million-
     “Meta reinforcement learning for rate adaptation,” in IEEE INFOCOM                token     context    intelligence,”   https://huggingface.co/deepseek-ai/
     2023-IEEE Conference on Computer Communications. IEEE, 2023,                      DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf,            2026,     technical
     pp. 1–10.                                                                         report.
[17] ——, “Bitrate adaptation and guidance with meta reinforcement learn-
     ing,” IEEE Transactions on Mobile Computing, vol. 23, no. 11, pp.
     10 378–10 392, 2024.
[18] W. Li, X. Li, Y. Xu, Y. Yang, and S. Lu, “MetaABR: A meta-learning
     approach on adaptative bitrate selection for video streaming,” IEEE
     Transactions on Mobile Computing, vol. 23, no. 3, pp. 2422–2437, 2024.
[19] N. Kan, C. Li, Y. Jiang, W. Dai, J. Zou, H. Xiong, and L. Toni,
     “MERINA+: Improving generalization for neural video adaptation via
                                                                                                                               15



                S UPPLEMENTARY M ATERIAL                           C. Patch Records
                    S1. M AIN N OTATION                                The proposer output is parsed into a JavaScript Object
                                                                   Notation (JSON)-like record with typed fields. Table S3 gives
  Table S1 summarizes the notation used in the controller-
                                                                   compact examples of candidate patch records across the con-
maintenance formulation and SafeLink-Agent design.
                                                                   troller classes considered in this paper. These examples make
                                                                   explicit that the proposer output names the controller, states
         S2. AGENT P ROMPT AND PATCH D ETAILS                      when the patch is activated, selects an allowed operation, and
   This supplementary material records the proposer interface      fills only bounded parameters.
in SafeLink-Agent. It specifies the structured context provided        Table S4 shows a concrete RobustMPC patch output in the
to the proposer, the prompt template, and representative candi-    same record style. A candidate that misses a required field,
date patch outputs. These details support the reproduction of      uses an unsupported operation, or violates parameter bounds
the proposal-generation step used in the maintenance work-         is rejected before replay.
flow.

A. Structured Prompt Context
   The prompt uses compact summaries instead of full raw
traces. When multiple proposal rounds are needed, SafeLink-
Agent reuses the same template and updates Patch History
with the accepted or rejected patches and their verifier feed-
back. Table S2 gives an example of the structured context
seen by the agentic patch proposer. The concrete values are
compacted from replay statistics, controller metadata, patch
schemas, verifier constraints, regression memory, and Patch
History.

B. Prompt Template
   The prompt is organized as an instruction-following mainte-
nance task. In our implementation, DeepSeek-V4-Pro receives
a system instruction, structured context, patch schema, verifier
constraints, and output-format requirement. The same template
is reused across proposal rounds, while Patch History provides
the feedback from previous replay-verification results. The
template below shows the structure.
SYSTEM:
You are a controller maintenance proposer for ABR.
Suggest only candidate patches
allowed by the schema.
Do not output per-chunk bitrate actions.

TASK:
Given a new Starlink profile and replay evidence,
propose one patch that reduces severe sessions while
avoiding QoE regression on memory profiles.

INPUT:
1) profile_summary
2) failure_summary
3) controller_metadata
4) patch_schema
5) verifier_constraints
6) regression_memory_summary
7) patch_history

CONSTRAINTS:
- Use only approved patch type and features.
- Keep all parameters inside candidate bounds.
- Satisfy target-profile risk and QoE limits.
- Satisfy regression-memory limits.
- Prefer localized profile-conditioned repairs.
- Explain expected target improvement and risk.

OUTPUT:
Return one candidate patch and rationale.
                                                                                                                                                                          16




                                                                            TABLE S1
                                                         M AIN NOTATION USED IN CONTROLLER MAINTENANCE .

Symbol                              Meaning                                                Symbol                       Meaning
𝑡, 𝑇                                Chunk index and number of chunks in one 𝜏𝑘, 𝑗 , 𝐷 𝑘 , 𝑛𝑘                            The 𝑗th replay session, the 𝑘th Starlink profile,
                                    streaming session.                                                                  and the number of sessions in 𝐷 𝑘 .
                                                                                      tp
𝑧 (𝐷 𝑘 )                            Metadata summary of Starlink profile 𝐷 𝑘 . 𝜇tp , 𝑞0.05 , 𝜎tp                        Mean throughput, 5th-percentile throughput,
                                                                                                                        and throughput volatility.
𝜇lat , 𝐻ho                          Mean latency and handover or serving-satellite M, M 𝑘 , Smem                        Regression memory, memory for profile 𝐷 𝑘 ,
                                    change intensity.                                                                   and retained representative sessions.
𝐶, 𝐶𝑣 , 𝐶𝑣+1                        ABR controller, current controller version, and 𝐶𝑣 ⊕ 𝑝                              Controller obtained by applying patch 𝑝 to 𝐶𝑣 .
                                    committed next version.
Replay(𝐶, 𝜏 ), ℓ (𝐶, 𝜏 )            Replay interface and replay log.                𝑄 (𝐶, 𝜏 ), 𝐵(𝐶, 𝜏 )                 Session QoE and cumulative rebuffering under
                                                                                                                        controller 𝐶.
𝑎𝑡 , 𝑢(𝑎𝑡 ), 𝜌𝑡                     Bitrate action, bitrate utility, and chunk rebuffer-   𝜇, 𝜂                         Rebuffering and bitrate-smoothness penalty
                                    ing.                                                                                weights.
𝑄¯ (𝐶, 𝐷), 𝐵(𝐶,
           ¯    𝐷)                  Profile-level mean QoE and mean cumulative             𝑅sev (𝐶, 𝐷)                  Severe-session ratio of controller 𝐶 on profile
                                    rebuffering.                                                                        𝐷.
𝑇𝛼 (𝐶, 𝐷), Tail 𝛼 (𝐶, 𝐷)            Worst-tail rebuffering metric and the worst 𝛼          𝑏sev , 𝛼                     Severe-stall threshold and tail fraction.
                                    fraction of sessions.
𝑝, P, Ω( 𝑝)                         Candidate patch, admissible patch space, and           Schema𝐶𝑣 ( 𝑝)                Patch schema validation test for controller ver-
                                    patch complexity.                                                                   sion 𝐶𝑣 .
Itrig                               Maintenance-trigger indicator.                         𝛽sev , 𝛽tail                 Trigger thresholds for severe-session ratio and
                                                                                                                        worst-tail rebuffering.
𝑠 (𝐶, 𝐷), X𝑘                        Failure summary and maintenance context for 𝑁sev , 𝜌audit                           Number of severe sessions and audit-
                                    profile 𝐷 𝑘 .                                                                       intervention rate.
Fsev , Ftail                        Severe-session set and worst-tail session set. 𝐺 𝜃 , H𝑣                             Agentic patch proposer and Patch History.
meta(𝐶𝑣 )                           Controller metadata supplied to the proposer.  Γ, Γtar , Γmem                       Verifier constraints and their target-profile and
                                                                                                                        regression-memory blocks.
𝐷new                                Newly exposed target profile in the verifier 𝛿, 𝛾                                   Required severe-risk and tail-risk improve-
                                    constraints.                                                                        ments.
𝜖 , 𝜖reg                            Allowed QoE loss on the target profile and 𝜁 , 𝜅                                    Allowed severe-risk increase on regression
                                    regression memory.                                                                  memory and patch-complexity budget.




                                                                        TABLE S2
                                            E XAMPLE STRUCTURED CONTEXT PROVIDED TO THE AGENTIC PATCH PROPOSER .

        Context Field                         Example Value Provided to the Agent
        Profile summary                       profile_id: osn_low_tail; region: OSN; num_sessions: 173; p05_throughput: 63.8 Mbps;
                                              latency_p95: 78 ms; tags: [low-tail, high-latency].
        Failure summary                       controller: RobustMPC-v0; session_gt10s: 2.60%; worst5_rebuf: 11.77 s; symptoms: [aggressive
                                              high-bitrate request, buffer depletion after throughput drop].
        Controller metadata                   class: RobustMPC; version: v0; allowed_knobs: horizon ∈ {4, 5, 6}, margin ∈ {0.80, 0.85, 0.90}, bitrate
                                              cap ∈ {30, 60, 120} Mbps.
        Patch schema                          allowed_type:           profile-conditioned      rule;   operation: select admissible   configuration;
                                              activation_features: [throughput tail, volatility, latency]; max_rules: 2.
        Verifier constraints                  target_session_gt10s: ≤ 1%; target_qoe_loss: ≤ 8%; memory_qoe_loss: ≤ 2%;
                                              memory_session_increase: ≤ 0.5 pp; memory_worst5_increase: ≤ 1 s.
        Regression memory                     memory_profiles: [initial, high-volatility]; reference_qoe: 96.58; reference_session_gt10s:
                                              0.00%; anchor_sessions: 96.
        Patch History                         accepted: low-tail rule #3; rejected: global-safe rule #2; last_reject_reason: QoE loss on regression
                                              memory = 8.05%.




                                                                       TABLE S3
                                       E XAMPLE CANDIDATE PATCH RECORDS GENERATED BY THE AGENTIC PATCH PROPOSER .

 Controller                    Patch Type                      Activation Condition                        Operation                              Bounded Parameters
 BOLA                          Profile-conditioned configu-    Activate on low-tail or high-volatility     Select a buffer-threshold configura-   Lower buffer = 15 s;
                               ration                          profiles with severe-session evidence.      tion for the matching profile.         upper buffer = 45 s.
 RobustMPC                     Profile-conditioned configu-    Activate on low-tail or high-latency pro-   Select prediction horizon, safety      Horizon = 5; margin
                               ration                          files with repeated buffer depletion.       margin, and bitrate cap from ad-       = 0.85; bitrate cap =
                                                                                                           missible candidates.                   60 Mbps.
 Learned ABR                   Runtime auditor patch           Activate when low buffer and low safe       Attach or tune a runtime auditor       Safe-capacity margin
                                                               capacity make the requested bitrate         while leaving the learned policy       = 0.90; buffer guard
                                                               risky.                                      unchanged.                             = 1.0 s.
                                                                                                                                            17




                                                TABLE S4
                    E XAMPLE ROBUST MPC PATCH OUTPUT FROM THE AGENTIC PATCH PROPOSER .

Patch Field             Example Output Value
type                    profile_conditioned_rule
target_controller       RobustMPC-v0
condition               Activate when profile.tag contains low-tail or high-latency and p05_throughput < 65 Mbps.
operation               Select an admissible safe configuration for the matching profile; do not change per-chunk bitrate actions.
parameters              horizon: 5; safety_margin: 0.85; bitrate_cap: 60 Mbps; max_activation_rules: 1.
verifier_goals          Reduce session_gt10s on the target profile; keep QoE loss on regression memory ≤ 0.5%; do not increase
                        memory severe-session ratio.
rationale               The target profile shows a weak throughput tail and repeated buffer-depletion events after high-bitrate requests.
                        The patch should reduce aggressive requests only on matching profiles.
