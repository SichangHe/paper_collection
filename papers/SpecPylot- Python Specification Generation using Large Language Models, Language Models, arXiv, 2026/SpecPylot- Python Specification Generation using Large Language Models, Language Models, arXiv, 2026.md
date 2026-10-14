                                                    SpecPylot: Python Specification Generation using Large
                                                                      Language Models
                                                                   Ragib Shahariar Ayon                                                               Shibbir Ahmed
                                                                      Texas State University                                                        Texas State University
                                                                      San Marcos, TX, USA                                                           San Marcos, TX, USA
                                                                        ipd21@txstate.edu                                                            shibbir@txstate.edu

                                         Abstract                                                                                explicit specifications such as preconditions, postconditions, or in-
                                         Automatically generating formal specifications could reduce the ef-                     variants are missing altogether, which limits the applicability of au-
                                         fort needed to improve program correctness, but in practice, this is                    tomated verification and testing techniques in practice. This gap be-
                                                                                                                                 tween available analysis tools and real-world code has been widely
arXiv:2604.16560v1 [cs.SE] 17 Apr 2026




                                         still challenging. Many developers avoid writing contracts by hand,
                                         which limits the use of automated verification tools. Recent large                      observed in prior work on specification inference and contract-
                                         language models (LLMs) can generate specifications from code, but                       based verification [7, 8].
                                         these specifications often fail in terms of verification. The reason                       Recent LLMs appear promising in this space. Given source code,
                                         is syntax errors, overly strict constraints, or mismatches with pro-                    they can often articulate high-level behavioral constraints that re-
                                         gram behavior. We present SpecPylot, a Python tool that synthesizes                     semble human-written specifications, as demonstrated in several
                                         executable specifications for Python programs as icontract an-                          recent studies on LLM-assisted specification and invariant gen-
                                         notations and checks them using CrossHair’s symbolic execution.                         eration [6, 14, 18]. However, specifications produced directly by
                                         The tool relies on LLMs to propose candidate contracts and uses                         LLMs are frequently problematic. They may be inconsistent, overly
                                         CrossHair to validate them. When CrossHair finds a concrete                             restrictive, or incorrect regarding the program’s actual behavior.
                                         counterexample, SpecPylot updates only the generated contracts                          Furthermore, this issue was also reported in prior work evaluating
                                         and leaves the program itself untouched. In addition, the tool can                      LLM-generated specifications under formal verification [11, 12].
                                         produce coverage-driven pytest stubs and keep detailed execution                        Without validation, such contracts are difficult to reuse or trust.
                                         artifacts that are useful during debugging. Overall, the evaluation                        We present SpecPylot, a contract synthesis and verification pipeline
                                         indicates that SpecPylot is able to generate CrossHair-compatible                       for Python that addresses this gap by combining LLM-based specifi-
                                         contracts for most programs, but it also highlights the practical                       cation generation with solver-backed symbolic execution. SpecPylot
                                         limits introduced by bounded symbolic exploration and differences                       first asks an LLM to produce executable contracts as icontract [15]
                                         in LLM behavior.                                                                        annotations, and then relies on CrossHair to check whether those
                                                                                                                                 contracts are consistent with the program. If CrossHair finds a con-
                                                                                                                                 crete counterexample, SpecPylot uses that information to trigger
                                         CCS Concepts
                                                                                                                                 a refinement step. In that refinement step, the model is asked to
                                         • Software and its engineering → Formal software verifica-                              revise the contracts while leaving the underlying code untouched.
                                         tion.                                                                                   This design is inspired by recent verifier in the loop approaches
                                                                                                                                 for specification refinement, which were adapted to the Python
                                         Keywords                                                                                ecosystem and executable contracts [12, 21].
                                         Specification, Large Language Model, Python                                                At a high level, SpecPylot treats specification generation and
                                                                                                                                 specification checking as two separate concerns. The LLM is re-
                                         ACM Reference Format:                                                                   sponsible for proposing candidate semantic constraints. However,
                                         Ragib Shahariar Ayon and Shibbir Ahmed. 2026. SpecPylot: Python Specifica-              CrossHair acts as an execution based sanity check that can either
                                         tion Generation using Large Language Models. In 34th ACM Joint European                 confirm those constraints or expose concrete violations within a
                                         Software Engineering Conference and Symposium on the Foundations of Soft-
                                                                                                                                 bounded search. By iteratively refining contracts using counterex-
                                         ware Engineering (FSE Companion ’26), July 5–9, 2026, Montreal, QC, Canada.
                                         ACM, New York, NY, USA, 5 pages. https://doi.org/10.1145/3803437.3806427
                                                                                                                                 amples, SpecPylot improves specification quality without requiring
                                                                                                                                 manual intervention from the human developer.
                                                                                                                                    SpecPylot is implemented as a practical research tool rather than
                                         1    Introduction                                                                       a mere prototype. It supports multiple LLM backends, configurable
                                                                                                                                 verification and refinement budgets, and optional coverage-driven
                                         Writing software specifications is still a slow and error-prone pro-
                                                                                                                                 test generation. Our evaluation shows that SpecPylot can generate
                                         cess, even for experienced developers. In many Python projects,
                                                                                                                                 checkable specifications for most programs in a small benchmark,
                                                                                                                                 while also highlighting the limitations imposed by bounded sym-
                                                                                                                                 bolic execution and the variability of LLM-generated contracts.
                                                                                                                                    In summary, this work makes the following contributions.
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         FSE Companion ’26, Montreal, QC, Canada                                                     • We designed and developed SpecPylot, a Python tool designed
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2636-1/26/07                                                              to generate executable specifications using LLMs, while also
                                         https://doi.org/10.1145/3803437.3806427                                                       verifying them through symbolic execution.
FSE Companion ’26, July 5–9, 2026, Montreal, QC, Canada                                                      Ragib Shahariar Ayon and Shibbir Ahmed


     • Our approach allows the use of concrete counterexamples                           SpecPylot                    Refinement Loop
       from CrossHair to refine and correct any incorrect or overly
       strict contracts, without changing the original program.
     • The system is built to be practical and user-friendly, sup-
       porting various LLM providers, offering user-defined limits                      Prompts      Large Language     Contracts        Verify
                                                                        Python Code
       for verification and refinement, and including optional test                                       Model       Annotated code    Contracts
       generation based on coverage analysis.
     • We evaluated the tool on a small set of Python programs,
       providing insights into which types of specifications can be
       verified, how long the process takes, and the costs involved.
                                                                                              Verified                             Generated
                                                                                            Python Code         Test Cases         Metadata
2    Related Work/Research Gap
Earlier work on automatic specification generation relied on pro-                       Figure 1: Overview of SpecPylot.
gram analysis to extract properties from code. More recent ap-
proaches use learning-based techniques, including large language
models. SpecPylot builds on this direction by focusing on how LLM-      specifications are written manually and therefore do not address
generated specifications can be made usable under execution-based       the cost of producing contracts. Related work in other language
verification. Before LLMs were widely used, most work on spec-          ecosystems follows similar ideas under different assumptions. Au-
ification inference relied on static or dynamic analysis. Dynamic       toReSpec [4] targets Java and JML, combining multiple LLMs with
invariant detectors such as Daikon [8] infer properties by observ-      verifier feedback to improve robustness. In contrast, SpecPylot fo-
ing execution traces, while static techniques based on constraint       cuses on Python, executable icontract specifications, and refine-
solving or abstract interpretation attempt to establish lightweight     ment guided by concrete counterexamples from symbolic execution.
correctness guarantees [2, 7]. Several hybrid approaches combine        By closely coupling specification generation with execution-based
these ideas with symbolic execution or mutation strategies [6, 13].     validation, SpecPylot supports iterative refinement and enables
Although these methods can be effective in controlled settings,         analysis of both successful and failing cases in practice.
they often depend on restricted specification grammars, limited
language features, or substantial manual effort. In practice, this      3     SpecPylot Approach
makes them difficult to apply to realistic Python programs.
    More recently, researchers have explored using large language       SpecPylot is a contract synthesis and verification pipeline for Python.
models to generate specifications directly from source code. This       Given a target program, it prompts an LLM to produce icontract-
direction builds on the strong performance of LLMs in related tasks     annotated code and uses CrossHair to check whether the inferred
such as code generation [20], summarization [1], and defect predic-     contracts are consistent with the program behavior. Figure 1 sum-
tion [10]. Several studies report that LLMs can produce invariants      marizes the data flow of SpecPylot, including the verification and
or contracts that resemble those written by developers [6, 14, 18].     refinement loop and its termination conditions. Users can configure
SpecGen [12], for example, combines few-shot prompting with             the LLM backend, refinement budgets, and CrossHair exploration
mutation-based heuristics to generate JML specifications that can       limits (Section 5).
be checked by a verifier. Other approaches filter model outputs
using ranking or static analysis. A common limitation across this       3.1    Contract generation
line of work is that specification generation is typically treated as   SpecPylot renders an LLM request from prompt templates, and
a one-shot activity, using fixed prompts or a single model, with        the target program, and the model returns a single, well-formed
little support for diagnosing or repairing incorrect specifications.    wrapper containing contract-annotated code. The pipeline validates
Alongside generation techniques, some efforts concentrate on eval-      the wrapper and basic syntactic well-formedness. If the output does
uation rather than generation. FormalBench [11] examines the            not conform, SpecPylot retries a bounded number of times with
robustness and consistency of LLM-generated specifications un-          explicit formatting repair instructions before proceeding.
der different prompting strategies. Agent-based frameworks such            Here we provide a concrete example of the contract produced
as CodeVisionary [17] and RepoMasterEval [19] study collabora-          by SpecPylot. Listing 1 shows an icontract-annotated implemen-
tive reasoning in code generation more broadly. Recent work also        tation of Absolute.absolute generated by SpecPylot. The exam-
explores verifier-in-the-loop approaches that use test oracles or       ple illustrates how SpecPylot expresses input assumptions using
formal feedback to refine generated annotations [9]. While these        @require (e.g., restricting num to an int) and encodes postcon-
approaches show promising results in verification-aware languages       ditions using @ensure (e.g., ensuring the return value is a non-
such as Dafny, they target different ecosystems and rely on test        negative integer and matches the mathematical definition of abso-
assertions as primary specification oracles.                            lute value for both non-negative and negative inputs).
    In the Python ecosystem, the Python-by-Contract dataset [21]           These examples are intended to make the generated contracts
provides a collection of programs annotated with executable icon-       concrete and to facilitate reproduction and inspection of SpecPylot’s
tract specifications [15] and has been used to evaluate tools such      outputs. The class-based formulation in the listing 1 came from the
as CrossHair [16]. These resources are valuable, but they assume        dataset example rather than from any requirement of the approach.
    SpecPylot : Python Specification Generation using Large Language Models                             FSE Companion ’26, July 5–9, 2026, Montreal, QC, Canada


    The approach itself is general and applies equally to ordinary top-            to Python, and added four sequential Python programs, yielding
    level functions.                                                               20 programs total across five types. We have used two best models,
1  # icontract annotated code                                                      Claude Sonnet 4.5 and GPT-4o, inspired by prior research on JML
2  from icontract import require, ensure                                           specification generation [4, 11, 12]. Experiments ran on an Apple M4
 3 class Absolute:
                                                                                   MacBook Pro (24GB RAM). SpecPylot is implemented in Python 3.12.
 4     @require(lambda num: isinstance(num, int))                                  We use this dataset to evaluate both the effectiveness and efficiency
 5     @ensure(lambda result: isinstance(result, int))                             of SpecPylot.
 6     @ensure(lambda result: result >= 0)
 7     @ensure(lambda num, result: (num >= 0 and result ==
                                                                                   4.1      Effectiveness of SpecPylot
        num) or (num < 0 and result == -num))
 8     def absolute(self, num: int) -> int:
 9         if 0 <= num:                                                             claude sonnet 4 5                                   80%                   20%
10             return num
11         else:                                                                               gpt 4o                         75%                            25%

12             return -num                                                                                                       Passed       Inconclusive
    Listing 1: icontract-annotated                    implementation          of
    Absolute.absolute.                                                             Figure 2: Pass and inconclusive rates of SpecPylot across 20
    3.2    Verification with CrossHair                                             programs for Claude Sonnet 4.5 and GPT-4o.
    SpecPylot invokes CrossHair check with icontract analysis on
    the annotated code. The outcome is classified into three statuses                  To evaluate the ef-
    used throughout the pipeline: PASSED when no counterexample                    fectiveness of SpecPylot,
                                                                                                                              CONFIRMED        UNKNOWN
    is found and the analysis is exhaustive under the configured lim-              we report the pass rate
    its, REFUTED when CrossHair produces a counterexample for at                   and inconclusive rate,
    least one contract, and INCONCLUSIVE when CrossHair finds no                   i.e., the fraction of pro-       140
    counterexample but cannot exhaustively explore the relevant paths              grams labeled PASSED
                                                                                   and INCONCLUSIVE out             120
    under the limits.




                                                                                                                    Average number of paths
                                                                                   of the total dataset size.       100 91.5
    3.3    Budgeted counterexample-driven                                          Figure 2 visualizes these
           refinement                                                              rates as percentages for          80
                                                                                   GPT-4o and Claude Son-
    Refinement is triggered only on REFUTED runs that satisfy a user-
                                                                                   net 4.5. Using Anthropic’s        60
    defined budget policy. Concretely, a refutation qualifies for refine-
                                                                                   Claude Sonnet 4.5 with            40
                                                                                                                                           42.0
    ment only when a concrete counterexample is reported, the check
                                                                                   SpecPylot, we achieved a
    run does not time out, and the refutation is produced within the re-                                             20
                                                                                   pass rate of 80% (16/20)                       11.2
    finement time budget. When refinement is allowed, SpecPylot builds
                                                                                   and an inconclusive rate                                       4.8
    a second LLM request containing (i) the current annotated code
                                                                                   of 20% (4/20). Using               0  claude-sonnet-4-5   gpt-4o
    and (ii) a compact evidence bundle extracted from CrossHair (for
                                                                                   OpenAI’s GPT-4o with
    example, the failing call and diagnostic context). The LLM revises
                                                                                   SpecPylot, we achieved a
    only the contracts, and SpecPylot re-runs CrossHair on the revised                                            Figure 3: Average CONFIRMED
                                                                                   pass rate of 75% (15/20)
    code. This loop continues until the run becomes PASSED, becomes                                               and UNKNOWN paths explored
                                                                                   and an inconclusive rate
    INCONCLUSIVE, or reaches the maximum refinement rounds.                                                       by CrossHair for INCONCLUSIVE
                                                                                   of 25% (5/20).
                                                                                                                  cases.
                                                                                       INCONCLUSIVE cases
    3.4    Optional test-case generation and artifacts                             commonly arise for loop-
    When enabled, SpecPylot runs CrossHair cover on the final anno-                heavy or highly branched code, where path explosion and time-
    tated code to emit coverage-driven examples as pytest stubs. Each              out limits prevent exhaustive exploration; thus, the absence of
    run stores the final annotated program and a structured summary                a counterexample reflects an incomplete search rather than a
    of outcomes, including verification status, refutation evidence when           proof. Figure 3 reports the average number of paths explored for
    present, and refinement traces. If logging is enabled, SpecPylot ad-           INCONCLUSIVE cases, and the error bars represent standard mean
    ditionally records prompts, raw model outputs, intermediate code               error. For contracts generated by Claude Sonnet 4.5, CrossHair
    versions, and CrossHair stdout/stderr to support debugging and                 explored on average 91 CONFIRMED paths and 11.2 UNKNOWN paths;
    reproducible evaluation.                                                       for GPT-4o, the averages were 42 CONFIRMED paths and 4.8 UNKNOWN
                                                                                   paths. In our evaluation, the INCONCLUSIVE cases were add_loop,
    4     Experimental Results and Evaluation                                      binary_search, mysqrt, and digit_root (for both Claude Son-
    To evaluate SpecPylot, we randomly selected 16 SpecGenBench                    net 4.5 and GPT-4o), and calculator (for GPT-4o). Across both
    programs [12] across four control-flow categories (branched, single-           models, these INCONCLUSIVE outcomes are associated with pro-
    loop, multi-path loop, and nested loop), translated them from Java             grams featuring multi-path loop control flow and/or nested loops,
    FSE Companion ’26, July 5–9, 2026, Montreal, QC, Canada                                                   Ragib Shahariar Ayon and Shibbir Ahmed


    which expand the symbolic search space beyond what CrossHair            Verification is performed using crosshair check. When coverage
    can cover within the configured per-path and per-condition bud-         is enabled, SpecPylot additionally invokes crosshair cover to
    gets, causing it to return an UNKNOWN-style outcome rather than         generate coverage-driven pytest stubs. Timeouts and exploration
    CONFIRMED over all paths.                                               limits can be configured independently for checking and coverage,
                                                                            including overall timeout, per-condition timeout, per-path timeout,
    4.2     Efficiency of SpecPylot                                         and the maximum number of uninteresting iterations. These set-
    We evaluate the efficiency of SpecPylot in terms of end-to-end run-     tings control how thoroughly CrossHair explores execution paths.
    time and API cost when paired with GPT-4o and Claude Sonnet 4.5.        Finally, users specify output and log directories. When logging is
    We conducted an efficiency comparison between Claude Sonnet 4.5         enabled, SpecPylot records LLM prompts and responses, interme-
    and GPT-4o when used with SpecPylot. Each point summarizes the          diate annotated code, and CrossHair stdout and stderr, which
    average per-issue cost in two dimensions: the x-axis shows average      supports debugging and reproducible evaluation.
    end-to-end runtime (including contract generation, refinement, and
    CrossHair analysis), while the y-axis shows average token con-          6   Limitations
    sumption (in thousands). Lower values on both axes indicate a more      This work has several limitations worth keeping in mind. When
    efficient configuration. In our evaluation, GPT-4o is faster on aver-   CrossHair reports a PASSED result, this should not be interpreted
    age, whereas Claude Sonnet 4.5 tends to use more tokens per issue.      as a proof of correctness. It only means that no counterexample was
    Both GPT-4o and Claude Sonnet 4.5 required refinement in only           found within the chosen exploration limits, and bugs may still exist.
    a small subset of tasks, averaging 1.2 total LLM iterations per run,    Similarly, INCONCLUSIVE results indicate that exploration stopped
    indicating minimal reliance on the refinement loop. Refinement          early, because of UNKNOWN paths, rather than that the contracts are
    overlapped on binary_search.py and calculator.py, with GPT-             correct. In our experience, programs with deep loops or complex
    specific cases (gcd.py, is_all_unique.py) and a Claude-specific         branching quickly stress symbolic execution and lead to timeouts,
    case (divide.py). GPT consistently required a single refinement         which makes results sensitive to the configured budgets. The qual-
    pass, whereas Claude required two passes for divide.py, result-         ity of results also depends on the typing information. CrossHair
    ing in slightly higher refinement effort in that case. Total runtime    performs noticeably better when types are precise, while imprecise
    is primarily driven by closed-source LLM response latency and           annotations can restrict the explored inputs or cause internal errors.
    CrossHair’s symbolic search, as well as test case generation. Over-     Finally, the contracts generated by LLMs should be viewed as best-
    all, GPT-4o is faster and less expensive, while achieving a slightly    effort suggestions. They can be incomplete, overly strong, or simply
    lower pass rate than Claude Sonnet 4.5. On average, Claude Sonnet       unhelpful; results vary across models and configurations, and our
    4.5 uses 5,480 tokens per issue, and GPT-4o uses 4,756 tokens per       conclusions are necessarily limited by the size of the evaluation.
    issue; both models converge quickly, requiring 1.02 refinement it-
    erations on average. Across all 20 programs, the total API cost is      7   Conclusion and Future Work
    $1.09 for Claude Sonnet 4.5 and $0.80 for GPT-4o.                       In this work, we presented SpecPylot, a pipeline for automatically
                                                                            annotating Python programs with executable contracts and check-
    5     Usage of SpecPylot                                                ing them using CrossHair ’s solver-backed symbolic execution.
    SpecPylot is invoked from the command line. Users provide a tar-        We evaluated the tool with two widely used closed-source LLMs,
    get file and can set options that control provider selection, refine-   GPT-4o and Claude Sonnet 4.5, and examined both how often the
    ment behavior, CrossHair limits, and artifact logging. The pipeline     generated contracts could be verified and the time and cost of the
    stages are described in Section 3. A typical invocation executing       end-to-end process. Across our benchmark, SpecPylot generated
    SpecPylot on absolute.py using GPT-4o, enabling 2 refinements           CrossHair-compatible contracts for most programs, but the results
    and coverage-driven test generation as below:                           also highlight several practical limitations. In particular, bounded
                                                                            symbolic exploration and variability in LLM-generated specifica-
1   $ specpylot --target ./absolute.py --provider openai \
                                                                            tions continue to affect verification outcomes. This is especially for
2     --model gpt-4o --refine 2 --coverage
                                                                            programs with complex control flow. In the future, we can extend
                                                                            the tool to support PEP 316-style docstring contracts in addition to
    5.1     Configuration and controllable parameters                       icontract. We also intend to explore LLM-agent workflows that
    SpecPylot provides a small set of configuration options that allow      operate at the repository level, using a broader project context to
    users to balance cost, runtime, and the amount of recorded artifacts.   guide contract generation across multiple files and modules. We
    Users first select an LLM provider and model, and may adjust decod-     also plan to evaluate the approach on real-world contracts mined
    ing parameters such as temperature. API credentials are supplied        from recent GitHub repositories to assess generalization beyond
    via environment variables or a local .env file, which is loaded at      LLM training data.
    startup. The tool also exposes controls for retries and refinement.
    Users can configure the maximum number of retries for format-           8   Data Availability and Tool Demo
    ting or parsing failures, the number of refinement rounds, and          The reproduction package, evaluation results, and dataset are avail-
    an optional refinement budget. This budget limits refinement to         able in Zenodo [5], and we provide a tool demonstration in YouTube [3].
    refutations produced within a user-defined time window, which           We hope these artifacts serve as a useful resource for future research
    helps bound the number of additional LLM calls in difficult cases.      in this area.
SpecPylot : Python Specification Generation using Large Language Models                                             FSE Companion ’26, July 5–9, 2026, Montreal, QC, Canada


References                                                                                     Computational Linguistics (Volume 1: Long Papers), Wanxiang Che, Joyce Nabende,
 [1] Toufique Ahmed and Premkumar Devanbu. 2022. Few-shot training llms for                    Ekaterina Shutova, and Mohammad Taher Pilehvar (Eds.). Association for Com-
     project-specific code-summarization. In Proceedings of the 37th IEEE/ACM inter-           putational Linguistics, Vienna, Austria, 21991–22014. doi:10.18653/v1/2025.acl-
     national conference on automated software engineering. 1–5.                               long.1068
 [2] Anoud Alshnakat, Dilian Gurov, Christian Lidström, and Philipp Rümmer. 2020.         [12] Lezhi Ma, Shangqing Liu, Yi Li, Xiaofei Xie, and Lei Bu. 2025. SpecGen: Automated
     Constraint-based contract inference for deductive verification. Deductive Software        Generation of Formal Program Specifications via Large Language Models. In 2025
     Verification: Future Perspectives: Reflections on the Occasion of 20 Years of KeY         IEEE/ACM 47th International Conference on Software Engineering (ICSE). 16–28.
     (2020), 149–176.                                                                          doi:10.1109/ICSE55347.2025.00129
 [3] Ragib Shahariar Ayon. 2026. Specpylot Tool Demonstration. https://youtu.be/K         [13] Facundo Molina, Pablo Ponzio, Nazareno Aguirre, and Marcelo Frias. 2021.
     az4Bvb93ro. [Online; accessed Jan-2026].                                                  EvoSpex: An evolutionary algorithm for learning postconditions. In 2021
 [4] Ragib Shahariar Ayon and Shibbir Ahmed. 2026. AutoReSpec: A Framework for                 IEEE/ACM 43rd International Conference on Software Engineering (ICSE). IEEE,
     Generating Specification using Large Language Models. In Proceedings of the 2026          1223–1235.
     IEEE/ACM Third International Conference on AI Foundation Models and Software         [14] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. 2023.
     Engineering (FORGE ’26) (Rio de Janeiro, Brazil). ACM, New York, NY, USA, 1–11.           Can large language models reason about program invariants?. In International
     doi:10.1145/3793655.3793731                                                               Conference on Machine Learning. PMLR, 27496–27520.
 [5] Ragib Shahariar Ayon and Shibbir Ahmed. 2026. Replication Package of the FSE         [15] Marko Ristin. 2017. icontract-hypothesis - Combine contracts and automatic
     2026 Tool Demo Paper Entitled "SpecPylot: Python Specification Generation using           testing. https://github.com/mristin/icontract-hypothesis. [Online; accessed
     Large Language Models". Zenodo. doi:10.5281/zenodo.19491112 Accepted at the               20-July-2022].
     34th ACM Joint European Software Engineering Conference and Symposium on             [16] Phillip Schanely. 2017. CrossHair - An analysis tool for Python that blurs the
     the Foundations of Software Engineering (FSE Companion ’26), Montreal, QC,                line between testing and type systems. https://github.com/pschanely/CrossHair.
     Canada..                                                                                  [Online; accessed 20-July-2022].
 [6] Saikat Chakraborty, Shuvendu Lahiri, Sarah Fakhoury, Akash Lal, Madanlal             [17] Xinchen Wang, Pengfei Gao, Chao Peng, Ruida Hu, and Cuiyun Gao. 2025. Code-
     Musuvathi, Aseem Rastogi, Aditya Senthilnathan, Rahul Sharma, and Nikhil                  Visionary: An Agent-based Framework for Evaluating Large Language Models
     Swamy. 2023. Ranking llm-generated loop invariants for program verification. In           in Code Generation. arXiv:2504.13472 [cs.SE] https://arxiv.org/abs/2504.13472
     Findings of the Association for Computational Linguistics: EMNLP 2023. 9164–9175.    [18] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun
 [7] Patrick Cousot, Radhia Cousot, Manuel Fähndrich, and Francesco Logozzo. 2013.             Li, Shing-Chi Cheung, and Cong Tian. 2024. Enchanting program specification
     Automatic inference of necessary preconditions. In International Workshop on              synthesis by large language models using static analysis and program verification.
     Verification, Model Checking, and Abstract Interpretation. Springer, 128–148.             arXiv preprint arXiv:2404.00762 (2024).
 [8] Michael D Ernst, Jeff H Perkins, Philip J Guo, Stephen McCamant, Carlos Pacheco,     [19] Qinyun Wu, Chao Peng, Pengfei Gao, Ruida Hu, Haoyu Gan, Bo Jiang, Jinhe Tang,
     Matthew S Tschantz, and Chen Xiao. 2007. The Daikon system for dynamic                    Zhiwen Deng, Zhanming Guan, Cuiyun Gao, et al. 2024. Repomastereval: Evalu-
     detection of likely invariants. Science of computer programming 69, 1-3 (2007),           ating code completion via real-world repositories. arXiv preprint arXiv:2408.03519
     35–45.                                                                                    (2024).
 [9] João Pascoal Faria, Emanuel Trigo, Vinicius Honorato, and Rui Abreu. 2026.           [20] Zhengran Zeng, Hanzhuo Tan, Haotian Zhang, Jing Li, Yuqun Zhang, and Ling-
     Automatic Generation of Formal Specification and Verification Annotations                 ming Zhang. 2022. An extensive study on pre-trained models for program under-
     Using LLMs and Test Oracles. arXiv preprint arXiv:2601.12845 (2026).                      standing and generation. In Proceedings of the 31st ACM SIGSOFT international
                                                                                               symposium on software testing and analysis. 39–51.
[10] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li, Xiapu Luo,
                                                                                          [21] Jiyang Zhang, Marko Ristin, Phillip Schanely, Hans Wernher van de Venn, and
     David Lo, John Grundy, and Haoyu Wang. 2024. Large language models for
                                                                                               Milos Gligoric. 2022. Python-by-Contract Dataset. In Proceedings of the 30th
     software engineering: A systematic literature review. ACM Transactions on
                                                                                               ACM Joint European Software Engineering Conference and Symposium on the
     Software Engineering and Methodology 33, 8 (2024), 1–79.
                                                                                               Foundations of Software Engineering (ESEC/FSE). ACM, 1652–1656.
[11] Thanh Le-Cong, Bach Le, and Toby Murray. 2025. Can LLMs Reason About
     Program Semantics? A Comprehensive Evaluation of LLMs on Formal Specifica-
     tion Inference. In Proceedings of the 63rd Annual Meeting of the Association for
