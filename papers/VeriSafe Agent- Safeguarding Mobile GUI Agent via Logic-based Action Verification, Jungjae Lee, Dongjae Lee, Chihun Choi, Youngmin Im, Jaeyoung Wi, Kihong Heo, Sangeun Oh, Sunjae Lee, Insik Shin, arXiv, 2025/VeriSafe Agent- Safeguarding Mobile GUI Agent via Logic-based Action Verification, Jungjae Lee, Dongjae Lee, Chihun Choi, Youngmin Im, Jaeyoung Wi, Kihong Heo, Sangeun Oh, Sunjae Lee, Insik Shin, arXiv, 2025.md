                                            VeriSafe Agent: Safeguarding Mobile GUI Agent via
                                                      Logic-based Action Verification
                                                         Jungjae Lee∗                                       Dongjae Lee∗                               Chihun Choi
                                                School of Computing, KAIST                          School of Computing, KAIST                         Korea University
                                                     Republic of Korea                                   Republic of Korea                             Republic of Korea
                                                 dlwjdwo00701@kaist.ac.kr                            dongjae.lee00@kaist.ac.kr                      clgns0102@korea.ac.kr

                                                        Youngmin Im                                         Jaeyoung Wi                                 Kihong Heo
                                                School of Computing, KAIST                          School of Computing, KAIST                  School of Computing, KAIST
arXiv:2503.18492v2 [cs.HC] 11 Sep 2025




                                                     Republic of Korea                                   Republic of Korea                           Republic of Korea
                                                    ym.im@kaist.ac.kr                                 wijaeyoung@kaist.ac.kr                      kihong.heo@kaist.ac.kr

                                                         Sangeun Oh                                          Sunjae Lee†                                 Insik Shin†
                                                      Korea University                               Sungkyunkwan University                    School of Computing, KAIST
                                                      Republic of Korea                                  Republic of Korea                           Republic of Korea
                                                   sangeunoh@korea.ac.kr                               sunjae.lee@skku.edu                           ishin@kaist.ac.kr
                                         Abstract                                                                       To the best of our knowledge, VSA is the first attempt to
                                         Large Foundation Models (LFMs) have unlocked new pos-                          bring the rigor of formal verification to GUI agents, bridging
                                         sibilities in human-computer interaction, particularly with                    the gap between LFM-driven actions and formal software
                                         the rise of mobile Graphical User Interface (GUI) Agents                       verification. We implement VSA using off-the-shelf LFM ser-
                                         capable of interacting with mobile GUIs. These agents al-                      vices (GPT-4o) and evaluate its performance on 300 user
                                         low users to automate complex mobile tasks through simple                      instructions across 18 widely used mobile apps. The results
                                         natural language instructions. However, the inherent prob-                     demonstrate that VSA achieves 94.33%–98.33% accuracy in
                                         abilistic nature of LFMs, coupled with the ambiguity and                       verifying agent actions, outperforming existing LFM-based
                                         context-dependence of mobile tasks, makes LFM-based au-                        verification methods by 30.00%–16.33%, and increases the
                                         tomation unreliable and prone to errors. To address this crit-                 GUI agent’s task completion rate by 90%–130%.
                                         ical challenge, we introduce VeriSafe Agent (VSA)1 : a formal                  CCS Concepts
                                         verification system that serves as a logically grounded safe-
                                                                                                                        • Computing methodologies → Mobile agents.
                                         guard for Mobile GUI Agents. VSA deterministically ensures
                                         that an agent’s actions strictly align with user intent before                 Keywords
                                         executing the action. At its core, VSA introduces a novel                      GUI Agent, AI Safety; Formal Verification
                                         autoformalization technique that translates natural language
                                         user instructions into a formally verifiable specification. This               ACM Reference Format:
                                                                                                                        Jungjae Lee, Dongjae Lee, Chihun Choi, Youngmin Im, Jaeyoung
                                         enables runtime, rule-based verification of agent’s actions,
                                                                                                                        Wi, Kihong Heo, Sangeun Oh, Sunjae Lee, and Insik Shin. 2025.
                                         detecting erroneous actions even before they take effect.
                                                                                                                        VeriSafe Agent: Safeguarding Mobile GUI Agent via Logic-based
                                         ∗ Co-first authors : Jungjae Lee, Dongjae Lee                                  Action Verification. In The 31st Annual International Conference on
                                         † Co-corresponding authors : Sunjae Lee, Insik Shin                            Mobile Computing and Networking (ACM MOBICOM ’25), November
                                         ∗ Co-first authors: Junjae Lee, Dongjae Lee.
                                                                                                                        4–8, 2025, Hong Kong, China. ACM, New York, NY, USA, 15 pages.
                                         † Co-corresponding authors: Sunjae Lee, Insik Shin.
                                                                                                                        https://doi.org/10.1145/3680207.3765248
                                         1 The system is available at: https://github.com/VeriSafeAgent/VeriSafeAgent


                                                                                                                        1    Introduction
                                                                                                                        The advent of Large Foundation Models (LFMs) [1–3] has
                                         This work is licensed under a Creative Commons Attribution-                    revolutionized human-computer interaction, paving the way
                                         NonCommercial 4.0 International License.
                                         ACM MOBICOM ’25, Hong Kong, China
                                                                                                                        for a new generation of agents capable of interacting with
                                         © 2025 Copyright held by the owner/author(s).                                  graphical user interfaces (GUIs) [4–13]. Among these, Mobile
                                         ACM ISBN 979-8-4007-1129-9/2025/11                                             GUI Agents stand out for their ability to automate complex
                                         https://doi.org/10.1145/3680207.3765248                                        tasks within mobile applications, reducing manual effort and
ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China                                                                J. Lee, D. Lee, et al.


enhancing user convenience. By leveraging the reasoning             3) Compounding Error Probability: Mobile tasks typically
and natural language understanding capabilities of LFMs,         comprise a sequence of actions, each requiring verification.
these agents can interpret user requests and translate them      Continuously relying on LFMs for validation at every step
into sequences of UI interactions [4, 6–8].                      increases the likelihood of accumulated errors, which can
   However, despite significant advancements, existing Mo-       ultimately degrade overall system accuracy, despite efforts
bile GUI Agents still face fundamental limitations that hin-     to improve it.
der their reliability and safety in real-world applications.        To overcome these challenges, we introduce VeriSafe Agent
One major challenge stems from the probabilistic nature          (VSA), a deterministic, logic-based verification system for
of LFMs, which can lead to unpredictable and erroneous           Mobile GUI Agents. To the best of our knowledge, this is
actions. Additionally, mobile app interactions are often am-     the first attempt to provide a reliable pre-action verification
biguous and context-dependent, making it difficult even for      mechanism grounded in logic-based reasoning rather than
state-of-the-art LFMs to generate consistently accurate ac-      existing probabilistic methods, bridging the gap between
tions [12, 14, 15]. These challenges are especially critical     probabilistic actions and deterministic safety. Specifically,
for tasks involving sensitive operations, such as financial      VSA leverages the concept of autoformalization [17], which
transactions or private communications, where errors can         automatically translates natural language user instructions
have serious or irreversible consequences. Therefore, imple-     into a formal specification. Using the translated specification,
menting robust safeguards and verification mechanisms is         VSA performs runtime verification to ensure the correctness
essential to ensuring the safe and reliable deployment of        of the agent’s actions in runtime.
Mobile GUI Agents.                                                  However, unlike conventional software verification [18–
   Recent approaches [8, 16] have attempted to mitigate these    21], which operates on predefined safety requirements, VSA
challenges by introducing reflection agents that use LFMs        faces the unique challenge of formalizing impromptu, user-
to review the actions of the primary GUI agent and pro-          defined instructions on-the-fly, across diverse and dynamic
vide feedback. However, these approaches come with signifi-      landscape of mobile applications. To accomplish this, VSA
cant drawbacks. Since reflection agents also rely heavily on     introduces three key innovations:n
LFMs, they remain susceptible to the same errors, leading           (1) Domain-Specific Language (DSL) and Developer Library1 :
to a compounding of inaccuracies. Furthermore, repeated                 A specialized language and accompanying tools tai-
LFM queries for reflection incur substantial computational              lored to dynamic nature of mobile environments. Col-
costs and latency, further limiting their practicality. These           lectively, they can encode both the natural-language
limitations highlight three key challenges inherent in relying          user instructions and corresponding UI actions as log-
solely on LFMs for verification:                                        ical formulas.
   1) Existence of Irreversible and Risky Action: One way to        (2) Intent Encoder and Verification Engine: A system that
improve verification accuracy is to analyze both the action             systematically translates user instructions into logi-
and its resulting screen state. While the app screen after              cal constraints (expressed as our DSL) and performs
the action (post-action verification) provides useful context           runtime, deterministic verification against these con-
for verification, many critical mobile actions (e.g., making a          straints.
payment, sending a message) are irreversible. In such cases,        (3) Structured Feedback Generation: A proactive mecha-
verification becomes meaningless, as the agent cannot filter            nism that provides actionable feedback to the GUI
or "undo" the erroneous actions. This fundamentally defeats             agent, before executing an action, identifying specific
the core purpose of verification, which prevents critical er-           logical violations and unmet conditions to guide the
rors before they occur. To ensure genuine safeguard against             agent toward correct task completion.
critical errors, verification must be performed before execut-
                                                                    We implement a prototype of VSA using off-the-shelf on-
ing the action (pre-action).
                                                                 line LFM service (GPT-4o) and integrate it with M3A (Mul-
   2) The Forward Assessment Problem: To Verify an agent’s
                                                                 timodal Autonomous Agent for Android) GUI agent [12].
action before its execution, it requires a forward-looking as-
                                                                 Our evaluation, conducted on 300 user instructions across 18
sessment: predicting the effect of the proposed action before
                                                                 widely used mobile applications demonstrates that with an
execution. However, this process can be as difficult – if not
                                                                 estimated ∼437 additional lines of code (LoC) per app, VSA
more difficult – than generating the action itself. Further-
                                                                 successfully verifies GUI agent actions with up to 98.33%
more, the predicted outcome aligns with the user’s overall
                                                                 accuracy, achieving a false positive rate of 1.3% and a false
goal adds another layer of complexity. Consequently, this
                                                                 negative rate of 0.3%. This significantly outperforms baseline
approach is akin to solving a simpler problem with a more
complex one, potentially turning verification into a perfor-     1 The   library is available   at:   https://github.com/VeriSafeAgent/
mance bottleneck.                                                VeriSafeAgent_Library
VeriSafe Agent                                                                 ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China


reflection agents by 23.2%. Furthermore, VSA’s structured               Software Verification for Safety-Critical Systems. Soft-
feedback, derived from logical verification results, enables         ware verification [27–36] encompasses a range of methodolo-
the GUI agent to enhance its task completion rate by 130%,           gies to ensure that software systems behave correctly accord-
a substantial improvement compared to reflection agents,             ing to specification. These formal verification techniques
which failed to correct any tasks.                                   have been widely adopted to provide strong correctness
                                                                     guarantees in safety-critical domains, including hardware
2    Background and Motivation                                       design [31], automotive systems [32], and cyber-physical sys-
Graphical User Interface (GUI) Agents. GUI Agents [4–                tems [33, 34]. Among them, dynamic verification [35] aims
10] are software programs designed to interact autonomously          to check the properties of the program or detect incorrect be-
with applications through graphical user interfaces. By inter-       haviors when the program is executed. The formal definition
preting visual and semantic information presented in GUIs            of malfunctions is written in mathematical expressions such
and simulating human interactions (e.g., clicks, swipes, and         as first-order logic, linear temporal logic, and finite-state au-
text entry), GUI agents enable automation of digital tasks           tomaton. Once the verification properties are defined, verifi-
without requiring internal access to application code or APIs.       cation can be performed by checking whether an automaton
Recent advancements in artificial intelligence, particularly         reaches an accept state or by converting the problem into a
driven by Large Foundation Models (LFMs), have signifi-              satisfiability modulo theory (SMT) problem to find satisfying
cantly enhanced the capabilities of GUI agents, enabling             variable assignments using SMT solvers [37]. In particular,
them to understand complex user instructions and inter-              runtime verification is a type of dynamic verification that
pret sophisticated mobile application GUIs. However, due             monitors the execution of a program in runtime [36]. It de-
to the inherently probabilistic nature of LFMs and often             tects anomalous behavior through systematic observation
ambiguous and under-specified nature of GUI interactions,            of program execution.
contemporary GUI agents are susceptible to incorrect ac-
tions [14, 15, 22–26], necessitating robust verification mech-       3     VeriSafe Agent (VSA): Overview
anisms to ensure reliability and safety in practical scenarios.      Inspired by the success of formal verification in other do-
   Safeguarding GUI Agents using Reflection. The cur-                mains, this work adapts techniques from software verifica-
rent practice for safeguarding GUI agents often involves             tion to solve the specific challenges of Mobile GUI Agent
the use of reflection agents, which utilize LFMs to review           safety and reliability.
the actions generated by the primary GUI agent. Reflection-              As illustrated in Figure 1, VSA is layered on top of an exist-
based approach can be broadly classified into two categories:        ing GUI agent, acting as a verification layer before the agent’s
pre-action verification and post-action verification.                proposed UI actions are injected into a mobile app. Given
   Pre-action reflection [16] evaluates a proposed action before     a user instruction, VSA translates it into a logical formula
it is executed on the mobile app. This approach serves as            representing the conditions for successful task completion.
an effective guardrail by providing an opportunity to abort          Then, when the GUI agent generates a UI action, VSA verifies
or correct erroneous actions before they occur. However, it          whether this action satisfies the pre-defined logical formula.
frequently suffers from low verification accuracy because it         If the action is verified as correct, it is passed on to the mobile
requires predicting the outcome of an action. Such inaccura-         application. If the action fails verification, VSA provides feed-
cies lead to high false negatives and positives, paradoxically       back to the GUI agent, explaining the reason for the failure
decreasing the overall system accuracy and undermining the           and guiding the agent to generate a corrected action.
intended safety benefits.                                            3.1    Challenges
   Conversely, post-action reflection [8] evaluates an action
                                                                     In doing so, VSA addresses three key challenges:
after its execution, leveraging the resulting application state
to concretely assess the correctness of the action. While this         C1. How to formally express the user’s intent and the app’s
approach significantly improves verification accuracy, it has              execution flow in logically tractable representation?
a critical limitation: it cannot prevent irreversible actions. For     C2. How to accurately translate natural language user in-
irreversible actions such as financial transactions or sending             structions into a formal representation and perform
messages, post-action verification becomes ineffective, as                 runtime verification against it?
such actions cannot be undone once they are performed.                 C3. How to effectively communicate verification results
   VSA is designed to address these limitations, providing a               back to the GUI agent in an actionable, explainable
reliable pre-action verification that is based on a logic-based            manner?
deduction instead of probabilistic reasoning.                        C1. Conventional software verification techniques typically
                                                                     rely on precise, pre-defined formal specifications of program
                                                                     behaviors. However, mobile GUI agents operate on natural
ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China                                                               J. Lee, D. Lee, et al.




                                                                                               𝑝∧𝑞 →𝑟




   (a) Traditional Mobile GUI Agent System                 (b) Mobile GUI Agent System with VeriSafe Agent integration

             Figure 1: Comparison of (a) a traditional GUI agent system and (b) VSA integrated system.

language instructions, which are inherently informal and am-        by identifying unmet or violated conditions based on the
biguous. Therefore, we need a representation system that can        logical verification results.
clearly express both the user’s intent and the corresponding        3.2    System Workflow
logical flow of the application to fulfill that intent. To ad-
                                                                    This section describes the high-level workflow of how VSA
dress this, VSA introduces a domain-specific language (DSL,
                                                                    logically verifies GUI agent actions.
§ 4.1) and an associated developer library (§ 4.2). The DSL
                                                                       App Development Phase. To enable rigorous rule-based
provides the syntax and semantics for expressing user intent
                                                                    verification, VSA requires app developers to define the criti-
as logical rules that must be satisfied. The developer library
                                                                    cal states and transitions relevant for verification using VSA
enables app developers to explicitly define the app states
                                                                    developer library (§ 4.2). This includes declaring application
and transitions required to construct these rules. Together,
                                                                    state spaces and their update mechanisms. While this re-
they allow VSA to represent both the desired behavior (user
                                                                    quires additional developer effort, typically involving 5 to
intent) and the actual behavior (app execution) in a unified,
                                                                    10 lines of code per state, and potentially more depending
logically verifiable manner.
                                                                    on the application’s complexity, such practices are already
   C2. Natural language is often vague, underspecified, and
                                                                    common in modern app development workflows [38–40].
prone to misinterpretation, making it difficult to accurately
                                                                       Intent Encoding. Given a natural language user instruc-
translate into a formal DSL suitable for logical verification.
                                                                    tion, the Intent Encoder first translates it into structured logi-
Even the most capable language models often fail to do this
                                                                    cal rules capturing essential constraints and logical depen-
without proper external guidance. To address this challenge,
                                                                    dencies within the user instruction. For example, an instruc-
VSA employs a self-corrective encoding approach (§ 5.1) that
                                                                    tion "Book tickets to the movie M at 7 pm" can be conceptually
enables the language model to iteratively refine its transla-
                                                                    translated into the following logical rule:
tion based on syntactic and semantic checks. Furthermore,
to achieve efficient yet robust verification, VSA provides a                  MovieInfo(title=“M”, time=7pm) → Book
two-tiered verification strategy (§ 5.2), adjusting verification    where each constraint (e.g., title=“M”, time=7pm) is a condi-
intensity according to the action’s significance.                   tion must be satisfied before booking the ticket.
   C3. Simply flagging an action as incorrect is insufficient          Verification. When the GUI agent generates a UI action,
for improving the overall practicality of Mobile GUI Agents.        the VSA developer library (§ 4.2), embedded within the mo-
To enhance their accuracy and reliability, we must provide          bile application, intercepts the action and returns the antici-
actionable feedback that correctly guides agents toward the         pated state transition that would result from the execution of
goal. However, LFM-generated feedback is often vague, un-           this action. The Intent Verifier (§ 5.2) then evaluates whether
derspecified, or even incorrect, potentially leading to re-         this state transition is valid according to the logical rules
peated errors or suboptimal actions. Therefore, VSA incorpo-        generated earlier. For example, if the state transition indi-
rates a structured feedback generation mechanism (Figure 6)         cates that the name of the restaurant is ‘S’ instead of ‘R’,
that systematically generates precise, rule-based feedback          the IsNameR Boolean variable would be evaluated to False,
VeriSafe Agent                                                                       ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China


indicating that the action is invalid and we can’t proceed to                  Specification      F     Rule∗
Reserve.                                                                       Rule               F     Pred ∧ . . . ∧ Pred → Objective
   Feedback Generation. Based on the verification result,                                         |     Pred ∧ . . . ∧ Pred → Done
VSA provides structured feedback to the GUI agent. If verifi-                  Pred               F     Objective | StatePred(Constraint∗ )
cation succeeds, the action is passed on to the mobile app for                 Constraint         F     Variable Operator Constant
execution, and Feedback Generator (Figure 6) guides subse-
                                                                               Constant           F     String | Number | Boolean
quent actions. If verification fails, the action is discarded, and
                                                                                                  |     Date | Time | Enumeration
Feedback Generator explains precisely which predicates or
constraints were unmet, guiding the agent toward generating                    Operator           F     =|≠|≃|>|≥|<|≤|⊆|⊈
a correct action.
   This workflow continues until either the task reaches a                          Figure 2: Simplified syntax of our DSL
final state or the GUI agent explicitly terminates the task de-
spite feedback, resulting in task failure. Through this system-           𝑅1 :RestaurantInfo(name = “R”)
atic approach, VSA ensures that Mobile GUI Agents adhere                       ∧ ReserveInfo(date = Today, time < 19:00, available = True)
to the logical constraints defined by user instructions while                  → Reserve
interacting with mobile applications.
                                                                          𝑅2 :Reserve ∧ ReserveResult(success = True) → Done
4     Domain-Specific Language
                                                                          𝑅3 :RestaurantInfo(name = “R”)
This section details the domain-specific language (DSL) and
                                                                               ∧ ReserveInfo(date = Today, time < 19:00, available ≠ True)
the associated developer library. DSL and developer library
are the basis for formally representing user instructions and                  → Done
GUI agent actions. Throughout the remainder of this paper,                Figure 3: Specification for the instruction “Reserve
we illustrate VSA using the running example: "Reserve restau-             restaurant R before 7 PM. If the restaurant is not avail-
rant R before 7 PM. If the restaurant is not available at that            able at that time, do nothing.”
time, do nothing."                                                        predicates and objectives of the other rules. State predicates
4.1     Design of Domain-Specific Language                                specify the conditions that must hold in the application for
                                                                          the intermediate step to be achieved. When the objective of
We first clarify the formal syntax and semantics of our DSL,
                                                                          another rule is used as a predicate, it establishes a precedence
which enables the formal representation of the user intent
                                                                          relationship between rules. A rule is satisfied if all predicates
and desired app execution flow. Our DSL is designed to flex-
                                                                          hold. If a rule ends with Done and such a rule is satisfied,
ibly express a wide range of constraints, execution flows,
                                                                          the task is considered complete.
and conditional branches found in natural language user
                                                                             State Predicate. State predicates represent abstract states
instructions.
                                                                          of applications. They ignore overly specific information (e.g.,
4.1.1 Syntax and Semantics. Inspired by logic programming
                                                                          size of buttons) and represent only the information important
languages (e.g., Datalog [41] and Prolog [42]), our DSL is
                                                                          for verification. A state predicate 𝑝 takes the form 𝑝 (𝑐 1, . . . , 𝑐𝑛 ),
structured around Horn clauses. A Horn clause refers to a
                                                                          where each 𝑐𝑖 is a constraint. Each constraint allows us to
logical formula with the specific structure 𝑝 1 ∧𝑝 2 ∧· · ·∧𝑝𝑛 →
                                                                          express a target state precisely. For example, a state predi-
𝑜, where 𝑝 1, 𝑝 2, . . . , 𝑝𝑛 , 𝑜 are predicates evaluating to boolean
                                                                          cate of RestaurantInfoResult can have constraints on restau-
values. Horn clauses are optimized for representing objective
                                                                          rant_name, location, and cuisine_type.
attainment conditions and execution flow, commonly used
                                                                             Constraint. A constraint 𝑐 has the form 𝑣𝑎𝑟 𝑜𝑝 𝑐𝑜𝑛𝑠𝑡
in program verification [43–46]. Each Horn clause signifies
                                                                          (e.g., 𝑥 = 10), where 𝑥 is a variable representing a specific
that the preconditions for 𝑜 to be satisfied are 𝑝 1, 𝑝 2, . . . , 𝑝𝑛 .
                                                                          element within the application state (e.g., restaurant_name,
The formal syntax of our DSL is summarized in Figure 2.
                                                                          location). 𝑜𝑝 is a comparison operator, and 𝑐𝑜𝑛𝑠𝑡 represents
   Specification and Rule. In our DSL, a single user instruc-
                                                                          a constant value. The expression 𝑥; 𝑜𝑝; 𝑐𝑜𝑛𝑠𝑡 returns true if
tion is expressed as a set of Horn clauses called specification.
                                                                          the variable 𝑥 meets the condition defined by the operator 𝑜𝑝
Each Horn clause is called a rule, which represents a list of
                                                                          and the constant 𝑐𝑜𝑛𝑠𝑡. If 𝑥 has not been observed in the app,
predicates (preconditions) and the objective to be achieved
                                                                          it defaults to undefined, making the constraint always false.
(conclusion). Rules break down a user instruction into mul-
                                                                          The variable 𝑥 can be one of the following six types: string,
tiple smaller steps, making it easier to verify complex in-
                                                                          number, Boolean, enumeration, date, and time. For example,
structions incrementally. Each rule consists of predicates
                                                                          given a constraint 𝑥 ≥ 10, if the value of the variable 𝑥 was
and an objective which represent the precondition and inter-
                                                                          observed to be 15 in the application, then the constraint is
mediate step, respectively. Predicates are composed of state
                                                                          considered true.
ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China                                                              J. Lee, D. Lee, et al.


4.1.2 Running Example. Consider our running example of             for rule-based logical verification—a level of precision that
reserving a restaurant. The instruction is translated into the     is unattainable with automated approaches like static code
specification shown in Figure 3. RestaurantInfo is a pred-         analysis or LFM-driven dynamic analysis.
icate that represents conditions on information about the             Furthermore, this approach aligns with established prac-
restaurant you want to reserve, with the constraint that the       tices in modern mobile app development. Frameworks like
name must be “R”. ReserveInfo is information about the             React Native (state management [38]), Android’s Jetpack
reservation, with the selected date, time, and availability as     Compose (state hoisting [39]), and iOS’s SwiftUI (@State [40])
constraints. The first rule, 𝑅1 , means to make a reservation      all encourage developers to manage app state and transitions.
if the restaurant name is “R” and the reservation is avail-        By closely mirroring these familiar paradigms, VSA ensures
able before 19:00 today. The second rule, 𝑅2 , indicates task      seamless, intuitive, and minimally invasive integration into
completion if the reservation is confirmed to be successful.       standard app development workflows.
The last rule, 𝑅3 , represents another task completion if the      4.2.1 States Definition. A state, in the context of the VSA
reservation is not available before 19:00 today.                   Library, is characterized by a set of typed variables (as de-
   Notice that the objective Reserve of rule 𝑅1 appears as a       fined in § 4.1.1) that capture essential details relevant to the
predicate in rule 𝑅2 . This signifies that 𝑅1 must be satisfied    application’s current context—each variable corresponds to
before proceeding to 𝑅2 .                                          the constraint of the state predicate. Each state definition
   Specification is dynamically evaluated during the agent’s       includes i) name, ii) description, and iii) variables:
interaction with the application. Initially, all variables 𝑥 are      Developers can define these states using an external JSON
considered undefined. The values of these variables are up-        file or provided APIs (i.e., defineState()):
dated at runtime by the state transitions caused by the GUI          {
agent’s actions. These updates are governed by pre-defined               " name " : " RestaurantInfo " ,
state update methods written in the developer library (see               " description " : " Information about the
§ 4.2). Whenever a variable’s value changes, the associated                   restaurant you want to reserve . " ,
constraint is re-evaluated.                                              " variables " : [ { " name " : " String " } ]
   For example, consider the ReserveInfo predicate. If the           }
GUI agent attempts to reserve restaurant “R” at 18:00 today,       These defined states are then used as candidate state pred-
the update rule will set the values of the date and time vari-     icates when VSA’s Intent Encoder (§ 5.1) translates user
ables to Today and 18:00, respectively. When we evaluate           instruction into a specification.
the constraints against the updated variables, date=Today          4.2.2 Pre-action State Update Triggers. VSA enables devel-
and time<19:00 will both be true. If availability is observed      opers to define triggers specifying when and how state vari-
to be true in the app state after selection, all constraints of    ables are updated. Triggers correspond directly to mean-
the ReserveInfo predicate are true, and the predicate itself       ingful state transitions within the mobile application. Most
becomes true. This runtime evaluation of the specification         triggers are associated with UI interaction handlers (e.g.,
allows VSA to continuously monitor the agent’s progress            onClickListener) or critical points in the application logic.
and verify whether its actions are leading the application            Triggers return the expected state update before execut-
toward a state that satisfies the user’s intent.                   ing the action. The returned update is used to verify the
4.2    Developer Library                                           action. This ahead-of-time update provides two key benefits:
                                                                   i) It prevents irreversible actions (e.g., financial transaction,
To effectively generate specification from a user instruction
                                                                   sending a message) from being executed if they violate the
and evaluate it against agent’s actions, VSA requires a defi-
                                                                   user’s intent; ii) It allows the GUI agent to easily retry with
nition of two key components: (i) the set of candidate state
                                                                   a different action without having to revert the effects of a
predicates (i.e., the application’s state space) that serve as
                                                                   previous, incorrect action (e.g., deleting incorrect text input).
building blocks for the specification, and (ii) the mechanisms
                                                                      To facilitate pre-action updates, the VSA developer library
through which each predicate’s constraint variables 𝑥 are
                                                                   provides wrapper listeners for common UI input handlers.
updated during app execution (i.e., state transitions).
                                                                   These wrappers intercept user interactions and update the
   To this end, VSA provides a developer library that empow-
                                                                   relevant state variables according to the developer-defined
ers app developers to explicitly define application states (as
                                                                   logic before executing the original event handler’s code. The
state predicates) and their corresponding update mechanisms
                                                                   original ‘onClick’ code which performs the actual opera-
(as state transitions). This approach capitalizes on developers’
                                                                   tion is executed only if the verification succeeds. For example,
deep understanding of their application’s internal logic and
                                                                   consider the ‘RestaurantInfo’ state predicate defined earlier.
intended behavior. Although it requires additional developer
effort, it enables highly accurate state definitions suitable
VeriSafe Agent                                                               ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China


A developer could associate a trigger with the search button’s      optimize the LFM-based autoformalization method in the
click listener as follows:                                          context of mobile agents to automatically convert instruc-
searchButton . VSAOnClickListener (() -> {
                                                                    tions into specifications written in our DSL. Relying solely
  vsaStateManager . updateState ( " RestaurantInfo " , {            on LFM’s output poses risks due to their probabilistic nature
        " name " : searchTextField . getText () ,                   and potential for hallucinations. To address this limitation,
     }) ;                                                           we applied self-corrective encoding, which corrects errors au-
     /* existing code for onClickListener */                        tomatically, and experience-driven encoding techniques that
  }) ;                                                              gradually adapt to each app.
                                                                    5.1.1 Self-Corrective Encoding. To ensure the encoded spec-
   Another key advantage of developer-defined state predi-
                                                                    ification is correct and includes all relevant constraints, VSA
cates is the control over granularity. In many mobile tasks,
                                                                    employs two complementary self-corrective techniques: (i)
individual atomic actions are not inherently meaningful. For
                                                                    rule-based syntax checking, and (ii) decoding-based seman-
example, in an e-commerce application, entering individual
                                                                    tics checking. These methods allow the LFM to incrementally
fields of a shipping address (street, city, zip code) is a set of
                                                                    identify, correct, and refine its translations, improving accu-
preparatory steps. The critical state change is the submission
                                                                    racy and reliability.
of the complete address. Verifying every single atomic action
                                                                       As an initial step, the Intent Encoder prompts the LFM with:
would be inefficient and could mislead LFMs to think that
                                                                    i) the user’s natural language instruction and ii) the set of
some steps are incomplete. By allowing developers to strate-
                                                                    developer-defined states (from the developer library). From
gically define verification checkpoints that have a meaning-
                                                                    this information and user instruction, the Intent Encoder
ful impact on the task’s execution, VSA can significantly
                                                                    generates a draft specification representing the user’s intent
improve the efficiency and accuracy of task verification.
                                                                    using available states. The draft specification then undergoes
4.2.3 Post-action State Update Triggers. While pre-action           two checking stages:
verification is ideal for preventing errors, some action out-          Rule-based Syntax Checking. Inspired by conventional
comes are inherently unpredictable (e.g., the result of a net-      programming languages, VSA checks that the generated
work request). For these scenarios, VSA supports post-action        Specification strictly adheres to the DSL’s syntax (§ 4.1.1)
state updates. Developers can call the ‘updateState()’ API          and that the types of constants 𝑐 used within the Specifica-
directly, often within asynchronous callbacks, to update the        tion are consistent with the types of variables declared in
state after the outcome of an action is known. This allows          the developer-defined states. For example, if the LFM gen-
developers to handle dynamic application behaviors and real-        erates a state predicate like RestaurantInfo(name ≥ 100)
world uncertainties such as network delays, asynchronous            while the type of the name variable is defined as ‘String’
operations, error conditions, and dynamically determined            in the developer library, this inconsistency is immediately
content.                                                            flagged as a syntax error. If an error is detected, a structured
   For instance, consider a flight booking app where the            error message is returned to the encoding LFM as feedback,
price and availability of flights change dynamically based          guiding it toward a corrected translation.
on real-time data. A developer can define a FlightSearchRe-            Decoding-Based Semantics Checking. To further vali-
sult state with variables for price, availability, and departure    date the semantic correctness of the translation, the gener-
time. They can then associate a state update trigger with the       ated Specification is decoded back into a natural language
asynchronous network callback that gets executed when the           description using a separate decoder LFM. A checker LFM
user clicks the “Search” button. Upon receiving the network         then compares this decoded description to the original user
response, the developer-defined trigger logic updates the           instruction, confirming that the encoding genuinely captures
FlightSearchResult based on the actual results. If the net-         the user’s intent rather than merely manipulating symbols.
work fails or no seats are available, the trigger can handle        If discrepancies are found, the checker LFM identifies the
these conditions appropriately, updating the state to reflect       root cause and provides feedback to the encoding LFM.
the error or unavailability. This ability to embed complex,            These complementary checking mechanisms significantly
conditional logic directly into the verification framework          improve the robustness and accuracy of the intent encoding
enables VSA to handle a wide range of user requirements             process, effectively mitigating risks associated with solely
and edge cases.                                                     relying on probabilistic LFM outputs.
5 Verification Engine                                               5.1.2 Experience-driven Encoding. Although Self-corrective
                                                                    Encoding significantly enhances translation accuracy, it oc-
5.1 Intent Encoder                                                  casionally produces hallucinations when presented with an
Natural language instructions cannot be directly used for           enormous number of candidate state predicates.
formal verification; a formalization process is required. We
ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China                                                                    J. Lee, D. Lee, et al.


   To address this challenge, VSA introduces an Experience-          F1 : "To perform Reserve, 1. RestaurantInfo that represents
driven Encoding, which leverages previously successful en-           Information about the restaurant you want to reserve should have
codings to guide subsequent translations. When an instruc-           ‘name’ equal to “R”; 2. ReserveInfo that represents reservation details
                                                                     should have ‘date’ equal to “Today” and ‘time’ less than 19:00, and
tion is successfully translated and verified, its result spec-
                                                                     ‘available’ equal to True. So far, you have achieved step 1."
ification is cached. Since a single specification consists of
multiple rules representing an instruction’s intermediate ob-        F2 : "To complete the task, 1. perform Reserve 2. ReserveResult that
jectives, numerous instructions for the same application may         represents reservation result should have ‘success’ equal to "True"."
share similar rules. By retrieving and prioritizing predicates
                                                                     F3 : "To complete the task, 1. RestaurantInfo that represents
based on past encoding experience, we can significantly re-
                                                                     Information about the restaurant you want to reserve should have
duce the search space for the LFM encoder, improving both
                                                                     ‘name’ equal to “R”; 2. ReserveInfo that represents reservation details
efficiency and consistency.
                                                                     should have ‘date’ equal to “Today” and ‘time’ less than 19:00, but
5.2    Intent Verifier                                               ‘available’ not equal to True. So far, you have achieved step 1."
The verification process is straightforward. When the GUI            Figure 4: An example of roadmap feedback. Each 𝐹𝑖
agent generates an action, the associated state updates (de-         corresponds to Rule 𝑅𝑖 in the Specification
fined via the developer library, § 4.2) are triggered. They
update the values of the variables 𝑥 of the corresponding
constraints and state predicates in the Specification. After
each update, the affected predicates are re-evaluated to a
new truth value.                                                        When the GUI agent generates a critical action, VSA checks
   Based on this basic mechanism, VSA performs two levels            for the complete satisfaction of the conditions required to
of verification: Predicate-level Verification at the predicate       achieve a specific Objective 𝑜. If any predicate in the corre-
level and Rule-level Verification at the rule level.                 sponding rule is unsatisfied, the action is considered invalid
   Predicate-level Verification is performed at every state          and blocked. Hard feedback is provided to the agent, detailing
update. Whenever a state predicate within the Specification          the specific unmet conditions. This prevents the execution
is re-evaluated due to a variable update, its truth value is         of potentially irreversible or incorrect actions that would
checked. If a predicate evaluates to false, this indicates a po-     definitively violate the user’s intent.
tential violation of the user’s intent. For example, if the Speci-      This two-tiered verification approach guides the agent
fication includes the predicate RestaurantInfo(name = “R”),          toward its objectives while ensuring the safe execution of
and the agent’s action causes the name variable to be up-            high-risk actions.
dated to “S”, the predicate would evaluate to false, indicating      6    Structured Feedback Generator
a potential violation of user intent.
                                                                     The effectiveness of a verification system hinges not only
   It is important to note that an incorrect predicate at this
                                                                     on error detection but also on its ability to guide the agent
stage does not necessarily mean a definitive error because
                                                                     towards correct behavior. This section explains how VSA
the updated state may represent an intermediate step neces-
                                                                     generates structured feedback based on verification results.
sary to eventually reach the final, correct state. For example,
                                                                     VSA provides three distinct types of feedback: i) Roadmap
when buying three apples, the number of apples might be in-
                                                                     Feedback, ii) Predicate-level Soft Feedback, and iii) Rule-level
cremented one at a time. Each intermediate update (1 apple,
                                                                     Hard Feedback.
then 2 apples) would result in a false value for a predicate
                                                                     Roadmap Feedback. VSA provides roadmap feedback that
requiring three apples, until the final update.
                                                                     outlines the overall path toward task completion regardless
   Therefore, upon detecting a failed verification, VSA re-
                                                                     of verification outcome. Because the logical Specification
verts the predicate update and provides the GUI agent with
                                                                     of VSA explicitly encodes the preconditions required for
soft feedback (Figure 6). This feedback serves as a warning,
                                                                     achieving the user’s objective, it naturally serves as a com-
indicating a potential deviation from the intended path, and
                                                                     prehensive guideline for the GUI agent.
encourages the agent to double-check its subsequent actions.
                                                                        Specifically, the Feedback Generator converts each rule
   Rule-level Verification is performed at irreversible or
                                                                     in the Specification into a natural language explanation, de-
critical checkpoints within the task execution. To identify
                                                                     tailing which predicates must be satisfied for each objective.
these checkpoints, we modified the GUI agent’s prompt so
                                                                     These explanations incorporate developer-defined descrip-
that it generates a critical flag along with the action if that
                                                                     tions for each state predicate, constraints, and currently sat-
action is intended to directly achieve one of the objectives 𝑜
                                                                     isfied predicates. For example, Figure 4 demonstrates the
within the Specification (e.g., Reserve).
                                                                     roadmap feedback for the restaurant reservation scenario
                                                                     after successfully searching for restaurant “R”.
VeriSafe Agent                                                                ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China


Unlike approaches relying on ambiguous action histories or         studies, we set a similarity threshold of 0.7 to determine
abstract planning, this structured guidance clearly commu-         equivalence.
nicates both current progress and next objectives.
   Predicate-level Soft Feedback. When predicate-level
                                                                   8     Evaluation
verification fails (i.e., a state predicate evaluates to false),   In this section, we evaluate the performance of VSA against
VSA provides feedback indicating that the agent’s action           baseline guardrail frameworks in terms of i) verification accu-
may be incorrect. This feedback includes a description of          racy, ii) feedback effect, and iii) latency and cost. Throughout
the desired state for the violated predicate, allowing the         the experiments, we integrated each framework, including
agent to reconsider its action. Because predicate-level errors     VSAwith the M3A mobile GUI agent [12]—a simple yet pow-
could represent intermediate steps rather than genuine er-         erful mobile GUI agent powered by GPT-4o—and conducted
rors (as described in § 5.2), soft feedback is advisory rather     evaluations using a Google Pixel 8 smartphone.
than strictly prohibitive. If the GUI agent generates the same        Baselines & VSA Variants. To evaluate VSA, we compare
action even after receiving the feedback, VSA permits the          it with two LFM-based reflection schemes: Pre-action reflec-
action, acknowledging its non-critical nature.                     tion [16] and Post-action reflection [8], both of which utilize
   Rule-level Hard Feedback. For critical actions subject to       GPT-4o as their backbone LFM. For VSA, we evaluate two
rule-level verification, VSA provides comprehensive feedback       variants: VSA-cold and VSA-warm. VSA-cold encodes user
at the rule level, detailing all state predicates that remain      instructions solely using self-corrective encoding, without
unfulfilled. Unlike soft feedback, if the GUI agent generates      cached memory. On the other hand, VSA-warm leverages
the same action again after receiving hard feedback, VSA will      both self-corrective encoding and experience-driven encod-
not allow the action to proceed. Instead, it enforces that all     ing, assuming that a cached list of candidate predicates is
required state predicates must be satisfied before permitting      available for the given instruction (see § 5.1 for details).
the critical action to be executed.                                8.1     Dataset
   Through these structured, deterministic feedback mecha-
                                                                   To comprehensively evaluate VSA, we constructed a dataset1
nism, VSA effectively guide GUI agents toward correct task
                                                                   of 300 user instructions, divided into two complementary
completion, significantly outperforming existing reflection-
                                                                   subsets of 150 instructions each: the Correct dataset and the
based methods. By eliminating ambiguity and providing
                                                                   Wrong dataset.
clear, actionable guidance grounded in formal logic, VSA
                                                                      Each instruction is paired with an execution path—a se-
enhances the reliability, safety, and practicality of automated
                                                                   quence of UI actions performed by the GUI agent. In the
mobile task execution.
                                                                   Correct dataset, instructions are matched with execution
7    Implementation                                                paths that accurately fulfill the user’s intent. In contrast,
Our VSA implementation is designed as a modular compo-             the Wrong dataset deliberately introduces mismatches be-
nent that can be seamlessly integrated with existing GUI           tween instructions and their corresponding execution paths.
agents without requiring modifications to their underlying         Specifically, we altered key details in the original Correct
architecture. VSA is implemented using Python, and its In-         instructions to create discrepancies. For example, "On Play
tent Encoder leverages off-the-shelf LFM GPT-4o.                   Books, turn to the search page and check for top-selling books"
   Developer Library Guidelines. Developers should care-           was modified to "On Play Books, turn to the search page and
fully determine the granularity of State Predicates to suit        check for newly released books", making the original execu-
their application context. Overly fine-grained State Predi-        tion path no longer satisfy the updated instruction. Such
cates can make the encoded specification too detailed, in-         cases test the verification framework’s ability to detect er-
creasing the false positive rate. Conversely, coarse-grained       rors, enabling evaluation of both True Positives (correctly
State Predicates may introduce loopholes in the encoded            rejecting invalid executions) and False Negatives (incorrectly
specification, leading to a higher false negative rate. To as-     accepting invalid executions).
sist with finding the sweet spot, the VSA Library provides            Of the 150 unique instructions, 125 were sampled from the
detailed documentation and guidelines on how to effectively        LlamaTouch dataset [15], selected based on app popularity
define State Predicates. Given the potential severity of false     (global usage), instruction realism (likelihood of real-world
negatives, it’s recommended to begin with a fine-grained           occurrence), and current app availability. We excluded tasks
verification first and then iteratively refine the predicates to   that were overly localized, deprecated, or overly specific and
minimize false positives.                                          prone to overfitting. The remaining 25 instructions were
   String Similarity. To compare strings semantically rather       newly created to form the Challenge dataset, designed to
than structurally, we use OpenAI’s text-embedding-3-small          1 The   dataset   is   available   at:   https://github.com/VeriSafeAgent/
model [1] and compute cosine similarity. Based on empirical        VeriSafeAgent
ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China                                                                                                                                                                          J. Lee, D. Lee, et al.


                                                                          Pre-action Reflection                     Post-action Reflection            VSA-Cold              VSA-Warm
                                                      (a) LlamaTouch Dataset                                                                                                           (b) Challenge Dataset
      100                 95.6
                                 99.2
                                                      94.5
                                                             98.4               96.8 100.0                   95.6
                                                                                                                    99.0           100                            94.0                                             96.0 95.8                          94.1
                                                                                                                                                                                              92.0                                             88.9
       90          86.0                        87.4                                                   84.7                          90                     88.0                                      85.7
                                                                    83.2 82.2                                                                                                          82.7
       80   73.2                                                                               73.7                                 80
       70                               66.2                                                                                        70
(%)




                                                                                                                                                    62.0                        60.9                                                    59.6
       60                                                                                                                           60                                                                      58.3
       50                                                                                                                           50       44.0                                                                                46.2
       40                                                                                                                           40
                                                                                                                                                                         31.6
       30                                                                                                                           30
                   Accuracy                    Precision                  Recall                      F1 Score                                      Accuracy                    Precision                    Recall                     F1 Score

                                                                                             Figure 5: Verification accuracy

push the system to its limits with longer action sequences,                                                                                    Error Type                                Variant             LlamaTouch                 Challenge
multiple constraints, and conditional branches. Spanning 9                                                                                                                             VSA-Cold                     76/250                     24/50
                                                                                                                                      Overall Missing Predicate
different applications, these instructions average 19.16 steps                                                                                                                         VSA-Warm                     24/250                     14/50
(maximum 40), far exceeding LlamaTouch’s average of 5.67                                                                                                                               VSA-Cold                     10/250                      3/50
                                                                                                                                     Critical Missing Predicate
steps.                                                                                                                                                                                 VSA-Warm                     3/250                       2/50
   Finally, as described in § 4.2, VSA relies on developer-                                                                                                                            VSA-Cold                      7/250                      4/50
                                                                                                                                         Superfluous Predicate
defined state specifications and state-update triggers. To                                                                                                                             VSA-Warm                      0/250                      0/50
emulate this in closed-source mobile apps, we manually an-                                                                               Constraint Mismatch
                                                                                                                                                                                       VSA-Cold                      8/250                     11/50
notated state predicates and state transitions for each GUI                                                                                                                            VSA-Warm                      4/250                      6/50
screen and action in the dataset. This manual annotation                                                                                     Table 1: VSA predicate translation accuracy
serves as a surrogate for direct integration with the devel-
oper library, effectively replicating the library’s intended                                                                       runtime analysis) is beyond this paper’s scope (§ 10), these
functionality.                                                                                                                     results underscore its promise.
                                                                                                                                      An interesting observation is the high recall of Pre-action
8.2         Verification Accuracy                                                                                                  Reflection on the Challenge Dataset. However, this comes
Figure 5 presents the verification accuracy of different verifi-                                                                   at the cost of a high false positive rate (72%), leading to
cation methods, evaluated using standard metrics: Accuracy,                                                                        excessive error flagging when instructions become complex.
Precision, Recall, and F1 Score. Notably, VSA consistently                                                                         While this increases the chance of detecting any error, the
outperforms reflection-based methods across all metrics and                                                                        likelihood that a flagged action is truly erroneous remains
datasets, achieving near-perfect accuracy on the LlamaTouch                                                                        low (low precision).
dataset.                                                                                                                              Predicate Translation Accuracy. To gain deeper insight
   For simple tasks in LlamaTouch dataset, post-action re-                                                                         into the verification results, we further evaluated VSA at
flection achieves significantly higher accuracy compared to                                                                        the state predicate level. We manually constructed a ground-
pre-action reflection. This is because it leverages the action’s                                                                   truth set of predicates 𝑃𝐺𝑇 for each instruction and compared
resulting screen as additional context for verification. How-                                                                      it against 𝑃𝑆𝑝𝑒𝑐 generated by VSA.
ever, it has critical limitations: it cannot correct irreversible                                                                     VSA’s Verification errors fall into three categories: 1) Miss-
actions. Moreover, our results indicate that this advantage                                                                        ing Predicate — necessary predicates absent from the speci-
diminishes significantly as instructions become more com-                                                                          fication, potentially allowing incorrect behaviors (False Neg-
plex and involve longer action sequences (as seen in the                                                                           atives); 2) Superfluous Predicate — unnecessary predicates
Challenge dataset). This trend highlights the compounding                                                                          included, potentially rejecting correct behaviors (False Posi-
effect of errors stemming from over-reliance on LLMs for                                                                           tives); 3) Constraint Mismatch — correct predicate but with
verification.                                                                                                                      inaccurate constraints, which can cause both False Negatives
   In contrast, VSA performs pre-action verification while                                                                         and False Positives.
maintaining high performance across both datasets, thanks                                                                             Table 1 shows the counts of such errors. Note that Overall
to its design that encodes the specification once and performs                                                                     Missing Predicate counts all predicates absent relative to 𝑃𝐺𝑇 ,
subsequent verification in a rule-based manner, regardless                                                                         which defines the maximal set of possible predicates (includ-
of task complexity or length. Notably, VSA-Warm achieves                                                                           ing semantically overlapping ones). In practice, VSA tends
near-perfect results on LlamaTouch and significantly outper-                                                                       to select a minimal set of core constraints, which can lead
forms all baselines on Challenge, highlighting the benefit of                                                                      to an overestimation of “missing” predicates. We therefore
a well-constructed predicate memory. While building such a                                                                         also report Critical Missing Predicates, which are those whose
memory (e.g., via offline exploration, user demonstrations,                                                                        absence directly affects verification results.
VeriSafe Agent                                                                                                                                                 ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China


                      Pre-action Reflection             Post-action Reflection              VSA-Cold             VSA-Warm                                          Success without Feedback              Success with Feedback
                                                                            100                  100                  100
               100
                                                    94 96              96                   96                   96




                                                                                                                            The number of instructions
                                     94                                                                                                                  20
               90               88
                                                                                                                                                                                                                        13
               80                                                                                                                                        15                                                9
Accuracy (%)




                                                                                                                                                                                 0            0
               70                                                                                                                                        10
                           62                  60                                      60
               60                                                 58                                        58                                                    10            10            10           10           10
                                                                                                                                                         5
               50
                      44                  44                 44                   44                   44                                                0
               40                                                                                                                                                Agent       Pre-action   Post-action   VSA-Cold    VSA-Warm
                      Majority at 1       Majority at 3      Majority at 5        Majority at 7        Majority at 9                                          w/o feedback   Reflection   Reflection

           Figure 6: Verification accuracy with Majority-at-N                                                                                            Figure 7: Effect of feedback on task completion

                                                                                                                            logic-based feedback generation against the LLM-based feed-
   A key observation is that VSA-Warm significantly reduces
                                                                                                                            back used in reflection methods.
both missing and superfluous predicates. This demonstrates
                                                                                                                               We instructed the M3A GUI agent to execute 25 challeng-
that predicate memory effectively improves translation accu-
                                                                                                                            ing instructions from our Challenge dataset. Initially, without
racy by narrowing the search space for necessary predicates.
                                                                                                                            external feedback, M3A successfully completed only 10 of 25
Furthermore, the distribution of errors across all three types
                                                                                                                            tasks (40% success rate). We then integrated each verification
indicates that, despite VSA’s strong overall verification per-
                                                                                                                            system with M3A and re-executed the failed instructions to
formance, residual risks from predicate translation remain. In
                                                                                                                            observe whether the feedback can correct the previously
the Discussion section, we propose complementary policies
                                                                                                                            failed tasks.
to mitigate these risks and further enhance VSA’s safety.
                                                                                                                               Figure 7 summarizes the results. Notably, Neither pre-
   Randomness Mitigation. Although VSA issues only a
                                                                                                                            action nor post-action reflection corrected any previously
single LFM query per task, repeated verification of the same
                                                                                                                            failed tasks. In contrast, VSA-Cold corrected 9 of 15 failures
instruction may yield inconsistent results due to the stochas-
                                                                                                                            (60%), and VSA-Warm corrected 13 of 15 (86%). The two
ticity of LFMs. The same inconsistency applies to all methods
                                                                                                                            remaining failures under VSA-Warm were due to unconven-
that invoke an LFM, including reflection-based approaches.
                                                                                                                            tional app designs rather than misunderstanding of context.
To mitigate this randomness, we employ a majority-voting
                                                                                                                            For instance, one clock application required time input as a
scheme that repeats verification 𝑁 times and returns the
                                                                                                                            single numerical sequence (e.g., "143000" for 14:30:00) rather
majority decision (Majority-at-𝑁 ).
                                                                                                                            than separate hour, minute, and second components. Such
   Figure 6 reports accuracy on 50 instructions from the Chal-
                                                                                                                            unconventional interfaces could limit VSA’s ability to pro-
lenge dataset as 𝑁 increases. Reflection-based schemes show
                                                                                                                            vide meaningful feedback. Nevertheless, given that M3A
limited gains and remain less accurate overall, whereas both
                                                                                                                            employs GPT-4o—one of the most capable LLMs—achieving
VSA-Cold and VSA-Warm improve substantially, reaching
                                                                                                                            this performance improvement through systematic harness
96% and 100%, respectively.
                                                                                                                            demonstrates VSA’s effectiveness.
   This performance disparity stems from differences in veri-
                                                                                                                               VSA’s superior performance stems from its ability to gen-
fication mechanisms: reflection schemes produce direct true/-
                                                                                                                            erate precise, deterministic feedback that clearly identifies
false judgments with relatively low variance, whereas VSA
                                                                                                                            what needs correction (i.e., unmet predicates). Moreover,
encodes a logical specification with multiple predicates—
                                                                                                                            VSA’s roadmap feedback proactively guides agents toward
small stochastic differences can flip individual predicate
                                                                                                                            correct execution paths, preventing errors from happening
decisions—making majority voting especially effective at
                                                                                                                            in the first place. For example, when asked to upvote the
averaging out noise.
                                                                                                                            most controversial comment in a subreddit, M3A without
   These findings indicate that VSA can achieve substantial
                                                                                                                            feedback repeatedly toggled the upvote button because it
performance gains through majority voting. However, in-
                                                                                                                            could not identify whether the upvote has been properly
creasing verification iterations introduces considerable over-
                                                                                                                            set. However, when VSA provided clear guidance that the
head in terms of latency and cost. We analyze this trade-off
                                                                                                                            precondition to set ’upvote’ to ’true’ had been satisfied, M3A
in detail in § 8.4.
                                                                                                                            completed the task without unnecessary repetition.
8.3                  Effectiveness of Feedback Generation                                                                      By contrast, reflection methods rely on LFM-generated
The usefulness of a verification system lies not just in identi-                                                            narrative feedback that is often misleading or inconsistent;
fying errors, but in improving the GUI agent’s performance                                                                  we observed cases where a reflection method initially flagged
through feedback generation. This section evaluates VSA’s                                                                   an action as incorrect but reversed its judgment when the
 ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China                                                                                               J. Lee, D. Lee, et al.


                                         Pre-action Reflection        Post-action Reflection               VSA-Cold        VSA-Warm
                                (a) Trend of latency overhead                                                          (b) Trend of cost overhead
              250                                                                             6

              200                                                                             5

                                                                                              4
              150
Latency (s)




                                                                                   Cost ($)
                                                                                              3
              100
                                                                                              2
               50                                                                             1

                0                                                                             0
                    0   4   8   12   16 20 24              28    32     36    40                  0    4      8       12   16 20 24             28     32      36     40
                                     Number of steps                                                                       Number of steps
                Figure 8: Latency and cost overhead of verification methods with respect to the number of action steps.

 agent repeated the same action, indicating indecisive and                               specifications with additional constraints. However, this in-
 unreliable guidance.                                                                    crease remains trivial compared to the 𝑂 (𝑁 ) complexity of
    A potential limitation of VSA, though not observed in                                reflection-based methods.
 our evaluation, is that false positives could prematurely ter-                             GUI Agents inherently incur substantial latency and cost
 minate tasks that the agent might otherwise complete suc-                               due to their reliance on complex cognitive reasoning. As
 cessfully. Unlike reflection-based methods, where agents                                shown in Figure 8, tasks exceeding 10 steps can cost over $1
 typically recover within 1–3 actions after misleading feed-                             and take nearly a minute to complete. Therefore, minimizing
 back, a single incorrect predicate in VSA’s specification could                         this overhead is as critical for practical deployment as achiev-
 halt task execution entirely. However, our evaluation demon-                            ing high accuracy. VSA thus proves to be more suitable and
 strates that VSA’s decisive feedback provides practical bene-                           practical for real-world deployment across all dimensions
 fits that significantly outweigh the risks of rare false positives.                     compared to existing approaches.
 In safety-critical applications such as automated mobile tasks,                         8.5          Developer Burden
 preventing erroneous actions—even at the cost of occasional
                                                                                        To estimate the developer effort required for VSA integration,
 false positives—is preferable to allowing potentially harmful
                                                                                        we analyzed 18 commercial mobile applications from our
 actions to proceed.
                                                                                        dataset. Since these applications are closed-source, we simu-
 8.4                Latency and Cost                                                    lated the integration process by manually enumerating the
VSA not only enhances verification reliability but also sig-                            verification-relevant state predicates for each of the 18 target
nificantly reduces latency and cost overhead. Figure 8 plots                            apps. We then estimated the lines of code (LoC) by multi-
the additional latency and cost incurred by verification as a                           plying predicate counts by the average LoC per predicate
function of task length (number of steps). As shown by the                              measured from our reference implementation.
fitted lines, VSA consistently maintains lower overhead than                               On average, each application required 58.77 predicates,
reflection-based methods across all task lengths. Notably,                              translating to approximately ∼437 LoC. Across all 18 apps, we
because reflection-based approach requires an additional                                generated 1,058 predicates in total, of which 540 (51%) were
LFM query for each action, its overhead scales proportion-                              activated during our experiments. The number of predicates
ally with task length. While not depicted in the graph for                              varied with application complexity. Google Tasks, a single-
clarity, its overhead is comparable to that of the GUI agent                            function app, required only 22 predicates, while feature-rich
itself, effectively doubling the total expense.                                         applications like Instagram, X (Twitter), and Facebook re-
   In contrast, VSA shows near constant overhead, indepen-                              quired 81, 91, and 72 predicates, respectively. This correlation
dent of task length. This is because VSA uses LFM only once                             between application complexity and predicate count is ex-
– when encoding user instructions into formal specifications.                           pected, as more complex applications naturally have more
All subsequent action verifications are performed using rule-                           states to verify.
based logic. Although Figure 8 shows a slight upward trend                                 While these estimates suggest a non-negligible implemen-
in VSA’s overhead for longer tasks, this increase is attributed                         tation effort, several factors mitigate the burden. First, many
to more complex instructions naturally producing longer                                 predicates follow standard patterns that could be templated
VeriSafe Agent                                                               ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China


or automated. Second, the predicate definitions align nat-          state management, there is significant potential to "piggy-
urally with existing application state logic that developers        back" on these existing mechanisms. Integrating VSA in this
already maintain. Third, predicate granularity provides a           way could streamline the development process and reduce
practical lever for balancing coverage and effort, allowing         the overhead associated with adopting VSA.
developers to selectively implement only safety-critical pred-         Automated State Definition via LFM. Another approach
icates.                                                             for simplifying VSA’s integration is automating the state def-
   Overall, the effort required for predicate definition repre-     inition process using LFMs. Existing GUI agents [4, 6, 7]
sents a one-time investment that yields ongoing benefits in         often employ LFM-powered screen analysis to automatically
error prevention and agent reliability. For applications where      annotate GUI elements and infer application state. A similar
automated agents perform high-stakes tasks, the safety im-          approach could be adapted to identify and define candidate
provements demonstrated in our experiments justify this             state predicates for VSA. However, while this automation
initial development effort.                                         could reduce developer effort, it introduces inherent risks due
                                                                    to the probabilistic nature of LFMs. Relying on potentially
9    Related Work                                                   inaccurate LFM-derived state definitions could compromise
Validating LFM responses. The probabilistic nature of               the system’s reliability. Therefore, while LFM-based automa-
LFMs often leads to hallucinated or inaccurate content. Nu-         tion offers a potential convenience, the current approach of
merous methods have been proposed to mitigate these issues,         developer-defined states ensures the precision necessary for
including Chain-of-Verification (CoVe) [47], concept-level          a robust verification system.
validation and rectification (EVER) [48], self-refinement [49],        Automated Predicate Memory Construction. As demon-
and retrieval-augmented knowledge grounding (Re-KGR) [50].          strated in the evaluation, VSA-Warm’s performance signif-
These approaches typically leverage additional LFM invoca-          icantly benefits from the pre-populated predicate memory.
tions for self-reflections [8, 16] or rely on external validation   However, the current implementation relies on VSA-Cold to
against ground-truth data or knowledge bases [51–55]. How-          successfully complete tasks before they can be added to the
ever, in mobile task automation, actions of a mobile GUI            memory, creating a performance bottleneck. One promising
agent lack a ground truth and its semantic ambiguity makes          approach involves leveraging direct user feedback. By simply
verification exceptionally difficult. VSA effectively handles       asking the user whether a task was completed successfully
this challenge by designing a domain-specific language (DSL,        or not, we can obtain a ground-truth verification result. This
§ 4.1) and developer library (§ 4.2) that effectively capture       user-provided ground truth can then be used to selectively
the underlying semantics of these ambiguous GUI actions.            populate the predicate memory. This approach would bypass
   Leveraging Formal Logic for AI Safety. Recent research           the VSA-Cold bottleneck and accelerate the creation of a
has explored the use of formal logic to ensure the safety and       robust and accurate predicate memory, leading to improved
reliability of AI agents, particularly in areas like planning       overall performance.
and control [18–21, 56, 57]. Notably, SELP [20] ensures safe           Interactive Feedback & Dual Verification While VSA
and efficient robot task planning by integrating constrained        achieves high verification accuracy, it cannot guarantee 100%
decoding and domain-specific fine-tuning. Ziyi et al. [19]          safety. This is critical in high-risk scenarios like financial
proposed a safety module for LFM-based robot agents by              transactions where even a single error is unacceptable. To ad-
converting natural language safety constraints into Linear          dress these limitations, we propose human-in-the-loop strate-
Temporal Logic. However, while previous works typically             gies. Specifically, we recommend two complementary safe-
focus on agents with a pre-defined safety concerns such as          guards: (1) interactive rule-level confirmation that prompts
map navigation or indoor task planning [18–21], our system          users for confirmation when rules are repeatedly violated,
targets agents with an enormous number of environment,              enabling quick human identification of potential False Pos-
i.e., mobile apps. To handle different environments of mobile       itives. (2) Dual verification requiring human approval for
apps, our optimized autoformalization algorithm effectively         critical operations (payments, data transfers) regardless of
translates safety requirements for diverse set of mobile tasks.     VSA’s verification outcome—which guards against potential
10     Discussion & Future Work                                     False Negatives. These mechanisms provide practical safe-
                                                                    guards for commercial deployment while preserving VSA’s
Piggybacking on App Development Frameworks. The                     automation benefits.
current VSA implementation relies on developer-defined
state and transition definition. However, given that modern         11    Conclusion
mobile development frameworks like React Native, Jetpack            This paper introduced VeriSafe Agent (VSA), a novel logic-
Compose, and SwiftUI [38–40] already incorporate built-in           based verification system designed to enhance the safety
                                                                    and reliability of Mobile GUI Agents. Through VSA, we have
ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China                                                                                 J. Lee, D. Lee, et al.


demonstrated that logic-driven verification can effectively                       model for gui agents, 2024. URL https://arxiv.org/abs/2312.08914.
safeguard GUI agents against the inherent uncertainties of                   [14] Mingzhe Xing, Rongkai Zhang, Hui Xue, Qi Chen, Fan Yang, and Zhen
LFM-based task automation. As AI-driven tasks become in-                          Xiao. Understanding the weakness of large language model agents
                                                                                  within a complex android environment, 2024. URL https://arxiv.org/
creasingly integrated into our daily life, VSA presents a cru-                    abs/2402.06596.
cial step toward safer use of AIs.                                           [15] Li Zhang, Shihe Wang, Xianqing Jia, Zhihan Zheng, Yunhe Yan, Longxi
                                                                                  Gao, Yuanchun Li, and Mengwei Xu. Llamatouch: A faithful and
Acknowledgments                                                                   scalable testbed for mobile ui task automation. In Proceedings of the
This work was partly supported by the Institute of Informa-                       37th Annual ACM Symposium on User Interface Software and Technology,
tion & Communications Technology Planning & Evaluation                            New York, NY, USA, 2024.
                                                                             [16] Yanda Li, Chi Zhang, Wanqi Yang, Bin Fu, Pei Cheng, Xin Chen, Ling
(IITP) grant (RS-2019-II190421, RS-2022-II221045, RS-2025-                        Chen, and Yunchao Wei. Appagent v2: Advanced agent for flexible
25442569, RS-2025-02305705, RS-2020-II201819, RS-2023-00232728),                  mobile interactions, 2024. URL https://arxiv.org/abs/2408.11824.
the National Research Foundation of Korea(NRF) grant (RS-                    [17] Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus N. Rabe, Charles
2024-00338454, RS-2021-NR060080, RS-2025-00522352, RS-                            Staats, Mateja Jamnik, and Christian Szegedy. Autoformalization with
2024-00347516), and K-Startup grant (20144069) funded by                          large language models. In Sanmi Koyejo, S. Mohamed, A. Agarwal,
                                                                                  Danielle Belgrave, K. Cho, and A. Oh, editors, Proceedings of the 36th
Korea government (MSIT).                                                          International Conference on Neural Information Processing Systems,
                                                                                  2022.
References                                                                   [18] Jason Xinyu Liu, Ziyi Yang, Ifrah Idrees, Sam Liang, Benjamin Schorn-
 [1] openai. Creating safe agi that benefits all of humanity, 2023. URL           stein, Stefanie Tellex, and Ankit Shah. Grounding complex natural
     https://openai.com/.                                                         language commands for temporal tasks in unseen environments. In
 [2] anthropic. Talk to claude, 2023. URL https://claude.ai/.                     Conference on Robot Learning, CoRL 2023, 6-9 November 2023, Atlanta,
 [3] meta. Introducing llama 2, 2023. URL https://ai.meta.com/llama/.             GA, USA, volume 229 of Proceedings of Machine Learning Research,
 [4] Hao Wen, Yuanchun Li, Guohong Liu, Shanhui Zhao, Tao Yu, Toby                pages 1084–1110. PMLR, 2023.
     Jia-Jun Li, Shiqi Jiang, Yunhao Liu, Yaqin Zhang, and Yunxin Liu.       [19] Ziyi Yang, Shreyas Sundara Raman, Ankit Shah, and Stefanie Tellex.
     Empowering llm to use smartphone for intelligent task automation.            Plug in the safety chip: Enforcing constraints for llm-driven robot
     arXiv preprint arXiv:2308.15272, 2023.                                       agents. In IEEE International Conference on Robotics and Automation,
 [5] Hao Wen, Shizuo Tian, Borislav Pavlov, Wenjie Du, Yixuan Li,                 ICRA 2024, Yokohama, Japan, May 13-17, 2024, pages 14435–14442.
     Ge Chang, Shanhui Zhao, Jiacheng Liu, Yunxin Liu, Ya-Qin Zhang,              IEEE, 2024.
     and Yuanchun Li. Autodroid-v2: Boosting slm-based gui agents via        [20] Yi Wu, Zikang Xiong, Yiran Hu, Shreyash S. Iyengar, Nan Jiang, Aniket
     code generation, 2024. URL https://arxiv.org/abs/2412.18116.                 Bera, Lin Tan, and Suresh Jagannathan. SELP: generating safe and
 [6] Sunjae Lee, Junyoung Choi, Jungjae Lee, Munim Hasan Wasi, Hojun              efficient task plans for robot agents with large language models. CoRR,
     Choi, Steve Ko, Sangeun Oh, and Insik Shin. Mobilegpt: Augmenting            abs/2409.19471, 2024.
     llm with human-like app memory for mobile task automation. New          [21] Ike Obi, Vishnunandan LN Venkatesh, Weizheng Wang, Ruiqi Wang,
     York, NY, USA, 2024. Association for Computing Machinery. ISBN               Dayoon Suh, Temitope I Amosa, Wonse Jo, and Byung-Cheol Min.
     9798400704895. doi: 10.1145/3636534.3690682. URL https://doi.org/10.         Safeplan: Leveraging formal logic and chain-of-thought reasoning for
     1145/3636534.3690682.                                                        enhanced safety in llm-based robotic task planning. arXiv preprint
 [7] Chi Zhang, Zhao Yang, Jiaxuan Liu, Yucheng Han, Xin Chen, Zebiao             arXiv:2503.06892, 2025.
     Huang, Bin Fu, and Gang Yu. Appagent: Multimodal agents as smart-       [22] William Liu, Liang Liu, Yaxuan Guo, Han Xiao, Weifeng Lin, Yuxiang
     phone users, 2023. URL https://arxiv.org/abs/2312.13771.                     Chai, Shuai Ren, Xiaoyu Liang, Linghao Li, Wenhao Wang, et al. Llm-
 [8] Junyang Wang, Haiyang Xu, Haitao Jia, Xi Zhang, Ming Yan, Weizhou            powered gui agents in phone automation: Surveying progress and
     Shen, Ji Zhang, Fei Huang, and Jitao Sang. Mobile-agent-v2: Mobile           prospects. 2025.
     device operation assistant with effective navigation via multi-agent    [23] Chaoyun Zhang, Shilin He, Jiaxu Qian, Bowen Li, Liqun Li, Si Qin,
     collaboration, 2024. URL https://arxiv.org/abs/2406.01014.                   Yu Kang, Minghua Ma, Guyue Liu, Qingwei Lin, Saravan Rajmohan,
 [9] openai. Introducing operator, 2025. URL https://openai.com/index/            Dongmei Zhang, and Qi Zhang. Large language model-brained gui
     introducing-operator/.                                                       agents: A survey, 2025. URL https://arxiv.org/abs/2411.18279.
[10] anthropic. Computer use (beta), 2025. URL https://docs.anthropic.       [24] Shuai Wang, Weiwen Liu, Jingxuan Chen, Yuqi Zhou, Weinan Gan,
     com/en/docs/agents-and-tools/computer-use.                                   Xingshan Zeng, Yuhan Che, Shuai Yu, Xinlong Hao, Kun Shao, Bin
[11] Boyuan Zheng, Boyu Gou, Jihyung Kil, Huan Sun, and Yu Su. Gpt-               Wang, Chuhan Wu, Yasheng Wang, Ruiming Tang, and Jianye Hao.
     4v(ision) is a generalist web agent, if grounded. In Proceedings of the      Gui agents with foundation models: A comprehensive survey, 2025.
     41st International Conference on Machine Learning, ICML’24. JMLR.org,        URL https://arxiv.org/abs/2411.04890.
     2024.                                                                   [25] Yuanchun Li, Hao Wen, Weijun Wang, Xiangyu Li, Yizhen Yuan, Guo-
[12] Christopher Rawles, Sarah Clinckemaillie, Yifan Chang, Jonathan              hong Liu, Jiacheng Liu, Wenxing Xu, Xiang Wang, Yi Sun, Rui Kong,
     Waltz, Gabrielle Lau, Marybeth Fair, Alice Li, William Bishop, Wei           Yile Wang, Hanfei Geng, Jian Luan, Xuefeng Jin, Zilong Ye, Guanjing
     Li, Folawiyo Campbell-Ajala, Daniel Toyama, Robert Berry, Divya              Xiong, Fan Zhang, Xiang Li, Mengwei Xu, Zhijun Li, Peng Li, Yang
     Tyamagundlu, Timothy Lillicrap, and Oriana Riva. Androidworld: A             Liu, Ya-Qin Zhang, and Yunxin Liu. Personal llm agents: Insights
     dynamic benchmarking environment for autonomous agents, 2024.                and survey about the capability, efficiency and security, 2024. URL
     URL https://arxiv.org/abs/2405.14573.                                        https://arxiv.org/abs/2401.05459.
[13] Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu,          [26] Junlin Xie, Zhihong Chen, Ruifei Zhang, Xiang Wan, and Guanbin Li.
     Junhui Ji, Yan Wang, Zihan Wang, Yuxuan Zhang, Juanzi Li, Bin Xu,            Large multimodal agents: A survey, 2024. URL https://arxiv.org/abs/
     Yuxiao Dong, Ming Ding, and Jie Tang. Cogagent: A visual language            2402.15116.
VeriSafe Agent                                                                              ACM MOBICOM ’25, November 4–8, 2025, Hong Kong, China


[27] B. Berard, P. McKenzie, M. Bidoit, A. Finkel, F. Laroussinie, A. Petit,     [48] Haoqiang Kang, Juntong Ni, and Huaxiu Yao. Ever: Mitigating hallu-
     L. Petrucci, and P. Schnoebelen. Systems and Software Verification:              cination in large language models through real-time verification and
     Model-Checking Techniques and Tools. Springer Berlin Heidelberg,                 rectification, 2023. URL https://arxiv.org/abs/2311.09114.
     2014. ISBN 9783662045596.                                                   [49] Aman Madaan, Niket Tandon, Prakhar Gupta, et al. Self-refine: Itera-
[28] Christel Baier and Joost-Pieter Katoen. Principles of Model Checking.            tive refinement with self-feedback, 2023. URL https://arxiv.org/abs/
     The MIT Press, 2008. ISBN 026202649X.                                            2303.17651.
[29] Edmund M. Clarke, Orna Grumberg, Daniel Kroening, Doron A. Peled,           [50] Mengjia Niu, Hao Li, Jie Shi, Hamed Haddadi, and Fan Mo. Mitigat-
     and Helmut Veith. Model checking, 2nd Edition. MIT Press, 2018.                  ing Hallucinations in Large Language Models via Self-Refinement-
[30] Bruno Blanchet, Patrick Cousot, Radhia Cousot, Jérôme Feret, Laurent             Enhanced Knowledge Retrieval, 2024. URL https://arxiv.org/abs/2405.
     Mauborgne, Antoine Miné, David Monniaux, and Xavier Rival. A                     06545.
     static analyzer for large safety-critical software. CoRR, abs/cs/0701193,   [51] Sewon Min, Kalpesh Krishna, Ximing Lyu, Mike Lewis, Wen-tau Yih,
     2007.                                                                            Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, and Hannaneh Ha-
[31] Thomas Kropf. Introduction to Formal Hardware Verification: Methods              jishirzi. FactScore: Fine-grained atomic evaluation of factual precision
     and Tools for Designing Correct Circuits and Systems. Springer-Verlag,           in long form text generation, 2023.
     1st edition, 1999. ISBN 3540654453.                                         [52] Ian Chern, Shiyang Chern, Shushan Chen, Weizhi Yuan, Kai Feng,
[32] Nijat Rajabli, Francesco Flammini, Roberto Nardone, and Valeria Vit-             Chunting Zhou, Junxian He, Graham Neubig, Pengfei Liu, et al. Fac-
     torini. Software verification and validation of safe autonomous cars:            Tool: Factuality detection in generative AI–A tool augmented frame-
     A systematic literature review. IEEE Access, 9:4797–4819, 2020.                  work for multi-task and multi-domain scenarios, 2023.
[33] Rose Bohrer, Yong Kiam Tan, Stefan Mitsch, Magnus O. Myreen, and            [53] Feng Nan, Ramesh Nallapati, Zhiling Wang, Cicero Nogueira dos San-
     André Platzer. Veriphy: verified controller executables from verified            tos, Huan Zhu, Dong Zhang, Kathy McKeown, and Bing Xiang. Entity-
     cyber-physical system models. In Proceedings of the 39th ACM SIGPLAN             level factual consistency of abstractive text summarization, 2021.
     Conference on Programming Language Design and Implementation, page          [54] Ben Goodrich, Vrindavan Rao, Peter J. Liu, and Mina Saleh. Assessing
     617–630, 2018.                                                                   the factual accuracy of generated text. In Proceedings of the 25th
[34] Stefan Mitsch and André Platzer. Modelplex: Verified runtime vali-               ACM SIGKDD International Conference on Knowledge Discovery & Data
     dation of verified cyber-physical system models. Formal Methods in               Mining, pages 166–175, 2019.
     System Design, 2016.                                                        [55] Kurt Shuster, Spencer Poff, M. Chen, Douwe Kiela, and Jason Weston.
[35] Glenford J Myers, Corey Sandler, and Tom Badgett. The art of software            Retrieval augmentation reduces hallucination in conversation, 2021.
     testing. John Wiley & Sons, 2011.                                           [56] Francesco Fuggitti and Tathagata Chakraborti. NL2LTL - a python
[36] Ezio Bartocci, Yliès Falcone, Adrian Francalanza, and Giles Reger. In-           package for converting natural language (NL) instructions to linear
     troduction to runtime verification. Lectures on Runtime Verification:            temporal logic (LTL) formulas. In Brian Williams, Yiling Chen, and
     Introductory and Advanced Topics, pages 1–33, 2018.                              Jennifer Neville, editors, Thirty-Seventh AAAI Conference on Artificial
[37] Leonardo de Moura and Nikolaj Bjørner. Z3: An Efficient SMT Solver.              Intelligence, AAAI, pages 16428–16430. AAAI Press, 2023.
     In International Conference on Tools and Algorithms for the Construction    [57] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt,
     and Analysis of Systems (TACAS), 2008.                                           and Caroline Trippel. nl2spec: Interactively translating unstructured
[38] Meta. State, 2025. URL https://reactnative.dev/docs/state.                       natural language to temporal logics with large language models. In
[39] Google. State and jetpack compose, 2025. URL https://developer.                  Constantin Enea and Akash Lal, editors, Computer Aided Verification -
     android.com/develop/ui/compose/state.                                            35th International Conference, CAV 2023, Paris, France, July 17-22, 2023,
[40] Apple. State, 2025. URL https://developer.apple.com/documentation/               Proceedings, Part II, volume 13965 of Lecture Notes in Computer Science,
     swiftui/state.                                                                   pages 383–396. Springer, 2023.
[41] Serge Abiteboul, Richard Hull, and Victor Vianu. Foundations of
     Databases: The Logical Level. Addison-Wesley Longman Publishing
     Co., Inc., USA, 1st edition, 1995. ISBN 0201537710.
[42] Leon Sterling and Ehud Shapiro. The art of Prolog (2nd ed.): advanced
     programming techniques. MIT Press, Cambridge, MA, USA, 1994. ISBN
     0262193388.
[43] Temesghen Kahsai, Philipp Rümmer, Huascar Sanchez, and Martin
     Schäf. Jayhorn: A framework for verifying java programs. In Computer
     Aided Verification. Springer International Publishing, 2016.
[44] Arie Gurfinkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A.
     Navas. The seahorn verification framework. In Computer Aided
     Verification, pages 343–361. Springer International Publishing, 2015.
[45] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. Rusthorn:
     Chc-based verification for rust programs. ACM Trans. Program. Lang.
     Syst., 43(4), 2021.
[46] Nikolaj Bjørner, Arie Gurfinkel, Ken McMillan, and Andrey Ry-
     balchenko. Horn Clause Solvers for Program Verification, pages 24–51.
     Springer International Publishing, 2015.
[47] Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu,
     Xian Li, Asli Celikyilmaz, and Jason Weston. Chain-of-verification
     reduces hallucination in large language models, 2023. URL https:
     //arxiv.org/abs/2309.11495.
