                                  Highlights
                                  LLM-based Framework for Generating and Verifying Parallel DEVS Statecharts
                                  Vamsi Krishna Vasa, Hessam S. Sarjoughian, Edward J. Yellig


                                         • Large Language Models (LLMs) have been leveraged in an agentic framework for developing Parallel DEVS
                                           (PDEVS) statecharts in two stages: i) Generated PDEVS plausible facts (natural language representation of
                                           PDEVS specifications) and ii) Using the facts and PDEVS schema to generate PDEVS statecharts.
                                         • Logical inaccuracies in plausible facts result in inaccurate statecharts. The proposed framework generates
                                           behavior conditions, converts them into propositional logic, and verifies the plausible facts using logical
                                           entailment. The methodology includes a controlled-correction mechanism for verifying (re)generated facts.

                                         • The verification mechanism is evaluated from completeness and correctness aspects. Model checking using
                                           Timed Automata variants of the PDEVS statecharts shows the improvement in properties such as deadlock and
                                           phase reachability. A quantitative scoring is provided to evaluate the correctness of the generated statecharts.
arXiv:2608.14956v1 [cs.LG] 15 Aug 2026




                                         • Experimental evaluation of the PDEVS statecharts using multiple publicly available (small, large, instruction-
                                           tuned, and reasoning-oriented) LLMs shows the generalizability of the developed framework and methodology.
LLM-based Framework for Generating and Verifying Parallel
DEVS Statecharts
Vamsi Krishna Vasaa , Hessam S. Sarjoughiana,∗ and Edward J. Yelligb
a Arizona State University, Tempe, Arizona, USA
b Intel Corporation, Chandler, Arizona, USA



ARTICLE INFO                                      ABSTRACT
Keywords:                                         The development of models demands sound modeling and simulation knowledge as well as
Behavioral Modeling                               domain knowledge. Every model should accurately represent a system’s dynamics and be
Parallel DEVS Statecharts                         verifiable. Toward this objective, this research introduces an agentic PDEVS-LLM framework to
Large Language Models                             assist human modelers in generating and verifying PDEVS statecharts for behavior modeling of
Boolean Logic Entailment                          atomic Parallel Discrete Event System Specification (PDEVS) models. The framework supports
Model Checking                                    (re)generating plausible facts from a system description prompt using the agentic LLM used for
                                                  generating plausible facts. Inconsistencies in plausible facts lead to incorrect PDEVS statecharts
                                                  having logical structure and behavioral inaccuracies. A controlled-correction mechanism is
                                                  developed to verify the logical consistency of the plausible facts. The agentic LLM is used to
                                                  generate key behavioral conditions from the system description prompt. The plausible facts are
                                                  then verified against the behavioral conditions using propositional logic entailment for a finite
                                                  number of times. The verification results enable the generation of modification prompts that can
                                                  reduce errors in generated plausible facts, resulting in more accurate PDEVS statecharts. To
                                                  verify a statechart’s logical correctness, its Timed Automata counterpart is manually created
                                                  and verified for deadlock and reachability properties. The human modeler may regenerate
                                                  plausible facts and PDEVS statecharts iteratively and incrementally. A basic correctness metric
                                                  is introduced to quantify the completeness and accuracy of the expected behavioral traits of the
                                                  PDEVS statechart models. A collection of example systems with varying levels of complexity
                                                  is developed to demonstrate the capabilities and limitations of LLMs. The evaluation of the
                                                  proposed verification mechanism shows a substantial improvement in the logical consistency of
                                                  generated statecharts.




1. Introduction
    A conceptual system description is the first artifact for creating a simulatable model. It should convey a notional
understanding of the system and its anticipated simulated behavior. To specify a system, modelers must also understand
the concepts and methods of modeling languages in order to identify and formalize its combined structural and
behavioral aspects. In this regard, Large Language Models (LLMs) with appropriate capabilities and knowledge can
support the development of simulation models. Natural Language Processing (NLP) has been proposed for generating
formal models from textual descriptions (Liu, Yang, Schornstein, Liang, Idrees, Tellex and Shah, 2022). Similar to
many scientific domains, Machine Learning is expected to aid the modeling, simulation, and experimentation lifecycle.
However, it is challenging to generate correct simulation models from conceptual system descriptions using machine
learning . Models must be based pn sound modeling principles, grounded in modeling formalisms, and implementable
in simulators.
    Machine learning is becoming integral to modeling and simulation due to continuing advances in transformer-
based agentic frameworks. They can generate input/output state-based models directly from system descriptions.
These frameworks aim to produce models that are capable of accurately simulating time-indexed behaviors. An early
effort uses GPT-3 Codex framework to generate code given a textual prompt describing a first-in-first-out inventory
model(Jackson, Saenz and Ivanov, 2024). GPT-4 provided with a Classic DEVS modeling grammar, simple system
prompts, and Co-Pilot is also used to generate simulatable code (Carreira-Munich, Paz-Marcolla and Castro, 2024).
Customized GPT-4 is proposed for generating activity-based models using its metamodel with textual system prompts
(Alshareef, Keller, Carbo and Zeigler, 2024). An LLM-based agentic framework (Vasa, Sarjoughian and Yellig, 2025)
    ∗ Corresponding author

        vvasa1@asu.edu (V.K. Vasa); hessam.Sarjoughian@asu.edu (H.S. Sarjoughian); edward.j.yellig@intel.com (E.J. Yellig)
     ORCID (s):


: Preprint submitted to Elsevier                                                                                                   Page 1 of 21
is also developed for generating models using grammars for the PDEVS formalism (Chow and Zeigler, 1994) and
PDEVS statecharts (Fard and Sarjoughian, 2015). The basis of this approach is generate plausible facts which underpin
the LLM-based generation of statecharts. Such approaches require expert modelers to examine the correctness and
viability of generated models and code.
    Increasing behavioral complexity often introduces logical misalignments with the original conceptual system
description. This results in manually finding and correcting model inconsistencies. To address this need, a verification
mechanism based on Boolean propositional logic is proposed for PDEVS-LLM Vasa et al. (2025) to aid in correcting
plausible PDEVS specifications. Such a mechanism aids in generating PDEVS statecharts that can be logically
represent the system description. Consequently, this research proposes a incremental and iterative mechanism to
refine the PDEVS plausible facts, thereby improving the logical alignment of plausible facts with respect to the
system prompt. The proposed framework uses the system descriptions to identify the behavioral conditions that the
plausible facts are expected to satisfy. Both the specifications of the plausible facts and behavioral conditions are
translated into propositional logic for satisfiability and entailment-based verification. The verification outcomes are
then used to regenerate the plausible facts, forming a controlled-correction loop to arrive at more accurate statecharts.
In the remainder of this paper, the background and related works within the scope of this research are described.
The methodology, a collection of atomic PDEVS models and statecharts exhibiting simple to complex behaviors,
experimental setups, and case studies with evaluations, is provided. A discussion of the limitations and future works
concludes the paper.


2. Background
2.1. LLMs as AI Agents
    Recent progress in transformer-based LLMs has unlocked their use for a wide array of cognitive and creative
tasks (Fan, Li, Ma, Lee, Yu and Hemphill, 2024). These models excel at translating natural language instructions into
programming code, among other skills. When integrated into interactive chat platforms featuring user-driven prompts,
LLMs maintain conversational context using a memory mechanism. Text input is first tokenized, then mapped to
high-dimensional embeddings. The model generates output by successively predicting the next token (𝑘𝑛 ) based on a
context window of preceding tokens (𝑘𝑛−1 , … , 𝑘0 ). The length of this window is limited by the model’s architecture.
    The growing popularity of system-level prompting has catalyzed research into instructing LLM agents via explicit
system prompts. In this paradigm, LLMs dynamically adapt their predictions according to roles and constraints defined
by such prompts, enabling sophisticated context sensitivity, task-specific alignment, and persona-driven reasoning
across multiple application domains (Gao, Lan, Li, Yuan, Ding, Zhou, Xu and Li, 2024; Xiao, Hao, Hanchen, Yifan,
Xuanyu, Hanyu, Yu, Hangliang, Kaiwen, Kejuan, Shudan, Xiang, Aohan, Zhengxiao, Chenhui, Sheng, Tianjun, Yu,
Huan, Minlie, Yuxiao and Jie, 2023).

2.2. Modeling with Parallel DEVS
    Parallel Discrete Event Specification (PDEVS) (Chow and Zeigler, 1994) naturally facilitates the modeling of
discrete-event systems. Its modular, hierarchical foundation is defined as two complementary abstract algebraic
structures, one for atomic models and the other for coupled models. Atomic models represent the basic building
blocks of a system. Coupled models are composed of multiple atomic models (or other coupled models) inter-
connected to represent the overall system. Atomic models in PDEVS (Chow and Zeigler, 1994) are specified as
⟨𝑋𝑀𝑏 , 𝑌 𝑏 , 𝑆, 𝛿 , 𝛿 , 𝛿 , 𝜆, 𝑡𝑎⟩ where,
        𝑀        𝑒𝑥𝑡  𝑖𝑛𝑡  𝑐𝑜𝑛

    • 𝑋𝑀
       𝑏 and 𝑌 𝑏 are independent sets of input and output ports with arbitrary values
              𝑀

    • 𝑆 is the set of phases the atomic component can operate in
    • 𝛿𝑒𝑥𝑡 ∶ 𝑄 × 𝑋𝑀𝑏 → 𝑆, is the External state transition function, which defines how the system state changes upon

      receiving an external event. It is a function of state variables (𝑄) and the input event (𝑋𝑀
                                                                                                 𝑏 )


    • 𝛿𝑖𝑛𝑡 ∶ 𝑆 → 𝑆, is the Internal state transition function, which defines the system’s behavior when the time advance
      for a particular state expires
    • 𝛿𝑐𝑜𝑛 ∶ 𝑆 ×𝑋𝑀 𝑏 → 𝑆, is the Confluence transition function, which resolves conflicts when an internal and external

      transition occur simultaneously.

: Preprint submitted to Elsevier                                                                            Page 2 of 21
    • 𝜆 ∶ 𝑆 → 𝑌𝑀
               𝑏 , is the Output function, which determines the output event to be generated while exiting a state.


    • 𝑡𝑎 ∶ 𝑆 → 𝑅+ 0
                    ∪ {∞}, is the time advance function, it determines how long the model stays in a given state before
      triggering an internal transition.

   As the focus of this work is to introduce a controlled verification of the LLM-driven generation of statecharts of
atomic PDEVS models, the discussion on coupled model specification is excluded.

2.3. PDEVS Statecharts
    The abstract atomic model can be made concrete using PDEVS statecharts which is based on UML statecharts
(Vasa et al., 2025). As in the 𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 and 𝜆, can be specified using Action-Level Real-Time DEVS (ALRT-DEVS)
(Sarjoughian and Gholami, 2015). Each of the 𝛿𝑒𝑥𝑡 and 𝛿𝑖𝑛𝑡 functions can have a sequence of actions. The 𝛿𝑒𝑥𝑡 and 𝛿𝑖𝑛𝑡 are
defined as EXTERNAL -EVENT[GUARD-CONDITION]𝑂𝑃 𝑇 / ACTIONS and INTERNAL -EVENT[GUARD-CONDITION]𝑂𝑃 𝑇
/ ACTIONS for pairs of source and target states, respectively. The statechart state is used to define 𝜆 function as
OUTPUT (PORT, MESSAGES)[GUARD -CONDITION ]𝑂𝑃 𝑇 / ACTIONS. The output functions can be assigned to state
transitions entering a state or state self-transitions. The PDEVS external and output functions have input and output
ports, respectively. The statechart specification includes an initialization function for every atomic model’s initial state
𝑆𝑖 ⊆ 𝑆. Select elements for the statechart of a job processor with a queue that processes the jobs in First-In-First-Out
(FIFO) fashion are provided below:

                                              S: phase = {idle, active}, queue = []
                 𝛿𝑒𝑥𝑡 : !(port-in, Job)[phase == idle] / queue.Append(Job), phase = active, @ pTime
                                  𝛿𝑒𝑥𝑡 : !(port-in, Job)[phase == active] / queue.Append(Job)
                          𝛿𝑖𝑛𝑡 : [phase == active && queue.Len == 0] / phase = idle, @ Infinity
                           𝛿𝑖𝑛𝑡 : [phase == active && queue.Len != 0] / phase = active, @ pTime
                               𝜆: ?[phase == active] / queue.Remove(Job), container.add(Job)


    The IDLE, and ACTIVE are the possible state values for the state variable PHASE. The ! is used for incoming events.
The ? is used for outgoing events. The ADD action adds the event JOB to a container. Containers are necessary to
produce multiple output events on multiple output ports at the same time. The @ signifies the amount of logical time
allocated to external and internal event state transition functions. In this example, PT IME is the processing time. The
QUEUE is initialized as one of the state variables, as it becomes a deciding factor in transitions. The A PPEND , R EMOVE
AND L EN would add incoming jobs, removes the job in FIFO manner, and returns the length of the QUEUE respectively.
    The two external transition functions (𝛿𝑒𝑥𝑡 ) describe the behavior of adding incoming jobs to the queue during both
the IDLE and ACTIVE phases. The internal transition functions (𝛿𝑖𝑛𝑡 ) govern phase changes based on the current state
variables, specifically the QUEUE. When the QUEUE is not empty, the processor selects the first job in line for execution;
otherwise, it transitions back to the IDLE phase. Upon completion, the processed job is removed from the QUEUE and
dispatched through the output port as defined by the output function (𝜆).

2.4. Propositional Logic - Satisfiability and Entailment
    The Propositional Logic (PL) provides a rigorous and systematic way to reason about truth and falsehood in
statements by representing them symbolically. Propositional Logic (PL) is a branch of formal logic concerned with
propositions and their logical relationships. In PL, statements are treated as formulae with symbolic relationships
between propositions, an indivisible unit, which can only take one of two truth values: true or false. Logical operators
such as and (∧), or (∨), not (¬), and implies (⇒) are used to form these formulae which exhibit the relation. Every
proposition is a formula. If 𝜑 and 𝜓 are formulae, then so are the logical relationships between them, such as (¬𝜑)
(negation), (𝜑 ∧ 𝜓) (conjunction) and (𝜑 ⇒ 𝜓) (implication).
    The main motivation for propositional logic is to provide a rigorous and systematic way to reason about truth
and falsehood in statements. In everyday reasoning, facts are often combined, for example, “If it is raining, then the
ground must be wet”. Propositional logic facilitates the formalization of such reasoning into symbolic expressions. The
atomic propositions in this statement are “it is raining” (denoted by propositional variable 𝑝), and “the ground is wet”
(denoted by propositional variable 𝑞). The implication in logical statement can be symbolically represented as 𝑝 ⇒ 𝑞.
By abstracting statements into truth values, we can focus on the logical structure of reasoning rather than the content
of the statements themselves.


: Preprint submitted to Elsevier                                                                              Page 3 of 21
Table 1
Defined propositions for Processor with Queue system.
                                      Proposition                     Definition
                                          𝑏                  Processor is in busy state
                                          𝑔                Job is generated by generator
                                          𝑖                   Processor is in idle state
                                          𝑗              Job signal is received by processor
                                          𝑜             Processed job is sent to output port
                                          𝑝             Job is being processed by processor
                                          𝑞                     Job added to queue


Table 2
PDEVS specifications for a processor with queue expressed in natural language and their propositional logic equivalents.
         PDEVS                                          Natural Language                                     Propositional Logic
       Specifications
                            whenever state is “busy” and “queue” is empty, the state must be “idle” and
          Internal                                                                                               (𝑏 ∧ ¬𝑞) ⇒ 𝑖
                                 time_advance must be infinity (duration to wait for the next job).
         Transitions
                            whenever state is “busy” and “queue” is not empty, the state must be “busy”
                                                                                                                 (𝑏 ∧ 𝑞) ⇒ 𝑏
                                      and time_advance must be 2 (to process the next job).
                           whenever a job is received at job_in and the state is “idle”, the state must be
          External                                                                                               (𝑗 ∧ 𝑖) ⇒ 𝑏
                                 “busy” and time_advance must be 2 (indicating processing time).
         Transitions
                            whenever a job is received at job_in, the state is “busy”, the job is added to
                           the “queue” and time_advance must be the remaining processing time for the            (𝑗 ∧ 𝑏) ⇒ 𝑞
                                                             current job.
           Output          whenever the state is “busy”, the first job must be removed from the “queue”,
                                                                                                                (𝑏) ⇒ (𝑝 ∧ 𝑜)
          Function                             the job is sent to processed_job_out.



    Satisfiability. A set of formulae (Γ) checks satisfiability if there exists an assignment of truth values to its
propositions that makes all the formulae true simultaneously. For instance, consider the Processor with Queue example
from Section 2.3. The propositions defined for the statechart are tabulated in Table. 1.
    Behavioral traits from the PDEVS Specifications for external and internal transitions and output functions can be
abstracted using these propositions. The natural language representation of the specifications and the propositional
formulae are shown in Table. 2. As these specifications hold true for the system and drives the model behavior, we can
consider the set of formulae to be facts (say Γ𝑝𝑟𝑜𝑐 ) (that are assumed to be true). Γ𝑝𝑟𝑜𝑐 should be contradiction-free for
a satisfiable model. Propositional logic representation of these PDEVS facts allows us to check for satisfiability which
accounts for a contradiction-free behavioral traits. Out of 128 boolean assignments for the propositions (Table. 1), 29
assignments satisfies all the facts from Table 2, making the Γ𝑝𝑟𝑜𝑐 satisfiable.
    Entailment. A formula (𝜑) is considered to be entailed by a set of formulae (Γ) if in every assignment of proposition
in {true, false} that makes all formulae in Γ true (satisfiable) also makes 𝜑 true. The entailment of 𝜑 by Γ is denoted
as Γ ⊧ 𝜑.
    A widely adopted approach for verifying entailment involves transforming the problem into an equivalent
satisfiability check. Γ ⊧ 𝜑 iff Γ ∪ {¬𝜑} is unsatisfiable. If Γ′ = Γ ∪ {¬𝜑} is unsatisfiable, then there is no assignment
of propositions where Γ is true but 𝜑 is false. Thus, entailment holds. If Γ′ = Γ ∪ {¬𝜑} is satisfiable, then there exists
an assignment/s of propositions where Γ is true but 𝜑 is false. Thus, entailment does not hold.
    Taking into account the PDEVS facts (Γ𝑝𝑟𝑜𝑐 ) for Processor with Queue, the external transition function (refer
Table. 2) of the model should entail the condition: Processor should become busy if it is idle and a job arrives, i.e.,
𝜑𝑝𝑟𝑜𝑐𝑒𝑥𝑡 = (𝑖) ∧ (𝑗) → (𝑏).

                                               Γ𝑝𝑟𝑜𝑐𝑒𝑥𝑡 = {(𝑗 ∧ 𝑖) → 𝑏, (𝑗 ∧ 𝑏) → 𝑞}
                                                     𝜑𝑝𝑟𝑜𝑐𝑒𝑥𝑡 = (𝑖) ∧ (𝑗) → (𝑏),
                                                 Γ′𝑝𝑟𝑜𝑐 = Γ𝑝𝑟𝑜𝑐𝑒𝑥𝑡 ∪ {¬𝜑𝑝𝑟𝑜𝑐𝑒𝑥𝑡 }
                                                        𝑒𝑥𝑡


    There exists no boolean assignment of the propositions, that makes all the formulae in Γ′𝑝𝑟𝑜𝑐 to be true, Thus
                                                                                                     𝑒𝑥𝑡
Γ𝑝𝑟𝑜𝑐 is unsatisfiable. Thus, we can verify that the condition is held (entailed) by the external transition function, or
 ′
     𝑒𝑥𝑡
Γ𝑝𝑟𝑜𝑐𝑒𝑥𝑡 ⊧ 𝜑𝑝𝑟𝑜𝑐𝑒𝑥𝑡 .

: Preprint submitted to Elsevier                                                                                           Page 4 of 21
                                                    (a) Editor view.




                                                    (b) Verifier view.
                 Figure 1: Snapshot of the Processor with Queue system as Timed Automata in UPPAAL



2.5. Model Checking using UPPAAL
    Formal verification provides mathematical rigor that a behavior model satisfies specific constraints and properties.
Approaches like Testing and Simulation, only explore a subset of scenarios that are possible, whereas formal
verification operates on an abstract model of the system and checks completeness with respect to all possible states and
executions. Within this paradigm, model checking has emerged as one of the most widely used automated techniques.
Model checking systematically explores the entire state space of the model to verify whether the specified properties
hold. This is achieved by encoding the system into a formal representation such as timed automata and defining desired
properties in a formal language, often using logic-based specifications. The basic properties are deadlock detection and
phase reachability of state machines. The definitions for these properties are as follows:

Deadlock: A condition in which the simulation reaches a state from which no further transitions are possible. In this
   state, the system halts all progress because no internal or external events can trigger subsequent state changes.
Phase reachability: A property ensuring that all defined phases of the model are reachable through at least one valid
 sequence of transitions from the initial state. It verifies that the model’s behavioral structure allows exploration of
                                          every phase specified in the system.

The advantage of model checking lies in its automation and exhaustiveness: the verification engine traverses every
reachable phase and every possible execution path.
    UPPAAL (Bengtsson, Larsen, Larsson, Pettersson and Yi, 1996) provides a graphical modeling language to
describe component behaviors in a system as networks of processes (automata) extended with variables, clocks and
control structure (for, if, while, etc). Entire system is modeled by combining all such components in parallel through
synchronization channels. The verifier tool in UPPAAL allows to check for properties such as invariants, deadlock,
and phase reachability by exploring state space of a system. UPPAAL can be leveraged to replicate a timed automata
for an PDEVS statechart to analyze these completeness properties. Detailed explanation on creating an analogous
timed automata for an PDEVS statechart is provided in Section 6.1. The syntax for checking Deadlock and Phase
reachability using the verifier language in UPPAAL are A[] not deadlock, and E<> system.phase. Note that
phase reachability must be checked for all phases of the system.


: Preprint submitted to Elsevier                                                                           Page 5 of 21
    The replica of Processor with Queue system discussed earlier in form of Timed Automata is illustrated in Fig. 1.
job? checks the arrival of the job in the processor. In the model editor (Fig. 1a) clk keeps track of internal clock, needed
to process the job. Q_sz keeps the count of jobs in queue. job, clk, and Q_sz variables are declared as channels,
clock, and int datatypes, respectively, in UPPAAL. For this system, Deadlock and Phase reachability are satisfied,
same is evident from UPPAAL verifier (Fig. 1a).


3. Related Work
3.1. LLMs for Modeling and Simulation
    Machine learning has attracted considerable interest for its potential to support various aspects of simulation
modeling. NLP techniques have been explored for generating conceptual models directly from textual descriptions,
focusing on the identification and extraction of model elements from narrative text (Shuttleworth and Padilla, 2022).
More broadly, LLMs are said to simplify and streamline the activities of modeling and simulation lifecycle, such as
comparing and analyzing simulation outputs (Giabbanelli, 2023).
    In a related study, reinforcement learning was proposed to automate modifications to existing classic DEVS models
in order to achieve a desired output (David and Syriani, 2022). The idea is to map DEVS specification to a Markov
Decision Process (MDP), enabling reinforcement learning—implemented as a proximal policy optimization (PPO)
agent—to iteratively apply actions that alter individual components of an atomic model. Idealy, each action corresponds
to an element of the DEVS formalism, and the resulting model output is evaluated against the ground truth being an
existing model. This iterative process continues until the generated model closely approximates the desired behavior.
The work was demonstrated using a traffic light system, where the RL agent optimizes the time to the next event.
All other aspects of DEVS models — such as external and internal transition functions, component modification, and
coupling adjustments in coupled models — are left as future research.
    Using human expert knowledge in the loop, a framework has been proposed to automatically generate simulation
code for inventory logistics systems based on textual prompts (Jackson et al., 2024). This study demonstrates that GPT-
Codex (Chen, Tworek, Jun, Yuan, Pinto, Kaplan, Edwards, Burda, Joseph, Brockman et al., 2021) can be leveraged
to generate executable models from concise scenario descriptions. Given a description of a finite-capacity inventory
and a set of recurring prompts, the framework produces Python code capable of sequentially increasing and decreasing
entries in a numerical array list. In contrast, the proposed PDEVS-LLM approach aims to generate models that explicitly
capture both the structural and behavioral aspects of model components, as well as their hierarchical composition.
    A framework for generating classic DEVS models using LLMs has been developed (Carreira-Munich et al., 2024).
This work seeks to automate the specification of executable simulation models from system descriptions through the
use of LLM-based agents, conversation histories, and a Co-Pilot architecture. The framework employs two primary
agents: the Concept Specifier and the Formal Specifier. The Concept Specifier leverages DEVS concepts, iterative user
prompts describing the target system, and prior conversation history to produce a conceptual DEVS specification. The
Formal Specifier then refines this output into a formal specification by utilizing Python grammar, user prompts, and
accumulated dialogue context. The DEVS Co-Pilot framework enables modelers to iteratively modify and correct
both conceptual and formal specifications via natural-language interaction. Once the modeler finalizes the formal
specification, a domain-specific language (DSL) parser can automatically generate PythonDEVS code. This work
highlights the advantages of adopting PDEVS statecharts over traditional state machines commonly used in LLMs,
as the resulting hierarchical models can accommodate the Parallel DEVS formalism.

3.2. AI-assisted Simulation Tools
    In the domain of system dynamics and hybrid simulation, Stella Architect (isee systems inc., 2024) has evolved
to include AI-driven modeling assistance: recent versions support an AI Assistant that enables generation of working
simulation models and analysis of Causal Loop Diagrams (CLDs) directly from textual prompts, thereby lowering the
barrier for domain experts to go from conceptual descriptions to executable models. Some recent user experiments
show that GPT-4 can even translate Stella model descriptions into executable Python or Stella code, hinting at growing
synergy between generative AI and system dynamics frameworks (Van Wyk and Kruger, 2023).
    In the agent-based and discrete-event modeling space, AnyLogic has seen efforts toward automated model
generation using templates, external scripts, and semantic mappings (AnyLogic Company, 2021). For example, one
approach reads Excel templates and programmatically instantiates AnyLogic building blocks and connectors (via Java
and XML) to assemble simulation models automatically. More broadly, ontology-based transformations are used to

: Preprint submitted to Elsevier                                                                              Page 6 of 21
generate material flow models (exporting to the AnyLogic .alp format) with minimal human intervention (Dahmen,
Schönemann and Scholz-Reiter, 2023). And in industrial settings, companies like AIG use data-driven simulation
construction (via Java tools interfacing with AnyLogic) to accelerate business process modeling.
    Turning to Simulink, the MathWorks ecosystem is increasingly integrating AI and generative techniques into its
Model-Based Design paradigm (MathWorks, 2024). Simulink supports incorporating AI models (e.g., neural networks,
reduced-order models) trained in MATLAB or external frameworks and simulating them within larger control, signal
processing, or physical models (MathWorks, 2023). MathWorks is also embedding AI copilots/generative assistants to
help users construct models more quickly. In research, there are efforts such as SLGPT, which uses transfer learning
to directly generate Simulink models from natural language or structured descriptions (Shrestha and Csallner, 2021) .
More recently, SimuGen (Ren, Wu and Xu, 2025) has proposed a multimodal agentic framework that jointly reasons
over textual prompts and partial diagrammatic cues to build valid Simulink simulation models, coordinating subagents
for code generation, testing, and debugging.
    While these AI-enhanced tools mark significant progress toward intelligent and automated simulation development,
they primarily focus on model synthesis within fixed paradigms—for example, Stella Architect in continuous system
dynamics, AnyLogic in agent-based or discrete-event domains, and Simulink in control and physical system modeling.
Their AI components largely assist in diagram construction or code suggestion from textual prompts but seldom ensure
formal correctness or hierarchical behavioral consistency. In contrast, the proposed PDEVS-LLM framework aims at
constructing models that can correctly simulate the structures and behaviors of target systems. By coupling generative
LLM agents with formal PDEVS semantics and controlled-correction mechanism, PDEVS-LLM aims not only to
generate models from natural language but also to verify and refine their structural and behavioral fidelity.

3.3. Verification based refinement in LLM applications
    Recently, multiple verification-based iterative prompting techniques have been proposed to improve the responses
of pre-trained LLMs. One approach is to reduce the hallucinations in LLMs by first drafting an initial response and
then planning the verification questions for fact-checking the draft. Questions are answered independently and based
on which final responses are generated. Another approach proposes using Recursive Criticism and Improvement (RCI)
prompting for domain-specific tasks (such as solving computer tasks) (Kim, Baldi and McAleer, 2023). It involves
two steps: criticizing the previous answers and improving them based on some critiques. While the study demonstrates
superior performance in addressing computational tasks, this approach does not account for mathematical modeling
theories that ground the development of simulations such as LLM-generated PDEVS models.
    Works such as ProCo (Wu, Zeng, Zhang, Tan, Shen and Jiang, 2024), can extract the key conditions that are present
in the prompt. Conditions (such as Arithmetic problems from the GSM8K dataset (Cobbe, Kosaraju, Bavarian, Chen,
Jun, Kaiser, Plappert, Tworek, Hilton, Nakano, Hesse and Schulman, 2021)) are used to generate the substitution-
based verification questions for generated answers. For tasks such as generating discrete-event models, identifying key
conditions from system descriptions is challenging since models have complicated structures and complex behavior
that are not directly included in the description.
    Building upon these verification-oriented paradigms, GPT-4 is used to produce SysML/UML-compliant activity
and flow-based models through human directed refinement (Alshareef et al., 2024). The iterative process involves
prompting, syntactic correction, code generation, and simulation validation. While this workflow demonstrates the
feasibility of LLM-assisted model synthesis, there persist discrepancies between syntactic correctness and behavioral
accuracy: for example, parallel flows, synchronization nodes, and control semantics are frequently misplaced or under-
specified. Such limitations highlight that the refinement process in simulation modeling parallels the verification-based
controlled-correction loop—where simulation outcomes, metamodel constraints, and domain rules act as verification
feedback guiding the LLM toward behaviorally valid models. In contrast, in the PDEVS-LLM framework (Vasa et al.,
2025) supported integrated plausible atomic PDEVS statechart model generation and propositional verification. These
and other works suggest that the use of LLM for constructing models that have correct syntax and semantics remains
an open challenge.


4. Methodology
    The paper proposes an agentic-framework that can assist in developing the behavior of atomic Parallel DEVS
Statecharts models based on LLM-generated PDEVS plausible facts and behavioral conditions. The generated
statecharts are evaluated for both completeness and correctness. Model checking properties, namely Deadlock and

: Preprint submitted to Elsevier                                                                            Page 7 of 21
Figure 2: Overview for the proposed framework to generate. The Red arrows represents API LLM calls, both Agentic
and Non-Agentic. The Blue arrows represent the Python function calls. The Green arrow represent the feedback for
controlled-correction with Modification Prompt.



Phase Reachability, are employed to measure improvements with and without the proposed verification mechanism.
For this purpose, Timed Automata replicas of the statecharts are manually developed in the UPPAAL tool to verify
these properties. Additionally, a Statechart Correctness Score is introduced to manually assess the correctness of each
element within a statechart and aggregate the results into a single numerical value. Experiments are conducted using
multiple publicly available LLMs to demonstrate the generalizability of the proposed verification mechanism.
    PDEVS-LLM (Vasa et al., 2025) introduced an agentic Framework which generates PDEVS statecharts from
the provided System Description in two stages: Plausible PDEVS facts extraction, and Atomic and Coupled model
generation using the extracted facts. The Plausible facts span the PDEVS specifications (explained in Section 2.2) in
natural language. It is a set of statements, which represent the behavioral traits such as internal/external transitions
and output functions. Considering that PDEVS statecharts generated in latter stage result from these facts, it is safe to
assume that these facts are the natural language representation of the statechart (or say behavior model). The logical
contradictions and erroneous PDEVS specifications in these facts leads to the generation of wrong PDEVS statecharts
in the latter stage needing a domain expert to rectify.
    This paper proposes a revised agentic framework for PDEVS Statechart generation, integrated with a verification
mechanism (in propositional logic domain) to correct the PDEVS Plausible facts. The proposed framework (refer to
Fig. 2) facilitates the PDEVS statechart generation for atomic components in four phases: i) Behavioral conditions
Identification and (intial) PDEVS Plausible facts generation. ii) Behavioral conditions Satisfiability Check. iii)
Segregated Entailment Verification and Controlled-Correction of PDEVS Plausible Facts. iv) PDEVS Statechart
Generation.
    Behavioral conditions are based on the model’s behavior, which can be formalized to have internal/external
transition and output functions defined in terms of state and time. The behavioral conditions can be used to verify
that a model has a correct behavior dynamics. Natural Language Representation lacks the uniqueness in sematic
way. The interpretations for a single statement can vary from multiple perspectives. Symbolic representation, such
as propositional logic provides a common ground to confine the semantic meaning to a single interpretation. Proposed
Segregated Entailment Verification provides a way to verify the logical consequence of the behavioral condition
by the PDEVS facts in the reduced form of propositional logic. This facilitates the deterministic filtration of the non-
entailed conditions (by facts) to use in engineering a modification prompt in controlled-correction loop. This navigates
the (re)generated model behavior towards logical alignment with the system description.
    Post termination of the correction loop, the plausible facts with most entailed conditions is selected and used for
statechart generation. The Atomic Model Generator Agent proposed in (Vasa et al., 2025) is used to generate PDEVS
statecharts. The system prompt for this agent incorporates the Statechart Grammar represented in EBNF style, which

: Preprint submitted to Elsevier                                                                            Page 8 of 21
                                    Figure 3: Illustration of the Proposed Framework.



aids the LLM in parsing the plausible facts into the PDEVS statechart. The framework is equipped for translation of
PDEVS statecharts into XML format to store in a relational database and into PlantUML syntax for visualization. The
code and test cases to replicate the experiments in this paper are available at GitHub Repository.

4.1. Plausible PDEVS Facts and Behavioral Conditions: Derivation and Satisfiability
    Parallel DEVS specifications (models) are algebraic structures containing general and domain-specific knowledge
of the system to be simulated (as explained in Section 2.2). To verify the correctness of domain-specific system
models, behavioral conditions can be extracted from their descriptions. These conditions can be formalized to have
internal/external transitions and output functions defined in terms of state. These conditions can be used to verify that a
model has correct behavior dynamics. A feedback control can be engineered based on the outcome of this verification
to improve the logical consistency of the PDEVS plausible facts.
    PDEVS Specification Generator generates the PDEVS plausible facts for the component described in the system
description using the Few-shot technique (Brown, Mann, Ryder, Subbiah, Kaplan, Dhariwal, Neelakantan, Shyam,
Sastry, Askell, Agarwal, Herbert-Voss, Krueger, Henighan, Child, Ramesh, Ziegler, Wu, Winter, Hesse, Chen, Sigler,
Litwin, Gray, Chess, Clark, Berner, McCandlish, Radford, Sutskever and Amodei, 2020). The generated specification
conforms to the elements of the PDEVS formalism and is structured in JSON format. The Agent retains history to
ensure the contextual consistency during modifications and possesses the knowledge about the PDEVS Specifications
as the system prompt. The system prompt used in the experiments is inspired by PDEVS-LLM. For the segregated
entailment verification, we consider external transition (𝛿𝑒𝑥𝑡 ), internal transition (𝛿𝑖𝑛𝑡 ), and output function (𝜆) from
the generated facts.
    Simultaneously, the behavior conditions to be satisfied by the specifications are identified and extracted in JSON
format. Given a model specification, the behavior conditions are generated for time-state functions, 𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆 and
are denoted as 𝐶𝑒𝑥𝑡 , 𝐶𝑖𝑛𝑡 , 𝐶𝑜𝑢𝑡 respectively. The system prompt used to identify the behavior conditions from the given
system description is as follows:

    You are a system designer analyzing a component from a larger system. Your task is to derive atomic,
    verifiable behavioral conditions for the component under three categories:

    - Behavior Types:

    1. Internal Behavior: Actions or transitions triggered by the component’s own state or internal logic.



: Preprint submitted to Elsevier                                                                              Page 9 of 21
    Not caused by external messages. E.g., transitioning from busy to idle after finishing a task.

    2. External Behavior: Actions triggered by receiving an external signal/message/input from another
    component. These occur when the component is in a certain state and responds to the input. E.g.,
    transitioning to busy when receiving a job while in idle.

    3. Output Behavior: Outputs/messages generated because of a state change or a condition. Typically
    sent just before an internal transition occurs.

    - Output Requirements:

    1. Each condition must be atomic: a minimal, indivisible unit of behavior.
    2. Use clear causal phrasing like:

                                              "If state is X, perform Y”
                              "If input Z is received while in state A, transition to B”
                                          "If state is Y, generate output Z”


     Fig. 3 illustrates the proposed framework. Before proceeding with the verification, it is important to check the
logical consistency of the facts and conditions individually. There is no point in verification process if facts and/or
conditions themselves are logically contradicting. To address this, an LLM call is leveraged to translate the natural
language representations of facts and conditions into the set of propositional logic formulae. To avoid multiple
definitions in facts formulae and conditions formulae for the same proposition (symbol), we use common propositions
identified from the system description. The facts and conditions in propositional logic can be described in form of sets
as Γ = {Γ𝑒𝑥𝑡 , Γ𝑖𝑛𝑡 , Γ𝑜𝑢𝑡 }, and 𝜑 = {𝜑𝑒𝑥𝑡 , 𝜑𝑖𝑛𝑡 , 𝜑𝑜𝑢𝑡 } respectively.
     The logical consistency of facts (Γ) and conditions (𝜑) is evaluated by satisfiability check using a SAT solver. If
either or both fail the check, a domain expert or an LLM is tasked to rectify and mitigate the contradiction. The same is
depicted in Fig. 3, this internal loop can be exited if both the entities pass satisfiability check or a pre-determined no. of
iterations are exhausted. The satisfiability check for conditions is conducted only once (in second phase) as they are not
revised based on the verification results. On the other hand, satisfiability check for PDEVS facts is conducted in every
iteration of the controlled-correction loop (third phase) as the PDEVS facts are modified according to the verification
results.
     Since the facts and conditions are derived directly from the system description, any logical inconsistency in the
description inevitably produces an unsatisfiable set of PDEVS facts and/or behavioral conditions. To address this, we
impose predefined thresholds, (𝑛, and 𝑚 for facts and conditions, respectively) on the number of allowable revisions.
If, after exceeding this threshold, a satisfiable set of PDEVS facts or conditions cannot be obtained, the process is
TERMINATEd (as illustrated in Fig. 3 and Algorithm 1).

4.2. Segregated Entailment Verification and Controlled-correction
     The PDEVS external, internal, and output functions are distinct. The external and internal transition functions can
read and write the model’s state variables. The output function should only read the state variables. For instance, the
Processor (described in 2.3) processing the job is an independent activity from the processor receiving jobs or sending
jobs to output. This clear distinction allows the identification of individual conditions for each of these entities and
verification of them separately. Post passing the satisfiability check, the entailment check is conducted categorically,
i.e., each condition in 𝜑𝑖𝑛𝑡 is checked for entailment against Γ𝑖𝑛𝑡 , and same goes for (𝜑𝑒𝑥𝑡 , Γ𝑒𝑥𝑡 ) and (𝜑𝑜𝑢𝑡 , Γ𝑜𝑢𝑡 ) pairs.
     As illustrated in Fig. 3, the verification can end with three possibilities. i) If every condition from all three categories
passes the entailment check, then the facts in natural language from the current iteration are passed for the PDEVS
statechart generation. ii) If some/all of the conditions in any of the categories fail the entailment check, the controlled-
correction loop is initiated to refine the facts. iii) In case the first possibility is not achieved and controlled-correction
loop iterations exhaust the pre-defined threshold (𝑔), the version of PDEVS facts (Γ) with the most entailment count
(across all categories) is opted and its natural language counterpart is used for statechart generation.
     To initiate the controlled-correction loop, the non-entailed conditions in natural language ({𝐶𝑒𝑥𝑡       ′ , 𝐶 ′ , 𝐶 ′ })are
                                                                                                                    𝑖𝑛𝑡   𝑜𝑢𝑡
parsed in the below represented modification prompt format:




: Preprint submitted to Elsevier                                                                                  Page 10 of 21
    Verify whether the following behavioral traits are already captured in the generated facts. If any are
    missing or incomplete, refine the facts accordingly by updating transitions, states, and time advance.
    Analyze properly and only modify if needed to suffice the system description.

                                    ′ »
    internal transition function: «𝐶𝑖𝑛𝑡

                                    ′ »
    external transition function: «𝐶𝑒𝑥𝑡

                       ′ »
    output function: «𝐶𝑜𝑢𝑡

    Include any missing ports, phases and state variables according, fix errors, and ensure time advance is
    present for transitions. Strictly, retain the needed states and transitions. Return the full updated
    facts in the json format only. No additional text needed outside json.


    Please note that 𝐶𝑖𝑛𝑡
                       ′ , 𝐶 ′ , and 𝐶 ′ in the modification prompt only represent the conditions that failed the
                             𝑒𝑥𝑡       𝑜𝑢𝑡
entailment check. If the all the conditions from a particular category pass the entailment check, the category is
omitted from the verification process in upcoming iterations. This forms the controlled feedback to navigate PDEVS
Specification Generator (agent) towards logical consistency with the system description. The entire process is divided
into four phases which is described in Algorithm 1.


5. Experimental Setup
    Experiments are conducted with multiple LLMs as base models for the PDEVS Specification Generator Agent
with the temperature parameter fixed at 0.3. Apart from the agent, four separate LLM API calls (along with the
fixed system descriptions) are designed : i) Identifying Behavioral Conditions, ii) Extracting propositions from
System Description, iii) Translating a subset of PDEVS facts (𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆) from natural language to propositional
logic formulae (Γ = {Γ𝑒𝑥𝑡 , Γ𝑖𝑛𝑡 , Γ𝑜𝑢𝑡 }), and iv) Translating Behavioral Conditions to Propositional logic formulae
(𝜑 = {𝜑𝑒𝑥𝑡 , 𝜑𝑖𝑛𝑡 , 𝜑𝑜𝑢𝑡 }). Framework leverages GPT-4o-mini with the temperature fixed at 0.3 (for more determinism
in responses (Peeperkorn, Kouwenhoven, Brown and Jordanous, 2024)) for these calls. The system prompts are
engineered to generate the responses in JSON format to facilitate better key-value extraction after parsing. Framework
is equipped for three retries for any of the above LLM-calls if the JSON parsing of the response fails before terminating
with an error.
    The Boolean SAT solver functions are developed using z3-solver python library by Microsoft (de Moura and
Bjørner, 2008) which provides the syntax to parse the propositional logic formulae and conduct the satisfiability check.
The theresholds for satisifiabilty check for both the facts and condition are set to 3., i.e., 𝑚 = 𝑛 = 3. The entailment
verification can be conducted by reducing it to satisfiability check problem as discussed in Section 2.4. After obtaining
the final PDEVS facts, following PDEVS-LLM (Vasa et al., 2025) EBNF style PDEVS Statechart Grammar is used to
generate the statecharts. As per PDEVS-LLM, GPT-4-0125-preview with temperature set to 0.7 is used for the task.
    The proposed framework is evaluated on a test set of fourteen curated system descriptions (discussed in Ap-
pendix A) for standalone atomic components with varying complex behaviors. The test set also include the components
of MiniFab, a benchmark discrete-event system (DES) model widely used in the modeling and simulation community.
As the generated PDEVS statecharts are the resultants of generated PDEVS facts, we compare the completeness
and correctness of the statecharts generated using PDEVS facts before and after verification. This shows the impact
of the proposed Segregated Entailment Verification based controlled-correction loop. The later sections report the
performance of the proposed verification mechanism while using the following publicly available models used as base
model for PDEVS Specification Generator: Llama-3.1-8b, Llama-3.3-70b, Ministral-3b, Ministral-8b,
Mistral-7b-instruct, Qwen3-32b, Claude-opus-4.1, GPT-4o-mini. The set of models spans a variety of
categories, which includes small, large, instruction-tuned, and reasoning-oriented models.

5.1. Case Study: Phone
   Consider a Phone system exhibiting a complex behavior. Phone operates in On, Off, SearchingForService,
Ready and Active phases. It includes two state variables, queue to store incoming calls and a boolean variable
service to maintain the availability of the service to take calls. It has two input ports, OnOff to receive “start/stop”
inputs and incomingVoice to receive incoming call (“talk” events). The output port outgoingVoice handles the
outgoing voice (“TALK”) events.

: Preprint submitted to Elsevier                                                                           Page 11 of 21
Algorithm 1 Framework Algorithm. The ⇒, and → indicates Agent, and standalone LLM call respectively.
Require: System Description (𝑁) of the Component in Natural Language Representation
                                                                      P HASE-1: B EHAVIORAL C ONDITIONS IDENTIFICATION
                                                                      AND (INITIAL ) PDEVS P LAUSIBLE FACTS G ENERATION

           PDEVS Specification
 1: 𝑁 ⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇒
                                         ⇐ {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆}
                Generator
           Behavioral conditions
 2: 𝑁 ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←→
                                          ← {𝐶𝑒𝑥𝑡 , 𝐶𝑖𝑛𝑡 , 𝐶𝑜𝑢𝑡 }
             Identification
                         Propositional Logic
 3: {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆} ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←→
                                                      ← {Γ𝑒𝑥𝑡 , Γ𝑖𝑛𝑡 , Γ𝑜𝑢𝑡 } = Γ
                                Translation
                                 Propositional Logic
 4: {𝐶𝑒𝑥𝑡 , 𝐶𝑖𝑛𝑡 , 𝐶𝑜𝑢𝑡 } ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←→
                                                          ← {𝜑𝑒𝑥𝑡 , 𝜑𝑖𝑛𝑡 , 𝜑𝑜𝑢𝑡 } = 𝜑
                                        Translation
                                                                    P HASE-2: B EHAVIORAL CONDITION SATISFIABILITY CHECK

 5: #𝑐𝑜𝑛𝑑𝑖𝑡𝑖𝑜𝑛𝑠 = 0
 6: while 𝑆𝐴𝑇 (𝜑) ≠ 𝑇 𝑅𝑈 𝐸 do
 7:     if #𝑐𝑜𝑛𝑑𝑖𝑡𝑖𝑜𝑛𝑠 ≤ 𝑚 then
 8:          Redo {𝐶𝑒𝑥𝑡 , 𝐶𝑖𝑛𝑡 , 𝐶𝑜𝑢𝑡 } (an Expert or LLM)
                                                Propositional Logic
 9:              {𝐶𝑒𝑥𝑡 , 𝐶𝑖𝑛𝑡 , 𝐶𝑜𝑢𝑡 } ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←→
                                                                       ← {𝜑𝑒𝑥𝑡 , 𝜑𝑖𝑛𝑡 , 𝜑𝑜𝑢𝑡 } = 𝜑
                                                     Translation
10:             #𝑐𝑜𝑛𝑑𝑖𝑡𝑖𝑜𝑛𝑠 += 1
11:         else TERMINATE
                                                                    P HASE-3: SEGREGATED E NTAILMENT V ERIFICATION AND
                                                                    C ONTROLLED-C ORRECTION OF PDEVS P LAUSIBLE FACTS

12: #𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑖𝑜𝑛 = 0
13: while #𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑖𝑜𝑛 ≤ 𝑔 do
14:     #𝑓 𝑎𝑐𝑡𝑠 = 0
15:     while 𝑆𝐴𝑇 (Γ) ≠ 𝑇 𝑅𝑈 𝐸 do
16:          if #𝑓 𝑎𝑐𝑡𝑠 ≤ 𝑛 then
17:              Redo {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆} (an Expert or LLM)
                                                Propositional Logic
18:                     {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆} ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←→
                                                                          ← {Γ𝑒𝑥𝑡 , Γ𝑖𝑛𝑡 , Γ𝑜𝑢𝑡 } = Γ
                                                     Translation
19:                 #𝑓 𝑎𝑐𝑡𝑠 += 1
20:             else TERMINATE
21:         for 𝑥 ∈ {𝑒𝑥𝑡, 𝑖𝑛𝑡, 𝑜𝑢𝑡} do
22:             𝐶𝑥′ = ∅
23:             for 𝜑𝑥𝑘 ∈ 𝜑𝑥 , where k = 1,2,... do
24:                 if 𝜑𝑥𝑘 ̸⊧ Γ𝑥 then 𝐶𝑥′ = 𝐶𝑥′ ∪ 𝐶𝑥𝑘
25:               ′ , 𝐶 ′ , 𝐶 ′ } = ∅ then
            if {𝐶𝑒𝑥𝑡     𝑖𝑛𝑡    𝑜𝑢𝑡
26:             ({𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆} is finalized and Jump to PHASE-4
27:                   ′ , 𝐶′ , 𝐶′ }
            𝐶 ′ = {𝐶𝑒𝑥𝑡       𝑖𝑛𝑡   𝑜𝑢𝑡
                  Modification Prompt
28:         𝐶 ′ ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←→
                                                  ← 𝑀(𝐶 ′ )
                          Parsing
                         PDEVS Specification
29:         𝑀(𝐶 ′ ) ⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇒
                                                       ⇐ {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆}
                                Generator
                                 Propositional Logic
30:         {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆} ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←→
                                                              ← {Γ𝑒𝑥𝑡 , Γ𝑖𝑛𝑡 , Γ𝑜𝑢𝑡 } = Γ
                                         Translation
31:         #𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑖𝑜𝑛 += 1

                                                                             P HASE-4: PDEVS STATECHART G ENERATION

32: {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆} with high entailment count is finalized.
                             PDEVS Statechart
33: {𝛿𝑒𝑥𝑡 , 𝛿𝑖𝑛𝑡 , 𝜆} ⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇐⇒
                                                    ⇐ 𝑆𝐶
                                  Generator
34: R ETURN 𝑆𝐶



    Phone turns on with “start” and turns off with “stop” commands (messages). When turned on it will enter
SearchingForService phase stays there for 2 time units. If service value is True, it will transition to Ready, else
will return to On and retries after 1 time unit. If “talk” event is received in Ready phase, Phone will transition to
Active phase and generated the output “TALK” in response to “talk” event. If interrupted in Active, the incoming



: Preprint submitted to Elsevier                                                                                           Page 12 of 21
Table 3
Extracted propositions for Phone component
                                     Proposition                        Definition
                                          𝑎                           Phone is active
                                          𝑐                     Call is received by phone
                                          𝑓                           Service is found
                                          𝑖               Phone is interrupted by another call
                                         𝑚                Interrupting call is stored in memory
                                          𝑛                             Phone is on
                                         𝑛𝑓                        Service is not found
                                          𝑜                             Phone is off
                                          𝑞             Phone is in the queue for searching service
                                         𝑞1              Phone is in the queue for receiving calls
                                          𝑟                  Phone is ready to receive calls
                                          𝑠                   Phone is searching for service
                                         𝑠𝑝                   Stop event received by phone
                                         𝑠𝑡                   Start event received by phone
                                         𝑡1                      Talk event a1 is received
                                         𝑡2                    Talk event A1 is responded
                                         𝑡3                     Talk event b2 is received
                                         𝑡4                    Talk event B2 is responded
                                         𝑡5                      Talk event z1 is received
                                         𝑡6                    Talk event Z2 is responded


Table 4
Results of the segregated entailment verification (SEV) for the Phone system. The controlled-correction loop threshold is
set to 3. The iteration with maximum conditions (overall) being entailed by the generated facts is highlighted.
              Condition                                                                                    SEV Results(#𝑖𝑡𝑒𝑟 )
                                         Natural Language                         Propositional Logic
                Type                                                                                       1      2         3
                              If in SearchingForService phase for 2 time
                           units and service is found, transition to Ready           (𝑠 ∧ 𝑓 ) → (𝑟)        ✓       ✗       ✓
               Internal                             phase.
                              If in SearchingForService phase for 2 time
                             units and service is not found, return to On            (𝑠 ∧ 𝑛𝑓 ) → (𝑛)       ✗       ✓        ✗
                                                    phase.
                           If in Active phase and current conversation is
                              completed, start with the first interrupted              (𝑎) → (𝑡1)          ✗       ✗        ✗
                                          talk event from memory.
                            If input ’start’ is received while in Off phase,
                                           transition to On phase.
                                                                                     (𝑠𝑡 ∧ 𝑜) → (𝑛)        ✓       ✓       ✓
               External     If input ’stop’ is received while in any phase,
                                           transition to Off phase.
                                                                                       (𝑠𝑝) → (𝑜)          ✓       ✗       ✓
                                    If in On phase and input event for
                           SearchingForService is triggered, transition to             (𝑛) → (𝑠)           ✗       ✓        ✗
                                         SearchingForService phase.
                           If in Ready phase and input event ’a1’ to ’z1’      (𝑟∧(𝑡1∨𝑡2∨𝑡3∨𝑡4∨𝑡5∨𝑡6)) →
                                 is received, transition to Active phase.                  (𝑎)
                                                                                                           ✗       ✓        ✗
                                  If in Active phase and conversation is
                Output
                                  completed, generate output event for                 (𝑎) → (𝑜)           ✗       ✗        ✗
                                               outgoingVoice.
                           If in Active phase and interrupted by another
                                call, store the interrupting talk event in           (𝑎 ∧ 𝑖) → (𝑚)         ✗       ✓        ✗
                                                   memory.



“talk” event will be stored in the queue/memory. service can toggle between True/False at any time. The desired
PDEVS statechart generated manually by an expert is illustrated in Fig. 4a.
    The above explained behavior is transcribed in the natural language as a system description and is provided as
input to the proposed framework. The propositions from the system description are tabulated in Table. 3. These
propositions are then used to translate the identified behavioral conditions into their propositional logic counterparts
(refer Table. 4). The last three columns of Table. 4 show the results of Segregated Entailment Verification for three
iteration of controlled-correction loop. The reported results are obtained by using gpt-4o-mini as base model for
PDEVS Specification Generator agent. For the provided system description, the PDEVS facts in the 2𝑛𝑑 iteration

: Preprint submitted to Elsevier                                                                                                 Page 13 of 21
                                                (a) Desired PDEVS statechart




                           (b) Generated PDEVS statechart using the PDEVS facts before verification




                            (c) Generated PDEVS statechart using the PDEVS facts after verification

     Figure 4: Desired and Generated PDEVS statecharts for Phone system visualized using CoSMoS modeling tool.



entail the most conditions (5 out of 9) compared to that of the other iterations. The PDEVS facts from this iteration are
finalized and used for the corrected PDEVS statechart.
    Fig. 4b and 4c visualize the PDEVS statecharts generated using the PDEVS facts before and after (#𝑖𝑡𝑒𝑟 − 1)
verification, respectively (as #𝑖𝑡𝑒𝑟 − 2 resulted in more conditions being entailed). The illustration represents the
lack of logical consistency in phase transitions before proposed SEV and incorrect phases (Dynamic). As per
the statechart, the Ready phase is never achieved after the Phone is turned on. The missing linkage between the
On-SearchingForService-Ready contributes to a major misalignment of this statechart with the system description.

: Preprint submitted to Elsevier                                                                           Page 14 of 21
Table 5
Analogy to model a Timed Automata for given PDEVS Statechart.
          PDEVS Statecharts                                         UPPAAL Timed Automata
                 Phases                                                       Locations
             State variables                                        defined as Local Declarations.
    Input/output ports and messages                             defined as synchronization channels.
                                        External events can be defined using channels. Guard and Action can be declared in
      External Transition Function      Guard and Update properties of the UPPAAL transition respectively. Time Advance
                                                       can be handled using a clock variable locally declared.
                                          Triggered by adding the invariant [ internal clock ≥ Time advance ] in the Guard
      Internal Transition Function        property of the transition. Guard and Action can be declared in the Guard and
                                                                          Update properties.
            Output Function                                                    Omitted



Missing transitions from all the other phases to Off, deprives the phone of the turning off mechanism. On the other
hand, after correction (Fig. 4c), most of the inaccuracies have been eliminated by navigating the generation towards
logical consistency through segregated entailment verification. The Phase reachability issue has been resolved and
missing transitions from before correction have been added. It is noteworthy to acknowledge that even after correction,
the statechart might not be completely correct. For instance, considering the expert generated statechart (Fig. 4a), the
desired internal transitions: SearchingForService → On (if service == False), and Active → Ready (if there
are no interrupted call events) are missing in the final output. However, the improvement over the previous version
(before correction) significantly reduces the manual efforts needed for refining the final statechart.


6. Statechart Evaluation
6.1. Model Checking
    Model checking provides a rigorous framework for verifying whether a system model satisfies certain desirable
properties. Unlike simulation, which explores specific execution traces, model checking systematically explores the
entire state space of the system to ensure correctness across all possible behaviors. This makes it particularly well
suited for evaluating PDEVS statecharts, where the combination of discrete events and timing constraints can lead to
subtle behaviors such as deadlocks or unreachable phases that may not be exposed through limited simulation runs.
    In this work, we leverage the UPPAAL to analyze our PDEVS specifications given in form of statecharts. Timed
Automata replicas for the PDEVS statecharts are manually created in the UPPAAL Editor, with necessary Global,
Local and System Declarations. We design and follow a specific analogy to construct a close replica using UPPAAL
options for a given PDEVS statechart. The analogy is explained in Table. 5. The Output function could be mechanized
using the sychronization, but serves no purpose for property verification. Taking this into consideration, we omit the
replication of Output function. After replicating the statecharts, we use the syntax explained in the sub-section of model
checking to check for Deadlock and Phase reachability properties.
    The Fig. 5 shows the Timed Automata replicas for the PDEVS statecharts generated (shown in Fig. 4). start?,
stop? and talk? events are declared in the Global declarations and triggered using a separate event generator
component. Q_talks (to maintain the no. of interrupted calls stored), x (elapsed time), ta (time advance) and
service (to check for service availability) variables are declared in Local declarations of the Phone. Model checking
on the Phone system before correction resulted in No Deadlock, and No Phase reachability for Active, Ready,
searching_for_service and dynamic phases. After correction the Phase reachability property is satisfied in the
model checking.
    To understand the generalizability of the proposed technique, we conducted experiments with eight publicly
available LLMs as base models for PDEVS Specification Generator Agent and the results are reported in Table. 6. The
results show that smaller models such as Llama-3.1-8b and Ministral-8b achieved relatively significant outcomes
for both deadlock and phase reachability. Most base models exhibited improvements in the properties after integration
of the proposed controlled-correction loop, notably in reducing deadlock cases and improving phase reachability
outcomes. Notably, Mistral-7b-instruct was an exception, displaying the increment in number of deadlock failures
(2 in BV, 3 in AV). In contrast, advanced reasoning models such as Qwen3-32b and GPT-4o-mini demonstrated
consistent improvements for satisfiability of both properties.


: Preprint submitted to Elsevier                                                                              Page 15 of 21
                              (a) Timed automata for the Phone system before correction (Fig. 4b)




                               (b) Timed automata for the Phone system after correction (Fig. 4c)
Figure 5: Manually generated Timed Automata replicas for the Phone example using UPPAAL. The snapshots are taken
from the Editor tab of UPPAAL.


6.2. Statechart Correctness
    For every PDEVS statecharts, it is important to determine whether each of its internal and external transition
and output functions associated with the phases are needed or not. Along with the necessity of these elements, the
correctness of the properties associated such as guard condition, action, time advance and internal/external events
should also be evaluated. To achieve the numerical value for correctness a domain expert is tasked to manually collect
the information needed for the evaluation of statechart’s correctness with respect to the provided system description.


: Preprint submitted to Elsevier                                                                        Page 16 of 21
Table 6
Model Checking results over the test set comprising of 14 system descriptions using various publicly available LLMs as base
model for PDEVS Specification Generator Agent. These models are categorized as small models (< 10B parameters)† ,
large models (> 30B parameters)‡ , instruction tuned * , and reasoning oriented § . BV, and AV stands for the stats before
and after verification respectively.
                                                           No. of Systems         No. of Systems
                                                            suffering with          not satisfying
                                                              Deadlock           Phase reachability
                                          LLM
                                                           BV        AV          BV          AV
                                     Llama-3.1-8b†          5         2           5           2
                                      Ministral-3b†         1         1           1           0
                                      Ministral-8b†         4         2           1           0
                                     Llama-3.3-70b‡         1         0           1           0
                                   Mistral-7b-instruct*       2        3          2              0
                                      Qwen3-32b‡§             3        2          3              1
                                   Claude-opus-4.1*§          0        0          1              0
                                    GPT-4o-mini*§             3        1          3              1


Table 7
Statechart correctness scores for the Phone PDEVS statechart resulted from the PDEVS facts before correction. The
values in green cells are calculated by averaging the values in blue cells from the same row. The values in yellow cell is
calculated by averaging the values in green cells. The red cells are avoided in the calculations as they represent the wrong
specification.
                                                                                                  Time      Avg. Correctness
                    Transition               Needed?      Guard      Message          Action
                                                                                                 Advance    (Transition Wise)
             Off → On (start event)                1         1             1             1          0              0.75
             On → Off (stop event)                 1         1             1             1          1                1
          Ready → Active (talk event)              1         1             1             1          1                1
          Active → Active (talk event)             1         1             1             1          1                1
                                                Correctness Score                                                0.9375
                                        (a) External Transition Function Correctness Score
                                                                                               Time      Avg. Correctness
                          Transition                   Needed?       Guard      Action
                                                                                              Advance    (Transition wise)
                     Active ⤏ Active             1                     0             0           1            0.333
              SearchingForService ⤏ Dynamic      0                     -             -           -               -
                                       Correctness Score                                                      0.167
                                         (b) Internal Transition Function Correctness Score
                                                                                             Avg. Correctness
                            Phase       Needed?       Guard       Message      Action
                                                                                             (Function Wise)
                            Active          1           1         1              1                  1
                                                Correctness Score                                   1
                                                (c) Output Function Correctness Score



    For each external transition, domain expert will answer the following questions: Is the transition needed?, is Guard
condition correct?, Is the Message (along with its port) is correct?, Is the Action correct?, Is the Time advance correct?
Similar questions except for the Message are answered for each internal transition. For each output, the expert decides
whether its is needed in that phase or not followed by Guard, Action and Message validity check. Yes is assigned value
1 and No is assigned value 0 to have a numerical score for correctness of PDEVS specifications.
    Once the correctness questions are evaluated by the expert as 1 true and 0 as false, the correctness score for each
transition or function is computed by averaging the entries where the Needed? can range from 0 to 1. These scores for
the individual parts of the external transition, internal transition, and output functions are then aggregated and averaged
to determine the overall correctness score categorically. Table 7 presents the calculated statechart correctness scores



: Preprint submitted to Elsevier                                                                                         Page 17 of 21
Table 8
Performance of multiple LLMs as base model for PDEVS Specification Generator in terms of the proposed Statechart
Correctness Score Before Verification (BV) and After Verification (AV). The improvement and decline in the scores is
highlighted in red and green respectively.
                                        External Transition Fn.   Internal Transition Fn.      Output Fn.
                        Model
                                          BV           AV           BV           AV           BV       AV
                    Llama-3.1-8b        0.9434       0.8809       0.6416       0.7736       0.7935   0.8571
                     Ministral-3b       0.8065       0.7755       0.6427       0.7801       0.8809   0.9047
                     Ministral-8b       0.8392       0.8142       0.7857       0.7857       0.8571   0.8571
                    Llama-3.3-70b       0.8244       0.8928       0.6548       0.7991       0.7856   0.9285
                  Mistral-7b-instruct   0.8100       0.8100       0.7976       0.8214       0.7142   0.7142
                      Qwen3-32b         0.7471       0.9214       0.6667       0.8849        0.738   0.9523
                   Claude-opus-4.1      0.9047       1.0000       1.0000       1.0000       1.0000   1.0000
                     GPT-4o-mini        0.6423       0.7757       0.7175       0.8555       0.6944   0.7222



for the phone system before correction (Fig. 4b). The second internal transition (refer to Table. 7b) is not considered
in calculations as the transition is not required and is not in alignment with the provided system description.
    We do similar calculations as shown in Table 7 for the Phone system after verification (Fig. 4c). The correctness
scores for external transition, internal transition, and output are 0.8214, 0.6670, and 1.0000, respectively. We highlight
the decrease in external transition correctness score, which is evident due to higher number of correct transitions with
one incorrect transition (On → SearchingForService in Fig. 4c). We observe the significant improvement in the
internal transition correctness score.
    The results in Table. 8 highlight the comparative performance of different LLMs used as base models for the
PDEVS Specification Generator before and after verification based correction. For these experiments eight systems
(out ot 14) towards the higher end of behavioral complexity are shortlisted (explained in Appendix A). Most models
demonstrate notable improvement after verification, especially in the external transition and outputs, indicating that the
verification mechanism improves model correctness. Claude-opus-4.1 and Qwen-3-32b achieved the highest post-
verification accuracy, showing perfect or near-perfect consistency across all external, internal, and output functions. In
contrast, smaller models (Llama-3.1-8b, Ministral-3b/8b) exhibited a decline in the external transition function,
suggesting sensitivity to model scale and reasoning depth.


7. Limitations
    Although our experiments show significant improvement in the statechart generation through the proposed
controlled-correction mechanism, the approach still suffers from drawbacks. The underlying assumption for the
proposed framework is that the formulated system description contains the information needed to construct models
without any contradictions. Provided system description is the only reference for an Agent to extract the PDEVS
specifications as well an LLM call to determine the behavioral conditions. The contradicting prompt leads to an
unsatifiable set of PDEVS facts or behavioral conditions in Propositional Logic. This leads to termination of the entire
process after a pre-defined threshold for iterations (𝑚, 𝑛).
    Another major drawback is the dependency on LLMs for identifying the propositions and using them to accurately
translate natural language representations into propositional logic formulae. Even after providing clear instructions,
LLMs sometimes sway from generating accurate translations, be it the identification of propositions or formulae. This
leads to inaccurate identification of key behavioral conditions, which can cause mistakes in the generated PDEVS
statecharts. More accurate way to obtain the propositional logic translation should help reduce such cascading errors
throughout the framework.
    The use of propositional logic for verification of PDEVS specifications is a starting idea, as it removes behaviors
that should be specified in atomic, coupled, and statecharts PDEVS models. For example, the time advance property
required for internal and external transition functions should be verified temporally and modified accordingly. However,
Propositional Logic, for example, in comparison to Timed Automata, is atemporal. As a consequence, no significant
improvement in the time advance is noticed even after the controlled-correction loop.




: Preprint submitted to Elsevier                                                                              Page 18 of 21
Table 9
Descriptions of systems considered for evaluating the proposed framework.
       System                                                                    Description
      Processor                          Processes incoming jobs with a 2-second delay, transitioning between idle and busy states.
 Processor with Queue                                      Another variant of processor with a queuing mechanism.
       CarWash            A carwash that services cars and trucks with a 20-time-unit wash duration for cars and 40-time-unit for trucks; queues
                                                                   cars and denies service to trucks if busy.
        Phone            Manages power, service search, and call handling while maintaining active conversations and handling interruptions using
                                                                                  FIFO order.
        Counter                               Counts up, resets, stops, or provides the current count based on received inputs.
 Coordinator (MiniFab)                Manages overall workflow by routing jobs between machines and synchronizing their operations.
 MachineAB (MiniFab)                 Performs the initial processing steps on incoming wafers or parts before passing them downstream.
 MachineCD (MiniFab)               Handles intermediate processing tasks, often involving transformation or inspection before final stages.
  MachineE (MiniFab)                              Completes the final processing or finishing step before jobs exit the system.
      Skateboard             A skateboard that can adjust speed based on desired input, can start/stop, and reports speed every 5 minutes.
        Tracker                             Tracks routes and outputs computed waypoints or nothing based on push/pull inputs.
     BridgeSystem        A traffic light controlling the east-to-west/west-to-east direction on the bridge, alternating between green and red every
                                           50 seconds and allowing vehicles to cross within 10 seconds with a queuing mechanism.
 HummingbirdFeeder-1     A component that feeds hummingbirds of different sizes, consuming nectar at species-specific rates and requiring refilling
                                                                        when nectar drops below 2 oz.
 HummingbirdFeeder-2                               Another variant of HummingbirdFeeder with more behavioral complexity.




8. Conclusion
    Earlier works such as (Carreira-Munich et al., 2024) and (Vasa et al., 2025) proposed using LLM to for developing
and simulating Classic and Parallel DEVS models by extracting specifications and then using them as facts to
generate simulation code or and PDEVS statecharts. Without verifcation, the generated models and code are prone
to logical inconsistencies. To overcome this, we propose a logical consistency–based verification mechanism for
PDEVS plausible facts incoporating satisfiability and entailment checks for PDEVS statecharts. By translating PDEVS
specifications and behavioral conditions into propositional logic, a controlled-correction loop is designed to refine
PDEVS specifications incrementally and iteratively. This verification mechanism improves the logical alignment of
generated PDEVS statecharts with the intended system descriptions.
    The proposed PDEVS-LLM framework is evaluated through both manual correctness scoring and formal model
checking using UPPAAL’s deadlock and phase reachability applied to Timed Automata variants of the PDEVS
statecharts. Experiments across multiple publicly available LLMs demonstrated that the verification mechanism
consistently enhanced correctness, particularly in internal transitions and output functions, and improved completeness
criteria in the generated PDEVS specifications.
    Simulations often serve as digital twins of complex systems. The behavior of modular, hierarchical simulations
(PDEVS) requires input/output interactions. Although PDEVS-LLM automatically generates coupled models, it does
not have any mechanism to verify model correctness. As a part of future work, we aim to extend the PDEVS statecharts
verification for hierarchical PDEVS models. Another research direction is on developing evaluation frameworks that
can assist in identifying and correcting behavioral errors in PDEVS statecharts and coupled models.

Acknowledgments

This research is supported by Intel Corporation, Chandler, Arizona, USA. The authors would like to express their
sincere gratitude to Bharadhwaj Balasubramaniam from Intel Corporation for his fruitful discussions. The authors also
extend their appreciation to Vamsi Krishna Pendyala, Shivam Deotarse, and Kiran Venkatachalam from the Arizona
Center for Integrative Modeling and Simulation (ACIMS), Arizona State University, for their insightful discussions
on LLMs and evaluations of the PDEVS statecharts.

A. Test cases (systems) for Evaluation
    Table 9 presents the set of systems curated from PDEVS models (Zeigler and Sarjoughian, 2003; Sarjoughian,
2024; ACIMS, 2023) for evaluating the proposed framework. Their complexities can be characterized in terms of
the number of primary (phase and sigma) and secondary state variables (e.g., FIFO queue), input and output events,

: Preprint submitted to Elsevier                                                                                                   Page 19 of 21
internal and external transition functions, and output functions. For example, the Processor system operates in two
phases—Idle and Busy with two state transitions and one output function whereas the Phone system exhibits richer
behavior across five phases (Active, Off, On, Ready, and SearchingForService) with eleven state transitions, and
one output function (refer to Fig. 4a).
    For the statechart correctness evaluation, we focus on eight systems representing a relatively high level of behavioral
complexity to highlight the effect of the verification mechanism in managing intricate behavioral logic. The selected
systems are CarWash, Phone, Coordinator, MachineAB, MachineE, BridgeSystem, and HummingbirdFeeder-1
& 2. The prompts (descriptions) for these systems are provided at GitHub Repository.


References
ACIMS, 2023. DEVS-Suite Simulator, version 7.0. https://acims.asu.edu/devs-suite/, accessed 15th January 2025.
Alshareef, A., Keller, N., Carbo, P., Zeigler, B.P., 2024. Generative AI with modeling and simulation of activity and flow-based diagrams, in:
   Simulation Tools and Techniques, Springer Nature Switzerland, Cham. pp. 95–109.
AnyLogic Company, 2021. Automatic generation of simulation models using process templates, in: Proceedings of the AnyLogic Conference 2021.
Bengtsson, J., Larsen, K., Larsson, F., Pettersson, P., Yi, W., 1996. UPPAAL — a tool suite for automatic verification of real-time systems, in: Alur,
   R., Henzinger, T.A., Sontag, E.D. (Eds.), Hybrid Systems III, Springer Berlin Heidelberg, Berlin, Heidelberg. pp. 232–243.
Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J.D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S.,
   Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J., Winter, C., Hesse, C., Chen, M., Sigler, E.,
   Litwin, M., Gray, S., Chess, B., Clark, J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., Amodei, D., 2020. Language models
   are few-shot learners, in: Larochelle, H., Ranzato, M., Hadsell, R., Balcan, M., Lin, H. (Eds.), Advances in Neural Information Process-
   ing Systems, Curran Associates, Inc.. pp. 1877–1901. URL: https://proceedings.neurips.cc/paper_files/paper/2020/file/
   1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf.
Carreira-Munich, T., Paz-Marcolla, V., Castro, R., 2024. DEVS Copilot: Towards generative AI-assisted formal simulation modelling based on
   large language models, in: 2024 Winter Simulation Conference (WSC), pp. 2785–2796. doi:10.1109/WSC63780.2024.10838994.
Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H.P.D.O., Kaplan, J., Edwards, H., Burda, Y., Joseph, N., Brockman, G., et al., 2021.
   Evaluating Large Language Models Trained on Code. arXiv preprint arXiv:2107.03374 .
Chow, A., Zeigler, B., 1994. Parallel DEVS: a parallel, hierarchical, modular modeling formalism, in: Proceedings of Winter Simulation Conference,
   pp. 716–722. doi:10.1109/WSC.1994.717419.
Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., Schulman, J., 2021.
   Training verifiers to solve math word problems. URL: https://arxiv.org/abs/2110.14168, arXiv:2110.14168.
Dahmen, J., Schönemann, M., Scholz-Reiter, B., 2023. Ontology-based automatic generation of material flow simulation models. Journal of
   Intelligent Manufacturing doi:10.1007/s10845-023-02257-3.
David, I., Syriani, E., 2022. DEVS Model Construction As A Reinforcement Learning Problem, in: 2022 Annual Modeling and Simulation
   Conference (ANNSIM), pp. 30–41.
Fan, L., Li, L., Ma, Z., Lee, S., Yu, H., Hemphill, L., 2024. A Bibliometric Review of Large Language Models Research from 2017 to 2023. ACM
   Trans. Intell. Syst. Technol. 15.
Fard, M.D., Sarjoughian, H.S., 2015. Visual and persistence behavior modeling for DEVS in CoSMoS, in: Proceedings of the Symposium on
   Theory of Modeling & Simulation: DEVS Integrative M&S Symposium, Society for Computer Simulation International, San Diego, CA, USA.
   p. 227–234.
Gao, C., Lan, X., Li, N., Yuan, Y., Ding, J., Zhou, Z., Xu, F., Li, Y., 2024. Large language Models Empowered Agent-based Modeling and Simulation:
   A survey and perspectives. Humanities and Social Sciences Communications 11, 1–24.
Giabbanelli, P.J., 2023. GPT-Based models meet simulation: How to efficiently use large-scale pre-trained language models across simulation tasks,
   in: 2023 Winter Simulation Conference (WSC), pp. 2920–2931. doi:10.1109/WSC60868.2023.10408017.
isee systems inc., 2024. Stella Architect Version 4 Release Notes. isee systems. Lebanon, NH, USA. Available at: https://www.iseesystems.
   com/resources/help/v4/Content/Release_Notes.htm.
Jackson, I., Saenz, M.J., Ivanov, D., 2024. From natural language to simulations: Applying AI to automate simulation modelling of logistics systems.
   International Journal of Production Research 62, 1434–1457.
Kim, G., Baldi, P., McAleer, S., 2023. Language models can solve computer tasks. URL: https://arxiv.org/abs/2303.17491,
   arXiv:2303.17491.
Liu, J.X., Yang, Z., Schornstein, B., Liang, S., Idrees, I., Tellex, S., Shah, A., 2022. Lang2ltl: Translating natural language commands to temporal
   specification with large language models, in: Workshop on Language and Robotics at CoRL 2022.
MathWorks, 2023. Integrating AI into simulink for simulation and deployment. https://www.mathworks.com/videos/integrating-ai-
   into-simulink-for-simulation-and-deployment-1699640610671.html. Accessed 9th October 2025.
MathWorks, 2024. AI and Model-Based Design. MathWorks. Available at: https://www.mathworks.com/solutions/ai-model-based-
   design.html.
de Moura, L., Bjørner, N., 2008. Z3: An efficient SMT solver, in: Proceedings of the Theory and Practice of Software, 14th International Conference
   on Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2008), Springer. pp. 337–340. doi:10.1007/978-3-540-
   78800-3_24.
Peeperkorn, M., Kouwenhoven, T., Brown, D., Jordanous, A., 2024. Is temperature the creativity parameter of large language models? arXiv preprint
   arXiv:2405.00492 .


: Preprint submitted to Elsevier                                                                                                   Page 20 of 21
Ren, J., Wu, H., Xu, Y., 2025. SimuGen: Multimodal Agentic Framework for Automated Simulink Model Generation. https://arxiv.org/
   abs/2506.15695. ArXiv preprint arXiv:2506.15695.
Sarjoughian, H.S., 2024. Modeling & simulation theory and applications. Lecture notes, School of Computing and Intelligent Systems, Arizona
   State University, Tempe, Arizona, USA.
Sarjoughian, H.S., Gholami, S., 2015. Action-level real-time DEVS modeling and simulation. Simulation 91, 869–887.
Shrestha, S.L., Csallner, C., 2021. SLGPT: Using transfer learning to directly generate simulink model files and find bugs in the simulink toolchain,
   in: Proceedings of the 25th International Conference on Evaluation and Assessment in Software Engineering, Association for Computing
   Machinery, New York, NY, USA. p. 260–265. URL: https://doi.org/10.1145/3463274.3463806, doi:10.1145/3463274.3463806.
Shuttleworth, D., Padilla, J., 2022. From narratives to conceptual models via natural language processing, in: 2022 Winter Simulation Conference
   (WSC), pp. 2222–2233. doi:10.1109/WSC57314.2022.10015274.
Van Wyk, R., Kruger, K., 2023. Evaluating the Use of Generative AI for Automated System Dynamics Model Creation. Technical Report. University
   of Pretoria. Available at: https://repository.up.ac.za/bitstreams/eb9edb5e-e835-446b-b36a-481dce56085c/download.
Vasa, V., Sarjoughian, H., Yellig, E., 2025. Generative statecharts-driven PDEVS modeling, in: Winter Simulation Conference. https:
   //acims.asu.edu/wp-content/uploads/sites/18/2025/10/ACIMS___PDEVS_WSC2025__PrePrint.pdf.
Wu, Z., Zeng, Q., Zhang, Z., Tan, Z., Shen, C., Jiang, M., 2024. Large Language Models Can Self-Correct with Key Condition Verification. URL:
   https://arxiv.org/abs/2405.14092, arXiv:2405.14092.
Xiao, L., Hao, Y., Hanchen, Z., Yifan, X., Xuanyu, L., Hanyu, L., Yu, G., Hangliang, D., Kaiwen, M., Kejuan, Y., Shudan, Z., Xiang, D., Aohan,
   Z., Zhengxiao, D., Chenhui, Z., Sheng, S., Tianjun, Z., Yu, S., Huan, S., Minlie, H., Yuxiao, D., Jie, T., 2023. AgentBench: Evaluating LLMs as
   Agents. arXiv preprint arXiv: 2308.03688 .
Zeigler, B.P., Sarjoughian, H.S., 2003. Introduction to DEVS modeling and simulation with java: Developing component-based simulation models
   Technical Document, University of Arizona, Tucson, Arizona, USA.




: Preprint submitted to Elsevier                                                                                                   Page 21 of 21
