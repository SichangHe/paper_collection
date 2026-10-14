                                              Consistency Meets Verification: Enhancing Test
                                              Generation Quality in Large Language Models
                                                     Without Ground-Truth Solutions
                                            1st Hamed Taherkhani        2nd Alireza DaghighFarsoodeh           3rd Mohammad Chowdhury             4th Hung Viet Pham
                                               York University                   York University                      York University                York University
                                               Toronto, Canada                   Toronto, Canada                      Toronto, Canada                Toronto, Canada
                                              hamedth@yorku.ca                  aliredaq@yorku.ca                    ehsansh@yorku.ca               hvpham@yorku.ca

                                                                                                5th Hadi Hemmati
arXiv:2602.10522v1 [cs.SE] 11 Feb 2026




                                                                                                  York University
                                                                                                  Toronto, Canada
                                                                                                 hemmati@yorku.ca



                                            Abstract—Large Language Models (LLMs) have significantly         due to hallucination, where models invent code that looks
                                         advanced automated test generation, yet existing methods often      plausible but is incorrect. They argue that post-processing
                                         rely on ground-truth code for verification, risking bug propa-      strategies are needed to mitigate hallucinations.
                                         gation and limiting applicability in test-driven development. We
                                         present ConVerTest, a novel two-stage pipeline for synthesizing        Other studies have explored generating valid LLM-based
                                         reliable tests without requiring prior code implementations.        test cases, generally relying on execution of ground-truth code
                                         ConVerTest integrates three core strategies: (i) Self-Consistency   solutions for verifying tests [15]–[18]. However, generating
                                         (SC) to generate convergent test cases via majority voting; (ii)    tests from the code under test is risky because any bugs in the
                                         Chain-of-Verification (CoVe) for iterative, reasoning-guided code   implementation can be reflected into the tests, making faulty
                                         refinement; and (iii) a Dual Execution Agreement to cross-
                                         validate code and tests through consensus. Experiments on           behavior appear correct. Such tests capture what the code
                                         B IG C ODE B ENCH and L ESS BASIC P YTHON P ROBLEMS (LBPP)          currently does rather than what it should do, which undermines
                                         benchmarks demonstrate that ConVerTest improves test validity,      their ability to detect errors. In some real-world scenarios like
                                         line coverage, and mutation scores by up to 39%, 28%, and 18%       test-driven development, the code does not even exist yet, so
                                         respectively over baselines. Our findings highlight ConVerTest as   relying on it for test generation is impossible. By contrast,
                                         a robust solution for mitigating hallucinations and enhancing the
                                         reliability of autonomous software testing agents.                  generating tests from natural language description ties them
                                            Index Terms—Testing, Verification, Large Language Models,        to the intended behavior, ensuring tests remain independent,
                                         Consistency                                                         meaningful, and capable of revealing mistakes. Moreover,
                                                                                                             generating test cases from natural language is one of the core
                                                               I. I NTRODUCTION                              components of code generation agents, where they heavily
                                            LLMs have been successfully applied to a wide range              rely on valid and useful test cases in their feedback loop
                                         of coding tasks in recent years, including automated test           to debug generated code solutions [19]–[23]. Generating tests
                                         generation [1]–[5]. However, several challenges remain. A           without relying on code solutions is particularly challenging
                                         central difficulty in LLM-based test generation lies in verifying   because there is no ground-truth implementation to provide
                                         the correctness of the generated test cases [2], [6]–[8]. For       feedback and refine the tests, so instead we need to develop a
                                         example, as shown in Table I, only 35–51% of tests generated        method that enforces consistency and mitigates hallucinations
                                         by Gemma3.3 on BigCodeBench [9] and 54–73% of those                 to synthesize valid and reliable test cases.
                                         generated by CodeQwen3 on LBPP [10] are valid. This raises             Hallucination mitigation techniques can be applied in multi-
                                         a fundamental question: how to verify the verifier (the test        ple stages of LLM workflows, during and after generation [24].
                                         cases)?                                                             In this paper, we propose ConVerTest, which adapts and
                                            Existing LLM-based test generation creates a ”circularity of     extends existing methods to improve the reliability and con-
                                         error” by using the implementation under test as the ground-        sistency of automated test generation in software development.
                                         truth oracle. This approach fails to detect faulty behavior         Our method incorporates Self-Consistency (SC) [25] and
                                         because tests are generated to match current code logic rather      Chain-of-Verification (CoVe) [26] to mitigate hallucinations
                                         than intended specifications. Some recent studies have raised       during the generation stage without relying on a ground-truth
                                         hallucination issues that cause invalid test generation [2], [6]–   code solution. However, as shown in Section V, enforcing
                                         [8], [11]–[14]. Yang et al. [14] find that a substantial share of   consistency during generation alone is insufficient for produc-
                                         LLM-generated unit tests are invalid (often 34–62%), mainly         ing valid tests. A post-generation step is therefore necessary
to filter out remaining invalid tests. To this end, we adopt          LLMs. The model (1) generates an initial draft, (2) creates
a dual-agreement strategy [27] as a verification mechanism,           verification questions to scrutinize its own claims and as-
whereby generated tests are cross-checked against candidate           sumptions, (3) answers these questions (often independently
code solutions. Using this strategy, we systematically eliminate      to reduce bias) to detect and correct errors or “hallucinations,”
invalid tests, retaining only those that pass an additional           and (4) synthesizes the results into a revised, verified response.
verification. The verification step acts as a ground-truth proxy      Because functionally correct code generation is a known weak-
that eliminates invalid tests that could not be fixed in the          ness of LLMs due to subtle logical flaws and hallucinations,
generation stage and ensures a more rigorous and trustworthy          we apply CoVe to code synthesis: draft → interrogate →
test generation process. Finally, through ablation studies, we        refine. This structured self-correction shifts generation beyond
demonstrate the importance of each component in the pipeline.         pattern matching toward a process analogous to human devel-
The quality of the test suites is evaluated at different stages       oper review, yielding more robust and logically sound code.
to demonstrate the contribution of each step to the overall
effectiveness of ConVerTest.                                          On Self-Consistency
   Our empirical results demonstrate the following. First, SC            SC [25] improves LLM reasoning by sampling multiple
improves test suite quality by increasing the proportion of           diverse reasoning paths for the same prompt and selecting
valid tests by 7–19% and significantly enhancing test ad-             the final answer via majority vote, based on the intuition that
equacy metrics. Second, ConVerTest further outperforms                valid solution paths typically converge on a single correct
SC, improving test validity by 7–39% through the elimination          outcome. This is well-suited to unit test generation because
of invalid test cases during the post-generation verification         tests are convergent: they validate a single deterministic result
stage. Third, ablation studies on ConVerTest, conducted               for given inputs. We therefore generate a test stub, sample
by progressively removing stages, reveal that all components          many completions, and choose the most frequent (most con-
contribute to classification accuracy and test suite quality.         sistent) completion. This consensus-based selection helps filter
These findings confirm the complementary strengths of its             stochastic generation errors, especially in assertion statements,
core components: SC for convergent test generation, CoVe for          and promotes convergence to the most probable assertions.
iterative code refinement, and dual execution agreement for
                                                                      On Dual Execution Agreement
consensus-based verification.
                                                                         Dual Execution Agreement selects the best code solution
The key contributions of this paper are as follows:                   from multiple candidates by using LLM-generated test cases
  (i) We propose consistency-driven components inspired by            as a filter. Each candidate solution is executed against each
      the natural language processing domain and adapt them           generated test; solution–test pairs that pass are “inliers.” Solu-
      to synthesize reliable, high-quality code and test artifacts.   tions passing the same set of tests are grouped into consensus
 (ii) We design and implement a novel two-stage pipeline              sets, which are scored by how many solutions and tests they
      that combines consistency-driven generation with a              contain. The final solution is chosen from the highest-scoring
      consensus-based verification stage, creating a more ef-         consensus set, motivated by the idea that correct solutions pass
      fective pipeline by drawing on hallucination mitigation         more tests and align with more similar solutions. Since CoVe
      strategies applied at both generation and post-generation       and SC improve code and tests but do not guarantee correct-
      stages.                                                         ness, we adapt Dual Execution Agreement as a post-generation
(iii) We conduct a large-scale empirical study on SOTA                quality gate to validate the generated tests themselves. The key
      models and challenging benchmarks, demonstrating that           principle is mutual corroboration: deliberatively produced code
      ConVerTest improves test validity rates by up to 39%            (CoVe) and consensus-derived tests are treated as independent
      while also achieving high test adequacy. In addition,           high-confidence artifacts, and consensus-set behavior is used
      through comprehensive ablation studies, we quantify the         to distinguish valid from invalid tests.
      individual contributions of each component and con-
      firm that each part contributes to the performance of                                   III. A PPROACH
      ConVerTest.                                                        ConVerTest is illustrated in Figure 1. ConVerTest
   We also released the data and source code for our ex-              consists of two stages. The first stage, the Consistency-Driven
periments to facilitate replication and extension by other re-        Generation Stage 1 , is responsible for generating verified
searchers (https://github.com/HamedTaherkhani/ConVerTest).            code candidate solutions as well as consistent test cases.
                                                                      The second stage, the Consensus Verification Stage 4 , is
                       II. BACKGROUND                                 responsible for validating the generated tests using a consen-
  This study uses three methodologies: CoVe, SC, and Dual             sus mechanism between the tests and the solutions. In the
Execution Agreement.                                                  generation stage, ConVerTest employs two simultaneous
                                                                      pipelines: one for test generation 2 and another for code
On Chain-of-Verification                                              generation 3 . The test generation pipeline produces M test
  CoVe [26] is a deliberative, multi-stage reasoning method           cases through SC, while the code generation pipeline produces
that improves factual accuracy and logical consistency in             Z code candidate solutions using CoVe.
                                                               Consistency-Driven Generation and Verification Pipeline
                                                      Consistency-Driven Generation Stage                 1                                                                     Consensus Verification Stage                    4
                                                        Test Generation via Self-consistency                  2
                                                                                                                                                                                  Dual Execution Agreement 5
                                                                             Repeat M times




                                                                                                                                                                                                                       ...
                                                                                                                                                                                      ...
                                                                                                    Test consistency checker
                                                                                                                                                    M tests


                                                                                                                            Most consistent test
                 Test Stub Generator                       Test Completion                                                                                                       Z Verified Solutions                     M tests
                                                                                        …




                                                                                                                                                         Z Verified Solutions
                                           …                                       N complete tests
                                       M Test Stubs
                                                                                                                                                                                                                              M tests
                                                      Code Verification via Chain-of-Verification                 3                                                                              Best Solution

                                                                          1.1
  Problem
  Statement
                                                                             Repeat until all questions are
                                                                                     answered
                                                                                                                                                                                                                   6
                                                                                 Verification Questions                  Verification Answers




                 Generate Solution     Baseline Solution     Plan Verification                        Execute Verifications                                                                              Pass or
                                                                Questions                                                                                                                                 Fail ?
                                                                                                                                                                                            Discard
                                                                                                                      Yes                          Repeat Z times
                                                                                                                                      d
                                                                                                                              Issues detected?


                                                                                                                                  No
                                                                                                                                                                                                      Add to Test Suite

                                                                                                                              Return Baseline
                                                            Verification-Guided Code                   Final                     Solution

                                                                    Generation                  Verified Response



Fig. 1: Overview of ConVerTest. The pipeline operates in two stages: (i) the Consistency-Driven Generation Stage, which
produces verified code candidates via Chain-of-Verification and generates diverse, convergent test cases through SC; and (ii)
the Consensus Verification Stage, which applies a Dual Execution Agreement to cross-validate candidate solutions against
generated tests and filter invalid ones.


   The generated tests and code candidate solutions are then                                              divergent, creative exploration during initial test stub genera-
used in a dual-execution agreement process 5 during the                                                   tion. The process then transitions to a constrained, convergent
consensus verification stage to distinguish valid from invalid                                            reasoning phase in the second stage. This shift creates the
tests. The invalid tests are discarded, while the valid ones are                                          ideal environment for SC, which leverages majority voting to
incorporated into the test suite 6 . Each stage of our pipeline                                           identify a single, optimal completion from diverse samples.
is described in detail in the following subsections.                                                         Stage 1: Generation of Test Stubs: At this stage, the
                                                                                                          language model must generate a set of M diverse test stubs.
A. Consistency-Driven Generation Stage                                                                    A test stub is the skeleton structure of a unit test that defines
                                                                                                          the test scenario without concrete expected output values or
   In Stage 1 , two concurrent pipelines are employed: one                                                specific assertion logic. It includes the test setup function,
responsible for generating consistent tests and the other for                                             the input variable, and the function call. By directing the
generating verified code.                                                                                 model toward this higher-level task, we guide it to produce
   1) Test Generation via SC: 2                                                                           a comprehensive set of test scenarios. This approach reduces
   In order to generate diverse and consistent test cases, we                                             the risk of omission of critical cases that may arise from
propose a two-stage SC approach. Generating a diverse set of                                              computational complexity or hallucination in a single-shot
test scenarios requires exploring a wide range of possibilities,                                          generation.
including edge cases, boundary conditions, and typical usage                                                 The following is an example of a test stub:
patterns. In contrast, completing a given test stub with the 1 import u n i t t e s t
correct assertion for a deterministic function is a simpler 2
                                                                   3 c l a s s TestAnagramCombosMultiplePermutations ( u n i t t e s t
task. Attempting to perform both tasks in a single prompt                     . TestCase ) :
can create a conflict; the LLM might default to simple, safe 4               def setUp ( s e l f ) :
scenarios for which it can easily generate correct assertions, 5                   s e l f . s u b w o r d s = [ ” ab ” , ” cd ” , ” e f ” ]
                                                                   6               s e l f . whole word = ” a b c d e f ”
thereby sacrificing the diversity of the test suite. By decoupling 7
these objectives, the pipeline enables the LLM to prioritize 8               def t e s t m u l t i p l e p e r m u t a t i o n s p o s s i b l e ( s e l f ) :
9             r e s u l t = anagram combos ( s e l f . sub words , s e l f      Formulation of a Verification Plan: Following the genera-
                      . whole word )                                         tion of the baseline solution, the next stage comprises creating
       Stage 2: Completion and Refinement via SC: Following                  a structured verification plan. Rather than performing ad-
    the generation of the stubs, the second stage focuses on                 hoc testing, this step programmatically generates a series of
    completing each stub using SC. For each of the M stubs,                  specific, analytical questions designed to probe the correctness
    the model is prompted N times to generate a complete and                 of the baseline code. The generation of these questions is
    concrete test function including specific expected outputs and           guided by the original problem statement (as the ground truth)
    assertions. This multiple-sampling strategy is the core of our           and the baseline solution. The questions are designed to cover
    SC implementation. It is motivated by the observation that               several critical aspects of the baseline solution:
    while language models may produce inconsistent or erroneous                 • Correctness: Assessing whether the code produces the

    outputs for complex tasks, they tend to converge on a correct                  correct output for a set of valid inputs.
    or most probable answer when sampled repeatedly.                            • Logic and Reasoning: Examining the underlying algo-
       We select the most consistent completion for each stub using                rithm for logical soundness and completeness.
    a consensus-based approach. The N generated completions are                 • Edge Case Handling: Probing the solution’s behavior
    first parsed to extract the underlying test logic and assertions.              with atypical or boundary inputs (e.g., empty lists, null
    By analyzing the abstract syntax tree (AST) of each comple-                    values, zero).
    tion, we identify and group functionally identical test cases,              • Constraint Adherence: Verifying that the solution re-
    abstracting away syntactic variations such as differing variable               spects all explicit and implicit constraints mentioned in
    names or formatting. The test case with the highest frequency                  the problem statement.
    of occurrence among the N samples is then chosen as the final               • Robustness: Evaluating the code’s error-handling capa-
    test for that stub. This process is repeated for all M stubs and               bilities when presented with invalid or unexpected inputs.
    produces a final suite of M complete and consistent test cases.          This stage yields a list of targeted verification questions that
       This two-stage decomposition provides a significant advan-            constitute a formal checklist for subsequent analysis.
    tage: it first ensures broad test coverage by generating distinct           Execution of Verification Questions: Each question from
    test scenarios and then refines each idea to produce a single,           the verification plan is systematically addressed by analyzing
    highly consistent and reliable completion of test scenario by            the baseline solution’s behavior. This analysis yields a corre-
    implementing the expected output and assertion statements.               sponding set of verification answers. These answers provide a
       2) Code Verification via CoVe: 3                                      detailed diagnosis of the code, explaining not only if it passes a
       To enhance the reliability and correctness of generated code,         particular check but also why, by reasoning about the expected
    we employ a multi-stage, iterative refinement process termed             versus actual behavior.
    CoVe. This methodology implements a systematic verification                 This stage results in a critical judgment of the solution’s
    and correction loop. The core principle of CoVe is to model              overall correctness and logic. Based on the collective evidence
    the rigorous process of human code review, where a solution is           from the verification answers, a conclusion is made as to
    critically inspected against a set of targeted criteria, and feed-       whether the code contains significant flaws that render it
    back from this analysis directly informs subsequent revisions.           incorrect or incomplete.
    The objective is to identify and rectify logical flaws, missed              Iterative Refinement via Verification-Guided Generation:
    edge cases, and deviations from the problem description.                 The outcome of the analysis stage dictates the next step in the
       A code solution can have multiple valid implementation                pipeline. The process follows a conditional, iterative loop:
    pathways (e.g., an iterative vs. a recursive solution, or solutions        1) If the analysis concludes that no issues are present,
    using different library functions). A simple majority vote on                  the verification loop terminates. The baseline solution is
    the final code text would fail, as syntactically different but                 considered to have successfully passed the verification
    functionally identical solutions would not form a consen-                      process and is returned as the final, validated output.
    sus. CoVe is better suited for this task because it focuses                2) If the analysis identifies one or more issues, the pipeline
    on iteratively refining a single reasoning path through self-                  advances to a corrective step called verification-guided
    interrogation and correction, mirroring a human code review                    generation. In this step, the LLM is prompted to produce
    process [28]. This process improves the logical soundness and                  a revised solution. The prompt is supplemented with
    correctness of a solution regardless of its specific implementa-               the full context of the verification process: the original
    tion details. The CoVe process is deconstructed into a sequence                prompt, the flawed baseline solution, the set of verifica-
    as illustrated in the following.                                               tion questions, and the detailed verification answers that
       Baseline Solution Generation: The process starts with the                   reveal the errors.
    generation of an initial candidate solution, hereafter referred to          This contextual information directs the model to produce
    as the baseline solution. This solution is produced by an LLM            a corrected solution that specifically addresses the identified
    in direct response to a given problem statement or prompt.               shortcomings.
    This initial code serves as the starting point for the verification         The process is repeated Z times, yielding Z candidate
    pipeline and is treated as a draft that requires verification rather     solutions that are then used in the subsequent consensus-based
    than a final response.                                                   verification step.
B. Consensus Verification Stage                                     B. Datasets
   The Consensus Verification Stage 4 is the final phase of           We use two datasets in our evaluations: BigCodeBench-
the pipeline and is responsible for selecting a single most reli- Hard [9] and Less Basic Python Problems (LBPP) [10].
able code solution from a set of previously verified candidates.      BigCodeBench is a large-scale benchmark for evaluating
It follows the principle of Dual Execution Agreement, in which code generation LLMs through realistic programming chal-
multiple candidate solutions and multiple generated test cases lenges that require diverse function calls from 139 libraries
mutually validate one another to establish a strong consensus across 7 domains and the ability to follow complex natural
on correct program behavior. This stage takes two inputs: (i) language instructions. BigCodeBench-Hard is an extended
a set of Z candidate solutions that passed the initial checks in version with more difficult tasks involving higher complexity.
the Code Verification stage, and (ii) a set of M generated test       LBPP is a newly proposed benchmark for evaluating code
cases produced by the Test Generation stage. Each candidate generation in LLMs. It was created to address contamination
solution is executed on every generated test case, producing an issues in widely used benchmarks like HumanEval and MBPP.
execution matrix of pass/fail outcomes for all (solution, test) LBPP contains 161 manually crafted Python problems that are
pairs.                                                            deliberately more difficult and designed to avoid overlap with
   Using this matrix, the method forms agreement sets, where existing datasets.
each agreement set is a group of solutions that pass the exact
same subset of test cases. For example, if Solution A and
Solution B both pass Test 1 and Test 3 but fail all other tests, C. Evaluation Metrics
they are assigned to the same agreement set. This clustering          To assess the quality of test suites, we use two categories of
identifies groups of solutions that exhibit identical behavior metrics: (i) Validity Rate (VR) for measuring the proportion
across the provided tests.                                        of valid test cases, and (ii) test adequacy metrics including
   Each agreement set is assigned a consensus score to estimate Mutation Score (MS) and Line Coverage (LC), both widely
reliability:                                                      adopted in evaluating LLM-generated tests [31].
                                     √
score = (number of tests passed)× number of solutions in set. 1) Validity Rate (VR): A test case is considered valid if
                                                                  it executes successfully against the ground-truth implemen-
The first factor rewards sets whose solutions pass more tests, tation without producing any errors. Given functions F =
reflecting robustness and comprehensiveness. The second fac- {f1 , . . . , fn } and corresponding test sets Ti = {ti1 , . . . , tim },
                                                                                                                                   i
tor captures consensus strength: more solutions agreeing on a binary function V (tij ) indicates whether test case tij is valid
the same behavior provides a stronger signal of correctness. for fi . The overall validity rate is defined as:
The square root introduces diminishing returns so that very                                  Pn Pmi
large groups of simple or mediocre solutions do not domi-                                       i=1         V (tij )
nate smaller but higher-quality clusters. Agreement sets are                          VR =        Pnj=1              .
                                                                                                      i=1 mi
ranked in descending order by this consensus score, and a
representative solution from the top-ranked set is selected as        2) Mutation Score (MS): Using the Mutmut tool, mutants
the final solution. This ensures the selected output is both are generated per function. If |Mi | is the number of mutants
extensively validated by tests and supported by agreement for fi and Ki the killed mutants, the mutation score is:
among independently generated solutions. In addition to se-                                        Pn
lecting the best solution, this stage evaluates the generated                                             Ki
                                                                                          MS = Pni=1           .
test cases themselves. The chosen best solution is treated as                                        i=1 |Mi |
a reliable reference: each generated test is labeled valid if it
passes on this solution and invalid if it fails. These labels         3) Line Coverage (LC): For each function fi , let L(fi )
enable computation of precision, recall, and F1 scores for the    denote   its lines of code and L(tij ) the lines covered by test
generated tests.                                                  tij . The  union of covered lines is:

                     IV. E XPERIMENT D ESIGN                                                         mi
                                                                                                     [
A. Models                                                                                 C(fi ) =         L(tij ),
                                                                                                     j=1
   We employ three models in our experiments, selected
to represent different providers (Alibaba, Google, and Ope-         with coverage ratio
nAI), parameter scales, and abilities. Specifically, we in-
clude (i) a fine-tuned coding-oriented language model, (ii)                                                 |C(fi )|
                                                                                        Coverage(fi ) =              .
a reasoning-focused model, and (iii) a general-purpose text                                                 |L(fi )|
generation model. The models are qwen3-coder-480b-a35b-
                                                                    The average coverage is then:
instruct [29], GPT-5-Mini-2025-08-071 , and Gemma-3.3-
12b-it [30].                                                                                     n
                                                                                              1X
  1 https://openai.com/index/introducing-gpt-5/
                                                                                       LC =         Coverage(fi ).
                                                                                              n i=1
TABLE I: Holistic Test Generation (HTG), Two-Stage Test             single step rather than generating the stub and the completion
Generation (TSTG), and Self-Consistency Test Generation             separately. In TSTG, we follow the two-stage procedure but,
(SCTG) Comparison. All values are in percentages (%)                we sample only once (N =1). This corresponds to a two-stage
 Dataset Approach LLM        VR       LC       MS       #Tests      chain-of-thought approach.
        HTG                  62       81       57       1808           The results in Table I show that TSTG consistently produces
        TSTG      CodeQwen3 70 ↑8     85 ↑4    63 ↑6    2187        more valid tests and higher-quality test cases in terms of line
        SCTG                 76 ↑14   88 ↑7    67 ↑10   2187
 BCB                                                                coverage (LC) and mutation score (MS) relative to HTG by
        HTG                  35       54       64       1501
        TSTG      Gemma3.3 45↑10      78↑24    71↑7     2097        improving validity by 4–10%, LC by 4–24%, and MS by 6–
        SCTG                 51↑16    82↑28    74↑10    2097
                                                                    16%. Adding SC to the process yields further gains: relative to
        HTG                  61       72       50       3090
        TSTG      Gpt-5-Mini 68 ↑7    86 ↑14   62 ↑12   3109        HTG, SC improves validity by 7–19%, and relative to TSTG,
        SCTG                 72 ↑11   89 ↑17   63 ↑13   3109
                                                                    by 3–13%. In addition, SC consistently increases the validity
        HTG                  54       85       70       2115
        TSTG      CodeQwen3 60 ↑6     91 ↑6    81 ↑11   2788        of synthesized tests and enhances their quality, improving LC
        SCTG                 73 ↑19   94 ↑9    85 ↑15   2788        by 7–28% and MS by 10–18%.
 LBPP
        HTG                  38       60       44       1595           When comparing the performance of the different large
        TSTG      Gemma3.3 45 ↑7      74 ↑14   51 ↑7    2938
        SCTG                 53 ↑15   76 ↑16   57 ↑13   2938        language models, we observe distinct capability levels as
        HTG                  70       71       49       2818        shown in Table I. CodeQwen3 shows particularly strong results
        TSTG      Gpt-5-Mini 74 ↑4    90 ↑19   65 ↑16   3019
        SCTG                 77 ↑7    91 ↑20   67 ↑18   3019        on the BCB dataset, achieving the highest scores in all metrics
                                                                    with the SC approach (VR 76, LC 88, MS 67). Gpt-5-
                                                                    Mini demonstrates competitive performance, especially on the
   4) Precision and Recall: In this paper, precision measures       LBPP dataset where it achieves a high validity rate (VR 77).
the purity of the final test suite after ConVerTest has             Gpt-5-Mini benefits the most from SC, showing the largest
filtered it. It answers the question: “Of all the test cases that   absolute gains in line coverage on both datasets when moving
ConVerTest decided to keep, what percentage are actually            from the Holistic method to SC.
valid?”. A high precision score means that the final test suite        Gemma3.3 consistently scores lower than the other two
is clean and contains very few incorrect or invalid tests.          models in both datasets. The performance gap is most evident
Recall measures how well ConVerTest avoids throwing                 on the more complex LBPP dataset. Despite its lower baseline
away valid tests. It answers the question: “Of all the test         performance, it is important to note that Gemma3.3 still shows
cases that were actually valid to begin with, what percentage       significant improvement when using the TSTG and SCTG
did ConVerTest successfully identify and keep?”. A high             techniques. For example, its validity rate on LBPP improves
recall score means that the filtering process is not overly         from 38 to 53 with SCTG. This finding suggests that, while the
aggressive and preserves most of the useful, valid tests that       choice of model is crucial for overall performance, employing
were generated.                                                     advanced generation strategies provides substantial benefits for
                                                                    all models, regardless of their capability.
D. Research Questions
  • RQ1: Effectiveness of SC. To what extent does the two-             Answer to RQ1: SCTG is a highly effective technique
    stage Self-Consistency improve the validity and adequacy           for synthesizing higher-quality tests, significantly out-
    of synthesized tests compared to holistic and two-stage            performing simpler baselines like HTG and TSTG. SC
    generation methods?                                                consistently improves test validity rate by up to 19%,
  • RQ2: Reliability of Consensus Verification. How accu-
                                                                       line coverage by up to 28%, and mutation score by up
    rately can the consensus verification stage classify test          to 18%.
    cases as valid or invalid, and what is its impact on
    preserving high-quality tests within the final suite?
  • RQ3: Component Contribution. What are the indi-                 B. How accurately can the consensus verification stage clas-
    vidual and collective impacts of CoVe, SC, and Two-             sify test cases as valid or invalid, and what is its impact on
    Stage Generation (TSG) on the overall performance of            preserving high-quality tests within the final suite?
    ConVerTest?                                                        To evaluate the effectiveness of the consensus verification
                                                                    stage in distinguishing between valid and invalid test cases, we
                         V. R ESULTS
                                                                    use precision, recall, and F1 scores. Additionally, we assess
A. To what extent does the two-stage Self-Consistency im-           the extent to which ConVerTest retains high-quality tests
prove the validity and adequacy of synthesized tests compared       by comparing the mutation score (MS) and line coverage (LC)
to holistic and two-stage generation methods?                       before and after the verification phase.
   In this RQ, we examine the strength of SC Test Generation        Precision as Validity Rate. The precision metric is equivalent
(SCTG). To this end, we compare SCTG against two simpler            to the Validity Rate (VR) of the resulting test suite. That
baselines: Holistic Test Generation (HTG) and Two-Stage Test        is, precision measures the proportion of tests that are valid
Generation (TSTG). In HTG, the entire test, including the           among those retained after filtering. As shown in Table II,
test stub and the test output and assertions, are produced in a     ConVerTest substantially improves VR across all models
TABLE II: Effectiveness of ConVerTest in verifying test cases in terms of precision, recall, and F1 scores and retaining
valuable tests in terms of LC and MS scores. Colored arrows show the percentage change from the Self-Consistency to
ConVerTest. All values are in percentages (%). A dash (-) indicates that the cell has no value.
                             Dataset Approach              LLM           recall precision (VR) F1 LC      MS
                                     Self-Consistency Tests              –       72            –    89    63
                                                            Gpt-5-Mini
                                     ConVerTest                          95      86 ↑16        90   87 ↓2 61 ↓2
                             BCB     Self-Consistency Tests           –          76            –    88    67
                                                            CodeQwen3
                                     ConVerTest                       91         91 ↑15        91   87 ↓1 67 –0
                                     Self-Consistency Tests              –       51            –    82    74
                                                            Gemma3.3
                                     ConVerTest                          90      90 ↑39        90   81 ↓1 72 ↓2
                                     Self-Consistency Tests           –          73            –    94    85
                                                            CodeQwen3
                                     ConVerTest                       93         88 ↑15        90   93 ↓1 85 –0
                             LBPP    Self-Consistency Tests              –       77            –    91    67
                                                            Gpt-5-Mini
                                     ConVerTest                          96      84 ↑7         89   91 –0 65 ↓2
                                     Self-Consistency Tests              –       53            –    76    57
                                                            Gemma3.3
                                     ConVerTest                          89      84 ↑39        86   74 ↓2 55 ↓2



and datasets. For instance, on BigCodeBench, ConVerTest                  logic. By filtering these out, ConVerTest ensures that the
boosts the VR from 72 to 86 for GPT-5-Mini and from 76 to 91             remaining LC and MS are derived solely from valid assertions.
for CodeQwen3, representing absolute gains of 14% and 15%                As shown in our results, the significant gains in Validity Rate
respectively. On the LBPP dataset, ConVerTest improves                   (up to 39%) far outweigh the negligible, expected reductions
the VR from 73 to 88 for CodeQwen3, and from 53 to 84 for                in coverage (1–2%).
Gemma3.3.
Precision, Recall, and F1 Scores. As shown in Table II,                       Answer to RQ2: The consensus verification stage
ConVerTest achieves consistently high precision and recall.                   improves precision by up to 39%. At the same time, it
For example, on BigCodeBench, ConVerTest yields a pre-                        maintains high recall to avoid discarding valid ones,
cision of 91 and recall of 91 for CodeQwen3, resulting in                     resulting in high F1 scores across all models. This
an F1 score of 91. Similarly, for GPT-5-Mini, ConVerTest                      comes at the cost of a minimal, expected drop in
attains a precision of 86 and recall of 95, confirming its ability            mutation score and line coverage, demonstrating that
to accurately identify valid test cases. On the LBPP dataset,                 ConVerTest successfully retains the vast majority of
ConVerTest maintains high verification accuracy, achieving                    valuable tests while significantly enhancing the validity
an F1 score of 90 for CodeQwen3 and 89 for GPT-5-Mini.                        of the test suite.
Notably, the Gemma3.3 model, despite having lower baseline
test quality, also benefits significantly from ConVerTest,
achieving an F1 score of 86 with a large precision gain                  C. What are the individual and collective impacts of CoVe, SC,
(+39%).                                                                  and Two-Stage Generation (TSG) on the overall performance
Mutation Score and Line Coverage. While ConVerTest’s                     of ConVerTest?
verification stage is designed to remove invalid tests, it may              To investigate the contribution of each component in
also inadvertently discard a small number of valid tests. As             ConVerTest, we performed an ablation study in which we
a result, a slight drop in mutation score and line coverage is           progressively removed or altered the test and code generation
expected. However, the gain in VR outweighs this drop. This is           components, while observing their effects on test suite metrics
evident in the results: for CodeQwen3 on BigCodeBench, the               and on the classification ability of ConVerTest (recall,
mutation score remains unchanged (67), while line coverage               precision, and F1 scores). Table III reports the comparative
decreases slightly from 88 to 87. For GPT-5-Mini, mutation               results across different configurations on both BigCodeBench
score drops from 63 to 61 and line coverage from 89 to 87.               (BCB) and LBPP datasets using multiple LLMs.
On the LBPP dataset, we observe similar trends: CodeQwen3                   It is important to note that the precision metric is equivalent
retains its mutation score (85), with only a 1% drop in LC.              to the Validity Rate (VR) of the resulting test suite. The
For Gemma3.3, although the absolute scores are lower, the                precision also represents the precision of the dual-agreement
verification stage results in only a 2% decrease in both metrics.        classification ability in ConVerTest. Thus, they are essen-
Coverage-Validity Trade-off. While Table II indicates a                  tially the same in this table.
marginal decrease in LC and MS after verification, this repre-           ConVerTest without CoVe. In the first ablation study,
sents a shift from a high-quantity, low-reliability test suite to a      the only change relative to the previous configuration is the
high-precision, high-reliability one. The initial test suites often      removal of CoVe. Instead, we use vanilla code generation. In
contain invalid tests that artificially inflate coverage metrics         vanilla code generation, we generate the baseline solution, as
by executing code lines without actually verifying correct               we did with CoVe, but treat it as the final solution without
TABLE III: Ablation study of ConVerTest, demonstrating the contribution of each component. The configurations show
the impact of progressively removing CoVe for code generation and SC and Two-Stage Generation (TSG) for test generation.
Performance is measured across classification metrics (Recall, Precision/VR, F1-score) and test adequacy (Line Coverage and
Mutation Score). All values are in percentages (%)
Dataset Approach                       LLM        Recall            Precision (VR)   F1             LC              MS
      ConVerTest                                91                  91               91             87              67
      ConVerTest w/o CoVe            CodeQwen3 85 ↓6                91 –0            88 ↓3          82 ↓5           61 ↓6
      ConVerTest w/o CoVe & SC                  85 –0               88 ↓3            86 ↓2          81 ↓1           61 –0
      ConVerTest w/o CoVe & SC & TSG            85 –0               86 ↓2            85 ↓1          76 ↓5           54 ↓7
      ConVerTest                                90                  90               90             81              72
      ConVerTest w/o CoVe            Gemma3.3 88 ↓2                 90 –0            89 ↓1          77 ↓4           68 ↓4
  BCB ConVerTest w/o CoVe & SC                  88 –0               88 ↓2            88 ↓1          77 –0           68 –0
      ConVerTest w/o CoVe & SC & TSG            88 –0               85 ↓3            86 ↓2          51 ↓26          60 ↓8
      ConVerTest                                95                  86               90             87              61
      ConVerTest w/o CoVe            Gpt-5-Mini 93 ↓2               83 ↓3            88 ↓2          84 ↓3           58 ↓3
      ConVerTest w/o CoVe & SC                  93 –0               80 ↓3            86 ↓2          84 –0           58 –0
      ConVerTest w/o CoVe & SC & TSG            93 –0               76 ↓4            84 ↓2          68 ↓16          47 ↓11
      ConVerTest                                93                  88               90             93              85
      ConVerTest w/o CoVe            CodeQwen3 81 ↓12               89 ↑1            85 ↓5          86 ↓7           79 ↓6
      ConVerTest w/o CoVe & SC                  77 ↓4               86 ↓3            81 ↓4          82 ↓4           75 ↓4
      ConVerTest w/o CoVe & SC & TSG            81 ↑4               89 ↑3            85 ↑4          78 ↓4           69 ↓6
      ConVerTest                                89                  84               86             74              55
      ConVerTest w/o CoVe            Gemma3.3 85 ↓4                 84 –0            84 ↓2          71 ↓3           49 ↓6
 LBPP ConVerTest w/o CoVe & SC                  83 ↓2               84 –0            83 ↓1          69 ↓2           45 ↓4
      ConVerTest w/o CoVe & SC & TSG            84 ↑1               76 ↓8            80 ↓3          53 ↓16          38 ↓7
      ConVerTest                                96                  84               89             91              65
      ConVerTest w/o CoVe            Gpt-5-Mini 93 ↓3               84 –0            88 ↓1          89 ↓2           62 ↓3
      ConVerTest w/o CoVe & SC                  92 ↓1               82 ↓2            87 ↓1          87 ↓2           60 ↓2
      ConVerTest w/o CoVe & SC & TSG            92 –0               80 ↓2            86 ↓1          65 ↓22          42 ↓18



applying planning or verification. This leads to a significant       LC falls from 82 to 81. On LBPP, CodeQwen3 shows declines
drop in the recall of dual agreement verification because the        in both recall and precision, as well as decreases in MS and
candidate solutions generated by vanilla code generation are         LC (from 86 to 82 and from 79 to 75, respectively). Gemma3.3
much less accurate than those produced with CoVe. As a result,       exhibits a slightly different pattern: precision remains the
ConVerTest incorrectly classifies more valid tests as invalid        same, but recall drops from 85 to 83, and LC and MS decrease
and removes them from the test suite.                                from 71 to 69 and from 49 to 45, respectively. These results
   Discarding more valid tests sharply decreases both the            demonstrate that replacing SC with Two-Stage test generation
mutation score (MS) and line coverage (LC) of the resulting          (TSG) substantially degrades adequacy metrics, reduces the
test suites. Specifically, LC decreases by 2–7% and MS by            validity rate of the test suites, and weakens ConVerTest’s
3–6%. Thus, replacing CoVe with vanilla code generation              predictive ability compared to configurations that incorporate
degrades the quality of the generated code and reduces the           SC in the test generation process.
recall of ConVerTest’s classification ability. This decrease
is consistent across all dataset LLM combinations.
ConVerTest without CoVe and SC. In the second ablation               ConVerTest without CoVe and SC and TSG. The final
study, we remove only the SC test generation component from          ablation study evaluates ConVerTest without CoVe, SC, and
the previous configuration. In this setting, CoVe is not used for    TSG. In this setting, we rely solely on holistic test generation
test generation, and SC is excluded as well. However, we retain      and vanilla code generation, meaning that no verification or
the Two-Stage test generation (TSG) and replace SC with CoT          consistency techniques are applied during the code or test
prompting for test generation. In 5 out of 6 cases, this reduces     generation process.
both the precision of the approach and the validity rate of the
test suites compared to the previous configuration. In addition,
both line coverage (LC) and mutation score (MS) decrease in             Removing CoVe and SC results in a non-trivial decrease
most cases. This is expected because, as shown in Table I,           in test adequacy metrics, specifically line coverage (LC) and
SC test generation yields higher-quality and more adequate           mutation score (MS). LC decreases by 4–26%, while MS
tests than TSG. The decline in the precision of ConVerTest           decreases by 6–18%. For example, on LBPP–Gpt-5-Mini, LC
under this configuration shows that test case quality directly       drops by 22 (absolute) and MS by 18 (absolute). This is
affects ConVerTest’s ability to distinguish invalid tests, and       expected, as the quality of holistic test generation is consid-
improving test quality enhances ConVerTest’s effectiveness           erably lower than that of TSG or SC. The reduced quality
in verifying test cases.                                             of holistic test generation also degrades the classification
   This configuration consistently reduces both validity and         ability of ConVerTest. In 5 out of 6 cases, the precision
adequacy compared to the previous setup. For example, on             of ConVerTest declines. For instance, on Gemma3-LBPP,
BCB with CodeQwen3, precision drops from 91 to 88, while             LC decreases by 16, MS by 7, and precision by 8.
    Answer to RQ3: Each component of ConVerTest                           could be traced back to ambiguities or incompleteness in the
    has a significant impact on its overall performance.                  function docstring itself. This suggests that the quality of the
    The ablation study reveals that CoVe is critical for                  dataset is a critical factor and that LLMs are susceptible to
    producing reliable code solutions for the verification                generating incorrect tests when the function docstring is not
    stage, and its removal substantially degrades recall                  perfectly clear.
    and test suite adequacy. SC plays a crucial role in                      The remaining categories, violating input constraints (7%)
    enhancing the initial quality and validity of generated               and output-format inconsistency (7%), represent more direct
    tests, as its absence leads to lower precision and                    logical contradictions but are less frequent.
                                                                             These findings strongly support the need for a robust
    reduced adequacy scores.
                                                                          verification mechanism like ConVerTest. The prevalence of
                                                                          semantic errors (28% + 15% + 12%) underscores why simple
                         VI. D ISCUSSION                                  syntactic checks are insufficient. The dual execution agreement
   While our results demonstrate that ConVerTest can ef-                  at the core of ConVerTest is well-suited to detect these
fectively filter invalid test cases, it is crucial to understand          discrepancies. When a test expects a behavior not specified
the underlying reasons why LLMs generate such tests in the                in the docstring, it will likely fail against a code solution
first place. To this end, we conducted a qualitative analysis to          generated via the rigorous CoVe process, which is designed
categorize the types of errors that lead to invalid test cases.           to adhere closely to that same docstring. By establishing a
   We randomly sampled 100 invalid tests generated from both              consensus between independently generated code and tests,
the BigCodeBench and LBPP datasets. Two graduate students                 ConVerTest effectively creates a proxy for ground truth that
with experience in software engineering independently catego-             can identify and discard tests suffering from these common
rized the root cause of failure for each test. A third graduate           forms of LLM hallucination and misinterpretation.
student then reviewed the classifications and resolved any
conflicts, ensuring a reliable categorization. The percentage                                 VII. R ELATED W ORK
of agreement between the first two annotators is 79%. The                 A. Test case generation
results of this analysis are summarized in Table IV.                         In recent years, LLMs have opened new possibilities for
                                                                          automatically generating unit tests, making them easier for
TABLE IV: Categorization of Root Causes for Invalid LLM-                  developers to create while also reducing development time.
Generated Test Cases                                                      By learning from large collections of developer-written tests,
Category of Invalidity                                    Frequency (%)   these models can create test cases that go beyond what tradi-
Expecting behavior not requested in the spec                   28
                                                                          tional techniques offer. Researchers have tried different ways
Wrong API / function call                                      19         to improve the quality of these tests, including pretraining
Misunderstanding the Function Logic from NL Description        15         and fine-tuning on code-related tasks [32]–[35], reinforcement
Misread edge-case logic                                        12
Ambiguities or Incompleteness in the Function Docstring        12
                                                                          learning [36], better prompt design [2], [37], [38], the use of
Violating stated input constraints / preconditions              7         documentation [4], [5], and even integration with search-based
Output-format inconsistency                                     7         methods [39].
                                                                             At the same time, challenges remain. Studies show that
   Our analysis reveals several key insights. The most preva-             LLM-generated tests often struggle with correctness [40]–
lent issue, accounting for 28% of invalid tests, is the LLM               [42] and may provide limited coverage on some benchmarks.
generating tests that expect behavior not requested in the                This has led to direct comparisons with well-established tools
specification. This form of hallucination, where the model                such as EvoSuite [3], [43] and Pynguin [43], [44], which
makes assumptions or invents requirements, is a significant               underscores the need for continued refinement.
challenge. For example, a model might assert that a function                 Several recent projects demonstrate how the field is moving
should sort a list in-place when the docstring only specifies             forward. Liu et al. [45] introduced AID, which combines
that a sorted list should be returned.                                    LLMs with differential testing to reveal faults in programs
   The second most common failure (19%) is the use of a                   that already pass conventional test suites. Alagarsamy et
wrong API or function call. This is particularly common                   al. [33] developed A3Test, which applies domain adaptation to
in complex benchmarks like BigCodeBench, where models                     produce assertion-informed test cases with consistent naming.
must correctly utilize functions from various libraries. These            ChatTester [1] focuses on refining the tests produced by
errors range from calling a non-existent function to providing            ChatGPT through iterative feedback loops, improving their
incorrect arguments, indicating a weakness in the model’s                 precision. In another study, Ouédraogo et al. [46] compared
knowledge of specific library APIs.                                       multiple LLMs with EvoSuite, examining their strengths in
   A significant portion of the errors stems from a deeper                coverage, readability, and correctness.
semantic misunderstanding. Failures to correctly interpret                   Before these advances, traditional methods relied mainly
natural language logic (15%) and edge-case logic (12%)                    on search-based [47], [48], constraint-based [49], or random-
show that LLMs can struggle with complex requirements.                    based [50] strategies to maximize code coverage. Although
Furthermore, we found that in 12% of the cases, the invalidity            effective for this narrow purpose, they often resulted in test
cases that were difficult to maintain. The move toward LLM-        diverse, these datasets may not fully represent all programming
driven approaches marks an important step forward, even if         paradigms, strongly-typed languages, or large-scale system
more work is needed to address current limitations.                testing. Thus, generalizability to other languages or real-
                                                                   world projects remains for future work. We deliberately se-
B. Inconsistency in LLMs                                           lected benchmarks that are widely used, challenging, and
   Recent research has increasingly framed inconsistency as        designed to avoid contamination (LBPP) or trivial solutions
a fundamental limitation of LLMs, with multiple strategies         (BigCodeBench-Hard). This choice increases external validity
proposed to improve robustness and reasoning reliability.          compared to smaller or potentially leaked datasets.
Dhuliawala et al. [26] introduce CoVe, where models explicitly        Model and Data Bias: The performance of ConVerTest
plan and answer fact-checking questions to reduce hallucina-       is constrained by the underlying LLMs, which vary in coding
tions. Similarly, He et al. [51] extend this idea in retrieval-    capabilities and may contain biases from their training data.
augmented generation, proposing CoV-RAG, which integrates          For instance, weaker models (e.g., Gemma3.3) show lower
verification to refine both external retrieval and internal gen-   baseline performance. Moreover, although LBPP was designed
eration. Complementing verification-based methods, Zhao et         to mitigate training-data leakage, residual contamination can-
al. [52] propose Consistency Alignment as a two-stage training     not be entirely ruled out. To mitigate this, we explicitly
framework: instruction augmentation followed by consistency-       tested with three heterogeneous models of different strengths
based preference alignment, aiming to improve robustness to        (a code-specialized LLM, a reasoning-focused model, and a
paraphrased prompts.                                               general-purpose model). The consistent improvements across
   Another prominent direction builds on SC [25], originally       all models demonstrate that ConVerTest is not narrowly
formulated as sampling multiple reasoning chains and aggre-        tuned to one configuration or LLM, and that its benefits
gating by majority voting. Chen et al. [53] propose Self-Para-     generalize despite underlying model biases.
Consistency, leveraging paraphrased inputs to generate diverse        Conclusion Validity and Practical Applicability:
but high-probability reasoning paths, thus reducing the heavy      ConVerTest has not yet been evaluated in continuous
sampling cost of standard SC. Huang et al. [54] extend this        integration pipelines, test-driven development workflows,
idea with Mirror-Consistency, which incorporates minority          or at industrial scale. Its multi-stage pipeline introduces
and inconsistent answers as valuable signals to calibrate con-     additional computational cost due to repeated sampling,
fidence and reduce overconfidence. Wang et al. [55] propose        verification, and dual execution, which may limit deployment
Soft Self-Consistency (Soft-SC), replacing hard majority voting    in resource-constrained environments. We measured adequacy
with probability-weighted scoring, enabling more efficient         preservation (mutation score and line coverage) and showed
selection in tasks with diverse valid outputs. Further, Prasad     that ConVerTest discards only a small fraction of valid
et al. [56] embed SC into training through Self-Consistency        tests while substantially improving overall validity. This
Preference Optimization (SCPO), aligning models to prefer          trade-off suggests that, despite higher computational cost, the
consistent responses even without gold supervision. These ap-      resulting test suites are more trustworthy and therefore more
proaches converge on the principle that internal disagreement      cost-effective in the long run.
among model samples, rather than being discarded, can be
leveraged as a structured signal for reliability.                            IX. C ONCLUSION AND F UTURE W ORK
                                                                      In this paper, we introduced ConVerTest, a novel ap-
     VIII. L IMITATIONS AND T HREATS TO VALIDITY                   proach that addresses the challenge of generating valid and
   While ConVerTest shows promising results in generating          reliable test cases with LLMs without relying on ground-
valid and reliable test cases, several limitations must be         truth implementations. By combining three complemen-
considered. We also highlight how our design choices mitigate      tary strategies—Self-Consistency for convergent test genera-
or alleviate these threats.                                        tion, Chain-of-Verification for iterative code refinement, and
   Internal Validity: Our approach relies on specific sampling     Dual Execution Agreement for consensus-based verification—
strategies (e.g., number of test completions in SC and verifica-   ConVerTest systematically mitigates hallucinations and en-
tion rounds in CoVe). Different hyperparameter choices may         hances the quality of synthesized test suites. Our empirical
lead to different outcomes. Moreover, our consensus-based          evaluation on B IG C ODE B ENCH -H ARD and LBPP demon-
verification assumes that convergence across independently         strates that ConVerTest achieves superior performance
generated artifacts correlates with correctness, which may not     compared to holistic and two-stage baselines, consistently
hold if multiple incorrect yet internally consistent outputs are   improving validity rates, line coverage, and mutation scores.
produced. To mitigate this, we conducted extensive ablation        Furthermore, ablation studies confirmed the critical contri-
studies to show that each component (SC, CoVe, and Dual            bution of each pipeline component, validating the necessity
Execution Agreement) individually contributes to the overall       of integrating consistency-driven generation with consensus
results, and their combination consistently achieves the best      verification.
results.                                                              While ConVerTest advances the reliability of automated
   External Validity: Our experiments focus on Python pro-         test generation, several opportunities remain for future explo-
gramming tasks from BigCodeBench and LBPP. Although                ration. First, extending our approach to other programming
languages and multi-modal tasks, such as tests derived from                      [13] Z. Yuan, M. Liu, S. Ding, K. Wang, Y. Chen, X. Peng, and Y. Lou,
API specifications or natural language documentation, would                           “Evaluating and improving chatgpt for unit test generation,” Proceedings
                                                                                      of the ACM on Software Engineering, vol. 1, no. FSE, pp. 1703–1726,
broaden its applicability. Second, incorporating semantic and                         2024.
dynamic analysis techniques into the verification stage could                    [14] L. Yang, C. Yang, S. Gao, W. Wang, B. Wang, Q. Zhu, X. Chu, J. Zhou,
further reduce false positives and capture deeper logical flaws                       G. Liang, Q. Wang et al., “An empirical study of unit test generation
                                                                                      with large language models,” arXiv preprint arXiv:2406.18181, 2024.
that execution-based verification may miss. Third, adapting                      [15] V. Guilherme and A. Vincenzi, “An initial investigation of chatgpt
ConVerTest for interactive and incremental development                                unit test generation capability,” in Proceedings of the 8th Brazilian
workflows, such as test-driven development or continuous                              Symposium on Systematic and Automated Software Testing, ser. SAST
                                                                                      ’23. New York, NY, USA: Association for Computing Machinery, 2023,
integration pipelines, would enable tighter integration into                          p. 15–24. [Online]. Available: https://doi.org/10.1145/3624032.3624035
real-world software engineering practices. Finally, future work                  [16] V. Li and N. Doiron, “Prompting code interpreter to write
should explore hybrid strategies that combine ConVerTest                              better unit tests on quixbugs functions,” 2023. [Online]. Available:
                                                                                      https://arxiv.org/abs/2310.00483
with search-based or formal verification approaches.                             [17] K. Li and Y. Yuan, “Large language models as test case generators:
                                                                                      Performance evaluation and enhancement,” 2024. [Online]. Available:
                       X. DATA AVAILABILITY                                           https://arxiv.org/abs/2404.13340
                                                                                 [18] Z. Sollenberger, J. Patel, C. Munley, A. Jarmusch, and S. Chan-
   We released the data and source code for our experiments                           drasekaran, “Llm4vv: Exploring llm-as-a-judge for validation and verifi-
to facilitate replication and extension by other researchers                          cation testsuites,” in SC24-W: Workshops of the International Conference
(https://github.com/HamedTaherkhani/ConVerTest).                                      for High Performance Computing, Networking, Storage and Analysis,
                                                                                      2024, pp. 1885–1893.
                              R EFERENCES                                        [19] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Re-
                                                                                      flexion: Language agents with verbal reinforcement learning,” Advances
 [1] Z. Yuan, M. Liu, S. Ding, K. Wang, Y. Chen, X. Peng, and Y. Lou,                 in Neural Information Processing Systems, vol. 36, 2024.
     “Evaluating and improving chatgpt for unit test generation,” Proc.          [20] A. Zhou, K. Yan, M. Shlapentokh-Rothman, H. Wang, and Y.-X. Wang,
     ACM Softw. Eng., vol. 1, no. FSE, Jul. 2024. [Online]. Available:                “Language agent tree search unifies reasoning acting and planning in
     https://doi.org/10.1145/3660783                                                  language models,” arXiv preprint arXiv:2310.04406, 2023.
 [2] Y. Chen, Z. Hu, C. Zhi, J. Han, S. Deng, and J. Yin, “Chatunitest: A        [21] D. Huang, Q. Bu, J. M. Zhang, M. Luck, and H. Cui, “Agentcoder:
     framework for llm-based test generation,” in Companion Proceedings of            Multi-agent-based code generation with iterative testing and optimisa-
     the 32nd ACM International Conference on the Foundations of Software             tion,” arXiv preprint arXiv:2312.13010, 2023.
     Engineering, 2024, pp. 572–576.                                             [22] H. Taherkhani, M. Sepindband, H. V. Pham, S. Wang, and H. Hemmati,
 [3] Y. Tang, Z. Liu, Z. Zhou, and X. Luo, “Chatgpt vs sbst: A                        “Epic: Cost-effective search-based prompt engineering of llms for code
     comparative assessment of unit test suite generation,” IEEE Trans.               generation,” arXiv preprint arXiv:2408.11198, 2024.
     Softw. Eng., vol. 50, no. 6, p. 1340–1359, Jun. 2024. [Online].             [23] L. Zhong, Z. Wang, and J. Shang, “Ldb: A large language model
     Available: https://doi.org/10.1109/TSE.2024.3382365                              debugger via verifying runtime execution step-by-step,” arXiv preprint
 [4] V. Vikram, C. Lemieux, J. Sunshine, and R. Padhye, “Can large                    arXiv:2402.16906, 2024.
     language models write good property-based tests?” arXiv preprint            [24] S. M. T. I. Tonmoy, S. M. M. Zaman, V. Jain, A. Rani, V. Rawte,
     arXiv:2307.04346, 2023.                                                          A. Chadha, and A. Das, “A comprehensive survey of hallucination
 [5] L. Plein, W. C. Ouédraogo, J. Klein, and T. F. Bissyandé, “Automatic           mitigation techniques in large language models,” 2024. [Online].
     generation of test cases based on bug reports: a feasibility study               Available: https://arxiv.org/abs/2401.01313
     with large language models,” in Proceedings of the 2024 IEEE/ACM            [25] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdh-
     46th International Conference on Software Engineering: Companion                 ery, and D. Zhou, “Self-consistency improves chain of thought reasoning
     Proceedings, 2024, pp. 360–361.                                                  in language models,” arXiv preprint arXiv:2203.11171, 2022.
 [6] Y. Tian, W. Yan, Q. Yang, X. Zhao, Q. Chen, W. Wang, Z. Luo, L. Ma,         [26] S. Dhuliawala, M. Komeili, J. Xu, R. Raileanu, X. Li, A. Celikyilmaz,
     and D. Song, “Codehalu: Investigating code hallucinations in llms via            and J. Weston, “Chain-of-verification reduces hallucination in large
     execution-based verification,” in Proceedings of the AAAI Conference             language models,” arXiv preprint arXiv:2309.11495, 2023.
     on Artificial Intelligence, vol. 39, no. 24, 2025, pp. 25 300–25 308.       [27] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J.-G. Lou, and
 [7] F. Liu, Y. Liu, L. Shi, H. Huang, R. Wang, Z. Yang, L. Zhang, Z. Li,             W. Chen, “Codet: Code generation with generated tests,” 2022.
     and Y. Ma, “Exploring and evaluating hallucinations in llm-powered               [Online]. Available: https://arxiv.org/abs/2207.10397
     code generation,” arXiv preprint arXiv:2404.00971, 2024.                    [28] S. Kouemo Ngassom, A. Moradi Dakhel, F. Tambon, and F. Khomh,
 [8] M. Schäfer, S. Nadi, A. Eghbali, and F. Tip, “An empirical evaluation of        “Chain of targeted verification questions to improve the reliability of
     using large language models for automated unit test generation,” IEEE            code generated by llms,” in Proceedings of the 1st ACM International
     Transactions on Software Engineering, vol. 50, no. 1, pp. 85–105, 2024.          Conference on AI-Powered Software, ser. AIware 2024. New York,
 [9] T. Y. Zhuo, M. C. Vu, J. Chim, H. Hu, W. Yu, R. Widyasari, I. N. B.              NY, USA: Association for Computing Machinery, 2024, p. 122–130.
     Yusuf, H. Zhan, J. He, I. Paul et al., “Bigcodebench: Benchmarking               [Online]. Available: https://doi.org/10.1145/3664646.3664772
     code generation with diverse function calls and complex instructions,”      [29] Q. Team, “Qwen3 technical report,” 2025. [Online]. Available:
     arXiv preprint arXiv:2406.15877, 2024.                                           https://arxiv.org/abs/2505.09388
[10] A. Matton, T. Sherborne, D. Aumiller, E. Tommasone, M. Alizadeh,            [30] G. Team, A. Kamath, J. Ferret, S. Pathak, N. Vieillard, R. Merhej,
     J. He, R. Ma, M. Voisin, E. Gilsenan-McMahon, and M. Gallé,                     S. Perrin, T. Matejovicova, A. Ramé, M. Rivière, L. Rouillard,
     “On leakage of code generation evaluation datasets,” arXiv preprint              T. Mesnard, G. Cideron, J. bastien Grill, S. Ramos, E. Yvinec,
     arXiv:2407.07565, 2024.                                                          M. Casbon, E. Pot, I. Penchev, G. Liu, F. Visin, K. Kenealy,
[11] M. L. Siddiq, J. C. Da Silva Santos, R. H. Tanvir, N. Ulfat,                     L. Beyer, X. Zhai, A. Tsitsulin, R. Busa-Fekete, A. Feng, N. Sachdeva,
     F. Al Rifat, and V. Carvalho Lopes, “Using large language models to              B. Coleman, Y. Gao, B. Mustafa, I. Barr, E. Parisotto, D. Tian,
     generate junit tests: An empirical study,” in Proceedings of the 28th            M. Eyal, C. Cherry, J.-T. Peter, D. Sinopalnikov, S. Bhupatiraju,
     International Conference on Evaluation and Assessment in Software                R. Agarwal, M. Kazemi, D. Malkin, R. Kumar, D. Vilar, I. Brusilovsky,
     Engineering, ser. EASE ’24. New York, NY, USA: Association                       J. Luo, A. Steiner, A. Friesen, A. Sharma, A. Sharma, A. M. Gilady,
     for Computing Machinery, 2024, p. 313–322. [Online]. Available:                  A. Goedeckemeyer, A. Saade, A. Feng, A. Kolesnikov, A. Bendebury,
     https://doi.org/10.1145/3661167.3661216                                          A. Abdagic, A. Vadi, A. György, A. S. Pinto, A. Das, A. Bapna,
[12] H. Taherkhani, J. Shin, M. A. Tahir, M. R. H. Misu, V. S.                        A. Miech, A. Yang, A. Paterson, A. Shenoy, A. Chakrabarti, B. Piot,
     Gattani, and H. Hemmati, “Toward automated validation of language                B. Wu, B. Shahriari, B. Petrini, C. Chen, C. L. Lan, C. A. Choquette-
     model synthesized test cases using semantic entropy,” 2025. [Online].            Choo, C. Carey, C. Brick, D. Deutsch, D. Eisenbud, D. Cattle,
     Available: https://arxiv.org/abs/2411.08254                                      D. Cheng, D. Paparas, D. S. Sreepathihalli, D. Reid, D. Tran, D. Zelle,
     E. Noland, E. Huizenga, E. Kharitonov, F. Liu, G. Amirkhanyan,               [45] K. Liu, Z. Chen, Y. Liu, J. M. Zhang, M. Harman, Y. Han, Y. Ma,
     G. Cameron, H. Hashemi, H. Klimczak-Plucińska, H. Singh, H. Mehta,               Y. Dong, G. Li, and G. Huang, “Llm-powered test case generation for
     H. T. Lehri, H. Hazimeh, I. Ballantyne, I. Szpektor, I. Nardini,                  detecting bugs in plausible programs,” arXiv preprint arXiv:2404.10304,
     J. Pouget-Abadie, J. Chan, J. Stanton, J. Wieting, J. Lai, J. Orbay,              2024.
     J. Fernandez, J. Newlan, J. yeong Ji, J. Singh, K. Black, K. Yu,             [46] W. C. Ouédraogo, K. Kaboré, Y. Li, H. Tian, A. Koyuncu, J. Klein,
     K. Hui, K. Vodrahalli, K. Greff, L. Qiu, M. Valentine, M. Coelho,                 D. Lo, and T. F. Bissyandé, “Large-scale, independent and comprehen-
     M. Ritter, M. Hoffman, M. Watson, M. Chaturvedi, M. Moynihan,                     sive study of the power of llms for test case generation,” arXiv preprint
     M. Ma, N. Babar, N. Noy, N. Byrd, N. Roy, N. Momchev, N. Chauhan,                 arXiv:2407.00225, 2024.
     N. Sachdeva, O. Bunyan, P. Botarda, P. Caron, P. K. Rubenstein,              [47] M. Harman and P. McMinn, “A theoretical and empirical study of search-
     P. Culliton, P. Schmid, P. G. Sessa, P. Xu, P. Stanczyk, P. Tafti,                based testing: Local, global, and hybrid search,” IEEE Transactions on
     R. Shivanna, R. Wu, R. Pan, R. Rokni, R. Willoughby, R. Vallu,                    Software Engineering, vol. 36, no. 2, pp. 226–247, 2009.
     R. Mullins, S. Jerome, S. Smoot, S. Girgin, S. Iqbal, S. Reddy, S. Sheth,    [48] P. Delgado-Pérez, A. Ramı́rez, K. J. Valle-Gómez, I. Medina-Bulo, and
     S. Põder, S. Bhatnagar, S. R. Panyam, S. Eiger, S. Zhang, T. Liu,                J. R. Romero, “Interevo-tr: Interactive evolutionary test generation with
     T. Yacovone, T. Liechty, U. Kalra, U. Evci, V. Misra, V. Roseberry,               readability assessment,” IEEE Transactions on Software Engineering,
     V. Feinberg, V. Kolesnikov, W. Han, W. Kwon, X. Chen, Y. Chow,                    vol. 49, no. 4, pp. 2580–2596, 2022.
     Y. Zhu, Z. Wei, Z. Egyed, V. Cotruta, M. Giang, P. Kirk, A. Rao,             [49] X. Xiao, S. Li, T. Xie, and N. Tillmann, “Characteristic studies of
     K. Black, N. Babar, J. Lo, E. Moreira, L. G. Martins, O. Sanseviero,              loop problems for structural test generation via symbolic execution,” in
     L. Gonzalez, Z. Gleicher, T. Warkentin, V. Mirrokni, E. Senter,                   2013 28th IEEE/ACM International Conference on Automated Software
     E. Collins, J. Barral, Z. Ghahramani, R. Hadsell, Y. Matias, D. Sculley,          Engineering (ASE). IEEE, 2013, pp. 246–256.
     S. Petrov, N. Fiedel, N. Shazeer, O. Vinyals, J. Dean, D. Hassabis,          [50] C. Pacheco, S. K. Lahiri, M. D. Ernst, and T. Ball, “Feedback-directed
     K. Kavukcuoglu, C. Farabet, E. Buchatskaya, J.-B. Alayrac, R. Anil,               random test generation,” in 29th International Conference on Software
     Dmitry, Lepikhin, S. Borgeaud, O. Bachem, A. Joulin, A. Andreev,                  Engineering (ICSE’07). IEEE, 2007, pp. 75–84.
     C. Hardin, R. Dadashi, and L. Hussenot, “Gemma 3 technical report,”          [51] B. He, N. Chen, X. He, L. Yan, Z. Wei, J. Luo, and Z.-H. Ling,
     2025. [Online]. Available: https://arxiv.org/abs/2503.19786                       “Retrieving, rethinking and revising: The chain-of-verification can
[31] J. Shin, H. Hemmati, M. Wei, and S. Wang, “Assessing evaluation                   improve retrieval augmented generation,” 2024. [Online]. Available:
     metrics for neural test oracle generation,” IEEE Transactions on Software         https://arxiv.org/abs/2410.05801
     Engineering, 2024.                                                           [52] Y. Zhao, L. Yan, W. Sun, G. Xing, S. Wang, C. Meng, Z. Cheng,
[32] M. Tufano, D. Drain, A. Svyatkovskiy, S. K. Deng, and N. Sundaresan,              Z. Ren, and D. Yin, “Improving the robustness of large language
     “Unit test case generation with transformers and focal context,” arXiv            models via consistency alignment,” in Proceedings of the 2024 Joint
     preprint arXiv:2009.05617, 2020.                                                  International Conference on Computational Linguistics, Language
[33] S. Alagarsamy, C. Tantithamthavorn, and A. Aleti, “A3test: Assertion-             Resources and Evaluation (LREC-COLING 2024), N. Calzolari, M.-Y.
     augmented automated test case generation,” Information and Software               Kan, V. Hoste, A. Lenci, S. Sakti, and N. Xue, Eds. Torino, Italia:
     Technology, vol. 176, p. 107565, 2024.                                            ELRA and ICCL, May 2024, pp. 8931–8941. [Online]. Available:
[34] J. Shin, S. Hashtroudi, H. Hemmati, and S. Wang, “Domain adaptation               https://aclanthology.org/2024.lrec-main.782/
     for code model-based unit test case generation,” in Proceedings of the       [53] W. Chen, W. Wang, Z. Chu, K. Ren, Z. Zheng, and Z. Lu,
     33rd ACM SIGSOFT International Symposium on Software Testing and                  “Self-para-consistency: Improving reasoning tasks at low cost for large
     Analysis, 2024, pp. 1211–1222.                                                    language models,” in Findings of the Association for Computational
[35] N. Rao, K. Jain, U. Alon, C. Le Goues, and V. J. Hellendoorn, “Cat-               Linguistics: ACL 2024, L.-W. Ku, A. Martins, and V. Srikumar, Eds.
     lm training language models on aligned code and tests,” in 2023 38th              Bangkok, Thailand: Association for Computational Linguistics, Aug.
     IEEE/ACM International Conference on Automated Software Engineer-                 2024, pp. 14 162–14 167. [Online]. Available: https://aclanthology.org/
     ing (ASE). IEEE, 2023, pp. 409–420.                                               2024.findings-acl.842/
[36] B. Steenhoek, M. Tufano, N. Sundaresan, and A. Svyatkovskiy, “Re-            [54] S. Huang, Z. Ma, J. Du, C. Meng, W. Wang, and Z. Lin, “Mirror-
     inforcement learning from automatic feedback for high-quality unit                consistency: Harnessing inconsistency in majority voting,” in Findings
     test generation,” in 2025 IEEE/ACM International Workshop on Deep                 of the Association for Computational Linguistics: EMNLP 2024, Y. Al-
     Learning for Testing and Testing for Deep Learning (DeepTest). IEEE,              Onaizan, M. Bansal, and Y.-N. Chen, Eds. Miami, Florida, USA:
     2025, pp. 37–44.                                                                  Association for Computational Linguistics, Nov. 2024, pp. 2408–2420.
[37] Y. Zhang, W. Song, Z. Ji, N. Meng et al., “How well does llm generate             [Online]. Available: https://aclanthology.org/2024.findings-emnlp.135/
     security tests?” arXiv preprint arXiv:2310.00710, 2023.                      [55] H. Wang, A. Prasad, E. Stengel-Eskin, and M. Bansal, “Soft
[38] A. M. Dakhel, A. Nikanjam, V. Majdinasab, F. Khomh, and M. C.                     self-consistency improves language model agents,” 2024. [Online].
     Desmarais, “Effective test generation using pre-trained large language            Available: https://arxiv.org/abs/2402.13212
     models and mutation testing,” Information and Software Technology, vol.      [56] A. Prasad, W. Yuan, R. Y. Pang, J. Xu, M. Fazel-Zarandi, M. Bansal,
     171, p. 107468, 2024.                                                             S. Sukhbaatar, J. Weston, and J. Yu, “Self-consistency preference
[39] C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen, “Codamosa: Escaping            optimization,” 2025. [Online]. Available: https://arxiv.org/abs/2411.
     coverage plateaus in test generation with pre-trained large language              04109
     models,” in 2023 IEEE/ACM 45th International Conference on Software
     Engineering (ICSE). IEEE, 2023, pp. 919–931.
[40] V. Li and N. Doiron, “Prompting code interpreter to write better unit
     tests on quixbugs functions,” arXiv preprint arXiv:2310.00483, 2023.
[41] V. Guilherme and A. Vincenzi, “An initial investigation of chatgpt
     unit test generation capability,” in Proceedings of the 8th Brazilian
     Symposium on Systematic and Automated Software Testing, 2023, pp.
     15–24.
[42] Z. Yuan, Y. Lou, M. Liu, S. Ding, K. Wang, Y. Chen, and X. Peng,
     “No more manual tests? evaluating and improving chatgpt for unit test
     generation,” arXiv preprint arXiv:2305.04207, 2023.
[43] S. Bhatia, T. Gandhi, D. Kumar, and P. Jalote, “Unit test generation using
     generative ai: A comparative performance analysis of autogeneration
     tools,” in Proceedings of the 1st International Workshop on Large
     Language Models for Code, 2024, pp. 54–61.
[44] C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen, “Codamosa: Escaping
     coverage plateaus in test generation with pre-trained large language
     models,” in Proceedings of the 45th International Conference on
     Software Engineering, ser. ICSE ’23. IEEE Press, 2023, p. 919–931.
     [Online]. Available: https://doi.org/10.1109/ICSE48619.2023.00085
