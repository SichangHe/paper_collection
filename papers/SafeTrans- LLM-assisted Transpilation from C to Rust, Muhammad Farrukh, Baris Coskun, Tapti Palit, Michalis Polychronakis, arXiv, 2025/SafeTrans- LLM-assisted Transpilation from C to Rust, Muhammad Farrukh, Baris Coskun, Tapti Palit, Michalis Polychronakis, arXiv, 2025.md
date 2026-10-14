                                                        SafeTrans: LLM-assisted Transpilation from C to Rust
                                                                     Muhammad Farrukh                                                                   Baris Coskun∗
                                                                   Stony Brook University                                                           Amazon Web Services
                                                                       New York, USA                                                                   New York, USA
                                                                mufarrukh@cs.stonybrook.edu                                                         barisco@amazon.com

                                                                             Tapti Palit                                                         Michalis Polychronakis
                                                                University of California, Davis                                                   Stony Brook University
                                                                         Davis, USA                                                                   New York, USA
                                                                     tpalit@ucdavis.edu                                                          mikepo@cs.stonybrook.edu
arXiv:2505.10708v2 [cs.CR] 22 Apr 2026




                                         Abstract                                                                                “systems” language with acceptable runtime overhead, and major
                                         Rust is a strong contender for a memory-safe alternative to C as a                      projects have started distributing some components written in Rust,
                                         “systems” language, but porting the vast amount of existing C code                      or at least have introduced tooling support for integrating Rust code
                                         to Rust remains daunting. In this paper, we evaluate the potential                      in existing C/C++ code bases (e.g., Firefox, Chrome, Linux, Win-
                                         of large language models (LLMs) to automate the transpilation of C                      dows). Automating the translation of existing C code into Rust,
                                         code to idiomatic Rust. We present SafeTrans, a generic framework                       however, is challenging due to substantial syntactic and seman-
                                         that leverages LLMs to i) transpile C code into Rust, and ii) iter-                     tic disparities between the two languages, particularly concerning
                                         atively repair compilation and runtime errors. A key novelty of                         memory management and ownership.
                                         our approach is a few-shot guided repair technique for translation                          Initial attempts to this problem adopted rule-based translation
                                         errors, which provides contextual information and example code                          approaches [8, 12, 14, 18, 44]. These methods scale to large programs
                                         snippets for specific error types, guiding the LLM toward the cor-                      and yield functionally equivalent code, but often fail to produce
                                         rect solution. Another novel aspect of our work is the evaluation                       idiomatic and safe Rust, undermining their security benefits.
                                         of the security implications of the transpilation process, showing                          With the advent of large language models (LLMs), recent stud-
                                         how some vulnerability classes in C persist in the translated Rust                      ies have focused on exploring their potential for automating code
                                         code. SafeTrans was evaluated with six leading LLMs on 2,653 C                          translation. LLMs can generate more idiomatic code than previous
                                         programs and two real-world C projects. Our results show that                           methods, but they come with their own set of challenges. Pan et
                                         iterative repair improves the rate of successful translations from                      al. [29] performed one of the first studies to understand the limi-
                                         54% to 80% for the best-performing LLM (gpt-4o).                                        tations of LLMs for code translation, and present a taxonomy of
                                                                                                                                 bugs introduced during the translation process. Similarly, Ou et
                                         CCS Concepts                                                                            al. [28] developed a repository-level benchmark for code transla-
                                                                                                                                 tion evaluation, and developed a taxonomy of translation errors.
                                         • Security and privacy → Software security engineering.
                                                                                                                                 LLM-transpiled code requires comprehensive methods to verify its
                                         Keywords                                                                                correctness, an issue that recent studies attempt to address using
                                                                                                                                 various techniques [5, 9, 26, 41, 42]. Aside from correctness, LLMs
                                         Transpilation, Rust, LLM, Memory Safety, Vulnerability Mitigation                       also struggle with larger applications. Modern LLMs support large
                                         ACM Reference Format:                                                                   context windows, but recent studies show that they often cannot
                                         Muhammad Farrukh, Baris Coskun, Tapti Palit, and Michalis Polychronakis.                attend to all parts of long inputs uniformly, impacting their effec-
                                         2026. SafeTrans: LLM-assisted Transpilation from C to Rust. In 1st Workshop             tiveness [23, 24]. Several studies have tackled this issue by dividing
                                         on Code Translation, Transformation, and Modernization (ReCode ’26), April              larger applications into smaller translation tasks [27, 34, 35, 43]. Al-
                                         12–18, 2026, Rio de Janeiro, Brazil. ACM, New York, NY, USA, 8 pages.
                                                                                                                                 though these studies identify the causes of translation errors, how
                                         https://doi.org/10.1145/3786180.3788317
                                                                                                                                 to use this knowledge to improve transpilation accuracy remains
                                                                                                                                 unclear.
                                         1    Introduction
                                                                                                                                     Unlike the above recent works in automated transpilation using
                                         Many of the software systems used by enterprises and individual                         LLMs, which mostly focus on handling the translation of larger
                                         users rely on huge legacy C/C++ code bases. Migration to memory-                        applications and developing additional approaches to verify the
                                         safe languages will be a slow and tedious task if not (at least par-                    correctness of the translated programs, our research addresses sev-
                                         tially) automated. Rust is the strongest contender for a memory-safe                    eral fundamental questions specific to C-to-Rust translation. First,
                                         ∗ This work does not relate to Baris Coskun’s position at Amazon.                       we identify the Rust features that LLMs struggle to handle, which
                                                                                                                                 lead to the most frequent translation errors. We extend our anal-
                                                                                                                                 ysis beyond building a simple taxonomy, by incorporating these
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   findings to improve translation accuracy in the form of contextual
                                         ReCode ’26, Rio de Janeiro, Brazil                                                      information that aids the repair process.
                                         © 2026 Copyright held by the owner/author(s).                                               Second, we evaluate the effectiveness of using this additional
                                         ACM ISBN 979-8-4007-2411-4/2026/04
                                         https://doi.org/10.1145/3786180.3788317                                                 contextual information as part of a guided repair process to fix
ReCode ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                  Farrukh et al.


faulty translations. This is achieved by analyzing the most frequent         LLM-based C-to-Rust Translation: In recent years, LLMs have
translation errors and assembling targeted instructions along with        been used for a wide range of applications [6, 15, 19, 20, 25, 32, 40] in-
example code snippets to guide the LLMs towards the correct solu-         cluding code generation. Pan et al. [29] conducted a comprehensive
tion. Finally, we examine the effect of vulnerabilities present in C on   analysis of LLMs’ translation capabilities across multiple language
the corresponding Rust translations. This targeted approach distin-       pairs, including C to Rust. Their study also provides a detailed taxon-
guishes our work from previous transpilation studies by specifically      omy of LLM-based translation bugs but lacks in-depth insights into
examining the language-level semantic challenges in translating           issues specific to C-to-Rust translation. For C-to-Rust translation,
from a memory-unsafe language to one with strict safety guaran-           several studies enhance LLM-based approaches with program analy-
tees enforced at compilation time.                                        sis, formal verification, and fuzzing to improve translation accuracy.
    To this end, we developed SafeTrans, a framework for evaluat-         VERT [41] uses WebAssembly to generate oracle Rust programs for
ing LLMs in their C-to-Rust code translation capabilities. We used        formal equivalence testing. FLOURINE [9] verifies translated code
SafeTrans to perform a total of 15,918 translations across 2,653 C        via fuzzing, and SPECTRA [26] enhances translation using mul-
programs and six LLMs. The combination of basic repair with few-          timodal specifications. These tools, however, are limited to small
shot guided repair achieves compilation repair success rates of up to     programs (<600 LoC). Some recent works [5, 16, 27, 34, 35, 39] focus
93.5% for gpt-4o and 89.8% for DeepSeek-V3. Guided repair effec-          on translating large-scale C programs to Rust by decomposing the
tively resolves challenging Rust compilation errors, such as trait im-    source code for incremental translation, while others employ LLM-
plementation failures, with an average resolution rate of 58.7%, and      powered agents for transpilation and testing [17, 22, 36] Finally, a
borrow-checker violations with an average rate of 74.2% across all        user study by Li et al. [21] demonstrates that human strategies for
LLMs. Overall, our repair techniques collectively achieve substantial     C-to-Rust translation differ from those used by automated tools.
improvements in computational accuracy (CA), increasing the over-
all translation success rate from 54% to 80% for gpt-4o. Even smaller     3     SafeTrans Overview
models, such as Qwen2.5-Coder and DeepSeek-Coder, nearly dou-
                                                                          In this section, we present SafeTrans, our framework for automating
ble their CA, highlighting the broad applicability and effectiveness
                                                                          C-to-Rust translation, along with the methodology used to evaluate
of our approach.
                                                                          translation fidelity. The overall translation process comprises four
    In summary, we make the following main contributions:
                                                                          main steps, as illustrated in Figure 1: transpilation, compilation,
• We present the design and implementation of SafeTrans, an end-          repair, and validation. The original C program is first transpiled into
  to-end framework for comprehensively evaluating the C-to-Rust           Rust using an LLM. The resulting Rust program is then compiled,
  code transpilation capabilities of LLMs.                                and if compilation fails, an iterative repair process is initiated to fix
• We demonstrate that just providing compiler error messages and          the errors using both generic and guided prompts. After successful
  feedback is insufficient for repairing many types of faulty trans-      compilation, the program is executed and validated against the
  lations, and introduce a novel few-shot guided repair approach          original C program’s test cases. In case of runtime or validation
  to improve the repair rate.                                             errors, another iterative repair cycle is initiated.
• We identify 10,375 vulnerabilities (e.g., out of bounds access,
  null-pointer dereference) in the 2,653 source C programs used in        3.1    Transpilation from C to Rust
  our evaluation, and demonstrate their behavior in the translated
                                                                          The first step in the translation pipeline is to generate an initial Rust
  Rust programs.
                                                                          version of the original C program using an LLM. The input program
Our prototype implementation and data set are publicly available          is included in the prompt, along with instructions for producing
through https://github.com/FarrukhCyber/SafeTrans.                        safe code and adhering to the required output format.
                                                                              We use this initial prompt to query the LLM, which can result in
                                                                          two scenarios. Ideally, the LLM generates a response that adheres
2    Background and Related Work                                          to the required output format, allowing us to extract the Rust code
Rule-based C-to-Rust Translation: Conventional solutions to               based on the predefined tags. In the second case, the LLM fails
source-to-source translation have predominantly relied on rule-           to generate a valid response, either because the prompt and the
based methodologies. The most prominent tool in this category is          output exceed its context window, or because it produces incoherent
C2Rust [18], which translates C programs to Rust using both pre-          output, without adhering to the required format. In such cases, we
defined and custom rules. Despite its scalability, C2Rust produces        discard the response, a condition we refer to as a Generation Error.
non-idiomatic code with excessive use of unsafe blocks.
   A recent study of C2Rust by Emre et al. [8] investigates the un-       3.2    Compilation and Repair:
derlying causes of unsafety. The authors propose a technique that         In the compilation phase, the transpiled code is compiled using
relies on feedback from the rustc compiler to refactor a certain          the rustc compiler. If the compilation is successful, the resulting
type of raw pointers into Rust references. Inspired by C2Rust, sev-       binary is provided as input to the runtime testing and validation
eral studies have attempted to address its limitations. CROWN [44]        phase. Otherwise, SafeTrans attempts to automatically repair the
improves upon C2Rust’s output by converting raw pointers to ref-          compilation errors by initiating an iterative repair phase.
erences, but it is limited to mutable and non-array raw pointers.            Basic Repair: In case of a compilation error, the rustc com-
Similarly, other tools [11–13] focus on specific translation chal-        piler provides detailed error messages which can be passed to the
lenges, such as converting lock APIs and certain data types.              LLM along with the transpiled Rust program to provide additional
SafeTrans: LLM-assisted Transpilation from C to Rust                                                                                  ReCode ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                        Transpilation                                         Compilation                                  Testing and Validation
                                                       {}
                                                                                                                 1101
                                                                                                                 0111
                         C-to-Rust                                                                               1001


             {}           Prompt
                                           LLM
                                                       Rust
                                                                         Compile Rust Program
                                                                                                             Executable
                                                                                                                              Execute Unit Tests                               1101
                                                                                                                                                                               0111
                                                                                                                                                                               1001
                                                                                                                                                                                      {}
                                                     Program                                                                                                                   Validated
            Original
            C Program                   Generation                  Rust                  Compilation                                             Validation                     Rust
                                                               {}                                            Feedback                                               Feedback   Program
                                          Error                     Program                   Failed                                                  Failed


                                                                               Basic Repair          <K                            Error Type               <K
                                                                LLM                               attempts                                               attempts
                                                                                 Prompt                                          Identification


                                                                              Guided Repair          < 2K
                                                                                                  attempts
                                                                                                                                Error-Specific
                                                                                 Prompt                                         Repair Prompt



                                                                                                        Iterative Repair

             Figure 1: High-level architecture of SafeTrans’ transpilation, compilation, repair, and validation pipeline.


context about the issue. Recent studies [7] have demonstrated the ef-                                   it queries the LLM with an appropriately updated (dynamically
fectiveness of this approach. We adopt an iterative repair approach                                     generated) prompt.
to resolve compilation errors similar to Pan et al. [29]. In each it-
eration, the incorrect Rust translation and the repair instructions
within the prompt are updated based on the results of the previous
iteration, while the base prompt remains unchanged. At the end                                          4      Experimental Setup
of each iteration, the generated Rust program is compiled again,                                        Large Language Model Selection: For our empirical study, we se-
and if compilation fails, a new repair cycle is initiated. The phase                                    lect a diverse set of LLMs, ranging from small open-source models to
continues until either the program is successfully compiled, or a                                       state-of-the-art (SOTA) LLMs. Among the SOTA LLMs, we include
predefined maximum number of iterations is reached (set to five in                                      gpt-4o and DeepSeek-V3 (671B). For small open-source LLMs,
our experiments).                                                                                       we select Qwen2.5-Coder (7B), Codestral (22B), DeepSeek-Coder
   Guided Repair: Even after several iterations, some programs                                          (16B), and Llama3 (70B). As a rapidly evolving field, LLMs are fre-
may still fail to compile. To improve the translation success rate,                                     quently updated, and new models are being released regularly. Due
we introduce a new guided repair strategy, which uses few-shot                                          to time and cost reasons we could not include other recently re-
learning by incorporating error-specific contextual information in                                      leased models, such as Claude and Gemini, but we tried to select
the repair prompt. We selected the top eight most frequent errors,                                      a set of models that are representative of the spectrum of choices
for which we developed tailored repair instructions, outlining key                                      and capabilities in the current state of the art.
aspects to address along with common causes and fixes.                                                     Data Set Collection and Pre-Processing: For code translation
   To maintain conciseness within the LLM’s context length con-                                         tasks, we use the CodeNet data set [30], and two real-world C li-
straints and minimize noise, we only include instructions relevant                                      braries, url_parser [2] and avl_tree [1], which have been used in
to the errors present in the current compilation output. The instruc-                                   prior LLM-based translation studies. These two programs include
tions first explain the Rust property that was violated, leading to                                     comprehensive end-to-end test cases and represent challenging
that error, followed by concrete examples of incorrect and corrected                                    translation tasks. The CodeNet data set [30] comprises 4,053 com-
code snippets to assist the LLM in resolving the issue.                                                 petitive programming problems written in over 50 programming
                                                                                                        languages. Since our focus is on C, we filter the data set to retain
3.3     Runtime Testing and Validation                                                                  only those problems that have an adequate number of solutions
Successfully compiled Rust programs proceed to the runtime testing                                      written in C.
and validation phase, which executes the program with various                                              After some preprocessing steps, our final evaluation data set
test cases and validates the output against the expected results. We                                    contains 2,653 C programs. The test cases in our dataset achieve an
consider a C program as successfully translated if the generated                                        average line coverage of approximately 87%.
Rust program passes all test cases. Erroneous outcomes of this
dynamic analysis phase include Runtime Error, Infinite Loop, and
Test Case Error. Our unit tests are based on the test cases available
in the CodeNet data set used in our evaluation. If the translated                                       5      Results
Rust program fails to run properly or does not pass the test cases, it                                  We present the results of our experimental evaluation, focusing on
undergoes another round of iterative repair, this time with prompts                                     the following research questions: RQ1: How base LLMs perform
tailored to the specific type of runtime error encountered.                                             on C-to-Rust translation task? RQ2: What compilation errors occur
   In this phase, SafeTrans iteratively repairs the program until it                                    and how effective is iterative repair? RQ3: How effective is guided
passes all test cases or exceeds the maximum number of repair at-                                       repair for persistent errors? RQ4: What is the overall improvement
tempts (set to five in our tests). In each iteration, SafeTrans performs                                in translation success rate? RQ5: How does SafeTrans scale on
both compilation and runtime test checks, and if the validation fails,                                  complex real-world programs?
ReCode ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                                                    Farrukh et al.


                              Correct Translations                 Compilation Errors                Infinite Loops                             Table 1: Effectiveness of iterative repairing of failed Rust
                              Generation Errors                    Runtime Errors                    Test Case Errors
                                                                                                                                                compilations.
                       100                                                                                          2250
                        90                                                                                         2000                                              Compilation           Repair     Pass
                                                                                                            7%                                        LLM                        Repaired
                                                                                5%             4%                                                                       Failures          Rate (%) Rate (%)
                        80                                                                                  9%     1750
                                                                                12%
                                                                                              11%                                                     Qwen2.5-Coder         1743     1090     62.5     23.4
% of Transpiled Programs




                        70




                                                                                                                         Number of C Programs
                                                                                                                   1500                               Llama3                1884     1096     58.1     14.1
                                                                  7%
                        60                                                                                                                            DeepSeek-Coder        1836     1021     55.6     33.7
                                                                                                                   1250
                        50                           4%                                                                                               Codestral              906      778     85.8     28.9
                                      5%                          25%                                              1000                               GPT-4o                 558      522     93.5     43.4
                        40                                                                                  71%
                                                     24%                        66%           69%                  750                                DeepSeek-V3            579      520     89.8     47.1
                        30          20%
                              54%              49%
                        20                                                                                         500
                                                             33% 34%                                                                            all errors in most models, and up to 30% for Qwen2.5-Coder and
                        10          21%              22%                  17%           15%
                                                                                                                   250
                                                                                                      10%                                       Llama3, suggesting that LLMs struggle with type inference and
                         0                                                                                  2%     0
                                    4o                 -v3          ral           er                der llama3                                  trait bounds. Beyond these common errors, some models exhibit
                               gpt-              eek         code
                                                                  st          -cod             -co
                                            eeps                          qwen            seek                                                  distinct error patterns. For example, 18.9% of DeepSeek-V3 trans-
                                           d                                          deep
Figure 2: Percentage of correct Rust translations out of 2,653                                                                                  lations fail due to E0428 (“duplicate definition”), while Codestral
C programs, and breakdown of the different types of failures                                                                                    and DeepSeek-Coder struggle disproportionately (19–22%) with
for unsuccessful translations.                                                                                                                  E0599 (“method not found”). Similarly, Qwen2.5-Coder and Llama3
                                                                                                                                                result in high rates of “lifetime issues” and “borrow conflicts.”

                                                                                                                                                5.2.2 Iterative Compilation Repair. To evaluate the effectiveness
5.1                          RQ1: Basic Translation Success Rate                                                                                of SafeTrans’ repair phase, we introduce two metrics: i) Repair
To assess the “out-of-the-box” performance of LLMs in C to Rust                                                                                 Rate: the percentage of transpiled programs that initially failed to
translation, we adopt computational accuracy (CA), proposed by                                                                                  compile, but then were successfully fixed during the repair phase,
Rozière et al. [31] and Szafraniec et al. [37], as our primary evalu-                                                                           resulting in a compilable program; ii) Pass Rate: the percentage of
ation metric. CA is defined as the ratio of successfully translated                                                                             repaired programs that run successfully and pass all test cases.
programs to the total number of translation samples.                                                                                               Table 1 provides a breakdown of the outcomes of the iterative
   Figure 2 presents a comparative analysis of the six evaluated                                                                                compilation repair phase in terms of repair rate and pass rate for
LLMs in their ability to perform basic C-to-Rust translation (with-                                                                             each LLM. The Compilation Failures column corresponds to the
out any attempt to fix any errors). For each model, the left bar in                                                                             number of programs that failed to compile after the base translation.
the group represents CA, while the right stacked bar illustrates a                                                                              We observe that gpt-4o and DeepSeek-V3 achieve high repair rates
breakdown of the encountered translation errors. Following the                                                                                  of 93.5% and 89.8%, respectively, outperforming the other LLMs. In-
categorization of Pan et al. [29], we classify these errors into five                                                                           terestingly, despite being significantly smaller, Codestral performs
distinct types: ① Generation Error: The model either fails to gener-                                                                            comparably to larger LLMs (only 7.7% and 4% lower than gpt-4o
ate a response according to required format, or the prompt exceeds                                                                              and DeepSeek-V3 in terms of repair rate). The repair rate of Llama3
the LLM’s context length. ② Compilation Error: The transpiled Rust                                                                              (58.1%) is comparable to other smaller code-oriented LLMs, such as
code fails to compile. ③ Runtime Error: The Rust code is compiled                                                                               Qwen2.5-Coder (62.5%) and DeepSeek-Coder (55.6%), suggesting
successfully, but the execution of the program fails (e.g., panics)                                                                             that it can effectively leverage repair prompts to fix faulty trans-
④ Infinite Loop: The program enters a non-terminating loop. ⑤ Test                                                                              lations. The relatively lower pass rates across all LLMs compared
Case Error: Execution of at least one test case fails.                                                                                          to their repair rates suggest that while these models can interpret
   Among the evaluated models, gpt-4o and DeepSeek-V3 achieve                                                                                   compiler feedback and fix syntactic issues, they often lose sight of
the highest base computational accuracy (54% and 49%, respec-                                                                                   the original program intent and functional equivalence.
tively). As evident from the stacked bars, compilation errors are
the most frequent failure mode across all models.                                                                                               5.3     RQ3: Effectiveness of Guided Repair
                                                                                                                                                Even after iterative compilation repair, certain compilation errors
5.2                          RQ2: Compilation Error Analysis                                                                                    remain. Many of the most frequent errors before repair continue to
5.2.1 Error Distribution. A high frequency of compilation errors                                                                                appear in abundance, which means that merely providing compiler
demands an in-depth study of their root causes. The transpiled                                                                                  feedback to the LLM is insufficient for resolving them. To better
Rust programs result in a diverse range of errors, but we focus on                                                                              understand why LLMs struggle with these persistent errors, we se-
the most frequent ones that comprise the vast majority of cases,                                                                                lected the following ones (top-8) for further investigation: ① E0277:
since they represent the core features of Rust with which LLMs                                                                                  The type does not implement a required trait. ② E0308: Mismatched
struggle. Additionally, we only consider the compilation errors for                                                                             types encountered. ③ E0425: Use of an undeclared name or iden-
which rustc provides specific error codes, because this makes the                                                                               tifier. ④ E0599: Attempted call on a type that doesn’t support it.
categorization of errors easier for systematic analysis.                                                                                        ⑤ E0384: Cannot assign to an immutable variable. ⑥ E0282: Unable
   We observe consistent occurrence of some errors across all LLMs.                                                                             to infer enough type information. ⑦ E0502: Cannot borrow as mu-
Specifically, errors E0277 (“trait not implemented”) and E0308 (“mis-                                                                           table because it is also borrowed as immutable. ⑧ E0499: Cannot
matched types”) are the most prevalent, accounting for over 18% of                                                                              borrow as mutable more than once at a time.
SafeTrans: LLM-assisted Transpilation from C to Rust                                                                                                                       ReCode ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                              Correct Translations                 Compilation Errors                Infinite Loops                             are highly effective at debugging erroneous programs when pro-
                              Generation Errors                    Runtime Errors                    Test Case Errors
                       100                                                                                          2250                        vided with appropriate feedback. Similarly, compilation errors for
                                                                                                                                                Codestral, Qwen2.5-Coder, DeepSeek-Coder, and Llama3 drop
                        90                                                                                         2000
                                                                                                                                                by 30, 45, 44, and 47 percentage points, respectively. Among these,
                        80                                                                                         1750                         Llama3 exhibits the largest reduction in compilation errors, indi-
% of Transpiled Programs




                        70                                                                                  19%




                                                                                                                         Number of C Programs
                                                                                                                   1500                         cating that even general-purpose LLMs can substantially benefit
                        60                                                      10%           13%
                                                                                                                   1250                         from our iterative repair strategies. For the smaller LLMs, we can
                        50                                                                                                                      see that there is an increase in non-compilation errors. This occurs
                                                                                                            32%    1000
                        40    80%              79%                 7%           34%           27%                                               because programs that previously failed to compile, once repaired,
                        30                                                                                         750                          may generate new runtime or logic errors due to the hallucination
                                                             55%
                        20                           4%            32%                                             500                          tendencies of LLMs. However, the overall increase in CA shows the
                                      4%                                  34%           34%
                                                                                21%           25%     22%
                                                                                                            24%
                                                                                                                   250                          potential of targeted iterative repair techniques across models.
                        10          15%              16%
                         0                                         4%                                       2%     0
                                    4o                 -v3          ral           er                der llama3                                  5.5    RQ5: Scalability on Complex Programs
                               gpt-              eek         code
                                                                  st          -cod             -co
                                            eeps                          qwen            seek
                                           d                                          deep                                                      To assess SafeTrans’s scalability, we evaluated it on two real-world
Figure 3: Final translation success rate and error breakdown                                                                                    libraries, url_parser [2] and avl_tree [1], which have been used
for the full SafeTrans pipeline.                                                                                                                in prior studies [21, 27, 45]. While existing tools such as C2SaferRust,
   For each of these errors, we examine both their successful and                                                                               VERT, FLOURINE, and SACTOR either fail to compile these pro-
failed repair cases to identify recurring patterns that lead to the                                                                             grams or produce translations with extensive unsafe code, Safe-
error. Based on these observations, we develop guided instructions                                                                              Trans successfully compiles both libraries while avoiding unsafe
that describe the common causes and provide example fixes where                                                                                 constructs. However, verification remains partial, as test-based feed-
applicable, which are used in our subsequent guided repair phase.                                                                               back alone is insufficient to pinpoint semantic errors. A detailed
For example, error E0384 typically occurs when a new value is                                                                                   comparison is provided in Appendix A.1 (Table 3).
assigned to an immutable variable. Our analysis reveals that such
common patterns include reassigning struct instances and vari-                                                                                  6 Vulnerability Analysis
ables introduced through pattern matching. The instructions in our                                                                              6.1 Identification of Potential Vulnerabilities
guided repair are tailored to these patterns and provide examples
                                                                                                                                                A major goal of our study is to assess the extent to which any vul-
to assist the LLM in resolving the error.
                                                                                                                                                nerabilities present in the original C code are effectively mitigated
   To evaluate the effectiveness of guided repair in resolving com-
                                                                                                                                                in the translated Rust code. Instead of planting bugs in existing pro-
pilation errors, we define the resolution rate (RR) metric, which
                                                                                                                                                grams or collecting a different data set of vulnerable programs, we
measures the percentage of targeted errors successfully repaired.
                                                                                                                                                observe that due to the nature of the CodeNet data set, its programs
Overall, guided repair proves highly effective across most error
                                                                                                                                                already contain numerous flaws that would pose security risks if
categories. Llama3 achieves the highest average RR, resolving
                                                                                                                                                they were to be used in production.
over 60% of common errors, followed closely by DeepSeek-V3 and
                                                                                                                                                    Inspired by the FormAI data set [38], we used the Efficient SMT-
Codestral. Commonly encountered errors such as E0384, E0282,
                                                                                                                                                based Context-Bounded Model Checker (ESBMC) [10] formal ver-
and E0425 exhibit resolution rates above 80% across multiple mod-
                                                                                                                                                ification tool to analyze the programs in our CodeNet data set
els, showing that these issues can be fixed reliably when LLMs re-
                                                                                                                                                and identify various types of vulnerabilities in them. ESBMC uses
ceive targeted feedback. Even challenging type inference errors like
                                                                                                                                                bounded model checking, which examines the correctness of a pro-
E0277 (“trait not implemented”) and E0308 (“mismatched types”)
                                                                                                                                                gram by converting it into a finite state transition model and explor-
achieve an average resolution rate of approximately 59% and 55%, re-
                                                                                                                                                ing possible states (up to a predefined boundary). It automatically
spectively, indicating that guided repair effectively improves model
                                                                                                                                                verifies both predefined safety properties (e.g., out-of-bounds array
performance even on complex errors.
                                                                                                                                                access, illegal pointer dereferences, overflows) and user-defined
5.4                          RQ4: Overall Translation Success Rate                                                                              program assertions. We should note that the flaws reported by ES-
After combining the basic and guided compilation repair ap-                                                                                     BMC represent potential vulnerabilities—determining whether they
proaches, in this section we evaluate the overall performance of the                                                                            are indeed exploitable is outside the scope of this work. For the
complete SafeTrans pipeline in successfully translating C programs                                                                              sake of brevity, we refer to these flaws simply as vulnerabilities in
into Rust. Figure 3 illustrates the substantial improvements achieved                                                                           the rest of this section.
through the iterative repair techniques across all LLMs. The com-                                                                                   The outcome of scanning a program with ESBMC can be catego-
putational accuracy (CA) of both gpt-4o and DeepSeek-V3 is in-                                                                                  rized into one of the following three cases: i) Verification Successful:
creased by approximately 25% compared to their base CA, reaching                                                                                indicates that no flaws have been found within the defined bounds;
80% and 79%, respectively. Even for the underperforming models,                                                                                 ii) Verification Failed: ESBMC detected one or more flaws in the tar-
CA is improved by roughly twice (+22% for Codestral, +17% for                                                                                   get program; iii) Scan Error: during verification, ESBMC may crash
Qwen2.5-Coder, +19% for DeepSeek-Coder and +12% for Llama3).                                                                                    or timeout. Approximately 70% of the programs failed verification,
   For gpt-4o and DeepSeek-V3, we observe a drastic reduction                                                                                   i.e., they contain some form of flaw that was not reported by the
across all error types, particularly in compilation errors, which drop                                                                          authors of CodeNet. As pointed out by previous works [10, 38],
below 2% (from 22–23% in Figure 2). This indicates that larger LLMs                                                                             ESBMC cannot produce false positives or false negatives, as each
ReCode ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                           Farrukh et al.


Table 2: Distribution of the types of detected vulnerabilities                 such vulnerabilities often propagate to the Rust translations due to
in the original C programs, as provided by ESBMC [10].                         the absence of explicit checked functions.
                                                                                  Null Pointer Dereferences: We observe that the majority of
            Vulnerability Type                          Instances
                                                                               the unsafe code in Rust translations arises from global variable
            Buffer Overflow                                 3,258              usage rather than raw pointer usage (approximately 9.77% of all
            Array Bounds Violated                           2,951              translated programs across models contain at least one raw pointer
            Arithmetic Overflow                             2,859
                                                                               dereference). However, we still found cases where a null pointer
            Dereference Failure: NULL Pointer                 753
                                                                               dereference vulnerability in C propagates to the Rust translation
            Division by Zero                                  196
            VLA Array Size Overflows Address Space            175              due to incorrect handling of unsafe blocks. While translating a C
            Dereference Failure: Forgotten Memory             100              implementation of B+ trees, gpt-4o introduces a bug by incorrectly
            Dereference Failure: Invalid Pointer               47              translating a C for-loop to a Rust range expression which further
                                                                               leads to a segmentation fault.
identified issue is validated by counterexamples, and the fact that        1 // C: Shift elements right when inserting
successful verification only occurs up to a predefined bound. This         2 for (i = leaf -> num_keys ; i > insertion_point ; i - -) {...}
means that the possibility of some bugs hiding deep in the program         1 // Rust : Empty range when insertion_point < num_keys
                                                                           2 for i in ((* leaf ). num_keys .. insertion_point ). rev () {...}
still exists, but as we show, ESBMC still identifies plenty of potential
vulnerabilities in the tested programs.                                           When inserting at position 0 with num_keys = 1, the range
    Table 2 shows the distribution of the most frequently reported             (1..0).rev() produces no iterations. Consequently, existing ele-
types of vulnerabilities in the original C programs as reported                ments are not shifted, and pointers[1] remains uninitialized as
by ESBMC. A single program can contain multiple vulnerabilities                ptr::null_mut(). The corruption occurs during range queries,
across multiple types. Overall, ESBMC identified a total of 10,375             which iterate over all keys and unconditionally dereference their
vulnerabilities in the 2,653 programs (about five per program).                associated pointers.

6.2     Vulnerability Mitigation                                               7   Limitations and Future Work
Despite explicit instructions to generate safe Rust code, all the              For our guided repair of compilation errors, we constructed con-
evaluated models still produced very few translations containing               textual rules for only the top-eight errors we encountered, and
some unsafe Rust code blocks (0.89% for DeepSeek-Coder, 1.25%                  incorporate them in the prompt during the repair process. As we
for Llama3, 2.0% for Qwen2.5-Coder, 1.8% for gpt-4o, 3.4% for                  have shown, this approach yields a high resolution rate for target
Codestral, and 4.4% for DeepSeek-V3). Moreover, in terms of aver-              errors. It is possible that after addressing the top errors, other com-
age proportion of unsafe lines across all translated programs, the             pilation error types may prevent successful translation. Therefore,
models exhibit roughly comparable behavior, with a mean unsafe                 the set of custom instructions for guided repair prompts can be
ratio of approximately 34% overall.                                            expanded to address additional errors, which would potentially
   For each identified flaw, ESBMC generates a “proof” of vulnera-             increase further the success rate of compilation repair.
bility in the form of program states that trigger the flaw. However,
in some complex cases, these states do not show complete execution             8   Conclusion
traces and therefore cannot be directly applied to the transpiled Rust         We presented SafeTrans, a framework that leverages LLMs to auto-
programs. We employ a combination of automated and manual anal-                mate the transpilation of C code into Rust. Our approach combines
ysis to determine whether the same vulnerabilities in the original C           basic repair and few-shot guided repair to address the inherent
programs can be triggered in the corresponding Rust translations.              challenges in translating C code to idiomatic and safe Rust. Our ex-
First, we used a combination of Rust memory-safety verification and            tensive experimental evaluation results demonstrate that SafeTrans
undefined-behavior detection tools, including Rudra [4], RAPx [3],             offers significant improvements in both computational accuracy
and miri [33]. None of these tools report any vulnerabilities in the           (up to 25%) and compilation error repairing (up to 93.5%) compared
transpiled Rust programs. Next, we perform manual analysis to                  to basic LLM transpilation. Our analysis of the security implica-
identify any cases missed by automated checkers. Since scaling this            tions of the transpilation process highlights that LLM generated
manual analysis to all translations is not possible, we only focus on          translations require further processing to mitigate source program
arithmetic overflow and null pointer dereference vulnerabilities.              vulnerabilities. We believe our findings highlight the potential of
   Arithmetic Overflows: Rust provides built-in protections                    LLMs for automated transpilation to memory-safe languages and
against arithmetic overflows in debug mode, but does not perform               will encourage further research in this area.
runtime checks in release mode by default. Although these checks
can also be enabled in release mode, performing an overflow check              Acknowledgments
for every arithmetic expression can introduce a significant perfor-            We thank the anonymous reviewers for their constructive feed-
mance overhead in computation-intensive programs. Rust allows                  back. This work was supported by the Office of Naval Research
developers to selectively use methods such as checked_add and                  (ONR) through award N00014-24-1-2054, with additional support
checked_sub to handle overflows safely. Only 0.15% of correct                  by Amazon through the Amazon Research Awards program.
translations across all models use these check functions. In our
manual analysis of transpiled Rust programs corresponding to C
programs with arithmetic overflow vulnerabilities, we found that
SafeTrans: LLM-assisted Transpilation from C to Rust                                                                       ReCode ’26, April 12–18, 2026, Rio de Janeiro, Brazil


References                                                                                [25] Muhammad Muzammil, Abisheka Pitumpe, Xigao Li, Amir Rahmati, and Nick
 [1] [n. d.]. An AVL Tree Implementation In C. https://github.com/xieqing/avl-                 Nikiforakis. 2025. The Poorest Man in Babylon: A Longitudinal Study of Cryp-
     tree/tree/master.                                                                         tocurrency Investment Scams. In Proceedings of The Web Conference (WWW).
 [2] [n. d.]. url.h. https://github.com/jwerle/url.h/tree/master.                         [26] Vikram Nitin, Rahul Krishna, and Baishakhi Ray. 2024. Spectra: Enhancing the
 [3] Artisan-Lab. 2025. RAPx: Rust Analysis Platform. https://github.com/Artisan-              code translation ability of language models by generating multi-modal specifica-
     Lab/RAPx. https://github.com/Artisan-Lab/RAPx Accessed: 2025-05-13.                       tions. arXiv preprint arXiv:2405.18574 (2024).
 [4] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021.            [27] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025.
     Rudra: finding memory safety bugs in Rust at the ecosystem scale. In Proceedings          C2SaferRust: Transforming C Projects into Safer Rust with NeuroSymbolic Tech-
     of the ACM SIGOPS 28th Symposium on Operating Systems Principles. 84–99.                  niques. arXiv preprint arXiv:2501.14257 (2025).
 [5] Yubo Bai and Tapti Palit. 2025. RustAssure: Differential Symbolic Testing for        [28] Guangsheng Ou, Mingwei Liu, Yuxuan Chen, Xin Peng, and Zibin Zheng. 2024.
     LLM-Transpiled C-to-Rust Code. arXiv preprint arXiv:2510.07604 (2025).                    Repository-level code translation benchmark targeting Rust. arXiv preprint
 [6] Efe Bozkir, Süleyman Özdel, Ka Hei Carrie Lau, Mengdi Wang, Hong Gao, and                 arXiv:2411.13990 (2024).
     Enkelejda Kasneci. 2024. Embedding large language models into extended re-           [29] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lam-
     ality: Opportunities and challenges for inclusion, engagement, and privacy. In            bert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh
     Proceedings of the 6th ACM Conference on Conversational User Interfaces. 1–7.             Sinha, and Reyhaneh Jabbarvand. 2024. Lost in translation: A study of bugs
 [7] Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi. 2023. Fixing         introduced by large language models while translating code. In Proceedings of
     Rust compilation errors using LLMs. arXiv preprint arXiv:2308.05177 (2023).               the IEEE/ACM 46th International Conference on Software Engineering. 1–13.
 [8] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Trans-             [30] Ruchir Puri, David S Kung, Geert Janssen, Wei Zhang, Giacomo Domeniconi,
     lating C to Safer Rust. Proc. ACM Program. Lang. 5, OOPSLA, Article 121 (oct              Vladimir Zolotov, Julian Dolby, Jie Chen, Mihir Choudhury, Lindsey Decker, et al.
     2021).                                                                                    2021. Codenet: A large-scale AI for code dataset for learning a diversity of coding
 [9] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Maria Chris-               tasks. arXiv preprint arXiv:2105.12655 (2021).
     takis, Brandon Paulsen, Joey Dodds, and Daniel Kroening. 2024. Towards trans-        [31] Baptiste Roziere, Marie-Anne Lachaux, Lowik Chanussot, and Guillaume Lample.
     lating real-world code with LLMs: A study of translating to Rust. arXiv preprint          2020. Unsupervised Translation of Programming Languages. In Advances in
     arXiv:2405.11514 (2024).                                                                  Neural Information Processing Systems (NeurIPS), Vol. 33. 20601–20611.
[10] Mikhail R Gadelha, Felipe R Monteiro, Jeremy Morse, Lucas C Cordeiro, Bernd          [32] Ranjan Sapkota, Shaina Raza, Maged Shoman, Achyut Paudel, and Manoj Karkee.
     Fischer, and Denis A Nicole. 2018. ESBMC 5.0: an industrial-strength C model              2025. Image, Text, and Speech Data Augmentation using Multimodal LLMs for
     checker. In Proceedings of the 33rd ACM/IEEE International Conference on Auto-            Deep Learning: A Survey. arXiv preprint arXiv:2501.18648 (2025).
     mated Software Engineering. 888–891.                                                 [33] Scott Olson. [n. d.]. Miri: an Interpreter for Rust’s Mid-level Intermediate Repre-
[11] Jaemin Hong. 2023. Improving Automatic C-to-Rust Translation with Static                  sentation. https://github.com/rust-lang/miri.
     Analysis. In Proceedings of the 45th IEEE/ACM International Conference on Software   [34] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A Seshia, and Koushik Sen.
     Engineering (ICSE). 273–277.                                                              2024. Syzygy: Dual Code-Test C to (safe) Rust Translation using LLMs and
[12] Jaemin Hong and Sukyoung Ryu. 2023. Concrat: An automatic C-to-Rust lock                  Dynamic Analysis. arXiv preprint arXiv:2412.14234 (2024).
     API translator for concurrent programs. In 2023 IEEE/ACM 45th International          [35] Momoko Shiraishi and Takahiro Shinagawa. 2024. Context-aware Code Segmen-
     Conference on Software Engineering (ICSE). IEEE, 716–728.                                 tation for C-to-Rust Translation using Large Language Models. arXiv preprint
[13] Jaemin Hong and Sukyoung Ryu. 2024. Don’t Write, but Return: Replacing Output             arXiv:2409.10506 (2024).
     Parameters with Algebraic Data Types in C-to-Rust Translation. Proceedings of        [36] HoHyun Sim, Hyeonjoong Cho, Yeonghyeon Go, Zhoulai Fu, Ali Shokri, and
     the ACM on Programming Languages 8, PLDI (2024), 716–740.                                 Binoy Ravindran. 2025. Large Language Model-Powered Agent for C to Rust
[14] Jaemin Hong and Sukyoung Ryu. 2024. To Tag, or Not to Tag: Translating C’s                Code Translation. arXiv:2505.15858 [cs.PL] https://arxiv.org/abs/2505.15858
     Unions to Rust’s Tagged Unions. In Proceedings of the 39th IEEE/ACM International    [37] Marc Szafraniec, Baptiste Roziere, Hugh Leather, Francois Charton, Patrick La-
     Conference on Automated Software Engineering. 40–52.                                      batut, and Gabriel Synnaeve. 2022. Code translation with compiler representa-
[15] Rasha Ahmad Husein, Hala Aburajouh, and Cagatay Catal. 2025. Large language               tions. arXiv preprint arXiv:2207.03578 (2022).
     models for code completion: A systematic literature review. Computer Standards       [38] Norbert Tihanyi, Tamas Bisztray, Ridhi Jain, Mohamed Amine Ferrag, Lucas C
     & Interfaces 92 (2025), 103917. doi:10.1016/j.csi.2024.103917                             Cordeiro, and Vasileios Mavroeidis. 2023. The FormAI dataset: Generative AI in
[16] Ali Reza Ibrahimzada, Kaiyao Ke, Mrigank Pawagi, Muhammad Salman Abid,                    software security through the lens of formal verification. In Proceedings of the
     Rangeet Pan, Saurabh Sinha, and Reyhaneh Jabbarvand. 2025. AlphaTrans: A                  19th International Conference on Predictive Models and Data Analytics in Software
     Neuro-Symbolic Compositional Approach for Repository-Level Code Translation               Engineering. 33–43.
     and Validation. Proceedings of the ACM on Software Engineering 2, FSE (2025),        [39] Chaofan Wang, Tingrui Yu, Chen Xie, Jie Wang, Dong Chen, Wenrui Zhang,
     2454–2476.                                                                                Yuling Shi, Xiaodong Gu, and Beijun Shen. 2025. EvoC2Rust: A Skeleton-guided
[17] Ali Reza Ibrahimzada, Brandon Paulsen, Reyhaneh Jabbarvand, Joey Dodds,                   Framework for Project-Level C-to-Rust Translation. arXiv:2508.04295 [cs.SE]
     and Daniel Kroening. 2025. MatchFixAgent: Language-Agnostic Autonomous                    https://arxiv.org/abs/2508.04295
     Repository-Level Code Translation Validation and Repair. arXiv preprint              [40] HanXiang Xu, ShenAo Wang, Ningke Li, Kailong Wang, Yanjie Zhao, Kai Chen,
     arXiv:2509.16187 (2025).                                                                  Ting Yu, Yang Liu, and HaoYu Wang. 2024. Large language models for cyber
[18] Immunant. 2022. C2Rust. https://github.com/immunant/c2rust.                               security: A systematic literature review. arXiv preprint arXiv:2405.04760 (2024).
[19] Hamed Jelodar, Mohammad Meymani, and Roozbeh Razavi-Far. 2025. Large                 [41] Aidan ZH Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel
     Language Models (LLMs) for Source Code Analysis: applications, models and                 Kroening. 2024. VERT: Verified equivalent Rust transpilation with large language
     datasets. arXiv preprint arXiv:2503.17502 (2025).                                         models as few-shot learners. arXiv preprint arXiv:2404.18852 (2024).
[20] Yoonsang Kim, Zainab Aamir, Mithilesh Singh, Saeed Boorboor, Klaus Mueller,          [42] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
     and Arie E. Kaufman. 2025. Explainable XR: Understanding User Behaviors of                Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and unleashing the power
     XR Environments using LLM-assisted Analytics Framework. IEEE Transactions                 of large language models in automated code translation. Proceedings of the ACM
     on Visualization and Computer Graphics (2025).                                            on Software Engineering 1, FSE (2024), 1585–1608.
[21] Ruishi Li, Bo Wang, Tianyu Li, Prateek Saxena, and Ashish Kundu. 2024. Trans-        [43] Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, and Daniel
     lating C to Rust: Lessons from a user study. arXiv preprint arXiv:2411.14174              Kroening. 2024. Scalable, validated code translation of entire projects using large
     (2024).                                                                                   language models. arXiv preprint arXiv:2412.08035 (2024).
[22] Tianyu Li, Ruishi Li, Bo Wang, Brandon Paulsen, Umang Mathur, and Prateek            [44] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership
     Saxena. 2025. Adversarial Agent Collaboration for C to Rust Translation. arXiv            guided C to Rust translation. In International Conference on Computer Aided
     preprint arXiv:2510.03879 (2025).                                                         Verification. Springer, 459–482.
[23] Tianle Li, Ge Zhang, Quy Duc Do, Xiang Yue, and Wenhu Chen. 2024.                    [45] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill Levchenko,
     Long-context LLMs struggle with long in-context learning. arXiv preprint                  and Varun Chandrasekaran. 2025. LLM-Driven Multi-step Translation from C to
     arXiv:2404.02060 (2024).                                                                  Rust using Static Analysis. arXiv preprint arXiv:2503.12511 (2025).
[24] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele
     Bevilacqua, Fabio Petroni, and Percy Liang. 2024.                   Lost in the
     Middle: How Language Models Use Long Contexts.                       Transactions
     of the Association for Computational Linguistics 12 (02 2024), 157–
     173.         doi:10.1162/tacl_a_00638 arXiv:https://direct.mit.edu/tacl/article-
     pdf/doi/10.1162/tacl_a_00638/2336043/tacl_a_00638.pdf
ReCode ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                         Farrukh et al.


A Appendix                                                             Table 3: Comparison of C-to-Rust translation tools on the
                                                                       url_parser (UP) and avl_tree (AT) programs.
A.1 Comparison with Prior C-to-Rust
    Translation Tools                                                     Tool          Model         Prog. Comp. Safe Comments

Table 3 summarizes each tool’s reported performance across three          C2SaferRust   gpt-4o-mini   UP     ✓    ×   Reports unsafe lines; no test cov-
                                                                                                                      erage mentioned.
metrics: compilation success, complete code safety, and verification
                                                                          VERT          gpt-4         UP     ×    –   Complete translation fails to com-
completeness. These include mostly prototype tools that require                                                       pile.
non-trivial setup, and in some cases manual intervention in appro-                      claude-2      AT     ✓    –   Only subset of functions trans-
                                                                                                                      lated.
priately formatting the source programs. Therefore, the presented
                                                                          FLOURINE      claude-3.5    UP     ×    –   Complete translation fails to com-
results have been gathered directly from the respective publications                                                  pile.
describing each tool, rather than from independent experimenta-           SACTOR        gpt-4o        UP     ✓    ×   Partially idiomatic; fails verifica-
tion.                                                                                                                 tion.
                                                                                        gpt-4o        AT     ✓    ×   Partially idiomatic; fails verifica-
                                                                                                                      tion.
                                                                          SafeTrans     gpt-4o        UP     ✓    ✓   Passes partial verification.
                                                                                        gpt-4o        AT     ✓    ✓   Passes partial verification.
