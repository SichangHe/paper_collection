                                         Working Document - Formalising Software Requirements with Large Language
                                         Models
                                         ARSHAD BEG∗∗ , DIARMUID O’DONOGHUE∗ , and ROSEMARY MONAHAN∗ , Maynooth University,
                                         Ireland

                                         This draft is a working document, having a summary of nighty-four (94) papers with additional sections on Traceability of Software
                                         Requirements (Section 4), Formal Methods (Section 5), Unifying Theories of Programming (UTP) and Theory of Institutions (Section
                                         6). Please refer to abstract of [7, 8]. Key difference of this draft from our recently anticipated ones with similar titles, i.e. AACS 2025
                                         [7] and SAIV 2025 [8] is:
                                             [7] is a two page submission to ADAPT Annual Conference, Ireland. Submitted on 18th of March, 2025, it went through the
arXiv:2506.14627v2 [cs.SE] 23 Jun 2025




                                         light-weight blind review and accepted for poster presentation. Conference was held on 15th of May, 2025.
                                             [8] is a nine page paper with additional nine pages of references and summary tables, submitted to Symposium on AI Verification
                                         (SAIV 2025) on 24th of April, 2025. It went through rigorous review process. The uploaded version on arXiv.org [8] is the improved
                                         one of the submission, after addressing the specific suggestions to improve the paper.

                                         CCS Concepts: • Computing methodologies → Artificial intelligence; Natural language processing; Large language models;
                                         Knowledge representation and reasoning; Formal languages; Logic; • Software and its engineering → Software creation
                                         and management; Software requirements engineering; Software requirements specifications; Formal software verification;
                                         Formal verification; Theorem proving; Model-checking.

                                         Additional Key Words and Phrases: Chain-of-Thought (CoT), Prompt-Engineering, {Zero, One, and Few}-shot prompting


                                         1    INTRODUCTION
                                         Relying on natural language in software requirements often leads to ambiguity. In addition, requirements which are not
                                         expressed in a formal mathematical notation cannot be guaranteed through formal verification techniques as required
                                         to meet standards e.g. [9, 11, 70] in safety critical software. Expressing requirements in formal notation requires training
                                         in the domain of requirements engineering, as well as knowledge of formal notation and associated proof methods,
                                         often increasing the software development cycle time by a factor of 30% [44]. In this project, we aim to ease the burden
                                         of writing specification, helping to bridge the gap between the need for formal verification techniques and their lack of
                                         use in the software industry (due to the fast pace of the industry environment).
                                             Formalising software requirements ensures clarity, correctness and verifiability, and requires formal specification
                                         languages, logic and verification techniques, such as theorem proving and model-checking, to guarantee the correctness
                                         of the software system under construction. Like all other fields, the development of Large Language Models (LLMs) has
                                         opened a world of opportunities where we can exploit their power to generate formal requirements and accompanying
                                         specifications.
                                             In this paper, we present the results of our structured literature review which examines how large language models
                                         are currently used to assist in writing formal specifications. Main research questions for conducting systematic literature
                                         review on the topic are as follows:
                                         RQ1: What methodologies leverage Large Language Models (LLMs) to transform natural language software require-
                                         ments into formal notations?
                                         ∗ All authors contributed equally to this research.


                                         Authors’ address: Arshad Beg, arshad.beg@mu.ie; Diarmuid O’Donoghue, diarmuid.odonoghue@mu.ie; Rosemary Monahan, rosemary.monahan@mu.ie,
                                         Maynooth University, Maynooth, Ireland.
                                                                                                                                                                                  1
2                                                           Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


RQ2: What are the emerging trends and future research directions in using LLMs for software requirements formalisa-
tion?
    The structure of the paper is organized as follows. Section 2 presents the methodology used to select the relevant
literature. Section 3 provides a brief overview of works focused on the formalisation of software requirements using
large language models (LLMs) addressing RQ1. Literature concerning the traceability of software requirements is
discussed in Section 4. Section 5 lists down well-known formal notations developed over the last three decades of
research by the formal method community and its related tools. Section 6 explores studies involving formal proofs
within the frameworks of Unifying Theories of Programming (UTP) and the Theory of Institutions. Section 7 presents
future directions based on our findings and the discussion on chain of thought and prompt engineering in sub-section
7.1, addressing RQ2. Concluding remarks are provided in Section 8.


2    METHODOLOGY FOR LITERATURE REVIEW
To conduct a structured and thorough review of literature on Natural Language Processing (NLP), Large Language
Models (LLMs), and their use in software requirements, the following approach is followed. Several academic databases,
including IEEE Xplore, ACM Digital Library, Scopus, Springer Link, and Google Scholar, are searched using specific
keywords. The core search terms include “NLP,” “LLMs,” and “Software Requirements,” with broader terms such as
“specification,” “logic,” “verification,” “model checking,” and “theorem proving” used to expand the scope. The number of
results differs notably across databases. For example, IEEE Xplore returns 17 peer-reviewed articles, Scopus lists 20,
Springer Link filters to 595, ACM Digital Library provides 1,368 results, and Google Scholar shows 14,800 references
since 2021. These discrepancies highlight the importance of applying precise selection methods to extract the most
relevant studies.
    To streamline the process of locating strong contributions, the AI-powered tool Elicit [20] is used. Elicit supports the
literature review by offering summarised content and DOIs for suggested papers. While it helps reduce the manual
workload during the initial phase, every suggested paper in this review is manually reviewed to ensure its relevance.
This ensures that the final list excludes any unrelated or off-topic material. After the initial filtering, a manual review is
performed to confirm the relevance and quality of each paper. Abstracts are first assessed to judge suitability. If the
abstract lacks clarity or depth, a further examination of the full text is conducted.
    Abstracts are closely read, and when necessary, the full text is reviewed using the following exclusion and inclusion
criteria:
    Inclusion Criteria: Studies are included if they offer meaningful theoretical or empirical insights related to NLP,
LLMs, and their application in software requirements. This includes topics like specification, formal logic, verification,
and formal methods.
    Exclusion Criteria: Papers are excluded if they show in-sufficient relevance to the intersection of NLP/LLMs and
software requirements, or if their abstracts or full texts lack sufficient detail. Non-peer-reviewed materials, duplicates,
and items suggested by Elicit but deemed irrelevant after manual review are also removed.


3    FORMALISING REQUIREMENTS THROUGH LLMS
The paper [18] proposes using LLMs, like GPT-3.5, to verify code by analysing requirements and explaining whether
they are met. The work [17] details about nl2spec, a framework that leverages LLMs to generate formal specifications
from natural language, addressing the challenge of ambiguity in system requirements. Users can iteratively refine
Working Document - Formalising Software Requirements with Large Language Models                                         3


translations, making formalization easier. The work [17] provides an open-source implementation with a web-based
interface.
  The work [73] provides verification and refinement of natural language explanations by making LLMs and theorem
provers work together. A neuro-symbolic framework i.e. Explanation-Refiner is represented. LLMs and theorem provers
are integrated together to formalise explanatory sentences. The theorem prover then provides the guarantee of validated
sentence explanations. Theorem prover also provides feedback for further improvements in NLI (Natural Language
Inference) model. Error correction mechanisms can also be deployed by using the tool Explanation-Refiner. Consequently,
it automatically enhances the quality of explanations of variable complexity. [4] outlines key research directions for the
stages of software requirement engineering, conducts a SWOT analysis, and share findings from an initial evaluation.
  In [50], symbolic NLP and ChatGPT performance is compared while generating correct JML output against given
natural language pre-conditions. In [5], domain models are generated against natural language requirements for
industry-based case study. Domain model extractor is designed and applied to four industrial requirements documents.
The accuracy and overall performance is reported for the designed model extractor. An automatic synthesis of software
specifications is provided through LLMs in [59]. We know that software configurations give an insight of how the
software will behave. While software are frequently discussed and documented in a variety of external sources, including
software manuals, code comments, and online discussion forums, making it hard for system administrators to get the
most optimal configurations due to lack of clarity and organisation in provided documentation. Work [59] proposed
SpecSyn framework that uses an advanced language model to automatically generate software specifications from
natural language text. It treats specification generation as a sequence-to-sequence learning task and outperforms
previous tools by 21% in accuracy, extracting specifications from both single and multiple sentences.
  AssertLLM tool is presented in [23]. The tool generates assertions to do hardware verification from design spec-
ifications, exploiting three customised LLMs. It is done in three phases, first understanding specifications, mapping
signal definitions and generating assertions. The results show that AssertLLM produced 89% correct assertions with
accurate syntax and function. The work [30] reports on formal verification of NASA’s Node Control Software natural
language specifications. The software is deployed at International Space Station. Errors found in the natural language
requirements are reported by the authors with a commentary on lessons learnt.
  SpecLLM [54] explores the space of generating and reviewing VLSI design specifications with LLMs. The cumbersome
task of chip architects can be improved by exploiting the power of LLMs for synthesising natural language specifications
involved in chip designing. So, the utility of LLMs is explored with the two stages i.e. (1) generation of architecture
specifications from scratch and from register transfer logic (RTL) code; and (2) reviewing these generated specifications.
  The paper [68] introduced a model-based language (Requirements Specification Language - RSL) that enhances
software requirements specification by incorporating constrained natural language phrases, including verbs, adjectives,
and prepositions, grouped by nouns. It also presented an advanced tooling framework that captures application logic
specifications, enabling automated transformations into code, validated through a controlled experiment. The framework
functionality is integrated as development platform named ReDSeeDS. The work was a part of EU project, maintained
at www.redseeds.eu [68]. A similar work is reported in [31] which describes the details of ARSENAL framework and
methodology designed to perform automatic requirements specification extraction from natural language. The generated
specification can be verified automatically through the framework.
  An interesting work is presented in [51]. Business process models specifes the requirements of process-aware
information systems. It includes generation of natural language from business process models. Domain experts and
system analysts find it difficult to validate BPMs directly. The automation of generating a text which describes these
4                                                          Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


models is done in [51]. For the translation process, BPMs are translated to RPST - a tree like structure of the process model
which is then used to generate sentences first. These generated sentences are refined by adding linguistic complexity
later-on. The generated natural language is found complete and more understandable. In primitive work of 1996 [69], the
software requirements were expressed in a limited set of natural language. Authors [69] referred it as controlled natural
language. For Controlled Language (CL) , authors used the Alvey Natural Language Toolkit (ANLT). This intermediate
notation is then translated to logical expressions in order to detect and remove ambiguities in requirement specifications.
In [74], the potential and power of LLMs is exploited for smart grid requirement specifications improvement. Here, the
performance of GPT-4o and Claude 3.5 Sonnet is analysed through f1-scores, achieving in range of 79% - 94%.
    The paper [91] reports the translation between NL and Linear Temporal Logic (LTL) formulas through the use of
LLMs. The challange of low accuracy and high cost during model training and tuning of general purpose LLMs is
considered in [91]. Dynamic prompt generation and human interaction with LLMs are amalgamated to deal with the
mentioned challenges. Unstructured natural language requirements are converted to NL-LTL pairs. The approach
achieved up to 94.4% accuracy on publicly available datasets with 36 and 255,000 NL-LTL pairs. Dealing with a different
domain domain, it improved from 27% to 78% through interactive prompt evolution.
    In [81], authors present ESBMC-AI, a framework that combined Large Language Models (LLMs) with Formal
Verification to automatically detect and fix software vulnerabilities. The approach used Bounded Model Checking
(BMC) to identify errors and generate counterexamples, which were then fed into LLM to repair the code, followed
by re-verification with BMC. Evaluated on 50,000 C programs from the FormAI dataset, ESBMC-AI effectively fixed
issues like buffer overflows and pointer dereference failures with high accuracy, making it a valuable tool for software
development and CI/CD integration. In [38], authors reported performance of LLMs to translate natural language
into formal rules by training them on datasets for regular expressions (regex), first-order logic (FOL), and linear-time
temporal logic (LTL) . The results show that the models adapt well to new terms and symbols, and outperformed
existing methods in regular expression translation.
    In [62], SynVer is presented. SynVer is a framework to synthesise and verify C programs. Built on the Verified Software
Toolchain, the tool usage was applied on benchmarks containing basic coding tasks, Separation Logic assertions, and
API specifications. In [72], five different benchmark datasets are used to analyse the performance of GPT-3.5 and GPT-4,
making sure the low-level software requirements meet all high-level requirements. The results reported in [72] showed
that GPT-3.5, using zero-shot prompting with explanations, correctly detected full coverage in four out of five datasets
and achieved 99.7% recall in spotting missing coverage from a removed low-level requirement.
    SAT-LLM, a unique framework to remove conflicting requirements is represented in [24]. It integrated Satisfiability
Modulo Theories (SMT) solvers with LLMs. The performance of LLMs struggles while removing complex requirements
conflicts. With the capability of formal reasoning, integrating SMT solvers with LLMs makes it a viable approach for the
task. Experiments are performed with SAT-LLM and it performed well as compared to standalone performance of LLM
i.e. ChatGPT identified 33% of conflicts with a Precision of 0.85, Recall of 0.31, and an F1 score of 0.46, struggling with
hidden or complex conflicts. SAT-LLM performed better, identifying 80% of conflicts with a Precision of 1.00, Recall of
0.83, and an F1 score of 0.91. [21] used input of error messages, variable names, procedure documentation and user
questions. The suitablility of NLP techniques is discussed by going through the literature for each step of software
development life cycle. The authors of [21] indicated NLP a good candidate for software development. For instance,
they discussed available literature for generating assertions by synthesising sentences in testing phase.
    The paper [63] introduced Req2Spec, an NLP-based tool that analyses natural language requirements to create
formal specifications for HANFOR, a large-scale requirements and test generation tool. Tested on 222 automotive software
Working Document - Formalising Software Requirements with Large Language Models                                      5


requirements at BOSCH, it correctly formalized 71% of them. A primitive work in the domain is about RML [36]. RML
bundled with features of writing requirements, which are based on conceptual model, having attribute of organisation
and abstraction, maintaining precision, consistency and clarity. Well-defined logic and semantics of RML are presented
in [36]. The work [22] evaluated GPT-4o’s ability to generate specifications for C programs that can be verified using
VeriFast, a static verifier based on separation logic. Their experiments, which use different user inputs and prompting
techniques, show that while GPT-4o’s specifications maintain functional behaviour, they often fail verification and
include redundancies when verifiable. The primitive work [66] described automatic translation from natural language
sentences to temporal logic, in order to deploy formal verification of the requirements.
  Paper [89] introduced a methodology Lemur that integrated large language models with automated reasoners
for program verification, formally defining transition rules, proving their soundness, and demonstrating practical
improvements on synthetic and competition benchmarks. Performance of Lemur is compared with Code2Inv, ESBMC,
and UAutomizer while using SV-COMP benchmarks. Code2Inv is a comprehensive work of 2020 [80], contributing
towards learning-based end-to-end program verification. Code2Inv utilised reinforcement learning to train an invariant
synthesizer to propose loop invariants. [65] is a systematic review of the domain i.e. translating between natural
language software requirements to formal ones, based on the databases of Scopus, ACM, IEEE Xplore and Clarivate.
[67] proposed a pipeline integrating Large Language Models (LLMs) to automatically refine and decompose safety
requirements for autonomous driving, addressing frequent updates in the automotive domain. The work evaluated
LLMs’ ability to support Hazard Analysis and Risk Assessment (HARA) through iterative design science and expert
assessments, ultimately implementing the prototype in an industrial setting. The responsible software development
team evaluated its efficiency.
  [92] presented a framework to ensure consistency between different representations of specifications, maintaining
semantic alignment between oral and formal descriptions while ensuring implementation potential through synthesis.
It included time extraction, input-output partitioning, and semantic reasoning beyond syntactic parsing. The framework
of [92] performed well on various test examples. The work [64] reports available NLP tools for Topological Functioning
Modelling (TFM). Among six selected LLM pipelines, best performance tools found were the Stanford CoreNLP toolkit,
FreeLing, and NLTK toolkit. In [60], power of LLMs is utilised for generating Dafny tasks. 178 problems are selected
from MBPP benchmark. Three types of prompts are used: (1) Context less prompts, (2) Signature prompt comprised
of method signature and test cases, and (3) Context of Thought (CoT) prompt based on decomposition of problems
into multiple steps and inclusion of retrieval augmentation generated problems and solutions. GPT-4 outperformed
PaLM-2 on the evaluated tasks and achieved the best results using the retrieval-augmented CoT prompt. The technique
described in [60] provided 153 verified Dafny solutions to MBPP problems, including 103 synthesized by GPT-4 and 50
written manually.
  The work [93] introduced LeanDojo, an open-source toolkit that enables programmatic interaction with Lean theorem
prover, providing annotated proof data to support premise selection in theorem proving. Using LeanDojo’s extracted
data, [93] developed ReProver, a retrieval-augmented LLM-based prover that effectively selects premises, significantly
improving theorem proving efficiency while requiring only one GPU week of training. Furthermore, a new benchmark
with 98,734 theorems and proofs from Lean’s math library constructed. It is designed to test generalization to novel
premises, and demonstrate ReProver’s superiority over non-retrieval baselines and GPT-4. Thor [47] is a framework
developed to integrate language models with theorem provers. The task of finding relevant premises while proving
conjecture is the crucial task in implementing automatic theorem provers. Thor [47] is presented to handle this very
task. The class methods for selecting relevant premises are named Hammers. To test the performance of the framework,
6                                                          Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


the PISA dataset is used. It improved the accuracy from 39% to 57%, while 8.2% of the proofs could not be solved neither
from the language models nor from the theorem provers. Thor also outperformed the previous works while using
MiniF2F dataset. The paper [35] explores the space of integrating Co-pilot (github) with formal methods. It introduces
key formal languages i.e. Dafny, Ada/SPARK, Frama-C, and KeY alongwith the interactive theorem provers (Coq, Isabelle
/ HOL and Lean). The integration of Copilot and formal methods is proposed through development of IDE containing
language servers. The examples of such existing IDEs are VSCode and Eclipse where multiple programming languages
support is available in one IDE through Language Server Protocol (LSP).
    A very comprehensive study on the state of the art of formal specification and verification on autonomous robotic
systems is [56]. The authors did literature review on cyber-physical systems, omitting pure software-based systems.
The survey covered human-controlled and autonomous systems. These were either remotely operated or self-governing.
Formal properties like safety, security and reliability were considered. Mechanical and physical considerations are
excluded from the scope of the survey [56].
    [14] is a comprehensive work on NLP verification, where existing verification approaches are exhaustively analysed
in the paper. A structured NLP Verification Pipeline has been established compromising six critical components:
data selection, generation of perturbations, choice of embedding functions, definition of subspaces, robust training, and
verification through existing algorithms. To validate this pipeline, ANTONIO tool has been implemented. It enabled
modular experimentation with various pipeline components. The key contribution of [14] is the identification of gaps
in existing approaches and the proposal of novel solutions to improve the robustness and reliability of NLP verification
pipelines. NLP verification results have been reported through additional criteria. Standard verifiability metrics has
been extended, comparing geometric with sematic subspaces. Semantic perturbations are employed while conducting
experiments. In [14], the importance of reporting volumes, generalisability, and embedding error of verified subspaces
is emphasised. The reason behind is the great impact of these factors on reliability and interpretability of verification
results. The paper [14] indicates the future expansion by evaluating model robustness against adversarial perturbations
and dataset variations.
    Granberry et al. [34] explored how combining large language models (LLMs) with symbolic analysis can help generate
specifications for C programs. They enhanced LLM prompts using outputs from PathCrawler and EVA to produce ACSL
annotations. Their findings showed that PathCrawler generated context-aware annotations, while EVA contributed to
reducing runtime errors.
    The purpose of Dafny is to automate proofs by outsourcing them to an SMT solver. The SMT solver needs assertions
while automating the process. [61] presented a framework named Laurel to generate Dafny assertions using LLMs.
Mugnier et al. [61] designed two domain-specific prompting techniques. First one locates the position in code where
assertion is missing. This is done through analysis of the verifier’s error message. At the particular location with missing
assertion, a placeholder is inserted. Second technique involves provision of example assertions from codebase. Laurel
was able to generate over 50% of the required helper assertions, making it a viable approach to deploy, while automating
program verification process.
    The work [57] represents a novel framework named SpecGen to generate specifications through LLMs. Two phases
are applied. First phase is about having prompts in conversational style. Second phase is deployed where correct
specifications are not generated. Here, four mutation operators are applied to ensure the correctness of the generated
specifications. Two benchmarks i.e. SV-COMP and SpecGen are used. Verifiable specifications are generated successfully
for 279 out of 384 programs, making [57] a viable approach. The work [13] deals with the challenges involved in
NL2SQL transformation, being widely deployed in Business Intelligence (BI) applications. Bora et al. [13] developed a
Working Document - Formalising Software Requirements with Large Language Models                                             7


new benchmark focused on typical NL questions in industrial BI scenarios. Authors added question categories in the
developed benchmark. Furthermore, two new semantic similarity evaluation metrics are represented in [13], increasing
NL2SQL transformation capabilities.


4    TRACEABILITY OF SOFTWARE REQUIREMENTS
A dynamic requirements traceability model is proposed in [76], enabling improved software quality through verification
and validation of functional requirements. The model ensured software scalability as well, dealing both small and
large-sized projects. A novel model for traceability and verification in the early development phase is presented in
[77]. Adaptability to requirement changes is improvised in the model and its impact is assessed. [29] provided a
comprehensive review of software requirements traceability, covering key elements, challenges, and techniques. The
study classified traceability approaches and highlighted prospects for future research.
    The empirical analysis of requirements completeness is performed in [75]. By enforcing completeness in requirements
ensured reduced defect rates. Here, traceability metrics is produced and regression analysis is performed to quantify the
software quality. [40] introduced the RETRO tool for automating requirements traceability matrix (RTM) generation.
The study showed that RETRO significantly improved accuracy and efficiency compared to manual tracing methods.
[84] proposed a hybrid approach combining VSM and BTM-GA to enhance traceability link generation. The method
outperformed traditional IR techniques, improving recall and precision, particularly in agile development contexts.
    Trustrace [2] is a trust-based traceability recovery approach. It leverages mined data from software repositories. In
comparison to standard IR techniques, Trustrace improved precision and recall in traceability link retrieval. [37] applied
deep learning for traceability, incorporating semantic understanding and domain knowledge. This is done using BI-GRU.
It outperformed traditional approaches of VSM and LSI in terms of accuracy and effectiveness. A topology-based
model-driven approach for backward requirements traceability is presented in [6], formalising specifications and
establishing trace links between real-world functional units and software artifacts.
    In order to manage software evolution process, [16] proposed an event-based traceability mechanism. The work
reported performance improvement in change management by linking artifacts through an event service. It maintained
consistency being deployed in distributed development environment. Tracebok [19] is a body of knowledge on software
requirements traceability. The framework categorised traceability approaches and provided guidance for implementing
traceability in software projects. [58] reviewed visualisation tools and techniques for software requirements trace-
ability. The challenges emphasised were scalability and visual cluttering, providing insights of improved traceability
visualisation.
    In [78], Z notation is used to represent the SRS and design artifacts in order to establish the traceability of functional
requirements. The SRS document originally used UML diagrams for requirement analysis and software design. Z
notation established trace paths based on defined rules. A prototype framework based on XML is developed to trace the
requirements in software design. The designed framework is named as RVVF (Requirement Verification and Validation
Framework). [15] established the concept that terminology extraction can improve traceability from formal models to
textual requirements. Cerbah et al. [15] presented a fully implemented system that analysed text corpora to generate
hierarchically organised terminological resources and formal class hierarchies. These resources and formal class
hierarchies are then communicated to the Troeps knowledge server via an XML stream. The system also enabled user
validation of terminology elements and supports bidirectional linkage between the model and source documents. Survey
paper [82] examined requirements traceability, including definitions, challenges, and tools. [71] represented a tool
8                                                          Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


named TOOR - traceability of object-oriented requirements. The tool is based on the principles of hyper-programming
and hyper-requirements.
    Goknil et al. [33] addressed requirements and their relationships from a traceability perspective. It introduced a
metamodel for requirements that included formally defined relation types. The relations are formalised using first-order
logic to enable inference and consistency checking. A supporting tool demonstrated the approach on a real-world
requirements document, helping to uncover hidden dependencies and detect contradictions.

5     FORMAL METHODS AND TESTING
A detailed examination of the interaction between formal specification techniques and software testing is presented in
the 2009 ACM survey [41]. The paper argues that formal descriptions of systems can significantly support the testing
process. It introduces a classification of formal specification languages into several distinct categories. These include
model-based methods such as Z and VDM, languages grounded in finite-state representations like FSMs and Statecharts,
algebraic approaches such as OBJ, process algebraic notations like CSP and CCS, and hybrid methods that integrate
both continuous and discrete system behaviours—although the latter are treated as outside the scope of the survey.
    In practical applications, formal methods can contribute to testing by either enabling the automated generation of
test cases or offering mechanisms to define precise test oracles. Executable specifications, in particular, may be subjected
to model-checking techniques to assess conformance with desired properties. The theoretical underpinnings that link
formal specifications with testing processes are also explored, with [28] offering foundational contributions—especially
in identifying test selection assumptions that underpin the effectiveness of test generation. Each category of formalism
is associated with its own techniques for producing relevant test artefacts.

5.1    Model-Based
In this category, testing often involves partitioning the input domain using assumptions about uniform system behaviour
within each partition. Logical expressions—frequently cast in disjunctive normal form—are used to define these partitions
and guide automation. Further approaches include domain analysis techniques that focus on identifying critical
boundaries for functions and operators. Additionally, refinement-based testing and mutation techniques are discussed
as part of this landscape. Although highly suitable for defining test oracles, model-based methods are often limited in
their ability to automatically generate tests without the assistance of theorem-proving tools.

5.2    Finite State-Based
Testing approaches that rely on finite-state representations frequently define correctness in terms of language-based
conformance between the implementation and its specification. A common strategy involves using a fault model to
constrain the number of system states considered. Test generation techniques initially focus on deterministic finite-state
machines, before expanding to address partial and non-deterministic forms. While these methods offer structured ways
to derive test suites, the primary challenge lies in managing the combinatorial growth in possible state sequences.

5.3    Process Algebras
Systems described using process algebra are typically interpreted through labelled transition systems (LTS), which
can be infinite. To address this, state space reduction techniques are often employed. In many respects, the methods
and challenges of testing in this domain resemble those found in finite-state approaches, particularly with regard to
scalability and complexity management.
Working Document - Formalising Software Requirements with Large Language Models                                          9


5.4    Algebraic
Algebraic specifications are especially well-suited to object-oriented software. Test cases in this setting may be derived
either from the syntactic structure of operations or from the logical axioms that define their intended behaviours.
This method provides a strong formal basis for validation, although transforming abstract axioms into executable test
procedures requires further elaboration and interpretation.
    The survey places particular emphasis on the value of automated reasoning tools in supporting test activities. Model
checkers are highlighted as being capable of producing counterexamples when temporal properties are not satisfied,
which can subsequently be re-purposed as test cases. Similarly, properties defined in temporal logic can guide the
construction of structured test sequences.


5.5    Formal Tools
Isabelle/HOL is a powerful theorem prover based on higher-order logic. It features robust automation, a large repository
of verified theorems, and tools for interactive proof construction. The system allows formal reasoning about complex
mathematical properties and software systems, offering both depth and flexibility in its approach.
    Frama-C is a modular platform designed for the formal analysis of C code. It supports ACSL (ANSI-C Specification
Language) for specifying expected behaviour and includes plug-ins for static analysis, verification, and integration with
theorem provers. This makes it highly applicable to domains that demand rigorous validation of software correctness.
    There has been significant progress in the use of probabilistic techniques for formal verification [25, 45, 49]. Proba-
bilistic model-checking focuses on evaluating how likely a system is to meet certain criteria, rather than delivering
absolute verdicts. A comprehensive overview of developments in this area is provided in [1], particularly in the field of
statistical model-checking, which offers scalable solutions for analysing stochastic systems in practical contexts.
    Promela is a modelling language aimed at the representation of concurrent systems. It is paired with the SPIN model
checker, which is widely used in both academic and industrial settings. A supporting tool, Modex, can automatically
extract Promela models from C code. SPIN evaluates properties defined in linear-time temporal logic (LTL), and when
verification fails, the counterexamples it provides can be used to create test cases. Its command-line interface makes it
suitable for automation and integration into larger tool-chains.
    TLA+ offers a mathematical framework for specifying systems, particularly those involving concurrency. It em-
phasises logical precision using simple mathematical constructs. PlusCal provides a more familiar, algorithm-like
syntax that compiles directly into TLA+, enabling a smoother transition for developers accustomed to pseudocode-style
representations.


6     FORMAL PROOFS IN UTP AND THEORY OF INSTITUTION
[88] provided a tutorial introduction to Hoare and He’s Unifying Theories of Programming (UTP) and the concept of
designs. It explained how alphabetised relational calculus could describe various programming constructs, illustrating
their application to imperative programming theories like Hoare logic and the refinement calculus. [32] introduced the
concept of institutions as a formal framework to model logical systems. It presented several foundational results, such
as gluing signatures, preserving theory structuring, and extending institutions to include constraints for abstract data
types, contributing significantly to the theory of specifications and programming languages.
    [87] discussed Circus, a concurrent language that integrated imperative programming, CSP, and Z through the
unifying theories of programming. It provided a formalisation of Circus in the UTP framework, highlighting its use for
10                                                         Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


refining concurrent systems. [39] explored integrating runtime verification into an automated UAS Traffic Management
system. It demonstrated how runtime verification could ensure system safety by applying formal requirements to
various subsystems, validated through real-world flight simulations.
     [12] presented formal verification applied to the RTEMS real-time operating system, using Promela models and the
SPIN model-checker to verify multi-core processor qualification for spaceflight. It discussed linking UTP semantics to
enhance the test generation process, with a focus on future research directions.
     [26] introduced Isabelle/UTP, an implementation of Hoare and He’s UTP for unifying formal semantics. It enabled
mechanising computational theories across paradigms and provided proof tools for Hoare logic, refinement calculus,
and other computational paradigms, supporting the development of automated verification tools. [46] discussed the
use of UML and the UML Testing Profile (UTP) in model-based testing for resource-constrained real-time embedded
systems. It addressed the generation of test artefacts from UTP standards and presented a detailed algorithm for creating
test cases for such systems.
     [27] presented a Java model of the priority inheritance protocol in the RTEMS real-time operating system, verified
using Java Pathfinder. It detected and fixed known bugs in the RTEMS implementation, ensuring the absence of issues
like data races, deadlocks, and priority inversions. [83] proposed an iterative prompting framework for pre-trained
language models to handle multi-step reasoning tasks. It introduced a context-aware prompter that dynamically
synthesised prompts based on the current step’s context, improving the model’s reasoning capabilities in complex tasks.

7     FUTURE DIRECTIONS
In this section, we outline prospective directions informed by the literature review. Much of the literature in this
review employed queries containing a problem description and some instructions to achieve a desired outcome. Such
querying of LLMs without training or examples of the current task is typically referred as zero-shot prompting and
shows excellent performance on many tasks [48]. Surprisingly, they also showed that the performance of LLM on some
challenging problems can be improved by encouraging the LLM to reason using intermediate steps through a simple
addition to problem prompts (“Lets think step by step”).

7.1    Advanced Prompt Engineering
Beyond this approach is one-shot prompting that includes an example of a solved problem to guide the LLM into
generating the desired output [55]. This can be extended to few-shot prompting where a number of differing examples
guide the LLM. But improved results are not assured as some studies e.g. [95] show that zero-shot can outperform the
few-shot case [96]. [42] reviewed the evolution of prompt engineering in LLMs, including discussions on self-consistency
and multimodal prompt learning. It also reviewed the literature related to adversarial attacks and evaluation strategies
for ensuring robust AI interactions.
     Chain of Thought (CoT) [85] prompting involves a sequence of prompts producing intermediate results that are
generated by the LLM and used to drive subsequent prompting interactions. These orchestrated interactions can improve
LLM performance on tasks requiring logic, calculation and decision-making in areas like math, common sense reasoning,
and symbolic manipulation. CoT requires the LLM to articulate the distinct steps of its reasoning, by subdividing larger
tasks into multi-step reasoning stages, acting as a precursor for subsequent stages. But the CoT approach may require
careful analysis when used with larger LLM offering long input contexts. This is because of the lost-in-the-middle
problem where LLM show a U-shaped attention bias [42] and can fail to attend to information in the middle of the
context window.
Working Document - Formalising Software Requirements with Large Language Models                                         11


    PromptCoT [94] enhanced the quality of solutions for diffusion-based generative models by employing the CoT
approach. The computational cost is minimised through adapter-based fine-tuning. Prompt design is explored in detail
in [3]. It discussed Chain-of-Thought and Reflection techniques, along with best practices for structuring prompts and
building LLM-based agents.
    Besta et al. [10] introduced the concept of reasoning topologies, examining how structures such as Chains, Trees,
and Graphs of Thought improve LLM reasoning. They also proposed a taxonomy of structured reasoning techniques,
highlighting their influence on both performance and efficiency. Structured Chain-of-Thought (SCoT) prompting was
proposed by [53] to enhance code generation by incorporating structured programming principles. This approach
significantly improved the accuracy and robustness of LLM-based code synthesis compared to standard CoT methods.
Building on the theme of automation, [79] introduced Automate-CoT, a technique for automatically generating and
selecting rational chains for CoT prompting. By minimising dependence on human annotations, it enabled more flexible
adaptation of CoT strategies across diverse reasoning tasks. Complementing these efforts, [86] presented a prompt
pattern catalog that offered reusable design patterns to optimise LLM interactions, thereby refining prompt engineering
practices for a wide range of applications. Additionally, [90] proposed Reprompting (Gibbs sampling-based algorithm)
for discovering optimal CoT prompts. The proposed prompting technique consistently outperformed human-crafted
alternatives and demonstrated high adaptability across various reasoning benchmarks.
    Retrieval Augmented Generation (RAG) [52] supplements problem information with specifically retrieved information
and is often used in knowledge intensive tasks. This helps ensure the LLM attends specifically to the retrieved information
when addressing the users prompt. LLM model selection (chat vs reasoning) and fine tuning such as with LoRA [43]
remain among a growing number of possibilities for exploration.
    Based on the literature survey conducted, we sketch one line research agenda: in VERIFAI, we aim to improve
the techniques that bridge the gap between informal natural language description and rigorous formal specifications,
through refinement of prompt engineering, the incorporation of chain-of-thought reasoning and the development of
hybrid neuro-symbolic approaches.


8    CONCLUSIONS
The role of large language models in formalising software requirements is surveyed in this paper. The key contribution
of the selected papers is on bridging the gap between informal natural language descriptions and rigorous formal
specifications. We can enhance requirement formalisation through automating translations. The accuracy of translated
ones is of key importance. We can deploy iterative refinements to improve the accuracy and correctness of the generated
requirements. While LLMs is contributing significantly in improving development cycle, the challenges of ambiguity
resolution, verification and domain adaptation shall be the focus areas of future research.
    In future research, the refinement of prompt engineering techniques, the incorporation of chain-of-thought reasoning
and the development of hybrid neuro-symbolic approaches are the key areas to look at. Our survey concludes with the
remarks that the better collaboration with industry and academia will further enhance the domain.


9    ACKNOWLEDGEMENTS
This work is partly funded by the ADAPT Research Centre for AI-Driven Digital Content Technology, which is funded
by Research Ireland through the Research Ireland Centres Programme and is co funded under the European Regional
Development Fund (ERDF) through Grant 13/RC/2106 P2.
12                                                                      Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


REFERENCES
 [1] Gul Agha and Karl Palmskog. 2018. A survey of statistical model checking. ACM Transactions on Modeling and Computer Simulation 28, 1 (2018),
     6:1–6:39. https://doi.org/10.1145/3158668
 [2] Nasir Ali, Yann-Gaël Guéhéneuc, and Giuliano Antoniol. 2013. Trustrace: Mining Software Repositories to Improve the Accuracy of Requirement
     Traceability Links. IEEE Transactions on Software Engineering 39, 5 (2013), 725–741. https://doi.org/10.1109/TSE.2012.71
 [3] Xavier Amatriain. 2024. Prompt Design and Engineering: Introduction and Advanced Methods. (2024). arXiv:cs.SE/2401.14423 https://arxiv.org/abs/
     2401.14423
 [4] Chetan Arora, John Grundy, and Mohamed Abdelrazek. 2023. Advancing Requirements Engineering through Generative AI: Assessing the Role of
     LLMs. (2023). arXiv:cs.SE/2310.13976 https://arxiv.org/abs/2310.13976
 [5] Chetan Arora, Mehrdad Sabetzadeh, Lionel Briand, and Frank Zimmer. 2016. Extracting domain models from natural-language requirements:
     approach and industrial evaluation. In Proceedings of the ACM/IEEE 19th International Conference on Model Driven Engineering Languages and
     Systems (MODELS ’16). Association for Computing Machinery, New York, NY, USA, 250–260. https://doi.org/10.1145/2976767.2976769
 [6] Erika Asnina, Bernards Gulbis, Janis Osis, Gundars Alksnis, Uldis Donins, and Armands Slihte. 2011. Backward Requirements Traceability within
     the Topology-based Model Driven Software Development. In MDA & MDSD 2011 - Proceedings of the 3rd International Workshop on Model-Driven
     Architecture and Modeling-Driven Software Development, In conjunction with ENASE 2011, Beijing, China, June 2011, Janis Osis and Oksana Nikiforova
     (Eds.). SciTePress, 36–45.
 [7] Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan. 2025. Formalising Software Requirements using Large Language Models. (2025).
     arXiv:cs.SE/2506.10704 https://arxiv.org/abs/2506.10704
 [8] Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan. 2025. A Short Survey on Formalising Software Requirements using Large Language
     Models. (2025). arXiv:cs.SE/2506.11874 https://arxiv.org/abs/2506.11874
 [9] Ron Bell. 2006. Introduction to IEC 61508. In Proceedings of the 10th Australian Workshop on Safety Critical Systems and Software - Volume 55 (SCS
     ’05). Australian Computer Society, Inc., AUS, 3–12.
[10] Maciej Besta, Florim Memedi, Zhenyu Zhang, Robert Gerstenberger, Nils Blach, Piotr Nyczyk, Marcin Copik, Grzegorz Kwasniewski, Jürgen Müller,
     Lukas Gianinazzi, Ales Kubicek, Hubert Niewiadomski, Onur Mutlu, and Torsten Hoefler. 2024. Topologies of Reasoning: Demystifying Chains,
     Trees, and Graphs of Thoughts. CoRR abs/2401.14295 (2024). https://doi.org/10.48550/arXiv.2401.14295 arXiv:2401.14295
[11] Benjamin Brosgol. 2011. Do-178c: the next avionics safety standard. Ada Lett. 31, 3 (Nov. 2011), 5–6. https://doi.org/10.1145/2070336.2070341
[12] Andrew Butterfield and Frédéric Tuong. 2023. Applying Formal Verification to an Open-Source Real-Time Operating System. In Theories of
     Programming and Formal Methods - Essays Dedicated to Jifeng He on the Occasion of His 80th Birthday (Lecture Notes in Computer Science), Jonathan P.
     Bowen, Qin Li, and Qiwen Xu (Eds.), Vol. 14080. Springer, 348–366. https://doi.org/10.1007/978-3-031-40436-8_13
[13] Bora Caglayan, Mingxue Wang, John D. Kelleher, Shen Fei, Gui Tong, Jiandong Ding, and Puchao Zhang. 2024. BIS: NL2SQL Service Evaluation
     Benchmark for Business Intelligence Scenarios. In Service-Oriented Computing: 22nd International Conference, ICSOC 2024, Tunis, Tunisia, December
     3–6, 2024, Proceedings, Part II. Springer-Verlag, Berlin, Heidelberg, 357–372. https://doi.org/10.1007/978-981-96-0808-9_27
[14] Marco Casadio, Tanvi Dinkar, Ekaterina Komendantskaya, Luca Arnaboldi, Matthew L. Daggitt, Omri Isac, Guy Katz, Verena Rieser, and Oliver Lemon.
     2025. NLP Verification: Towards a General Methodology for Certifying Robustness. (2025). arXiv:cs.CL/2403.10144 https://arxiv.org/abs/2403.10144
[15] Farid Cerbah and Jérôme Euzenat. 2001. Using Terminology Extraction to Improve Traceability from Formal Models to Textual Requirements. In
     Natural Language Processing and Information Systems, Mokrane Bouzeghoub, Zoubida Kedad, and Elisabeth Métais (Eds.). Springer Berlin Heidelberg,
     Berlin, Heidelberg, 115–126.
[16] J. Cleland-Huang, C.K. Chang, and M. Christensen. 2003. Event-based traceability for managing evolutionary change. IEEE Transactions on Software
     Engineering 29, 9 (2003), 796–810. https://doi.org/10.1109/TSE.2003.1232285
[17] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Caroline Trippel. 2023. nl2spec: Interactively Translating Unstructured
     Natural Language to Temporal Logics with Large Language Models. (2023). arXiv:cs.LO/2303.04864 https://arxiv.org/abs/2303.04864
[18] Juan Ortiz Couder, Dawson Gomez, and Omar Ochoa. 2024. Requirements Verification Through the Analysis of Source Code by Large Language
     Models. In SoutheastCon 2024. 75–80. https://doi.org/10.1109/SoutheastCon52093.2024.10500073
[19] Ana Marcia Debiasi Duarte, Denio Duarte, and Marcello Thiry. 2016. TraceBoK: Toward a Software Requirements Traceability Body of Knowledge.
     In 2016 IEEE 24th International Requirements Engineering Conference (RE). 236–245. https://doi.org/10.1109/RE.2016.32
[20] Elicit. 2025. Elicit - The AI Research Assistant. https://elicit.com. (2025). Accessed: 2025-04-11 at 12:49PM.
[21] Michael D. Ernst. 2017. Natural Language is a Programming Language: Applying Natural Language Processing to Software Development. In
     2nd Summit on Advances in Programming Languages (SNAPL 2017) (Leibniz International Proceedings in Informatics (LIPIcs)), Benjamin S. Lerner,
     Rastislav Bodík, and Shriram Krishnamurthi (Eds.), Vol. 71. Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 4:1–4:14.
     https://doi.org/10.4230/LIPIcs.SNAPL.2017.4
[22] Wen Fan, Marilyn Rego, Xin Hu, Sanya Dod, Zhaorui Ni, Danning Xie, Jenna DiVincenzo, and Lin Tan. 2025. Evaluating the Ability of Large
     Language Models to Generate Verifiable Specifications in VeriFast. (2025). arXiv:cs.SE/2411.02318 https://arxiv.org/abs/2411.02318
[23] Wenji Fang, Mengming Li, Min Li, Zhiyuan Yan, Shang Liu, Hongce Zhang, and Zhiyao Xie. 2024. AssertLLM: Generating Hardware Verification
     Assertions from Design Specifications via Multi-LLMs. In 2024 IEEE LLM Aided Design Workshop (LAD). 1–1. https://doi.org/10.1109/LAD62341.2024.
     10691792
Working Document - Formalising Software Requirements with Large Language Models                                                                         13


[24] Mohamad Fazelnia, Mehdi Mirakhorli, and Hamid Bagheri. 2024. Translation Titans, Reasoning Challenges: Satisfiability-Aided Language Models
     for Detecting Conflicting Requirements. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE ’24).
     Association for Computing Machinery, New York, NY, USA, 2294–2298. https://doi.org/10.1145/3691620.3695302
[25] Antonio Filieri, Carlo Ghezzi, and Giordano Tamburrelli. 2011. Run-time efficient probabilistic model checking. In Proceedings of the 33rd
     International Conference on Software Engineering, ICSE 2011, Richard N. Taylor, Harald C. Gall, and Nenad Medvidovic (Eds.). ACM, 341–350.
     https://doi.org/10.1145/1985793.1985840
[26] Simon Foster, James Baxter, Ana Cavalcanti, Jim Woodcock, and Frank Zeyda. 2020. Unifying semantic foundations for automated verification tools
     in Isabelle/UTP. Science of Computer Programming 197 (2020), 102510. https://doi.org/10.1016/j.scico.2020.102510
[27] Saurabh Gadia, Cyrille Artho, and Gedare Bloom. 2016. Verifying Nested Lock Priority Inheritance in RTEMS with Java Pathfinder. In Formal
     Methods and Software Engineering, Kazuhiro Ogata, Mark Lawford, and Shaoying Liu (Eds.). Springer International Publishing, Cham, 417–432.
     https://doi.org/10.1007/978-3-319-47846-3_26
[28] Marie-Claude Gaudel. 1995. Testing can be formal, too. In TAPSOFT‘95: Theory and Practice of Software Development, 6th International Joint
     Conference CAAP/FASE (Lecture Notes in Computer Science), Peter D. Mosses, Mogens Nielsen, and Michael I. Schwartzbach (Eds.), Vol. 915. Springer,
     82–96. https://doi.org/10.1007/3-540-59293-8_188
[29] E. C. Genvigir and N. L. Vijaykumar. 2010. Requirements Traceability. In Handbook of Research on Software Engineering and Productivity
     Technologies: Implications of Globalization, Muthu Ramachandran and Ricardo de Carvalho (Eds.). IGI Global Scientific Publishing, 102–120.
     https://doi.org/10.4018/978-1-60566-731-7.ch008
[30] Vincenzo Gervasi and Bashar Nuseibeh. 2002. Lightweight validation of natural language requirements. Softw. Pract. Exper. 32, 2 (Feb. 2002),
     113–133. https://doi.org/10.1002/spe.430
[31] Shalini Ghosh, Daniel Elenius, Wenchao Li, Patrick Lincoln, Natarajan Shankar, and Wilfried Steiner. 2016. ARSENAL: Automatic Requirements
     Specification Extraction from Natural Language. In NASA Formal Methods, Sanjai Rayadurgam and Oksana Tkachuk (Eds.). Springer International
     Publishing, Cham, 41–46.
[32] Joseph A. Goguen and Rod M. Burstall. 1992. Institutions: abstract model theory for specification and programming. J. ACM 39, 1 (Jan. 1992),
     95–146. https://doi.org/10.1145/147508.147524
[33] Arda Goknil, Ivan Kurtev, Klaas van den Berg, and Jan-Willem Veldhuis. 2011. Semantics of trace relations in requirements models for consistency
     checking and inferencing. Software & Systems Modeling 10, 1 (2011), 31–54. https://doi.org/10.1007/s10270-009-0142-3
[34] George Granberry, Wolfgang Ahrendt, and Moa Johansson. 2025. Specify What? Enhancing Neural Specification Synthesis by Symbolic Methods.
     In Integrated Formal Methods, Nikolai Kosmatov and Laura Kovács (Eds.). Springer Nature Switzerland, Cham, 307–325.
[35] George Granberry, Wolfgang Ahrendt, and Moa Johansson. 2025. Towards Integrating Copiloting and Formal Methods. In Leveraging Applications of
     Formal Methods, Verification and Validation. Specification and Verification, Tiziana Margaria and Bernhard Steffen (Eds.). Springer Nature Switzerland,
     Cham, 144–158.
[36] Sol J. Greenspan, Alexander Borgida, and John Mylopoulos. 1986. A requirements modeling language and its logic. Information Systems 11, 1 (1986),
     9–23. https://doi.org/10.1016/0306-4379(86)90020-7
[37] Jin Guo, Jinghui Cheng, and Jane Cleland-Huang. 2017. Semantically enhanced software traceability using deep learning techniques. In Proceedings
     of the 39th International Conference on Software Engineering (ICSE ’17). IEEE Press, 3–14. https://doi.org/10.1109/ICSE.2017.9
[38] Christopher Hahn, Frederik Schmitt, Julia J. Tillman, Niklas Metzger, Julian Siber, and Bernd Finkbeiner. 2022. Formal Specifications from Natural
     Language. (2022). arXiv:cs.SE/2206.01962 https://arxiv.org/abs/2206.01962
[39] Abigail Hammer, Matthew Cauwels, Benjamin Hertz, Phillip H. Jones, and Kristin Y. Rozier. 2022. Integrating runtime verification into an automated
     UAS traffic management system. Innov. Syst. Softw. Eng. 18, 4 (2022), 567–580. https://doi.org/10.1007/S11334-021-00407-5
[40] Jane Huffman Hayes, Alex Dekhtyar, Senthil Karthikeyan Sundaram, E. Ashlee Holbrook, Sravanthi Vadlamudi, and Alain April. 2007. REquirements
     TRacing On target (RETRO): improving software maintenance through traceability recovery. Innovations in Systems and Software Engineering 3, 3
     (September 2007), 193–202. https://doi.org/10.1007/s11334-007-0024-1
[41] Robert M. Hierons, Kirill Bogdanov, Jonathan P. Bowen, Rance Cleaveland, John Derrick, Jeremy Dick, Marian Gheorghe, Mark Harman, Kalpesh
     Kapoor, Paul J. Krause, Gerald Lüttgen, Anthony J. H. Simons, Sergiy A. Vilkomir, Martin R. Woodward, and Hussein Zedan. 2009. Using formal
     specifications to support testing. ACM Comput. Surv. 41, 2, 9:1–9:76. https://doi.org/10.1145/1459352.1459354
[42] Cheng-Yu Hsieh, Yung-Sung Chuang, Chun-Liang Li, Zifeng Wang, Long T. Le, Abhishek Kumar, James R. Glass, Alexander Ratner, Chen-Yu Lee,
     Ranjay Krishna, and Tomas Pfister. 2024. Found in the middle: Calibrating Positional Attention Bias Improves Long Context Utilization. In Findings
     of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024, Lun-Wei Ku, Andre Martins,
     and Vivek Srikumar (Eds.). Association for Computational Linguistics, 14982–14995. https://doi.org/10.18653/V1/2024.FINDINGS-ACL.890
[43] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2022. LoRA: Low-Rank
     Adaptation of Large Language Models. In The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022.
     OpenReview.net. https://openreview.net/forum?id=nZeVKeeFYf9
[44] Marieke Huisman, Dilian Gurov, and Alexander Malkis. 2024. Formal Methods: From Academia to Industrial Practice. A Travel Guide. (2024).
     arXiv:cs.SE/2002.07279 https://arxiv.org/abs/2002.07279
[45] Thomas Hérault, Richard Lassaigne, Frédéric Magniette, and Sylvain Peyronnet. 2004. Approximate probabilistic model checking. In Verification,
     Model Checking, and Abstract Interpretation, 5th International Conference, VMCAI 2004 (Lecture Notes in Computer Science), Bernhard Steffen and
14                                                                        Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


     Giorgio Levi (Eds.), Vol. 2937. Springer, 73–84. https://doi.org/10.1007/978-3-540-24622-0_8
[46] Padma Iyenghar, Elke Pulvermueller, and Clemens Westerkamp. 2011. Towards Model-Based Test automation for embedded systems using UML
     and UTP. In ETFA2011. 1–9. https://doi.org/10.1109/ETFA.2011.6058982
[47] Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygóźdź, Piotr Mił oś, Yuhuai Wu, and Mateja Jamnik. 2022.
     Thor: Wielding Hammers to Integrate Language Models and Automated Theorem Provers. In Advances in Neural Information Processing Systems,
     S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (Eds.), Vol. 35. Curran Associates, Inc., 8360–8373.
[48] Takeshi Kojima, Shixiang (Shane) Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. Large Language Models are Zero-Shot Reasoners.
     In Advances in Neural Information Processing Systems, S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (Eds.), Vol. 35. Curran
     Associates, Inc., 22199–22213.
[49] Marta Z. Kwiatkowska, Gethin Norman, and David Parker. 2002. PRISM: probabilistic symbolic model checker. In Computer Performance Evaluation,
     Modelling Techniques and Tools, 12th International Conference, TOOLS 2002 (Lecture Notes in Computer Science), Tony Field, Peter G. Harrison,
     Jeremy T. Bradley, and Uli Harder (Eds.), Vol. 2324. Springer, 200–204. https://doi.org/10.1007/3-540-46029-2_13
[50] Iat Tou Leong and Raul Barbosa. 2023. Translating Natural Language Requirements to Formal Specifications: A Study on GPT and Symbolic NLP. In
     2023 53rd Annual IEEE/IFIP International Conference on Dependable Systems and Networks Workshops (DSN-W). 259–262. https://doi.org/10.1109/DSN-
     W58399.2023.00065
[51] Henrik Leopold, Jan Mendling, and Artem Polyvyanyy. 2014. Supporting Process Model Validation through Natural Language Generation. IEEE
     Transactions on Software Engineering 40, 8 (2014), 818–840. https://doi.org/10.1109/TSE.2014.2327044
[52] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim
     Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2020. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In Advances in Neural
     Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual,
     Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin (Eds.). https://proceedings.neurips.cc/paper/2020/
     hash/6b493230205f780e1bc26945df7481e5-Abstract.html
[53] Jia Li, Ge Li, Yongmin Li, and Zhi Jin. 2025. Structured Chain-of-Thought Prompting for Code Generation. ACM Trans. Softw. Eng. Methodol. 34, 2,
     Article 37 (Jan. 2025), 23 pages. https://doi.org/10.1145/3690635
[54] Mengming Li, Wenji Fang, Qijun Zhang, and Zhiyao Xie. 2024. SpecLLM: Exploring Generation and Review of VLSI Design Specification with
     Large Language Model. (2024). arXiv:cs.AR/2401.13266 https://arxiv.org/abs/2401.13266
[55] Yunshui Li, Binyuan Hui, Xiaobo Xia, Jiaxi Yang, Min Yang, Lei Zhang, Shuzheng Si, Ling-Hao Chen, Junhao Liu, Tongliang Liu, Fei Huang,
     and Yongbin Li. 2024. One-Shot Learning as Instruction Data Prospector for Large Language Models. (2024). arXiv:cs.CL/2312.10302 https:
     //arxiv.org/abs/2312.10302
[56] Matt Luckcuck, Marie Farrell, Louise A. Dennis, Clare Dixon, and Michael Fisher. 2019. Formal Specification and Verification of Autonomous
     Robotic Systems: A Survey. ACM Comput. Surv. 52, 5, Article 100 (Sept. 2019), 41 pages. https://doi.org/10.1145/3342355
[57] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2024. SpecGen: Automated Generation of Formal Program Specifications via Large Language
     Models. (2024). arXiv:cs.SE/2401.08807 https://arxiv.org/abs/2401.08807
[58] Abdulkadir Ahmad Madaki and Wan Mohd Nazmee Wan Zainon. 2022. A Review on Tools and Techniques for Visualizing Software Requirement
     Traceability. In Proceedings of the 11th International Conference on Robotics, Vision, Signal Processing and Power Applications, Nor Muzlifah Mahyuddin,
     Nor Rizuan Mat Noor, and Harsa Amylia Mat Sakim (Eds.). Springer Singapore, Singapore, 39–44.
[59] Shantanu Mandal, Adhrik Chethan, Vahid Janfaza, S M Farabi Mahmud, Todd A Anderson, Javier Turek, Jesmin Jahan Tithi, and Abdullah Muzahid.
     2023. Large Language Models Based Automatic Synthesis of Software Specifications. (2023). arXiv:cs.SE/2304.09181 https://arxiv.org/abs/2304.09181
[60] Md Rakib Hossain Misu, Cristina V. Lopes, Iris Ma, and James Noble. 2024. Towards AI-Assisted Synthesis of Verified Dafny Methods. Proc. ACM
     Softw. Eng. 1, FSE, Article 37 (July 2024), 24 pages. https://doi.org/10.1145/3643763
[61] Eric Mugnier, Emmanuel Anaya Gonzalez, Ranjit Jhala, Nadia Polikarpova, and Yuanyuan Zhou. 2024. Laurel: Generating Dafny Assertions Using
     Large Language Models. (2024). arXiv:cs.LO/2405.16792 https://arxiv.org/abs/2405.16792
[62] Prasita Mukherjee and Benjamin Delaware. 2024. Towards Automated Verification of LLM-Synthesized C Programs. (2024). arXiv:cs.PL/2410.14835
     https://arxiv.org/abs/2410.14835
[63] Anmol Nayak, Hari Prasad Timmapathini, Vidhya Murali, Karthikeyan Ponnalagu, Vijendran Gopalan Venkoparao, and Amalinda Post. 2022.
     Req2Spec: Transforming Software Requirements into Formal Specifications Using Natural Language Processing. In Requirements Engineering:
     Foundation for Software Quality: 28th International Working Conference, REFSQ 2022, Birmingham, UK, March 21–24, 2022, Proceedings. Springer-Verlag,
     Berlin, Heidelberg, 87–95.
[64] Erika Nazaruka and J?nis Osis. 2018. Determination of Natural Language Processing Tasks and Tools for Topological Functioning Modelling. In
     Proceedings of the 13th International Conference on Evaluation of Novel Approaches to Software Engineering (ENASE 2018). SCITEPRESS - Science and
     Technology Publications, Lda, Setubal, PRT, 501–512. https://doi.org/10.5220/0006817205010512
[65] Sabina-Cristiana Necula, Florin Dumitriu, and Valerică Greavu-S, erban. 2024. A Systematic Literature Review on Using Natural Language Processing
     in Software Requirements Engineering. Electronics 13, 11 (2024). https://doi.org/10.3390/electronics13112055
[66] Rani Nelken and Nissim Francez. 1996. Automatic translation of natural language system specifications into temporal logic. In Computer Aided
     Verification, Rajeev Alur and Thomas A. Henzinger (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 360–371.
Working Document - Formalising Software Requirements with Large Language Models                                                                     15


[67] Ali Nouri, Beatriz Cabrero-Daniel, Fredrik Törner, Håkan Sivencrona, and Christian Berger. 2024. Engineering Safety Requirements for Autonomous
     Driving with Large Language Models. In 2024 IEEE 32nd International Requirements Engineering Conference (RE). 218–228. https://doi.org/10.1109/
     RE59067.2024.00029
[68] Wiktor Nowakowski, Michał Śmiałek, Albert Ambroziewicz, and Tomasz Straszak. 2013. Requirements-level language and tools for capturing
     software system essence. Computer Science and Information Systems 10, 4 (2013), 1499–1524.
[69] M. Osborne and C.K. MacNish. 1996. Processing natural language software requirement specifications. In Proceedings of the Second International
     Conference on Requirements Engineering. 229–236. https://doi.org/10.1109/ICRE.1996.491451
[70] Rob Palin, David Ward, Ibrahim Habli, and Roger Rivett. 2011. ISO 26262 safety cases: Compliance and assurance. In 6th IET International Conference
     on System Safety 2011. 1–6. https://doi.org/10.1049/cp.2011.0251
[71] F.A.C. Pinheiro and J.A. Goguen. 1996. An object-oriented tool for tracing requirements. In Proceedings of the Second International Conference on
     Requirements Engineering. 219–. https://doi.org/10.1109/ICRE.1996.491449
[72] Anamaria-Roberta Preda, Christoph Mayr-Dorn, Atif Mashkoor, and Alexander Egyed. 2024. Supporting High-Level to Low-Level Requirements
     Coverage Reviewing with Large Language Models. In Proceedings of the 21st International Conference on Mining Software Repositories (MSR ’24).
     Association for Computing Machinery, New York, NY, USA, 242–253. https://doi.org/10.1145/3643991.3644922
[73] Xin Quan, Marco Valentino, Louise A. Dennis, and André Freitas. 2024. Verification and Refinement of Natural Language Explanations through
     LLM-Symbolic Theorem Proving. (2024). arXiv:cs.CL/2405.01379 https://arxiv.org/abs/2405.01379
[74] Lasse M. Reinpold, Marvin Schieseck, Lukas P. Wagner, Felix Gehlhoff, and Alexander Fay. 2024. Exploring LLMs for Verifying Technical System
     Specifications Against Requirements. (2024). arXiv:cs.SE/2411.11582 https://arxiv.org/abs/2411.11582
[75] Patrick Rempel and Parick Mäder. 2017. Preventing Defects: The Impact of Requirements Traceability Completeness on Software Quality. IEEE
     Transactions on Software Engineering 43, 8 (2017), 777–797. https://doi.org/10.1109/TSE.2016.2622264
[76] A.M. Salem. 2006. Improving Software Quality through Requirements Traceability Models. In IEEE International Conference on Computer Systems
     and Applications, 2006. 1159–1162. https://doi.org/10.1109/AICCSA.2006.205236
[77] Ahmed M Salem. 2010. Model for Enhancing Requirements Traceability and Analysis. International Journal of Advanced Computer Science and
     Applications 1, 5 (2010). https://doi.org/10.14569/IJACSA.2010.010503
[78] Sabnam Sengupta, Ananya Kanjilal, and Swapan Bhattacharya. 2008. Requirement Traceability in Software Development Process: An Empirical
     Approach. In 2008 The 19th IEEE/IFIP International Symposium on Rapid System Prototyping. 105–111. https://doi.org/10.1109/RSP.2008.14
[79] Kashun Shum, Shizhe Diao, and Tong Zhang. 2023. Automatic Prompt Augmentation and Selection with Chain-of-Thought from Labeled Data. In
     Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023, Houda Bouamor, Juan Pino, and Kalika Bali
     (Eds.). Association for Computational Linguistics, 12113–12139. https://doi.org/10.18653/V1/2023.FINDINGS-EMNLP.811
[80] Xujie Si, Aaditya Naik, Hanjun Dai, Mayur Naik, and Le Song. 2020. Code2Inv: A Deep Learning Framework for Program Verification. In Computer
     Aided Verification, Shuvendu K. Lahiri and Chao Wang (Eds.). Springer International Publishing, Cham, 151–164.
[81] Norbert Tihanyi, Ridhi Jain, Yiannis Charalambous, Mohamed Amine Ferrag, Youcheng Sun, and Lucas C. Cordeiro. 2024. A New Era in
     Software Security: Towards Self-Healing Software via Large Language Models and Formal Verification. (2024). arXiv:cs.SE/2305.14752 https:
     //arxiv.org/abs/2305.14752
[82] RICHARD TORKAR, TONY GORSCHEK, ROBERT FELDT, MIKAEL SVAHNBERG, UZAIR AKBAR RAJA, and KASHIF KAMRAN. 2012. REQUIRE-
     MENTS TRACEABILITY: A SYSTEMATIC REVIEW AND INDUSTRY CASE STUDY. International Journal of Software Engineering and Knowledge
     Engineering 22, 03 (2012), 385–433. https://doi.org/10.1142/S021819401250009X arXiv:https://doi.org/10.1142/S021819401250009X
[83] Boshi Wang, Xiang Deng, and Huan Sun. 2022. Iteratively Prompt Pre-trained Language Models for Chain of Thought. In Proceedings of the
     2022 Conference on Empirical Methods in Natural Language Processing, Yoav Goldberg, Zornitsa Kozareva, and Yue Zhang (Eds.). Association for
     Computational Linguistics, Abu Dhabi, United Arab Emirates, 2714–2730. https://doi.org/10.18653/v1/2022.emnlp-main.174
[84] Bangchao Wang, Rong Peng, Zhuo Wang, Xiaomin Wang, and Yuanbang Li. 2020. An Automated Hybrid Approach for Generating Requirements Trace
     Links. International Journal of Software Engineering and Knowledge Engineering 30, 07 (2020), 1005–1048. https://doi.org/10.1142/S0218194020500278
     arXiv:https://doi.org/10.1142/S0218194020500278
[85] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi, Quoc V Le, and Denny Zhou. 2022. Chain-of-Thought
     Prompting Elicits Reasoning in Large Language Models. In Advances in Neural Information Processing Systems, S. Koyejo, S. Mohamed, A. Agarwal,
     D. Belgrave, K. Cho, and A. Oh (Eds.), Vol. 35. Curran Associates, Inc., 24824–24837.
[86] Jules White, Quchen Fu, Sam Hays, Michael Sandborn, Carlos Olea, Henry Gilbert, Ashraf Elnashar, Jesse Spencer-Smith, and Douglas C. Schmidt. 2023.
     A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT. CoRR abs/2302.11382 (2023). https://doi.org/10.48550/ARXIV.2302.11382
     arXiv:2302.11382
[87] Jim Woodcock and Ana Cavalcanti. 2002. The Semantics of Circus. In ZB 2002: Formal Specification and Development in Z and B, Didier Bert,
     Jonathan P. Bowen, Martin C. Henson, and Ken Robinson (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 184–203. https://doi.org/10.1007/3-
     540-45648-1_10
[88] Jim Woodcock and Ana Cavalcanti. 2004. A Tutorial Introduction to Designs in Unifying Theories of Programming. In Integrated Formal Methods,
     Eerke A. Boiten, John Derrick, and Graeme Smith (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 40–66.
[89] Haoze Wu, Clark Barrett, and Nina Narodytska. 2024. Lemur: Integrating Large Language Models in Automated Program Verification. (2024).
     arXiv:cs.FL/2310.04870 https://arxiv.org/abs/2310.04870
16                                                                   Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


[90] Weijia Xu, Andrzej Banburski-Fahey, and Nebojsa Jojic. 2023. Reprompting: Automated Chain-of-Thought Prompt Inference Through Gibbs
     Sampling. CoRR abs/2305.09993 (2023). https://doi.org/10.48550/ARXIV.2305.09993 arXiv:2305.09993
[91] Yilongfei Xu, Jincao Feng, and Weikai Miao. 2024. Learning from Failures: Translation of Natural Language Requirements into Linear Temporal
     Logic with Large Language Models. In 2024 IEEE 24th International Conference on Software Quality, Reliability and Security (QRS). 204–215.
     https://doi.org/10.1109/QRS62785.2024.00029
[92] Rongjie Yan, Chih-Hong Cheng, and Yesheng Chai. 2015. Formal consistency checking over specifications in natural languages. In 2015 Design,
     Automation & Test in Europe Conference & Exhibition (DATE). 1677–1682.
[93] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan J Prenger, and Animashree Anandkumar. 2023.
     LeanDojo: Theorem Proving with Retrieval-Augmented Language Models. In Advances in Neural Information Processing Systems, A. Oh, T. Naumann,
     A. Globerson, K. Saenko, M. Hardt, and S. Levine (Eds.), Vol. 36. Curran Associates, Inc., 21573–21612.
[94] Junyi Yao, Yijiang Liu, Zhen Dong, Mingfei Guo, Helan Hu, Kurt Keutzer, Li Du, Daquan Zhou, and Shanghang Zhang. 2024. PromptCoT: Align
     Prompt Distribution via Adapted Chain-of-Thought. In 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 7027–7037.
     https://doi.org/10.1109/CVPR52733.2024.00671
[95] Xi Ye and Greg Durrett. 2022. The Unreliability of Explanations in Few-shot Prompting for Textual Reasoning. In Advances in Neural Information
     Processing Systems, S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (Eds.), Vol. 35. Curran Associates, Inc., 30378–30392.
[96] Haodi Zhang, Min Cai, Xinhe Zhang, Chen Jason Zhang, Rui Mao, and Kaishun Wu. 2023. Self-Convinced Prompting: Few-Shot Question Answering
     with Repeated Introspection. (2023). arXiv:cs.CL/2310.05035 https://arxiv.org/abs/2310.05035
Working Document - Formalising Software Requirements with Large Language Models                                          17


10    APPENDIX A - SUMMARY TABLES

     Paper   Tool / Framework / Tech- Description
             nique
     [18]    LLM-based Code Verifica- Uses LLMs like GPT-3.5 to verify code by analyzing requirements and
             tion                     explaining whether they are met.
     [17]    nl2spec                          A framework leveraging LLMs to generate formal specifications from
                                              natural language, addressing ambiguity in system requirements with
                                              iterative refinement.
     [73]    Explanation-Refiner              A neuro-symbolic framework integrating LLMs and theorem provers to
                                              formalize and validate explanatory sentences, providing error correction
                                              and feedback for improving NLI models.
     [50]    Not Specified                    Analyzes research directions in software requirement engineering, con-
                                              ducting a SWOT analysis and sharing evaluation findings.
     [5]     Symbolic NLP vs. ChatGPT         Compares the performance of symbolic NLP and ChatGPT in generating
                                              correct JML output from natural language preconditions.
     [4]     Domain Model Extractor           Generates domain models from natural language requirements in an
                                              industrial case study, evaluating accuracy and performance.
     [59]    SpecSyn                          A framework using LLMs for automatic synthesis of software specifica-
                                              tions, improving accuracy by 21% over previous tools.
     [23]    AssertLLM                        A tool generating assertions for hardware verification from design
                                              specifications using three customized LLMs, achieving 89% correctness.
     [30]    Formal Verification         of   Reports on formal verification of NASA’s Node Control Software natural
             NASA’s Software                  language specifications, highlighting errors and lessons learned.
     [54]    SpecLLM                          Explores using LLMs for generating and reviewing VLSI design specifi-
                                              cations, improving chip design documentation.
     [68]    Requirements Specification       Enhanced software requirements specification using constrained natu-
             Language (RSL), ReDSeeDS         ral language and automated transformations into code.
     [31]    ARSENAL Framework and            Automated extraction of requirements specification from natural lan-
             Methodology                      guage with automatic verification.
     [51]    BPM-to-NL         Translation    Generated natural language descriptions from business process models
             Process                          for better validation.
     [61]    Laurel                           A framework to generate Dafny assertions to automate program verifi-
                                              cation process for a SMT solver
                      Table 1. Summary of LLMs related literature: Tools, Frameworks, and Achievements
18                                                         Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


     Paper   Tool / Framework / Tech- Description
             nique
     [61]    Laurel                           A framework to generate Dafny assertions to automate program verifi-
                                              cation process for a SMT solver
     [69]    Controlled Natural Lan- Expressed software requirements in a limited set of natural language
             guage (CL) with ANLT    and translated to logical expressions to detect ambiguities.
     [74]    LLM-based Analysis for           Improved smart grid requirement specifications with GPT-4o and
             Smart Grid Requirements          Claude 3.5 Sonnet, achieving F1-scores between 79% - 94%.
     [91]    NL-to-LTL Translation via        Converted unstructured natural language requirements to NL-LTL pairs,
             LLMs                             achieving 94.4% accuracy on public datasets.
     [81]    ESBMC-AI                         Combined LLMs with Formal Verification to detect and fix software
                                              vulnerabilities with high accuracy.
     [38]    LLM-based Formal Specifi- Translated natural language into formal rules (regex, FOL, LTL) with
             cations Translation       high adaptability and performance.
     [62]    SynVer Framework                 Synthesized and verified C programs using the Verified Software
                                              Toolchain.
     [72]    LLM-based Requirement            Ensured low-level software requirements met high-level requirements,
             Coverage Analysis                achieving 99.7% recall in spotting missing coverage.
     [24]    SAT-LLM                          Integrated SMT solvers with LLMs to improve conflict identification in
                                              requirements; significantly outperformed standalone LLMs in detecting
                                              complex conflicts.
     [21]    NLP for Software Develop- Assessed NLP techniques for various software development stages,
             ment                      highlighting their suitability for generating assertions and processing
                                       developer queries.
     [63]    Req2Spec                         NLP-based tool that formalises natural language requirements for HAN-
                                              FOR; achieved 71% accuracy in formalising 222 automotive require-
                                              ments at BOSCH.
     [36]    RML (Requirements Model- Introduced a conceptual model-based framework ensuring precision,
             ing Language)            consistency, and clarity in requirements writing.
     [22]    GPT-4o for VeriFast Verifi- Evaluated GPT-4o’s ability to generate C program specifications for
             cation                      VeriFast; found that while functional behavior was preserved, verifica-
                                         tion often failed or contained redundancies.
     [66]    NL to Temporal Logic             Developed an automatic translation mechanism from natural language
             Translation                      sentences to temporal logic for formal verification.
                      Table 2. Summary of LLMs related literature: Tools, Frameworks, and Achievements
Working Document - Formalising Software Requirements with Large Language Models                                        19


   Paper    Tool / Framework / Tech- Description
            nique
   [14]     ANTONIO toolkit                 A comprehensive analysis of NLP verification approaches and intro-
                                            duces a structured NLP Verification Pipeline with six key compo-
                                            nents. The work includes identifying gaps in existing methods, propos-
                                            ing novel solutions for improved robustness, extending standard verifi-
                                            ability metrics, and emphasizing the importance of reporting verified
                                            subspace (geometric and semantic) properties for better reliability and
                                            interpretability.
   [89]     Lemur                           Integrated LLMs with automated reasoners for program verification,
                                            defining sound transition rules and demonstrating improved perfor-
                                            mance on benchmark tests.
   [65]     Systematic Review               Conducted a comprehensive review on natural language to formal
                                            specification translation, analyzing research across multiple academic
                                            databases.
   [67]     LLM-based Safety Require- Designed a pipeline using LLMs to refine and decompose safety require-
            ments Pipeline            ments for autonomous vehicles, evaluated through expert assessments
                                      and industrial implementation.
   [92]     Specification Consistency       Ensured consistency between oral and formal specifications, incorporat-
            Framework                       ing time extraction, input-output partitioning, and semantic reasoning,
                                            with positive evaluation results.
   [64]     NLP Tools for TFM               Evaluated six NLP pipelines for Topological Functioning Modelling
                                            (TFM). Found that Stanford CoreNLP, FreeLing, and NLTK performed
                                            best.
   [60]     LLM-based Dafny Task            Used LLMs (GPT-4, PaLM-2) to generate Dafny tasks from MBPP
            Generation                      benchmark using different prompting strategies (context-less, signature,
                                            retrieval-augmented CoT). GPT-4 achieved best results with retrieval-
                                            augmented CoT prompt, producing 153 verified Dafny solutions.
   [93]     LeanDojo & ReProver             Introduced LeanDojo, an open-source toolkit for interacting with the
                                            Lean theorem prover. Developed ReProver, a retrieval-augmented LLM-
                                            based prover that improved theorem proving efficiency. Created a bench-
                                            mark with 98,734 theorems and proofs for testing generalization.
   [47]     Thor and class methods          Introduced a framework named Thor which integrates language models
            named Hammers                   with theorem provers. Hammers are implemented to find the appropri-
                                            ate premises to complete the proofs of conjectures. Datasets used are
                                            PISA and MiniF2F.
   [35]     Not specified                   The work proposes the integration of major formal languages (Dafny,
                                            Ada/SPARK, Frama-C, and KeY), their interactive theorem provers (Coq,
                                            Isabelle/HOL, Lean) with Copilot.
   [56]     Systematic Review               Conducted a comprehensive survey on formal specification and verifica-
                                            tion of autonomous robotic systems in 2018. This is based on literature
                                            available of ten years (2008 - 2018).
   [34]     Symbolic analysis        and    The quality of annotations produced in ACSL format is measured for
            LLMs prompts                    PathCrawler and EVA (tools available in Frama-C). PathCrawler gener-
                                            ated more context-aware annotations while, EVA efficiency improved
                                            having less run-time errors.
                    Table 3. Summary of LLMs related literature: Tools, Frameworks, and Achievements
20                                                      Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


     Paper   Tool / Framework           /   Description
             Methodology Devised
     [76]    Dynamic      Requirements      Proposed a model to improve software quality through verification and
             Traceability Model             validation of functional requirements, addressing scalability for both
                                            small and large projects.
     [77]    Early Phase Traceability       Introduced a model for early development phase traceability and verifi-
             and Verification Model         cation, with enhanced adaptability to requirement changes and impact
                                            analysis.
     [29]    Comprehensive Review           Reviewed software requirements traceability, covering elements, chal-
                                            lenges, techniques, classified approaches, and identified future research
                                            directions.
     [75]    Empirical Analysis with        Conducted an empirical study enforcing requirements completeness,
             Traceability Metrics           introducing traceability metrics and regression analysis to quantify
                                            software quality and reduce defect rates.
     [40]    RETRO                          Developed RETRO, a tool for automating RTM generation, significantly
                                            improving accuracy and efficiency over manual tracing methods.
     [84]    VSM + BTM-GA Hybrid Ap- Proposed a hybrid method for traceability link generation that outper-
             proach                  formed traditional IR techniques, particularly in agile development,
                                     enhancing recall and precision.
     [2]     Trustrace                      Introduced a trust-based traceability recovery approach using mined
                                            repository data, achieving better precision and recall than standard IR
                                            methods.
     [37]    Deep       Learning-Based      Applied deep learning with BI-GRU for traceability, incorporating se-
             Traceability (BI-GRU)          mantic understanding and domain knowledge, outperforming VSM and
                                            LSI methods.
     [6]     Topology-Based      Model- Presented a topology-based, model-driven traceability technique for-
             Driven Approach            malising specifications and establishing trace links between real-world
                                        functions and software artifacts.
     [16]    Event-Based Traceability       Proposed a mechanism to support software evolution through event-
             Mechanism                      based artifact linking, improving change management performance and
                                            maintaining consistency in distributed environments.
     [19]    Tracebok                       Introduced a traceability body of knowledge framework categorising
                                            traceability approaches and offering practical guidance for software
                                            projects.
     [58]    Traceability Visualisation     Reviewed visualisation tools and techniques, identifying issues such as
             Review                         scalability and visual clutter, and suggesting ways to improve traceabil-
                                            ity visualisation.
             Table 4. Summary of Other Sections of Literature Review: Tools, Frameworks, and Methodologies
Working Document - Formalising Software Requirements with Large Language Models                                        21


   Paper    Tool / Framework            /   Description
            Methodology Devised
   [48]     Zero-Shot CoT                   Demonstrated that zero-shot prompts with simple additions like “Let’s
                                            think step by step” can significantly enhance LLM reasoning without
                                            training examples.
   [55]     One-Shot Prompting              Used a single example to guide LLMs in generating desired outputs,
                                            showing potential as an alternative to zero- and few-shot approaches.
   [95]     Few-Shot Evaluation             Found that zero-shot prompting can outperform few-shot setups, chal-
                                            lenging assumptions on example-based prompting.
   [96]     Self-Consistent Few-Shot        Showed that prompting with few examples isn’t always better and
            Prompting                       proposed techniques to refine few-shot reliability.
   [42]     Prompt Engineering Re- Surveyed prompt engineering strategies, including multimodal prompts,
            view                   adversarial prompting, and robustness evaluations.
   [85]     Chain of Thought (CoT)          Proposed stepwise reasoning in prompts to improve LLM performance
                                            in tasks requiring logic, math, and symbolic manipulation.
   [42]     Lost-in-the-Middle              Highlighted LLMs’ U-shaped attention patterns, warning against long
                                            prompts where important middle-context information may be over-
                                            looked.
   [52]     Retrieval Augmented Gen- Introduced a method to retrieve relevant knowledge for augmenting
            eration (RAG)            prompts, enhancing performance on knowledge-intensive tasks.
   [43]     LoRA                            Proposed Low-Rank Adaptation for fine-tuning LLMs efficiently with-
                                            out retraining the entire model, supporting modular adaptability.
   [83]     Iterative Prompting Frame- Proposed a context-aware iterative prompting method for LLMs in
            work                       multi-step reasoning tasks, dynamically synthesizing prompts to im-
                                       prove reasoning accuracy.
   [88]     UTP Tutorial                    Provided an introduction to Unifying Theories of Programming (UTP)
                                            and the use of alphabetised relational calculus to describe imperative
                                            constructs such as Hoare logic and refinement calculus.
   [32]     Institutions                    Introduced institutions as a formal framework for modeling logical sys-
                                            tems, including results on signature gluing and constraints for abstract
                                            data types, contributing to the theory of specification languages.
   [87]     Circus                          Described Circus, a language combining CSP, Z, and imperative pro-
                                            gramming, formalised using UTP to refine concurrent systems.
   [39]     Runtime Verification for        Applied runtime verification in UAS traffic management, using formal
            UAS                             requirements to validate system safety across subsystems, confirmed
                                            via flight simulations.
   [12]     UTP-Based RTEMS Verifica- Verified RTEMS real-time OS using Promela and SPIN, linking UTP
            tion                      semantics for test generation and discussing future directions in space-
                                      grade verification.
             Table 5. Summary of Other Sections of Literature Review: Tools, Frameworks, and Methodologies
22                                                      Arshad Beg, Diarmuid O’Donoghue, and Rosemary Monahan


     Paper   Tool / Framework           /   Description
             Methodology Devised
     [26]    Isabelle/UTP                   Introduced Isabelle/UTP to mechanise UTP semantics, providing formal
                                            proof tools for various paradigms, supporting development of auto-
                                            mated verification tools.
     [46]    UML Testing Profile (UTP)      Discussed use of UML and UTP for model-based testing of embedded
                                            systems, presenting algorithms for test artefact generation under re-
                                            source constraints.
     [27]    Java Model of RTEMS            Presented a verified Java model for RTEMS’s priority inheritance pro-
                                            tocol using Java Pathfinder, fixing known issues like data races and
                                            deadlocks.
             Table 6. Summary of Other Sections of Literature Review: Tools, Frameworks, and Methodologies
