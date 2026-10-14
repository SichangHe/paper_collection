                                        Test-Oriented Programming: rethinking coding for the GenAI era
                                                                                                                    Jorge Melegati
                                                                                                              melegati@fe.up.pt
                                                                                                       INESC TEC, Faculty of Engineering
                                                                                                              University of Porto
                                                                                                               Porto, Portugal

                                        Abstract                                                                                similar to the emergence of high-level languages, e.g., C, that in-
                                        Large language models (LLMs) have shown astonishing capability                          creased the abstraction level of assembly instructions. To this aim,
                                        of generating software code, leading to its use to support developers                   we propose Test-Oriented Programming (TOP), a novel par-
                                        in programming. Proposed tools have relied either on assistants for                     adigm consisting of the complete delegation of code generation
                                                                                                                                based on natural language specifications, in which developers are
arXiv:2604.08102v1 [cs.SE] 9 Apr 2026




                                        improved auto-complete or multi-agents, in which different model
                                        instances are orchestrated to perform parts of a problem to reach a                     only responsible for verifying test code to solve the ambiguity issue
                                        complete solution. We argue that LLMs can enable a higher-level of                      of natural languages. To assess the feasibility of our proposal, we
                                        abstraction, a new paradigm we called Test-Oriented Programming                         developed Onion, a proof-of-concept tool that implements systems
                                        (TOP). Within this paradigm, developers only have to check test                         in Python based on configuration files. Using Onion, a developer
                                        code generated based on natural language specifications, rather                         only needs to checks and, if needed, modifies configuration files
                                        than focusing on production code, which could be delegated to the                       and test code. We evaluated the capacity of the tool for generating
                                        LLMs. To evaluate the feasibility of this proposal, we developed a                      a proposed system when relying on different LLM models. In this
                                        proof-of-concept tool and used it to generate a small command-line                      process, we also identified challenges to be overcome to take this
                                        program employing two different LLMs. We obtained promising                             paradigm to real projects.
                                        results and identified challenges for the use of this paradigm for
                                        real projects.                                                                          2    Test-Oriented Programming
                                                                                                                                Current research and practice have explored the use of GenAI
                                        CCS Concepts                                                                            for SE. Initially, coding assistants, e.g., GitHub Copilot, were inte-
                                        • Software and its engineering → Software creation and man-                             grated in IDEs to generate snippets of code, complete functions or
                                        agement.                                                                                classes based on natural-language descriptions or function signa-
                                                                                                                                tures. More recently, multiple agents [3], i.e., different instances
                                        Keywords                                                                                of LLMs, perform specific tasks towards a common goal. Finally,
                                        AI4SE, generative artificial intelligence, test-oriented programming                    the term “vibe coding” represents a development workflow based
                                                                                                                                on a conversational process between the developer and a chatbot.
                                        ACM Reference Format:                                                                   However, these proposals do not change the level of abstraction of
                                        Jorge Melegati. 2026. Test-Oriented Programming: rethinking coding for
                                                                                                                                programming since the output is still in conventional programming
                                        the GenAI era. In 2026 IEEE/ACM 48th International Conference on Software
                                        Engineering (ICSE-Companion ’26), April 12–18, 2026, Rio de Janeiro, Brazil.
                                                                                                                                languages to be checked by developers.
                                        ACM, New York, NY, USA, 2 pages. https://doi.org/10.1145/3774748.3795666                    To reach higher levels of abstraction, a reasonable candidate
                                                                                                                                would be natural languages, which, however, suffer from ambigu-
                                                                                                                                ities. In conventional programming languages, these ambiguities
                                        1    Introduction
                                                                                                                                are solved by formal specifications. Another issue is the lack of
                                        The emergence of more powerful large language models (LLMs) em-                         determinism of LLMs, for which a mitigation strategy being ex-
                                        ployed for Generative AI (GenAI) promises to increase developers’                       plored is the Assured LLM-based Software Engineering [1]. This
                                        productivity and to improve the quality of produced software [2].                       approach consists of the application of LLMs to SE in which all
                                        To achieve this aim, current approaches include auto-complete as-                       LLM responses come “with some verifiable claim to its utility” [1].
                                        sistants, such as Github Copilot, vibe coding, or the use of multiple                   For example, test-driven development (TDD) can be employed to
                                        agents. However, these approaches still require the inspection of                       guarantee that there exists a way to verify the generated code [5].
                                        production code by developers which, despite the increased speed of                         We argue that the combination of LLMs and TDD represents a
                                        code generation, do not represent an increased level of abstraction.                    higher-level programming paradigm, which we call Test-Oriented
                                           We argue that GenAI allows the increase of the abstraction level                     Programming (TOP). TOP is based on creating code for automatic
                                        of software development, i.e., instructions could be given to the                       tests (test code), which, alongside natural language specifications,
                                        machine in a language closer to natural languages. This shift is                        is used to automatically generate production code. It represents
                                                                                                                                an increased abstraction level of programming by completely au-
                                                                                                                                tomatizing the creation of production code, which was previously
                                        This work is licensed under a Creative Commons Attribution 4.0 International License.   performed by developers. TOP is related to several existent con-
                                        ICSE-Companion ’26, Rio de Janeiro, Brazil                                              cepts in SE, therefore it is essential to discuss its novelty. First, even
                                        © 2026 Copyright held by the owner/author(s).
                                        ACM ISBN 979-8-4007-2296-7/2026/04                                                      though TOP is also based on the idea of having tests created before
                                        https://doi.org/10.1145/3774748.3795666                                                 production code as TDD, it proposes another level of programming
ICSE-Companion ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                      Jorge Melegati


abstraction which is not the case for TDD in which tests and produc-        failed the same tests. For GPT-4o-mini, just in one try, we had to
tion code stay at the same level. This shift is only possible thanks to     modify the test code before checking the implementation. This issue
the automatic generation of code enabled by GenAI. Second, TOP              happened more often with the Gemini 2.5-Flash model, however,
aims to be a generic paradigm suitable to any problem, requiring            these issues were more related to supporting code, such as class
trained developers capable of inspecting test code and, as such, is         imports or test execution. A possible explanation for these issues is
not equivalent of low-code development tools, that are adequate             the fact that prompts had been optimized for another model.
for citizen developers but tailored for specific contexts.                     The speed and amount of test code, especially for the Gemini
                                                                            2.5-Flash model, represent a challenge for the developer responsible
3    Preliminary results                                                    for checking it. In some tries, the fact that the model was not able
To evaluate the feasibility and identify potential challenges to im-        to generate code that fulfilled the tests prompted the developer to
plement TOP, we developed a proof-of-concept tool called Onion.             check the test code, identifying issues on it and fixing it. This issue
It is an iterative, command-line tool that, based on a configuration        indicates the need for automatic tools to support the developer in
file following a pre-defined template in YAML, generates code by            the verification of the test code as summarized in the following
interacting with a LLM with pre-defined prompts and with the de-            challenge: the amount of the generated test code represents a
veloper, responsible for verifying the test code. The configuration         challenge for developers verifying it. We also observed the issue
file contains, as lists of natural language statements, i) a description    of the lack of determinism of LLMs in the generation of production
of the project describing several details of system, including its goal,    and test code: most of the tries led to the generation of different out-
library dependencies, and outputs and ii) the description of accep-         puts. In summary, for the same model, there is some variability
tance tests. Based on this information, the tool generates a structure      of the generated code. Finally, we observed a large difference of
file, also in YAML, containing the description of all the packages          the generated code: the ones created by GPT-4o-mini were shorter
to be created and their classes and respective methods. This file           and had less comments, while the ones created by Gemini 2.5-Flash
could be changed by the developer. Then, the tool creates a file            were longer and contained several comments. This issue can be
containing the acceptance tests and, for each class, a file containing      related to the increased verbosity observed in reasoning models [4].
tests. The developer verifies these files and, if needed, modify them.      This observation leads us to the following challenge: there is a
The execution of the tests are then used to generate the code of the        huge difference to the generated code for different models.
classes. If, after a defined number of tries, the generation fails, the
tool aborts and the developer should modify the tests, the structure        4    Discussion and Conclusion
or even the main configuration file. Once all the classes’ tests pass,      Onion is a proof-of-concept and, at the current stage of develop-
the acceptance tests are run and used to generate the main file of          ment, not adequate for the development of a real, complex system.
the system. The prompts used in the process were defined through            We expect that more complex systems would need to be broken
an iterative process to allow the completion of the task when using         into modules, which in their turn could be generated by the tool.
OpenAI’s GPT-4o-mini. The tool is available here1 .                         For example, in a microservices architecture, each microservice
    To evaluate the tool, we employed it to generate a command-line         could be a Onion project. However, our evaluation already brings
tool to handle BibTEXentries, persisting them into a pre-defined file,      pieces of evidence to support the feasibility of TOP: i) the automatic
with options to add entries, list all the entries and search for specific   generation of production code based on test code without human
text in the entries. We employed two different LLMs: OpenAI’s GPT-          intervention, and ii) of test code based on specifications with mini-
4o mini and Google’s Gemini 2.5-Flash, to compare a reasoning and           mal human intervention. We also identified three challenges that
a non-reasoning model.                                                      need to be handled to employ TOP in real projects.
    First, we used the tool to generate a structure configuration file
containing all the classes and the respective methods, which we             References
accepted without changes. Then, keeping the structure unchanged,            [1] Nadia Alshahwan, Mark Harman, Inna Harper, Alexandru Marginean, Shubho
                                                                                Sengupta, and Eddy Wang. 2024. Assured Offline LLM-Based Software Engineering.
we generated the production code five times for each LLM from                   In Proceedings of the ACM/IEEE 2nd International Workshop on Interpretability,
scratch, interacting with the tool as needed. For each run, we col-             Robustness, and Benchmarking in Neural Software Engineering, Vol. 1. ACM, New
lected the interactions needed to complete the tasks, the generated             York, NY, USA, 7–12.
                                                                            [2] Angela Fan, Beliz Gokkaya, Mark Harman, Mitya Lyubarskiy, Shubho Sengupta,
code and all the logs, including the prompts sent to the models. All            Shin Yoo, and Jie M. Zhang. 2023. Large Language Models for Software Engineering:
this data is available as a supplemental package2 .                             Survey and Open Problems. In 2023 IEEE/ACM International Conference on Software
                                                                                Engineering: Future of Software Engineering (ICSE-FoSE). IEEE, 31–53.
    All the tries were successful but with different levels of developer    [3] Junda He, Christoph Treude, and David Lo. 2025. LLM-Based Multi-Agent Systems
intervention and code quality. In none of the tries, we had to directly         for Software Engineering: Literature Review, Vision, and the Road Ahead. ACM
modify the production code. In most of the tries, the generation                Transactions on Software Engineering and Methodology 34, 5 (jun 2025), 1–30.
                                                                            [4] Joonwon Jang, Jaehee Kim, Wonbin Kweon, Seonghyeon Lee, and Hwanjo Yu. 2025.
of the production code failed because of inconsistencies in the test            Verbosity-Aware Rationale Reduction: Sentence-Level Rationale Reduction for
code. Once we fixed these issues, the production code was correctly             Efficient and Effective Reasoning. In Findings of the Association for Computational
implemented. However, in two tries, one for each model, we had                  Linguistics: ACL 2025. Association for Computational Linguistics, Stroudsburg, PA,
                                                                                USA, 20769–20784.
to add comments in the test code to guide the generation of the             [5] Moritz Mock, Jorge Melegati, and Barbara Russo. 2025. Generative AI for Test
production code since the models were always creating code which                Driven Development: Preliminary Results. In Agile Processes in Software Engineer-
                                                                                ing and Extreme Programming – Workshops. Springer Nature Switzerland, Cham,
                                                                                24–32.
1 https://github.com/TOProgramming/onion
2 https://doi.org/10.5281/zenodo.17227298
