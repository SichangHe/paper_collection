                                                 FormalSpecCpp: A Dataset of C++ Formal
                                                     Specifications created using LLMs
                                                            Madhurima Chakraborty∗                                         Peter Pirkelbauer, Qing Yi
                                                               mchak009@ucr.edu                                        pirkelbauer2@llnl.gov, yi7@llnl.gov
                                                        University of California, Riverside                       Lawrence Livermore National Laboratory (LLNL)
                                                                     CA, USA                                                        CA, USA



                                            Abstract—FormalSpecCpp is a dataset designed to fill the gap           better documentation of function behavior, and supports run-
arXiv:2502.15217v1 [cs.SE] 21 Feb 2025




                                         in standardized benchmarks for verifying formal specifications            time behaviors for contract verification. Although this is
                                         in C++ programs. To the best of our knowledge, this is the                promising for newer codebases, manually adapting it to the
                                         first comprehensive collection of C++ programs with well-defined
                                         preconditions and postconditions. It provides a structured bench-         scale of legacy C++ is prohibitively expensive.
                                         mark for evaluating specification inference tools and testing the            Using LLMs to generate formal specifications is a viable
                                         accuracy of generated specifications. Researchers and developers          solution to this bottleneck. Given that such specifications can
                                         can use this dataset to benchmark specification inference tools,          be verified against existing test suites, they enhance code
                                         fine-tune Large Language Models (LLMs) for automated speci-
                                                                                                                   reliability without requiring extensive manual effort. This work
                                         fication generation, and analyze the role of formal specifications
                                         in improving program verification and automated testing. By               highlights the potential of LLMs in supporting automated
                                         making this dataset publicly available, we aim to advance                 specification generation, addressing the need for tools that
                                         research in program verification, specification inference, and AI-        can infer formal specifications from code. Our dataset enables
                                         assisted software development. The dataset and the code are               an empirical evaluation of the specification inference tools.
                                         available at https://github.com/MadhuNimmo/FormalSpecCpp.
                                                                                                                   By comparing inferred specifications against ground truth,
                                                                                                                   researchers can assess precision, recall, and correctness in
                                                                 I. I NTRODUCTION
                                                                                                                   automated inference methods.
                                            Preconditions and postconditions serve as formal specifi-                 The FormalSpecCpp dataset is derived from the Dafny-
                                         cations that define the expected state of a program before                synthesis benchmark [4], which provides formally verified
                                         and after code execution. This ensures software correctness,              Dafny programs with preconditions and postconditions. We
                                         formal verification, and code reliability [1], [2]. Despite their         use a prompt-driven approach with OpenAI’s GPT-4-turbo
                                         significance, standardized benchmarks for C++ programs with               model to systematically translate these Dafny programs into
                                         formal specifications have been notably absent due to the                 C++, ensuring that the generated code preserves its formal
                                         lack of standardization, the complexity of C++, the evolving              specifications.
                                         language standards, and the limited adoption of formal con-                  This dataset is the ground truth benchmark for evaluating
                                         tracts. There is a growing need for formal specification support          formal specification inference tools by providing verified C++
                                         within programming languages to improve software reliability.             programs with preconditions and postconditions. It also en-
                                         Historically, C++ lacked support for formal specifications.               ables the testing of formal verification tools to assess how
                                         Recognizing their importance, the C++ Standards Committee                 well they enforce these specifications. Additionally, it sup-
                                         committed to introducing formal specifications in C++26 [3].              ports static and dynamic analysis research, helping researchers
                                         This will standardize the ability to specify function contracts           examine the impact of different specification techniques on
                                         directly in the language. For example, refer to the code below:           software correctness, tool performance, and contract validation
                                         int f(const int x)                                                        in real-world C++ programs.
                                             pre (x != 1) // a precondition assertion
                                             post(r : r != 2) // a postcondition assertion                            Our prompt engineering methodology systematically trans-
                                         {                                                                         lates Dafny specifications into C++ by explicitly handling
                                             contract_assert(x != 3); // an assertion statement
                                             return x;                                                             type mapping, assertion transformation, and safety constraints.
                                         }                                                                         This structured approach reduces hallucinations, improves
                                                                                                                   syntactic correctness, and ensures that the translated contracts
                                            This feature represents a better alternative to the current
                                                                                                                   accurately represent program intent.
                                         practice of using macros or comments for specifying contracts,
                                         allowing developers to express expectations more clearly and
                                         formally. It also enhances the reliability of the code, facilitates                             II. BACKGROUND

                                           ∗ This work was performed under the auspices of the U.S. Department       This section briefly overviews the background details: for-
                                         of Energy by Lawrence Livermore National Laboratory under Contract DE-    mal specifications in software engineering, LLMs and prompt
                                         AC52-07NA27344. LLNL-CONF-2002128                                         engineering.
            Python programs            Dafny programs                                          Translated                  Manual
             from the MBPP               with formal                                              CPP                    Inspection
                 Dataset                specifications                                          Program



                                                                     LLM based
                                                                   translation of
                                                                  code and tests



                                          Python tests                                        Translated
                                        from the MBPP                                          CPP Test                    Test
                                            dataset                                                                      Execution



Fig. 1. Pipeline for translating Python programs and tests from the MBPP dataset to C++ using Dafny formal specifications and LLM-based translation.



A. Formal Specifications                                                      • Specification Preservation: Ensuring formal properties
   Formal specifications define the expected behavior of soft-                  are accurately translated between languages.
                                                                              • Type Safety: Mapping Dafny types to appropriate C++
ware using precise mathematical statements, typically through
preconditions (requirements before execution) and postcondi-                    equivalents.
                                                                              • Assertion Mapping: Converting Dafny verification con-
tions (guarantees after execution). They play a critical role in
software correctness, modular reasoning, and formal verifica-                   structs into valid C++ assertions and macros.
tion [1], [2].                                                                By carefully designing prompts, we systematically trans-
   Despite their benefits, manual specification writing is com-            formed Dafny programs with verified specifications into C++
plex and time-consuming, especially for large or legacy code-              implementations while preserving formal correctness.
bases. This has led to increasing research in automating spec-
ification inference, reducing the cost of manual annotations                            III. T HE F O R M A L S P E C C P P DATASET
while improving software reliability.                                        This section describes the steps to generate the
                                                                           FormalSpecCpp dataset. Figure 1 presents the workflow.
B. Large Language Models (LLMs)
   LLMs are transformer-based neural networks trained on vast              A. Conversion of Dafny Programs to C++
text corpora, enabling them to generate human-like text and                   The Dafny-synthesis benchmark [4], which contains veri-
code. These models, such as GPT-4, excel in code synthesis,                fied Dafny programs with formal specifications, is the starting
reasoning, and text generation, making them valuable tools for             point for generating C++ programs. Their study evaluated
automating formal specification inference.                                 how well LLMs can synthesize Dafny code, including formal
   LLMs can be broadly categorized into:                                   specifications and validation conditions that pass the Dafny
   • General-purpose models (e.g., GPT-4, Claude) trained                  verifier.
     on diverse text and code.                                                While their approach relies on few-shot prompting with the
   • Code-specific models (e.g., Code Llama) optimized for                 LLM to generate formal specifications [4], we opted for a
     programming tasks.                                                    different strategy. Instead of inferring formal specifications
   For our dataset development, we selected GPT-4-turbo,                   directly for C++ using LLMs, we used LLMs for a structured
a variant of OpenAI’s GPT models, known for its strong                     translation process from Dafny to C++. This decision was
performance in generating semantically correct code and a                  based on the following key considerations:
large 128k-token context window [5]. Prompt engineering is                    • Formal correctness preservation: Since Dafny pro-
used to refine the model inputs to systematically guide the                      grams in the benchmark are already verified, translating
synthesis of formal specifications.                                              their specifications directly to C++ ensures that formal
                                                                                 and logical correctness is maintained rather than relying
C. Prompt Engineering                                                            on speculative inference by the LLM.
   Prompt engineering involved designing structured inputs to                 • Avoiding prompt dependence and unnecessary con-
guide LLMs toward accurate and relevant outputs. Effective                       straints: Prior work [4] found that effective specifica-
prompts improve clarity, control structure, and mitigate issues                  tion inference with LLMs requires carefully engineered
like hallucinations or incorrect type inferences.                                prompts, yet the results are often redundant or overly
   In our work, prompt engineering plays three critical roles:                   restrictive. By translating verified Dafny specifications,
                                            Fig. 2. Dafny to C++ Code Translation Prompt



      we eliminate reliance on complex prompt tuning and           incorrect test specifications, such as misordered arguments,
      prevent the introduction of unnecessary constraints.         incorrect expected values, or type mismatches (unsigned
  By structuring the translation process around an already         int vs. double). Compilation errors, on the other hand,
verified source, we minimize potential inaccuracies introduced     often reflected the limitations of LLM-based translation of the
by the generative process, resulting in a more deterministic       tests.
and reliable benchmarking pipeline. We considered only those          Although automated tests identified structural defects, they
programs from Dafny-synthesis that had both preconditions          could not ensure semantic correctness. Some programs were
and postconditions defined, totaling 105 programs. Since C++       compiled successfully but contained incorrect specifications or
does not yet natively support preconditions and postconditions,    logical inconsistencies that required manual review.
we defined a custom format to represent them consistently          D. Manual Verification of Translations
across all programs:
                                                                      To address these shortcomings, one of the authors, an expert
#define REQUIRE(cond) assert(cond)
#define ENSURE(cond) assert(cond)
                                                                   in formal specifications and C++ programming, manually
                                                                   reviewed and refined a subset of translated programs and test
  The final prompt for converting the programs is shown in         cases. This process focused on:
Figure 2.                                                             • Correcting errors detected by automated tests, such as
                                                                        misaligned assertions, type mismatches, and faulty pre-
B. Conversion of Associated Tests
                                                                        conditions.
   The Dafny-synthesis benchmark includes test cases that             • Inspecting a subset of successful programs to verify
were manually translated from Python tests in the MBPP                  semantic correctness and adherence to best practices.
dataset [6]. In contrast, we used LLM to directly convert             • Refining specifications and tests to better capture intended
the original MBPP test cases into C++, translating test input,          function behavior.
expected output, and assertions while maintaining functional          Manual verification uncovered errors that automated meth-
equivalence.                                                       ods missed, particularly in cases where specifications were
C. Automated Testing of Translated Programs                        syntactically valid but logically incorrect. These included
                                                                   logical inconsistencies such as misaligned assertions and faulty
   After generating the C++ programs and their corresponding       precondition constraints. This step improved the dataset’s
tests, we performed automated test execution to validate their     reliability by ensuring that specifications accurately reflected
correctness. This step revealed several types of errors, includ-   program behavior.
ing: (a) inconsistencies in preconditions and postconditions,         The FormalSpecCpp dataset is available at
(b) incomplete or ill-formed test cases that failed to capture     https://github.com/MadhuNimmo/FormalSpecCpp. It serves
intended functionality, and (c) mismatches between expected        as a standardized dataset for evaluating and improving
and actual outputs, indicating discrepancies in program behav-     precondition and postcondition inference in C++. It will be
ior.                                                               useful in advancing research in specification verification and
   The automated tests provided valuable feedback, identifying     automated program analysis.
functional issues in the translated programs. In our initial
run, 62 programs passed all tests, while 43 failed due to                      IV. C OST A NALYSIS AND E FFICIENCY
assertion errors, linker errors, and compilation errors. Further     The conversion process from Dafny to C++ programs
analysis showed that many assertion failures stemmed from          and tests was highly efficient, as summarized in Table I. A
total of 105 files with preconditions and postconditions were                      VI. C ONCLUDING R EMARKS
processed, with all converted programs successfully compiling
                                                                       This paper introduces the FormalSpecCpp dataset with
on the first attempt, achieving a 100% success rate. The
                                                                    formal specifications for C++, encouraging the community
entire process was completed in approximately 27 minutes,
                                                                    to utilize it for diverse research applications. Although the
demonstrating the scalability and speed of the approach.
                                                                    benchmark is a significant step forward, there is room for
   The total cost for converting these files was $2.07, av-         improvement. We highlight some of the challenges and lessons
eraging $0.02 per file. Similarly, generating the associated        learned along the way. This is meant to serve as a guidance
test cases cost an additional $1.31 and required around             for researchers interested in extending the approach.
15 minutes. These results underscore the minimal resource
usage and cost-efficiency of the pipeline. Dafny files averaged     A. Code Translation
17.3 lines of code, while the converted C++ code showed a
                                                                       The prompt to convert Dafny programs into valid and
91.2% increase in size, with an average of 33.1 lines per file.
                                                                    semantically correct C++ code required non-trivial iterative
   This workflow’s smooth transition and minimal resource
                                                                    refinement, especially given the differences in their type sys-
overhead demonstrate its potential for practical use in large-
                                                                    tems. For instance, Dafny supports an unbounded integer
scale datasets and real-world applications.
                                                                    type, which can represent any integer value without overflow,
                                                                    whereas C++ offers multiple fixed-size integer types, includ-
                            TABLE I
                        OVERALL S TATISTICS
                                                                    ing int, unsigned int, short, and long. C++ has a
                                                                    well-defined overflow behavior for signed integers and wraps
      Statistic                                     Value           around for unsigned integers. One should be mindful of these
      Total files processed                         105             changes when translating from one programming language to
      Successfully compiled programs(1st attempt)   105 (100%)      another.
      Total cost                                    $2.07
      Average cost per file                         $0.02           B. Prompt Engineering Refinements
      Average Dafny lines                           17.3
      Average C++ lines                             33.1               Crafting effective prompts for Dafny to C++ translation
                                                                    involved refining the language model’s handling of precon-
                                                                    ditions, postconditions, and correct C++ constructs. Early
                     V. R ELATED W ORKS                             iterations resulted in misaligned assertions and syntax errors
                                                                    due to differences in language semantics. The iterative process
A. Formal Methods and Specifications
                                                                    focused on explicitly specifying rules around types, precondi-
   Hoare’s axiomatic basis for computer programming [2]             tions, invariants, and postconditions, ensuring consistency and
established the foundation for reasoning about program cor-         correctness across the translations.
rectness through preconditions and postconditions, while Di-
jkstra’s weakest precondition calculus [7] provided system-         C. Test Case Translation
atic approaches for deriving specifications. These theoretical         Adapting test cases from Dafny to C++ required a struc-
frameworks influenced the development of specification lan-         tured approach to facilitate compatibility with C++ testing
guages like JML [8] and modern verification-oriented pro-           frameworks. We designed prompts to guide the LLM in
gramming languages such as Dafny [9]. Meyer’s design by             generating accurate C++ test cases in a predefined format,
contract [1] further popularized the use of preconditions and       reducing manual effort and ensuring smooth integration into
postconditions in software development. However, the manual         the C++ testing environment.
effort required to write formal specifications has historically        Refining these prompts provided valuable insights into the
limited their widespread adoption in industrial practice [10].      strengths and limitations of using LLMs for test case transla-
                                                                    tion. While improved prompts enhanced the LLM’s handling
B. Automated Specification Inference                                of complex cases, challenges remained, such as occasional
   The challenge of manual specification writing has motivated      misinterpretation of logical relationships or the generation of
extensive research in automated specification inference. Early      syntactically correct but semantically flawed code.
approaches like Daikon pioneered dynamic analysis techniques
to infer likely program invariants [11]. Static analysis methods,   D. Future work
including abstract interpretation [12] and symbolic execu-             Some natural extensions to this work are (a) including
tion [13], provided more comprehensive approaches but faced         additional programs and programming languages, (b) refining
scalability challenges with complex codebases [14].                 the prompt engineering process, (c) exploring reinforcement
   Recent research has demonstrated the potential of LLMs           learning and hybrid approaches to further enhance the specifi-
in generating specifications and code for formal verification       cation generation and validation, and (d) extending the dataset
languages like Dafny [4] and Java [15]. This trend aligns           to include larger programs with more complex specifications
with broader efforts to leverage AI in software engineering         to test the scalability and robustness of the inference and
tasks, particularly in areas requiring formal reasoning.            validation processes.
                              R EFERENCES
 [1] B. Meyer, “Applying “design by contract”,” Computer, vol. 25, no. 10,
     pp. 40–51, 1992.
 [2] C. A. R. Hoare, “An axiomatic basis for computer programming,”
     Communications of the ACM, vol. 12, no. 10, pp. 576–580, 1969.
 [3] T. Doumler, A. Krzemieński, G. Ažman, L. Dionne, T. Honermann,
     J. Lakos, L. Lippincott, J. Maurer, R. McDougall, J. Merrill et al.,
     “Contracts for c+,” 2024.
 [4] M. R. H. Misu, C. V. Lopes, I. Ma, and J. Noble, “Towards ai-
     assisted synthesis of verified dafny methods,” Proceedings of the ACM
     on Software Engineering, vol. 1, no. FSE, pp. 812–835, 2024.
 [5] OpenAI, “Gpt-4 and gpt-4 turbo documentation,” 2024, accessed: 2024-
     11-25. [Online]. Available: https://platform.openai.com/docs/models/
     gpt-4-and-gpt-4-turbo#gpt-4-turbo-and-gpt-4
 [6] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,
     E. Jiang, C. Cai, M. Terry, Q. Le et al., “Program synthesis with large
     language models,” arXiv preprint arXiv:2108.07732, 2021.
 [7] E. W. Dijkstra, A Discipline of Programming. Prentice Hall, 1976.
 [8] G. T. Leavens, E. Poll, C. Clifton, Y. Cheon, C. Ruby, D. Cok, P. Müller,
     J. Kiniry, P. Chalin, D. M. Zimmerman et al., “Jml reference manual,”
     2008.
 [9] K. R. M. Leino, “Dafny: An automatic program verifier for functional
     correctness,” in International Conference on Logic for Programming,
     Artificial Intelligence, and Reasoning. Springer, 2010, pp. 348–370.
[10] J. Woodcock, P. G. Larsen, J. Bicarregui, and J. Fitzgerald, “Formal
     methods: Practice and experience,” ACM computing surveys (CSUR),
     vol. 41, no. 4, pp. 1–36, 2009.
[11] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco, M. S.
     Tschantz, and C. Xiao, “The daikon system for dynamic detection of
     likely invariants,” Science of computer programming, vol. 69, no. 1-3,
     pp. 35–45, 2007.
[12] P. Cousot and R. Cousot, “Abstract interpretation: a unified lattice model
     for static analysis of programs by construction of approximation of fix-
     points,” in Proceedings of the 4th ACM SIGPLAN-SIGACT Symposium
     on Principles of Programming Languages, 1977, pp. 238–252.
[13] J. C. King, “Symbolic execution and program testing,” Communications
     of the ACM, vol. 19, no. 7, pp. 385–394, 1976.
[14] C. Calcagno, D. Distefano, P. W. O’hearn, and H. Yang, “Compositional
     shape analysis by means of bi-abduction,” Journal of the ACM (JACM),
     vol. 58, no. 6, pp. 1–66, 2011.
[15] L. Ma, S. Liu, Y. Li, X. Xie, and L. Bu, “Specgen: Automated generation
     of formal program specifications via large language models,” arXiv
     preprint arXiv:2401.08807, 2024.
