                                                                                                                                                           1




      Automated Repair of Declarative Software
  Specifications in the Era of Large Language Models
            Md Rashedul Hasan, Jiawei Li, Iftekhar Ahmed, Member, IEEE and Hamid Bagheri, Member, IEEE


   Abstract—The growing adoption of declarative software                                 properties. This integration simplifies the analysis and
specification languages, coupled with their inherent difficulty in                       verification of Alloy specifications and enables a seamless user
debugging, has underscored the need for effective and automated
repair techniques applicable to such languages. Researchers have                         experience within the Alloy environment. Although the Alloy
recently explored various methods to automatically repair                                Analyzer is a powerful tool, Alloy users, much like Java or C
declarative software specifications, such as template-based repair,                      developers, may still inadvertently introduce subtle bugs while
feedback-driven iterative repair, and bounded exhaustive
approaches. The latest developments in large language models
                                                                                         writing their specifications. Even though the Alloy Analyzer can
provide new opportunities for the automatic repair of declarative                        assist in automatically verifying properties and producing
specifications. In this study, we assess the effectiveness of utilizing                  counterexamples that highlight assertion violations, the actual
OpenAI’s ChatGPT to repair software specifications written in                            process of debugging, evaluating, and resolving issues can still
the Alloy declarative language. Unlike imperative languages,
specifications in Alloy are not executed but rather translated into                      be difficult and timeconsuming, particularly for specifications
logical formulas and evaluated using backend constraint solvers                          that capture intricate behaviors and large systems [50], [57].
to identify specification instances and counterexamples to                                  In recent years, researchers have explored using various
assertions. Our evaluation focuses on ChatGPT’s ability to                               methods to automatically repair declarative software
improve the correctness and completeness of Alloy declarative
specifications through automatic repairs. We analyze the results                         specifications, such as template-based repair [93], [95],
produced by ChatGPT and compare them with those of leading                               feedback-driven iterative repair [19], and bounded exhaustive
automatic Alloy repair methods. Our study revealed that while                            approaches [18], [34]. ARepair [88] is considered the first
ChatGPT falls short in comparison to existing techniques, it was                         approach for automated program repair in Alloy. It operates by
able to successfully repair bugs that no other technique could
address. Our analysis also identified errors in ChatGPT’s                                fixing bugs identified by failing test cases, and thus assumes that
generated repairs, including improper operator usage, type                               tests are available to verify correctness. However, tests are not
errors, higherorder logic misuse, and relational arity mismatches.                       commonly used in Alloy specifications, where users rely on
Additionally, we observed instances of hallucinations in
ChatGPT-generated repairs and inconsistency in its results. Our
                                                                                         assertions to describe expectations and use the Alloy Analyzer
study provides valuable insights for software practitioners,                             to validate them. Moreover, ARepair can be susceptible to the
researchers, and tool builders considering ChatGPT for                                   overfitting issue when test cases are insufficient, resulting in
declarative specification repairs.                                                       generated repairs that pass the tests but are incorrect in general
   Index Terms—Declarative Specification, Automated Repair,                              [19], similar to the problems encountered in traditional
LLMs                                                                                     imperative-based automatic program repair (APR) approaches.
                                                                                         BeAFix [34] technique utilizes assertions as correctness oracles
                                                                                         and mitigates the overfitting problem. Nevertheless, the BeAFix
                     I. INTRODUCTION
                                                                                         approach’s drawback is that it can be time-consuming as it

T       HE versatile nature of declarative specification
       languages has enabled their application in various
       software engineering problems. One such language is
the Alloy specification language [36], which employs
                                                                                         exhaustively enumerates the possible candidate repairs up to a
                                                                                         certain threshold and verifies if any of them successfully satisfy
                                                                                         the failing assertions. A prior research [95] has shown that
                                                                                         BeAFix is limited in generating complex repairs for a range of
relational algebra and first-order logic to solve a broad range                          Alloy specifications as the number of repair candidates to be
of tasks in software engineering. These tasks include software                           tried can be prohibitively large, indicating ample opportunity for
design [12]–[14], [37], [43], [83], software verification [10],                          improvement.
[28], [58], [63], [67], [74], [85], network security [56], [64],                            The advent of Large Language Models (LLMs) trained on
[75], security analysis of emerging platforms, such as IoT and                           massive amounts of natural language documents, code, and
Android platforms [6], [8], [9], [11], [15], [77], test case                             specifications has revolutionized the field of natural language
generation [41], [59], [62], [70], [78], and more. Furthermore,                          processing and the applications thereof. By employing advanced
the Alloy specification language is seamlessly integrated with                           architectures, such as transformers [20], [86], and leveraging the
the Alloy Analyzer, which enables users to automatically                                 power of large datasets, these pre-trained models have
verify if the provided specifications meet certain desirable                             demonstrated remarkable accuracy in predicting not only natural
  M. Hasan and H. Bagheri are with the School of Computing, University of Nebraska-
                                                                                         language but also code and specifications. Notably, LLMs have
Lincoln, Lincoln, NE, USA. E-mail: {mhasan6,hbagheri}@cse.unl.edu                        proven adept at tasks such as code completion and generating
  J. Li, I. Ahmed are with the Donald Bren School of Information and Computer Science,
University of California, Irvine, USA. E-mail: {jiawl28,iftekha}@uci.edu
                                                                                         code from natural language descriptions [92]. The potential of
                                                                                         LLMs has been demonstrated by Codex [21], one of the largest
                                                                                                                                      2


models which is now incorporated in Github Copilot 1 , a                   •   We provide a complete replication package to support the
practical tool designed to aid developers by producing code                    verifiability and replication of our study [1].
based on user input. ChatGPT2 is another language model that
has garnered significant attention since its public release in                     II. BACKGROUND AND MOTIVATION
November 2022. Its intuitive interface allows users to interact
with the model naturally, making it a valuable asset for software      A. Alloy Overview
engineering tasks.
                                                                          Alloy is a formal modeling language with a comprehensible
    The well-established potential of ChatGPT in program
                                                                       syntax inspired by object-oriented notations and a semantics
 generation and automation, combined with the widely-known
                                                                       based on first-order relational logic [3]. An Alloy specification
 challenges involved in repairing formal specifications, which
                                                                       consists of three key components: (1) data types, (2) formulas
 is a time-consuming and laborious process for software
                                                                       that define constraints over data types, and (3) commands to
 developers, inspired us to conduct a systematic empirical
                                                                       execute the analyzer. The language uses signatures (sig) to
 study. The primary objective of our study is to explore the
                                                                       define basic data types, which can be structured using fields to
 possibilities of using ChatGPT for repairing faulty Alloy
                                                                       capture the relationships between signatures.
 specifications, and to identify any obstacles that must be
 addressed to make it a viable solution.                                  Facts (fact) are formulas that take no arguments, and
                                                                       introduce constraints that always hold in every instance of the
    In this paper, we present and interpret the results of our
                                                                       specification, thus restricting the model space of the
 comprehensive evaluation of ChatGPT’s effectiveness in
                                                                       specification. The formulas can be further structured using
 repairing faulty Alloy specifications, comparing it to the state-
                                                                       predicates (pred) and functions (fun), which are named,
 of-the-art Alloy APR techniques recently proposed in the
                                                                       parameterized Alloy formulas that can be invoked. Assertions
 literature. Our evaluation includes ARepair [88], BeAFIX [34],
                                                                       (assert) are named formulas that capture expected properties of
 ATR [95], and ICEBAR [19] as baselines for comparison. We
                                                                       the specification, i.e., properties that the user wants to verify.
 evaluate all the techniques on two sets of benchmarks,
                                                                       The check and run commands are used to invoke the automated
 developed by other research groups, consisting of 1,974
                                                                       analyzer for checking assertions (assert), which are Alloy
 defective specifications from ARepair [88] and Alloy4Fun
                                                                       formulas used to check properties, and running predicates
 [55]. We provide a categorization of the errors we discovered
                                                                       (pred), respectively.
 and discuss the implications of these findings for formal
                                                                          Formulas in Alloy specifications are expressed in relational
 specification repair. Our research aims to address the following
                                                                       logic, which is a first-order logic that has been extended with
 questions:
                                                                       relational operators such as transpose, union, difference, and
       • RQ1: How does the performance of the LLM-based                intersection. In addition to the usual universal and existential
         repair, realized atop ChatGPT, compare to that of the         quantifiers (all and some, respectively), Alloy supports one and
         stateof-the-art techniques for repairing Alloy                lone quantifiers, which respectively stand for "exists exactly
         specifications?                                               one" and "exists at most one". Furthermore, Alloy features
       • RQ2: How consistent are the repairs generated by the          important relational operators such as relational join, which
         LLM-based repair, which is built on top of ChatGPT,           generalizes composition to n-ary relations and allows for the
         when using the same prompt and faulty specifications?         expression of navigations as in object orientation. Another
       • RQ3: What are the primary categories of mistakes              significant operator is the transitive closure, which can be
         present in ChatGPT’s generated Alloy repairs?                 applied only to binary relations and extends the expressiveness
       • RQ4: What impact do prompts have on the Alloy repairs         of Alloy beyond that of first-order logic.
         produced by ChatGPT?                                             The Alloy Analyzer automates the analysis of Alloy
                                                                       specifications by translating them into propositional formulas
    To summarize,            this    paper   makes   the   following   and using off-the-shelf SAT solvers to find either
    contributions:                                                     counterexamples that violate asserted properties (with check
       • We conduct the first empirical study, to the best of our      command) or model instances that satisfy predicates (with run
         knowledge, that explores the effectiveness of LLM-based       command). In fact, the analyzer performs two types of
         Alloy repair, realized atop ChatGPT, in comparison to         automated analysis: simulation and model checking.
         that of the state-of-the-art techniques for repairing Alloy      Simulation demonstrates the consistency of model
         specifications. This study becomes increasingly crucial       specifications by generating a satisfying model instance, while
         with the prevalence of powerful AI tools.                     model checking involves finding a counterexample–a model
       • We offer a comprehensive analysis and interpretation of       instance that violates a particular assertion. When provided with
         the results obtained, accompanied by a categorization of      a specification M and an assertion p, the Alloy Analyzer searches
         errors that arise from LLM-based repair compared to           for counterexamples by solving a propositional formula that
         other techniques for Alloy APR.                               represents the constraints of M and the negation of p (M∧¬p).
                                                                       On the other hand, if p is a predicate, the Alloy Analyzer will

   1
    https://github.com/features/copilot
   2
    https://chat.openai.com/chat
                                                                                                                                       3


search for model instances that satisfy p by solving the formula     room based on whether they own a key to that room. Finally,
M ∧p. Alloy’s analysis is bounded-exhaustive, meaning that if a      to ensure the secure access of SecureLab, the assert is_secured
specification M, an assertion (or a predicate) p, and a bound t      is used to verify that only researchers can enter the secure lab.
(referred to as the scope in Alloy’s context) are given, then the       To verify the assertion, the Alloy Analyzer is executed on
Alloy Analyzer will only find a counterexample (or a satisfying      this specification using the check command, as shown in line
instance) for p of size that is bounded by t, if such a t-bounded    31. The Analyzer generates a counterexample that violates the
counterexample (or instance) exists.                                 assertion by describing a scenario where an employee owns a
                                                                     key that can open SecureLab. This demonstrates that the
                                                                     specification contains a bug that violates the asserted property.
                                                                     The objective is to evaluate the effectiveness of a repair method
                                                                     using LLMs, such as ChatGPT, compared to the state-of-theart
                                                                     Alloy repair for fixing such bugs.

                                                                                          III. RELATED WORK
                                                                    A. Automated Program Repair
                                                                       Automatic program repair has become an increasingly popular
                                                                    research topic due to the growing demand for reliable software.
                                                                    There are several different approaches to automatic program repair.
                                                                    Constraint-based repair techniques, such as SemFix [65],
                                                                    FoRenSiC [17], Angelix [60], AFix [38], StarFix [94], Jobstmann
                                                                    et al. [39], and Gopinath et al. [30], use constraints to produce
                                                                    repairs that are correct by construction, ensuring that they adhere to
                                                                    a given specification or pass a test suite. In contrast, generate-and-
                                                                    validate repair techniques, such as Pachika [23], PAR [42], Prophet
                                                                    [54], Debroy and Wong [24], and GenProg [47], find several repair
                                                                    candidates using stochastic search or invariant inferences, and then
                                                                    verify them against the given specifications. Learning-based repair
                                                                    techniques, such as iFixR [45], Fixminer [44], DLFix [51], and
                                                                    DeepDelta [61], learn fixes from repair samples.
                                                                       Some research efforts in program synthesis and repair, such as
                                                                    [7], [46], [60], [65], [66], [81], [82], integrate existing tools like
                                                                    test-input generation or symbolic execution to synthesize desired
                                                                    programs. These integrations are common in modern synthesis
                                                                    techniques, including the multi-disciplinary ExCAPE project [4]
                                                                    and the SyGuS competition [5]. As a result, many practical and
              Fig. 1: A faulty Alloy specification.                 useful tools have been developed, such as Sketch [80], which
                                                                    generates low-level bit-stream programs, Autograder [79], which
                                                                    provides feedback on programming homework, and FlashFill [31],
 B. Illustrative Example                                            [32], which constructs Excel macros.
    The Alloy specification presented in Fig. 1 addresses a room       Alloy Repair. Compared to automatic program repair and
 access control problem. The specification begins by defining       synthesis approaches for imperative programs, there has been
 several classes or types, called sig’s. The Room type has only     relatively less research dedicated to APR techniques for declarative
 one subclass, SecureLab. The Person type has two non-              specifications, such as Alloy.
 overlapping subclasses, Employee and Researcher, both                 ARepair [88] was the first APR approach for Alloy, which
 sharing a common field, owns, which represents a set of keys       generates fixes for Alloy specifications violating test cases. The
 owned by a person. The Key type has a field, opened_by,            ARepair approach utilizes three techniques: AUnit [84] tests, which
 which represents exactly one room that can be opened by the        are unit tests expressed as Alloy predicates; AlloyFL [89] fault
                                                                    localizer, which uses unit tests to identify potentially problematic
 key. Additionally, a couple of facts are defined in the
                                                                    statements in the program; and mutation-based repairs (e.g., [47]),
 specification to capture additional constraints. The first fact
                                                                    which randomly mutate Alloy expressions in an attempt to fix bugs.
 specifies that there must be at least one employee and one         However, prior studies [19], [34], [95] show that it suffers from
 researcher, and at least one employee who owns more than one       overfitting due to using tests as an oracle for repairs, which may not
 key.                                                               generalize to unseen tests.
    The second fact in the Alloy specification for a room access       BeAFIX [34] addresses the overfitting issue by using assertions
 control problem (Fig. 1, lines 15–21), specifies that every room   as the basis for repairing Alloy specifications. Assertions are more
 can be opened by some key and that each employee owns at           natural in Alloy development and represent a larger set of tests than
 least one key, which cannot open SecureLab. In addition to         individual test cases. BeAFix also relies on the user to identify
 these facts, there is a predicate called CanEnter, which is a      faulty statements. To generate repairs, BeAFix exhaustively
 boolean function that checks whether a person can enter a          searches all possible repair candidates up to a certain bound by
                                                                                                                                         4

mutation and uses Alloy counterexamples for variabilization             initialized from a pre-trained model on auto-regressive generation
feasibility checking.                                                   and then fine-tuned using reinforcement learning from human
     ATR [95] is a template-based approach for repairing Alloy          feedback (RLHF) [96]. RLHF first fine-tunes the model with a
  specifications that extends the fault localization techniques of      small dataset of prompts and desired outputs written by human
  FLACK. FLACK is designed to identify potentially faulty Alloy         labelers. Next, a reward model is trained on a larger set of prompts
  expressions responsible for assertion failures by analyzing           by sampling outputs from the fine-tuned model and using human
  counterexamples and PMAXSAT instances to extract relevant             labeler to rank each individual output, which reflects the human
  information. ATR builds on FLACK’s methodology by generating          preference. Finally, reinforcement learning is applied to calculate
  repair candidates using templates and by leveraging the               the reward of the generated output based on the reward model and
  discrepancies between counterexamples and satisfying                  adjust the weights of LLM. The trained LLMs (e.g., ChatGPT)
  instances to eliminate unsuitable candidates.                         have shown better understanding of human intentions and
     ICEBAR [19] is a tool that uses ARepair as a backend tool          superior performances in various downstream tasks [16], [40],
  for repairing faulty Alloy specifications based on a set of Alloy     [49], [69], [91] to most state-of-the-art LLM-based approaches.
  tests. However, ARepair is more susceptible to producing               However, there is still a lack of understanding about ChatGPT’s
  overfitting repairs due to its use of tests as oracles. ICEBAR      feasibility and performance on automated specification repair. In
  mitigates overfitting by using property-based oracles, which        this work, we make the first step to evaluate ChatGPT’s ability to
                                                                      improve the correctness and completeness of Alloy declarative
  represent large families of intended behavior tests. It also uses
                                                                      specifications through automatic repairs.
  Alloy counterexamples to prune certain partial fixes that can
  never lead to repairs.
                                                                                       IV. EXPERIMENTAL DESIGN
 B. Large Language Models
    Large Language Models (LLMs) [20] have been pre-trained           A. Repair Scenarios
 [22], [71] on large text corpora so that they learn the general         We explore five repair scenarios that involve different
 knowledge about the target natural language. Then, these             prompts given to ChatGPT to guide the repair process. These
 models are either fine-tuned [71] with task-specific data or         repair scenarios are intended to cover all practical repair
 prompted [52] with task-related information to obtain a decent       situations similar to those studied in prior APR research. A
 performance on various downstream tasks. Fine-tuning                 ChatGPT prompt refers to the initial text or input given to the
 requires a human annotated dataset to train the LLMs in a            ChatGPT language model, which is designed to generate
 supervised manner. Since constructing a training dataset with        responses. It is a starting point for the AI system to generate a
 sufficient size is costly, prompting may be a desired alternative    coherent and relevant response based on its training and
 for LLMs with billions of parameters. It directly instructs          knowledge. The prompt can be a question, statement, or any
 LLMs without any fine-tuning by providing natural language           other form of input that the user provides to initiate a
 descriptions of the downstream task and optionally a few             conversation or request information from the ChatGPT language
 examples of the task being handled by human, which relieves          model. In the following we present each of the five repair
 the cost of collecting human annotated training data in              scenarios, summarized in Table I, along with a concrete
 finetuning.                                                          example, depicted in in Figure 2.
    LLMs are built on the transformer architecture [86] and can be       • Repair Scenario 1. The benchmark specifications
 classified into auto-regressive language models [20], masked
                                                                            contained both bug locations and fix comments.
 language models [25], and encoder-decoder [48] language models
                                                                            Additionally, ChatGPT was tasked with fixing the bugs
 based on their pre-training objectives. Autoregressive language
                                                                            without being instructed to pass the assertions.
 models employ “generative pre-training", predicting the next
                                                                         • Repair Scenario 2. The benchmark specifications only
 token in a sequence (e.g., GPT-3 [20], [73]). Masked language
 models predict masked tokens using the remaining token                     included bug locations, without any fix comments.
 sequence as context (e.g., BERT [25]), while encoder-decoder               Additionally, ChatGPT was tasked with fixing the bugs
 language models are trained on sequence-to-sequence tasks,                 without being instructed to pass the assertions.
 excelling in translation and summarization tasks (e.g., T5, BART        • Repair Scenario 3. The benchmark specifications had no
 [48], [72]). Recently, pre-trained natural language LLMs have              bug locations or fix comments. Additionally, ChatGPT was
 been adapted for source code, such as CodeGPT/Codex [21]                   tasked with passing the assertions to fix the bugs.
 (based on GPT3 [20]), CodeBERT/GraphCodeBERT [26], [33]                 • Repair Scenario 4. The benchmark specifications had no
 (based on BERT [25], [53]), and CodeT5 [90] (based on T5 [72]).            bug locations or fix comments. Additionally, ChatGPT was
 Those LLMs have been evaluated and fine-tuned for various                  tasked with fixing the bugs without being instructed to pass
 software engineering tasks, such as automated code repair and              the assertions.
 clone detection, demonstrating promising results.                       • Repair Scenario 5. The benchmark specifications only
    More recently, researchers have found that LLMs trained under           included bug locations, without any fix comments.
 a reinforcement learning paradigm tend to align better with                Additionally, ChatGPT was tasked with passing the
 human preference [68], [69], [96]. Specifically, ChatGPT [68]              assertions to fix the bugs.
 is a LLM that was trained in such a paradigm and has received
 much attention from researchers and practitioners. It is first
                                                                                                                                      5


                                                                            Repair          Bug        Fix      Passing assertion
                                                                            Scenario      location   comment       requirement
                                                                            Scenario-1      Yes        Yes             No
                                                                            Scenario-2      Yes        No              No
                                                                            Scenario-3      No         No              Yes
                                                                            Scenario-4      No         No              No
                                                                            Scenario-5      Yes        No              Yes


                                                                                     TABLE I: Repair Scenarios Summary


                                                                       B. Baselines
                                                                        In this study, we compare a ChatGPT-based Alloy repair
                                                                     technique with four state-of-the-art automated repair techniques for
                                                                     faulty Alloy specifications. These techniques include (1) ARepair
                                                                     [88], the first APR technique for Alloy, (2) BeAFIX [34], a bounded
                                                                     exhaustive repair method, (3) ATR [95], which uses templates for
                                                                     repair, and (4) ICEBAR [19], a feedback-driven iterative repair
                                                                     approach. These techniques have been proposed recently in the
                                                                     literature and serve as baselines for comparison with a ChatGPT-
                                                                     based repair approach. Further details about these baselines can be
                                                                     found in Section III.

                                                                     C. Subject Systems
                                                                        In our evaluation, we employ two distinct benchmark suites:
                                                                     ARepair [88] and Alloy4Fun [55]. These benchmark suites have
                                                                     been extensively studied and were developed by independent
                                                                     research groups, allowing for a fair comparison of various
                                                                     techniques.
                                                                        The Alloy4Fun benchmark [55] includes a collection of 1936
                                                                     hand-written faulty specifications that were gathered from student
                                                                     submissions for six different Alloy problems. These problems
                                                                     include the modeling of a labeled transition system (lts), an
                                                                     automated production line (production), class registrations
                                                                     (classroom), a work and source distribution problem (cv), various
                                                                     graph properties such as acyclic and completeness (graphs), and a
                                                                     file system trash can (trash).
                                                                        The ARepair benchmark [88] is composed of 38 faulty
                                                                     specifications that were obtained from a total of 12 Alloy problems.
                                                                     Six of these problems, named addr (address book modeling), cd
                                                                     (object and class hierarchy modeling), ctree (undirected tree
                                                                     modeling), farmer (chicken crossing problem modeling), bempl and
                                                                     other (both modeling the security lab access problem), and grade
                                                                     (gradebook specification modeling), were obtained from the Alloy
                                                                     Analyzer. The remaining faulty specifications were obtained from
                                                                     graduate student homework and are named arr (sorted arrays
                                                                     modeling), blancedBST (balanced binary search tree modeling), dll
                                                                     (doubly linked list modeling), fsm (finite state machine modeling),
                                                                     and student (sorted linked list modeling).
                                                                        The benchmark datasets include specifications ranging from tens
                                                                     to hundreds of lines, with real bugs written by humans. The defects
                                                                     present in the benchmarks cover a diverse range, from
                                                                     straightforward ones that can be fixed by modifying a single
                                                                     operator to complex ones that demand the synthesis of novel
                                                                     expressions and substitution of the entire predicate body.
                                                                     Additionally, the benchmarks come with the correct versions of the
Fig. 2: Examples of prompts for various repair scenarios.            specifications, which serve as ground truths for verifying the
Figures partially represent excerpts from the faulty specification   accuracy of the obtained results.
provided to ChatGPT.
                                                                                                                                        6


D. Implementation                                                      repair scenarios utilizing ChatGPT. These scenarios involve
   We implement an apparatus to conduct our empirical study            diverse prompts given to ChatGPT, which guide the repair
in Java and Python on top of Alloy Analyzer APIs and by                process and are detailed in Section IV-A.
accessing the ChatGPT API endpoint, which allowed us to                2) RQ2–Consistency of the repairs: To assess ChatGPT’s
directly collect and save responses. We utilized the gpt-              reliability as a repair technique, we conducted a consistency test,
3.5turbo model from the ChatGPT family, which is a stable and          as LLM-based techniques may not generate the same repairs
                                                                       given the same prompt and faulty specification. The test involved
reliable version of the GPT engine. Our implementation allows
                                                                       providing ChatGPT with the exact same repair prompt ten
for the direct submission of each faulty Alloy specification
                                                                       different times for ten different faulty specifications, including a
prepared for the scenarios detailed earlier via the API and
                                                                       bug location indicator. We used new chat sessions each time and
stores the response in a text file.                                    measured the similarity of the generated repairs using BLEU,
   For the evaluation and verification process of each repaired        ROUGE-L, METEOR, and BERTbased semantic similarity
Alloy specification, we used Alloy Analyzer version 4.2 APIs.          metrics. We also verified the validity of the generated repairs
We collected responses from ChatGPT five times for each                across ten prompts by checking them using the Alloy formal
faulty specification in each of the two benchmark suites, based        analyzer, ensuring consistency.
on the aforementioned five scenarios. This involved                    3) RQ3–Category of Mistakes: For answering RQ3, we did a
approximately 10,000 requests sent to the ChatGPT server. To           manual inspection of the mistakes made by ChatGPT. In total,
evaluate the generated patches, we used a system with an 8core         we analyzed 6,559 mistakes. We followed an open coding
CPU, 8-core GPU, and 16-core neural engine, all based on the           protocol [29] to categorize the mistakes. Specifically, two
ARM architecture, with 8 GB of RAM and running macOS                   authors of this study independently checked all mistakes and
Ventura with Oracle Java SE Development Kit 8u202 (64-bit              categorized them. During the analysis, each emerging category
version).                                                              was compared with existing ones to determine if it is a new
   For language models such as ChatGPT, the “temperature” is           category through multiple comparison sessions. Finally, the two
a hyperparameter that controls the randomness of the model’s           authors exchanged ideas for the categorization and reached a
output during text generation. It determines how creative or           consensus through negotiated agreement [27].
deterministic the model’s responses will be. Choosing an               4) RQ4–Impacts of Prompts: To investigate the impact of
appropriate temperature value depends on the specific use case         prompts on the Alloy repairs produced by ChatGPT, we designed
and the desired output style. So it is essential to systematically     a study that varies three main elements of prompts for Alloy
explore different values of temperature before deciding. We            repair: (1) Bug Location Indicator: A binary factor that
conducted tests with various temperature values for ChatGPT            determines whether the prompt contains a bug location indicator
                                                                       or not. (2) Fix Comment: A binary factor that determines whether
during our experimentation. We explored temperature values
                                                                       the prompt contains a fix comment or not. (3) Assertion
from 0.05 to 1, with a 0.05 scale increment, and compared the
                                                                       Instruction: A binary factor that determines whether the prompt
results with the samples selected from the benchmark dataset.
                                                                       instructs ChatGPT to pass assertions or not. We also followed the
We found that the default temperature value provided the best          best practices outlined in [2]. We designed a set of repair prompts
results when evaluated on the benchmark samples. This                  based on the above factors (cf. Section IV-A and Fig. 2). For each
outcome affirmed the effectiveness of the default setting for          prompt, we ran the ChatGPT repair process and collected the
ChatGPT in our specific task and led us to use it for our              resulting repairs. We evaluated the quality of the repair using the
experiments.                                                           same metrics as in our prior experiments. We also manually
                                                                       inspected the repairs to identify any major mistakes or
E. Methods                                                             hallucinations.
  This section overviews the methods we utilized to address
the four research questions.                                                          V. EXPERIMENTAL RESULTS
 1) RQ1–Comparing with the state-of-the-art techniques for
                                                                        Results for RQ1: State-of-the-art Comparison.
 Alloy specification repair: To investigate RQ1, we conducted
                                                                        In our experiments, we compared the ChatGPT-based Alloy
 a comparative analysis between ChatGPT-based Alloy repair           repair with four state-of-the-art Alloy repair tools: ATR [95],
 and four state-of-the-art Alloy repair tools: ATR [95],             ARepair [87], BeAFix [34] and ICEBAR [19]. To ensure a fair
 ARepair [87], BeAFix [34], and ICEBAR [19]. We used the             evaluation, we employed the same benchmark specifications as
 same benchmark specifications, namely the ARepair and               those used by these tools. The results of our findings are displayed
 Alloy4Fun benchmark suites, that were employed by these             in Table II. The columns labeled Models and Total #specs indicate
 tools to ensure a fair evaluation. In both benchmarks, we           the model groups and the total number of buggy specifications in
 utilized the specifications’ corresponding assertions as            each group, respectively. Each subsequent column in the table
 oracles and automatically generated test suites using AUnit         represents the total number of correctly repaired specifications by
 [84] for ARepair [88]. Recall that ARepair requires tests as        each respective tool. It is worth mentioning that each tool has a
 oracles during the repair process; we thus followed the             different development strategy and addresses specification
 procedure suggested in [88], as test cases are not commonly         attributes differently. Overall, ChatGPT was able to repair 26%
 available alongside Alloy specifications. To encompass repair       (517/1974) of the total specifications in Repair Scenario 2. This
 situations commonly explored in prior automated program             represents the best result achieved by ChatGPT in this scenario (see
 repair (APR) research, we created and executed five distinct        Fig 2). In the individual benchmarks, ChatGPT repaired 26%
                                                                                                                                                       7

TABLE II: Comparison to the state-of-the-art Alloy repair techniques, i.e., ARepair [88], ICEBAR [19], BeAFIX [34], and ATR [95], on the
ARepair and Alloy4Fun benchmarks.


                            #specs
 Alloy4Fun




              lts




              addr           1           1           1           1            1               1             0             0            0           1
              arr            2           2           2           2            1               1             1             1            0           1
              balancedBST    3           1           2           1            1               3             2             2            0           0
              bempl          1           0           1           0            1               0             1             1            1           1
              cd             2           0           2           2            2               1             1             2            0           2
   ARepair




              ctree          1           1           0           0            0               0             0             1            0           1
              dll            4           0           3           3            2               4             4             3            0           1
              farmer         1           0           0           0            0               1             0             0            0           0
              fsm            2           2           2           1            2               2             1             0            0           0
              grade          1           0           1           0            1               1             0             1            0           0
              other          1           0           0           1            1               1             0             0            1           0
              student        19          2           7           13           10             14            10            15            2           4
             Summary         38          9           21          24            22            29            20            26             4         11

               Total        1974        194        1072         1005          1308          430           517            329           151       385

TABLE III: Concurrent Representation of Similarity Metrics for ChatGPT’s Repairs in Consistency Test. ChatGPT was prompted with
ten repair prompts, each repeated ten times, and the similarity of its repairs for each prompt was measured.

                                              Instructed to Pass Assertion                          Not instructed to Pass Assertion

                       PROMPT        BLEU     ROUGE-L       METEOR           BERTSim        BLEU     ROUGE-L        METEOR       BERTSim
                           1         0.642      0.281          0               0.641        0.139      0.245           0           0.585
                           2         0.906      0.708        0.613             0.905          0          0           0.135         0.525
                           3         0.481      0.062          0               0.481          0          0           0.646         0.537
                           4         0.982      0.857        0.646             0.982          0          0           0.113           0
                           5         0.859      0.562        0.539             0.858        0.034      0.058         0.135         0.593
                           6         0.718      0.125          0               0.717          0          0           0.646           0
                           7         0.624      0.062        0.646             0.623          0          0             0             0
                           8         0.859      0.562          0               0.858        0.121      0.201         0.060         0.647
                           9         0.859      0.562          0               0.858          0          0             0           0.537
                          10         0.718      0.432          0               0.717        0.034      0.058         0.189         0.593
                        Average      0.765      0.378        0.244             0.764        0.033     0.0562         0.202         0.402

 (497/1936) of the Alloy4Fun benchmark in Repair Scenario 2 and                         • Specifications cd and dll could not be fixed by ARepair, but
 76% (29/38) of the ARepair benchmark in Repair Scenario 1. In                            ChatGPT fixed them in 4 instances.
 the overall comparison of repair scenarios 1, 2, 3, and 5, ChatGPT                     • The specification farmer remained unfixed by all four repair
 outperformed ARepair, which only had a 9% repair rate among all                          tools but was resolved by ChatGPT in Repair Scenario 1.
 the specifications. Although ChatGPT falls behind the other repair                     • Specification grade could not be fixed by ARepair and
 tools in the Alloy4Fun benchmark, except for ARepair, it achieved                        BeAFix, but ChatGPT resolved it in 2 instances.
 the best performance on the ARepair benchmark with 29 repairs                          • Specification other could not be fixed by ARepair and
 in Repair Scenario 1.                                                                    ICEBAR, but ChatGPT fixed it in 2 instances.
    While ChatGPT did not surpass the existing tools in terms of
                                                                                        Based on the results, ChatGPT exhibits inconsistent and varied
 total repairs, it demonstrated promising results by fixing unique
                                                                                     behavior across the benchmarks. While it does not consistently
 specifications that were not addressed by the previous tools. For                   outperform the existing tools, it demonstrates promise in finding
 example:                                                                            fixes for specific buggy specifications that the other tools fail to
   • Specification bempl could not be fixed by ARepair and                           address. This indicates that ChatGPT has potential for resolving
     BeAFix but was successfully repaired by ChatGPT in 4                            problematic specifications.
     instances.
                                                                                                                                       8


                                                                      Results for RQ2: Consistency of the repairs.
 Observation 1: ChatGPT can fix unique specifications that were      One potential issue with repair techniques based on LLMs is that,
 not addressed by the previous repair tools.                      given the exact prompt and faulty specification, they may not
                                                                  generate the same repairs. So we conducted a consistency check to
                                                                  evaluate ChatGPT’s reliability as a repair technique by assessing
                                                                  whether it consistently generates the same repairs given the same
                                                                  prompt and faulty specification. Ten different faulty specifications
                                                                  were used, and for each one, we provided the same repair prompt
                                                                  ten times to ChatGPT. Each prompt was given in a new chat session
                                                                  with no context, and we asked ChatGPT to satisfy the assertions for
                                                                  each of these faulty specifications: "Consider the following Alloy
                                                                  specification. There is a bug in this specification. Fix the bug so that
                                                                  it satisfies the assertions." We then conducted ten repetitions of the
                                                                  same prompt on ChatGPT for the same ten faulty specifications.
                                                                  Each prompt was again presented in a new chat session with no
                                                                  context. However, during these replications, ChatGPT was not
                                                                  explicitly requested to satisfy the assertions.
                                                                     We measured the similarity of ChatGPT’s generated repairs using
                                                                  various metrics such as BLEU, ROUGE-L, METEOR, and a BERT-
                                                                  based semantic similarity metric. The results, presented in Table III,
                                                                  show the average similarity among the ten generated repairs for
                                                                  each of the ten prompts. For instance, when ChatGPT was
                                                                  instructed to pass the assertion for prompt 1, the ten instances of
                                                                  repairs had an average score of 0.642 on BLEU, 0.281 on ROUGE-
                                                                  L, 0 on METEOR, and 0.641 on the BERT-based semantic
                                                                  similarity metric. The BERTbased semantic similarity metric is
                                                                  particularly meaningful as it evaluates repairs in a semantic space
                                                                  by converting them into BERT encodings. However, the obtained
                                                                  results indicate that ChatGPT’s responses to the same prompts are
                                                                  not highly consistent. We used Welch’s t-test [76] to check if the
                                                                  scores for “Instructed to pass assertion” and “Not instructed to pass
                                                                  assertion” are statistically significantly different or not for the same
                                                                  prompt. We decided to use Welch’s t-test because it does not assume
                                                                  equal variance between groups but only assumes normality of the
                                                                  data. Considering the multiple tests conducted, we applied the
                                                                  Bonferroni correction [35] to account for multiple hypothesis
                                                                  corrections, resulting in an adjusted p-value of 0.005. The analysis
                                                                  results revealed significant differences between all pairs of scores
                                                                  for the same prompt (Welch’s t-test, p-val<6.660e-05).

                                                                     Observation 2: ChatGPT shows inconsistency by generating
                                                                     different repairs for the same input on different executions.


                                                                     Results for RQ3: Primary Category of Mistakes.
                                                                     During our assessment of the ChatGPT’s unsuccessful repairs,
                                                                  we discovered that the responses across different repair scenarios
                                                                  contained a number of errors in the Alloy specifications. Upon
                                                                  further investigation, we identified several interesting categories of
                                                                  these mistakes. Table IV displays the categories of mistakes found
                                                                  in ChatGPT repairs across the five repair scenarios, along with their
                                                                  respective quantities and proportions within each category.

                                                                      •   Incorrect use of operator: We observed a few errors where
                                                                          incorrect operators were used. For instance, the "&"
                                                                          operator was used in certain cases where both sides of an
Fig. 3: Venn diagrams depict the comparison of ARepair,                   expression were not compatible. This mismatch resulted in a
ICEBAR, BeAFix, ATR, and ChatGPT in five different scenarios              type error. Similar issues led to other errors as well.
across two benchmark suits. The repair cases shared between
these techniques are highlighted in the overlapping regions.
                                                                                                                                            9



                              TABLE IV: Quantity and proportion of mistakes from ChatGPT repairs

                                                  Quantity and proportion of mistakes

      Type of Errors                    Scenario-1          Scenario-2          Scenario-3            Scenario-4           Scenario-5

      Wrong use of operator          336/1974 (17%)      197/1974 (10%)       278/1974 (14%)      120/1974 (6.07%)        158/1974 (8%)

      Wrong type                     450/1974 (23%)      246/1974 (12%)       424/1974 (21%)       1125/1974 (57%)       637/1974 (32%)

      Misusing higher-order logic             0 (0%)               0 (0%)              0 (0%)             1 (0.05%)                0 (0%)

      Mismatch relational arity      321/1974 (16%)      349/1974 (18%)       335/1974 (17%)        225/1974 (11%)       332/1974 (17%)

      Hallucination                   180/1974 (9%)        122/1974 (6%)       162/1974 (8%)          186/1974 (9%)      370/1974 (19%)

  • Incorrect type: This error occurred due to the presence of           but also highlight the imperfections in its assumptions. The error
    unexpected tokens such as " ", "{", and "|". We noticed these        types Incorrect use of operator and Incorrect type indicate that
    errors when the structure or arrangement of the code did not         ChatGPT’s logic representation for repairing a specification might
    conform to the grammar and rules of the Alloy                        be initially correct, but it becomes inaccurate due to the use of
    specifications, resulting in syntax errors.                          unnecessary or irrelevant operators. The errors made by ChatGPT
  • Misuse of higher-order logic: We encountered this type of            demonstrate that the repairs provided may lack reliability and
    logical error, which happened due to the absence of higher-          consistency. The categorization of errors based on each repair
    order quantification. This occurred in a single case. This           scenario can be found in Table IV.
    specific error suggests that higher-order quantification could
    not be skolemized, meaning that the process of replacing              Observation 3: ChatGPT makes different types of
    quantified variables with skolem constants or functions was           mistakes with Incorrect type being the most frequent.
    unsuccessful. Consequently, the analysis could not proceed,
    resulting in an error.
  • Mismatch in relational arity: This error occurred when a              Results for RQ4: Impact of the prompts.
    relational join was not legal or valid due to incompatible            The Venn diagrams presented in Figure 3 illustrate the outcomes
    types on the left-hand side and right-hand side of the             obtained by ChatGPT in five distinct scenarios across two
    expression. For example, consider the following expression:        benchmark suites. This depiction showcases the interrelation and
                                                                       commonality of solutions among various tools. As discussed in
                                                                       RQ1, ChatGPT demonstrates the ability to repair certain unique
      left-hand side is u.(this/User <: profile)                       faulty specifications in the ARepair benchmark suite that were not
      (type = {this/Work})                                             addressed by any of the other repair techniques. With the exception
      right-hand side is this/Work                                     of Repair Scenario 4, ChatGPT’s repairs were not entirely
      (type = {this/Work})}                                            encompassed by all the other repair techniques in the ARepair
                                                                       benchmark suite. In this specific scenario, the repairs generated by
                                                                       ChatGPT aligned completely with those produced by ICEBAR,
      In this expression, the specific relational join provided by     BeAFix, and ATR. However, the results appear inconsistent when
   ChatGPT is not valid because the left-hand side and the right-      attempting to satisfy the assertion in Repair Scenarios 3 and 5. In
   hand side have incompatible types. The left hand side involves      Repair Scenario 3, the results overlap with the other tools, while in
   the subset operator <: applied to this/User and profile, while      Repair Scenario 5, the number of correct fixes is comparatively
   the right-hand side is simply this/Work. We observed such           lower. Nonetheless, there are some distinctive fixes for specific
   issues in a large number of instances provided by ChatGPT,          specifications like bempl, cd, and dll. When considering the
   resulting in Type Errors.                                           Alloy4Fun benchmarks, the results across all repair scenarios were
   • Hallucination: This error occurred when ChatGPT referenced        found to be a subset of ICEBAR, BeAFix, and ATR. The Venn
   a variable in a predicate or fact that had not been previously      diagrams provide a clear illustration of how the impact of different
   defined or declared within the scope of the current code.           prompts has a diverse effect on the segmentation of the data and
   Based on our thorough investigation, we were able to categorize     influences ChatGPT’s responses to each scenario. Specifically, the
these mistakes across all repair scenarios. Among the error types,     obtained results reveal a significant impact of the prompt, with
the Incorrect type had the highest impact, affecting (57%) of the      Repair Scenario 4, which has the least amount of guidance
specifications in Repair Scenario 4 and (32%) in Repair Scenario       provided, performing the worst compared to all other Repair
5 across the two benchmarks. Although the Missing higher-order         Scenarios.
logic error only affected one specification, it provided significant      During the analysis of the impact of “Bug Location” information
insight into the types of mistakes that can occur with ChatGPT.        as part of the prompt, the bug location was provided in the
The error type Hallucination indicates that ChatGPT’s attempts         specification as a comment, but only in specific repair scenarios (cf.
to repair the program reflect its large-scale training capabilities,   Table I) for both benchmark suites. Notably, in the ARepair
                                                                                                                                    10

benchmark, there was clear guidance on how to fix the bug in one         Our study identifies instances of hallucinations in generated
scenario (i.e., Scenario 1), as shown in Figure 2 (Repair Scenario    repairs. Future research should focus on minimizing such
1), for instance, in the form of “replace c.ˆext with c.ˆ~ext”.       hallucinations through improved training, fine-tuning, and
However, for the Alloy4Fun benchmark, there was no explicit           validation processes. Inconsistency in the repairs generated by
instruction on how to conduct the fix. Consequently, the              ChatGPT is another area that needs attention. Ensuring more
performance of ChatGPT for the Alloy4Fun benchmark                    consistent and reliable repairs can be achieved by refining the
consistently lagged behind that of the ARepair benchmark,             model’s behavior in specific scenarios and enhancing its ability
indicating the impact of “Bug Location.”                              to produce consistent repairs to similar buggy specifications.
    When analyzing the impact of assertion information, we
                                                                         Implications for tool builders. Despite falling short in
  observed no significant impact of requiring to pass assertions in
                                                                      comparison to existing repair techniques for Alloy declarative
  the prompt. We posit that this may be attributed to ChatGPT’s
  proficiency in understanding natural language text but limited
                                                                      specifications, ChatGPT has demonstrated its ability to address
  capability in verifying logical assertions.                         certain buggy specifications that existing methods could not
                                                                      handle. This indicates that it can be used as a complementary
                                                                      tool alongside other repair techniques to improve overall
    Observation 4: Specific instruction on how to fix the bug         effectiveness. For example, a hybrid approach combining
    as part of the prompt has the most significant impact on          existing tools and ChatGPT is worth exploring.
    ChatGPT’s performance.
                                                                         Given the identified errors and inconsistencies, we posit that
                                                                      incorporating a human-in-the-loop validation step in the repair
                                                                      process with ChatGPT may be able to enhance the reliability of
           VI. DISCUSSION AND IMPLICATIONS                            the repaired specifications. Indeed, while it may be useful for
                                                                      brainstorming alternative solutions to challenging specification
   This section presents implications for tool builders,
                                                                      issues, human validation backed by the automated Alloy
 researchers, and software practitioners when considering the
                                                                      Analyzer can help verify the correctness of repairs, prevent
 use of OpenAI’s ChatGPT for automatic repair of declarative
                                                                      hallucinations from being accepted, and provide additional
 specifications.
                                                                      insights for further improvement.
    Implications for software practitioners. ChatGPT falls
 short when compared to existing techniques in terms of overall                         VII. THREATS TO VALIDITY
 effectiveness. Therefore, Alloy users should not solely rely on
 ChatGPT for all repair tasks. Rather, users should consider             We have taken all reasonable steps to mitigate potential
 ChatGPT as a supplementary tool for specification repair,            threats that could hamper the validity of this study, it is still
 particularly when other techniques have exhausted their              possible that our mitigation strategies might not have been
 capabilities or failed to address certain types of bugs, as          effective.
 indicated in Observation 1. In such cases, ChatGPT may                  ChatGPT may show better performance when being used in a
 provide alternative solutions that can be considered alongside       conversational way. That is, humans provide necessary feedback
 existing repairs.                                                    to the response ChatGPT gives so that the model can give better
    Due to identified errors in ChatGPT’s generated repairs,          results in the following rounds. However, as the first work to
 users should exercise caution and critically validate the            investigate the performance and the feasibility of ChatGPT on
 suggested repairs. Specifically, users should be aware of            repairing specification bugs, we believe our analysis sheds light
 potential issues like improper operator usage, type errors,          on how good ChatGPT fixes specification bugs in Alloy.
 higher-order logic misuse, relational arity mismatches, and             It is possible that our manual labeling process for identifying
 hallucinations when relying on ChatGPT for specification             the categories could have introduced unintentional bias. To
 repairs. The most frequent errors observed are related to the        address this, two authors inspected and labeled independently. A
 wrong use of operators and types. This occurrence can be             Cohen kappa of 0.95 indicates a high reliability of our labeling.
 attributed, in part, to Alloy’s alternative syntax for various          Our conclusions may not be generalizable to Alloy problems
 logic operators (e.g., ‘and’ for conjunction) and the syntactic      that are not included in the two benchmarks we experimented in
 similarities between certain logical and relational operators        this study.
 (e.g., ‘not’ for negation vs. ‘no’ for emptiness check, ‘&&’ for
 conjunction vs. ‘&’ for intersection). Manually reviewing and                            VIII. CONCLUSION
 verifying the repairs is essential to ensure their correctness and      To aid programmers in rectifying mistakes in specifications
 reliability.                                                         and promote the adoption of formal specifications in day-today
   Implications for researchers. Our study highlights that            software engineering, various automatic repair approaches have
 ChatGPT can fix unique specifications that were not addressed        recently been proposed. Despite notable progress, these
 by state-of-the-art repair tools. This suggests that ChatGPT         approaches exhibit certain limitations. Recently introduced,
 might be particularly useful for niche or specific buggy             ChatGPT, a large language model, can generate fixes for bugs in
 specifications that might be challenging for conventional            specifications based on provided prompts and related Alloy
 repair approaches. Further exploration and understanding of          specifications.
 the types of buggy specifications ChatGPT is most effective at           Our findings reveal that while ChatGPT is not able to
 repairing can help in optimizing its use.                              perform on par with the existing techniques, it demonstrates
                                                                                                                                                                11


 surprising capability in repairing bugs that other techniques                      [18] S. G. Brida, G. Regis, G. Zheng, H. Bagheri, T. Nguyen, N. Aguirre, and
                                                                                         M. F. Frias, “Beafix: An automated repair tool for faulty alloy models,” in
 fail to address. However, our results also identify some
                                                                                         36th IEEE/ACM International Conference on Automated Software
 mistakes made by ChatGPT, including incorrect operator                                  Engineering, ASE 2021, Melbourne, Australia, November 15-19, 2021,
 usage, incorrect types, misuse of higher-order logic, and                               pp. 1213–1217.
 relational arity mismatches. Additionally, we observed                             [19] ——, “ICEBAR: feedback-driven iterative repair of alloy specifications,”
                                                                                         in 37th IEEE/ACM International Conference on Automated Software
 instances of hallucination in the generated repairs. The
                                                                                         Engineering, ASE 2022. ACM, pp. 55:1–55:13.
 findings of this study offer valuable insights for tool builders,                  [20] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A.
 researchers, and software practitioners who are contemplating                           Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language models are
 the utilization of ChatGPT for automatic repair of declarative                          few-shot learners,” Advances in neural information processing systems,
                                                                                         vol. 33, pp. 1877–1901, 2020.
 specifications.
                                                                                    [21] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H.
    The data collected and statistical analyses conducted in this                        Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
 study have been made publicly available on the project website                          language models trained on code,” arXiv:2107.03374, 2021.
 [1] to ensure the verifiability and reproducibility of our                         [22] A. M. Dai and Q. V. Le, “Semi-supervised sequence learning,” Advances
 findings.                                                                               in neural information processing systems, vol. 28, 2015.
                                                                                    [23] V. Dallmeier, A. Zeller, and B. Meyer, “Generating fixes from object
                                                                                         behavior anomalies,” in Proceedings of the 2009 IEEE/ACM International
                                                                                         Conference on Automated Software Engineering, ser. ASE ’09, USA,
                               REFERENCES                                                2009, p. 550–554.
                                                                                    [24] V. Debroy and W. E. Wong, “Using mutation to automatically suggest
  [1]    “Project website,” https://sites.google.com/view/alloy-repair/home.             fixes for faulty programs,” in Software Testing, Verification and
  [2]    “Prompt        engineering,”                                                    Validation. IEEE, 2010, pp. 65–74.
            https://help.openai.com/en/articles/     6654000-best-practices-for-    [25] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pretraining of
         prompt-engineering-with-openai-api.                                             deep bidirectional transformers for language understanding,”
   [3] D. Jackson, Software Abstractions. MIT Press, 2012.                               arXiv:1810.04805, 2018.
   [4] “Excape project,” https://excape.cis.upenn.edu/, 2020.                       [26] Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng, M. Gong, L. Shou, B. Qin,
   [5] “Sygus,” https://sygus.org/, 2020.                                                T. Liu, D. Jiang et al., “Codebert: A pre-trained model for programming
   [6] M. Alhanahnah, C. Stevens, and H. Bagheri, “Scalable analysis of                  and natural languages,” arXiv:2002.08155, 2020.
         interaction threats in iot systems,” in ISSTA’20: 29th ACM SIGSOFT,        [27] J. Forman and L. Damschroder, “Qualitative content analysis,” in
         pp. 272–285.                                                                    Empirical methods for bioethics: A primer. Emerald Group Publishing
                                                                                         Limited, 2007.
   [7] P. Attie, A. Cherri, K. D. Al Bab, M. Sakr, and J. Saklawi, “Model and
         program repair via sat solving,” in MEMOCODE. IEEE, 2015, pp. 148–         [28] J. P. Galeotti, N. Rosner, C. G. Lopez Pombo, and M. F. Frias, “TACO:
         157.                                                                            Efficient SAT-Based Bounded Verification Using Symmetry Breaking and
                                                                                         Tight Bounds,” IEEE Transactions on Software Engineering, vol. 39, no.
   [8] H. Bagheri, E. Kang, S. Malek, and D. Jackson, in FM 2015: Formal
                                                                                         9, pp. 1283–1307, Sep. 2013.
         Methods, 2015, vol. 9109, pp. 73–89.
                                                                                    [29] B. G. Glaser, “Open coding descriptions,” Grounded theory review, vol.
   [9] ——, “Detection of design flaws in the androidecurity flaws in the
                                                                                         15, no. 2, pp. 108–110, 2016.
         android permission system,” Formal Aspects of Computing, vol. 30, no.
         5, pp. 525–544, 2018.                                                      [30] D. Gopinath, M. Z. Malik, and S. Khurshid, “Specification-based program
   [10] H. Bagheri, E. Kang, and N. Mansoor, “Synthesis of assurance cases               repair using SAT,” in Tools and Algorithms for the Construction and
         for software certification,” in ICSE-NIER 2020: 42nd International              Analysis of Systems - 17th International Conference, TACAS 2011, vol.
         Conference on Software Engineering, New Ideas and Emerging Results,             6605.             Springer, 2011, pp. 173–188.
         Seoul, South Korea, 27 June - 19 July, 2020. ACM, pp. 61–64.               [31] S. Gulwani, “Automating string processing in spreadsheets using
   [11] H. Bagheri, A. Sadeghi, R. Jabbarvand, and S. Malek, “Practical,                 inputoutput examples,” in POPL. ACM, 2011, pp. 317–330.
         formal synthesis and automatic enforcement of security policies for        [32] S. Gulwani, W. R. Harris, and R. Singh, “Spreadsheet data manipulation
         android,” in Proceedings of DSN, 2016, pp. 514–525.                             using examples,” Commun. ACM, vol. 55, pp. 97–105, Aug. 2012.
   [12] H. Bagheri and K. Sullivan, “Pol: Specification-driven synthesis of         [33] D. Guo, S. Ren, S. Lu, Z. Feng, D. Tang, S. Liu, L. Zhou, N. Duan, A.
         architectural code frameworks for platform-based applications,” in              Svyatkovskiy, S. Fu et al., “Graphcodebert: Pre-training code
         Proceedings of the 11th ACM International Conference on Generative              representations with data flow,” arXiv preprint arXiv:2009.08366, 2020.
         Programming and Component Engineering (GPCE’12). Dresden,                  [34] S. Gutiérrez Brida, G. Regis, G. Zheng, H. Bagheri, T. Nguyen, N.
         Germany: ACM, 2012, pp. 93–102.                                                 Aguirre, and M. Frias, “Bounded exhaustive search of alloy specification
   [13] ——, “Model-driven synthesis of formally precise, stylized software               repairs,” in Proceedings of the 43rd ACM/IEEE International Conference
         architectures,” Formal Aspects of Computing, vol. 28, no. 3, pp. 441–           on Software Engineering ICSE 2021, Virtual.
         467, Mar. 2016.                                                            [35] W. Haynes, “Bonferroni correction,” in Encyclopedia of Systems Biology.
   [14] H. Bagheri, C. Tang, and K. Sullivan, “Trademaker: Automated                     Springer, 2013, pp. 154–154.
         dynamic analysis of synthesized tradespaces,” in Proceedings of the        [36] D. Jackson, Software Abstractions - Logic, Language, and Analysis. MIT
         36th International Conference on Software Engineering, ser. ICSE                Press, 2006.
         2014. New York, NY, USA: ACM, 2014, pp. 106–116.                           [37] D. Jackson, I. Shlyakhter, and M. Sridharan, “A micromodularity
   [15] H. Bagheri, J. Wang, J. Aerts, N. Ghorbani, and S. Malek, “Flair:                mechanism,” in Proceedings of the 8th European Software Engineering
         efficient analysis of android inter-component vulnerabilities in                Conference Held Jointly with 9th ACM SIGSOFT International
         response to incremental changes,” Empir. Softw. Eng., vol. 26, no. 3, p.        Symposium on Foundations of Software Engineering, ser. ESEC/FSE-9.
         54, 2021. [16] Y. Bang, S. Cahyawijaya, N. Lee, W. Dai, D. Su, B.               New York, NY, USA: ACM, 2001, pp. 62–73.
         Wilie, H. Lovenia, Z. Ji, T. Yu, W. Chung et al., “A multitask,            [38] G. Jin, L. Song, W. Zhang, S. Lu, and B. Liblit, “Automated
         multilingual, multimodal evaluation of chatgpt on reasoning,                    atomicityviolation fixing,” SIGPLAN Not., vol. 46, no. 6, p. 389–400, Jun.
         hallucination, and interactivity,” arXiv preprint arXiv:2302.04023,             2011.
         2023.                                                                      [39] B. Jobstmann, A. Griesmayer, and R. Bloem, “Program repair as a game,”
[17] R. Bloem, R. Drechsler, G. Fey, A. Finder, G. Hofferek, R. Könighofer, J.           in Computer Aided Verification, 2005, pp. 226–238.
      Raik, U. Repinski, and A. Sülflow, “Forensic– an automatic debugging          [40] A. Kashefi and T. Mukerji, “Chatgpt for programming numerical
      environment for c programs,” in Hardware and Software: Verification and            methods,” arXiv preprint arXiv:2303.12093, 2023.
      Testing. Berlin, Heidelberg: Springer Berlin Heidelberg, 2013, pp.            [41] S. Khurshid and D. Marinov, “Testera: Specification-based testing of java
       260–265.                                                                          programs using sat,” Automated Software Engineering, vol. 11, 2004.
                                                                                                                                                              12

[42] D. Kim, J. Nam, J. Song, and S. Kim, “Automatic patch generation learned     [60] S. Mechtaev, J. Yi, and A. Roychoudhury, “Angelix: Scalable multiline
     from human-written patches,” in 35th International Conference on                  program patch synthesis via symbolic analysis,” in Proceedings of the
     Software Engineering, ICSE ’13, San Francisco, CA, USA, May 1826,                 38th International Conference on Software Engineering, ser. ICSE ’16,
     2013, pp. 802–811.                                                                2016, p. 691–701.
[43] J. S. Kim and D. Garlana, “Analyzing architectural styles,” Journal of       [61] A. Mesbah, A. Rice, E. Johnston, N. Glorioso, and E. Aftandilian,
     Systems and Software, vol. 83, no. 7, pp. 1216–1235, 2010.                        “Deepdelta: Learning to repair compilation errors,” ser. ESEC/FSE, 2019,
[44] A. Koyuncu, K. Liu, T. F. Bissyandé, D. Kim, J. Klein, M. Monperrus, and          p. 925–936.
     Y. Le Traon, “Fixminer: Mining relevant fix patterns for automated           [62] N. Mirzaei, J. Garcia, H. Bagheri, A. Sadeghi, and S. Malek, “Reducing
     program repair,” Empirical Software Engineering, pp. 1–45, 2020.                  combinatorics in gui testing of android applications,” in Proceedings
[45] A. Koyuncu, K. Liu, T. F. Bissyandé, D. Kim, M. Monperrus, J. Klein, and          ICSE, 2016, pp. 559–570.
     Y. Le Traon, “Ifixr: Bug report driven program repair,” in Proceedings of    [63] J. P. Near and D. Jackson, “Derailer: Interactive security analysis for web
     the 2019 27th ACM Joint Meeting on European Software Engineering                  applications,” ser. ASE ’14, pp. 587–598.
     Conference and Symposium on the Foundations of Software Engineering,         [64] T. Nelson, C. Barratt, D. J. Dougherty, K. Fisler, and S. Krishnamurthi,
     p. 314–325.                                                                       “The margrave tool for firewall analysis,” in Uncovering the Secrets of
[46] X.-B. D. Le, D.-H. Chu, D. Lo, C. Le Goues, and W. Visser, “S3:                   System Administration: Proceedings of the 24th Large Installation System
     Syntaxand semantic-guided repair synthesis via programming by                     Administration Conference, LISA, 2010.
     examples,” in Proceedings of the 2017 11th Joint Meeting on Foundations      [65] H. D. T. Nguyen, D. Qi, A. Roychoudhury, and S. Chandra, “Semfix:
     of Software Engineering, ser. ESEC/FSE 2017, p. 593–604.                          Program repair via semantic analysis,” in 2013 35th International
[47] C. Le Goues, T. Nguyen, S. Forrest, and W. Weimer, “Genprog: A generic            Conference on Software Engineering (ICSE), 2013, pp. 772–781.
     method for automatic software repair,” IEEE Trans. Software Eng., vol.       [66] T. Nguyen, W. Weimer, D. Kapur, and S. Forrest, “Connecting program
     38, no. 1, pp. 54–72, 2012.                                                       synthesis and reachability: Automatic program repair using test-input
[48] M. Lewis, Y. Liu, N. Goyal, M. Ghazvininejad, A. Mohamed, O. Levy, V.             generation,” in International Conference on Tools and Algorithms for the
     Stoyanov, and L. Zettlemoyer, “Bart: Denoising sequence-to-sequence               Construction and Analysis of Systems’17. Springer, pp. 301–318.
     pre-training for natural language generation, translation, and               [67] J. Nijjar and T. Bultan, “Bounded verification of ruby on rails data
     comprehension,” arXiv preprint arXiv:1910.13461, 2019.                            models,” in Proceedings of the 2011 International Symposium on Software
[49] T.-O. Li, W. Zong, Y. Wang, H. Tian, Y. Wang, and S.-C. Cheung, “Finding          Testing and Analysis, ser. ISSTA ’11, pp. 67–77.
     failure-inducing test cases with chatgpt,” arXiv preprint                    [68] T. OpenAI, “Chatgpt: Optimizing language models for dialogue,” OpenAI,
     arXiv:2304.11686, 2023.                                                           2022.
[50] X. Li, D. Shannon, J. Walker, S. Khurshid, and D. Marinov, “Analyzing        [69] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C.
     the uses of a software modeling tool,” in Proceedings of the Sixth                Zhang, S. Agarwal, K. Slama, A. Ray et al., “Training language models to
     Workshop on Language Descriptions, Tools, and Applications,                       follow instructions with human feedback,” 2022.
     LDTA@ETAPS 2006, Vienna, Austria, April 1, 2006, ser. Electronic Notes       [70] P. Ponzio, N. Aguirre, M. F. Frias, and W. Visser, “Field-exhaustive
     in Theoretical Computer Science, J. Boyland and A. Sloane, Eds., vol. 164,        Testing,” in Proceedings of the 2016 24th ACM SIGSOFT International
     no.     2.    Elsevier,   2006,    pp.     3–18.    [Online]. Available:          Symposium on Foundations of Software Engineering, ser. FSE 2016. New
     https://doi.org/10.1016/j.entcs.2006.10.001                                       York, NY, USA: ACM, 2016, pp. 908–919.
[51] Y. Li, S. Wang, and T. N. Nguyen, “Dlfix: Context-based code                 [71] A. Radford, K. Narasimhan, T. Salimans, I. Sutskever et al., “Improving
     transformation learning for automated program repair,” in Proceedings of          language understanding by generative pre-training,” 2018.
     the ACM/IEEE 42nd International Conference on Software Engineering,          [72] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou,
     ser. ICSE ’20, 2020, p. 602–614.                                                  W. Li, and P. J. Liu, “Exploring the limits of transfer learning with a
[52] P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, and G. Neubig, “Pretrain,           unified text-to-text transformer,” The Journal of Machine Learning
     prompt, and predict: A systematic survey of prompting methods in natural          Research, vol. 21, no. 1, pp. 5485–5551, 2020.
     language processing,” ACM Computing Surveys, vol. 55, no. 9, pp. 1–35,       [73] G. Recchia, “Teaching autoregressive language models complex tasks by
     2023.                                                                             demonstration,” arXiv preprint arXiv:2109.02102, 2021.
[53] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L.    [74] N. Rosner, J. Galeotti, S. Bermudez, G. M. Blas, S. P. D. Rosso, L.
     Zettlemoyer, and V. Stoyanov, “Roberta: A robustly optimized bert                 Pizzagalli, L. Zemin, and M. F. Frias, “Parallel bounded analysis in code
     pretraining approach,” arXiv preprint arXiv:1907.11692, 2019.                     with rich invariants by refinement of field bounds,” in Proceedings of the
[54] F. Long and M. Rinard, “Automatic patch generation by learning correct            International Symposium on Software Testing and Analysis (ISSTA), 2013,
     code,” ser. POPL ’16. New York, NY, USA: Association for Computing                pp. 23–33.
     Machinery, 2016, p. 298–312.                                                 [75] N. Ruchansky and D. Proserpio, “A (not) NICE way to verify the openflow
[55] N. Macedo, A. Cunha, J. Pereira, R. Carvalho, R. Silva, A. C. R. Paiva, M.        switch specification: formal modelling of the openflow switch using
     S. Ramalho, and D. C. Silva, “Experiences on teaching alloy with an               alloy,” in August 12-16, 2013. ACM, 2013, pp. 527–528.
     automated assessment platform,” vol. 12071. Springer, 2020, pp. 61–77.       [76] G. D. Ruxton, “The unequal variance t-test is an underused alternative to
[56] F. A. Maldonado-Lopez, J. Chavarriaga, and Y. Donoso, “Detecting                  student’s t-test and the mann–whitney u test,” Behavioral Ecology, vol.
     network policy conflicts using alloy,” in Abstract State Machines, Alloy,         17, no. 4, pp. 688–690, 2006.
     B, TLA, VDM, and Z - 4th International Conference, ABZ, ser. Lecture         [77] B. R. Schmerl, J. Gennari, A. Sadeghi, H. Bagheri, S. Malek, J. Cámara,
     Notes in Computer Science, vol. 8477. Springer, 2014, pp. 314–317.                and D. Garlan, “Architecture modeling and analysis of security in android
[57] N. Mansoor, H. Bagheri, E. Kang, and B. Sharif, “An empirical study               systems,” in Software Architecture - 10th European Conference, ECSA
     assessing software modeling in alloy,” in 11th IEEE/ACM International             2016, 2016, pp. 274–290.
     Conference on Formal Methods in Software Engineering, FormaliSE              [78] D. Shao, S. Khurshid, and D. Perry, “Whispec: White-box testing of
     2023, Melbourne, Australia, May 14-15, 2023. IEEE, 2023, pp. 44–54.               libraries using declarative specifications,” in Proc. of LCSD’07, 2007.
     [Online].        Available:      https://doi.org/10.1109/FormaliSE58978.     [79] R. Singh, S. Gulwani, and A. Solar-Lezama, “Automated feedback
     2023.00013                                                                        generation for introductory programming assignments,” in PLDI. ACM,
[58] N. Mansoor, J. A. Saddler, B. V. R. e Silva, H. Bagheri, M. B. Cohen, and         2013, pp. 15–26.
     S. Farritor, “Modeling and testing a family of surgical robots: an           [80] A. Solar-Lezama, “Program sketching,” Int. J. Softw. Tools Technol.
     experience report,” in Proceedings of the 2018 ACM Joint Meeting on               Transf., vol. 15, no. 5-6, pp. 475–495, 2013.
     European Software Engineering Conference and Symposium on the
                                                                                  [81] S. Srivastava, S. Gulwani, and J. S. Foster, “From program verification to
     Foundations of Software Engineering, ESEC/SIGSOFT FSE, Lake Buena
                                                                                       program synthesis,” in POPL.             ACM, 2010, pp. 313–326.
     Vista, FL, USA. ACM, 2018, pp. 785–790.
                                                                                  [82] ——, “Template-based program verification and program synthesis,” Soft.
[59] D. Marinov and S. Khurshid, “Testera: A novel framework for automated
                                                                                       Tools for Technol. Transfer, vol. 15, no. 5-6, pp. 497–518, 2013.
     testing of java programs,” in Proceedings of the IEEE International
                                                                                  [83] C. Stevens and H. Bagheri, “Reducing run-time adaptation space via
     Conference on Automated Software Engineering, 2001.
                                                                                       analysis of possible utility bounds,” in ICSE ’20. ACM, 2020, pp. 1522–
                                                                                       1534.
                                                                                  13

[84] A. Sullivan, K. Wang, and S. Khurshid, “Aunit: A test automation tool for
     alloy,” in 11th IEEE International Conference on Software Testing,
     Verification and Validation, ICST 2018, Västerås, Sweden, April 9-13,
     2018. IEEE Computer Society, 2018, pp. 398–403.
[85] E. Torlak, M. Taghdiri, G. Dennis, and J. P. Near, “Applications and
     extensions of alloy: past, present and future,” Mathematical Structures in
     Computer Science, vol. 23, no. 4, pp. 915–933, 2013.
[86] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
     Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” Advances in
     neural information processing systems, vol. 30, 2017.
[87] K. Wang, A. Sullivan, and S. Khurshid, “Automated model repair for
     alloy,” in Proceedings of the 33rd ACM/IEEE International Conference on
     Automated Software Engineering, ASE 2018, Montpellier, France,
     September 3-7, 2018. ACM, 2018, pp. 577–588.
[88] ——, “Arepair: a repair framework for alloy,” in Proceedings of the 41st
     International Conference on Software Engineering: Companion
     Proceedings, ICSE 2019, Montreal, QC, Canada, May 25-31, 2019. IEEE
     / ACM, 2019, pp. 103–106.
[89] K. Wang, A. Sullivan, D. Marinov, and S. Khurshid, “Fault localization
     for declarative models in alloy,” in 31st IEEE International Symposium on
     Software Reliability Engineering, ISSRE 2020, Coimbra, Portugal,
     October 12-15, 2020. IEEE, 2020, pp. 391–402.
[90] Y. Wang, W. Wang, S. Joty, and S. C. Hoi, “Codet5: Identifier-aware
     unified pre-trained encoder-decoder models for code understanding and
     generation,” arXiv preprint arXiv:2109.00859, 2021.
[91] C. S. Xia and L. Zhang, “Keep the conversation going: Fixing 162 out of
     337 bugs for $0.42 each using chatgpt,” arXiv preprint arXiv:2304.00385,
     2023.
[92] F. F. Xu, U. Alon, G. Neubig, and V. J. Hellendoorn, “A systematic
     evaluation of large language models of code,” in MAPS@PLDI 2022: 6th
     ACM SIGPLAN International Symposium on Machine Programming, San
     Diego, CA, USA, 13 June 2022, S. Chaudhuri and C. Sutton, Eds. ACM,
     2022, pp. 1–10.
[93] G. Zheng, H. Bagheri, and T. Nguyen, “Debugging declarative models in
     alloy,” in IEEE International Conference on Software Maintenance and
     Evolution, ICSME 2020, Adelaide, Australia, September 28 - October 2,
     2020. IEEE, 2020, pp. 844–848.
[94] G. Zheng, Q. Loc Le, T. Nguyen, and Q.-S. Phan, “Automatic data
     structure repair using separation logic,” SIGSOFT Softw. Eng. Notes, vol.
     43, no. 4, p. 66, Jan. 2019.
[95] G. Zheng, T. Nguyen, S. G. Brida, G. Regis, N. Aguirre, M. F. Frias, and
     H. Bagheri, “ATR: template-based repair for alloy specifications,” in
     ISSTA ’22: 31st ACM SIGSOFT International Symposium on Software
     Testing and Analysis, Virtual Event, South Korea, July 18 - 22, 2022, S.
     Ryu and Y. Smaragdakis, Eds. ACM, 2022, pp. 666–677.
[96] D. M. Ziegler, N. Stiennon, J. Wu, T. B. Brown, A. Radford, D. Amodei,
     P. Christiano, and G. Irving, “Fine-tuning language models from human
     preferences,” arXiv preprint arXiv:1909.08593, 2019.
