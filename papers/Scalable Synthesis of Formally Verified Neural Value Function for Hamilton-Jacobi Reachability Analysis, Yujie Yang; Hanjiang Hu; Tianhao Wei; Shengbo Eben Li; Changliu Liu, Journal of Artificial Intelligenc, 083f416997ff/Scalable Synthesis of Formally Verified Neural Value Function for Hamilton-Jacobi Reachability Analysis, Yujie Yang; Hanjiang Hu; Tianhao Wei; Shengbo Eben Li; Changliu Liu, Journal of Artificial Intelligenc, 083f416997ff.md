                                                 Scalable Synthesis of Formally Verified Neural Value
                                                 Function for Hamilton-Jacobi Reachability Analysis

                                           Yujie Yang                                                     yangyj21@mails.tsinghua.edu.cn
                                           School of Vehicle and Mobility, Tsinghua University,
                                           Beijing, 100084, China
                                           Robotics Institute, Carnegie Mellon University,
                                           Pittsburgh, PA, 15289, USA
arXiv:2407.20532v2 [eess.SY] 31 Jul 2024




                                           Hanjiang Hu                                                           hanjianh@andrew.cmu.edu
                                           Tianhao Wei                                                              twei2@andrew.cmu.edu
                                           Robotics Institute, Carnegie Mellon University,
                                           Pittsburgh, PA, 15289, USA

                                           Shengbo Eben Li                                                           lishbo@tsinghua.edu.cn
                                           School of Vehicle and Mobility & College of AI, Tsinghua University,
                                           Beijing, 100084, China


                                           Changliu Liu                                                              cliu6@andrew.cmu.edu
                                           Robotics Institute, Carnegie Mellon University,
                                           Pittsburgh, PA, 15289, USA


                                                                                       Abstract
                                                   Hamilton-Jacobi (HJ) reachability analysis provides a formal method for guarantee-
                                               ing safety in constrained control problems. It synthesizes a value function to represent
                                               a long-term safe set called feasible region. Early synthesis methods based on state space
                                               discretization cannot scale to high-dimensional problems, while recent methods that use
                                               neural networks to approximate value functions result in unverifiable feasible regions. To
                                               achieve both scalability and verifiability, we propose a framework for synthesizing veri-
                                               fied neural value functions for HJ reachability analysis. Our framework consists of three
                                               stages: pre-training, adversarial training, and verification-guided training. We design three
                                               techniques to address three challenges to improve scalability respectively: boundary-guided
                                               backtracking (BGB) to improve counterexample search efficiency, entering state regulariza-
                                               tion (ESR) to enlarge feasible region, and activation pattern alignment (APA) to accelerate
                                               neural network verification. We also provide a neural safety certificate synthesis and verifi-
                                               cation benchmark called Cersyve-9, which includes nine commonly used safe control tasks
                                               and supplements existing neural network verification benchmarks. Our framework suc-
                                               cessfully synthesizes verified neural value functions on all tasks, and our proposed three
                                               techniques exhibit superior scalability and efficiency compared with existing methods.


                                           1. Introduction
                                           Safety is a primary concern in controller design, especially for control systems interacting
                                           with the physical world, such as autonomous driving and robot locomotion. In these sys-
                                           tems, safety is usually specified by inequality constraints on system states. For example,

                                                                                             1
safety constraints in a robot locomotion task require the distance between the robot and
surrounding obstacles to be always positive. Such safety constraints must be satisfied not
only in a single time step but also in all time steps over an infinite horizon. When designing
a controller, it is important to know from which states it can satisfy the infinite-horizon
safety constraints and from which states it cannot. The deployment of any controller should
be restricted to a set of states where long-term constraint satisfaction is ensured, which is
called a feasible region.
    Hamilton-Jacobi (HJ) reachability analysis provides a formal method for computing fea-
sible regions of control systems with safety constraints (Bansal et al., 2017). In HJ reacha-
bility analysis, a feasible region is represented by the zero-sublevel set of a value function,
which is defined as the maximum value of the constraint function over a trajectory. In gen-
eral nonlinear systems, exactly computing the value function is difficult because it involves
solving the HJ partial differential equation, which does not have a closed-form solution in
most cases (Bansal et al., 2017). Traditional methods numerically solve the HJ equation on
a grid representing a discretization of the state space (Mitchell, 2007, 2008). These meth-
ods’ computational complexity grows exponentially with state dimension, making them
intractable in high-dimensional systems. Although some techniques, such as system de-
composition (Chen et al., 2016), are proposed for accelerating value function computation,
they only apply to some special scenarios. Recent methods use neural networks to approx-
imate the solution of the HJ equation by minimizing the error between the two sides of the
equation (Fisac et al., 2019; Bansal & Tomlin, 2021). The error is computed on states ran-
domly sampled in the state space and minimized by gradient-based optimization algorithms.
Although these methods scale well to high-dimensional systems, the zero-sublevel sets of
their value functions are no longer guaranteed to be valid feasible regions due to neural
network approximation errors. Specifically, their zero-sublevel sets may violate two basic
properties of a feasible region: constraint satisfaction and forward invariance. Constraint
satisfaction means all states in a feasible region satisfy the safety constraint themselves.
Forward invariance means starting from any state in a feasible region, its subsequent states
can always be kept in this region by some control policy. Violating these two properties
may cause possible constraint violations, even starting from a state inside the zero-sublevel
set, making the value function unreliable for safe control.
    The problem of invalid feasible regions necessitates verification of neural HJ reachability
value functions. Recently, some researchers have begun to use neural network verification
tools to formally verify and synthesize neural safety certificates, such as neural control bar-
rier functions (CBFs) (Wang et al., 2023; Zhang et al., 2024) and neural control Lyapunov
functions (CLFs) (Chang et al., 2019; Abate et al., 2020). Similar to HJ reachability value
function, these safety certificates also represent feasible regions by their zero-sublevel sets.
The difference is that these functions are not defined through equations but through certain
inequality conditions. For example, the time derivative of a CBF must be upper bounded by
an extended class K function, and a CLF must be a positive definite function with negative
time derivatives. Existing works try to verify whether these conditions are strictly satisfied
by the neural safety certificates in the entire state space. Such problems can be transformed
into standard neural network verification problems, which can be solved by existing verifi-
cation tools (Liu et al., 2021). This verification procedure can also be embedded into neural
safety certificate synthesis, resulting in verification-guided training methods (Wang et al.,

                                               2
2023; Zhang et al., 2024). If verification fails on a synthesized safety certificate, the found
counterexamples are added to the dataset, and the safety certificate is further trained on
these counterexamples. This process is repeated until the neural safety certificate is suc-
cessfully verified. However, these methods currently only work on low-dimensional or linear
systems and are difficult to scale to high-dimensional nonlinear systems and real-world con-
trol tasks. Through our study, we discover three main challenges that restrict the scalability
of these methods:

   • Difficulty of searching and eliminating counterexamples. Successful verifica-
     tion requires strict satisfaction of inequality conditions in all states, and not a single
     counterexample is allowed. However, counterexamples become extremely sparse in
     high-dimensional spaces, making it difficult to find and eliminate all of them.

   • Severe shrinkage of feasible region. When training neural safety certificates on
     counterexamples, their zero-sublevel sets tend to shrink so that the inequality condi-
     tions can be more easily satisfied. Although slight shrinkage is sometimes acceptable,
     severe shrinkage can be a serious problem because it results in overly conservative
     control policies and poor control performance. We find in our experiments that, in
     some cases, the feasible region shrinks so much that it even disappears.

   • High computational complexity of verification. The computational complexity
     of neural network verification algorithms typically grows exponentially with the input
     dimension, which equals the system’s state dimension. As shown in our experiments,
     verifying a relatively small value network in a 4-dimensional system can take more
     than 2 hours on a common computing platform.

    The above analysis reveals a key challenge of synthesizing neural HJ reachability value
functions: the trade-off between scalability and verifiability. Traditional numerical methods
based on state space discretization ensure verifiability but sacrifice scalability. Neural HJ
reachability methods scale well to high-dimensional systems but their synthesized networks
are not verified. Recent verification-guided training methods provide a promising way to
synthesize verifiable neural safety certificates, but they again sacrifice scalability because of
the aforementioned three challenges. To achieve both scalability and verifiability, we propose
a scalable framework for synthesizing formally verified neural HJ reachability value func-
tions, as shown in Figure 1. Our framework consists of three stages: pre-training, adversarial
training, and verification-guided training. Pre-training and verification-guided training are
widely used in existing neural safety certificate synthesis methods (Wang et al., 2023; Chang
et al., 2019; Abate et al., 2020). The former aims to obtain a reasonable approximation
of the value function, while the latter aims to fine-tune the network on counterexamples
until it becomes a valid safety certificate. However, directly performing verification on a
pre-trained value network is inefficient because a pre-trained network usually has a large
number of counterexamples, while only a single one can be found in each verification step.
To improve fine-tuning efficiency, we add an adversarial training stage between them, which
searches and eliminates counterexamples in a batched manner. Verification-guided training
does not start until adversarial training can hardly find any counterexamples. Although
there are many advanced methods for neural network verification, e.g., α, β-CROWN (Xu

                                               3
    Pre-training                                             Adversarial training
                                                                                      Search counterexample
                       MSE
                                                                         Objective
    𝒳                                        Pre-train                   gradient
                                               loss          𝒳                                  Search
    𝑉
                                                                                               direction
                       APA                                   𝑉
                                                                         Constraint
                                                                          tangent
                                                                                                 Step
   𝒳 State space       𝒟 Dataset       𝒴 Output set                                             length
                                                             𝒟       Filter         BGB
   𝑉 Value             𝑓 Dynamics       ℎ Constraint

    Verification-guided training                                                             Update network
                                                                         Constraint
                   𝒳                                                       loss
                                    Hold            𝑉        𝒟
    𝑓
                                                             𝑉           Invariance             Adversarial
    𝑉         MILP                                                          loss                   loss
    ℎ                                                        𝒳
                                   Violate          𝒟                         ESR
                   𝒴                                         𝑉



Figure 1: Neural HJ reachability value function synthesis framework. Our framework con-
sists of three stages: pre-training, adversarial training, and verification-guided training. The
circles of state space and dataset in pre-training and adversarial training mean randomly
sampling states from these sets, while in verification-guided training, the state space and
output set are in analytical form. Our three key techniques are highlighted in blue boxes,
namely APA, BGB, and ESR. The three middle figures show the synthesis results on a
2D task Double Integrator. The pre-trained feasible region is larger than the true feasible
region, indicating that it is invalid. After adversarial training and verification-guided train-
ing, the feasible region becomes valid. Details of the experiment can be found in Section 5.




                                                         4
et al., 2020; Wang et al., 2021), we choose a basic method: mixed integer linear program-
ming (MILP) (Tjeng et al., 2017). This is because most advanced methods are designed for
robust image classification problems, while we consider safety certificate synthesis problems,
which have much lower input dimensions and smaller neural networks. In such small-scale
problems, those advanced methods perform even worse than the basic MILP (Wang et al.,
2021). Note that this does not mean that our problem is simpler than robust image classifi-
cation; in some sense, our problem is even harder as we require certain properties to hold in
the entire input space instead of a small disturbance set. With our three-stage framework in
place, the next step is to find specific methods to solve the problem in each stage. Although
there are many well-studied methods for these three stages, we find that directly using state-
of-the-art methods makes the framework quickly fail as the problem dimension increases,
because these methods cannot effectively solve the aforementioned three challenges. To
this end, we propose three techniques to improve the scalability of our framework, each
designed to address one of the three challenges. First, we find that counterexample search
in adversarial training is difficult because existing gradient-based search methods are ineffi-
cient in searching along the boundary of feasible region. We propose a backtracking method
that rotates the search direction towards the boundary to accelerate counterexample search.
Second, we exploit the fact that constraint-satisfying states that enter the feasible region in
one step are also feasible and penalize the value of these states in fine-tuning to alleviate the
shrinkage of feasible region. Third, we discover that the number of linear segments of the
neural network greatly affects the computational complexity of solving MILP. We design a
regularization term for network pre-training to reduce the number of linear segments and
thus accelerate verification. Our main contributions are summarized as follows.

   • We propose a scalable framework for synthesizing formally verified neural HJ reacha-
     bility value functions. Our framework synthesizes neural value functions from coarse
     to fine with high efficiency through three stages: pre-training, adversarial training,
     and verification-guided training. Pre-training approximates the solution to an HJ
     equation by gradient descent on data samples and obtains a value network that is
     likely to be invalid. Adversarial training searches counterexamples in a batched man-
     ner based on necessary and sufficient conditions for feasible region and fine-tunes the
     value network to eliminate counterexamples. Verification-guided training formulates
     the value network verification problem as an MILP and further fine-tunes the network
     on counterexamples until it is verified.

   • To accelerate counterexample search in adversarial training, we propose an algorithm
     called boundary-guided backtracking (BGB) that efficiently searches along the bound-
     ary of feasible region. When approaching the boundary, BGB rotates the search di-
     rection towards the tangent plane of the boundary so that larger step sizes can be
     taken without stepping out of the feasible region.

   • To alleviate feasible region shrinkage, we present entering state regularization (ESR)
     that adds a penalty term into the loss function when fine-tuning the value network.
     ESR first identifies constraint-satisfying states that enter the feasible region in one
     step and then encourages the values of these states to be negative so that they are
     included in the feasible region.

                                               5
   • To accelerate MILP-based verification, we design a regularization method called ac-
     tivation pattern alignment (APA) for pre-training of value network and dynamics
     network. APA reduces linear segments of a neural network by penalizing the dif-
     ference in the activation patterns of neighboring states while minimizing the loss of
     network’s approximation ability.

   • We provide a benchmark called Cersyve-9 for neural safety certificate synthesis and
     verification in safe control problems, which supplements existing neural network verifi-
     cation benchmarks. Cersyve-9 contains nine commonly used control tasks with various
     dimensions, including linear and nonlinear system dynamics and safety constraints.
     Extensive experiments on Cersyve-9 demonstrate the effectiveness, scalability, and
     efficiency of our synthesis framework. The code of our benchmark is available on
     GitHub1 .

2. Related Works
2.1 Synthesis of Neural HJ Reachability Value Function
Traditional HJ reachability analysis computes the value function by numerically solving
the HJ PDE on a discretized grid of the state space. The computational complexity of
this method grows exponentially with state dimension, making it inapplicable to high-
dimensional problems. To deal with this issue, researchers have explored using neural
networks to approximate the value function.
    A straightforward method for learning a neural value function is to minimize the error
between the two sides of the HJ equation by gradient descent on state samples (Darbon
et al., 2020; Bansal & Tomlin, 2021). However, this method is hard to converge because
the HJ equation does not yield a contraction mapping and thus does not satisfy the con-
vergence conditions of fixed point iteration. In practice, this method typically requires
specific initialization of the value function or rely on certain neural network architectures
to converge to the correct solution. Fisac et al. (2019) solve this problem by introducing
a discount factor into the value function, modifying the original maximum constraint for-
mulation of HJ reachability to a maximum discounted constraint formulation. Under the
discounted formulation, the HJ equation also changes to a discounted version, which yields
a contraction mapping and enables convergence of fixed point iteration with an arbitrary
initialization. This makes temporal difference learning methods in reinforcement learning
(RL) applicable to computing the value function. Since then, the discounted value function
has been extensively used for neural HJ reachability analysis in safe control tasks, especially
when combined with RL algorithms. For example, Hsu et al. (2021) consider reach-avoid
problems and add goal information to the value function proposed by (Fisac et al., 2019).
They derive a discounted reach-avoid Bellman backup and prove that their reach-avoid
Q-learning algorithm converges to an arbitrarily tight conservative approximation of the
reach-avoid set. Yu et al. (2023) establish a self-consistency condition for computing the
value function of a specific policy. They use the value function as the objective function
and constraint for shield and main policies, respectively. The value function is also used
for policy switching during training and safety shield during evaluation. He et al. (2024)
1. https://github.com/intelligent-control-lab/Cersyve.jl


                                                    6
applies the method proposed by (Hsu et al., 2021) to train a reach-avoid value function
in a quadrupedal robot locomotion task. Their value function controls the switch between
an agile policy and a recovery policy, and also guides the recovery policy as an objective
function.
     Despite these advancements, there is an inherent problem in approximating value func-
tion with neural networks: the zero-sublevel set of the value network may not be a valid
feasible region due to approximation errors. Specifically, the zero-sublevel set may violate
the two basic properties of a feasible region: constraint satisfaction and forward invariance.
This can be problematic when using these value networks for constructing constraints in
policy optimization or monitoring unsafe actions in safety filters. With these two prop-
erties unsatisfied, even if the current state is inside the zero-sublevel set, the system may
still run into a constraint-violating state sometime in the future. This problem necessitates
additional verification of the value network, which is not addressed by existing works.

2.2 Verification of Neural Safety Certificates

Safety certificates are real-valued functions of system state that are used to represent feasible
regions and construct constraints or safety filters of control policy. HJ reachability value
function is a kind of safety certificate, and two other representative examples are CBF and
CLF. CBF and CLF are defined through certain inequality conditions which, when strictly
satisfied, ensure that the zero-sublevel sets of these safety certificates are feasible regions.
Similar to HJ reachability value function, CBF and CLF can also be represented by neural
networks, and the resulting neural CBF and CLF also face the problem of verification.
    With the development of neural network verification tools (Liu et al., 2021), some recent
studies have begun to formally verify the inequality conditions of neural CBF and CLF. For
example, Zhang et al. (2024) first decompose a neural CBF into piecewise linear segments
and then solve a nonlinear program to verify safety of each segment. To deal with the non-
differentiable ReLU activation function, they leverage a generalization of Nagumo’s theorem
to prove invariance of sets with non-smooth boundaries and derive necessary and sufficient
conditions for safety. While Zhang et al. (2024) focus on verifying a given neural CBF,
verification of neural safety certificates can also be combined with their training process.
This yields a verification-guided training scheme of neural safety certificates, which iterates
between a learner and a verifier. The learner updates the certificate on data samples to
enforce the satisfaction of safety properties. The verifier either verifies the certificate’s
validity in the entire state space or generates counterexamples and adds them to the dataset
for further training. This iterative procedure terminates when no counterexample is found
by the verifier, in which case the neural safety certificate is formally verified. This training
scheme is widely used for synthesizing formally verified neural CBFs (Peruffo et al., 2021;
Abate et al., 2021; Chen et al., 2024) and neural CLFs (Chang et al., 2019; Abate et al., 2020;
Dai et al., 2021). To improve the efficiency of the verifier, Wang et al. (2023) leverage the
Branch-and-Bound scheme to identify partitions of the state space that are not guaranteed
to satisfy CBF conditions. Additional data from these partitions are incorporated into the
training dataset for further optimization. To accelerate neural CBF training, some works
exploit Lipschitz continuity property of neural CBF and use robust training techniques to
ensure the satisfaction of CBF conditions (Anand & Zamani, 2023; Tayal et al., 2024).

                                               7
    Despite these exploratory works, challenges remain in scaling verifiable neural safety
certificate synthesis methods to high-dimensional problems. Most existing methods only
apply to control systems with less than four state dimensions (Abate et al., 2020; Wang
et al., 2023; Tayal et al., 2024) or special systems with four to eight dimensions whose
state consists of the derivatives of the same variable, and the dynamics is described by
a single scalar ordinary differential equation (Peruffo et al., 2021; Abate et al., 2021).
Chang et al. (2019) and Dai et al. (2021) synthesize verified neural Lyapunov functions
on six-dimensional humanoid and quadrotor systems respectively, but their training takes
hours, and the obtained feasible regions are small, which may result in overly conservative
control policies. Through our study, we discover three main challenges that restrict the
scalability of these methods: 1) difficulty of searching and eliminating counterexamples, 2)
severe shrinkage of feasible region, and 3) high computational complexity of verification. We
propose three techniques to mitigate these three challenges respectively, and they together
significantly improve the scalability of our synthesis framework.

3. Preliminaries
3.1 State Constraint and Feasible Region
Consider a discrete-time deterministic control system:

                                       xt+1 = f (xt , ut ),                                 (1)

where x ∈ X is the state, u ∈ U is the control input, f is the system dynamics, and t ∈ N is
the time step. A control policy maps a state to a control input, i.e., π : X → U. The closed-
loop dynamics under control policy π is denoted as fπ (x) := f (x, π(x)). Safety constraint
of the system is specified by:
                                     h(xt ) ≤ 0, ∀t ∈ N,                                  (2)
where h is the constraint function and the inequalities (2) are called state constraints. Before
implementing a control policy, it is necessary to identify the states where the closed-loop
system always satisfies the state constraints. Such states constitute the feasible region of
the policy, which is defined as follows.

Definition 1 (Feasible region). A feasible region of policy π, denoted as Xπ , is a subset of
the state space X such that ∀x ∈ Xπ , h(xt ) ≤ 0, t ∈ N, where x0 = x and xt+1 = fπ (xt ).

    From the above definition, we can derive a set of necessary and sufficient conditions for
feasible region: constraint satisfaction and forward invariance.

Theorem 1 (necessary and sufficient conditions for feasible region). Xπ is a feasible region
of π if and only if

  1. (Constraint satisfaction) ∀x ∈ Xπ , h(x) ≤ 0.

  2. (Forward invariance) ∀x ∈ Xπ , fπ (x) ∈ Xπ .

    The proof of Theorem 1 follows directly from Definition 1 and is omitted here. Constraint
satisfaction means all states in a feasible region satisfy the state constraint at the current

                                                8
time step. Forward invariance means for any state in the feasible region, its next state
under the closed-loop dynamics still lies in this region. These two conditions are useful for
determining and identifying feasible regions because they only involve a single-step state
transition instead of infinite steps as Definition 1. They are also used as the conditions for
verifying neural HJ reachability value functions in this paper.

3.2 Hamilton-Jacobi Reachability Analysis
Hamilton-Jacobi (HJ) reachability analysis identifies the feasible region of a control system
with state constraints by computing a value function. In a closed-loop system under a given
control policy, the value function is defined as the maximum value of the constraint function
in a trajectory sampled by the policy.

Definition 2 (HJ reachability value function). The HJ reachability value function of control
policy π is defined as
                                   V π (x) := max h(xt ),                                (3)
                                                  t∈N

where x0 = x and xt+1 = fπ (xt ).

   A desirable property of the value function is that its zero-sublevel set is a feasible region.

Theorem 2. The zero-sublevel set of V π , denoted as XV π := {x ∈ X |V π (x) ≤ 0}, is a
feasible region of π.

Proof. We prove that XV π satisfies the two conditions in Theorem 1. ∀x ∈ XV π , we have
h(x) ≤ maxt∈N h(xt ) = V π (x) ≤ 0. Thus, XV π satisfies constraint satisfaction. ∀x ∈ XV π ,
we have V π (fπ (x)) = maxt≥1 h(xt ) ≤ maxt∈N h(xt ) = V π (x) ≤ 0. Thus, XV π satisfies
forward invariance. Therefore, XV π is a feasible region of π.

    Theorem 2 makes the value function useful for representing feasible regions and synthe-
sizing safe controllers. For example, with a possibly unsafe nominal policy and a safe backup
policy π, one can determine whether the nominal policy will lead to a possibly unsafe state
by checking if the next state is in XV π . Specifically, if the next state is in XV π , it is safe as
π can keep the state always in XV π . If the next state is not in XV π , it is possibly unsafe
as π has no safety guarantee outside XV π , and we should replace the nominal policy with
π to compute a safe action. This zero-sublevel set property is one of the most fundamental
properties of safety certificates. In addition to HJ reachability value function, other safety
certificates, such as CBF and CLF, also have similar properties.
    In a stochastic control system, the HJ reachability value function satisfies an HJ PDE
(Bansal et al., 2017). In a deterministic closed-loop system, the minimum and maximum
operators on control inputs and disturbances in the HJ PDE can be omitted, resulting in a
simplified equation called the risky self-consistency condition.

Theorem 3 (Risky self-consistency condition). Let V π be the value function of π, ∀x ∈ X ,
we have
                           V π (x) = max{h(x), V π (fπ (x))}.                          (4)

                                                 9
    The risky self-consistency condition is a recursive relationship between the values of the
previous and subsequent states. In RL, the value function of reward also has a similar
self-consistency condition. Here, the name “risky” distinguishes the HJ reachability value
function from the reward value function, reflecting the former’s relationship to safety con-
straints. With the risky self-consistency condition, we can compute the value function by
solving equation (4). However, this equation does not have an analytical solution in most
cases, and traditional numerical methods based on state space discretization cannot scale to
high-dimensional systems. This necessitates using a neural network to represent the value
function and approximate the solution of equation (4).

3.3 Synthesizing Neural HJ Reachability Value Function
A straightforward method for fitting a neural network to the solution of (4) is to minimize
the error between the two sides of the equation. However, this method is hard to con-
verge because equation (4) does not yield a contraction mapping. To create a contraction
mapping, Fisac et al. (2019) modify the risky self-consistency condition to a discounted
version:
                     V π (x) = (1 − γ)h(x) + γ max{h(x), V π (fπ (x))},                 (5)
where γ ∈ (0, 1) is a discounted factor. They prove that equation (5) induces a contraction
mapping on the value function space under the infinity norm (Fisac et al., 2019). This
ensures that a fixed point iteration converges to the unique solution of equation (5), which
is a discounted version of the value function. As the discount factor γ approaches one, the
solution of (5) approaches that of (4), which is the original value function.
    Suppose we use a feedforward neural network Vθπ to represent the value function, where
θ is the network parameters. To approximate the solution of equation (5), we minimize the
mean squared error (MSE) between the two sides of the equation:

                      N
                 1 X π (i)
      LRSC (θ) =    (Vθ (x ) − ((1 − γ)h(x(i) ) + γ max{h(x(i) ), Vθπ (fπ (x(i) ))}))2 ,     (6)
                 N
                      i=1

where the subscript “RSC” stands for risky self-consistency condition, N is the number of
state samples, and x(i) stands for the i-th state sample. In practice, the states are uniformly
sampled from the state space. However, a problem with this method is that the obtained
value network may not be a valid safety certificate. Specifically, the zero-sublevel set of Vθπ ,
denoted as XVθπ , may not strictly satisfy the necessary and sufficient conditions for a feasible
region given in Theorem 1. The cause for this invalidity is two-fold: 1) approximation errors
of Vθπ make it not exactly the solution to (5), and 2) when the discount factor γ is less than
one, the zero-sublevel set of the solution to the discounted self-consistency condition (5) is
an over-approximation of that of the solution to the original self-consistency condition (4)
(Akametalu et al., 2024). Since the zero-sublevel set of the solution to (4) is already the
maximum feasible region of π, any of its over-approximations is not a valid feasible region.
This invalidity may lead to unsafe behaviors when using Vθπ for synthesizing control policies.
To address this issue, this paper aims to synthesize neural HJ reachability value functions
with verified zero-sublevel sets.


                                               10
Problem 1. Given a control system (1) and a control policy π, synthesize a neural HJ
reachability value function Vθπ , such that its zero-sublevel set is a verified feasible region of
π, i.e., it strictly satisfies the conditions of constraint satisfaction
                               ∀x ∈ X , Vθπ (x) ≤ 0 ⇒ h(x) ≤ 0,                               (7)
and forward invariance
                            ∀x ∈ X , Vθπ (x) ≤ 0 ⇒ Vθπ (fπ (x)) ≤ 0.                          (8)
    Note that the constraint satisfaction and forward invariance conditions only ensure that
the zero-sublevel set of Vθπ is a feasible region but do not ensure that Vθπ is an exact solution
to (4). In fact, they are only necessary conditions for Vθπ to be an exact solution. We
choose to verify these two conditions because exact verification of (4), which is an equation
involving a neural network, is almost impossible due to neural network approximation errors.
In addition, since any safety certificate represents a feasible region by its level set, these
two conditions can also be used to verify other safety certificates, such as CBF and CLF,
with minor modifications.

3.4 Verifying Neural Network via Mixed Integer Linear Programming
Verification of a neural network is to check whether the network’s output lies in a specific
output set for all inputs in a given input set (Liu et al., 2021). Mathematically, let X be the
input set, Y be the output set, and NN(·) be the neural network. A verification problem
requires to check whether the following assertion holds:
                                      ∀x ∈ X , y = NN(x) ∈ Y.                                 (9)
In this paper, we consider the case where NN(·) is a feedforward neural network with ReLU
activation functions. In this case, NN(·) is a piecewise linear function, and the equality
y = NN(x) can be encoded as a set of linear and integer constraints (Tjeng et al., 2017).
Moreover, if the input set X and the complement of the output set Y can be expressed
by a finite number of linear constraints, e.g., X and the complement of Y are polytopes,
assertion (9) can be checked by solving a mixed integer linear programming (MILP):
                            find x,     s.t. x ∈ X , y ∈
                                                       / Y, y = NN(x).                       (10)
Problem (10) tries to find a counterexample in the input set such that the corresponding
output of the neural network is not in the output set. If the problem is feasible, the
property to verify is violated and a counterexample is found. If the problem is infeasible,
the property holds. Note that problem (10) is a feasibility problem, i.e., an optimization
problem without an objective function. It is also possible to include an objective function in
(10), with common examples like maximum violation and minimum disturbance (Liu et al.,
2021). In this paper, since we only focus on whether the property holds or not and have no
preference for counterexamples, we omit the objective function to simplify the problem.

4. Method
This section formally introduces our neural HJ reachability value function synthesis frame-
work. We first provide an overview of our synthesis framework and then detail three key
techniques that significantly improve its scalability.

                                                 11
4.1 Overview
Our framework consists of three stages: pre-training, adversarial training, and verification-
guided training. Pre-training learns a value network without verification, which probably
violates the feasible region conditions. Adversarial training efficiently searches for coun-
terexamples and eliminates most of them by fine-tuning the network. Verification-guided
training finds remaining counterexamples by solving the MILP and further fine-tunes the
network until the feasible region conditions are verified. Pre-training is performed first
and is separate from the other two stages. Adversarial training is performed next, and if
no counterexamples are found in a certain number of iterations, verification-guided train-
ing starts. If a counterexample is found, we return to adversarial training until the next
time verification-guided training is triggered. This process is repeated until verification
succeeds, at which point we have synthesized a valid neural value function. Compared
with most existing neural safety certificate synthesis methods that include pre-training and
verification-guided training (Wang et al., 2023; Chang et al., 2019; Abate et al., 2020), our
framework adds an adversarial training stage between them. This is because a pre-trained
value network usually has a large number of counterexamples, while only a single one can be
found in each verification step, making verification-guided training inefficient. In contrast,
adversarial training searches counterexamples in a batched manner, making the search much
less expensive than that in verification-guided training in terms of computation. First us-
ing adversarial training to reduce counterexamples to a small number and then performing
verification-guided training greatly improves fine-tuning efficiency.
    In pre-training, we learn a value network by minimizing the following loss function.

                                Lpre (θ) = LRSC (θ) + LAPA (θ),                            (11)

where LAPA (θ) is a regularization term computed by activation pattern alignment (APA),
which reduces the number of linear segments of a neural network to accelerate verification.
This technique will be detailed in Section 4.2. The pre-trained value network is not verified
and may violate the feasible region conditions. We fine-tune the network in the next two
stages to make its zero-sublevel set a verified feasible region.
    In adversarial training, we first search for counterexamples, i.e., states that violate
the feasible region conditions. For simplicity of narration, we call the counterexamples
of the constraint satisfaction condition the constraint counterexamples and those of the
forward invariance condition the invariance counterexamples. To find these two kinds of
counterexamples, we solve two corresponding optimization problems. The optimization
problem for finding constraint counterexamples is

                                 max h(x),     s.t. Vθπ (x) ≤ 0,                           (12)
                                 x∈X

and that for finding invariance counterexamples is

                              max Vθπ (fπ (x)),    s.t. Vθπ (x) ≤ 0.                       (13)
                              x∈X

If the optimal value of (12) is greater than zero, the solution is a constraint counterexam-
ple. Similarly, if the optimal value of (13) is greater than zero, the solution is an invariance
counterexample. Generally, problem (12) and (13) are non-convex in both their objective

                                              12
functions and constraints and are thus difficult to solve. However, to find counterexamples,
we do not need to solve them exactly but only need to find feasible points with positive
objective functions, i.e., h(x) > 0 and Vθπ (x) ≤ 0 for constraint counterexamples and
Vθπ (fπ (x)) > 0 and Vθπ (x) ≤ 0 for invariance counterexamples. To achieve this goal effi-
ciently, we propose a gradient-based search method called boundary-guided backtracking
(BGB), which will be detailed in Section 4.3.
     After obtaining counterexamples, we store them in a dataset for fine-tuning the value
network. In each iteration, we randomly sample the two kinds of counterexamples from the
dataset and minimize their corresponding loss functions computed according to the feasible
region conditions. The loss function for constraint counterexamples is
                                                  N
                                                  con
                                              1 X
                               Lcon (θ) =             −Vθπ (x(i)
                                                             con ),                      (14)
                                             Ncon
                                                   i=1

and that for invariance counterexamples is
                                         N
                                        inv
                                    1 X               (i)            (i)
                        Linv (θ) =          Vθπ (fπ (xinv )) − Vθπ (xinv ),              (15)
                                   Ninv
                                          i=1

where Ncon and Ninv are the numbers of constraint and invariance counterexamples re-
                  (i)      (i)
spectively, and xcon and xinv stands for the i-th constraint counterexample and invariance
counterexample, respectively. We discover in our experiments that directly minimizing these
two loss functions will result in severe shrinkage of the value network’s zero-sublevel set.
A possible reason for the shrinkage is that minimizing (15) only decreases the difference
between the values of the next state and the current state, but their respective values may
increase instead. To mitigate this problem, we include an additional regularization term in
the loss function of adversarial training:
                          Ladv (θ) = Lcon (θ) + Linv (θ) + LESR (θ),                     (16)
where LESR (θ) is computed using entering state regularization (ESR), which will be detailed
in Section 4.4.
    In verification-guided training, we use mixed integer linear programming (MILP) to ver-
ify the feasible region conditions or find counterexamples. If the conditions are verified, we
obtain a valid neural value function, and the algorithm ends. If counterexamples are found,
we add them to the dataset for further fine-tuning. The core problem is how to formu-
late the verification of the feasible region conditions as MILPs. In a standard verification
problem (9), there is only one function NN(·), while in our problem, verification of each
condition involves two functions, and their corresponding inequalities have an implication
relationship. To deal with this problem, we first concatenate the two functions into a single
function with two outputs:
                                    π 
                                                              Vθπ (x)
                                                                       
                                    Vθ (x)
                       Mcon (x) =           , Minv (x) =                  .               (17)
                                     h(x)                   Vθπ (fπ (x))
With this concatenation, the feasible region conditions can be naturally expressed by re-
stricting the output of the concatenated function in the complement of the second quad-
rant in a two-dimensional space. Take the constraint satisfaction condition as an example,

                                                 13
“Vθπ (x) ≤ 0 ⇒ h(x) ≤ 0” means the output of Mcon should not be in the second quadrant.
Thus, we can define an output set whose complement is the second quadrant so that the
output constraint “y ∈ / Y” can be expressed by linear inequality constraints. Therefore,
verification of the constraint satisfaction condition can be formulated as

                         find x,    s.t. x ∈ X , y = Mcon (x), y1 ≤ 0, y2 ≥ 0,                           (18)

where yi stands for the i-th element of y. Here, we assume that the state space X is a
hyperrectangle, which is true in most cases. Then, constraint x ∈ X in problem (18) can
be expressed by linear inequalities. Now, as long as Mcon is piecewise linear, problem (18)
is an MILP. Since Vθπ is a piecewise linear neural network, Mcon is piecewise linear when
the constraint function h is piecewise linear. Here, we assume that h is piecewise linear,
and the nonlinear case will be left for future work2 . Verification of the forward invariance
condition can be similarly formulated as

                         find x,     s.t. x ∈ X , y = Minv (x), y1 ≤ 0, y2 ≥ 0.                          (19)

If the dynamics f and the policy π are both piecewise linear functions, Minv is piecewise
linear. Similar to h, we assume that f and π are piecewise linear, and the nonlinear case
will be left for future work. To show how problems (18) and (19) can be encoded as MILPs,
we explicitly write them in a unified standard form of MILP as follows. Here, we view Mcon
and Minv as a single feedforward neural network with ReLU activation functions.

                 find x                                                                                (20a)
                  s.t.   Xl ≤ x ≤ Xu ,                                                                 (20b)
                         z0 = x,                                                                       (20c)
                         ẑj = Wj zj−1 + bj , j = 1, . . . , l,                                        (20d)
                         if ˆlj,k ≥ 0, zj,k = ẑj,k , j = 1, . . . , l − 1, k = 1, . . . , dj ,        (20e)
                         if ûj,k ≤ 0, zj,k = 0,                                                       (20f)
                         otherwise, zj,k ≤ ẑj,k ,                                                     (20g)
                                        zj,k ≥ 0,                                                      (20h)
                                        zj,k ≤ ẑj,k − ˆlj,k (1 − δj,k ), δj,k ∈ {0, 1},                (20i)
                                        zj,k ≤ ûj,k δj,k ,                                             (20j)
                         ẑl = y,                                                                      (20k)
                         y1 ≤ 0, y2 ≥ 0,                                                                (20l)

where Xl and Xu are lower and upper bounds of X , the inequality signs in (20b) represent
element-wise comparisons, ẑj and zj are the j-th layers of the neural network Mcon or Minv
before and after activation, ẑj,k and zj,k are the k-th elements in the i-th layers, ˆlj,k and
ûj,k are the lower and upper pre-activation bounds, δj,k is the binary variable for activation
status. Equations (20e) to (20j) are encodings of ReLU, which follow the method proposed
by Tjeng et al. (2017). The pre-activation bounds ˆlj,k and ûj,k can be computed by any
2. One possible solution is to approximate a nonlinear h using piecewise linear functions, e.g., Taylor model.


                                                      14
reachability-based verification method (Liu et al., 2021), and we use CROWN (Zhang et al.,
2018) in this paper.
    Precisely speaking, the output constraint y2 ≥ 0 in (18) and (19) should be a strict
one, i.e., y2 > 0, according to the feasible region conditions. However, this would make
the two problems no longer standard MILPs and thus difficult to solve. Here, we relax the
strict constraint to a non-strict one to maintain MILP formulations at a slight expense of
completeness: the solutions to (18) and (19) are not counterexamples when y1 ≤ 0 and
y2 ≥ 0 simultaneously hold with equality. Fortunately, this problem is minor in practice
because the situation where these two equalities simultaneously hold is rare: it can only
happen on the boundary of a feasible region. In most cases, such a situation can be avoided
by slightly shrinking the feasible region through fine-tuning. Moreover, when solving (18)
and (19) with numerical optimizers, such as Gurobi, there are likely to be numerical errors
in the inequality constraints, i.e., the constraints are violated by a small amount within a
certain tolerance. Therefore, even without relaxation, y2 has to be strictly less than zero
with some margin so that the optimizer can consider the constraint y2 > 0 unsatisfiable
and conclude that the problem is infeasible.
    In summary, our framework synthesizes a verified neural HJ reachability value function
in three stages by solving four subproblems of problem (1), which are defined as follows.
Subproblem 1 (Pre-training). Train a value network Vθπ by minimizing loss function (11).
Subproblem 2 (Counterexample search). Find constraint counterexamples and invariance
counterexamples of a value network Vθπ by solving problem (12) and (13), respectively.
Subproblem 3 (Fine-tuning). Fine-tune a value network Vθπ by minimizing loss function
(16) on counterexamples found by solving subproblems 2 or 4.
Subproblem 4 (Verification). Verify constraint satisfaction condition and forward invari-
ance condition of a value network Vθπ by solving problem (18) and (19), respectively. If
both problems are infeasible, return the verified Vθπ . If either problem is feasible, return the
found counterexamples.
Subproblem 1 is first solved in the pre-training stage. Then, subproblem 2 and 3 are
iteratively solved in the adversarial training stage until no counterexample is found from
subproblem 2. Next, subproblem 4 is solved in the verification guided-training stage. When
counterexamples are found from subproblem 4, they will still be used to solve subproblem
3, and the algorithm returns to the adversarial training stage. This process is repeated until
subproblem 4 returns a verified value function.
    As mentioned above, we propose three techniques to address the three challenges of
improving the scalability of neural value function synthesis and verification. The three
techniques correspond to solving subproblems 1, 2, and 3, respectively. The following three
subsections provide a detailed introduction to each technique.

4.2 Activation Pattern Alignment
A major difficulty in scaling our proposed framework is the high computational complexity
of MILP-based verification. Our experiment shows that verifying a relatively small value
network in a four-dimensional system can take more than 2 hours on a common computing

                                               15
platform. To alleviate this problem, we first analyze the reason for such a high compu-
tational complexity through the solving mechanism of MILPs. For a neural network with
ReLU activation functions, each ReLU unit can be either active or inactive. To handle a
neural network constraint, a binary variable is introduced for each ReLU unit to model its
activation status, i.e., zero represents an inactive unit, and one represents an active unit,
as shown in (20i) and (20j). With these binary variables, MILP problems are solved us-
ing a branch-and-bound algorithm. The branching step divides the problem into smaller
sub-problems by fixing the values of some binary variables. The bounding step estimates
the lower and upper bounds of the objective function in the sub-problems. The computa-
tional complexity of the branch-and-bound algorithm is mainly determined by the number
of branches to explore, which relies on the number of possible combinations of the binary
variable values. Since each binary variable corresponds to a ReLU unit, we can also say
that the computational complexity relies on the number of possible activation patterns of
the neural network. Each activation pattern corresponds to a linear segment of the neural
network. These linear segments divide the input set into different regions, in each of which
the neural network is a linear function. Since the number of linear segments largely deter-
mines the computational complexity of solving MILPs, we aim to reduce it to accelerate
verification.
    For a neural network with a given structure, its number of linear segments can vary
greatly depending on the network parameter values. For a neural network with N ReLU
units, there is at least one linear segment and at most 2N linear segments in a given input
set. To reduce the number of linear segments, we introduce a regularization method called
activation pattern alignment (APA) when solving subproblem 1 in pre-training. Suppose
we are updating the value network on a batch of states {x(i) }N
                                                              i=1 . APA first adds a Gaussian
noise to each state and obtains a disturbed counterpart of the state:

                                       x̃(i) = x(i) + ξ (i) ,                              (21)

where ξ (i) ∼ N (0, σ 2 ). Then, APA computes the following regularization term and adds it
to the pre-training loss function (11).

                                 N l−1 dj
                           1 XXX      min{fkj (x(i) ) · fkj (x̃(i) ), 0}
           LAPA (θ) = αAPA                                                     ,           (22)
                           N     min{dropgrad(fkj (x(i) ) · fkj (x̃(i) )), −ϵ}
                                i=1 j=1 k=1

where αAPA > 0 is a coefficient, l is the number of network layers, dj is the number of
neurons in the j-th layer, fkj is the value of the k-th neuron in the j-th layer before activa-
tion, and ϵ is a small constant for numerical stability. This regularization term encourages
states that are close to each other to have similar activation patterns. It takes effect when
the activation patterns of x(i) and its disturbed counterpart x̃(i) are different. In this case,
the multiplication of their pre-activation values in the numerator is penalized and driven
towards a positive value so that their activation patterns become the same. The last layer
of the neural network is excluded when computing LAPA because it does not have a ReLU
activation function and thus does not influence the number of linear segments. The denom-
inator of LAPA does not have a gradient with respect to network parameters θ and only
serves as a normalization term.

                                                16
    Reducing the number of linear segments essentially reduces the nonlinearity of a neu-
ral network. From this perspective, other neural network regularization methods may also
achieve this goal. A widely used regularization method is weight decay, which incorpo-
rates an L2 regularization on the network parameters into the optimization process. An-
other method is the signal-to-noise ratio (SNR) loss proposed by Wei et al. (2024), which
is designed to reduce the variance and improve the stability of ReLU units to mitigate
performance degradation in certified training. Compared with these methods, APA most
effectively reduces linear segments while retaining the network’s approximation ability to
the greatest extent, as shown in Section 5.4.1. This is because APA only takes effect when
activation patterns of neighboring states are different and does not affect the specific pre-
activation values when they have the same sign.

4.3 Boundary-Guided Backtracking
In subproblem 2, we solve two constrained optimization problems (12) and (13) to find
counterexamples of the feasible region conditions. Compared with a standard adversarial
training problem (Goodfellow et al., 2014), these two problems not only have a boundary
constraint on the optimization variable but also have a non-convex constraint given by the
zero-sublevel set of the value network. This zero-sublevel set constraint makes these two
problems difficult to solve because most existing adversarial training methods, such as the
fast gradient sign method (Goodfellow et al., 2014) and projected gradient descent (PGD)
method (Madry et al., 2017), cannot directly handle such non-convex constraints.
    A straightforward method for handling the zero-sublevel set constraint is to perform
a backtracking line search in each PGD iteration, resulting in PGD with backtracking
(PGD-B). Specifically, we start the search from an initial state x(0) randomly sampled in
the zero-sublevel set. In each iteration, we perform a backtracking line search along the
gradient of the objective function followed by a projection operation until the resulting state
is in the zero-sublevel set:

                               x(k+1) = ΠX (x(k) + η s gobj,(k) ),                        (23)

where ΠX is the projection operator on X , η ∈ (0, 1) is a constant, s ∈ N is the smallest
number such that Vθπ (x(k+1) ) ≤ 0, and gobj,(k) is the unit vector of the gradient of the
objective function. Take problem (12) as an example,

                                              ∇x h(x)
                                gobj,(k) =                     .                          (24)
                                             ∥∇x h(x)∥2 x=x(k)

The problem with PGD-B is that the search becomes very inefficient when approaching the
boundary of the zero-sublevel set. This is because the gradient of the objective function
becomes almost vertical to the boundary, i.e., in the same direction as the gradient of the
constraint function. This is obvious for problem (13) because the gradients of Vθπ (fπ (x))
and Vθπ (x) are very similar as long as the time step of the system is not very large. For
problem (12), this phenomenon occurs when the boundary of the zero-sublevel set overlaps
or is very close to that of the constrained set. When the gradient becomes vertical to the
boundary, the backtracking line search will end up in very small step sizes or even stops
to avoid stepping out of the zero-sublevel set, as shown in Figure 2(a). It seems to be a

                                                17
                   𝑔obj , 𝑘                                        𝑔con , 𝑘   𝑔obj , 𝑘

                       𝑠=1
                      𝑠=2
                                                                                            𝑠=1
                      ⋯
                                                                                                𝑠=2
                    𝑥 𝑘+1
                                 𝑥con /𝑥inv                                              𝑥 𝑘+1 𝑥con /𝑥inv
              𝑥𝑘                                                         𝑥𝑘
                                                                                                     𝑏𝑘
                      𝑉𝜃𝜋 𝑥 ≤ 0                                                  𝑉𝜃𝜋 𝑥 ≤ 0


                     (a) PGD-B                                                    (b) BGB

Figure 2: Search steps of PGD-B and BGB. The black dot represents the current position
of the search, and the orange dots represent possible counterexamples. (a) PGD-B always
searches along the gradient of the objective function and gets stuck near the boundary of
the feasible region. (b) BGB rotates the search direction towards the tangent plane of the
boundary and effectively search along the boundary, thus finding counterexamples more
efficiently.


minor problem since the counterexamples we are searching for are also located near the
boundary of the zero-sublevel set; otherwise, the state cannot leave the zero-sublevel set or
violate the constraint in one step unless it is already very close to the boundary. However,
practically, PGD-B would get stuck somewhere not exactly at a counterexample because
the initial state is randomly chosen and counterexamples are sparsely distributed. In this
case, even if close to a counterexample, PGD-B may never find it because PGD-B can only
search towards the boundary but not along it.
    To solve the problem of PGD-B, we propose a boundary-guided backtracking (BGB)
method that can efficiently search counterexamples along the boundary. This is achieved
by rotating the line search direction towards the tangent plane of the boundary when ap-
proaching it. Specifically, instead of performing the line search along gobj,(k) , BGB computes
the search direction as a weighted sum of gobj,(k) and another unit vector b(k) , as shown
in Figure 2(b). b(k) is perpendicular to gobj,(k) , coplanar with both gobj,(k) and gcon,(k) and
makes an obtuse angle with gcon,(k) , where gcon,(k) is the unit vector of the gradient of the
constraint function, i.e.,
                                                        ∇x Vθπ (x)
                                          gcon,(k) =                        .                               (25)
                                                       ∥∇x Vθπ (x)∥2 x=x(k)

Then, b(k) is computed as

                                b̂(k)
                   b(k) =                 ,   b̂(k) = (gobj,(k) · gcon,(k) )gobj,(k) − gcon,(k) .           (26)
                              ∥b̂(k) ∥2

                                                           18
     𝒳                                                   𝒳




                  𝑉𝜃𝜋 𝑥 ≤ 0                                             𝑉𝜃𝜋 𝑥 ≤ 0




                   (a) RSR                                               (b) ESR

Figure 3: Regularized states of RSR and ESR. (a) The darker blue dots represent regular-
ized states and the lighter ones are their next states. The regularized states are randomly
sampled in the state space and may be infeasible. (b) The darker red dots represent regu-
larized states and the lighter ones are their next states. The regularized states are entering
states and must be feasible.


BGB line search is performed as

                      x(k+1) = ΠX (x(k) + ηls (ηas gobj,(k) + (1 − ηas )b(k) )),          (27)

where ηl and ηa are backtracking coefficients for step size and search direction, respectively.
The key of BGB is the unit vector b(k) , which determines the changing range of search
direction. We set b(k) vertical to gobj,(k) to ensure that the search direction always makes
a sharp angle with gobj,(k) so that the objective function is always increased. The reason
for setting b(k) coplanar with both gobj,(k) and gcon,(k) is that this is the quickest way to
rotate the search direction from gobj,(k) to the tangent plane of the boundary. Vector b(k)
should make an obtuse angle with gcon,(k) because this is the direction where the constraint
function decreases. Compared with a standard backtracking line search, BGB not only
decreases the step size but also rotates the search direction towards the boundary in each
iteration. The rotation of the search direction prevents BGB from getting stuck near the
boundary and enables it to search efficiently along the boundary. This ability greatly
improves the efficiency of finding counterexamples and accelerates adversarial training, as
evident in Section 5.4.2.

4.4 Entering State Regularization
We discover in our experiments that when fine-tuning the value network in subproblem 3,
directly minimizing loss functions (14) and (15) on counterexamples will result in severe
shrinkage of the zero-sublevel set. Similar phenomena are also observed in other works on
safety certificate synthesis (Chang et al., 2019; Liu et al., 2023). These works deal with this
problem by adding a regularization term that minimizes the output of the value network
on randomly sampled states, as shown in Figure 3(a). This method is called random state

                                                 19
regularization (RSR), and the mathematical formula of its regularization term is
                                                    N
                                                  rnd
                                              1 X           (i)
                             LRSR (θ) = αRSR          Vθπ (xrnd ),                          (28)
                                             Nrnd
                                                     i=1

                               (i)
where αRSR is a coefficient, xrnd is the i-th state uniformly sampled from the state space,
and Nrnd is the number of sampled states. The problem with RSR is that it may cause some
infeasible states to be mistakenly included in the zero-sublevel set, resulting in violations of
the feasible region conditions. To avoid this problem, we only regularize states that do not
compromise the satisfaction of feasible region conditions when included in the zero-sublevel
set. According to the definition of a feasible region, we can derive the following theorem,
which provides a method for expanding a feasible region.

Theorem 4 (Feasible region expansion). Let Xπ be a feasible region of π. ∀x ∈ X \ Xπ , if
h(x) ≤ 0 and fπ (x) ∈ Xπ , Xπ ∪ {x} is also a feasible region of π.

    Theorem 4 tells us that if a state outside the feasible region satisfies the state constraint
and enters the feasible region in one step, it can be included in the feasible region. Such
states are called entering states. The core idea of our regularization method, called entering
state regularization (ESR), is to include entering states into the zero-sublevel set of the value
network, as shown in Figure 3(b). In model predictive control, there is a concept similar
to entering state called precursor set, which is defined as the set of all states whose next
state is in the current set (Borrelli et al., 2017). The precursor set is used for computing
the maximal control invariant set: start from the whole state space as the initial set and
iteratively intersect the current set with its precursor set, the resulting set gradually shrinks
and converges to the maximal control invariant set. Our entering states are those in the
precursor set but not in the current set, and they are used for enlarging a feasible region
instead of shrinking it. To perform ESR, we first randomly sample some states in the state
space in each iteration and then filter out entering states that satisfy:

                          h(x) ≤ −δ, Vθπ (x) > 0, Vθπ (fπ (x)) ≤ −δ,                        (29)

where δ is a small positive constant. The purpose of introducing this constant is to avoid the
undesirable influence of the regularization on nearby states. Specifically, due to the gener-
alization ability of neural networks, when including an entering state into the zero-sublevel
set, some of its nearby states may also be included. These nearby states may not be entering
states and may cause violation of the feasible region conditions. By introducing δ, we set a
margin of entering states to the boundary of the constrained set and the zero-sublevel set,
thus decreasing the probability of mistaken inclusion. Using the filtered entering states, we
compute the following regularization term and add it to the value loss function.
                                                    N
                                                    ent
                                                1 X           (i)
                             LESR (θ) = αESR            Vθπ (xent ),                        (30)
                                               Nent
                                                     i=1

                                                                              (i)
where αESR is a coefficient, Nent is the number of entering states, and xent stands for the
i-th entering state. Minimizing (30) will decrease the values of entering states until they

                                               20
become negative, in which case they are included in the zero-sublevel set and will no longer
be identified as entering states. It is worth mentioning that the states filtered out by (29) are
not necessarily feasible because the value network has not been verified yet. For example, it
is possible that the next state fπ (x), which is currently in the zero-sublevel set, is excluded
from the set in later iterations, making the current state x also infeasible. Therefore, this
regularization method may also cause mistaken inclusion of infeasible states. However, our
method is based on the fact that the value network is pre-trained, which ensures that the
zero-sublevel set does not deviate much from the feasible region. This greatly decreases
the probability of including infeasible states. Moreover, since the zero-sublevel set usually
shrinks during fine-tuning and soon becomes smaller than the feasible region, the filtered
entering states are feasible in most cases. Compared with ESR, existing regularization
methods are more harmful to the feasible region conditions because they use randomly
sampled states for regularization, which are more likely to include infeasible states.


4.5 Analysis of Proposed Framework

In this subsection, we analyze some important properties of our proposed value function
synthesis framework. First, we study the soundness and completeness of the verification in
our framework. In our problem, soundness means that when MILP (18) is infeasible, the
constraint satisfaction condition (7) actually holds, and when MILP (19) is infeasible, the
forward invariance condition (8) actually holds. Completeness means that when either of
the two problems is feasible, its corresponding condition is actually violated. According to
the derivation of MILPs (18) and (19), except for the strictness of their output constraints,
their infeasibilities are equivalent to the satisfaction of conditions (7) and (8), respectively.
Therefore, our method is sound and complete, but its implementation is subject to floating
point error induced incompleteness, as discussed in Section 4.1.
    Next, we study the relationship between the zero-sublevel set of a verified Vθπ , denoted
as XVθπ , and the feasible region of π. Since a verified Vθπ satisfies conditions (7) and (8),
which are necessary and sufficient conditions for a feasible region, XVθπ is a feasible region
of π. Since the feasible region satisfying conditions (7) and (8) is not unique, XVθπ may not
be the maximum feasible region of π but only an under-approximation of it. Nevertheless,
being a feasible region of π, XVθπ already guarantees that trajectories starting from inside it
and sampled under π are safe in the long term. This enables us to use Vθπ and π to construct
a safety filter in which Vθπ is a safety monitor and π is a backup policy (Hsu et al., 2023).
Specifically, starting from inside XVθπ , the safety filter checks in each step whether the next
state after applying some nominal action is still in XVθπ . If this is true, the nominal action
is applied. Otherwise, the nominal action is replaced by the action computed by π, which
ensures by forward invariance condition that the next state is still in XVθπ . This safety filter
can ensure strict long-term constraint satisfaction for an arbitrary policy.
   Finally, we discuss the stability of our training loop, i.e., whether it is guaranteed to find
a verified value function and under what conditions will it fail. Although our framework
successfully synthesizes verified value functions on various tasks in our experiments (See
Section 5), such success is not guaranteed. In some cases, the training loop may not be
able to find a verified value function with a non-trivial zero-sublevel set, even if such a true

                                               21
value function exists. The reasons for the failure of synthesis are multiple, and we list four
main potential failure modes as follows.
  1. Instability of adversarial training. There are always counterexamples found in
     adversarial training, and they cannot be eliminated. As a result, verification cannot
     start before the maximum number of iterations is exceeded. This may be because
     the counterexample search is too inefficient, or catastrophic forgetting happens in
     adversarial training.

  2. Instability of verification-guided training. No counterexamples can be found in
     adversarial training, but verification always fails. This indicates that counterexamples
     exist and the search algorithm is not effective enough to find them.

  3. Inefficient verification. Verification takes so long that the time limit is exceeded.
     This is because the computational complexity of solving the MILPs is too high.

  4. Converging to invalid local optima. The value function becomes all positive in
     the state space, and its zero-sublevel set becomes empty. This is because too many
     feasible states are mistakenly excluded from the zero-sublevel set during fine-tuning,
     causing the set to shrink so much that it disappears.
In essence, these failure modes all stem from the three challenges to improve scalability
mentioned in Section 1. While our proposed three techniques address these challenges to
some extent, they persist as the problem’s dimension increases.

5. Experiments
Through experiments, we aim to answer the following questions: 1) Can our proposed
framework synthesize verified neural HJ reachability value functions on different safe control
tasks? 2) Can APA accelerate verification, and how does it perform compared with other
neural network regularization methods? 3) Can BGB accelerate counterexample search, and
how does it perform compared with other search methods? 4) Can ESR enlarge feasible
region, and how does it perform compared with other feasible region regularization methods?
We answer the first question by testing our framework on nine commonly used safe control
tasks. We answer the remaining three questions by comparing our proposed three techniques
with several existing methods. Before that, we first introduce a neural safety certificate
synthesis and verification benchmark and some implementation details of our framework.

5.1 Cersyve-9 Benchmark
There have been several benchmarks for neural network verification (Brix et al., 2023),
including image classification datasets such as MNIST (LeCun et al., 2010) and CIFAR
(Krizhevsky et al., 2009), vehicle collision prediction problem (Ehlers, 2017), and aircraft
collision avoidance system ACAS Xu (Owen et al., 2019). However, these benchmarks are
incompatible with the verification of neural safety certificates because of the underlying
differences between their problems and safe control tasks. Specifically, safe control tasks
require neural networks to satisfy certain properties everywhere in the state space, i.e., the
input set of the verification problem is the entire state space, while existing benchmarks

                                             22
        (a) Double Integrator           (b) Pendulum                  (c) Unicycle




            (d) Lane Keep               (e) Quadrotor                (f) Cart Pole




            (g) Point Mass              (h) Robot Arm                (i) Robot Dog

Figure 4: Snapshots of safe control tasks in Cersyve-9. The grey objects in Unicycle, Point
Mass, Robot Arm, and Robot Dog are obstacles. The green circle in Robot Dog is the goal.




only consider verification in either a small disturbance set around data samples (LeCun
et al., 2010; Krizhevsky et al., 2009; Ehlers, 2017) or part of the state space (Owen et al.,
2019). In addition, verifying neural safety certificates involves system dynamics and control
policies, which requires certain conversions like (18) and (19) before it can be formulated
as standard verification problems while existing benchmarks only consider verification of a
single neural network.

    To bridge this gap, we provide a benchmark called Cersyve-9 for neural safety Certificate
synthesis and verification in safe control tasks. Cersyve-9 contains: (1) Nine commonly
used control tasks with state dimensions ranging from two to six, as shown in Figure 4 and
Table 1. These tasks include both linear and nonlinear dynamics and safety constraints.
(2) A set of neural safety certificate synthesis tools, including pre-training, adversarial
training, and verification-guided training modules, as well as evaluation tools for synthesized
certificates. These tools facilitate secondary development and performance comparison of
different synthesis algorithms. (3) An MILP-based neural safety certificate verification
algorithm, as well as neural value functions synthesized and verified by our framework on
all nine tasks for comparing different verification algorithms.

                                              23
                  Task           State dim    Control dim     Dynamics     Constraint
          Double Integrator          2              1          Linear        Linear
             Pendulum                2              1         Nonlinear      Linear
              Unicycle               3              2         Nonlinear     Nonlinear
             Lane Keep               4              1          Linear        Linear
             Quadrotor               4              2         Nonlinear      Linear
             Cart Pole               4              1         Nonlinear      Linear
            Point Mass               4              2         Nonlinear     Nonlinear
            Robot Arm                6              3          Linear       Nonlinear
            Robot Dog                5              /         Nonlinear     Nonlinear

Table 1: Information of safe control tasks in Cersyve-9. In Robot Dog, we directly fit
the closed-loop dynamic model with a neural network, and thus, the control dimension is
irrelevant to value network synthesis and verification.


5.1.1 Task descriptions
Each task in Cersyve-9 defines state space, control input space, dynamic model, and safety
constraints, which are detailed as follows.
Double Integrator requires stabilizing a second-order linear system to the origin under
boundary constraints on the position. The state of this task is x = [p, ṗ]⊤ ∈ R2 , where p
is the position. The control input is u ∈ R. The state space and control input space are
hyperrectangles specified by [xmin , xmax ] and [umin , umax ], respectively. All following tasks
adopt the setting of hyperrectangular state and control input spaces. The dynamic model
of this task is
                                      pt+1 = pt + ṗt ∆t,
                                                                                             (31)
                                      ṗt+1 = ṗt + ut ∆t,
where ∆t is the time step. The safety constraint is plb ≤ p ≤ pub , where plb and pub are
lower and upper bounds on the position, respectively.
Pendulum requires stabilizing a pendulum to the upright position under boundary con-
straints on its angle (Brockman et al., 2016). The state of this task is x = [θ, θ̇]⊤ ∈ R2 ,
where θ is the angle of the pendulum. The control input u ∈ R is the torque applied to the
pendulum. The dynamic model is

                              θt+1 = θt + θ̇t+1 ∆t,
                                                                                             (32)
                                                             
                                              3g          9u
                              θ̇t+1 = θ̇t +      sin θt +       ∆t,
                                              2l          ml2

where m is the mass of the pendulum, l is its length, and g is the gravitational acceleration.
The safety constraint is θlb ≤ θ ≤ θub .
Unicycle requires controlling a unicycle model to avoid collision with a circular obstacle.
The state of this task is x = [v, xo , yo ]⊤ ∈ R3 , where v is the velocity angle of the unicycle,
and xo , yo is the position of the obstacle in the unicycle frame. The control input is u =
[a, ω]⊤ ∈ R2 , where a is the acceleration of the unicycle, and ω is its angular velocity. The

                                               24
dynamic model is

                          vt+1 = vt + at ∆t,
                        xo(t+1) = (xot − vt ∆t) cos(ωt ∆t) + yot sin(ωt ∆t),                     (33)
                        yo(t+1) = yot cos(ωt ∆t) − (xot − vt ∆t) sin(ωt ∆t).

                            p
The safety constraint is x2o + yo2 ≥ ro , where ro is the radius of the obstacle.
Lane Keep requires keeping a 2DOF vehicle dynamics model in a straight line under
boundary constraints on its lateral position and heading angle. The state of this task is
x = [y, ϕ, vy , ω]⊤ ∈ R4 , where y is the lateral position of the vehicle, ϕ is the heading angle,
vy is the lateral velocity, and ω is the angular velocity. The control input u = δ ∈ R is the
front wheel angle. The dynamic model is

                     yt+1 = yt + (ϕt vx + vy )∆t,
                    ϕt+1 = ϕt + ωt ∆t,
                                                                  
                                  k1 + k2            ak1 − bk2
                  vy(t+1) = 1 +           ∆t vyt +               − vx ωt ∆t,                     (34)
                                    mvx                 mvx
                                                   k1 a2 + k2 b2
                                                                  
                           ak1 − bk2
                    ωt+1 =            vyt ∆t + 1 +               ∆t ωt ,
                              Iz vx                    Iz vx

where k1 and k2 are the cornering stiffness of the front and rear wheels, respectively, a and
b are the distance from the center of gravity to the front and rear axles, respectively, m
is the mass of the vehicle, Iz is the moment of inertia on the vertical axis, and vx is the
longitudinal velocity, which is a constant value. The safety constraints are ylb ≤ y ≤ yub
and ϕlb ≤ ϕ ≤ ϕub .
Quadrotor requires controlling a 2D quadrotor to a hover position under boundary con-
straints on its vertical position and roll angle. The state of this task is x = [z, θ, ż, θ̇]⊤ ∈ R4 ,
where z is the vertical position of the quadrotor, and θ is the roll angle. The control input
u = [T1 , T2 ]⊤ ∈ R2 represents the thrust forces exerted by the rotors. The dynamic model
is
                            zt+1 = zt + żt ∆t,
                            θt+1 = θt + θ̇t ∆t,
                                                                  
                                            (T1t + T2t ) cos θt                                  (35)
                            żt+1 = żt +                       − g ∆t,
                                                   m
                                          (T2t − T1t )d
                            θ̇t+1 = θ̇t +               ∆t,
                                               Iy

where m is the mass of the quadrotor, d is the diameter, and Iy is the moment of inertia.
The safety constraints are zlb ≤ z ≤ zub and θlb ≤ θ ≤ θub .
Cart Pole requires balancing a pole on a moving cart to the upright position under bound-
ary constraints on the cart position and the pole angle (Brockman et al., 2016). The state
of this task is x = [y, θ, ẏ, θ̇]⊤ ∈ R4 , where y is the cart position, and θ is the pole angle.

                                                 25
The control input u = F ∈ R is the force applied to the cart. The dynamic model is

                            yt+1 = yt + ẏt ∆t,
                            θt+1 = θt + θ̇t ∆t,
                                           F + mlθ̇t2 sin θt − mlθ̈t cos θt                              (36)
                            ẏt+1 = ẏt +                                   ∆t,
                                                         M
                            θ̇t+1 = θ̇t + θ̈t ∆t,

where m is the mass of the pole, M is the total mass of the pole and the cart, l is the length
of the pole, and
                              3M g sin θt − 3(F + mlθ̇t2 sin θt ) cos θt
                        θ̈t =                                            .
                                       (4M − 3m cos2 θt )l
The safety constraints are ylb ≤ y ≤ yub and θlb ≤ θ ≤ θub .
Point Mass has the same setting as Unicycle except that the model is changed to a 2D
point mass. The state of this task is x = [vx , vy , xo , yo ]⊤ ∈ R4 , where vx and vy are the
velocities on the x and y axes, respectively. The control input is u = [a, ω]⊤ ∈ R2 . The
dynamic model is

                          vx(t+1) = (vxt + at ∆t) cos(ωt ∆t) + vyt sin(ωt ∆t),
                          vy(t+1) = vyt cos(ωt ∆t) − (vxt + at ∆t) sin(ωt ∆t),
                                                                                                         (37)
                          xo(t+1) = (xot − vt ∆t) cos(ωt ∆t) + yot sin(ωt ∆t),
                          yo(t+1) = yot cos(ωt ∆t) − (xot − vt ∆t) sin(ωt ∆t).
                           p
The safety constraint is x2o + yo2 ≥ ro .
Robot Arm requires controlling a robot arm with three joints to a target position while
avoiding collision with a wall in the front. The state of this task is x = [θ1 , θ2 , θ3 , θ̇1 , θ̇2 , θ̇3 ]⊤ ∈
R6 , where θ1 is the angle of the first joint, and θ2 and θ3 are the incremental angles of the sec-
ond and third joints relative to their previous joints. The control input u = [θ̈1 , θ̈2 , θ̈3 ]⊤ ∈ R3
represents the angular accelerations of the three joints. The dynamic model is obtained
through forward Euler discretization and omitted here. The safety constraint is that the
length of the robot arm’s projection on the horizontal axis must not exceed a specific
threshold:                                            
                                      X3         Xi
                                           cos     θj  ≤ 1.5.                                            (38)
                                         i=1        j=1

Robot Dog is a robot locomotion task designed by He et al. (2024), which requires con-
trolling a robot dog to reach a goal while avoiding obstacles on its way. The state of this
task is x = [v, xg , yg , xo , yo ]⊤ ∈ R5 , where v is the velocity of the robot dog, xg , yg is the
position of the goal, and xo , yo is the position of the obstacle. In this task, we directly fit a
closed-loop dynamic model with a neural network on data collected by an RL policy, and
thus, the control
              p input is irrelevant to value function synthesis and verification. The safety
constraint is x2o + yo2 ≥ ro .

                                                     26
5.1.2 Implementation details
For tasks with linear dynamic models and constraint functions, we directly use their ana-
lytical forms for value network synthesis. For tasks with nonlinear dynamics or constraints,
we fit the nonlinear dynamics or constraints with neural networks for synthesis. We design
linear control policies with control limits for all tasks except Robot Dog, where we use a
neural network policy trained using the method proposed by He et al. (2024). In Robot Dog,
we directly fit the closed-loop dynamic model with a neural network, and thus, the control
dimension is irrelevant to value network synthesis. In other tasks with nonlinear dynamics,
we fit the open-loop dynamic models with neural networks and substitute linear control
policies to obtain closed-loop dynamics. In this way, all functions involved in verification
are piecewise linear, so the verification problems can be formulated as MILPs. In theory,
we could use the original nonlinear versions of the dynamics and constraints by calling some
verifiers for nonlinear cyber-physical systems (Ivanov et al., 2019; Tran et al., 2020). The
reason why we approximate these functions with piecewise linear neural networks is to better
integrate with existing verification tools. Our neural network approximation of dynamics
and constraints did introduce model mismatch to real-world robot dynamics, but that does
not affect the validity of our benchmark because we can think of synthesis and verification
as inherently performed on systems with approximated dynamics and constraints. It will
be our future work to investigate exact synthesis and verification with respect to nonlinear
dynamics and constraints.
     We follow the practice of Nagabandi et al. (2018) to train neural network dynamic
models. We use a neural network fϕ (x, u) to parameterize the change of state in a time
step, i.e., the predicted next state is x̂t+1 = xt + fϕ (xt , ut ). Training data is collected by
uniformly sampling initial states in the state space and executing random control inputs
at every time step. The collected data is recorded in the form of state transition pairs,
i.e., D = {(x(i) , u(i) , x′(i) )}N
                                  i=1 , where N is the number of data. To ensure the loss function
weights different state elements equally, we subtract the mean and divide the standard
deviation of the data. We then add zero-mean Gaussian noises with a standard deviation
of 0.01 to all data. We train the dynamic model by minimizing the following loss function.

                                        N
                                    1 X
                       Ldyn (ϕ) =       ∥(x′(i) − x(i) ) − fϕ (x(i) , u(i) )∥22 .            (39)
                                    N
                                       i=1

For Robot Dog, we directly train a closed-loop dynamic model fϕ (x) with training data
collected by a neural network policy. Data preprocessing and loss function of Robot Dog
are similar to those of other tasks.
    We use the same neural network structure in all tasks. Both the dynamics and value
networks have two hidden layers with 32 neurons each. The constraint network has two
hidden layers with 16 neurons each. Other hyperparameters of our framework are listed in
Table 2. We ran all experiments on an AMD Ryzen 7 5800 8-Core CPU.

5.2 Evaluation Procedure and Metrics
To evaluate synthesis results, we consider three aspects: 1) counterexample search efficiency,
2) verification efficiency, and 3) size of feasible region.

                                                  27
Stage                  Hyperparameter                           Value
                       Learning rate for dynamics network         1e-3
                       Learning rate for value network            3e-4
                       Batch size                                 256
                       Training epochs for dynamics network       100
Pre-training
                       Iterations for value network             100000
                       Discount factor for value network           0.9
                       Weight decay                               1e-3
                       APA coefficient for dynamics network       0.01
                       APA coefficient for value network          1e-4
                       APA constant ϵ                             1e-4
                       SNR coefficients for dynamics network   (0, 1e-3)
                       SNR coefficients for value network       (0, 0.1)
                       APA & SNR noise scale                       0.1
                       Learning rate                            1e-4
                       Max iteration                           100000
                       Batch size for counterexample search     1000
                       PGD steps per iteration                   10
                       PGD step size                             0.1
Adversarial training
                       Backtracking steps                        20
                       BGB search direction discount             0.5
                       BGB step length discount                  0.8
                       ESR coefficient                           0.1
                       ESR sample batch size                    1000
                       ESR margin δ                             0.01

                  Table 2: Detailed hyperparameters.




                                  28
     For counterexample search efficiency, we count the number of fine-tuning iterations,
total fine-tuning time, and the number of verifications. A smaller number of fine-tuning
iterations means more counterexamples are found and eliminated in each iteration, thus
indicating a higher search efficiency. Fine-tuning time is an overall evaluation of the number
of fine-tuning iterations and time consumption of each iteration, the latter of which largely
depends on the time consumption of counterexample search. Fine-tuning time also counts
the time of all failed verifications, i.e., all verifications except the last one. When the number
of verifications exceeds one, all verification fails except the last one. A failed verification
means that counterexamples still exist, but adversarial training can no longer find them.
Therefore, more verifications also mean that counterexample search is less inefficient. Note
that calling verification does not increase fine-tuning iterations because it is a required step
of each iteration to check whether verification should be called and call it when necessary.
     For verification efficiency, we count the time of the final verification that proves the
feasible region conditions hold. This time plus the fine-tuning time equals the total synthesis
time of the value function.
     For the size of feasible region, we compute a metrics called the true feasible rate (TFR),
which is defined as the proportion of states identified as feasible in all feasible states. In
practice, TFR is approximately computed on a certain number of states randomly sampled
in the state space. To determine whether a state is feasible, we check a finite-length trajec-
tory starting from it. The state is considered feasible if there is no constraint violation in
the trajectory. The trajectory length is set to 100 for all tasks, which is enough to give cor-
rect feasibility results in most cases. For Robot Dog, He et al. (2024) synthesized a neural
value function without verification and used it as a safety filter in a real-world robot dog
locomotion task. We compare the neural value functions synthesized using their method
and our framework to demonstrate the necessity and effectiveness of our framework.

5.3 Synthesis Results
Our proposed framework successfully synthesized neural HJ reachability value functions on
all nine tasks in Cersyve-9, and the results are shown in Table 3. TFRs on most tasks are
greater than 0.8, and the lowest TFR is above 0.4, indicating that the synthesized value
networks represent non-trivial feasible regions. As state dimension increases, it generally
requires more fine-tuning iterations and time to synthesize a verified value network. This
is because searching counterexamples becomes more difficult in higher-dimensional spaces.
The number of verifications also shows a similar increase with state dimension. Another
observation is that systems with nonlinear dynamics generally require more verification
time. This is because nonlinear dynamics results in more linear segments of Minv defined
in (17) for forward invariance verification.
    To understand the effect of fine-tuning on the value network, we plot the changing
curves of TFR and the cumulative number of found counterexamples during fine-tuning
in Robot Arm in Figure 5. At an early stage of fine-tuning, TFR decreases quickly, and
counterexamples increase quickly. In each iteration, the value network is updated on a large
number of counterexamples, excluding many of them from the zero-sublevel set. Verification
cannot be called at this stage because there are many counterexamples found in every
iteration. After 10K iterations, counterexamples can hardly be found in each iteration,

                                               29
                   Task             FT iter (k)        FT time (s)                                # Verify        Verify time (s)            TFR
       Double Integrator                 1.2               28.5                                       1                  0.5                 0.940
          Pendulum                       1.1               31.4                                       1                   3.9                0.962
           Unicycle                      6.9              175.0                                       1                  11.6                0.911
          Lane Keep                       5.9             184.7                                       4                  1.4                 0.750
          Quadrotor                       1.6              55.3                                       1                  2.9                 0.906
          Cart Pole                      2.4               83.3                                       1                 171.5                0.404
         Point Mass                       8.6             321.7                                        4                 48.2                0.594
         Robot Arm                       25.2             853.8                                       15                  5.5                0.403
         Robot Dog                        6.3             333.7                                        2                311.9                0.872

Table 3: Neural HJ reachability value function synthesis results of our proposed framework.


       1.0                                                                                      1e4
                                                                                            6
       0.8                                                     Cumulative counterexamples   5
       0.6                                                                                  4
 TFR




                                                                                            3
       0.4
                                                                                            2
       0.2
                                                                                            1
       0.0                                                                                  0
             0.0     0.5       1.0       1.5     2.0    2.5                                     0.0        0.5      1.0        1.5     2.0       2.5
                           Fine-tuning iteration        1e4                                                      Fine-tuning iteration            1e4

                           (a) TFR.                                                               (b) Cumulative counterexamples.

Figure 5: TFR and cumulative number of found counterexamples during fine-tuning in
Robot Arm. The dashed gray lines stand for the iterations at which verification is called.


and therefore verification starts to be called frequently. At this stage, the value network is
updated on only a few counterexamples, mostly found by verification, in each iteration. As
a result, the change in TFR is very small. This stage continues until the last verification
proves the feasible region conditions hold and returns a valid value network.
    To demonstrate how counterexamples are eliminated through fine-tuning, we visual-
ize the boundary of the zero-sublevel set and counterexamples before fine-tuning and the
boundary after fine-tuning in Double Integrator in Figure 6. Before fine-tuning, there are
many counterexamples near the boundary of the zero-sublevel set. These counterexamples
leave the zero-sublevel set in one step, violating the forward invariance condition and mak-
ing the set not a valid feasible region. This invalidity is also confirmed by the fact that
the pre-trained region is larger than the true region, which is impossible for a valid feasi-
ble region. After fine-tuning, all counterexamples are eliminated, and the zero-sublevel set
shrinks into a valid feasible region slightly smaller than the true region.

                                                              30
Figure 6: Regions and counterexamples in Double Integrator. The pre-trained and verified
regions are zero-sublevel sets of the value networks before and after fine-tuning, respectively.
The heatmap shows the contours of the value network after fine-tuning. The lighter red
dots are counterexamples before fine-tuning, and the darker red dots are their next states.


    To demonstrate the necessity and effectiveness of our method, we visualize the value
trajectories and heatmaps of the value networks synthesized by He et al.’s (2024) method
and our method in Robot Dog, as shown in Figure 7. We choose an initial state that leads
to a constraint violation and compare the values of the two networks on the trajectory. The
value of He et al.’s (2024) network is negative on the initial state, and gradually increases
to positive values along the trajectory. This means that the state starts from inside the
zero-sublevel set but goes out eventually, indicating that the zero-sublevel set of their value
network is not a valid feasible region because it violates the forward invariance condition.
In contrast, our value network consistently outputs positive values on the whole trajectory,
indicating that it correctly excludes the states from its zero-sublevel set. Comparing the
heatmaps of the two value networks, we can see that our network moves the infeasible region
to the upper left. This excludes infeasible states in the upper left from the zero-sublevel set
and includes more feasible states in the lower right into the set. As a result, the zero-sublevel
set becomes a valid feasible region without a significant reduction in its size.

5.4 Comparison Studies
In this subsection, we demonstrate the effectiveness of the three proposed techniques, i.e.,
APA, BGB, and ESR, by comparing them with several existing methods that aim to solve
similar problems.

5.4.1 Neural network regularization
We compare APA with two existing neural network regularization methods, weight decay
(WD) and SNR (Wei et al., 2024), to study its effectiveness in reducing verification time.
We compare these methods from three aspects: number of linear segments, network perfor-

                                               31
    1.00                                   1.5          1.00                                   1.5
    0.75                                   1.2          0.75                                   1.2
    0.50                                   0.9          0.50                                   0.9
                                           0.6                                                 0.6
    0.25                                                0.25
                                           0.3                                                 0.3
    0.00                                                0.00
y




                                                   y
                                           0.0                                                 0.0
    0.25                                                0.25
                                             0.3                                                 0.3
    0.50                                     0.6        0.50                                     0.6
    0.75                                     0.9        0.75                                     0.9
    1.00                                     1.2        1.00                                     1.2
           1.0   0.5   0.0   0.5    1.0                        1.0   0.5   0.0   0.5    1.0
                        x                                                   x


    1.00                                  0.30          1.00                                  0.30
    0.75                                  0.15          0.75                                  0.15
    0.50                                  0.00          0.50                                  0.00
                                            0.15                                                0.15
    0.25                                                0.25
                                            0.30                                                0.30
    0.00                                                0.00
y




                                                   y




                                            0.45                                                0.45
    0.25                                                0.25
                                            0.60                                                0.60
    0.50                                    0.75        0.50                                    0.75
    0.75                                    0.90        0.75                                    0.90
    1.00                                    1.05        1.00                                    1.05
           1.0   0.5   0.0   0.5   1.0                         1.0   0.5   0.0   0.5   1.0
                        x                                                   x


Figure 7: Value trajectories and heatmaps of value networks synthesized by He et al.’s
(2024) method (upper) and ours method (lower) in Robot Dog. In the left two figures, the
red circle in the middle is an obstacle, and the green circle in the bottom right corner (a
quarter shown) is the goal. The two trajectories start from the same initial state (marked
with a red circle) and are sampled by the same policy. They are both truncated at a
constraint-violating state.




                                                   32
                                         w/o reg     Pendulum                                                  w/o reg
                             105         WD          Quadrotor                                        103      WD
                                         SNR         Robot Arm                                                 SNR
 Estimated linear segments


                                         APA                                                                   APA




                                                                              Verification time (s)
                             104                                                                      102

                             103                                                                      101

                             102                                                                      100
                             101
                                   101     102     103     104   105   106                                   103           104             105
                                                     Samples                                                        Estimated linear segments

                                     (a) Linear segment estimate.                                     (b) Linear segments vs. verification time.

Figure 8: Estimated number of linear segments and its relationship with verification time.
In Figure (b), dots with the same color represent the same method in different tasks. For a
thorough comparison of verification times of different regularization methods on each task,
see Table 4.


mance, and verification time. First, we show the relationship between the number of linear
segments and verification time. Then, we compare the number of linear segments and net-
work performance of the three regularization methods. Finally, we compare the verification
times of the three methods on all tasks in Cersyve-9.
    Due to the branch-and-bound solving mechanism of MILP, verification time is closely
related to the number of linear segments of neural networks (Wolsey, 2020). We use a
sampling-based method to estimate the number of linear segments of a neural network.
Specifically, we uniformly sample a certain number of states in the state space, compute the
neural network’s activation pattern on each state, and count the number of unique activa-
tion patterns. This gives us an underestimate of the number of linear segments, and this
estimate becomes more accurate as the number of samples increases. Figure 8(a) shows the
relationship between the estimated number of linear segments and the number of samples.
The two have a linear relationship when the number of samples is small. As the number of
samples increases, the growth rate of linear segments decreases. Theoretically, an infinite
number of samples will give an accurate number of linear segments. We use 106 samples in
our experiments to balance estimation accuracy and computational complexity. Although
this results in an underestimate, it reflects the relative number of linear segments of dif-
ferent methods, which is informative for comparing their verification times. We visualize
the relationship between the number of linear segments and verification time in Figure
8(b). It shows that the two are approximately linearly related, which is consistent with
the branch-and-bound MILP solving mechanism. This allows us to approximately compare
the verification times of different networks by comparing their number of linear segments
without actually solving verification problems.
    We compare the number of linear segments of dynamics networks and value networks
trained with different regularization methods, as shown in Figure 9. Since regularization

                                                                             33
                                                       103                                                                1.0
                   1.50                                                           1.4
                                                                                  1.2                                     0.8
                   1.25




                                                                Linear segments
 Linear segments


                                                       102                        1.0
                   1.00                                                                                                   0.6
                                                                                  0.8




                                                         MSE




                                                                                                                            TFR
                   0.75
                                                       101                        0.6                                     0.4
                   0.50                                                           0.4
                                                                                                                          0.2
                   0.25                                                           0.2
                                                       100
                   0.00                                                           0.0                                     0.0
                          w/o reg   WD    SNR    APA                                    w/o reg   WD     SNR        APA

                             (a) Dynamics networks.                                           (b) Value networks.

Figure 9: Number of linear segments and performance of dynamics networks and value
networks trained with different regularization methods. The results of dynamics networks
are averaged on five tasks with nonlinear dynamics. For each task, all scores are normalized
by dividing those without regularization. The results of value networks are averaged on all
tasks except Cart Pole and Robot Dog, where synthesis failed without regularization.


usually sacrifices the performance of neural networks, we also compare the performance of
different regularization methods. For dynamics networks, we compute the MSE on a test
dataset for performance metrics. For value networks, we compute TFR after fine-tuning
(after the network is successfully verified) for performance metrics. For a fair comparison,
we use the same dynamics network trained with APA to train value networks in each task.
Figure 9(a) shows that APA reduces linear segments of dynamics networks by about five
times compared with no regularization, while WD and SNR both increase linear segments
instead. Moreover, APA has a much lower MSE compared with WD and SNR. Figure
9(b) shows that both APA and WD significantly reduce linear segments of value networks,
and APA brings a greater reduction of about four times. SNR still results in increased
linear segments of value networks. In addition, APA has a higher TFR compared with
WD and SNR, indicating larger feasible regions. These results indicate that APA is the
most effective in reducing linear segments with minimum performance sacrifice. This is
attributed to the appropriate design of APA penalty, which only takes effect when the sign
of pre-activation values of neighboring states are different. In contrast, WD and SNR are
not directly targeted at making activation patterns consistent. They penalize the network
parameters at all times, resulting in large performance sacrifices and inefficiency in reducing
linear segments.
    The regularization strength of APA depends on the coefficient αAPA , which trades off
between the number of linear segments and neural network performance. We train dynam-
ics and value networks under different values of αAPA and visualize the results in Figure
10. Figure 10(a) shows that the number of linear segments of dynamics network quickly
decreases as αAPA increases from 0 to 10−3 and continues to decrease steadily as αAPA
increases from 10−3 to 10−1 . On the other hand, MSE also increases as αAPA increases, and
its increasing rate becomes faster. An appropriate choice of αAPA for dynamics network
should be around 10−3 to 10−2 , which balances the number of linear segments and MSE.

                                                               34
                   1.0                                                                  1.0                                    1.0
                                                             102
                   0.8                                                                  0.8                                    0.8
 Linear segments




                                                                      Linear segments
                   0.6                                                                  0.6                                    0.6




                                                               MSE




                                                                                                                                 TFR
                                                             101
                   0.4                                                                  0.4                                    0.4
                   0.2                                                                  0.2                                    0.2
                   0.0                                       100                        0.0                                    0.0
                         0       10 3         10 2    10 1                                    0     10 5         10 4   10 3
                                        APA                                                                APA


                             (a) Dynamics networks.                                               (b) Value networks.

Figure 10: Number of linear segments and performance of dynamics networks and value
networks trained under different APA coefficients. The results are averaged on the same
tasks as in Figure 9. All scores are normalized by dividing those of αAPA =0.


Figure 10(b) shows that both the number of linear segments of value network and TFR
decreases as αAPA increases. The decrease rate of linear segments is relatively stable under
different values of αAPA . The decrease rate of TFR is small at first and gradually increases
as αAPA increases. An appropriate choice of αAPA for value network should be around 10−4 .
    We compare the verification time of different regularization methods in Table 4. It shows
that APA has the shortest verification time overall, especially in high-dimensional tasks. In
some tasks, such as Unicycle, Lane Keep, and Quadrotor, APA reduces the verification times
by more than 100 times compared with no regularization. Note that without regularization,
verification may take much longer than the time limit (2 hours) in high-dimensional tasks.
The acceleration of verification brought about by APA greatly improves the scalability of our
synthesis framework, enabling it to solve higher-dimensional tasks. The superiority of APA
is due to its effectiveness in reducing linear segments of both dynamics and value networks.
WD also significantly reduces the verification time compared with no regularization because
it reduces linear segments of value networks. However, the acceleration of WD is not so
significant as that of APA in most nonlinear tasks because it cannot reduce linear segments
of dynamics networks. In contrast, SNR has longer verification times than no regularization,
which is consistent with the fact that it increases linear segments of both dynamics networks
and value networks. SNR performs poorly because it is designed to increase the robustness
of a neural network under disturbances, and the results show that this robustness-oriented
objective does not always align with the objective of reducing the number of linear segments.

5.4.2 Counterexample search
We compare our counterexample search method, BGB, with two existing search methods:
projected boundary search (PBS) proposed by Liu et al. (2023) and PGD with standard
backtracking (PGD-B), to study its search efficiency. We count the number of fine-tuning
iterations and fine-tuning times of the three search methods, as shown in Table 5. Results
show that BGB has the smallest number of fine-tuning iterations and fine-tuning time among
the three methods, indicating that it has the highest counterexample search efficiency. PBS

                                                                     35
                          Task              w/o reg        WD          SNR         APA
                  Double Integrator           2.1           0.2         0.5        0.5
                     Pendulum                30.0          0.91        13.58       3.9
                      Unicycle              2597.5         12.42      393.3       11.6
                     Lane Keep               202.4          8.0       1540.9       1.4
                     Quadrotor             Timeout        141.01     Timeout       2.9
                     Cart Pole             Timeout        133.18      1009.1      171.5
                    Point Mass              1216.6          61.2     Timeout      48.2
                    Robot Arm                178.3          7.0       1071.8       5.5
                    Robot Dog              Timeout        1043.9     MaxIter      311.9

Table 4: Verification time (in seconds) of different regularization methods. The dynamics
networks (for nonlinear tasks) and value networks in each column are trained with the same
regularization method. “Timeout” means that fine-tuning exceeds the time limit (2 hours).
“MaxIter” means that fine-tuning exceeds the iteration limit (100k).


                                          FT iter (k)                        FT time (s)
               Task
                                   PBS        PGD-B       BGB         PBS        PGD-B        BGB
       Double Integrator           1.6        1.2          1.2      25.3         50.1         28.5
          Pendulum                 1.5        1.1          1.1      31.3         55.4         31.4
           Unicycle              MaxIter      54.1         6.9     MaxIter      3963.6       175.0
          Lane Keep               41.0        33.1         5.9      916.2       2370.0       184.7
          Quadrotor               21.8         3.1         1.6      578.3        223.7       55.3
          Cart Pole               43.8        62.6         2.4     1276.8       4590.0       83.3
         Point Mass              MaxIter      35.1         8.6     MaxIter      3199.2       321.7
         Robot Arm               MaxIter     MaxIter       25.2    MaxIter      MaxIter      853.8
         Robot Dog               MaxIter      51.5         6.3     MaxIter      3436.2       333.7

Table 5: Number of fine-tuning iterations and fine-tuning time of different counterexample
search methods.


has the lowest search efficiency, exceeding the iteration limit on most high-dimensional
tasks. This is because projecting the state to the boundary of feasible region in every step
is unnecessary and significantly harms search efficiency3 . We need the state to be close to
the boundary only at the final step, not at all intermediate steps. PGD-B also has lower
search efficiency than BGB because standard backtracking can only search toward but not
along the boundary, making it easy to get stuck near the boundary.


3. Projecting the state to the boundary of feasible region in every step is unnecessary not only for HJ
   reachability but also for other safety certificates such as CBF and CLF, at least in discrete-time systems,
   because the feasible region conditions are the same for all safety certificates. The projection may become
   necessary in continuous-time systems where counterexamples must be exactly on the boundary.


                                                     36
                                           TFR                      FT iter (k)
                  Task
                                 w/o reg    RSR      ESR      w/o reg    RSR      ESR
           Double Integrator      0.897     0.960    0.940      1.1       1.2      1.2
              Pendulum            0.856     0.952    0.962      1.0      1.0      1.0
               Unicycle           0.671     0.907    0.911      1.2       3.9      6.9
              Lane Keep           0.651     0.693    0.750      3.5      1.6       5.9
              Quadrotor           0.872     0.901    0.906      2.2       2.3     1.6
              Cart Pole           0.014     0.207    0.404      4.1      14.5     2.4
             Point Mass           0.180     0.549    0.594      1.6       7.5      8.6
             Robot Arm            0.000     0.405    0.403      3.5      79.3     25.2
             Robot Dog            0.659     0.865    0.872      4.0      12.2      6.3

Table 6: TFR and number of fine-tuning iterations of different feasible region regularization
methods.


5.4.3 Feasible region regularization
We compare our feasible region regularization method, ESR, with RSR (Chang et al., 2019;
Liu et al., 2023) and no regularization to study its effectiveness in enlarging feasible regions.
Any feasible region regularization method will make fine-tuning harder because it inevitably
includes some infeasible states into the zero-sublevel set. To evaluate the negative impact on
fine-tuning, we not only compute the TFR of the value networks but also count the number
of fine-tuning iterations of each regularization method, as shown in Table 6. It shows that
ESR has the highest TFR on almost all tasks, significantly increasing TFR compared with
no regularization, especially on high-dimensional tasks. TFR of no regularization becomes
smaller as the state dimension increases, indicating that fine-tuning tends to mistakenly
exclude feasible states from the zero-sublevel set, resulting in feasible region shrinkage.
RSR also increases TFR compared with no regularization, but it is not so effective as ESR,
and its number of fine-tuning iterations is not less than ESR. This is because RSR randomly
pushes all states into the zero-sublevel set, which will mistakenly include more infeasible
states than ESR, resulting in lower regularization efficiency and a greater negative impact
on fine-tuning.

5.4.4 Ablation study
We perform ablation studies to show how the proposed three techniques contribute to the
reduction of overall synthesis time and the increase of TFR, and the results are shown in
Figure 11.
     First, we test a baseline algorithm called Vanilla that directly minimizes MSE without
neural network regularization in pre-training, uses PGD-B to search counterexamples, and
performs fine-tuning without feasible region regularization. Results show that Vanilla fails
to synthesize value functions on three higher-dimensional nonlinear tasks, i.e., Cart Pole,
Point Mass, and Robot Dog. Moreover, it also fails on Robot Arm because the TFR is zero,
i.e., the zero-sublevel set of the value function shrinks to an empty set.

                                               37
                             101
                                       Vanilla           APA          APA+BGB             APA+BGB+ESR
Normalized synthesis time




                                                                                                  Timeout                   Timeout                               Timeout
                             100

                            10 1

                            10 2
                                        ble r              m       cyc
                                                                      le             ep             tor         t Po
                                                                                                                       le
                                                                                                                                      Mas
                                                                                                                                            s
                                                                                                                                                          t Ar
                                                                                                                                                              m
                                                                                                                                                                            t Do
                                                                                                                                                                                g
                                    Doeugrato         dulu      Uni           e Ke               dro      Car                     t                   o                  o
                                                  Pen                      Lan             Qua                                Poin                Rob                Rob
                                    Int

                            1.0
                                                                                                                       Vanilla                  APA+BGB
                            0.8                                                                                        APA                      APA+BGB+ESR
                            0.6
TFR




                            0.4
                            0.2
                            0.0
                                                           m          le              p               r             le                   s                 m                   g
                                        ble r         dulu        cyc             Kee            roto           t Po                  Mas              t Ar              t Do
                                   Doeugrato     Pe n          Uni         Lan
                                                                              e
                                                                                          Qua
                                                                                              d           Car                 Poin
                                                                                                                                  t
                                                                                                                                                  Rob
                                                                                                                                                      o
                                                                                                                                                                    Rob
                                                                                                                                                                        o
                                   In t


Figure 11: Ablation study of three techniques with respect to synthesis time and TFR. The
normalized synthesis time is the synthesis time, i.e., fine-tuning time plus verification time,
of each algorithm divided by that of Vanilla. The “Timeout” annotation on top of the bars
means the corresponding experiments exceed the time limit (2 hours), and we use the time
limit for normalization in these tasks.




                                                                                          38
    Next, we add APA in pre-training and keep the adversarial training part unchanged.
Results show that APA significantly reduces synthesis time on almost all tasks, especially
higher-dimensional ones. The comparison of synthesis time on Robot Arm is meaningless
because all algorithms fail to synthesize a non-trivial value function except the last one
that uses all three techniques. APA’s reduction of synthesis time is mainly attributed
to its acceleration of verification, not only the last verification that proves hold but also
intermediate failed verifications.

    Then, we add BGB for counterexample search and keep the fine-tuning loss unchanged.
Results show that BGB further reduces synthesis time on all tasks and does not cause
significant changes in TFR. BGB’s reduction of synthesis time is mainly attributed to its
acceleration of counterexample search, which results in fewer fine-tuning iterations.

    Finally, we add ESR to fine-tuning loss, obtaining the complete version of our algorithm.
Results show that ESR substantially increases TFR on almost all tasks, especially Cart Pole
and Robot Arm, where other algorithms fail or almost fail to synthesize non-trivial value
functions. Although the synthesis times of the complete algorithm increase compared with
APA+BGB on some tasks, it still achieves a large acceleration compared with Vanilla.
Except for the first two lower-dimensional tasks, the acceleration compared with Vanilla is
close to or more than 10 times on all tasks, and the acceleration on Quadrotor reaches about
100 times. Note that Vanilla exceeds the time limit on three tasks, where the acceleration of
our techniques could be much greater than that shown in the figure. These results indicate
that APA and BGB significantly reduce synthesis time, ESR substantially increases TFR,
and these three techniques together significantly improve the scalability of our framework.


6. Conclusion

This paper proposes a scalable framework for formally synthesizing verified neural HJ reach-
ability value functions. The framework consists of three stages: pre-training, adversarial
training, and verification-guided training. We propose three techniques that significantly
improve the scalability of our framework: boundary-guided backtracking (BGB) to acceler-
ate counterexample search, entering state regularization (ESR) to enlarge feasible regions,
and activation pattern alignment (APA) to accelerate MILP-based verification. We also
provide a neural safety certificate synthesis and verification benchmark called Cersyve-9,
including nine commonly used safe control tasks. Our framework successfully synthesizes
verified neural value functions on all tasks in our benchmark. Extensive experiments show
that the three proposed techniques exhibit superior scalability and efficiency compared with
existing methods. While our experiments mainly focus on the synthesis side, the proposed
benchmark could also foster additional study in the verification community on scaling up
verification algorithms with respect to these unique types of problems. For future work,
there is still room for further scaling this framework to higher-dimensional problems. Also,
considering the approximation error of neural network dynamic models in verification is
necessary for applying this framework to real-world tasks. Moreover, this framework can
be used to synthesize and verify other neural safety certificates, such as neural CBFs and
CLFs.

                                             39
Acknowledgments

This work is in part supported by the National Science Foundation under Grant No.
2144489. Any opinions, findings, and conclusions or recommendations expressed in this
material are those of the authors and do not necessarily reflect the views of the National
Science Foundation.

References
Abate, A., Ahmed, D., Edwards, A., Giacobbe, M., & Peruffo, A. (2021). Fossil: a software
     tool for the formal synthesis of lyapunov functions and barrier certificates using neural
     networks. In Proceedings of the 24th International Conference on Hybrid Systems:
     Computation and Control, pp. 1–11.
Abate, A., Ahmed, D., Giacobbe, M., & Peruffo, A. (2020). Formal synthesis of lyapunov
     neural networks. IEEE Control Systems Letters, 5 (3), 773–778.
Akametalu, A. K., Ghosh, S., Fisac, J. F., Rubies-Royo, V., & Tomlin, C. J. (2024). A
    minimum discounted reward hamilton–jacobi formulation for computing reachable
    sets. IEEE Transactions on Automatic Control, 69 (2), 1097–1103.
Anand, M., & Zamani, M. (2023). Formally verified neural network control barrier certifi-
    cates for unknown systems. IFAC-PapersOnLine, 56 (2), 2431–2436.
Bansal, S., Chen, M., Herbert, S., & Tomlin, C. J. (2017). Hamilton-jacobi reachability:
     A brief overview and recent advances. In 2017 IEEE 56th Annual Conference on
     Decision and Control (CDC), pp. 2242–2253. IEEE.
Bansal, S., & Tomlin, C. J. (2021). Deepreach: A deep learning approach to high-dimensional
     reachability. In 2021 IEEE International Conference on Robotics and Automation
     (ICRA), pp. 1817–1824. IEEE.
Borrelli, F., Bemporad, A., & Morari, M. (2017). Predictive control for linear and hybrid
     systems. Cambridge University Press.
Brix, C., Müller, M. N., Bak, S., Johnson, T. T., & Liu, C. (2023). First three years of the
      international verification of neural networks competition (vnn-comp). International
      Journal on Software Tools for Technology Transfer, 25 (3), 329–339.
Brockman, G., Cheung, V., Pettersson, L., Schneider, J., Schulman, J., Tang, J., & Zaremba,
     W. (2016). Openai gym..
Chang, Y.-C., Roohi, N., & Gao, S. (2019). Neural lyapunov control. Advances in neural
    information processing systems, 32.
Chen, M., Herbert, S., & Tomlin, C. J. (2016). Fast reachable set approximations via state
     decoupling disturbances. In 2016 IEEE 55th Conference on Decision and Control
     (CDC), pp. 191–196. IEEE.
Chen, S., Molu, L., & Fazlyab, M. (2024). Verification-aided learning of neural network
     barrier functions with termination guarantees..
Dai, H., Landry, B., Yang, L., Pavone, M., & Tedrake, R. (2021). Lyapunov-stable neural-
     network control..

                                             40
Darbon, J., Langlois, G. P., & Meng, T. (2020). Overcoming the curse of dimensionality for
     some hamilton–jacobi partial differential equations via neural network architectures.
     Research in the Mathematical Sciences, 7 (3), 20.
Ehlers, R. (2017). Formal verification of piece-wise linear feed-forward neural networks. In
     Automated Technology for Verification and Analysis: 15th International Symposium,
     ATVA 2017, Pune, India, October 3–6, 2017, Proceedings 15, pp. 269–286. Springer.
Fisac, J. F., Lugovoy, N. F., Rubies-Royo, V., Ghosh, S., & Tomlin, C. J. (2019). Bridging
      hamilton-jacobi safety analysis and reinforcement learning. In 2019 International
      Conference on Robotics and Automation (ICRA), pp. 8550–8556. IEEE.
Goodfellow, I. J., Shlens, J., & Szegedy, C. (2014). Explaining and harnessing adversarial
    examples..
He, T., Zhang, C., Xiao, W., He, G., Liu, C., & Shi, G. (2024). Agile but safe: Learning
     collision-free high-speed legged locomotion..
Hsu, K.-C., Hu, H., & Fisac, J. F. (2023). The safety filter: A unified view of safety-critical
     control in autonomous systems. Annual Review of Control, Robotics, and Autonomous
     Systems, 7.
Hsu, K. C., Rubies-Royo, V., Tomlin, C. J., & Fisac, J. F. (2021). Safety and liveness
     guarantees through reach-avoid reinforcement learning. In 17th Robotics: Science and
     Systems, RSS 2021. MIT Press Journals.
Ivanov, R., Weimer, J., Alur, R., Pappas, G. J., & Lee, I. (2019). Verisig: verifying safety
     properties of hybrid systems with neural network controllers. In Proceedings of the
     22nd ACM International Conference on Hybrid Systems: Computation and Control,
     pp. 169–178.
Krizhevsky, A., Hinton, G., et al. (2009). Learning multiple layers of features from tiny
     images..
LeCun, Y., Cortes, C., Burges, C., et al. (2010). Mnist handwritten digit database..
Liu, C., Arnon, T., Lazarus, C., Strong, C., Barrett, C., Kochenderfer, M. J., et al. (2021).
      Algorithms for verifying deep neural networks. Foundations and Trends® in Opti-
      mization, 4 (3-4), 244–404.
Liu, S., Liu, C., & Dolan, J. (2023). Safe control under input limits with neural control
      barrier functions. In Conference on Robot Learning, pp. 1970–1980. PMLR.
Madry, A., Makelov, A., Schmidt, L., Tsipras, D., & Vladu, A. (2017). Towards deep
    learning models resistant to adversarial attacks..
Mitchell, I. M. (2007). Comparing forward and backward reachability as tools for safety
     analysis. In International Workshop on Hybrid Systems: Computation and Control,
     pp. 428–443. Springer.
Mitchell, I. M. (2008). The flexible, extensible and efficient toolbox of level set methods.
     Journal of Scientific Computing, 35, 300–329.
Nagabandi, A., Kahn, G., Fearing, R. S., & Levine, S. (2018). Neural network dynamics for
    model-based deep reinforcement learning with model-free fine-tuning. In 2018 IEEE
    international conference on robotics and automation (ICRA), pp. 7559–7566. IEEE.

                                              41
Owen, M. P., Panken, A., Moss, R., Alvarez, L., & Leeper, C. (2019). Acas xu: Integrated
    collision avoidance and detect and avoid capability for uas. In 2019 IEEE/AIAA 38th
    Digital Avionics Systems Conference (DASC), pp. 1–10. IEEE.
Peruffo, A., Ahmed, D., & Abate, A. (2021). Automated and formal synthesis of neural
      barrier certificates for dynamical models. In International conference on tools and
      algorithms for the construction and analysis of systems, pp. 370–388. Springer.
Tayal, M., Zhang, H., Jagtap, P., Clark, A., & Kolathaya, S. (2024). Learning a formally
     verified control barrier function in stochastic environment..
Tjeng, V., Xiao, K., & Tedrake, R. (2017). Evaluating robustness of neural networks with
     mixed integer programming..
Tran, H.-D., Yang, X., Manzanas Lopez, D., Musau, P., Nguyen, L. V., Xiang, W., Bak, S.,
     & Johnson, T. T. (2020). Nnv: the neural network verification tool for deep neural
     networks and learning-enabled cyber-physical systems. In International Conference
     on Computer Aided Verification, pp. 3–17. Springer.
Wang, S., Zhang, H., Xu, K., Lin, X., Jana, S., Hsieh, C.-J., & Kolter, J. Z. (2021). Beta-
    crown: Efficient bound propagation with per-neuron split constraints for neural net-
    work robustness verification. Advances in Neural Information Processing Systems, 34,
    29909–29921.
Wang, X., Knoedler, L., Mathiesen, F. B., & Alonso-Mora, J. (2023). Simultaneous syn-
    thesis and verification of neural control barrier functions through branch-and-bound
    verification-in-the-loop training..
Wei, T., Wang, Z., Niu, P., ABUDUWEILI, A., Zhao, W., Hutchison, C., Sample, E., &
     Liu, C. (2024). Improve certified training with signal-to-noise ratio loss to decrease
     neuron variance and increase neuron stability..
Wolsey, L. A. (2020). Integer programming. John Wiley & Sons.
Xu, K., Zhang, H., Wang, S., Wang, Y., Jana, S., Lin, X., & Hsieh, C.-J. (2020). Fast and
     complete: Enabling complete neural network verification with rapid and massively
     parallel incomplete verifiers..
Yu, D., Zou, W., Yang, Y., Ma, H., Li, S. E., Yin, Y., Chen, J., & Duan, J. (2023). Safe
     model-based reinforcement learning with an uncertainty-aware reachability certifi-
     cate..
Zhang, H., Wu, J., Vorobeychik, Y., & Clark, A. (2024). Exact verification of relu neural
     control barrier functions. Advances in Neural Information Processing Systems, 36.
Zhang, H., Weng, T.-W., Chen, P.-Y., Hsieh, C.-J., & Daniel, L. (2018). Efficient neural
     network robustness certification with general activation functions. In Advances in
     neural information processing systems, Vol. 31.




                                            42
