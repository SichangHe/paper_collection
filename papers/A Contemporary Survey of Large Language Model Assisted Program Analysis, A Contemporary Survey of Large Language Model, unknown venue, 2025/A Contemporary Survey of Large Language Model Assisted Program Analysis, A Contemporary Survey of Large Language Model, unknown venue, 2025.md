                                                                                                                                                                     1



                                          A Contemporary Survey of Large Language Model
                                                    Assisted Program Analysis
                                                                   Jiayimei Wang, Tao Ni, Wei-Bin Lee, Qingchuan Zhao∗


                                           Abstract—The increasing complexity of software systems              systems, and exploitation of security loopholes in
                                        has driven significant advancements in program analysis,               sensitive government networks. Accordingly, many
                                        as traditional methods unable to meet the demands of mod-              techniques have been proposed to detect such vul-
                                        ern software development. To address these limitations,
                                                                                                               nerabilities that compromise software quality and
arXiv:2502.18474v1 [cs.SE] 5 Feb 2025




                                        deep learning techniques, particularly Large Language
                                        Models (LLMs), have gained attention due to their context-             reliability, and program analysis has been proven
                                        aware capabilities in code comprehension. Recognizing the              effective in such tasks. It aims to examine compter
                                        potential of LLMs, researchers have extensively explored               programs to identify or verify their properties to
                                        their application in program analysis since their intro-               detect vulnerabilities through abstract interpretation,
                                        duction. Despite existing surveys on LLM applications in               constraint solving, and automated reasoning [4].
                                        cybersecurity, comprehensive reviews specifically address-
                                        ing their role in program analysis remain scarce. In this                 However, as software complexity and scale in-
                                        survey, we systematically review the application of LLMs               crease, traditional program analysis methods en-
                                        in program analysis, categorizing the existing work into               counter challenges in meeting the demands of con-
                                        static analysis, dynamic analysis, and hybrid approaches.              temporary development. Specifically, these tradi-
                                        Moreover, by examining and synthesizing recent studies,                tional methods face substantial challenges in han-
                                        we identify future directions and challenges in the field.
                                        This survey aims to demonstrate the potential of LLMs
                                                                                                               dling dynamic behaviors, cross-language interac-
                                        in advancing program analysis practices and offer action-              tions, and large-scale codebases [5], [6]. Fortunately,
                                        able insights for security researchers seeking to enhance              recent advancements in machine learning have ini-
                                        detection frameworks or develop domain-specific models.                tiated a shift in program analysis [7] and shed light
                                          Keywords—Large Language Model, Program Analysis,                     on a promising research direction to address the
                                        Vulnerability Detection                                                limitations of traditional program analysis methods.
                                                                                                                  In particular, the literature has attempted to com-
                                                            I.    I NTRODUCTION                                bine deep learning with program analysis, applying
                                                                                                               it to strengthen the detection of vulnerabilities and
                                           With the continuous advancement of information                      achieve automated code fixes, thereby minimizing
                                        technology, software plays an increasingly signif-                     human intervention and increasing precision [8].
                                        icant role in daily life, making its quality and                       However, deep learning models lack the ability to
                                        reliability a critical concern for both academia and                   effectively integrate contextual information over
                                        industry [1]. This is because software vulnerabili-                    long sequences, limiting their performance in tasks
                                        ties in domains such as finance, healthcare, critical                  requiring deep reasoning or multi-turn understand-
                                        infrastructure, aerospace, and cybersecurity [2] can                   ing [9], [10]. Consequently, these models struggle
                                        lead to considerable financial losses or even societal                 to handle complex software and large codebases
                                        harm [3]. Examples include data breaches in finan-                     and lack the capability for cross-project analysis.
                                        cial systems, malfunctioning medical devices, dis-
                                        ruptions to power grids, failures in aviation control                     Fortunately, the most recent advancement, i.e.,
                                                                                                               large language model (LLM), has been found
                                           Jiayimei Wang, Tao Ni, and Qingchuan Zhao are with the              promising in addressing the limitations of early
                                        Department of Computer Science, City University of Hong                deep learning models, such as constrained con-
                                        Kong, Hong Kong SAR (e-mail: jwang2664-c@my.cityu.edu.hk,
                                        taoni2@cityu.edu.hk, cs.qczhao@cityu.edu.hk). Wei-Bin Lee is with      textual understanding and generalization, enabling
                                        the Information Security Center, Hon Hai Research Institute, Taipei,   them to handle tasks across multiple domains with
                                        Taiwan and the Department of Information Engineering and Com-          greater versatility [11]–[15]. Particularly, as for
                                        puter Science, Feng Chia University, Taichung, Taiwan (e-mail: wei-
                                        bin.lee@foxconn.com, wblee@fcu.edu.tw).                                program analysis, LLMs surpass traditional deep
                                           ∗
                                             The corresponding author.                                         learning methods and have been applied to various
                                                                                                                            2


                                                                                      Vulnerability Detection (§ III-A)
                                                                                        Malware Detection (§ III-B)
                                             LLM for Static Analysis (§ III)
                                                                                       Program Verification (§ III-C)
                                                                                    Static Analysis Enhancement (§ III-D)
                                                                                        Malware Detection (§ IV-A)
       LLM for Program Analysis             LLM for Dynamic Analysis (§ IV)                   Fuzzing (§ IV-B)
                                                                                        Penetration Testing (§ IV-C)
                                                                                        Unit Test Generation (§ V-A)
                                            LLM for Hybrid Approach (§ V)
                                                                                               Others (§ V-B)

                                      Fig. 1: Taxonomy of the survey.

tasks [16]–[20], including automated vulnerability            future research directions in § VI and conclude the
and malware detection, code generation and repair,            survey in § VII.
and providing scalable solutions that integrate static
and dynamic analysis methods. Moreover, it also                                II. BACKGROUND
shows a great potential to cope with the growing                In this section, we first introduce prior knowledge
difficulty of analyzing modern software systems.              about program analysis (§ II-A), including static
   Though promising, the literature lacks a com-              analysis and dynamic analysis and the limitations in
prehensive and systematica view of LLM-assisted               existing approaches, and then present the concepts
program analysis given the presence of numerous               of LLMs as well as the necesseity of leveraging
related attempts and applications. Therefore, this            LLMs for advancing program analysis (§ II-B).
work aims to systematically review the state-of-the-
art of LLM-assisted program analysis applications             A. Program Analysis
and specify its role in the development of program               Program analysis is the process of analyzing the
analysis. To this end, we systematically review the           behavior of computer programs to learn about their
use of LLMs in program analysis and organized                 properties [21]. Program analysis can find bugs or
them into a structured taxonomy. Figure 1 illustrates         security vulnerabilities, such as null pointer deref-
the classification framework, where the relevant re-          erences or array index out-of-bounds errors. It is
search is categorized into LLM for static analysis,           also used to generate software test cases, automate
LLM for dynamic analysis, and hybrid approach.                software patching and improve program execution
Unlike previous surveys that broadly examined the             speed through compiler optimization. Specifically,
applications of LLMs in cybersecurity, our work               program analysis can be categorized into two main
narrows its focus to program analysis, delivering             types: static analysis and dynamic analysis [22].
a more detailed and domain-specific exploration.              Static analysis examines a program’s code without
In addition, we collect the limitations mentioned             execution, dynamic analysis collects runtime infor-
in selected studies and analyze the improvements              mation through execution, and hybrid analysis com-
brought by the integration of LLMs, and specify the           bines both approaches for comprehensive results.
potential challenges and future research directions of           Static Analysis. Static analysis (a.k.a. compile-
LLMs in this domain.                                          time analysis) is a program analysis approach
   The survey is organized as follows. We first               that identifies program properties by examining its
introduce the background of program analysis and              source code without executing the program. The
large language model in § II. We then examine the             pipeline for static analysis consists of key stages
application of LLMs in static analysis in § III and           illustrated in Figure 2. The process begins with
discusses the use of LLMs in dynamic analysis in              parsing the code to extract essential structures and
§ IV. We next explore how LLMs assist hybrid                  relationships, which are transformed into interme-
approaches that combine static and dynamic analysis           diate representations (IRs) such as symbol tables,
in § V. We finally address the challenges of applying         abstract syntax trees (ASTs), control flow graphs
LLMs to program analysis and outline potential                (CFGs), and data flow graphs (DFGs). These IRs are
                                                                                                                                                                                                               3


            Source Code                                       Model Extraction                          Intermediate Representations                       Analysis                             Results
 public class example{
   public static int example(int x) {
     if (x > 0) {
                                                                                                                                                       Control Analysis                  Execution Metrics
       int result = 1;
           while (x > 1) result *= x--;
           return result;                                                                                                                           Complexity Evaluation
     }
     return 0;                                                                                                                                                                                  Coverage
   }
   public static void main(String[] args) {
                                                                                                                                                       Path Simulation
     int y = example(5)
     System.out.println(y);
   }                                                                                                                                                Vulnerability Detection                 Detected Defects
 }                                                                                                          AST     CFG       DFG




                                                                                   Fig. 2: Static analysis workflow.

                            Source Code                                     Instrumented Code                                  Compiled Program                               Program Trace
             public class example{                                    ①
               public static void main(String[] args) {
                 int a = 3;
                                                                      Tmp1 = a == 3;
                                                                      Tmp2 = b == 5;
                                                                                                                                        Binary                                  API Calls
                 int b = 5;                                           Tmp3 = Tmp1 || Tmp2;
                 int c = 2;                                           Top.id = InstanceID;
                 int d;                                               Top.index = 4;
                                                                      $sample_values(Tmp1,Tmp2,Tmp3);                           Debug Information                             I/O Operations
                                                                      if(Tmp3)
                 ① if (a == 3 || b == 5) {
                    ② a = b + c;
                        d = a + 2;
                                                                      ②                                                                                                       Execution Paths
                                                                      a = b + c;
                    System.out.println("Value of a: " + a);
                                                                      d = a + 2;
                    System.out.println("Value of d: " + d);
                                                                      Top.id = InstanceID;
                  }
                                                                      Top.index = 5;                                                                                          Thread Events
             }                                                        $count_stmt;                                                     Test Suite


                                                                               Fig. 3: Dynamic analysis workflow.

then analyzed to detect issues such as unreachable                                                                           The architecture and configuration features of
code, data dependencies, and syntactic errors. These                                                                      LLMs (e.g., model families, parameter size, and
series of processes ultimately enhance code quality                                                                       context window length) collectively determine their
and reliability.                                                                                                          capabilities, performance and applicability. The
   Dynamic Analysis. Dynamic analysis (a.k.a. run-                                                                        studies selected in this survey involve LLM model
time analysis) is a program analysis approach that                                                                        families such as LLaMA [26], CodeLLaMA [27]
uncovers program properties by repetitively exe-                                                                          and GPT [28], [29]. The parameter size of a
cuting programs in one or more runs [23]. The                                                                             large model typically refers to the number of
stages involved in dynamic analysis are depicted                                                                          variables used for learning and storing knowledge.
in Figure 3. These stages include instrumenting the                                                                       The parameter size represents a model’s learning
source code to enable runtime tracking, compiling                                                                         capacity, indicating its ability to capture complexity
the instrumented code into a binary, and executing                                                                        and detail from data. Generally, larger parameter
it with test suites. After completing the above steps,                                                                    sizes enhance the model’s expressive power,
program traces such as function calls, memory ac-                                                                         enabling it to learn more intricate patterns and finer
cesses and system calls are captured.                                                                                     details. The context window refers to the range
                                                                                                                          of text fragments a model uses when generating
B. Large Language Models                                                                                                  each output. It determines the amount of contextual
   Large Language Models (LLMs) are large-scale                                                                           information the model can reference during
neural networks built on deep learning techniques,                                                                        generation. Selecting appropriate architectures and
primarily utilizing the Transformer architecture [24].                                                                    configurations for LLMs in different scenarios is
Transformer models utilize self-attention mecha-                                                                          crucial for optimizing their performance.
nism to identify relationships between elements
within a sequence, which enables them to out-                                                                                      III. LLM FOR S TATIC A NALYSIS
perform other machine learning models in under-                                                                              Static analysis examines various objects, such
standing contextual relationships. Trained on vast                                                                        as analyzing vulnerabilities and detecting malware
datasets, LLMs learn syntax, semantics, context,                                                                          in source code binary executables. Analyzing vul-
and relationships within language, enabling them                                                                          nerabilities in source code requires techniques like
to generate and comprehend natural language [25].                                                                         dependency analysis and taint tracking to trace the
Furthermore, LLMs possess knowledge reasoning                                                                             flow of sensitive data. On the other hand, Detecting
capabilities, allowing them to retrieve and synthesize                                                                    malware focuses on control flow examination and
information from large datasets to answer questions                                                                       behavior modeling to identify malicious patterns.
involving common sense and factual knowledge.                                                                             Consequently, LLM assistance differs by program
                                                                                                                                             4


    Reference           AST   CFG   DFG   OS   App   Vulnerability Type                      LLM’s assistance

    LLift [30]          ✗     ✓     ✗     ✓     ✗    Use-before-initialization (UBI).        Path analysis.
    SLFHunter [31]      ✓     ✓     ✓     ✓     ✗    Command injection vulnerabilities.      Taint sinks.
    LATTE [32]          ✗     ✓     ✓     ✓     ✗    Binary taint analysis for data flows.   Binary taint analysis and code slicing.
                                                                                             Memory allocation and deallocation inten-
    IMMI [33]            ✗    ✓     ✓     ✓     ✗    Kernel memory bugs.
                                                                                             tions
    DefectHunter [34]   ✓     ✓     ✓     ✗    ✓     General vulnerability.                  Code sequence embeddings.
    IRIS [35]           ✗     ✓     ✓     ✗    ✓     Taint analysis in smart contracts.      Taint sources and sinks.
    VERACATION [36]     ✓     ✗     ✓     ✗    ✓     Syntactic-based vulnerability.          Filters non-vulnerability-related statements.
                                                     Vulnerabilities in Code review pro-
    Mao et al. [37]     ✓      ✗    ✓     ✗    ✓                                             Simulates multi-role discussions.
                                                     cesses.
                                                                                             Fine-tuned with multitask self-instructed
    MSIVD [38]           ✗    ✓     ✓     ✗    ✓     General vulnerability.
                                                                                             learning.
    GPTScan [39]        ✓      ✗    ✓     ✗    ✓     Smart contract logic vulnerabilities.   Analyzes smart contract semantics.
    Yang et al. [40]    ✓      ✗    ✗     ✗    ✓     IoT software vulnerability.             Explains vulnerabilities in code.
    LLbezpeky [41]      ✗      ✗    ✗     ✗    ✓     Android security vulnerability.         Android application security.
    SkipAnalyzer [42]   ✓      ✗    ✓     ✗    ✓     Bug detection.                          Identifies bugs and generates patches.
                                                                                             Extracts attributes of smart contract byte-
    HYPERION [43]        ✗    ✓     ✓     ✗    ✓     DApp Inconsistencies.
                                                                                             code.
    Zhang et al. [44]   ✓     ✗     ✓     ✗    ✓     General vulnerability.                  Detects vulnerabilities and fixes.
    GPTLENS [45]        ✓     ✗     ✓     ✗    ✓     Smart contract vulnerability.           Generates diverse vulnerability hypotheses.
    LuaTaint [46]       ✓     ✓     ✓     ✗    ✓     IoT vulnerability                       Prunes false alarms.


TABLE I: Overview of the intermediate representations (AST, CFG, DFG) employed, their application
domains (OS-level or application-level vulnerabilities), their application to specific vulnerability types,
and the assistance provided by LLMs across selected studies



type and analysis purpose, which will be discussed                  feature extraction, enhanced detection accuracy, and
in this section across four directions: (i) vulnera-                remediation strategies. These capabilities enable
bility detection (§ III-A), (ii) malware detection (§               efficient and precise identification of OS-level and
III-B), (iii) program verification (§ III-C), and (iv)              application-level vulnerabilities. Additionally, a
static analysis enhancement (§ III-D).                              detailed comparison of the best-performing LLMs in
                                                                    the reviewed studies reveals key factors influencing
                                                                    their effectiveness and adoption. Table II presents a
A. LLM for Vulnerability Detection                                  comprehensive summary of these models, including
   Vulnerability detection focuses on identifying                   their model family, parameter sizes, context window
potential security risks or weaknesses in software                  sizes, and open-source availability.
through automated tools and techniques,                                OS-level Vulnerability. OS-level vulnerabilities
which demand precise code analysis and a                            refer to security flaws within critical components
deep understanding of program behavior [47],                        of an operating system, such as the kernel, system
[48]. Leveraging their advanced contextual                          libraries, or device drivers. These vulnerabilities
comprehension, LLMs can analyze both semantic                       can compromise the stability and security of
and syntactic patterns in source code, providing                    the entire system, allowing attackers to gain
actionable suggestions and remediation strategies for               unauthorized access, disrupt operations, or
addressing vulnerabilities. As a result, integrating                cause system-wide failures affecting all running
LLMs into vulnerability detection has become a                      applications. Common examples include memory
prominent application in program analysis.                          management errors, privilege escalation, and
   To provide a clearer understanding of LLM                        resource misuse. Leveraging LLMs, tools like the
applications in vulnerability detection, Table I                    LLift framework [30] address challenges such as
summarizes the intermediate representations                         path sensitivity and scalability in detecting OS-level
(IRs) utilized and the specific vulnerability types                 vulnerabilities. By combining constraint-guided
addressed in selected studies. Figure 4 offers a visual             path analysis with task decomposition, LLift
overview of LLM integration at various stages,                      improves the detection of issues like use-before-
highlighting their roles in contextual understanding,               initialization (UBI) in large-scale codebases. Ye et
                                                                                                                                                 5



         Data Collection                      Pre-processing                              Detection Model             Vulnerability Reports

                                                                                    Automatic Vulnerability
                                       Semantic & Syntactic Analysis
                                                                                         Detection                    Confidence Scores
       OS-level Vulnerability

                                            Data Flow Tracking                          False Positive Filtering

         Application-level
                                                                                                                      Vulnerability Types
          Vulnerability                   Control Flow Tracking                    Patch Solution Generation




                                                                                                                    Vulnerable Components
          Code Source                                                            Enhance Detection Accuracy &
                                         Contextual Understanding
                                                                                     Reduce False Positive
           Kernel Code
                                                                                   Automatic Code Review &               Root Causes
                                            Feature Extraction
                                                                                       Patch Generation
      Application Source Code


           IoT Software
                                                                       LLM Assistance                              Remediation Recommendations


                             Fig. 4: A diagram of LLMs’ application in vulnerability detection.

al. [31] developed SLFHunter, which integrates                                 abilities can compromise the application’s perfor-
static taint analysis with LLMs to identify command                            mance, data integrity, or user privacy. However, they
injection vulnerabilities in Linux-based embedded                              typically do not affect the overall stability of the
firmware. The LLMs are utilized to analyze                                     operating system. Common examples include input
custom dynamically linked library functions and                                validation issues, logic errors, and misconfigura-
enhance the capabilities of traditional analysis                               tions. These vulnerabilities can result in unautho-
tools. Furthermore, Liu et al. [32] proposed a                                 rized access or data breaches, as well as application-
system called LATTE, which combines LLMs                                       specific security incidents [49]–[55].
with binary taint analysis. The code slicing and
                                                                                  To address the challenges in application-level
prompt construction modules serve as the core of
                                                                               vulnerability detection, Wang et al. [34] introduced
LATTE, where dangerous data flows are isolated for
                                                                               the Conformer mechanism, which integrates self-
analysis. These modules reduce the complexity for
                                                                               attention and convolutional networks to capture both
LLMs by providing context-specific input, allowing
                                                                               local and global feature patterns. To further refine
improved efficiency and precision in vulnerability
                                                                               the detection process, they optimize the attention
detection through tailored prompt sequences that
                                                                               mechanism to reduce noise in multi-head attention
guide the LLM in the analysis process. In addition,
                                                                               and improve model stability. By combining struc-
Liu et al. [33] proposed a system for detecting
                                                                               tural information processing, pre-trained models,
kernel memory bugs using a novel heuristic
                                                                               and the Conformer mechanism in a multi-layered
called Inconsistent Memory Management Intentions
                                                                               framework, the approach improves detection accu-
(IMMI). The system detects kernel memory bugs by
                                                                               racy and efficiency. Building on these advancements,
summarizing memory operations and slicing code
                                                                               IRIS [35] proposes a neuro-symbolic approach that
related to memory objects. It uses static analysis
                                                                               combines LLMs with static analysis to support
to infer inconsistencies in memory management
                                                                               reasoning across entire projects. The static analysis
responsibilities between caller and callee functions.
                                                                               is responsible for extracting candidate sources and
LLMs assist in interpreting complex memory
                                                                               sinks, while the LLM infers taint specifications
management mechanisms and enable the
                                                                               for specific CWE categories. Similarly, Cheng et
identification of bugs such as memory leaks
                                                                               al. [36] combined semantic-level code clone de-
and use-after-free errors with improved precision.
                                                                               tection with LLM-based vulnerability feature ex-
   Application-level Vulnerability. Application-                               traction. By integrating program slicing techniques
level vulnerabilities are security weaknesses found                            with the LLM’s semantic understanding, they re-
within individual software programs. These vulner-                             fined vulnerability feature detection. This approach
                                                                                                                    6


addresses the limitations of traditional syntactic-            the efficiency of vulnerability detection and reduce
based analysis.                                                costs, ultimately improving scalability and feasi-
                                                               bility in large IoT systems [57]–[59]. Meanwhile,
Reference       LLM           MF        Param CW Open-Source   Xiang et al. [46] proposed LuaTaint, a static anal-
LLift [30]        GPT-4-0613     GPT-4      - 32768   ✗
                                                               ysis framework designed to detect vulnerabilities
SLFHunter [31]    GPT-4.0        GPT-4      - 32768   ✗        in the web configuration interfaces of IoT de-
LATTE [32]        GPT-4.0        GPT-4      - 32768   ✗        vices. LuaTaint integrates flow-, context-, and field-
IMMI [33]         ChatGPT-4-1106 GPT-4      - 32768   ✗
DefectHunter [34] UniXcoder        -      250M 768    ✓        sensitive static taint analysis with key features such
IRIS [35]         GPT-4.0        GPT-4      - 32768   ✗        as framework-specific adaptations for the LuCI web
VERACATION [36] GPT-4.0          GPT-4      -  1024   ✗        interface and pruning capabilities powered by GPT-
Mao et al. [37]   GPT-3.5-turbo GPT-3.5   175B 4096   ✗
MSIVD [38]        CodeLlama-13B CodeLlama 13B 2048    ✓        4. By converting Lua code into ASTs and CFGs,
GPTScan [39]      GPT-3.5-turbo GPT-3.5   175B 4096   ✗        the framework performs precise taint analysis to
Yang [40]         ChatGPT-4.0    GPT-4      - 32768   ✗
                                                               identify vulnerabilities like command injection and
LLbezpeky [41]    GPT-4.0        GPT-4      - 32768   ✗
SkipAnalyzer [42] ChatGPT-4.0    GPT-4      -  8192   ✗        path traversal. The system uses dispatching rules and
HYPERION [43] LLaMA2 [56] LLaMA             -  4096   ✓        LLM-powered alarm pruning to improve detection
Zhang et al. [44] ChatGPT-4.0    GPT-4      -  8192   ✗
GPTLENS [45]      GPT-4.0        GPT-4      - 32768   ✗
                                                               precision, reduce false positives, and efficiently an-
LuaTaint [46]     GPT-4.0        GPT-4      -  1920   ✗        alyze firmware across large-scale datasets.
                                                                   Mohajer et al. [42] presented SkipAnalyzer, a tool
TABLE II: Overview of the best-performing LLMs                 that employs LLMs for bug detection, false positive
used in referenced papers, their model families                filtering, and patch generation. By improving the
(MF), parameter sizes (Param), context window                  precision of existing bug detectors and automating
sizes (CW), and open-source availability.                      patching, this approach significantly reduces false
                                                               positives and ensures accurate bug repair. Mean-
                                                               while, Zhang et al. [44] introduced tailored prompt
   Mao et al. [37] implemented a multi-role ap-                engineering techniques with GPT-4 [29], leveraging
proach where LLMs act as different roles, such                 auxiliary information such as API call sequences
as testers and developers, simulating interactions             and data flow graphs to provide structural and se-
in a real-life code review process. This strategy              quential context. This approach also employs chain-
fosters discussions between these roles, enabling              of-thought prompting to enhance reasoning capabil-
each LLM to provide distinct insights on potential             ities, demonstrating improved accuracy in detecting
vulnerabilities. MSIVD [38] introduces a multi-task            vulnerabilities across Java and C/C++ datasets. Ex-
self-instructed fine-tuning technique that combines            tending the application of LLMs in decentralized
vulnerability detection, explanation, and repair, im-          applications and smart contract analysis, Yang et
proving the LLM’s ability to understand and reason             al. [43] developed HYPERION, which combines
about code through multi-turn dialogues. Addition-             LLM-based natural language analysis with sym-
ally, the system integrates LLMs with a data flow              bolic execution to address inconsistencies between
analysis-based GNN, which models the program’s                 DApp descriptions and smart contracts. The system
control flow graph to capture variable definitions             integrates a fine-tuned LLM to analyze front-end
and data propagation paths. This enables the model             descriptions, while symbolic execution processes
to rely not only on the literal information in the             contract bytecode to recover program states, effec-
code but also on the program’s graph structure for             tively identifying discrepancies that may undermine
more precise detection. Similarly, GPTScan [39]                user trust.
demonstrates how GPT can be applied to code un-                    For smart contract vulnerability detection, Hu et
derstanding and matching scenarios, reducing false             al. [45] introduced GPTLENS, a two-stage adversar-
positives and uncovering new vulnerabilities previ-            ial framework leveraging LLMs. GPTLENS assigns
ously missed by human auditors.                                two synergistic roles to LLMs: an auditor generates
   In the domain of IoT software, Yang et al. [40]             a diverse set of vulnerabilities with associated rea-
explored the application of LLMs combined with                 soning, while a critic evaluates and ranks these vul-
static code analysis for detecting vulnerabilities.            nerabilities based on correctness, severity, and prof-
By leveraging prompt engineering, LLMs enhance                 itability. This open-ended prompting approach facil-
                                                                                                                7


itates the identification of a broader range of vulner-   al. [68] utilized decompiled and disassembled out-
abilities, including those that are uncategorized or      puts of the Babuk ransomware as inputs to the LLM
previously unknown. Experimental results on real-         to generate function descriptions through carefully
world smart contracts show that GPTLENS outper-           designed prompts. The generated descriptions were
forms traditional one-stage detection methods while       evaluated using BLEU [69] and ROUGE [70] met-
maintaining low false positive rates. Focusing on         rics to measure functional coverage and agreement
Android security and software bug detection, Math-        with analysis articles. Additionally, Simion et al.
ews et al. [41] introduced LLbezpeky, an AI-driven        [71] evaluated the feasibility of using out-of-the-box
workflow that assists developers in detecting and         open-source LLMs for malware detection by analyz-
rectifying vulnerabilities. Their approach analyzed       ing API call sequences extracted from binary files.
Android applications, achieving over 90% success in       The study benchmarked four open-source LLMs
identifying vulnerabilities in the Ghera benchmark.       (Llama2-13B, Mistral [72], Mixtral, and Mixtral-
                                                          FP16 [73]) using API call sequences extracted from
   Takeaway 1                                             20,000 malware and benign files. The results showed
                                                          that the models, without fine-tuning, achieved low
   Researchers utilize static analysis with dif-
                                                          accuracy and were unsuitable for real-time detec-
   ferent intermediate representations and LLMs
                                                          tion. These findings highlight the need for fine-
   to address different types of vulnerabilities.
                                                          tuning and integration with traditional security tools.
   ASTs enhance syntactic reasoning and code
                                                             Analyzing malicious behaviors to detect malware
   representation for syntax-related vulnerabili-
                                                          is another approach. Zahan et al. [74] employed
   ties. CFGs address control flow issues such as
                                                          a static analysis tool named CodeQL [75] to pre-
   privilege escalation by prioritizing paths and
                                                          screen npm packages. This step filtered out benign
   detecting anomalies. DFGs focus on data-flow
                                                          files, thereby reducing the number of packages re-
   vulnerabilities such as command injection,
                                                          quiring further investigation. Following this step,
   enabling LLMs to infer taint sources and
                                                          they utilized GPT-3 and GPT-4 models to analyze
   refine detection rules. This integration of IRs
                                                          the remaining JavaScript code for detecting complex
   and LLMs strengthens detection capabilities.
                                                          or subtle malicious behaviors. The outputs from the
   Among LLMs, GPT-4 is commonly adopted
                                                          LLMs were refined iteratively. Accuracy improved
   for its large context window and versatil-
                                                          through continuous adjustments to the model’s focus
   ity. Task-specific models like UniXcoder [60]
                                                          based on feedback and re-evaluation.
   perform well in specialized scenarios, while
                                                             Other studies focus on applying LLMs
   open-source models such as CodeLlama [61]
                                                          specifically to Android malware detection. Khan et
   provide reproducibility and flexibility.
                                                          al. [76] extracted Android APKs to obtain source
                                                          code and opcode sequences, constructing call graphs
                                                          to represent the structural relationships between
B. LLM for Malware Detection                              functions. Models such as CodeBERT [77] and
   Malware detection determines whether a program         GPT were employed to generate semantic feature
has malicious intent and is an essential aspect of pro-   representations, which were used to annotate the
gram analysis research. Initially, signature-based de-    nodes in the call graphs. The graphs were enriched
tection methods were predominantly used. As mal-          with structural and semantic information. These
ware evolved, new detection techniques emerged,           enriched graphs were then processed through a
including behavior-based detection, heuristic detec-      graph-based neural network to detect malware in
tion, and model checking approaches. Data mining          Android applications. Zhao et al. [78] first extracted
and machine learning algorithms soon followed,            features from Android APK files using static
further enhancing detection capabilities [62]–[67].       analysis, categorizing them into permission view,
   Traditional malware detection methods struggle         API view, and URL & uses-feature view. A multi-
with challenges like obfuscation and polymorphic          view prompt engineering approach was applied to
malware. LLMs offer a new approach to enhance             guide the LLM in generating textual descriptions
detection accuracy and adapt to evolving threats          and summaries for each feature category. The
by analyzing code semantics and patterns. Fujii et        generated descriptions were transformed into vector
                                                                                                               8


representations, which served as inputs for a deep       highlight the diverse applications of these models
neural network (DNN)-based classifier to determine       in automating verification tasks. The inputs in
whether the APK was malicious or benign. Finally,        these studies can be categorized into four types: (i)
the LLM produced a diagnostic report summarizing         Code, which includes program implementations or
the potential risks and detection results.               snippets used for analysis or synthesis. (ii) Specifi-
                                                         cations, referring to formal descriptions of program
   Takeaway 2                                            behavior, such as preconditions, postconditions, or
   The integration of LLMs with static analysis          logical formulas. (iii) Formal methods, encompass-
   techniques enables the analysis of structured         ing mathematical constructs like theorems, proofs,
   input sources, including decompiled func-             and loop invariants for ensuring correctness. (iv)
   tions, API call sequences, JavaScript code            Error and debugging information, such as coun-
   files, and APK attributes. A key commonality          terexamples, type hints, or failed code generation
   across approaches is the reliance on LLMs             cases that aid in resolving programming issues.
   to process static features and generate se-               Proof Generation. Proof generation in program
   mantic representations, textual descriptions,         verification automates the creation of formal proofs
   or embeddings, which are subsequently used            to ensure program correctness, logical consistency,
   for classification or detection tasks. Addition-      and compliance with specifications. This process
   ally, we notice that both open-source LLMs            reduces the need for manual effort and enhances ver-
   (e.g., Llama2-13B and Mistral) and propri-            ification efficiency by streamlining complex proof
   etary models (e.g., GPT-4) are widely utilized        tasks. Kozyrev et al. [79] developed CoqPilot, a
   in this task.                                         VSCode plugin that integrates LLMs such as GPT-4,
                                                         GPT-3.5, LLaMA-2 [26], and Anthropic Claude [93]
                                                         with Coq-specific tools like CoqHammer [94] and
C. LLM for Program Verification                          Tactician [95] to automate proof generation in
   Automated program verification employs tools          the Coq theorem prover. The authors implemented
and algorithms to ensure that a program’s behav-         premise selection for better LLM prompting and
ior aligns with predefined specifications, enhanc-       created an LLM-guided mechanism that attempted
ing both software reliability and security. Tradi-       fixing failing proofs with the help of the Coq’s error
tional verification methods often require substantial    messages. Additionally, Zhang et al. [80] developed
manual effort, particularly for writing specifications   the Selene framework to automate proof generation
and selecting strategies. These processes are often      in software verification using LLMs. The framework
complex and prone to errors, especially in large-        is built on the industrial-level operating system
scale systems. In contrast, automated verification       microkernel [96], seL4 [97], and introduces the
generates key elements such as invariants, precon-       technique of lemma isolation to reduce verification
ditions, and postconditions, using techniques like       time. Its key contributions include efficient proof
static analysis and model checking to ensure correct-    validation, dependency augmentation, and showcas-
ness. The integration of LLMs further enhances this      ing the potential of LLMs in automating complex
process by enabling the automatic analysis of code       verification tasks.
features and the efficient selection of verification         Invariant Generation. Invariant generation iden-
strategies. This reduces manual intervention and         tifies properties that remain true during program
significantly accelerates verification. Consequently,    execution, providing a logical foundation for ver-
automated program verification has evolved into          ifying correctness and analyzing complex iterative
a more efficient and reliable method for ensuring        structures like loops and recursion.
software quality. This subsection introduces diverse         Some studies have explored various ways to
applications of LLMs in program verification, high-      leverage LLMs for generating and ranking loop
lighting their role in automating and enhancing          invariants. Janßen et al. [82] investigated the utility
critical tasks.                                          of ChatGPT in generating loop invariants. The
   Table III provides an overview of various studies     authors used ChatGPT to annotate 106 C programs
utilizing LLMs for program verification. It summa-       from the SV-COMP Loops category [98] with loop
rizes their targets, methodologies, and outcomes to      invariants written in ACSL [99], evaluating the
                                                                                                                                                   9


 Reference             Target                         LLM                      Param   OS   Input                 Output

                                                      Claude                      -    ✗
                                                      LLaMA-2-13B               13B    ✓
 CoqPilot [79]         Proof generation                                                     Formal methods        Coq proofs
                                                      GPT-3.5                     -    ✗
                                                      GPT-4*                      -    ✗
                                                      GPT-3.5-turbo            175B    ✗
 Selene [80]           Proof generation                                                     Specifications        Formal proofs
                                                      GPT-4*                      -    ✗
                                                      GPT-3.5-turbo            175B    ✗                          Reranked LLM-generated invari-
 iRank [81]            Loop invariant ranking                                               Formal methods
                                                      GPT-4*                      -    ✗                          ants
 Janßen et al. [82]    Loop invariant generation      GPT-3.5                  175B    ✗    Specifications        Valid loop invariants
 Pirzada et al. [83]   Loop invariant generation      GPT-3.5-Turbo-Instruct   175B    ✗    Formal methods        Loop invariants
                                                      LLaMA-3-8B                 8B    ✓
 LaM4Inv [84]          Loop invariant generation      GPT-3.5-Turbo            175B    ✗    Code                  Loop invariants
                                                      GPT-4-Turbo*                -    ✗
 Pei et al. [85]       Invariant prediction           GPT-4                       -    ✗    Code                  Static invariants
                                                      GPT-3.5-turbo-0613*      175B    ✗
 AutoSpec [86]         Specification synthesis                                              Code                  Specifications
                                                      Llama-2-70B               70B    ✓
                                                      GPT-3.5-turbo            175B    ✗
 LEMUR [87]            Automated verification                                               Specifications        Loop invariants
                                                      GPT-4*                      -    ✗
 SynVer [88]           Automated verification         GPT-4                       -    ✗    Specifications        Candidate C programs
                                                                                            Code and specifica-
 PropertyGPT [89]      Smart contract verification    GPT-4-0125-preview         -     ✗                          Formal verification properties
                                                                                            tions
                       Python symbolic execu-         GPT-4o-mini                -     ✗    Error and debugging   Initial Z3Py code
 LLM-Sym [90]
                       tion                           GPT-4o                     -     ✗    Error and debugging   Refined Z3Py code
                       Verification strategy selec-                                         Code and specifica-
 CFStra [91]                                          GPT-3.5-turbo            175B    ✗                          Identified code features
                       tion                                                                 tions
                       Error specification infer-
 Chapman et al. [92]                                  GPT-4                      -     ✗    Formal methods        Error specifications
                       ence


TABLE III: Overview referenced studies, detailing their targets, LLMs employed, parameter sizes
(Param), open-source availability (OS), input types, and resulting outputs.



validity and usefulness of these invariants. They                              invariants from the Daikon [102] dynamic analyzer,
integrated ChatGPT with the Frama-C [100] inter-                               they developed a static analysis-based method using
active verifier and the CPAchecker [101] automatic                             a scratchpad approach. This technique incrementally
verifier to assess how well the generated invariants                           generates invariants and achieves performance com-
enable these tools to solve verification tasks. Results                        parable to Daikon without requiring code execution.
showed that ChatGPT can produce valid and useful                               It also provides a static and cost-effective alternative
invariants for many cases, facilitating software                               to dynamic analysis.
verification by augmenting traditional methods with
insights provided by LLMs. Additionally, Chakra-                                  Integrating LLMs with Bounded Model Checking
bor et al. [81] observed that employing LLMs in                                (BMC) has shown potential in enhancing loop
a zero-shot setting to generate loop invariants often                          invariant generation. Pirzada et al. [83] proposed
led to numerous attempts before producing correct                              a modification to the classical BMC procedure that
invariants, resulting in a high number of calls to                             avoids the computationally expensive process of
the program verifier. To mitigate this issue, they                             loop unrolling by transforming the CFG. Instead
introduced iRank, a re-ranking mechanism based on                              of unrolling loops, the framework replaces loop
contrastive learning, which effectively distinguishes                          segments in the CFG with nodes that assert the
correct from incorrect invariants. This method                                 invariants of the loop. These invariants are generated
significantly reduces the verification calls required,                         using LLMs and validated for correctness using
improving efficiency in invariant generation.                                  a first-order theorem prover. This transformation
                                                                               produces loop-free program variants in a sound
  Besides, Pei et al. [85] explored using LLMs to                              manner, enabling efficient verification of programs
predict program invariants that were traditionally                             with unbounded loops. Their experimental results
generated through dynamic analysis. By fine-tuning                             demonstrate that the resulting tool, ESBMC
LLMs on a dataset of Java programs annotated with                              ibmc, significantly improves the capability of the
                                                                                                            10


industrial-strength software verifier ESBMC [103],     verification include smart contract verification,
verifying more programs compared to state-of-the-      symbolic execution, strategy selection and error
art tools such as SeaHorn [104] and VeriAbs [105],     specification inference. For instance, Liu et al. [89]
including cases these tools could not handle.          developed a novel framework named PropertyGPT,
Wu et al. [84] proposed LaM4Inv, a framework that      leveraging GPT-4 to automate the generation of
integrates LLMs with BMC to improve this process.      formal properties such as invariants, pre-/post-
The framework employs a ’query-filter-reassemble’      conditions, and rules for smart contract verification.
pipeline. LLMs generate candidate invariants,          The framework embeds human-written properties
BMC filters out incorrect predicates, and valid        into a vector database and retrieves reference
predicates are iteratively refined and reassembled     properties for customized property generation,
into invariants.                                       ensuring their compilation, appropriateness, and
   Automated Program Verification. Automating          runtime verifiability through iterative feedback and
program specification presents challenges such as      ranking. Similarly, Wang et al. [90] introduced an
handling programs with complex data types and          iterative framework named LLM-Sym. This tool
code structures. To address these issues, Wen et       leverages LLMs to bridge the gap between program
al. [86] introduced an approach called AutoSpec.       constraints and SMT solvers. The process begins
Driven by static analysis and program verification,    by extracting control flow paths, performing type
AutoSpec uses LLMs to generate candidate spec-         inference, and iteratively generating Z3 [108] code
ifications. Programs are decomposed into smaller       to solve path constraints. A notable feature of LLM-
components to help LLMs focus on specific sec-         Sym is its self-refinement mechanism, which utilizes
tions. The generated specifications are iteratively    error messages to debug and enhance the generated
validated to minimize error accumulation. This pro-    Z3 code. If the code generation process fails, the
cess enables AutoSpec to handle complex code           system directly employs LLMs to solve the con-
structures, such as nested loops and pointers, mak-    straints. Once constraints are resolved, Python test
ing it more versatile than traditional specification   cases are automatically generated from Z3’s outputs.
synthesis techniques. Wu et al. [87] introduced the       Another approach [91] automates the selection
LEMUR framework. In this hybrid system, LLMs           of verification strategies to overcome limitations
generate program properties like invariants as sub-    of traditional tools like CPAchecker [101]. These
goals, which are then verified and refined by rea-     tools often require users to manually select strate-
soners such as CBMC [106], ESBMC [103] or              gies, making the process more complex and time-
UAUTOMIZER [107]. The framework is based on a          consuming. LLMs analyze code features to identify
sound proof system, thus ensuring correctness when     suitable strategies, streamlining the verification pro-
LLMs propose incorrect properties. An oracle-based     cess and minimizing user input. This automation
refinement mechanism improves these properties,        not only improves efficiency but also minimizes
enabling LEMUR to enhance efficiency in verifi-        reliance on expert knowledge. Additionally, Chap-
cation and handle complex programs more effec-         man et al. [92] proposed a method that combines
tively than traditional tools. Additionally, Mukher-   static analysis with LLM prompting to infer error
jee et al. [88] introduced SynVer, a framework         specifications in C programs. Their system queries
that integrates LLMs with formal verification tools    the LLM when static analysis encounters incomplete
for automating the synthesis and verification of C     information, enhancing the accuracy of error specifi-
programs. SynVer takes specifications in Separa-       cation inference. This approch is effective for third-
tion Logic, function signatures, and input-output      party functions and complex error-handling paths.
examples as input. It leverages LLMs to generate
candidate programs and uses SepAuto, a verification       Takeaway 3
backend, to validate these programs against the
specifications. The framework prioritizes recursive       The applications of LLMs in program veri-
program generation, reducing the dependency on            fication span various tasks, including proof
manual loop invariants and improving verification         generation, specification synthesis, loop in-
success rates.                                            variant generation, and strategy selection.
   Others. Other applications of LLMs in program
                                                                                                           11



   These methods streamline the verification           Advisor, and Operator to propose and implement op-
   process by automating the generation of prop-       timizations while preserving semantic correctness.
   erties, invariants, and other critical compo-          Explainable Fault Localization. Yan et al. [112]
   nents essential for program analysis. Despite       proposed CrashTracker, a hybrid framework that
   their diverse applications, these methods share     combines static analysis with LLMs. This approach
   a common goal: reducing reliance on expert          improves the accuracy and explainability of crashing
   knowledge and improving verification effi-          fault localization in framework-based applications.
   ciency. A key aspect of achieving this goal         CrashTracker introduces Exception-Thrown Sum-
   is the iterative refinement of LLM-generated        maries (ETS) to represent fault-inducing elements
   outputs. This refinement process often incor-       in the framework. It also uses Candidate Informa-
   porates static analysis or hybrid frameworks        tion Summaries (CIS) to extract relevant contextual
   that integrate formal verification tools, further   information for identifying buggy methods. ETS
   enhancing reliability.                              models are employed to identify potential buggy
                                                       methods. LLMs then generate natural language fault
                                                       reports based on CIS data, enhancing the clarity of
                                                       fault explanations. CrashTracker demonstrates state-
D. LLM for Static Analysis Enhancement
                                                       of-the-art performance in precision and explainabil-
   Beyond the previously mentioned applications of     ity when applied to Android applications.
LLMs, other studies focus on leveraging LLMs to           Extract Method Refactoring. Pomian et
assist in certain processes of static analysis.        al. [113] introduced EM-Assist, a tool that
   Code Review Automation. Lu et al. [109] pro-        combines LLMs and static analysis to enhance
posed LLaMA-Reviewer, a model that leverages           Extract Method (EM) refactoring in Java and
LLMs to automate code review. It incorporates          Kotlin projects. EM-Assist uses LLMs to generate
instruction-tuning of a pre-trained model and em-      EM refactoring suggestions and applies static
ploys Parameter-Efficient Fine-Tuning techniques to    analysis to discard irrelevant or impractical options.
minimize resource requirements. The system auto-       To improve the quality of suggestions, the tool
mates essential code review tasks, including pre-      employs program slicing and ranking mechanisms
dicting review necessity, generating comments, and     to prioritize refactorings aligned with developer
refining code.                                         preferences. EM-Assist automates the entire
   Code Coverage Prediction. Dhulipala et              refactoring process by leveraging the IntelliJ IDEA
al. [110] introduced CodePilot, a system that          platform to safely implement changes.
integrates planning strategies and LLMs to predict        Obfuscated Code Disassembly. Rong et al. [114]
code coverage by analyzing program control flow.       introduced DISASLLM, a framework that combines
CodePilot first generates a plan by analyzing          traditional disassembly techniques with LLMs. The
program semantics, dividing the code into steps        LLM component validates disassembly results and
derived from control flow structures, such as loops    repairs errors in obfuscated binaries, enhancing the
and branches. Subsequently, CodePilot adopts           quality of the output. Through batch processing and
either a single-prompt approach (Plan+Predict in       GPU parallelization, DISASLLM achieves substan-
one step) or a two-prompt approach (planning first,    tial improvements in both the accuracy and speed
followed by coverage prediction). These approaches     of decoding obfuscated code, outperforming state-
guide LLMs to predict which parts of the code are      of-the-art methods
likely to be executed based on the formulated plan.       Privilege Variable Detection. Wang et al. [115]
   Decompiler Optimization. Hu et al. [111] pro-       presented a hybrid workflow that combines LLMs
posed DeGPT, a framework designed to enhance           with static analysis to detect user privilege-related
the clarity and usability of decompiler outputs for    variables in programs. The program is first ana-
reverse engineering tasks. DeGPT begins by ana-        lyzed to identify relevant variables and their data
lyzing the raw output of decompilers, identifying      flows, which provides an initial set of potential
issues such as ambiguous variable names, missing       user privilege-related variables. The LLM is used
comments, and poorly structured code. The frame-       to evaluate these variables by understanding their
work leverages LLMs in three distinct roles:Referee,   context and scoring them based on their relationship
                                                                                                               12


to user privileges.                                             IV.   LLM FOR DYNAMIC A NALYSIS
   Static Bug Warning Inspection. Wen et                    Dynamic analysis encompasses profiling and test-
al. [116] proposed LLM4SA, a framework that              ing. Profiling focuses on understanding program per-
integrates LLMs with static analysis tools to            formance by analyzing execution, such as counting
automatically inspect large volumes of static bug        statement or procedure executions through instru-
warnings. LLM4SA first extracts bug-relevant code        mentation. Testing aims to make sure the test suites
snippets using program dependence traversal. It then     can cover a program. Statement coverage verifies
formulates customized prompts with techniques            that every statement in the code is executed at least
such as Chain-of-Thought reasoning and few-shot          once during testing. Branch, condition, and path
learning. To ensure precision, the framework             coverage evaluate how thoroughly all branches, con-
applies pre- and post-processing steps to validate       ditions, and execution paths are tested [23]. This sec-
the results. This approach tackles challenges            tion examines how LLMs enhance dynamic analysis,
like token limitations by optimizing input size,         focusing on (i) malware detection (§ IV-A) under
reduces inconsistencies in LLM responses through         profiling, (ii) fuzzing (§ IV-B) and (iii) penetration
structured prompt engineering, and mitigates false       testing (§ IV-C) under testing.
positives via comprehensive validation.
                                                         A. LLM for Malware Detection
   Static Analysis Alert Adjudication. Flynn et
al. [117] proposed using LLMs to automatically              As discussed in § III-B, the definition of malware
adjudicate static analysis alerts. The system gener-     detection is provided. This subsection focuses
ates prompts with relevant code and alert details,       on using LLMs to analyze runtime data for
enabling the LLM to classify alerts as true or false     malware detection. The distinction between static
positives. To address context window limitations,        and dynamic analysis depends primarily on the
the system summarizes relevant code and provides         input source. For instance, if API call sequences
mechanisms for the LLM to request additional de-         are captured during program runtime, such as
tails or verify its classifications.                     through sandboxes, debuggers, or runtime analysis
                                                         frameworks, they are classified as dynamic analysis.
   Static Analysis Enhancement by Pseudo-code            Conversely, API call sequences extracted through
Execution. Hao et al. [118] presented E&V, a             methods like decompilation or disassembly from
system designed to enhance static analysis using         static files are classified as static analysis. Table IV
LLMs by simulating the execution of pseudo-code          provides an overview of LLMs in both static and
and verifying the results without needing external       dynamic approaches and their testing accuracy.
validation. It validates the results of the analy-          Yan et al. [119] proposed a dynamic malware
sis through an automatic verification process that       detection method that utilizes GPT-4 to generate text
checks for errors and inconsistencies in the pseudo-     representations for API calls, which are an essential
code execution. This system is particularly useful for   feature in dynamic malware analysis. Their method
tasks like crash triaging and backward taint analysis    incorporates the innovative use of prompt engineer-
in large codebases like the Linux kernel.                ing, allowing GPT-4 to generate highly detailed,
                                                         context-rich descriptions for each API call in a
                                                         sequence. These descriptions go beyond simple API
   Takeaway 4                                            names and delve into the specifics of how each API
   The methods in this subsection demonstrate            call behaves within the context of the malware’s ex-
   how LLMs integrate with static analysis               ecution. This provides a much deeper understanding
   across domains such as debugging, fault lo-           of the malware’s actions, as opposed to traditional
   calization, code refactoring, and privilege de-       approaches that primarily rely on raw, unprocessed
   tection. A notable insight is the use of LLMs         sequences of API calls. After generating these de-
   not just as generative tools but as collabora-        scriptions, the next step in the pipeline involves
   tors that complement static analysis through          using BERT to convert the textual descriptions
   contextual reasoning and iterative refinement.        into embeddings. These embeddings encapsulate the
                                                         semantic information of the API calls and their
                                                                                                                                                    13


 Reference              Target Malware            Input Source                           Type     LLM                  Param   CW     OS   Accuracy
 Fujii et al. [68]      Babuk ransomware          Decompiled/disassembled functions      Static   ChatGPT-4.0              -   8192   ✗    90.90%
                                                                                                  Llama2-13B             13B   4096   ✓    50%
                                                                                                  Mistral               7.3B   8192   ✓    51%
 Simion et al. [71]     General malicious files   API call sequences                     Static
                                                                                                  Mixtral              7∼13B   4096   ✓    67%
                                                                                                  Mixtral-FP16         7∼13B   4096   ✓    72%
                                                                                                  GPT-3.5-turbo-1106    175B   4096   ✗    91%
 Zahan et al. [74]      Malicious packages        JavaScript code files                  Static
                                                                                                  GPT-4-1106-preview       -   8192   ✗    99%
                                                                                                  CodeBERT              125M   512    ✓    95.29%
 Khan et al. [76]       Android malware           APK files                              Static   GPT-2                 1.5B   1024   ✓    94.89%
                                                                                                  RoBERTa               125M   512    ✓    94.94%
 Zhao et al. [78]       Android malware           APK files                              Static   GPT-4-1106-preview       -   8192   ✗    97.15%
                                                                                                  BERT                  110M   512    ✓
 Yan et al. [119]       General malware           API call sequences                   Dynamic                                             95.61%
                                                                                                  GPT-4                    -   8192   ✗
 Sun et al. [120]       Linux-based malware       System call traces                   Dynamic    ChatGPT-3.5           175B   4096   ✗    -
                                                                                                  BERT                  110M   512    ✓    67.72%
                                                                                                  DistilBERT             66M   512    ✓    63%
                                                                                                  GPT-2                 1.5B   1024   ✓    69%
 Sanchez et al. [121]   IoT malware               System call traces                   Dynamic
                                                                                                  BigBird               110M   4096   ✓    87%
                                                                                                  Longformer            150M   4096   ✓    86%
                                                                                                  Mistral               7.3B   8192   ✓    58%
 Li et al. [122]        Android malware           Code features and system calls        Hybrid    ChatGPT                  -   -      ✗    -


TABLE IV: Overview of the LLMs used in referenced papers, their target malware, input sources, type of
analysis, parameter sizes (Param), context window sizes (CW), open-source availability (OS), and testing
accuracy.



interactions, thereby forming a high-quality repre-                                   Takeaway 5
sentation of the entire API sequence. These repre-
sentations are then passed through a CNN, which                                       Dynamic malware detection with LLMs ana-
performs feature extraction and classification. This                                  lyzes runtime behaviors like API and system
comprehensive approach addresses several major                                        call traces to improve accuracy and inter-
challenges faced by traditional API-based models.                                     pretability. Larger models like GPT-4 enhance
                                                                                      adaptability to unseen patterns, while smaller
                                                                                      models like BERT are efficient for real-time
                                                                                      tasks. Hybrid approaches further optimize de-
                                                                                      tection by balancing interpretability and scal-
                                                                                      ability.


   Similarly, Sun et al. [120] developed a frame-                                  B. LLM for Fuzzing
work that uses dynamic analysis and LLMs to                                           Fuzzing is a technique for automated software
generate detailed cyber threat intelligence (CTI)                                  testing that inputs randomized data into a program
reports. The framework captures syscall execution                                  to detect vulnerabilities like crashes, assertion fail-
traces of malware and converts them into natural                                   ures, or undefined behaviors. The classifications of
language descriptions using a Linux syscall trans-                                 fuzzing is shown in Figure 5. Fuzzing approaches
former. These descriptions are organized into an                                   are categorized by three dimensions: test case gen-
Attack Scenario Graph (ASG) to preserve essential                                  eration, input structure, and program structure. Test
details and reduce redundancy. Sanchez et al. [121]                                case generation can be mutation-based which alters
applied pre-trained LLMs with transfer learning for                                existing inputs, or generation-based which creates
malware detection. They fine-tuned the models with                                 new inputs from scratch. Input structure distin-
a classification layer on a dataset of benign and                                  guishes smart fuzzing which utilizes input format
malicious system calls. This approach allows the                                   knowledge, from dumb fuzzing which generates
model to distinguish between normal and malicious                                  inputs blindly. Program structure analysis classifies
behavior while avoiding the need for training from                                 fuzzing as black-box, grey-box, or white-box, based
scratch by leveraging pre-trained LLMs.                                            on the tester’s level of program insight.
                                                                                                                         14



                          Test Case Generation
                                                 Mutation-based     and transitions to unexplored protocol states. This
                                                 Generation-based   approach overcomes challenges like reliance on
                                                                    initial seeds and restricted state-space exploration.
                                                  Smart Fuzzing
 Fuzzing Classification     Input Structure                            Beyond domain-specific applications, frameworks
                                                  Dumb Fuzzing      like LLAMAFUZZ [127] and CHATFUZZ [129]
                                                                    showcase the adaptability of LLMs for general
                                                    Blackbox
                                                                    program fuzzing. Zhang et al. proposed LLAMA-
                           Program Structure         Greybox        FUZZ, which combines greybox fuzzing with LLM-
                                                    Whitebox        based mutation to enhance branch coverage and
                                                                    bug detection. Its focus on structured data inputs
                Fig. 5: Fuzzing classifications.                    makes it an effective tool for augmenting traditional
                                                                    fuzzing methods, demonstrating improvements over
                                                                    AFL++ [137]. Similarly, Hu et al. introduced CHAT-
   The use of LLMs for fuzzing is summarized in                     FUZZ, leveraging ChatGPT to generate format-
Table V, which highlights the strategies, program                   conforming test cases for highly structured inputs,
structures, LLMs employed, and applications in the                  addressing the efficiency limitations of traditional
studies. Most research utilizing LLMs for fuzzing                   mutation- and grammar-based fuzzers. These frame-
focuses on greybox fuzzing.                                         works demonstrate the ability of LLMs to adapt
   Qiu et al. [123] introduced CHEMFuzz, an                         to structured program requirements while advancing
LLM-assisted fuzzing framework designed for                         fuzzing efficiency.
quantum chemistry software. CHEMFuzz uses                              Lemieux et al. [130] introduced CODAMOSA,
an evolutionary fuzzing approach with LLM-                          an approach that integrates LLMs into testing work-
based input mutation and output analysis to                         flows. CODAMOSA combines Search-Based Soft-
address the syntactic and semantic complexities                     ware Testing (SBST) with Codex [135] to gener-
of quantum chemistry software. The two-module                       ate test cases and address coverage stagnation. It
system combining syntactic mutation operators with                  integrates LLM-generated Python code into SBST
anomaly detection detected 40 bugs and 81 potential                 workflows, highlighting the collaboration between
warnings in Siesta 4.1.5 [134]. Eom et al. [126]                    traditional testing and LLM-driven techniques. As-
introduced CovRL, a framework that integrates                       mita et al. [132] explored LLM-based fuzzing in
coverage-guided reinforcement learning with                         BusyBox [138], a widely used Linux utility suite.
LLMs to enhance fuzzing for JavaScript engines.                     Their approach combines LLM-assisted seed gen-
The approach combines Term Frequency-Inverse                        eration with crash reuse to enhance efficiency in
Document Frequency (TF-IDF) weighted coverage                       black-box fuzzing workflows. Using GPT-4, they
maps with reinforcement learning to guide the                       demonstrated how LLMs handle complex inputs and
LLM-based mutator. This enables the generation of                   reuse crashes for cross-variant testing, improving
more effective test cases, discovering new coverage                 vulnerability detection. Additionally, Xia et al. [133]
areas and improving the efficiency of JavaScript                    proposed Fuzz4All, a universal fuzzing framework
engine fuzzing. Deng et al. [128] introduced                        that extends fuzzing beyond language- or system-
FuzzGPT, a framework for fuzzing deep learning                      specific constraints. Fuzz4All uses autoprompting
libraries. By mining historical bug-triggering                      and an iterative fuzzing loop to transform user-
programs and leveraging LLMs such as Codex                          provided inputs into prompts for generating diverse
[135] and CodeGen [136], FuzzGPT generates edge-                    test cases.
case inputs using strategies like few-shot, zero-shot,
and fine-tuned learning. This targeted approach                        Takeaway 6
exploits API-specific vulnerabilities, illustrating
the effectiveness of LLMs in managing complex                          LLM-based fuzzing frameworks have ad-
software ecosystems. Meng et al. [131] introduced                      vanced automated testing by combining
CHATAFL, an LLM-guided mutation-based                                  mutation-based and generation-based strate-
framework for protocol fuzzing. The framework                          gies with models like GPT-3.5, Codex, and
extracts protocol grammars, enhances seed diversity,
                                                                                                                                                   15


 Reference            Target                      TCG          PS       LLM                           Param      OS   LLMs Usage
                                                                        GPT-3.5                       175B       ✗
                      Quantum chemistry                                                                               Input file mutation and output
 CHEMFuzz [123]                                 Mutation     Greybox    Claude-2* [124]                 -        ✗
                      software                                                                                        analysis
                                                                        Bard [125]                      -        ✗
 CovRL [126]          JavaScript Engines        Mutation     Greybox    CodeT5+                       220M       ✓    Generates valid test cases
                                                                                                                      Mutate structured data inputs
 LLAMAFUZZ [127]      Real-world programs       Mutation     Greybox    llama-2-7b-chat-hf             7B        ✓
                                                                                                                      and generate new seeds
                                                                        Codex (code-davinci-002)        -        ✗    Mutatie and refine test cases
 FuzzGPT [128]        Deep Learning Libraries   Mutation     Greybox
                                                                        CodeGen (350M/2B/6B-mono)   350M/2B/6B   ✓    Generates initial test cases
                                                                                                                      Generates format-conforming
 CHATFUZZ [129]       General programs          Mutation     Greybox    GPT-3.5-turbo                 175B       ✗
                                                                                                                      variations of existing seeds
                                                                                                                      Generates tailored inputs and
 CODAMOSA [130]       Python modules            Mutation     Greybox    Codex                           -        ✗
                                                                                                                      extends callable sets
                      Network protocol                                                                                Extracts grammars and enrich
 CHATAFL [131]                                  Mutation     Greybox    GPT-3.5-turbo                 175B       ✗
                      implementations                                                                                 seed corpora
                                                             Greybox,
 Asmitaet al. [132]   BusyBox                   Mutation                GPT-4-0613                      -        ✗    Generate seeds
                                                             blackbox
                      Compilers, SMT solvers,
                                                Mutation,
 Fuzz4All [133]       quantum frameworks and                 Greybox    GPT-4.0                         -        ✗    Generates fuzzing inputs
                                                generation
                      programming toolchains.


TABLE V: Overview of the LLM-based fuzzers used in referenced papers, including their target software,
test case generation (TCG), program structure (PS), model parameters, open-source availability (OS), and
usage details.



    CodeGen. As shown in Table V, these tools                                   proved remediation effectiveness by 32%, and re-
    share common goals, such as improving test                                  duced costs by 46%. Additionally, Goyal et al. [142]
    coverage, addressing domain-specific chal-                                  proposed Pentest Copilot, a framework that uses
    lenges, and automating seed generation and                                  GPT-4-turbo to enhance penetration testing work-
    refinement.                                                                 flows. Pentest Copilot incorporates chain-of-thought
                                                                                reasoning and retrieval-augmented generation to au-
                                                                                tomate tool orchestration and exploit exploration.
C. LLM for Penetration Testing                                                  It ensures adaptability with a web-based interface.
                                                                                This approach combines automation with expert
   Penetration testing is a controlled security assess-                         oversight, enhancing the accessibility of penetration
ment that simulates real-world attacks to identify,                             testing while preserving technical depth.
evaluate, and mitigate vulnerabilities in systems and
networks [139].                                                                    Additionally, some frameworks are designed
   Deng et al. [140] explored the capabilities of                               as agent-based systems. Bianou et al. [143]
LLMs in penetration testing, revealing that while                               presented PENTEST-AI, a framework guided by
these models excel at sub-tasks, they face chal-                                the MITRE ATT&CK framework for multi-agent
lenges in maintaining context across multi-step                                 penetration testing. The framework automates
workflows. To address this limitation, the au-                                  reconnaissance, exploitation, and reporting tasks
thors proposed PentestGPT, a framework integrating                              using specialized LLM agents. PENTEST-AI
reasoning, generation, and parsing modules. This                                reduces human intervention while aligning
framework significantly improved task completion                                with established cybersecurity methodologies,
rates by 228.6% compared to GPT-3.5 and demon-                                  illustrating the synergy between LLMs and
strated effective performance in real-world scenar-                             structured security frameworks in addressing real-
ios. Huang et al. [141] developed PenHeal, an LLM-                              world challenges. Muzsai et al. [144] proposed
based framework combining penetration testing and                               HackSynth, an LLM-driven penetration testing
remediation. PenHeal includes a Pentest Module                                  agent with two modules: a Planner for generating
that uses techniques like counterfactual prompting to                           commands and a Summarizer for processing
autonomously detect vulnerabilities. Its remediation                            feedback. Tested on newly developed CTF-based
module offers tailored strategies based on sever-                               benchmarks, HackSynth demonstrated its capability
ity and cost efficiency. Compared to PentestGPT,                                to autonomously exploit vulnerabilities and achieve
PenHeal increased detection coverage by 31%, im-                                optimal performance with GPT-4. Gioacchini et
                                                                                                                                                                                                          16


   Pre-Engagement               Reconnaissance                       Vulnerability                       Exploitation                         Post                              Reporting
     Interactions                                                    Identification                                                        Exploitation
                             Gather target                       Use automated tools or            Exploit vulnerabilities           Gather additional                  Provide risk
   Establish Objectives      information passively                manual techniques to             to gain access or                 insights and assess the            assessments and
                             and actively.                       detect vulnerabilities.           escalate privileges.              impact.                            remediation strategies.
                            PentestGPT: Interprets tool        PenHeal: Enhances vulnerability
                                                                                                                                                                       PenHeal: Provides remediation
                            outputs and generates actionable   detection with Counterfactual      HackSynth: Automates              PentestGPT: Assists with lateral
      Define Scope                                                                                                                                                     strategies based on severity and
                            steps.                             Prompting.                         exploitation processes.           movement and multi-step tasks.     cost.
                            Pentest Copilot: Optimizes tool    HackSynth: Vulnerability           Pentest Copilot: Generates and
                                                                                                                                                                       Pentest Copilot: Generates
                            orchestration and command          identification via iterative       optimizes exploitation scripts.   PentestAgent: Supports attack      structured and detailed reports.
                                                               commands.                          PENTEST-AI: Executes              path analysis and persistence
      Set Rules of          generation.
                                                               PentestAgent: Dynamically
                                                                                                                                                                       PentestAgent: Automates
      Engagement            PENTEST-AI: Automates                                                 automated exploitation tasks.     strategies.                        comprehensive report creation.
                                                               analyzes and verifies
                            intelligence gathering.            vulnerabilities.




                          Fig. 6: Integration of LLMs across the six steps of penetration testing.

al. [145] developed AutoPenBench, a framework                                                          intelligence gathering. They improve vulnera-
with 33 tasks covering experimental and real-                                                          bility identification through dynamic analysis
world penetration testing scenarios. AutoPenBench                                                      methods, including counterfactual prompting.
compares autonomous and semi-autonomous agents,                                                        Additionally, LLMs assist in post-exploitation
tackling reproducibility challenges in penetration                                                     by facilitating multi-step attack strategies.
testing research. Fully autonomous agents achieved
a 21% success rate, significantly lower than the 64%
success rate of semi-autonomous setups. Shen et                                                                    V.          LLM FOR H YBRID A PPROACH
al. [146] introduced PentestAgent, leveraging LLMs                                                  A hybrid approach employs both static and dy-
and Retrieval-Augmented Generation (RAG) to                                                      namic analysis techniques at different stages. For
automate intelligence gathering, vulnerability                                                   example, combining static features like code struc-
analysis,      and     exploitation.    PentestAgent                                             ture or permissions with dynamic behaviors such as
dynamically integrates tools and adapts to diverse                                               system calls or memory usage represents a hybrid
environments, improving task completion and                                                      approach. This section discusses the role of LLMs
operational efficiency. It outperforms existing                                                  in hybrid approaches, focusing on two aspects: (i)
LLM-based penetration testing systems.                                                           LLM for unit test generation (§ V-A) and (ii) other
   As illustrated in Figure 6, penetration test-                                                 hybrid methods (§ V-B).
ing involves six stages: pre-engagement interac-
tions, reconnaissance, vulnerability identification,
                                                                                                 A. LLM for Unit Test Generation
exploitation, post-exploitation, and reporting. Pre-
engagement interactions establish objectives, define                                                Unit testing is a fundamental practice in soft-
scope, and set rules of engagement. Reconnaissance                                               ware development that focuses on verifying the
gathers target information through passive and active                                            functionality of individual components or ”units”
methods to identify attack vectors. Vulnerability                                                of a program. By isolating and testing each unit,
identification uses automated tools and manual tech-                                             developers can ensure code correctness, detect errors
niques to detect and verify weaknesses. Exploita-                                                early, and improve overall code quality. Traditional
tion leverages these vulnerabilities to demonstrate                                              unit test generation methods are written manually
potential risks, while post-exploitation assesses the                                            by developers and generally involve search-based,
breach’s impact and ensures persistence if needed.                                               constraint-based, or random techniques to maximize
Finally, reporting consolidates findings into struc-                                             code coverage [147]. Automated unit test gen-
tured documentation with risk assessments and re-                                                eration leverages tools and techniques to generate
mediation strategies.                                                                            tests automatically, reducing developer workload
                                                                                                 and improving coverage. Static analysis is essential
   Takeaway 7                                                                                    in guiding test generation by examining the pro-
                                                                                                 gram’s structure, dependencies, and control flow.
   LLMs can be applied across multiple stages                                                    Dynamic analysis complements this by evaluating
   of penetration testing. For example, LLM-                                                     the generated tests through runtime execution, iden-
   driven frameworks simplify reconnaissance                                                     tifying errors, and refining test quality. Together,
   by automating tool output interpretation and                                                  these hybrid approaches enhance the efficiency and
                                                                                                 effectiveness of unit test generation.
                                                                                                                                          17


                       Automated Test                        Post-Process &
    Source File         Generation        Test Command
                                                             Update Test File      dependencies or fail to focus on critical components
                           Prompt
                         Engineering         Run Test
                                                                                   of the code.
                                                             Existing Test Suite
 Existing Test Suite
                            LLMs
                                                                                      Dynamic Analysis-Assited Unit Test Genera-
                                             Test Pass
                                                                                   tion. Dynamic analysis complements static tech-
                                                             Coverage Report
  Coverage Report       Generated Test
                            Suite        Coverage Increase                         niques by validating and refining test cases through
                                                                                   iterative processes, improving coverage and cor-
Fig. 7: Workflow of unit test generation with LLMs.                                rectness. For example, TestART [153] uses a co-
                                                                                   evolutionary framework to iteratively generate and
                                                                                   repair tests based on runtime feedback, addressing
   Performance Comparison Between LLMs and                                         flaky or invalid tests often produced by traditional
Traditional Test Generation Tools. A study eval-                                   methods. In ChatUniTest [151], dynamic validation
uated the performance of ChatGPT and Pyn-                                          integrates runtime error detection with rule-based
guin [148] in generating unit tests for Python pro-                                and LLM-driven repair, ensuring that generated tests
grams, focusing on three types of code structures:                                 are compilable and logically sound. Furthermore,
procedural scripts, function-based modular code,                                   ChatTester [154] demonstrates how iterative prompt-
and class-based modular code. Bhatia et al. [149]                                  ing based on dynamic feedback can address missed
compared the tools in terms of coverage, correct-                                  statements and branches, progressively improving
ness, and iterative improvement through prompt                                     line and branch coverage. These dynamic techniques
engineering. They found that ChatGPT and Pynguin                                   allow LLM-based approaches to adapt and refine
achieved comparable statement and branch cover-                                    tests, addressing limitations of traditional static tools
age. Iterative prompting improved ChatGPT’s cov-                                   that lack iterative capabilities.
erage for function- and class-based code, saturating
                                                                                      Prompt Engineering. Techniques like adaptive
after four iterations, but showed no improvement for
                                                                                   focal context in ChatUniTest [151] and program
procedural scripts. The study also revealed minimal
                                                                                   slicing in HITS [155] streamline prompts by re-
overlap in missed statements, suggesting combining
                                                                                   ducing irrelevant information, ensuring the LLM
the tools could enhance coverage. However, Chat-
                                                                                   remain focused. Chain-of-thought reasoning, as seen
GPT often generated incorrect assertions, especially
                                                                                   in aster [150], enhanced the LLM’s ability to han-
for less structured code, due to its focus on natural
                                                                                   dle complex dependencies and generated logically
language over code semantics. The authors con-
                                                                                   coherent tests. Additionally, AGONETEST [156]
cluded that while LLMs like ChatGPT are promis-
                                                                                   employed structured prompts incorporating mock
ing for unit test generation, integrating semantic
                                                                                   dependencies and example inputs, guiding the LLM
understanding and combining them with traditional
                                                                                   to generate more comprehensive test cases. These
tools could address current limitations and improve
                                                                                   techniques address the inflexibility of traditional
performance.
                                                                                   tools, which often rely on predefined templates and
   Static Analysis-Assited Unit Test Generation.                                   lack the ability to dynamically adapt prompts based
One improvement is the ability of LLMs to generate                                 on code context.
focused and meaningful test cases by using static
analysis to extract and structure relevant context.                                   Takeaway 8
For instance, aster [150] and ChatUniTest [151]
integrate techniques such as dependency extrac-                                       Static and dynamic analysis operate at dis-
tion, program slicing, and adaptive focal context.                                    tinct stages in unit test generation. Static
These methods ensure that prompts sent to LLMs                                        analysis extracts dependencies and slices pro-
are concise and focused, enabling the generation                                      grams, enabling LLMs to generate targeted,
of tests that better align with the target methods.                                   logically structured tests. Dynamic analysis
Similarly, APT [152] employs a property-based ap-                                     then validates and refines these tests through
proach to guide LLMs in generating tests using                                        runtime feedback. Prompt engineering tech-
the ”Given-When-Then” paradigm, which improves                                        niques such as adaptive focal context and
logical structure in generated tests. These static anal-                              structured prompts, align test generation with
ysis techniques address the limitations of traditional                                code semantics to enhance coverage.
methods, which often struggle to extract relevant
                                                                                                             18


B. Others                                                  Malware Reverse Engineering. Williamson et
                                                        al. [162] integrated LLMs with static and dynamic
   In addition to the previously discussed methods      analysis techniques to enhance malware reverse
for unit test generation, other hybrid approaches       engineering. In the static phase, tools like IDA
integrate static and dynamic analysis through an        Pro examined binaries to extract structural details
agent framework. This framework first performs          such as embedded strings and control flow. In the
static analysis, such as extracting ASTs and ana-       dynamic phase, sandboxes monitored malware be-
lyzing code structure, and then conducts dynamic        havior, capturing network and system interactions.
testing.                                                LLMs synthesized results from both phases, deriv-
   Multi-Agent Framework for Secure Code Gen-           ing actionable insights and identifying indicators of
eration. Nunez et al. [157] introduced AutoSafe-        compromise (IoCs).
Coder, an innovative multi-agent framework de-
signed to improve the security of automatically gen-       Takeaway 9
erated code. The framework leverages three distinct
LLM-driven agents working collaboratively to gen-          LLMs enhance hybrid methods by iteratively
erate, analyze, and secure code. The Coding Agent          refining the outputs of static (e.g., AST anal-
is responsible for generating the initial code, while      ysis in AutoSafeCoder, coverage gaps in
the Static Analyzer Agent identifies potential vul-        CoverUp) and dynamic (e.g., fuzzing, runtime
nerabilities through AST analysis. Meanwhile, the          feedback) analysis process. They bridge code
Fuzzing Agent detects runtime errors by employing          structures with runtime behaviors, enabling
mutation-based fuzzing techniques, ensuring that the       secure code generation, high-coverage tests,
generated code performs securely during execution.         and actionable malware analysis.
Interactive feedback loops integrate both static and
dynamic testing methods into the code generation                         VI. D ISCUSSION
process, optimizing the outputs from the LLM at
each stage.                                                The use of LLMs in the field of program anal-
                                                        ysis has mitigated several previous limitations such
   Coverage Test Generation. Pizzorno et al. [158]
                                                        as false positives, performance overhead, inherent
presented CoverUp, a method for generating Python
                                                        knowledge barriers, path explosion, the trade-off
regression tests with high code coverage. CoverUp
                                                        between speed and accuracy, and the difficulty of
evaluates existing code coverage, identifies gaps,
                                                        achieving automation across diverse systems without
and uses LLMs to generate new tests informed
                                                        heavy manual intervention. Despite these advance-
by static analysis. If tests fail to execute or en-
                                                        ments, new limitations and challenges have emerged
hance coverage, CoverUp iteratively refines them
                                                        with the introduction of LLMs. The following sub-
using error messages and code context. This process
                                                        sections provide an overview of these challenges (§
continues until all segments are fully tested and
                                                        VI-A) and discuss potential future research direc-
integration issues are resolved.
                                                        tions (§ VI-B).
   Malware Analysis. Li et al. [122] used reverse
engineering tools to extract static and dynamic
features from Android APK files, organizing them        A. Challenges
into permissions, system calls, and metadata. They         Technical Limitations. LLMs face several tech-
used tailored prompts to guide ChatGPT in gener-        nical challenges in program analysis. First, incor-
ating textual analyses and maliciousness scores for     rect data type identification and information loss
each application. These results were compared with      during decompilation reduce analysis accuracy. Sec-
three existing Android malware detection models:        ond, LLMs often oversimplify patches, limiting
Drebin [159], MaMaDroid [160], and XMAL [161].          their ability to address vulnerabilities in real-world
Although traditional models showed strong classi-       applications. In some cases, they produce empty
fication capabilities, the authors noted their limi-    responses, particularly during software verification
tations in interpretability and dataset dependency.     and patching tasks. Third, LLMs struggle with
ChatGPT offered comprehensive analyses and ex-          variable reuse, often confusing identically named
planations but lacked decision-making capabilities.     variables in different scopes. Finally, LLMs struggle
                                                                                                            19


to analyze logic vulnerabilities involving intricate    static analysis, enabling early vulnerability
control flows, complex nesting, and time-based com-     detection without runtime execution. This reduces
petition conditions. These challenges reduce their      computational overhead, avoids repeated executions,
effectiveness in assessing such scenarios.              and improves scalability for analyzing large systems.
   Model Characteristics and Limitations.LLMs           Pei et al. [163] showed how fine-tuning LLMs
are non-deterministic and may produce varying           eliminates the need for runtime information by
outputs for identical inputs, complicating              predicting program invariants from source code,
consistency in repeated vulnerability assessments.      enabling earlier safety checks during compilation.
This variability hinders reliable and repeatable           Emulating Human Security Researchers for
results. Additionally, LLMs are prone to                Vulnerability Detection. Advancing code under-
hallucinations, generating fabricated information       standing and reasoning capabilities enable LLMs
that misleads vulnerability detection. These            to replicate systematic approaches used by human
limitations in consistency and accuracy make LLMs       security researchers. LLMs overcome the rule-based
insufficient for reliable program analysis.             limitations of traditional tools by analyzing complex
   Cost and Dependency Issues. The effectiveness        code contexts and identifying nuanced vulnerabili-
of LLM-based program analysis relies on prompt          ties. This enables LLMs to mimic hypothesis-driven
engineering, which requires significant expertise.      processes, identifying subtle vulnerabilities missed
Poorly designed prompts can lead to ineffective         by automated methods. Glazunov et al. [164] in-
results or introduce biases, limiting the model’s       troduced Project Naptime to replicate human secu-
ability to detect vulnerabilities. Furthermore, using   rity researchers’ workflows for vulnerability detec-
LLMs can be costly, especially when analyzing long      tion. The framework employs tools such as a code
code segments, due to the large number of tokens        browser, Python interpreter, and debugger, enabling
required. The inherent token limits of LLMs also        LLMs to perform expert-level code analysis and vul-
restrict their ability to handle extensive or complex   nerability detection. Evaluated on the CyberSecEval
programs, making scalability a challenge in real-       2 [165] benchmark, this approach improves detec-
world applications.                                     tion and demonstrates the feasibility of automating
                                                        complex security tasks.
B. Future Directions
                                                                        VII.   C ONCLUSION
   Deep Integration of LLMs with Analysis Tech-
niques. Most current methods use LLMs inde-                Integrating LLMs into program analysis enhances
pendently of program analysis. Integrating LLMs         vulnerability detection, code comprehension, and
with static analysis into a unified workflow offers     security assessments. LLMs’ natural language
opportunities for enhanced effectiveness. Some stud-    processing capabilities, combined with static
ies [30] have acknowledged that their methods lack      and dynamic analysis techniques have improved
effective integration of LLMs with other models         automation, scalability, and interpretability in
or techniques. Frameworks combining LLMs with           program analysis. These advancements facilitate
GNNs [38] for program control and data flow have        faster vulnerability detection and provide deeper
shown significant improvements in detection accu-       insights into software behavior. Challenges such
racy. Future work should focus on integrating LLMs      as token limitations, path explosion, complex logic
with static and dynamic analysis to create more         vulnerabilities, and LLM hallucinations remain
effective solutions for vulnerability detection.        barriers. The studies reviewed in this survey
   Transforming Dynamic Analysis into Static            highlight recent progress, offering insights into its
Analysis. Transforming tasks traditionally requiring    current state and emerging opportunities. Future di-
dynamic analysis into static analysis with LLMs         rections include developing domain-specific models,
is an emerging direction. Tasks like runtime            refining hybrid methods, and enhancing reliability
vulnerability detection and memory corruption           and interpretability to fully utilize LLMs in program
analysis historically depended on dynamic               analysis. This survey aims to assist in addressing the
analysis to capture execution-specific behaviors.       mentioned challenges and inspire the development
LLM integration can shift these processes to            of more effective program analysis frameworks.
                                                                                                                                              20


                         R EFERENCES                                       [15]   Z. Lin, X. Hu, Y. Zhang, Z. Chen, Z. Fang, X. Chen, A. Li,
                                                                                  P. Vepakomma, and Y. Gao, “Splitlora: A split parameter-
                                                                                  efficient fine-tuning framework for large language models,”
 [1]   T. Mens, M. Wermelinger, S. Ducasse, S. Demeyer,                           arXiv preprint arXiv:2407.00952, 2024.
       R. Hirschfeld, and M. Jazayeri, “Challenges in software
                                                                           [16]   P. Sharma and B. Dash, “Impact of big data analytics and chat-
       evolution,” in Eighth International Workshop on Principles
                                                                                  gpt on cybersecurity,” in 2023 4th International Conference
       of Software Evolution (IWPSE’05). IEEE, 2005, pp. 13–22.
                                                                                  on Computing and Communication Systems (I3CS). IEEE,
 [2]   H. Li, H. Kwon, J. Kwon, and H. Lee, “Clorifi: software                    2023, pp. 1–6.
       vulnerability discovery using code clone verification,” Con-
                                                                           [17]   T. Ni, Y. Du, Q. Zhao, and C. Wang, “Non-intrusive and
       currency and Computation: Practice and Experience, vol. 28,
                                                                                  unconstrained keystroke inference in vr platforms via infrared
       pp. 1900 – 1917, 2016.
                                                                                  side channel,” arXiv preprint arXiv:2412.14815, 2024.
 [3]   A. Aggarwal and P. Jalote, “Integrating static and dynamic
                                                                           [18]   T. Ni, X. Zhang, and Q. Zhao, “Recovering fingerprints from
       analysis for detecting vulnerabilities,” 30th Annual Inter-
                                                                                  in-display fingerprint sensors via electromagnetic side chan-
       national Computer Software and Applications Conference
                                                                                  nel,” in Proceedings of the 2023 ACM SIGSAC Conference on
       (COMPSAC’06), vol. 1, pp. 343–350, 2006.
                                                                                  Computer and Communications Security, 2023, pp. 253–267.
 [4]   K. Goseva-Popstojanova and A. Perhinschi, “On the capability
                                                                           [19]   T. Ni, X. Zhang, C. Zuo, J. Li, Z. Yan, W. Wang, W. Xu,
       of static code analysis to detect security vulnerabilities,” Inf.
                                                                                  X. Luo, and Q. Zhao, “Uncovering user interactions on
       Softw. Technol., vol. 68, pp. 18–33, 2015.
                                                                                  smartphones via contactless wireless charging side channels,”
 [5]   S. Siddiqui, R. Metta, and K. Madhukar, “Towards multi-                    in 2023 IEEE Symposium on Security and Privacy (SP).
       language static code analysis,” 2023 IEEE 34th International               IEEE, 2023, pp. 3399–3415.
       Symposium on Software Reliability Engineering Workshops
                                                                           [20]   Z. Fang, Z. Lin, Z. Chen, X. Chen, Y. Gao, and Y. Fang, “Au-
       (ISSREW), pp. 81–82, 2023.
                                                                                  tomated federated pipeline for parameter-efficient fine-tuning
 [6]   J. Wang, M. Huang, Y. Nie, and J. Li, “Static analysis of                  of large language models,” arXiv preprint arXiv:2404.06448,
       source code vulnerability using machine learning techniques:               2024.
       A survey,” 2021 4th International Conference on Artificial
                                                                           [21]   F. Nielson, H. R. Nielson, and C. Hankin, Principles of
       Intelligence and Big Data (ICAIBD), pp. 76–86, 2021.
                                                                                  program analysis. springer, 2015.
 [7]   B. Chernis and R. M. Verma, “Machine learning methods for
                                                                           [22]   A. K. Ashish and J. Aghav, “Automated techniques and tools
       software vulnerability detection,” Proceedings of the Fourth
                                                                                  for program analysis: Survey,” in 2013 Fourth International
       ACM International Workshop on Security and Privacy Ana-
                                                                                  Conference on Computing, Communications and Networking
       lytics, 2018.
                                                                                  Technologies (ICCCNT), 2013, pp. 1–7.
 [8]   M. Pradel and K. Sen, “Deepbugs: A learning approach
                                                                           [23]   F. Lösch, “Instrumentation of java program code for control
       to name-based bug detection,” Proceedings of the ACM on
                                                                                  flow analysis,” Ph.D. dissertation, Universitätsbibliothek der
       Programming Languages, vol. 2, no. OOPSLA, pp. 1–25,
                                                                                  Universität Stuttgart, 2005.
       2018.
                                                                           [24]   A. Vaswani, “Attention is all you need,” Advances in Neural
 [9]   D. Zou, Y. Zhu, S. Xu, Z. Li, H. Jin, and H. Ye, “Interpreting
                                                                                  Information Processing Systems, 2017.
       deep learning-based vulnerability detector predictions based
       on heuristic searching,” ACM Transactions on Software En-           [25]   M. R. Douglas, “Large language models,” Communications
       gineering and Methodology (TOSEM), vol. 30, pp. 1 – 31,                    of the ACM, vol. 66, pp. 7 – 7, 2023.
       2021.                                                               [26]   H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A.
[10]   G. Ye, Z. Tang, H. Wang, D. Fang, J. Fang, S. Huang,                       Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro,
       and Z. Wang, “Deep program structure modeling through                      F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample,
       multi-relational graph-based learning,” in Proceedings of                  “Llama: Open and efficient foundation language models,”
       the ACM International Conference on Parallel Architectures                 2023. [Online]. Available: https://arxiv.org/abs/2302.13971
       and Compilation Techniques, ser. PACT ’20. New York,                [27]   M. AI, “Codellama: Open code-focused language models,”
       NY, USA: Association for Computing Machinery, 2020,                        https://ai.meta.com/research/code-llama, 2023.
       p. 111–123. [Online]. Available: https://doi.org/10.1145/           [28]   T. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan,
       3410463.3414670                                                            P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell
[11]   T. Ahmed and P. Devanbu, “Few-shot training llms for                       et al., “Language models are few-shot learners,” in Advances
       project-specific code-summarization,” Proceedings of the 37th              in Neural Information Processing Systems, vol. 33, 2020, pp.
       IEEE/ACM International Conference on Automated Software                    1877–1901. [Online]. Available: https://arxiv.org/abs/2005.
       Engineering, 2022.                                                         14165
[12]   S. Choi, Y. K. Tan, M. H. Meng, M. Ragab, S. Mondal,                [29]   OpenAI, “Gpt-4 technical         report,”   https://openai.com/
       D. Mohaisen, and K. M. M. Aung, “I can find you in sec-                    research/gpt-4, 2023.
       onds! leveraging large language models for code authorship          [30]   H. Li, Y. Hao, Y. Zhai, and Z. Qian, “The hitchhiker’s guide
       attribution,” arXiv preprint arXiv:2501.08165, 2025.                       to program analysis: A journey with large language models,”
[13]   S. Choi and D. Mohaisen, “Attributing chatgpt-generated                    2023. [Online]. Available: https://arxiv.org/abs/2308.00245
       source codes,” IEEE Transactions on Dependable and Secure           [31]   J. Ye, X. Fei, X. de Carné de Carnavalet, L. Zhao, L. Wu,
       Computing, 2025.                                                           and M. Zhang, “Detecting command injection vulnerabilities
[14]   Z. Lin, G. Qu, Q. Chen, X. Chen, Z. Chen, and K. Huang,                    in linux-based embedded firmware with llm-based taint
       “Pushing large language models to the 6g edge: Vision, chal-               analysis of library functions,” Computers & Security, vol.
       lenges, and opportunities,” arXiv preprint arXiv:2309.16739,               144, p. 103971, 2024. [Online]. Available: https://www.
       2023.                                                                      sciencedirect.com/science/article/pii/S0167404824002761
                                                                                                                                           21


[32]   P. Liu, C. Sun, Y. Zheng, X. Feng, C. Qin, Y. Wang,                      detection: New perspectives,” 2023. [Online]. Available:
       Z. Li, and L. Sun, “Harnessing the power of llm to                       https://arxiv.org/abs/2310.01152
       support binary taint analysis,” 2023. [Online]. Available:        [46]   J. Xiang, L. Fu, T. Ye, P. Liu, H. Le, L. Zhu, and W. Wang,
       https://arxiv.org/abs/2310.08275                                         “Luataint: A static analysis system for web configuration
[33]   D. Liu, Z. Lu, S. Ji, K. Lu, J. Chen, Z. Liu, D. Liu,                    interface vulnerability of internet of things devices,” 2024.
       R. Cai, and Q. He, “Detecting kernel memory bugs through                 [Online]. Available: https://arxiv.org/abs/2402.16043
       inconsistent memory management intention inferences,” in          [47]   Y. Chen, R. Tang, C. Zuo, X. Zhang, L. Xue, X. Luo, and
       33rd USENIX Security Symposium (USENIX Security 24).                     Q. Zhao, “Attention! your copied data is under monitoring:
       Philadelphia, PA: USENIX Association, Aug. 2024, pp. 4069–               A systematic study of clipboard usage in android apps,” in
       4086. [Online]. Available: https://www.usenix.org/conference/            Proceedings of the 46th IEEE/ACM International Conference
       usenixsecurity24/presentation/liu-dinghao-detecting                      on Software Engineering, 2024, pp. 1–13.
[34]   J. Wang, Z. Huang, H. Liu, N. Yang, and Y. Xiao,                  [48]   H. Lu, Q. Zhao, Y. Chen, X. Liao, and Z. Lin, “Detecting
       “Defecthunter: A novel llm-driven boosted-conformer-based                and measuring aggressive location harvesting in mobile apps
       code vulnerability detection mechanism,” 2023. [Online].                 via data-flow path embedding,” Proceedings of the ACM on
       Available: https://arxiv.org/abs/2309.15324                              Measurement and Analysis of Computing Systems, vol. 7,
[35]   Z. Li, S. Dutta, and M. Naik, “Llm-assisted static analysis for          no. 1, pp. 1–27, 2023.
       detecting security vulnerabilities,” 2024. [Online]. Available:   [49]   Q. Zhao, C. Zuo, G. Pellegrino, and Z. Lin, “Geo-locating
       https://arxiv.org/abs/2405.17238                                         drivers: A study of sensitive data leakage in ride-hailing
[36]   Y. Cheng, L. K. Shar, T. Zhang, S. Yang, C. Dong, D. Lo,                 services,” in 26th Annual Network and Distributed System
       S. Lv, Z. Shi, and L. Sun, “Llm-enhanced static analysis                 Security Symposium (NDSS 2019). Internet Society, 2019.
       for precise identification of vulnerable oss versions,” 2024.     [50]   Q. Zhao, H. Wen, Z. Lin, D. Xuan, and N. Shroff, “On the
       [Online]. Available: https://arxiv.org/abs/2408.07321                    accuracy of measured proximity of bluetooth-based contact
[37]   Z. Mao, J. Li, D. Jin, M. Li, and K. Tei, “Multi-role consensus          tracing apps,” in Security and Privacy in Communication
       through llms discussions for vulnerability detection,” 2024.             Networks: 16th EAI International Conference, SecureComm
       [Online]. Available: https://arxiv.org/abs/2403.14274                    2020, Washington, DC, USA, October 21-23, 2020, Proceed-
                                                                                ings, Part I 16. Springer, 2020, pp. 49–60.
[38]   A. Z. H. Yang, H. Tian, H. Ye, R. Martins, and C. L.
                                                                         [51]   T. Ni, G. Lan, J. Wang, Q. Zhao, and W. Xu, “Eavesdropping
       Goues, “Security vulnerability detection with multitask
                                                                                mobile app activity via {Radio-Frequency} energy harvest-
       self-instructed fine-tuning of large language models,” 2024.
                                                                                ing,” in 32nd USENIX Security Symposium (USENIX Security
       [Online]. Available: https://arxiv.org/abs/2406.05892
                                                                                23), 2023, pp. 3511–3528.
[39]   Y. Sun, D. Wu, Y. Xue, H. Liu, H. Wang, Z. Xu, X. Xie,
                                                                         [52]   T. Ni, J. Li, X. Zhang, C. Zuo, W. Wang, W. Xu, X. Luo,
       and Y. Liu, “Gptscan: Detecting logic vulnerabilities in
                                                                                and Q. Zhao, “Exploiting contactless side channels in wireless
       smart contracts by combining gpt with program analysis,”
                                                                                charging power banks for user privacy inference via few-shot
       in Proceedings of the IEEE/ACM 46th International
                                                                                learning,” in Proceedings of the 29th Annual International
       Conference on Software Engineering, ser. ICSE ’24.
                                                                                Conference on Mobile Computing and Networking, 2023, pp.
       ACM, Apr. 2024, p. 1–13. [Online]. Available: http:
                                                                                1–15.
       //dx.doi.org/10.1145/3597503.3639117
                                                                         [53]   T. Ni, Y. Chen, W. Xu, L. Xue, and Q. Zhao, “Xporter: A
[40]   Y. Yang, “Iot software vulnerability detection techniques                study of the multi-port charger security on privacy leakage
       through large language model,” in Formal Methods and                     and voice injection,” in Proceedings of the 29th Annual Inter-
       Software Engineering: 24th International Conference on                   national Conference on Mobile Computing and Networking,
       Formal Engineering Methods, ICFEM 2023, Brisbane, QLD,                   2023, pp. 1–15.
       Australia, November 21–24, 2023, Proceedings. Berlin,
       Heidelberg: Springer-Verlag, 2023, p. 285–290. [Online].          [54]   T. Ni, “Sensor security in virtual reality: Exploration and
       Available: https://doi.org/10.1007/978-981-99-7584-6 21                  mitigation,” in Proceedings of the 22nd Annual International
                                                                                Conference on Mobile Systems, Applications and Services,
[41]   N. S. Mathews, Y. Brus, Y. Aafer, M. Nagappan, and                       2024, pp. 758–759.
       S. McIntosh, “Llbezpeky: Leveraging large language models
       for vulnerability detection,” 2024. [Online]. Available:          [55]   Q. Zhao, C. Zuo, B. Dolan-Gavitt, G. Pellegrino, and Z. Lin,
       https://arxiv.org/abs/2401.01269                                         “Automatic uncovering of hidden behaviors from input vali-
                                                                                dation in mobile apps,” in 2020 IEEE Symposium on Security
[42]   M. M. Mohajer, R. Aleithan, N. S. Harzevili, M. Wei, A. B.               and Privacy (SP). IEEE, 2020, pp. 1106–1120.
       Belle, H. V. Pham, and S. Wang, “Skipanalyzer: A tool
                                                                         [56]   H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A.
       for static code analysis with large language models,” 2023.
                                                                                Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro,
       [Online]. Available: https://arxiv.org/abs/2310.18532
                                                                                F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample,
[43]   S. Yang, X. Lin, J. Chen, Q. Zhong, L. Xiao, R. Huang,                   “Llama: Open and efficient foundation language models,”
       Y. Wang, and Z. Zheng, “Hyperion: Unveiling dapp                         2023. [Online]. Available: https://arxiv.org/abs/2302.13971
       inconsistencies using llm and dataflow-guided symbolic
                                                                         [57]   S. Yuan, H. Li, X. Han, G. Xu, W. Jiang, T. Ni, Q. Zhao, and
       execution,” 2024. [Online]. Available: https://arxiv.org/abs/
                                                                                Y. Fang, “Itpatch: An invisible and triggered physical adver-
       2408.06037
                                                                                sarial patch against traffic sign recognition,” arXiv preprint
[44]   C. Zhang, H. Liu, J. Zeng, K. Yang, Y. Li, and H. Li, “Prompt-           arXiv:2409.12394, 2024.
       enhanced software vulnerability detection using chatgpt,”         [58]   Y. Chen, T. Ni, W. Xu, and T. Gu, “Swipepass: Acoustic-
       2024. [Online]. Available: https://arxiv.org/abs/2308.12697              based second-factor user authentication for smartphones,”
[45]   S. Hu, T. Huang, F. İlhan, S. F. Tekin, and L. Liu,                     Proceedings of the ACM on Interactive, Mobile, Wearable and
       “Large language model-powered smart contract vulnerability               Ubiquitous Technologies, vol. 6, no. 3, pp. 1–25, 2022.
                                                                                                                                           22


[59]   Q. Zhao, C. Zuo, J. Blasco, and Z. Lin, “Periscope: Compre-             C. Bamford, D. S. Chaplot, D. de las Casas, E. B. Hanna,
       hensive vulnerability analysis of mobile app-defined bluetooth          F. Bressand, G. Lengyel, G. Bour, G. Lample, L. R. Lavaud,
       peripherals,” in Proceedings of the 2022 ACM on Asia Con-               L. Saulnier, M.-A. Lachaux, P. Stock, S. Subramanian,
       ference on Computer and Communications Security, 2022, pp.              S. Yang, S. Antoniak, T. L. Scao, T. Gervet, T. Lavril,
       521–533.                                                                T. Wang, T. Lacroix, and W. E. Sayed, “Mixtral of experts,”
[60]   D. Guo, S. Lu, N. Duan, Y. Wang, M. Zhou, and                           2024. [Online]. Available: https://arxiv.org/abs/2401.04088
       J. Yin, “Unixcoder: Unified cross-modal pre-training for         [74]   N. Zahan, P. Burckhardt, M. Lysenko, F. Aboukhadijeh,
       code representation,” 2022. [Online]. Available: https:                 and L. Williams, “Shifting the lens: Detecting malicious
       //arxiv.org/abs/2203.03850                                              npm packages using large language models,” 2024. [Online].
[61]   B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E.          Available: https://arxiv.org/abs/2403.12196
       Tan, Y. Adi, J. Liu, R. Sauvestre, T. Remez, J. Rapin,           [75]   GitHub, “Codeql: Github’s static analysis engine for code
       A. Kozhevnikov, I. Evtimov, J. Bitton, M. Bhatt, C. C.                  vulnerabilities,” https://codeql.github.com/, 2025, accessed:
       Ferrer, A. Grattafiori, W. Xiong, A. Défossez, J. Copet,               January 15, 2025.
       F. Azhar, H. Touvron, L. Martin, N. Usunier, T. Scialom,         [76]   I. Khan and Y.-W. Kwon, “A structural-semantic approach
       and G. Synnaeve, “Code llama: Open foundation models for                integrating graph-based and large language models represen-
       code,” 2024. [Online]. Available: https://arxiv.org/abs/2308.           tation to detect android malware,” in ICT Systems Security and
       12950                                                                   Privacy Protection, N. Pitropakis, S. Katsikas, S. Furnell, and
[62]   O. A. Aslan and R. Samet, “A comprehensive review on                    K. Markantonakis, Eds. Cham: Springer Nature Switzerland,
       malware detection approaches,” IEEE Access, vol. 8, pp.                 2024, pp. 279–293.
       6249–6271, 2020.                                                 [77]   Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng, M. Gong,
[63]   H. Alasmary, A. Anwar, J. Park, J. Choi, D. Nyang, and                  L. Shou, B. Qin, T. Liu, D. Jiang, and M. Zhou, “Codebert: A
       A. Mohaisen, “Graph-based comparison of iot and android                 pre-trained model for programming and natural languages,”
       malware,” in Computational Data and Social Networks, 2018,              2020. [Online]. Available: https://arxiv.org/abs/2002.08155
       pp. 259–272.                                                     [78]   W. Zhao, J. Wu, and Z. Meng, “Apppoet: Large language
[64]   F. Shen, J. Del Vecchio, A. Mohaisen, S. Y. Ko, and L. Ziarek,          model based android malware detection via multi-view
       “Android malware detection using complex-flows,” IEEE                   prompt engineering,” 2024. [Online]. Available: https:
       Transactions on Mobile Computing, vol. 18, no. 6, pp. 1231–             //arxiv.org/abs/2404.18816
       1245, 2018.                                                      [79]   A. Kozyrev, G. Solovev, N. Khramov, and A. Podkopaev,
[65]   H. Alasmary, A. Khormali, A. Anwar, J. Park, J. Choi,                   “Coqpilot, a plugin for llm-based generation of proofs,” 10
       A. Abusnaina, A. Awad, D. Nyang, and A. Mohaisen, “An-                  2024, pp. 2382–2385.
       alyzing and detecting emerging internet of things malware:       [80]   L. Zhang, S. Lu, and N. Duan, “Selene: Pioneering automated
       A graph-based approach,” IEEE Internet of Things Journal,               proof in software verification,” 2024. [Online]. Available:
       vol. 6, no. 5, pp. 8977–8988, 2019.                                     https://arxiv.org/abs/2401.07663
[66]   H. Kang, J.-w. Jang, A. Mohaisen, and H. K. Kim, “De-            [81]   S. Chakraborty, S. K. Lahiri, S. Fakhoury, M. Musuvathi,
       tecting and classifying android malware using static analysis           A. Lal, A. Rastogi, A. Senthilnathan, R. Sharma, and
       along with creator information,” International Journal of               N. Swamy, “Ranking llm-generated loop invariants for
       Distributed Sensor Networks, vol. 11, no. 6, p. 479174, 2015.           program verification,” 2024. [Online]. Available: https:
[67]   A. Mohaisen, O. Alrawi, and M. Mohaisen, “Amal: high-                   //arxiv.org/abs/2310.09342
       fidelity, behavior-based automated malware analysis and clas-    [82]   C. Janßen, C. Richter, and H. Wehrheim, “Can chatgpt
       sification,” computers & security, vol. 52, pp. 251–266, 2015.          support software verification?” 2023. [Online]. Available:
[68]   S. Fujii and R. Yamagishi, “Feasibility study for supporting            https://arxiv.org/abs/2311.02433
       static malware analysis using llm,” 2024. [Online]. Available:   [83]   M. A. A. Pirzada, G. Reger, A. Bhayat, and L. C.
       https://arxiv.org/abs/2411.14905                                        Cordeiro, “Llm-generated invariants for bounded model
[69]   M. Post, “A call for clarity in reporting bleu scores,” 2018.           checking without loop unrolling,” in Proceedings of the
       [Online]. Available: https://arxiv.org/abs/1804.08771                   39th IEEE/ACM International Conference on Automated
                                                                               Software Engineering, ser. ASE ’24. New York, NY, USA:
[70]   K. Ganesan, “Rouge 2.0: Updated and improved measures                   Association for Computing Machinery, 2024, p. 1395–1407.
       for evaluation of summarization tasks,” 2018. [Online].                 [Online]. Available: https://doi.org/10.1145/3691620.3695512
       Available: https://arxiv.org/abs/1803.01937
                                                                        [84]   G. Wu, W. Cao, Y. Yao, H. Wei, T. Chen, and
[71]   C.-A. Simion, G. Balan, and D. T. GavriluŢ, “Benchmarking              X. Ma, “Llm meets bounded model checking: Neuro-
       out of the box open-source llms for malware detection based             symbolic loop invariant inference,” in Proceedings of the
       on api calls sequences,” in Intelligent Data Engineering and            39th IEEE/ACM International Conference on Automated
       Automated Learning – IDEAL 2024, V. Julian, D. Camacho,                 Software Engineering, ser. ASE ’24. New York, NY, USA:
       H. Yin, J. M. Alberola, V. B. Nogueira, P. Novais, and                  Association for Computing Machinery, 2024, p. 406–417.
       A. Tallón-Ballesteros, Eds. Cham: Springer Nature Switzer-             [Online]. Available: https://doi.org/10.1145/3691620.3695014
       land, 2025, pp. 133–142.
                                                                        [85]   K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can
[72]   A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford,                    large language models reason about program invariants?”
       D. S. Chaplot, D. de las Casas, F. Bressand, G. Lengyel,                in Proceedings of the 40th International Conference on
       G. Lample, L. Saulnier, L. R. Lavaud, M.-A. Lachaux,                    Machine Learning, ser. Proceedings of Machine Learning
       P. Stock, T. L. Scao, T. Lavril, T. Wang, T. Lacroix,                   Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt,
       and W. E. Sayed, “Mistral 7b,” 2023. [Online]. Available:               S. Sabato, and J. Scarlett, Eds., vol. 202. PMLR,
       https://arxiv.org/abs/2310.06825                                        23–29 Jul 2023, pp. 27 496–27 520. [Online]. Available:
[73]   A. Q. Jiang, A. Sablayrolles, A. Roux, A. Mensch, B. Savary,            https://proceedings.mlr.press/v202/pei23a.html
                                                                                                                                           23


 [86]   C. Wen, J. Cao, J. Su, Z. Xu, S. Qin, M. He, H. Li, S.-C.                J. Signoles, and N. Williams, “The dogged pursuit of
        Cheung, and C. Tian, “Enchanting program specification                   bug-free c programs: the frama-c software analysis platform,”
        synthesis by large language models using static analysis                 Commun. ACM, vol. 64, no. 8, p. 56–68, Jul. 2021. [Online].
        and program verification,” in Computer Aided Verification:               Available: https://doi.org/10.1145/3470569
        36th International Conference, CAV 2024, Montreal, QC,           [101]   D. Beyer and M. E. Keremoglu, “Cpachecker: A tool for
        Canada, July 24–27, 2024, Proceedings, Part II. Berlin,                  configurable software verification,” in Computer Aided Ver-
        Heidelberg: Springer-Verlag, 2024, p. 302–328. [Online].                 ification, G. Gopalakrishnan and S. Qadeer, Eds. Berlin,
        Available: https://doi.org/10.1007/978-3-031-65630-9 16                  Heidelberg: Springer Berlin Heidelberg, 2011, pp. 184–190.
 [87]   H. Wu, C. Barrett, and N. Narodytska, “Lemur: Integrating        [102]   M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant,
        large language models in automated program verification,”                C. Pacheco, M. S. Tschantz, and C. Xiao, “The daikon
        2024. [Online]. Available: https://arxiv.org/abs/2310.04870              system for dynamic detection of likely invariants,” Science
 [88]   P. Mukherjee and B. Delaware, “Towards automated                         of Computer Programming, vol. 69, no. 1, pp. 35–45,
        verification of llm-synthesized c programs,” 2024. [Online].             2007, special issue on Experimental Software and Toolkits.
        Available: https://arxiv.org/abs/2410.14835                              [Online]. Available: https://www.sciencedirect.com/science/
 [89]   Y. Liu, Y. Xue, D. Wu, Y. Sun, Y. Li, M. Shi, and                        article/pii/S016764230700161X
        Y. Liu, “Propertygpt: Llm-driven formal verification of smart    [103]   R. Menezes, M. Aldughaim, B. Farias, X. Li, E. Manino,
        contracts through retrieval-augmented property generation,”              F. Shmarov, K. Song, F. Brauße, M. R. Gadelha, N. Tihanyi,
        2024. [Online]. Available: https://arxiv.org/abs/2405.02580              K. Korovin, and L. C. Cordeiro, “Esbmc v7.4: Harnessing
 [90]   W. Wang, K. Liu, A. R. Chen, G. Li, Z. Jin, G. Huang, and                the power of intervals,” 2023. [Online]. Available: https:
        L. Ma, “Python symbolic execution with llm-powered code                  //arxiv.org/abs/2312.14746
        generation,” 2024. [Online]. Available: https://arxiv.org/abs/   [104]   A. Gurfinkel, T. Kahsai, A. Komuravelli, and J. A. Navas,
        2409.09271                                                               “The seahorn verification framework,” in Computer Aided
 [91]   J. Su, L. Deng, C. Wen, S. Qin, and C. Tian,                             Verification, D. Kroening and C. S. Păsăreanu, Eds. Cham:
        “Cfstra: Enhancing configurable program analysis through                 Springer International Publishing, 2015, pp. 343–361.
        llm-driven strategy selection based on code features,”           [105]   P. Darke, S. Agrawal, and R. Venkatesh, “Veriabs: A
        in Theoretical Aspects of Software Engineering: 18th                     tool for scalable verification by abstraction (competition
        International Symposium, TASE 2024, Guiyang, China, July                 contribution),” in Tools and Algorithms for the Construction
        29 – August 1, 2024, Proceedings. Berlin, Heidelberg:                    and Analysis of Systems: 27th International Conference,
        Springer-Verlag, 2024, p. 374–391. [Online]. Available:                  TACAS 2021, Held as Part of the European Joint
        https://doi.org/10.1007/978-3-031-64626-3 22                             Conferences on Theory and Practice of Software, ETAPS
 [92]   P. J. Chapman, C. Rubio-González, and A. V. Thakur,                     2021, Luxembourg City, Luxembourg, March 27 – April 1,
        “Interleaving static analysis and llm prompting,” in                     2021, Proceedings, Part II. Berlin, Heidelberg: Springer-
        Proceedings of the 13th ACM SIGPLAN International                        Verlag, 2021, p. 458–462. [Online]. Available: https:
        Workshop on the State Of the Art in Program Analysis,                    //doi.org/10.1007/978-3-030-72013-1 32
        ser. SOAP 2024. New York, NY, USA: Association for               [106]   D. Kroening and M. Tautschnig, “Cbmc – c bounded model
        Computing Machinery, 2024, p. 9–17. [Online]. Available:                 checker,” in Tools and Algorithms for the Construction and
        https://doi.org/10.1145/3652588.3663317                                  Analysis of Systems, E. Ábrahám and K. Havelund, Eds.
 [93]   Anthropic, “Claude,” https://www.anthropic.com/claude,                   Berlin, Heidelberg: Springer Berlin Heidelberg, 2014, pp.
        2025, accessed: January 16, 2025.                                        389–391.
 [94]   z. Czajka and C. Kaliszyk, “Hammer for coq: Automation           [107]   M. Heizmann, J. Christ, D. Dietsch, E. Ermis, J. Hoenicke,
        for dependent type theory,” J. Autom. Reason., vol. 61,                  M. Lindenmann, A. Nutz, C. Schilling, and A. Podelski, “Ul-
        no. 1–4, p. 423–453, Jun. 2018. [Online]. Available:                     timate automizer with smtinterpol,” in Tools and Algorithms
        https://doi.org/10.1007/s10817-018-9458-4                                for the Construction and Analysis of Systems, N. Piterman
                                                                                 and S. A. Smolka, Eds. Berlin, Heidelberg: Springer Berlin
 [95]   L. Blaauwbroek, J. Urban, and H. Geuvers, The Tactician:
                                                                                 Heidelberg, 2013, pp. 641–643.
        A Seamless, Interactive Tactic Learner and Prover for Coq.
        Springer International Publishing, 2020, p. 271–277. [Online].   [108]   L. De Moura and N. Bjørner, “Z3: an efficient smt solver,” in
        Available: http://dx.doi.org/10.1007/978-3-030-53518-6 17                Proceedings of the Theory and Practice of Software, 14th In-
                                                                                 ternational Conference on Tools and Algorithms for the Con-
 [96]   G. Klein, J. Andronick, K. Elphinstone, T. Murray,
                                                                                 struction and Analysis of Systems, ser. TACAS’08/ETAPS’08.
        T. Sewell, R. Kolanski, and G. Heiser, “Comprehensive
                                                                                 Berlin, Heidelberg: Springer-Verlag, 2008, p. 337–340.
        formal verification of an os microkernel,” ACM Trans.
        Comput. Syst., vol. 32, no. 1, Feb. 2014. [Online]. Available:   [109]   J. Lu, L. Yu, X. Li, L. Yang, and C. Zuo, “Llama-
        https://doi.org/10.1145/2560537                                          reviewer: Advancing code review automation with large
                                                                                 language models through parameter-efficient fine-tuning,” in
 [97]   T. S. Group, “sel4: The world’s first operating-system kernel
                                                                                 2023 IEEE 34th International Symposium on Software
        with an end-to-end proof of implementation correctness,”
                                                                                 Reliability Engineering (ISSRE).      Los Alamitos, CA,
        https://sel4.systems/, n.d., accessed: 2025-01-18.
                                                                                 USA: IEEE Computer Society, oct 2023, pp. 647–658.
 [98]   D. Beyer, Competition on Software Verification and Witness               [Online]. Available: https://doi.ieeecomputersociety.org/10.
        Validation: SV-COMP 2023, 04 2023, pp. 495–522.                          1109/ISSRE59848.2023.00026
 [99]   P. Baudin, J.-C. Filliâtre, C. Marché, B. Monate, Y. Moy,      [110]   H. Dhulipala, A. Yadavally, and T. N. Nguyen, “Planning
        and V. Prevosto, ACSL: ANSI/ISO C Specification Language.                to guide llm for code coverage prediction,” in Proceedings
        [Online]. Available: http://frama-c.com/download/acsl.pdf                of the 2024 IEEE/ACM First International Conference
[100]   P. Baudin, F. Bobot, D. Bühler, L. Correnson, F. Kirchner,              on AI Foundation Models and Software Engineering, ser.
        N. Kosmatov, A. Maroneze, V. Perrelle, V. Prevosto,                      FORGE ’24. New York, NY, USA: Association for
                                                                                                                                             24


        Computing Machinery, 2024, p. 24–34. [Online]. Available:        [125]    Google, “Bard,” 2023, accessed: 2024-12-09. [Online].
        https://doi.org/10.1145/3650105.3652292                                   Available: https://bard.google.com
[111]   P. Hu, R. Liang, and K. Chen, “Degpt: Optimizing decompiler      [126]    J. Eom, S. Jeong, and T. Kwon, “Covrl: Fuzzing javascript
        output with llm,” Proceedings 2024 Network and Distributed                engines with coverage-guided reinforcement learning for
        System Security Symposium, 2024. [Online]. Available:                     llm-based mutation,” 2024. [Online]. Available: https:
        https://api.semanticscholar.org/CorpusID:267622140                        //arxiv.org/abs/2402.12222
[112]   J. Yan, J. Huang, C. Fang, J. Yan, and J. Zhang,                 [127]    H. Zhang, Y. Rong, Y. He, and H. Chen, “Llamafuzz: Large
        “Better debugging: Combining static analysis and llms                     language model enhanced greybox fuzzing,” 2024. [Online].
        for explainable crashing fault localization,” 2024. [Online].             Available: https://arxiv.org/abs/2406.07714
        Available: https://arxiv.org/abs/2408.12070                      [128]    Y. Deng, C. S. Xia, C. Yang, S. D. Zhang, S. Yang, and
[113]   D. Pomian, A. Bellur, M. Dilhara, Z. Kurbatova,                           L. Zhang, “Large language models are edge-case fuzzers:
        E. Bogomolov, T. Bryksin, and D. Dig, “Together                           Testing deep learning libraries via fuzzgpt,” 2023. [Online].
        we go further: Llms and ide static analysis for                           Available: https://arxiv.org/abs/2304.02014
        extract method refactoring,” 2024. [Online]. Available:          [129]    J. Hu, Q. Zhang, and H. Yin, “Augmenting greybox
        https://arxiv.org/abs/2401.15298                                          fuzzing with generative ai,” 2023. [Online]. Available:
[114]   H. Rong, Y. Duan, H. Zhang, X. Wang, H. Chen, S. Duan, and                https://arxiv.org/abs/2306.06782
        S. Wang, “Disassembling obfuscated executables with llm,”        [130]    C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen,
        2024. [Online]. Available: https://arxiv.org/abs/2407.08924               “Codamosa: Escaping coverage plateaus in test generation
[115]   H. Wang, Z. Wang, and P. Liu, “A hybrid llm workflow                      with pre-trained large language models,” in Proceedings of
        can help identify user privilege related variables in                     the 45th International Conference on Software Engineering,
        programs of any size,” 2024. [Online]. Available: https:                  ser. ICSE ’23. IEEE Press, 2023, p. 919–931. [Online].
        //arxiv.org/abs/2403.15723                                                Available: https://doi.org/10.1109/ICSE48619.2023.00085
[116]   C. Wen, Y. Cai, B. Zhang, J. Su, Z. Xu, D. Liu, S. Qin,          [131]    R. Meng, M. Mirchev, M. Böhme, and A. Roychoudhury,
        Z. Ming, and T. Cong, “Automatically inspecting thousands of              “Large language model guided protocol fuzzing,” in Pro-
        static bug warnings with large language model: How far are                ceedings of the 31st Annual Network and Distributed System
        we?” ACM Trans. Knowl. Discov. Data, vol. 18, no. 7, Jun.                 Security Symposium (NDSS), 2024.
        2024. [Online]. Available: https://doi.org/10.1145/3653718        [132]   Y. Oliinyk, M. Scott, R. Tsang, C. Fang, H. Homayoun
[117]   L.    Flynn    and    W.     Klieber,     “Using    llms     to           et al., “Fuzzing busybox: Leveraging llm and crash reuse for
        automate static-analysis adjudication and rationales,”                    embedded bug unearthing,” arXiv preprint arXiv:2403.03897,
        CrossTalk:    The     Journal      of    Defense      Software            2024.
        Engineering,    May     2024,      pre-publication     version.   [133]   C. S. Xia, M. Paltenghi, J. L. Tian, M. Pradel, and L. Zhang,
        [Online].   Available:    https://insights.sei.cmu.edu/library/           “Fuzz4all: Universal fuzzing with large language models,”
        using-llms-to-automate-static-analysis-adjudication-and-rationales/       2024. [Online]. Available: https://arxiv.org/abs/2308.04748
[118]   Y. Hao, W. Chen, Z. Zhou, and W. Cui, “E&v: Prompting            [134]    ICMAB-CSIC, “Siesta,” 2023, accessed: 2024-12-09.
        large language models to perform static analysis by pseudo-               [Online]. Available: https://departments.icmab.es/leem/siesta/
        code execution and verification,” 2023. [Online]. Available:
        https://arxiv.org/abs/2312.08477                                 [135]    M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto,
                                                                                  J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman,
[119]   P. Yan, S. Tan, M. Wang, and J. Huang, “Prompt                            A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry,
        engineering-assisted malware dynamic analysis using gpt-4,”               P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov,
        2023. [Online]. Available: https://arxiv.org/abs/2312.08317               A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P.
[120]   Y. S. Sun, Z.-K. Chen, Y.-T. Huang, and M. C. Chen,                       Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes,
        “ Unleashing Malware Analysis and Understanding With                      A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak,
        Generative AI ,” IEEE Security & Privacy, vol. 22,                        J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders,
        no. 03, pp. 12–23, May 2024. [Online]. Available: https:                  C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra,
        //doi.ieeecomputersociety.org/10.1109/MSEC.2024.3384415                   E. Morikawa, A. Radford, M. Knight, M. Brundage,
[121]   P. M. S. Sánchez, A. H. Celdrán, G. Bovet, and G. M. Pérez,            M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei,
        “Transfer learning in pre-trained large language models for               S. McCandlish, I. Sutskever, and W. Zaremba, “Evaluating
        malware detection based on system calls,” 2024. [Online].                 large language models trained on code,” 2021. [Online].
        Available: https://arxiv.org/abs/2405.09318                               Available: https://arxiv.org/abs/2107.03374
[122]   Y. Li, S. Fang, T. Zhang, and H. Cai, “Enhancing                 [136]    E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou,
        android malware detection: The influence of chatgpt on                    S. Savarese, and C. Xiong, “Codegen: An open large
        decision-centric task,” 2024. [Online]. Available: https:                 language model for code with multi-turn program synthesis,”
        //arxiv.org/abs/2410.04352                                                2023. [Online]. Available: https://arxiv.org/abs/2203.13474
[123]   F. Qiu, P. Ji, B. Hua, and Y. Wang, “Chemfuzz: Large             [137]    A. Fioraldi, D. Maier, H. Eißfeldt, and M. Heuse, “AFL++
        language models-assisted fuzzing for quantum chemistry                    : Combining incremental steps of fuzzing research,” in 14th
        software bug detection,” 2023 IEEE 23rd International                     USENIX Workshop on Offensive Technologies (WOOT 20).
        Conference on Software Quality, Reliability, and Security                 USENIX Association, Aug. 2020. [Online]. Available: https:
        Companion (QRS-C), pp. 103–112, 2023. [Online]. Available:                //www.usenix.org/conference/woot20/presentation/fioraldi
        https://api.semanticscholar.org/CorpusID:267771438               [138]    N. Wells, “Busybox: A swiss army knife for linux,” Linux
[124]   Anthropic, “Claude-2,” 2023, accessed: 2024-12-09. [Online].              Journal, vol. 2000, no. 78es, pp. 10–es, 2000.
        Available: https://www.anthropic.com/index/claude-2              [139]    B. Arkin, S. Stender, and G. McGraw, “Software penetration
                                                                                                                                               25


        testing,” IEEE Security & Privacy, vol. 3, no. 1, pp. 84–87,               “Llm-based unit test generation via property retrieval,” 2024.
        2005.                                                                      [Online]. Available: https://arxiv.org/abs/2410.13542
[140]   G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li,                [153]   S. Gu, Q. Zhang, C. Fang, F. Tian, L. Zhu, J. Zhou,
        Y. Xu, T. Zhang, Y. Liu, M. Pinzger, and S. Rass,                          and Z. Chen, “Testart: Improving llm-based unit testing via
        “PentestGPT: Evaluating and harnessing large language                      co-evolution of automated generation and repair iteration,”
        models for automated penetration testing,” in 33rd                         2024. [Online]. Available: https://arxiv.org/abs/2408.03095
        USENIX Security Symposium (USENIX Security 24).                    [154]   Z. Yuan, Y. Lou, M. Liu, S. Ding, K. Wang, Y. Chen, and
        Philadelphia, PA: USENIX Association, Aug. 2024, pp. 847–                  X. Peng, “No more manual tests? evaluating and improving
        864. [Online]. Available: https://www.usenix.org/conference/               chatgpt for unit test generation,” 2024. [Online]. Available:
        usenixsecurity24/presentation/deng                                         https://arxiv.org/abs/2305.04207
[141]   J. Huang and Q. Zhu, “Penheal: A two-stage                         [155]   Z. Wang, K. Liu, G. Li, and Z. Jin, “Hits: High-coverage
        llm    framework    for   automated      pentesting     and                llm-based unit test generation via method slicing,” 2024.
        optimal     remediation,”     https://synthical.com/article/               [Online]. Available: https://arxiv.org/abs/2408.11324
        655e0b6b-8ece-4830-bb82-649bac33bd5e, 6 2024.                      [156]   A. Lops, F. Narducci, A. Ragone, M. Trizio, and C. Bartolini,
[142]   D. Goyal, S. Subramanian, and A. Peela, “Hacking, the lazy                 “A system for automated unit test generation using large
        way: Llm augmented pentesting,” 2024. [Online]. Available:                 language models and assessment of generated test suites,”
        https://arxiv.org/abs/2409.09493                                           2024. [Online]. Available: https://arxiv.org/abs/2408.07846
[143]   S. G. Bianou and R. G. Batogna, “Pentest-ai, an llm-powered        [157]   A. Nunez, N. T. Islam, S. Jha, and P. Najafirad, “Autosafe-
        multi-agents framework for penetration testing automation                  coder: A multi-agent framework for securing llm code gen-
        leveraging mitre attack,” in 2024 IEEE International Con-                  eration through static analysis and fuzz testing,” 09 2024.
        ference on Cyber Security and Resilience (CSR), 2024, pp.          [158]   J. A. Pizzorno and E. D. Berger, “Coverup: Coverage-
        763–770.                                                                   guided llm-based test generation,” 2024. [Online]. Available:
[144]   L. Muzsai, D. Imolai, and A. Lukács, “Hacksynth: Llm                      https://arxiv.org/abs/2403.16218
        agent and evaluation framework for autonomous penetration          [159]   R. Kumar, Z. Xiaosong, R. U. Khan, J. Kumar, and I. Ahad,
        testing,” 2024. [Online]. Available: https://arxiv.org/abs/2412.           “Effective and explainable detection of android malware
        01778                                                                      based on machine learning algorithms,” in Proceedings
[145]   L. Gioacchini, M. Mellia, I. Drago, A. Delsanto,                           of the 2018 International Conference on Computing and
        G. Siracusano, and R. Bifulco, “Autopenbench:                              Artificial Intelligence, ser. ICCAI ’18. New York, NY,
        Benchmarking generative agents for penetration testing,”                   USA: Association for Computing Machinery, 2018, p. 35–40.
        2024. [Online]. Available: https://arxiv.org/abs/2410.03225                [Online]. Available: https://doi.org/10.1145/3194452.3194465
[146]   X. Shen, L. Wang, Z. Li, Y. Chen, W. Zhao, D. Sun,                 [160]   L. Onwuzurike, E. Mariconti, P. Andriotis, E. D. Cristofaro,
        J. Wang, and W. Ruan, “Pentestagent: Incorporating llm                     G. Ross, and G. Stringhini, “Mamadroid: Detecting android
        agents to automated penetration testing,” 2024. [Online].                  malware by building markov chains of behavioral models
        Available: https://arxiv.org/abs/2411.05185                                (extended version),” 2019. [Online]. Available: https://arxiv.
                                                                                   org/abs/1711.07477
[147]   S. Bhatia, T. Gandhi, D. Kumar, and P. Jalote, “Unit test
        generation using generative ai : A comparative performance         [161]   B. Wu, S. Chen, C. Gao, L. Fan, Y. Liu, W. Wen, and
        analysis of autogeneration tools,” in Proceedings of the 1st               M. R. Lyu, “Why an android app is classified as malware?
        International Workshop on Large Language Models for Code,                  towards malware classification interpretation,” 2020. [Online].
        ser. LLM4Code ’24. New York, NY, USA: Association for                      Available: https://arxiv.org/abs/2004.11516
        Computing Machinery, 2024, p. 54–61. [Online]. Available:          [162]   A. Williamson and M. Beauparlant, “Malware reverse engi-
        https://doi.org/10.1145/3643795.3648396                                    neering with large language model for superior code compre-
[148]   S. Lukasczyk and G. Fraser, “Pynguin: automated unit test                  hensibility and ioc recommendations,” 2024.
        generation for python,” in Proceedings of the ACM/IEEE             [163]   K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can
        44th International Conference on Software Engineering:                     large language models reason about program invariants?”
        Companion Proceedings, ser. ICSE ’22. ACM, May                             in Proceedings of the 40th International Conference on
        2022. [Online]. Available: http://dx.doi.org/10.1145/3510454.              Machine Learning, ser. Proceedings of Machine Learning
        3516829                                                                    Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt,
[149]   S. Bhatia, T. Gandhi, D. Kumar, and P. Jalote, “Unit test                  S. Sabato, and J. Scarlett, Eds., vol. 202. PMLR,
        generation using generative ai : A comparative performance                 23–29 Jul 2023, pp. 27 496–27 520. [Online]. Available:
        analysis of autogeneration tools,” 2024. [Online]. Available:              https://proceedings.mlr.press/v202/pei23a.html
        https://arxiv.org/abs/2312.10622                                   [164]   S. Glazunov and M. Brand, “Project naptime: Evaluating
                                                                                   offensive security capabilities of large language
[150]   R. Pan, M. Kim, R. Krishna, R. Pavuluri, and S. Sinha,
                                                                                   models,”       https://googleprojectzero.blogspot.com/2024/06/
        “Multi-language unit test generation using llms,” 2024.
                                                                                   project-naptime.html, 2024, accessed: 2024-10-16.
        [Online]. Available: https://arxiv.org/abs/2409.03093
                                                                           [165]   M. Bhatt, S. Chennabasappa, Y. Li, C. Nikolaidis, D. Song,
[151]   Y. Chen, Z. Hu, C. Zhi, J. Han, S. Deng, and J. Yin,
                                                                                   S. Wan, F. Ahmad, C. Aschermann, Y. Chen, D. Kapil,
        “Chatunitest: A framework for llm-based test generation,”
                                                                                   D. Molnar, S. Whitman, and J. Saxe, “Cyberseceval
        in Companion Proceedings of the 32nd ACM International
                                                                                   2: A wide-ranging cybersecurity evaluation suite for
        Conference on the Foundations of Software Engineering,
                                                                                   large language models,” 2024. [Online]. Available: https:
        ser. FSE 2024. New York, NY, USA: Association
                                                                                   //arxiv.org/abs/2404.13161
        for Computing Machinery, 2024, p. 572–576. [Online].
        Available: https://doi.org/10.1145/3663529.3663801
[152]   Z. Zhang, X. Liu, Y. Lin, X. Gao, H. Sun, and Y. Yuan,
