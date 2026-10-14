                                         A framework for assessing the capabilities of code generation of
                                         constraint domain-specific languages with large language models

                                                                                      David Delgado
                                               Universitat Oberta de Catalunya, Rambla del Poblenou, 154-156, Barcelona, 08018, Barcelona, Spain

                                                                                      Lola Burgueño
                                                    ITIS Software, Universidad de Málaga, Avda. Cervantes 2, Málaga, 29071, Málaga, Spain
arXiv:2603.05278v1 [cs.SE] 5 Mar 2026




                                                                                      Robert Clarisó
                                               Universitat Oberta de Catalunya, Rambla del Poblenou, 154-156, Barcelona, 08018, Barcelona, Spain




                                        Abstract
                                        Large language models (LLMs) can be used to support software development tasks, e.g., through
                                        code completion or code generation. However, their effectiveness drops significantly when con-
                                        sidering less popular programming languages such as domain-specific languages (DSLs).
                                            In this paper, we propose a generic framework for evaluating the capabilities of LLMs gener-
                                        ating DSL code from textual specifications. The generated code is assessed from the perspectives
                                        of well-formedness and correctness. This framework is applied to a particular type of DSL, con-
                                        straint languages, focusing our experiments on OCL and Alloy and comparing their results to
                                        those achieved for Python, a popular general-purpose programming language.
                                            Experimental results show that, in general, LLMs have better performance for Python than for
                                        OCL and Alloy. LLMs with smaller context windows such as open-source LLMs may be unable
                                        to generate constraint-related code, as this requires managing both the constraint and the domain
                                        model where it is defined. Moreover, some improvements to the code generation process such
                                        as code repair (asking an LLM to fix incorrect code) or multiple attempts (generating several
                                        candidates for each coding task) can improve the quality of the generated code. Meanwhile,
                                        other decisions like the choice of a prompt template have less impact. All these dimensions
                                        can be systematically analyzed using our evaluation framework, making it possible to decide the
                                        most effective way to set up code generation for a particular type of task.
                                        Keywords: Large language models, Domain-specific languages, framework, code generation,
                                        quality


                                        1. Introduction

                                            Recent advances in generative artificial intelligence (AI), and in particular large language
                                        models (LLMs), have made significant progress towards generating source code from textual
                                        requirements. Such tools can be used to improve developer productivity [1], e.g., integrating code
                                        autocomplete tools in integrated development environments (IDEs). Moreover, they facilitate
the rapid exploration of ideas or the quick creation of prototypes supported by AI tools, e.g., AI
software engineering agents [2] and the notion of vibe coding1 .
    The power of LLMs comes from the vast dataset used in its training phase. As a result, when
it comes to code generation, LLMs are able to extract patterns from a large collection of code
samples, effectively learning the syntax and semantics of programming languages and the rela-
tionships between textual requirements (e.g., comments in source code) and their source code
implementation. Nevertheless, this is only the case for popular general-purpose programming
languages (GPL), such as Python, Java, C or C#, where there is a large collection of samples
publicly available. The performance of LLMs worsens when dealing with low-resource pro-
gramming languages such as domain-specific languages (DSLs) [3]. In these languages, the
number of available code samples is small compared to GPLs. The lack of examples makes the
LLM’s knowledge of the language less precise. Therefore, evaluating the quality of the code
generated by LLMs is critical, especially for DSLs.
    A notable subset of domain-specific languages (DSLs) includes formal constraint and query
languages, such as OCL [4] and Alloy [5]. Unlike natural language, which is inherently am-
biguous and imprecise for specifying system behavior, these languages provide a precise and
formal notation [6]. Thus, they are particularly well-suited for expressing integrity constraints
in software systems, such as invariants, pre-conditions and post-conditions. These constraints
support rigorous verification, validation, and testing. However, these languages create several
unique challenges from the point of view of code generation:
    • They are low-resource programming languages, which makes LLMs perform worse than
      for general-purpose languages.

    • The constraints or queries they define refer to a schema or specification in which the con-
      straint should be checked or enforced. That is, code generation needs to manage two
      different tasks at once: how the schema is provided (or generated) and how the constraints
      use the information therein.
    • They are declarative rather than procedural. Hence, it is not always possible to execute
      them, but they need to be verified or tested against positive and negative samples.
    • Constraints are usually global rather than local. As result, it is harder to consider them in
      isolation, as they may interact among them and cause unintended side-effects. This makes
      it harder to consider requirements individually as sometimes several constraints need to be
      dealt simultaneously to reach a satisfactory solution.

    In this paper, we present a modular framework for assessing LLM-based code generation,
which supports both GPLs and constraint and query DSLs. The framework supports different
prompt styles, prompt augmentation techniques and quality evaluation strategies. This frame-
work enables the exploration of different alternatives for code generation, which allows develop-
ers to identify the best approach to generate code for their particular language. To validate the
effectiveness of our framework, we have instantiated it for two DSLs (Alloy and OCL) and one
GPL (Python). For our experiments, we have collected and curated a set of examples in OCL,


   1 Vibe coding is an approach to software development where the developer collaborates with AI tools to brainstorm,

code, test and debug.


                                                         2
Alloy and Python composed of domain specification plus integrity constraints. We have instan-
tiated our framework and used it to evaluate the code generation capabilities of four different
LLMs, namely DeepSeek-coder, GPT-4o, GPT-4o-mini, and Llama 3.1.
     Specifically, this paper presents the following novel contributions to the field of LLM-based
code generation:
    1. A flexible and highly configurable modular assessment framework for code generation in
       which all relevant decisions about the code generation process (prompt template, LLM,
       use of code generation, use of multiple attempts, . . . ) can be parameterized. In this way,
       it is possible to study the impact of decisions on the code generation process. While other
       works on code generation focus on one or a few dimensions, this framework can adapt
       to diverse code generation scenarios and supports the systematic comparison of multiple
       code generation settings.
    2. A study of the specific challenges surrounding code generation for the constraint languages
       OCL and Alloy, comparing the results to those achieved for general-purpose languages like
       Python, and enriching existing datasets with additional synthetic data.
    3. A set of comprehensive code generation experiments that explores and evaluates all pos-
       sible configurations (more than 90k) for a set of coding tasks in order to select the best
       possible alternative.
    The remainder of this paper is organized as follows. Section 2 presents the necessary back-
ground to contextualize our approach. Section 3 introduces our modular LLM-based evaluation
framework, while Section 4 describes the particular instantiation of the framework that we use
in the experiments in this paper. In Section 5, we illustrate the application of this framework and
assess the quality of the generated code through several experiments. Section 6 discusses related
work in the field, positioning our contribution within the broader research landscape. Finally,
Section 7 concludes the paper and outlines directions for future research.


2. Background

    Since their inception, LLMs have been used for a variety of code-related tasks, such as code
completion (i.e., proposing code snippets that extend a code fragment), automatic test genera-
tion, and generation of code from textual comments. In this paper, we focus on the latter: the
generation of code from textual specifications. In this section, we present the notion of code
generation, how it relates to DSLs and techniques used to improve the performance of LLMs in
this task.

2.1. Code generation
   In the context of software engineering, the term code generation has been used with a variety
of meanings. For instance, in the context of model-based software engineering (MBSE), code
generation usually refers to the translation of a high-level formal specification (a model2 of a


   2 Note that the term “model” is used with different meanings in AI and MBSE. In the AI field, a model is a mathemat-

ical representation of the patterns learned from a dataset, e.g., a trained neural network or a statistical model. Meanwhile,
in MBSE a model is an abstraction of a system or software artifact. In this paper, we use a particular type of software
model, which we call interchangeably domain or conceptual model. To avoid confusion, each time we talk about an AI
model, we will refer to it with a precise name, e.g., AI model, machine learning model, language modelor LLM

                                                             3
software system) into low-level executable code. In this scenario, the formal nature of the input
notation enables the use of dedicated model transformation and templates, which use a com-
bination of patterns and rules to match elements in the original specification and declare their
intended translation.
    On the other hand, code generation consists in the creation of source code from a flexible
high-level description in natural language or partial code snippets [7]. This is the definition
of code generation that we adopt in this paper. This type of code generation helps translate
human intent into machine-executable code, allowing developers to quickly prototype, automate
repetitive tasks, and even generate complex software systems.
    Code generation has undergone a significant transformation since the appearance of LLMs,
achieving remarkable capabilities in understanding and generating code in various programming
languages [7, 1]. LLMs are already pre-trained with a vast amount of data, including code written
in several programming languages and even DSLs. Consequently, there is no need to train them
to achieve positive results in code generation tasks. However, not every language is equally
represented in the pre-training dataset of an LLM, making the effectiveness and quality of code
generation with LLMs language-dependent.

2.2. Low-resource programming languages and DSLs
     The effectiveness of AI methods based on machine learning depends on the quality and quan-
tity of data available for training. Having less data or worse data reduces the quality of the pat-
terns discovered in the learning process: they may be incorrect, e.g., assume a particular case can
be generalized; or incomplete, e.g., they may fail to include unusual corner cases.
     In the context of natural language processing, such as in machine translation, languages are
typically classified as high resource if there are many publicly available high-quality samples that
can be used for training purposes, and low resource if there are only a few. In code generation,
this problem is also discussed as the high, low, and very low resource programming languages
problem [8, 9, 10, 11, 3, 12]. Popular general-purpose languages tend be high resource, while
DSLs tend to be at the lower end of these classifications, with few available examples. The
scarcer the data about a language, the more difficult it is for an LLM to generate code that follows
the syntax and semantics of the language and implements the input specification faithfully.
     DSLs present additional challenges in code generation with LLMs, making it even more
necessary to adjust the code generation process. First, there is a lack of benchmarks [12] and
training datasets [13, 14], which makes it challenging even to generate code that can be success-
fully parsed. Moreover, there are fewer tools available for code evaluation, making it necessary
to create language-specific tools to check if the generated code achieves the intended goals.

2.2.1. Prompt engineering
    Prompting is a primary method for interacting with LLMs. With this technique, the user in-
puts a set of instructions in natural language (the prompt), asking the LLM to generate a response
that aligns with the given information.
    The construction of effective prompts, called prompt engineering, is a rapidly evolving field
of study. There are many different prompt engineering techniques, some of which can be applied
to any kind of task and others which are specific to particular tasks. Nevertheless, not every
technique works for every use case and not every technique works with any LLM size [15].
There are several techniques that are worth mentioning in the context of this paper:


                                                 4
   • Chain of Thought (CoT) is used to deal with complex tasks by decomposing them into
     simpler steps to guide the LLM [16]. The entire reasoning process occurs within a single
     prompt, and the LLM generates the entire chain of reasoning in one go.
   • Iterative prompting (or dialogue-based prompting, or conversational prompting) consist of
     prompting the LLM, receiving the response and incorporating it into the context of a new
     prompt. In this case, the reasoning spreads across multiple interactions and may involve
     external interactions (such as a tool invokation) and decision-making.
    Prompt augmentation, also called context engineering, is used to provide more information
or context to a base prompt. This additional information is always relevant to the task at hand and
helps the LLM improve the quality of its response [15]. An example of relevant context in the
context of this paper would be the description of the domain where the constraints are defined.
    Although prompt augmentation is limited by the maximum context window size of LLMs,
this shortcoming can be avoided by carefully selecting which information is provided as con-
text. That is, considering the task being addressed and the prompt, we select the subset of frag-
ments from the context that is relevant from our particular task. This technique, called retrieval-
augmented generation (RAG) has been used to help the LLM adhere to the grammar of a specific
target language, to improve the its ability to generate code that is syntactically valid [17].
    At the same time, LLMs are in-context learners, this is, they demonstrate the ability to ac-
quire new skills directly from prompt interactions, particularly through a limited number of ex-
amples [18]. This capability allows us to define a new classification and categorize prompting
strategies depending on the number of examples provided within the prompt: zero-shot prompt-
ing, where the LLM performs a code task without any explicit examples, and few-shot prompting,
where the LLM learns from a small set of examples included in the prompt.

2.3. Evaluation of generated code
    LLMs can produce code that is not syntactically valid or that does not accurately implement
the provided requirements. Thus, it is important to assess the quality and suitability of the gen-
erated code. There are different ways to evaluate LLM-produced code. In this sub-section, we
discuss the most relevant approaches and, particularly, those used in the remainder of this paper.
    A straight-forward way to evaluate generated code is its manual inspection carried out by hu-
man experts. Unfortunately, manual inspection can be very time-consuming. LLMs can generate
code much faster than its manual review takes. As a result, manual inspection is not feasible in
scenarios where code generation is used intensively or in large software systems. To address this
challenge, automated evaluation metrics have been proposed.
    Automatic code evaluation can be split into two sub-groups: (1) assessing whether the code
is syntactically and semantically valid in the given programming language (i.e., the code is well-
formed), and (2) assessing whether the generated code fulfills the intended functionality as spec-
ified by the user (i.e., the code is correct).
    A piece of code is considered syntactically valid or well-formed when it follows the ba-
sic structural and syntactic rules of the language, i.e., it can be parsed without errors. Well-
formedness can be evaluated using a parser for the target language.
    Moreover, a piece of code is considered semantically valid when it is well-formed and con-
forms to specific semantic rules, e.g., not allowing the use of undefined variables. Semantic
validation can be evaluated by using a semantic analyzer, which is usually part of the language
compiler. Nevertheless, it is often assessed implicitly by code execution [7, 19]. As a conse-
quence, it is usually a part of correctness evaluation, which also involves code execution.
                                                  5
                                                                       PARAMETERS



                   Delivery     Target    Prompt     Number of     LLM                   Code                  Code
                   strategy   language   template     attempts   selection              repair?               repair?




       INPUT                                                                                                                    OUTPUT



                                                                                                                          YES
     Code task                                                                                                                     Code



      Domain                   Build     Prompt(s)   Generate        Code           Well-formedness   YES
                                                                                                            Correctness
     description              prompt                  code                                check                check

                                                                                                      NO
                                A                       B                                 C                     D
    Domain model                                                                                                          NO




        Figure 1: Graphical representation of the framework as a flow diagram, including labeled components.



     Correctness is the term used to evaluate whether a piece of code meets the intended specifica-
tion [19, 20]. One strategy to assess correctness is considering it a matching problem: look for an
exact match of the generated code with a provided solution that it is known as correct. However,
this approach has limited applicability due to the expressiveness of programming languages:
there are many different ways to write code that has exactly the same behavior. The number of
alternative solutions to a coding task is so large that in practice it is impractical to assess cor-
rectness by looking for matches against a reference solution [21]. A similar problem appears if,
instead of using exact matches, we rely on similarity metrics from natural language processing
such as BLEU or ROUGE [20]. Again, these approaches are adequate for machine translation
and text summarization, but are inadequate for code evaluation [22, 23], due the expressiveness
of programming languages.
     Another strategy is assessing functional correctness by means of unit tests [7, 24]. In this
approach, the generated code is considered correct only if it passes the unit tests. Moreover,
functional correctness is assessed predominantly using two metrics: accuracy and pass@k [19,
25]. Accuracy measures the number of times that generated code is correct in the first attempt.
On the other hand, pass@k measures the likelihood that at least one of the k generated code
samples achieves functional correctness [26]. This metric not only indicates how often the model
succeeds in the first attempt, considering that pass@1 is equal to accuracy, but also highlights
the potential benefit of multiple generation attempts [19].
     Last but not least, large language models have been recently integrated into evaluation pro-
cesses, leading to the emergence of the “LLM-as-a-judge” paradigm [27], an evaluation approach
that is explainable, scalable, and very aligned with human preferences [28]. In this approach,
LLMs are assessed for their ability to evaluate and interpret certain outputs. For example, spe-
cific frameworks have been developed to test LLMs’ capabilities in code evaluation and compre-
hension [29].


3. A modular framework for LLM-based code generation evaluation

    This section presents the architecture and components of our proposed framework. This
framework supports the customization of a code generation process, its execution using the se-
lected prompts and LLMs and the evaluation of the generated code.

                                                                             6
    Figure 1 presents the functional flow, artifacts and tools of our proposed framework. In all the
Figures in this Section, gray boxes represent an action, orange boxes represent software artifacts,
and white shapes represent data and parameters.
    The inputs to our framework are: (1) the code task, which is a natural language description
of the specification(s) or query(ies) to be implemented; (2) the domain description, using natural
language to characterize the relevant features of the domain where the constraint will be evalu-
ated; and (3) the domain model, providing a formal description of the domain using a modeling
notation. This framework is very flexible in terms of the inputs to the code generation process: it
can operate using only the domain description, only the domain model, or both. This flexibility
supports different code generation scenarios.
    Our framework also considers diverse prompting strategies, prompt augmentation techniques
and evaluation metrics, offering an automatic evaluation of the quality of their outputs. These
parameters can be specified by the user before generating code, allowing the evaluation and
comparison of multiple customized versions of the code generation process.
    This framework is organized around four main stages: building the prompt or prompts used
to generate code (block A in Figure 1, described in Section 3.1); providing the prompts to the
LLM and extracting the generated code (block B in Figure 1, described in Section 3.2); checking
the well-formedness of the generated code (block C in Figure 1, described in Section 3.3); and,
for code snippets that are well-formed, checking their correctness (block D in Figure 1, described
in Section 3.4).
    In the following subsections, we describe the main stages of the framework in the order in
which they are applied.

3.1. Building code generation prompts
    Given the inputs, our framework builds different prompts following a set of predefined prompt
templates. Each prompt template exploits different prompting strategies with the goal to guide
the LLM towards the generation of an appropriate output.
    We define prompting templates that, in order to provide context and guidance to the LLM,
operate on two key and orthogonal dimensions:
   1. Augmentation: This dimension leverages Chain of Reasoning (CoR) strategies, which en-
      courage iterative prompting, helping the model achieve a deeper understanding of the task
      at hand and improving the quality of the generated code.
   2. Task-Oriented Prompting: This dimension focuses on designing prompts that accommo-
      date multiple tasks within the same domain, ensuring clarity and precision in guiding the
      LLM.
    The basic prompt construct in our system is a single instruction. Considering that our goal
is to evaluate the generation of code for constraints / invariant specifications in a DSL3 , this
construct is structured as: “Code the following constraint in {LANGUAGE}:”, followed
by the coding task provided as input (e.g., “the number of employees of the company must be less
than or equal to 50”). Then, this prompt construct is systematically augmented with additional
information to enhance its effectiveness.
    Given the characteristics of the code to be generated, our framework incorporates specific el-
ements as part of this augmentation process. These elements, supplied as input to the framework,

  3 Note that our framework would also work for GPLs.

                                                        7
may include a detailed description of the domain and the domain model itself. The domain model
can be formalized in a DSL such as PlantUML or described in natural language. Each template
used in the system is designed to evaluate how different combinations of augmentations impact
the overall performance of the prompt.
    Our framework also supports the option in which the LLM is asked to generate information
to enrich the prompt in two different ways: (1) given the inputs, we ask the LLM to explain that
domain model; the explanation generated is provided in a subsequent prompt where we request
the LLM to solve the coding task; (2) given the inputs, we ask the LLM to generate a domain
model either in natural language or following the syntax of a specific DSL (e.g., PlantUML).
Then, that output is used to enrich the following prompt where we request the coding task to be
solved.
                                       Table 1: Prompting templates.


         PT    Domain Description      Domain Model        Explain DM     Code DM      Prompts
         PT1             ✓                                                                   1
         PT2                               Formal                                            1
         PT3                                NL                                               1
         PT4                               Formal                ✓                           2
         PT5                                NL                   ✓                           2
         PT6             ✓                                                  NL               2
         PT7             ✓                                                 Formal            2
         PT8             ✓                 Formal                                            1
         PT9             ✓                  NL                                               1


    Table 1 illustrates the combination of these augmentations and the nine prompting templates
(PT) included in our framework. The prompts are constructed by concatenating the augmentation
components outlined in the table in JSON format. For instance, considering the use case of a DSL
for the specification of invariants, we would supply the following file to the LLM:
[
    {
         "role": "user",
         "content": "Consider the context description of the domain: {DOMAIN DESCRIPTION}"
    },
    {
         "role": "user",
         "content": "Code the following constraint in {LANGUAGE}:
         {CODING TASK}"
    }
]


    The input to our framework may also involve several closely related coding tasks, such as
generating code for several invariants or constraints in the same domain. The second dimension
(Task-Oriented Prompting) focuses on how tasks are presented to the LLM when dealing with
multiple related tasks within the same domain. A collection of tasks can be delivered to the LLM
in the following ways:
    1. OP1: Batch delivery. All tasks are presented in the same prompt at once as a list. The
       expected LLM behavior is that it generates an output that contains a list with the result for
       each task.
                                                    8
   2. OP2: Chained sequential delivery. Tasks are presented one by one, and the outputs of
      earlier tasks are incrementally added to the context of subsequent tasks. Note that this
      requires multiple prompts. For example, the third coding task will receive the output of
      the first and second tasks as part of its input prompt, but not the results from the fourth
      task.
   3. OP3: Isolated delivery. Each task is prompted independently without knowledge of other
      tasks, focusing on a single, isolated response per task. The output consist of a single coding
      sample.

3.2. Code generation and extraction
    In this stage, the input coding tasks that are provided are used to build different prompts using
the prompting templates described in the previous Section. These are used to prompt the LLM,
producing an output that consists of usually some natural language (NL) description of the code
plus the code requested.
    The user may also request multiple attempts of code generation for the same task. Given
that LLMs are not deterministic, each attempt will produce similar code snippets with slight
variations among them. Using multiple attempts increases the cost of the code generation process
(k attempts means k calls to the LLM), but it also increases the likelihood that one of the generated
versions is well-formed and correct (see Section 5.3.5).
    The LLM’s output is processed to extract the generated code. If the prompt contained multi-
ple coding tasks, the response is expected to contain an output for each task hence an additional
splitting step is required to isolate and extract individual code snippets.
    In our implementation of the framework, this stage is designed to be highly modular. The
inputs (i.e., datasets consisting on code tasks, domain description(s) and domain model(s)) are in-
dependent of the framework. The LLM component used in the framework can be easily replaced,
allowing for the code generation evaluation of various LLMs (e.g., GPT-4, Llama, custom fine-
tuned models) without altering the overall framework. Similarly, the prompting templates are
designed to be extensible, supporting diverse prompting strategies and future extensions.

3.3. Well-formedness evaluation
    Once we have generated code for the target coding task, the first step is to verify the well-
formedness of the generated code. A code snippet is considered well-formed when it follows the
syntactic rules of the language it is generated. This check is performed using a well-formedness
validator, such as a parser or compiler of the language.
    Our implementation enables the use of different parsers, compilers, or validation tools de-
pending on the target language. This flexibility also applies to the framework capability to inte-
grate different target languages by plugging in the appropriate well-formedness tools. Depending
on the tool used to perform the well-formedness check, it is possible to be assessing the syntactic
validity but also semantic correctness at the same time.
    Code snippets that fail the well-formedness check undergo a single-pass code repair process4 .
The error message generated by the well-formedness assertion tool together with the faulty code,
is used as input to the code repair process. Figure 2 illustrates the process, which leverages
Chain-of-Thought (CoT) reasoning. First, it provides the faulty code and the error message to

   4 A single-pass or 1-pass code repair typically refers to a code fixing process that involves making corrections or

improvements to source code in a single pass – that is, reviewing and editing the code only once.
                                                          9
an LLM. Using this information, the LLM generates an explanation of the error. Then, this
explanation is used by a second LLM to generate a new version of the code, where hopefully the
error has been fixed. Note that, given the use of CoT, in Figure 2, the orange boxes represent two
distinct LLMs. However, this process could also be performed using a single LLM and a single
prompt. Finally, the repaired code undergoes a well-formedness evaluation, as outlined in the
previous step.
    As previously mentioned, we are only performing a single round (or single-pass) of code
repair: if the well-formedness validation fails after repair, the coding task is considered failed,
without additional rounds of code repair. This is why there is no loop in Figures 1 and 2 if the
final well-formedness check fails.
                                YES                                                                                                      Well-formed
                                                                                                                                                code

                                                                                                                              YES
                               NO
   Code      Well-formedness                  Code
                 validator                                                                    Fixed
                                                                           Error
                                                              LLM                      LLM            Well-formedness
                                                                        Explanation           code
                                            Parser          Feedback                   Code               validator             NO
                                          feedback


                                                                       CODE REPAIR




Figure 2: Well-formedness checking process diagram (component C in Figure 1), detailing the well-formedness valida-
tion and the well-formedness code repair flow.



3.4. Correctness evaluation
    If a code snippet is well-formed, it can proceed to the following evaluation stage: the correct-
ness check. A code snippet is considered correct when it is executable (that is, it is syntactically
and semantically correct) and complies with the natural language specification for the target
coding task.
    Similarly to the well-formedness stage, the correctness validator is designed as a plug-and-
play component. This allows for the integration of various verification methods, such as unit test-
ing frameworks (e.g., AUnit for Alloy), formal verification tools, or custom correctness checkers,
depending on the requirements of the specific language and code task.
    Code snippets that fail the correctness check undergo a single-pass code repair process, which
implies that code repair occurs only once. The process is shown in Figure 3: the error messages
/ feedback from the correctness validator, along with the faulty code is provided as input to the
LLM. The LLM then generates a fixed version of the code, which is sent back for correctness
check. Similarly to what happens in well-formedness repair, we only perform a single round of
code repair, so the process ends if the final correctness check fails.

                                    YES
    Code        Correctness                                                                                                                 Code
                 validator


                                                                                                                        YES
                                    NO
                                                     Code
                                                                                              Fixed                                 NO
                                                                                LLM                    Correctness
                                                                                              code
                                                                                Code                    validator
                                                 Error
                                               feedback

                                                                           CODE REPAIR



Figure 3: Correctness checking process diagram (component D in Figure 1), detailing the flow between the correctness
validator (see Figure 4) and the correctness code repair process.

                                                                              10
    While the notion of correctness we are using is binary (either a code snippet is correct or not),
when we are considering multiple code generation attempts there are different ways to measure
the success of code generation. In the following, we describe the two metrics that we use in the
experiments in this paper: pass@k and accuracy.

Pass@k. When using multiple code generation attempts, pass@k evaluates the probability that
at least one of the k generated samples is correct. Formula 1 shows how pass@k is calculated,
considering that n represents the total number of input examples, c represents the number of
correct samples, k is them number of samples selected, and C is a combination function. By
computing the probability that all selected samples are incorrect and subtracting that from 1, we
obtain the probability that at least one is correct.
                                                    C(n − c, k)
                                    pass@k = 1 −                                                 (1)
                                                     C(n, k)
Accuracy. Accuracy measures the number of times in which the generated code is correct in the
first attempt. The formula of accuracy is shown in the equation 2.
     Note that both pass@k and accuracy are related as accuracy is equal to pass@1, when k = 1.
                                         correct examples
                       accuracy =                             = pass@1                           (2)
                                    total number o f examples

4. Framework instantiation
    To assess the effectiveness of our approach, we have applied it to two DSLs for constraint
languages: OCL and Alloy. Our framework supports any language. For the sake of comparison
between low-resource and high-resource languages, we have also applied it to assess one general-
purpose language: Python. In the following, we explain the instantiation of our framework to
these languages.
    The well-formedness and correctness validators are language-specific. In this section, we ex-
plain the tools and approaches we have used to evaluate both the well-formedness and correctness
of these three languages.

4.1. Well-formedness evaluation
    We have implemented two distinct approaches for the evaluation of well-formedness:
   1. Automatic syntactic validation: This approach employs parser implementations derived
      from existing grammar repositories, specifically the ANTLR grammars for OCL, Alloy,
      and Python available at [30], [31] and [32]. These parsers are used to verify the syntactic
      correctness of the code. A piece of code is deemed well-formed if the parser completes
      without reporting syntax errors.
   2. Manual validation via tool execution: This is complementary to the automatic syntactic
      validation. In this case, the code is executed within dedicated environments (USE OCL
      for OCL, Alloy Analyzer for Alloy) and Python interpreters, which are used to manually
      validate the well-formedness of inputs through dynamic compilation and execution. This
      manual inspection involves reviewing the error messages produced by these tools during
      execution to determine well-formedness. This manual validation captures errors that may
      not be captured by syntactic parsing alone because the tool execution also performs a
      semantic validation.
                                               11
                 Code task
                                                                                  YES         Code
                                                               Correctness
             Domain description                                assessment
                                              LLM               feedback
                                                                                  NO



                 Code to be              CORRECTNESS
                 evaluated                VALIDATION




      Figure 4: Correctness validator. Overview of the validation process via our LLM-as-a-judge framework.



4.2. Correctness evaluation
    To assess the correctness of the generated code we used the following approaches:
   1. Automatic evaluation employing an LLM-as-a-Judge [33]: This approach leverages a large
      language model to automatically evaluate whether the generated code meets the expected
      correctness criteria. We used the same LLM (GPT-4o-mini) to assess every correctness
      evaluation for every target language, to obtain comparable results.
      We have implemented LLM-as-a-Judge as described in Figure 4. The LLM evaluates the
      correctness of a generated piece of code (code to be evaluated) using the inputs coding
      task specification in natural language and domain description. If the generated code is
      incorrect, the correctness assessment feedback is sent to the correctness code repair phase.
   2. Manual evaluation based on specification fulfilment: In this approach, a human evaluator
      manually assesses whether the generated code satisfies the intended requirements, either
      by verifying adherence to the input specification or by confirming that the code correctly
      implements the specified constraint.

4.3. Practical considerations
Language-specific guidelines. Since this paper puts the focus on constraints / invariants, it is
worth mentioning that some languages can describe a given constraint in many alternative ways.
In order to facilitate the analysis of the generated code (e.g., to make it easier to locate the gener-
ated constraints inside the fragment of generated code), we provide language-specific instructions
to guide how constraints should be described:

    • Python: We instruct the LLM to generate one function per constraint, returning a boolean
      value indicating whether the constraint is satisfied. This restriction is necessary because
      Python is a general-purpose language. As a result, without any guidance, the LLM tends
      to generate entire program fragments implementing the constraint rather than a concise
      constraint checker, resulting in heterogeneous and non-comparable outputs.
    • Alloy: We request the LLM to generate each constraint as a single and unique fact. Alloy
      also offers multiple constructs capable of expressing constraints (e.g., facts, predicates and
      assertions), and our initial experiments showed a diversity of structural variations. Stan-
      dardizing constraints as facts ensures consistency across examples and aligns the Alloy
      representation with those produced in Python and OCL.


                                                      12
   • OCL: No language-specific guideline is needed. OCL is designed explicitly as a constraint
     specification language, and invariants are expressed using a dedicated grammatical con-
     struct (context <Classifier> inv <Name>: <Expression>). Because the language has a
     canonical form for invariants, the LLM consistently generated constraints in the expected
     form without additional instructions. Consequently, constraints in OCL are naturally uni-
     form and require no further guidance.

Large Language Models. The framework is designed to be model-agnostic and does not de-
pend on a specific LLM provider or API. It supports a modular architecture that allows for the
integration of multiple language models through adapter components, enabling straightforward
substitution or comparison of different LLMs. In this work, we have implemented and tested the
framework using four models: DeepSeek Coder 6.7B, Llama 3.1, GPT-4o, and GPT-4o-mini.
When generating multiple attempts, in order to ensure non-deterministic behavior, we have to set
the temperature parameter of the LLM to a value that enables some degree of flexibility in the
outputs. For the experiments in this paper, we have used a temperature of 0.3, which introduces
a mild stochasticity in the generated code, while avoiding outputs that are repetitive and less
representative of the model’s behavior in practice.

Context window. LLMs are constrained by the size of their context windows. For instance, GPT-
4o supports up to 128,000 tokens, which is substantially larger than the context window available
in smaller models, such as DeepSeek Coder 6.7B. If a prompting strategy involves a domain
model of significant size, it is very likely that the resulting prompt will exceed the context window
of the evaluated LLMs. One commonly used technique to address such scenarios is retrieval-
augmented generation (RAG) [13]. However, this framework does not currently implement or
rely on RAG.

Replicability package. Our implementation of the framework, together with all the experiments
reported in the following section, is available on our Github repository [34].


5. Validation

    In this section, we describe the experiments performed to assess the feasibility of our frame-
work when studying the effectiveness of LLMs for code generation tasks. In Section 5.1, we
present an initial experiment to assess the performance of our code evaluator. In Section 5.2,
we describe the datasets used in our experiments. Using the instantiation and implementation of
our framework and these datasets, we study the different factors that may impact the quality of
the generated code. These are: target language (Section 5.3.1); choice of LLM (Section 5.3.2);
prompt delivery approach (Section 5.3.3); task delivery approach (Section 5.3.4); and code re-
pair (Section 5.3.5). We conclude by discussing the results and key takeaways in Section 5.4 and
discussing threats to validity in Section 5.5.

5.1. Manual vs automatic evaluation
    Our framework compares multiple strategies to generate code, considering different LLMs,
prompt delivery strategies, use of code repair, . . . However, the sheer number of combinations
quickly makes it impossible to use human evaluation to compare all the generated code snippets.
Thus, it is necessary to use techniques for automatic code evaluation. As discussed in Section 2.3,
this evaluation should not consist of measuring the similarity with respect to a gold-standard
                                                 13
reference solution, as this does not properly consider valid alternative implementations of the
same constraint [35, 36]. Instead, we should focus on assessing how faithfully the invariant
implements the intended constraint.
    In this section, we discuss the approaches that we have used to automatically assess the well-
formedness and correctness of the generated code. Given that the evaluation step is critical for
our experiments, we will measure the quality of this automatic evaluation, comparing it to a
manual evaluation performed by a human expert.

Manual evaluation. The manual evaluation has covered 1,512 code snippets: 56 coding tasks,
generated with 9 different prompt templates for 3 target languages: OCL, Alloy and Python. The
protocol used for the manual evaluation has been the following. One author (a PhD candidate
with experience in model-driven engineering and AI) has inspected the code snippets, identifying
representative examples and common problems. These examples have been discussed among all
three co-authors to identify common evaluation criteria, some of which are language-specific.
For example, the use of non-existing libraries in OCL in the generated code (e.g., a Date type) has
been considered a correctness problem; similarly, in Alloy any incorrect usage of multiplicities
(such as one or lone) or the subset operator in has been considered a correctness problem rather
than a well-formedness issue. Using this set of criteria, the manual evaluation of the examples
was carried out by the same author that selected the initial set of samples.
    Well-formedness has been checked in two stages. First, an ANTLR parser for the target lan-
guage has been used to identify whether the code is syntactically correct. Then, all code snippets
that are syntactically correct have been validated on an analysis or execution environment for the
target language: the UML-based Specification Environment (USE) for OCL, the Alloy Analyzer
for Alloy and a Python 3.9 interpreter for Python. These tools can identify semantic errors such
as type errors or naming problems. If the corresponding tool is able to read the code snippet
without errors, the code is deemed well-formed.
    Correctness has been checked only on well-formed code snippets. This step has been per-
formed manually, with the assistance of the previously mentioned analysis and execution tools.
For instance, in some of the more complex constraints, we have populated the domain models to
inspect the effect of the generated constraints.

Automatic evaluation. We have assessed the performance of GPT-4o-mini, DeepSeek3.1, o3,
and Llama-3.3-70B as the LLM judges by comparing its validation results with the results of the
manual evaluation. To evaluate how well the generated code aligns with our manual evalua-
tion, we frame the problem as a binary classification problem, i.e., the code is either correct or
incorrect.

Measuring the quality of an evaluation. Although accuracy is usually used to study the quality
of AI models, it requires a balanced dataset. Otherwise, it can give a false sense of model
performance by favoring the majority class. Since this is not the case in our experiments (cf.
Section 5.2), we use precision and recall as our primary evaluation metrics.
    Precision is the proportion of true positives among all positive predictions. Equation 3
presents the formula, in which TP (true positives) are code fragments marked as correct by both
the manual evaluation and the automatic check. FP (false positives) are code fragments marked
as correct by the automatic check but incorrect according to the manual evaluation.
                                     | code considered correct by both (TP) |
              Precision =                                                                      (3)
                            | code considered correct by automatic eval. (TP + FP) |
                                                 14
    Recall is calculated as the ratio given by dividing the number of fragments of code marked as
correct by both human and automatic evaluation (TP) by the number of fragments of code marked
correct by the human (TP + FN). Equation 4 presents the formula, where FN (false negatives)
are code fragments marked as incorrect by the automatic evaluation but marked correct by the
manual evaluation.
                                   | code marked as correct by both (TP) |
                   Recall =                                                                    (4)
                              | code considered correct by human (TP + FN) |
Discussion of the results. Table 2 compares the results of 4 LLM-based judges: GPT-4o-mini,
DeepSeek, o3, and Llama-3.3. Overall, all models achieve comparable performance, with pre-
cision and recall typically ranging between 0.7 and 0.85. However, notable differences emerge
across languages. In Python, o3 exhibits a larger gap between precision and recall, indicating
a tendency to overestimate correctness relative to GPT-4o-mini, which shows a more balanced
trade-off. In contrast, Llama-3.3 demonstrates both higher precision and recall for Python, re-
sulting in the most balanced performance among the evaluated judges for this language. For
Alloy and OCL, the differences between judges are smaller, though DeepSeek consistently at-
tains higher recall, suggesting a more permissive evaluation strategy.
    Moreover, these results show a disagreement around 15-30% in precision and recall for the
best models. It should be noted that in complex AI/ML tasks such as machine translation or
code generation, some level of disagreement is expected even among human experts [37]. For
instance, [36] reports Pearson correlations between human annotators ranging from 0.7 to 0.9
when rating code commit descriptions, indicating strong but imperfect agreement. Similarly, [28]
shows that strong LLM judges such as GPT-4 achieve high alignment with human preferences
on MT-bench and Chatbot Arena benchmarks, including coding tasks, with 85% agreement be-
tween GPT-4 and humans—exceeding the 81% agreement observed among humans themselves.
These results suggest that discrepancies between LLM-as-a-judge evaluations and human solu-
tions largely reflect the inherent variability of human judgment rather than deficiencies in auto-
mated evaluation.
    Overall, the results indicate that LLM-as-a-judge approaches provide a reliable approxima-
tion of human correctness judgments, with no single model uniformly dominating across all
languages and metrics. For GPT-4o-mini and Llama-3.3, the precision and recall values are
similar. This suggests that automatic evaluation neither substantially overestimates correctness
nor misses many correct solutions. That is, errors are spread equally among false positives and
negatives, supporting the robustness of LLM-based judging in this setting.
    It is worth mentioning that the concrete values of precision and recall for well-formedness
are lower due to the way in which the evaluations have been performed. The automatic eval-
uation of well-formedness implemented in the framework relies solely on a parser and checks
only syntactic correctness, whereas the manual evaluation was performed by executing the code,
therefore it considers both syntax and semantics (i.e., conformance to the domain model). As
such, the manual evaluation is stricter, which creates some discrepancies.
    To provide further details about automatic evaluation, Figure 5 presents two confusion ma-
trices. The left one illustrates the alignment of our parser-based automatic evaluation of well-
formedness with a human expert evaluation. Meanwhile, the second matrix (right) illustrates
the alignment between manual evaluation and the LLM-as-a-judge assessment in the case of



                                               15
Table 2: Performance of automatic code evaluation for determining well-formedness and correctness across different
LLMs


                                  Well-formedness                                            Correctness
                 Language        Precision        Recall   GPT-4o-mini                 DeepSeek                   o3                 Llama-3.3
                                                           Prec.   Rec.          Prec.       Rec.         Prec.        Rec.     Prec.      Rec.
                 Alloy               0.574        0.504    0.763   0.798         0.814      0.843         0.809        0.819    0.754      0.762
                 OCL                 0.786        0.853    0.696   0.688         0.664      0.799         0.706        0.826    0.717      0.731
                 Python              1.000        1.000    0.770   0.834         0.571      0.857         0.611        0.849    0.774      0.859




                                Well-formedness                                                              Correctness
                                                                                                                                                   500
                                                                   700
                                                                                                                                                   450
                                                                   600
         YES              83                       76                                 YES           220                        147                 400

                                                                   500
                                                                                                                                                   350
MANUAL




                                                                             MANUAL
                                                                     Count




                                                                                                                                                     Count




                                                                   400                                                                             300


                                                                   300                                                                             250

         NO               71                       750                                NO            109                        504                 200
                                                                   200

                                                                                                                                                   150
                                                                   100
                          YES                      NO                                               YES                        NO
                                    AUTO                                                                          AUTO


               Figure 5: Confusion matrices for well-formedness and correctness using GPT-4o-mini as the LLM judge.




                                                                           16
correctness.5 In both matrices, rows represent the manual evaluation outcomes, while columns
indicate the result of our automatic check of well-formedness or correctness. The top-left cell
(true positives) counts cases where both manual evaluation and the automatic check agree that
the criterion is met (it passes the check). The top-right cell (false negatives) records instances
where the manual evaluation decides that the criterion is met, but the automatic check disagrees.
The bottom-left cell (false positives) represents cases where the manual evaluation indicates that
the criterion is not met, but the automatic check suggests otherwise. Lastly, the bottom-right cell
(true negatives) captures cases where both manual evaluation and the automatic check agree that
the criterion is not met (it does not pass the check).
    True positives and negatives dominate these confusion matrices, reflecting the high levels
of agreement that were previously discussed. In conclusion, even if the proposed automated
evaluation strategy is not perfect, it achieves a reasonable degree of precision. Thanks to it, we
have been able to evaluate thousands of code generation tasks using several combinations of code
generation strategies, which would have been impossible to do manually. Section 5.3 provides a
detailed description of the experiments performed and the variables being studied.

5.2. Datasets used in the experiments
    For the evaluation of the framework we have employed two datasets adapted from prior
studies [14, 13] to cover a wide range of constraint scenarios, ensuring broad applicability. It is
worth noting that the dataset in [13] is not fully used due to problems which are unrelated to our
framework itself, such as exceeding the limit of the context window size of the particular LLMs
that we have selected for evaluation.
    Unfortunately, all the datasets that fit our purpose and were considered lack domain descrip-
tions in natural language. To enrich them with the descriptions, we have followed the process
illustrated in Figure 6. From the original dataset, we have extracted the domain model, coding
tasks, and code solutions. Then, using an LLM independent of those used for evaluation (in our
case, Google Gemini 2.5 Pro), we have synthetically generated domain descriptions. There were
a total of 30 domains (15 per dataset) where the generation of a domain description was neces-
sary. The prompt6 that requests a domain description includes the PlantUML model in textual
format as well as the set of constraints in the model.
    The datasets being used were originally designed for the evaluation of generated OCL code.
To this end, they provide a reference solution for each of the constraints in OCL. However, they
do not provide reference solutions for other languages such as Alloy or Python. As mentioned in
Section 5.1, this not an issue as we will be using LLM-as-a-judge rather than a NLP score that
compares generated solution with a gold-standard reference solution.
    Table 3 summarizes the characteristics of the domain models used in the experiments: the
number of models in each dataset and the total number of classes, associations, and integrity
constraints. Moreover, for each of these elements, we report the average length (in words) of
its description in textual format. In the case of class diagrams, they can be described using
natural language or a formal notation such as PlantUML, so the table provides both word counts.
The word count information is relevant, for instance, to compare the number of tokens used by
different prompting strategies.


   5 For the sake of conciseness, we only present the confusion table for the experiments with GPT-4o-mini.
   6 The complete prompt can be found at this link: urlhttps://github.com/david-xander/code-generation-framework-for-

dsls/blob/main/datasets/generate_domain_context_prompt.md

                                                         17
         Table 3: Datasets used in the experiments: domains and features of the class diagram for each domain

                        Domains                                                 Class diagrams
       Dataset
                   #      Word count      Classes     Associations            Word count (average)                   Constraints
                                                                         Natural language        Formal         #      Word count
       DS1         15         169.13         253          431                    325.60          251.87         86         17.36
       DS2         13         188.08          75           27                    261.31           98.92         96         12.49
Word count: Average number of words used in the textual representation of each category. For example, constraints’ word count is the
  average number of words required to describe the constraints in the dataset. Other columns represent dataset metrics as labeled.

                                       Example

                                        Domain                       Few-shot
                                         model


                                                                                                   Domain
       Original                        Code task                     Prompt               LLM
                        Extract                       Augment                                     description
       Dataset

                                         Code                                                                                  Completed
                                        solution                                                                 Add
                                                                                                                                dataset




                                              Figure 6: Dataset completion process



5.3. Results
    By using our framework and framework instantiation, in the following, we study and de-
scribe the different factors that can affect the quality of the generated code using the previously
described datasets.
    The detailed breakdown of our experiments is as follows: we evaluate two datasets, includ-
ing a total of 30 different domain models and 182 constraints. Each experiment was performed
using 4 different LLMs, although open source LLMs were unable to perform some tasks due
to their limited context window which was insufficient to process the prompt and context infor-
mation. Each experiment was targeting one of 3 different languages (OCL, Alloy and Python).
Experiments were performed with a variety of settings, in order to measure their impact in the
well-formedness and correctness of the generated code: 9 different prompting templates, 2 task-
delivery methods (batch vs isolated) and 2 code repair strategies (with and without code repair).
Moreover, we also measured the effects of increasing the number of attempts in each experiment
(pass@k, using k=3). As a whole, a total of 98,397 code generation tasks were evaluated as part
of these experiments.

5.3.1. Does code generation depend on the target programming language?
Hypothesis. The efficacy of LLM in code generation is influenced by the target programming
language.

Experiments. We compare the quality of the code generated for the two DSLs OCL and Alloy
to a general-purpose language like Python.

Results. Figure 7 shows the results for code generation targeting OCL, Alloy and Python.
    Python achieves the best results both for well-formedness and correctness. Almost 100% of
the Python code generated in the experiments is well-formed, but correctness is only achieved
in (at most) 80% of the experiments. Meanwhile, Alloy and OCL already have problems with
                                               18
           1.0                                                         1.0
                       LLM                                                                                 LLM
                   deepseek-coder:6.7b                                                                 deepseek-coder:6.7b
                   gpt-4o                                                                              gpt-4o
                   gpt-4o-mini                                                                         gpt-4o-mini
                   llama3.1:latest                                                                     llama3.1:latest
           0.8                                                         0.8




           0.6                                                         0.6
Accuracy




                                                            Accuracy
           0.4                                                         0.4




           0.2                                                         0.2




           0.0                                                         0.0
                 ALLOY              OCL         PYTHON                       ALLOY            OCL             PYTHON
                              Target Language                                           Target Language

                         (a) Well-formedness                                         (b) Correctness

Figure 7: Well-formedness and correctness of code generation across LLMs and target languages. Accuracy (defined in
Section 3.4) is shown for each LLM–language pair, with four bars per target language.



well-formedness. Moreover, even when excluding code that is not well-formed, Alloy and OCL
code has more errors affecting its correctness.
     Python exhibits superior semantic coherence and broader applicability across tasks compared
to the DSLs. However, this advantage diminishes for tasks closely aligned with the inherent
purposes of the DSLs, e.g., OCL has less of a disadvantage when generating integrity constraints
that use set operators and navigations through associations.
     Coding tasks focusing on multiplicity (e.g., size() or notEmpty() in OCL and one, lone,
some in Alloy) were generally well-handled in all the target languages. Nevertheless, derived
attributes and tasks requiring inference from implicit logic pose significant challenges for LLMs.

Discussion. There are noticeable differences in the quality of the generated code across lan-
guages. There are several issues that seem to contribute to the problems being identified:

           • Alloy and OCL include some niche operators that are not common in general-purpose
             programming languages. An example could be the set and relational operators from Alloy.
             These operators have very specific typing restrictions and semantics, making them hard to
             use without having access to examples. For instance, Alloy’s subset operation in caused
             many well-formedness problems because LLMs were incapable to use it properly, e.g.,
             comparing sets of different type.

           • Unlike general-purpose programming languages, Alloy and OCL lack a standard library
                                                  19
      that offers frequent types for managing data types such as dates. As a result, in experiments
      where dates are involved, LLMs often hallucinates functions that could perform date and
      time operations.

5.3.2. Does the quality of the generated code depend on the LLM being used?
Hypothesis. Different LLMs lead to different solutions of different quality.

Experiments. We have compared four different LLMs: two proprietary ones by OpenAI (GPT-
4o, GPT-4o-mini) and two open-source LLMs (DeepSeek Coder 6.7b and Llama 3.1).

Results and discussion. Figure 7 illustrates the relative performance of the four different LLMs
for code generation tasks.
    Looking into the results, GPT-4o is the best when considering both well-formedness and
code quality. These results are closely followed by GPT-4o-mini, which only drops in perfor-
mance when considering OCL code. This seems to indicate that GPT-4o has been trained with
OCL snippets (or, at least, some OCL-like textual notation) while GPT-4o-mini has not had this
information available in its training dataset.
    In contrast, DeepSeek and Llama 3.1 exhibit much worse results, having serious problems
even generating well-formed code. DeepSeek has an edge when generating Alloy code, but even
then the quality of the results is poor: 40% of well-formed code snippets for Alloy and, within
those, less than 15% of the correct ones. This makes open source LLMs unusable in practice for
code generation tasks targeting constraint-focused DSLs. For this reason, for the remainder of
the experiments we will be using GPT-4o and GPT-4o-mini as the LLMs of choice.

5.3.3. Which prompting technique performs best?
Hypothesis. As explained in Section 3, our framework provides different prompt templates to
describe the code generation task and provide the relevant contextual information. Our hypothe-
sis is that the prompting technique might have an impact on the quality of the result.

Experiments. Our framework by default uses all the prompting templates described in Table 1.
We have used them for the OpenAI GPT models (GPT-4o and GPT-4o-mini) and for each target
language (Alloy, OCL and Python).

Results. Figure 8 shows the relative accuracy of these prompt templates for each LLM and
language. Given that the previous Sections have discussed the effect of the target programming
language and the LLM, we will focus our discussion on the impact of the prompt template in the
code generation process.

Discussion. The graphs show slight differences in correctness between different prompt tem-
plates, but there does not seem to be a clear winner or trend. For instance, in GPT-4o PT2
achieves worse results than PT1, while for GPT-4o-mini PT2 performs better than PT1 for Alloy
and Python. Also, PT6 is the best for Alloy and Python, but not for OCL. Furthermore, the dif-
ference between different PTs is most noticeable for OCL, while being less relevant for Python
and Alloy.
    It is important to establish whether the observed differences in correctness between different
prompt templates are significant or not. If not, then the choice of prompt template can be based
on other factors, such as the number of tokens used by each prompt template (see Table 4). That

                                               20
           1.0                                                           1.0                                                          1.0
                                           LLM                                                               LLM                                                      LLM
                                           gpt-4o                                                            gpt-4o                                                   gpt-4o
                                           gpt-4o-mini                                                       gpt-4o-mini                                              gpt-4o-mini
           0.8                                                           0.8                                                          0.8



           0.6                                                           0.6                                                          0.6
Accuracy




                                                              Accuracy




                                                                                                                           Accuracy
           0.4                                                           0.4                                                          0.4



           0.2                                                           0.2                                                          0.2



           0.0                                                           0.0                                                          0.0
                 1   2   3   4   5     6    7    8    9                         1   2    3    4    5    6     7    8   9                    1   2    3   4   5    6    7    8   9
                     Prompt Template Index                                          Prompt Template Index                                       Prompt Template Index

                         (a) Python.                                                     (b) OCL.                                                    (c) Alloy.

Figure 8: Impact of different prompting templates in the accuracy of generated code. Bars represent the performance of
each LLM, with two bars shown for each prompt template.

                                       Table 4: Number of tokens required by each of the prompting templates

                              PT           Domain Description                  Domain Model                 Explain DM     Code DM                  Total
                              PT1                    178.60                                                                                         178.60
                              PT2                                                   175.39                                                          175.39
                              PT3                                                   293.45                                                          293.45
                              PT4                                                   175.39                    293.45∗                               468.84
                              PT5                                                   293.45                    293.45∗                               586.90
                              PT6                    178.60                                                                  293.45∗                472.05
                              PT7                    178.60                                                                  175.39∗                353.99
                              PT8                    178.60                         175.39                                                          353.99
                              PT9                    178.60                         293.45                                                          472.05
                                                (∗ ) Estimated values based on average word counts for the datasets.



is, if all prompt templates have comparable performance, we can use the one requiring the least
amount of tokens (and thus, the cheapest). To determine whether the observed differences are
significant, we will perform an statistical test.
     Considering that accuracy is an aggregate metric that is computed from correctness, and that
the correctness evaluation for each instance is represented by a binary number, a suitable statisti-
cal test is Chi-Square. It measures the discrepancy between observed and expected frequencies,
as shown in Equation 5, where χ2 is the Chi-Square statistic, Oi is the observed frequency for
category i, Ei is the expected frequency for category i, and n is the total number of categories.
                                                                                        n
                                                                                        X (Oi − Ei )2
                                                                               χ2 =                                                                                             (5)
                                                                                        i=1
                                                                                                       Ei
    Our null hypothesis (H0 ) considers that the differences in performance observed between
prompt templates (PT) with a single LLM and a single language (as seen in Figure 8) are not
significant: there is no association between the prompt template and accuracy, therefore, the

                                                                                              21
accuracy proportions are equal across all prompt templates. On the other hand, our alterna-
tive hypothesis (HA ) considers that there is an association between prompting templates and
correctness: at least one prompting template (PT) leads to a correctness proportion (accuracy)
significantly different from what we would expect under independence. Choosing a significance
level of α = 0.05, when the computed P-Value is lower than the significance level, we accept our
null hypothesis (H0 ) and conclude that the differences observed between prompt templates are
not significant. Otherwise, if the P-Value is equal or greater than the significance level, we will
reject our null hypothesis (H0 ),
                      Table 5: Chi-Square Statistics for Different Models and Languages

      Language     Model       Chi-Square Statistic    P-Value      Degrees of Freedom      Significance
      ALLOY        GPT-4o             21.33             0.0063              8                Significant
      ALLOY      GPT-4o-mini           5.52             0.7004              8              Not significant
      OCL          GPT-4o             12.66             0.1243              8              Not significant
      OCL        GPT-4o-mini          43.97           5.76 × 10−7           8             Highly significant
      PYTHON       GPT-4o              4.24             0.8345              8              Not significant
      PYTHON     GPT-4o-mini          11.36             0.1819              8              Not significant


    Table 5 shows the statistical values calculated that allowed us to assess the significance of
each combination of language and LLM. In total, 4 combinations do not show evidence that PT
significantly affects correctness. Nevertheless, there are 2 combinations that show significant
differences in performance: Alloy with GPT-4o, and OCL with GPT-4o-mini. Looking at these
2 significant combinations, it is important to identify the prompt templates that contribute to the
observed differences. In particular, we observe that:
   • For Alloy and GPT-4o, PT1, PT6 and PT7 showcase the best results, while PT3 and PT8
     offer the worst.
   • For OCL and GPT-4o-mini, PT1, PT7 and PT9 offer the best results, while PT2, PT3 and
     PT8 offer the worst.
    In conclusion, while there is no general trend, for some combinations of languages and LLM,
PT1 and PT6 achieve the best results, while PT3 and PT8 are the worst performers. There is no
common distinguishable trait shared by the best PTs (PT1, PT6) and worst PTs (PT3, PT8), such
as the use or formal or informal descriptions of the domain model. This implies that we cannot
draw any conclusions regarding which is the best prompt template (or whether providing the
context information helps or not). This disproves our initial hypothesis.
    Given that there is no clear advantage in terms of the quality of the output, PT1 can be
considered the best option since it uses the least number of tokens – which improves efficiency,
sustainability, and price (if applicable).

5.3.4. Does the way in which the coding tasks are delivered/submitted to the LLM affect the
       quality of the generated code?
Hypothesis. As discussed in Section 3.1, when generating code for a set of integrity constraints,
there are different ways to deliver these tasks. Our hypothesis is that the choice of the delivery
method has an impact on the quality of the output.
Experiments. In this section, we have compared batch submission, where the code generation
is required to generate all invariants in a single invocation; and isolated submission, where a
different call to the LLM is performed for each individual invariant.
                                                22
Results and discussion. Figure 9 illustrates the accuracy of two alternative task delivery options:
generating all invariants in one shot, or generating invariants one by one. These results showcase
a comparable performance of both modes, with the exception of OCL where there is a clear
advantage from generating invariants individually.

            1.0                                                                     1.0
                  Delivery strategy                                                                          Delivery strategy
                        All tasks                                                                                  All tasks
                        One by one                                                                                 One by one
            0.8                                                                     0.8


            0.6                                                                     0.6
 Accuracy




                                                                         Accuracy
            0.4                                                                     0.4


            0.2                                                                     0.2


            0.0                                                                     0.0
                   ALLOY              OCL     PYTHON                                      ALLOY        OCL          PYTHON
                            Target Language                                                       Target Language

                      (a) Well-formedness.                                                    (b) Correctness.

Figure 9: Performance of the delivery strategy methods. Each bar represents the performance of a delivery strategy, with
two bars shown for each target language.


    However, these results only consider the correctness of the results provided in each call to the
code generator and do not consider the integration of those results for the case of isolated submis-
sion. That is, when generating invariants individually, the code generator may make assumptions
about the underlying model, such as how certain information will be stored in the model. This
may happen, for instance, if the prompt template being used provides a textual description of
the domain model rather than a domain model, so the structure and naming of elements of the
domain model needs to be assigned by the LLM. There is no guarantee that the decisions made
by each call to the code generator will be consistent among them. Thus, the code generator may
assume that some information is an attribute on one call, and then that it is stored by means of an
association in a subsequent call. These different assumptions may cause the resulting invariants
to be incompatible, and thus impossible to integrate. As a result, considering these integration
issues, the increased cost (each call to the code generator must provide the context information)
and the fact the isolated submission does not yield better performance than batch submission in
general, batch submission would be the preferred strategy.
    Incompatibility problems can be grouped into two categories, (1) errors related to the domain
model conformance, and (2) errors caused by assumptions, or inferred information, that extend
or modify the original domain model. For example, when a LLM assumes association roles that
are not defined by the domain model explicitly, these names may differ from one constraint to
another, potentially causing incompatibilities between the generated invariants. Another related
example occurs when a LLM assumes the choice of a particular an association role name when
generating one constraint: since previous and following constraints will not be aware of this
                                                          23
assumption, navigation conflicts may appear.

5.3.5. Do multiple attempts to generate code and/or code repair improve the quality of the gen-
       erated code?
Hypothesis. As LLMs are non-deterministic and given the same input, different queries to the
LLM could lead to different outputs, running the code generation process multiple times in-
creases the chance of producing a correct solution. The output of the LLM can also be evaluated
to detect problems in the generated code. If problems are detected, then they are reported to
the LLM and a fix is requested. Our hypothesis is that these two strategies, either isolated or
combined, will help improve the quality of the generated code7 .

Experiments. We have applied both strategies and quantify their impact on the quality of the
generated code. We have used GPT-4o and GPT-4o-mini to study the aggregated results of both
LLMs.

Results and discussion. Figure 10 illustrates the effects of allowing k code generation attempts
(where 1≤k≤3) for the same task as well as the inclusion of a round of code repair for incorrect
code. In Fig. 10(a) we see the correctness gains achieved by increasing the number of attempts
(k). Increasing the number of attempts has a linear increase in terms of costs, and it increases
the probability of obtaining correct generated code. However, as expected, there are diminishing
returns: as we increase the number of attempts, the percentage of correct tasks also increases but
each attempt provides smaller improvements.
    Fig. 10(b) shows the effects of including code repair in the code generation pipeline. Code
repair always increases the likelihood of producing correct code, as it is only invoked for those
cases where the initially generated code was incorrect. There is an increase of 10-20% in the
number of correctly generated tasks when applying a single round of code repair.
    Moreover, code repair can be combined with multiple (k) attempts, which implies applying
code repair to each incorrect generated piece of code. This combination achieves the best results.
The only disadvantage is that it requires more calls to the LLM, thus increasing the cost of the
code generation process.

5.4. Discussion and takeaways
     Our findings highlight several important aspects of LLM performance in code generation
across different programming languages. First, the target language plays a crucial role in de-
termining the appropriate model choice. Performance can vary significantly, especially for low-
resource languages, where selecting a model with prior exposure to the language becomes criti-
cal.
     When an LLM is already knowledgeable of the target language, the influence of prompt
engineering appears to diminish. In such cases, most prompts lead to similar results, suggesting
that linguistic familiarity can compensate for less optimized prompt design.
     Moreover, we observe that including multiple constraints within a single prompt, provided
they belong to the same domain, tends to produce better and more consistent outputs. Providing


    7 Note that even if code repair (i.e., requesting fixes to the LLM) is more costly because it requires invoking the LLM

two more times (one for the repair itself and one to assess correctness of the repaired code), it offers an additional chance
to generate correct code.

                                                            24
                          1.0                                                                            1.0
                                Number of Attempts (k)
                                           k=1
                                           k=2
                          0.8                                                                            0.8
                                           k=3
Correctness Probability




                                                                               Correctness Probability
                          0.6                                                                            0.6


                          0.4                                                                            0.4

                                                                                                                       Number of Attempts (k)
                                                                                                                           k=1
                          0.2                                                                            0.2               k=2
                                                                                                                           k=3
                                                                                                                           Code Repair Gain
                          0.0                                                                            0.0
                                  ALLOY              OCL            PYTHON                                     ALLOY           OCL              PYTHON
                                              Target Language                                                            Target Language
                           (a) Correctness gain with more attempts (Pass@3).                                      (b) Pass@3 + code repair.

Figure 10: Correctness gain with more attempts or with code correction. Both graphs show increasing correctness
probability (see Section 3.4 and Equation 1) with additional attempts. Each attempt is denoted by k and represented with
a bar, where the first attempt correspond to k = 1. The second graph additionally illustrates the effect of code repair. The
gray region on the top of each attempt bar represents the additional gain achieved through repair.



constraints to the LLM separately may lead to conflicts or incompatible interpretations by the
model.
    Finally, re-prompting a task multiple times (i.e., multiple attempts) generally leads to higher
success rates compared to asking the model to repair an incorrect output after a failed attempt.
This indicates that regenerating solutions from scratch may be effective. Given that code repair
is sometimes successful in fixing problems in the generated code, a combination of multiple
attempts with code repair is the best performing strategy, although it is also the one that requires
the most resources.
    Table 6 collects a series of concrete guidelines for practitioners, summarizing the key take-
aways gathered from our findings.

5.5. Threats to validity
    In this subsection, we discuss the potential threats to validity that may affect our experimental
design and the interpretation of the results.
    Our experiments have considered code generation tasks for three target languages: OCL,
Alloy and Python. OCL and Alloy are two usual formal notations for describing integrity con-
straints in systems. The results we have obtained may differ for other general-purpose languages
and DSLs, as the performance of LLMs depends on whether the target language (or similar ones)
is present in the training dataset. To mitigate this, future work could include a broader range of
target languages, particularly underrepresented or low-resource DSLs, and explore model fine-
tuning or prompting strategies tailored to such languages.
    Also, our experiments have used a fixed set of LLMs for code generation: GPT-4o, GPT-
4o-mini, DeepSeek Coder 6.7b and Llama 3.1. Other LLMs may achieve different performance
in the task under study and be affected differently by factors such as prompt templates, batch
delivery, code repair, and multiple attempts. Precisely, the proposed framework has been built
                                                  25
                              Table 6: Practical guidelines for practitioners


ID    Guideline                                            Rationale / Practical Insight
G1    Prioritize selecting a model that is well            Model–language alignment has a larger im-
      aligned with the target language, particu-           pact on output quality than prompt tuning
      larly for low-resource or less common lan-           when language support is limited.
      guages.
G2    When the model already supports the target           Over-engineering prompts yields diminish-
      language well, avoid extensive prompt en-            ing returns when baseline language compe-
      gineering; instead, rely on basic validation         tence is strong.
      and multiple attempts.
G3    Specify multiple constraints from the same           Consolidating related constraints reduces
      domain within a single prompt rather than            the risk of incompatible or contradictory
      across multiple prompts.                             generations.
G4    If resources make it viable, use multiple            Multiple attempts and code repair can both
      code generation attempts and code repair.            improve code correctness and are comple-
                                                           mentary to each other.


to support the evaluation of different LLMs and different code generation strategies. It is worth
noting that, in our preliminary experiments, our initial idea was to study a larger set of LLMs
in Ollama (including Mistral 7b, Code Llama 7b, Qwen 2.5 Coder 7b, and Granite Code 8b).
Unfortunately, we had to discard them for several reasons, including incompatibility with our
hardware (NVIDIA RTX A5000 with 24GB of VRAM), frequent freezing, or excessively long
response times ranging from 5 to 10 minutes.
    Given the large number of tasks and alternative code generation strategies, we have relied
on LLM-as-a-judge to provide an automatic assessment of the correctness of generated code. In
Section 5.1, we have measured its accuracy compared to manual code evaluation in 1,512 tasks.
While being less precise than manual evaluation, it is becoming a well-accepted alternative as it
offers a reasonable compromise that avoids subjectivity, variability and enables the large-scale
evaluation and comparison of multiple code generation strategies [38].
    Finally, our experiments use two datasets (Section 5.2) obtained and adapted from the lit-
erature, which ensures that our evaluation is based on publicly available and widely accepted
sources. While this adds transparency and reproducibility, it also introduces external biases.
Our results may be related to the domain information and the type of constraints used in these
datasets. Some constraints appearing in those datasets may be easier to encode in some target
constraint language, leading to unfair comparison. For example, constraints referring to dates
and times may be easier to express in a general-purpose language like Python (which has native
datatypes to handle these concepts) than in DSLs like Alloy or OCL (which do not include a
native Date datatype). Moreover, our experiments have used textual descriptions of the domain
models in our datasets that are generated by an LLM. As a result, these synthetic descriptions
may differ from human-created domain descriptions, for instance, being more concise, less am-
biguous or more predictable. This may affect external validity, limiting our ability to generalize
these results to other domains with human-created textual specifications.


                                                   26
6. Related work

     Abukhalaf et al. [39] investigated the generation of Object Constraint Language (OCL) con-
straints using Codex, emphasizing the importance of combining UML models with natural lan-
guage specifications in prompts to enhance correctness. Their work involved the automatic eval-
uation of well-formedness using USE-OCL [40] (a tool for modeling, validating, and testing
OCL constraints within UML models) and the manual assessment of correctness. Additionally,
they developed a dataset comprising 15 UML models and 114 OCL constraints, each paired with
its respective natural language specification, to support and validate their findings.
     Another prompt augmentation approach reduces the UML model used as context and instead
includes only the relevant subset of classes in the prompt with the UML model. OCL constraints
were generated using GPT-4, with automatic evaluation of well-formedness conducted via USE-
OCL execution and manual evaluation of correctness [14]. However, there is no mention of any
specific technique for correctness evaluation or functional correctness assertion through unit test
cases, such as a test case scenario involving model instantiation in USE-OCL.
     A locally fine-tuned language model demonstrates similar syntactic accuracy to GPT-4 Turbo
while surpassing it in semantic similarity for OCL generation [13]. In order to be able to fine-tune
the model, a dataset with 52 models and 369 OCL constraints was created with synthetic natural
language specifications. They used executions of Eclipse EMF and OCL plugins to assess well-
formedness, and an exact match to assess for correctness approach based on cosine similarity.
     Hong et al. [41] conducted a qualitative study evaluating the effectiveness of using LLMs for
generating Alloy formulas. They focused on the analysis of the Alloy code generation of graph
and binary relations basic properties. Specifically, they used an Alloy specification, and prompt
the LLM to complete the specification according to the coding task. As a result, the authors did
not aim to generate a complete Alloy specification, including the modeling aspect, nor did they
explore how to effectively address such scenarios. In contrast, our work focuses specifically on
constraint generation within this context. Their research complements our efforts by examining
other scenarios for Alloy code generation. We notice that they relied on manual executions of the
Alloy Analyzer to evaluate well-formedness and conducted manual checks to ensure functional
correctness. They assert that their work represents the first study leveraging LLMs to address
traditional synthesis problems using Alloy.
     Testing plays a crucial role in assessing the correctness of generated Alloy code. The AUnit
testing framework [42] provides foundational concepts for unit testing declarative models written
in Alloy, including definitions for test cases, coverage, and coverage criteria. While the initial
AUnit framework laid the groundwork, the tool proposed [43] primarily focused on integrating
AUnit as an extension within the Alloy Analyzer, which does not fully automate the testing
process in a way that directly supports the easy and automated validation of generated Alloy code.
Nevertheless, the core concepts of the AUnit framework, such as its definition of declarative test
cases (a valuation and an Alloy command) and model coverage criteria, remain highly relevant
and could be instrumental in automating correctness validation for generated code, even if further
development is required to achieve full automation.
     Finally, when the program fails to compile or it does not pass any of the tests, the feedback
and the faulty code can be used as input to prompt the LLM to explain the problem and to fix the
code [19].
     Fine-tuning re-trains an LLM for a new task by adjusting its AI model parameters. This pro-
cess requires an extensive dataset for this retraining process, which in the case of code generation
would be a large collection of code samples. However, in some cases this is considered impracti-
                                                27
cal, e.g., due to the data scarcity of DSLs as well as the high computational cost of the re-training.
In contrast, parameter-efficient fine-tuning achieves similar results to fine-tuning while keeping
most of the language model unchanged [20]: it updates only a small set of parameters, mak-
ing the process more efficient and requiring fewer computational resources. This technique has
been proven more effective than full fine-tuning, in-context learning, and retrieval-augmented
generation (RAG) with LLMs targeting code generation [44, 20].


7. Conclusions

    In the context of low-resource programming languages, code generation using LLMs faces
significant challenges. The lack of examples in the LLM’s training datasets causes problems
in terms of the well-formedness and correctness of the generated code. In this paper, we have
proposed a framework to evaluate the capabilities of LLMs generating code from textual require-
ments in terms of both well-formedness and correctness. The proposed framework is flexible,
allowing the comparison of different LLMs, code generation prompts, and the use of different
quality evaluation tools for code.
    We have decided to study code generation for a family of DSLs: constraint and query lan-
guages. Using our framework, we have evaluated ≈100,000 code generation tasks for Alloy,
OCL and Python using different code generation strategies. Given the number of experiments,
the use of automated evaluation (rather than manual evaluation) has been a necessity. Experi-
ments show that the target language and LLM of choice are the most relevant factors affecting
the quality of generated code. Enabling code repair and multiple code generation attempts im-
prove the quality of generated code, while the prompt template and task delivery mode have a
lesser impact. While some of these results are particular to constraint and query languages, some
lessons learned can also be relevant to other DSLs. For reproducibility purposes, we provide all
the software artifacts used in an open source repository [34].
    Regarding future work, we would like to integrate in our framework and test the impacts of
retrieval-augmented generation (RAG) techniques to retrieve the relevant pieces of the domain
model that are relevant for a particular piece of code. Moreover, we would like to study how to
make the well-formedness and correctness checkers available as tools to the LLMs, e.g., using
approaches like Model Context Protocol (MCP) [45], and to assess whether code generation can
improve with the availability of such tools to the LLM. We will look into how to integrate fine-
tuning into our assessment framework, e.g., how to use the examples of generated code during the
evaluation as data for the fine-tuning process. Finally, we would like to evaluate our framework
with different datasets and languages.


Acknowledgement

    This project has been funded by the Spanish Ministry of Science, Innovation, and Universities
under contract PID2021-125527NB-I00 and PID2023-147592OB-I00 (project SE4GenAI); the
research network RED2022-134647-T (MCIN/AEI/10.13039/501100011033, AI4SE network);
University of Málaga under project JA.B1-17 PPRO-B1-2023-037 and a doctoral grant from
Universitat Oberta de Catalunya.




                                                 28
    Appendix A. Example of a complete specification

        In this appendix, we provide a complete example of a coding task. We describe three ele-
    ments: the domain model, the target constraint (which is defined over the previous domain) and
    the generated code in the three target languages (OCL, Alloy and Python).
        We show two alternative characterizations of the domain model: as a textual description in
    natural language or as a class diagram in PlantUML. Our framework will use one description
    or the other depending on the prompt template selected by the user. The sample generated code
    shown in this Appendix has been generated using the prompting template 1 or PT1 (generate
    code from a textual domain description).

    Domain description. The textual domain description is the following:

           We have accidents, which may be of a specific type for example, a rear end colli-
           sion. Each accident occurs on a roadway and may involve multiple victims, with a
           recorded number of fatal victims.
           Vehicles are captured. Some particular kind of vehicles are those that are traveling,
           and more specifically, we also distinguish those involved in accidents, are classified
           as crashed vehicles. A crashed vehicle is associated with a single accident and the
           roadway where the accident occurred. Each accident involves one or more such
           vehicles.
           The system needs to keep track of people. There are three primary subtypes accord-
           ing to the system: living persons, deceased persons and travelers. Travelers can be
           further categorized into drivers, passengers and victims.
           Each Travel instance represents a trip, consisting of one vehicle and one or more
           travelers. This allows us to trace who was traveling in which vehicle at the time of
           the incident.


    Domain model in PlantUML. Figure A.11 shows the PlantUML class diagram that captures the
    previously described domain.

    Coding task. The following is the description of the target constraint in natural language:

           A rear-end collision must involve exactly two vehicles.

    Generated code. The following listings show the code generated in Python, OCL, and Alloy
    for the previous coding task considering the textual domain description. Notice that the Python
    code is a boolean function that checks whether the property holds, the OCL code formalizes the
    constraint as an invariant and the Alloy code expresses it as a fact.
1   def c h e c k _ r e a r _ e n d _ c o l l i s i o n _ c o n s t r a i n t ( accidents ) :
2       for accident in accidents :
3               if accident [ ’ type ’] == ’ rear end collision ’ and len ( accident [ ’ c r a s h e d _ v e h i c l e s
                         ’ ]) != 2:
4                       return False
5
6        return True


1   context Accident inv :
2       self . type = ’ rear - end collision ’ implies self . crashedVehicles - > size () = 2

                                                            29
                                       Person                          Travel                     Vehicle


                                                         travel 1..1            travel 1..1

                                                    travelers 1..*          vehicle 1..1

              DeceasedPerson         LivingPerson             Traveler                        TravelingVehicle




                                        Passenger                           Driver               CrashedVehicle


                                                                                   vehicles 1..*            crashedvehicle 1..*

                                                                            accident 1..1

                                                                             RoadTraﬃcAccident
                                                                                                                           Roadway
                                                                         fatalvictims : EInt

                                                        accident 1..1roadtraﬃcaccident 1..*

                                                      victims 1..*                                roadwaywithaccident 1..1
                                                                                                                  roadwaywithaccident 1..1

                                                            Victim              RearEndCollision                 RoadwayWithAccident




                                          Figure A.11: Domain model in PlantUML.



1   fact R e a r E n d C o l l i s i o n I n v o l v e s T w o V e h i c l e s {
2       all a : Accident | a . type = R e a r E n d C o l l i s i o n implies # a . c ra s he dV e hi c le s = 2
3   }




    References

     [1] V. Murali, C. Maddila, I. Ahmad, M. Bolin, D. Cheng, N. Ghorbani, R. Fernandez, N. Na-
         gappan, P. C. Rigby, AI-Assisted Code Authoring at Scale: Fine-Tuning, Deploying, and
         Mixed Methods Evaluation, Proceedings of the ACM on Software Engineering 1 (FSE)
         (2024) 1066–1085. doi:10.1145/3643774.
         URL https://dl.acm.org/doi/10.1145/3643774

     [2] Z. Rasheed, M. Waseem, M. A. Sami, K.-K. Kemell, A. Ahmad, A. Nguyen-Duc, K. Systä,
         P. Abrahamsson, Autonomous Agents in Software Development: A Vision Paper, in:
         L. Marchesi, A. Goldman, M. I. Lunesu, A. Przybylek, A. Aguiar, L. Morgan, X. Wang,
         A. Pinna (Eds.), Agile Processes in Software Engineering and Extreme Programming -
         Workshops - XP 2024 Workshops, Bozen-Bolzano, Italy, June 4-7, 2024, Revised Selected
         Papers, Vol. 524 of Lecture Notes in Business Information Processing, Springer, 2024, pp.
         15–23. doi:10.1007/978-3-031-72781-8_2.
         URL https://doi.org/10.1007/978-3-031-72781-8_2
     [3] F. Cassano, J. Gouwar, F. Lucchetti, C. Schlesinger, A. Freeman, C. J. Anderson, M. Q.
         Feldman, M. Greenberg, A. Jangda, A. Guha, Knowledge Transfer from High-Resource
         to Low-Resource Programming Languages for Code LLMs, Proceedings of the ACM on
         Programming Languages 8 (OOPSLA2) (2024) 677–708. doi:10.1145/3689735.
         URL https://dl.acm.org/doi/10.1145/3689735

                                                                       30
 [4] J. Cabot, M. Gogolla, Object Constraint Language (OCL): A Definitive Guide, in:
     M. Bernardo, V. Cortellessa, A. Pierantonio (Eds.), Formal Methods for Model-Driven
     Engineering - 12th International School on Formal Methods for the Design of Computer,
     Communication, and Software Systems, SFM 2012, Bertinoro, Italy, June 18-23, 2012.
     Advanced Lectures, Vol. 7320 of Lecture Notes in Computer Science, Springer, 2012, pp.
     58–90. doi:10.1007/978-3-642-30982-3_3.
     URL https://doi.org/10.1007/978-3-642-30982-3_3
 [5] D. Jackson, Software Abstractions - Logic, Language, and Analysis, MIT Press, 2006.
     URL http://mitpress.mit.edu/catalog/item/default.asp?ttype=2&tid=10928
 [6] I. S. Bajwa, B. Bordbar, M. G. Lee, OCL Constraints Generation from Natural Language
     Specification, in: 2010 14th IEEE International Enterprise Distributed Object Computing
     Conference, IEEE, Vitoria, ES, Brazil, 2010, pp. 204–213. doi:10.1109/EDOC.2010.33.
     URL http://ieeexplore.ieee.org/document/5630350/
 [7] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda,
     N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sas-
     try, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavar-
     ian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes,
     A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Bal-
     aji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa,
     A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew,
     D. Amodei, S. McCandlish, I. Sutskever, W. Zaremba, Evaluating Large Language Models
     Trained on Code, arXiv:2107.03374 [cs] (Jul. 2021). doi:10.48550/arXiv.2107.03374.
     URL http://arxiv.org/abs/2107.03374
 [8] B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan, Y. Adi, J. Liu,
     R. Sauvestre, T. Remez, J. Rapin, A. Kozhevnikov, I. Evtimov, J. Bitton, M. Bhatt, C. C.
     Ferrer, A. Grattafiori, W. Xiong, A. Défossez, J. Copet, F. Azhar, H. Touvron, L. Martin,
     N. Usunier, T. Scialom, G. Synnaeve, Code Llama: Open Foundation Models for Code,
     arXiv:2308.12950 [cs] (Jan. 2024). doi:10.48550/arXiv.2308.12950.
     URL http://arxiv.org/abs/2308.12950
 [9] D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. K.
     Li, F. Luo, Y. Xiong, W. Liang, DeepSeek-Coder: When the Large Language Model
     Meets Programming – The Rise of Code Intelligence, arXiv:2401.14196 [cs] (Jan. 2024).
     doi:10.48550/arXiv.2401.14196.
     URL http://arxiv.org/abs/2401.14196
[10] R. Li, L. B. Allal, Y. Zi, N. Muennighoff, D. Kocetkov, C. Mou, M. Marone, C. Akiki,
     J. Li, J. Chim, Q. Liu, E. Zheltonozhskii, T. Y. Zhuo, T. Wang, O. Dehaene, M. Davaadorj,
     J. Lamy-Poirier, J. Monteiro, O. Shliazhko, N. Gontier, N. Meade, A. Zebaze, M.-H. Yee,
     L. K. Umapathi, J. Zhu, B. Lipkin, M. Oblokulov, Z. Wang, R. Murthy, J. Stillerman, S. S.
     Patel, D. Abulkhanov, M. Zocca, M. Dey, Z. Zhang, N. Fahmy, U. Bhattacharyya, W. Yu,
     S. Singh, S. Luccioni, P. Villegas, M. Kunakov, F. Zhdanov, M. Romero, T. Lee, N. Timor,
     J. Ding, C. Schlesinger, H. Schoelkopf, J. Ebert, T. Dao, M. Mishra, A. Gu, J. Robinson,
     C. J. Anderson, B. Dolan-Gavitt, D. Contractor, S. Reddy, D. Fried, D. Bahdanau, Y. Jernite,
     C. M. Ferrandis, S. Hughes, T. Wolf, A. Guha, L. v. Werra, H. d. Vries, StarCoder: may the
                                                31
     source be with you!, arXiv:2305.06161 [cs] (Dec. 2023). doi:10.48550/arXiv.2305.06161.
     URL http://arxiv.org/abs/2305.06161
[11] F. Cassano, J. Gouwar, D. Nguyen, S. Nguyen, L. Phipps-Costin, D. Pinckney, M.-H. Yee,
     Y. Zi, C. J. Anderson, M. Q. Feldman, A. Guha, M. Greenberg, A. Jangda, MultiPL-E: A
     Scalable and Polyglot Approach to Benchmarking Neural Code Generation, IEEE Transac-
     tions on Software Engineering 49 (7) (2023) 3675–3691. doi:10.1109/TSE.2023.3267446.
     URL https://ieeexplore.ieee.org/document/10103177/
[12] S. Joel, J. J. Wu, F. H. Fard, A Survey on LLM-based Code Generation for Low-Resource
     and Domain-Specific Programming Languages, ACM Transactions on Software Engineer-
     ing and Methodology (3770084) (oct 2025). doi:10.1145/3770084.
     URL https://doi.org/10.1145/3770084
[13] F. Pan, V. Zolfaghari, L. Wen, N. Petrovic, J. Lin, A. Knoll, Generative AI for OCL
     Constraint Generation: Dataset Collection and LLM Fine-tuning, in: 2024 IEEE Inter-
     national Symposium on Systems Engineering (ISSE), IEEE, Perugia, Italy, 2024, pp. 1–8.
     doi:10.1109/ISSE63315.2024.10741141.
     URL https://ieeexplore.ieee.org/document/10741141/
[14] S. Abukhalaf, M. Hamdaqa, F. Khomh, PathOCL: Path-Based Prompt Augmentation for
     OCL Generation with GPT-4, in: Proceedings of the 2024 IEEE/ACM First International
     Conference on AI Foundation Models and Software Engineering, ACM, Lisbon Portugal,
     2024, pp. 108–118. doi:10.1145/3650105.3652290.
     URL https://dl.acm.org/doi/10.1145/3650105.3652290

[15] J. Wei, Y. Tay, R. Bommasani, C. Raffel, B. Zoph, S. Borgeaud, D. Yogatama, M. Bosma,
     D. Zhou, D. Metzler, E. H. Chi, T. Hashimoto, O. Vinyals, P. Liang, J. Dean, W. Fedus,
     Emergent Abilities of Large Language Models, Transactions on Machine Learning Re-
     search (2022).
     URL https://openreview.net/forum?id=yzkSU5zdwD

[16] J. Wei, X. Wang, D. Schuurmans, M. Bosma, b. ichter, F. Xia, E. Chi, Q. V. Le, D. Zhou,
     Chain-of-Thought Prompting Elicits Reasoning in Large Language Models, in: S. Koyejo,
     S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, A. Oh (Eds.), Advances in Neural
     Information Processing Systems, Vol. 35, Curran Associates, Inc., 2022, pp. 24824–24837.
     URL https://proceedings.neurips.cc/paper_files/paper/2022/file/9d5609613524ecf4f15af0f7b31

[17] N. Bassamzadeh, C. Methani, Plan with Code: Comparing approaches for robust NL to
     DSL generation (Aug. 2024).
     URL https://arxiv.org/abs/2408.08335
[18] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan,
     P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan,
     R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler,
     M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever,
     D. Amodei, Language models are few-shot learners, in: Proceedings of the 34th Interna-
     tional Conference on Neural Information Processing Systems, NIPS ’20, Curran Associates
     Inc., Red Hook, NY, USA, 2020, event-place: Vancouver, BC, Canada.

                                              32
[19] T. X. Olausson, J. P. Inala, C. Wang, J. Gao, A. Solar-Lezama, Is Self-Repair a Silver Bullet
     for Code Generation?, arXiv:2306.09896 [cs] (Feb. 2024). doi:10.48550/arXiv.2306.09896.
     URL http://arxiv.org/abs/2306.09896
[20] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy,
     H. Wang, Large Language Models for Software Engineering: A Systematic Literature Re-
     view, ACM Transactions on Software Engineering and Methodology 33 (8) (2024) 1–79.
     doi:10.1145/3695988.
     URL https://dl.acm.org/doi/10.1145/3695988
[21] Y. Dong, J. Ding, X. Jiang, G. Li, Z. Li, Z. Jin, CodeScore: Evaluating Code Generation by
     Learning Code Execution, ACM Transactions on Software Engineering and Methodology
     34 (3) (2025) 1–22. doi:10.1145/3695991.
     URL https://dl.acm.org/doi/10.1145/3695991
[22] J. Liu, C. S. Xia, Y. Wang, L. ZHANG, Is Your Code Generated by ChatGPT Really
     Correct? Rigorous Evaluation of Large Language Models for Code Generation, in: A. Oh,
     T. Naumann, A. Globerson, K. Saenko, M. Hardt, S. Levine (Eds.), Advances in Neural
     Information Processing Systems, Vol. 36, Curran Associates, Inc., 2023, pp. 21558–21572.
     URL https://proceedings.neurips.cc/paper_files/paper/2023/file/43e9d647ccd3e4b7b5baab53f03
[23] S. Ren, D. Guo, S. Lu, L. Zhou, S. Liu, D. Tang, N. Sundaresan, M. Zhou, A. Blanco, S. Ma,
     CodeBLEU: a Method for Automatic Evaluation of Code Synthesis, arXiv:2009.10297 [cs]
     (Sep. 2020). doi:10.48550/arXiv.2009.10297.
     URL http://arxiv.org/abs/2009.10297
[24] N. S. Mathews, M. Nagappan, Test-Driven Development and LLM-based Code Gen-
     eration, in: Proceedings of the 39th IEEE/ACM International Conference on Au-
     tomated Software Engineering, ACM, Sacramento CA USA, 2024, pp. 1583–1594.
     doi:10.1145/3691620.3695527.
     URL https://dl.acm.org/doi/10.1145/3691620.3695527

[25] Z. Rasheed, M. Waseem, K. Systä, P. Abrahamsson, Large Language Model Evalu-
     ation Via Multi AI Agents: Preliminary results, arXiv:2404.01023 [cs] (Apr. 2024).
     doi:10.48550/arXiv.2404.01023.
     URL http://arxiv.org/abs/2404.01023

[26] S. Kulal, P. Pasupat, K. Chandra, M. Lee, O. Padon, A. Aiken, P. S. Liang, SPoC:
     Search-based Pseudocode to Code, in: H. Wallach, H. Larochelle, A. Beygelzimer,
     F. d. Alché-Buc, E. Fox, R. Garnett (Eds.), Advances in Neural Information Processing
     Systems, Vol. 32, Curran Associates, Inc., 2019.
     URL https://proceedings.neurips.cc/paper_files/paper/2019/file/7298332f04ac004a0ca44cc69ec

[27] Z. Sollenberger, J. Patel, C. Munley, A. Jarmusch, S. Chandrasekaran, LLM4VV:
     Exploring LLM-as-a-Judge for Validation and Verification Testsuites, in: SC24-W:
     Workshops of the International Conference for High Performance Computing, Net-
     working, Storage and Analysis, IEEE, Atlanta, GA, USA, 2024, pp. 1885–1893.
     doi:10.1109/SCW63240.2024.00238.
     URL https://ieeexplore.ieee.org/document/10820751/

                                               33
[28] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li,
     E. Xing, H. Zhang, J. E. Gonzalez, I. Stoica, Judging LLM-as-a-Judge with MT-Bench
     and Chatbot Arena, in: A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, S. Levine
     (Eds.), Advances in Neural Information Processing Systems, Vol. 36, Curran Associates,
     Inc., 2023, pp. 46595–46623.
     URL https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf

[29] Y. Zhao, Z. Luo, Y. Tian, H. Lin, W. Yan, A. Li, J. Ma, CodeJudge-Eval: Can Large
     Language Models be Good Judges in Code Understanding?, in: O. Rambow, L. Wan-
     ner, M. Apidianaki, H. Al-Khalifa, B. D. Eugenio, S. Schockaert (Eds.), Proceedings of
     the 31st International Conference on Computational Linguistics, Association for Computa-
     tional Linguistics, Abu Dhabi, UAE, 2025, pp. 73–95.
     URL https://aclanthology.org/2025.coling-main.7/
[30] Antlr Project, grammars-v4/ocl at master · antlr/grammars-v4 (2025).
     URL https://github.com/antlr/grammars-v4/tree/master/ocl
[31] Antlr Project, grammars-v4/alloy at master · antlr/grammars-v4 (2025).
     URL https://github.com/antlr/grammars-v4/tree/master/alloy
[32] Antlr Project, grammars-v4/python/python3_13 at master · antlr/grammars-v4 (2025).
     URL https://github.com/antlr/grammars-v4/tree/master/python/python3_13
[33] J. Gu, X. Jiang, Z. Shi, H. Tan, X. Zhai, C. Xu, W. Li, Y. Shen, S. Ma, H. Liu,
     S. Wang, K. Zhang, Y. Wang, W. Gao, L. Ni, J. Guo, A survey on llm-as-a-judge (2025).
     arXiv:2411.15594.
     URL https://arxiv.org/abs/2411.15594
[34] D. Delgado, L. Burgueño, R. Clarisó, Complementary software artifacts (2025).
     URL https://github.com/david-xander/code-generation-framework-for-dsls

[35] G. Crupi, R. Tufano, A. Velasco, A. Mastropaolo, D. Poshyvanyk, G. Bavota, On the effec-
     tiveness of llm-as-a-judge for code generation and summarization, IEEE Trans. Software
     Eng. 51 (8) (2025) 2329–2345. doi:10.1109/TSE.2025.3586082.
     URL https://doi.org/10.1109/TSE.2025.3586082
[36] X. Hu, Q. Chen, H. Wang, X. Xia, D. Lo, T. Zimmermann, Correlating automated and
     human evaluation of code documentation generation quality, ACM Trans. Softw. Eng.
     Methodol. 31 (4) (2022) 63:1–63:28. doi:10.1145/3502853.
     URL https://doi.org/10.1145/3502853
[37] M. Freitag, G. F. Foster, D. Grangier, V. Ratnakar, Q. Tan, W. Macherey, Experts, errors,
     and context: A large-scale study of human evaluation for machine translation, Trans. Assoc.
     Comput. Linguistics 9 (2021) 1460–1474. doi:10.1162/TACL_A_00437.
     URL https://doi.org/10.1162/tacl_a_00437
[38] J. Gu, X. Jiang, Z. Shi, H. Tan, X. Zhai, C. Xu, W. Li, Y. Shen, S. Ma, H. Liu,
     S. Wang, K. Zhang, Y. Wang, W. Gao, L. Ni, J. Guo, A Survey on LLM-as-a-Judge,
     arXiv:2411.15594 [cs] (Mar. 2025). doi:10.48550/arXiv.2411.15594.
     URL http://arxiv.org/abs/2411.15594
                                              34
[39] S. Abukhalaf, M. Hamdaqa, F. Khomh, On Codex Prompt Engineering for OCL Gen-
     eration: An Empirical Study, in: 2023 IEEE/ACM 20th International Conference on
     Mining Software Repositories (MSR), IEEE, Melbourne, Australia, 2023, pp. 148–157.
     doi:10.1109/MSR59073.2023.00033.
     URL https://ieeexplore.ieee.org/document/10173990/

[40] M. Gogolla, F. Büttner, M. Richters, USE: A UML-based specification environment for
     validating UML and OCL, Science of Computer Programming 69 (1-3) (2007) 27–34, pub-
     lisher: Elsevier.
[41] Y. Hong, S. Jiang, Y. Fu, S. Khurshid, On the Effectiveness of Large Lan-
     guage Models in Writing Alloy Formulas, arXiv:2502.15441 [cs] (Feb. 2025).
     doi:10.48550/arXiv.2502.15441.
     URL http://arxiv.org/abs/2502.15441
[42] A. Sullivan, R. N. Zaeem, S. Khurshid, D. Marinov, Towards a test automation framework
     for alloy, in: Proceedings of the 2014 International SPIN Symposium on Model Checking
     of Software, ACM, San Jose CA USA, 2014, pp. 113–116. doi:10.1145/2632362.2632369.
     URL https://dl.acm.org/doi/10.1145/2632362.2632369
[43] A. Sullivan, K. Wang, S. Khurshid, AUnit: A Test Automation Tool for Alloy, in: 2018
     IEEE 11th International Conference on Software Testing, Verification and Validation
     (ICST), IEEE, Vasteras, 2018, pp. 398–403. doi:10.1109/ICST.2018.00047.
     URL https://ieeexplore.ieee.org/document/8367067/

[44] M. Weyssow, X. Zhou, K. Kim, D. Lo, H. Sahraoui, Exploring Parameter-Efficient Fine-
     Tuning Techniques for Code Generation with Large Language Models, ACM Transactions
     on Software Engineering and Methodology (2025) 3714461doi:10.1145/3714461.
     URL https://dl.acm.org/doi/10.1145/3714461
[45] Anthropic, Introducing the Model Context Protocol (2024).
     URL https://www.anthropic.com/news/model-context-protocol




                                            35
