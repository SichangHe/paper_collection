                                                   Unifying Qualitative and Quantitative Safety
                                                     Verification of DNN-Controlled Systems

                                                    Dapeng Zhi1 , Peixin Wang†2 , Si Liu3 , Luke Ong2 , and Min Zhang1
                                                                          1 East China Normal University
                                                                             zhi.dapeng@163.com
                                                                          zhangmin@sei.ecnu.edu.cn
arXiv:2404.01769v1 [cs.LG] 2 Apr 2024




                                                                       2 Nanyang Technological University
                                                                     {peixin.wang,luke.ong}@ntu.edu.sg
                                                                                3 ETH Zurich
                                                                             si.liu@inf.ethz.ch



                                                 Abstract. The rapid advance of deep reinforcement learning techniques enables
                                                 the oversight of safety-critical systems through the utilization of Deep Neural
                                                 Networks (DNNs). This underscores the pressing need to promptly establish cer-
                                                 tified safety guarantees for such DNN-controlled systems. Most of the existing
                                                 verification approaches rely on qualitative approaches, predominantly employ-
                                                 ing reachability analysis. However, qualitative verification proves inadequate for
                                                 DNN-controlled systems as their behaviors exhibit stochastic tendencies when
                                                 operating in open and adversarial environments. In this paper, we propose a novel
                                                 framework for unifying both qualitative and quantitative safety verification prob-
                                                 lems of DNN-controlled systems. This is achieved by formulating the verifica-
                                                 tion tasks as the synthesis of valid neural barrier certificates (NBCs). Initially, the
                                                 framework seeks to establish almost-sure safety guarantees through qualitative
                                                 verification. In cases where qualitative verification fails, our quantitative verifica-
                                                 tion method is invoked, yielding precise lower and upper bounds on probabilistic
                                                 safety across both infinite and finite time horizons. To facilitate the synthesis
                                                 of NBCs, we introduce their 𝑘-inductive variants. We also devise a simulation-
                                                 guided approach for training NBCs, aiming to achieve tightness in computing
                                                 precise certified lower and upper bounds. We prototype our approach into a tool
                                                 called UniQQ and showcase its efficacy on four classic DNN-controlled systems.


                                        1     Introduction
                                        The widespread adoption of deep reinforcement learning techniques has propelled ad-
                                        vancements in autonomous systems, endowing them with adaptive decision-making ca-
                                        pabilities by Deep Neural Networks (DNNs) [34]. Ensuring the safety of these DNN-
                                        controlled systems emerges as a critical concern, necessitating the provision of certified
                                        safety guarantees. Formal methods, renowned for their rigorousness and automaticity
                                        † Corresponding author


                                            This work is a technical report for the paper with the same name to appear in the 36th Interna-
                                            tional Conference on Computer Aided Verification (CAV 2024).
2       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

in delivering verified safety assurances, stand as a promising means to address this con-
cern. However, most of the existing formal verification approaches rely on qualitative
approaches, predominantly employing reachability analysis [46]. Despite their signif-
icance, qualitative results fall short for DNN-controlled systems due to the constant
influence of various uncertainties from different sources, such as environment noises
[67], unreliable sensors [54], and even malicious attacks [66]. When qualitative verifi-
cation fails, it becomes both desirable and practical to obtain quantitative guarantees,
including quantified lower and upper bounds on the safety probabilities of the systems.
This necessitates the use of quantitative verification engines [46].
     Quantitative verification has proven its efficacy in enhancing the design and de-
ployment across a variety of applications, including autonomous systems [31], self-
adaptive systems [12], distributed communication protocols [24], and probabilistic pro-
grams [56]. These applications are commonly modeled using automata-based quanti-
tative formalisms [23], such as Markov chains, timed automata, and hybrid automata,
and undergo verification using tools such as Prism [30] and Storm [25]. Nonetheless,
the quantitative verification of DNN-controlled systems is challenging due to the incor-
poration of intricate and almost inexplicable decision-making models by DNNs [45].
Compounding the issue, the difficulty is amplified by the continuous and infinite state
space, as well as the non-linear dynamics inherent in DNN-controlled systems. First,
building a faithful automata-based probabilistic model for a DNN-controlled system is
challenging. This difficulty arises as one cannot predict the action a DNN might take
until a specific state is provided, and exhaustively enumerating all continuous states
is impractical. Second, even if such a model is constructed under certain constraints,
such as bounded steps [7] and state abstractions [29], verification is susceptible to state
exploration issues—a well-known problem in model checking[51]. For instance, the
verification process can take up to 50 minutes for just 7 steps [7].
     Leveraging barrier certificates (BCs) for verification emerges as a promising tech-
nique for formally establishing the safety of non-linear and stochastic systems [41,32].
A BC partitions the state space of the system into two parts, ensuring that all trajecto-
ries starting from a given initial set, located within one side of the BC, cannot reach a
given set of states (deemed to be unsafe), located on the other side, almost surely (i.e.,
with probability 1) or with probability at least 𝑝 ∈ [0, 1). Once a BC is computed, it
can be used to certify systems’ safety properties either qualitatively or quantitatively.
Recently, studies have shown that BCs can be implemented and trained in neural forms
called Neural Barrier Certificates (NBCs). NBCs facilitate the synthesis of BCs and
improve their expressiveness [69,36,57,37,1]. A relevant survey is delegated to [16].
     In this paper, we propose a unified framework for both qualitatively and quantita-
tively verifying the safety of DNN-controlled systems by leveraging NBCs. The key
idea is to reduce both qualitative and quantitative verification problems into a cohesive
synthesis task of their respective NBCs. Specifically, we first seek to establish almost-
sure safety guarantees through qualitative verification. In cases where qualitative verifi-
cation fails, our quantitative verification method is invoked, yielding precise lower and
upper bounds on probabilistic safety across both infinite and finite time horizons.
     We also establish relevant theoretical results. In qualitative verification, we prove
that an NBC satisfying corresponding conditions serves as a qualitative safety certifi-
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems      3

cate. In the quantitative counterpart, we establish that valid NBCs can be utilized to
calculate certified upper and lower bounds on the probabilistic safety of systems, en-
compassing both infinite and finite time horizons. For infinite time horizons, as the
lower bounds on probabilistic safety approach zero, indicating a decreasing trend in
safety probabilities along the time horizon, we provide both linearly and exponentially
decreasing lower and upper bounds on the safety probabilities over finite time horizons.
    To facilitate the synthesis of valid NBCs, we further relax their constraints by defin-
ing their 𝑘-inductive variants [4]. This necessitates the conditions to be inductive for
𝑘-compositions of the transition relation within a specified bound 𝑘 [10]. Consequently,
synthesizing a qualified NBC becomes more manageable under these 𝑘-inductive con-
ditions, while ensuring safety guarantees. As valid NBCs are not unique and yield
different certified bounds, we devise a simulation-guided approach to train potential
NBCs. This approach aims to enhance their capability to produce more precise certified
bounds. Specifically, we estimate safety probabilities through simulation. The differ-
ences between the simulation results and the bounds provided by potential NBCs are
incorporated into the loss function. This integration can yield more precise certified
bounds after potential NBCs are successfully validated.
    We prototype our approach into a tool, called UniQQ, and apply it to four classic
DNN-controlled problems. The experimental results showcase the effectiveness of our
unified verification approach in delivering both qualitative and quantitative safety guar-
antees across diverse noise scenarios. Additionally, the results underscore the efficacy
of 𝑘-inductive variants in reducing verification overhead, by 25% on average, and that
of our simulation-based training method in yielding tighter safety bounds, with an up
to 47.5% improvement over ordinary training approaches.
Contributions. Overall, we make the following contributions.
 1. We present a novel framework that unifies both qualitative and quantitative safety
    verification of DNN-controlled systems by reducing these verification problems
    into the cohesive task of synthesizing NBCs.
 2. We establish relevant theoretical results, including new constraints of NBCs for
    both qualitative and quantitative safety verification and the associated lower and
    upper bounds for safety probabilities in both linear and exponential forms.
 3. To accelerate training, we relax the constraints of NBCs by introducing their 𝑘-
    inductive variants. We also present a simulation-guided approach designed to train
    potential NBCs to compute safety bounds as tightly as possible.
 4. We develop a prototype of our approach, showcasing its efficacy across four classic
    DNN-controlled systems.
All omitted proofs and supplementary experimental results are given in the Appendix.

2     Preliminaries
Let N, Z, and R be the sets of natural numbers, integers, and real numbers, respectively.
2.1   DNN-controlled Systems
We consider DNN-controlled systems where the control policies are implemented by
deep neural networks and suppose the networks are trained for specific tasks. Formally,
4        Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

a DNN-controlled system is a tuple 𝑀 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅), where 𝑆 ⊆ R𝑛 is the set of
(possibly continuous and infinite) system states, 𝑆0 ⊆ 𝑆 is the set of initial states, 𝐴 is
the set of actions, 𝜋 : 𝑆 → 𝐴 is the trained policy implemented by a neural network,
 𝑓 : 𝑆 × 𝐴 → 𝑆 is the system dynamics, and 𝑅 : 𝑆 × 𝐴 × 𝑆 → R is the reward function.
Trajectories. A trained DNN-controlled system 𝑀 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅) is a decision-
making system that continuously interacts with the environment. At each time step
𝑡 ∈ N0 , it observes a state 𝑠𝑡 and feeds 𝑠𝑡 into its planted NN to compute the optimal
action 𝑎 𝑡 = 𝜋(𝑠𝑡 ) that shall be taken. Action 𝑎 𝑡 is then performed, which transits 𝑠𝑡
into the next state 𝑠𝑡+1 = 𝑓 (𝑠𝑡 , 𝑎 𝑡 ) via the system dynamics 𝑓 and earns a reward
𝑟 𝑡+1 = 𝑅(𝑠𝑡 , 𝑎 𝑡 , 𝑠𝑡+1 ). Given an initial state 𝑠0 ∈ 𝑆0 , a sequence of states generated
during interaction is called a trajectory, denoted as 𝜔 = {𝑠𝑡 }𝑡 ∈N0 . To ease the notation,
we denote by 𝜔𝑡 the 𝑡-th element of 𝜔, i.e., 𝜔𝑡 = 𝑠𝑡 , and by Ω the set of all trajectories.
State Perturbations. As DNN-controlled systems collect state information via sensors,
uncertainties inevitably originate from sensor errors, equipment inaccuracy, or even ad-
versarial attacks [67,65]. Therefore, the observed states of the systems can be perturbed
and actions are computed based on the perturbed states. Formally, an observed state
at time step 𝑡 is 𝑠ˆ𝑡 := 𝑠𝑡 + 𝛿𝑡 where 𝛿𝑡 ∼ 𝜇 is a random noise and 𝜇 is a probability
distribution over R𝑛 . We denote by 𝑊 := supp (𝜇) the support of 𝜇. Due to pertur-
bation, the actual successor state is 𝑠𝑡+1 := 𝑓 (𝑠𝑡 , 𝑎ˆ 𝑡 ) with 𝑎ˆ 𝑡 := 𝜋( 𝑠ˆ𝑡 ) and the reward
is 𝑟 𝑡+1 := 𝑅(𝑠𝑡 , 𝑎ˆ 𝑡 , 𝑠𝑡+1 ). Note that the successor state and the reward are calculated
according to the actual state and the action on the perturbed state, and this update is
common [67]. We then denote a DNN-controlled system 𝑀 perturbed by a noise distri-
bution 𝜇 as 𝑀 𝜇 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅, 𝜇).
Assumptions. Given a DNN-controlled system 𝑀 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅), we assume that
the state space 𝑆 is compact in the Euclidean topology of R𝑛 , its system dynamics 𝑓
and trained policy 𝜋 are Lipschitz continuous. This assumption is common in control
theory [70]. For perturbation, we assume that the noise distribution 𝜇 either has bounded
support or is a product of independent univariate distributions.
Probability Space. Given a DNN-controlled system 𝑀 𝜇 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅, 𝜇), for
each initial state 𝑠0 ∈ 𝑆0 , there exists a probability space (Ω𝑠0 , F𝑠0 , P𝑠0 ) such that Ω𝑠0
is the set of all trajectories starting from 𝑠0 by the environmental interaction, F𝑠0 is a
𝜎-algebra over Ω𝑠0 (i.e., a collection of subsets of Ω𝑠0 that contains the empty set ∅
and is closed under complementation and countable union), and P𝑠0 : F𝑠0 → [0, 1]
is a probability measure on F𝑠0 . We denote the expectation operator in this probability
space by E𝑠0 .

2.2   Barrier Certificate and its Neural Implementation

Barrier certificates (BCs) are powerful tools to certify the safety of continuous-time
dynamical systems. In the following we describe the discrete-time BCs which this work
is based upon. We refer readers to [40,42] for details about continuous-time BCs.

Definition 1 (Discrete-time Barrier Certificates). Given a DNN-controlled system
𝑀 = (𝑆, 𝑆0 , 𝐴, 𝑓 , 𝜋, 𝑅) with an unsafe set 𝑆𝑢 ⊆ 𝑆 such that 𝑆𝑢 ∩ 𝑆0 = ∅. A discrete-
time barrier certificate is a real-valued function 𝐵 : 𝑆 → R such that for some constant
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems             5

𝜆 ∈ (0, 1], it holds that:

             𝐵(𝑠) ≤ 0                                               for all 𝑠 ∈ 𝑆0 ,          (1)
             𝐵(𝑠) > 0                                               for all 𝑠 ∈ 𝑆𝑢 ,          (2)
             𝐵( 𝑓 (𝑠, 𝜋(𝑠))) − 𝐵(𝑠) + 𝜆 · 𝐵(𝑠) ≤ 0                   for all 𝑠 ∈ 𝑆.           (3)

     If there exists such a BC for the system 𝑀, then 𝑀 is safe, i.e., the system cannot
reach a state in the unsafe set 𝑆𝑢 from the initial set 𝑆0 . The intuition is that: Con-
dition (3) implies that for any 𝑠 ∈ 𝑆 such that 𝐵(𝑠) ≤ 0, 𝐵( 𝑓 (𝑠, 𝜋(𝑠))) ≤ 0. Since
Condition (1) asserts that the initial value of 𝐵 is not greater than zero, any trajectory
𝜔 ∈ Ω𝑠0 starting from an initial state 𝑠0 ∈ 𝑆0 cannot enter the unsafe set 𝑆𝑢 , where
𝐵(𝑠) > 0 (see Condition (2)), thereby ensuring the safety of the system.
     Finding a BC is restricted to the expressiveness of templates. For example, even
if there exists a function satisfying Conditions (1) to (3), it may be not found under
polynomial forms. Recent work [69,39,68] proposes a neural implementation of BCs
as deep neural networks, leveraging the expressiveness of neural networks. The neural
implementation of a BC is called a neural barrier certificate (NBC), which consists of
training and validation. First, a learner trains a neural network (NN) to fit over a finite
set of samples the conditions for a BC. After training, an NBC is then checked whether
it meets the conditions. This is achieved by a verifier using SMT solvers [69,39] or other
methods like Sum-of-Squares programming [68]. If the validation result is false, a set of
counterexamples can be generated for future training. This iteration is repeated until a
trained candidate is validated or a given timeout is reached. This training and validation
iteration is called CounterExample-Guided Inductive Synthesis (CEGIS) [2].

3     Verification Problem and Our Framework
3.1   Problem Statement
We consider the safety of DNN-controlled systems from both qualitative and quantita-
tive perspectives. Below we fix a DNN-controlled system 𝑀 𝜇 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅, 𝜇)
and an unsafe set 𝑆𝑢 ⊆ 𝑆 such that 𝑆0 ∩ 𝑆𝑢 = ∅ throughout the paper.

Definition 2 (Almost-Sure Safety). The system 𝑀 𝜇 is almost-surely (a.s.) safe, if a.s.
no trajectories starting from any initial state 𝑠0 ∈ 𝑆0 enter 𝑆𝑢 , i.e.,

                             ∀𝑠0 ∈ 𝑆0 .𝜔 ∈ Ω𝑠0 =⇒ 𝜔𝑡 ∉ 𝑆𝑢 ∀𝑡 ∈ N.

This almost-sure safety is a qualitative property and we call it “almost-sure” due to
the stochasticity from state perturbations. Since the almost-sure safety does not always
exist with the increase of state perturbations, we propose the notion of probabilistic
safety over infinite time horizons.

Definition 3 (Probabilistic Safety over Infinite Time Horizons). The system 𝑀 𝜇 is
probabilistically safe over infinite time horizons with [𝑙inf , 𝑢 inf ], where 0 ≤ 𝑙 inf ≤ 𝑢 inf ≤
1, if the probability of not entering 𝑆𝑢 falls into [𝑙inf , 𝑢 inf ] for all the trajectories from
any initial state 𝑠0 ∈ 𝑆0 , i.e.,
                                                                    
              ∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ∈ N} ∈ [𝑙inf , 𝑢 inf ].
6        Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

    The probabilistic safety is a quantitative property and 𝑙inf , 𝑢 inf are called lower and
upper bounds on the safety probabilities over infinite time horizons, respectively. Once
both bounds equal one, it implies the almost-sure safety. When the lower bound 𝑙inf = 0,
indicating that the system reaches the unsafe region at some time step 𝑇 < ∞, it is
significant to figure out how the safety probability decreases over the finite time horizon.
Therefore, we present the probabilistic safety over finite time horizons as follows.

Definition 4 (Probabilistic Safety over Finite Time Horizons). The system 𝑀 𝜇 is
probabilistically safe over a finite time horizon 𝑇 ∈ [0, ∞) with [𝑙 fin , 𝑢 fin ], where 0 ≤
𝑙fin ≤ 𝑢 fin ≤ 1, if the probability of not entering 𝑆𝑢 within 𝑇 falls into [𝑙fin , 𝑢 fin ] for all
the trajectories starting from any initial state 𝑠0 ∈ 𝑆0 ,
                                                               
               ∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ∈ [𝑙 fin , 𝑢 fin ].

Safety Verification Problems of DNN-Controlled Systems. Consider a DNN-controlled
system 𝑀 𝜇 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅, 𝜇) with an unsafe set 𝑆𝑢 ∈ 𝑆 such that 𝑆0 ∩ 𝑆𝑢 = ∅. We
formulate the qualitative and quantitative safety verification problems of 𝑀 𝜇 as follows:

 1. Qualitative Verification (QV): To answer whether 𝑀 𝜇 is almost-surely safe.
 2. Quantitative Verification over Infinite Time Horizons (QVITH): To compute
    certified lower and upper bounds 𝑙inf , 𝑢 inf on the safety probability of 𝑀 𝜇 over
    infinite time horizons.
 3. Quantitative Verification over Finite Time Horizons (QVFTH): To compute
    certified lower and upper bounds 𝑙 fin , 𝑢 fin on the safety probability of 𝑀 𝜇 over a
    finite time horizon 𝑇.

3.2   Overview of Our Framework
We first provide an overview of our unified framework designed to address the three
safety verification problems. Our framework builds on two fundamental results: (i) all
the problems can be reduced to the task of defining BCs under specific conditions, and
the defined BCs can be used to certify almost-sure safety for QV or safety bounds for
QVITH and QVFTH, respectively, and (ii) these BCs can be implemented and trained
in neural forms. The fundamental results are presented in Sections 4 to 6, respectively.
     The synthesis of NBCs has a preset timeout threshold, i.e., it will fail if NBCs cannot
be successfully synthesized within the time threshold. The procedure of our framework
is sketched in Figure 1, which consists of the following three steps:
Step 1: QV. We try to synthesize an NBC satisfying conditions in Theorem 1. If such
an NBC is successfully synthesized, we can conclude that the system 𝑀 𝜇 is almost-
surely safe by Theorem 1 and finish the verification. Alternatively, we can resort to
synthesizing a 𝑘-inductive NBC in Theorem 8 whose conditions are weaker than those
in Theorem 1. If the synthesis fails, we proceed to quantitative verification.
Step 2: QVITH. We try to synthesize two NBCs under the conditions in Theorems 2
and 3, respectively. If the synthesis fails, a timeout will be reported and the process
will be terminated. Otherwise, we can obtain the lower bound 𝑙 inf and the upper bound
𝑢 inf on probabilistic safety over infinite time horizons. Alternatively, we can choose to
synthesize the 𝑘-inductive variants of NBCs in Theorems 9 and 10. If the lower bound
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems                              7

              Start

                                                   Qualitative Verification
    Synthesize an NBC under the                                                          𝑘-inductive NBC
                                                        (Section 4.1)
      conditions in Theorem 1
                                                                                       Almost-surely safe by
                                                                                           Theorem 8.
                                  Yes
             Succeed?                             Almost-surely safe

                  No                               (Theorem 1)

                                               Quantitative Verification
     Synthesize two NBCs under the                                                    Lower and upper bounds
                                              over Infinite Time Horizon
    conditions in Theorems 2 and 3                                                     on infinite-time safety
                                                       (Section 4.2)
                                                                                         are computed by
                                                                                        Theorems 9 and 10.
                    Yes Lower and upper bounds                             Yes
       Succeed?              over infinite time               𝑙 inf ≥ 𝛿?
        No                  (Theorems 2 and 3)                     No                      (Section 5)

                                                   Quantitative Verification           Exponential bounds
      Synthesize two NBCs under the                over Finite Time Horizon           Lower and upper bounds
     conditions in Theorems 4 and 6                       (Section 4.3)                  in exponentially
                                                                                        decreasing order by
                                   Yes       Linear lower and upper                     Theorems 5 and 7.
                Succeed?
                                             bounds over finite time
                       No                      (Theorems 4 and 6)                         (Section 4.3)


                  Timeout                                                  Verified

                             Fig. 1. Our unified verification framework.


𝑙inf is no less than some preset safety threshold 𝛿 ∈ (0, 1), we terminate the verification.
The purpose of setting 𝛿 is to prevent the verification from returning a meaningless
lower bound such as 0. If 𝑙inf is less than 𝛿, we resort to computing safety bounds over
finite time horizons.
Step 3: QVFTH. We try to synthesize two NBCs satisfying conditions in Theorems 4
and 6, respectively. If the synthesis fails, a timeout will be reported and the verifica-
tion will terminate. Otherwise, we can compute the linear lower and upper bounds on
probabilistic safety over finite time horizons according to the synthesized NBCs. Alter-
natively, we can choose to synthesize two NBCs satisfying conditions in Theorems 5
and 7 to achieve exponential bounds, which might be tighter than linear ones.


4     Qualitative and Quantitative Safety Verification

In this section, we reduce all three safety verification problems of DNN-controlled sys-
tems into a cohesive problem of defining corresponding BCs. We establish specific con-
ditions for candidate BCs and provide formulas for computing lower and upper bounds
for quantitative verification based on the defined BCs.
8       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

4.1 Qualitative Safety Verification
Theorem 1 (Almost-Sure Safety). Given an 𝑀 𝜇 with an initial set 𝑆0 and an unsafe
set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such that for some constant
𝜆 ∈ (0, 1], the following conditions hold:

        𝐵(𝑠) ≤ 0                                                     for all 𝑠 ∈ 𝑆0 ,    (4)
        𝐵(𝑠) > 0                                                    for all 𝑠 ∈ 𝑆𝑢 ,     (5)
        𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) − 𝐵(𝑠) + 𝜆 · 𝐵(𝑠) ≤ 0          for all (𝑠, 𝛿) ∈ 𝑆 × 𝑊,       (6)

then 𝑀 𝜇 is almost-surely safe, i.e., ∀𝑠0 ∈ 𝑆0 . 𝜔 ∈ Ω𝑠0 =⇒ 𝜔𝑡 ∉ 𝑆𝑢 ∀𝑡 ∈ N.
Intuition. The BC in Theorem 1 is similar to that in Definition 1 except Condition (6), in
which we consider all stochastic behaviors of the system from state perturbations. We
prove the theorem by contradiction and the proof resembles that in [41, Proposition 2].
4.2 Quantitative Safety Verification over Infinite Time Horizon
Below we present the state-dependent lower and upper bounds on probabilistic safety
over infinite time horizons.
Theorem 2 (Lower Bounds on Infinite-time Safety). Given an 𝑀 𝜇 with an initial
set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such that for
some constant 𝜖 ∈ [0, 1], the following conditions hold:

          𝐵(𝑠) ≥ 0                                                 for all 𝑠 ∈ 𝑆,        (7)
          𝐵(𝑠) ≤ 𝜖                                                for all 𝑠 ∈ 𝑆0 ,       (8)
          𝐵(𝑠) ≥ 1                                                for all 𝑠 ∈ 𝑆𝑢 ,       (9)
         E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 0           for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,      (10)

then the safety probability over infinite time horizons is bounded from below by
                                                              
            ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ∈ N} ≥ 1 − 𝐵(𝑠0 ).              (11)
Intuition. A BC under conditions in Theorem 2 is a non-negative real-valued function
satisfying the supermartingale property, i.e., the expected value of the function remains
non-increasing at every time step for all states not in 𝑆𝑢 (see Condition (10)). We prove
the theorem by Ville’s Inequality [53] and the proof resembles that in [41, Theorem 15].
Theorem 3 (Upper Bounds on Infinite-time Safety). Given an 𝑀 𝜇 with an initial set
𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such that for
some constants 𝛾 ∈ (0, 1), 0 ≤ 𝜖 ′ < 𝜖 ≤ 1, the following conditions hold:
        0 ≤ 𝐵(𝑠) ≤ 1                                                  for all 𝑠 ∈ 𝑆,    (12)
        𝐵(𝑠) ≥ 𝜖                                                     for all 𝑠 ∈ 𝑆0 ,   (13)
                   ′
        𝐵(𝑠) ≤ 𝜖                                                    for all 𝑠 ∈ 𝑆𝑢 ,    (14)
        𝐵(𝑠) − 𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] ≤ 0         for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,     (15)
then the safety probability over infinite time horizons is bounded from above by
                                                              
            ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ∈ N} ≤ 1 − 𝐵(𝑠0 ).              (16)
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems        9

Intuition. A BC under conditions in Theorem 3 is a bounded non-negative function
satisfying the 𝛾-scaled submartingale property [52], i.e., the expected value of 𝐵 is in-
creasing at each time step for states not in 𝑆𝑢 (Condition (15)). We prove the theorem by
Optional Stopping Theorem [55], while former work is based on fix-point theory [49].
4.3   Quantitative Safety Verification over Finite Time Horizon
When the safety probability over infinite time horizons exhibits a decline, it becomes
advantageous to analyze the decreasing changes over finite time horizons. In the follow-
ing, we present our theoretical results on finite-time safety verification, starting with two
results related to lower bounds.
Theorem 4 (Linear Lower Bounds on Finite-time Safety). Given an 𝑀 𝜇 with an
initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such
that for some constants 𝜆 > 𝜖 ≥ 0 and 𝑐 ≥ 0, the following conditions hold:

           𝐵(𝑠) ≥ 0                                                 for all 𝑠 ∈ 𝑆,      (17)
           𝐵(𝑠) ≤ 𝜖                                               for all 𝑠 ∈ 𝑆0 ,      (18)
           𝐵(𝑠) ≥ 𝜆                                               for all 𝑠 ∈ 𝑆𝑢 ,      (19)
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝑐               for all 𝑠 ∈ 𝑆,      (20)
then the safety probability over a finite time horizon 𝑇 is bounded from below by
                                                         
       ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≥ 1 − (𝐵(𝑠0 ) + 𝑐𝑇)/𝜆.
Intuition. A BC in Theorem 4 satisfies the c-martingale property [48], i.e., the expected
value of 𝐵 can increase at every time step as long as it is bounded by a constant 𝑐
(Condition (20)), which is less conservative than the supermartingle property (Condi-
tion (10)), at the cost providing safety guarantees over finite time horizons. We prove
the theorem by Ville’s Inequality [53] and the proof resembles that in [4, Theorem 9].
Theorem 5 (Exponential Lower Bounds on Finite-time Safety). Given an 𝑀 𝜇 if
there exists a function 𝐵 : 𝑆 → R such that for some constants 𝛼 > 0, 𝛽 ∈ R, and
𝛾 ∈ [0, 1), the following conditions hold:
       𝐵(𝑠) ≥ 0                                                    for all 𝑠 ∈ 𝑆,       (21)
       𝐵(𝑠) ≤ 𝛾                                                   for all 𝑠 ∈ 𝑆0 ,      (22)
       𝐵(𝑠) ≥ 1                                                   for all 𝑠 ∈ 𝑆𝑢 ,      (23)
       𝛼E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝛼𝛽           for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 .      (24)
then the safety probability over a finite time horizon 𝑇 is bounded from below by
                                                           𝛼𝛽        𝛼𝛽
                                                                          − 𝐵(𝑠0 )) · 𝛼 −𝑇 .
                                                 
∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≥ 1 −         +(
                                                          𝛼−1      𝛼−1
Intuition. A BC in Theorem 5 satisfies that its 𝛼-scaled expectation can increase at most
𝛼𝛽 at every time step (Condition (24)). We establish a new result in discrete-time DNN-
controlled systems and prove it by the discrete version of Gronwall’s Inequality [22],
which is inspired by former work [59] in continuous-time dynamical systems.
    Then we propose our two results of upper bounds on safety probabilities.
10        Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

Theorem 6 (Linear Upper Bounds on Finite-time Safety). Given an 𝑀 𝜇 with an
initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier function 𝐵 : 𝑆 → R such that
for some constants 𝛽 ∈ (0, 1), 𝛽 < 𝛼 < 1 + 𝛽, 𝑐 ≥ 0, the following conditions hold:
           𝐵(𝑠) ≥ 0                                                    for all 𝑠 ∈ 𝑆,     (25)
           𝐵(𝑠) ≤ 𝛽                                              for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,     (26)
           𝛼 ≤ 𝐵(𝑠) ≤ 1 + 𝛽                                          for all 𝑠 ∈ 𝑆𝑢 ,     (27)
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≥ 𝑐            for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 .     (28)
then the safety probability over a finite time horizon 𝑇 is bounded from above by
                                                                    1
      ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≤ 1 − 𝐵(𝑠0 ) − 𝑐 · 𝑇 + 𝛽.
                                                                      2

Intuition. A BC in Theorem 6 is non-negative and its value is bounded when states
are in 𝑆𝑢 (Condition (27)). Moreover, Condition (28) is the inverse of the c-martingale
property in Theorem 4, i.e., the expected value of 𝐵 should increase at least 𝑐 at every
time step.

Theorem 7 (Exponential Upper Bounds on Finite-Time Safety). Given an 𝑀 𝜇 with
an initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier function 𝐵 : 𝑆 → R
such that for some constants 𝐾 ′ ≤ 𝐾 < 0, 𝜖 > 0 and a non-empty interval [𝑎, 𝑏], the
following conditions hold:
     𝐵(𝑠) ≥ 0                                                      for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,   (29)
      ′
     𝐾 ≤ 𝐵(𝑠) ≤ 𝐾                                                      for all 𝑠 ∈ 𝑆𝑢 ,   (30)
     E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ −𝜖                   for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,   (31)
     𝑎 ≤ 𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) − 𝐵(𝑠) ≤ 𝑏                 for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 and 𝛿 ∈ 𝑊,     (32)

then the safety probability over a finite time horizon 𝑇 is bounded from above by
                                                              2(𝜖 · 𝑇 − 𝐵(𝑠0 )) 2
     ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≤ 𝑒𝑥 𝑝(−                     ).
                                                                  𝑇 · (𝑏 − 𝑎) 2

Intuition. A BC under the Conditions (29) to (32) is a difference-bounded ranking su-
permartingale [15]. Condition (31) is the supermartingale difference condition, i.e., the
expectation of 𝐵 should decrease at least 𝜖 at each time step, while Condition (32) im-
plies that the update of 𝐵 should be bounded. We prove this theorem by Hoeffding’s
Inequality on Supermartingales [26] and the proof resembles that in the work [15].

5    Relaxed 𝒌-Inductive Barrier Certificates

We now introduce 𝑘-inductive barrier certificates, capable of offering both qualitative
and quantitative safety guarantees, while relaxing the strict conditions for safety through
the utilization of the 𝑘-induction principle [18,10]. Prior to presenting our theoretical
results, we first define the notion of 𝑘-inductive update functions as follows.
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems                     11

Definition 5 (𝑘-inductive Update Functions). Given an 𝑀 𝜇 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅, 𝜇), a
𝑘-inductive update function 𝑔 𝑘𝜋, 𝑓 with respect to 𝜋, 𝑓 is defined recursively, i.e.,

                                   
                                   
                                    𝑔 𝜋, 𝑓 (𝑔 𝑘−1
                                               𝜋, 𝑓 (𝑠 𝑡 , Δ𝑡
                                                            𝑘−1 ), 𝛿
                                                                     𝑡+𝑘−1 )     if 𝑘 > 1
                  𝑘           𝑘
                                   
                                   
                𝑔 𝜋, 𝑓 (𝑠𝑡 , Δ𝑡 ) = 𝑓 (𝑠𝑡 , 𝜋(𝑠𝑡 + 𝛿𝑡 ))                         if 𝑘 = 1
                                   
                                                                                 if 𝑘 = 0
                                   
                                    𝑠𝑡
                                   
where Δ𝑡𝑘 = [𝛿𝑡 , 𝛿𝑡+1 , . . . , 𝛿𝑡+𝑘−1 ] is a noise vector of length 𝑘 with each 𝛿𝑡 ∼ 𝜇, and
𝑔 𝜋, 𝑓 (𝑠𝑡 , 𝛿𝑡 ) := 𝑓 (𝑠𝑡 , 𝜋(𝑠𝑡 + 𝛿𝑡 )).
Intuitively, 𝑔 𝑘𝜋, 𝑓 computes the value of a state after 𝑘 steps given a 𝑘-dimensional noise
vector Δ 𝑘 ∈ 𝑊 𝑘 ⊆ R𝑛×𝑘 , where 𝑊 = supp (𝜇) is the support of 𝜇. To calculate the
expectation w.r.t. 𝑘-dimensional noises, we denote by 𝜇 𝑘 the product measure on 𝑊 𝑘 .
5.1   𝒌-Inductive Barrier Certificates for Qualitative Safety
Theorem 8 (𝑘-inductive Variant of Almost-Sure Safety). Given an 𝑀 𝜇 with an
initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a 𝑘-inductive barrier certificate
𝐵 : 𝑆 → R such that the following conditions hold:
    Ó
      0≤𝑖<𝑘 𝐵(𝑔 𝜋, 𝑓 (𝑠, Δ )) ≤ 0
                𝑖         𝑖                                 ∀(𝑠, Δ𝑖 ) ∈ 𝑆0 × 𝑊 𝑖 , (33)
   𝐵(𝑠) > 0                                                                               ∀𝑠 ∈ 𝑆𝑢 ,    (34)
   Ó                                                                                 𝑖             𝑖
     0≤𝑖<𝑘 (𝐵(𝑔 𝜋, 𝑓 (𝑠, Δ )) ≤ 0) =⇒ 𝐵(𝑔 𝜋, 𝑓 (𝑠, Δ )) ≤ 0                    ∀(𝑠, Δ ) ∈ 𝑆 × 𝑊 ,
               𝑖          𝑖               𝑘         𝑘                                                  (35)
then the system 𝑀 𝜇 is almost-surely safe, i.e., ∀𝑠0 ∈ 𝑆0 . 𝜔 ∈ Ω𝑠0 =⇒ 𝜔𝑡 ∉ 𝑆𝑢 ∀𝑡 ∈ N.
     Intuition. Condition (33) implies that the state sequences starting from the safe set
will remain in the safe set for the next 𝑘 −1 consecutive time steps, while Condition (35)
means that for any 𝑘 consecutive time steps, if the system is safe, then the system will
still be safe at the (𝑘 + 1)-th time step. We prove the theorem by contradiction.
     Note that Condition (35) contains an implication, in order to compute the 𝑘-inductive
BC, we replace it with its sufficient condition:
                             Í
      −𝐵(𝑔 𝑘𝜋, 𝑓 (𝑠, Δ 𝑘 )) − 0≤𝑖<𝑘 𝜏𝑖 · (−𝐵(𝑔 𝑖𝜋, 𝑓 (𝑠, Δ𝑖 ))) ≥ 0, ∀(𝑠, Δ𝑖 ) ∈ 𝑆 × 𝑊 𝑖 . (36)

If there exist 𝜏0 , . . . , 𝜏𝑘−1 ≥ 0 satisfying Equation (36), Condition (35) is satisfied.
5.2   𝒌-Inductive Barrier Certificates for Quantitative Safety
Theorem 9 (𝑘-inductive Lower Bounds on Infinite-time Safety). Given an 𝑀 𝜇 , if
there exists a k-inductive barrier certificate 𝐵 : 𝑆 → R such that for some constants
𝑘 ∈ N ≥1 , 𝜖 ∈ [0, 1] and 𝑐 ≥ 0, the following conditions hold:
           𝐵(𝑠) ≥ 0                                                               for all 𝑠 ∈ 𝑆        (37)
           𝐵(𝑠) ≤ 𝜖                                                             for all 𝑠 ∈ 𝑆0 ,       (38)
           𝐵(𝑠) ≥ 1                                                             for all 𝑠 ∈ 𝑆𝑢 ,       (39)
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝑐                            for all 𝑠 ∈ 𝑆,        (40)
                          𝑘         𝑘
           EΔ𝑘 ∼𝜇 𝑘 [𝐵( 𝑓 𝜋, 𝑓 (𝑠, Δ )) | 𝑠] − 𝐵(𝑠) ≤ 0                          for all 𝑠 ∈ 𝑆,        (41)
12      Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

then the safety probability over infinite time horizons is bounded from below by
                                                                        𝑘 (𝑘 − 1)𝑐
    ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔0 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ∈ N} ≥ 1 − 𝑘 𝐵(𝑠0 ) −               .
                                                                               2
Intuition. Condition (40) requires the barrier certificate to be a c-martingale at every
time step and Condition (41) requires the barrier certificate sampled after every 𝑘-th
step to be a supermartingale. We prove the theorem by Ville’s Inequality [53].
Theorem 10 (𝑘-inductive Upper Bounds on Infinite-time Safety). Given an 𝑀 𝜇 , if
there exists a barrier certificate 𝐵 : 𝑆 → R such that for some constant 𝛾 ∈ (0, 1),
0 ≤ 𝜖 ′ < 𝜖 ≤ 1, 𝑐 ≤ 0 the following conditions hold:

       0 ≤ 𝐵(𝑠) ≤ 1                                                 for all 𝑠 ∈ 𝑆     (42)
       𝐵(𝑠) ≥ 𝜖                                                   for all 𝑠 ∈ 𝑆0 ,    (43)
                  ′
       𝐵(𝑠) ≤ 𝜖                                                   for all 𝑠 ∈ 𝑆𝑢 ,    (44)
       E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≥ 𝑐                  for all 𝑠 ∈ 𝑆,     (45)
       𝐵(𝑠) − 𝛾 𝑘 · EΔ𝑘 ∼𝜇 𝑘 [𝐵(𝑔 𝑘𝜋, 𝑓 (𝑠, Δ 𝑘 )) | 𝑠] ≤ 0   for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,    (46)
then the safety probability over infinite time horizons is bounded from above by
                                                                        𝑘 (𝑘 − 1)𝑐
    ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑋𝑢 for all 𝑡 ∈ N} ≤ 1 − 𝑘 𝐵(𝑠0 ) −                 .
                                                                               2
Intuition. This BC is non-negative and bounded (Condition 42). Condition (45) is the
inverse of the c-martingale property, while Condition (46) requires the barrier certificate
sampled after every 𝑘-th step to be a 𝛾 𝑘 -scaled submartingale. We prove the theorem
by the Optional Stopping Theorem [55].
Remark 1. To make the probabilistic bounds in Theorem 9 and Theorem 10 non-trivial,
the value of 𝑘 should be bounded by
                                       √︁
                        (𝑐 − 2𝐵(𝑠0 )) + 4𝐵(𝑠0 ) 2 + 𝑐2 − 4𝑐(𝐵(𝑠0 ) − 2)
               1≤𝑘≤                                                     .
                                            2𝑐
6     Synthesis of Neural Barrier Certificates
In this section, we show that the BCs defined in the previous sections for DNN-controlled
systems can be implemented and synthesized in the form of DNNs, akin to those for
linear or nonlinear stochastic systems [68].
    We adopt the CEGIS-based method [2] to train and validate target NBCs. Figure 2
sketches the workflow. In each loop iteration, we train a candidate BC in the form of a
neural network which is then passed to the validation. If the validation result is false,
we compute a set of counterexamples for future training. This iteration is repeated until
a trained candidate is validated or a given timeout is reached. Moreover, we propose a
simulation-guided training method by adding additional terms to the loss functions to
improve the tightness of upper and lower bounds calculated by the trained NBCs.
    We present the synthesis of NBCs in Theorem 2 for probabilistic safety over infinite
time horizons, as an example. We defer to Appendix the synthesis of other NBCs.
6.1   Training Candidate NBCs
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems                  13

Two pivotal factors in the training phase are         Start
the generation of training data and the con-
struction of the loss function.               Discretize state space
Training Data Discretization. As the state
space 𝑆 is possibly continuous and infinite,                            Refined state
                                                           Train




                                                                                             space
we choose a finite set of states for training
candidate NBCs. This can be achieved by                         NBC
discretizing the state space 𝑆 and construct-             Validate                Refine
ing a discretization 𝑆˜ ⊆ 𝑆 such that for each                                         No
𝑠 ∈ 𝑆, there is a 𝑠˜ ∈ 𝑆˜ with ||𝑠 − 𝑠˜ || 1 < 𝜏,
where 𝜏 > 0 is called the granularity of 𝑆.    ˜            Valid?                Timeout?
As 𝑆 is compact and thus bounded, this dis-                         No
cretization can be computed by simply pick-                     Yes                    Yes
ing the vertices of a grid with sufficiently               Finish                   Fail
small cells. For the re-training after vali-
dation failure, 𝑆˜ will be reconstructed with        Fig. 2. CEGIS-based NBC synthesis [2].
counterexamples and a smaller granularity 𝜏. Once the discretization 𝑆˜ is obtained, we
construct two finite sets 𝑆˜0 := 𝑆˜ ∩ 𝑆0 and 𝑆˜𝑢 := 𝑆˜ ∩ 𝑆𝑢 used for the training process.
Loss Function Construction. A candidate NBC is initialized as a neural network ℎ 𝜃
w.r.t. the network parameter 𝜃. ℎ 𝜃 is trained by minimizing the following loss function:
         L (𝜃) := 𝑘 1 · L1 (𝜃) + 𝑘 2 · L2 (𝜃) + 𝑘 3 · L3 (𝜃) + 𝑘 4 · L4 (𝜃) + 𝑘 5 · L5 (𝜃)
where 𝑘 𝑖 ∈ R, 𝑖 = 1, · · · , 5 are the algorithmic parameters balancing the loss terms.
   The first loss term is defined via the condition in Condition (7) as:

                                           1 Í
                             L1 (𝜃) =              (max{0 − ℎ 𝜃 (𝑠), 0})
                                           ˜ 𝑠∈ 𝑆˜
                                         | 𝑆|
                                                                               ˜
Intuitively, a loss will incur if either ℎ 𝜃 (𝑠) is less than zero for any 𝑠 ∈ 𝑆.
    Correspondingly, the second and third loss terms are defined via Conditions (8)
and (9) as:
              1 Í
                          (max{ℎ 𝜃 (𝑠) − 𝜖, 0}) , and L3 (𝜃) = | 𝑆˜1 |
                                                                        Í
 L2 (𝜃) =                                                                     (max{1 − ℎ 𝜃 (𝑠), 0}) .
              ˜
            | 𝑆0 | 𝑠∈ 𝑆˜0                                           𝑢
                                                                       𝑠∈ 𝑆˜𝑢

The fourth loss term is defined via the condition in Condition (10) as:
                                                                                      
                             1          Í                Í ℎ 𝜃 (𝑠′ )
             L4 (𝜃) =                           max{                 − ℎ 𝜃 (𝑠) + 𝜁, 0}
                        | 𝑆˜ \ 𝑆˜𝑢 | 𝑠∈ 𝑆\
                                        ˜ 𝑆˜𝑢        𝑠 ′ ∈ D𝑠
                                                              𝑁


where for each 𝑠 ∈ 𝑆˜ \ 𝑆˜𝑢 , D𝑠 is the set of its successor states such that D𝑠 := {𝑠′ | 𝑠′ =
𝑓 (𝑠, 𝜋(𝑠 + 𝛿𝑖 )), 𝛿𝑖 ∼ 𝜇, 𝑖 ∈ [1, 𝑁]}, 𝑁 > 0 is the sample number of successor states.
We use the mean of ℎ 𝜃 (·) at the 𝑁 successor states to approximate the expected value
E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] for each 𝑠 ∈ 𝑆˜ \ 𝑆˜𝑢 , and 𝜁 > 0 to tighten the condition.
Simulation-guided Loss Term. A trained BC that satisfies the above four conditions
can provide lower bounds on probabilistic safety over infinite time horizons for the sys-
14       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

tem. However, these conditions have nothing to do with the tightness of lower bounds
and we may obtain a trivial zero-valued lower bound by the trained BC.
    To assure the tightness of lower bounds from trained NBCs, we propose a simulation-
guided method based on Equation (11). For each 𝑠0 ∈ 𝑆˜0 , we execute the control system
𝑁 ′ > 0 episodes, and calculate the safety frequency 𝕗𝑠 of all the 𝑁 ′ trajectories over
infinite time horizons. Based on the statistical results, the last loss term is defined as:
                                       1 Í
                          L5 (𝜃) =                 (max{𝕗𝑠 + ℎ 𝜃 (𝑠) − 1, 0})
                                       ˜
                                     | 𝑆0 | 𝑠∈ 𝑆˜0
Intuitively, this term is to enforce the value of the derived lower bound to approach the
statistical result as closely as possible, ensuring its tightness.
    We emphasize that our simulation-guided method plus the NBC validation (see next
section) is sound, as we will validate the trained BC to ensure it satisfies all the BC
conditions (see also Theorem 12).

6.2   NBC Validation
A candidate NBC ℎ 𝜃 is valid if it meets the Conditions (7) to (10). The first three
conditions condition can be checked by the following constraint
                    inf ℎ 𝜃 (𝑠) ≥ 0 ∧ sup ℎ 𝜃 (𝑠) ≤ 𝜖 ∧ inf ℎ 𝜃 (𝑠) ≥ 1
                    𝑠∈𝑆                   𝑠∈𝑆0                  𝑠∈𝑆𝑢

using the interval bound propagation approach [21,58]. When any state violates the
above equation, it is treated as a counterexample and added to 𝑆˜ for future training.
    For Condition (10), Theorem 11 reduces the validation from infinite states to finite
ones, which are easier to check.

Theorem 11. Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 +
𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 0 for any state 𝑠 ∈ 𝑆 \ 𝑆𝑢 if the formula below
                           E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] ≤ 𝐵( 𝑠˜) − 𝜁                  (47)

holds for any state 𝑠˜ ∈ 𝑆˜ \ 𝑆˜𝑢 , where 𝜁 = 𝜏 · 𝐿 𝐵 · (1 + 𝐿 𝑓 · (1 + 𝐿 𝜋 )) with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵
being the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.

    To check the satisfiablility of Equation (47) in ℎ 𝜃 and a state 𝑠˜, we need to compute
the expected value E 𝛿∼𝜇 [ℎ 𝜃 ( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜]. However, it is difficult to compute its
closed form because ℎ 𝜃 is provided in the form of neural networks. Hence, We bound
the expected value E 𝛿∼𝜇 [ℎ 𝜃 ( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] via interval arithmetic [21,58] instead
of computing it, which is inspired by the work [33,70]. In particular, given the noise
distribution 𝜇 and its support 𝑊 = {𝛿 ∈ R𝑛 | 𝜇(𝛿) > 0}, we first partition 𝑊 into finitely
𝑚 ≥ 1 cells, i.e., cell(W) = {𝑊1 , · · · , 𝑊𝑚 }, and use maxvol =                  max vol(𝑊𝑖 )
                                                                                𝑊𝑖 ∈cell(W)
to denote the maximal volume with respect to the Lebesgue measure of any cell in the
partition, respectively. For the expected value in Equation (47), we bound it from above:
                                                        Í
              E 𝛿∼𝜇 [ℎ 𝜃 ( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] ≤   maxvol · sup 𝛿 𝐹 (𝛿)
                                                     𝑊𝑖 ∈cell(W)
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems           15

where, 𝐹 (𝛿) = ℎ 𝜃 ( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))). The supremum can be calculated via interval arith-
metic. We refer interested readers to [33] and [70] for more details.
Theorem 12 (Soundness). If a trained NBC is valid, it can certify the almost-sure
safety for the qualitative verification, or the derived bound by the NBC is a certified
lower/upper bound on the safety probability for the quantitative case.

      The proof of soundness is straightforward by the NBC validation.

7     Evaluation
Our experimental goals encompass evaluating the effectiveness of (i) the qualitative and
quantitative verification methods within our framework, (ii) the 𝑘-inductive BCs, and
(iii) the simulation-guided training method, respectively.
7.1    Benchmarks and Experimental Setup
We assess the effectiveness of our approach on four classic DNN-controlled tasks from
public benchmarks: Pendulum and Cartpole from the DRL training platform OpenAI’s
Gym [11], while B1 and Tora commonly used by the state-of-the-art safety verification
tools [28]. All experiments are executed on a workstation running Ubuntu 18.04, with a
32-core AMD Ryzen Threadripper CPU, 128GB RAM, and a single 24564MiB GPU .
     For the safety verification of DNN-controlled systems, we consider state perturba-
tions of uniform noises with zero means and different radii. Specifically, for each state
𝑠 = (𝑠1 , . . . , 𝑠 𝑛 ), we add noises 𝑋1 , . . . , 𝑋𝑛 to each dimension of 𝑠 and obtain the per-
turbed state (𝑠1 + 𝑋1 , . . . , 𝑠 𝑛 + 𝑋𝑛 ), where 𝑋𝑖 ∼ U(−𝑟, 𝑟) (1 ≤ 𝑖 ≤ 𝑛, 𝑟 ≥ 0).
     For qualitative evaluations, the existence
of an NBC in Theorem 1 can ensure the Table 1. Qualitative verification results.
almost-sure safety of the whole system. Due Task Perturbation Verification 𝑘. #Fail.
to the data sparsity of an initial state, we ran-                           0    ✓       1     0
                                                                     𝑟 = 0.01 Unknown 1        0
domly choose 10,000 initial states (instead of CP
                                                                     𝑟 = 0.01    ✓       2     0
a single one) from the initial set 𝑆0 . For quan-                    𝑟 = 0.03 Unknown 1 207
titative evaluations, to measure the quantita-                          𝑟=0      ✓       1     0
tive safety probabilities from the system level, PD                  𝑟 = 0.01 Unknown 1 675
we calculate the mean values of lower/upper                          𝑟 = 0.03 Unknown 1 720
bounds by NBCs on these 10,000 states un-                               𝑟=0      ✓       1     0
der different perturbations. The correctness of                      𝑟 = 0.02 Unknown 1        0
                                                            Tora
such system-level safety bounds is witnessed                         𝑟 = 0.02    ✓       2     0
by Theorem 12 as each lower/upper bound on                           𝑟 = 0.04 Unknown 1 1113
a single state 𝑠0 is a certified bound for the                          𝑟=0      ✓       1     0
exact safety probability from 𝑠0 , and thus the             B1        𝑟 = 0.1    ✓       1     0
same holds on the system level. We also sim-                          𝑟 = 0.2 Unknown    1    43
ulate 10,000 episodes starting from each of these 10,000 initial states under different
perturbations and use the statistical results as the baseline.
7.2    Effectiveness of Qualitative Safety Verification
Table 1 shows the qualitative verification results under different perturbation radii 𝑟’s
and induction bounds 𝑘’s. Given a perturbed DNN-controlled system, we verify its
16      Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

qualitative safety by training an NBC under the conditions in Theorem 1. Once such an
NBC is trained and validated, the system is verified to be almost-surely safe, marked as
✓. If no valid barrier certificates are trained within a given timeout, the result is marked
as Unknown.
    As for simulation, we record the number of those episodes where the system enters
the unsafe region, marked as the column #Fail. in the table. We can observe that for
the systems that are successfully verified by NBCs, no failed episodes are detected by
simulation. For systems with failed episodes by simulation, no corresponding NBCs
can be trained and validated. The consistency experimentally reflects the effectiveness
of our approach.
    Furthermore, we note that for CP with 𝑟 = 0.01 and Tora with 𝑟 = 0.02, there are
no failed episodes, but no NBCs in Theorem 1 can be synthesized for these systems.
By applying Theorem 8, we find the 2-inductive NBCs, which ensures the safety of the
systems. It demonstrates that 𝑘-inductive variants can relax the conditions of NBCs and
thus ease the synthesis of valid NBCs for qualitative safety verification.
    As the perturbation radius increases, ensuring almost-sure safety becomes challeng-
ing, and qualitative verification only results in the conclusion of Unknown. Conse-
quently, we proceed to conduct quantitative verification over infinite time horizons.
7.3 Effectiveness of Quantitative Safety Verification over Infinite Time Horizon
Figure 3 (a-d) show the certified upper and lower bounds and simulation results (i.e.,
black lines marked with ‘•’) over infinite time horizons. The red lines marked with ‘■’
and blue lines marked with ‘+’ represent the mean values of the lower bounds in Theo-
rem 2 and the upper bounds in Theorem 3 on the chosen 10,000 initial states calculated
by the corresponding NBCs, respectively. The purple lines marked with ‘▲’ and green
lines marked with ‘×’ represent the mean values of the 2-inductive upper and lower
bounds calculated by the corresponding NBCs in Theorems 9 and 10, respectively. We
can find that the certified bounds enclose the simulation outcomes, demonstrating the
effectiveness of our trained NBCs.
    Table 2 shows a comparison of aver-
age synthesis time (in seconds) for different
NBCs. We observe that the synthesis time of
2-inductive NBCs is 25% faster than that of Table 2. Synthesis time for different NBCs.
normal NBCs, at the sacrifice of tightness. Task Lower 2-Lower Upper 2-Upper
Note that the tightness of certified bounds de- CP 2318.5 1876.0 2891.9 2275.3
                                                  PD 1941.6 1524.0 2282.7 1491.5
pends on specific systems and perturbations.
                                                  Tora 280.3      218.5 895.1    650.7
Investigating what factors influence the tight- B1       587.4    313.6 1127.3   840.1
ness to yield tighter bounds is an interesting
future work to explore.
    Approaching zero for infinite time horizons, the lower bounds indicate a declining
trend in safety probabilities over time. Therefore, we proceed to conduct quantitative
verification over finite time horizons, providing both linear and exponential lower and
upper bounds.
7.4 Effectiveness of Quantitative Safety Verification over Finite Time Horizon
Figure 3 (e-h) depict the certified upper and lower bounds and simulation results (i.e.,
black lines) over finite time horizons from the system level. Fix a sufficiently large
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems          17




                    (a) CP                                         (b) PD




                   (c) Tora                                       (d) B1




               (e) CP (𝑟 = 0.3)                               (f) PD (𝑟 = 1.0)




                (g) Tora (𝑟 = 0.3)                              (h) B1 (𝑟 = 1.5)
Fig. 3. The certified upper and lower bounds over infinite (a-d) and finite (e-h) time horizons,
respectively, and their comparison with the simulation results.

noise level for each system, the x-axis represents the time horizon, while the y-axis
corresponds to the safety probabilities. The purple lines and blue lines represent the
18       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang




                     (a) CP                                         (b) PD




                   (c) Tora                                          (d) B1
Fig. 4. The certified bounds w/ and w/o simulation-guided loss terms over infinite time horizons.
mean values of the exponential lower and upper bounds calculated by the correspond-
ing NBCs in Theorem 5 and Theorem 7, respectively. The red lines and green lines
represent the mean values of the linear lower and upper bounds calculated by the corre-
sponding NBCs in Theorem 4 and Theorem 6, respectively. The results indicate that our
computed certified bounds encapsulate the statistical outcomes. Moreover, the exponen-
tial upper bounds are always tighter than the linear upper bounds, and the exponential
lower bounds become tighter than the linear ones with the increase of time. It is worth
exploring the factors to generate tighter results in future work.
7.5 Effectiveness of Simulation-guided Loss Term
The simulation-guided loss term is proposed in Section 6.1 to tighten the certified
bounds calculated by NBCs. To evaluate its effectiveness, we choose NBCs in The-
orems 2 and 3, and train them with and without the simulation-guided loss terms. The
comparison between them is shown in Figure 4. The red lines marked with ‘■’ and blue
lines marked with ‘+’ represent the mean values of the bounds in Theorems 2 and 3 on
initial states calculated by the corresponding NBCs trained with the simulation-guided
loss terms, respectively. The purple lines with ‘▲’ and green lines with ‘×’ represent
the mean values of the bounds calculated by the NBCs trained without the simulation-
guided loss terms. Apparently, the upper and lower bounds derived by NBCs trained
without the simulation-guided loss terms are looser than the bounds trained with these
terms. Specifically, the results computed by NBCs with simulation-guided loss terms
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems    19

can achieve an average improvement of 47.5% for lower bounds and 31.7% for upper
bounds, respectively. Hence, it is fair to conclude that accounting for simulation-guided
loss terms is essential when conducting quantitative safety verification.

8   Related Work
Barrier Certificates for Stochastic Systems. Our unified safety verification framework
draws inspiration from research on the formal verification of stochastic systems employ-
ing barrier certificates. Prajna et al. [40,41,42] propose the use of barrier certificates
in the safety verification of stochastic systems. This idea has been further expanded
through data-driven approaches [44] and 𝑘-inductive variants [4]. As the dual problem
of computing safety probabilities, computing reachability probabilities in stochastic
dynamical systems has been studied for both infinite [20,61,62] and finite time hori-
zons [60,59]. Probabilistic programs, viewed as stochastic models, have their reacha-
bility and termination probabilities investigated using proof rules [19] and Martingale-
based approaches [14,15,5], where the latter are subsequently unified through order-
theoretic fixed-point approaches [52,49,50].
Formal Verification of DNN-controlled Systems. Modeling DNN-controlled systems
as Markov Decision Processes (MDPs) and verifying these models using probabilistic
model checkers, such as PRISM [30] and Storm [25], constitutes a quantitative ver-
ification approach. Bacci and Parker [8,7] employ abstract interpretation to construct
interval MDPs and yield safety probabilities within bounded time. Carr et al. [13] pro-
pose probabilistic verification of DNN-controlled systems by constraining the analysis
to partially observable finite-state models. Amir et al. propose a scalable approach based
on DNN verification techniques to first support complex properties such as liveness [3].
     Reachability analysis is a pivotal qualitative approach in the safety verification of
DNN-controlled systems. Bacci et al. [6] introduce a linear over-approximation-based
method for calculating reachable set invariants over an infinite time horizon for DNN-
controlled systems. Other reachability analysis approaches, such as Verisig [28] and
Polar [27], focus solely on bounded time. These approaches do not consider perturba-
tions as they assume actions on states to be deterministic.
Barrier Certificates for Training and Verifying DNN Controllers. BC-based meth-
ods [1,39] have recently been investigated for training and verifying DNN controllers.
The key idea is to train a safe DNN controller through interactive computations of cor-
responding barrier certificates to ensure qualitative safety [63,17]. Existing BC-based
approaches for the verification of DNN-controlled systems focus solely on qualitative
aspects but neglect the consideration of perturbations [47,64]. Our approach comple-
ments them by accommodating the inherent uncertainty in DNN-controlled systems.

9   Conclusion and Future Work
We have systematically studied the BC-based qualitative and quantitative safety verifi-
cation of DNN-controlled systems. This involves unifying and transforming the verifi-
cation problems into a general task of training corresponding neural certificate barriers.
We have also defined the conditions that a trained certificate should satisfy, along with
the corresponding lower and upper bounds presented in both linear and exponential
forms and 𝑘-inductive variants. Through the unification of these verification problems,
20       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

we have established a comprehensive framework for delivering various safety guaran-
tees, whether qualitatively or quantitatively, in a unified manner.
    Our framework sheds light on the quest for scalable and multipurpose safety veri-
fication of DNN-controlled systems. It accommodates both qualitative and quantitative
aspects in verified results, spans both finite and infinite time horizons, and encompasses
certified bounds presented in both linear and exponential forms. Our work also show-
cases the potential to circumvent verification challenges posed by DNN controllers.
From our experiments, we acknowledge that both qualitative and quantitative verifica-
tion results are significantly dependent on the quality of the trained NBCs. Our next
step is to explore more sophisticated deep learning methods to train valid NBCs for
achieving more precise verification results.

Acknowledgments
We thank the anonymous reviewers of CAV 2024 for their valuable comments. The
work has been supported by the NSFC Programs (62161146001, 62372176), Huawei
Technologies Co., Ltd., the Shanghai International Joint Lab (22510750100), the Shang-
hai Trusted Industry Internet Software Collaborative Innovation Center, and the Na-
tional Research Foundation, Singapore, under its RSS Scheme (NRF-RSS2022-009).

References
 1. Abate, A., Ahmed, D., Edwards, A., Giacobbe, M., Peruffo, A.: FOSSIL: a software tool for
    the formal synthesis of lyapunov functions and barrier certificates using neural networks. In:
    HSCC’21. pp. 24:1–24:11. ACM (2021)
 2. Abate, A., David, C., Kesseli, P., Kroening, D., Polgreen, E.: Counterexample guided induc-
    tive synthesis modulo theories. In: CAV’18. pp. 270–288. Springer (2018)
 3. Amir, G., Schapira, M., Katz, G.: Towards scalable verification of deep reinforcement learn-
    ing. In: FMCAD’21. pp. 193–203. IEEE (2021)
 4. Anand, M., Murali, V., Trivedi, A., Zamani, M.: k-inductive barrier certificates for stochastic
    systems. In: HSCC’22. pp. 12:1–12:11. ACM (2022)
 5. Asadi, A., Chatterjee, K., Fu, H., Goharshady, A.K., Mahdavi, M.: Polynomial reachability
    witnesses via stellensätze. In: PLDI’21. pp. 772–787. ACM (2021)
 6. Bacci, E., Giacobbe, M., Parker, D.: Verifying reinforcement learning up to infinity. In: IJ-
    CAI’21. pp. 2154–2160 (2021)
 7. Bacci, E., Parker, D.: Probabilistic guarantees for safe deep reinforcement learning. In: FOR-
    MATS’20. pp. 231–248. Springer (2020)
 8. Bacci, E., Parker, D.: Verified probabilistic policies for deep reinforcement learning. In:
    NFM’22. pp. 193–212. Springer (2022)
 9. Berkenkamp, F., Turchetta, M., Schoellig, A.P., Krause, A.: Safe model-based reinforcement
    learning with stability guarantees. In: NeurIPS. pp. 908–918 (2017)
10. Brain, M., Joshi, S., Kroening, D., Schrammel, P.: Safety verification and refutation by k-
    invariants and k-induction. In: SAS’15. pp. 145–161. Springer (2015)
11. Brockman, G., Cheung, V., Pettersson, L., Schneider, J., Schulman, J., Tang, J., Zaremba,
    W.: OpenAI Gym (2016), arXiv:1606.01540
12. Calinescu, R., Ghezzi, C., Kwiatkowska, M., Mirandola, R.: Self-adaptive software needs
    quantitative verification at runtime. Communications of the ACM 55(9), 69–77 (2012)
13. Carr, S., Jansen, N., Topcu, U.: Task-aware verifiable RNN-based policies for partially ob-
    servable markov decision processes. Artif. Intell. Res. 72, 819–847 (2021)
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems                21

14. Chakarov, A., Sankaranarayanan, S.: Probabilistic program analysis with martingales. In:
    CAV’13. pp. 511–526. Springer (2013)
15. Chatterjee, K., Fu, H., Novotný, P., Hasheminezhad, R.: Algorithmic analysis of qualitative
    and quantitative termination problems for affine probabilistic programs. In: POPL’16. pp.
    327–342. ACM (2016)
16. Dawson, C., Gao, S., Fan, C.: Safe control with learned certificates: A survey of neural
    lyapunov, barrier, and contraction methods for robotics and control. IEEE Trans. Robot. 39,
    1749 – 1767 (2023)
17. Deshmukh, J., Kapinski, J., Yamaguchi, T., Prokhorov, D.: Learning deep neural network
    controllers for dynamical systems with safety guarantees. In: ICCAD’19. pp. 1–7. IEEE
    (2019)
18. Donaldson, A.F., Haller, L., Kroening, D., Rümmer, P.: Software verification using k-
    induction. In: SAS’11. pp. 351–368. Springer (2011)
19. Feng, S., Chen, M., Su, H., Kaminski, B.L., Katoen, J., Zhan, N.: Lower bounds for possibly
    divergent probabilistic programs. Proc. ACM Program. Lang. 7(OOPSLA1), 696–726 (2023)
20. Feng, S., Chen, M., Xue, B., Sankaranarayanan, S., Zhan, N.: Unbounded-time safety verifi-
    cation of stochastic differential dynamics. In: CAV’20. pp. 327–348. Springer (2020)
21. Gowal, S., Dvijotham, K., Stanforth, R., Bunel, R., Qin, C., Uesato, J., Arandjelovic, R.,
    Mann, T.A., Kohli, P.: On the effectiveness of interval bound propagation for training verifi-
    ably robust models. CoRR abs/1810.12715 (2018)
22. Gronwall, T.H.: Note on the derivatives with respect to a parameter of the solutions of a
    system of differential equations. Annals of Mathematics pp. 292–296 (1919)
23. Hahn, E.M., Hartmanns, A., Hensel, C., Klauck, M., Klein, J., Křetı́nskỳ, J., Parker, D.,
    Quatmann, T., Ruijters, E., Steinmetz, M.: The 2019 comparison of tools for the analysis of
    quantitative formal models: (QComp 2019 competition report). In: TACAS’19. pp. 69–92.
    Springer (2019)
24. Hamers, R., Jongmans, S.: Discourje: Runtime verification of communication protocols in
    clojure. In: TACAS’20. pp. 266–284 (2020)
25. Hensel, C., Junges, S., Katoen, J.P., Quatmann, T., Volk, M.: The probabilistic model checker
    storm. International Journal on Software Tools for Technology Transfer pp. 1–22 (2021)
26. Hoeffding, W.: Probability inequalities for sums of bounded random variables. The collected
    works of Wassily Hoeffding pp. 409–426 (1994)
27. Huang, C., Fan, J., Chen, X., Li, W., Zhu, Q.: Polar: A polynomial arithmetic framework for
    verifying neural-network controlled systems. In: ATVA’22. pp. 414–430. Springer (2022)
28. Ivanov, R., Carpenter, T., Weimer, J., Alur, R., Pappas, G., Lee, I.: Verisig 2.0: Verification
    of neural network controllers using taylor model preconditioning. In: CAV’21. pp. 249–262.
    Springer (2021)
29. Jin, P., Tian, J., Zhi, D., et al.: Trainify: A CEGAR-driven training and verification framework
    for safe deep reinforcement learning. In: CAV’22. pp. 193–218. Springer (2022)
30. Kwiatkowska, M., Norman, G., Parker, D.: Prism 4.0: Verification of probabilistic real-time
    systems. In: CAV’11. pp. 585–591. Springer (2011)
31. Kwiatkowska, M., Norman, G., Parker, D.: Probabilistic model checking and autonomy.
    Annu. Rev. Control Robot. Auton. Syst. 5, 385–410 (2022)
32. Lavaei, A., Soudjani, S., Frazzoli, E.: Safety barrier certificates for stochastic hybrid systems.
    In: ACC’22. pp. 880–885. IEEE (2022)
33. Lechner, M., Zikelic, D., Chatterjee, K., Henzinger, T.A.: Stability verification in stochastic
    control systems via neural network supermartingales. In: AAAI’22. pp. 7326–7336 (2022)
34. Lillicrap, T., Hunt, J., Pritzel, A., Heess, N., Erez, T., Tassa, Y., Silver, D., Wierstra, D.:
    Continuous control with deep reinforcement learning. CoRR abs/1509.02971 (2015)
35. Lillicrap, T., Hunt, J., Pritzel, A., Heess, N., Erez, T., Tassa, Y., Silver, D., Wierstra, D.:
    Continuous control with deep reinforcement learning. In: ICLR (2016)
22       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

36. Mathiesen, F.B., Calvert, S.C., Laurenti, L.: Safety certification for stochastic systems via
    neural barrier functions. IEEE Control Syst. Lett. 7, 973–978 (2022)
37. Meng, Y., Qin, Z., Fan, C.: Reactive and safe road user simulations using neural barrier
    certificates. In: IROS’21. pp. 6299–6306. IEEE (2021)
38. Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D., Riedmiller,
    M.A.: Playing atari with deep reinforcement learning. CoRR abs/1312.5602 (2013)
39. Peruffo, A., Ahmed, D., Abate, A.: Automated and formal synthesis of neural barrier certifi-
    cates for dynamical models. In: TACAS’21. pp. 370–388. Springer (2021)
40. Prajna, S., Jadbabaie, A.: Safety verification of hybrid systems using barrier certificates. In:
    Alur, R., Pappas, G.J. (eds.) HSCC’04. pp. 477–492. Springer (2004)
41. Prajna, S., Jadbabaie, A., Pappas, G.J.: A framework for worst-case and stochastic safety
    verification using barrier certificates. IEEE Trans. Automat. Contr. 52(8), 1415–1428 (2007)
42. Prajna, S., Rantzer, A.: On the necessity of barrier certificates. IFAC Proceedings Volumes
    38(1), 526–531 (2005)
43. Ruan, W., Huang, X., Kwiatkowska, M.: Reachability analysis of deep neural networks with
    provable guarantees. In: IJCAI’18. pp. 2651–2659 (2018)
44. Salamati, A., Lavaei, A., Soudjani, S., Zamani, M.: Data-driven safety verification of stochas-
    tic systems via barrier certificates. In: ADHS’21. pp. 7–12. Elsevier (2021)
45. Samek, W., Montavon, G., Lapuschkin, S., et al.: Explaining deep neural networks and be-
    yond: A review of methods and applications. Proc. of the IEEE 109(3), 247–278 (2021)
46. Seshia, S.A., Sadigh, D., Sastry, S.S.: Toward verified artificial intelligence. Communications
    of the ACM 65(7), 46–55 (2022)
47. Sha, M., Chen, X., Ji, Y., Zhao, Q., Yang, Z., Lin, W., Tang, E., Chen, Q., Li, X.: Synthesizing
    barrier certificates of neural network controlled continuous systems via approximations. In:
    DAC’21. pp. 631–636. IEEE (2021)
48. Steinhardt, J., Tedrake, R.: Finite-time regional verification of stochastic non-linear systems.
    Int. J. Robotics Res. 31(7), 901–923 (2012)
49. Takisaka, T., Oyabu, Y., Urabe, N., Hasuo, I.: Ranking and repulsing supermartingales for
    reachability in probabilistic programs. In: ATVA’18. pp. 476–493. Springer (2018)
50. Takisaka, T., Oyabu, Y., Urabe, N., Hasuo, I.: Ranking and repulsing supermartingales for
    reachability in randomized programs. ACM Trans. Prog. Lang. Syst. 43(2), 5:1–5:46 (2021)
51. Tschaikowski, M., Tribastone, M.: Tackling continuous state-space explosion in a markovian
    process algebra. Theoretical Computer Science 517, 1–33 (2014)
52. Urabe, N., Hara, M., Hasuo, I.: Categorical liveness checking by corecursive algebras. In:
    LICS’17. pp. 1–12. IEEE (2017)
53. Ville, J.: Etude critique de la notion de collectif (1939)
54. Wan, X., Zeng, L., Sun, M.: Exploring the vulnerability of deep reinforcement learning-based
    emergency control for low carbon power systems. In: IJCAI’22. pp. 3954–3961 (2022)
55. Williams, D.: Probability with martingales. Cambridge university press (1991)
56. Winkler, T., Gehnen, C., Katoen, J.: Model checking temporal properties of recursive prob-
    abilistic programs. In: FOSSACS’22. pp. 449–469. Springer (2022)
57. Xia, J., Hu, M., Chen, X., Chen, M.: Accelerated synthesis of neural network-based bar-
    rier certificates using collaborative learning. In: Proceedings of the 59th ACM/IEEE Design
    Automation Conference. pp. 1201–1206 (2022)
58. Xu, K., Shi, Z., Zhang, H., Wang, Y., Chang, K., Huang, M., et al.: Automatic perturbation
    analysis for scalable certified robustness and beyond. In: NeurIPS’20 (2020)
59. Xue, B.: A new framework for bounding reachability probabilities of continuous-time
    stochastic systems. CoRR abs/2312.15843 (2023)
60. Xue, B., Fränzle, M., Zhan, N.: Inner-approximating reachable sets for polynomial systems
    with time-varying uncertainties. IEEE Trans. Autom. Control. 65(4), 1468–1483 (2020)
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems              23

61. Xue, B., Li, R., Zhan, N., Fränzle, M.: Reach-avoid analysis for stochastic discrete-time
    systems. In: ACC’21. pp. 4879–4885. IEEE (2021)
62. Xue, B., Zhan, N., Fränzle, M.: Reach-avoid analysis for polynomial stochastic differential
    equations. IEEE Trans. Autom. Control. (2023)
63. Yang, Z., Zhang, Y., Lin, W., Zeng, X., Tang, X., Zeng, Z., Liu, Z.: An iterative scheme
    of safe reinforcement learning for nonlinear systems via barrier certificate generation. In:
    CAV’21. pp. 467–490. Springer (2021)
64. Zeng, X., Yang, Z., Zhang, L., Tang, X., Zeng, Z., Liu, Z.: Safety verification of nonlinear
    systems with bayesian neural network controllers. In: AAAI’23. pp. 15278–15286 (2023)
65. Zhang, H., Gu, J., Zhang, Z., Du, L., et al.: Backdoor attacks against deep reinforcement
    learning based traffic signal control systems. Peer Peer Netw. Appl. 16(1), 466–474 (2023)
66. Zhang, H., Chen, H., Boning, D.S., Hsieh, C.: Robust reinforcement learning on state obser-
    vations with learned optimal adversary. In: ICLR’21 (2021)
67. Zhang, H., Chen, H., Xiao, C., Li, B., Liu, M., Boning, D.S., Hsieh, C.: Robust deep rein-
    forcement learning against adversarial perturbations on state observations. In: NeurIPS’20.
    pp. 21024–21037 (2020)
68. Zhao, H., Qi, N., Dehbi, L., Zeng, X., Yang, Z.: Formal synthesis of neural barrier certificates
    for continuous systems via counterexample guided learning. ACM Trans. Embed. Comput.
    Syst. 22(5s), 146:1–146:21 (2023)
69. Zhao, H., Zeng, X., Chen, T., Liu, Z.: Synthesizing barrier certificates using neural networks.
    In: HSCC’20. pp. 1–11 (2020)
70. Zikelic, D., Lechner, M., Henzinger, T.A., Chatterjee, K.: Learning control policies for
    stochastic systems with reach-avoid guarantees. In: AAAI’23. pp. 11926–11935 (2023)
24       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

                                        Appendix
1    Probability Theory
We start by reviewing some notions from probability theory.
Random Variables and Stochastic Processes. A probability space is a triple (Ω, F , P),
where Ω is a non-empty sample space, F is a 𝜎-algebra over Ω, and P(·) is a probability
measure over F , i.e. a function P: F → [0, 1] that satisfiesÍthe following properties: (1)
                                                               ∞
P(∅) = 0, (2)P(Ω − 𝐴) = 1 − P[ 𝐴], and (3) P(∪∞   𝑖=0 𝐴𝑖 ) =   𝑖=0 P( 𝐴𝑖 ) for any sequence
      ∞
{ 𝐴𝑖 }𝑖=0 of pairwise disjoint sets in F .
     Given a probability space (Ω, F , P), a random variable is a function 𝑋 : Ω → R ∪
{∞} that is F -measurable, i.e., for each 𝑎 ∈ R we have that {𝜔 ∈ Ω|𝑋 (𝜔) ≤ 𝑎} ∈ F .
Moreover, a discrete-time stochastic process is a sequence {𝑋𝑛 }∞  𝑛=0 of random variables
in (Ω, F , P).
Conditional Expectation. Let (Ω, F , P) be a probability space and 𝑋 be a random
variable in (Ω, F , P). The expected value of the random variable 𝑋, denoted by E[𝑋],
is
Í the Lebesgue integral of 𝑋 wrt P. If the range of 𝑋   is a countable set 𝐴, then E[𝑋] =
                                                     ′
   𝜔 ∈ 𝐴 𝜔 · P(𝑋 = 𝜔). Given a sub-sigma-algebra F ⊆ F , a conditional expectation of
𝑋 for the given F ′ is a F ′ -measurable random variable 𝑌 such that, for any 𝐴 ∈ F ′ ,
we have:

                                    E[𝑋 · I 𝐴] = E[𝑌 · I 𝐴]                                 (48)

Here, I 𝐴 : Ω → {0, 1} is an indicator function of 𝐴, defined as I 𝐴 (𝜔) = 1 if 𝜔 ∈ 𝐴
and I 𝐴 (𝜔) = 0 if 𝜔 ∉ 𝐴. Moreover, whenever the conditional expectation exists, it is
also almost-surely unique, i.e., for any two F ′ -measurable random variables 𝑌 and 𝑌 ′
which are conditional expectations of 𝑋 for given F ′ , we have that P(𝑌 = 𝑌 ′ ) = 1.
Filtrations and Stopping Times. A filtration of the probability space (Ω, F , P) is an
infinite sequence {F𝑛 }∞   𝑛=0 such that for every 𝑛, the triple (Ω, F𝑛 , P) is a probability
space and F𝑛 ⊆ F𝑛+1 ⊆ F . A stopping time with respect to a filtration {F𝑛 }∞              𝑛=0 is
a random variable 𝑇 : Ω → N0 ∪ {∞} such that, for every 𝑖 ∈ N0 , it holds that
{𝜔 ∈ Ω|𝑇 (𝜔) ≤ 𝑖} ∈ F𝑖 . Intuitively, 𝑇 returns the time step at which some stochastic
process shows a desired behavior and should be “stopped”.
    A discrete-time stochastic process {𝑋𝑛 }∞        𝑛=0 in (Ω, F , P) is adapted to a filtration
{F𝑛 }∞𝑛=0 , if for all 𝑛 ≥ 0, 𝑋 𝑛 is a  random  variable  in (Ω, F𝑛 , P).
                                  ∞
Stopped Process. Let {𝑋𝑛 } 𝑛=0 be a stochastic process adapted to a filtration {F𝑛 }∞         𝑛=0
and let 𝑇 be a stopping time w.r.t. {F𝑛 }∞                                  ˜ ∞
                                              𝑛=0 . The stopped process { 𝑋𝑛 } 𝑛=0 is defined by
                                            (
                                              𝑋𝑛 , for 𝑛 < 𝑇,
                                     𝑋˜ 𝑛 =
                                              𝑋𝑇 , for 𝑛 ≥ 𝑇 .

Martingales. A discrete-time stochastic process {𝑋𝑛 }∞                              ∞
                                                          𝑛=0 to a filtration {F𝑛 } 𝑛=0 is a
martingale (resp. supermartingale, submartingale) if for all 𝑛 ≥ 0, E[|𝑋𝑛 |] < ∞ and it
holds almost surely (i.e., with probability 1) that E[𝑋𝑛+1 |F𝑛 ] = 𝑋𝑛 (resp. E[𝑋𝑛+1 |F𝑛 ] ≤
𝑋𝑛 , E[𝑋𝑛+1 |F𝑛 ] ≥ 𝑋𝑛 ).
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems          25

Ranking Supermartingales. Let 𝑇 be a stopping time w.r.t. a filtration {F𝑛 }∞      𝑛=0 . A
discrete-time stochastic process {𝑋𝑛 }∞  𝑛=0 w.r.t. a stopping time 𝑇 is a ranking super-
martingale (RSM) if for all 𝑛 ≥ 0, E[|𝑋𝑛 |] < ∞ and there exists 𝜖 > 0 such that it holds
almost surely (i.e., with probability 1) that 𝑋𝑛 ≥ 0 and E[𝑋𝑛+1 |F𝑛 ] ≤ 𝑋𝑛 − 𝜖 · I𝑇 >𝑛 .

Theorem 13 (Hoeffding’s Inequality on Supermartingales [26]). Let {𝑋𝑛 } 𝑛∈N0 be a
supermartingale w.r.t. a filtration {F𝑛 } 𝑛∈N0 , and {[𝑎 𝑛 , 𝑏 𝑛 ]} 𝑛∈N0 be a sequence of non-
empty intervals in R. If 𝑋0 is a constant random variable and 𝑋𝑛+1 − 𝑋𝑛 ∈ [𝑎 𝑛 , 𝑏 𝑛 ] a.s.
for all 𝑛 ∈ N0 , then
                                                                         !
                                                           2𝜆2
                      P(𝑋𝑛 − 𝑋0 ≥ 𝜆) ≤ exp − Í𝑛−1
                                                                       2
                                                     𝑘=0 (𝑏 𝑘 − 𝑎 𝑘 )

for all 𝑛 ∈ N0 and 𝜆 > 0.

Theorem 14 (Optional Stopping Theorem (OST) [55]). Consider a stopping time
𝑇 w.r.t. a filtration {F𝑛 }∞
                           𝑛=0 and a martingale (resp. supermartingale, submartingale)
{𝑋𝑛 }∞
     𝑛=0  adapted   to {F𝑛 } ∞ . Then E[|𝑋 |] < ∞ and E[𝑋 ] = E[𝑋 ] (resp. E[𝑋 ] ≤
                             𝑛=0           𝑇                𝑇       0            𝑇
E[𝑋0 ], E[𝑋𝑇 ] ≥ E[𝑋0 ]) if one of the following conditions holds:

    – 𝑇 is bounded, i.e., 𝑇 < 𝑐 for some constant 𝑐;
    – E[𝑇] < ∞, and there exists a constant 𝑐 such that for all 𝑛 ∈ N, |𝑋𝑛+1 − 𝑋𝑛 | ≤ 𝑐;
    – The stopped process { 𝑋˜ 𝑛 }∞  𝑛=0 w.r.t. 𝑇 is bounded, i.e., there exists some constant 𝑐
      such that | 𝑋˜ 𝑛 | ≤ 𝑐 for all 𝑛 ∈ N.

Theorem 15 (Ville’s Inequality [53]). For any nonnegative supermartingale {𝑋𝑛 }∞
                                                                               𝑛=0
and any real number 𝑐 > 0,
                                                             E[𝑋0 ]
                                 P[sup𝑛≥0 𝑋𝑛 ≥ 𝑐] ≤                 .
                                                               𝑐
This theorem is also called Doob’s nonnegative supermartingale inequality.

Theorem 16 (Discrete Version of Gronwall’s Inequality [22]). Consider a real num-
ber sequence {𝑢 𝑛 }∞
                   𝑛=0 such that

                                   𝑢 𝑛+1 ≤ 𝑎 · 𝑢 𝑛 + 𝑏 ∀𝑛 ≥ 0
where 𝑎 > 0 and 𝑏 ∈ R. Then
                                                    𝑛
                                                   ∑︁
                             𝑢 𝑛+1 ≤ 𝑎 𝑛 · 𝑢 0 +         𝑎 𝑛−𝑘 · 𝑏 ∀𝑛 ≥ 0
                                                   𝑘=1

2     Supplementary Materials for Section 4
Below we fix a DNN-controlled system 𝑀 𝜇 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅, 𝜇) with an unsafe set
𝑆𝑢 ∈ 𝑆 such that 𝑆0 ∩ 𝑆𝑢 = ∅. We also define 1 𝐴 (𝑥) = 1 if 𝑥 ∈ 𝐴 and 1 𝐴 (𝑥) = 0 if 𝑥 ∉ 𝐴,
where 𝑥 ∈ R is a random variable and 𝐴 ⊆ R is a set.
26      Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

2.1   Proof for Section 4.1

Theorem 1 (Almost-Surely Safety). Given an 𝑀 𝜇 with an initial set 𝑆0 and an unsafe
set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such that for some constant
𝜆 ∈ (0, 1], the following conditions hold:

        𝐵(𝑠) ≤ 0                                                           for all 𝑠 ∈ 𝑆0 ,    (4)
        𝐵(𝑠) > 0                                                           for all 𝑠 ∈ 𝑆𝑢 ,    (5)
        𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) − 𝐵(𝑠) + 𝜆 · 𝐵(𝑠) ≤ 0              for all (𝑠, 𝛿) ∈ 𝑆 × 𝑊,         (6)
then the system 𝑀 𝜇 is almost-surely safe, i.e., ∀𝑠0 ∈ 𝑆0 .𝜔 ∈ Ω𝑠0 =⇒ 𝜔𝑡 ∉ 𝑆𝑢 ∀𝑡 ∈ N.

Proof. We prove it by contradiction. Assume that there exists a barrier certificate 𝐵
satisfying conditions (4)-(6), but the system is unsafe, i.e., there are a time step 𝑇 > 0
and an initial state 𝑠0 ∈ 𝑆0 such that a trajectory 𝜔 ∈ Ω𝑠0 starting from 𝑠0 satisfies
𝜔𝑡 ∈ 𝑆 for all 𝑡 ∈ [0, 𝑇] and 𝜔𝑇 ∈ 𝑆𝑢 . Condition (6) implies that for any state 𝑠 ∈ 𝑆
such that 𝐵(𝑠) ≤ 0 and a noise 𝛿 ∈ 𝑊, the value of 𝐵 at the next step is no more than
zero, i.e., 𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) ≤ 0. As a result, 𝐵(𝜔𝑇 ) must be no more than zero, which
is contradictory to Condition (5). Therefore, the system with a BC is almost-surely safe.
                                                                                         ⊔
                                                                                         ⊓

2.2   Proofs for Section 4.2

Theorem 2 (Lower Bounds on Infinite-time Safety). Given an 𝑀 𝜇 with an initial set
𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such that for some
constant 𝜖 ∈ [0, 1], the following conditions hold:
          𝐵(𝑠) ≥ 0                                                         for all 𝑠 ∈ 𝑆,      (7)
          𝐵(𝑠) ≤ 𝜖                                                        for all 𝑠 ∈ 𝑆0 ,     (8)
          𝐵(𝑠) ≥ 1                                                        for all 𝑠 ∈ 𝑆𝑢 ,     (9)
          E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 0               for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,       (10)
then the safety probability over infinite time horizons is bounded from below by
                                                               
          ∀𝑠 − 0 ∈ 𝑆0 .P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ∈∈ N} ≥ 1 − 𝐵(𝑠0 ).                   (11)

Proof. First, we construct a stochastic process {𝑋𝑡 }𝑡 ≥0 over the set Ω of all trajectories
such that 𝑋𝑡 (𝜔) := 𝐵(𝜔𝑡 ) for any 𝜔 ∈ Ω. Let 𝜅 be the first time that a trajectory enters
the unsafe set 𝑆𝑢 , i.e., 𝜅(𝜔) := inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Then we define the stopped
process { 𝑋˜ 𝑡 }𝑡 ≥0 by
                                      (
                                 ˜      𝑋𝑡 , for 𝑡 < 𝜅,
                                 𝑋𝑡 =
                                        𝑋 𝜅 , for 𝑡 ≥ 𝜅.

Next, we want to prove that { 𝑋˜ 𝑡 }𝑡 ≥0 is a non-negative supermartingale. For 𝑡 < 𝜅, we
have that
                        E[ 𝑋˜ 𝑡+1 | F̃𝑡 ] = E[𝑋𝑡+1 | F𝑡 ] ≤ 𝑋𝑡 = 𝑋˜ 𝑡 ,
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems           27

where the inequality is obtained by Condition (10). For 𝑡 ≥ 𝜅, we have that

                                   E[ 𝑋˜ 𝑡+1 | F̃𝑡 ] = 𝑋 𝜅 = 𝑋˜ 𝑡 .
Combined with Condition (7), we can conclude that { 𝑋˜ 𝑡 }𝑡 ≥0 is a non-negative super-
martingale. According to Condition (9), we have that 𝑆𝑢 ⊆ {𝑠 ∈ 𝑆 | 𝐵(𝑠) ≥ 1}.
Therefore, for any initial state 𝑠0 ∈ 𝑆0 , it follows that
                                                                
                         P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∈ 𝑆𝑢 for some 𝑡 ∈ N}
                                                            
                      ≤ P𝑠0 {𝜔 ∈ Ω𝑠0 | sup𝑡 ∈N 𝑋𝑡 (𝜔) ≥ 1}
                      = P𝑠0 {𝜔 ∈ Ω𝑠0 | sup𝑡 ∈N 𝑋˜ 𝑡 (𝜔) ≥ 1}
                                                            

                        ≤ 𝑋˜ 0 (𝜔) = 𝑋0 (𝜔)

where the last inequality is derived by Ville’s Inequality (see Theorem 15). Finally, by
means of complementation, we have the lower bound of Equation (11).                    ⊔
                                                                                       ⊓

    Theorem 3 (Upper Bounds on Infinite-time Safety). Given an 𝑀 𝜇 with an initial
set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such that for
some constants 𝛾 ∈ (0, 1), 0 ≤ 𝜖 ′ < 𝜖 ≤ 1, the following conditions hold:

        0 ≤ 𝐵(𝑠) ≤ 1                                                       for all 𝑠 ∈ 𝑆,    (12)
         𝐵(𝑠) ≥ 𝜖                                                         for all 𝑠 ∈ 𝑆0 ,   (13)
                    ′
         𝐵(𝑠) ≤ 𝜖                                                         for all 𝑠 ∈ 𝑆𝑢 ,   (14)
         𝐵(𝑠) − 𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] ≤ 0               for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,   (15)
then the safety probability over infinite time horizons is bounded from above by
                                                             
             ∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ∈ N} ≤ 1 − 𝐵(𝑠0 ).                   (16)

Proof. Construct a stochastic process {𝑋𝑡 }𝑡 ≥0 over the set Ω of all trajectories such that
𝑋𝑡 (𝜔) := 𝐵(𝑠𝑡 ) for any 𝜔 ∈ Ω. Let 𝜅 be a stopping time at which the state first enters
𝑆𝑢 , i.e., 𝜅(𝜔) := inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Then construct a new stochastic process {𝑌𝑡 }𝑡 ≥0
such that 𝑌𝑡 := 𝛾 𝑡 𝑋𝑡 . The stopped process {𝑌˜𝑡 }𝑡 ≥0 is defined by
                                         (
                                          𝑌𝑡 , for 𝑡 < 𝜅,
                                   𝑌˜𝑡 =
                                          𝑌𝜅 , for 𝑡 ≥ 𝜅.

Next, we want to prove that {𝑌˜𝑡 }𝑡 ≥0 is a submartingale. For 𝑡 < 𝜅, we have that

                    E[𝑌˜𝑡+1 | F̃𝑡 ] = E[𝑌𝑡+1 | F𝑡 ]
                                  = E[𝛾 𝑡+1 𝑋𝑡+1 | F𝑡 ] = 𝛾 𝑡+1 E[𝑋𝑡+1 | F𝑡 ]
                                  = 𝛾 𝑡 · 𝛾E[𝑋𝑡+1 | F𝑡 ] ≥ 𝛾 𝑡 𝑋𝑡 = 𝑌˜𝑡

where the inequality is obtained by Condition (15). For 𝑡 ≥ 𝜅, we have that
                                    E[𝑌˜𝑡+1 | F̃𝑡 ] = 𝑌𝜅 = 𝑌˜𝑡
28      Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

By Condition (12), 𝑌˜𝑡 ∈ [0, 1]. Thus, {𝑌˜𝑡 }𝑡 ≥0 is a submartingale satisfying the third
condition of the Optional Stopping Theorem (OST) (see Theorem 14). By applying
OST, we obtain that
           𝑋0 = E[𝑌˜0 ] ≤ E[𝑌˜𝜅 ] = E[𝛾 𝜅 𝑋 𝜅 ]
              = E[𝛾 𝜅 𝑋 𝜅 | 𝜅 < ∞]P𝑠0 (𝜅 < ∞) + E[𝛾 𝜅 𝑋 𝜅 | 𝜅 = ∞]P𝑠0 (𝜅 = ∞)
              = E[𝛾 𝜅 𝑋 𝜅 | 𝜅 < ∞]P𝑠0 (𝜅 < ∞) + 0 ≤ P𝑠0 (𝜅 < ∞)
                                                        
              = P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∈ 𝑆𝑢 for some 𝑡 ∈ N}
where the fourth equality is derived from the fact that 𝛾 𝜅 𝑋 𝜅 = 0 for 𝜅 = ∞ as 𝛾 ∈ (0, 1)
and the second inequality stems from the fact that 𝛾 𝜅 𝑋 𝜅 ≤ 1. Finally, by means of
complementation, we obtain the upper bound of Equation (16).                             ⊔
                                                                                         ⊓

2.3   Proofs for Section 4.3
Theorem 4 (Linear Lower Bounds on Finite-time Safety). Given an 𝑀 𝜇 with an
initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R such
that for some constants 𝜆 > 𝜖 ≥ 0 and 𝑐 ≥ 0, the following conditions hold:
           𝐵(𝑠) ≥ 0                                                 for all 𝑠 ∈ 𝑆,     (17)
           𝐵(𝑠) ≤ 𝜖                                                for all 𝑠 ∈ 𝑆0 ,    (18)
           𝐵(𝑠) ≥ 𝜆                                                for all 𝑠 ∈ 𝑆𝑢 ,    (19)
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝑐               for all 𝑠 ∈ 𝑆,     (20)
then the safety probability over a finite time horizon 𝑇 is bounded from below by
                                                          
      ∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 | 𝜔 ∈ Ω𝑠0 , 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≥ 1 − (𝐵(𝑠0 ) + 𝑐𝑇)/𝜆.

Proof. Construct a stochastic process {𝑋𝑡 }𝑡 ≥0 over the set Ω of all trajectories such that
𝑋𝑡 (𝜔) := 𝐵(𝑠𝑡 ) for any 𝜔 ∈ Ω. Let 𝜅 be a stopping time at which the state first enters
𝑆𝑢 , i.e., 𝜅(𝜔) := inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Then construct a new stochastic process {𝑌𝑡 }𝑡 ≥0
such that 𝑌𝑡 := 𝑋𝑡 + (𝜅 − 𝑡)𝑐. The stopped process {𝑌˜𝑡 }𝑡 ≥0 is defined by
                                        (
                                   ˜      𝑌𝑡 , for 𝑡 < 𝜅,
                                  𝑌𝑡 =
                                          𝑌𝜅 , for 𝑡 ≥ 𝜅.

Next, we want to prove that {𝑌˜𝑡 }𝑡 ≥0 is a non-negative supermartingale. According to
Condition (17), {𝑌˜𝑡 }𝑡 ≥0 is non-neagtive. For 𝑡 < 𝜅, we have that
                E[𝑌˜𝑡+1 | F̃𝑡 ] = E[𝑌𝑡+1 | F𝑡 ] = E[𝑋𝑡+1 + (𝜅 − 𝑡 − 1)𝑐 | F𝑡 ]
                              = E[𝑋𝑡+1 | F𝑡 ] + (𝜅 − 𝑡)𝑐 − 𝑐
                              ≤ 𝑋𝑡 + 𝑐 + (𝜅 − 𝑡)𝑐 − 𝑐
                              = 𝑋𝑡 + (𝜅 − 𝑡)𝑐 = 𝑌𝑡 = 𝑌˜𝑡

where the inequality is obtained by Condition (20). For 𝑡 ≥ 𝜅, we have that
                                   E[𝑌˜𝑡+1 | F̃𝑡 ] = 𝑌𝜅 = 𝑌˜𝑡
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems            29

Therefore, we can conclude that {𝑌˜𝑡 }𝑡 ≥0 is a non-negative supermartingale. By Ville’s
Inequality (Theorem 15), we have that for a constant 𝜆′ > 0,
                                                                        𝑋0 + 𝑐𝜅
                   P[sup𝑡 ∈ [0,𝜅 ] 𝑌𝑡 ≥ 𝜆′ ] = P[sup𝑡 ∈N𝑌˜𝑡 ≥ 𝜆′ ] ≤
                                                                          𝜆′
By the definition, 𝑌𝑡 ≥ 𝜆′ ⇔ 𝑋𝑡 ≥ 𝜆′ − (𝜅 − 𝑡)𝑐 := 𝑟 𝑡 , so we have that P[sup𝑡 ∈ [0,𝜅 ] 𝑋𝑡 ≥
sup𝑡 ∈ [0,𝜅 ] 𝑟 𝑡 ] ≤ 𝑋0𝜆+𝑐𝜅
                          ′  . As the maximum of 𝑟 𝑡 in [0, 𝜅] is 𝜆′ , let 𝜆 = 𝜆′ , we can derive
that
                                                          𝑋0 + 𝑐𝜅
                              P[sup𝑡 ∈ [0,𝜅 ] 𝑋𝑡 ≥ 𝜆] ≤           ,
                                                             𝜆
which by Condition (19) implies that
                                                                           𝑋0 (𝜔) + 𝑐𝜅
           ∀𝑠0 ∈ 𝑆0 .P𝑠0 [{𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∈ 𝑆𝑢 for some 𝑡 ≤ 𝜅}] ≤
                                                                                𝜆
Finally, by means of complementation, we obtain the lower bound of Equation (21).
                                                                                                ⊔
                                                                                                ⊓

    Theorem 5 (Exponential Lower Bounds on Finite-time Safety). Given an 𝑀 𝜇
with an initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a function 𝐵 : 𝑆 → R such that
for some constants 𝛼 > 0, 𝛽 ∈ R, and 𝛾 ∈ [0, 1), the following conditions hold:
         𝐵(𝑠) ≥ 0                                                           for all 𝑠 ∈ 𝑆,    (21)
         𝐵(𝑠) ≤ 𝛾                                                          for all 𝑠 ∈ 𝑆0 ,   (22)
         𝐵(𝑠) ≥ 1                                                          for all 𝑠 ∈ 𝑆𝑢 ,   (23)
         𝛼E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝛼𝛽                  for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 .   (24)
then the safety probability over a finite time horizon 𝑇 is bounded from below by
                                                           𝛼𝛽    𝛼𝛽
                                                                    −𝐵(𝑠0 ))·𝛼 −𝑇 .
                                                   
∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 | 𝜔 ∈ Ω𝑠0 , 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≥ 1−     +(
                                                          𝛼−1 𝛼−1
                                                                              (25)

Proof. Construct a stochastic process {𝑋𝑡 }𝑡 ≥0 over the set Ω of all trajectories such that
𝑋𝑡 (𝜔) := 𝜔𝑡 for any 𝜔 ∈ Ω. Let 𝜅 be the first time that a trajectory enters the unsafe set
𝑆𝑢 , i.e., 𝜅(𝜔) := inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Define the stopped process { 𝑋˜ 𝑡 }𝑡 ≥0 by
                                         (
                                           𝑋𝑡 , for 𝑡 < 𝜅,
                                  𝑋˜ 𝑡 =
                                           𝑋 𝜅 , for 𝑡 ≥ 𝜅.

According to Condition (24) and the law of total expectation, we have that

                              𝛼E[𝐵( 𝑋˜ 𝑡+1 ) | F̃𝑡 ] − 𝐵( 𝑋˜ 𝑡 ) ≤ 𝛼𝛽
                                                      𝐵( 𝑋˜ 𝑡 )
                            ⇒ E[𝐵( 𝑋˜ 𝑡+1 ) | F̃𝑡 ] ≤           +𝛽
                                                         𝛼
                                                  E[𝐵( 𝑋˜ 𝑡 )]
                            ⇒ E[𝐵( 𝑋˜ 𝑡+1 )] ≤                  +𝛽                            (49)
                                                      𝛼
30       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

Next, define a new stochastic process {𝑌𝑡 }𝑡 ≥0 such that 𝑌𝑡 := E[𝐵( 𝑋˜ 𝑡 )]. By Equa-
tion (49), we obtain that 𝑌𝑡+1 ≤ 𝑌𝛼𝑡 + 𝛽. By the discrete version of Gronwall’s Inequality
(see Theorem 16), we have that
                              𝑡     𝑡
                                            !                    𝑡 h
                            ∑︁    Ö                             ∑︁                   i
                   −𝑡                    −1
            𝑌𝑡 ≤ 𝛼 · 𝑌0 +              𝛼      · 𝛽 = 𝛼 −𝑡 · 𝑌0 +      𝛼 − (𝑡 −𝑘 ) · 𝛽
                             𝑘=1 𝑖=𝑘+1                                𝑘=1
                                           𝑡
                                          ∑︁                                   𝛼(1 − 𝛼𝑡 )
               = 𝛼 −𝑡 · 𝑌0 + 𝛼 −𝑡 · 𝛽 ·         𝛼 𝑘 = 𝛼 −𝑡 · 𝑌0 + 𝛼 −𝑡 · 𝛽 ·
                                          𝑘=1
                                                                                 1−𝛼
                              𝛼𝛽   𝛼𝛽
               = 𝛼 −𝑡 · 𝑌0 +     −    · 𝛼 −𝑡                                                      (50)
                             𝛼−1 𝛼−1
Pick a time step 𝑇 > 0. It is observed that {𝜔 ∈ Ω | 𝑋𝑡 (𝜔) ∈ 𝑆𝑢 for some 𝑡 ≤ 𝑇 } =
{𝜔 ∈ Ω | 𝑋˜ 𝑇 ∈ 𝑆𝑢 }. Thus, we have that
                            P[𝑋𝑡 ∈ 𝑆𝑢 for some 𝑡 ≤ 𝑇]
                          =P[ 𝑋˜ 𝑇 ∈ 𝑆𝑢 ] = E[1𝑆𝑢 ( 𝑋˜ 𝑇 )]
                          ≤E[𝐵( 𝑋˜ 𝑇 )]
                                                   𝛼𝛽   𝛼𝛽
                          ≤𝛼 −𝑇 · 𝐵(𝑋0 ) +            −    · 𝛼 −𝑇
                                                  𝛼−1 𝛼−1
where the first inequality is obtained by Conditions (21) and (23), the second inequality
is derived by Equation (50). Finally, by means of complementation, we obtain the lower
bound.


     Theorem 6 (Linear Upper Bounds on Finite-time Safety) Given an 𝑀 𝜇 with an
initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier function 𝐵 : 𝑆 → R such that
for some constants 𝛽 ∈ (0, 1), 𝛽 < 𝛼 < 1 + 𝛽, 𝑐 ≥ 0, the following conditions hold:
          𝐵(𝑠) ≥ 0                                                              for all 𝑠 ∈ 𝑆,    (25)
          𝐵(𝑠) ≤ 𝛽                                                     for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,       (26)
          𝛼 ≤ 𝐵(𝑠) ≤ 1 + 𝛽                                                     for all 𝑠 ∈ 𝑆𝑢 ,   (27)
          E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≥ 𝑐                   for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 .       (28)
then the safety probability over a finite time horizon is bounded from above by
                                                                       1
     ∀𝑠0 ∈ 𝑆0 . P𝑠0 {𝜔 | 𝜔 ∈ Ω𝑠0 , 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≤ 1 − 𝐵(𝑠0 ) − 𝑐 · 𝑇 + 𝛽.
                                                                         2


Proof. Construct a stochastic process {𝑋𝑡 }𝑡 ≥0 over the set Ω of all trajectories such that
𝑋𝑡 (𝜔) := 𝜔𝑡 for any 𝜔 ∈ Ω. Let 𝜅 be the first time that a trajectory enters the unsafe set
𝑆𝑢 , i.e., 𝜅(𝜔) := inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Define the stopped process { 𝑋˜ 𝑡 }𝑡 ≥0 by
                                         (
                                           𝑋𝑡 , for 𝑡 < 𝜅,
                                  𝑋˜ 𝑡 =
                                           𝑋 𝜅 , for 𝑡 ≥ 𝜅.
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems             31

Pick a time step 𝑇 > 0. It is observed that {𝜔 ∈ Ω | 𝑋𝑡 (𝜔) ∈ 𝑆𝑢 for some 𝑡 ≤ 𝑇 } =
{𝜔 ∈ Ω | 𝑋˜ 𝑇 ∈ 𝑆𝑢 }. Thus, we have that

                                P[𝑋𝑡 ∈ 𝑆𝑢 for some 𝑡 ≤ 𝑇]
                              = P[ 𝑋˜ 𝑇 ∈ 𝑆𝑢 ] = E[1𝑆𝑢 ( 𝑋˜ 𝑇 )]                               (51)
Moreover, let 0 ≤ 𝑇1 ≤ 𝑇2 ≤ 𝑇, it is found that {𝜔 ∈ Ω | 𝑋˜ 𝑇1 ∈ 𝑆𝑢 } ⊆ {𝜔 ∈ Ω | 𝑋˜ 𝑇2 ∈
𝑆𝑢 }. Therefore, we have that
                               P[ 𝑋˜ 𝑇1 ∈ 𝑆𝑢 ] ≤ P[ 𝑋˜ 𝑇2 ∈ 𝑆𝑢 ]                               (52)

By Conditions (26) and (27), we have that
                           𝐵( 𝑋˜ 𝑡 ) ≤ 1𝑆𝑢 ( 𝑋˜ 𝑡 ) + 𝛽 for any 𝑡 ≥ 0                          (53)
By Condition (28) and the law of total expectation, we obtain that

                              E[𝐵( 𝑋˜ 𝑡+1 ) | F̃𝑡 ] − 𝐵( 𝑋˜ 𝑡 ) ≥ 𝑐
                            ⇒ E[𝐵( 𝑋˜ 𝑡+1 ) | F̃𝑡 ] ≥ 𝐵( 𝑋˜ 𝑡 ) + 𝑐
                            ⇒ E[𝐵( 𝑋˜ 𝑡+1 )] ≥ E[𝐵( 𝑋˜ 𝑡 )] + 𝑐
By the iterative calculation, we have that E[𝐵( 𝑋˜ 𝑡 )] ≥ 𝐵(𝑋0 ) + 𝑐 · 𝑡. Then we can derive
that

                          P[ 𝑋˜ 𝑇 ∈ 𝑆𝑢 ] =E[1𝑆𝑢 ( 𝑋˜ 𝑇 )]
                                               E[1𝑆𝑢 ( 𝑋˜ 𝑡 )]
                                          Í𝑇
                                         ≥ 𝑡=0
                                                𝑇 +1
                                                         𝑋˜ 𝑡 )] − 𝛽)
                                          Í𝑇
                                               (E[𝐵(
                                         ≥ 𝑡=0
                                                   𝑇 +1
                                          Í𝑇
                                               𝐵(𝑋    0) + 𝑐 · 𝑡
                                         ≥ 𝑡=1                     −𝛽
                                                𝑇 +1
                                                     1
                                         =𝐵(𝑋0 ) + 𝑐 · 𝑇 − 𝛽
                                                     2
where the first equality is obtained by Equation (51), the first inequality stems from
Equation (52) and the second inequality is obtained by Equation (53). Finally, by means
of complementation, we obtain the upper bound.                                       ⊔
                                                                                     ⊓

    Theorem 7 (Exponential Upper Bounds on Finite-Time Safety). Given an 𝑀 𝜇
with an initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier function 𝐵 : 𝑆 → R
such that for some constants 𝐾 ′ ≤ 𝐾 < 0, 𝜖 > 0 and a non-empty interval [𝑎, 𝑏], the
following conditions hold:
    𝐵(𝑠) ≥ 0                                                            for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,   (29)
      ′
    𝐾 ≤ 𝐵(𝑠) ≤ 𝐾                                                            for all 𝑠 ∈ 𝑆𝑢 ,   (30)
    E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ −𝜖                         for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 ,   (31)
    𝑎 ≤ 𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) − 𝐵(𝑠) ≤ 𝑏                  for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 and 𝛿 ∼ 𝜇,          (32)
32        Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

then the safety probability over a finite time horizon 𝑇 is bounded from above by
                                                                 2(𝜖 · 𝑇 − 𝐵(𝑠0 )) 2
     ∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 | 𝜔 ∈ Ω𝑠0 , 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ≤ 𝑒𝑥 𝑝(−                     ).
                                                                     𝑇 · (𝑏 − 𝑎) 2

Proof. Let 𝜅 be a stopping time over the set Ω of all trajectories at which the state first
enters 𝑆𝑢 , i.e., 𝜅(𝜔) := inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Define the stopped process { 𝑋˜ 𝑡 }𝑡 ≥0 by
                                      (
                                        𝐵(𝑠𝑡 ), for 𝑡 < 𝜅,
                                 𝑋𝑡 =
                                        𝐵(𝑠 𝜅 ), for 𝑡 ≥ 𝜅.

Next, we prove that {𝑋𝑡 }𝑡 ≥0 is ranking supermartingale w.r.t. 𝜅, i.e., E[𝑋𝑡+1 |F𝑡 ] ≤
𝑋𝑡 − 𝜖 · 1 𝜅 >𝑡 for all 𝑡 ≥ 0. To prove this inequality, we consider two cases.

 – When 𝜅 > 𝑡, we have that 𝑋𝑡 = 𝐵(𝑠𝑡 ). By Condition (31), we obtain that E[𝑋𝑡+1 |
   F𝑡 ] = E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠𝑡 , 𝜋(𝑠𝑡 + 𝛿))) | 𝑠𝑡 ] ≤ 𝐵(𝑠𝑡 ) − 𝜖 = 𝑋𝑡 − 𝜖.
 – When 𝜅 ≤ 𝑡, we have that 𝑋𝑡 = 𝐵(𝑠 𝜅 ). Then we can obtain that E[𝑋𝑡+1 | F𝑡 ] =
   𝑋 𝜅 = 𝑋𝑡 .

According to the two cases, we can conclude that E[𝑋𝑡+1 |F𝑡 ] ≤ 𝑋𝑡 − 𝜖 · 1 𝜅 >𝑡 for all
𝑡 ≥ 0. Hence, we prove that {𝑋𝑡 }𝑡 ≥0 is a ranking supermartingale w.r.t. 𝜅.
    Construct a new stochastic process {𝑌𝑡 }𝑡 ≥0 such that 𝑌𝑡 := 𝑋𝑡 + 𝜖 · min{𝜅, 𝑡}. Then
we want to prove that {𝑌𝑡 }𝑡 ≥0 is a supermatirngale and 𝑌𝑡+1 − 𝑌𝑡 ∈ [𝑎 + 𝜖, 𝑏 + 𝜖]. First,
we have that
                  E[𝑌𝑡+1 | F𝑡 ] = E[𝑋𝑡+1 + 𝜖 · min{𝑡 + 1, 𝜅} | F𝑡 ]
                               = E[𝑋𝑡+1 | F𝑡 ] + 𝜖 · E[min{𝑡 + 1, 𝜅} | F𝑡 ]
                               ≤ 𝑋𝑡 − 𝜖 · 1 𝜅 >𝑡 + 𝜖 · E[min{𝑡 + 1, 𝜅} | F𝑡 ]
Second, we consider two cases:

 – If 𝜅 > 𝑡, then min{𝑡 + 1, 𝜅} = 𝑡 + 1 and E[min{𝑡 + 1, 𝜅} | F𝑡 ] = 𝑡 + 1. We can thus
   derive that
                    E[𝑌𝑡+1 | F𝑡 ] ≤ 𝑋𝑡 − 𝜖 · 1 𝜅 >𝑡 + 𝜖 · E[min{𝑡 + 1, 𝜅} | F𝑡 ]
                                  = 𝑋𝑡 − 𝜖 + 𝜖 · (𝑡 + 1)
                                  = 𝑋𝑡 + 𝜖 · 𝑡
                                  = 𝑌𝑡

 – If 𝜅 ≤ 𝑡, then min{𝑡 + 1, 𝜅} = 𝜅 = 𝜅 · 1 𝜅 ≤𝑡 . Since the event 𝜅 · 1 𝜅 ≤𝑡 is measurable in
   F𝑡 , E[𝜅 · 1 𝜅 ≤𝑡 | F𝑡 ] = 𝜅 · 1 𝜅 ≤𝑡 . We can thus derive that
                    E[𝑌𝑡+1 | F𝑡 ] ≤ 𝑋𝑡 − 𝜖 · 1 𝜅 >𝑡 + 𝜖 · E[min{𝑡 + 1, 𝜅} | F𝑡 ]
                                  = 𝑋𝑡 − 0 + 𝜖 · 𝜅
                                  = 𝑌𝑡
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems           33

Hence, {𝑌𝑡 }𝑡 ≥0 is a supermartingale. Moreover, since 𝜅 ≤ 𝑡 implies 𝑋𝑡+1 = 𝑋𝑡 , we have
that 𝑋𝑡+1 − 𝑋𝑡 = 1 𝜅 >𝑡 · (𝑋𝑡+1 − 𝑋𝑡 ). Thus, we can obtain that

                   𝑌𝑡+1 − 𝑌𝑡 = 𝑋𝑡+1 − 𝑋𝑡 + 𝜖 · (min{𝑡 + 1, 𝜅} − min{𝑡, 𝜅})
                              = 𝑋𝑡+1 − 𝑋𝑡 + 𝜖 · 1 𝜅 >𝑡
                              = 1 𝜅 >𝑡 · (𝑋𝑡+1 − 𝑋𝑡 + 𝜖)
where the second equality is derived by the fact that min{𝑡 + 1, 𝜅} − min{𝑡, 𝜅} = 1 𝜅 >𝑡 .
It follows that 𝑌𝑡+1 − 𝑌𝑡 ∈ [𝑎 + 𝜖, 𝑏 + 𝜖].
     We use Hoeffding’s Inequality on Supermartingales (see Theorem 13) to prove our
result. Pick a time step 𝑇 > 0. Let 𝜈 = 𝜖 · 𝑇 − 𝑋0 and 𝜈ˆ = 𝜖 · min{𝑇, 𝜅} − 𝑋0 . Note that
𝜈 = 𝜈ˆ whenever 𝜅 > 𝑇. By Conditions (29) and (30), we have that 𝜅 > 𝑇 iff 𝑋𝑇 ≥ 0.
For any 𝑠0 ∈ 𝑆0 , we can derive that
                          P𝑠0 (𝜅 > 𝑇) = P𝑠0 (𝑋𝑇 ≥ 0 ∧ 𝜅 > 𝑇)
                                        = P𝑠0 ((𝑋𝑇 + 𝜈ˆ ≥ 𝜈) ∧ 𝜅 > 𝑇)
                                        ≤ P𝑠0 (𝑋𝑇 + 𝜈ˆ ≥ 𝜈)
                                        = P𝑠0 (𝑌𝑇 − 𝑌0 ≥ 𝜖 · 𝑇 − 𝑋0 )
                                                 −2 · (𝜖 · 𝑇 − 𝐵(𝑠0 )) 2
                                                                        
                                        ≤ exp
                                                     𝑇 · (𝑏 − 𝑎) 2

for all 𝑇 > 𝐵(𝑠𝜖 0 ) . Finally, as {𝜔 | 𝜅(𝜔) > 𝑇 } = {𝜔 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 }, we have
that
                                                                     
                  P𝑠0 (𝜅 > 𝑇) = P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ≤ 𝑇 } ,
which implies the upper bound.                                                                 ⊔
                                                                                               ⊓

3     Supplementary Materials for Section 5
Fix a DNN-controlled system 𝑀 𝜇 = (𝑆, 𝑆0 , 𝐴, 𝜋, 𝑓 , 𝑅, 𝜇) with an unsafe set 𝑆𝑢 ∈ 𝑆
such that 𝑆0 ∩ 𝑆𝑢 = ∅.
3.1    Proof for Section 5.1
Theorem 8 (𝑘-inductive Variant of Almost-Sure Safety). Given an 𝑀 𝜇 with an initial
set 𝑆0 and an unsafe set 𝑆𝑢 . If there exists a 𝑘-inductive barrier certificate 𝐵 : 𝑆 → R
such that the following conditions hold:
     Û
           𝐵(𝑔 𝑖𝜋, 𝑓 (𝑠, Δ𝑖 )) ≤ 0                            ∀(𝑠, Δ𝑖 ) ∈ 𝑆0 × 𝑊 𝑖 ,  (33)
      0≤𝑖<𝑘
      𝐵(𝑠) > 0                                                                  ∀𝑠 ∈ 𝑆𝑢 ,    (34)
       Û
           (𝐵(𝑔 𝑖𝜋, 𝑓 (𝑠, Δ𝑖 )) ≤ 0) =⇒ 𝐵(𝑔 𝑘𝜋, 𝑓 (𝑠, Δ 𝑘 )) ≤ 0     ∀(𝑠, Δ𝑖 ) ∈ 𝑆 × 𝑊 𝑖 ,   (35)
      0≤𝑖<𝑘

then the system 𝑀 𝜇 is almost-surely safe, i.e., ∀𝑠0 ∈ 𝑆0 .𝜔 ∈ Ω𝑠0 =⇒ 𝜔𝑡 ∉ 𝑆𝑢 ∀𝑡 ∈ N.
Proof. We prove it by contradiction. Assume that there exists a 𝑘-inductive barrier cer-
tificate 𝐵 satisfying Conditions (33) to (35), but the system is unsafe, i.e., there exist
34        Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

a time step 𝑇 > 0 and an initial state 𝑠0 ∈ 𝑆0 such that a trajectory starting from 𝑠0
enters the unsafe set 𝑆𝑢 at 𝑇, which means 𝑠𝑇 ∈ 𝑆𝑢 . By Condition (34), we have that
𝐵(𝑠𝑇 ) > 0. Condition (33) implies that 𝐵(𝑠0 ) ≤ 0, 𝐵(𝑠1 ) ≤ 0, . . . , 𝐵(𝑠 𝑘−1 ) ≤ 0, which
means the state sequences starting from the safe set will remain in the safe set for the
next 𝑘 −1 consecutive time steps. By Condition (35), we have that for any 𝑘 consecutive
time steps, if the system is safe, then the system will still be safe in the (𝑘 + 1)-th time
step. Then by applying the 𝑘 induction principle with Condition (33) as the base case
and Condition (35) as the inductive hypothesis, we can derive that 𝐵(𝑠𝑡 ) ≤ 0 for all
𝑡 ∈ N. This is contradictory to Condition (34). Therefore, the system with a 𝑘-inductive
BC is almost-surely safe.                                                                  ⊔
                                                                                           ⊓

3.2    Proofs for Section 5.2
Theorem 9 (𝑘-inductive Lower Bounds on Unbounded-time Safety). Given an 𝑀 𝜇
with an initial set 𝑆0 and an unsafe set 𝑆𝑢 . If there exists a k-inductive barrier certificate
𝐵 : 𝑆 → R such that for some constants 𝑘 ∈ N ≥1 , 𝜖 ∈ [0, 1] and 𝑐 ≥ 0, the following
conditions hold:
             𝐵(𝑠) ≥ 0                                                  for all 𝑠 ∈ 𝑆       (37)
             𝐵(𝑠) ≤ 𝜖                                                 for all 𝑠 ∈ 𝑆0 ,     (38)
             𝐵(𝑠) ≥ 1                                                for all 𝑠 ∈ 𝑆𝑢 ,      (39)
             E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝑐                for all 𝑠 ∈ 𝑆,      (40)
             EΔ𝑘 ∼𝜇 𝑘 [𝐵(𝑔 𝑘𝜋, 𝑓 (𝑠, Δ 𝑘 )) | 𝑠] − 𝐵(𝑠) ≤ 0            for all 𝑠 ∈ 𝑆,      (41)

then the safety probability over infinite time horizons is bounded from below by
                                                                         𝑘 (𝑘 − 1)𝑐
     ∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 | 𝜔0 ∈ Ω𝑠0 , 𝜔𝑡 ∉ 𝑆𝑢 for all 𝑡 ∈ N} ≥ 1 − 𝑘 𝐵(𝑠0 ) −            .
                                                                                2
Proof. Let 𝜅 be the first time that a trajectory enters the unsafe set 𝑆𝑢 , i.e., 𝜅(𝜔) :=
inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Construct a stochastic process {𝑋𝑡 }𝑡 ≥0 over the set Ω of all
trajectories such that for any 𝜔 ∈ Ω.
                                       (
                                         𝐵(𝑠𝑡 ), for 𝑡 < 𝜅,
                              𝑋𝑡 (𝜔) =
                                         𝐵(𝑠 𝜅 ), for 𝑡 ≥ 𝜅.

According to Condition (39), we have that 𝑆𝑢 ⊆ {𝑠 ∈ 𝑆 | 𝐵(𝑠) ≥ 1}. Therefore, for any
initial state 𝑠0 ∈ 𝑆0 , it follows that

                          P𝑠0 [{𝜔 | 𝜔 ∈ Ω𝑠0 , 𝜔𝑡 ∈ 𝑆𝑢 for some 𝑡 ∈ N}]
                        ≤ P𝑠0 [{𝜔 | 𝜔 ∈ Ω𝑠0 , sup𝑡 ∈N 𝑋𝑡 (𝜔) ≥ 1}]
Then construct 𝑘 new stochastic processes {𝑌𝑡𝑖 }𝑡 ≥0 ’s for all 𝑖 ∈ [0, 𝑘 − 1] such that
𝑌𝑡𝑖 := 𝑋𝑖+𝑡 𝑘 . Intuitively, given a process {𝑋𝑡 }𝑡 ≥0 , each new process {𝑌𝑡𝑖 }𝑡 ≥0 consists of
the states in {𝑋𝑡 }𝑡 ≥0 after every 𝑘 steps, starting from 𝑋𝑖 . Next, we want to prove that
each {𝑌𝑡𝑖 }𝑡 ≥0 is a non-negative supermartingale. For 𝑖 + 𝑡𝑘 < 𝜅, we have that
                           𝑖
                        E[𝑌𝑡+1 | F𝑡 ] = E[𝑋𝑖+(𝑡+1) 𝑘 | F𝑡 ] ≤ 𝑋𝑖+𝑡 𝑘 = 𝑌𝑡𝑖
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems       35

where the inequality is obtained by Condition (41). For 𝑖 + 𝑡𝑘 ≥ 𝜅, we have that
                                     𝑖
                                  E[𝑌𝑡+1 | F𝑡 ] = 𝑋𝑖+𝑡 𝑘 = 𝑌𝑡𝑖 .
Combined with Condition (37), we can conclude that {𝑌𝑡𝑖 }𝑡 ≥0 is a non-negative super-
martingale for all 𝑖 ∈ [0, 𝑘 − 1]. Then by Boole’s inequality, we have that
                          P𝑠0 [{𝜔 ∈ Ω𝑠0 | sup𝑡 ∈N 𝑋𝑡 (𝜔) ≥ 1}]
                          𝑘−1
                          ∑︁
                      ≤         P𝑠0 [{𝜔 ∈ Ω𝑠0 | sup𝑡 ∈N 𝑋𝑖+𝑡 𝑘 (𝜔) ≥ 1}]
                          𝑖=0
                          𝑘−1
                          ∑︁
                      =         P𝑠0 [{𝜔 ∈ Ω𝑠0 | sup𝑡 ∈N𝑌𝑡𝑖 (𝜔) ≥ 1}]
                          𝑖=0
                          𝑘−1
                          ∑︁
                      ≤         E[𝑋𝑖 ]
                          𝑖=0

where the last inequality is obtained by Doob’s nonnegative supermartingale inequality.
By applying Condition (40) and the law of total expectation recursively, we obtain that
                                    E[𝑋𝑡+1 | F𝑡 ] ≤ 𝑋𝑡 + 𝑐
                                 ⇒ E[𝑋𝑡+1 ] ≤ E[𝑋𝑡 ] + 𝑐
                                 ⇒ E[𝑋𝑡+1 ] ≤ 𝑋0 + 𝑐 · (𝑡 + 1)
Therefore, we can derive that
                          P𝑠0 [{𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∈ 𝑆𝑢 for some 𝑡 ∈ N}]
                                 𝑘−1
                                 ∑︁                         𝑘 (𝑘 − 1)𝑐
                       ≤ 𝑋0 +          (𝑋0 + 𝑖𝑐) = 𝑘 𝑋0 +
                                 𝑖=1
                                                                 2

Finally, by means of complementation, we obtain the upper bound.                           ⊔
                                                                                           ⊓




Remark 2. To make the probabilistic bound above non-trivial, the value of 𝑘 should be
bounded by
                                      √︁
                     (𝑐 − 2𝐵(𝑠0 )) + 4𝐵(𝑠0 ) 2 + 𝑐2 − 4𝑐(2 + 𝐵(𝑠0 )) 2
            1≤𝑘≤
                                            2𝑐




Theorem 10 (𝑘-inductive Upper Bounds on Unbounded-time Safety). Given an 𝑀 𝜇
with an initial set 𝑆0 and an unsafe set 𝑆𝑢 , if there exists a barrier certificate 𝐵 : 𝑆 → R
such that for some constant 𝛾 ∈ (0, 1), 0 ≤ 𝜖 ′ < 𝜖 ≤ 1, 𝑐 ≤ 0 the following conditions
36       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

hold:

         0 ≤ 𝐵(𝑠) ≤ 1                                                            for all 𝑠 ∈ 𝑆    (42)
         𝐵(𝑠) ≥ 𝜖                                                              for all 𝑠 ∈ 𝑆0 ,   (43)
         𝐵(𝑠) ≤ 𝜖 ′                                                            for all 𝑠 ∈ 𝑆𝑢 ,   (44)
         E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) | 𝑠] − 𝐵(𝑠) ≥ 𝑐                              for all 𝑠 ∈ 𝑆    (45)
                    𝑘
         𝐵(𝑠) − 𝛾       · EΔ𝑘 ∼𝜇 𝑘 [𝐵(𝑔 𝑘𝜋, 𝑓 (𝑠, Δ 𝑘 )) | 𝑠] ≤ 0          for all 𝑠 ∈ 𝑆 \ 𝑆𝑢     (46)
then the safety probability over infinite time horizons is bounded from above by
                                                                    𝑘 (𝑘 − 1)𝑐
     ∀𝑠0 ∈ 𝑆0 .P𝑠0 {𝜔 ∈ Ω𝑠0 | 𝜔𝑡 ∉ 𝑋𝑢 for all 𝑡 ∈ N} ≤ 1 − 𝑘 𝐵(𝑠0 ) −            .
                                                                           2

Proof. Construct a stochastic process {𝑋𝑡 }𝑡 ≥0 over the set Ω of all trajectories such that
𝑋𝑡 (𝜔) := 𝐵(𝑠𝑡 ) for any 𝜔 ∈ Ω. Let 𝜅 be a stopping time at which the state first enters
𝑆𝑢 , i.e., 𝜅(𝜔) := inf{𝑡 ∈ N | 𝜔𝑡 ∈ 𝑆𝑢 }. Then construct a new stochastic process {𝑌𝑡 }𝑡 ≥0
stopped at 𝜅 such that
                                      (
                                        𝛾 𝑡 𝑋𝑡 , for 𝑡 < 𝜅,
                                 𝑌𝑡 =
                                        𝛾 𝑋 𝜅 , for 𝑡 ≥ 𝜅.
                                          𝜅


It is observed that {𝜔 ∈ Ω | 𝑋𝑡 (𝜔) ∈ 𝑆𝑢 for some 𝑡 ∈ N} = {𝜔 ∈ Ω | 𝜅(𝜔) < ∞}.
Thus, we have that
                             P[𝑋𝑡 ∈ 𝑆𝑢 for some 𝑡 ∈ N] = P[𝜅 < ∞]                                 (54)
Moreover, we can derive that

         P[𝜅 < ∞] ≥ E[𝛾 𝜅 𝑋 𝜅 | 𝜅 < ∞]P[𝜅 < ∞] + 0
                        = E[𝛾 𝜅 𝑋 𝜅 | 𝜅 < ∞]P[𝜅 < ∞] + E[𝛾 𝜅 𝑋 𝜅 | 𝜅 = ∞]P[𝜅 = ∞]
                        = E[𝛾 𝜅 𝑋 𝜅 ] = E[𝑌𝜅 ]
where the first inequality is obtained by the fact 𝛾 ∈ (0, 1) and Condition (42), and the
second equality holds as 𝛾 𝜅 = 0 when 𝜅 = ∞.
    Next, we construct 𝑘 new stochastic processes {𝑍𝑡𝑖 }𝑡 ≥0 ’s for 𝑖 ∈ [0, 1] such that
𝑍𝑡 := 𝑌𝑖+𝑡 𝑘 . Intuitively, given a process {𝑌𝑡 }𝑡 ≥0 , each new process {𝑍𝑡𝑖 }𝑡 ≥0 consists of
  𝑖

the states in {𝑌𝑡 }𝑡 ≥0 after every 𝑘 steps, starting from 𝑌𝑖 . We want to prove that each
{𝑍𝑡 }𝑡 ≥0 is a submartingale. For 𝑖 + 𝑡𝑘 < 𝜅, we have that
                 𝑖
              E[𝑍𝑡+1 | F𝑡 ] = E[𝛾 𝑖+(𝑡+1) 𝑘 𝑋𝑖+(𝑡+1) 𝑘 | F𝑡 ]
                                = 𝛾 𝑖+𝑡 𝑘 · 𝛾 𝑘 E[𝑋𝑖+(𝑡+1) 𝑘 | F𝑡 ] ≥ 𝛾 𝑖+𝑡 𝑘 𝑋𝑖+𝑡 𝑘 = 𝑍𝑡𝑖

where the inequality is obtained by Condition (46). For 𝑖 + 𝑡𝑘 ≥ 𝜅, we have that
                                         𝑖
                                      E[𝑍𝑡+1 | F𝑡 ] = 𝑌𝑖+𝑡 𝑘 = 𝑍𝑡𝑖
Hence, {𝑍𝑡𝑖 }𝑡 ≥0 is a submartingale for all 𝑖 ∈ [0, 𝑘 − 1]. By Condition (42), {𝑍𝑡𝑖 }𝑡 ≥0
satisfies the conditions of the Optional Stopping Theorem (OST). Then by applying
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems        37

OST, we obtain that
                                       𝑘−1
                                       ∑︁                 𝑘−1
                                                          ∑︁                𝑘−1
                                                                            ∑︁
               P[𝜅 < ∞] ≥ E[𝑌𝜅 ] =           E[𝑍 𝜅𝑖 ] ≥         E[𝑍0𝑖 ] =         E[𝑋𝑖 ]
                                       𝑖=0                𝑖=0               𝑖=0

By applying Condition (45) and the law of total expectation recursively, we have that

                                   E[𝑋𝑡+1 | F𝑡 ] ≥ 𝑋𝑡 + 𝑐
                               ⇒ E[𝑋𝑡+1 ] ≥ E[𝑋𝑡 ] + 𝑐
                               ⇒ E[𝑋𝑡+1 ] ≥ 𝑋0 + (𝑡 + 1)𝑐
Therefore, we have that
                                      𝑘−1
                                      ∑︁                             𝑘 (𝑘 − 1)𝑐
                   P[𝜅 < ∞] ≥ 𝑋0 +           (𝑋0 + 𝑖𝑐) = 𝑘 𝑋0 +
                                       𝑖=1
                                                                          2

Finally, by means of complementation, we obtain the upper bound.                           ⊔
                                                                                           ⊓




4     Supplementary Materials for Section 6



Similar to those in Section 6.1, the training phase of the other NBCs also involves
two steps, i.e., training data construction and loss function definition. Training data
construction can be achieved by discretizing the state space 𝑆 and constructing a dis-
cretization 𝑆˜ ⊆ 𝑆 such that for each 𝑠 ∈ 𝑆, there is a 𝑠˜ ∈ 𝑆˜ with ||𝑠 − 𝑠˜ || 1 < 𝜏, where
𝜏 > 0 is called the granularity of 𝑆. ˜ Once the discretization 𝑆˜ is obtained, we construct
two finite sets 𝑆˜0 := 𝑆˜ ∩ 𝑆0 and 𝑆˜𝑢 := 𝑆˜ ∩ 𝑆𝑢 used for the training process.
    We provide the training loss functions and validation theorems for several barrier
certificates, The fundamental idea for the others is consistent. The training loss func-
tions are composed of the conditions of NBCs and the simulation-guided term for tight-
ness. In the validation phase, we utilize Lipschitz continuity to reduce the validation of
the infinite state space to a finite set of states , by applying stricter conditions.




4.1   Loss Functions of NBCs




The loss function of NBCs in Theorem 3. Similarly, we define the loss function of NBCs
in Theorem 3 as:
38       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang



      L (𝜃) := 𝑘 1 · L1 (𝜃) + 𝑘 2 · L2 (𝜃) + 𝑘 3 · L3 (𝜃) + 𝑘 4 · L4 (𝜃) + 𝑘 5 · L5 (𝜃)
                  1 ∑︁
      L1 (𝜃) =               (max{ℎ 𝜃 (𝑠) − 1, 0} + max{0 − ℎ 𝜃 (𝑠), 0})
                   ˜
                | 𝑆|
                       𝑠∈ 𝑆˜
                   1 ∑︁
      L2 (𝜃) =                 (max{𝜖 − ℎ 𝜃 (𝑠), 0})
                | 𝑆˜0 | ˜
                        𝑠∈ 𝑆0
                   1 ∑︁
      L3 (𝜃) =                 (max{ℎ 𝜃 (𝑠) − 𝜖 ′ , 0})                                       (55)
                   ˜
                | 𝑆𝑢 | ˜
                        𝑠∈ 𝑆𝑢
                                                                               !
                      1         ∑︁                        ∑︁ ℎ 𝜃 (𝑠′ )
      L4 (𝜃) =                        max{ℎ 𝜃 (𝑠) − 𝛾 ·                + 𝜁, 0}
                | 𝑆˜ \ 𝑆˜𝑢 | ˜ ˜                        𝑠 ′ ∈ D𝑠
                                                                 𝑁
                              𝑠∈ 𝑆\𝑆𝑢
                   1 ∑︁
      L5 (𝜃) =                 (max{1 − 𝕗𝑠 − ℎ 𝜃 (𝑠), 0})
                | 𝑆˜0 | ˜
                      𝑠∈ 𝑆0

where L1 (𝜃), · · · , L4 (𝜃) are defined via the four conditions of the barrier certificate,
correspondingly. L5 (𝜃) is the regularization term to assure the tightness of upper bounds
via the same simulation-based method and Equation (16).

The loss function of NBCs in Theorem 4. The loss function of NBCs in Theorem 4 is:

      L (𝜃) := 𝑘 1 · L1 (𝜃) + 𝑘 2 · L2 (𝜃) + 𝑘 3 · L3 (𝜃) + 𝑘 4 · L4 (𝜃) + 𝑘 5 · L5 (𝜃)
                  1 ∑︁
      L1 (𝜃) =               (max{0 − ℎ 𝜃 (𝑠), 0})
                   ˜
                | 𝑆|
                       𝑠∈ 𝑆˜
                   1 ∑︁
      L2 (𝜃) =                (max{ℎ 𝜃 (𝑠) − 𝜖, 0})
                | 𝑆˜0 | ˜
                        𝑠∈ 𝑆0
                   1 ∑︁
      L3 (𝜃) =                 (max{𝜆 − ℎ 𝜃 (𝑠), 0})                                          (56)
                | 𝑆˜𝑢 | ˜
                        𝑠∈ 𝑆𝑢
                                                                        !
                  1 ∑︁              ∑︁ ℎ 𝜃 (𝑠′ )
      L4 (𝜃) =                max{                − ℎ 𝜃 (𝑠) − 𝑐 + 𝜁, 0}
                   ˜
                | 𝑆|                        𝑁
                     𝑠∈ 𝑆  ˜       𝑠′ ∈ D
                                      𝑠

                         𝑇
                 1 ∑︁ ∑︁                                          
      L5 (𝜃) =              max{𝕗𝑡𝑠 − 1 + (ℎ 𝜃 (𝑠) + 𝑐 · 𝑡)/𝜆, 0}
                 ˜
               | 𝑆0 | ˜ 𝑡=1
                      𝑠∈ 𝑆0

where the last term L5 (𝜃) is to assure the tightness of bounds using the simulation-
based method. Specifically, we execute the control system from each 𝑠 ∈ 𝑆˜0 , and calcu-
late the safe frequency at each time step 𝕗𝑡𝑠 , 𝑡 = 1, · · · , 𝑇 of all these trajectories starting
from each initial state 𝑠.

The loss function of NBCs in Theorem 5. The loss function of NBCs in Theorem 5 can
be defined as:
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems       39



     L (𝜃) := 𝑘 1 · L1 (𝜃) + 𝑘 2 · L2 (𝜃) + 𝑘 3 · L3 (𝜃) + 𝑘 4 · L4 (𝜃) + 𝑘 5 · L5 (𝜃)
                 1 ∑︁
     L1 (𝜃) =               (max{0 − ℎ 𝜃 (𝑠), 0})
                  ˜
               | 𝑆|
                      𝑠∈ 𝑆˜
                  1 ∑︁
     L2 (𝜃) =                (max{ℎ 𝜃 (𝑠) − 𝛾, 0})
               | 𝑆˜0 | ˜
                       𝑠∈ 𝑆0
                  1 ∑︁
     L3 (𝜃) =                 (max{1 − ℎ 𝜃 (𝑠), 0})                                      (57)
               | 𝑆˜𝑢 | ˜
                       𝑠∈ 𝑆𝑢
                                                                                   !
                     1        ∑︁              ∑︁ ℎ 𝜃 (𝑠′ )
     L4 (𝜃) =                      max{𝛼                   − ℎ 𝜃 (𝑠) − 𝛼𝛽 + 𝜁, 0}
               | 𝑆˜ \ 𝑆˜𝑢 | ˜ ˜             𝑠 ′ ∈ D𝑠
                                                     𝑁
                           𝑠∈ 𝑆\𝑆𝑢
                         𝑇                                              
                 1 ∑︁ ∑︁          𝑠        𝛼𝛽     𝛼𝛽               −𝑡
     L5 (𝜃) =                max{𝕗𝑡 − 1 +     −(     − ℎ 𝜃 (𝑠)) · 𝛼 , 0}
              | 𝑆˜0 | ˜ 𝑡=1               𝛼−1    𝛼−1
                    𝑠∈ 𝑆0

where the last term L5 (𝜃) is to assure the tightness of bounds using the simulation-
based method. Specifically, we execute the control system from each 𝑠 ∈ 𝑆˜0 , and calcu-
late the safe frequency at each time step 𝕗𝑡𝑠 , 𝑡 = 1, · · · , 𝑇 of all these trajectories.




The loss function of NBCs in Theorem 6. We define the loss function as:
     L (𝜃) := 𝑘 1 · L1 (𝜃) + 𝑘 2 · L2 (𝜃) + 𝑘 3 · L3 (𝜃) + 𝑘 4 · L4 (𝜃) + 𝑘 5 · L5 (𝜃)
                 1 ∑︁
     L1 (𝜃) =              (max{0 − ℎ 𝜃 (𝑠), 0})
                  ˜
               | 𝑆|
                     𝑠∈ 𝑆˜
                    1        ∑︁
     L2 (𝜃) =                       (max{ℎ 𝜃 (𝑠) − 𝛽, 0})
               | 𝑆˜ \ 𝑆˜𝑢 | ˜ ˜
                            𝑠∈ 𝑆\𝑆𝑢
                  1 ∑︁
     L3 (𝜃) =                (max{𝛼 − ℎ 𝜃 (𝑠), 0} + max{ℎ 𝜃 (𝑠) − 1 − 𝛽, 0})             (58)
               | 𝑆˜𝑢 | ˜
                       𝑠∈ 𝑆𝑢
                                                                              !
                    1        ∑︁                ∑︁ ℎ 𝜃 (𝑠′ )
     L4 (𝜃) =                        max{𝑐 −                + ℎ 𝜃 (𝑠) + 𝜁, 0}
               | 𝑆˜ \ 𝑆˜𝑢 | ˜ ˜               𝑠′ ∈ D
                                                       𝑁
                             𝑠∈ 𝑆\𝑆𝑢                  𝑠

                            𝑇                                            
                 1      ∑︁ ∑︁                     1
      L5 (𝜃) =                       1 − ℎ 𝜃 (𝑠) − 𝑐 · 𝑡 + 𝛽 − 𝕗𝑡𝑠 , 0}
                 ˜
               | 𝑆0 |                             2
                        𝑠∈ 𝑆˜0 𝑡=1




The loss function of NBCs in Theorem 7. We define the loss function as:
40       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

L (𝜃) := 𝑘 1 · L1 (𝜃) + 𝑘 2 · L2 (𝜃) + 𝑘 3 · L3 (𝜃) + 𝑘 4 · L4 (𝜃) + 𝑘 5 · L5 (𝜃)
               1        ∑︁
L1 (𝜃) =                       (max{0 − ℎ 𝜃 (𝑠), 0})
             ˜    ˜
          | 𝑆 \ 𝑆𝑢 | ˜ ˜
                       𝑠∈ 𝑆\𝑆𝑢
             1 ∑︁
L2 (𝜃) =                (max{𝐾 ′ − ℎ 𝜃 (𝑠), 0} + max{ℎ 𝜃 (𝑠) − 𝐾, 0})
          | 𝑆˜𝑢 | ˜
                  𝑠∈ 𝑆𝑢
                                                                          !
               1        ∑︁            ∑︁ ℎ 𝜃 (𝑠′ )
L3 (𝜃) =                        max{                − ℎ 𝜃 (𝑠) + 𝜖 + 𝜁, 0}
          | 𝑆˜ \ 𝑆˜𝑢 | ˜ ˜           𝑠′ ∈ D
                                              𝑁
                     𝑠∈ 𝑆\𝑆𝑢                 𝑠

              1       ∑︁
L4 (𝜃) =                  (max{ℎ 𝜃 (𝑠′ ) − ℎ 𝜃 (𝑠) − 𝑏 + 𝜁, 0} + max{𝑎 − ℎ 𝜃 (𝑠′ ) + ℎ 𝜃 (𝑠) + 𝜁, 0})
         | 𝑆˜ \ 𝑆˜𝑢 | ˜ ˜
                     𝑠∈ 𝑆\𝑆𝑢
                    𝑇 
                                   2(𝜖𝑡 − ℎ 𝜃 (𝑠)) 2
                                                                 
            1 ∑︁ ∑︁                                       𝑠
L5 (𝜃) =                max{𝑒𝑥 𝑝(−                   ) − 𝕗𝑡 , 0}
         | 𝑆˜0 | ˜ 𝑡=1               𝑡 · (𝑏 − 𝑎) 2
                𝑠∈ 𝑆0
                                                                                                  (59)

4.2   NBCs Validation




Theorem 11 Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 +𝛿))) |
𝑠] − 𝐵(𝑠) ≤ 0 for any state 𝑠 ∈ 𝑆 \ 𝑆𝑢 if the formula below
                              E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] ≤ 𝐵( 𝑠˜) − 𝜁

holds for any state 𝑠˜ ∈ 𝑆˜ \ 𝑆˜𝑢 , where 𝜁 = 𝜏 · 𝐿 𝐵 · (1 + 𝐿 𝑓 · (1 + 𝐿 𝜋 )) with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵
being the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.




Proof. Let 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵 be the Lipschitz constants for the system dynamics 𝑓 , the trained
policy 𝜋 and the neural network function 𝐵, respectively. Given a state 𝑠 ∈ 𝑆 \ 𝑆𝑢 , let 𝑠˜
be such that || 𝑠˜ − 𝑠|| 1 ≤ 𝜏. By the Lipschitz continuities, we have that
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))]
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + ||( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 · 𝐿 𝑓
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
and

                        −𝐵(𝑠) ≤ −𝐵( 𝑠˜) + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 ≤ −𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 ,
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems                    41

Thus, we can derive that

             E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] − 𝐵(𝑠)
           ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) − 𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵
           ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) − 𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵
           ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) + 𝜁
           ≤0


Validating NBCs in Theorem 3. A candidate NBC in Theorem 3 can be validated if it
meets the conditions in Conditions (12) to (15). For the first three conditions, we can
check


            inf 𝐵(𝑠) ≥ 0 ∧ sup 𝐵(𝑠) ≤ 1 ∧ inf 𝐵(𝑠) ≥ 𝜖 ∧ sup 𝐵(𝑠) ≤ 𝜖 ′                               (60)
            𝑠∈𝑆                  𝑠∈𝑆                  𝑠∈𝑆0                 𝑠∈𝑆𝑢

using the interval bound propagation approach [21,58]. Similarly, for the condition in
Condition (15), Theorem 17 reduces validation from infinite states to finite ones, which
is easier to check.

Theorem 17. Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have B(s)-𝛾·E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠+
𝛿))) | 𝑠] ≤ 0 for all 𝑠 ∈ 𝑆 \ 𝑆𝑢 if the formula below
                         𝐵( 𝑠˜) − 𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜁 ≤ 0                         (61)

holds for any state 𝑠˜ ∈ 𝑆˜ \ 𝑆˜𝑢 , where 𝜁 = 𝜏 · 𝐿 𝐵 · (𝛾 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 1) with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵
being the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.

Proof. By the Lipschitz continuities and 𝛾 ∈ (0, 1), we have that
        𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))]
      ≥𝛾 · {E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − || 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 }
      ≥𝛾 · {E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − ||( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 · 𝐿 𝑓 }
      ≥𝛾 · {E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )}
      ≥𝛾 · {E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )}
and
                     −𝐵(𝑠) ≥ −𝐵( 𝑠˜) − ||𝑠 − 𝑠˜ || 1 · 𝐿 𝐵 ≥ −𝐵( 𝑠˜) − 𝜏 · 𝐿 𝐵

Thus, we can derive that
         𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] − 𝐵(𝑠)
       ≥ 𝛾 · {E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )} − 𝐵( 𝑠˜) − 𝜏 · 𝐿 𝐵
       = 𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) − 𝛾 · 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) − 𝜏 · 𝐿 𝐵
42       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

Finally, we have:

         𝐵(𝑠) − 𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))]
      ≤ 𝐵( 𝑠˜) − 𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝛾 · 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵
       = 𝐵( 𝑠˜) − 𝛾 · E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜁
      ≤0

Validating NBCs in Theorem 4. A candidate NBC can be validated if it meets the
conditions in Conditions (17) to (20). For the first three conditions, we can check

                      inf 𝐵(𝑠) ≥ 0 ∧ sup 𝐵(𝑠) ≤ 𝜖 ∧ inf 𝐵(𝑠) ≥ 𝜆                                  (62)
                      𝑠∈𝑆                  𝑠∈𝑆0                  𝑠∈𝑆𝑢

using the interval bound propagation approach [21,58]. For the condition in Condi-
tion (20), Theorem 18 reduces validation from infinite states to finite ones, which is
easier to check.

Theorem 18. Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 +
𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝑐 for all 𝑠 ∈ 𝑆 if the formula below
                        E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] − 𝐵( 𝑠˜) + 𝜁 ≤ 𝑐                     (63)
                         ˜ where 𝜁 = 𝜏 · 𝐿 𝐵 · (1 + 𝐿 𝑓 · (1 + 𝐿 𝜋 )) with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵 being
holds for any state 𝑠˜ ∈ 𝑆,
the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.

Proof. Given a state 𝑠 ∈ 𝑆, let 𝑠˜ be such that || 𝑠˜ −𝑠|| 1 ≤ 𝜏. By the Lipschitz continuities,
we have that
          E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))]
        ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵
        ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + ||( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 · 𝐿 𝑓
        ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
        ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
and

                    −𝐵(𝑠) ≤ −𝐵( 𝑠˜) + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 ≤ −𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 ,
Thus, we can derive that
          E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] − 𝐵(𝑠) − 𝑐
        ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵 − 𝑐
        ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) + 𝜁 − 𝑐
        ≤0

Validating NBCs in Theorem 5. A candidate NBC can be validated if it meets the
conditions in Conditions (21) to (24). For the first three conditions, we can check
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems                     43



                       inf 𝐵(𝑠) ≥ 0 ∧ sup 𝐵(𝑠) ≤ 𝛾 ∧ inf 𝐵(𝑠) ≥ 1                                     (64)
                       𝑠∈𝑆                  𝑠∈𝑆0                  𝑠∈𝑆𝑢

using the interval bound propagation approach [21,58]. For the condition in Condi-
tion (24), Theorem 19 reduces validation from infinite states to finite ones, which is
easier to check.

Theorem 19. Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have 𝛼 · E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 +
𝛿))) | 𝑠] − 𝐵(𝑠) ≤ 𝛼𝛽 if the formula below
                         𝛼 · E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] − 𝐵( 𝑠˜) ≤ 𝛼𝛽                       (65)

holds for any state 𝑠˜ ∈ 𝑆˜ \ 𝑆˜𝑢 , where 𝜁 = 𝛼 · 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵 with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵
being the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.

Proof. Given a state 𝑠 ∈ 𝑆, let 𝑠˜ be such that || 𝑠˜ −𝑠|| 1 ≤ 𝜏. By the Lipschitz continuities,
we have that
            E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))]
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + ||( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 · 𝐿 𝑓
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
and

                      −𝐵(𝑠) ≤ −𝐵( 𝑠˜) + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 ≤ −𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 ,
Thus, we can derive that
      𝛼 · E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] − 𝐵(𝑠) − 𝛼𝛽
    ≤𝛼 · E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) − 𝛼𝛽 + 𝛼 · 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵
    ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) − 𝛼𝛽 + 𝜁
    ≤0

Validating NBCs in Theorem 6. A candidate NBC can be validated if it meets the
conditions in Conditions (25) to (28). For the first two conditions, we can check

                                 inf 𝐵(𝑠) ≥ 0 ∧        sup 𝐵(𝑠) ≤ 𝛽                                   (66)
                                 𝑠∈𝑆                  𝑠∈𝑆\𝑆𝑢

using the interval bound propagation approach [21,58]. The condition in Condition (27)
is satisfied straightforwardly, Because candidate NBCs are neural networks that are
Lipschitz continuous [43]. For the condition in Condition (28), Theorem 20 reduces
validation from infinite states to finite ones, which is easier to check.
44       Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

Theorem 20. Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 +
𝛿))) | 𝑠] − 𝐵(𝑠) ≥ 𝑐 if the formula below

                         E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] − 𝐵( 𝑠˜) ≥ 𝑐 + 𝜁                    (67)

holds for any state 𝑠˜ ∈ 𝑆˜ \ 𝑆˜𝑢 , where 𝜁 = 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵 with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵
being the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.

Proof. By the Lipschitz continuities and 𝛾 ∈ (0, 1), we have that
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))]
         ≥E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − || 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵
         ≥E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − ||( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 · 𝐿 𝑓
         ≥E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
         ≥E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )

and
                     −𝐵(𝑠) ≥ −𝐵( 𝑠˜) − ||𝑠 − 𝑠˜ || 1 · 𝐿 𝐵 ≥ −𝐵( 𝑠˜) − 𝜏 · 𝐿 𝐵
Thus, we can derive that
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] − 𝐵(𝑠) − 𝑐
        ≥ E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) − 𝐵( 𝑠˜) − 𝜏 · 𝐿 𝐵 − 𝑐
        = E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) − 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) − 𝜏 · 𝐿 𝐵 − 𝑐

Finally, we have:
           𝐵(𝑠) − E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] + 𝑐
         ≤ 𝐵( 𝑠˜) − E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵 + 𝑐
         = 𝐵( 𝑠˜) − E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝑐 + 𝜁
         ≤0

Validating NBCs in Theorem 7. A candidate NBC can be validated if it meets the
conditions in Conditions (29) to (32). For the first two conditions, we can check

                     inf 𝐵(𝑠) ≥ 0 ∧ inf 𝐵(𝑠) ≥ 𝐾 ′ ∧ sup 𝐵(𝑠) ≤ 𝐾                                 (68)
                   𝑠∈𝑆\𝑆𝑢                   𝑠∈𝑆𝑢                    𝑠∈𝑆𝑢

using the interval bound propagation approach [21,58]. Condition (30) is satisfied
straightforwardly, Because candidate NBCs are neural networks that are Lipschitz con-
tinuous [43]. For the condition in Condition (31), Theorem 21 reduces validation from
infinite states to finite ones, which is easier to check.

Theorem 21. Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 +
𝛿))) | 𝑠] − 𝐵(𝑠) ≤ −𝜖 if the formula below
                           E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) | 𝑠˜] − 𝐵( 𝑠˜) ≤ −𝜖                     (69)
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems                45

holds for any state 𝑠˜ ∈ 𝑆˜ \ 𝑆˜𝑢 , where 𝜁 = 𝜏 · 𝐿 𝐵 · (1 + 𝐿 𝑓 · (1 + 𝐿 𝜋 )) with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵
being the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.


Proof. Given a state 𝑠 ∈ 𝑆, let 𝑠˜ be such that || 𝑠˜ −𝑠|| 1 ≤ 𝜏. By the Lipschitz continuities,
we have that
           E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))]
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + ||( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 · 𝐿 𝑓
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )

and
                     −𝐵(𝑠) ≤ −𝐵( 𝑠˜) + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 ≤ −𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 ,
Thus, we can derive that
          E 𝛿∼𝜇 [𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))] − 𝐵(𝑠) + 𝜖
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵 + 𝜖
         ≤E 𝛿∼𝜇 [𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))] − 𝐵( 𝑠˜) + 𝜁 + 𝜖
         ≤0



Validating NBCs in Theorem 8. A candidate NBC can be validated if it meets the
conditions in Conditions (33) to (35). For the first two conditions, we can check



                                 sup 𝐵(𝑠) ≤ 0 ∧ inf 𝐵(𝑠) > 0                                      (70)
                                 𝑠∈𝑆0                  𝑠∈𝑆𝑢



using the interval bound propagation approach [21,58]. For the condition in Condi-
tion (35), Theorem 22 reduces validation from infinite states to finite ones, which is
easier to check.


                                                                    Ó
Theorem 22. Given an 𝑀 𝜇 and a function 𝐵 : 𝑆 → R, we have 0≤𝑖<𝑘 (𝐵(𝑔 𝑖𝜋, 𝑓 (𝑠, Δ𝑖 )) ≤
0) =⇒ 𝐵(𝑔 𝑘𝜋, 𝑓 (𝑠, Δ 𝑘 )) ≤ 0 ∀(𝑠, Δ𝑖 ) ∈ 𝑆 × 𝑊 𝑖 if the formula below

                               𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)))) − 𝐵( 𝑠˜) + 𝜁 ≤ 0                          (71)
                         ˜ where 𝜁 = 𝜏 · 𝐿 𝐵 · (1 + 𝐿 𝑓 · (1 + 𝐿 𝜋 )) with 𝐿 𝑓 , 𝐿 𝜋 , 𝐿 𝐵 being
holds for any state 𝑠˜ ∈ 𝑆,
the Lipschitz constants of 𝑓 , 𝜋 and 𝐵, respectively.
46           Dapeng Zhi, Peixin Wang† , Si Liu, Luke Ong, and Min Zhang

                                      Table 3. Experimental settings.

      Task         Dim.            Alg.             A.F.              Size           A.T.           S.P.
      CP              4           DQN              ReLU            3 × 200           Dis.         Gym
      PD              3          DDPG            Sigmoid           2 × 200          Cont.          Gym
      Tora            4          DDPG            Sigmoid           2 × 200          Cont.        Verisig
      B1              2          DDPG              ReLU            2 × 100          Cont.        Verisig
      Remarks. Dim.: dimension; Alg.: DRL algorithm; A.F.: activation function; A.T.: action
      type; S.P.: sources of problems; Dis.: discrete; Cont.: continuous.

Proof. Given a state 𝑠 ∈ 𝑆, let 𝑠˜ be such that || 𝑠˜ −𝑠|| 1 ≤ 𝜏. By the Lipschitz continuities,
we have that
                  𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿)))
                ≤𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) + || 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵
                ≤𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) + ||( 𝑠˜, 𝜋( 𝑠˜ + 𝛿)) − (𝑠, 𝜋(𝑠 + 𝛿))|| 1 · 𝐿 𝐵 · 𝐿 𝑓
                ≤𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
                ≤𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 )
and
                       −𝐵(𝑠) ≤ −𝐵( 𝑠˜) + || 𝑠˜ − 𝑠|| 1 · 𝐿 𝐵 ≤ −𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 ,

Thus, we can derive that
                    𝐵( 𝑓 (𝑠, 𝜋(𝑠 + 𝛿))) − 𝐵(𝑠)
                  ≤𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) − 𝐵( 𝑠˜) + 𝜏 · 𝐿 𝐵 · 𝐿 𝑓 · (1 + 𝐿 𝜋 ) + 𝜏 · 𝐿 𝐵
                  ≤𝐵( 𝑓 ( 𝑠˜, 𝜋( 𝑠˜ + 𝛿))) − 𝐵( 𝑠˜) + 𝜁
                  ≤0
5      Implementation Details and Additional Experimental Results
5.1     Benchmarks and Experimental Settings
To demonstrate the generality of our approach, we train systems with different activa-
tion functions and network structures of the planted NNs, using different DRL algo-
rithms such as DQN [38] and DDPG [35]. Table 3 gives the details of training settings.
 1. CartPole (CP). A pole is attached by an un-actuated joint to a cart. The goal of
    training is to learn a controller that prevents the pole from falling over by applying
    a force of +1 or −1 to the cart.
 2. Pendulum (PD). A pendulum that can rotate around an endpoint is delineated.
    Starting from a random position, the pendulum shall swing up and stay upright.
 3. Tora. A cart is attached to a wall with a spring. It is free to move on a frictionless
    surface. Inside the cart, there is an arm free to rotate about an axis. The controller’s
    goal is to stabilize the system at the equilibrium state where all the variables are 0.
 4. B1. A classic nonlinear systems, where agents in both systems aim to avoid dan-
    gerous areas from the preset initial state space.
Unifying Qualitative and Quantitative Safety Verification of DNN-Controlled Systems    47

                  Table 4. Synthesis time of different NBCs (in seconds).

Task L.B.i. 𝑘-L.B.i. U.B.i. 𝑘-U.B.i. 𝑙-L.B.f. 𝑒-L.B.f. 𝑙-U.B.f. 𝑒-U.B.f. Quali. 𝑘-Quali.
CP 2318.5 1876.0 2891.9 2275.3 3127.5 3359.0 3277.8 3509.1 1755.2 1059.3
PD 1941.6 1524.0 2282.7 1491.5 2015.5 2218.3 2076.8 2272.2 1433.7                 811.9
Tora 280.3    218.5 895.1     650.7 396.4 429.6 340.6             501.7 623.0     415.8
B1   587.4    313.6 1127.3    840.1 775.9 824.7 894.2 1184.6 1022.3               566.7



5.2   Efficiency of Training and Validating NBCs.
Table 4 shows synthesis time of different NBCs in seconds, i.e., L.B.i.(NBCs for lower
bounds on infinite-time safety), 𝑘-L.B.i.(𝑘-inductive lower bounds on infinite-time safety),
U.B.i.(NBCs for upper bounds on infinite-time safety), 𝑘-U.B.i.(𝑘-inductive upper bounds
on infinite-time safety), 𝑙-L.B.f.(NBCs for linear lower bounds on finite-time safety), 𝑒-
L.B.f.(NBCs for exponential lower bounds on finite-time safety), 𝑙-U.B.f.(NBCs for lin-
ear upper bounds on finite-time safety), 𝑒-U.B.f.(NBCs for exponential upper bounds
on finite-time safety), Quali.(NBCs for almost-surely safety), and 𝑘-Quali.(NBCs for
𝑘-inductive almost-surely safety).
    In general, high-dimensional systems e.g., CP (4-dimensional state space) cost more
time than low-dimensional ones, e.g, B1 (2-dimensional state space). That is because
the validation step suffers from the curse of high-dimensionality [9].
