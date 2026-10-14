                                             Towards Practical Requirement Analysis and
                                              Verification: A Case Study on Software IP
                                             Components in Aerospace Embedded Systems

                                          Zhi Ma1,2 , Cheng Wen2 , Jie Su2 , Ming Zhao3 , Bin Yu1,⋆ , Xu Lu1 , and Cong
                                                                             Tian1,⋆
arXiv:2404.00795v1 [cs.SE] 31 Mar 2024




                                                          1
                                                            ICTT and ISN Laboratory, Xidian University, China
                                                     2
                                                         Guangzhou Institute of Technology, Xidian University, China
                                                             3
                                                               Beijing Institute of Control Engineering, China
                                                 Abstract. IP-based software design is a crucial research field that aims
                                                 to improve efficiency and reliability by reusing complex software com-
                                                 ponents known as intellectual property (IP) components. To ensure the
                                                 reusability of these components, particularly in security-sensitive soft-
                                                 ware systems, it is necessary to analyze the requirements and perform for-
                                                 mal verification for each IP component. However, converting the require-
                                                 ments of IP components from natural language descriptions to temporal
                                                 logic and subsequently conducting formal verification demands domain
                                                 expertise and non-trivial manpower. This paper presents a case study
                                                 on software IP components derived from aerospace embedded systems,
                                                 with the objective of automating the requirement analysis and verifica-
                                                 tion process. The study begins by employing Large Language Models to
                                                 convert unstructured natural language into formal specifications. Subse-
                                                 quently, three distinct verification techniques are employed to ascertain
                                                 whether the source code meets the extracted temporal logic properties.
                                                 By doing so, five real-world IP components from the China Academy of
                                                 Space Technology (CAST) have been successfully verified.


                                         1     Introduction
                                         Background and Its Importance. Software systems are becoming increas-
                                         ingly complex and diverse, requiring high levels of efficiency and reliability. One
                                         way to achieve these goals is to reuse existing software components that have
                                         been proven to work well in different contexts. These components are known as
                                         intellectual property components (components of intellectual property, or simply
                                         IP components) [1,2,3], and they can range from simple functions to entire sub-
                                         systems. IP-based software design is a crucial research field that aims to facilitate
                                         and optimize the reuse of IP components across various software systems [4,5,6].
                                             However, reusing IP components is not a trivial task. It requires ensuring that
                                         the components meet the specific requirements or specifications of the target
                                         system, and that they do not introduce any errors or vulnerabilities. Therefore,
                                         it is necessary to analyze the requirements and perform formal verification for
                                         each IP component before integrating it into the system. This process involves
                                         converting the natural language descriptions of the requirements into formal
                                         ⋆
                                             Corresponding authors: Cong Tian and Bin Yu
2      Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian




                        Fig. 1: The workflow of our study
logic expressions, and then checking whether the source code of the component
satisfies these expressions. However, this process is often time-consuming and
labor-intensive, as it demands domain expertise and manual intervention.
    Research Problem and Gap. Despite the advancements in IP-based soft-
ware design, there is still a lack of effective and automated methods for analyzing
and verifying IP components, especially in security-sensitive software systems.
These systems have strict requirements that must be thoroughly verified to en-
sure safety and reliability. Typically, these complex requirements are expressed
in natural language, incorporating domain knowledge, and require a significant
time investment for understanding [7,8,9]. Additionally, these systems often use
IP components from different sources and domains, adding to the complexity
of verification tasks. Therefore, there is a critical need for a comprehensive ap-
proach to automated requirements analysis and verification for IP components.
    Our Objective and Contributions. In this paper, we present a case study
on software IP components derived from aerospace embedded systems, with the
objective of automating the requirement analysis and verification process. As il-
lustrated in Fig. 1, our approach consists of two modules: (1) the construction of
a prompting engineering framework utilizing Large Language Models (LLMs) to
transform unstructured natural language into Linear Temporal Logic (LTL), en-
capsulating this process into an automated tool to reduce the costs and barriers
to formalization application; (2) the use of three distinct verification techniques
to ascertain whether the source code meets the extracted temporal logic prop-
erties, ensuring the consistency of software requirements and code from various
perspectives. By doing so, we successfully verified five real-world IP components
from the China Academy of Space Technology (CAST), demonstrating the fea-
sibility and effectiveness of our approach.

2   Background and IP Example
Background of Aerospace Embedded Software IP. Functional modules in
software can be represented using a input-output model. The execution of a func-
tional module involves three steps: input, calculation, and output. Firstly, the
                                    Title Suppressed Due to Excessive Length      3


                      Input           Software IP        Output
                       Port           Component           Port




                                        Formal            Knowedge
               Implementation
                                        Model              Model
                                ⊨                   ⊨

          Fig. 2: A General Model for Aerospace Embedded Software IP
input end acquires the necessary computational resources. Then, the computa-
tion is performed. Finally, the output end produces the computation result. The
interpretation of the input and output may vary, resulting in different software
models. In contrast to general software functional modules, software intellectual
property (IP) refers to reusable software knowledge entities that have intellectual
property rights. It includes software that has specific functions and is charac-
terized by clear contextual dependencies, interface definitions, comprehensive
design documentation, and rigorous quality verification [10].
    A software IP with a proper structure should reflect its key characteris-
tics accurately and comprehensively throughout its creation and utilization. It
abstracts and consolidates the software knowledge of developers, forming the
foundational concept for reusing complex software components. Generally, the
representation model for software IP consists of the following triplets:
                              IP = (KL, F M, IM P )                              (1)
Where KL denotes the knowledge model, F M denotes the formal model, and
IM P denotes the implementation.
    A knowledge model is a structured representation of the knowledge within
software IP, which is the most abstract and information-rich aspect. Knowledge
models usually use informal natural language and graphical models, while for-
mal models use formal language. The implementation mainly involves program
code. From an abstract and refined perspective, the knowledge model covers
the entire lifecycle of software IP, providing it with the most extensive content.
The knowledge model helps developers and users understand software IPs from
different perspectives. It also enables the search, adaptation, and assembly of
software IPs. A formal model represents the knowledge model formally. Unlike
knowledge models, formal models allow a deeper understanding of software IPs.
They bridge the cognitive gap between software IP creators and users and pro-
vide security guarantees for intelligent software synthesis. Finally, the program
code in the implementation must match the description in the formal model, as
shown in Fig. 2. Therefore, to ensure the reusability and trustworthiness of the
IP component, we need to verify that:
                               IM P |= F M |= KL                                 (2)
that is, we need to verify that the implementation conforms to the formal proper-
ties, and that the formal properties reflect the essential knowledge of the software
IP. In other words, the implementation, the formal specification, and the knowl-
edge representation of the software IP are consistent and compatible with each
4        Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian
Table 1: Variables in struct Fg333saCheck are presented in a table in the document
Data Name Data Type Category Explanation
buffer      uint8*   input port The input string buffer
rdLen       uint32   input port Length of the input string buffer
frm         uint32 state variable Frame count
...           ...  state variable ...
bComSuc     uint32  output port A flag indicates whether the validation success
cntLenRd    int32   output port Continuous read length error count
cntHead     int32   output port Continuous frame header error count
cntCheck    int32   output port Continuous check error count
cntUpdata   int32   output port Continuous data update error count
totalLenRd  int32   output port Total read length error count
totalHead   int32   output port Total frame header error count
totalCheck  int32   output port Total check error count
totalUpdata int32   output port Total data update error count
...           ...   output port ...

              Table 2: Requirement in Natural Language Description
    This IP is used to verify whether the data received by the sensor meets the standard
    of the Fg333 type fiber optic gyroscope communication protocol. The verification
    rules are as follows:
    1. Validate the data length for correctness: if the length is not 19, increment
       cntLenRd and totalLenRd + 1, and return a validation failure.
    2. Validate whether the frame count is updated: if the frame count is not updated,
       increment cntUpdata and totalUpdata + 1, and return a validation failure.
    3. Validate whether the frame header is correct: if the frame header is not 0xAC12,
       increment cntHead and totalHead + 1, and return a validation failure.
    4. Validate whether the checksum is correct: if the checksum is correct, return
       validation success; otherwise, return validation failure.


other. This way, we can ensure that the software IP is developed according to
the abstract design and meets the desired functionality and quality.
     An Industrial IP Example. In the following, we provide an illustrative
example of industrial software IP. The purpose of this example is to motivate
our research and highlight the complexities involved in analyzing and verifying
IP components for aerospace embedded systems. It is important to note that
the software IP components we analyzed and verified were obtained from China
Academy of Space Technology (CAST). Due to the confidentiality of CAST, we
are unable to publicly share these IP components. Therefore, the requirement
description and code implementation of the IP example presented in our paper
has been simplified and abstracted.
     The provided Software IP component, namely Fg333saCheck, implements
the Fg333 fiber optic gyroscope communication protocol validation algorithm,
which is a method to check whether the data received from a fiber optic gyroscope
(FOG) is correct and consistent with the expected format. A FOG is a device that
measures the angular velocity of a moving object by detecting the interference
of light waves in a closed loop of optical fiber. There are different types of FOGs,
such as closed-loop and open-loop, that use different control and demodulation
algorithms. The validation algorithm depends on the specific FOG model and
                                       Title Suppressed Due to Excessive Length    5

                                  Member Function
                            fun1()       fun2()      fun3()     ...
      Input               write                                read
                                                                       Output
       Port                           Private Variable                  Port
                            State        Parameter        Local
                           Variable       Variable       Variable


                     Fig. 3: Implementation of Software IP
protocol. One example of a FOG protocol is the Fg333 protocol, which uses
a 19-byte data frame with a frame header, a frame count, a checksum, and
other information. The validation algorithm for this protocol involves verifying
the data length, the frame count, the frame header, and the checksum of each
data frame. The validation algorithm is important for ensuring the accuracy and
reliability of the FOG data, which can be used for various aerospace applications
such as navigation, positioning, and attitude control [11].
    The software IP is associated with a comprehensive knowledge model that
combines fundamental information, domain expert knowledge, and software de-
velopment process knowledge. This includes the documentation of software re-
quirements and design, which is typically expressed in natural language. In this
specific case, the requirements and design documentation are contained within
a three-page Word document. We provide below a partial excerpt of the natu-
ral language description of the knowledge model, comprising two modules. The
first module consists of interface description information for inputs and outputs,
as illustrated in Table 1. This module includes interface function names, types,
and explanations. The second module consists of the IP’s requirement specifica-
tion document, as depicted in Table 2, wherein functional requirements of the
IP are documented in natural language. We can see that the knowledge model
is articulated entirely in natural language. In order to ensure consistency be-
tween the code implementation, the formal model, and this knowledge, domain
knowledge validators often need to manually convert the information into LTL
formulas [12,13]. This task requires significant expertise and time, as it necessi-
tates a deep understanding of the knowledge model.
    The formal model of this IP is a specification described using formal lan-
guage, which has the characteristics of normativity and non-ambiguity. Using
formal language to describe software IP can minimize the cognitive gap between
software IP creators and users, which is beneficial for correctly understanding
the meaning of software IP and providing guidance and security guarantees for
its reuse. In general, for a given program M , based on Floyd-Hoare logic [14,15],
its formal model can be represented as a Hoare triplet:
                                         {p} M {q}                                (3)
Here, p denotes the property that M ’s input satisfies (precondition), and q rep-
resents the property that the output satisfies after the execution of M (post-
condition). The assertion (p, q) defines the program M ’s contract. The formal
model serves as a bridge between requirements expressed in natural language
formats and the implementation of code written in programming languages. It
6        Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian
 1 // Interface.h
 2 extern void Fg333saCheckFun(void *p);
 3
 4 // Entity.c
 5 void Fg333saCheckFun(Fg333saCheck *is) {
 6     uint08 chksum;
 7     is->bComSuc = FALSE;
 8     if (is->rdLen == 19) {
 9         is->cntLenRd = 0;
10         if (is->buffer[17] != (is->frm)) {
11             is->cntUpdata = 0;
12             is->frm = is->buffer[17];
13             if ((is->buffer[0] == 0xAC) && (is->buffer[1] ==   0x12)) {
14                 is->cntHead = 0;
15                 chksum = CheckSumAdd08(&is->buffer[0], 18);
16                 if (chksum == is->buffer[18]) {
17                     is->cntCheck = 0;
18                     is->bComSuc = TRUE;
19                 } else {
20                     is->cntCheck++;
21                     is->totalCheck++;
22                 }
23             } else {
24                 is->cntHead++;
25                 is->totalHead++;
26             }
27         } else {
28             is->cntUpdata++;
29             is->totalUpdata++;
30         }
31     } else {
32         is->cntLenRd++;
33         is->totalLenRd++;
34     }
35     return;
36 }


                      Listing 1.1: Partial Implementation Sample
requires the manual abstraction of knowledge models and code implementations
and must undergo rigorous formal verification before it can be used.
    The implementation of a software IP comprises two parts: the interface and
the entity, as illustrated in Fig. 3. The interface represents the visible components
of a software IP. Each software IP exposes only one interface to the external
world, consisting of input and output ports. While the entity consists of two
parts: private variables and member functions. Private variables are exclusively
used internally within the software IP, shared among internal member functions,
and remain invisible externally. External access to private variables can only
occur through the ports.
    A partial implementation sample of Fg333 protocol validationis presented in
Listing 1.1. The interface can be declared within the .h file of the software IP
code, allowing external environments to access the software IP interface solely
through the Fg333saCheckFun function, without requiring knowledge of the in-
terface’s implementation details. The entity of a software IP exists in the form
of a .c (source file) or .a (compiled static link library), representing the specific
implementation of the software IP’s functionality.

3     LTL Property Mining
In the field of software engineering, the translation of software requirement doc-
uments from natural language to formal language is a crucial and complex pro-
cess. This step is vital for ensuring the accuracy and consistency of require-
ments, serving as an input for the formal verification of software properties.
                                  Title Suppressed Due to Excessive Length        7

By utilizing Large Language Models (LLMs) like OpenAI’s GPT series [16,17],
Google’s BERT [18], and T5, which leverage deep learning technology, significant
progress has been made in this domain [7,19,20,21]. These sophisticated tools are
specifically designed to comprehend and generate human language. Through the
analysis and processing of vast amounts of textual data, these models acquire
an understanding of the intricate structures and patterns of language. The key
benefits of these models include 1. Advanced Language Comprehension - their
ability to deeply understand the subtle semantics and context within natural
language is crucial for accurately interpreting software requirement documents.
2. Flexible Text Generation - these models not only understand natural lan-
guage but can also generate formal language descriptions that adhere to specific
grammatical and formatting requirements. 3. Adaptability and Versatility - they
can be applied to various software engineering tasks and different programming
contexts, handling requirement documents with diverse styles and structures.
4. Continuous Learning and Improvement - as these models are continuously
trained, their ability to comprehend complex requirements and generate precise
formalized descriptions is consistently enhanced. 5. Automation and Efficiency
- the use of LLMs can reduce the cost of verification efforts and make it easier
to adopt formal methods.
    While Large Language Models (LLMs) offer a promising solution for trans-
lating natural language into formal language, increasing automation in the verifi-
cation process, reducing costs related to formal methods, and lowering adoption
barriers, there are challenges. Knowledge models written in natural language of-
ten lack standardization and precision, and not all requirement descriptions can
be easily converted into formal specifications. These factors significantly impact
the accuracy and reliability of outcomes. For instance, in Table 2 of the knowl-
edge model, the requirement descriptions for the first three functionalities are
non-standard and mix natural language with mathematical symbols.
    Mining Process. To enhance the accuracy and success rate of transforming
natural language into formal language, we have divided the mining of the IP
knowledge model into the following three steps:
1. Filter requirement descriptions that contain temporal properties in prepara-
   tion for translation into Linear Temporal Logic (LTL);
2. Standardize the natural language obtained in the first step, and refine abstract
   variable descriptive nouns into variable names at the code level;
3. Translate the intermediate results obtained in the 2nd step into LTL formulas.

3.1   Step I: Requirements Description Filtering.

This initial phase involves identifying and selecting requirement descriptions that
contain temporal aspects, which are crucial for transformation into LTL. The
importance of this step lies in its ability to filter out irrelevant or inapplicable
requirements, focusing only on those that can feasibly be transformed into formal
specifications. This process includes a detailed examination of the language used
in the requirements to determine the presence of temporal elements, ensuring
that only suitable requirements proceed to the next phase.
8       Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian

    First, collect a large number of software requirement documents, which should
include various types of requirement descriptions, temporal and non-temporal.
This data will serve to train an LLM to identify and differentiate between differ-
ent types of requirement descriptions. In the training data, mark the descriptions
that have temporal properties. This marking might involve identifying specific
temporal vocabulary (such as ‘after’, ‘before’, ‘during’, etc.) or statements with
time constraints. Subsequently, use these annotated data to train the LLM. Dur-
ing the training process, the model learns how to distinguish between temporal
and non-temporal requirement descriptions based on textual features (vocab-
ulary, grammatical structure, etc.). Finally, optimize and validate the model’s
performance through cross-validation and testing sets to ensure the model accu-
rately identifies requirements descriptions that contain temporal properties.
    By the way, our decision to convert natural language into Linear Temporal
Logic (LTL) stems from two main reasons. Firstly, several advanced formal ver-
ification tools rely on LTL specifications for verifying properties, making LTL a
suitable input for these tools. Secondly, LTL can be easily translated into other
temporal logic constraint languages like CTL [13,22] and PPTL [23] to provide
a more comprehensive depiction of software systems.

3.2   Step II: Natural Language Standardization and Refinement

Upon isolating the pertinent requirements, the next step is to standardize the
natural language used in these requirements. This standardization involves re-
structuring sentences for clarity, removing ambiguities, and ensuring consistency
in terminology. Additionally, this step involves refining abstract variable descrip-
tors into specific, code-level variable names. This refinement is critical for main-
taining consistency and ensuring that the translated requirements accurately
reflect the intended functionalities in the code.
    Taking the first requirement, Requirement A, from Table 2 as an exam-
ple: “Validate the data length for correctness: if the length is not 19, increment
cntLenRd and totalLenRd + 1, and return a validation failure.” This require-
ment describes a function that IP Fag333saCheck should possess, merging nat-
ural language with mathematical formulas. The term ’length’ here abstracts a
concept from the code level. We categorize such descriptions as implicit require-
ment descriptions, which are expressions that are not standardized. Translating
them directly into an LTL expression might conceal critical information at the
code level and disrupt the subsequent consistency validation. Hence, we have
developed a specific prompt engineering approach for the LLM, as illustrated in
Fig. 4, to transform implicit requirement descriptions into explicit ones. More
precisely, program variables mentioned in the requirements should utilize data
interfaces as defined in the knowledge model. The contents of Table 1 should be
used as a query dictionary to match program variables to their corresponding
‘Data Name’ in the ‘Explanation’ column. The blending of natural language with
mathematical formulas should be avoided. Also, function return values should
be denoted by TRUE and FALSE for success and failure, respectively. Following
this procedure, we obtain the explicit requirement description for Requirement
                                          Title Suppressed Due to Excessive Length                  9

      Prompt

      Prompt file: Transforming non-standard natural language software requirements into stan-
      dardized natural language descriptions that align with the style of Linear Temporal Logic
      (LTL) formulas.
      Objective: To convert non-standard, vague, or ambiguous software requirements into more
      coherent, precise, and standardized representations that adhere to the principles of Linear
      Temporal Logic (LTL).
      Method:
      1. Understanding Original Requirements: initially comprehend the given non-standard nat-
         ural language descriptions of software requirements.
      2. Identifying Key Elements: Extract key actions, objects, conditions, etc.
      3. Altering Mixed Expression Styles: When encountering natural language mixed with
         mathematical formulas, rewrite the mathematical formulas in a natural language style.
      4. Standardizing Language Representations: Reconstruct the original requirements using
         clear and direct language to express these elements.
      5. Applying Temporal Logic Vocabulary: Use LTL concepts like ”always”, ”until”, ”even-
         tually”, etc., to make the representations more aligned with the LTL style.
      6. Precisely Describe Variables involved in requirements: Consult the knowledge model
         tables to transform abstract descriptions into more concrete ones.
      7. Providing Conversion Examples: For each requirement, offer examples comparing before
         and after the transformation.
      8. Explaining Conversion Rationale: Briefly explain why such transformations make the
         requirements more aligned with the style of LTL formulas.
      Example:
      – Original Requirement: ”When a user clicks a button, the system should display data,
        but only if the network connection is normal.
      – Standardized Requirement: ”The system always displays data when the user clicks a
        button and the network connection is normal.
      – Explanation: The original requirement uses conditional and temporal language; the trans-
        formed requirement more explicitly employs ”always” and conditional conjunction, align-
        ing with the expression style of LTL.
      Conclusion: Ensure that all transformed requirements maintain the integrity and accuracy
      of the original intent while being more suited for LT-style logical analysis.


Fig. 4: Prompt: Conversion of Implicit Requirement Descriptions into Explicit Forms

A: “Validate the Correctness of Data Length: If the data length reLen is not
equal to 19, the values of the variables cntLenRd and totalLenRd will increase
by 1 each, and the return value will be FALSE.” Similarly, we applied the LLM
to rewrite the second requirement, Requirement B, from Table 2, resulting in:
“Validate Frame Count Update: If the frame count pbuff equals frm, then the
values of the variables cntUpdata and totalupdata will increase by 1 each, and
the return value will be FALSE.”

3.3      Step III: Translation into LTL Formulas

The final step in the process involves translating standardized and refined re-
quirements into LTL formulas. This translation requires a thorough understand-
ing of both natural language semantics and formal logic syntax. The goal is to
create precise and unambiguous LTL representations of the requirements that are
logically sound and true to the original natural language descriptions. This step is
vital as it connects informal requirement descriptions with formal specifications,
facilitating a more effective application of automated verification processes.
    In a similar manner, we construct a prompt engineering framework, utiliz-
ing LLMs to translate explicit requirements obtained from the second step into
10        Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian

     Prompt

     Prompt file: Translate the following natural language sentences into an LTL formula and
     explain your translation step by step. Remember that X means “next”, U means “until”,
     G means “globally”, F means “finally” or “will”. The formula should only contain atomic
     propositions or operators |, &, ∼, →, ↔, X, U , G, F .
     Natural Language: “When the database receives a query request, the system must return
     the result within 5 seconds.”
     Translation Process: “The database receives a query request” translates to the atomic
     proposition “d”. “The system must return the result within 5 seconds” translates to the
     atomic proposition “s”. “When...then” indicates a sequential relationship, which can be
     translated as a combination of “X” (next) and “U ” (until). Given the specific time con-
     straint (5 seconds), we use “U ” to represent this temporal relationship, but the specific
     time model needs to be defined in the model or context.
     LTL Formula: d → X(s U 5 seconds)
     Explanation: This means once the database receives a query request (d), the system must
     return the result (s) within the next 5 seconds.
     Natural Language: “If the server runs continuously for more than 24 hours, it needs to
     be automatically restarted.”
     Translation Process: “Server runs continuously for more than 24 hours” translates to the
     atomic proposition “sr”. “Needs to be automatically restarted” translates to the atomic
     proposition “ar”. “If...then” indicates a conditional relationship, corresponding to the log-
     ical implication “→”. Again, the specific time constraint (24 hours) needs to be defined in
     the model or context.
     LTL Formula: G(sr → X(ar))
     Explanation: This means if the server runs continuously for more than 24 hours (sr), then
     in the next state (X), it needs to be automatically restarted (ar).


       Fig. 5: Prompt: Translate Explicit Requirements into LTL Formulas

LTL formulas. Fig. 5 illustrates our specific approach. The process begins with
the identification of atomic propositions, translating each significant element
or condition in natural language sentences into atomic propositions. An atomic
proposition is a basic, indivisible statement in LTL. Subsequently, the translation
involves mapping tenses and logical structures from the natural language to cor-
responding LTL operators, including specific temporal constraints mentioned in
the natural language. Ultimately, the LTL formula is constructed by combining
atomic propositions with LTL operators, ensuring a rigorous and academically
sound translation from natural language to formal logic representation. Taking
the first requirement ‘Validate the Correctness of Data Length’ as the translation
subject, the resultant LTL formula is:
                    G(reLen! = 19 → F (cntLenRd′ = cntLenRd + 1
                                     && totalLenRd′ = totalLenRd + 1                                 (4)
                                                      && reVal = FALSE))

4     Verification of the Implementation
Tools used. Software formal verification tools can be helpful in proving the
memory safety and correctness of programs. CBMC [24] is a Bound Model
Checker tool used for analyzing programs written in the ANSI-C language. The
bounded model checking technique is a type of software model checking that
makes symbolic execution based on SAT procedures. The bounded model check-
ing examines counterexamples of a specific length and generates a propositional
formula that is satisfiable if and only if such a counterexample exists [25].
                                   Title Suppressed Due to Excessive Length       11

    CPAChecker [26,27] is a versatile framework that enables users to tailor pro-
gram analysis to their specific requirements. It allows for the customization of
verification methods and configurations based on the code’s structural aspects,
including loops, recursion, and properties like memory safety and reachability.
Verification inputs are created by combining the code and specifications, which
are then used to construct program and property models, along with algorithm
instances. By utilizing composite CPA analysis methods, CPAChecker explores
the reachable space and generates detailed verification reports.
    TRACE, our independently developed dynamic verification tool, employs a
trace-based runtime verification technique to analyze system behavior by exam-
ining its execution traces [28,29]. The tool utilizes the symbol execution tool
KLEE [30,31] to generate test cases covering various code branches and dynam-
ically executes the code, while using the debugging tool GDB to obtain actual
execution traces. An execution trace is a sequence of events or states representing
the system’s activity over time. These traces are compared against a specification
of desired or undesired properties, which can be expressed using formalisms like
temporal logics and automata. Trace-based verification differs from traditional
formal verification techniques such as model checking or theorem proving as it
focuses on a subset of possible behaviors and interacts directly with the actual
system rather than a formal model. While this approach enhances the scalability
and practicality of trace-based verification, it sacrifices exhaustiveness and rigor.
    Verification Process. Our verification process for a Software IP component
includes the following three steps:
1. Identifying properties to be verified from the requirements;
2. Generating a verification harness that can be compiled, the implementation
   of the IP component is called within a main function, and the source code of
   the harness is annotated using the specification language;
3. Executing various verification tools to verify safety properties and functional
   correctness properties derived from the requirements.

4.1   Step I: Identifying Properties to be Verified
The activity of selecting properties for verification lacks a well-established sys-
tematic approach. However, two primary categories of properties can be sub-
ject to verification: safety and functional correctness, which are expressed
through preconditions and postconditions or temporal logic formulas.
    Safety properties encompass areas such as memory safety, integer safety, and
numeric overflow. By proactively ensuring that these issues do not occur during
program execution, we can ensure the safety and reliability of software systems.
To verify these safety properties, assertions can be automatically inserted into
the program using tools like CBMC, CPAChecker, and KLEE. Table 3 showcases
the safety properties supported by different tools, allowing for the application of
bounded model checking, static analysis, and symbol execution.
    The derivation of functional correctness properties from software require-
ments, as elaborated in Section 3, involves the application of Hoare Logic nota-
tion, as introduced by Hoare [32]. This notation necessitates the identification
12        Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian
      Table 3: Safety properties that Different Tools can Automatically Verify
                  Safety Property           CBMC      CPAChecker       KLEE
       Out of Bounds Array Access             ✔           ✘             ✔
       Invalid Pointer Dereference            ✔           ✔             ✔
       Division by Zero                       ✔           ✘             ✔
       Integer Overflow                       ✔           ✔             ✘
       Pointer Arithmetic Overflow            ✔           ✘             ✘
       Floating Point Arithmetic Overflow     ✔           ✘             ✘
       Shift Operation Overflow               ✔           ✘             ✔
       Memory Leak                            ✔           ✘             ✔
       Termination                            ✘           ✔             ✘
       Data Race                              ✘           ✔             ✘
       Dead Lock                              ✘           ✔             ✘

of preconditions and postconditions for each function to express behavior prop-
erties accurately. Temporal logic is employed to articulate temporal properties
requiring verification, where one property must be satisfied before verifying an-
other. For example, the initial requirement can be represented using an LTL
formula, as demonstrated in Formula 4.

4.2     Step II: Generating Verification Harnesses
Unlike most program analysis and verification approaches, software IP is an
independent component that requires calling and execution, similar to an API.
Therefore, a verification harness (also known as a test harness) [33,34,35] is
necessary to drive the verification process.
    The verification harness includes the translation of target functional correct-
ness properties into a specific notation that can be executed by each tool. The
concept of contracts is employed, During the process of translating properties to
annotations. The syntax of the annotation depends on the tool being used. In
our verification harness, we utilize a ASSUME and ASSERT notation. The use
of these annotations simplifies the process, as the assume and assert clauses are
commonly employed in verification tools for setting pre/post-conditions. There-
fore, it allows us to easily adapt this harness to three different verification tools
using macro conversions, as shown at the top of Listing 1.2 (Lines 1-15). For
instance, CBMC utilizes Cprover annotations to define the properties that a
program should satisfy. Cprover annotations consist of keywords and pragmas
that are added as comments in the source code. An example of an annotation
is CPROVER assert(condition, message), which verifies whether a condition
holds at a specific program point. Our ASSERT macro can be converted to the
Cprover annotation, as shown in Line 3 of Listing 1.2. Similarly, when using
KLEE to generate test input for the runtime verification tool TRACE, there
is a need to simplify the most commonly used intrinsic, klee make symbolic,
which creates an unconstrained symbolic object. This principle of macro usage
also applies to KLEE and CPAChecker.
    Listing 1.2 provides an example of a verification harness that targets the
verification of the first requirement mentioned in Table 2 of Section 2. This ver-
ification harness is partly generated based on templates and follows a standard
structure. Firstly, it declares and initializes the necessary variables that the IP
component uses (Lines 18-27), which are similar to the variables that need to be
                                       Title Suppressed Due to Excessive Length   13
 1 #ifdef __CBMC__
 2 #define __ASSUME(condition) __CPROVER_assume(condition)
 3 #define __ASSERT(condition) __CPROVER_assert(condition, "")
 4 #elif __CPACHECKER__
 5 #define __ASSUME(condition) __VERIFIER_assume(condition)
 6 #define __ASSERT(condition) __VERIFIER_assert(condition)
 7 #elif __KLEE__
 8 #define __ASSUME(condition) klee_assume(condition)
 9 #define __ASSERT(condition) assert(condition)
10
11 void __MAKE_SYMBOLIC(void *addr, size_t nbytes, const char *name){
12 #ifdef __KLEE__
13     klee_make_symbolic(addr, nbytes, name);
14 #endif
15 }
16
17 void main() {
18     // Initialize variables
19     Fg333saCheck pIp;
20     __MAKE_SYMBOLIC(&pIp, sizeof(Fg333saCheck), "pIp");
21
22     unint08 buffer[19];
23     __MAKE_SYMBOLIC(buffer, sizeof(buffer), "buffer");
24     pIp.buffer = &buffer[0];
25
26     int32 cntLenRd_old = pIp.cntLenRd;
27     int32 totalLenRd_old = pIp.totalLenRd;
28
29     // Preconditions
30     __ASSUME(pIp.rdLen != 19);
31
32     // Call the IP interface to be verified
33     Fg333saCheckFun(&pIp);
34
35     // Postconditions
36     __ASSERT(pIp.bComSuc == FALSE);
37     __ASSERT(pIp.cntLenRd == cntLenRd_old + 1);
38     __ASSERT(pIp.totalLenRd == totalLenRd_old + 1);
39 }


       Listing 1.2: A Verification Harness to Verify the First Requirement
made symbolic in KLEE. Then, it includes the preconditions for the target prop-
erties (Line 30). Next, it calls the IP component to be verified (Line 33), similar
to using the API interface. Lastly, the expected postconditions are specified.
    When an IP component involves multiple properties for verification, they
can be integrated within the same verification harness if they share the same
preconditions. However, if the properties have distinct preconditions, a new ver-
ification harness is necessary for each unique precondition. Subsequently, it is
crucial to examine the union of the preconditions from all verification harnesses
to ensure comprehensive coverage of all possible preconditions. For safety prop-
erties, a verification harness without preconditions and postconditions suffices.
To verify safety properties, we have developed a tool that automatically gen-
erates such verification harnesses using lightweight static analysis and pattern
matching. Although our properties mining process contributes partially to fill-
ing in the preconditions and postconditions, we still need to manually input
the functional correctness properties into the verification harnesses, due to the
significant engineering effort involved in our underlying implementation.

4.3    Step III: Executing three Verification Tools

Once all verification harnesses have been prepared, we initially execute the ver-
ification harness without any preconditions or postconditions to verify safety
properties. Table 4 presents a detailed description of the results obtained from
14        Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian
               Table 4: Verification results of 5 IPs in Safety Properties
                           LoC
IP Name                                   Code Feature               CBMC       CPAChecker KLEE
                    (Source+Harness)
Fg333saCheck             140+35         pointer, array, loop        ✘ (IO)            ✔            ✔
Fg333saUnpack             77+35         floating point arithmetic ✘ (IO, FPO)      ✘ (FPO)         ✔
PowerOnJudge              85+33         pointer                        ✔              ✔            ✔
GyroChooseFun             50+58         pointer, array, loop           ✔              ✔            ✔
AttiCal                   68+44         pointer, array                 ✔              ✔            ✔
     ✔ indicates that the tool successfully verifies all the supported safety properties, as outlined in
     Table 3. While ✘ indicates the tool reports that some safety properties cannot be satisfied. ”IO”
     refers to integer overflow, and ”FPO” stands for floating point arithmetic overflow.

     Table 5: Verification results of 5 IPs in Functional Correctness Properties
                             Pre/post-conditions                 Temporal logic properties
     IP Name                    (Proved/All)                          (Proved/All)
                             CBMC           CPAChecker                   TRACE+KLEE
     Fg333saCheck             5/5                3/5                            8/8
     Fg333saUnpack            1/7                1/7                            0/1
     PowerOnJudge             6/6                6/6                            9/9
     GyroChooseFun            4/7                4/7                            0/1
     AttiCal                  4/5                4/5                            0/1
         All                 20/30              18/30                          17/20

proving safety properties in five software IPs, utilizing CBMC, CPAChecker, and
KLEE. These five software IPs each have a verification harness but do not include
any pre/post-conditions. Each IP consists of approximately one hundred lines of
code, which encompasses arrays, pointers, floating-point operations, etc. Three
IPs have been successfully proven to be safe using all three techniques. Only some
cases of integer overflow and floating-point arithmetic overflow have been found
in Fg333saUnpack and Fg333saCheck. It is worth noting that both CBMC and
CPAChecker reported the floating point arithmetic overflow, while only CBMC
reported the integer overflow. However, KLEE did not identify these two issues.
After conducting a manual analysis, we discovered that these two issues were
indeed potential defects that occurred only under specific preconditions. This
highlights the importance of using multiple tools to verify safety properties.
    Table 5 presents the verification results for five IPs. It shows the number of
functional properties that were examined and the corresponding number of prop-
erties that were successfully verified by each tool (indicated as Proved/All). The
properties consist of 20 temporal logic properties identified through LLM-based
automatic mining and 30 manually added pre/post-conditions. Of the 20 tem-
poral logic properties, TRACE+KLEE successfully verified 17. Similarly, out
of the 30 pre/post-condition pairs, only 20 were successfully verified. Manual
analysis revealed that unsuccessful verifications were influenced by factors like
multiple loop structures, floating point arithmetic, and quantifiers. This under-
scores the need for enhancements in both verification capability and scalability
in the context of industrial scenarios.

5      Discussion
Our work has several implications for the field of security-critical IP-based soft-
ware development, particularly in the domain of aerospace embedded systems.
                                  Title Suppressed Due to Excessive Length      15

First, our work shows that Large Language Models can be used to automate
the requirement analysis process, reducing the time and effort required to con-
vert natural language descriptions into formal logic expressions. Second, our
work demonstrates that verification harnesses can be automatically generated
for each IP component, simplifying the verification process and ensuring con-
sistency and completeness. Third, our work reveals that different verification
techniques can be applied to the same IP component, providing complementary
perspectives and insights on the correctness and robustness of the component.
Our work also provides a novel and comprehensive solution that seamlessly in-
tegrates requirement analysis and verification. Note that our work differs from
other related studies in several aspects. For instance, unlike other work that used
predefined templates or rules to convert natural language into formal logic, our
work leverages Large Language Models to perform this task in an interactive
and flexible way. Furthermore, unlike some work that relied on a single verifica-
tion technique, our work employs three different verification techniques, namely
model checking, static analysis, and symbolic execution, to verify the same IP
component, enhancing the confidence and reliability of the verification results.
    However, our work also has some limitations and challenges that need to be
considered and addressed in future research. One limitation is that our work de-
pends on the quality and availability of the natural language descriptions of the
IP components, which may not always be clear, complete, or consistent. There-
fore, future work could explore ways to improve the natural language processing
and understanding capabilities of the Large Language Models, or to incorporate
other sources of information, such as diagrams, specifications, or documentation,
to enhance the requirement analysis process. Another challenge is that our work
requires a large amount of computational resources and time to perform the
verification process, especially for large and complex IP components. Therefore,
future work could investigate methods to optimize the verification process, such
as parallelization, abstraction, or approximation, to reduce the computational
cost and time. A third challenge is that our work does not consider the inter-
actions and dependencies among different IP components, which may affect the
overall functionality and performance of the system.

6   Related Work
Property Mining. How to acquire better-automated tool support for efficiently
transforming natural language documents into formalized formulas has emerged
as a hot research topic in the field of formalization in recent years. Andrew
et al. from Princeton University proposed the automated software verification
toolchain VST [36,37], which aims to achieve this objective. It requires users to
manually specify properties for verification. The process involves defining pre-
conditions, postconditions, and loop invariants to facilitate automated program
verification with the aid of VST. In the formalization projects of garbage collec-
tion and the Verve [38] system conducted at Microsoft, a plethora of tools were
employed to support the automated verification of properties. This included
type-preserving compilers and automatic theorem provers, significantly enhanc-
16     Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian

ing the efficiency of property verification tasks. Beyer and colleagues from Freie
Universität Berlin introduced an automatic verification tool based on abstract
interpretation, CPAchecker [26,27], which necessitates manual insertion of asser-
tions and error labels to represent properties for verification. The correctness of
software programs is demonstrated through the reachability analysis of target
states. In our research, we have developed a prompting engineering framework
that leverages LLMs to translate natural language into LTL formulas. To en-
hance the accuracy of the translation, we conducted extensive preprocessing of
the natural language inputs. This involved filtering out natural language state-
ments that embody temporal properties and converting non-standard natural
language descriptions into standardized ones.
Program Verification. Works that have utilized the CBMC, CPAChecker,
and runtime verification tools have reported successful applications in various
industries. For instance, the CBMC has recently demonstrated its effectiveness
in verifying memory safety in the boot code of AWS Data Centers [39] as well as
in Amazon Web Services [40]. In another study [41], the CBMC was employed
to detect previously undetected bugs in the driver software for flash memory.
The CBMC has also been used in conjunction with field testing [42]. These
findings collectively support the notion that the CBMC tool is developed suffi-
ciently for industrial usage. CPAChecker has been applied to Google App Engine
Cloud [43]. Notably, other works in the literature compare static analysis tools
using either CBMC or CPAChecker, although not specifically comparing the
CBMC and CPAChecker tools [44,45,46,47]. However, the main difficulties of
using CBMC and CPAChecker, as well as their potential complementary us-
age, are not well-established in the literature. Additionally, many existing works
propose different methods and tools for runtime verification [48,28,49,29]. In our
study, we employ our proprietary tool, Trace, for the verification of the temporal
logic properties in aerospace-embedded software IP. This decision stems from the
fact that CBMC and CPAChecker have proven to be ineffective in verifying the
temporal logic property in practical scenarios. We distinguish our work by show-
casing the integration of three widely utilized verification techniques. Through
this combination, we achieve the successful verification of safety properties and
functional correctness in industrial programs within the aerospace field.

7    Conclusions
In conclusion, we presented a case study on software IP components derived
from aerospace-embedded systems, and proposed a novel and comprehensive so-
lution for the practical requirement analysis and verification process. We employ
Large Language Models to translate natural language requirements into pro-
gram specifications and utilize three different verification techniques to verify
the corresponding implementation. We have successfully verified five real-world
IP components from CAST and demonstrated the feasibility and effectiveness
of our solution. As for future work, we are considering developing techniques to
verify the integration and combination of multiple IP components. We also plan
to conduct more experiments on more real-world IP components from CAST.
                                   Title Suppressed Due to Excessive Length         17

Acknowledgements

The authors would like to thank the anonymous reviewers for their constructive
comments. This work was supported in part by the National Natural Science
Foundation of China (Nos. 62372304, 62302375, 62192734), and the China Post-
doctoral Science Foundation funded project.


References

 1. Carsten Böke, Carsten Ditze, HJ Eickerling, Uwe Glässer, Bernd Kleinjohann,
    Franz Rammig, and Wolfgang Thronicke. Software ip in embedded systems. Virtual
    Components Design and Reuse, pages 47–64, 2001.
 2. Flavio R Wagner, Wander O Cesario, Luigi Carro, and Ahmed A Jerraya. Strate-
    gies for the integration of hardware and software ip components in embedded
    systems-on-chip. Integration, 37(4):223–252, 2004.
 3. SreeCharan Gundabolu and Xiaofang Wang. On-chip data security against un-
    trustworthy software and hardware ips in embedded systems. In 2018 IEEE Com-
    puter Society Annual Symposium on VLSI (ISVLSI), pages 644–649. IEEE, 2018.
 4. Júlio CB de Mattos, Lisane Brisolara, Renato Hentschke, Luigi Carro, and Flávio R
    Wagner. Design space exploration with automatic generation of ip-based embed-
    ded software. In IFIP Working Conference on Distributed and Parallel Embedded
    Systems, pages 237–246. Springer, 2004.
 5. Joachim Kunkel. Toward ip-based system-level soc design. Computer, 36(05):88–
    89, 2003.
 6. Raphael CS Machado, Davidson R. Boccardo, Vinı́cius G Pereira de Sá, and Jayme
    L. Szwarcfiter. Software control and intellectual property protection in cyber-
    physical systems. EURASIP Journal on Information Security, 2016:1–14, 2016.
 7. Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Car-
    oline Trippel. nl2spec: Interactively translating unstructured natural language to
    temporal logics with large language models. arXiv preprint arXiv:2303.04864,
    2023.
 8. Chuyue Sun, Christopher Hahn, and Caroline Trippel. Towards improving ver-
    ification productivity with circuit-aware translation of natural language to sys-
    temverilog assertions. In First International Workshop on Deep Learning-aided
    Verification, 2023.
 9. Juan Zhai, Yu Shi, Minxue Pan, Guian Zhou, Yongxiang Liu, Chunrong Fang,
    Shiqing Ma, Lin Tan, and Xiangyu Zhang. C2s: translating natural language com-
    ments to formal program specifications. In Proceedings of the 28th ACM Joint
    Meeting on European Software Engineering Conference and Symposium on the
    Foundations of Software Engineering, pages 25–37, 2020.
10. Ivica Crnkovic, Séverine Sentilles, Aneta Vulgarakis, and Michel RV Chaudron. A
    classification framework for software component models. IEEE Transactions on
    Software Engineering, 37(5):593–615, 2010.
11. Herve C Lefevre. The fiber-optic gyroscope. Artech house, 2022.
12. Andrea Brunello, Angelo Montanari, and Mark Reynolds. Synthesis of ltl formulas
    from natural language texts: State of the art and research directions. In 26th
    International symposium on temporal representation and reasoning (TIME 2019).
    Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik, 2019.
18      Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian

13. Madjid Maidi. The common fragment of ctl and ltl. In Proceedings 41st Annual
    Symposium on Foundations of Computer Science, pages 643–652. IEEE, 2000.
14. Vaughan R Pratt. Semantical considerations on floyd-hoare logic. In 17th Annual
    Symposium on Foundations of Computer Science (sfcs 1976), pages 109–121. IEEE,
    1976.
15. Mingsheng Ying. Floyd–hoare logic for quantum programs. ACM Transactions on
    Programming Languages and Systems (TOPLAS), 33(6):1–49, 2012.
16. Tianyu Wu, Shizhu He, Jingping Liu, Siqi Sun, Kang Liu, Qing-Long Han, and
    Yang Tang. A brief overview of chatgpt: The history, status quo and potential
    future development. IEEE/CAA Journal of Automatica Sinica, 10(5):1122–1136,
    2023.
17. Jan Kocoń, Igor Cichecki, Oliwier Kaszyca, Mateusz Kochanek, Dominika Szydlo,
    Joanna Baran, Julita Bielaniewicz, Marcin Gruza, Arkadiusz Janz, Kamil Kanclerz,
    et al. Chatgpt: Jack of all trades, master of none. Information Fusion, page 101861,
    2023.
18. Sudharsan Ravichandiran. Getting Started with Google BERT: Build and train
    state-of-the-art natural language processing models using BERT. Packt Publishing
    Ltd, 2021.
19. Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun
    Li, Shing-Chi Cheung, and Cong Tian. Enchanting program specification synthe-
    sis by large language models using static analysis and program verification. In
    International Conference on Computer Aided Verification. Springer, 2024.
20. Cheng Wen, Yuandao Cai, Bin Zhang, Jie Su, Zhiwu Xu, Dugang Liu, Shengchao
    Qin, Zhong Ming, and Cong Tian. Automatically inspecting thousands of static
    bug warnings with large language model: How far are we? ACM Transactions on
    Knowledge Discovery from Data, 2024.
21. Danning Xie, Byungwoo Yoo, Nan Jiang, Mijung Kim, Lin Tan, Xiangyu Zhang,
    and Judy S Lee. Impact of large language models on generating software specifi-
    cations. arXiv preprint arXiv:2306.03324, 2023.
22. Nan Zhang, Bin Yu, Cong Tian, Zhenhua Duan, and Xiaoshuai Yuan. Temporal
    logic specification mining of programs. Theoretical Computer Science, 857:29–42,
    2021.
23. Xinya Ning, Nan Zhang, Zhenhua Duan, and Cong Tian. Pptl specification mining
    based on lnfg. Theoretical Computer Science, 937:85–95, 2022.
24. Daniel Kroening and Michael Tautschnig. Cbmc–c bounded model checker: (com-
    petition contribution). In Tools and Algorithms for the Construction and Analysis
    of Systems: 20th International Conference, TACAS 2014, Held as Part of the Euro-
    pean Joint Conferences on Theory and Practice of Software, ETAPS 2014, Greno-
    ble, France, April 5-13, 2014. Proceedings 20, pages 389–391. Springer, 2014.
25. Armin Biere, Alessandro Cimatti, Edmund M Clarke, Masahiro Fujita, and Yun-
    shan Zhu. Symbolic model checking using sat procedures instead of bdds. In
    Proceedings of the 36th annual ACM/IEEE Design Automation Conference, pages
    317–320, 1999.
26. Dirk Beyer and M Erkan Keremoglu. Cpachecker: A tool for configurable soft-
    ware verification. In Computer Aided Verification: 23rd International Conference,
    CAV 2011, Snowbird, UT, USA, July 14-20, 2011. Proceedings 23, pages 184–190.
    Springer, 2011.
27. Stefan Löwe, Mikhail Mandrykin, and Philipp Wendler. Cpachecker with sequen-
    tial combination of explicit-value analyses and predicate analyses: (competition
    contribution). In Tools and Algorithms for the Construction and Analysis of Sys-
    tems: 20th International Conference, TACAS 2014, Held as Part of the European
                                   Title Suppressed Due to Excessive Length        19

    Joint Conferences on Theory and Practice of Software, ETAPS 2014, Grenoble,
    France, April 5-13, 2014. Proceedings 20, pages 392–394. Springer, 2014.
28. Giles Reger and Klaus Havelund. What is a trace? a runtime verification perspec-
    tive. In International Symposium on Leveraging Applications of Formal Methods,
    pages 339–355. Springer, 2016.
29. Richard Bubel, Dilian Gurov, Reiner Hähnle, and Marco Scaletta. Trace-based
    deductive verification. In Proceedings of 24th International Conference on Logic,
    volume 94, pages 73–95, 2023.
30. Cristian Cadar, Daniel Dunbar, Dawson R Engler, et al. Klee: Unassisted and
    automatic generation of high-coverage tests for complex systems programs. In
    OSDI, volume 8, pages 209–224, 2008.
31. Cristian Cadar and Martin Nowack. Klee symbolic execution engine in 2019. In-
    ternational Journal on Software Tools for Technology Transfer, 23:867–870, 2021.
32. Charles Antony Richard Hoare. An axiomatic basis for computer programming.
    Communications of the ACM, 12(10):576–580, 1969.
33. Jiong Gong, Yun Wang, Haihao Shen, Xu Deng, Wei Wang, and Xiangning Ma.
    Fast: Formal specification driven test harness generation. In Tenth ACM/IEEE
    International Conference on Formal Methods and Models for Codesign (MEM-
    CODE2012), pages 33–42. IEEE, 2012.
34. Camila Ribeiro Rocha and Eliane Martins. A method for model based test harness
    generation for component testing. Journal of the Brazilian Computer Society,
    14:7–23, 2008.
35. Dirk Beyer and Thomas Lemberger. Software verification: Testing vs. model check-
    ing: A comparative evaluation of the state of the art. In Hardware and Software:
    Verification and Testing: 13th International Haifa Verification Conference, HVC
    2017, Haifa, Israel, November 13-15, 2017, Proceedings 13, pages 99–114. Springer,
    2017.
36. Qinxiang Cao, Lennart Beringer, Samuel Gruetter, Josiah Dodds, and A. Appel.
    Vst-floyd: A separation logic tool to verify correctness of c programs. Journal of
    Automated Reasoning, pages 367–422, 2018.
37. S. Lin, Pan Du, W. Huber, and W. Kibbe. Model-based variance-stabilizing trans-
    formation for illumina microarray data. Nucleic Acids Research, 36:e11–e11, 2008.
38. Jean Yang and Chris Hawblitzel. Safe to the last instruction: automated verifica-
    tion of a type-safe operating system. Communications of the ACM, 54:123–131,
    2011.
39. Byron Cook, Kareem Khazem, Daniel Kroening, Serdar Tasiran, Michael
    Tautschnig, and Mark R Tuttle. Model checking boot code from aws data centers.
    In Computer Aided Verification: 30th International Conference, CAV 2018, Held
    as Part of the Federated Logic Conference, FloC 2018, Oxford, UK, July 14-17,
    2018, Proceedings, Part II 30, pages 467–486. Springer, 2018.
40. Nathan Chong, Byron Cook, Jonathan Eidelman, Konstantinos Kallas, Kareem
    Khazem, Felipe R Monteiro, Daniel Schwartz-Narbonne, Serdar Tasiran, Michael
    Tautschnig, and Mark R Tuttle. Code-level model checking in the software de-
    velopment workflow at amazon web services. Software: Practice and Experience,
    51(4):772–797, 2021.
41. Moonzoo Kim, Yunho Kim, and Hotae Kim. Unit testing of flash memory device
    driver through a sat-based model checker. In 2008 23rd IEEE/ACM International
    Conference on Automated Software Engineering, pages 198–207. IEEE, 2008.
42. Hendrik Post, Carsten Sinz, Florian Merz, Thomas Gorges, and Thomas Kropf.
    Linking functional requirements and software verification. In 2009 17th IEEE
    International Requirements Engineering Conference, pages 295–302. IEEE, 2009.
20      Zhi Ma, Cheng Wen, Jie Su, Ming Zhao, Bin Yu, Xu Lu, and Cong Tian

43. Dirk Beyer, Georg Dresler, and Philipp Wendler. Software verification in the google
    app-engine cloud. In Computer Aided Verification: 26th International Conference,
    CAV 2014, Held as Part of the Vienna Summer of Logic, VSL 2014, Vienna,
    Austria, July 18-22, 2014. Proceedings 26, pages 327–333. Springer, 2014.
44. Dirk Beyer. Status report on software verification: (competition summary sv-comp
    2014). In Tools and Algorithms for the Construction and Analysis of Systems:
    20th International Conference, TACAS 2014, Held as Part of the European Joint
    Conferences on Theory and Practice of Software, ETAPS 2014, Grenoble, France,
    April 5-13, 2014. Proceedings 20, pages 373–388. Springer, 2014.
45. Herbert Rocha, Raimundo Barreto, Lucas Cordeiro, and Arilo Dias Neto. Un-
    derstanding programming bugs in ansi-c software using bounded model checking
    counter-examples. In Integrated Formal Methods: 9th International Conference,
    IFM 2012, Pisa, Italy, June 18-21, 2012. Proceedings 9, pages 128–142. Springer,
    2012.
46. Hélene Collavizza, Michel Rueher, and Pascal Van Hentenryck. Comparison be-
    tween cpbpv, esc/java, cbmc, blast, eureka and why for bounded program verifica-
    tion. arXiv preprint arXiv:0808.1508, 2008.
47. Guang Chen, Dexi Wang, Tianchi Li, Chao Zhang, Ming Gu, and Jiaguang Sun.
    Scalable verification framework for c program. In 2018 25th Asia-Pacific Software
    Engineering Conference (APSEC), pages 129–138. IEEE, 2018.
48. Moran Omer and Doron Peled. Runtime verification prediction for traces with data.
    In International Conference on Runtime Verification, pages 148–167. Springer,
    2023.
49. Lukas Convent, Sebastian Hungerecker, Torben Scheffel, Malte Schmitz, Daniel
    Thoma, and Alexander Weiss. Hardware-based runtime verification with embedded
    tracing units and stream processing. In International Conference on Runtime
    Verification, pages 43–63. Springer, 2018.
