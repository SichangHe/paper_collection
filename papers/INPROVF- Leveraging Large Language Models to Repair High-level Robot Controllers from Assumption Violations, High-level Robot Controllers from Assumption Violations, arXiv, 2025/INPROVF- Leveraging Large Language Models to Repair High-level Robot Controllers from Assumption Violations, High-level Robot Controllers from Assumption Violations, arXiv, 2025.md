                                                      INPROVF: Leveraging Large Language Models to Repair
                                                      High-level Robot Controllers from Assumption Violations
                                                              Qian Meng∗ , Jin Peng Zhou∗ , Kilian Q. Weinberger, and Hadas Kress-Gazit


                                            Abstract— This paper presents INPROVF, an automatic
                                         framework that combines large language models (LLMs) and
                                         formal methods to speed up the repair process of high-
                                         level robot controllers. Previous approaches based solely on
                                         formal methods are computationally expensive and cannot scale
arXiv:2503.13660v1 [cs.RO] 17 Mar 2025




                                         to large state spaces. In contrast, INPROVF uses LLMs to
                                         generate repair candidates, and formal methods to verify their
                                         correctness. To improve the quality of these candidates, our
                                         framework first translates the symbolic representations of the
                                         environment and controllers into natural language descrip-
                                         tions. If a candidate fails the verification, INPROVF provides
                                         feedback on potential unsafe behaviors or unsatisfied tasks,
                                         and iteratively prompts LLMs to generate improved solutions.          Fig. 1. INPROVF overview. Given a discrete abstraction, a specification,
                                         We demonstrate the effectiveness of INPROVF through 12                and an assumption violation we use LLMs and formal methods to repair
                                         violations with various workspaces, tasks, and state space sizes.     the behaviors of high-level robot controllers under assumption violations.



                                                               I. I NTRODUCTION                                   Recent advances in large language models (LLMs) present
                                            Safety-critical robotic applications, such as autonomous           a unique opportunity to overcome the scalability problem
                                         driving [1], search and rescue missions [2], and assistive            of formal methods-based repair. Modern LLMs, trained
                                         caregiving robots (e.g. [3]), benefit from formal guarantees          on Internet-scale data across diverse domains, have strong
                                         to ensure safe operations and task completions, the lack of           priors and can address complex reasoning tasks–ranging
                                         which may result in harm to users and even loss of life               from competitive mathematics and coding problems to PhD-
                                         in catastrophic events. One way to provide such guarantees            level science questions [10]. Since repairing high-level robot
                                         is the use of formal synthesis—an automatic technique                 controllers under assumption violation is itself a complex
                                         that transforms temporal logic specifications into correct-by-        reasoning task, we aim to leverage the reasoning capacities
                                         construction systems— to create provably correct high-level           of LLMs to scale up repair.
                                         robot controllers that compose low-level robot skills to sat-            In this work, we propose INPROVF, a hybrid framework
                                         isfy temporally extended tasks in complex environments [4].           that combines the strengths of LLMs and formal methods to
                                            Among formal synthesis methods, Generalized Reactiv-               repair assumption violations in high-level robot controllers
                                         ity(1) (GR(1)) synthesis [5] is used in robotics applications         at runtime. We use LLMs to generate repair candidates, and
                                         due to its relatively low polynomial-time complexity with             then verify them through formal methods. If the verification
                                         respect to the state space and its expressivity covering many         fails, we employ formal analysis to provide feedback, which
                                         robotic tasks [6]. A GR(1) specification takes the form of an         is then used by LLMs to iteratively refine the candidates.
                                         implication from assumptions about the environment’s be-                 As illustrated in Fig. 1, INPROVF consists of four
                                         haviors to guarantees on the robot’s behaviors. Specifically,         key steps: Informalization, Repair Prompt, Verification, and
                                         the guarantees depend on the validity of the assumptions;             Feedback. In Informalization, we convert the symbolic ab-
                                         if any assumption is violated at runtime, the synthesized             stractions of both the environment and the synthesized high-
                                         controller is no longer guaranteed to be correct, leading to          level controller into natural languages (NL) descriptions that
                                         potential undesirable behaviors.                                      capture their underlying semantics–specifically, the physical
                                            To address assumption violations, our previous work [7]            meaning of the abstraction and the behavior description of
                                         leverages formal methods-based approaches [8] to repair               the controller (Sec. V-A). Our intuition is that LLMs, primar-
                                         robot behaviors by generating new skills necessary for task           ily trained on natural language data and further fine-tuned
                                         satisfaction following assumption violations. However, our            through reinforcement learning from human feedback [11],
                                         previous repair approach fails to scale to real-world settings        are suitable for processing these informalized NL represen-
                                         with large state spaces at runtime due to the state explosion         tations. Next, in the Repair Prompt step, we assemble the
                                         problem that has challenged formal methods for decades [9].           NL descriptions of the abstractions, the robot’s behaviors,
                                                                                                               the task specifications, and the assumption violations into a
                                           *Equal contribution.
                                           The authors are with Cornell University in Ithaca, NY 14850, USA.   prompt for LLMs to generate repair candidates–new skills
                                         Email: {qm34,jz563,kqw4,hadaskg}@cornell.edu.                         that potentially enable the robot to fulfill its tasks under
the violation (Sec. V-B). To ensure the soundness of the
candidates, the Verification step first checks their syntax
against a predefined grammar, and then check whether the
specification, updated by the violation and the new skills,
is realizable (Sec. V-C). If the verification step fails, the
Feedback step automatically generates NL feedback, through
syntax and counterstrategy analyses, for LLMs to iteratively      Fig. 2. Example 1 from Sec. VC of [7]. Under an unexpected cup status
                                                                  change, the robot creates a new skill (blue arrow) to handle the violation.
generate more promising repair candidates (Sec. V-D).
   Contributions. To our knowledge, INPROVF is the first
framework that leverages LLMs to accelerate the repair
                                                                                          III. P RELIMINARIES
process of assumption violations in large state spaces. By
integrating LLM-based skill generation with verification and      Example 1. Consider a mobile manipulator in a factory-
feedback via formal methods, INPROVF enables provably-            like workspace in Fig. 2. The robot is tasked to move the
correct robotic systems to remain robust in complex, real-        cup between the loading table t2 and the assembly table
world environments with prohibitively large state spaces.         t4 depending on the status of the cup, with the assumption
                                                                  that the status of the cup can only change when it is on the
                    II. R ELATED W ORK                            tables, and the constraint that an empty cup is not allowed
   Synthesis for robots. Synthesis from Linear Temporal           to appear in x0 . However, when the robot holds the cup in
Logic (LTL) and GR(1) specifications operates on a discrete       x2 while executing a skill yoriginal that moves the robot from
abstraction of the environment and the robot’s skills [4].        x4 to x0 via x2 , the cup status changes from full to empty.
The abstraction can be automatically generated from sensor        The robot should create new skills, e.g., the new skill ynew
inputs using, e.g. [12]. Synthesis takes as input a tempo-        indicated by the blue arrow in Fig. 2, that drives the robot
ral logic [13] specification encoding the safety and task         back to x4 . The robot then places the cup to t2 , waits for
requirements for the robot. While traditionally provided by       the cup to be filled up again, and continues the execution.
the user, specifications can also be automatically generated         Abstractions. We model the physical state space with a
from natural language task descriptions using LLMs [14].          discrete abstraction. An abstraction comprises a set of atomic
Synthesis algorithms (e.g. [5]) automatically generate a high-    propositions AP partitioned into environment inputs X and
level controller that composes robot skills to satisfy the        system outputs Y (AP = X ∪ Y). The set of inputs X ,
given specification, thereby providing correctness guarantees,    representing the environment states, is further divided into
assuming the abstraction matches the physical world.              sets of controllable inputs Xc and uncontrollable inputs Xu
   Assumption violations. To address temporary environ-           (X = Xc ∪ Xu ). Controllable inputs Xc represent the part
ment assumption violations, [15] synthesizes robust con-          of the environment that the robot can control indirectly,
trollers that can maintain safety constraints during the vi-      e.g. the position of the robot base. Uncontrollable inputs
olations, while [16] tolerates intermittent violations that       Xu represent the part of the environment that the robot has
occur only a fixed number of times consecutively, separated       no control over, e.g. the position of an obstacle. An input
by violation-free intervals. Cooperative synthesis generates      state σX ⊆ X and a controllable input state σc ⊆ Xc are
controllers that do not attempt to violate assumptions [17].      subsets of inputs and controllable inputs, respectively. Let
For long-lasting violations that make the specifications unre-    the physical state space be X ⊆ Rn . A grounding function
alizable, [18] leverages counterstrategies [19] to generate ad-   G : X → 2X maps each input π ∈ X into a set of physical
ditional assumptions that restore the realizability. Similarly,   states G(π) ⊆ X. Intuitively, the grounding function captures
[15] employs unrealizability analysis [20] to guide the user      the physical meaning of each input.
in adding new liveness assumptions. Our previous work [7]            In Example 1, the inputs are πor ∈ X , where o is an object
utilizes synthesis-based repair [8] to create new robot skills    and r is a region, The grounding function maps each input
to ensure task success given the violations.                      πor to the set of physical states where the object o locates
   LLMs for formal methods. The formal methods commu-             in the region r. An uncontrollable input πempty represents
nity has leveraged LLMs to enhance scalability. [21] employs      that the cup is empty. The input state in Fig. 2 is σX :=
                                                                     x2      ee              x3      t0       t3
LLMs for automated theorem proving, tackling mathematical         {πbase  , πcup , πempty , πcone , πblock , πstone }, meaning the robot
problems that otherwise are computationally intractable and       base is in x2 , the cup is in the end-effector and is empty, the
require human inputs. Similarly, [22] leverages LLMs to           cone is in x3 , the block is in t0 , and the stone is in t3 .
generate program loop invariants–crucial for reasoning about         The system outputs Y represent the robot skills. Each skill
the correctness of programs with loops–and then verify the        has a set of preconditions, may have intermediate states, and
invariants using formal techniques. In symbolic execution,        results in postconditions. Each state is a controllable input
[23] utilizes LLMs to translate path constraints of real-         state. In Example 1, the precondition of the new skill ynew
                                                                        x2      ee      t0
world Python programs into SMT constraints, improving the         is {πbase  , πcup , πblock } (stone and cone are uncontrollable),
                                                                                                     x1      ee     t0
scalability of symbolic execution for complex programs. The       the intermediate state is {πbase       , πcup  , πblock }, and the post-
                                                                                     x4      ee     t0
software engineering community proposes to combine LLMs           condition is {πbase , πcup , πblock }.
and static analysis to identify software security bugs [24].         Specifications. We use the GR(1) fragment of LTL for its
synthesis algorithm and expressivity. The syntax of LTL is                  • Σ is a set of states and Σ0 ⊆ Σ is the set of initial states.
φ := π | ¬φ | φ ∨ φ | ⃝φ | φ Uφ where a formula φ is                        • X and Y are sets of inputs and outputs.
constructed recursively from atomic propositions π ∈ AP,                    • δ : Σ × 2X → Σ is the transition function that maps a
logical operators (¬, ∨), and temporal operators next (⃝)                       state and an input state to the next state.
and until (U). Additional logical operators (∧, →, ↔) and                   • γX : Σ → 2X maps a state to its labeled input state.
temporal operators eventually (♢) and always (□) can be                     • γY : Σ → 2Y maps a state to its labeled output state.
derived from previous operators. The semantics of LTL is
                                                                              A strategy description D for the strategy As is a natural
defined over infinite traces τ = (σ0 , σ1 , . . . ), where each
                                                                           language description of how As would behave.
σi ⊆ AP denotes the set of propositions that are true at
                                                                              If the set of winning states does not overlap with all
step i. When a trace suffix starting at position i satisfies a
                                                                           system liveness goals or does not cover the initial states,
formula φ, we denote this as τ i |= φ. By convention, we
                                                                           a winning strategy for the system does not exist, i.e. the
say that a trace τ satisfies a formula φ, denoted as τ |= φ, if
                                                                           specification is unrealizable. Conversely, a winning strategy
the formula is satisfied from the beginning of the trace (i.e.,
                                                                           for the environment, or a counterstrategy [19], exists.
τ 0 |= φ). The satisfaction relation is defined recursively as
                                                                           Definition 3. A counterstrategy is a nondeterministic finite
follows: τ i |= π if π ∈ σi (π is true at step i); τ i |= ⃝φ if
                                                                           automaton Ae = (Σ, Σ0 , X , Y, δe , δs , γX , γY , γg ) where
τ i+1 |= φ (φ holds at the next step); τ i |= ♢φ if ∃j ≥ i such
that τ j |= φ (φ eventually holds); and τ i |= □φ if ∀j ≥ i,                • Σ, Σ0 , X , Y, γX , γY are the same as in Definition 2.
τ j |= φ (φ always holds). A more detailed introduction of                  • δe : Σ → 2X maps a state to the next input state.
LTL semantics can be found in [13].                                         • δs : Σ × 2X → 2Σ maps a state σ and the next input state
    Specifications in the GR(1) fragment of LTL take the form                   σX to a set of possible next states δs (σ, σX ) ⊆ 2X .
φ = φe → φs where φe = φie ∧ φte ∧ φge represents the                       • γg : Σ → N maps a state σ to the index of a system
environment assumptions and φs = φis ∧ φts ∧ φgs denotes                        liveness goal the state attempts to satisfy.
the system guarantees. The initial constraints φie and φis ,               When synthesis produces a strategy, we deploy the strategy
defined over X and Y, specify the initial conditions of                    on robots as the high-level controller. During the robot exe-
the environment and the system, respectively. The safety                   cution, environment safety assumptions φte may be violated.
constraints, φte and φts , capture conditions that      V must      hold   Definition 4. An assumption violation is a triplet t =
at all times and take the form of φta =                        t
                                                           i □φa,i , for   (σX , σY , σX′
                                                                                          ) such that ∃i, σX ∪ σY ∪ ⃝σX    ′
                                                                                                                               ̸|= φte,i .
a ∈ {e, s}, where φte,i is defined over AP ∪ ⃝X and φts,i                                                 x2    ee    x
                                                                              In Example 1, σX := {πbase , πcup , πcone 3        t0
                                                                                                                             , πblock      t3
                                                                                                                                      , πstone },
over AP ∪⃝AP. Lastly, we have the liveness constraints φge                                           ′
                                                                           σY := {yoriginal }, and σX := σX ∪ {πempty }.
and φgs which encode environment assumptions and system
goals V  that must be satisfied repeatedly. For a ∈ {e, s},                                  IV. P ROBLEM S TATEMENT
φga = i □♢φga,i where each φga,i is defined over AP.                         We tackle the runtime repair problem of high-level robot
    Writing GR(1) specification can be partially automated                 controllers under assumption violations.
from the abstraction (e.g., from topological constraints, skills           Problem 1. Given (i) an abstraction of the environment
definitions, etc), allowing the user to provide the task speci-            X and skills Y, (ii) specifications consisting of a task
fication φtask that captures the essence of the task. We define            specification φtask and a GR(1) specification φ such that
such φtask as a sub-specification of                                                                                                    ′
                                       V φ.                                φtask ⪯ φ, (iii) an assumption violation t = (σX , σY , σX     ),
Definition 1. Let φ = φie ∧ i □φte,i ∧ i □♢φge,i →
                                                       V
                                                                           and (iv) a set of example strategies and their descriptions
                              g
φi ∧ i □φts,i ∧ i □♢φs,i and φtask = φ′ie ∧ i □φ′te,i ∧
        V            V                                      V
Vs                                                                         {(Ais , Di )}ki=1 ; find a set of new skills Ynew that makes the
           ′g     ′i
                       V       ′t
                                     V          ′g
   i □♢φe,i → φs ∧       i □φs,i ∧     i □♢φs,i be GR(1) specifi-          specification φ realizable under the violation t, at runtime.
cations. φtask is a sub-specification of φ, denoted φtask ⪯ φ, if
∀a ∈ {e, s}, φ′ia = φia , {φ′ta,i }i ⊆ {φta,i }i , {φ′g          g                                   V. A PPROACH
                                                     a,i }i ⊆ {φa,i }i .
    In Example 1, an example constraint not included in the                   To address Problem 1 in large state spaces, we propose
task specification φtask but in the full GR(1) specification φ             a hybrid framework INPROVF, as depicted in Fig. 3, that
is: one object cannot appear in two places simultaneously.                 leverages LLMs to efficiently produce new skill candidates,
    Synthesis. GR(1) synthesis [5] first transforms the GR(1)              and formal methods to verify them. We first informalize the
specification into a two-player game between the environ-                  abstraction into the NL description of its physical meaning.
ment and the system, where the transition rules for each                   We then synthesize a strategy from the specification and
player are defined by the safety constraints φte and φts , and the         use few-shot prompting to obtain the NL description of the
winning conditions are defined by the liveness goals φge and               strategy behavior (Sec. V-A). Next, we leverage LLMs to
φgs , respectively. Next, synthesis computes a set of winning              generate a set of new skill candidates that potentially repair
states from which the system is guaranteed to win the game,                the behavior of the strategy under the violation (Sec. V-B).
a process called realizability check. Finally, synthesis extracts          We verify the candidates through syntax and realizability
a finite automaton from the winning states as the robot                    checking (Sec. V-C). If the candidates cannot repair the
strategy.                                                                  violation, we provide feedback on syntax and counterstrategy
Definition 2. A strategy is a deterministic finite automaton               analyses to the LLMs (Sec. V-D). Fig. 4 presents a case study
As = (Σ, Σ0 , X , Y, δ, γX , γY ) where                                    that walks through our framework with Example 1.
                                                                                to only produce a set of new skill candidates Ynew in a
                                                                                predefined domain-specific language (DSL). We also require
                                                                                the new skills to be formatted as JSON files only, and we
                                                                                perform regular expression matching to extract Ynew from the
                                                                                responses. Fig. 4E presents the repair prompt, and Figs. 4F
                                                                                and 4G show two example repair candidates for Example 1.
                                                                                C. Verification
                                                                                   After obtaining a set of new skill candidates Ynew , we ver-
                                                                                ify the correctness of Ynew through syntax and realizability
                                                                                checking, ensuring that Ynew indeed repairs the violation.
                                                                                   Syntax check. We check the syntax of Ynew against the
                                                                                DSL grammar shown in the repair prompt (Fig. 4E). We
                                                                                leverage a parser to automatically transform Ynew into a set
                                                                                of abstract syntax trees (ASTs). If parsing is successful, the
Fig. 3. INPROVF system details. Our system consists of four steps:
Informalization translates formal abstraction and strategy into natural lan-
                                                                                new skills are in the correct syntax. We also ensure type
guage descriptions; Repair leverages LLMs to generate new skill candidates;     correctness by recursively traversing each node of the ASTs,
Verification ensures the correctness of the candidates through syntax and re-   verifying each component of Ynew against its expected type.
alizability checking; Feedback leverages formal analyses to provide concise
NL feedback to assist LLMs for iterative prompting.
                                                                                   Realizability check. Once Ynew is in the correct syntax,
                                                                                we check whether Ynew can repair the assumption violation.
A. Informalization                                                              We use a compiler from [7] to add Ynew to φ and relax
   We begin by leveraging LLMs to translate the environment                     the assumptions in φ that are violated by the violation t =
                                                                                            ′
abstraction and the synthesized strategy into informal natural                  (σX , σY , σX ), resulting in an updated specification φ′ . We
language descriptions. Since LLMs are primarily trained on                      then leverage the realizability check of a GR(1) synthesizer
natural language data and optimized for a wide range of                         Slugs [25] to check the realizability of φ′ . If φ′ is realizable,
reasoning tasks on NL traces, we hypothesize that LLMs                          then Ynew is verified to be sufficient to solve the violation.
better utilize the abstraction and strategy behaviors in natural
                                                                                D. Feedback
languages than in the formal representations.
   Abstraction informalization. We take in an abstraction                          If the new skills Ynew do not pass the verification step,
consisting of the environment inputs X and a grounding                          we provide three types of feedback, each of which targets a
function G that maps each input to a set of physical states.                    different type of error, to ensure that we have informative and
We prompt LLMs to describe the physical meaning of the                          yet concise NL feedback to LLMs for iterative prompting.
abstraction. Fig. 4A presents the prompt, and Fig. 4B shows                        Syntax feedback. For syntax errors detected in the syntax-
the informalized abstraction description for Example 1.                         checking procedure, we provide feedback based on the nodes
   Strategy informalization. Next, we obtain the behavior                       of the ASTs that violate the grammar and the grammar rules
description of the strategy As , synthesized from the GR(1)                     that are violated. For instance, for a new skill ynew ∈ Ynew
specification φ. Since each state of the strategy consists of                   that contains an uncontrollable input πu ∈ Xu in its precon-
environment input propositions, we leverage the previously                      dition, we automatically provide the following feedback: “πu
generated environment abstraction description to provide                        in the precondition of ynew is not a controllable input.”
the context for LLMs to ingest the strategy behavior. Our                          Counterstrategy. Next, if the new skills Ynew are syntac-
preliminary study found that this is a relatively challenging                   tically correct but the updated specification φ′ remains unre-
task due to the complexity of the strategy, which is a finite                   alizable, meaning skills in Ynew do not repair the violation,
automaton as described in Definition 2. So, we use one-shot                     we compute a counterstrategy Ae to provide feedback. While
prompting–including one example translation in the prompt–                      the counterstrategy contains information about the cause of
to help steer LLMs towards generating accurate strategy                         the unrealizability of φ′ , LLMs may not be able to utilize
behavior. Fig. 4C describes the one-shot prompt and Fig. 4D                     the formal representation of the counterstrategy (as shown
shows the resulting strategy behavior for Example 1. Fig. 6A                    in Definition 3). We thus perform formal analysis on the
shows the example translation for Example 1.                                    counterstrategy to transform it into concise NL feedback.
                                                                                   Safety analysis. Given the V counterstrategy Ae and the sys-
B. Repair                                                                       tem safety constraints φts = i □φts,i , we provide feedback
   The repair process takes in the description of the abstrac-                  on if and which skill violates any safety constraint □φts,i . As
tion X , the existing robot skills Y, the task specification                    shown in Algorithm 1, We first identify any transition (σ, σ ′ )
φtask ⪯ φ, provided by the user, that only contains the                         in Ae such that σ ′ is a sink state, i.e. there are no outgoing
essential constraints of the full GR(1) specification φ, the                    edges from σ ′ (Line 1). We are interested in sink states
                                       ′
assumption violation t = (σX , σY , σX   ), and the behavior                    because those are the states where the system has no valid
description D of the strategy As synthesized from φ. We                         next move, indicating states that violate safety constraints.
form a prompt that combines the inputs and asks LLMs                            We then iterate through all system safety constraints □φts,i
    A. Abstraction informalization prompt.                                                    E. Repair prompt.
    You are a researcher in robotics and an expert in formal methods for robotics.            You are a researcher in robotics and an expert in formal methods for robotics.
    You are given an abstraction that contains a set of input propositions X, a               You are given: (1) an abstraction of the physical workspace and objects in the
    physical state space PS \subseteq Rˆn, and a grounding function G: X ->                   workspace, (2) a set of robot skills, (3) a task specification, (4) the original
    2ˆPS that maps each input proposition to a set of physical states. You are                behavior of the synthesized strategy, and (5) a violated observation during the
    asked to explain the physical meaning of the input propositions.                          robot execution. You are asked to provide a set of new skills that along with
    # Input propositions: <Inserted input propositions X >                                    the original skills can allow the robot to recover from the violation and satisfy
    # Grounding: <Inserted grounding function G >                                             the task specification.
    Please only provide a concise, general explanation covering all input propo-              # Abstraction:
    sitions’ physical meaning. Do not provide any examples.                                   ## Input propositions: <Inserted inputs X and informalized abstraction>
    <Informalized abstraction to be returned here>                                            ## Output propositions: <Inserted output propositions Y>
                                                                                              # Task specification:
                                                                                              We use the GR(1) fragment of Linear Temporal Logic to encode the task
    B. Example informalized abstraction description from LLMs.                                specification. The task specification is given in the following JSON file:
    Each input proposition \( p_{o\_r} \) represents the condition that                       <Inserted task specification φtask >
    object \( o \) is located within region \( r \). The grounding function                   # Strategy behavior: <Inserted informalized strategy behavior>
    \( G \) maps each proposition \( p_{o\_r} \) to the set of physical                       # Assumption Violation: During the robot execution, we detect that an
    states where the pose of object \( o \) is in region \( r \). The                         observed transition violates some environment safety assumptions.
    proposition ”empty” signifies the status of the cup, indicating whether it is             ## The violated observation is in the following JSON file:
    empty.                                                                                    <Inserted assumption violation t = (σX , σY , σX       ′
                                                                                                                                                       )>
                                                                                              ## The violated environment safety assumptions are as follows:
    C. Strategy informalization prompt.                                                       <Inserted violated assumptions φviolated >
    You are a researcher in robotics and an expert in formal methods for robotics.            # Returns: After the assumption violation, we relax the violated assumption
    You are given an abstraction of the environment, a set of robot skills, a GR(1)           to include the observed violation transition. You are asked to provide a set
    specification, and its corresponding synthesized strategy. You are asked to               of new skills that, along with the original skills, allow the robot to continue
    describe the behavior of the strategy. I will first give an example of a strategy,        satisfying the task after the assumption violation. Please respond with new
    its behavior description, and its explanation. Then, I will ask you to describe           skills only in the following format:
    the behavior of a different strategy.
                                                                                              ‘ ‘ ‘ JSON
    # Example: <Inserted strategy informalization example (A1s , D 1 ). See
                                                                                              { ” new skill 0 ”: [
    Fig. 6A for the exact text >
                                                                                                               [ <PRECONDITION>,
    # Problem: Now, I will ask you to describe the behavior of a different strategy.
                                                                                                                    [<POSTCONDITION>,             ...]] ,
    You are given: (1) an abstraction of the physical workspace and objects in
                                                                                                               [ <PRECONDITION>,
    the workspace, (2) a set of robot skills, (3) a task specification, and (4) a
                                                                                                                    [<POSTCONDITION>,             ...]] ,
    synthesized robot controller.
                                                                                                               ...] ,
    ## Input propositions: <Inserted inputs X and informalized abstraction>
                                                                                                      ” new skill 1 ”: [
    ## Output propositions: <Inserted output propositions Y>
                                                                                                               [ <PRECONDITION>,
    ## Task specification: We use the GR(1) fragment of Linear Temporal Logic to
                                                                                                                    [<POSTCONDITION>,             ...]    ],
    encode the task specification. The task specification is given in the following
                                                                                                               [ <PRECONDITION>,
    JSON file: <Inserted task specification φtask >
                                                                                                                    [<POSTCONDITION>,             ...]] ,
    ## Strategy: We represent the robot strategy synthesized from the specification
                                                                                                               ...] ,
    as a finite state automaton. For each node, ’rank’ represents which liveness
                                                                                                      ...}
    goal the node is trying to satisfy, ’state’ represents the value of each variable in
                                                                                              ‘‘‘
    the state, in the order of the field ’variables’, and ’trans’ represents the possible
    successor states. The strategy is in the JSON file: <Inserted strategy As >               The response follows the grammar:
    Please describe the behavior of the synthesized strategy only. Do not provide
    any explanation: <Informalized strategy behavior to be returned here>                     <new_skill>: [<intermediate_transition>+]
                                                                                              <intermediate_transition> = [<precondition>,
                                                                                                                          [<postcondition>+]]
    D. Example informalized strategy behavior from LLMs.                                      <precondition> = [<controllable_input>+]
    The synthesized strategy behaves as follows:                                              <postcondition> = [<controllable_input>+]
    Initially, the robot’s base is at position x4, the cup is at location t2, the block
    is at location t1, the cone is at x3, the stone is at t0, and the cup is empty.           Each pre or post-condition in the new skills should be a complete controllable
    When the cup becomes **not empty**, the robot executes **skill4** to pick                 input state. Do not include original skills in the new skills. Do not include
    up the block from t1 and then **skill7** to place the block at t3. Next, the              any comments in skills. <New skill candidates to be returned here>
    robot uses **skill2** to pick up the cup from t2. It then executes **skill1**
    to move from x4 via x2 to x0 while holding the cup. At x0, the robot uses
    **skill6** to place the cup on the table.                                                 F. Example new skill candidates that violate safety constraints.
    When the cup becomes **empty** again, the robot executes **skill3** to
                                                                                              ‘ ‘ ‘ JSON
    pick up the cup from the table. It then uses **skill0** to move from x0 via
                                                                                              {       ” new skill 0 ”: [
    x2 to x4 while holding the cup. At x4, the robot executes **skill5** to place
                                                                                                          [[” p base x2 ” ,      ” p cup ee ”] ,
    the cup back at t2.
                                                                                                          [[” p base x3 ” ,      ” p cup ee ” ] ] ] ,
    This behavior repeats indefinitely, with the robot moving the cup between t2
                                                                                                          [[” p base x3 ” ,      ” p cup ee ”] ,
    and the table whenever the cup transitions between empty and not empty.
                                                                                                          [[” p base x4 ” ,      ” p cup ee ”]]]]}
                                                                                              ‘‘‘
    G. Example new skill candidates that cannot satisfy liveness constraints.
                                                                                              Feedback from safety analysis: new skill 0 violates the hard constraints
    ‘ ‘ ‘ JSON                                                                                !(p base x3’ & p cone x3’)
    {       ” new skill 0 ”: [
                 [[” p base x2 ” , ” p cup ee ” , ” p block t3 ”] ,
                 [[” p base x4 ” , ” p cup ee ” , ” p block t3 ”]]]]}
    ‘‘‘
    Feedback from liveness analysis: The new skills cannot satisfy the liveness
    goals ( empty -> p cup t2 )


Fig. 4. Case study for Example 1. (A)-(D) describe the prompts and LLM responses from informalization. (E)-(G) present the repair prompt and two
                                                                                                                                     region
sets of new skill candidates from LLMs, along with the feedback from formal analyses. We use p object region to represent the input πobject and prime
(’) for the next operator (⃝), following the syntax of GR(1) formulas in Slugs [25].

(Line 2), and check whether the transition violates any safety                              safety constraint of interest, and then leveraging an SMT
constraint (Line 3). We perform this check by formulating                                   solver Z3 [26] to check the satisfiability of the conjunction,
a conjunction of the labels of σ, the labels of σ ′ , and the                               as done in [20]. If the constraint □φts,i is violated, we provide
 Algorithm 1: Safety Analysis                                            Algorithm 2: Liveness Analysis
  Input: Counterstrategy         Ae , System safety constraints           Input: Counterstrategy      Ae , Liveness goals
             φts = i □φts,i                                                       φgs = n            g
                     V                                                                   V
                                                                                            i=1  □♢φ s,i
  Output: NL feedback on violated safety constraints                      Output: NL feedback on unsatisfied liveness goals
             ′                    ′
1 for σ, σ ∈ Σ such that σ ∈ δs (σ, δe (σ)) and                         1 SCCs := find strongly connected components(Ae );
   δs (σ ′ , δe (σ ′ )) = ∅ do                                          2 for S ∈ SCCs do
2      for □φts,i in φts do                                             3     if (∀σ ∈ S, ̸ ∃σ ′ ̸∈ S.σ ′ ∈ δs (σ, δe (σ))) ∧ (∃σ ∈
3             if γX (σ) ∪ γY (σ) ∪ ⃝(γX (σ ′ ) ∪ γY (σ ′ )) ̸|= φts,i           S.δs (σ, δe (σ)) ̸= ∅) then
                then                                                    4          L := {i | ∃σ, σ ′ ∈ S.σ ′ ∈ δs (σ, δe (σ)), γg (σ) ≤
4                   yield to feedback: “skills in γY (σ) violate the                 i < γg (σ ′ ) mod n};
                      hard constraints □φts,i .”                        5          L′ := {i | ∃σ ∈ S.γg (σ) = i} \ L ;
                                                                        6          return “The new skills cannot satisfy liveness
                                                                                     goals {□♢φgs,i | i ∈ L′ } after satisfying liveness
                                                                                     goals {□♢φgs,i | i ∈ L}.”
the following NL feedback: “the skills in γY (σ) violate
the safety constraint □φts,i ” (Line 4). Fig. 4F presents an
example safety analysis feedback for Example 1.
   Liveness analysis. Given V   the counterstrategy Ae and the
                                  n
system liveness goals φgs = i=1 □♢φgs,i , we provide feed-
back on which liveness goals are not satisfied given the new
skills. Algorithm 2 describes our approach. We first leverage
Tarjan’s algorithm [27] to identify a set of strongly connected
sets in the nodes Σ of Ae (Line 1). We then only consider               Fig. 5. Example workspace. Left: An apartment-like workspace where a
the sinking ones, i.e. there is no outgoing edge towards                mobile manipulator performs laundry tasks. Right: An emergency room-like
                                                                        workspace where a robot swarm performs patrolling tasks.
other components, and are not singletons without transitions
(Line 3). Thus, we identify a sinking strongly connected                    the status of a cup changes (Example 1), and factory-
component that can trap the robot within it once any state of               stone where a static obstacle stone unexpectedly moves.
the component is reached. We then identify the indices of a                 Detailed descriptions can be found in Sec. VC of [7].
set of liveness goals L satisfied in the component (Line 4).             • Large. A larger version of the factory example with
We note that the inequality comparisons are modulo n (where                 additional regions surrounding the workspace in Fig. 2,
n ∈ N is the total number of system liveness goals arranged                 increasing the number of input propositions from 29
in a cyclic order); that is, the condition γg (σ) ≤ i < γg (σ ′ )           to 71. The three violations, large-cone, large-cup, and
mod n in Line 4 means that γg (σ) ≤ i < γg (σ ′ ) if γg (σ) ≤               large-stone, are the same as those in the factory example.
γg (σ ′ ), and (γg (σ) ≤ i ≤ n) ∨ (1 ≤ i < γg (σ ′ )) if γg (σ) >
                                                                         • Laundry. A mobile manipulator is responsible for laun-
γg (σ ′ ). Next, we obtain the indices of another set of liveness
                                                                            dry tasks in an apartment-like workspace (Fig. 5 left).
goals L′ that the robot attempts to, but cannot, satisfy in
                                                                            In the violation laundry-box, an obstacle box blocks the
the component (Line 5). Lastly, we provide feedback which
                                                                            path to a folding table. In the violation laundry-pick, the
states that the robot cannot satisfy the liveness goals in L′
                                                                            skill that picks up a cloth fails, and the robot should
after satisfying L (Line 6). Fig. 4G presents an example
                                                                            attempt to pick up another cloth instead. In the violation
feedback from liveness analysis for Example 1.
                                                                            laundry-fold, a folding table is malfunctioning, and the
   Both the safety and liveness analyses have computation
                                                                            robot should use another folding table instead.
complexity O(|Σ|2 ) since they only access each state and
                                                                         • ER. A swarm of robots is in an emergency room (ER)-
transition of the counterstrategy at most a finite number of
                                                                            like workspace (Fig. 5 right). In the violation ER-skill, a
times. Our feedback allows LLMs to correct their mistakes
                                                                            low-level controller failure causes some robots to enter
and generate more promising repair candidates.
                                                                            an undesired region. In the violation ER-patient, a patient
                          VI. E XAMPLES                                     enters the ER unexpectedly, requiring the swarm to visit
                                                                            the ER in response. In the violation ER-operate, a patient
  Our examples aim to explore the following questions:
                                                                            appears in an operation room unexpectedly, forcing the
Q1. Does INPROVF repair violations more efficiently than                    swarm to patrol other operation rooms instead.
     the state-of-the-art formal-methods-based approach?                   Informalization examples. For strategy informalization
Q2. How does each component (informalization, feedback)                 (Sec. V-A), we use an example in Fig. 6A for object-centric
     contribute to the overall performance of INPROVF?                  abstraction and the one in Fig. 6B for swarm abstraction.
  Examples. We evaluate 12 violations in four workspaces                   Baseline and Ablations. Our previous work [7] provides
over two abstraction types (object-centric and swarm [28]).             a synthesis-based baseline that modifies the pre and post-
 • Factory. A mobile manipulator operates in a factory-like             conditions of existing skills to suggest new skills that repair
   workspace (Fig. 2). During the execution, the robot en-              the violations. We also consider two ablations of INPROVF:
   counters three violations: factory-cone where an obstacle            no-inform where we do not perform informalization and
   cone moves to the front of the robot, factory-cup where              instead directly include the abstraction and strategy in the
                                                                                                                        TABLE I
    A. Strategy informalization example for object-centric abstraction.                I NFORMALIZATION AVERAGE RUNTIME WITH STANDARD DEVIATION ( S )
    Inputs: [”p base x0”, ”p base x1”, ”p base x2”, ”p base x3”]
    Outputs: [”skill0”, ”skill1”]
    Task specification and strategy: <omitted for space >                                              Abstraction-inform      Synthesis   Strategy-inform
    Behavior: Initially, the robot’s base is in x0, and the liveness goal                  Factory       16.32 ± 6.91        1.94 ± 0.58   65.79 ± 29.11
    ‘p base x0‘ which requires the base to repeatedly reach x0 is satisfied. The            Large       16.14 ± 10.78       90.43 ± 3.48   44.46 ± 12.09
    robot then executes skill0 to move to x1 and then x3, satisfying the liveness          Laundry       17.83 ± 7.78       24.81 ± 2.83   42.99 ± 12.03
    goal ‘p base x3‘ which requires the base to repeatedly reach x3. Next, the               ER          10.17 ± 4.64        1.79 ± 0.03    27.63 ± 8.60
    robot executes skill1 to move back to x0 via x1, satisfying the liveness goal
    ‘p base x0‘ again. This behavior continues indefinitely.
    Explanation: ”Initially, the robot’s base is in x0, and the liveness goal          s). However, for the three larger examples (64-79 variables),
    ‘p base x0‘ which requires the base to repeatedly reach x0 is satisfied”
    corresponds to node 0. ”The robot then executes skill0 to move to x1 and           INPROVF significantly outperforms the baseline. In these
    then x3, satisfying the liveness goal ‘p base x3‘ which requires the base to       larger cases, the baseline fails to complete within the 3000-
    repeatedly reach x3” corresponds to the transitions from node 0 to node 1,
    node 2, node 3, and then node 4. ”Next, the robot executes skill1 to move          second time limit. We also remove the time limit for the
    back to x0 via x1, satisfying the goal ‘p base x0‘ again” corresponds to the       larger-cup violation, but the baseline does not terminate after
    transitions from node 4 to node 5, node 6, node 7, and then back to node 0.
                                                                                       18523.93 s, eventually causing a machine out-of-memory
    B. Strategy informalization example for swarm abstraction.
                                                                                       crash. In contrast, for these larger examples, within five
    Inputs: [”p swarm x0”, ”p swarm x1”, ”p swarm x2”, ”p swarm x3”]                   iterations, INPROVF successfully repairs every violation
    Outputs: [”skill0”, ”skill1”, ”skill2”, ”skill3”]
    Task specification and strategy: <omitted for space >
                                                                                       except one in a single run; the failed run is for the laundry-
    Behavior: Initially, the robot swarm is in x0 and the liveness goal                fold violation. These results indicate that INPROVF is more
    ‘p swarm x0 & !p swarm x1 & !p swarm x2 & !p swarm x3‘ which re-
    quires the swarm to repeatedly stay in x0 only is satisfied. The swarm
                                                                                       scalable and efficient than the baseline in large state space
    then executes skill0 to reach x1 and x2, and then executes skill1 to reach         (Q1). Our ablation studies show that INPROVF achieves a
    x3, satisfying the goal ‘p swarm x3 & !p swarm x0 & !p swarm x1 &
    !p swarm x2‘ which requires the swarm to repeatedly stay in x3 only. Next,
                                                                                       higher success rate (97.22%) than no-inform (55.56%) and
    the robot executes skill2 to move to x1 and x2, and finally executes skill3 to     no-feedback (72.22%). Additionally, in the successful runs,
    reach x0, satisfying the first goal again. This behavior continues indefinitely.
    Explanation: ”Initially, the robot swarm is in x0 and the liveness goal
                                                                                       the runtime for no-inform is on average 7.43% higher than
    ‘p swarm x0 & !p swarm x1 & !p swarm x2 & !p swarm x3‘ which re-                   that of INPROVF. These results suggest both informalization
    quires the swarm to repeatedly stay in x0 only is satisfied” corresponds
    to node 0 and 1. ”The swarm then executes skill0 to reach x1 and x2”
                                                                                       and feedback are critical for INPROVF to achieve high
    corresponds to the transitions from node 1 to node 2, node 2 to node 3             performance in runtime repair (Q2).
    or node 4, and node 3 or node 4 to node 5 and then node 6. ”and then
    executes skill1 to reach x3, satisfying the goal ‘p swarm x3 & !p swarm x0
    & !p swarm x1 & !p swarm x2‘ which requires the swarm to repeatedly                              VII. L IMITATIONS AND C ONCLUSION
    stay in x3 only” corresponds to the transitions from node 6 to node 7, and
    then node 8 or node 9, and then node 10. ”Next, the robot executes skill2             We present INPROVF, a novel hybrid framework that
    to move to x1 and x2” corresponds to the transitions from node 10 to node          combines the scalability of LLMs and the guarantees of for-
    11 or node 12, and then to node 13, node 14, and node 15. ”and finally
    executes skill3 to reach x0, satisfying the first goal again” corresponds to       mal methods to efficiently repair high-level robot controllers
    the transitions from node 15 to node 16 or node 17, and then to node 0.            under assumption violations at runtime with prohibitively
                                                                                       large state space. Our experiments across various state space
Fig. 6. Strategy informalization examples. Example translations from                   sizes indicate that our approach outperforms the formal
strategy to its behavior used to form the strategy informalization prompt
(Fig. 4C). (A) is for object-centric examples, and (B) for the swarm example.
                                                                                       methods-based approach in settings with large state spaces.
                                                                                          Nonetheless, our evaluation faces several limitations. First,
repair prompt; and no-feedback, where we perform the                                   since there is no standard benchmark for runtime repair, our
iterative prompting without feedback from formal analyses.                             evaluation instances are limited. In future work, we plan to
   Setup. We run our experiments on a Linux machine with a                             leverage LLMs to procedurally generate a diverse range of
2.3GHz 8-core AMD RyzenTM -7 CPU. We use OpenAI o1-                                    repair instances across various abstraction types for a more
preview-2024-09-12 as the LLM for INPROVF. We measure                                  comprehensive evaluation. Moreover, the formal-methods-
runtime in seconds. We set the runtime limit to 3000 seconds.                          based repair executes on CPUs, and its implementation has
For INPROVF and its ablations, we set a maximum limit for                              not been optimized, while the LLM components of IN-
feedback iteration to be 5 for monetary cost control of LLMs.                          PROVF run on GPUs and benefit from extensive engineering
We run 5 trials with different random seeds for the baseline                           optimizations. Thus, a direct runtime comparison may not be
and 3 trials for INPROVF and its ablations for each violation.                         fair. Future work will focus on developing evaluation metrics
   Results. Fig. 7 presents the success rates and the runtime                          that better account for the hardware disparities. Finally,
comparison for the successful trails. For INPROVF and its                              we currently assess the quality of informalization indirectly
ablations, we also show the detailed runtime breakdown of                              through the final repair correctness, which is neither sound
each key component. We do not include the runtime for infor-                           nor complete. Future work will explore automatic evaluation
malization in Fig. 7 because we only perform informalization                           methods that directly measure the quality of informalization.
once offline for each example; other violations under the                              Additionally, we will work on further improving the scala-
same example can reuse the informalization results. Table I                            bility of formal methods components within our framework,
shows the average runtime and standard deviation for each                              such as realizability check.
informalization component over three trials per example.
   Analysis. In the factory example with a small state space                                                  ACKNOWLEDGMENTS
(37 variables), the average runtime of formal-methods-based                              We thank Lin Luan for her invaluable assistance in enhanc-
baseline (144.05 s) is comparable to that of INPROVF (92.36                            ing the visual presentation of Figs. 1, 3, and 5, Kevin Guan
Fig. 7. Main results. Success rates and runtime comparison among of baseline, INPROVF, and ablation studies (no-inform and no-feedback). The success
rates n/m represents n successful runs in m total runs. We only show the runtime for the successful runs, including the detailed runtime breakdown of
various components. Each error bar shows the standard deviation of the total runtime for each violation and configuration.

for his insightful discussion on the design of the experiments                 [12] G. Konidaris, L. P. Kaelbling, and T. Lozano-Perez, “From skills
in Sec. VI, Bo-Ruei Huang and Andrew Violette for their                             to symbols: Learning symbolic representations for abstract high-level
                                                                                    planning,” Journal of Artificial Intelligence Research, vol. 61, pp. 215–
insightful discussion on the ER example (Fig. 5 right), and                         289, 2018.
anonymous reviewers from ICLR 2025 VerifAI Workshop                            [13] E. Clarke, O. Grumberg, and D. Peled, Model Checking. The MIT
for their detailed and insightful comments.                                         Press, 2000.
                                                                               [14] Y. Chen, R. Gandhi, Y. Zhang, and C. Fan, “Nl2tl: Transforming
                             R EFERENCES                                            natural languages to temporal logics using large language models,” in
                                                                                    Proceedings of the 2023 Conference on Empirical Methods in Natural
 [1] E. Yurtsever, J. Lambert, A. Carballo, and K. Takeda, “A survey of             Language Processing, pp. 15880–15903, 2023.
     autonomous driving: Common practices and emerging technologies,”          [15] K. W. Wong, R. Ehlers, and H. Kress-Gazit, “Resilient, provably-
     IEEE access, vol. 8, pp. 58443–58469, 2020.                                    correct, and high-level robot behaviors,” IEEE Transactions on
 [2] M. Lyu, Y. Zhao, C. Huang, and H. Huang, “Unmanned aerial vehicles             Robotics, vol. 34, no. 4, pp. 936–952, 2018.
     for search and rescue: A survey,” Remote Sensing, vol. 15, no. 13,        [16] R. Ehlers and U. Topcu, “Resilience to intermittent assumption viola-
     p. 3266, 2023.                                                                 tions in reactive synthesis,” in Proceedings of the 17th International
 [3] R. Madan, S. Valdez, D. Kim, S. Fang, L. Zhong, D. T. Virtue, and              Conference on Hybrid Systems: Computation and Control (HSCC),
     T. Bhattacharjee, “Rabbit: A robot-assisted bed bathing system with            pp. 203–212, 2014.
     multimodal perception and integrated compliance,” in Proceedings          [17] R. Ehlers, R. Könighofer, and R. Bloem, “Synthesizing cooperative
     of the 2024 ACM/IEEE International Conference on Human-Robot                   reactive mission plans,” in 2015 IEEE/RSJ International Conference
     Interaction, pp. 472–481, 2024.                                                on Intelligent Robots and Systems (IROS), pp. 3478–3485, IEEE, 2015.
 [4] H. Kress-Gazit, M. Lahijanian, and V. Raman, “Synthesis for robots:
                                                                               [18] R. Alur, S. Moarref, and U. Topcu, “Counter-strategy guided refine-
     Guarantees and feedback for robot behavior,” Annual Review of
                                                                                    ment of gr (1) temporal logic specifications,” in 2013 Formal Methods
     Control, Robotics, and Autonomous Systems, vol. 1, pp. 211–236,
                                                                                    in Computer-Aided Design, pp. 26–33, IEEE, 2013.
     2018.
 [5] R. Bloem, B. Jobstmann, N. Piterman, A. Pnueli, and Y. Sa’ar,             [19] R. Könighofer, G. Hofferek, and R. Bloem, “Debugging formal
     “Synthesis of reactive (1) designs,” Journal of Computer and System            specifications using simple counterstrategies,” in 2009 Formal Methods
     Sciences, vol. 78, no. 3, pp. 911–938, 2012.                                   in Computer-Aided Design, pp. 152–159, IEEE, 2009.
 [6] C. Menghi, C. Tsigkanos, P. Pelliccione, C. Ghezzi, and T. Berger,        [20] V. Raman and H. Kress-Gazit, “Towards minimal explanations of
     “Specification patterns for robotic missions,” IEEE Transactions on            unsynthesizability for high-level robot behaviors,” in 2013 IEEE/RSJ
     Software Engineering, vol. 47, no. 10, pp. 2208–2224, 2019.                    International Conference on Intelligent Robots and Systems (IROS),
 [7] Q. Meng and H. Kress-Gazit, “Automated Robot Recovery from                     pp. 757–762, IEEE, 2013.
     Assumption Violations of High-Level Specifications,” in 2024 IEEE         [21] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik,
     20th International Conference on Automation Science and Engineering            T. Lacroix, Y. Wu, and G. Lample, “Draft, Sketch, and Prove: Guid-
     (CASE), pp. 4154–4161, IEEE, Aug. 2024.                                        ing formal theorem provers with informal proofs,” in International
 [8] A. Pacheck and H. Kress-Gazit, “Physically feasible repair of reactive,        Conference on Learning Representations, 2023.
     linear temporal logic-based, high-level tasks,” IEEE Transactions on      [22] M. A. Pirzada, G. Reger, A. Bhayat, and L. C. Cordeiro, “Llm-
     Robotics, 2023.                                                                generated invariants for bounded model checking without loop un-
 [9] A. Valmari, “The state explosion problem,” in Advanced Course on               rolling,” in Proceedings of the 39th IEEE/ACM International Confer-
     Petri Nets, pp. 429–528, Springer, 1996.                                       ence on Automated Software Engineering, pp. 1395–1407, 2024.
[10] OpenAI, “Learning to reason with LLMs,” 2024.                             [23] W. Wang, K. Liu, A. R. Chen, G. Li, Z. Jin, G. Huang, and L. Ma,
[11] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin,             “Python symbolic execution with LLM-powered code generation,”
     C. Zhang, S. Agarwal, K. Slama, et al., “Training language models              arXiv preprint arXiv:2409.09271, 2024.
     to follow instructions with human feedback,” Advances in neural           [24] Z. Li, S. Dutta, and M. Naik, “Llm-assisted static analysis for detecting
     information processing systems, vol. 35, pp. 27730–27744, 2022.                security vulnerabilities,” arXiv preprint arXiv:2405.17238, 2024.
[25] R. Ehlers and V. Raman, “Slugs: Extensible GR(1) synthesis,” in
     Computer Aided Verification: 28th International Conference, CAV
     2016, Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part II
     28, pp. 333–339, Springer, 2016.
[26] L. De Moura and N. Bjørner, “Z3: An efficient SMT solver,” in
     International Conference on Tools and Algorithms for the Construction
     and Analysis of Systems, pp. 337–340, Springer, 2008.
[27] R. Tarjan, “Depth-first search and linear graph algorithms,” SIAM
     journal on computing, vol. 1, no. 2, pp. 146–160, 1972.
[28] S. Moarref and H. Kress-Gazit, “Automated synthesis of decentralized
     controllers for robot swarms from high-level temporal logic specifica-
     tions,” Autonomous Robots, vol. 44, no. 3, pp. 585–600, 2020.
