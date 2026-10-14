                                         From Business Requirements to Test Assertions:
                                         Evaluating LLM-Generated Oracles on Real Bugs
                                         Tiancheng Ma #
                                         Department of EECS, University of Tennessee, Knoxville, TN, USA

                                         Nasir U. Eisty #
                                         Department of EECS, University of Tennessee, Knoxville, TN, USA

                                               Abstract
                                         Background. The oracle problem (determining the correct expected outcome for a test) remains
                                         a major bottleneck in automated testing, and is increasingly relevant as non-experts rely on AI-
                                         generated code they cannot reliably validate. Objective. We study whether large language models
                                         (LLMs) can generate generalizable test oracles directly from natural-language business requirements,
                                         without access to source code or example input–output pairs. Method. We propose a reproducible,
                                         requirement-driven pipeline grounded in Defects4J. For each of 10 real bugs from Defects4J Lang
                                         (Bugs 1 and 3–11), we (i) extract behavioral changes via buggy/fixed diffs, (ii) manually translate
                                         the change into a business requirement, (iii) construct a requirement-derived oracle (REQ) as a gold
                                         standard, and (iv) prompt five LLMs (DeepSeek-V3, Gemma-3n, Llama-3, Mistral-7B, and Qwen-3)
                                         to generate Java oracle code. We evaluate oracle correctness and generalization under two targets:
arXiv:2607.10277v1 [cs.SE] 11 Jul 2026




                                         agreement with REQ and agreement with the system under test (SUT), reporting macro-averaged
                                         accuracy, precision, recall, and F1. Results. LLMs achieve non-trivial generalization but with
                                         substantial bug- and model-level variance. Generated oracles align more closely with REQ than with
                                         SUT, and correlations between requirement technicality/ambiguity ratings and oracle accuracy are
                                         weak with wide confidence intervals. Conclusion. No detectable linear relationship exists between
                                         requirement properties and oracle accuracy in this dataset, suggesting that pretraining coverage
                                         and the semantic specificity of the required behavior dominate oracle correctness. As a pilot proof
                                         of concept, these findings are preliminary and are intended to establish feasibility and motivate
                                         larger-scale empirical investigation.

                                         2012 ACM Subject Classification Software and its engineering → Software testing and debugging

                                         Keywords and phrases test oracle generation; large language models; business requirements; empirical
                                         study; Defects4J


                                          1     Introduction

                                         Context. A successful software project depends not only on correct and verified imple-
                                         mentation, but on the accurate translation of real-world business requirements into reliable
                                         software behavior. In practice, business requirements are written in natural language, which
                                         is well known to be prone to ambiguity, incompleteness, and inconsistencies [9]. These
                                         characteristics make it difficult for developers to precisely interpret the intended behavior
                                         and implement code that fully satisfies stakeholder expectations.
                                             Moreover, delivering high-quality software requires not only correct implementation but
                                         also extensive testing, since no developer can guarantee that their code is free of defects.
                                         Effective testing, however, demands substantial effort: developers must create large numbers
                                         of test cases along with corresponding test oracles, the expected outputs used to determine
                                         correctness. Producing these oracles often requires deep domain knowledge, significant human
                                         labor, and in many scenarios, the correct expected output may be unclear or even inaccessible
                                         for complex test cases. As a result, oracle construction has long been recognized as one of the
                                         most costly and difficult components of software testing. This challenge is especially relevant
                                         when testers only have access to high-level business requirements, rather than source code,
0:2   LLM-Generated Test Oracles from Business Requirements


      formal specifications or example input-output pairs.
           At the same time, the landscape of software development is rapidly shifting with the
      rise of AI. Both technical developers and non-technical professionals increasingly rely on AI
      tools to generate code, analyze data, or prototype new software features. Yet most of these
      users cannot reliably verify whether the AI-generated code is correct or practical. They often
      resort to ad-hoc verification or subjective judgment, but such methods are slow, inconsistent,
      and heavily influenced by an individual’s background and technical expertise. Recent studies
      further show that non-technical business professionals often struggle to identify flaws in
      AI-generated analyses, even when the errors require no programming knowledge to detect
      [11]. This gap between AI-generated output and users’ ability to verify correctness highlights
      the growing need for automated, reliable mechanisms for validating system behavior.
           Taken together, these observations reinforce the long-standing oracle problem [12, 1]:
      determining the correct expected output is frequently the bottleneck of automated testing.
      This motivates investigating whether modern LLMs can help automate oracle construction,
      enabling both experts and non-experts to verify AI-generated code more efficiently and
      effectively.
           While prior research has explored using LLMs to generate test inputs from natural
      language requirements and infer oracles from existing pairs of inputs and outputs, very few
      studies have examined whether LLMs can generate reliable and generalized test oracles
      directly from business requirements [8].
           Proposal & Evaluation. To investigate whether LLMs can generate reliable and
      generalizable test oracles from business requirements, we design a systematic and reproducible
      pipeline grounded in Defects4J. We adopt Defects4J as our primary dataset because it is
      actively maintained, widely used in software engineering research, and provides a curated
      collection of real, historical bugs with both buggy and fixed versions available. This allows
      us to construct controlled, realistic scenarios that reflect true software behaviors.
           Our approach operates at the granularity of individual bugs from projects of Defects4J [5].
      For each bug, we first check out the buggy and fixed versions of the project and compute
      the code differences between them, which provide the ground-truth behavioral change
      introduced by the fix. Using this information, we translate the observed change into
      a natural-language business requirement to intentionally mirror real-world development
      conditions, where requirements are expressed at a high level and rarely contain explicit
      code-level details.
           Based on the business requirement, we then construct a standard test oracle that precisely
      captures the expected correct behavior after the fix. This oracle serves as the authoritative
      specification against which LLM-generated oracles can be evaluated. Next, we use the
      business requirement to construct prompts that are provided to five LLMs, asking them
      to generate their own test oracles without exposing any source code or diff information.
      This setup reflects a realistic use case in which LLMs operate purely from business-level
      descriptions, which would occur for many non-technical AI users.
           To evaluate both human-constructed and LLM-generated oracles, we design a diverse set
      of test cases to measure not only correctness but also generalizability, whether the oracle
      captures the underlying intent of the requirement beyond the examples explicitly described.
           Contribution. We contribute (i) a reproducible, requirement-driven pipeline for evaluat-
      ing LLM oracle generation from business requirements alone, grounded in Defects4J [5], (ii)
      empirical results across five LLMs and ten real bugs with two oracle-correctness targets, and
      (iii) a correlation analysis of requirement attributes and oracle accuracy that informs future
      benchmark design. This work is scoped as a pilot proof of concept limited to ten bugs from a
T. Ma and N. U. Eisty                                                                               0:3


single Defects4J project (Lang); results are preliminary and intended to establish feasibility,
surface early empirical findings, and motivate future large-scale investigation across multiple
projects and LLMs.
    Research Question. To guide our study, we investigate the following research questions:
    RQ1: How well can LLMs generate requirement-driven test oracles that generalize to
    unseen test cases?
    RQ2: How do LLM-generated oracles compare to the requirement-derived oracle (REQ)
    and the system-under-test (SUT) across different types of bugs?
    RQ3: How do the characteristics of business requirements, particularly technicality and
    ambiguity, influence the performance of LLM-generated oracles?


 2     Related Work

Recent work on test oracle automation spans traditional specification-based methods, learning-
based techniques, and emerging LLM-based approaches. Classical mechanisms such as
assertions, contracts, and metamorphic relations remain limited in coverage and applicability,
while newer formal and learning-driven methods improve behavioral completeness. With
LLMs, researchers increasingly explore generating oracles from natural language and docu-
mentation, showing promising gains but still facing challenges in oracle quality, generalization,
and reproducibility.
    Pre-LLM oracle generation relied on formal specifications or learned behavioral models.
Liu et al.’s Vibration Method [7] automatically generates both test cases and oracles directly
from pre- and post-conditions, introducing test generation criteria that ensure coverage of
functional scenarios and their corresponding execution paths, an improvement over traditional
partitioning-based techniques that often leave paths uncovered. The SEER framework [4]
takes a fundamentally different approach by learning to distinguish passing from failing
behavior through a joint embedding of unit tests and methods under test, eliminating the
need for explicit assertions or formal specifications. Evaluated on more than 5,000 Java unit
tests, SEER achieved 93% accuracy, 86% precision, and 90% F1, with strong generalization
to unseen projects.
    With the rise of LLMs, researchers have explored generating oracles from documentation,
code, and natural language. Molina et al. [8] survey the landscape across 37 recent LLM-based
studies, finding that most work targets assertion generation while fewer address invariants,
metamorphic relations, or exception oracles; they identify oracle quality, reproducibility, and
dataset bias as key open challenges. Khandaker et al.’s AugmenTest [6] generates oracles from
documentation and developer comments rather than source code, comparing four prompting
strategies on 142 Java classes; an extended prompting strategy achieved up to 30% correctness
compared to 8.2% for TOGA, though RAG-based approaches underperformed, suggesting
difficulties integrating structured retrieval with LLM inference. Hossain et al.’s TOGLL
[3] fine-tunes seven code LLMs with six prompt designs on 110 large-scale Java projects,
producing 3.8× more assertion oracles and 4.9× more exception oracles than TOGA while
detecting over 1,000 mutants missed by EvoSuite.
    On the test-input side, Hasan et al. [2] generate high-level test skeletons from natural-
language scenarios, and Schäfer et al. [10] demonstrate that LLM-generated tests achieve
coverage competitive with EvoSuite but exhibit persistent difficulty with complex branching
logic. Yuan et al. [13] evaluate ChatGPT for unit test generation and find that oracle
correctness, not syntactic validity, is the primary bottleneck, directly motivating our focus
on requirement-driven oracle generation.
0:4   LLM-Generated Test Oracles from Business Requirements




           Figure 1 Workflow of the proposed approach.



         Overall, while LLM-based test generation has advanced rapidly, generating correct,
      generalizable oracles directly from natural-language business requirements remains under-
      explored [8, 1]. Existing work largely assumes access to source code or prior test examples;
      our study examines whether oracles can be inferred from requirements alone.


       3      Approach

      Our approach evaluates a requirements-only oracle generation setting: the LLM receives
      a natural-language business requirement and minimal method-level structure needed for
      compilation, but does not receive source code, buggy-to-fixed diffs, or example input-output
      pairs.
      Our pipeline (Figure 1) takes real bugs from Defects4J [5], derives a natural-language business
      requirement from each buggy-to-fixed diff, constructs a ground-truth REQ, and prompts five
      LLMs to generate their own oracles from the requirement alone, without access to source
      code or example inputs. The REQ oracle represents our manually constructed reference
      interpretation of the intended requirement-level behavior implied by the fix. Generated oracles
      are evaluated against both REQ and the SUT using a systematically constructed test suite.
      Comparing against REQ measures whether the LLM captures the intended specification,
      whereas comparing against SUT measures whether the generated oracle matches the observed
      implementation behavior.


       4      Implementation

      Our implementation is based on the Defects4J benchmark [5], focusing specifically on the
      Lang project and Bugs 1 and 3–11 (10 bugs in total), forming a pilot study, enabling detailed
      oracle construction and bug analysis. Full prompt templates for all bugs are provided in the
      replication package.
T. Ma and N. U. Eisty                                                                            0:5


4.1    Identify Bug Behavior
For each bug, we check out both the buggy and fixed versions using the following commands:
defects4j checkout -p Lang -v [BUG_ID]b -w Lang_[BUG_ID]_buggy
defects4j checkout -p Lang -v [BUG_ID]f -w Lang_[BUG_ID]_fixed

   We then compute the behavioral change by running a recursive unified diff over the two
versions:
diff -ru Lang_[BUG_ID]_buggy Lang_[BUG_ID]_fixed \
  > diff_Lang_[BUG_ID].txt

   The generated difference file reflects how the bug was repaired and serves as the basis for
understanding the intended corrected behavior.

4.2    Business Requirement Construction
Using diff_Lang_[BUG_ID].txt, we manually derive a corresponding business requirement.
Our objective is to express the expected system behavior in a non-technical, natural-language
form without exposing code-level details. These requirements intentionally retain some
ambiguity to mimic how stakeholders typically describe intended functionality.

4.3    Standard Test Oracle (REQ)
Given the code difference and the business requirement, we construct a requirement-derived
test oracle, denoted as REQ. This oracle captures the correct behavior implied by the fix
and serves as the reference oracle for comparison.

4.4    Prompt Construction
Each LLM prompt contains four structured components:
   Structure: package name, class name, return type, and method signature.
   Content Restrictions: prohibitions against using imports or external libraries.
   Output Format: instructing the model to output Java code only.
   Background Requirement: the business requirement derived earlier.

   Minimal implementation details (e.g., class names) are provided solely to eliminate the
need for post-processing and ensure all outputs are evaluated exactly as generated.

4.5    LLM Oracle Generation
We evaluate five LLMs: DeepSeek-V3, Gemma-3n-E4B-it, Llama-3-70B-chat-hf, Mistral-7B-
Instruct-v0.2, and Qwen3-Coder-480B-A35B-Instruct-FP8. All models are queried through
the Together AI API without any manual modification of their outputs.

4.6    Test Case Construction and Evaluation
For each bug, we construct a suite of test cases derived from the business requirement and
the REQ oracle. Each test case is executed against three standards:

1. SUT: the actual implementation in Defects4J.
2. REQ: the requirement-derived oracle.
3. LLM-Oracle: the oracle produced by each LLM.
0:6   LLM-Generated Test Oracles from Business Requirements


          This enables three key comparisons:
          REQ vs. SUT: Does the implementation satisfy the requirement?
          LLM vs. REQ: Does the LLM capture the intended specification?
          LLM vs. SUT: Does the LLM match real program behavior?
      If an LLM-generated oracle does not compile, we exclude that bug-model pair from the
      evaluation metrics and report the number of evaluated pairs in the summary table.

      4.7    Result Analysis
      We analyze results along three dimensions.
        First, we measure the technicality and ambiguity of each business requirement using
      ChatGPT 5.1 as an LLM-based evaluator, due to limited tool support for requirement
      ambiguity analysis. The evaluation prompt is:
       I’m doing research on LLMs’ performance to generate generalized test oracles given
           business requirements. Here are business requirements provided to LLMs, rate
           technical degree(1-5, where 1=not technical and 5=very technical) and ambiguous
           degree(1-5, where 1=not ambiguous and 5=very ambiguous):
       [bug_id: business requirement]

          Second, we compute accuracy, precision, recall, and F1-score for each bug and report
      macro-averaged values across all models and standards.
          Finally, we compute Pearson correlation coefficients and 95% confidence intervals to
      explore relationships between requirement attributes (technical degree, ambiguity) and LLM
      oracle accuracy. This allows us to assess whether requirement characteristics systematically
      influence LLM performance.


       5     Evaluation
      We evaluate three aspects: (1) characteristics of the business requirements, (2) per-bug LLM
      oracle performance, and (3) correlation between requirement attributes and oracle accuracy.

      5.1    Characteristics of the Business Requirements
      We scored each requirement on technical degree and ambiguity degree (1–5) using ChatGPT 5.1
      as an LLM-as-a-judge. Table 1 shows the results. Requirements range from highly technical
      with moderate ambiguity (Bugs 1, 6) to simple and unambiguous (Bugs 9, 10), providing a
      small but varied pilot benchmark for requirement-driven oracle generation.

      5.2    Performance of LLM-generated Oracles
      In this section, we first examine LLM performance on the ten bugs, detailing the observed
      behaviors relative to the underlying code changes. We then summarize the overall results by
      reporting the average macro-level metrics and highlighting general performance trends.
          Table 2 summarises per-bug outcomes. Bug 8 is the easiest (all models reach perfect
      accuracy); Bug 3 is the hardest (multi-step digit-counting logic defeats every model). Bugs
      involving structured lookup rules (Bug 4) or simple conditional exceptions (Bug 9) are handled
      well by most models, while numeric-type promotion (Bugs 1, 3) and subtle whitespace handling
      (Bug 10) prove consistently difficult. Mistral-7B is the weakest model across bugs, occasionally
      producing non-compiling output; Gemma-3n fails specifically on Unicode code-point iteration
      (Bug 6).
T. Ma and N. U. Eisty                                                                          0:7


   Table 1 Technicality and Ambiguity of Business Requirements (Rated by GPT-5.1)

             Technical    Ambiguity
      Bug    Degree       Degree    Rationale (Short)
             (1–5)        (1–5)
      Bug1   5            3         Highly technical numeric-type and boundary rules;
                                    moderate ambiguity about exact promotion order
                                    and edge-case definitions.
      Bug3   4            4         Conceptually clear but vague thresholds; moder-
                                    ately technical numeric representation logic.
      Bug4   3            3         Medium technicality; ambiguity about visible char-
                                    acters and Unicode normalization.
      Bug5   4            3         Moderately technical string-format parsing; ambi-
                                    guity in malformed patterns.
      Bug6   5            2         Very technical Unicode iteration; low ambiguity
                                    due to clear rules.
      Bug7   3            2         Straightforward error-handling rules with low am-
                                    biguity.
      Bug8   4            4         Technical timezone/calendar behavior with am-
                                    biguous DST logic and missing-field handling.
      Bug9   3            2         Logic is simple; low ambiguity beyond definition
                                    of position handling.
      Bug10 2             1         Extremely clear; minimal technicality and almost
                                    no ambiguity.
      Bug11 3             2         Some technical nuance about bounds and defaults;
                                    low ambiguity due to explicit rules.




    Table 3 reports macro-averaged metrics. DeepSeek-V3 is the top performer; Llama-3
and Qwen-3 form a solid second tier. Gemma-3n and Mistral-7B trail significantly. Across
all models (Gemma-3n excepted), REQ-target scores exceed SUT-target scores, confirming
that LLM-generated oracles align more naturally with the requirement specification used in
prompting than with the underlying implementation behavior. The Count column shows
how many bug cases were successfully evaluated for each model and target after excluding
non-compiling oracle outputs.




5.3   Correlation Between Requirement Attributes and Oracle Accuracy

For each of the ten bugs, we compute the Pearson correlation coefficient (r) and 95% CI
between each requirement attribute (technicality; ambiguity) and per-model oracle accuracy,
under both SUT and REQ targets. Figure 2 visualizes the results.
    All r values are near zero (technicality: −0.50 to +0.24; ambiguity: −0.36 to +0.03) and
all 95% CIs include zero under both evaluation settings. In this small dataset, no model
exhibits a consistent directional trend. We conclude that, within this dataset, neither
technicality nor ambiguity reliably predicts LLM oracle accuracy in this pilot
dataset. Other factors, such as pretraining coverage of the relevant algorithmic domain or
semantic specificity of the required behavior, appear to dominate oracle correctness.
0:8   LLM-Generated Test Oracles from Business Requirements


           Table 2 Per-bug performance summary (SUT target, macro-F1 range across 5 LLMs).

                             Bug    F1 range Key challenge
                             Bug 1  0.40–0.92 Hex digit-count type promo-
                                              tion
                             Bug 3 0.20–0.55 Decimal digit-count type selec-
                                              tion
                             Bug 4 0.60–1.00 Unicode lookup table (easy for
                                              most)
                             Bug 5 0.82–1.00 Locale-format validation
                             Bug 6 0.50–1.00 Code-point index iteration
                             Bug 7 0.70–1.00 Double-dash rejection rule
                             Bug 8 1.00–1.00 Timezone calendar lookup
                                              (trivial)
                             Bug 9 0.75–1.00 Region-end exception guard
                             Bug 10 0.40–0.85 Subtle    whitespace     non-
                                              removal
                             Bug 11 0.80–1.00 Boundary end<=start check

           Table 3 Average LLM Performance Across 10 Bugs

        LLM            Target   Avg Acc    Avg MacroP       Avg MacroR   Avg MacroF1     Count
        REQ-based      SUT       0.9580       0.7942           0.7952       0.7929        10
        Deepseek-V3    SUT       0.8590       0.7500           0.7569       0.7476        10
        Deepseek-V3    REQ       0.8892       0.8217           0.8280       0.8179        10
        Gemma-3n       SUT       0.7100       0.6659           0.6544       0.6356        10
        Gemma-3n       REQ       0.7064       0.6104           0.6113       0.5947        10
        Llama-3        SUT       0.8455       0.7130           0.7259       0.7140        10
        Llama-3        REQ       0.8695       0.7986           0.7844       0.7797        10
        Mistral-7B     SUT       0.6440       0.5699           0.5825       0.5428         9
        Mistral-7B     REQ       0.6617       0.5930           0.5831       0.5600         9
        Qwen-3         SUT       0.8077       0.6992           0.7188       0.7030        10
        Qwen-3         REQ       0.8379       0.7725           0.7983       0.7779        10



       6      Discussion
      This section interprets the findings of our three research questions, discusses threats to
      validity, and outlines implications for researchers and practitioners.

      6.1     RQ Answers
      RQ1: Generalization of Requirement-Driven LLM Test Oracles. LLMs can generate
      oracles that generalize to unseen test cases to a limited but measurable extent; performance
      varies substantially across bugs, with numerical-type promotion and digit-counting logic
      posing the greatest challenge, while structured rule-based bugs are handled reliably.
         RQ2: Comparison Against REQ-Derived and SUT Oracles. LLM-generated
      oracles score consistently higher against the REQ oracle than against the SUT, confirming
      that requirement-prompted LLMs model the intended specification more faithfully than the
      underlying implementation. This gap suggests that requirement-prompted LLMs behave
      more like specification-level oracle generators than implementation-level ones. DeepSeek-V3
T. Ma and N. U. Eisty                                                                             0:9




  Figure 2 Pearson correlation between accuracy and requirement attributes under REQ (top) and
SUT (bottom) targets across all five LLMs.


leads across both targets; Mistral-7B trails, with occasional non-compiling output.
    RQ3: Influence of Requirement Technicality and Ambiguity. Pearson correlations
between requirement technicality or ambiguity and LLM oracle accuracy are near zero across
all models and targets (all 95% CIs include zero), indicating that surface-level requirement
complexity does not reliably predict oracle correctness within this dataset.

6.2    Interpretation of Findings
Partial generalization is achievable but inconsistent. Our results show that modern
LLMs can infer correct oracle logic from natural-language business requirements and apply
it to unseen test inputs, but only partially. The wide spread in per-bug accuracy, from near-
perfect on structured, rule-based bugs (e.g., Bug 8, Bug 11) to consistently poor performance
on digit-counting or numeric-type promotion bugs (e.g., Bug 3), suggests that oracle quality
depends more on the semantic nature of the required behavior than on any surface-level
property of the requirement text. Bugs whose correct behavior maps closely to common
programming idioms present in LLM training data are handled well; bugs requiring multi-step
numeric reasoning or deep domain knowledge of type promotion rules are not.
    Requirement-level prompting creates a REQ–SUT gap. A consistent finding across
all five models is that LLM-generated oracles score higher against the REQ than against
the SUT. This is an expected but important observation: because LLMs are prompted
with the business requirement as the sole source of truth, they learn the specification’s
language, not the implementation’s behavior. This means that LLM-generated oracles are
more useful for requirement conformance checking than for regression testing of existing
systems. Practitioners should treat these two use cases as distinct when selecting oracle
generation strategies.
    Requirement complexity does not predict model accuracy in this dataset. The
absence of a detectable linear correlation between technicality or ambiguity ratings and oracle
accuracy has a nuanced implication. It provides little support for the simple hypothesis that
“harder requirements produce worse oracles,” but it does not mean that requirement properties
are irrelevant. Rather, it suggests that the relationship, if any, is nonlinear or moderated by
factors such as the semantic distance between the requirement text and the LLM’s training
distribution. Future work should explore richer characterizations of requirement difficulty,
such as the number of logical conditions or the presence of numeric constraints, rather than
coarse ordinal ratings.
0:10   LLM-Generated Test Oracles from Business Requirements


       6.3    Threats to Validity
       Internal. Business requirements and REQ oracles were derived manually from buggy-
       to-fixed diffs, introducing author subjectivity; different phrasing could shift LLM outputs.
       Technicality/ambiguity ratings from a single LLM judge (ChatGPT 5.1) carry no inter-rater
       reliability estimate. Test case suites are also manually constructed; a different suite could
       shift per-bug metrics. Our handling of non-compiling LLM outputs may also affect aggregate
       metrics, since excluding such outputs differs from treating them as oracle failures.
           External. The study covers 10 bugs from one Defects4J component (Lang) in Java,
       concentrated in string and numeric utilities. Generalisation to other languages, bug types, or
       requirement styles is untested. LLM results may shift with model updates.
           Construct. The REQ oracle is a single human interpretation and may not be unique.
       Accuracy against REQ/SUT does not fully capture practical oracle utility (e.g., false-positive
       rates in CI).


       6.4    Implications
       For researchers. This study provides an early, reproducible benchmark for requirement-
       driven oracle generation, a problem that existing literature addresses far less than input
       generation or assertion synthesis from source code [8, 1]. The pipeline, business requirements,
       and evaluation test cases are made available to support follow-on studies with larger bug
       corpora or finer-grained requirement representations.
           For practitioners. LLMs such as DeepSeek-V3 and Llama-3 already achieve macro-
       averaged accuracy above 0.84 against REQ, suggesting they are viable assistants for requirement-
       driven oracle drafting. However, developers should not rely on LLM-generated oracles as a
       substitute for manually reviewed assertions in safety-critical or numerically intensive code
       paths, where model accuracy drops significantly.


        7     Conclusion

       This study piloted whether LLMs can generate requirement-driven test oracles that generalize
       from business requirements alone, using real bugs from Defects4J across ten bugs, five LLMs,
       and two oracle targets.
            Our findings show that LLMs are capable of producing test oracles that capture substantial
       portions of intended behavior. Models such as Deepseek-V3, Llama-3, and Qwen-3 achieve
       high accuracy and reasonable F1 scores on unseen inputs, indicating that the problem is
       partially solved, particularly when required behavior is structured and well-defined. However,
       performance varies significantly: models struggle with nuanced numerical rules, Unicode
       handling, and edge-case validations, and weaker models like Gemma-3n and Mistral-7B often
       fail to produce compilable or correct outputs. LLM-generated oracles align more closely with
       the requirement-derived (REQ) oracle than with SUT behavior, confirming that LLMs more
       readily model intended specification than exact implementation logic.
            Our correlation analysis finds no meaningful relationship between requirement attributes
       (technicality and ambiguity) and LLM accuracy, suggesting that limitations arise from
       semantic or logical task difficulty rather than linguistic requirement complexity. In summary,
       LLMs provide a promising but incomplete solution to requirement-driven oracle generation,
       useful as assistive tools in automated testing, but not yet dependable enough to replace
       manually engineered oracles where high precision and semantic correctness are required.
T. Ma and N. U. Eisty                                                                                 0:11


Data Availability
The replication package for this study, including the business requirements derived for
each bug, the REQ oracles, the LLM-generated oracles, the test case suites, and the eval-
uation scripts, is available at: https://figshare.com/s/50c240d183532de44c7a. The
Defects4J benchmark used to derive bugs is publicly available at https://github.com/
rjust/defects4j [5]. LLM outputs were obtained via the Together AI API; model names
and versions are documented in the replication package.

     References
 1   Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo. The oracle
     problem in software testing: A survey. IEEE Transactions on Software Engineering, 41(5):507–
     525, 2015. doi:10.1109/TSE.2014.2372785.
 2   Navid Bin Hasan, Md. Ashraful Islam, Junaed Younus Khan, Sanjida Senjik, and Anindya
     Iqbal. Automatic high-level test case generation using large language models, 2025. URL:
     https://arxiv.org/abs/2503.17998, arXiv:2503.17998.
 3   Soneya Binta Hossain and Matthew B. Dwyer. Togll: Correct and strong test oracle generation
     with llms. In 2025 IEEE/ACM 47th International Conference on Software Engineering (ICSE),
     page 1475–1487. IEEE, April 2025. URL: http://dx.doi.org/10.1109/ICSE55347.2025.
     00098, doi:10.1109/icse55347.2025.00098.
 4   Ali Reza Ibrahimzada, Yigit Varli, Dilara Tekinoglu, and Reyhaneh Jabbarvand. Perfect is the
     enemy of test oracle. In Proceedings of the 30th ACM Joint European Software Engineering
     Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE ’22,
     page 70–81. ACM, November 2022. URL: http://dx.doi.org/10.1145/3540250.3549086,
     doi:10.1145/3540250.3549086.
 5   René Just, Darioush Jalali, and Michael D. Ernst. Defects4J: A database of existing faults to
     enable controlled testing studies for Java programs. In Proceedings of the 2014 International
     Symposium on Software Testing and Analysis (ISSTA), pages 437–440. ACM, 2014. doi:
     10.1145/2610384.2628055.
 6   Shaker Mahmud Khandaker, Fitsum Kifetew, Davide Prandi, and Angelo Susi. Augmentest:
     Enhancing tests with llm-driven oracles, 2025. URL: https://arxiv.org/abs/2501.17461,
     arXiv:2501.17461.
 7   Shaoying Liu and Shin Nakajima. Automatic test case and test oracle generation based on
     functional scenarios in formal specifications for conformance testing. IEEE Transactions on
     Software Engineering, 48(2):691–712, 2022. doi:10.1109/TSE.2020.2999884.
 8   Facundo Molina, Alessandra Gorla, and Marcelo d’Amorim. Test oracle automation in the era
     of llms. ACM Trans. Softw. Eng. Methodol., 34(5), May 2025. doi:10.1145/3715107.
 9   Sabina-Cristiana Necula, Florin Dumitriu, and Valerică Greavu-Serban. A systematic literature
     review on using natural language processing in software requirements engineering. Electronics,
     13:2055, 05 2024. doi:10.3390/electronics13112055.
10   Max Schäfer, Sarah Nadi, Aryaz Eghbali, and Frank Tip. An empirical evaluation of using
     large language models for automated unit test generation. IEEE Transactions on Software
     Engineering, 50(4):911–929, 2024. doi:10.1109/TSE.2024.3364264.
11   Yuvraj Virk and Dongyu Liu. Non-programmers assessing ai-generated code: A case study
     of business users analyzing data, 2025. URL: https://arxiv.org/abs/2508.06484, arXiv:
     2508.06484.
12   Elaine J. Weyuker. On testing non-testable programs. The Computer Journal, 25(4):465–470,
     1982. doi:10.1093/comjnl/25.4.465.
13   Zhiqiang Yuan, Yiling Lou, Mingwei Liu, Shiji Ding, Kaixin Wang, Yixuan Chen, and Xin
     Peng. No more manual tests? Evaluating and improving ChatGPT for unit test generation,
     2023. URL: https://arxiv.org/abs/2305.04207, arXiv:2305.04207.
