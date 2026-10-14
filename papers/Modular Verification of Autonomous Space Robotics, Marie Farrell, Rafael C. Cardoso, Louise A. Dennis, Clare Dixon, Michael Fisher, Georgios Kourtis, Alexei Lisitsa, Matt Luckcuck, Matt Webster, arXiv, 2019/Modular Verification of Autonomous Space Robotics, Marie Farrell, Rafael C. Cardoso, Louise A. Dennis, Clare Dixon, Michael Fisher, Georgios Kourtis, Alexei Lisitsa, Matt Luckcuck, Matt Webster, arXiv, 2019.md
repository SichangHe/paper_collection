                                                                   Modular Verification of Autonomous Space Robotics


                                                               Marie Farrell, Rafael C. Cardoso, Louise A. Dennis, Clare Dixon, Michael Fisher,
                                                                      Georgios Kourtis, Alexei Lisitsa, Matt Luckcuck and Matt Webster

                                                                                           Department of Computer Science
                                                                                               University of Liverpool
                                                                                           marie.farrell@liverpool.ac.uk
arXiv:1908.10738v1 [cs.SE] 28 Aug 2019




                                            Abstract—Ensuring that autonomous space robot control              (e.g. Event-B or Z), or algebraic specifications (e.g. CSP
                                         software behaves as it should is crucial, particularly as software    or CASL) amongst others to specify the nodes in a robotic
                                         failure in space often equates to mission failure and could           system. Each of these formalisms offers its own range of
                                         potentially endanger nearby astronauts and costly equipment.
                                         To minimise mission failure caused by software errors, we             benefits, and each tends to suit the verification of particular
                                         can utilise a variety of tools and techniques to verify that the      types of behaviour. However, in some cases we may only
                                         software behaves as intended. In particular, distinct nodes in        have access to the black-box or white-box implementation
                                         a robotic system often require different verification techniques      of a node and so, we must use (simulation-based) testing
                                         to ensure that they behave as expected. This paper introduces         techniques for verification.
                                         a method for integrating the various verification techniques
                                         that are applied to robotic software, via a First-Order Logic            Our approach facilitates the use of heterogeneous veri-
                                         (FOL) specification that captures each node’s assumptions and         fication techniques for the nodes in a robotic system. We
                                         guarantees. These FOL specifications are then used to guide           achieve this by specifying Assume-Guarantee [3] properties
                                         the verification of the individual nodes, be it by testing or the     in FOL, as high-level node specifications, and we employ
                                         use of a formal method. We also outline a way of measuring            temporal logic for reasoning about the combination of these
                                         our confidence in the verification of the entire system in terms
                                         of the verification techniques used.                                  FOL specifications. Thus, we attach the assumptions (A(i))
                                                                                                               and guarantees (G(o)) to individual nodes (shown in Fig. 1).
                                            Keywords-formal methods; heterogeneous verification; au-           This abstract specification can be seen as a logical prototype
                                         tonomous space robotics
                                                                                                               for individual nodes and thus the entire robotic system.
                                                               I. I NTRODUCTION                                     II. FOL A SSUME -G UARANTEE S PECIFICATIONS
                                            Robotic systems combine many hardware and software                    For each node, N , we specify AN (iN ) and GN (oN ) where
                                         components, usually represented as node-based architec-               iN is a variable representing the input to the node, oN is a
                                         tures. Each node in a robotic system may require different            variable representing the output from the node, and AN (iN )
                                         verification techniques, ranging from software testing to             and GN (oN ) are FOL formulae describing the assumptions
                                         formal methods. In fact, integrating (formal and non-formal)          and guarantees, respectively, of this node.
                                         verification techniques is crucial for the robotics domain [2].       Each individual node, N , obeys the following implication
                                         Verification should be carried out using the most suitable                          ∀iN , oN · AN (iN ) ⇒ ♦GN (oN )
                                         technique or formalism for each node. However, linking                where ‘♦’ is LTL’s [4] “eventually” operator. So, this
                                         heterogeneous verification results of individual nodes is             implication means that if the assumptions, AN (iN ), hold
                                         difficult and the current state-of-the-art for robotic software       then eventually the guarantee, GN (oN ), will hold. Note that
                                         development does not provide an easy way of achieving this.           our use of temporal operators here is motivated by the
                                            In Fig. 1, we consider a simple space robotic system: a            temporal nature of robotic systems and will be of use in
                                         planetary rover undertaking a remote inspection task. Here,           later extensions of this work.
                                         we have nodes representing the Vision system, a Planner                  Consider the autonomous Plan Reasoning Agent in Fig.
                                         that returns a set of potential plans between the current             1, we can specify the following simple assumption, A3 (i3 ):
                                         location and the next point to inspect, an autonomous Plan                       A3 (i3 ) = ∀p · p ∈ P lanSet ⇒ goal ∈ p
                                         Reasoning Agent that selects a plan, and a Hardware
                                                                                                               which ensures that every plan that is returned by the Planner
                                         Interface that sends commands to the rover’s actuators.
                                                                                                               contains the goal location. Then, we might specify the
                                            As illustrated by Fig. 1, we could use logical speci-
                                                                                                               guarantee that the agent chooses the shortest plan as follows:
                                         fications (e.g. temporal logic), model-based specifications
                                                                                                                         G3 (o3 ) = plan ∈ P lanSet
                                            This work is supported by grant EP/R026092 (FAIR-SPACE Hub)                              ∧ ∀p · p ∈ P lanSet ∧ p 6= plan
                                         through UKRI under the Industry Strategic Challenge Fund (ISCF) for
                                         Robotics and AI Hubs in Extreme and Hazardous Environments.                                   ⇒ length(plan) ≤ length(p)
        A1 (i1 )                      G1 (o1 )       A2 (i2 )                     G2 (o2 )    A3 (i3 )                   G3 (o3 )     A4 (i4 )                      G4 (o4 )
                                                                                                     Plan Reasoning                                Hardware
                      Vision:                                     Planner:
                                                                                                          Agent:                                   Interface:
                     Black-Box                                   Model-based
                                                                                                     Logical/Algebraic                             White-Box
                   Implementation                                Specification
                                                                                                       Specification                             Implementation

                                                                                                         Program Model                           Simulation-Based
                   Software Testing                             Theorem Proving
                                                                                                            Checking                                 Testing


Figure 1. We specify the Assume-Guarantee properties for each node (denoted by A(i) and G(o) respectively). These are then used to guide the verification
approach applied to each node, denoted by dashed lines, such as software testing for a black-box implementation of the Vision node. The solid arrows
represent data flow between nodes and that the assumptions of the next node should follow from the guarantee of the previous.

                                                 Simulation-
                            Testing              Based
                                                                      Formal                 level of confidence in the verification of the whole system as
                                                                      Methods                9/12, resulting in a confidence measure of 75%. Examining
                                                 Testing
   Vision                   X                    ✗                    ✗                      how this metric can be calculated for more complex systems
   Planner                  X                    X                    X                      with loops is a future direction for this work.
   Plan Reasoning
                            X                    X                    X
   Agent                                                                                                           IV. C ONCLUSIONS
   Hardware Inter-
                            X                    X                    ✗                         When verifying complex robotic systems, it is clear that
   face
                                                                                             no single verification technique is suitable for every node in
                             Table I
         V ERIFICATION TECHNIQUES APPLIED TO EACH NODE .                                     the system [2] and so a logical framework that allows us to
                                                                                             integrate the results from distinct verification techniques is
  Once the FOL assumption and guarantee are specified,                                       needed. We have outlined an initial approach to specifying
then we use these high-level specifications as properties to                                 assumptions and guarantees using FOL for individual nodes
be verified of the individual nodes. For the autonomous Plan                                 in robotic systems and we have used a simple, illustrative
Reasoning Agent, we can use a number of techniques for                                       example of a planetary rover to convey our approach. Once
verifying that it meets its associated FOL specification. For                                the FOL specifications have been constructed, they are
example, we can specify the node using the G WENDOLEN                                        then used to guide the more detailed verification of each
agent programming language and then use the AJPF model-                                      node. Furthermore, we introduce the notion of confidence in
checker to verify that it behaves as specified [1].                                          verification techniques and provide a broad categorisation.
  Nodes in a modular robotic architecture are linked to-                                        Our current work involves developing a calculus for
gether and transmit data between them so long as their                                       reasoning about and combining the Assume-Guarantee spec-
types/requirements match. Similarly, we can compose the                                      ifications of individual nodes. In the future, we plan to
assume-guarantee specifications of individual nodes in a                                     provide tool support for this and to evaluate it using a set
number of ways and we are working towards a calculus                                         of more complex robotic space missions. We also intend to
of inference rules that capture this behaviour. To this end,                                 further investigate the suitability of the confidence levels that
we are developing rules for sequentially composing, joining,                                 we have proposed in this paper.
branching and looping between nodes.                                                                                            R EFERENCES
     III. M EASURING C ONFIDENCE IN V ERIFICATION                                            [1] L. A. Dennis, M. Fisher, M. P. Webster, and R. H. Bordini.
                                                                                                 Model checking agent programming languages. Automated
   A key question is how using these different verification                                      Software Engineering, 19(1):5–63, 2012.
techniques affects our confidence in the verification of the
whole system. One might think that a formal proof of                                         [2] M. Farrell, M. Luckcuck, and M. Fisher. Robotics and
correctness corresponds to a higher level of confidence                                          Integrated Formal Methods: Necessity meets Opportunity. In
                                                                                                 Integrated Formal Methods, volume 11023 of LNCS, pages
than simple testing methods (especially over unbounded                                           161–171. Springer, 2018.
environments). However, formal verification is usually only
feasible on an abstraction of the system whereas testing can                                 [3] C. B. Jones. Tentative Steps Toward a Development Method
be carried out on the implemented code. Therefore, it is                                         for Interfering Programs. ACM Transactions on Programming
                                                                                                 Languages and Systems, 5(4):596–619, 1983.
our view that we achieve higher levels of confidence in
verification when multiple verification methods have been                                    [4] A. Pnueli. The Temporal Logic of Programs. In 18th
employed for each node in the system [5].                                                        Symposium on the Foundations of Computer Science, pages
   We have broadly partitioned current verification tech-                                        46–57. IEEE, 1977.
niques into three categories: testing, simulation-based testing                              [5] M. Webster, D. Western, D. Araiza-Illan, C. Dixon, K. Eder,
and formal methods. We have determined which of these                                            M. Fisher, and A. G. Pipe. A corroborative approach to
techniques might be employed for each node in our simple                                         verification and validation of human–robot teams. arXiv
example as shown in Table I. We then provide a score for our                                     preprint arXiv:1608.07403, 2016.
