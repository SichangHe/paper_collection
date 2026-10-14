                                          Automatic Assertion Mining in Assertion-Based
                                          Verification: Techniques, Challenges, and Future
                                                              Directions
                                                         Mohammad Reza Heidari Iman, Giorgio Di Natale, and Katell Morin-Allory
                                                         Univ. Grenoble Alpes, CNRS, Grenoble INP*, TIMA, 38000 Grenoble, France
                                                   {mohammadreza.heidari-iman, giorgio.di-natale, katell.morin-allory}@univ-grenoble-alpes.fr


                                          Abstract—Functional verification increasingly relies on         While each verification approach offers distinct advantages,
                                        Assertion-Based Verification (ABV), which has become a key        they also face challenges, such as scalability issues in formal
                                        approach for verifying hardware designs due to its efficiency     methods and a lack of exhaustiveness in simulation-based
                                        and effectiveness. Central to ABV are automatic assertion
                                        miners, which apply different techniques to generate assertions   techniques [21, 24, 25].
                                        automatically. This paper reviews the most recent, advanced,         While formal and simulation-based verification tech-
arXiv:2601.02248v1 [cs.SE] 5 Jan 2026




                                        and widely adopted assertion miners, offering a comparative       niques show significant potential, assertion-based verifica-
                                        analysis of their methodologies. The goal is to provide re-       tion has gained traction as a widely adopted method for
                                        searchers and verification practitioners with insights into the
                                        capabilities and limitations of existing miners. By identifying
                                                                                                          verifying complex digital systems. ABV leverages the advan-
                                        their shortcomings, this work also points toward directions for   tages of both formal and simulation-based approaches to
                                        developing more powerful and advanced assertion miners in         ensure design correctness [26–32]. This technique can be
                                        the future.                                                       applied at multiple levels of verification abstraction, ranging
                                          Index Terms—verification, assertion-based verification, auto-   from high-level assertions embedded in transaction-level
                                        matic assertion mining, automatic assertion miners, assertion
                                                                                                          testbenches to low-level assertions synthesized directly into
                                                                I. I NTRODUCTION                          hardware implementations [9, 26, 33–35]. The effectiveness
                                                                                                          of assertion-based verification primarily depends on the
                                           Embedded systems and microelectronic components are
                                                                                                          quality of the assertions themselves. These assertions are
                                        employed in a wide range of devices and industries, includ-
                                                                                                          regarded as valid and accurate rules that describe the
                                        ing automotive and medical sectors, as well as in general
                                                                                                          behavior and functionality of designs, which the designs
                                        safety-critical applications [1, 2]. Ensuring the correctness
                                                                                                          must adhere to [28, 36, 37].
                                        of the functionality of these systems is crucial, as any
                                                                                                             Assertion-based verification integrates elements of both
                                        failure could lead to disastrous consequences, ranging from
                                                                                                          formal verification and simulation-based verification, pro-
                                        financial or ecological harm to, in some cases, death or
                                                                                                          viding a more efficient and effective method for veri-
                                        serious injury [2–4]. One approach to preventing such
                                                                                                          fying complex digital systems [9]. This approach relies
                                        disasters in embedded systems is functional verification.
                                                                                                          on assertions, which are Boolean expressions that define
                                           Functional verification techniques aim to ensure that a
                                                                                                          the expected behavior of a design and must remain true
                                        hardware design behaves in accordance with the specified
                                                                                                          throughout its execution [38]. Within the scope of assertion-
                                        set of requirements outlined in its specification [5, 6]. As
                                                                                                          based verification, assertions can be defined through two
                                        hardware designs continue to grow in size and complexity,
                                                                                                          main methods: manual assertion generation and automated
                                        verification has become a critical component of modern de-
                                                                                                          assertion mining [17, 39, 40].
                                        sign flows [7, 8]. Today, approximately 51% of the total cost
                                        and time in the design process is allocated to verification          Manual definition of assertions demands substantial hu-
                                        [9].                                                              man expertise and a deep understanding of the design’s
                                           To advance functional verification techniques, it is essen-    functionality [17, 38, 41, 42]. This process is often costly,
                                        tial to explore and comprehend the various methodologies          time-intensive, and prone to errors [41, 43, 44]. To address
                                        employed in this domain. These include static verification        these challenges, significant efforts have been made to
                                        methods, often referred to as formal verification [10–14], dy-    automate assertion mining [28, 45–57]. These automated
                                        namic approaches, commonly known as simulation-based              tools employ various techniques, such as constructing Fi-
                                        verification techniques [15–17], and semi-formal strategies,      nite State Machines (FSMs) [28] or leveraging data mining
                                        widely recognized as assertion-based verification meth-           algorithms [58–60], to generate assertions without human
                                        ods [9, 18–20]. Formal verification focuses on ensuring           intervention. Despite their potential, automated assertion
                                        functional correctness through rigorous proofs rather than        miners still face several limitations. One major issue is their
                                        simulations [21]. This category encompasses techniques like       inability to produce assertion sets that comprehensively
                                        model checking, theorem proving, and equivalence check-           cover all aspects of design behavior, including corner cases.
                                        ing [21]. On the other hand, simulation-based verification        This lack of comprehensive coverage can lead to assertion
                                        evaluates design behavior through simulations, verifying its      sets that fail to capture the complete range of design
                                        correctness within the simulated environment [16, 22, 23].        behaviors. Additional shortcomings of current assertion
                                                                                                          miners include the generation of excessive assertions, re-
                                         * Institut National Polytechnique Grenoble Alpes                 dundancy (i.e., assertions that describe the same design
behavior), inconsistency (i.e., assertions that conflict with    A. GoldMine [46]
one another), lengthy execution times for assertion mining,         GoldMine is an automated tool designed to generate
and lack of readability of the generated assertions [61, 62].    assertions for RTL designs. Its methodology involves gener-
These issues collectively increase the risk of making the        ating simulation data, mining assertions using a decision
verification process more error-prone, time-consuming, and       tree algorithm, and verifying them formally. It employs
expensive.                                                       static analysis techniques, such as cone-of-influence anal-
   The automatic mining of assertions for digital designs        ysis, to narrow the focus to causal variables, improving
has been extensively explored in the literature. The study       the relevance of generated assertions. GoldMine adapts
in [47] introduced an assertion miner that uses dynamic          its approach through various configuration options like
dependency graphs to identify signal relationships within        sampling strategies and reset signal frequency to handle
a design and generate corresponding assertions. In [48],         combinational and sequential modules. The tool was eval-
a syntax-guided enumeration approach was proposed for            uated on the Rigel RTL design, demonstrating its capability
assertion mining. The technique presented in [28] leverages      to capture both simple and complex design behaviors, in-
predefined templates in the form of finite state machines        cluding temporal relationships across multiple logic levels.
to extract assertions. HARM is a hint-based assertion miner      In the following, we briefly provide the key strengths and
that utilizes simulation traces to generate Linear Tempo-        limitations of GoldMine:
ral Logic (LTL) assertions [54]. The extended version of            Key Strengths:
HARM incorporates a clustering algorithm to refine the
                                                                    ● Automation: GoldMine reduces manual effort by au-
mined assertion sets [55]. GoldMine, introduced in [46],
                                                                       tomating the assertion generation process, covering
employs formal verification and static code analysis to de-
                                                                       large design spaces efficiently.
rive assertions for Register-Transfer Level (RTL) designs. The
                                                                    ● Complexity Handling: It captures deep temporal and
method proposed in [53] focuses on extracting assertions by
                                                                       combinational relationships, providing insights into
converting sequential designs into pseudo-combinational
                                                                       unintentional but valid design behaviors.
designs. Additionally, ARTmine, a recent advancement in
                                                                    ● Design Coverage: Its assertions uncover unexplored
automatic assertion mining, employs specifically designed
                                                                       regions of the design, contributing to improved regres-
data mining techniques and algorithms to generate asser-
                                                                       sion test quality.
tion sets [41].
   Therefore, this manuscript builds upon our previously            Limitations and Areas for Improvement:
published survey [63], providing a revised and stream-              ● Dependence on Simulation Data: The quality of asser-
lined presentation focused on conceptual foundations and               tions heavily relies on diverse and high-quality simu-
methodologies in automatic assertion miners. The main                  lation data, which may not always be available.
contributions are summarized as follows:                            ● Heuristic Reliance: When decision-making in the as-
                                                                       sertion mining process is inconclusive, heuristics are
  ● We   present an analytical study and comparison of
                                                                       used, which can lead to trivial or irrelevant assertions.
    the most well-known and recent automatic assertion
                                                                    ● Handling Temporal Properties: Sequential behaviors
    miners.
                                                                       require significant methodological fine-tuning, limiting
  ● This study summarizes the strengths and limitations of
                                                                       its out-of-the-box applicability for complex temporal
    state-of-the-art automatic assertion miners, providing
                                                                       relationships.
    insights for researchers and engineers in the field of
                                                                    ● Over-Constrained Assertions: Some assertions, while
    verification to better enhance future generations of
                                                                       correct, may be too trivial or restrictive to add practical
    assertion miners by addressing their shortcomings and
                                                                       value.
    to aid in selecting the most appropriate miners for
                                                                    ● Limited Support for Non-Verilog/RTL Designs: Gold-
    their work.
                                                                       Mine is limited to working with Verilog designs and
  The paper is organized as follows: Section II provides               does not support SystemVerilog. Additionally, it can
a description of the most advanced automatic assertion                 only mine assertions from designs in RTL format,
miners, and Section III concludes the paper.                           meaning it cannot mine assertions for hardware de-
                                                                       signs implemented in the gate-level format.
            II. AUTOMATIC A SSERTION M INERS                     In conclusion, GoldMine’s ability to automate assertion
                                                                 generation and uncover unexplored design behaviors makes
   In this section, we provide detailed descriptions of the      it a valuable tool for early-stage RTL verification. However,
most commonly used and well-known automatic assertion            future research should address its limitations, particularly
miners by researchers in the field. The goal is to highlight     in improving the handling of temporal complexity, reducing
their strengths and shortcomings, offering insights into         dependence on simulation data, and refining its decision-
the limitations of current assertion miners and paving the       making processes, to make it more robust and efficient.
way for addressing these issues in future generations of
automatic assertion miners. The strengths and limitations        B. DDG [47]
discussed in this paper are not solely derived from the             This assertion miner leverages Dynamic Dependency
existing literature on assertion miners, but also from our       Graphs (DDGs) to describe the relationships between sig-
hands-on experience working directly and indirectly with         nals in a hardware design and automatically generate
these tools and their generated assertions over several years    properties. The methodology involves first generating DDGs
of research in this field.                                       from a set of use cases, followed by extracting initial
properties from these graphs. After applying refinement and      constrained by fixed patterns. A-TEAM follows a three-
abstraction steps, general properties are created, which are     step methodology: (1) generate candidate assertions using
then verified using a model-checker. This approach aims          execution traces and templates, (2) evaluate assertions by
to automatically identify relevant properties with minimal       injecting testable faults and measuring their fault cover-
use case data. In the following, we briefly provide the key      age, and (3) minimize the assertion set using an Integer
strengths and limitations of DDG:                                Linear Programming (ILP)-based approach to retain only
   Key Strengths:                                                assertions that maximize coverage. The result is a concise
  ● Efficient Use Case Requirements: The method is effec-        set of assertions that effectively capture DUV behaviors.
    tive even with minimal simulation data. As few as one        In the following, we briefly provide the key strengths and
    use case can be sufficient to generate useful properties,    limitations of A-TEAM:
    which contrasts with other methods that may require             Key Strengths:
    extensive simulation runs.                                      ● Customizable and Flexible Mining: The use of user-
  ● Word-Level Properties: By utilizing DDGs, the ap-                 defined templates enables A-TEAM to explore diverse
    proach can generate detailed, word-level properties               assertion patterns beyond pre-defined structures, mak-
    using a variety of operators. This offers more flexibility        ing it adaptable to various abstraction levels.
    and precision in capturing signal relationships.                ● Compact Assertions with High Coverage: A-TEAM pro-
  ● Generalization of Properties: The refinement and ab-              duces fewer but more compact assertions, achieving
    straction steps enable the creation of generalized prop-          higher fault coverage compared to decision-tree-based
    erties that are not tied to specific simulation data,             miners.
    making them broadly applicable across different design          ● Wide Applicability: A-TEAM can operate on execution
    scenarios.                                                        traces from different DUV abstraction levels, increasing
  ● Redundancy and Inconsistency: Our limited access                  its scope of application.
    to the generated assertions of this miner for some              ● Design Behavior Coverage: Our limited access to the
    benchmarks suggests that DDG is one of the best at                generated assertions of this miner for a few bench-
    minimizing redundant and inconsistent assertions.                 marks showed that, although the miner does not offer
                                                                      as high a design behavior coverage as newer genera-
Limitations and Areas for Improvement:
                                                                      tions of miners, it still provides competitive coverage.
  ● Scalability: As the design size increases, the complexity
                                                                    Limitations and Areas for Improvement:
    of extracting and processing properties from DDGs
                                                                    ● High Computational Overhead: The ILP-based mini-
    may lead to longer processing times, potentially mak-
    ing the method less efficient for large designs.                  mization and antecedent justification significantly in-
  ● Internal State Exploration: The method primarily fo-
                                                                      crease execution time, often exceeding that of simpler
    cuses on observable output signals and their relation-            approaches.
                                                                    ● Reliance on User-Defined Templates: The miner’s effec-
    ships, which may limit its ability to generate useful
    properties for internal signal states. Expanding the              tiveness depends heavily on the quality of templates,
    scope to include these internal states would improve              requiring substantial user expertise to achieve optimal
    its applicability for more complex designs. Our lim-              results.
                                                                    ● Limited Temporal Exploration: While A-TEAM supports
    ited access to the generated assertions for specific
    benchmarks showed that the design behavior coverage               multiple temporal templates, its ability to capture
    provided by this miner is considerably lower compared             complex temporal dependencies could be further en-
    to other miners.                                                  hanced.
                                                                    ● Scalability Challenges: The computational demands
  ● Model-Checker Bottleneck: The reliance on model-
    checking to verify properties may introduce a bottle-             and heuristic-based decision-making may struggle to
    neck, especially when dealing with large designs or a             scale efficiently for large and complex DUVs.
    high volume of generated properties.                         In conclusion, A-TEAM is a versatile and effective assertion
                                                                 mining tool that outperforms traditional approaches in
In conclusion, the property mining approach using Dy-
                                                                 coverage and compactness of mined assertions. However, its
namic Dependency Graphs offers an efficient and flexible
                                                                 reliance on user expertise, high execution time, and limited
way to generate useful properties with minimal simula-
                                                                 exploration of complex temporal behaviors present oppor-
tion data. While it excels in creating word-level properties
                                                                 tunities for future research to enhance its scalability, reduce
and generalizing across use cases, challenges remain in
                                                                 its computational demands, and increase its automation in
scalability, internal state analysis, and verification speed.
                                                                 assertion generation.
Addressing these challenges will enhance the approach’s
utility for a broader range of hardware verification tasks.      D. HARM [54]
                                                                   HARM (Hint-based Assertion Miner) and its extended
C. A-TEAM [28]                                                   version [55], which can be considered an enhanced version
   A-TEAM is an assertion mining tool designed to extract        of A-TEAM, are robust, template-driven assertion mining
assertions from execution traces of the design under ver-        tools designed for hardware verification. HARM methodol-
ification across various abstraction levels, including TLM,      ogy revolves around leveraging user-defined templates to
RTL, and gate-level designs. It is template-driven, allowing     mine assertions efficiently and flexibly from input traces.
users to define custom templates to guide assertion gener-       By utilizing a three-level parallelization strategy, customiz-
ation, making it more versatile than conventional miners         able ranking metrics, and filtering mechanisms, HARM
achieves significant computational speed and scalability.          In conclusion, HARM is a powerful and efficient tool
Furthermore, the miner allows users to define domain-              for hint-based assertion mining in hardware verification.
specific metrics for scoring and ranking assertions, tailoring     Its template-driven methodology, three-level paralleliza-
its outputs to context-specific needs. In the following, we        tion, and context-aware ranking mechanisms position it
briefly provide the key strengths and limitations of HARM:         as a competitive miner in the field. However, its reliance
   Key Strengths:                                                  on user-defined templates, the complexity of metric cal-
   ● Customizable and Flexible Methodology: HARM’s                 ibration, and its computational demands highlight areas
     template-based approach allows users to tailor the            where further research could improve its usability and
     mining process to specific domains, ensuring the rel-         performance. Addressing these limitations—such as re-
     evance of the generated assertions to the verification        ducing template dependency, automating metric tuning,
     context.                                                      and broadening the exploration of non-template asser-
   ● Highly Parallelized Algorithms: The three-level paral-        tions—would make HARM more accessible and versatile,
     lelization strategy (across evaluation units, template        paving the way for advancements in assertion mining
     permutations, and templates) fully exploits CPU cores,        methodologies.
     achieving substantial speed-ups, particularly for large
     datasets.                                                     E. ARTmine [41]
   ● User-Defined Context-Aware Metrics: HARM empowers
     users to define metrics for filtering and ranking asser-         ARTmine is an automatic assertion miner designed to
     tions, providing fine-grained control over the results.       generate temporal assertion sets for hardware verification.
     This makes it adaptable to various verification needs         The core methodology of ARTmine revolves around data
     and scenarios.                                                mining algorithms designed for mining association rules
   ● Scalability and Efficiency: Experimental results demon-       from simulation traces of hardware designs, with the goal of
     strate that HARM scales effectively with input size and       identifying critical design behaviors. These mined associa-
     outperforms state-of-the-art miners in terms of both          tion rules are then transformed into temporal assertions for
     speed and assertion quality.                                  verification. The mining process is designed to be both effi-
   ● Security Context: Our experiments utilizing HARM’s as-        cient and effective, with a specific focus on corner cases by
     sertions in the context of security and Hardware Trojan       adjusting the parameters of the miner. This ensures the tool
     detection demonstrate its significant applicability in        generates a minimal but highly relevant and accurate set of
     detecting Hardware Trojans.                                   assertions. ARTmine has demonstrated strong capabilities
   Limitations and Areas for Improvement:                          in mutant detection and assertion generation, particularly
                                                                   when compared to other assertion mining tools like HARM
   ● Template Dependency: While the template-based ap-
                                                                   and GoldMine. In the following, we briefly provide the key
     proach provides flexibility, it also introduces a de-
                                                                   strengths and limitations of ARTmine:
     pendency on the user’s ability to define meaningful
     templates. Ineffective or incomplete templates may               Key Strengths:
     result in suboptimal or irrelevant assertions.                  ● Efficient Assertion Generation: ARTmine is designed
   ● Metric Calibration Complexity: The ranking system,                to generate a minimal number of assertions that are
     while flexible, requires users to select from numerous            highly relevant and effective for verification. By focus-
     calibrate function configurations. This complexity may            ing on corner cases and using a controlled approach
     pose challenges for less experienced users and could              with configurable parameters in the tool, ARTmine
     benefit from automated or guided metric tuning.                   avoids the overgeneration of assertions. This is crucial
   ● Limited Exploration of Unknown Assertions: HARM’s                 in preventing the verification process from becoming
     reliance on templates inherently limits its ability to dis-       overwhelmed by unnecessary assertions, which is often
     cover assertions outside the predefined template scope,           a limitation in other assertion miners.
     potentially missing novel or unexpected behaviors.              ● Effective Mutant Detection: ARTmine has shown supe-
   ● Ranking Bias: The ranking formula gives higher weight             rior performance in detecting injected mutants. This
     to assertions that score well across all metrics but pe-          highlights its ability to identify significant design be-
     nalizes assertions with low scores in any single metric.          haviors that may not be captured by traditional as-
     While effective for filtering poor-quality assertions, this       sertion mining techniques. The tool’s focus on cor-
     may undervalue assertions with unique but isolated                ner cases further enhances its detection capabilities,
     strengths.                                                        making it particularly valuable in the verification of
   ● Evaluation Limited to Traces: HARM’s methodology                  complex hardware systems.
     evaluates assertions solely on the given input trace(s).        ● Scalability: ARTmine is capable of effectively handling
     This limits its applicability in scenarios where traces           large-scale designs. The tool can efficiently process
     are incomplete or do not fully represent the system’s             simulation traces and generate assertions, even for
     behavior.                                                         designs with a large number of components. This scal-
   ● High Number of Generated Assertions: Our experimen-               ability is a significant advantage for applying ARTmine
     tal analysis reveals that HARM generates a significantly          to real-world hardware verification tasks.
     higher number of assertions than all other miners,              ● Support for Temporal Patterns: ARTmine’s support for
     without necessarily offering better design behavior               a variety of temporal patterns, allows it to handle a
     coverage. This can potentially lead to a lengthier veri-          wide range of verification requirements. This flexibility
     fication process.                                                 makes ARTmine applicable to a diverse set of design
    scenarios, from simple to more complex verification                                   A CKNOWLEDGEMENT
    tasks.
  ● Security Context: Our experimental analysis of ART-            This work is partially funded by the “Resilient Trust”
    mine’s assertions in the realm of security and Hardware      project of the EU’s Horizon Europe research and innovation
    Trojan detection highlights its strong applicability in      programme under grant agreement No. 101112282.
    identifying Hardware Trojans.
                                                                                               R EFERENCES
  Limitations and Areas for Improvement:
  ● Limited   Temporal Pattern Support: While ARTmine             [1] S. K. Jena and M. Srinivas, “On the suitability of multi-core processing
                                                                      for embedded automotive systems,” in 2012 International Conference
    supports several key temporal patterns, its scope is              on Cyber-Enabled Distributed Computing and Knowledge Discovery,
    limited to specific predefined patterns. Other temporal           2012, pp. 315–322.
    patterns commonly found in hardware verification, are         [2] M. R. H. Iman and P. Yaghmaie, “A software control flow checking
                                                                      technique in multi-core processors,” International Journal of Embed-
    not directly supported in the current implementation.             ded Systems, vol. 13, no. 2, pp. 136–147, 2020.
    Extending ARTmine to handle a wider range of tempo-           [3] C. E. Salloum, M. Elshuber, O. Höftberger et al., “The across mpsoc – a
    ral patterns could further enhance its applicability and          new generation of multi-core processors designed for safety-critical
                                                                      embedded systems,” in 2012 15th Euromicro Conference on Digital
    make it more versatile for various hardware verification          System Design, 2012, pp. 105–113.
    scenarios.                                                    [4] D. Zuccala, S. Hon, M. R. H. Iman et al., “Formal analysis of
  ● Data Mining Thresholds: ARTmine is designed to han-               fault propagation in complex digital systems,” in Proceedings of the
    dle corner cases effectively, but the tool’s reliance on          International Symposium on Formal Methods and Models for System
                                                                      Design, ser. MEMOCODE ’25. New York, NY, USA: Association
    predefined data mining thresholds could lead to the               for Computing Machinery, 2026, p. 67–71. [Online]. Available:
    exclusion of some important but rare design behaviors.            https://doi.org/10.1145/3742875.3754691
  ● Scalability Challenges for Extremely Large Designs:           [5] T. Kropf, Introduction to Formal Hardware Verification: Methods and
                                                                      Tools for Designing Correct Circuits and Systems, 1st ed. Berlin,
    Although ARTmine demonstrates good scalability with               Heidelberg: Springer-Verlag, 1999.
    medium-to-large designs, it may face challenges when          [6] M. R. H. Iman, Advanced Techniques for Assertion-Based Verification
    applied to extremely large designs with significantly             in Hardware Designs Using Data Mining Algorithms, 1st ed. Cham:
                                                                      Springer Nature Switzerland, 2025.
    more I/O or state variables for one of its predefined         [7] W. Chen, S. Ray, M. Abadir et al., “Challenges and trends in modern
    temporal templates. As the number of variables in-                SoC design verification,” IEEE Design & Test, vol. PP, pp. 1–1, 08 2017.
    creases, the number of mined assertions and their             [8] M. R. Heidari Iman, Automatic Generation of Assertions for Functional
                                                                      Verification. Cham: Springer Nature Switzerland, 2025, pp. 27–43.
    associated computational overhead may grow expo-
                                                                  [9] H. Witharana, Y. Lyu, S. Charles et al., “A survey on assertion-based
    nentially. Optimizing the underlying algorithms to bet-           hardware verification,” ACM Computing Surveys (CSUR), vol. 54, no.
    ter scale with extremely large designs would make                 11s, pp. 1–33, 2022.
    ARTmine more applicable to cutting-edge hardware             [10] T. Grimm, D. Lettnin, and M. Hübner, “A survey on formal verification
                                                                      techniques for safety-critical systems-on-chip,” Electronics, vol. 7,
    systems, especially in the context of modern System-              no. 6, p. 81, 2018.
    on-Chips (SoCs) and extremely large designs.                 [11] D. Große, G. Fey, and R. Drechsler, “Enhanced formal verification flow
                                                                      for circuits integrating debugging and coverage analysis,” Electronic
   In conclusion, ARTmine is a strong and efficient auto-             Communications of the EASST, vol. 62, 2013.
matic assertion miner that excels in generating temporal         [12] R. Drechsler and G. Fey, “Formal verification meets robustness check-
                                                                      ing—techniques and challenges,” in Proc. of the 13th IEEE Symposium
assertions for hardware verification. Its ability to handle           on Design and Diagnostics of Electronic Circuits and Systems. IEEE,
a variety of temporal patterns, detect mutants with fewer             2010, pp. 4–4.
assertions compared to other miners, and scale to large          [13] H. Riener and G. Fey, “Faust: A framework for formal verification,
                                                                      automated debugging, and software test generation,” in Proc. of
designs makes it a valuable tool for hardware verification            the International SPIN Workshop on Model Checking of Software.
tasks. However, it does have certain limitations, such as the         Springer, 2012, pp. 234–240.
restricted set of supported temporal patterns and reliance       [14] G. Fey, “Assessing system vulnerability using formal verification tech-
                                                                      niques,” in Proc. of the International Doctoral Workshop on Math-
on predefined thresholds. These limitations present oppor-            ematical and Engineering Methods in Computer Science. Springer,
tunities for future research to extend ARTmine’s capabilities,        2011, pp. 47–56.
improve its handling of complex behaviors, and enhance its       [15] H. Rostami, M. Hosseini, A. Azarpeyvand et al., “Automatic high func-
scalability for next-generation hardware systems. With fur-           tional coverage stimuli generation for assertion-based verification,”
                                                                      in 2024 IEEE 30th International Symposium on On-Line Testing and
ther improvements in these areas, ARTmine could become                Robust System Design (IOLTS), 2024, pp. 1–7.
a powerful tool for comprehensive and efficient hardware         [16] M. Loghi, T. Margaria, G. Pravadelli et al., “Dynamic and formal ver-
verification across a wide range of design environments.              ification of embedded systems: A comparative survey,” International
                                                                      Journal of Parallel Programming, vol. 33, pp. 585–611, 2005.
                                                                 [17] M. R. Heidari Iman, Enhancing Assertion-Based Verification in
                                                                      Hardware Designs through Data Mining Algorithms. TalTech
                     III. C ONCLUSION                                 Press, 2024, serial number: 37/2024. [Online]. Available:
                                                                      https://doi.org/10.23658/taltech.37/2024
                                                                 [18] K. Datta and P. P. Das, “Assertion based verification using HDVL,” in
   In this paper, we surveyed and analyzed the most well-             Proc. of the 17th International Conference on VLSI Design. Proceedings.
known and widely used automatic assertion miners to                   IEEE, 2004, pp. 319–325.
                                                                 [19] Y. Li, W. Wu, L. Hou et al., “A study on the assertion-based verification
better explore their strengths and weaknesses. Our analysis           of digital IC,” in Proc. of the 2009 Second International Conference on
highlighted their pros and cons, emphasizing the current              Information and Computing Science, vol. 2. IEEE, 2009, pp. 25–28.
limitations of state-of-the-art automatic assertion miners.      [20] K. Alatoun, B. Shankaranarayanan, S. M. Achyutha et al., “SoC trust
By focusing on these limitations, we aimed to guide future            validation using assertion-based security monitors,” in Proc. of the
                                                                      2021 22nd International Symposium on Quality Electronic Design
improvements in automatic assertion miners, ultimately                (ISQED). IEEE, 2021, pp. 496–503.
enhancing the functional verification of hardware designs.       [21] R. Drechsler, Advanced formal verification. Springer, 2004.
[22] G. Fey and R. Drechsler, “Improving simulation-based verification         [44] M. R. Heidari Iman, Automatic Generation of Assertions for Security
     by means of formal methods,” in Proc. of the ASP-DAC 2004: Asia                Verification. Cham: Springer Nature Switzerland, 2025, pp. 69–93.
     and South Pacific Design Automation Conference 2004 (IEEE Cat.            [45] S. Hertz, D. Sheridan, and S. Vasudevan, “Mining hardware assertions
     No.04EX753), 2004, pp. 640–643.                                                with guidance from static analysis,” IEEE Transactions on Computer-
[23] N. Bombieri, F. Fummi, and G. Pravadelli, “Hardware design and sim-            Aided Design of Integrated Circuits and Systems, vol. 32, no. 6, pp.
     ulation for verification,” in Formal Methods for Hardware Verification,        952–965, 2013.
     M. Bernardo and A. Cimatti, Eds. Berlin, Heidelberg: Springer Berlin      [46] S. Vasudevan, D. Sheridan, S. Patel et al., “Goldmine: automatic
     Heidelberg, 2006, pp. 1–29.                                                    assertion generation using data mining and static analysis,” in DATE,
[24] L. Zhao, S. Chen, and Y. Wang, “Simulation-based hardware                      2010, pp. 626–629.
     verification with a graph-based specification,” Mathematical              [47] J. Malburg, T. Flenker, and G. Fey, “Property mining using dynamic
     Problems in Engineering, vol. 2018, p. 10, 2018. [Online].                     dependency graphs,” in ASP-DAC, Jan 2017, pp. 244–250.
     Available: https://www.proquest.com/scholarly-journals/simulation-        [48] G. Martino and G. Fey, “Syntax-guided enumeration of temporal
     based-hardware-verification-with-graph/docview/2002921501/se-2                 properties,” in 2019 FDL, 2019, pp. 1–8.
[25] A. Kamkin and M. Chupilko, “Survey of modern technologies of              [49] M. Soeken, U. Kühne, M. Freibothe et al., “Automatic property
     simulation-based verification of hardware,” Programming and Com-               generation for the formal verification of bus bridges,” in Proc. of
     puter Software, vol. 37, pp. 147–152, 05 2011.                                 the 14th IEEE International Symposium on Design and Diagnostics
[26] H. Sohofi and Z. Navabi, “Assertion-based verification for system-             of Electronic Circuits and Systems, 2011, pp. 417–422.
     level designs,” in Proc. of the Fifteenth International Symposium on      [50] J. Malburg, T. Flenker, and G. Fey, “Generating good properties from
     Quality Electronic Design. IEEE, 2014, pp. 582–588.                            a small number of use cases,” in Proc. of the IEEE International
[27] S. Lammermann, J. Ruf, T. Kropf et al., “Towards assertion-based               Verification and Security Workshop, 07 2016.
     verification of heterogeneous system designs,” in Proc. of the 2010       [51] F. Rogin, T. Klotz, G. Fey et al., “Advanced verification by automatic
     Design, Automation & Test in Europe Conference & Exhibition (DATE              property generation,” IET Comput. Digit. Tech., vol. 3, no. 4,
     2010). IEEE, 2010, pp. 1171–1176.                                              pp. 338–353, 2009. [Online]. Available: https://doi.org/10.1049/iet-
[28] A. Danese, N. D. Riva, and G. Pravadelli, “A-TEAM: Auto-                       cdt.2008.0110
     matic template-based assertion miner,” in Proc. of the 2017 54th          [52] ——, “Automatic generation of complex properties for hardware
     ACM/EDAC/IEEE Design Automation Conference (DAC), 2017, pp. 1–6.               designs,” in Proc. of the Conference on Design, Automation and
[29] S. Germiniani, “A complete assertion-based verification framework              Test in Europe, ser. DATE ’08. New York, NY, USA: Association
     from the edge to the cloud,” Ph.D. dissertation, University of Verona,         for Computing Machinery, 2008, p. 545–548. [Online]. Available:
     Verona, Italy, 2023.                                                           https://doi.org/10.1145/1403375.1403506
[30] L. Pierre, F. Pancher, R. Suescun et al., “On the effectiveness of        [53] M. R. Heidari Iman, J. Raik, M. Jenihhin et al., “A methodology for
     assertion-based verification in an industrial context,” in Formal              automated mining of compact and accurate assertion sets,” in 2021
     Methods for Industrial Critical Systems, C. Pecheur and M. Dierkes,            IEEE Nordic Circuits and Systems Conference (NorCAS), 2021, pp. 1–7.
     Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2013, pp. 78–93.     [54] S. Germiniani and G. Pravadelli, “HARM: A hint-based assertion
[31] P. Yeung and K. Larsen, “Practical assertion-based formal verification         miner,” IEEE Transactions on Computer-Aided Design of Integrated
     for SoC designs,” in Proc. of the 2005 International Symposium on              Circuits and Systems, vol. 41, no. 11, pp. 4277–4288, 2022.
     System-on-Chip, 2005, pp. 58–61.                                          [55] ——, “Exploiting clustering and decision-tree algorithms to mine
[32] P. Gurha and R. R. Khandelwal, “Systemverilog assertion based veri-            ltl assertions containing non-boolean expressions,” in Proc. of the
     fication of AMBA-AHB,” in Proc. of the 2016 International Conference           2022 IFIP/IEEE 30th International Conference on Very Large Scale
     on Micro-Electronics and Telecommunication Engineering (ICMETE),               Integration (VLSI-SoC), 2022.
     2016, pp. 641–645.                                                        [56] S. Vasudevan, L. Liu, and S. Hertz, A Comparative Study of Assertion
[33] A. M. Gharehbaghi, B. H. Yaran, S. Hessabi et al., “An                         Mining Algorithms in GoldMine.          Cham: Springer International
     assertion-based      verification   methodology      for  system-level         Publishing, 2019, pp. 609–645.
     design,” Computers & Electrical Engineering, vol. 33, no. 4,              [57] D. Sheridan, L. Liu, and S. Vasudevan, “Goldmine : Automatic asser-
     pp. 269–284, 2007, hardware/Software System on Chip                            tion generation and coverage closure in design validation,” 2011.
     Co-design: Approach and Application. [Online]. Available:                 [58] M. R. H. Iman, P. Chikul, G. Jervan et al., “Anomalous file system
     https://www.sciencedirect.com/science/article/pii/S0045790607000201            activity detection through temporal association rule mining,” in 9th
[34] B. Niemann and C. Haubelt, “Assertion-based verification                       ICISSP,, 2023, pp. 733–740.
     of transaction level models,” in Proc. of the Methoden                    [59] A. Roberts, M. R. Heidari Iman, M. Bellone et al., “ADAssure: De-
     und Beschreibungssprachen zur Modellierung und Verifikation                    bugging methodology for autonomous driving control algorithms,”
     von Schaltungen und Systemen, 2006. [Online]. Available:                       in 2024 Design, Automation & Test in Europe Conference & Exhibition
     https://api.semanticscholar.org/CorpusID:16944153                              (DATE), 2024, pp. 1–6.
[35] A. Habibi, S. Tahar, A. Samarah et al., “Efficient assertion based        [60] M. Shahin, M. Bertl, M. R. H. Iman et al., “Significant factors
     verification using TLM,” in Proc. of the Design, Automation & Test             extraction: A combined logistic regression and apriori association
     in Europe Conference, vol. 1, 2006, pp. 1–6.                                   rule mining approach,” in Machine Learning Methods in Systems,
[36] M. R. Heidari Iman, R. Drechsler, C. K. Jha et al., “Special session           R. Silhavy and P. Silhavy, Eds. Cham: Springer Nature Switzerland,
     paper: Application of functional verification techniques in hardware           2024, pp. 295–311.
     trust,” in 2025 IEEE International Symposium on Defect and Fault          [61] M. R. Heidari Iman, J. Raik, G. Jervan et al., “IMMizer: An innovative
     Tolerance in VLSI and Nanotechnology Systems (DFT), 2025, pp. 1–8.             cost-effective method for minimizing assertion sets,” in Proc. of the
[37] M. R. H. Iman, S. Ahmadi-Pour, R. Drechsler et al., “Processor                 2022 25th Euromicro Conference on Digital System Design (DSD), 2022,
     vulnerability detection with the aid of assertions: RISC-V case study,”        pp. 1–8.
     in 2024 IEEE Nordic Circuits and Systems Conference (NorCAS), 2024,       [62] M. R. Heidari Iman, J. Raik, M. Jenihhin et al., “An automated
     pp. 1–7.                                                                       method for mining high-quality assertion sets,” Microprocessors and
[38] M. Boulé and Z. Zilic, Generating Hardware Assertion Checkers: For             Microsystems, vol. 97, p. 104773, 2023.
     Hardware Verification, Emulation, Post-Fabrication Debugging and          [63] M. R. H. Iman, G. Di Natale, and K. Morin-Allory, “A survey on auto-
     On-Line Monitoring. Springer, 2008.                                            matic assertion miners,” in 2025 IEEE 28th International Symposium
                                                                                    on Design and Diagnostics of Electronic Circuits and Systems (DDECS),
[39] M. R. Heidari Iman, Automatic Evaluation and Minimization of
                                                                                    2025, pp. 55–60.
     Assertions. Cham: Springer Nature Switzerland, 2025, pp. 45–67.
[40] A. Danese, F. Filini, T. Ghasempouri et al., “Automatic generation
     and qualification of assertions on control signals: A time window-
     based approach,” in VLSI-SoC: Design for Reliability, Security, and
     Low Power, Y. Shin, C. Y. Tsui, J.-J. Kim et al., Eds. Cham: Springer
     International Publishing, 2016, pp. 193–221.
[41] M. R. Heidari Iman, G. Jervan, and T. Ghasempouri, “ARTmine: Auto-
     matic association rule mining with temporal behavior for hardware
     verification,” in 2024 Design, Automation & Test in Europe Conference
     & Exhibition (DATE), 2024, pp. 1–6.
[42] Property Generation. Dordrecht: Springer Netherlands, 2008, pp. 75–
     97.
[43] S. Katz, O. Grumberg, and D. Geist, “Have I written enough proper-
     ties? A method of comparison between specification and implemen-
     tation,” in ACM CHARME, 1999, pp. 280–297.
