                                         Trusta: Reasoning about Assurance Cases with Formal
                                         Methods and Large Language Models
                                         ZEZHONG CHEN, Shanghai Key Laboratory of Trustworthy Computing, East China Normal University,
                                         China
arXiv:2309.12941v1 [cs.SE] 22 Sep 2023




                                         YUXIN DENG, Shanghai Key Laboratory of Trustworthy Computing, East China Normal University, China
                                         WENJIE DU, Shanghai Normal University, China
                                         Assurance cases can be used to argue for the safety of products in safety engineering. In safety-critical areas, the
                                         construction of assurance cases is indispensable. Trustworthiness Derivation Trees (TDTs) enhance assurance
                                         cases by incorporating formal methods, rendering it possible for automatic reasoning about assurance cases.
                                         We present Trustworthiness Derivation Tree Analyzer (Trusta), a desktop application designed to automatically
                                         construct and verify TDTs. The tool has a built-in Prolog interpreter in its backend, and is supported by the
                                         constraint solvers Z3 and MONA. Therefore, it can solve constraints about logical formulas involving arithmetic,
                                         sets, Horn clauses etc. Trusta also utilizes large language models to make the creation and evaluation of
                                         assurance cases more convenient. It allows for interactive human examination and modification. We evaluated
                                         top language models like ChatGPT-3.5, ChatGPT-4, and PaLM 2 for generating assurance cases. Our tests
                                         showed a 50%-80% similarity between machine-generated and human-created cases. In addition, Trusta can
                                         extract formal constraints from text in natural languages, facilitating an easier interpretation and validation
                                         process. This extraction is subject to human review and correction, blending the best of automated efficiency
                                         with human insight. To our knowledge, this marks the first integration of large language models in automatic
                                         creating and reasoning about assurance cases, bringing a novel approach to a traditional challenge. Through
                                         several industrial case studies, Trusta has proven to quickly find some subtle issues that are typically missed
                                         in manual inspection, demonstrating its practical value in enhancing the assurance case development process.
                                         CCS Concepts: • Do Not Use This Code → Generate the Correct Terms for Your Paper; Generate the
                                         Correct Terms for Your Paper; Generate the Correct Terms for Your Paper; Generate the Correct Terms for Your
                                         Paper.
                                         Additional Key Words and Phrases: Assurance cases, trustworthiness derivation trees, large language models,
                                         constraint solving
                                         ACM Reference Format:
                                         Zezhong Chen, Yuxin Deng, and Wenjie Du. 2023. Trusta: Reasoning about Assurance Cases with Formal
                                         Methods and Large Language Models. 00, 0, Article 000 ( 2023), 39 pages. https://doi.org/XXXXXXX.XXXXXXX

                                         1    INTRODUCTION
                                         In safety-critical areas such as medical, automotive, and avionics domains, the long-standing
                                         practice has showed that applying assurance cases [6, 7, 29] can bring system reliability and safety
                                         to conform to relevant industrial standards. An assurance case is a documented body of evidence
                                         Authors’ addresses: Zezhong Chen, Shanghai Key Laboratory of Trustworthy Computing, East China Normal University,
                                         3663 Zhongshan North Road, Shanghai, China, 200062; Yuxin Deng, yxdeng@sei.ecnu.edu.cn, Shanghai Key Laboratory of
                                         Trustworthy Computing, East China Normal University, 3663 Zhongshan North Road, Shanghai, China, 200062; Wenjie Du,
                                         Shanghai Normal University, 100 Guilin Road, Shanghai, China, 200233.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
                                         the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2023 Association for Computing Machinery.
                                         XXXX-XXXX/2023/0-ART000 $15.00
                                         https://doi.org/XXXXXXX.XXXXXXX


                                                                                                                   , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:2                                                                         Z. Chen, Y. Deng and W. Du


that provides a valid argument so that a specified set of claims regarding a product’s properties are
adequately justified for a given application in a given environment. It can be graphically depicted
as a finite tree whose root node represents the main claim about a system under consideration,
and the leaf nodes stand for evidences. The other nodes are composed of sub-claims and auxiliary
components. These sub-claims provide compelling, comprehensible, and valid cases [58]. Assurance
cases can demonstrate acceptable safety for a given system. They prove to be useful for risk
management. On one hand, they demonstrate that the risks associated with a system have been
identified. On the other hand, they show that the risk mitigation measures have been effectively
taken to ensure the system’s safety performance. The assurance cases can also be a communication
tool to bring different stakeholders to an agreement on the properties that should be satisfied by
the system.
   There exist a number of international functional safety standards that provide development
guidelines for safety-critical systems such as ISO 26262 [1] and DO-178C [21]. In particular, the
standard ISO 26262 explicitly recommends safety cases or assurance cases to demonstrate the
safety of systems in the automotive domain. Nowadays, assurance cases are widely used in the
nuclear industry, the health and defense sectors, the oil industry, rail transport, automobile, and
avionics [52, 53]. It is envisaged that they can be helpful in other areas, such as finance and
telecommunications, which provide basic infrastructures for the whole society. There exists a huge
amount of literature arguing for a robust evidence-based approach for guaranteeing trustworthiness
in software systems [16], but most of the work on concrete assurance cases is not published due to
various reasons such as security, confidentiality, and sensitivity.
   Assurance cases for complex systems can be very large. For example, a typical assurance case
for an air traffic control system may result in a document with over 500 pages and 400 referenced
documents [40]. The construction and evaluation of assurance cases is time-consuming as it requires
too much manual work. As one of the steps in the overall safety certification process, a dedicated
safety assessor is required to review and challenge the content of an assurance case. During the
evaluation process of an assurance case, the safety assessor is asked to evaluate the validity of the
assurance case and discuss their judgment with the assurance case developers. The high manual
workload involved in the construction and evaluation of assurance cases makes this process long
and time-consuming. The main challenge for the safety assessor is to check the loopholes in a large
assurance case without omission. To make things worse, the content of assurance cases is usually
based on text description (informal description in natural languages), which may be ambiguous
and is not amenable to automated assessment. Since the evaluation of assurance cases largely
depends on human insight and experience, it is error prone due to faults in human judgment. This
complexity reveals the potential need for automation and artificial intelligence intervention, a gap
that the introduction of the Trusta framework in this paper aims to address by combining large
language models and human interaction in a novel and efficient way to create and reason about
assurance cases.
   The need for automation in assurance case generation stems from the inherent complexity
and resource-intensive nature of manually creating, maintaining, and updating assurance cases.
Traditional methods often require significant expert involvement, extensive documentation, and
meticulous tracking of claims, evidence, and arguments. This manual process can be error-prone,
leading to potential inconsistencies and gaps that may jeopardize the integrity of the assurance case.
Furthermore, as systems evolve and regulatory requirements change, updating assurance cases
can become a cumbersome and time-consuming task. Automation offers the promise of efficiency,
consistency, and adaptability, allowing for the real-time generation and updating of assurance
cases, tailored to specific contexts and standards. The introduction of tools like Trusta that leverage
advanced technologies such as large language models holds the potential to revolutionize the field

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                           000:3




                    Fig. 1. GSN notation.                                    Fig. 2. CAE notation.




                                            Fig. 3. TDT notation.


by facilitating a more streamlined and dynamic approach to assurance case generation, thereby
reducing the burden on human experts and enhancing overall effectiveness and reliability.
   In order to facilitate the reasoning about assurance cases, we introduced the model of Trust-
worthiness Derivation Trees (TDTs) [18] and exploited a few formal methods. A TDT is like an
assurance case with only claims and evidences. An assurance case can be converted into a TDT in
two steps: (i) For assurance cases in the Goal Structuring Notation (GSN) [26, 36] format, turn the
auxiliary components (contexts, assumptions, justifications, and strategies) into descriptions of
nodes, while retaining the principal components (goals and solutions); for the Claim-Argument-
Evidence (CAE) [46] notation, the auxiliary components are represented by arguments and the
principal components by claims and evidences; (ii) Then add formal expressions and necessary
parameters to express every principal component. Appendix A showcases an example of the mutual
conversion between an assurance case in GSN format and a TDT. By using formal expressions or
logical formulas to represent the properties of a system, we open the door to automatic reasoning
about TDTs and eventually about assurance cases. Figure 1 shows the widely recognized GSN
representation of assurance cases, while Figure 2 shows the CAE notation. In contrast, Figure 3
introduces our novel representation, the TDT. The unique aspect of the TDT, distinct from the GSN
and CAE notations, is the incorporation of formal expressions. This makes it possible to perform
automatic reasoning from bottom to top.

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:4                                                                        Z. Chen, Y. Deng and W. Du


   In this paper, we introduce Trustworthiness Derivation Tree Analyzer (Trusta), which is a desktop
application for automatically constructing and verifying TDTs. At the frontend, the tool provides a
graphic user interface for creating and manipulating TDTs. In its backend, a lightweight Prolog
interpreter is built in. Moreover, it can invoke Z3 [17] and MONA [37] to solve corresponding
constraints in the formal expressions of goals. Aided by a large language model, the backend
also assists in breaking down a goal into sub-goals and helps in transforming natural language-
formulated goals into constraint-based expressions. Currently, the allowed formal expressions are
logical formulas involving arithmetic, sets, Horn clauses etc. In a TDT, each node is supported by
several sub-nodes. The validity of the sub-nodes implies the validity of the parent node. Therefore,
we can propagate the reasoning in a bottom-up fashion and eventually infer the validity of the root
node of the tree. We have conducted a few case studies such as automated guided vehicles. Indeed,
Trusta has helped us to quickly find some subtle problems that are otherwise difficult to spot by
manual inspection. It also provides error analysis reports using the counterexamples output by the
underlying constraint solvers.
   Trusta simplifies assurance cases without losing their expressiveness, and is capable of performing
automatic reasoning by incorporating formal methods. It can help an assurance case developer to
automatically identify potential errors and find the causes of the errors during the development
process. Furthermore, it can help a safety assessor to find the errors that are difficult to detect
manually. The tool also provides a detailed report on which parts are at risk and what the risks are
in a TDT. We believe that it can shorten the development cycle and improve safety for safety-critical
systems.
   There are two major steps in the process of creating assurance cases with Trusta, both leveraging
a large language model to assist the user in decision-making processes. The first step involves the
decomposition of a goal into sub-goals when creating nodes, a process that can be complex due to
the nested nature and interconnected relationships within a goal. Trusta employs a language model
to analyze the goal’s structure and semantics, offering recommendations for suitable sub-goals that
the user can then select or modify. The second step is the formalization of the goal into a constraint
formula, a task that demands precision and proper understanding of logical relations. Trusta’s
framework takes advantage of the large language model’s capability to comprehend and formulate
mathematical and logical expressions, providing users with suggestions for converting the goal into
a standardized constraint formula. Both steps represent a fusion of machine intelligence with human
oversight, aiming to alleviate some of the complexities and frustrations traditionally associated
with assurance case generation, while still ensuring accuracy and flexibility through interactive
user engagement.
   In this article, the application of a large language model serves as a critical innovation point
within Trusta’s assurance case generation process. By employing a series of specialized techniques,
outlined in Section 2, we design prompt inputs that enable the language model to output structured
information. Trusta’s framework subsequently parses these outputs to present the required content
either graphically or as mathematical expressions. More specifically, the application of the large
language model unfolds in two key scenarios.

   (1) Node creation in assurance cases: Within the input prompts, we incorporate not only the-
       oretical knowledge concerning assurance cases but also the content of the current layer
       of assurance case nodes. The purpose of this approach is to enable the language model to
       generate meaningful content for subsequent layers. Trusta then parses these generated nodes
       and visually displays them, providing users with an intuitive means of understanding and
       modification.


, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                           000:5


    (2) Conversion of text in a natural language to constraint formulas: In this step, the input
        prompts are designed to encapsulate theoretical understanding of constraint-solving, along
        with the natural language expression awaiting transformation. The language model outputs
        the corresponding constraint-solving expression, which Trusta then parses into a standardized
        constraint formula.
    The main contributions of this article can be summarized as follows:
    (1) Introduction of Trusta: A novel tool for enhancing assurance case creation through the
        integration of formal methods and large language models.
    (2) Intelligent automation: Trusta automates two of the most challenging steps in assurance
        case creation: the decomposition of goals into sub-goals and the translation of goals into
        constraint formulas, thereby providing smart recommendations.
    (3) Real-world applications and error analysis: We demonstrate Trusta’s practicality through
        case studies and its capability in identifying potential risks.
    (4) Cross-domain language model evaluation: A comprehensive study on the effectiveness
        of state-of-the-art language models (ChatGPT-3.5 [48], ChatGPT-4 [49], PaLM 2 [23]) in
        generating assurance cases across multiple domains, revealing a 50%-80% similarity between
        machine-generated and human-created cases.
   By amalgamating human expertise with machine-driven insights, this article posits Trusta as a
significant advancement in the field of safety-critical systems. Moreover, this research represents a
major shift in the formal methods domain, offering a solution to the efficiency challenges commonly
associated with the application of formal methods.
   The remainder of this article is organized into distinct sections to provide a coherent and com-
prehensive overview of Trusta and its applications in assurance case generation and evaluation.
Section 2 delves into the theoretical background, elucidating the key concepts of assurance cases,
large language models and constraint solvers. Section 3 introduces the architecture and function-
alities of Trusta, with particular emphasis on the integration of large language models and their
role in the two intricate steps of goal decomposition and goal translation. Section 4 presents a case
study that showcases the real-world application of Trusta in a safety-critical domain, followed
by Section 5 which offers a comparative analysis of Trusta with existing methodologies. Finally,
Section 6 first concludes the paper by summarizing the key contributions, and then discusses the
future directions of the research. Appendices give a few concrete assurance cases to show the
conversion between GSN and TDT formats.

2     BACKGROUND
In this section, we review some background knowledge about assurance cases, large language
models, and constraint solvers.

2.1    Assurance Cases
The assurance case [32], also known as safety case, is an essential construct within safety-critical
systems for demonstrating the safety and reliability of a system within specific operational contexts.
These cases typically encompass aspects of system design, development, and maintenance, with
an ultimate aim to ensure that the system meets safety and reliability criteria to achieve expected
performance in real-world operation. The theoretical origin of assurance cases is traced to the
domain of logical reasoning, notably introduced by the British philosopher Stephen Toulmin in
1958 [59]. The concept gained prominence with the rapid development in complex industries and the
wide use of novel automation technologies, as humans faced unprecedented technological risks [14].
The evolution and widespread practical application of the assurance case were notably influenced by

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:6                                                                        Z. Chen, Y. Deng and W. Du


the 1988 Piper Alpha oil platform disaster [57], underscoring the vital role of systematic, structured
argumentation in assessing and establishing system safety in increasingly intricate and risk-prone
technological landscapes.
   Today, assurance cases, or safety cases, play a crucial role across various domains, particularly
in industries that demand high standards of safety, reliability, and compliance. Representative
application fields include:
     • Aerospace industry [35, 55]: Due to stringent safety requirements, aerospace engineering
       employs assurance cases to verify and assure the safety and reliability of airplanes [24],
       satellites [3], and spacecraft systems [61].
     • Railway industry [5, 44]: Assurance cases are used to substantiate the safety and reliability
       of railway systems, such as signaling, train control, and operating equipment, reducing
       accident risk and ensuring passenger and staff safety.
     • Automotive industry [25, 50]: With the advent of autonomous driving [11], assurance cases
       are deployed to argue for the safety and reliability of self-driving systems.
     • Medical devices [9]: Medical device manufacturers (e.g., infusion pumps [38], pacemak-
       ers [31]) utilize assurance cases to demonstrate the safety and compliance of the design,
       manufacturing, and usage processes of their products.
     • Nuclear energy industry [7, 39, 63]: Given stringent demands for safety and compliance,
       assurance cases are employed to assess the safety of nuclear power stations, facilities, and
       nuclear material management systems.
     • Oil and chemical industry [4, 28, 45]: In the oil, gas, and chemical sectors, assurance
       cases are utilized to evaluate and ensure safety and reliability throughout the process, pre-
       venting major accidents, averting environmental disasters, and safeguarding workers and
       environmental safety.
     • Military and defense [34]: In the highly security-sensitive military and defense sector, assur-
       ance cases are used to evaluate the safety and reliability of weapon systems, communication
       systems, and defensive mechanisms.
     • Finance and banking [22]: Financial and banking industries leverage assurance cases to
       verify the security and compliance of financial transaction systems, safeguarding financial
       data and transactions.
     • Safety management and regulation development [8]: In shaping safety management
       and regulations, such as cybersecurity regulation [8], school disaster prevention [64], and
       pandemic control policies [27], assurance cases play a role in risk assessment, design, and
       confirmation of control measures, provision of safety evidence, and promoting continuous
       improvement, thereby ensuring system safety and effective risk management.
   The purpose of an assurance case is to articulate a clear, comprehensive, and dependable argument
that a system’s operation meets acceptable safety within a specific environment [32]. An assurance
case serves as a tool for communicating ideas and information, often conveying content to a third
party such as regulatory authorities. To achieve this convincingly, it must be as clear as possible.
The system referred to by an assurance case can be any object, such as a pipeline network, software
configuration, or a set of operating procedures; the concept is not confined to considerations of
traditional engineering “design". Absolute safety is an unattainable goal, and the existence of an
assurance case is to persuade others that the system is sufficiently safe, embodying acceptable
safety with tolerable risks. Safety argumentation must take into consideration premises, as nearly
any system might be unsafe if used improperly or unexpectedly, such as arguing for the safety
of conventional house bricks [33]. Therefore, part of the work of an assurance case is defining
the context or specific environment of safety. An assurance case consists of three main elements,

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                           000:7




Fig. 4. Structure of assurance cases. [36]             Fig. 5. Creation process of assurance cases.


namely goals, argumentation, and evidence, and the relationship between these three elements is
depicted in Figure 4.
  The process of creating an assurance case consists of four basic steps: identifying goals, gathering
evidence, constructing arguments, and evaluating the assurance case [10]. As shown in Figure 5,
these steps build the fundamental framework of the assurance case, providing directions for safety
engineers and project managers. This structured approach ensures a coherent and transparent
connection between the goals, argumentation, and evidence, facilitating a clear and persuasive
presentation of the system’s safety and reliability. It is noteworthy that these four steps are not
completed all at once but are iteratively performed throughout the project development process.
As the project evolves and requirements change, the assurance case may need to be updated
and modified. Furthermore, to ensure the quality and effectiveness of the assurance case, these
four steps require good collaboration among the team members. This iterative and collaborative
approach ensures that the assurance case remains aligned with the project’s ongoing development
and continues to reflect an accurate and robust representation of the system’s safety and reliability.

2.2   Large Language Models
Large language models [15] have their origins in the progressive evolution of machine learning
algorithms and natural language processing techniques. They mark a significant advancement from
traditional rule-based systems, employing deep learning architectures such as Transformers [60], in-
troduced by Vaswani et al. in 2017. Application domains for these models are diverse, encompassing
machine translation, text generation, sentiment analysis, summarization, and more. The implemen-
tation rationale of large language models lies in their ability to process and generate human-like
text by learning from vast amounts of textual data, capturing intricate patterns and dependencies in
language. Advantages of these models include their high versatility and adaptability across various
tasks, often outperforming task-specific models. However, they are not without disadvantages;
their large-scale nature demands extensive computational resources for both training and inference.
Additionally, concerns regarding ethical considerations, biases embedded within the training data,
and the potential lack of interpretability and transparency make the deployment and use of large
language models a complex consideration.
   Large language models are capable of accomplishing a wide range of tasks. Their utilization is
straightforward, necessitating only an input box through which “prompts" are sent to guide the
model’s responses. However, truly harnessing the full potential of these models is less straightfor-
ward. It requires a certain expertise in crafting these prompts.
   We have categorized several techniques for making effective use of large language models, as
summarized in Table 1. These techniques include strategies to improve instruction quality, use of
reference text, task decomposition, promoting the model’s “thinking” process, integrating external

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:8                                                                             Z. Chen, Y. Deng and W. Du


              Table 1. Classification and summary of usage techniques for large language models

    Category                                     Technique                            Technique ID
    Optimizing Instruction Quality               Being Specific                       T1
                                                 Role-play                            T2
                                                 Instruction Segmentation             T3
                                                 Specifying Steps                     T4
                                                 Providing Examples                   T5
                                                 Setting Length                       T6
    Leveraging Reference Text                    Answer Reference                     T7
                                                 Citation Reference                   T8
    Task Decomposition                           Intent Classification                T9
                                                 Information Filtering                T10
                                                 Paragraph Summarization              T11
    Making the Model “Think"                     Solution Strategy                    T12
                                                 Simulate Thinking Process            T13
                                                 Asking for Omissions                 T14
    Combining External Tools                     Embedding-based Search               T15
                                                 Code Execution                       T16
    Systematic Testing                           Comparing to Gold Standard Answers   T17
                                                 Conducting A/B Tests                 T18


tools, and systematic testing. For instance, Technique T1 (Being Specific) is a method to improve
instruction quality by making queries more targeted, thereby eliciting more relevant responses
from the model. Another example, Technique T12 (Solution Strategy) makes the model generate
several potential solutions before coming up with a final answer, allowing it to explore various
avenues of thought. Furthermore, systematic testing plays an important role in the effective usage
of language models. Techniques T17 and T18 involve comparing model outputs to gold standard
answers and conducting A/B tests respectively, allowing for the evaluation and improvement of
model performance. In short, these techniques collectively offer an approach to refine prompts and
thereby extract more meaningful and valuable output from large language models. Each technique
listed in Table 1 can be individually applied or combined with others, depending on the complexity
of the task at hand and the specific objectives of the user.
     • T1 (Being Specific): Make queries more targeted by providing the model with detailed infor-
       mation for more relevant answers.
     • T2 (Role-play): Assign a role to the model within the query for more creative answers.
     • T3 (Instruction Segmentation): Use delimiters to distinguish different parts in the query.
     • T4 (Specifying Steps): List out the steps needed to complete the task to help the model
       generate accurate answers.
     • T5 (Providing Examples): Assist the model in understanding requirements through examples.
     • T6 (Setting Length): Specify the desired length of output in the query.
     • T7 (Answer Reference): Allow the model to generate more accurate answers by referring to a
       specific text.
     • T8 (Citation Reference): Instruct the model to quote specific parts from the reference text for
       more in-depth answers.
     • T9 (Intent Classification): Decompose complex queries by analyzing the main objective in
       user queries.

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                           000:9


      • T10 (Information Filtering): For applications requiring long conversations, summarize or
        filter out previous dialogue, keeping only the key information.
      • T11 (Paragraph Summarization): If dealing with long documents, split them into multiple
        paragraphs for summarization, and then combine these summaries.
      • T12 (Solution Strategy): Make the model generate possible solutions before producing the
        final answer.
      • T13 (Simulate Thinking Process): Allow the model to conduct an internal monologue, simu-
        lating a “thinking" process.
      • T14 (Asking for Omissions): Ask the model if it has omitted important information in the
        problem-solving process.
      • T15 (Embedding-based Search): Use embedding-based search for effective knowledge retrieval.
      • T16 (Code Execution): Leverage the model’s code generation capability to perform calculations
        or call APIs.
      • T17 (Comparing to Gold Standard Answers): Evaluate the quality of the model output by
        comparing it with preset gold standard answers.
      • T18 (Conducting A/B Tests): Compare the effects of different prompts on the model output
        to find the most effective prompting strategy.
  In the process of generating TDT nodes using large language models, as discussed in Section 3,
the techniques outlined above have been utilized.

2.3    Constraint Solvers
Constraint solvers [30] originated from the field of artificial intelligence and mathematical pro-
gramming in the latter half of the 20th century, becoming an essential tool for solving problems
expressed through constraints. The application fields of constraint solvers are manifold, including
scheduling, planning, resource allocation, and various optimization problems. The implementation
principle relies on techniques such as backtracking, consistency checking, and local search, often
coupled with heuristics, to explore the solution space systematically and efficiently. Advantages of
constraint solvers include their flexibility in modeling complex relationships and the ability to find
optimal or near-optimal solutions. However, their disadvantages may involve high computational
costs for large or complex problems and difficulty in modeling some real-world scenarios. For exam-
ple, constraint solvers are widely used in airline scheduling, where constraints like the maximum
number of working hours for pilots, mandatory rest periods, and aircraft maintenance schedules
must be simultaneously satisfied. In this application, constraint solvers enable the creation of
feasible schedules that adhere to all necessary regulations, though the complexity and size of the
problem may present computational challenges.

3     TOOL ARCHITECTURE AND IMPLEMENTATION
In Figure 6, we give an overview of the execution flow and the functional architecture of Trusta. The
tool is a desktop application created with Python’s GUI library PyQt [65]. It can be used as an IDE to
create TDTs, which are graphical representations of assurance cases, and provide various graphical
transformation operations. The tool consists of three modules: TDT Creator, TDT Evaluator, and
Report Generator. Below we discuss each of them in more detail.

3.1    TDT Creator
The TDT Creator consists of four sub-modules: (1) a UI controller is in charge of responding to
users’ actions, (2) a node creates or utilizes a large language model to derive child nodes from the

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:10                                                                              Z. Chen, Y. Deng and W. Du




              Fig. 6. An overview of the execution flow and the functional architecture of Trusta.


upper layer, (3) a data manager can modify the data in a tree, (4) a graphic operation module uses
the data of a tree to render TDT graphics and interactively modify the tree.
   UI Controller. Figure 7 gives a snapshot of creating a TDT with Trusta. After opening a TDT,
a tree is rendered automatically in the middle of the panel. Trusta provides many functions for
editing and displaying the information of the nodes in the tree. For example, we can select, move,
or resize nodes, modify node colors, rotate the entire tree, or hide some subtrees. In the bottom of
the panel, the information about a selected node is displayed and can be edited. On the left of the
panel is a project explorer, and on the right is an outline of the information with all the nodes in
the TDT.




, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                                           000:11




                                                                                                             Fig. 7. A snapshot of Trusta




                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:12                                                                       Z. Chen, Y. Deng and W. Du


   Node Creator. Trusta uses Prolog’s syntax for Horn clauses that describe rules and axioms. A rule
can describe a two-level subtree, and multiple rules are able to describe a more complex multi-level
tree. Two examples are given in Figure 12. On the left is a two-level tree generated by a rule, and
on the right is a more complex tree generated by three rules. The module of text analyzer can
recognize those rules so to construct TDTs on one hand and perform Prolog’s inference on the other
hand. These rules governing the splitting of nodes can be formulated through manual procedures
or with the integration of sophisticated large language models. Trusta, an innovative system in
this context, seamlessly integrates such a large language model, thereby facilitating an efficient
and user-friendly mechanism for node splitting. This integration enables users to accomplish node
divisions with a single click. The resultant split is immediately usable and operational. Should
any inconsistencies or errors be identified in the output, users are afforded the flexibility to enact
manual adjustments. This control mechanism ensures that the TDT nodes generated align precisely
with user expectations, thus providing a robust solution that harmonizes automated efficiency
with user-guided precision. This blend of automated and manual control represents a significant
advancement in the management of complex systems.
   The invocation of a large language model, particularly for complex tasks like assurance case
generation, requires carefully crafted prompts. Due to the length of the prompts used for the
creation of node-splitting rules, they are divided into two parts and illustrated in Figures 8 and 9.
The process under discussion is delineated into four distinct segments.

   (1) The first segment (lines 1-3) sets the context and defines the role of the language model as an
       expert in assurance cases. It provides a general format that the model’s output should follow
       and instructs the model to break down a given goal into various sub-goals. This section also
       asks the model to provide explanations for the breakdown as well as potential solutions for
       the sub-goals, setting up the stage for structured assurance case generation.
   (2) The second segment (lines 5-15) provides an in-depth look at the definitions and terminolo-
       gies employed in assurance cases. This section not only defines what a “Goal”, “Strategy”,
       and “Solution” are but also outlines the five basic CAE (Claim-Argument-Evidence) building
       blocks [46] essential for crafting assurance cases. These blocks are Decomposition, Substi-
       tution, Concretion, Calculation or Proof, and Evidence Incorporation. By introducing these
       conceptual tools, this segment equips the model with the necessary framework to understand
       and generate assurance cases more effectively.
   (3) The third segment (lines 17-55) offers multiple examples that individually highlight the use
       of each of the five building blocks: Decomposition, Substitution, Concretion, Calculation or
       Proof, and Evidence Incorporation. These examples cover various domains and goals such
       as self-driving cars, medical devices, and data encryption. For each example, the section
       details the building blocks employed, the breakdown strategy, the sub-goals, and solutions.
       Additionally, it provides explanations on how these elements are interconnected. These
       examples serve as both a comprehensive guide and a template for the model, aiding it in
       understanding how to structure and approach different types of assurance cases.
   (4) The fourth and final segment (lines 57-62) presents an incomplete example that consists
       solely of a placeholder for a goal, denoted as ⟨A_NEW_GOAL⟩ , which is intended to be
       decomposed. This incomplete example follows the same format as the examples in the third
       segment and is designed for completion by a large language model. When invoking the model,
       ⟨A_NEW_GOAL⟩ is replaced with a specific goal, as illustrated in the first line of Figure 10.

  The model’s output, as shown in Figure 10, is then parsed by the Trusta tool to generate the TDT
nodes. This effectively bridges the gap between theoretical modeling and practical implementation,

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:13




                   Fig. 8. Part 1 of 2: Prompt with domain knowledge of assurance case.




demonstrating that the model’s output is in a format compatible with Trusta for seamless integration
into a workflow.
   In order to evaluate the utility of cutting-edge language models for generating assurance cases,
we conducted a comprehensive analysis on 57 assurance case fragments across seven distinct
application domains. Figure 11 presents the summarized results, comparing the semantic similarity
between assurance cases created by humans and those generated by leading language models,
namely ChatGPT-3.5 and ChatGPT-4 from OpenAI, as well as PaLM 2 from Google. The domains
explored include Unmanned Aerial Vehicles (UAV) [61], AutoRobot [11], CubeSat [3], CyberSecu-
rity [8], Automobile [50], Pacemaker [31], and Aircraft [24]. While the average similarity metrics
generally lie between 50%-80%, this range still indicates a substantial contribution from these
models in aiding the generation of assurance cases. It is worth mentioning that similarity here
refers to the equivalence in the meaning of sentences within the assurance cases. Impressively,
among the 57 fragments analyzed, 18 were found to have 100% semantic similarity when generated

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:14                                                                              Z. Chen, Y. Deng and W. Du




Fig. 9. Part 2 of 2: Prompt with examples of assurance case, including the final example awaiting completion
by a large language model.




                            Fig. 10. Large language model output when splitting nodes.



by these AI models, illuminating their capability to produce reasonably accurate assurance case
content.

   Data Manager. The Data Manager is mainly used to store and edit TDTs created from rule text or
large language models. It is involved when users add, delete, select, or modify TDT nodes. Typically,
a user begins by constructing the skeleton of a TDT using a set of rules or the guidance from a
large language model. Subsequently, she refines the content of each node by adding descriptions,
types, and formal expressions. This results in a complete TDT, capable of representing a normal
assurance case, akin to the GSN or CAE notation.

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:15




Fig. 11. Comparative analysis of similarity between human-created and language model-created assurance
cases across different domains. The domains examined include UAV (Unmanned Aerial Vehicle) [61], Au-
toRobot [11], CubeSat [3], CyberSecurity [8], Automobile [50], Pacemaker [31], and Aircraft [24]. The models
compared are ChatGPT-3.5, ChatGPT-4, and PaLM 2. Similarity is measured as a percentage of resemblance
to human-created assurance cases in each domain.




                                                   
                                                       𝐶 : −𝐶1, 𝐶2.    
                                                                        
   (a) 𝐶 : −𝐶1, 𝐶2.                          (b)    𝐶1 : −𝐶11, 𝐶12. 
                                                                       
                                                   𝐶2 : −𝐶21, 𝐶22, 𝐶23.
                                                                       



                           Fig. 12. Two examples of rule texts and TDT skeletons



  Graphic Operation Module. The Graphic Operation Module is responsible for turning the TDT
data stored by the Data Manager into diagrams and provides functions such as zooming, moving,
and overview. This module has contributed significantly to GoJS [56], a JavaScript library for
creating interactive charts. We embed browser controls on a PyQt based framework to run GoJS.

3.2 TDT Evaluator
This is the module where formal methods are used for automatic reasoning about TDTs. We use
three constraint solvers [54] to check the validity of the properties specified by the formal expression
in each node of a TDT. Since different solvers are good at different types of reasoning, we use the
Type field in every node to indicate the evaluation type. For example, the type ’AbstractSet’ in
a node means that the formal expression in the node involves set operations about abstract sets,
so we are going to employ MONA to solve the constraints. The process involves the translation
of the natural language descriptions within nodes into formalized constraints, a task that can be
undertaken through manual translation or through interactive translation with the assistance of a
large language model [15].

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:16                                                                               Z. Chen, Y. Deng and W. Du




                  Fig. 13. Large language model interactive translation interface within Trusta.


   Data Controller. In order to verify that the whole TDT is sound, it suffices to show the soundness
of each two-level subtree in the TDT. A two-level subtree consists of a parent node and several child
nodes. It corresponds to a rule as shown in Figure 12. These child nodes represent the premises,
and the parent node stands for the conclusion of the rule. Suppose 𝐹 1, 𝐹 2, ..., 𝐹𝑛 are the formal
expressions of premises, and 𝐹 is the formal expression of the conclusion. In addition, we allow
two types of logical relations between the child nodes and their parent node, as indicated by a tag
on each edge in Figure 3. The “And" relation means that all the premises need to be combined to
lead to the conclusion. In this case, we check if the formula 𝐹 1 ∧ 𝐹 2 ∧ ... ∧ 𝐹𝑛 ∧ ¬𝐹 is satisfiable. If it
is unsatisfiable then the rule is sound. Otherwise, a solution exists and witnesses the unsoundness
of the rule. The “Or" relation means that any one of the premises can lead to the conclusion. In that
case, we need to check the satisfiability of the formula (𝐹 1 ∨ 𝐹 2 ∨ ... ∨ 𝐹𝑛 ) ∧ ¬𝐹 .
   Constraint Solvers. The satisfiability of the formulas given above are determined by constraint
solvers. According to our experience with industrial case studies, we have summarized four types
of constraints commonly encountered: logical relations, arithmetic, abstract sets, and concrete sets.
Unfortunately, there exists no single solver that can solve all those types of constraints. Therefore,
we have to call different solvers for different constraints. If the constraints are about logical relations,
we resort to a lightweight Prolog built in Trusta. For arithmetic related to first-order theories, we
take advantage of Z3. For some reasoning about abstract sets, i.e. unassigned sets whose elements
are not explicitly known, we make use of MONA. For concrete sets whose elements are given in
terms of arrays or lists, we use Python to deal with set operations.
   Below we take a brief look at three types of constraints via a few simple examples. Consider the
TDT shown in Figure 7. The number in the upper left corner of each node represents the node ID.
The node IDs from the set {16, 17, 18} correspond to a two-level subtree. The constraint for this

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                             000:17


subtree is captured by the expression 𝐸𝐿𝑜𝑔𝑖𝑐𝑎𝑙 in (1). It is the conjunction of three parts: the first
part says that a merge request with the same developer and committer is called self-reviewed; the
second part is an evidence, a list of records showing the developers and committers of some merge
requests; the third part is the negation of the property in the parent node, concerning about the
absence of self-reviewed merge request, where the symbol ‘\+’ is the Prolog syntax for negation.
The satisfiability of the formula 𝐸𝐿𝑜𝑔𝑖𝑐𝑎𝑙 can be checked by the lightweight Prolog built in Trusta.

              𝐸𝐿𝑜𝑔𝑖𝑐𝑎𝑙     =     “𝑠𝑒𝑙 𝑓 _𝑟𝑒𝑣𝑖𝑒𝑤𝑒𝑑 (𝑀) : − 𝑑𝑒𝑣𝑒𝑙𝑜𝑝𝑒𝑟 (𝑀, 𝐼𝐷), 𝑐𝑜𝑚𝑚𝑖𝑡𝑡𝑒𝑟 (𝑀, 𝐼𝐷).”
                                ∧ “𝑑𝑒𝑣𝑒𝑙𝑜𝑝𝑒𝑟 (𝑚𝑟𝑎 , 𝐴𝑙𝑖𝑐𝑒).
                                     𝑑𝑒𝑣𝑒𝑙𝑜𝑝𝑒𝑟 (𝑚𝑟𝑏 , 𝐵𝑜𝑏).
                                                                                                                      (1)
                                     𝑐𝑜𝑚𝑚𝑖𝑡𝑡𝑒𝑟 (𝑚𝑟𝑎 , 𝐷𝑎𝑣𝑖𝑑).
                                     𝑐𝑜𝑚𝑚𝑖𝑡𝑡𝑒𝑟 (𝑚𝑟𝑏 , 𝐸𝑣𝑒).”
                                ∧ ¬“\ + 𝑠𝑒𝑙 𝑓 _𝑟𝑒𝑣𝑖𝑒𝑤𝑒𝑑 (𝑀).”
   Now consider the node IDs from the set {19, 20, 21, 22}. They correspond to a two-level sub-
tree whose constraints are about arithmetic and captured by the formula 𝐸𝐴𝑟𝑖𝑡ℎ𝑚𝑒𝑡𝑖𝑐 in (2). The
formula is a conjunction of four parts: the first part defines the relationship between the variables
𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒_𝑡𝑖𝑚𝑒, 𝑝𝑟𝑜𝑐_𝑎𝑙𝑙_𝑡𝑖𝑚𝑒, and 𝑠𝑒𝑛𝑑_𝑡𝑖𝑚𝑒; the second and third parts define the constraints on
the last two variables; the last part is again the negation of the property in the parent node. The
satisfiability of the formula 𝐸𝐴𝑟𝑖𝑡ℎ𝑚𝑒𝑡𝑖𝑐 can be checked by Z3.

                    𝐸𝐴𝑟𝑖𝑡ℎ𝑚𝑒𝑡𝑖𝑐         =    “𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒_𝑡𝑖𝑚𝑒 = 𝑝𝑟𝑜𝑐_𝑎𝑙𝑙_𝑡𝑖𝑚𝑒 + 𝑠𝑒𝑛𝑑_𝑡𝑖𝑚𝑒”
                                            ∧ “𝑝𝑟𝑜𝑐_𝑎𝑙𝑙_𝑡𝑖𝑚𝑒 < 1”
                                                                                                                      (2)
                                            ∧ “𝑠𝑒𝑛𝑑_𝑡𝑖𝑚𝑒 < 0.5”
                                            ∧ ¬“𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒_𝑡𝑖𝑚𝑒 < 2”
   Then we consider the node IDs from the set {9, 10, 11, 12}. They correspond to a two-level subtree
that talks about abstract sets. Their constraints are captured by the formula 𝐸𝐴𝑏𝑠𝑡𝑟𝑎𝑐𝑡𝑆𝑒𝑡 in (3). The
formula is a conjunction of four parts: the first part defines the sets 𝐶 and 𝐷 together with an
element 𝑏; the second and third parts define the constraints between 𝐶, 𝐷, and 𝑏. The last part is
the negation of the property in the parent node. We can employ MONA to check the satisfiability
of the formula 𝐸𝐴𝑏𝑠𝑡𝑟𝑎𝑐𝑡𝑆𝑒𝑡 .

                         𝐸𝐴𝑏𝑠𝑡𝑟𝑎𝑐𝑡𝑆𝑒𝑡       =    “𝑆𝑒𝑡 𝐶, 𝐷; 𝐸𝑙𝑒𝑚 𝑏; ”
                                                ∧ “𝐶 𝑖𝑛𝑡𝑒𝑟 𝐷 = 𝑒𝑚𝑝𝑡𝑦; 𝑏 𝑖𝑛 (𝐶 𝑢𝑛𝑖𝑜𝑛 𝐷); ”
                                                                                                                      (3)
                                                ∧ “𝑏 𝑛𝑜𝑡𝑖𝑛 𝐷; ”
                                                ∧ ¬“𝑏 𝑖𝑛 𝐶; ”
   Constraint Formalizer. The interactive translation interface within Trusta is illustrated in Fig-
ure 13. The underlying conceptual framework draws inspiration from Cosler’s work [15] on
translating natural language into temporal logics. We have made certain adaptations to the prompt
words originally designed for translating temporal logics, as exemplified in Figure 14, in order
to accommodate the transformation of natural language into constraint expressions. We have
revised the introduction of the problem context to focus on constraint expression considerations
(lines 1-3). Symbol conventions have been adjusted to align with comprehensible notations for
constraint solvers (lines 5-7). A novel provision regarding numeric units has been introduced,
mandating a standardized adoption of international units (line 9). Furthermore, we present three
illustrative examples of constraint translation challenges (lines 11-27). Conclusively, we furnish
pending translations that encompass both natural language and manually generated sub-translation
cues (lines 29-31). This framework is seamlessly extended by a large language model, adhering to
the format of the provided examples, as demonstrated in Figure 15. These adjustments facilitate the
seamless transition from descriptive language to formal constraints, enhancing the applicability

                                                                   , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:18                                                                           Z. Chen, Y. Deng and W. Du




   Fig. 14. Prompt of large language model translation from natural language to constraint expressions.




   Fig. 15. Output of large language model translation from natural language to constraint expressions.


and efficacy of the translation process. This augmentation of the translation mechanism contributes
to the broader goal of enhancing automated reasoning within the Trusta framework.

3.3      Report Generator
Based on the results of constraint solving, Trusta reports on the vulnerabilities in the systems
modeled by TDTs. More specifically, if a property is invalid, the constraint solvers generate

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:19




                                           Fig. 16. AGV braking.


counterexamples to witness the invalidity of the property. For example, if we change the third
part of the formula 𝐸𝐴𝑟𝑖𝑡ℎ𝑚𝑒𝑡𝑖𝑐 into 𝑠𝑒𝑛𝑑_𝑡𝑖𝑚𝑒 < 1.5, then that formula is satisfiable. One so-
lution is (𝑝𝑟𝑜𝑐_𝑎𝑙𝑙_𝑡𝑖𝑚𝑒 = 0.9, 𝑠𝑒𝑛𝑑_𝑡𝑖𝑚𝑒 = 1.4, 𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒_𝑡𝑖𝑚𝑒 = 2.3). In that case, the goal
𝑟𝑒𝑠𝑝𝑜𝑛𝑠𝑒_𝑡𝑖𝑚𝑒 < 2 does not hold, so the TDT is unsound. This kind of feedback from the constraint
solvers provides TDT developers with more explicit information about the unsafe scenarios so they
can quickly fix the problems.

4     CASE STUDIES
Together with our industrial partner, we have constructed TDTs in more than a dozen real scenarios
such as checking the consistency of software constructions and the trustworthiness of software
implementation. Indeed, Trusta helped us to discover some subtle problems that were not noticed
before. In this section, we have conducted case demonstrations for both the creation and evaluation
of TDT pertaining to automated guided vehicles (AGV) in warehouses. This case uses the large
language model ChatGPT-3.5 [48]. To assess the variances between different large language models
and application domains in automatically generating assurance cases, we have also conducted
experiments using three of the current leading models—ChatGPT-3.5, ChatGPT-4 [49], and PaLM
2 [23]—across seven distinct domains for comparison.
   AGV robots move goods autonomously between the different areas of a warehouse, as shown
in Figure 16. They move along pre-designed routes and carry all kinds of loads. However, there
are crossings between the route of one AGV and that of another AGV or the footway of a person.
Therefore, potential risks exist and despite various preventive measures it is necessary to evaluate
the trustworthiness of a warehouse with AGVs. We have constructed a TDT for this purpose.

4.1    Creation of TDT
With Trusta for the construction of a TDT, it is only required to create a top-level goal, as illustrated
in Figure 17. We established a goal node with the objective: “The automatic guided vehicle can stop
safely when encountering obstacles.” Instructions were given to Trusta to decompose the goal into
three layers, utilizing a language model’s temperature parameter set at 0.8. This setting promotes
greater creativity and enables the discovery of potentially overlooked subgoals. In the context of
large language models [47], the sampling temperature is a value ranging from 0 to 2. Higher values
like 0.8 result in more random outputs, while lower values like 0.2 render the outputs more focused
and deterministic.
   Once the aforementioned inputs are prepared, Trusta is capable of generating a series of nodes,
as depicted in Figure 18. Trusta automatically generated 36 nodes, encompassing 23 subgoal nodes

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:20                                                                              Z. Chen, Y. Deng and W. Du




          Fig. 17. Screenshot of the input for the creation of TDT using Trusta in the context of AGV.


and 13 solution nodes. Upon enlargement, these are respectively displayed in Figures 19, 20, 21,
and 22. In Figure 19’s decomposition, the top-level goal “The automatic guided vehicle can stop
safely when encountering obstacles” (Node 1) has been broken down into three specific subgoals
that form a comprehensive strategy to meet the main objective. The strategy defined for each
subgoal elucidates the functionalities and considerations vital to the overarching aim of ensuring
safe stopping of the AGV. These subgoals include the accurate and timely detection of obstacles
by the AGV’s sensors (Node 2), the rapid and safe initiation of the braking system after receiving
sensor signals (Node 3), and the control system’s capability to execute safety strategies, such as
deceleration or stopping, after detecting obstacles (Node 4). Figures 20, 21 and 22 follow the same
pattern. Solutions at the leaf nodes of the TDT are created according to the upper-level nodes.
   The above example illustrates the one-time multi-layer generation of TDT using Trusta. In
practice, however, we can request the tool to decompose subgoals layer by layer, allowing users
to make timely adjustments and further create more granular subgoals. As the decomposition
progresses, there are typically two situations indicating that further decomposition of the goals
might not be necessary: (1) when the generated nodes start to have meanings that are identical to
their parent nodes or other existing nodes, and (2) when experts believe that the current goal node
can be substantiated with evidence. This method of creating TDT aligns more closely with user
expectations and ensures that the process does not consume excessive time.

4.2      Evaluation of TDT
Inevitably, AGVs traveling in a warehouse may encounter obstacles in front of them, which may be
people, goods, or other AGVs. A moving AGV should be able to recognize these obstacles and start
to slow down and stop before collision. In addition, the goods on the AGV should be stable without
sliding.
   Figure 16 shows the scenario in which an AGV is braking. The AGV on the left is moving towards
the right at speed 𝑣 and recognizes an obstacle with the distance of 𝑠 meters. After 𝑑𝑡 seconds

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:21




       Fig. 18. Screenshot of the output for the creation of TDT using Trusta in the context of AGV.




      Fig. 19. Top-level node decomposition: The AGV can stop safely when encountering obstacles.


of reaction time it starts to decelerate and brakes at a distance of 𝑥 meters. In order to avoid a
collision with the obstacle, the left AGV needs to generate sufficient deceleration. However, if the
deceleration is too large, it may cause the goods on the AGV to slide or even fall thus causing a
safety hazard.
   In collaboration with expert users, Trusta facilitated the creation of a TDT. The tool is capable of
automatically translating clearly articulated node contents into constraint expressions and subse-
quently conducting formal reasoning with constraint solvers. Nodes with ambiguous descriptions
can be interactively adjusted by users, as depicted in Figure 23. Within the graphical representation,
blue nodes denote ordinary nodes, green nodes represent newly generated constraint expression

                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:22                                                                            Z. Chen, Y. Deng and W. Du




Fig. 20. Second-level node decomposition: The sensors of the AGV can accurately and timely detect obstacles.


nodes, and yellow nodes are those identified by Trusta, with the assistance of a constraint solver,
as logical risks — specifically, goals where subgoals do not entirely support the parent goal.
   The case of AGV’s automatic braking underwent adjustments, and the final resultant TDT is
shown in Figure 24. It is noteworthy that the strategy information generated during the node
creation phase is now concealed, shifting the focus during the evaluation stage more toward the
translation process of constraint expressions. For a complete TDT with auxiliary information,
refer to Figure 30 in appendix B. Table 2 provides a summary of the node translations depicted
in Figure 24. These translations were accomplished through a large language model (GPT-3.5)
converting natural language into constraint expressions. In Table 2, the “Logical” column has
check marks indicating that the majority of these automated translations were logically coherent.
However, the “Variable” column has check marks denoting that manual adjustments were often
necessary for variable names to be compatible with the constraint solvers. It should be noted that
the first five sentences in the dataset did not explicitly contain constraint information, causing
the language model’s translation efforts to fail. In these instances, manual creation was the only
recourse to ensure correct solver execution.




, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:23




Fig. 21. Second-level node decomposition: The braking system of the AGV can start quickly and safely after
receiving sensor signals.




Fig. 22. Second-level node decomposition: The control system of the AGV can execute safety strategies, such
as deceleration or stopping, after detecting obstacles.


                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:24                                                                                Z. Chen, Y. Deng and W. Du




Fig. 23. Interactive adjustment of nodes in TDT creation: blue nodes represent ordinary nodes; green nodes
symbolize newly generated constraint expression nodes; yellow nodes denote goals where subgoals cannot
fully support the parent goal, indicating logical risks.




Fig. 24. Final TDT for the AGV’s automatic braking case: Illustration of the refined structure after adjustments,
emphasizing the translation result of constraint expressions in the evaluation stage.



, Vol. 00, No. 0, Article 000. Publication date: 2023.
                                                               Table 2. Summary of node translations: comparing automated and manual approaches in constraint expression generation using GPT-3.5.

                                                         No.   Natural language                                        LLM translation                       Logical   Variable   Human adjustment results
                                                          1    The automatic guided trolley can stop safely when
                                                               encountering obstacles
                                                          2    Able to decelerate to a standstill before impact                                                                   𝑥 < 𝑠 − 𝑣 ∗ 𝑑𝑡
                                                          3    The goods on the shelf will not slide                                                                              𝐹𝑚 < 𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛
                                                          4    The trolley can start braking at the appropriate time                                                              𝑠 = 3; 0 < 𝑑𝑡; 𝑑𝑡 < 0.1
                                                          5    The performance of the trolley brake module meets                                                                  0 < 𝑣; 𝑣 <= 1; 0.18 <= 𝑎; 𝑎 <=
                                                               the requirements                                                                                                   0.5; 𝑣 ∗ 𝑣 = 2 ∗ 𝑎 ∗ 𝑥
                                                          6    Obstacle detection distance is 3m                       𝑜𝑏𝑠𝑡𝑎𝑐𝑙𝑒_𝑑𝑖𝑠𝑡𝑎𝑛𝑐𝑒 == 3                  ✓                  𝑠=3
                                                          7    The maximum running speed of the trolley is 1 m/s       𝑡𝑟𝑜𝑙𝑙𝑒𝑦_𝑠𝑝𝑒𝑒𝑑 <= 1                      ✓                  𝑣 <= 1
                                                          8    The minimum acceleration of the trolley is 0.18 𝑚/𝑠 2   𝑡𝑟𝑜𝑙𝑙𝑒𝑦_𝑎𝑐𝑐𝑒𝑙𝑒𝑟𝑎𝑡𝑖𝑜𝑛 >= 0.18            ✓                  0.18 <= 𝑎
                                                          9    Braking reaction time is less than 0.1 s                𝑏𝑟𝑎𝑘𝑖𝑛𝑔_𝑟𝑒𝑎𝑐𝑡𝑖𝑜𝑛_𝑡𝑖𝑚𝑒 < 0.1                                0 < 𝑑𝑡; 𝑑𝑡 < 0.1
                                                         10    The friction coefficient between goods and shelves      𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛_𝑐𝑜𝑒 𝑓 𝑓 𝑖𝑐𝑖𝑒𝑛𝑡 > 0.2          ✓         ✓        𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛_𝑐𝑜𝑒 𝑓 𝑓 𝑖𝑐𝑖𝑒𝑛𝑡 > 0.2
                                                               is greater than 0.2
                                                         11    Cargo mass is 1kg                                       𝑐𝑎𝑟𝑔𝑜_𝑚𝑎𝑠𝑠 == 1                         ✓         ✓        𝑐𝑎𝑟𝑔𝑜_𝑚𝑎𝑠𝑠 = 1
                                                         12    Rate * Rate = 2 * Acceleration * Distance               𝑟𝑎𝑡𝑒 ∗ 𝑟𝑎𝑡𝑒 == 2 ∗ 𝑎𝑐𝑐𝑒𝑙𝑒𝑟𝑎𝑡𝑖𝑜𝑛 ∗       ✓                  𝑣 ∗𝑣 = 2∗𝑎 ∗𝑥
                                                                                                                       𝑑𝑖𝑠𝑡𝑎𝑛𝑐𝑒
                                                         13    The maximum acceleration of the trolley is 0.5𝑚/𝑠 2 𝑡𝑟𝑜𝑙𝑙𝑒𝑦_𝑎𝑐𝑐𝑒𝑙𝑒𝑟𝑎𝑡𝑖𝑜𝑛 <= 0.5                 ✓                  𝑎 <= 0.5
                                                         14    The pressure of goods on the shelf is 9.8 N             𝑠ℎ𝑒𝑙 𝑓 _𝑝𝑟𝑒𝑠𝑠𝑢𝑟𝑒 == 9.8                 ✓                  𝑝𝑟𝑒𝑠𝑠𝑢𝑟𝑒 = 9.8
                                                         15    The acceleration of gravity is 9.8 N/kg                 𝑔𝑟𝑎𝑣𝑖𝑡𝑦_𝑎𝑐𝑐𝑒𝑙𝑒𝑟𝑎𝑡𝑖𝑜𝑛 == 9.8             ✓         ✓        𝑔𝑟𝑎𝑣𝑖𝑡𝑦_𝑎𝑐𝑐𝑒𝑙𝑒𝑟𝑎𝑡𝑖𝑜𝑛 = 9.8
                                                         16    Pressure of object on horizontal plane = mass * grav- 𝑝𝑟𝑒𝑠𝑠𝑢𝑟𝑒 == 𝑚𝑎𝑠𝑠 ∗ 𝑔𝑟𝑎𝑣𝑖𝑡𝑦                ✓                  𝑝𝑟𝑒𝑠𝑠𝑢𝑟𝑒      =      𝑐𝑎𝑟𝑔𝑜_𝑚𝑎𝑠𝑠 ∗
                                                               itational acceleration                                                                                             𝑔𝑟𝑎𝑣𝑖𝑡𝑦_𝑎𝑐𝑐𝑒𝑙𝑒𝑟𝑎𝑡𝑖𝑜𝑛
                                                         17    Friction = friction coefficient * pressure              𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛                        ==     ✓         ✓        𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛                          =
                                                                                                                                                                                                                         Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models




                                                                                                                       𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛_𝑐𝑜𝑒 𝑓 𝑓 𝑖𝑐𝑖𝑒𝑛𝑡 ∗ 𝑝𝑟𝑒𝑠𝑠𝑢𝑟𝑒                        𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛_𝑐𝑜𝑒 𝑓 𝑓 𝑖𝑐𝑖𝑒𝑛𝑡 ∗ 𝑝𝑟𝑒𝑠𝑠𝑢𝑟𝑒
                                                         18    The friction force generated by the goods during 𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛_𝑓 𝑜𝑟𝑐𝑒 < 0.5                         ✓                  𝐹𝑚 <= 0.5
                                                               braking is less than 0.5 N
                                                         19    External force on object = mass * acceleration          𝑒𝑥𝑡_𝑓 𝑜𝑟𝑐𝑒 == 𝑚𝑎𝑠𝑠 ∗ 𝑎𝑐𝑐𝑒𝑙              ✓                  𝐹𝑚 = 𝑐𝑎𝑟𝑔𝑜_𝑚𝑎𝑠𝑠 ∗ 𝑎
                                                         20    The friction force that the shelf can give to the goods 𝑠ℎ𝑒𝑙 𝑓 _𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛_𝑓 𝑜𝑟𝑐𝑒 > 0.5          ✓                  𝑓 𝑟𝑖𝑐𝑡𝑖𝑜𝑛 > 0.5
                                                               is greater than 0.5 N




, Vol. 00, No. 0, Article 000. Publication date: 2023.
                                                                                                                                                                                                                         000:25
000:26                                                                             Z. Chen, Y. Deng and W. Du


                          Table 3. Physical kinematic equations used in the AGV example

                   Equation                            Detail
                      𝑠 = 𝑣𝑡           𝑠 (displacement), 𝑣 (velocity), 𝑡 (time)
                    𝑣 2 = 2𝑎𝑥    𝑣 (velocity), 𝑎 (acceleration), 𝑥 (displacement)
                   𝐹 𝑁 = 𝑚𝑔 𝐹 𝑁 (normal force), 𝑚 (mass), 𝑔 (acceleration of gravity)
                    𝐹 = 𝑢𝐹 𝑁    𝐹 (sliding friction force), 𝑢 (frictional coefficient)


   The fragment of a TDT shown in Figure 24 aims to demonstrate that an AGV can safely brake
when it encounters an obstacle. As previously mentioned, TDTs can be converted into assurance
cases, and the GSN format corresponding to Figure 24 can be specifically found in Figure 31 of
appendix B. The top node has two subtrees: the left subtree argues that an AGV will not collide
with obstacles, and the right one demonstrates that the goods on the AGV will not slide. The left
subtree is argued with the help of the uniformly variable linear motion equations, which are given
in Table 3. The data for those parameters can be taken from the AGV’s reference manual. The
maximum running speed is 𝑣 = 1𝑚/𝑠, and the maximum deceleration is 𝑎 = 0.5𝑚/𝑠 2 . The right
subtree argues with the help of the equation for static friction. Usually, the coefficient of friction
between the goods and the shelf on top of the AGV is greater than 0.2.
   The development of the TDT uncovers some details that should be carefully considered. For
example, on one hand we should set the minimum deceleration parameter of the AGV, as otherwise
a collision may occur during braking, and on the other hand it is more noteworthy to consider the
materials of the goods’ packaging and shelves. The coefficient of static friction of the corresponding
material should exceed a certain value to ensure the stability of the goods. Trusta turns out to be
helpful for the tuning of parameters. The construction and automatic evaluation of the TDT in this
study case increase our confidence in the safe use of AGVs.

5   RELATED WORK
Several assurance case editors have been developed to support GSN [2, 12, 20, 43, 62]. They facilitate
the development and maintenance of assurance cases. Some of them offer assurance case patterns
for users to reuse existing assurance cases [43, 62]. Luo et al. [41] provided an excellent survey of
assurance case tools and summarized a systematic process of assurance case assessment. They also
developed a tool to facilitate human evaluation. Chowdhury et al. [13] proposed a set of rules that
semi-formally define the structure and content of assurance cases. These rules guide the work of
assurance cases developers and reviewers. Assurance cases developers are instructed to use a more
rigorous approach to their arguments. External reviewers have a basic checklist that guides them
in assessing the rigor of arguments. Maksimov et al. [42] surveyed ten assurance case tools with
evaluation capabilities. These tools can examine both the structure and content of assurance cases.
Structural checks include structural constraints, correctness, integrity checks, and user queries.
Content checks include argument evaluation, evidence evaluation, evaluation tracking, evaluation
report, and evaluation interaction. Different tools utilize different approaches for content checks
such as type checking, Bayesian belief networks and Dempster-Shafer Theory. The only tool that
uses a formal logic is Resolute [51]. Similar to Trusta, Resolute is inspired by logic programming
and accompanies claims with user-defined logical rules for formal analysis, but SMT solvers are
not incorporated.
   Among these tools, AdvoCATE [19] stands out with a relatively higher degree of automation. It
utilizes high-level argument patterns to assist in the assurance case creation process. By interpreting
these templates, AdvoCATE can formulate detailed arguments, either interactively or through

, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                                 000:27


external data. Although its P-table structure effectively directs pattern instantiation, potential
challenges may arise when dealing with intricate or non-conventional assurance scenarios, possibly
affecting its versatility in diverse contexts.
   Although there are many types of assurance case tools, the current assurance case tools are still
immature. Most creation and evaluation techniques they support still rely heavily on manual work.
The content and evidence in the assurance case are primarily in the form of natural language. The
validity of assurance case decomposition cannot be demonstrated.
   In [18], we introduced TDTs as a more compact representation of assurance cases without losing
their expressive power. We gave a visualization tool that used Prolog syntax for importing and
exporting TDT data. Basic soundness checking of TDTs cannot be carried out within the tool itself,
but can be turned into the validity checking of propositional logical formulas and then performed
by an external Prolog inference engine.
   We note that the assessment of assurance cases plays a vital role in safety engineering. Although
some tools have been developed to assist assessors in judging the correctness of assurance cases,
they are far from being sufficiently automated. The accuracy of assessment is susceptible to human
subjective factors. The creation of assurance cases is largely a manual endeavor, further underscoring
the low levels of automation in this domain. In addition, finding bugs and tweaking them after an
assurance case is developed often waste a lot of time.

6 CONCLUSION AND FUTURE DIRECTIONS
We have presented Trusta, a tool that allows for safety modeling and automatic validation, as well
as a detailed report on safety vulnerabilities. The TDTs created by this tool can be adapted from
assurance cases by adding formal expressions, which can be used by constraint solvers to perform
formal reasoning. With the integration of large language models, Trusta also brings convenience in
creating safety cases, and assists users in translating natural language into constraint expressions,
streamlining the overall process. In fact, within the Trusta tool, TDT and traditional GSN can be
mutually converted. It can be observed that, without losing any information, the TDT representation
is more compact, emphasizing key points, making it more easily readable. Our experiments with
more than a dozen industrial cases show that Trusta is helpful to identify issues that are easily
overlooked by manual inspection.
   Looking forward to the future development of Trusta, several promising directions emerge. First,
there is an opportunity to trial and compare various large language models to discern the most
effective ones for specific tasks among a few assurance cases. Such comparative studies may pave
the way for nuanced insights and enhanced efficiencies. Second, by integrating more theoretical
knowledge, we can optimize prompt words to guide the models more effectively, harnessing their
potential in a more targeted manner. Third, the fine-tuning of these large language models to tailor
their performance in specialized tasks is an exciting avenue for research. By customizing these
models to the unique requirements of the safety domain, we anticipate significant advancements
in their applicability and accuracy. Finally, the integration and development of additional formal
languages within Trusta will broaden the horizons of automatic reasoning within TDTs, making it
more versatile and universally applicable. These future endeavors signal a robust pathway towards
more comprehensive, adaptable, and intelligent safety modeling and validation.

REFERENCES
 [1] ISO 26262. 2011. Road Vehicles-Functional Safety. (2011). https://www.iso.org/standard/43464.html
 [2] ACEdit. 2016. (2016). https://code.google.com/p/acedit/.
 [3] Rebekah Austin, Nagabhushan Mahadevan, Brian Sierawski, Gabor Karsai, Arthur Witulski, and John Evans. 2017.
     A CubeSat-payload radiation-reliability assurance case using goal structuring notation. In In Proceedings of the 2017


                                                                       , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:28                                                                                           Z. Chen, Y. Deng and W. Du


     Annual Reliability and Maintainability Symposium. IEEE, 1–8.
 [4] Michael Baram. 2010. Preventing accidents in offshore oil and gas operations: the US approach and some contrasting
     features of the Norwegian approach. Technical Report. Boston University School of Law.
 [5] Julie Beugin, Cyril Legrand, Juliette Marais, Marion Berbineau, and El-Miloudi El-Koursi. 2018. Safety appraisal of
     GNSS-based localization systems used in train spacing control. IEEE Access 6 (2018), 9898–9916.
 [6] Peter Bishop and Robin Bloomfield. 1998. A methodology for safety case development, Industrial Perspectives of
     Safety-Critical Systems. In Proceedings of the sixth safety-critical systems symposium.
 [7] Robin Bloomfield and Peter Bishop. 2009. Safety and assurance cases: Past, present and possible future–an Adelard
     perspective. In In Proceedings of the Making Systems Safer. Springer London, 51–67.
 [8] Robin Bloomfield, Peter Bishop, Eoin Butler, and Kate Netkachova. 2017. Using an assurance case framework to develop
     security strategy and policies. In In Proceedings of the Computer Safety, Reliability, and Security. Springer International
     Publishing, 27–38.
 [9] Robin Bloomfield, Nick Chozos, George Cleland, and LLP Adelard. 2012. Safety case use within the medical devices
     industry. In Supplements to: Using safety cases in industry and healthcare. The Health Foundation, London, 75–91.
[10] Robin Bloomfield and John Rushby. 2020. Assurance 2.0: A manifesto. arXiv preprint arXiv:2004.10474 (2020).
[11] Hamza Bourbouh, Marie Farrell, Anastasia Mavridou, Irfan Sljivo, Guillaume Brat, Louise Dennis, and Michael Fisher.
     2021. Integrating formal verification and assurance: an inspection rover case study. In In Proceedings of the NASA
     Formal Methods. Springer International Publishing, 53–71.
[12] CertWare. 2016. (2016). http://nasa.github.io/CertWare/.
[13] Thomas Chowdhury, Alan Wassyng, Richard F Paige, and Mark Lawford. 2020. Systematic evaluation of (safety)
     assurance cases. In International Conference on Computer Safety, Reliability, and Security. Springer, 18–33.
[14] George Cleland, Mark-Alexander Sujan, Ibrahim Habli, and John Medhurst. 2012. Evidence: using safety cases in
     industry and healthcare. The Health Foundation. 1–32 pages.
[15] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Caroline Trippel. 2023. nl2spec: Interac-
     tively Translating Unstructured Natural Language to Temporal Logics with Large Language Models. In International
     Conference on Computer Aided Verification. Springer.
[16] National Research Council. 2007. Software for dependable systems: Sufficient evidence? National Academies Press.
[17] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In International conference on Tools and
     Algorithms for the Construction and Analysis of Systems. Springer, 337–340.
[18] Yuxin Deng, Zezhong Chen, Wenjie Du, Bifei Mao, Zhizhang Liang, Qiushi Lin, and Jinghui Li. 2021. Trustworthiness
     Derivation Tree: A Model of Evidence-Based Software Trustworthiness. In Proceedings of the 21st International
     Conference on Software Quality, Reliability and Security Companion (QRS-C). IEEE, 487–493.
[19] Ewen Denney and Ganesh Pai. 2018. Tool support for assurance case development. Automated Software Engineering
     25, 3 (2018), 435–499.
[20] Ewen Denney, Ganesh Pai, and Josef Pohl. 2012. AdvoCATE: An assurance case automation toolset. In International
     Conference on Computer Safety, Reliability, and Security. Springer, 8–21.
[21] DO-178C. 2011. Software Considerations in Airborne Systems and Equipment Certification. (2011). https://www.
     do178.org/
[22] Bob Duncan and Mark Whittington. 2014. Compliance with standards, assurance and audit: does this equal security?.
     In In Proceedings of the 7th International Conference on Security of Information and Networks. Association for Computing
     Machinery, 77–84.
[23] Google. 2023. Introducing PaLM 2. (2023). https://ai.google/discover/palm2/.
[24] Patrick Graydon, John Knight, and Elisabeth Strunk. 2007. Assurance based development of critical systems. In In
     Proceedings of the 37th Annual IEEE/IFIP International Conference on Dependable Systems and Networks. IEEE, 347–357.
[25] Gerhard Griessnig and Adam Schnellbach. 2017. Development of the 2nd Edition of the ISO 26262. In In Proceedings of
     the Systems, Software and Services Process Improvement. Springer International Publishing, 535–546.
[26] The Assurance Case Working Group. 2021. Goal Structuring Notation Community Standard Version 3. (2021).
     https://scsc.uk/SCSC-141C.
[27] Ibrahim Habli, Rob Alexander, Richard Hawkins, Mark Sujan, John McDermid, Chiara Picardi, and Tom Lawton.
     2020. Enhancing Covid-19 Decision-Making by Creating an Assurance Case for Simulation Models. arXiv preprint
     arXiv:2005.08381 (2020).
[28] Jamie Henderson. 2012. Safety case use in the petrochemical industry. In Supplements to: Using safety cases in industry
     and healthcare. The Health Foundation, London, 55–64.
[29] ISO/IEC 15026. 2011. Systems and Software Engineering-Systems and Software Assurance-Part 2: Assurance Case.
     (2011). https://www.iso.org/standard/52926.html
[30] Joxan Jaffar and Michael J Maher. 1994. Constraint logic programming: A survey. The journal of logic programming 19
     (1994), 503–581.


, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                                    000:29


[31] Eunkyoung Jee, Insup Lee, and Oleg Sokolsky. 2010. Assurance cases in model-driven development of the pacemaker
     software. In In Proceedings of the Leveraging Applications of Formal Methods, Verification, and Validation. Springer
     Berlin Heidelberg, 343–356.
[32] Tim Kelly. 1999. Arguing safety: a systematic approach to managing safety cases. PhD thesis. University of York,
     Heslington, York, England.
[33] Tim Kelly. 2004. A systematic approach to safety case management. Journal of Passenger Cars: Electronic and Electrical
     Systems 113, 7 (2004), 257–266.
[34] Tim Kelly. 2012. Safety case use in the defence industry. In Supplements to: Using safety cases in industry and healthcare.
     The Health Foundation, London, 19–23.
[35] Tim Kelly, Iain Bate, John McDermid, and Alan Burns. 1997. Building a preliminary safety case: An example from
     aerospace. In In Proceedings of the Australian Workshop on Industrial Experience with Safety Critical Systems and Software.
     Not available, 1–10.
[36] Tim Kelly and Rob Weaver. 2004. The goal structuring notation–a safety argument notation. In In Proceedings of the
     Dependable Systems and Networks 2004 Workshop on Assurance Cases. Citeseer.
[37] Nils Klarlund and Anders Møller. 2001. Mona version 1.4: User manual. BRICS, Department of Computer Science,
     University of Aarhus Denmark.
[38] Brian Larson, John Hatcliff, and Patrice Chalin. 2013. Open source patient-controlled analgesic pump requirements
     documentation. In In Proceedings of the 5th International Workshop on Software Engineering in Health Care. IEEE, 28–34.
[39] Nancy Leveson. 2011. The Use of Safety Cases in Certification and Regulation. Technical Report. Massachusetts Institute
     of Technology Engineering Systems Division.
[40] Robert Lewis. 2009. Safety case development as an information modelling problem. In Safety-Critical Systems: Problems,
     Process and Practice. Springer, 183–193.
[41] Yaping Luo, Mark van den Brand, Zhuoao Li, and Arash Khabbaz Saberi. 2017. A systematic approach and tool support
     for GSN-based safety case assessment. Journal of Systems Architecture 76 (2017), 1–16.
[42] Mike Maksimov, Sahar Kokaly, and Marsha Chechik. 2019. A survey of tool-supported assurance case assessment
     techniques. Comput. Surveys 52, 5 (2019), 1–34.
[43] Yutaka Matsuno. 2011. D-case editor: A typed assurance case editor. University of Tokyo (2011).
[44] John Medhurst and David Embrey. 2012. Safety case use in the railway industry. In Supplements to: Using safety cases
     in industry and healthcare. The Health Foundation, London, 65–74.
[45] Pietro Mendes, Jeremy Hall, Stelvia Matos, and Bruno Silvestre. 2014. Reforming Brazil’s offshore oil and gas safety
     regulatory framework: Lessons from Norway, the United Kingdom and the United States. Energy Policy 74 (2014),
     443–453.
[46] Kateryna Netkachova, Oleksandr Netkachov, and Robin Bloomfield. 2014. Tool support for assurance case building
     blocks. In International Conference on Computer Safety, Reliability, and Security. Springer, 62–71.
[47] OpenAI. 2023. Create chat completion. (2023). https://platform.openai.com/docs/api-reference/chat.
[48] OpenAI. 2023. GPT-3.5 Documentation. (2023). https://platform.openai.com/docs/models/gpt-3-5.
[49] OpenAI. 2023. GPT-4 Documentation. (2023). https://platform.openai.com/docs/models/gpt-4.
[50] Robert Palin and Ibrahim Habli. 2010. Assurance of automotive safety–a safety case approach. In In Proceedings of the
     Computer Safety, Reliability, and Security. Springer Berlin Heidelberg, 82–96.
[51] Resolute. 2016. (2016). https://github.com/smaccm/smaccm/.
[52] David J Rinehart, John C Knight, and Jonathan Rowanhill. 2015. Current practices in constructing and evaluating
     assurance cases with applications to aviation. National Aeronautics and Space Administration, Langley Research Center.
[53] David J Rinehart, John C Knight, and Jonathan Rowanhill. 2017. Understanding What It Means for Assurance Cases to
     “Work”. Technical Report.
[54] Francesca Rossi, Peter Van Beek, and Toby Walsh. 2008. Constraint programming. Foundations of Artificial Intelligence
     3 (2008), 181–211.
[55] John Rushby, Xidong Xu, Murali Rangarajan, and Thomas Weaver. 2015. Understanding and evaluating assurance cases.
     Technical Report. NASA Langley Research Center.
[56] Farrukh Shahzad, Tarek R Sheltami, Elhadi M Shakshuki, and Omar Shaikh. 2016. A review of latest web tools and
     libraries for state-of-the-art visualization. Procedia Computer Science 98 (2016), 100–106.
[57] Vladimir Sklyar and Vyacheslav Kharchenko. 2020. Assurance case for safety and security implementation: a survey
     of applications. International Journal of Computing 19, 4 (2020), 610–619.
[58] Mark A Sujan, Ibrahim Habli, Tim P Kelly, Simone Pozzi, and Christopher W Johnson. 2016. Should healthcare
     providers do safety cases? Lessons from a cross-industry review of safety case practices. Safety Science 84 (2016),
     181–189.
[59] Stephen Toulmin. 2003. The Uses of Argument. Cambridge university press, England. 1–247 pages.



                                                                          , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:30                                                                                      Z. Chen, Y. Deng and W. Du


[60] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia
     Polosukhin. 2017. Attention is all you need. Advances in neural information processing systems 30 (2017).
[61] Michael Vierhauser, Sean Bayley, Jane Wyngaard, Wandi Xiong, Jinghui Cheng, Joshua Huseman, Robyn Lutz, and
     Jane Cleland-Huang. 2019. Interlocking safety cases for unmanned autonomous systems in shared airspaces. IEEE
     transactions on software engineering 47, 5 (2019), 899–918.
[62] Sebastian Voss, Bernhard Schätz, Maged Khalil, and Carmen Carlan. 2013. Towards modular certification using
     integrated model-based safety cases. In Proc. VeriSure: Verification and Assurance Workshop.
[63] Alan Wassyng, Tom Maibaum, Mark Lawford, and Hans Bherer. 2011. Software certification: Is there a case against
     safety cases?. In In Proceedings of the Foundations of Computer Software. Modeling, Development, and Verification of
     Adaptive Systems. Springer Berlin Heidelberg, 206–227.
[64] Evi Widowati, Adi Sutomo, and Wahyudi Istiono. 2021. Are Elementary Schools Ready for Disaster Preparedness and
     Safety? E3S Web Conf. 317 (2021), 1–13.
[65] Joshua Willman. 2021. Overview of PyQt5. In Modern PyQt. Springer, 1–42.

A    CONVERSION BETWEEN GSN AND TDT FORMATS
In this appendix, we present an illustrative example demonstrating the mutual conversion between
an assurance case in Goal Structuring Notation (GSN) format and a Trustworthiness Derivation
Tree (TDT). The example is inspired by the work of Austin et al. [3], where they employ GSN to
express an assurance case for system-level mitigation of radiation effects in a CubeSat science
experiment.
   Figure 25 shows the original GSN, and Figures 26, 27, and 28 are enlargements displaying various
parts of Figure 25 in detail. Figure 29 represents the conversion into TDT format. In fact, TDT can
also be translated back into GSN format using the Trusta tool. It can be observed that without
losing any information, the TDT representation is more compact and emphasizes the key points,
making it easier to read.




, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                                                                                         000:31




                                                                                                             Fig. 25. A CubeSat-payload radiation-reliability assurance case using goal structuring notation.




                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:32                                                   Z. Chen, Y. Deng and W. Du




                                                                              Fig. 26. Top-level GSN hierarchy.




, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:33




                                                                                                                  Fig. 27. Parts characterization hierarchy.




                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:34                                                   Z. Chen, Y. Deng and W. Du




                                                                        Fig. 28. System-level mitigation hierarchy.




, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:35


  By providing the GSN to TDT conversion, we offer a bridge between traditional assurance case
methodology and the more automated, formalized process enabled by Trusta. This facilitates a
smooth transition for practitioners familiar with GSN, opening the door to the benefits of automatic
reasoning and error detection in the assurance case development process.

B   THE GSN FORMAT OF THE AGV EXAMPLE
This appendix presents two figures. Figure 30 depicts the comprehensive TDT, serving as the
complete version of what is shown in Figure 24 from the main text. Figure 31 provides a graphical
representation of this TDT in the GSN format.
   In the TDT of Figure 30, each node corresponds directly to either a goal or solution in the GSN
representation. When transitioning to the GSN format, the auxiliary components, namely contexts,
assumptions, justifications, and strategies, are captured within the descriptions of the TDT nodes
in Figure 30.
   Collectively, these figures present a robust argument, underscoring the ability of the AGV to
safely brake when encountering obstacles, thereby visualizing the detailed assurance case.




                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:36                                                                            Z. Chen, Y. Deng and W. Du




   Fig. 29. A CubeSat-payload radiation-reliability assurance case using trustworthiness derivation tree.




, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:37




                                                                                                                 Fig. 30. The AGV example in TDT format.




                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
000:38                                                   Z. Chen, Y. Deng and W. Du




                                                                         Fig. 31. The AGV example in GSN format.




, Vol. 00, No. 0, Article 000. Publication date: 2023.
Trusta: Reasoning about Assurance Cases with Formal Methods and Large Language Models                          000:39


Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009




                                                                , Vol. 00, No. 0, Article 000. Publication date: 2023.
