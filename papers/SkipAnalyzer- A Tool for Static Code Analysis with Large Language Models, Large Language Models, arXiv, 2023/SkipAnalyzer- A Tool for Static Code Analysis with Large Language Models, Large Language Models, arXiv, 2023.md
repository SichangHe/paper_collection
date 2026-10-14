                                         SkipAnalyzer: A Tool for Static Code Analysis with
                                                      Large Language Models
                                                            Mohammad Mahdi Mohajer∗ , Reem Aleithan† , Nima Shiri Harzevili‡ , Moshi Wei§ ,
                                                                     Alvine Boaye Belle¶ , Hung Viet Pham∥ , Song Wang∗∗
                                                                               Lassonde School of Engineering, York University
                                                                                           Toronto, Ontario, Canada
                                                 {∗ mmm98,† reem1100,‡ nshiri, § moshiwei,∥ hvpham,∗∗ wangsong}@yorku.ca; ¶ alvine.belle@lassonde.yorku.ca


                                             Abstract—We introduce SkipAnalyzer, a large language model         time-consuming and labor-intensive process [8]. Additionally,
arXiv:2310.18532v2 [cs.SE] 18 Dec 2023




                                         (LLM)-powered tool for static code analysis. It can detect bugs,       these detected bugs still require manual fixes, demanding
                                         filter false positive warnings, and patch the detected bugs without    developers’ expertise and knowledge, which can be a resource-
                                         human intervention. SkipAnalyzer consists of three components,
                                         1) an LLM-based static bug detector that scans source code             intensive task [9], [10].
                                         and reports specific types of bugs, 2) an LLM-based false-                Recently, Large Language Models (LLMs) such as Chat-
                                         positive filter that can identify false-positive bugs in the results   GPT have demonstrated significant potential in various rea-
                                         of static bug detectors (e.g., the result of step 1) to improve        soning and decision-making roles, serving as intelligent
                                         detection accuracy, and 3) an LLM-based patch generator that           agents [11], [12], especially in SE tasks such as code genera-
                                         can generate patches for the detected bugs above. As a proof-of-
                                         concept, SkipAnalyzer is built on ChatGPT, which has exhibited         tion, understanding, and debugging. However, to date, there
                                         outstanding performance in various software engineering tasks.         has yet to be research exploring the capabilities of LLM-
                                             To evaluate SkipAnalyzer, we focus on two types of typical and     based tools for various static code analysis tasks. To address
                                         critical bugs that are targeted by static bug detection, i.e., Null    this gap, in this paper, we take a step toward developing a
                                         Dereference and Resource Leak as our subjects. We employ Infer         tool for code analysis based on LLMs named SkipAnalyzer.
                                         to aid the gathering of these two bug types from 10 open-source
                                         projects. Consequently, our experiment dataset contains 222            It contains three components: 1) an LLM-based static bug
                                         instances of Null Dereference bugs and 46 instances of Resource        detector that is capable of scanning source code and reporting
                                         Leak bugs. Our study demonstrates that SkipAnalyzer achieves           specific types of bugs, 2) an LLM-based false-positive filter
                                         remarkable performance in the mentioned static analysis tasks,         for identifying false-positive bugs (e.g., those from step 1) to
                                         including bug detection, false-positive warning removal, and bug       improve the detection accuracy, and 3) an LLM-based patch
                                         repair. In static bug detection, SkipAnalyzer achieves accuracy
                                         values of up to 68.37% for detecting Null Dereference bugs and         generator that can generate patches for the detected bugs.
                                         76.95% for detecting Resource Leak bugs, improving the precision       As a proof-of-concept, SkipAnalyzer is built on ChatGPT,
                                         of the current leading bug detector, Infer by 12.86% and 43.13%        which has consistently demonstrated outstanding performance
                                         respectively. For removing false-positive warnings, SkipAnalyzer       in various software engineering tasks [13].
                                         can reach a precision of up to 93.88% for Null Dereference bugs           To evaluate SkipAnalyzer, we select two typical and widely-
                                         and 63.33% for Resource Leak bugs. Additionally, SkipAnalyzer
                                         surpasses state-of-the-art false-positive warning removal tools.       studied bugs commonly targeted by static bug detection: Null
                                         Furthermore, in bug repair, SkipAnalyzer can generate syntacti-        Dereference and Resource Leak as our subjects. Following
                                         cally correct patches to fix its detected bugs with a success rate     existing works [14], [15], we utilize Infer to facilitate the
                                         of up to 97.30%.                                                       collection of these two types of bugs from 10 open-source
                                             Index Terms—Static analysis, ChatGPT, Large language mod-          projects. As a result, our experiment dataset includes 222
                                         els
                                                                                                                Null Dereference bugs and 46 Resource Leak bugs. When em-
                                                                                                                ploying ChatGPT, we leverage two different model versions:
                                                                I. I NTRODUCTION
                                                                                                                1) ChatGPT-3.5 Turbo and 2) ChatGPT-4. In this study, we
                                            Numerous static code analysis techniques have been utilized         adhere to the best practices of prompt engineering [16], [17]
                                         in the literature for the automatic detection of real-world            and create precise and context-aware prompts to effectively
                                         software bugs [1]–[5]. These tools typically rely on predefined        harness the language models’ capabilities. We explore vari-
                                         heuristic rules to scan and analyze the codebases or binaries of       ous prompting strategies, including zero-shot, one-shot, and
                                         software projects [3]–[5]. During this analysis, any violations        few-shot prompting, to evaluate the performance of different
                                         of these rules are categorized as a bug, leading the tools             ChatGPT models across various scenarios. By strategically
                                         to flag the corresponding code artifact, such as a line or             adapting our prompts and methodologies, we aim to identify
                                         a group of lines, as buggy. However, employing static bug              the most efficient and accurate ways of leveraging LLMs in
                                         detectors presents specific challenges. One primary issue is           static analysis.
                                         that most static bug detectors generate numerous false-positive           Our experiments reveal that SkipAnalyzer achieves remark-
                                         warnings [6], [7]. Consequently, additional manual review is           able performance with significant improvements when com-
                                         essential to validate the reported potential bugs, resulting in a      pared to previous baseline methods for each respective task:
1) Its LLM-based static bug detector achieves a precision rate      methods have been created to perform static bug detection
that is 12.86% higher for Null Dereference bugs and 43.13%          within the body of research and industry [22]. Infer, created
higher for Resource Leak bugs compared to Infer. 2) Its LLM-        by Meta, is a static bug detection tool capable of being utilized
based false-positive filter can enhance Infer’s precision rate by   across various programming languages, including Java, C,
28.68% for Null Dereference bugs and 9.53% for Resource             C++, Objective-C, and C#. It accomplishes this by utilizing
Leak bugs, surpassing the performance of existing baselines.        a predetermined set of rules to identify potential bugs and
Additionally, it can enhance the precision of SkipAnalyzer’s        conducting inter-procedural analysis as part of the project
first component by 16.31% for Null Dereference bugs. 3)             compilation process [23]. SpotBugs [24], an enhanced iteration
Its LLM-based patch generator can generate patches for the          of findBugs [25], [26], employs a methodology similar to
buggy codes and repair them with correctness rates of 97.30%        Infer. It leverages the concept of bug patterns, which consist
and 91.77% for Null Dereference and Resource Leak bugs,             of specific rules and templates designed to identify particular
respectively. Furthermore, on average, 98.77% of the generated      types of bugs. That being said, applying SpotBugs is limited
code for both Null Dereference and Resource Leak bugs are           only to Java byte codes and does not support other lan-
syntactically correct.                                              guages’ source codes or binaries. Google has also introduced
   As a summary, this paper contributes to the field in the         ErrorProne, a static bug detector tailored for Java programs
following ways:                                                     [27]. ErrorProne is designed to catch common programming
    • We propose SkipAnalyzer, a large language model (LLM)         errors and potential bugs during compilation. It enhances the
      powered tool for static code analysis that can detect bugs,   compiler’s type analysis, enabling developers to identify more
      filter false positive warnings, and patch the detected bugs   mistakes before advancing to production. In this study, we
      without human intervention.                                   employ Infer as a baseline for comparison with SkipAnalyzer’s
    • We show that SkipAnalyzer can be an effective static bug      first component and as the tool for generating warnings for our
      detector, improving the base results of the current state-    data collection.
      of-the-art tool, Infer.
                                                                    B. False-Positive Warning Removal
    • We demonstrate that SkipAnalyzer can effectively elimi-
      nate false-positive warnings from the output of static bug       A significant issue associated with the use of static bug
      detectors such as Infer and its first component, thereby      detectors is their tendency to generate a considerable volume
      enhancing their precision and surpassing the performance      of inaccurate warnings, which are essentially alerts that are
      of existing baseline methods in false-positive warning        not genuine indicators of actual bugs [14], [28]–[34]. Recent
      removal.                                                      research demonstrates that the false-positive warning rate
    • We illustrate that SkipAnalyzer exhibits the capability to    can escalate to as high as 91% [28]. Also, removing high
      repair bugs identified by static bug detectors through the    false positive warnings in static analysis tools is very time-
      generation of accurate patches, which we compare against      consuming for developers since it requires them to verify the
      a baseline approach from prior research.                      generated warnings manually, and it often results in frustration
    • We release the dataset and the source code for our            and diminished utilization of these tools [35], [36]. Therefore,
      experiments for future usages1 .                              exploring strategies for reducing false positive warnings in
   The structure of the remainder of this paper is as follows:      static bug detectors is crucial to increasing the developer’s
Section II presents the background of the study. Section III        trust and confidence while using such tools [36], [37]. Recent
presents the data collection of the study. Section IV describes     studies have addressed this issue by providing various tech-
the proposed approach. Section V presents the experiment            niques in detecting and eliminating false-positive warnings.
settings. Section VI presents the results of our work. Section      Junker et al. [38] introduced a method to address false-positive
VII presents the discussion. Section IX presents the related        warnings by transforming this issue into a syntactic model-
work. Section VIII presents the threats to validity, and Section    checking problem and employing SMT solvers to evaluate
X concludes the paper.                                              the feasibility of violation of formula in model checking as
                                                                    a counter-example. Wang et al. [39] have proposed a “Golden
                         II. BACKGROUND                             Features” set to detect actionable warnings and eliminate the
A. Static Bug Detection                                             unactionable ones. Hanam et al. [29] proposed an approach
   Static bug detection is an automated technique for inspect-      based on machine learning, where they created a warning
ing and analyzing a program’s source code, object code, or          prediction model to distinguish between actionable and non-
binaries, all without executing the program [18], [19]. This        actionable warnings. Recently, Kharkar et al. [14] introduced
process identifies potential bugs by examining how the code’s       distinct tools that leverage state-of-the-art neural models,
control and data flow align with specific bug patterns and rules    mostly transformer-based models, which are widely regarded
[19], [20]. If a code section violates any of these rules, the      as the most effective approach for eliminating false-positive
static bug detector will issue a warning concerning the violated    warnings. In this work, we opt to utilize the tools outlined
rule for that particular piece of code [21]. Multiple tools and     in this study as our baselines for comparison. These tools are
                                                                    referred to as feature-based approach, DeepInferEnhance, and
  1 https://doi.org/10.5281/zenodo.10043170                         a GPT-C powered approach [14].
C. Automated Program Repair                                          the capabilities of two state-of-the-art GPT models, specifi-
   Automated program repair (APR) techniques have recently           cally, GPT-3.5 Turbo [52] and GPT-4 [53]. Utilizing LLMs
garnered significant attention from researchers [9], [16], [40],     like ChatGPT as decision making components introduces a
[41]. The core concept of program repair is to automatically         novel approach to systematically interact with instruction-
generate program fixes to facilitate the testing and validation      tuned LLMs, a method known as prompt engineering. Prompt
of software systems [10], [42]. The APR tools usually take           engineering is the practice of creating tailored input queries
two inputs, a flawed code and a localization of the bug in           that effectively communicate with LLMs [16], [17]. Numerous
the flawed code or a description of the program’s expected           investigations leverage prompt engineering in their utilization
behaviour [43]. Automated program repair can be both done            of LLMs [9], [16], [54]–[56]. Prompt engineering as a practice
dynamically and statically. In the dynamic setting, the localiza-    offers the flexibility to utilize various strategies, including the
tion or description of the bug usually comes in the test suites      zero-shot approach, where the LLM is prompted without any
associated with that flawed code and should be executed to           prior input/output examples; the one-shot method, involving
test the validation of the generated patch by the tool [9], [43].    an additional example; and the few-shot strategy, denoted as
As an example, Liu et al. [1] introduced a method known              K-shot, which provides K examples as previous input/output
as Phoenix, which utilizes fix patterns derived from the static      pairs for the LLM [17], [54]. Moreover, in prompt engineering,
analysis of bug violations to generate patches. Their research       techniques like Chain-of-Thought (COT) are employed to en-
involved the utilization of the Defects4J benchmark dataset,         hance the correctness of generated output. This is achieved by
which includes test suites used to validate the effectiveness        either including the thinking steps in examples or requesting
of the generated patches for the faulty code. Furthermore,           an explanation of the decision-making process from the LLM
Xia et al. [9] investigated utilizing Large Language Models          [17], [57], [58].
(LLMs) for the first time for Automated Program Repair                                  III. DATA C OLLECTION
(APR). They examined nine recent and advanced LLMs using
five benchmark datasets. All the patches they generated for             In this work, we take two types of typical and critical bugs
the faulty codes were validated against the accompanying             that are targeted by static bug detection, i.e., Null Dereference
test suites in their respective datasets. In a static context, the   and Resource Leak as our subjects. To accelerate the data
bug’s description or localization is not provided through test       collection, we first applied Infer [23] to our experimental
suites; instead, it is presented using alternative heuristic or      projects with a focus on detecting Null Dereference and
formal methods [1], [2], [44]. For example, Tonder and Goues         Resource Leak bugs. The rationale behind selecting Infer is its
[2] proposed an APR technique for fixing general pointer             extensive adoption in various companies, including Microsoft.
safety properties using Separation Logic [45]. Bavishi et al.        Furthermore, Infer exhibits higher precision in comparison to
[1] introduced a method for generating patches and verifying         alternative static analysis tools, leading to the generation of
them using a static analyzer as the oracle, eliminating the          more valid warnings [14]. We apply Infer to a selection of
need for a test suite. Fu et al. [44] introduced VulRepair, a        seven prominent GitHub projects (with at least more than 200
neural Automated Program Repair (APR) method founded on              stars), along with three projects featured in prior research, to
the CodeT5 model [46]. Their research involved generating            generate warnings [14]. These projects are shown in Table I.
patches for localized bugs found in a pre-existing dataset [47],        Note that, as Infer can report false positives [14], [15], for
[48]. They evaluated the effectiveness of their approach using       each warning, reported, we further manually check whether it
a perfect prediction metric and compared the results to the          is a true bug and not a false positive. This manual labeling
ground truth data within the same dataset.                           process involves three authors with at least four years of
   In this study, we select VulRepair [44] as our baseline tool      development experience, each independently reviewing all the
to compare with SkipAnalyzer. This choice is made because            reported warnings by Infer. For each warning, they assign a
VulRepair, similar to our approach, does not necessitate the         binary label, i.e., zero indicating a “false positive”, signifying
execution of test cases for validation.                              that the warning generated by Infer is incorrect and does not
                                                                     represent a true bug, and one indicating a “true positive”,
D. Large Language Models                                             indicating that the warning is accurate and demonstrates a real
   Large Language Models (LLMs) have gained significant              bug. Following this individual labeling, the authors then col-
popularity in recent research and industrial applications. Nu-       laborate to identify and resolve any discrepancies or conflicts
merous recent studies are investigating the utilization of LLMs      in their assessments. After resolving these conflicts, we have
in the field of Software Engineering (SE), driven by the signif-     our comprehensive dataset containing warnings generated by
icant progress and advancements achieved by LLMs [9], [41],          Infer, along with their corresponding ground truth labels. Also,
[49]. ChatGPT [50], one of the most renowned LLMs, has               for each of the true bugs, the participants work together to
gained widespread recognition recently in performing software        create a patch that can fix the bug.
engineering tasks [9], [16], [17], [51]. ChatGPT is accessible                               IV. A PPROACH
throughout an API2 and has been created by harnessing
                                                                       Figure 1 provides an overview of SkipAnalyzer’s pipeline,
  2 https://platform.openai.com/docs/api-reference                   which contains 1) an LLM-based static bug detector that can
TABLE I: Summary of analyzed projects. In this table, projects highlighted in are from a recent study done by Kharkar et
al. [14], and projects highlighted in are the ones we collected from the popular repositories. The warnings reported in this
table are generated by Infer [23] and manually verified.
          Project                     Project Description              Version    LOC      Repository Group   Number of Verified Warnings
           nacos           Dynamic naming and configuration service     2.0.2    217,653        Alibaba                   58
    azure-maven-plugins        Maven plugins for Azure services         2.2.2    53,025        Microsoft                  45
                              Java library to automate Chromium,
       playwright-java                                                 1.13.0    67,548        Microsoft                  5
                             Firefox, and WebKit with a single API
                            Java Debug Server, an implementation of
         java-debug                                                    0.47.0    22,852        Microsoft                  2
                          Visual Studio Code (VSCode) Debug Protocol
      dolphinscheduler         Modern data orchestration platform       2.0.9    215,808        Apache                   100
                                 high-performance, Java-based
           dubbo                                                         3.2     350,957        Apache                   193
                                  open-source RPC framework
                           a tool to manipulate Android App Bundles
         bundletool                                                    1.15.1    135,711        Google                    51
                                   and Android SDK Bundles
                             set of core Java libraries from Google
           guava                                                       32.1.1    698,201        Google                    35
                                that includes new data structures
                                   release automation tool for
          jreleaser                                                     1.7.0    114,914      Community                   30
                                   Java and non-Java projects
                                 Java library for working with
           jsoup                                                       1.16.1    33,689       Community                   33
                            HTML Document Object Model (DOM)
                                                                         Total Number of Verified Warnings               552



scan source code and report specific types of bugs (Sec-               B. LLM-based False-Positive Warning Filter
tion IV-A), 2) an LLM-based false positive filter that can
identify false-positive bugs in the result of step 1 for improving        In the second component, SkipAnalyzer’s objective is to
the detection accuracy (Section IV-B), and 3) an LLM-based             improve the precision of static bug detection by eliminating
patch generator that can generate patches for the detected bugs        false-positive warnings. To achieve this, SkipAnalyzer takes
(Section IV-C).                                                        both the buggy code snippet and the warning associated with
                                                                       that code snippet, which is generated by a static bug detector.
                                                                       These warnings can originate from various static bug detectors,
                                                                       such as Infer or SkipAnalyzer itself. Subsequently, the LLM,
A. LLM-based Static Bug Detector                                       previously instructed with specialized guidelines, evaluates the
                                                                       buggy code snippet and its corresponding warning. Similar to
   In the first component, SkipAnalyzer takes the buggy code           the first component, the prompt in this stage allow for the
snippet as input for in-depth analysis by the LLM. The LLM             inclusion of additional examples, enabling the application of
has been given a specialized prompt with specifications for            one-shot or few-shot strategies.
each bug type to increase its detection validity. For example,
to address Null Dereference bugs, we collect common bug
patterns for this type of bug, like not having null checks before
dereferencing an object. We then provide this information to           C. LLM-based Static Bug Repair
the LLM in the initial prompt. This specialization helps the
LLM understand the task at hand. Additionally, for Resource              In the third component, SkipAnalyzer processes the buggy
Leak bugs, a similar approach is used. Moreover, specific              code snippet and the warning related to that particular bug
structured output requirements are defined to facilitate easy          in the code. It then proceeds to generate a patch for the
parsing and extracting necessary information from the LLM’s            buggy code, ultimately producing the fixed version of the
responses. Moreover, the prompt of this component supports             code. This component feeds the inputs mentioned above to
adding additional examples to apply one-shot or few-shot               the LLM, which has previously received tailored instructions
strategies. Given that we possess a ground truth for the               on addressing our specific types of bugs. It is worth noting
provided buggy code snippet, we expect SkipAnalyzer to                 that the prompt of this component does not support additional
recognize the problem previously identified by Infer and issue         examples for one-shot or few-shot strategies since examples in
a valid warning for it. Furthermore, SkipAnalyzer offers an            our dataset usually have multiple implementations of methods
additional explanation for each potential bug it detects and           with varying lengths and violate the maximum token limitation
the warnings it generates.                                             of our opted LLMs (more details in Section V-B).
                                                                   OpenAI API3 . According to the model documentation, there is
                                                                   a wide range of options available for each of the models, and
                                                                   each option comes with its distinct characteristics, including
                                                                   varying token lengths, associated costs, and update frequencies
                                                                   [50]. For ChatGPT-4 and ChatGPT-3.5 Turbo, we utilize the
                                                                   default settings, which provide maximum token support of
                                                                   8,192 and 4,097, respectively [52], [53]. Due to this limitation
                                                                   in the maximum input token, we constrain the code inputs to
                                                                   the method scope, implying that we only provide the methods
                                                                   themselves as input code snippets to the LLMs.

           Fig. 1: The overview of SkipAnalyzer.                   C. Prompting Strategies
                                                                      In each of the SkipAnalyzer’s components, we use different
                                                                   prompt engineering strategies such as zero-shot, one-shot, and
                 V. E XPERIMENT S ETTINGS                          few-shot strategies. In the zero-shot strategy, the LLM is
A. Research Questions                                              prompted without preceding examples from the previous LLM
                                                                   input and output pairs. In contrast, the few-shot and one-shot
  To evaluate the performance of SkipAnalyzer, we design
                                                                   strategies incorporate examples from the previous LLM input
experiments to answer the following research questions:
                                                                   and output pairs. The difference between the one-shot and
RQ1 (Static Bug Detection): What is the performance of             few-shot strategies lies in the number of examples included:
SkipAnalyzer in detecting bugs? In this research question,         the one-shot strategy employs a single example in the prompt,
we explore the potential of SkipAnalyzer in the realm of static    while the few-shot strategy encompasses multiple examples. In
bug detection. We present the performance of our approach for      the first component (LLM-based static bug detector) and the
static bug detection and compare it with our baseline, Infer,      second component (LLM-based false-positive warning filter),
while also conducting comparisons under various prompting          we use zero-shot, one-shot, and few-shot strategies. In this
strategies.                                                        paper, for the few-shot strategy, (K-shot), we input the model
RQ2 (False Positive Warning Removal): What is the                  with three examples (K = 3). The rationale for selecting
effectiveness of SkipAnalyzer in filtering false positive          K = 3 is based on the consideration that opting for values
warnings? In this research question, we delve into the effec-      exceeding three could potentially violate the maximum token
tiveness of SkipAnalyzer’s second component in identifying         limit constraint imposed on our inputs for ChatGPT models
and eliminating false-positive warnings from the output of         (details in Section V-B). In the third component (LLM-based
a static bug detector. This analysis is applied to both the        bug repair), we only use the zero-shot strategy due to the
warnings generated by Infer and those produced in response         limitations mentioned in Sections V-B and IV-C. Furthermore,
to RQ1. Eventually, we compare the results of our developed        in the prompts for all of SkipAnalyzer’s components, we
approach with recent state-of-the-art baselines provided by        request the LLM to explain its decision-making process and
Kharkar et al. [14] that utilize feature-based and neural models   the steps it takes to arrive at its conclusions. According to the
for false-positive warning removal.                                literature, this approach, known as zero-shot Chain-of-Thought
                                                                   reasoning, can enhance the output’s robustness and validity
RQ3 (Static Bug Repair): What is SkipAnalyzer’s perfor-            [57], [58].
mance in repairing a buggy code for a specific type of bug?
This RQ examines the potential of SkipAnalyzer in repairing        D. Data Sampling
instances of bugs identified. Note that, as we do not have
                                                                      Our experiments employ N-fold cross-validation to remove
test cases for the identified bugs, most generate-and-validate
                                                                   potential data sampling bias, with N set to 5 in this study [60].
program repair techniques cannot be our baselines, as these
                                                                   This approach involves splitting the dataset into five subsets,
approaches require a set of test cases as the ground truth. In
                                                                   where one-fifth of the data serves as the validation set, and the
this work, we choose VulRepair [44], a CodeT5-based static
                                                                   remaining four-fifths function are used for selecting examples
automated program repair model [59] that does need test cases
                                                                   in the process of prompting the LLMs for one-shot and few-
as the ground truth.
                                                                   shot strategies. We select the examples for these strategies
B. ChatGPT Versions                                                randomly in a uniform distribution. Also, in each of the
                                                                   examples utilized in one-shot and few-shot strategies, we
   We choose the latest variations of ChatGPT models [50],         incorporate one instance of a true-positive record and one
ChatGPT-4 [53] and ChatGPT-3.5 Turbo [52], as the primary          instance of an false-positive record to prevent any bias towards
backbone to build SkipAnalyzer. These models have demon-           a particular group of examples when applying these strategies
strated strong performance in various software engineering         to the LLM.
tasks, including code generation, code comprehension, and
debugging [9], [56]. We interact with these models using             3 https://platform.openai.com/docs/introduction
TABLE II: Summary of SkipAnalyzer’s results for each of the model-strategy combination in Static Bug Detection (RQ1)
using two datasets. In this table, rows highlighted in indicate the most effective combination of model and strategy for Null
Dereference bugs, and rows in indicate the most effective one for Resource Leak bugs.

         Dataset             Bug Type        Infer’s Precision   Strategy          Model       Accuracy    Precision   Recall   F1-Score
                                                                               GPT-3.5-Turbo    50.66%      52.32%     40.64%    45.75%
                                                                 Zero Shot
                                                                                  GPT-4         68.37%      63.76%     88.93%    74.27%
                                                                               GPT-3.5-Turbo    60.67%      62.49%     59.76%    61.09%
                          Null Dereference        50.9%          One Shot
                                                                                  GPT-4         64.54%      62.20%     79.18%    69.67%
                                                                               GPT-3.5-Turbo    60.47%      66.14%     48.63%    56.05%
                                                                 Few Shot
                                                                                  GPT-4         64.31%      65.21%     64.96%    65.09%
      Our collection
                                                                               GPT-3.5-Turbo    56.31%      44.34%     40.44%    42.30%
                                                                 Zero Shot
                                                                                  GPT-4         76.95%      82.73%     55.11%    66.15%
                                                                               GPT-3.5-Turbo    34.87%      35.03%     72.22%    47.18%
                           Resource Leak          39.6%          One Shot
                                                                                  GPT-4         72.78%      68.39%     63.55%    65.88%
                                                                               GPT-3.5-Turbo    49.31%      41.49%     65.55%    50.82%
                                                                 Few Shot
                                                                                  GPT-4         75.25%      74.12%     59.55%    66.04%
                                                                               GPT-3.5-Turbo    50.31%      69.85%     41.53%    52.09%
                                                                 Zero Shot
                                                                                  GPT-4         77.90%      81.87%     85.51%    83.65%
                                                                               GPT-3.5-Turbo    58.25%      70.90%     59.87%    64.92%
                          Null Dereference        65.2%          One Shot
                                                                                  GPT-4         70.51%      80.95%     72.56%    76.53%
                                                                               GPT-3.5-Turbo    56.47%      75.60%     51.28%    61.11%
                                                                 Few Shot
                                                                                  GPT-4         68.52%      80.57%     67.56%    73.50%
    Projects from [14]
                                                                               GPT-3.5-Turbo    61.66%       50.0%      50.0%     50%
                                                                 Zero Shot
                                                                                  GPT-4         84.61%       100%      71.42%    83.32%
                                                                               GPT-3.5-Turbo    46.66%        50%        70%     58.33%
                           Resource Leak          53.8%          One Shot
                                                                                  GPT-4         73.33%        60%        50%     54.54%
                                                                               GPT-3.5-Turbo    48.33%      36.66%       40%     38.26%
                                                                 Few Shot
                                                                                  GPT-4         68.33%        60%        40%      48%



E. Evaluation Metrics                                                       using two different ChatGPT models, i.e., ChatGPT-3.5 Turbo
   We employ the following evaluation metrics to assess our                 and ChatGPT-4 (more details in Section V-B).
experiments concerning each of our research questions:                      Baselines: As a baseline for SkipAnalyzer’s first component,
   For Static Bug Detection (RQ1) and False-Positive Warn-                  we select Infer, a state-of-the-art static bug detector. Using our
ing Removal (RQ2), since we have a ground truth for the                     collected dataset, we compare SkipAnalyzer’s performance in
warnings we generated for our dataset for evaluation, we                    static bug detection with Infer.
use Accuracy, Precision, and Recall metrics. Also, to choose                Result: Table II summarizes the results of SkipAnalyzer’s
the best combination of strategy and model, we use the F1-                  static bug detection task under different prompting strategies
score metric. For Static Bug Repair (RQ3), we assess the                    with different ChatGPT models using Infer on our collected
performance using two key measures that we devised: “Logic                  dataset and the projects used in the prior study by Kharkar
Rate”, which signifies the proportion of repaired code with                 et al [14]. We also show the optimal combination of model
correct logic, and “Syntax Rate”, indicating the proportion                 and strategy for the static bug detection task for each of the
of repaired code with correct syntax. To evaluate the “Logic                datasets, which is the one that has the highest F1-Score for a
Rate”, we assess correctness by comparing the repaired code                 specific bug type. Notably, in our collected dataset, the most
to manually crafted ground truth fix patches prepared by our                effective combination for both Null Dereference and Resource
team. In the case of the “Syntax Rate”, we employ a Java                    Leak bugs involves utilizing ChatGPT-4 in conjunction with
parser to validate the syntax of the generated code.                        the zero-shot strategy. Considering this, in static bug detec-
                                                                            tion, SkipAnalyzer can achieve accuracy, precision, and recall
                       VI. R ESULT A NALYSIS                                rates of 68.37%, 63.76%, and 88.93%, respectively, for Null
                                                                            Dereference bugs. Likewise, for Resource Leak bugs, these
  This section presents the results and answers the research                metrics can attain values of 76.95%, 82.73%, and 55.11%,
questions we asked in Section V-A.                                          respectively. This indicates that SkipAnalyzer exhibits preci-
                                                                            sion levels that are 12.86% and 43.13% higher than Infer,
A. RQ1: Performance of SkipAnalyzer on Static Bug Detection                 surpassing the performance of the state-of-the-art static bug
Approach: In the case of static bug detection, we input the                 detector baseline. Furthermore, it is noteworthy that some
code snippet of each record in our dataset to the SkipAna-                  other model-strategy combinations also demonstrate superior
lyzer’s first component. We expect that SkipAnalyzer will                   performance when compared to Infer. For instance, ChatGPT-
identify the issue previously described and detected by Infer               3.5-Turbo with the one-shot strategy continues to outperform
and produce a valid warning. We perform our experiments                     Infer in the detection of Null Dereference bugs, achieving a
under different prompting strategies such as zero-shot, one-                rate of 62.49% compared to Infer’s 50.9%. We can also see a
shot, and few-shot strategies (more details in Section V-C) by              similar result in the dataset from the projects used by Kharkar
et al. [14]. In this scenario, the most effective strategy and     that Kharkar et al. [14] did not provide the results of the
model combination is the zero-shot strategy coupled with the       feature-based logistic regression model and DeepInferEnhance
ChatGPT-4 model. Compared to Infer’s base results on this          for Resource Leak bugs. Therefore, we specified them with “–”
dataset depicted in Table II, we have a 16.6% and 46.2%            in Table IV.
boost in precision for Null Dereference and Resource Leak             2) Option 2 – SkipAnalyzer: Table III also shows the result
bugs, respectively.                                                of false-positive warning removal on the warnings generated
                                                                   by SkipAnalyzer in Section VI-A. Given that these warn-
 Answer to RQ1: SkipAnalyzer can significantly enhance             ings may arise from various model-strategy combinations, we
 the state-of-the-art static bug detection tool (i.e., Infer) on   selected the most effective model-strategy combination for
 detecting Null Dereference and Resource Leak bugs.                warning generation further to enhance precision through the
                                                                   false-positive warning removal process. Therefore, we opted
  bugs.                                                            for the zero-shot strategy with the ChatGPT-4 model.
                                                                      Moreover, it is worth noting that no false-positive warnings
B. RQ2: Performance of SkipAnalyzer on False-Positive Warn-        were associated with Resource Leak issues in the warnings
ing Removal                                                        generated by this specific model-strategy combination. Con-
Approach: For answering this RQ, we input both a code              sequently, our primary focus remains improving the false-
snippet and the warning linked to the code snippet generated       positive warnings related to Null Dereference issues.
by a bug detector to SkipAnalyzer. To examine the general-            As we can see in Table III, by selecting a proper model-
izability of SkipAnalyzer in removing false positives, we use      strategy combination, which is, in this case, the few-shot
the warnings generated by both Infer and SkipAnalyzer (as          strategy with the ChatGPT-4 model, we can improve the
described in Section VI-A). We also perform our experiments        precision by removing false-positive warnings of the warnings
under different prompting strategies such as zero-shot, one-       generated in Section VI-A by 16.31%.
shot, and few-shot strategies (more details in Section V-B) by
using two different ChatGPT models, i.e., ChatGPT-3.5 Turbo         Answer to RQ2: SkipAnalyzer can remove false-positive
and ChatGPT-4 (more details in Section V-B).                        warnings effectively and it outperforms the previous state-
Baselines: We select the state-of-the-art false-positive re-        of-the-art false-positive warning removal baselines.
moval approach proposed in the recent study conducted by
Kharkar et al. [14], i.e., GPT-C and also they created two         C. RQ3: Performance of SkipAnalyzer on Bug Repair
baselines to evaluate GPT-C, which are a feature-based lo-         Approach: For this RQ, we input SkipAnalyzer with the true
gistic regression model [14] and DeepInferEnhance (based           positive buggy code snippets. We instruct the SkipAnalyzer
on CodeBERTa) [14]. However, the authors neither disclosed         to understand the code and its corresponding warning and
the source code for their tool nor their experiments due to        generate a potential patch to repair the buggy code. Sub-
confidential issues. They also did not release their collected     sequently, we manually assess the generated code patches
dataset. Thus, to enable a meaningful comparison with the          for their syntactical and logical correctness. We perform our
baseline tools outlined in their study, we gathered data that      experiments under the zero-shot strategy by using two different
closely mirrored the one described in their paper, including the   ChatGPT models, i.e., ChatGPT-3.5 Turbo and ChatGPT-4
same projects and similar versions. Ultimately, we conducted       (more details in Section V-B). It is important to note that we
our experiments on a dataset akin to the one they utilized,        do not employ the one-shot or few-shot strategy for static bug
allowing for a fair and direct comparison between our tool         repair due to the limitations mentioned in Sections IV-C and
and their baseline tools.                                          V-B.
Result: As we explained, we have two options for the static        Baselines: We compare the results of our tool with a recent
bug detector utilized for false-positive warning removal:          baseline tool called VulRepair [44]. We used the model and
   1) Option 1 – Infer: Table III shows the results of applying    experiment codes offered by the authors to test this baseline
SkipAnalyzer as a false-positive warning removal tool on           tool on our collected dataset. We followed the same configu-
warnings generated by Infer and SkipAnalyzer.                      ration for training and evaluating their model on our dataset.
   As demonstrated, when dealing with Null Dereference bugs,       Result: Our research findings indicate that SkipAnalyzer can
we can enhance Infer’s precision by 28.68% by employing            serve as a robust bug repair tool. Table V displays the
the zero-shot strategy alongside the ChatGPT-4 model. In           performance of SkipAnalyzer in fixing Null Dereference and
the case of Resource Leak bugs, Infer’s precision can be           Resource Leakage bugs for different models. The results reveal
improved by up to 9.53% when utilizing the zero-shot strategy      that SkipAnalyzer surpasses the baseline tool, VulRepair [44],
combined with the ChatGPT-3.5-Turbo model. Furthermore,            with a substantial improvement. Specifically, SkipAnalyzer
in comparison to the current baselines [14], as indicated in       achieves a logic rate increase of up to 78.91% for Null
Table IV, our findings reveal that SkipAnalyzer can surpass        Dereference bugs and a rate increase of 78.87% for Resource
the existing baselines in terms of precision improvement, with     Leak bugs compared to VulRepair. Furthermore, it is worth
a margin of at least 11.21% and 3.97% for Null Dereference         noting that SkipAnalyzer does not require training or fine-
and Resource Leak bugs, respectively. Also, it is worth noting     tuning. In contrast, VulRepair mandates the adaptation and
TABLE III: Summary of SkipAnalyzer’s results in False-Positive Warning Removal (RQ2) on warnings generated by Infer
and SkipAnalyzer. In this table, POriginal is the precision of the static bug detector for the corresponding bug type and PAfter
is the precision of the static bug detector after applying False-Positive Warning Removal process. “Imp.” indicates the amount
of precision improvement. Rows highlighted in indicate the most effective combination of model and strategy for Null
Dereference bugs, and rows in indicate the most effective one for Resource Leak bugs. Also, the records that have no
improvement in precision are shown with “–”.
   Static Bug Detector          Bug Type            Strategy         Model           POriginal    PAfter     Imp.      Recall     Accuracy    F1-Score
                                                                  GPT-3.5-Turbo                    40%         -      13.07%       37.91%      19.71%
                                                   Zero Shot
                                                                     GPT-4                         95%       +29.8    27.30%       51.41%      42.42%
                                                                  GPT-3.5-Turbo                  59.32%        -      43.71%       43.91%      50.33%
                            Null Dereference        One Shot                          65.2%
                                                                     GPT-4                         95%       +29.8    51.66%       66.29%      66.93%
                                                                  GPT-3.5-Turbo                  53.63%        -      52.17%       41.40%      52.89%
                                                   Few Shot
                                                                     GPT-4                       93.88%     +28.68    64.23%       73.46%     76.27%
           Infer
                                                                  GPT-3.5-Turbo                  63.33%      +9.53     80%          75%       70.69%
                                                   Zero Shot
                                                                     GPT-4                         60%      +6.2%       60%         80%         60%
                                                                  GPT-3.5-Turbo                    40%         -        60%         50%         48%
                              Resource Leak         One Shot                          53.8%
                                                                     GPT-4                         60%      +6.2%       50%         75%        54.54%
                                                                  GPT-3.5-Turbo                    50%         -        80%         50%        61.53%
                                                    Few Shot
                                                                     GPT-4                         60%      +6.2%       60%         80%         60%
                                                                  GPT-3.5-Turbo                    70%         -      19.27%       32.93%      30.22%
                                                   Zero Shot
                                                                     GPT-4                         86%      +4.13%    26.72%       37.45%      40.78%
                                                                  GPT-3.5-Turbo                    67%         -      30.72%       32.72%      42.26%
      SkipAnalyzer          Null Dereference        One Shot                         81.87%
                                                                     GPT-4                        97.5%     +15.63    52.72%       59.92%      68.44%
                                                                  GPT-3.5-Turbo                  73.97%        -      38.18%       38.90%      50.36%
                                                   Few Shot
                                                                     GPT-4                       98.18%     +16.31    77.45%       80.25%     86.59%


TABLE IV: Performance of False-Positive Warning Removal                            TABLE V: Summary of SkipAnalyzer’s results in static bug
of baseline tools proposed by [14]. In this table column                           repair. The “Syntax Rate” column indicates the proportion
“Precision Imp.” indicates the precision improvement of Infer                      of generated patches that are syntactically correct. “Logic
after applying each of the baseline tools. Also, column “S.A.                      Rate” column represents the rate of generated patches that
Recall Imp.” shows SkipAnalyzer ’s improvement in Recall                           are logically correct.
for each bug type compared to the baseline tool.
                                                                                         Bug Type             Model         Logic Rate       Syntax Rate
     Baseline          Bug Type        Precision Imp.   Recall   SA. Recall Imp.
                                                                                                           GPT-3.5-Turbo        94.25%         100.0%
                    Null Dereference      +8.26%        65.1%       +12.35%
   Feature-based                                                                     Null Dereference         GPT-4             97.30%         99.55%
                     Resource Leak           –            –            –
                    Null Dereference     +15.13%        88.3%       -10.85%                                  VulRepair          18.39%           –
 DeepInferEnhance
                     Resource Leak           –            –            –                                   GPT-3.5-Turbo        87.11%         97.77%
                    Null Dereference     +17.47%        83.7%        -6.25%
      GPT-C                                                                           Resource Leak           GPT-4             91.77%         97.77%
                     Resource Leak        +5.56%        64.5%        +15.5%
                                                                                                             VulRepair          12.90%           –


training of our dataset for patch generation, showing the
superiority of SkipAnalyzer over the recent state-of-the-art                       For our analysis, we first collect all the missing bugs that
baseline tool, VulRepair. Also, VulRepair-generated patches                        SkipAnalyzer can not detect. Then, we manually examine
are not self-contained Java codes and should be appended to                        all the missing bugs and observe the possible recurring and
the buggy code. Hence, they are not parsable, and we specify                       common patterns among them.
the Syntax Rate for VulRepair’s generated patches with VI-C                           1) Null Dereference: We have identified three patterns
in Table V.                                                                        from Null Dereference bugs that SkipAnalyzer missed. Firstly,
                                                                                   SkipAnalyzer struggles to distinguish Null Dereferences of
 Answer to RQ3: SkipAnalyzer is effective in patching the                          objects within a null check for another object. This is often
 detected bugs. In addition, SkipAnalyzer can significantly                        observed when SkipAnalyzer overlooks objects that might
 outperform a recent state-of-the-art baseline tool, i.e., Vul-                    become null and dereferenced later within a null check for
 Repair.                                                                           another object. This issue becomes more pronounced when
                                                                                   these objects have some form of relationship with one another,
                          VII. D ISCUSSIONS                                        such as when the first object serves as an argument to a method
                                                                                   call of the second object. Figure 2 shows an example bug that
A. Reasons for Missing Detecting Bugs                                              is missing by SkipAnalyzer.
   SkipAnalyzer also has limitations such as it can miss de-                          Second, we have observed that SkipAnalyzer sometimes
tecting bugs in RQ1. In this section, we explore the underlying                    makes random assumptions about the method, API call, class
reasons behind the bugs that SkipAnalyzer cannot detect.                           variable, and instance variable that are usually outside the
 1 public DependentParameters getDependency() {                       1 private void cacheNormalInvokers( BitList <Invoker<T>>
 2 if ( this . dependency == null) {                                  2 invokers ) {
 3      Map<String, Object> taskParamsMap =                           3     BitList <Invoker<T>> clonedInvokers = invokers.clone();
 4      JSONUtils.parseObject ( this .getTaskParams (), new           4     clonedInvokers .removeIf(( invoker ) −>
 5      TypeReference<Map<String, Object>>() {});                     5     invoker . getUrl (). getProtocol (). equals (MOCK PROTOCOL));
 6       this . dependency = JSONUtils.parseObject(( String )         6     normalInvokers = clonedInvokers ;
 7      taskParamsMap.get(Constants .DEPENDENCE),                     7}
 8      DependentParameters. class );
 9 }                                                                    Ground Truth Warning: object returned by “in-
10     return this . dependency;                                        voker.getUrl().getProtocol()” could be null and is derefer-
11}                                                                     enced at line 5.
    Ground Truth Warning: object “taskParamsMap” last                   SkipAnalyzer’s Explanation: The ‘normalInvokers‘ object
    assigned on line 3 could be null and is dereferenced at line        is assigned the value of ‘clonedInvokers‘, which is a cloned
    7.                                                                  version of ‘invokers‘. However, there is no null check for
    SkipAnalyzer’s Explanation: The code checks if                      ‘clonedInvokers‘ before assigning it to ‘normalInvokers‘.
    “this.dependency” is null before assigning a value to it.           If ‘invokers.clone()‘ returns null, it will result in a null
    Therefore, there is no potential null dereference bug in this       dereference bug.
    code.
                                                                       Fig. 4: An example of a missing Null Dereference bug by
        Fig. 2: An example of a missing Null Dereference.              SkipAnalyzer. In this example, SkipAnalyzer missed the Null
                                                                       Dereference issue in the method call chain and did not report
                                                                       anything about it.
 1 private static void registerContextBeans ( ConfigurableListableBeanFactory
 2beanFactory , DubboSpringInitContext context ) {
 3    // register singleton                                              Third, another prevalent pattern is SkipAnalyzer’s difficulty
 4     registerSingleton (beanFactory , context );                    in detecting Null Dereferences that occur in a single line
 5     registerSingleton (beanFactory ,                               through a chain of method invocations. While SkipAnalyzer
 6 context . getApplicationModel ());
                                                                      may be able to detect the first object invoking a method, it
 7     registerSingleton (beanFactory ,
 8 context . getModuleModel());                                       often fails to identify the subsequent methods chained through
 9}                                                                   method calls to the initial object, which could also return null.
                                                                       As an example, we can look at Figure 4.
    Ground Truth Warning: object returned by “con-                        2) Resource Leak: The prevalent pattern of overlooked
    text.getApplicationModel()” could be null and is derefer-          Resource Leak bugs involves cases where the code partially
    enced by call to “registerSingleton(...)” at line 6.               handles the release of resources. This implies that while some
    SkipAnalyzer’s       Explanation:     The     values    of         resources are properly released after their use, there are still
    “context.getApplicationModel()”          and         “con-         other resources that remain unreleased. Figure 5 is an example
    text.getModuleModel()” are being checked for null                  of a missing Resource Leak bug due to this issue.
    before being registered as singletons, so there is no null
    dereference bug in this code.                                                      VIII. T HREATS TO VALIDITY
                                                                          In this research, our focus is solely on Java projects, and
  Fig. 3: An example of a missing Null Dereference bug by              we do not consider projects developed in other programming
  SkipAnalyzer. In this case, the “registerSingleton” is a function    languages. This choice stems from the limitation that Infer,
  declared as outside of the method where the Null Dereference         the tool we employ for generating warnings and the dataset,
  is detected. Consequently, SkipAnalyzer attempts to establish        is not capable of handling multiple programming languages.
  a connection between the registering for singleton and the Null      However, it is worth noting that Infer can be used with
  Dereference issue, even though they are not directly related.        languages like C and C#. Therefore, conducting a similar
                                                                       analysis on additional languages that Infer is compatible with
                                                                       can contribute to the validity of our research.
  current method’s scope. SkipAnalyzer’s inability to access the          Another potential challenge to the validity of our work
  implementation details of these entities hinders its ability to      is that the evaluation is conducted exclusively on a dataset
  determine whether they can return null or not. Consequently,         created from warnings generated by Infer, without taking
  SkipAnalyzer occasionally makes incorrect assumptions about          into account warnings generated by alternative static analysis
  the return values of such entities, leading to missing potential     tools like SpotBugs [24] or Error-Prone [27]. In this study,
  Null Dereference bugs. Figure 3 shows an example bug that            we opted not to include SpotBugs and Error-Prone as static
  cannot be detected by SkipAnalyzer because of the above              bug detectors. This decision was made because these tools
  reason.                                                              categorize bug types differently, and we aimed to maintain
                                                                                                IX. R ELATED W ORK
 1 private void executeForSdkArchive() {
 2     try (TempDirectory tempDir = new                                    A. LLM Applications in Software Engineering
 3     TempDirectory(getClass (). getSimpleName());
 4           ZipFile asarZip = new                                            Recently, there has been a considerable volume of research
 5           ZipFile (getSdkArchivePath (). get (). toFile ())) {          dedicated to exploring the capabilities of Large Language
 6        Path modulesPath =                                               Models (LLMs) within the domain of Software Engineering
 7       tempDir.getPath (). resolve (EXTRACTED SDK);                      (SE). For example, several studies focus on automated pro-
 8        try ( ZipFile modulesZip = getModulesZip(asarZip,                gram repair [9], [16], [41], [44], [61]–[67]. For instance, Xia
 9       modulesPath)) {
10          SdkAsarValidator . validateModulesFile (modulesZip);           et al. [9] conducted the first empirical study to evaluate nine re-
11          SdkAsar sdkAsar = SdkAsar.buildFromZip(asarZip,                cent state-of-the-art LLMs for automated program repair tasks
12          modulesZip, modulesPath);                                      on five different repair datasets. Mashhadi and Hemmati [67]
13          generateAppApks(sdkAsar.getModule(), tempDir);                 fine-tuned a repair dataset of single-line Java bugs on the
14       }                                                                 CodeBERT model. Also, numerous studies in software testing
15     } catch (ZipException e) {
16       throw CommandExecutionException.builder()                         and fuzzing utilize LLMs [54], [68]–[70]. For example, Deng
17             . withInternalMessage (”ASAR is not a valid zip file . ”)   et al. [69] proposed FuzzGPT, a novel LLM-based fuzzer that
18             . withCause(e)                                              can produce unusual programs for fuzzing real-world systems.
19             . build ();                                                 The same authors also provide TitanFuzz [70], the first LLM-
20     } catch (IOException e) {                                           based approach for fuzzing Deep Learning (DL) libraries.
21       throw new UncheckedIOException(”An error occurred when
22        processing the SDK archive.”, e );                               Kang et al. [54] proposed LIBRO, a framework that uses
23     }                                                                   LLMs to automate test generation from general bug reports.
24 }                                                                       Furthermore, there are studies that focus on Oracle genera-
                                                                           tion [71]–[73]. For example, Tufano et al. [71] proposed a
    Ground        Truth      Warning:     resource   of      type          novel assertion generation approach using a BART transformer
    “java.util.zip.ZipFile” acquired by call to “ZipFile(...)” at          model. Nie et al. [72] proposed an approach for predicting
    line 4 is not released after line 20.                                  the next statement in test methods that need reasoning about
    SkipAnalyzer’s Explanation: The resources “tempDir”                    the code execution by utilizing CodeT5 model. Dinella et al.
    and “asarZip” are allocated using the try-with-resources               [73] introduced TOGA, a neural transformer-based method
    syntax, which means they will be automatically released                for inferring both exceptional and assertion test conditions by
    and closed after the try block finishes. Therefore, there is           considering the context of the main method. Also, there are
    no resource leakage bug in this code.                                  studies that focus on mobile applications such as Android.
                                                                           [17], [74]. Feng et al. [17] introduced an automated technique
  Fig. 5: An example of a missing Resource Leak bug by Skip-               for Android bug reproduction, utilizing ChatGPT-3.5 to extract
  Analyzer. In this example, Although SkipAnalyzer correctly               reproducible steps and automate the bug replay procedure.
  identify “tempDir” as not buggy, it cannot detect the “asarZip”,         Taeb et al. [74] proposed an automated approach for producing
  which is an actual Resource Leak bug. The code does not                  a navigable video from a manual accessibility test of a mobile
  use Java 7 try-with-resources (try(...)) syntax for the “asarZip”        application by utilizing ChatGPT-4.
  object. It only uses it for “tempDir” and also “modulesZip”
  in the next lines.                                                                              X. C ONCLUSION
                                                                              This paper introduces a novel LLM-based tool for static
                                                                           code analysis. Our developed tool, SkipAnalyzer, can show-
  consistency in our bug classification [15]. Additionally, Infer          case the capabilities of LLMs like ChatGPT models in car-
  has better precision and outperforms them in accuracy [14].              rying out code analysis tasks, including static bug detection,
                                                                           false-positive warning removal, and bug repair. To generate
     Also, we exclusively employed LLM models from OpenAI,                 warnings, we employed Infer, a well-established static analysis
  specifically ChatGPT-4 and ChatGPT-3.5 Turbo. It is essential            tool, on prominent open-source Java projects and projects from
  to recognize that other companies have also introduced their             prior research. Subsequently, we meticulously labeled each of
  LLM models, such as Meta’s Llama2 and Google’s PaLM2                     the generated warnings for two types of bugs: Null Dereference
  and Bard. These alternative models may bring their own                   and Resource Leak, thereby creating a new dataset for our
  unique features and performance characteristics, which could             analytical work. We then harnessed the power of different
  potentially impact the validity of our findings.                         ChatGPT models (i.e., ChatGPT-3.5 Turbo, ChatGPT-4) under
     Furthermore, it is important to acknowledge that the per-             different prompting strategies. Our experiments reveal that
  formance of our SkipAnalyzer may exhibit variations across               SkipAnalyzer’s components can outperform baseline counter-
  different sets of projects. To account for this variability and          parts, all while offering significant advantages in terms of
  enhance the generalizability of our results, we have included            reduced costs and complexity.
  a diverse array of projects from various repositories and                   In the future, our research endeavors will broaden in scope
  backgrounds.                                                             as we aim to explore a wider array of Large Language Models
(LLMs), such as Meta’s Llama, Google’s Bard, and PaLM2,                            [16] J. Cao, M. Li, M. Wen, and S.-c. Cheung, “A study on prompt design,
and integrate them into SkipAnalyzer. We also intend to                                 advantages and limitations of chatgpt for deep learning program repair,”
                                                                                        arXiv preprint arXiv:2304.08191, 2023.
delve into a comparative analysis between fine-tuned LLMs                          [17] S. Feng and C. Chen, “Prompting is all your need: Automated
and LLMs that are specialized for specific tasks through                                android bug replay with large language models,” arXiv preprint
prompt engineering. Additionally, we find it intriguing to                              arXiv:2306.01987, 2023.
                                                                                   [18] L. Li, T. F. Bissyandé, M. Papadakis, S. Rasthofer, A. Bartel, D. Octeau,
assess SkipAnalyzer’s performance on different types of bugs.                           J. Klein, and L. Traon, “Static analysis of android apps: A systematic
Furthermore, adding additional components to SkipAnalyzer                               literature review,” Information and Software Technology, vol. 88, pp.
to further examine coding practices and styles would be                                 67–95, 2017.
                                                                                   [19] Q. Ashfaq, R. Khan, and S. Farooq, “A comparative analysis of static
helpful.                                                                                code analysis tools that check java code adherence to java coding
                                                                                        standards,” in 2019 2nd International Conference on Communication,
                               R EFERENCES                                              Computing and Digital systems (C-CODE). IEEE, 2019, pp. 98–103.
                                                                                   [20] C. Vassallo, S. Panichella, F. Palomba, S. Proksch, H. C. Gall, and
 [1] R. Bavishi, H. Yoshida, and M. R. Prasad, “Phoenix: Automated data-                A. Zaidman, “How developers engage with static analysis tools in
     driven synthesis of repairs for static analysis violations,” in Proceedings        different contexts,” Empirical Software Engineering, vol. 25, pp. 1419–
     of the 2019 27th ACM Joint Meeting on European Software Engineering                1457, 2020.
     Conference and Symposium on the Foundations of Software Engineering,          [21] D. A. Tomassi and C. Rubio-González, “On the real-world effectiveness
     2019, pp. 613–624.                                                                 of static bug detectors at finding null pointer exceptions,” in 2021 36th
 [2] R. van Tonder and C. L. Goues, “Static automated program repair for                IEEE/ACM International Conference on Automated Software Engineer-
     heap properties,” in Proceedings of the 40th International Conference              ing (ASE), 2021, pp. 292–303.
     on Software Engineering, 2018, pp. 151–162.                                   [22] N. S. Harzevili et al., “Automatic static bug detection for machine
 [3] K. Liu, A. Koyuncu, D. Kim, and T. F. Bissyandè, “Avatar: Fixing                  learning libraries: Are we there yet?” ArXiv, 2023, accessed 18 Oct.
     semantic bugs with fix patterns of static analysis violations,” in 2019            2023. [Online]. Available: https://arxiv.org/abs/2307.04080
     IEEE 26th International Conference on Software Analysis, Evolution            [23] Infer. Infer official website. [Online]. Available: https://fbinfer.com/
     and Reengineering (SANER), 2019, pp. 1–12.                                    [24] D. A. Tomassi, “Bugs in the wild: Examining the effectiveness of static
 [4] D. Marcilio, R. Bonifácio, E. Monteiro, E. Canedo, W. Luz, and                    analyzers at finding real-world bugs,” in Proceedings of the 2018 26th
     G. Pinto, “Are static analysis violations really fixed? a closer look at           ACM Joint Meeting on European Software Engineering Conference and
     realistic usage of sonarqube,” in 2019 IEEE/ACM 27th International                 Symposium on the Foundations of Software Engineering, ser. ESEC/FSE
     Conference on Program Comprehension (ICPC), 2019, pp. 209–219.                     2018. New York, NY, USA: Association for Computing Machinery,
 [5] A. Carvalho, W. Luz, D. Marcı́lio, R. Bonifácio, G. Pinto, and                    2018, p. 980–982.
     E. Dias Canedo, “C-3pr: A bot for fixing static analysis violations via       [25] D. Hovemeyer and W. Pugh, “Finding bugs is easy,” SIGPLAN
     pull requests,” in 2020 IEEE 27th International Conference on Software             Not., vol. 39, no. 12, p. 92–106, dec 2004. [Online]. Available:
     Analysis, Evolution and Reengineering (SANER), 2020, pp. 161–171.                  https://doi.org/10.1145/1052883.1052895
 [6] S. Afrose, Y. Xiao, S. Rahaman, B. P. Miller, and D. Yao, “Evaluation         [26] B. Cole, D. Hakim, D. Hovemeyer, R. Lazarus, W. Pugh, and
     of static vulnerability detection tools with java cryptographic api bench-         K. Stephens, “Improving your software using static analysis to find
     marks,” IEEE Transactions on Software Engineering, vol. 49, no. 2, pp.             bugs,” in Companion to the 21st ACM SIGPLAN Symposium on
     485–497, 2023.                                                                     Object-Oriented Programming Systems, Languages, and Applications,
 [7] S. Lipp, S. Banescu, and A. Pretschner, “An empirical study on the                 ser. OOPSLA ’06. New York, NY, USA: Association for Computing
     effectiveness of static c code analyzers for vulnerability detection,” in          Machinery, 2006, p. 673–674. [Online]. Available: https://doi.org/10.
     Proceedings of the 31st ACM SIGSOFT International Symposium on                     1145/1176617.1176667
     Software Testing and Analysis, ser. ISSTA 2022. New York, NY, USA:            [27] Google. (2023) Errorprone. Accessed on Date. [Online]. Available:
     Association for Computing Machinery, 2022, p. 544–555. [Online].                   https://errorprone.info/index
     Available: https://doi.org/10.1145/3533767.3534380                            [28] H. J. Kang, K. L. Aw, and D. Lo, “Detecting false alarms from
 [8] Y. Pan, X. Ge, C. Fang, and Y. Fan, “A systematic literature review of             automatic static analysis tools: How far are we?” in Proceedings of the
     android malware detection using static analysis,” IEEE Access, vol. 8,             44th International Conference on Software Engineering, ser. ICSE ’22.
     pp. 116 363–116 379, 2020.                                                         New York, NY, USA: Association for Computing Machinery, 2022, p.
 [9] C. S. Xia, Y. Wei, and L. Zhang, “Automated program repair                         698–709.
     in the era of large pre-trained language models,” in Proceedings              [29] Q. Hanam, L. Tan, R. Holmes, and P. Lam, “Finding patterns
     of the 45th International Conference on Software Engineering, ser.                 in static analysis alerts: Improving actionable alert ranking,” in
     ICSE ’23. IEEE Press, 2023, p. 1482–1494. [Online]. Available:                     Proceedings of the 11th Working Conference on Mining Software
     https://doi.org/10.1109/ICSE48619.2023.00129                                       Repositories, ser. MSR 2014. New York, NY, USA: Association
[10] L. Gazzola, D. Micucci, and L. Mariani, “Automatic software repair: A              for Computing Machinery, 2014, p. 152–161. [Online]. Available:
     survey,” in Proceedings of the 40th International Conference on Software           https://doi.org/10.1145/2597073.2597100
     Engineering, 2018, pp. 1219–1219.                                             [30] X. Yang, J. Chen, R. Yedida, Z. Yu, and T. Menzies, “Learning
[11] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and              to recognize actionable static code warnings (is intrinsically easy),”
     A. Anandkumar, “Voyager: An open-ended embodied agent with large                   Empirical Softw. Engg., vol. 26, no. 3, may 2021. [Online]. Available:
     language models,” arXiv preprint arXiv:2305.16291, 2023.                           https://doi.org/10.1007/s10664-021-09948-6
[12] C. H. Song, J. Wu, C. Washington, B. M. Sadler, W.-L. Chao, and Y. Su,        [31] H. Shen, J. Fang, and J. Zhao, “Efindbugs: Effective error ranking for
     “Llm-planner: Few-shot grounded planning for embodied agents with                  findbugs,” in 2011 Fourth IEEE International Conference on Software
     large language models,” in Proceedings of the IEEE/CVF International               Testing, Verification and Validation, 2011, pp. 299–308.
     Conference on Computer Vision, 2023, pp. 2998–3009.                           [32] Z. P. Reynolds, A. B. Jayanth, U. Koc, A. A. Porter, R. R. Raje, and
[13] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo,                   J. H. Hill, “Identifying and documenting false positive patterns generated
     J. Grundy, and H. Wang, “Large language models for software engineer-              by static code analysis tools,” in 2017 IEEE/ACM 4th International
     ing: A systematic literature review,” arXiv preprint arXiv:2308.10620,             Workshop on Software Engineering Research and Industrial Practice
     2023.                                                                              (SER&IP), 2017, pp. 55–61.
[14] A. Kharkar, R. Z. Moghaddam, M. Jin, X. Liu, X. Shi, C. Clement,              [33] T. Muske and A. Serebrenik, “Techniques for efficient automated elim-
     and N. Sundaresan, “Learning to reduce false positives in analytic                 ination of false positives,” in 2020 IEEE 20th International Working
     bug detectors,” in Proceedings of the 44th International Conference on             Conference on Source Code Analysis and Manipulation (SCAM), 2020,
     Software Engineering, 2022, pp. 1307–1316.                                         pp. 259–263.
[15] N. S. Harzevili, J. Shin, J. Wang, and S. Wang, “Characterizing and           [34] S. Heckman and L. Williams, “A systematic literature review of action-
     understanding software security vulnerabilities in machine learning                able alert identification techniques for automated static code analysis,”
     libraries,” arXiv preprint arXiv:2203.06502, 2022.                                 Information and Software Technology, vol. 53, no. 4, pp. 363–387, 2011.
[35] M. Christakis and C. Bird, “What developers want and need from               [52] OpenAI. (2023) Chatgpt-3.5. Accessed on Date. [Online]. Available:
     program analysis: an empirical study,” in Proceedings of the 31st                 https://platform.openai.com/docs/models/gpt-3-5
     IEEE/ACM international conference on automated software engineering,         [53] “Gpt-4 technical report,” ArXiv, 2023, accessed 17 Oct. 2023. [Online].
     2016, pp. 332–343.                                                                Available: https://arxiv.org/abs/2303.08774
[36] B. Johnson, Y. Song, E. Murphy-Hill, and R. Bowdidge, “Why don’t             [54] S. Kang, J. Yoon, and S. Yoo, “Large language models are few-
     software developers use static analysis tools to find bugs?” in 2013 35th         shot testers: Exploring llm-based general bug reproduction,” in 2023
     International Conference on Software Engineering (ICSE), 2013, pp.                IEEE/ACM 45th International Conference on Software Engineering
     672–681.                                                                          (ICSE). IEEE, 2023, pp. 2312–2323.
[37] U. Koc, S. Wei, J. S. Foster, M. Carpuat, and A. A. Porter, “An empirical    [55] D. Zan, B. Chen, F. Zhang, D. Lu, B. Wu, B. Guan, W. Yongji,
     assessment of machine learning approaches for triaging reports of a java          and J.-G. Lou, “Large language models meet NL2Code: A survey,”
     static analysis tool,” in 2019 12th ieee conference on software testing,          in Proceedings of the 61st Annual Meeting of the Association for
     validation and verification (icst). IEEE, 2019, pp. 288–299.                      Computational Linguistics (Volume 1: Long Papers). Toronto, Canada:
[38] M. Junker, R. Huuck, A. Fehnker, and A. Knapp, “Smt-based false                   Association for Computational Linguistics, Jul. 2023, pp. 7443–7464.
     positive elimination in static program analysis,” in Formal Methods          [56] B. Min, H. Ross, E. Sulem, A. P. B. Veyseh, T. H. Nguyen, O. Sainz,
     and Software Engineering: 14th International Conference on Formal                 E. Agirre, I. Heintz, and D. Roth, “Recent advances in natural language
     Engineering Methods, ICFEM 2012, Kyoto, Japan, November 12-16,                    processing via large pre-trained language models: A survey,” ACM
     2012. Proceedings 14. Springer, 2012, pp. 316–331.                                Comput. Surv., vol. 56, no. 2, sep 2023.
[39] J. Wang, S. Wang, and Q. Wang, “Is there a ”golden” feature set for static   [57] J. Wei and et al., “Chain-of-thought prompting elicits reasoning in large
     warning identification? an experimental evaluation,” in Proceedings of            language models,” arXiv, 2022, accessed 19 Oct. 2023.
     the 12th ACM/IEEE International Symposium on Empirical Software              [58] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, “Large
     Engineering and Measurement, ser. ESEM ’18. New York, NY, USA:                    language models are zero-shot reasoners,” in Advances in Neural In-
     Association for Computing Machinery, 2018.                                        formation Processing Systems, S. Koyejo, S. Mohamed, A. Agarwal,
[40] A. Arcuri, “On the automation of fixing software bugs,” in Companion              D. Belgrave, K. Cho, and A. Oh, Eds., vol. 35. Curran Associates,
     of the 30th International Conference on Software Engineering, ser.                Inc., 2022, pp. 22 199–22 213.
     ICSE Companion ’08. New York, NY, USA: Association for                       [59] Y. Wang, W. Wang, S. Joty, and S. C. Hoi, “Codet5: Identifier-aware
     Computing Machinery, 2008, p. 1003–1006. [Online]. Available:                     unified pre-trained encoder-decoder models for code understanding and
     https://doi.org/10.1145/1370175.1370223                                           generation,” arXiv preprint arXiv:2109.00859, 2021.
[41] Z. Fan, X. Gao, A. Roychoudhury, and S. H. Tan, “Improving automat-          [60] T.-T. Wong and P.-Y. Yeh, “Reliable accuracy estimates from k-fold cross
     ically generated code from codex via automated program repair,” arXiv             validation,” IEEE Transactions on Knowledge and Data Engineering,
     preprint arXiv:2205.10583, 2022.                                                  vol. 32, no. 8, pp. 1586–1594, 2020.
[42] W. Weimer, T. Nguyen, C. Le Goues, and S. Forrest, “Automatically            [61] H. Joshi, J. Cambronero Sanchez, S. Gulwani, V. Le, G. Verbruggen,
     finding patches using genetic programming,” in 2009 IEEE 31st Interna-            and I. Radiček, “Repair is nearly generation: Multilingual program
     tional Conference on Software Engineering. IEEE, 2009, pp. 364–374.               repair with llms,” Proceedings of the AAAI Conference on Artificial
                                                                                       Intelligence, vol. 37, no. 4, pp. 5131–5140, Jun. 2023.
[43] A. Nilizadeh, G. T. Leavens, X.-B. D. Le, C. S. Păsăreanu, and D. R.
                                                                                  [62] M. Jin, S. Shahriar, M. Tufano, X. Shi, S. Lu, N. Sundaresan, and
     Cok, “Exploring true test overfitting in dynamic automated program
                                                                                       A. Svyatkovskiy, “Inferfix: End-to-end program repair with llms,” arXiv
     repair using formal methods,” in 2021 14th IEEE Conference on
                                                                                       preprint arXiv:2303.07263, 2023.
     Software Testing, Verification and Validation (ICST), 2021, pp. 229–240.
                                                                                  [63] Z. Fan, X. Gao, M. Mirchev, A. Roychoudhury, and S. H. Tan,
[44] M. Fu, C. Tantithamthavorn, T. Le, V. Nguyen, and D. Phung,                       “Automated repair of programs from large language models,” in 2023
     “Vulrepair: A t5-based automated software vulnerability repair,” in               IEEE/ACM 45th International Conference on Software Engineering
     Proceedings of the 30th ACM Joint European Software Engineering                   (ICSE), 2023, pp. 1469–1481.
     Conference and Symposium on the Foundations of Software Engineering,
                                                                                  [64] F. Ribeiro, “Large language models for automated program repair,”
     ser. ESEC/FSE 2022. New York, NY, USA: Association for
                                                                                       in Companion Proceedings of the 2023 ACM SIGPLAN International
     Computing Machinery, 2022, p. 935–947. [Online]. Available: https:
                                                                                       Conference on Systems, Programming, Languages, and Applications:
     //doi.org/10.1145/3540250.3549098
                                                                                       Software for Humanity, ser. SPLASH 2023. New York, NY, USA:
[45] J. Berdine, A. Cox, S. Ishtiaq, and C. M. Wintersteiger, “Diagnosing              Association for Computing Machinery, 2023, p. 7–9.
     abstraction failure for separation logic–based analyses,” in Computer        [65] N. Jiang, K. Liu, T. Lutellier, and L. Tan, “Impact of code language
     Aided Verification, P. Madhusudan and S. A. Seshia, Eds.           Berlin,        models on automated program repair,” in Proceedings of the 45th
     Heidelberg: Springer Berlin Heidelberg, 2012, pp. 155–173.                        International Conference on Software Engineering, ser. ICSE ’23. IEEE
[46] Y. Wang, W. Wang, S. Joty, and S. C. Hoi, “CodeT5: Identifier-aware               Press, 2023, p. 1430–1442.
     unified pre-trained encoder-decoder models for code understanding and        [66] C. S. Xia and L. Zhang, “Less training, more repairing please: Revisiting
     generation,” in Proceedings of the 2021 Conference on Empirical                   automated program repair via zero-shot learning,” in Proceedings of
     Methods in Natural Language Processing. Online and Punta Cana,                    the 30th ACM Joint European Software Engineering Conference
     Dominican Republic: Association for Computational Linguistics, Nov.               and Symposium on the Foundations of Software Engineering,
     2021, pp. 8696–8708.                                                              ser. ESEC/FSE 2022. New York, NY, USA: Association for
[47] J. Fan, Y. Li, S. Wang, and T. N. Nguyen, “A c/c++ code vulnerability             Computing Machinery, 2022, p. 959–971. [Online]. Available: https:
     dataset with code changes and cve summaries,” in Proceedings of the               //doi.org/10.1145/3540250.3549101
     17th International Conference on Mining Software Repositories, ser.          [67] E. Mashhadi and H. Hemmati, “Applying codebert for automated pro-
     MSR ’20. New York, NY, USA: Association for Computing Machinery,                  gram repair of java simple bugs,” in 2021 IEEE/ACM 18th International
     2020, p. 508–512.                                                                 Conference on Mining Software Repositories (MSR), 2021, pp. 505–509.
[48] G. Bhandari, A. Naseer, and L. Moonen, “Cvefixes: Automated collec-          [68] C. Lemieux, J. P. Inala, S. K. Lahiri, and S. Sen, “Codamosa: Escaping
     tion of vulnerabilities and their fixes from open-source software,” in            coverage plateaus in test generation with pre-trained large language
     Proceedings of the 17th International Conference on Predictive Models             models,” in Proceedings of the 45th International Conference on
     and Data Analytics in Software Engineering, ser. PROMISE 2021. New                Software Engineering, ser. ICSE ’23. IEEE Press, 2023, p. 919–931.
     York, NY, USA: Association for Computing Machinery, 2021, p. 30–39.               [Online]. Available: https://doi.org/10.1109/ICSE48619.2023.00085
[49] Z. Zeng, H. Tan, H. Zhang, J. Li, Y. Zhang, and L. Zhang, “An extensive      [69] Y. Deng, C. S. Xia, C. Yang, S. D. Zhang, S. Yang, and L. Zhang,
     study on pre-trained models for program understanding and generation,”            “Large language models are edge-case fuzzers: Testing deep learning
     in Proceedings of the 31st ACM SIGSOFT international symposium on                 libraries via fuzzgpt,” arXiv preprint arXiv:2304.02014, 2023.
     software testing and analysis, 2022, pp. 39–51.                              [70] Y. Deng, C. S. Xia, H. Peng, C. Yang, and L. Zhang, “Fuzzing
[50] OpenAI. (2023) Chatgpt. Accessed on Date. [Online]. Available:                    deep-learning libraries via large language models,” arXiv preprint
     https://openai.com/blog/chatgpt                                                   arXiv:2212.14834, 2022.
[51] Q. Guo and et al., “Exploring the potential of chatgpt in automated          [71] M. Tufano, D. Drain, A. Svyatkovskiy, and N. Sundaresan, “Generating
     code refinement: An empirical study,” arXiv, 2023, accessed 19 Oct.               accurate assert statements for unit test cases using pretrained
     2023. [Online]. Available: https://arxiv.org/abs/2309.08221                       transformers,” in Proceedings of the 3rd ACM/IEEE International
     Conference on Automation of Software Test, ser. AST ’22. New York,
     NY, USA: Association for Computing Machinery, 2022, p. 54–64.
     [Online]. Available: https://doi.org/10.1145/3524481.3527220
[72] P. Nie, R. Banerjee, J. J. Li, R. J. Mooney, and M. Gligoric, “Learning
     deep semantics for test completion,” arXiv preprint arXiv:2302.10166,
     2023.
[73] E. Dinella, G. Ryan, T. Mytkowicz, and S. K. Lahiri, “Toga: A
     neural method for test oracle generation,” in Proceedings of the 44th
     International Conference on Software Engineering, ser. ICSE ’22.
     New York, NY, USA: Association for Computing Machinery, 2022,
     p. 2130–2141. [Online]. Available: https://doi.org/10.1145/3510003.
     3510141
[74] M. Taeb, A. Swearngin, E. School, R. Cheng, Y. Jiang, and J. Nichols,
     “Axnav: Replaying accessibility tests from natural language,” arXiv
     preprint arXiv:2310.02424, 2023.
