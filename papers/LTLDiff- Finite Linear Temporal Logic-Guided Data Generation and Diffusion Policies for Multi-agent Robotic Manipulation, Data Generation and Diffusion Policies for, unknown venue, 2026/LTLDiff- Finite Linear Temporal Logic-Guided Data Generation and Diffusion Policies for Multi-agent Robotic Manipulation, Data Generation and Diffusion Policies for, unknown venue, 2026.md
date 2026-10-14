                                             LTLDiff: Finite Linear Temporal Logic–Guided
                                               Data Generation and Diffusion Policies for
                                                  Multi-agent Robotic Manipulation

                                                      Chuhan Meng1[0009−0003−9279−6818] and Haiyan Yin2

                                                           University of Toronto, Toronto, ON, Canada
                                                           1
arXiv:2609.11043v1 [cs.RO] 10 Sep 2026




                                                                chuhan.meng@mail.utoronto.ca
                                          2
                                            A*STAR Centre for Frontier AI Research (A*STAR CFAR), Agency for Science,
                                                        Technology and Research (A*STAR), Singapore
                                                                  Yin_Haiyan@a-star.edu.sg


                                               Abstract. Multi-agent robotic manipulation tasks require coordination
                                               among agents to satisfy task-level temporal, logical, and safety con-
                                               straints. Recently, diffusion policies have been used to perform the task.
                                               However, they still suffer from desynchronization, incorrect action or-
                                               dering, and coordination failures in tasks that require simultaneous or
                                               sequential multi-agent interaction. Therefore, LTLDiff is proposed as a
                                               framework that combines Finite Linear Temporal Logic (LTLf ) specifica-
                                               tion learning for both the generation of demonstrations and learning via
                                               diffusion policies. Each task has a specific LTLf formula that is learned
                                               from a set of natural language instructions using a large-scale language
                                               model. To enable a fixed-dimensional vector embedding of the learned
                                               specification from the language model, LTLf uses an abstract syntax tree
                                               representation scheme. This embedding of logic serves as a condition for
                                               (i) logic-guided data collection and (ii) diffusion-based policy training,
                                               encouraging trajectories that are consistent with the desired ordering and
                                               coordination requirements. Experiments on multi-agent LTLDiff manip-
                                               ulation tasks demonstrate improved task success rates compared to the
                                               baseline. Together, these contributions demonstrate the effectiveness of
                                               LTLDiff for coordinated multi-agent manipulation.

                                               Keywords: Multi-agent Robotic Manipulation · Diffusion Policy · Fi-
                                               nite Linear Temporal Logic.


                                         1    Introduction
                                         Robust developments in robot platforms and control methodologies allow robotic
                                         systems to successfully implement tasks with fixed procedures [1,2] and carry out
                                         tasks following high-level instructions [3,4]. However, applying such capabilities
                                         in multi-agent robotics remains an issue. State-of-the-art methods in multi-agent
                                         robot control are predominantly found in two categories: one is the rule-based
                                         method, and the other is the learning-based method, neither of which has been
                                         demonstrated to be sufficient in the following ways. Rule-based methods [8] en-
                                         able safety and temporal requirements to be strictly satisfied through predefined
2      C. Meng and H. Yin

logic; However, they suffer from limited flexibility in adapting to novel tasks
and changing environmental conditions. The learning-based method [7] lacks
an essential mechanism to satisfy critical safety and temporal requirements in
actual task execution, despite having the flexibility to adapt to novel task set-
tings through behavior cloning and reinforcement learning approaches. Recent
frameworks such as RoboFactory [6] partially address this challenge by enforcing
compositional logical, spatial, and temporal constraints during data generation
for multi-agent tasks. Nevertheless, the resulting agents still lack explicit coor-
dination and temporal reasoning during execution because such constraints are
not incorporated into policy training.



    LTLDiff lies between the rule-based and the learning-based methods. It ad-
dresses these complementary limitations by leveraging diffusion policies for task
adaptation while incorporating LTLf specifications as structured conditioning
inputs. At the start, LTLDiff utilizes multi-agent robotics coordination by en-
coding LTLf , which is not enforced as hard rules but rather can be applied
generally at runtime with soft gradient guidance. Next, LTLDiff generalizes the
logic-guided diffusion policies, LTLDOG [5], to multi-agent diffusion policies by
extending them through the addition of LTLf conditioning. The gradient guid-
ance is applied during diffusion training by employing a regressor neural net-
work to predict LTLf satisfaction gradients in the multi-agent scenario, thereby
forecasting joint trajectory satisfaction and influencing the bias towards gen-
erated LTLf -satisfying behaviors during trajectory sampling. The expressive-
ness of logic-conditioned algorithms is guided by their dependence on predefined
LTLf specifications. To preserve this structure, LTLf formulas are parsed into
abstract syntax trees and encoded as fixed-dimensional vectors that preserve
compositional structure and temporal semantics. As a result, LTLDiff enables
reliable conditioning of both the data and diffusion policy on compositional and
temporally structured task semantics. Lastly, LTLDiff is applicable to multi-
agent execution, where all agents learn simultaneously using different policies
and local views. The coordination among the agents occurs implicitly based on
the target condition and task instruction, without any joint policy, which shows
good scalability.



    The primary contributions of this research work include: (i) An LTLf genera-
tor is proposed to pair LTLf formulas with each task based on natural-language
descriptions of task objectives and guides the data generation process using a
large language model. (ii) LTLMAG is proposed for multi-agent regressor-guided
planning, which integrates LTLf constraints into the diffusion policy. (iii) Ex-
perimental results on RoboFactory manipulation tasks demonstrate higher task
success rates across most evaluated tasks compared to the baseline method and
LTLDOG-R. Hence, they highlight the effectiveness of the proposed LTLDiff
framework.
                             LTLDiff for Multi-Agent Robotic Manipulation         3

2     Related Work
2.1   Multi-Agent Robotic Systems
A multi-agent system is composed of several separate agents. Every entity may
have conflicting objectives and access to different information. Tool-based agent
assistants [11] and simulation environments for societies or games [12] are the
two primary categories of multi-agent systems that are distinguished by their
functionalities. In contrast to the aforementioned two, LTLDiff focuses more on
the use of multi-agent collaboration, specifically the low-level manipulation of
embodied agents.

2.2   Robot Manipulation
Traditional robotic manipulation relies on rule-based approaches. A* [9] and
LTL-based [10] are often used to generate collision-free trajectories when the
geometric and kinematic constraints are known. These planning and control
strategies are restrictive in complex manipulation tasks, despite providing high
guarantees of safety and feasibility. Learning-based approaches emphasize the
value of flexibility and data-driven management. Behavioral Cloning [13,15] fo-
cuses on demonstrations, and Offline Reinforcement Learning [16] makes use of
offline data. The quality of offline data-based trajectories is further improved
by diffusion policies [14], which mainly focus on fulfilling safety-related tasks or
static constraints without explicitly addressing temporal logic or coordination
dependency.

2.3   Learning and Planning under Temporal Logic
Finite Linear Temporal Logic is a powerful formalism to express high-level con-
straints [14] of tasks in a temporal structure. LTLf formulas have been applied to
robotic planning to specify temporal constraints of tasks [17,18]. Reinforcement
learning in the context of LTLf objectives was also investigated to efficiently
learn policies satisfying LTLf formulas. The solutions so far require interacting
with the physical system through trial-and-error procedures, which may be ex-
pensive or even dangerous. Also, the existing solutions using LTLf are rarely
compatible with offline policy learning approaches [19]. Reliance on trial-and-
error interaction is reduced by using LTLf specifications to guide offline demon-
stration generation and by incorporating the same logic as a conditioning signal
in diffusion-based policy learning.

3     LTLDiff
3.1   Problem Formulation
LTLDiff focuses on offline learning of multi-agent robotic manipulation with sym-
bolic temporal constraints. The goal is to learn policies that perform physically
valid trajectories, and are guided by LTLf specifications expressing task-level
ordering and coordination requirements.
4       C. Meng and H. Yin




Fig. 1. LTLDiff Pipeline. The task descriptions and conditions are transformed into
atomic propositions and an LTLf formula by an LTLf generator. The encoded logic
and compositional constraints [6] are used in offline data generation, whereas multi-
agent observations and the LTLf embedding are utilized by LTLMAG for coordinated
trajectory generation.



Multi-Agent Setting. A system of N robotic agents {a1 , . . . , aN } is operating
in a shared environment. Agents receive RGB observations O = {oglobal , o1 , . . . , oN },
where oglobal denotes a global scene view and oi denotes the egocentric RGB ob-
servation of agent i. At each time step t, agent ai receives an observation oti ∈ O,
consisting of visual observations and states, sti ∈ S. A joint multi-agent trajec-
tory τ over a finite horizon T is defined as:

                                                                                  T
                              otglobal , ot1 , . . . , otN , st1 , . . . , stN
                          
                     τ=                                                            t
                                                                                       .   (1)


LTLf Task Specification. Each task is associated with a finite-horizon LTL
formula φ defined over a set of atomic propositions P. These propositions cor-
respond to task-relevant events such as objects, names, agents, etc. The LTLf
formula is formed according to the task description and target condition. There
are some temporal and logical constraints included implicitly in the description,
such as ordering (e.g., “grasp before lift”), safety (e.g., “always avoid collision”),
or coordination (e.g., “both agents must grasp before lifting”).


Offline Dataset. An offline dataset is formed by using:

                                   D = {(τ (k) , φ)}K
                                                    k=1 ,                                  (2)

where each demonstration trajectory τ (k) is paired with its task LTLf specifica-
tion φ. The dataset is collected before training, and no environment interaction
during learning.
                              LTLDiff for Multi-Agent Robotic Manipulation         5

Learning Objective. The aim of LTLDiff is to train a conditional diffusion
policy to execute tasks.
                             πθ (τ | zφ ),                             (3)
πθ represents the diffusion policy and zφ ∈ Rd represents the LTLf formula
after encoding it into a fixed-dimensional vector, which is passed to the diffusion
policy as a conditioning signal.


3.2   LTLf Generator

Each manipulation task begins with a natural language description of its task
and target conditions. These descriptions implicitly state temporal ordering and
logical dependencies that must be extracted and formalized. A large language
model called Qwen is used to generate the LTLf . Each LTLf formula is gen-
erated ten times using Qwen. Qwen then re-examines the task description and
target condition to select the most appropriate formula from the ten candidates.
The task description, target condition, and full prompt are provided in the sup-
plementary material.
    These generated formulas are presented in a formatted JSON structure,
which includes a description of the tasks, a set of atomic statements, and an
LTLf formula defined in the statements. Every atomic statement can be viewed
as an expression in Boolean manipulation based on an event or a state in a ma-
nipulation task. It represents different states associated with objects, interactions
between agents and objects, or coordination events.
    The LTLf is built through a restricted set of temporal and logical opera-
tors consistent with the implementation. Temporal relationships are expressed
using the operators F (eventually), G (globally), U (until), and X (next), which
capture ordering constraints, safety invariants, and goal conditions over time.
Logical structure is represented using the operators & (and), | (or), -> (impli-
cation), and ! (negation), allowing the specification of conditional dependencies
and forbidden conditions.


3.3   LTLf Encoder

After an LTLf specification is generated, it is converted to a structured 128-
dimensional vector representation by using the LTLf Encoder. This format can
be passed to the data generation process and diffusion policy. The encoding
process has two stages: tokenization and parsing, and AST-based embedding.


Tokenization and Parsing. Operators, propositions, and parentheses are ex-
plicitly separated to tokenize the LTLf formula φ ∈ LTLf (P ), where P is the set
of atomic propositions defined for the task. The tokenized formula is then parsed
to generate an Abstract Syntax Tree (AST) to denote its hierarchical structure.
The logical combination expression and the temporal constraints conveyed in
the LTLf formula are preserved in the AST.
6      C. Meng and H. Yin

AST-based Encoding. To enable learning with fixed-size neural network in-
puts, the Abstract Syntax Tree (AST) Tφ = (V, E) is converted into a fixed-
dimensional vector representation via recursive encoding. Each node v ∈ V
corresponds to either an atomic proposition (leaf node) p ∈ P or a tempo-
ral or logical operator (internal node) o ∈ {F, G, X, U, &, |, ->, !}. The edge set
E defines the parent–child relationships between operators and their operands,
preserving the hierarchical structure of the LTLf formula. The resulting root
embedding provides a compact representation of the full specification.
    Every leaf node in the AST is encoded as a one-hot vector on the set of propo-
sitions and represents an atomic proposition. For a leaf node v corresponding to
an atomic proposition p, the node embedding is defined as
                                hv = OneHot(p).                                (4)
The encoding process for an internal node starts with its operator encoding,
which combines with the encoded child nodes hu to show the internal structure
of the node. The operator encoding uses a summary representation which results
from recursive computation and averaging of embedded child nodes C(v) to create
their combined encoding. Equation 5 defines the internal node:
                          h                 1    X      i
                    hv = OneHot(ov ) ∥               hu .                   (5)
                                          |C(v)|
                                                  u∈C(v)

where OneHot(ov ) denotes the one-hot encoding of the operator type at node v.
Finally, the embedding of the full LTLf formula is given by the root node of the
AST:
                           zφ = Pad hroot(Tφ ) ∈ Rd ,
                                              
                                                                             (6)
where Pad(·) denotes zero-padding to a fixed dimension d = 128, consistent with
the regressor and diffusion policy input size.

3.4   LTLf Guided Offline Data Generation
With the aim of producing demonstrations that are applicable to the task, task-
level logic is incorporated into the motion planner employed in the task demon-
stration data generation process. In this regard, each task is considered to be
coupled with a fixed solution structure, which is constructed by a set of mo-
tion primitives. In addition, the data generation process is divided into various
phases, which are determined by the atomic propositions and the temporal struc-
ture defined in the LTLf formula. A phase is defined as every semantically valid
sub-task, according to the logic constraints. The atomic propositions are used as
the interface between high-level task semantics and low-level motion execution,
specifying the active and relevant task aspects.
    A structured vector representation of the LTLf formula is formed by the
atomic propositions, and it is used as a conditioning bias for modulating the
motion planning parameters. These motion planning parameters include veloc-
ity, smoothness of accelerations, and object position. Rather than directly map-
ping atomic propositions to specific parameter values, the presence of particular
                               LTLDiff for Multi-Agent Robotic Manipulation            7

propositions in the LTLf formula determines which motion planning parameters
are eligible for modulation, while the corresponding LTLf embedding values de-
termine the magnitude and direction of the applied adjustment. The motion
planner utilizes this conditioning bias for generating motion trajectories, which
are more correlated with the temporal structure of the LTLf formula. It gener-
ates demonstrations in the form of pairs made up of a trajectory and its LTLf
formula specification, defined in Eq. (2).
    Although RoboFactory supports spatial, temporal, and logical constraints
through separate modules that operate during data generation, these constraints
do not have a unified mechanism to specify task-level semantics. However, LTLf
has a unified compositional form with explicit temporal and logical operators,
which is beneficial for reasoning over entire trajectories and ensuring that local
behavior is not globally inconsistent. Therefore, LTLf is a machine-interpretable
formalism that unifies multi-agent interaction modeling, formal verifiability, and
conditioning for logic-guided data generation.


3.5   LTLMAG: Multi-Agent LTLf Guidance



Algorithm 1 LTLMAG: Multi-Agent LTLf Planning with Regressor Guidance
  Require: diffusion steps N , agent number Na , guidance signal ξi , regressor neural
  network gϕ (·)
  Initialize τ N ∼ N (0, I)
  for i = N − 1 down to 1 do
     for n = 1 to Na do
        Sample noise ϵ ∼ N (0, I)                  √
        τni−1 ← √1αi τni + (1 − αi ) πθ (τni | zφ ) + 1 − αi ϵ
     end for
      i−1
           ← concat {τni−1 }N     a
                                     
     τall                      n=1
      i−1       i−1           i
     τall  ← τall   + ξi gϕ (τall , zφ , i)
  end for
             0
  return τall



    LTLMAG is used as the multi-agent LTLf Guidance System, which is shown
in Algorithm 1. At the beginning, the diffusion policy starts with Gaussian noise
and gradually improves trajectories in the direction of workable solutions. Next,
to create action trajectories for each agent, LTLMAG uses the conditioned diffu-
sion policy in which sampling is done via an iterative reverse denoising procedure.
A single LTLf specification defines the temporal and coordination constraints of
the task and is shared across all agents. This specification is provided as input to
both the conditioned diffusion policy πθ and a learned regressor network gϕ . The
regressor is trained to approximate the target LTLf satisfaction gradient. Let
gϕ (τt , zφ , t) denote the correction predicted by the regressor, and let g ∗ (τt , zφ )
8      C. Meng and H. Yin

denote the target gradient direction obtained from the satisfaction estimator.
The training loss is defined as


                             2                             2
            Lreg = ∥gϕ − g ∗ ∥2 + 0.01 max 0, ∥gϕ ∥2 − 1        + 0.1Lsat .   (7)

where Lsat is an auxiliary binary cross-entropy loss for predicting LTLf satisfac-
tion when satisfaction labels are available. During the reverse diffusion process,
the output of the regressor neural network and the constant guidance signal ξi
bias the trajectory generation toward satisfying the symbolic task requirements
in the denoising dynamics. Here, ξi is a time-varying guidance weight that con-
trols the strength of LTLf satisfaction guidance at timestep i. By default, the
value is set to 0.1. The guidance follows a linear schedule, with stronger guid-
ance at early timesteps (2ξi ) and weaker guidance at later timesteps (0.1ξi ).
The guidance weight is fixed across agents and tasks, but varies across diffusion
timesteps. Larger values place stronger emphasis on satisfying the LTLf formula,
while smaller values make the sampler rely more on the learned diffusion prior.
Each agent keeps its path and performs local updates using reverse diffusion in-
dependently. The per-agent trajectories are concatenated at each cycle to form
a joint multi-agent trajectory, which represents the clean path predictions of all
agents after local denoising.
    Three key improvements are introduced to LTLDOG-R [5] that enable the
derivation of LTLMAG. First, a conditioned diffusion policy is applied to gen-
erate task-aware trajectories, considering both observations and LTLf embed-
dings through global conditioning. The reason is that unconditional diffusion
policy generates task-agnostic trajectories and depend on external guidance to
enforce coordination, which is unreliable at early denoising stages due to high
noise levels. Conditioning the Diffusion Policy on LTLf embeddings reshapes
the generative prior, steering denoising toward task-consistent and coordinated
trajectories from the outset. This conditioning allows the diffusion policy to in-
ternalize temporal structure during training, reducing the need for strong guid-
ance at inference and improving stability and sample efficiency in long-horizon
multi-agent tasks. Second, the original Graph Convolutional Neural Network
is replaced with a feed-forward neural network for the LTLf regressor, which
is the guidance signal. Since robot trajectories take the form of flattened ac-
tion sequences, multilayer perceptrons appear to be an efficient and effective
method for approximating functions that compute satisfaction scores for trajec-
tory–constraint pairs and their gradient. Third, the algorithm is extended from
single-agent to multi-agent through a two-stage update: per-agent local denois-
ing within each diffusion step, followed by regressor-based guidance applied to
the joint multi-agent trajectory to enforce cross-agent temporal and coordination
constraints. This extension enables coordinated trajectory generation and joint
logic satisfaction across multiple interacting agents. This is because LTLDOG-R
was originally defined for single-agent problems only, LTLMAG algorithm will
support multi-agent problems as demanded within RoboFactory.
                              LTLDiff for Multi-Agent Robotic Manipulation            9

4     Experiment


Table 1. Task success rates (%) across the baseline, LTLDOG-R (LTLR), and LTLDiff
under different dataset sizes.
                                       50 Demos         100 Demos         150 Demos
Task Level Task Name              Base LTLR LTLDiff Base LTLR LTLDiff Base LTLR LTLDiff
1-Agent    Pick Meat               32    65     80   61   82    93     58   76    87
           Stack Cube              17    13      9   38   27    18     44   32    21
           Strike Cube             26    66     80   42   55    64     40   62    75
           Average                 25    48    56    47   55    58     47   57    61
2-Agent    Pass Shoe                9     5     0    20   12      3    12    9      7
           Place Food               5    18     25   23   23    23     20   23    25
           Lift Barrier            24    67     81   60   82    92     58   84    96
           Two Robots Stack Cube   14    22     27   27   32    35     20   48    60
           Average                 13    28    33    33   37    38     28   41    47
3-Agent    Camera Alignment         7    45     56   10   60    73     19   55    67
           Three Robots Stack Cube 8      9     10    2    3      3    22   14      7
           Average                  8    27    33     6   32    38     21   35    37
4-Agent    Take Photo               5     9     12    8   10    12     20   16    24
           Long Pipeline Delivery   0     0      0    0    0      0     0    0      0
           Average                  3     5     6     4    5     6     10    8    12



    The experiments consist of two parts: (i) a comparison of task performance
among LTLDiff, the RoboFactory baseline, and the LTLDOG-R; (ii) an abla-
tion study on the use of LTLf formulas in data generation and diffusion policy
training.

4.1   Comparative Evaluation of LTLDiff and the RoboFactory
      Baseline
Conditioned diffusion policies are trained with egocentric RGB observations in an
offline imitation learning setting. A total of 11 tasks are evaluated; for each task,
policies are trained independently using 50, 100, and 150 expert demonstrations.
The baseline diffusion policy is just a diffusion model. LTLDOG-R uses regressor
guidance and is integrated into multi-agent problems. LTLDiff is improved over
LTLDOG-R, and the improvements are described in Section 3.5. Three policies
are trained under identical training settings, and the comparative results are
reported in Table 1.

Single-agent Tasks. The average task success rate of demos all improved sig-
nificantly over the baseline and the LTLDOG-R. Although the result shows that
the Stack Cube task is particularly challenging, it highlights the difficulty of ac-
curately manipulating objects based solely on visual observations, as well as the
impact of the height of the cube on its bouncing or rolling behavior. However,
LTLDiff performs better as the number of learning demonstrations increases.
This improvement is attributed to LTLf conditioning, which provides appropri-
ate inductive bias even in tasks that require less coordination.
10      C. Meng and H. Yin

Two-agent Tasks. Increases in terms of performance are more evident in the
two-agent tasks. There are marked improvements in the performance on the Lift
Barrier and Two Robots Stack Cube problems in the 150-demo case. On average,
across all two-agent tasks, LTLDiff achieves the highest success rate.


Three-agent Tasks. LTLDiff shows a large improvement in the three-agent
tasks. The average success rate of the 50, 100, and 150 demos increased by 25%,
32%, and 16%, respectively, compared to the baseline.


Four-agent Tasks. Although the average success rate for all demos is higher
than the baseline and the LTLDOG-R, it still remains low due to the complex-
ity of coordinating over a long-term horizon and adhering to overall temporal
constraints. Specifically, the "Long Pipeline Delivery" problem needs the learn-
ing system to maintain consistent temporal dependencies over long-term horizon
constraints, which has been quite challenging for the diffusion-based policy learn-
ing method from demonstrations.
    In conclusion, the results suggest that LTLf conditioning plays a more sig-
nificant role in improving task success than the regressor neural network alone.


4.2   Ablation Study



Table 2. Task success rates (%) for ablation studies of LTLf . The experiment (Gen)
is performed under the same conditions in Section 4.1, but only with LTLf in the data
generation. The experiment (Train) is performed in which all LTLf constraints remain
in diffusion only, and all other setups are the same.

                                         50 Demos 100 Demos 150 Demos
       Task Level Task Name              Gen Train Gen Train Gen Train
       1-Agent    Pick Meat               45 74 72      86    68  80
                  Stack Cube               6   7   10   15    12  20
                  Strike Cube             55 74 52      59    60  69
                  Average                 35 52 45      53    47  56
       2-Agent    Pass Shoe                1   0    5    3    10   7
                  Place Food              15 23 20      22    23  23
                  Lift Barrier            60 75 70      85    75  89
                  Two Robots Stack Cube 18 25 30        33    45  56
                  Average                 24 31 31      36    38  44
       3-Agent    Camera Alignment        10 52 40      67    55  62
                  Three Robots Stack Cube 8    9    1    3     2   7
                  Average                  9  31 21     35    29  35
       4-Agent    Take Photo              6    9    6   11     7  12
                  Long Pipeline Delivery   0   0    0    0     0   0
                  Average                  3   5    3    6     4   6
                              LTLDiff for Multi-Agent Robotic Manipulation        11

    The ablation study examines the importance of LTLf within LTLDiff by ad-
dressing the following questions: (1) What is the importance of LTLf constraints
in the data generation process? (2) What is the importance of LTLf constraints
in diffusion policy training? To answer these questions, two experiments are
conducted, and the results are shown in Table 2.

Importance of LTLf in Data Generation Incorporating LTLf constraints
into data generation captures task-level temporal logic that is difficult to infer
from demonstrations alone. Without constraints from the symbolic environment,
the diffusion policy inherits correlations between actions based solely on feasibil-
ity, resulting in repeated coordination errors in multi-agent settings. For exam-
ple, agents may act asynchronously in parallel tasks (e.g., Camera Alignment)
or execute incorrect action orders (e.g., Stacking tasks), leading to coordination
failures.

Importance of LTLf in Diffusion Policy The diffusion policies are condi-
tioned on LTLf to bias trajectory sampling based on behaviors that satisfy the
desired temporal relationships. Although diffusion models can learn the corre-
lation between local actions, their behavior can become unpredictable with the
increase in task complexity due to the lack of explicit global structure in the task.
This can cause collisions, unnecessary actions, and inefficient synchronization of
the agents, especially in three- and four-agent tasks, as ablation results show a
significant decrease in success rate compared to LTLDiff. The diffusion process is
given a crucial inductive bias through the conditioning of LTLf that favors tem-
poral consistency and coordinated behavior, especially in complex multi-agent
tasks.

5   Conclusion
This work investigates the usage of LTLf in the multi-agent robotic manipula-
tion with regard to learning from demonstrations. Task level constraints are in-
tegrated during the generation of demonstrations. In particular, demonstrations
are generated with the aid of motion planners and LTLf formulas. The demon-
strations are then used to train diffusion policies, which can learn task-level
temporal properties without the need for hard constraint enforcement during ex-
ecution. Based on the experiments conducted on the RoboFactory benchmark,
diffusion policies learned with constraint-aware demonstrations outperformed
diffusion policies on most of the multi-agent manipulation tasks with a high
level of coordination.
    Despite these contributions, LTLDiff still has a limitation: its performance
is poor when processing long-horizon tasks. To solve this problem, in the fu-
ture, incorporate a closed-loop feedback, such as receding horizon control, which
enables the system to continually replan based on real-time observations. This
solution enhances robustness by correcting execution errors and compensating
for state distributions not represented in the demonstration dataset.
12      C. Meng and H. Yin

References
1. Chi, C., Xu, Z., Xu, S., Yu, T., Wang, J., Li, Y.: Diffusion policy: Visuomotor policy
   learning via action diffusion. arXiv preprint arXiv:2303.04137 (2023)
2. Zhao, T.Z., Kumar, V., Levine, S., Finn, C.: Learning fine-grained bimanual ma-
   nipulation with low-cost hardware. arXiv preprint arXiv:2304.13705 (2023)
3. Black, K., Brown, N., Driess, D., Liu, C., Lynch, C., Ryoo, M.S., Levine, S.:
   π0 : A vision-language-action flow model for general robot control. arXiv preprint
   arXiv:2410.24164 (2024)
4. Kim, M.J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov,
   R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake,
   R., Sadigh, D., Levine, S., Finn, C.: OpenVLA: An Open-Source Vision-Language-
   Action Model. arXiv preprint arXiv:2406.09246 (2024)
5. Feng, Z., Luan, H., Goyal, P., Soh, H.: LTLDOG: Satisfying temporally-extended
   symbolic constraints for safe diffusion-based planning. IEEE Robotics and Automa-
   tion Letters 9(10), 8571–8578 (2024)
6. Qin, Y., Kang, L., Song, X., Yin, Z., Liu, X., Liu, X., Zhang, R., Bai, L.: Robo-
   Factory: Exploring Embodied Agent Collaboration with Compositional Constraints.
   arXiv preprint arXiv:2503.16408 (2025)
7. Deshpande, N., Vaidya, A.S., Samant, R.C., Mishra, P., Biradar, V., Keerthi, P.:
   Multi-agent deep reinforcement learning for multi-robot systems: A survey of chal-
   lenges and applications. International Journal of Environmental Sciences 11(4s),
   111–116 (2025)
8. Boldrer, M., Serra-Gomez, A., Lyons, L., Kratky, V., Alonso-Mora, J., Ferranti, L.:
   Rule-based Lloyd algorithm for multi-robot motion planning and control with safety
   and convergence guarantees. arXiv preprint arXiv:2310.19511 (2023)
9. Foead, D., Ghifari, A., Kusuma, M.B., Hanafiah, N., Gunawan, E.: A systematic
   literature review of A* pathfinding. Procedia Computer Science 179, 507–514 (2021)
10. Banerjee, A.S., Choppella, V.: Challenges and Opportunities in the Industrial Us-
   age Controller Synthesis Tools: A Review of LTL-Based Opensource Tools for Au-
   tomated Control Design. Results in Control and Optimization 18, 100511 (2025).
11. Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X.,
   Zhang, S., Liu, J., Awadallah, A.H., White, R.W., Burger, D., Wang, C.: AutoGen:
   Enabling next-gen LLM applications via multi-agent conversation. arXiv preprint
   arXiv:2308.08155 (2023)
12. Huang, J.-t., Li, E.J., Lam, M.H., Liang, T., Wang, W., Yuan, Y., Jiao, W.,
   Wang, X., Tu, Z., Lyu, M.R.: How Far Are We on the Decision-Making of LLMs?
   Evaluating LLMs’ Gaming Ability in Multi-Agent Environments. arXiv preprint
   arXiv:2403.11807 (2024)
13. Dalal, M., Mandlekar, A., Garrett, C., Handa, A., Salakhutdinov, R., Fox, D.:
   Imitating task and motion planning with visuomotor transformers. arXiv preprint
   arXiv:2305.16309 (2023)
14. Janner, M., Du, Y., Tenenbaum, J.B., Levine, S.: Planning with diffusion for flex-
   ible behavior synthesis. In: Proceedings of the 39th International Conference on
   Machine Learning (ICML 2022), pp. 9902–9915. PMLR (2022)
15. Jang, E., Irpan, A., Khansari, M., Kappler, D., Ebert, F., Lynch, C., Levine, S.,
   Finn, C.: BC-Z: Zero-shot task generalization with robotic imitation learning. In:
   Proc. Conf. on Robot Learning (CoRL), pp. 991–1002. PMLR (2022)
16. Chebotar, Y., Vuong, Q., Hausman, K., Xia, F., Lu, Y., Irpan, A., Kumar, A., Yu,
   T., Herzog, A., Pertsch, K., et al.: Q-Transformer: Scalable offline reinforcement
                                     LTLDiff for Multi-Agent Robotic Manipulation             13

   learning via autoregressive Q-functions. In: Proc. Conf. on Robot Learning (CoRL),
   pp. 3909–3928. PMLR (2023)
17. Kurtz, V., Lin, H.: Temporal logic motion planning with convex optimization via
   graphs of convex sets. IEEE Transactions on Robotics 39(5), 3791–3804 (2023)
18. Fainekos, G.E., Kress-Gazit, H., Pappas, G.J.: Temporal logic motion planning for
   mobile robots. In: Proceedings of the IEEE International Conference on Robotics
   and Automation (ICRA 2005), pp. 2020–2025. IEEE (2005)
19. Vaezipoor, P., Li, A.C., Icarte, R.A.T., McIlraith, S.A.: LTL2Action: Generaliz-
   ing LTL instructions for multi-task reinforcement learning. In: Proceedings of the
   38th International Conference on Machine Learning (ICML 2021), Proceedings of
   Machine Learning Research, pp. 10497–10508 (2021)


A      LTLf Formulae

                      Table 3: LTLf formulas for each robotic manipulation task.

Task               Atomic Propositions                   LTL Formula
                   p1 : meat grasped                     G(!p3 − > (!p3 U p1 ))
Pick Meat          p2 : meat lifted                      & G(p1 − > X(Fp2 ))
                   p3 : meat reaches target height       & G(p2 − > Fp3 )
                   p1 : blue cube grasped
                                                         G(!p2 − > (!p2 U p1 ))
                   p2 : blue cube placed on red cube
Stack Cube                                               & G(p1 − > X(Fp2 ))
                   p3 : blue and red cubes aligned
                                                         & G(p2 − > (p3 & p4 ))
                   p4 : blue cube above red cube
                   p1 : hammer identified                G(!p4 − > (!p4 U p1 ))
                   p2 : hammer grasped                   & G(p1 − > X(Fp2 ))
Strike Cube
                   p3 : hammer above cube                & G(p2 − > F(p3 & Fp4 ))
                   p4 : cube struck                      & G(p4 − > p3 )
                   p1 : agent 1 grasps barrier
                                                         G((p1 & p2 )− > p3 )
                   p2 : agent 2 grasps barrier
                                                         & G(!p4 − > (!p4 U p3 ))
Lift Barrier       p3 : both agents grasp barrier
                                                         & G(p3 − > X(F(p4 & p5 )))
                   p4 : barrier reaches target height
                                                         & G(p4 − > p5 )
                   p5 : barrier remains stable
                   p1 : first arm grasps shoe            G(!p4 − > (!p4 U p1 ))
                   p2 : shoe transferred to second arm   & G(p1 − > X(F(p2 & p3 )))
Pass Shoe
                   p3 : second arm grasps shoe           & G((p2 & p3 )− > Fp4 )
                   p4 : shoe reaches target location     & G(p4 − > p3 )
                   p1 : pot lid opened                   G(!p3 − > (!p3 U (p1 | p2 )))
                   p2 : food grasped                     & G((p1 | p2 )− > F(p1 & p2 ))
Place Food
                   p3 : food placed inside pot           & G((p1 & p2 )− > X(F(p3 & p4 )))
                   p4 : food near pot center             & G(p3 − > p4 )
               p1 : blue cube reaches target position
                                                         G(!p3 − > (!p3 U p1 ))
               p2 : red cube grasped
                                                         & G(p1 − > X(Fp2 ))
Two     Robots p3 : red cube placed on blue cube
                                                         & G(p2 − > X(F(p3 & p4 & p5 )))
Stack Cube     p4 : blue and red cubes aligned
                                                         & G(p3 − > (p1 & p4 & p5 ))
               p5 : red cube above blue cube

                   p1 : object reaches target position
                                                         G(!p4 − > (!p4 U (p1 & p2 & p3 )))
                   p2 : camera reaches target height
Camera    Align-                                         & G((p1 & p2 & p3 )− > X(Fp4 ))
                   p3 : agents grasp camera sides
ment                                                     & G(p4 − > (p1 & p2 ))
                   p4 : camera aligned with object
14        C. Meng and H. Yin

Task              Atomic Propositions                   LTL Formula

             p1 : blue cube reaches target position     G(!p3 − > (!p3 U p1 ))
             p : red cube placed on blue cube           & G(p1 − > X(Fp2 ))
Three Robots 2
             p3 : green cube placed on red cube         & G(p2 − > X(F(p3 & p4 )))
Stack Cube
             p4 : stack remains stable                  & G(p3 − > (p2 & p4 ))

                  p1 : object reaches target position
                  p2 : camera reaches target height     G(!p5 − > (!p5 U (p1 & p2 & p3 & p4 )))
Take Photo        p3 : camera aligned with object       & G((p1 & p2 & p3 & p4 )− > X(Fp5 ))
                  p4 : shutter arm near shutter         & G(p5 − > (p1 & p2 & p3 & p4 ))
                  p5 : photo taken
              p1 : first arm grasps shoe                G(!p5 − > (!p5 U p1 ))
              p2 : shoe passed to next arm              & G(p1 − > X(Fp2 ))
Long Pipeline p3 : shoe passed through pipeline         & G(p2 − > X(Fp3 ))
Delivery      p4 : final arm places shoe                & G(p3 − > X(F(p4 & Fp5 )))
              p5 : shoe reaches target location         & G(p5 − > p4 )




B       Task Descriptions

                      Table 4: Task descriptions and target conditions.

Task          Agent          Description                         Target Condition
              Num-
              ber
Pick Meat     1              There is a piece of meat placed The height of the meat reaches
                             on the table. A robotic arm a predefined threshold.
                             picks up the meat and lifts it
                             to a specified height.
Stack         1              A blue cube and a red cube are      The distance between the blue
Cube                         placed on the table. A robotic      and red cubes is within a
                             arm picks up the blue cube and      threshold, with the blue cube
                             places it on top of the red cube.   positioned at a greater height
                                                                 than the red cube.
Strike        1              A hammer and a cube are             The hammerhead is positioned
Cube                         placed on the table. A robotic      directly above the cube within
                             arm first identifies an optimal     a predefined distance thresh-
                             grasping position to pick up the    old.
                             hammer, then moves it to a
                             suitable position to strike the
                             cube.
Lift     Bar- 2              A long barrier is placed on the The barrier is elevated to the
rier                         table. Two robotic arms simul- specified height while main-
                             taneously grasp both ends of taining stability.
                             the barrier and lift it to a spec-
                             ified height.
                          LTLDiff for Multi-Agent Robotic Manipulation             15


Task        Agent   Description                         Target Condition
            Num-
            ber

Pass Shoe   2       A shoe is placed on the ta- The distance between the shoe
                    ble. One robotic arm grasps the and the target location is
                    shoe and passes it to the other within a predefined threshold.
                    one, which then places it at the
                    target location.
Place Food 2        A pot and a kind of food            The food is placed inside the
                    are placed on the table. One        pot, with the distance between
                    robotic arm lifts the pot’s lid,    the food and the center of the
                    while the other picks up the        pot being within a predefined
                    food and places it inside the       threshold.
                    pot.
Two         2       A blue cube and a red cube are      The blue cube is within the
Robots              placed on the table. A robotic      specified threshold distance
Stack               arm picks up the blue cube to       from the target position. The
Cube                a specified position, while the     distance between the blue and
                    other places the red cube on        red cubes remains within a
                    top of it.                          defined threshold, with the red
                                                        cube positioned at a greater
                                                        height than the blue cube.
Camera      3       A camera and an object are          The camera reaches a specified
Alignment           placed on the table. One            height, and the object is placed
                    robotic arm picks up the ob-        at the designated position that
                    ject to a specified position. The   aligns with the camera.
                    other two robotic arms grasp
                    both sides of the camera and
                    align it to the object.
Three       3       A blue cube, a red cube, and        The blue cube is positioned
Robots              a green cube are placed on the      within the specified target
Stack               table. One robotic arm picks up     range. Additionally, the red
Cube                the blue cube to a specified po-    cube is successfully placed on
                    sition. Another arm places the      top of the blue cube, and the
                    red cube on top of the blue one.    green cube is positioned atop
                    The last arm places the green       the red cube.
                    cube on top of the red one.
16      C. Meng and H. Yin


Task        Agent     Description                          Target Condition
            Num-
            ber

Take        4         A camera and an object are           The camera reaches a speci-
Photo                 placed on the table. One             fied height, and the object is
                      robotic arm picks up the object      placed at the designated posi-
                      and places it to a specified posi-   tion that aligns with the cam-
                      tion. Another two robotic arms       era. Additionally, the distance
                      grasp both sides of the camera       between the end effector of the
                      and align it to the object. The      last robotic arm and the cam-
                      last robotic arm clicks the shut-    era’s shutter is within a certain
                      ter.                                 threshold.
Long        4         A shoe is placed on the table. The distance between the shoe
Pipeline              Three robotic arms grasp the and the target location is
Delivery              shoe and pass it to the next within a predefined threshold.
                      robotic arm. The last robotic
                      arm places the shoe to a speci-
                      fied position.
                               LTLDiff for Multi-Agent Robotic Manipulation             17

C   Prompt Template For LTLf


task_description = """
Task: Take Photo
Agent: 4
A camera and an object are placed on the table.
One robotic arm picks up the object and places it
to a specified position. Another two robotic arms
grasp both sides of the camera and align it to the
object. The last robotic arm clicks the shutter.

Target Condition:
The camera reaches a specified height, and the
object is placed at the designated position that
aligns with the camera. Additionally, the distance
between the end effector of the last robotic arm
and the camera’s shutter is within a certain threshold.
"""

system_prompt = """
You are an expert in robotics and formal methods.

Given a task description, produce ONLY valid JSON with the fields:
{
  "task": "<short name of the task>",
  "propositions": [
    "<atomic proposition 1>",
    "<atomic proposition 2>",
    "..."
  ],
  "ltl_formula": "<detailed and structured LTL formula that uses all propositions and
        temporal operators (U, F, G) to encode the task>"
}

The LTL must:
- Use at least one temporal operator for ordering, such as U or G.
- Show conditions before and after the main event.
- Explicitly mention all propositions in the formula.
- Use ! for negation.
- Do not include any text outside the JSON.
- No explanations, no commentary.

Return only the JSON object.
"""
