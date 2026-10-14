                                               Reducing False Positives in Static Bug Detection with LLMs:
                                                            An Empirical Study in Industry
                                             Xueying Du1 , Jiayi Feng1 , Yi Zou1 , Wei Xu2 , Jie Ma2 , Wei Zhang2 , Sisi Liu2 , Xin Peng1 , Yiling Lou1 ∗†
                                                                                                        1 Fudan University

                                                                                                               China
                                                                                                              2 Tencent

                                                                                                               China
                                         ABSTRACT                                                                    To date, both academia and industry have proposed many static
                                         Static analysis tools (SATs) are widely adopted in both academia and        analysis tools (e.g., Github CodeQL [10], CppCheck [12], Facebook
                                         industry for improving software quality, yet their practical use is         Infer [24]), which are able to detect diverse bug types (e.g., Null-
arXiv:2601.18844v1 [cs.SE] 26 Jan 2026




                                         often hindered by high false positive rates, especially in large-scale      Pointer-Dereference and Use-After-Free) and have been widely
                                         enterprise systems. These false alarms demand substantial manual            adopted in practice [15, 23, 60].
                                         inspection, creating severe inefficiencies in industrial code review.          However, SATs often suffer from high false positive rates when
                                         While recent work has demonstrated the potential of large language          applied to large-scale software systems in practice. For example,
                                         models (LLMs) for false alarm reduction on open-source bench-               previous studies [15, 60] show that state-of-the-art open-source
                                         marks, their effectiveness in real-world enterprise settings remains        SATs (e.g., CodeQL and Infer) exhibit over 95% false alarm rates
                                         unclear. To bridge this gap, we conduct the first comprehensive em-         when detecting Null Pointer Dereference (NPD) bugs in large-scale
                                         pirical study of diverse LLM-based false alarm reduction techniques         projects such as the Linux Kernel. This limitation arises from the
                                         in an industrial context at Tencent, one of the largest IT companies        need to over-approximate program behaviors to guarantee sound-
                                         in China. Using data from Tencent’s enterprise-customized SAT               ness, producing spurious warnings along infeasible paths. The un-
                                         on its large-scale Advertising and Marketing Services software, we          derlying models of SATs typically abstract away complex features
                                         construct a dataset of 433 alarms (328 false positives, 105 true pos-       like pointer aliasing, external libraries, and conditional compilation,
                                         itives) covering three common bug types. Through interviewing               leading to mismatches with real-world behavior. Consequently,
                                         developers and analyzing the data, our results highlight the preva-         especially under heightened security requirements, the trade-off
                                         lence of false positives, which wastes substantial manual effort (e.g.,     between soundness and precision favors conservative reporting,
                                         10 - 20 minutes of manual inspection per alarm). Meanwhile, our             resulting in warnings that are formally justifiable but practically
                                         results show the huge potential of LLMs for reducing false alarms           infeasible, ultimately overwhelming developers with false alarms.
                                         in industrial settings (e.g., hybrid techniques of LLM and static              In practice, bug alarms reported by SATs would be manually
                                         analysis eliminate 94–98% of false positives with high recall). Fur-        inspected by developers to determine whether they correspond
                                         thermore, LLM-based techniques are cost-effective, with per-alarm           to true bugs or false positives. Such manual inspection is labor-
                                         costs as low as 2.1–109.5 seconds and $0.0011–$0.12, representing           intensive and time-consuming. Our survey within Tencent (i.e.,
                                         orders-of-magnitude savings compared to manual review. Finally,             one of the largest IT companies in China) reveals that developers
                                         our case analysis further identifies key limitations of LLM-based           spend on average more than 10 minutes reviewing one single static
                                         false alarm reduction in industrial settings.                               bug alarm, with many alarms even requiring multiple rounds of
                                                                                                                     inspection. Moreover, given the large scale of enterprise software
                                         CCS CONCEPTS                                                                codebase, one single scan can produce hundreds of alarms. There-
                                                                                                                     fore, the large volume of false positives leads to significant waste of
                                         • Software and its engineering → Maintaining software; • Com-
                                                                                                                     manual effort, highlighting the necessity of automatic false alarm
                                         puting methodologies → Artificial intelligence.
                                                                                                                     reduction techniques.
                                                                                                                        Traditional false alarm reduction techniques rely on symbolic
                                         KEYWORDS                                                                    execution [18, 31] or model checking [44, 54], which suffer from
                                         Static Bug Detection, Large Language Models, False Positives                scalability and generalization issues when applied to large-scale
                                                                                                                     enterprise software systems. Learning-based false positive reduc-
                                         1    INTRODUCTION                                                           tion techniques train neural networks on existing false and true
                                         Static analysis tools (SATs) play a crucial role in ensuring soft-          positives, which require massive labeled training data for each bug
                                         ware security, reliability, and maintainability. They scan codebases        type and thus have limited generalizability across different bug
                                         without extensive test execution [4–6, 48, 49, 51, 55, 63], facilitat-      types or for an enterprise where training data is unavailable. Re-
                                         ing early bug explosion during the software development process.            cently, given the rapid development of Large Language Models
                                                                                                                     (LLMs), some work [15, 60] proposes to reduce false alarms with
                                         ∗ Corresponding author
                                                                                                                     LLMs, and their experimental results have revealed the potential of
                                         † Authors’ Contact Information: Xueying Du, 21210240012@m.fudan.edu.cn;
                                                                                                                     LLMs in reducing false alarms reported by open-source SATs on
                                         Jiayi Feng, 23210240148@m.fudan.edu.cn; Yi Zou, zouy25@m.fudan.edu.cn;
                                         Wei Xu, davidxu@tencent.com; Jie Ma, jima@tencent.com; Wei Zhang,           synthetic and open-source projects (e.g., Juliet [25] and Gawk [20]).
                                         marserzhang@tencent.com; Sisi Liu, rainnyliu@tencent.com; Xin Peng,         Nevertheless, it still remains unclear how LLM-based false
                                         pengxin@fudan.edu.cn; Yiling Lou, yilinglou@fudan.edu.cn
Conference’17, July 2017, Washington, DC, USA                   Xueying Du1 , Jiayi Feng1 , Yi Zou1 , Wei Xu2 , Jie Ma2 , Wei Zhang2 , Sisi Liu2 , Xin Peng1 , Yiling Lou1


alarm reduction techniques perform in industry, i.e., for real-                 LLM-based techniques in reducing false positives for industrial
world proprietary enterprise software. In particular, (1) pro-                  software, e.g., LLMPFA, the hybrid techniques of static analysis
prietary enterprise software differs significantly from open-source             and LLMs, eliminates 94%–98% of false positives across different
software, especially for the code characteristics, development mod-             backbone LLMs while maintaining high recall.
els, and code review practices. For instance, enterprise codebases                 RQ3 (Cost analysis). We measure the time and money costs
typically enforce strict internal standards and follow rapid DevOps             of LLM-based false alarm reduction techniques when applied on
driven iterations, whereas open-source projects adopt more flexible,            Tencent datasets. In particular, the average time cost per alarm
community-defined norms and evolve at a slower pace. Moreover,                  ranges from 2.1 to 109.5 seconds, and the average expense per alarm
for code review practices, open-source projects benefit from exten-             is 0.0011$–0.12$. Such acceptable time and money costs make LLM-
sive peer reviews by diverse contributors, while proprietary enter-             based techniques especially valuable for supporting static false
prises tend to have more centralized reviews. These differences may             positive reduction in industrial practice, substantially reducing
impact the types and distributions of bugs in each environment.                 manual inspection effort (i.e., 10 - 20 minutes).
(2) Enterprise-customized SATs also differ a lot from open-source                  RQ4 (Breakdown and case analysis). We further perform
SATs (e.g., CodeQL). In fact, existing open-source SATs often fall              breakdown analysis and find the effectiveness variety of LLM-based
short of meeting the comprehensive and customized needs of en-                  false alarm reduction techniques across different bug categories. In
terprises, particularly in terms of efficiency, workflow integration,           particular, we find that most LLM-based techniques perform best
security, and cost. As a result, enterprises often develop customized           on Divide-by-Zero (DBZ) bugs, while their performance is lowest
SATs tailored to their specific needs and software. The performance             on Null Pointer Dereference (NPD) bugs. Moreover, we perform bad
differences between these enterprise-developed and open-source                  case analysis to identify the limitations of LLMs when applied to
tools can significantly influence the effectiveness of false positive           enterprise-scale bug detection, such as handling bugs of long code
reduction.                                                                      contexts, reasoning complex cascaded constraints, and insufficient
   To fill the knowledge gap, in this work, we perform an extensive             semantic understanding. These challenges remain future directions
study to empirically investigate how LLMs perform in reducing                   for advancing the effectiveness of LLMs-based false alarm reduction
static false alarms for large-scale industrial software systems at              in industry.
Tencent [53]. Tencent is one of the largest IT companies in China,                 To summarize, this paper makes the following contributions:
which covers diverse businesses such as social media, digital enter-              • Industrial Investigation. We interview developers and ana-
tainment, and cloud computing with billions of active users [9, 58].                 lyze real-world data within Tencent. Our analysis highlights
We collect data from the real-world static bug detection pipeline at                 the prevalence and serious impact from false positives reported
Tencent, which includes the bug alarms reported by its enterprise-                   by SATs in industrial settings.
customized SAT (i.e., BkCheck) on the large-scale software of its                 • Extensive Comparison. We conduct the first empirical study
Advertising and Marketing Services (AMS) business line (i.e., over                   to extensively investigate LLM-based false alarm techniques
hundreds of components). Based on the historical data, we con-                       in industrial settings. Our experiments cover a wide range of
struct a real-world industry false alarm reduction dataset of 433 bug                LLM-based techniques, including traditional learning-based
alarms (i.e., 328 false positives and 105 true positives), which covers              ones, basic LLMs, advanced prompting strategies, and hybrid
the three most frequent bug types, including Null Pointer Deref-                     techniques of LLMs and static analysis. We systematically eval-
erence (NPD), Out-of-Bounds (OOB), and Divide-by-Zero (DBZ)                          uate both the effectiveness and costs of LLM-based techniques
reported by BkCheck in Tencent. Based on our dataset, we empiri-                     in 433 real-world bug alarms collected from Tencent. While the
cally study the performance of LLMs in reducing false alarms for                     dataset cannot be released due to confidentiality, all methods
industrial software by answering the following research questions.                   and detailed results are available in our replication package [43].
   RQ1 (Prevalence of false positives in industry). We first                      • Insights and Implications. We perform both qualitative and
perform interviews with Tencent developers to investigate the                        quantitative analysis to show both the promise and limitations
application practice of SATs. SATs serve as a critical gated check-in                of LLM-based false alarm techniques in industry. Moreover, we
during the code review process at Tencent, and all the reported                      further discuss practical implications for both practitioners and
bug alarms would be manually reviewed by developers, with false                      researchers.
alarms proceeding to a second-round manual validation to avoid                     The remainder of this paper is organized as follows. Section 2
missing any potential bugs. False alarms are not only prevalent (i.e.,          presents related work. Section 3 introduces the dataset and the
over 76%), but also require massive manual inspection effort (i.e.,             detailed research settings. Section 4 presents the results and analysis.
on average 10 - 20 minutes per alarm).                                          Section 5 discusses our findings and presents implications for both
   RQ2 (Effectiveness of LLMs in reducing false alarms). We                     practitioners and researchers. Section 6 highlights the threats to
further evaluate a diverse range of different LLM-based false alarm             the validity of the study. Finally, Section 7 concludes the paper.
reduction techniques on Tencent datasets, including (1) basic LLMs,
(2) different advanced prompting strategies, (3) hybrid techniques              2 RELATED WORK
of static analysis and LLMs. Moreover, we also compare LLM-based
techniques with traditional learning-based techniques on Tencent                2.1 Enhancing LLMs in Vulnerability Detection
datasets. To the best of our knowledge, this is the most comprehen-             2.1.1 LLM-based Vulnerability Detection. The majority of exist-
sive evaluation on learning-based false alarm reduction of industrial           ing work focuses on prompt engineering [62, 68], such as chain-
software. Our experimental results show the strong potential of                 of-thought [59, 66] and few-shot learning [3], to facilitate more
Reducing False Positives in Static Bug Detection with LLMs:
An Empirical Study in Industry                                                                            Conference’17, July 2017, Washington, DC, USA


powerful LLM-based vulnerability detection. Additionally, recent            large-scale labeled training data for each bug type, which limits
work explores fine-tuning approaches [40, 47, 64] to enhance LLMs           their generalizability across different bug types or in an enterprise
in vulnerability detection. Furthermore, recent effort [16] explores        where training data is unavailable. Recent work combines LLMs
using historical vulnerability knowledge for retrieval-augmented            and static analysis information to identify false positives during
generation (RAG) to enhance LLMs’ vulnerability detection capabili-         static bug detection. Wen et al. [60] propose LLM4SA, which pro-
ties. Beyond these, further studies investigated different integration      vides LLMs with all the code contexts around the sink (e.g., callers
strategies to combine LLMs and static analysis to build more pow-           and callees of the sink and including hundreds of lines of code)
erful static bug detection techniques [22, 29, 30, 36, 52, 61, 65]. Li et   into one single prompt. Wang et al. [57] propose LLMDFA, which
al.[29] propose a framework that integrates UBITect with LLMs to            leverages few-shot chain-of-thought prompting to guide LLMs to
detect Use-Before-Initialization (UBI) bugs in the Linux kernel. Sun        analyze the path feasibility within each function. Du et al. [15]
et al. [52] employ LLMs to assist static analysis in identifying logic      propose LLM4PFA, which integrates static analysis–derived path
vulnerabilities in smart contracts. Li et al. [37] propose IRIS, which      constraints with agent-driven, context-aware reasoning, enabling
first leverages LLMs to identify the specifications of source/sinks         the model to more accurately assess source-to-sink reachability
for static analysis tools CodeQL for repository-level vulnerabil-           and thereby eliminate false positives caused by infeasible paths. Li
ity detection. Wang et al. [56] propose InferROI, which employs             et al. [32] propose BUGLENS, a post-refinement framework that
LLMs to infer resource-oriented intentions in code, combined with           guides LLMs through structured reasoning steps to assess security
a two-stage static analysis approach to inspect control-flow paths          impact and validate constraints from the source code. This work is
for potential resource leak detection.                                      parallel to ours.

2.1.2 Empirical Studies. Many efforts have been dedicated to eval-          2.2.3 Empirical Studies. Guo et al. [23] provide a comprehensive
uating LLMs in bug detection [14, 19, 26], covering diverse bench-          review of various methods for mitigating false positive static anal-
marks, LLMs, and metrics. However, these benchmarks are primar-             ysis warnings, highlighting the key challenges in this field based
ily derived from synthetic datasets (e.g., Juliet [25]) and open-source     on their survey results. Specifically, their study categorizes false
projects, whose bug distributions may differ significantly from those       positive elimination methods into five distinct approaches: Statisti-
encountered in real-world proprietary enterprise codebases. Fur-            cal Probability, Dynamic Program Testing, Machine learning, and
thermore, prior work has not systematically evaluated the ability           Clustering. However, their study does not explore the potential of
of LLMs to reduce false positives in static bug detection. This study       LLMs in mitigating false positives. Moreover, it focuses on false
fills this research gap by providing a comprehensive evaluation of          positives from open-source static analyzers, offering limited insight
LLMs in the context of false positive reduction in enterprise-level         into the effectiveness and challenges of addressing false positives in
static bug detection.                                                       enterprise settings. In addition, several works conduct evaluations
                                                                            and empirical studies of static analysis tools. Li et al. [33] and Lipp
                                                                            et al. [38] compare and evaluate the effectiveness and performance
2.2     False Positive Elimination in Bug Detection
                                                                            of JAVA and C SASTs, respectively. Ami et al. [1] conduct in-depth
2.2.1 Static Analysis-Based False Positive Elimination. A number of         interviews with 20 practitioners to investigate how developers per-
studies have explored the use of more precise static analysis tech-         ceive, select, and use SASTs. Li et al. [35] investigate why industrial
niques to identify and eliminate false positives from bug reports.          professionals utilize SAST benchmarks, identify barriers to their us-
These efforts primarily fall into two categories: model checking-           age, and explore potential improvements for existing benchmarks.
based and symbolic execution-based approaches. Model checking-              However, these works do not provide a comprehensive study of
based approaches [44, 54] abstract the program into a finite-state          SAST false positives and how to systematically eliminate them. Our
model and use formal verification tools to exhaustively explore all         work fills this gap.
possible execution states in order to determine the feasibility of
reported paths. Symbolic execution-based approaches [18, 31] sym-           3     RESEARCH SETTING
bolically execute the program to collect path constraints and verify
                                                                            The goal of our empirical study is to investigate the prevalence of
path feasibility using SMT solvers. Despite their precision, both cat-
                                                                            false positives produced by static analysis tools in industrial code-
egories face significant challenges. Exhaustively exploring all paths
                                                                            bases and to evaluate the effectiveness of existing learning–based
leads to path explosion, and their implementations are often tightly
                                                                            approaches in mitigating these false positives. This section outlines
coupled with specific static analyzers or require handcrafted rules
                                                                            the overall research setting. Section 3.1 details how we collected
for different vulnerability types, resulting in poor generalization
                                                                            real-world false positive data from an internal static analyzer within
and restricting their application to large-scale systems.
                                                                            Tencent. Section 3.2 introduces the research questions that guide
2.2.2 Learning-Based False Positive Elimination. With the rise of           this study and the specific settings for each research question.
deep learning, several approaches have been proposed to train pre-
dictive models that distinguish real bugs from false positives based        3.1    Data Collection
on features extracted from source code or warning reports. Lee et           We collected data from the main repositories of Tencent’s Adver-
al.[28] train a convolutional neural network (CNN) to learn lexical         tising division, encompassing all projects within the Advertising
patterns from code segments that trigger alarms. Kharkar et al.[27]         and Marketing Services (AMS) business line. The dataset covers
adopt a Transformer-based model to identify false positive warn-            warnings reported between September 2024 and June 2025, includ-
ings. However, these supervised learning-based approaches require           ing both real bugs and false positives. The overall data analysis and
Conference’17, July 2017, Washington, DC, USA                                            Xueying Du1 , Jiayi Feng1 , Yi Zou1 , Wei Xu2 , Jie Ma2 , Wei Zhang2 , Sisi Liu2 , Xin Peng1 , Yiling Lou1


collection pipeline is summarized in Table 1. In particular, the pro-                                    Data Collection. We constructed our dataset from the finalized
cess involves three key steps: (1) Automated scanning. A static                                          bug report forms generated during the above review phase. These
analyzer was applied to the codebases to generate warnings. (2)                                          forms contained 35 categories of bugs, as well as a portion of un-
Manual review. Enterprise code reviewers manually examined the                                           categorized cases. Bug Types. For this study, we selected the three
warnings to determine whether they represented real bugs or false                                        most frequently occurring and developer-validated categories: Null
positives. (3) Data collection. We collected the verified outcomes                                       Pointer Dereference (NPD), Out-of-Bounds (OOB), and Divide-by-
from the manual review records, followed by a secondary validation                                       Zero (DBZ). These categories accounted for approximately 52%,
to ensure correctness and data integrity.                                                                24%, and 10% of all recorded warnings, respectively, covering 86%
        a. Automated Scanning                                b. Manual Review
                                                                                                         in total and highlighting their significant impact on enterprise-scale
                                                                                                         software systems. Filtering Criteria. We systematically extracted all
       BkCheck
                                                 Developer      Reviewer                                 records of these three categories between September 2024 and June
                                                  Review        Validation
 Static Analyzer
                                Static
                               Warnings
                                                                                                         2025. Although our double checks revealed no correctness issues
                                                      Manual Review
                                                                                 Bug Report Forms        in the review forms, certain entries corresponded to deprecated
                                   c. Data collection                                                    code or contained incomplete contextual information, which could
                                                                                                         compromise the fairness of the evaluation. To ensure the rigor and
False Positives
  Real Bugs          Dataset
                                                Data                    Bug Report                       reliability of the dataset, we applied the following filtering crite-
                                              Filtering                  Retrieval
                                                                                                         ria: (1) Records associated with deprecated code were removed. (2)
                   Figure 1: Overview of Data Collection                                                 Records with incomplete code information or unavailable depen-
                                                                                                         dent context were excluded. (3) Cases with unresolved uncertainty
Static Analyzer. Mature open-source and commercial static analy-                                         regarding false positive status were discarded. (4) Duplicate records
sis tools often fall short of meeting the comprehensive requirements                                     were eliminated. Data Statistics. After filtering, we obtained a total
of enterprises during code review, particularly with respect to effi-                                    of 328 false positives and 105 real bugs. Table 1 summarizes the
ciency, workflow integration, security, and cost. As a result, Tencent                                   detailed statistics of the resulting dataset.
developed its own static analysis tool, BkCheck, to support large-                                                          Table 1: Statistics of Dataset
scale static scanning ensuring both high efficiency and security.
                                                                                                           Type        False Alarm Number                 Real Bug Number                Total
BkCheck is a proprietary static analysis tool developed by Ten-
                                                                                                           NPD                  107                               29                      136
cent’s CodeCC platform. It covers a wide range of detection rules,                                         DBZ                  139                               19                      158
including null pointer dereference, logic defects, divide-by-zero                                          OOB                  82                                57                      139
errors, and memory leaks. Compared to compiler-based analyzers                                             Total                328                              105                      433
such as Coverity [11] and CodeQL [10], BkCheck does not require
code compilation, which allows for faster scans and seamless inte-
gration into large-scale industrial projects. It has been widely de-
ployed in numerous flagship Tencent products, including WeChat                                           3.2      Research Questions
Pay and many popular Tencent games.                                                                      Based on the enterprise-level dataset we collected in real-world
Manual Review. During the code review phase, both developers                                             static bug detection, we addressed the following research questions:
and professional code reviewers manually inspected the warnings
reported by static analyzers. The review process consisted of two
independent rounds conducted by different reviewers. In the first                                          Research Question 1 (Prevalence of false positives in in-
round, developers examined each warning together with the corre-                                           dustry): What is the prevalence of false positives generated by
sponding code to determine whether it was a false positive or a real                                       static analysis tools in industrial practice?
bug. For warnings identified as false positives, developers were re-
quired to document the reason; for real bugs, the analyzer-reported                                         To answer this question, we first perform interviews with Ten-
root cause was retained. In the second round, dedicated code re-                                         cent developers to investigate the application practice of SATs, as
viewers validated the results of the first round by re-examining                                         well as analyzed the collected data. Specifically, we investigate (1)
the code, warnings, and the initial annotations. The final outcomes                                      the industrial use of SATs in Tencent (i.e., how SATs are integrated
from both rounds were consolidated into specialized bug report                                           into the code review workflow), (2) the false positive rates, and (3)
forms, which recorded the code snippet, bug category, and final                                          the manual effort spent in validating reported false alarms.
review decision. It is worth noting that this review phase is part                                          Interview Protocol. We designed an online survey question-
of Tencent’s routine code review workflow. As such, the resulting                                        naire containing open-ended questions to guide the interviews. The
manual annotations reflect the professional judgment of experi-                                          study protocol was approved by the Institutional Review Boards
enced enterprise developers and reviewers regarding false positives                                      (IRBs) of the authors’ institutions. The complete list of interview
and real bugs. Consistent with the “security-first” principle, it is                                     questions is provided in our replication package [43].
highly unlikely that true positives were inadvertently discarded. In                                        Interview Recruitment. We recruited five participants from
cases where reviewers could not reach a definitive conclusion, the                                       Tencent’s Advertising and Marketing Services (AMS) business line
warning was marked as unresolved for follow-up verification by                                           who were directly involved in software development and code
more senior reviewers.                                                                                   review. The group consisted of two developers and three code re-
                                                                                                         viewers, each with more than five years of professional experience.
Reducing False Positives in Static Bug Detection with LLMs:
An Empirical Study in Industry                                                                         Conference’17, July 2017, Washington, DC, USA


  Research Question 2 (Effectiveness of LLMs in reducing                  • LLM4SA [60] leverages LLMs to directly analyze bug warning
  false alarms): How effective are a diverse range of LLM-based              reports generated by static analysis tools. It supplies the model
  techniques in reducing false alarms?                                       with extensive code context surrounding the reported sink
                                                                             (e.g., callers, callees, and hundreds of lines of relevant code) and
                                                                             prompts the LLM to determine whether the warning constitutes
                                                                             a false positive.
   With the rapid advancement of LLMs, they have demonstrated
promising performance across a wide range of code-related tasks.          • LLM4PFA [15] improves complex inter-procedural path fea-
Their vulnerability detection capabilities have also been validated          sibility analysis to reduce false positives reported by static
on synthetic datasets (e.g., Juliet [25]) and relatively simple open-        bug analyzers. Specifically, LLM4PFA integrates static analy-
source function-level datasets (e.g., Devign [70]). This research            sis–derived path constraints with agent-driven, context-aware
question first investigates the practical effectiveness of LLMs in           reasoning, enabling the model to more accurately assess source-
reducing false positives generated by SATs on real-world industrial          to-sink reachability and thereby eliminate false positives caused
data. Specifically, we address the following four questions:                 by infeasible paths.
                                                                           Although several other hybrid methods could also be used for
     • RQ2.a. What is the effectiveness of directly applying differ-    false positive reduction, they cannot be directly applied to our tar-
       ent LLMs?                                                        get codebase for two reasons: (1) Tool dependency. For example,
     • RQ2.b. What is the effectiveness of employing advanced           IRIS [37] relies on CodeQL for core taint analysis; however, CodeQL
       prompting strategies with LLMs?                                  requires a fully compilable repository, which limits its generaliz-
     • RQ2.c. What is the effectiveness of advanced LLM-based           ability to our studied large-scale industrial codebase. (2) Bug-type
       methods combined with static analysis in reducing false          constraints. For instance, several bug types in our dataset fall out-
       positives?                                                       side the types supported by LLMDFA [57]. Therefore, we study
     • RQ2.d. How do LLM-based techniques compare with tradi-           LLM4SA and LLM4PFA given their easy adoption to our studied
       tional learning-based techniques in reducing false positives?    industrial codebases. Due to space limitations, we do not include the
                                                                        detailed prompts here. All implementation code for the baselines is
Model selection. To evaluate the impact of different backbone
                                                                        available in our replication package [43].
LLMs, we selected four representative state-of-the-art models that
                                                                        Compare with traditional learning-based techniques. To in-
are widely adopted in bug detection tasks. These include two closed-
                                                                        vestigate this, we first surveyed review studies evaluating learning-
source models, GPT-4o [21] and Claude-Opus-4 [8], as well as two
                                                                        based models for vulnerability detection [7, 42, 50] and selected
open-source models, Qwen-3-Coder [45] and DeepSeek-R1 [13].
                                                                        four representative state-of-the-art methods. These include two
Prompting strategies. Beyond a basic prompt setting, we adopt
                                                                        graph neural network (GNN)–based approaches and two methods
three most widely used and representative prompting strategies
                                                                        that fine-tune pre-trained language models (PLMs):
following previous research [39, 46, 67].
                                                                           GNN-based methods:
     • Chain-of-Thought (CoT) strategy [59, 66] explicitly guides
                                                                          • Devign [70]: A GNN-based vulnerability detection model that
       LLMs to perform step-by-step reasoning, thereby improving
                                                                             constructs a composite graph representation of source code by
       their ability to handle complex logical dependencies when
                                                                             integrating multiple program structures, including the abstract
       assessing whether a warning is a false positive.
                                                                             syntax tree (AST), control-flow graph (CFG), and data-flow
     • Few-shot learning strategy [3] provides LLMs with repre-              graph (DFG), then applies GNNs to learn semantic features
       sentative examples of both false positives and real bugs. By          from this graph representation for vulnerability prediction.
       observing these demonstrations, LLMs learn decision bound-
                                                                          • ReGVD [41]: A GNN-based model combines two GNN vari-
       aries and make more accurate, expert-like classifications.
                                                                             ants, ReGGNN and ReGCN, to enhance graph representation
     • Bug-type augmentation [69] enriches prompts with struc-               learning, thereby improving vulnerability detection accuracy.
       tured bug types description information as bug knowledge            PLM-based methods:
       to LLMs. This strategy supplies LLMs with explicit semantic        • LLMAO [64]: A PLM-based fault localization approach that
       cues about common bug patterns, enabling more informed                fine-tunes CodeGen on fault localization and vulnerability de-
       reasoning over static analysis warnings.                              tection datasets to improve detection precision.
   Both few-shot learning and bug-type augmentation can be re-
                                                                          • LineVul [17]: A PLM-based vulnerability detection model that
garded as forms of domain knowledge enhancement. Bug-type
                                                                             fine-tunes CodeBERT, offering both function-level and line-
augmentation provides relatively general domain knowledge, while
                                                                             level detection capabilities.
few-shot learning offers concrete representative examples that serve
as domain-specific guidance.                                              Research Question 3 (Costs Analysis): What are the costs
Hybrid methods between LLM and static analysis. Recent                    of using LLMs in false positives reduction?
studies [15, 60] have proposed LLM-based approaches that explicitly
integrate static analysis information for false positive reduction.        This RQ examines the practical costs of deploying LLM-based
However, these works have only been evaluated on open-source            approaches for false positive reduction in enterprise settings. Al-
datasets, and their effectiveness in real-world industrial settings     though LLMs demonstrate strong potential for mitigating false
remains uncertain. To bridge this gap, we evaluate the following        positives, their adoption in industrial settings must also account
methods on our enterprise dataset:                                      for associated costs. We focus on two dimensions of cost:
Conference’17, July 2017, Washington, DC, USA                   Xueying Du1 , Jiayi Feng1 , Yi Zou1 , Wei Xu2 , Jie Ma2 , Wei Zhang2 , Sisi Liu2 , Xin Peng1 , Yiling Lou1


     • Response time costs: The average response time per case                  Industrial Practice of SATs. As illustrated in Figure 2, BkCheck,
        for different LLMs and methods.                                         Tencent’s enterprise-customized SAT, functions as a critical gated
     • Economic costs: The monetary expense associated with                     check-in by scanning each commit. The reported bug alarms un-
        API usage, measured as the average cost per case across                 dergo up to two rounds of manual inspection: first, developers
        models and methods.                                                     manually review all reported alarms, and then those identified as
   By analyzing these factors, we aim to provide a comprehensive                false alarms are subjected to a second-round validation by a differ-
assessment of the feasibility and sustainability of adopting LLMs               ent reviewer to minimize the risk of overlooking potential bugs.
for false positive reduction in enterprise environments.                        Overall, SATs play a fundamental role in industrial software quality
                                                                                assurance, with their reported alarms being taken seriously as part
  Research Question 4 (Breakdown and case analysis): How                        of the enterprise code review process.
  do LLMs perform in reducing false positives across different
                                                                                                   a. Automated Scanning                                b. Manual Review
  vulnerability categories, and what are their limitations?
                                                                                                             Return to fix


Breakdown Analysis. False positives generated by static analysis                              Push             Run static                          True alarms
                                                                                             changes            checker
tools may differ significantly across vulnerability categories, as each                                                      Bug alarms                                        SAFE

category involves distinct bug patterns and detection challenges. To            Developers                     BkCheck                    Manual
                                                                                                                                          Review
                                                                                                                                                   False alarms      Manual
                                                                                                                                                                     Confirm
better understand these variations, we investigate the performance                                       Self-developed checker
                                                                                                               in Tencent
                                                                                                                                                      90%+

of LLMs in reducing false positives across the three most frequent
and impactful categories in our dataset: Null Pointer Dereference                       Figure 2: Overview of Code Review in Tencent
(NPD), Divide-by-Zero (DBZ), and Out-of-Bounds (OOB). This re-                  High False Positive Rate. In our final dataset from Tencent, the
search question aims to reveal whether LLMs exhibit consistent                  proportion of false positives was at 76% (e.g., 328 false positives
effectiveness across categories.                                                and 105 true bugs). In fact, the real-world distribution of false posi-
Case Analysis. We perform bad case analysis to better understand                tives could be even higher as a substantial number of false-positive
the limitations of LLMs in identifying false positives. This analysis           records are excluded from our final dataset due to incomplete or
provides deeper insights into two dimensions:(i) Error Patterns. We             inaccessible code contexts. When accounting for these discarded
categorize the representative bad cases where LLMs misdistinguish               cases, the false positive rate of static warnings is higher than 90%.
between false positives and real bugs, and further analyze the con-             Such a high false positive rate stems from a design trade-off: enter-
ditions under which the LLMs’ reasoning capabilities fall short. (ii)           prise static analysis tools prioritize recall over precision to ensure
Root Causes. We further investigate the underlying reasons behind               that no potential bugs are overlooked. Consequently, false positive
these bad cases, thereby providing a systematic understanding of                rates in enterprise settings are even higher than those of many
the inherent limitations of LLMs in static bug detection.                       open-source analyzers.
                                                                                High Manual Effort for Validation. As shown in Figure 2, each
4 RESULT AND ANALYSIS                                                           reported bug alarm undergoes up to two rounds of manual inspec-
                                                                                tion to minimize the risk of overlooking potential bug. Based on
4.1 Metrics and Setup
                                                                                our interviews, the average time required to examine a single alarm
For effectiveness evaluation (i.e, RQ2-RQ4), we use four commonly-              was approximately 10 minutes per round. As a result, one single
adopted metrics in bug detection tasks: accuracy, precision, recall,            bug alarm would cost 10 to 20 minutes of manual inspection effort.
and F1. Additionally, we use two metrics introduced in LLM4PFA [15]             As hundreds of alarms can be reported by SATs for scanning large-
to evaluate the effectiveness in identifying false positives generated          scale enterprise software, significant human effort are wasted for
by static analyzers: False Positive Reduction Precision (FPR_P) and             inspecting false alarms in practice.
False Positive Reduction Recall (FPR_R), which specifically measure
the precision and recall for negative samples (i.e., false positives)             Answer to RQ1: SATs play a fundamental role in industrial
in the dataset.                                                                   software quality assurance, with their reported alarms being
                                                                                  taken seriously as part of the enterprise code review process.
                            TN                  TN                                However, false alarms are extremely prevalent (i.e., with 90%
                FPR_P =            FPR_R =
                        TN + FN              TN + FP                              false alarm rate). Meanwhile, substantial manual effort is wasted
   To mitigate potential concerns regarding LLM randomness, we                    to inspect reported bug alarms, with one false alarm on average
executed each query three times per case and adopted a majority-                  taking 10 to 20 minutes of manual inspection. Consequently,
vote strategy to determine the final outcome. For traditional deep-               the automatic reduction of false positives in SATs is a critical
learning based methods, we directly applied the models trained on                 and urgent need in enterprise code review processes.
the original datasets used in their papers to conduct experiments,
since no enterprise-level training dataset is publicly available.
                                                                                4.3           RQ2: Effectiveness of LLMs in Reducing
4.2     RQ1: Prevalence of False Positives                                                    False Alarms
We conducted interviews with five participants and analyzed their               To investigate the effectiveness of LLMs in reducing false positives,
responses to the survey questionnaire. Based on this analysis, we               we conduct a comprehensive evaluation of various LLM-based false
derived the following interview results:                                        alarm reduction techniques on our Tencent datasets. Moreover, we
Reducing False Positives in Static Bug Detection with LLMs:
An Empirical Study in Industry                                                                       Conference’17, July 2017, Washington, DC, USA


compare the performance of LLM-based approaches with that of            studies [16] have shown that learning-based approaches often strug-
traditional learning-based methods.                                     gle to capture the true root causes of bugs. Instead, they tend to
                                                                        rely on superficial statistical patterns or secondary code features
4.3.1 Effectiveness of various LLM-based false alarm reduction tech-
                                                                        correlated with buggy functions. As a result, these methods are
niques. Table 2 compares the performance of all LLM-based false
                                                                        inherently limited in their ability to generalize to real-world enter-
alarm reduction techniques on our Tencent dataset using various
                                                                        prise bug detection.
backbone LLMs.
                                                                        Methods Comparison. Although Linevul reports a seemingly
Overall Effectiveness. LLMs demonstrate strong potential for
                                                                        high accuracy of 0.76, this result stems from its tendency to classify
static false positive reduction, with hybrid methods that combine
                                                                        all warnings as false positives. Since our dataset contains a large
LLMs and static analysis (i.e., LLM4SA and LLM4PFA) achieving
                                                                        proportion of false positive cases, this bias inflates its accuracy
the highest accuracy of 0.93-0.94. These LLM-based approaches
                                                                        but undermines practical value. A likely reason is that LineVul
also provide a degree of interpretability, making their outputs more
                                                                        was trained on the highly imbalanced BigVul dataset, where most
available to subsequent human validation.
                                                                        samples are non-vulnerable. By contrast, the other methods all
Method Comparison. Across all evaluated strategies, methods
                                                                        achieve accuracies below 0.44. Among them, ReGVD stands out due
combining LLMs with static analysis (i.e., LLM4SA and LLM4PFA)
                                                                        to its comparatively high recall of 0.87. However, its false positive
outperform standalone LLMs with different prompting strategies,
                                                                        recall is only 0.19, meaning that it only successfully eliminates
which in turn surpass basic prompt–only methods. Among prompt-
                                                                        19% of false positives. This limited effectiveness in reducing false
ing strategies, Chain-of-Thought (CoT) delivers the weakest perfor-
                                                                        alarms still imposes substantial manual validation costs, restricting
mance, even underperforming basic prompts in some cases. This
                                                                        its overall practical benefit.
may be due to these advanced LLMs have already internalized
                                                                        Interpretability. Traditional learning-based methods inherently
reasoning capabilities during the training process, and explicitly
                                                                        suffer from poor interpretability. Their outputs are limited to pre-
enforcing CoT prompts can paradoxically degrade performance.
                                                                        dicted labels without any explanatory context, which increases the
In contrast, few-shot enhanced prompting consistently yields the
                                                                        burden of manual validation during enterprise code review. In con-
best results among the three prompt strategies, underscoring the
                                                                        trast, LLM-based methods provide natural language explanations
value of providing concrete examples to guide LLM reasoning. Both
                                                                        alongside predictions. These explanations significantly support
LLM4SA and LLM4PFA not only demonstrate strong effectiveness,
                                                                        human reviewers.
with all backbone LLMs achieving accuracy rates above 0.86, but
also exhibit greater stability across different backbone LLMs com-       Answer to RQ2: LLMs demonstrate strong potential for reduc-
pared to methods relying solely on prompt strategies. These results      ing the false positives reported by SATs in industrial settings.
further validate the potential of integrating LLMs with static analy-    Among all LLM-based approaches, hybrid techniques that inte-
sis for effective false positive reduction.                              grate LLMs with static analysis (i.e., LLM4PFA) achieve the best
Generalization Across LLMs. Overall, the four state-of-the-art           effectiveness, successfully eliminating 94–98% of false positives
LLMs exhibit comparable levels of effectiveness, though their rela-      across different backbone LLMs while maintaining high re-
tive strengths vary across methods and prompting strategies. For         call. In contrast, traditional learning-based vulnerability detec-
instance, Claude performs competitively with bug-type–enhanced           tion methods perform poorly due to the scarcity of large-scale,
and few-shot–enhanced prompts, but its performance is noticeably         high-quality enterprise training data. Furthermore, LLM-based
weaker with basic prompts. In contrast, Qwen-3-Coder delivers            methods offer superior interpretability by augmenting label-
the most consistent performance across all prompting strategies.         only predictions with natural language explanations, thereby
Importantly, LLM4PFA exhibits strong generalization across all           increasing the practicality and usability of their outputs for
models, achieving accuracy above 0.93 in every case. Given that          subsequent manual validation.
enterprises typically prioritize recall over precision, LLM4PFA with
Claude (recall = 0.88) and DeepSeek-R1 (recall = 0.86) are more         4.4    RQ3: Costs Analysis
suitable for industrial practice.
                                                                        In order to provide a comprehensive assessment of the feasibility
4.3.2 Compare with traditional learning-based techniques. Table 3       and sustainability of adopting LLMs for false positive reduction
presents the results of four representative deep learning–based         in enterprise environments, Table 4 compares the time costs and
vulnerability detection methods on our Tencent dataset.                 economic costs of different LLM-based methods using various back-
Overall Effectiveness. Overall, all evaluated LLM-based meth-           bone LLMs.
ods consistently outperform deep learning approaches. The latter           Overall, LLM-based methods fall well within the acceptable range
exhibited markedly poor performance, with the highest accuracy          of both time and economic costs for an enterprise environment.
reaching only from 0.36 to 0.44 (except for LineVul). Two key fac-      Time Cost Analysis. The average processing cost per alarm ranges
tors may account for this limitation. First, deep learning–based        from 2.1 to 109.5 seconds, depending on the specific method and
methods are highly dependent on training data distribution. These       backbone model. Even the most time-consuming LLM, DeepSeek-
learning-based models trained on existing benchmark datasets per-       R1 (i.e, about 1-2 minutes per warning), remains substantially lower
form poorly when directly applied to previously unseen enterprise       than manual validation, which requires approximately 20 minutes
code, where large-scale, labeled training data is scarce. This lack     per warning across multiple review rounds. Moreover, when in-
of sufficient domain-specific training data makes fine-tuning such      tegrated with DeepSeek, LLM4PFA achieves an accuracy of 0.93
models for enterprise use particularly challenging. Second, prior       while maintaining a recall of 0.86, making it highly effective for
Conference’17, July 2017, Washington, DC, USA                            Xueying Du1 , Jiayi Feng1 , Yi Zou1 , Wei Xu2 , Jie Ma2 , Wei Zhang2 , Sisi Liu2 , Xin Peng1 , Yiling Lou1


                                        Table 2: Effectiveness of LLM-based Methods with different LLMs
                                   Technique               Model        Accuracy       Precision       Recall       F1     FPR_P        FPR_R
                                                          GPT-4o          0.50            0.28          0.66       0.39     0.80         0.45
                                                       Claude-Opus-4      0.40            0.26          0.83       0.40     0.83         0.26
                                  Basic Prompt
                                                       Qwen-3-Coder       0.55            0.29          0.62       0.40     0.81         0.52
                                                        DeepSeek-R1       0.43            0.27          0.84       0.41     0.85         0.29
                                                          GPT-4o          0.49            0.29          0.76       0.42     0.84         0.40
                                                       Claude-Opus-4      0.42            0.29          0.94       0.44     0.93         0.25
                                  Cot Enhanced
                                                       Qwen-3-Coder       0.48            0.29          0.79       0.42     0.85         0.38
                                                        DeepSeek-R1       0.40            0.28          0.90       0.42     0.89         0.24
                                                          GPT-4o          0.50            0.26          0.64       0.37     0.79         0.43
                                                       Claude-Opus-4      0.72            0.46          0.74       0.57     0.90         0.72
                                Few-shot Enhanced
                                                       Qwen-3-Coder       0.71            0.40          0.59       0.48     0.85         0.72
                                                        DeepSeek-R1       0.69            0.43          0.83       0.56     0.92         0.65
                                                          GPT-4o          0.53            0.27          0.54       0.36     0.78         0.52
                                                       Claude-Opus-4      0.67            0.41          0.87       0.56     0.93         0.60
                                Bug Type Enhanced
                                                       Qwen-3-Coder       0.65            0.37          0.64       0.47     0.85         0.65
                                                        DeepSeek-R1       0.64            0.38          0.83       0.52     0.91         0.57
                                                          GPT-4o          0.86            0.63          0.84       0.72     0.94         0.84
                                                       Claude-Opus-4      0.89            0.68          0.72       0.70     0.91         0.89
                                      LLM4SA
                                                       Qwen-3-Coder       0.92            0.85          0.65       0.74     0.90         0.96
                                                        DeepSeek-R1       0.91            0.77          0.86       0.81     0.95         0.92
                                                          GPT-4o          0.93           0.93           0.75       0.83     0.93         0.98
                                                       Claude-Opus-4      0.93            0.83          0.88       0.85     0.96         0.94
                                    LLM4PFA
                                                       Qwen-3-Coder       0.94           0.93           0.79       0.86     0.94         0.98
                                                        DeepSeek-R1       0.93            0.84          0.86       0.85     0.95         0.95

Table 3: Effectiveness of traditional learning-based methods                               per alarm ranges from 2.1 to 109.5 seconds, while the expense
   Tech.       Acc.      Pre.      Recall        F1     FPR_P       FPR_R
                                                                                           per alarm remains as low as $0.0011–$0.12. Compared to the
  Devign       0.44      0.35       0.61        0.44     0.60        0.34                  10–20 minutes typically required for manual inspection, these
  ReGVD        0.36      0.26       0.87        0.39     0.82        0.19                  techniques offer a substantial reduction in developer effort, un-
  LLMAO        0.36      0.22       0.67        0.34     0.71        0.26                  derscoring their practical value for mitigating false positives in
  LineVul      0.76      0.00       0.00        0.00     0.76        1.00                  static analysis within industry.

 Table 4: Cost of LLM-based Methods with different LLMs
                                                                                         4.5      RQ4: Breakdown and Case Analysis
       Tech.              Model         Ave. time cost (s)   Ave. API cost ($)
                         GPT-4o                 5.9                0.015                 Breakdown Analysis. Figure 3 illustrates the effectiveness vari-
                      Claude-Opus-4            12.8                0.065                 ety of LLM-based false alarm reduction techniques across different
   Basic Prompt
                      Qwen-3-Coder              2.1               0.0013
                       DeepSeek-R1             109.5              0.0046                 bug categories. Overall, the effectiveness of different LLM-based
                         GPT-4o                 7.9                0.020                 methods varies across bug categories. Almost all methods achieve
                      Claude-Opus-4            14.8                0.120                 their best performance on Divide-by-Zero (DBZ) bugs, largely be-
 Few-shot Prompt
                      Qwen-3-Coder              8.1               0.0011
                       DeepSeek-R1             60.5               0.0018                 cause the bug patterns in this category are relatively simple and
                         GPT-4o                 8.6                0.017                 consistent, making them easier for LLMs to identify. In contrast,
                      Claude-Opus-4            15.2                0.094                 Null Pointer Dereference (NPD) bugs exhibit more complex and
     LLM4SA
                      Qwen-3-Coder             17.2               0.0084
                       DeepSeek-R1             60.2               0.0024                 diverse patterns. Moreover, many NPD false positive cases involve
                         GPT-4o                12.6                0.020                 intricate conditional constraints, which pose significant challenges
                      Claude-Opus-4            16.7                0.120                 for LLMs to reason accurately about program behavior, resulting
     LLM4PFA
                      Qwen-3-Coder             16.1               0.0056
                       DeepSeek-R1             58.3               0.0025                 in comparatively lower performance in this category.
assisting enterprises in false positive reduction, as it can replace                      Answer to RQ4 (Breakdown Analysis): The effectiveness
at least one round of manual review and save considerable human                           of LLM-based methods vary across different bug categories. In
effort without compromising reliability.                                                  Tencent datasets, LLM-based methods achieve the best perfor-
Economic Cost Analysis. The average expense per alarm is 0.0011$                          mance on Divide-by-Zero (DBZ) bugs, while their performance
– 0.12$. In addition, two open-source models can be deployed within                       is lowest on Null Pointer Dereference (NPD) bugs.
enterprise infrastructure, eliminating API-related costs. Even the
most expensive commercial model (i.e., Claude-Opus-4, 0.12$ per                          Case Analysis. To better understand the limitations of LLMs in
warning) remains negligible compared to the substantial savings in                       reducing false positives, we conducted a manual analysis of two
manual effort, underscoring the usability of LLM-based approaches.                       types of failure cases: (1) cases where different prompt strategies
                                                                                         failed to help LLMs distinguish between false positives and real
 Answer to RQ3: LLM-based false alarm reduction techniques                               bugs, and (2) cases where all methods failed to classify correctly.
 are cost-effective in industrial settings, incurring both accept-                       Although confidentiality constraints prevent us from presenting the
 able time and economic costs. On average, the processing time                           actual code examples, our analysis reveals several key limitations
                                                                                         of LLMs in bug detection.
Reducing False Positives in Static Bug Detection with LLMs:
An Empirical Study in Industry                                                                                                                                                                                                                                          Conference’17, July 2017, Washington, DC, USA


                                        Type                                                                                                                                           Type




                                                                                                                                                                                                                                                                                                            1.00
                                                                                                                                                                                                                                                                                                            0.99
                                                                                                                                                           0.97
                                               NPD                                                                                                                                            NPD




                                                                                                                                             0.95




                                                                                                                                                                                                                                                                                                          0.95
                              1.0                                                                                                                                         1.0




                                                                                                                                                                                                                                                                                                 0.94
                                                                                                                                                        0.92
                                               OOB                                                                                                                                            OOB




                                                                                                                                                      0.88
                                                                                                                                      0.83




                                                                                                                                                                                                                                                                                          0.82
                                               DBZ                                                                                                                                            DBZ




                                                                                                                                   0.77




                                                                                                                                                                                                                                                                        0.77



                                                                                                                                                                                                                                                                                       0.75
                              0.8                                                                                                                                         0.8




                                                                                                 0.70




                                                                                                                                                                                                                                                    0.65
                                                      0.64




                                                                                                                     0.63




                                                                                                                                                                                                     0.61
                                                                                                                    0.59
                   Accuracy




                                                                                                                                                                                                                                                                               0.59
                                                                                                                                                                  FPR_R
                              0.6                                                                                                                                         0.6




                                                                 0.52
                                               0.51



                                                               0.49

                                                              0.46




                                                                                                                                                                                                                    0.42
                                                                                         0.42




                                                                                                                                                                                                                  0.39
                                                                                                                                                                                                                  0.38
                                                                                      0.36




                                                                                                                                                                                         0.35
                              0.4                                                                                                                                         0.4




                                                                                                             0.35
                                        0.33




                                                                                                                                                                                       0.32




                                                                                                                                                                                                                                          0.27
                                                                                                                                                                                                                                         0.26



                                                                                                                                                                                                                                                                 0.23
                              0.2                                                                                                                                         0.2

                              0.0                                                                                                                                         0.0
                                               pt              nce
                                                                   d                   e     d                e     d                4SA               4PF
                                                                                                                                                          A                                   pt                     ed                      e  d                   ed                   4SA               4PF
                                                                                                                                                                                                                                                                                                              A
                                        rom                 nha                    anc                    anc                     LLM               LLM                             rom                        anc                       anc                  anc                     LLM               LLM
                               asic
                                    P
                                                        ot E                ot E
                                                                                 nh                 e En
                                                                                                         h                                                                      ic P                        Enh                    Enh                     Enh
                              B                        C                -sh                      Typ                                                                      Bas                         Cot                 -sho
                                                                                                                                                                                                                              t                      pe
                                                                  Few                    Bug                                                                                                                        Few                     Bu   g Ty

                                                              (a) Accuracy Result using GPT-4o                                                                                                               (b) FPR_Recall Result using GPT-4o

                                        Type                                                                                                                                           Type




                                                                                                                                                                                                                                                                                                            1.00
                                                                                                                                                                                                                                                                                          0.99




                                                                                                                                                                                                                                                                                                            0.99
                                                                                                                                                           0.98
                                                                                                                                         0.98




                                                                                                                                                                                                                                                                                         0.96
                                               NPD                                                                                                                                            NPD




                                                                                                                                                          0.96




                                                                                                                                                                                                                                                                                                          0.95
                              1.0                                                                                                                                         1.0




                                                                                                                                                                                                                                                                                       0.93
                                                                                                                                      0.92
                                               OOB                                                                                                                                            OOB




                                                                                                                                                                                                                                                   0.87
                                                                                                                                                      0.86
                                                                                                                                   0.84




                                                                                                                                                                                                                                                                          0.83
                                                                                                                           0.82

                                               DBZ                                                                                                                                            DBZ




                                                                                                                                                                                                                                                                        0.79
                                                                                             0.79




                                                                                                                                                                                                                                                0.78
                                                                                             0.78




                              0.8                                                                                                                                         0.8
                                                                                                                    0.68




                                                                                                                                                                                                     0.67
                                                      0.66
                   Accuracy




                                                                                      0.56
                                                                         0.56




                                                                                                                                                                  FPR_R
                              0.6                                                                                                                                         0.6




                                                                                                                                                                                                                                         0.52
                                                                                                                                                                                                                            0.51
                                         0.50




                                                                                                                                                                                       0.48
                                        0.47




                                                                 0.46




                                                                                                             0.41
                                                              0.40




                              0.4                                                                                                                                         0.4




                                                                                                                                                                                              0.34



                                                                                                                                                                                                                     0.31




                                                                                                                                                                                                                                                                 0.30
                                                                                                                                                                                                                  0.23
                              0.2                                                                                                                                         0.2

                              0.0                                                                                                                                         0.0
                                          mp
                                                t
                                                               nce
                                                                   d                   e     d                e     d                4SA               4PF
                                                                                                                                                          A                                   pt                     ed                    ced                      ed                   4SA               4PF
                                                                                                                                                                                                                                                                                                              A
                                       Pro                  nha                    anc                    anc                     LLM               LLM                             rom                        anc                  han                       anc                     LLM               LLM
                                  ic                    ot E                ot E
                                                                                 nh                 e En
                                                                                                         h                                                                      ic P                        Enh               En                           Enh
                              Bas                      C                   h                      p                                                                       Bas                         Cot                 hot                        pe
                                                                  Fe   w-s               Bu  g Ty                                                                                                                   Few-s                   Bu   g Ty

                                                           (c) Accuracy Result using Qwen-3-Coder                                                                                                    (d) FPR_Recall Result using Qwen-3-Coder


                                                                                Figure 3: Comparison of performance for LLM-based methods

   (i) Limited capacity for long-context reasoning. We observed that                                                                                                            code contexts, (2) difficulty reasoning complex cascaded con-
LLMs are significantly less effective at mitigating false positives in                                                                                                          straints, and (3) insufficient semantic understanding. These
cases involving long code contexts. For cases where all methods                                                                                                                 challenges remain critical directions for advancing the practi-
failed, the average length of the function containing the warning                                                                                                               cal effectiveness of LLMs in future work.
was 95.6 lines longer than the overall dataset average, and 67.7 lines
longer than cases only correctly classified by LLM4PFA but missed
by other LLM-based methods. This demonstrates that LLMs struggle
                                                                                                                                                                           5 DISCUSSIONS
with extended context reasoning. Although LLM4PFA partially                                                                                                                5.1 Implications for Practitioners
alleviates this issue, the limitation persists.                                                                                                                            5.1.1 How LLMs Help in Practice. Our results from RQ2-RQ4 demon-
   (ii) Difficulty with complex cascaded constraints. When analyz-                                                                                                         strate that several mature LLM-based approaches (i.e., LLM4SA
ing code containing numerous loops, deeply nested conditional                                                                                                              and LLM4PFA) can effectively assist code reviewers in reducing
branches, or intricate logical expressions, LLMs often overlook                                                                                                            static false positives in real-world enterprise settings. Compared
boundary conditions or introduce logical inconsistencies. As a re-                                                                                                         with manually crafted rules, which suffer from poor scalability
sult, they fail to accurately track variable states across multiple                                                                                                        and limited coverage, and traditional deep learning approaches,
reasoning steps. For the cases misclassified by all methods, the                                                                                                           which struggle to generalize to proprietary data and often lack in-
average number of conditional statements was 21 higher than the                                                                                                            terpretability, LLM-based methods offer a more balanced trade-off
overall dataset average, and 18.9 higher than the subset solvable by                                                                                                       between effectiveness, interpretability, and efficiency.
LLM4PFA alone. This gap highlights the intrinsic weakness of LLMs                                                                                                          Effectiveness. The best-performing LLM-based method LLM4PFA
in handling multi-step, complex cascaded constraints reasoning.                                                                                                            achieved an accuracy of 0.93–0.94 across different state-of-the-art
   (iii) Insufficient semantic understanding. LLMs also struggle with                                                                                                      backbone models on our dataset, demonstrating strong potential
less common syntactic constructs, pointer manipulations, and user-                                                                                                         for false positive reduction. However, recall remains below the
defined, deeply nested data structures. Their training often lacks                                                                                                         enterprise-expected threshold of 90%, indicating that some degree
sufficient exposure to such patterns, leading to misinterpretation                                                                                                         of manual review is still necessary to guarantee absolute safety.
and erroneous reasoning when analyzing these cases.                                                                                                                        Nevertheless, LLM-based methods can feasibly replace at least one
                                                                                                                                                                           round of manual review in multi-stage validation workflows, re-
 Answer to RQ4 (Case Analysis): Although LLMs demon-
                                                                                                                                                                           ducing overall human effort significantly.
 strate promise in reducing false positives, they still face fun-
                                                                                                                                                                              Despite their promise, current LLM-based approaches face sev-
 damental limitations in enterprise-scale bug detection. Specifi-
                                                                                                                                                                           eral limitations: (1) Long-context reasoning. LLMs still struggle to
 cally, LLMs exhibit (1) limited effectiveness in handling long
                                                                                                                                                                           analyze warnings requiring deep or cross-module context [2, 34].
                                                                                                                                                                           The strong performance observed in our dataset partly reflects the
Conference’17, July 2017, Washington, DC, USA                   Xueying Du1 , Jiayi Feng1 , Yi Zou1 , Wei Xu2 , Jie Ma2 , Wei Zhang2 , Sisi Liu2 , Xin Peng1 , Yiling Lou1


limited context sensitivity of the static analyzers used, where most            Combining LLMs with Static Analysis. LLMs and static anal-
warnings involve only short code fragments. For cases requiring                 ysis complement each other effectively. Specifically, LLMs excel
deeper interprocedural reasoning, effectiveness degrades. (2) Com-              at understanding code snippets and generalizing across patterns,
plex constraint analysis. LLMs have difficulty accurately simulating            so they can enrich static analysis by providing scalable domain
program behavior in cases involving cascading constraints [15].                 knowledge and expanding the coverage of analysis rules. However,
While LLM4PFA alleviates this to some extent, the challenge has                 LLMs face limitations such as hallucinations and difficulties with
not been fully resolved. (3) Bug type coverage. Both prior work                 long-context reasoning tasks. Static analysis can mitigate these
and this study focus mainly on memory safety bugs, which ex-                    issues by providing reliable program facts and intermediate results,
hibit clearer patterns. The performance of LLMs on less common                  which help reduce hallucinations and assist LLMs in breaking down
bug types remains an open question. (4) Randomness in reasoning.                complex reasoning tasks. The competitive results of LLM4PFA fur-
LLM outputs exhibit randomness. For more stable results, majority               ther demonstrate the value of deeply integrating LLMs with static
voting across multiple runs (e.g., three per case in our evaluation)            analysis. Thus, combining LLMs with static analysis holds great
is recommended. Moreover, while LLMs show strong potential in                   promise as a future direction for static bug detection.
filtering false positives, their capacity to discover new bugs remains
bounded by the detection capabilities of static analyzers themselves.
How to leverage LLMs to help enterprises identify new bugs beyond               6     THREATS TO VALIDITY
the coverage of static analyzers remains an open challenge.                     Construct Validity. A potential threat arises from the reliabil-
Interpretability. Unlike most traditional deep learning models                  ity of manual labeling. To mitigate this, all labels were reviewed
that output only binary labels, LLM-based methods provide natural               through multiple rounds by experienced in-house developers and
language explanations alongside predictions. These explanations                 professional code reviewers, providing strong domain expertise
significantly support human reviewers, reducing the average time                and consistency. Our research team performed further validation,
to validate a warning from about 10 minutes to approximately 3                  and did not identify any correctness issues in the reviewed labels.
minutes. Even when explanations contain inaccuracies, they still                Internal Validity. Due to the randomness of LLMs, there is an
aid in quicker issue identification.                                            inherent risk to the reliability and consistency of experimental
Efficiency. As shown in RQ3, all evaluated LLMs perform static                  results. To mitigate this, we conducted multiple trials for each LLM-
false positive reduction at much lower time and acceptable eco-                 based method and reported the majority outcomes across repeated
nomic costs compared to manual review. Given that model per-                    runs. Moreover, the results of all methods with different LLMs are
formance is broadly comparable across LLMs, model selection in                  included in our replication package [43] to ensure transparency and
practice may emphasize efficiency. As such, the open-source Qwen-               reproducibility. Another threat is the limited dataset scope. Due to
3-Coder achieves a particularly favorable balance between time                  enterprise constraints, we collected all available data and applied
and economic cost, while also avoiding the practical challenges of              rigorous filtering to ensure quality. The final dataset includes 433
deploying closed-source models in enterprise environments.                      real cases spanning 10 months, which we believe remains valuable
                                                                                for identifying common false-positive patterns and evaluating the
                                                                                effectiveness of LLMs in false positive reduction.
                                                                                External Validity. Our data is collected from Tencent and primar-
5.2     Implications for Researchers                                            ily consists of C/C++ programs, which may limit generalizability
From a research perspective, our findings highlight several direc-              to other enterprise environments or languages. Nevertheless, the
tions for improving the use of LLMs in static bug detection.                    industrial scale of the dataset still provides meaningful insights for
Knowledge-enhanced LLMs. RQ2 shows that incorporating do-                       future work. Since the evaluated methods are language-agnostic,
main knowledge significantly improves LLMs reasoning accuracy.                  they can be extended to other programming languages. In future
Both bug-type descriptions and illustrative examples proved bene-               work, we plan to expand the dataset to include additional business
ficial, with examples yielding greater gains by explicitly exposing             lines and programming languages to further enhance the generaliz-
recurring bug patterns. In this study, such examples were manually              ability of our results.
constructed to guide LLM reasoning. Future research could explore
automated approaches for acquiring targeted knowledge (e.g., RAG
for high-quality historical cases), as well as investigating diverse            7     CONCLUSION
knowledge sources and modalities for enriching LLMs. These direc-               This work conducts the first comprehensive empirical study of
tions may enhance not only effectiveness but also interpretability.             diverse LLM-based false alarm reduction techniques in an indus-
Complex contextual and cascaded constraints analysis. Cur-                      trial context at Tencent, one of the largest IT companies in China.
rently, LLMs demonstrate strong capabilities in analyzing simple                Through interviewing developers and analyzing the data, our re-
code snippets but struggle with scenarios requiring complex con-                sults highlight the prevalence and bad impact of false positives.
text and cascaded constraints reasoning, which are prevalent in                 Meanwhile, our results show the huge potential of LLMs for re-
real-world software development. Promising approaches to enhanc-                ducing false alarms in industrial settings (with best techniques
ing LLMs in this direction include decomposing intricate reasoning              eliminating 94–98% of false positives). Furthermore, LLM-based
tasks into smaller, more manageable subproblems where LLMs                      techniques are cost-effectiveness, with low time and money costs.
perform more reliably, or designing hybrid pipelines to support                 Based on findings, we further discuss the practical implications for
complex contextual analysis.                                                    practitioners and outline promising directions for future research.
Reducing False Positives in Static Bug Detection with LLMs:
An Empirical Study in Industry                                                                                                    Conference’17, July 2017, Washington, DC, USA


REFERENCES                                                                                  [27] Anant Kharkar, Roshanak Zilouchian Moghaddam, Matthew Jin, Xiaoyu Liu, Xin
 [1] Amit Seal Ami, Kevin Moran, Denys Poshyvanyk, and Adwait Nadkarni. 2024.                    Shi, Colin Clement, and Neel Sundaresan. 2022. Learning to reduce false positives
     “False negative - that one is going to kill you”: Understanding Industry Perspec-           in analytic bug detectors. In Proceedings of the 44th International Conference
     tives of Static Analysis based Security Testing. In 2024 IEEE Symposium on Security         on Software Engineering (Pittsburgh, Pennsylvania) (ICSE ’22). Association for
     and Privacy (SP). IEEE, 3979–3997. https://doi.org/10.1109/sp54263.2024.00019               Computing Machinery, New York, NY, USA, 1307–1316. https://doi.org/10.1145/
 [2] Shengnan An, Zexiong Ma, Zeqi Lin, Nanning Zheng, Jian-Guang Lou, and                       3510003.3510153
     Weizhu Chen. 2024. Make your llm fully utilize the context. Advances in Neural         [28] Seongmin Lee, Shin Hong, Jungbae Yi, Taeksu Kim, Chul-Joo Kim, and Shin Yoo.
     Information Processing Systems 37 (2024), 62160–62188.                                      2019. Classifying false positive static checker alarms in continuous integration
 [3] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan,                      using convolutional neural networks. In 2019 12th IEEE Conference on Software
     Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda                  Testing, Validation and Verification (ICST). IEEE, 391–401.
     Askell, et al. 2020. Language models are few-shot learners. Advances in neural         [29] Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian. 2023. The Hitchhiker’s
     information processing systems 33 (2020), 1877–1901.                                        Guide to Program Analysis: A Journey with Large Language Models. (2023).
 [4] Yuandao Cai, Peisen Yao, Chengfeng Ye, and Charles Zhang. 2023. Place your                  arXiv:2308.00245 [cs.SE]
     locks well: understanding and detecting lock misuse bugs. In 32nd USENIX Secu-         [30] Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian. 2024. Enhancing Static
     rity Symposium (USENIX Security 23). 3727–3744.                                             Analysis for Practical Bug Detection: An LLM-Integrated Approach. Proc. ACM
 [5] Yuandao Cai, Peisen Yao, and Charles Zhang. 2021. Canary: practical static de-              Program. Lang. 8, OOPSLA1, Article 111 (apr 2024), 26 pages. https://doi.org/10.
     tection of inter-thread value-flow bugs. In Proceedings of the 42nd ACM SIGPLAN             1145/3649828
     International Conference on Programming Language Design and Implementation.            [31] Hongzhe Li, Taebeom Kim, Munkhbayar Bat-Erdene, and Heejo Lee. 2013. Soft-
     1126–1140.                                                                                  ware vulnerability detection using backward trace analysis and symbolic exe-
 [6] Yuandao Cai, Chengfeng Ye, Qingkai Shi, and Charles Zhang. 2022. Peahen: Fast               cution. In 2013 International Conference on Availability, Reliability and Security.
     and precise static deadlock detection via context reduction. In Proceedings of the          IEEE, 446–454.
     30th ACM Joint European Software Engineering Conference and Symposium on the           [32] Haonan Li, Hang Zhang, Kexin Pei, and Zhiyun Qian. 2025. Towards More
     Foundations of Software Engineering. 784–796.                                               Accurate Static Analysis for Taint-Style Bug Detection in Linux Kernel. In 40th
 [7] Partha Chakraborty, Krishna Kanth Arumugam, Mahmoud Alfadel, Meiyap-                        IEEE/ACM International Conference on Automated Software Engineering, ASE 2025.
     pan Nagappan, and Shane McIntosh. 2024. Revisiting the performance of deep             [33] Kaixuan Li, Sen Chen, Lingling Fan, Ruitao Feng, Han Liu, Chengwei Liu, Yang
     learning-based vulnerability detection on realistic datasets. IEEE Transactions on          Liu, and Yixiang Chen. 2023. Comparison and evaluation on static application
     Software Engineering 50, 8 (2024), 2163–2177.                                               security testing (sast) tools for java. In Proceedings of the 31st ACM Joint European
 [8] claude 2024. Claude 3.5 Sonnet. https://www.anthropic.com/news/claude-3-                    Software Engineering Conference and Symposium on the Foundations of Software
     family.                                                                                     Engineering. 921–933.
 [9] cloud 2025. Tencent Cloud. https://cloud.tencent.com.                                  [34] Tianle Li, Ge Zhang, Quy Duc Do, Xiang Yue, and Wenhu Chen. 2024.
[10] codeql 2025. CodeQL. https://codeql.github.com/.                                            Long-context llms struggle with long in-context learning. arXiv preprint
[11] coverity 2025. Coverity. https://scan.coverity.com.                                         arXiv:2404.02060 (2024).
[12] cppcheck 2025. Cppcheck. http://cppcheck.net/.                                         [35] Yuan Li, Peisen Yao, Kan Yu, Chengpeng Wang, Yaoyang Ye, Song Li, Meng
[13] deepseek 2024. DeepSeek-Coder-V2-Instruct. https://huggingface.co/deepseek-                 Luo, Yepang Liu, and Kui Ren. 2025. Understanding Industry Perspectives of
     ai/DeepSeek-Coder-V2-Instruct.                                                              Static Application Security Testing (SAST) Evaluation. Proceedings of the ACM
[14] Yangruibo Ding, Yanjun Fu, Omniyyah Ibrahim, Chawin Sitawarin, Xinyun                       on Software Engineering 2, FSE (2025), 3033–3056.
     Chen, Basel Alomair, David Wagner, Baishakhi Ray, and Yizheng Chen. 2024.              [36] Ziyang Li, Saikat Dutta, and Mayur Naik. 2024. LLM-Assisted Static Analysis for
     Vulnerability detection with code language models: How far are we? arXiv                    Detecting Security Vulnerabilities. arXiv:2405.17238 [cs.CR] https://arxiv.org/
     preprint arXiv:2403.18624 (2024).                                                           abs/2405.17238
[15] Xueying Du, Kai Yu, Chong Wang, Yi Zou, Wentai Deng, Zuoyu Ou, Xin Peng,               [37] Ziyang Li, Saikat Dutta, and Mayur Naik. 2025. IRIS: LLM-Assisted Static Analysis
     and Yiling Lou. 2025. Minimizing False Positives in Static Bug Detection via                for Detecting Security Vulnerabilities. arXiv:2405.17238 [cs.CR] https://arxiv.
     LLM-Enhanced Path Feasibility Analysis. arXiv preprint arXiv:2506.10322 (2025).             org/abs/2405.17238
[16] Xueying Du, Geng Zheng, Kaixin Wang, Jiayi Feng, Wentai Deng, Mingwei Liu,             [38] Stephan Lipp, Sebastian Banescu, and Alexander Pretschner. 2022. An empirical
     Bihuan Chen, Xin Peng, Tao Ma, and Yiling Lou. 2024. Vul-RAG: Enhancing                     study on the effectiveness of static C code analyzers for vulnerability detection.
     LLM-based Vulnerability Detection via Knowledge-level RAG. arXiv preprint                   In Proceedings of the 31st ACM SIGSOFT international symposium on software
     arXiv:2406.11147 (2024).                                                                    testing and analysis. 544–555.
[17] Michael Fu and Chakkrit Tantithamthavorn. 2022. LineVul: A Transformer-based           [39] Zhihong Liu, Zezhou Yang, and Qing Liao. 2024. Exploration on prompting
     Line-Level Vulnerability Prediction. In 19th IEEE/ACM International Conference              LLM with code-specific information for vulnerability detection. In 2024 IEEE
     on Mining Software Repositories, MSR 2022, Pittsburgh, PA, USA, May 23-24, 2022.            International Conference on Software Services Engineering (SSE). IEEE, 273–281.
     ACM, 608–620. https://doi.org/10.1145/3524842.3528452                                  [40] Qiheng Mao, Zhenhao Li, Xing Hu, Kui Liu, Xin Xia, and Jianling Sun. 2024. To-
[18] Mikhail R Gadelha, Enrico Steffinlongo, Lucas C Cordeiro, Bernd Fischer, and                wards Effectively Detecting and Explaining Vulnerabilities Using Large Language
     Denis Nicole. 2019. Smt-based refutation of spurious bug reports in the clang static        Models. arXiv:2406.09701 [cs.SE] https://arxiv.org/abs/2406.09701
     analyzer. In 2019 IEEE/ACM 41st International Conference on Software Engineering:      [41] Van-Anh Nguyen, Dai Quoc Nguyen, Van Nguyen, Trung Le, Quan Hung Tran,
     Companion Proceedings (ICSE-Companion). IEEE, 11–14.                                        and Dinh Phung. 2022. Regvd: Revisiting graph neural networks for vulnerabil-
[19] Zeyu Gao, Hao Wang, Yuchen Zhou, Wenyu Zhu, and Chao Zhang. 2023. How                       ity detection. In Proceedings of the ACM/IEEE 44th International Conference on
     Far Have We Gone in Vulnerability Detection Using Large Language Mod-                       Software Engineering: Companion Proceedings. 178–182.
     els. CoRR abs/2311.12420 (2023). https://doi.org/10.48550/ARXIV.2311.12420             [42] Chao Ni, Xin Yin, Liyu Shen, and Shaohua Wang. 2026. Learning-based models
     arXiv:2311.12420                                                                            for vulnerability detection: An extensive study. Empirical Software Engineering
[20] gawk 2025. Gawk. https://github.com/gvlx/gawk.                                              31, 1 (2026), 18.
[21] gpt4o 2024. GPT-4 Turbo. https://platform.openai.com/docs/models/gpt-4-and-            [43] package 2025. Replication Package. https://github.com/LLM4SFPR/static-bug-
     gpt-4-turbo.                                                                                false-positives-reduction-in-practice.
[22] Jinyao Guo, Chengpeng Wang, Xiangzhe Xu, Zian Su, and Xiangyu Zhang. 2025.             [44] Hendrik Post, Carsten Sinz, Alexander Kaiser, and Thomas Gorges. 2008. Re-
     RepoAudit: An Autonomous LLM-Agent for Repository-Level Code Auditing. In                   ducing false positives by combining abstract interpretation and bounded model
     Forty-second International Conference on Machine Learning, ICML 2025, Vancouver,            checking. In 2008 23rd IEEE/ACM International Conference on Automated Software
     BC, Canada, July 13-19, 2025. OpenReview.net. https://openreview.net/forum?                 Engineering. IEEE, 188–197.
     id=TXcifVbFpG                                                                          [45] qwen 2024. Qwen2.5-Coder-32B-Instruct. https://huggingface.co/Qwen/Qwen2.
[23] Zhaoqiang Guo, Tingting Tan, Shiran Liu, Xutong Liu, Wei Lai, Yibiao Yang,                  5-Coder-32B-Instruct.
     Yanhui Li, Lin Chen, Wei Dong, and Yuming Zhou. 2023. Mitigating false pos-            [46] Ze Sheng, Zhicheng Chen, Shuning Gu, Heqing Huang, Guofei Gu, and Jeff
     itive static analysis warnings: Progress, challenges, and opportunities. IEEE               Huang. 2025. Llms in software security: A survey of vulnerability detection
     Transactions on Software Engineering 49, 12 (2023), 5154–5188.                              techniques and insights. Comput. Surveys 58, 5 (2025), 1–35.
[24] infer 2025. Infer. https://fbinfer.com/.                                               [47] Alexey Shestov, Anton Cheshkov, Rodion Levichev, Ravil Mussabayev, Pavel
[25] juliet 2025. Juliet Test Suite for C/C++. https://samate.nist.gov/SARD/test-                Zadorozhny, Evgeny Maslov, Chibirev Vadim, and Egor Bulychev. 2024. Finetun-
     suites/112.                                                                                 ing Large Language Models for Vulnerability Detection. CoRR abs/2401.17010
[26] Avishree Khare, Saikat Dutta, Ziyang Li, Alaia Solko-Breslin, Rajeev Alur, and              (2024). https://doi.org/10.48550/ARXIV.2401.17010 arXiv:2401.17010
     Mayur Naik. 2023. Understanding the Effectiveness of Large Language Models             [48] Qingkai Shi, Rongxin Wu, Gang Fan, and Charles Zhang. 2020. Conquering the
     in Detecting Security Vulnerabilities. CoRR abs/2311.16169 (2023). https://doi.             extensional scalability problem for value-flow analysis frameworks. In Proceedings
     org/10.48550/ARXIV.2311.16169 arXiv:2311.16169                                              of the ACM/IEEE 42nd International Conference on Software Engineering. 812–823.
Conference’17, July 2017, Washington, DC, USA                                   Xueying Du1 , Jiayi Feng1 , Yi Zou1 , Wei Xu2 , Jie Ma2 , Wei Zhang2 , Sisi Liu2 , Xin Peng1 , Yiling Lou1


[49] Qingkai Shi, Xiao Xiao, Rongxin Wu, Jinguo Zhou, Gang Fan, and Charles Zhang.                    Hugo Larochelle, Alina Beygelzimer, Florence d’Alché-Buc, Emily B. Fox, and
     2018. Pinpoint: Fast and precise sparse value flow analysis for million lines                    Roman Garnett (Eds.). 10197–10207. https://proceedings.neurips.cc/paper/2019/
     of code. In Proceedings of the 39th ACM SIGPLAN Conference on Programming                        hash/49265d2447bc3bbfe9e76306ce40a31f-Abstract.html
     Language Design and Implementation. 693–706.
[50] Benjamin Jeremiah Steenhoek. 2024. Understanding and improving deep learning
     models for vulnerability detection. Ph. D. Dissertation. Iowa State University.
[51] Yulei Sui, Ding Ye, and Jingling Xue. 2012. Static memory leak detection using
     full-sparse value-flow analysis. In Proceedings of the 2012 International Symposium
     on Software Testing and Analysis. 254–264.
[52] Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Haijun Wang, Zhengzi Xu,
     Xiaofei Xie, and Yang Liu. 2023. When GPT Meets Program Analysis: To-
     wards Intelligent Detection of Smart Contract Logic Vulnerabilities in GPTScan.
     arXiv:2308.03314 [cs.CR]
[53] tencent 2025. Tencent. https://www.tencent.com.
[54] Manuel Valdiviezo, Cristina Cifuentes, and Padmanabhan Krishnan. 2014. A
     method for scalable and precise bug finding using program analysis and model
     checking. In Asian Symposium on Programming Languages and Systems. Springer,
     196–215.
[55] Carmine Vassallo, Sebastiano Panichella, Fabio Palomba, Sebastian Proksch, Har-
     ald C Gall, and Andy Zaidman. 2020. How developers engage with static analysis
     tools in different contexts. Empirical Software Engineering 25 (2020), 1419–1457.
[56] Chong Wang, Jianan Liu, Xin Peng, Yang Liu, and Yiling Lou. 2023. Boosting Static
     Resource Leak Detection via LLM-based Resource-Oriented Intention Inference.
     arXiv preprint arXiv:2311.04448 (2023).
[57] Chengpeng Wang, Wuqi Zhang, Zian Su, Xiangzhe Xu, Xiaoheng Xie, and Xi-
     angyu Zhang. 2024. LLMDFA: Analyzing Dataflow in Code with Large Language
     Models. In The Thirty-eighth Annual Conference on Neural Information Processing
     Systems.
[58] wechat 2025. WeChat. https://weixin.qq.com.
[59] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi,
     Quoc V Le, Denny Zhou, et al. 2022. Chain-of-thought prompting elicits reasoning
     in large language models. Advances in Neural Information Processing Systems 35
     (2022), 24824–24837.
[60] Cheng Wen, Yuandao Cai, Bin Zhang, Jie Su, Zhiwu Xu, Dugang Liu, Shengchao
     Qin, Zhong Ming, and Tian Cong. 2024. Automatically inspecting thousands
     of static bug warnings with large language model: How far are we? ACM
     Transactions on Knowledge Discovery from Data 18, 7 (2024), 1–34.
[61] Cheng Wen, Yuandao Cai, Bin Zhang, Jie Su, Zhiwu Xu, Dugang Liu, Shengchao
     Qin, Zhong Ming, and Tian Cong. 2024. Automatically Inspecting Thousands of
     Static Bug Warnings with Large Language Model: How Far Are We? ACM Trans.
     Knowl. Discov. Data 18, 7, Article 168 (jun 2024), 34 pages. https://doi.org/10.
     1145/3653718
[62] Fangzhou Wu, Qingzhao Zhang, Ati Priya Bajaj, Tiffany Bao, Ning Zhang, Ruoyu
     Wang, and Chaowei Xiao. 2023. Exploring the Limits of ChatGPT in Software
     Security Applications. CoRR abs/2312.05275 (2023). https://doi.org/10.48550/
     ARXIV.2312.05275 arXiv:2312.05275
[63] Hua Yan, Yulei Sui, Shiping Chen, and Jingling Xue. 2018. Spatio-temporal context
     reduction: A pointer-analysis-based static approach for detecting use-after-free
     vulnerabilities. In Proceedings of the 40th International Conference on Software
     Engineering. 327–337.
[64] Aidan Z. H. Yang, Claire Le Goues, Ruben Martins, and Vincent J. Hellendoorn.
     2024. Large Language Models for Test-Free Fault Localization. In Proceedings of
     the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024,
     Lisbon, Portugal, April 14-20, 2024. ACM, 17:1–17:12. https://doi.org/10.1145/
     3597503.3623342
[65] Alperen Yildiz, Sin G. Teo, Yiling Lou, Yebo Feng, Chong Wang, and Dinil Mon
     Divakaran. 2025. Benchmarking LLMs and LLM-based Agents in Practical
     Vulnerability Detection for Code Repositories. CoRR abs/2503.03586 (2025).
     https://doi.org/10.48550/ARXIV.2503.03586 arXiv:2503.03586
[66] Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex Smola. 2022. Automatic chain
     of thought prompting in large language models. arXiv preprint arXiv:2210.03493
     (2022).
[67] Xin Zhou, Sicong Cao, Xiaobing Sun, and David Lo. 2025. Large language model
     for vulnerability detection and repair: Literature review and the road ahead. ACM
     Transactions on Software Engineering and Methodology 34, 5 (2025), 1–31.
[68] Xin Zhou, Ting Zhang, and David Lo. 2024. Large Language Model for Vul-
     nerability Detection: Emerging Results and Future Directions (ICSE-NIER’24).
     Association for Computing Machinery, New York, NY, USA, 47–51. https:
     //doi.org/10.1145/3639476.3639762
[69] Xin Zhou, Ting Zhang, and David Lo. 2024. Large language model for vulner-
     ability detection: Emerging results and future directions. In Proceedings of the
     2024 ACM/IEEE 44th International Conference on Software Engineering: New Ideas
     and Emerging Results. 47–51.
[70] Yaqin Zhou, Shangqing Liu, Jing Kai Siow, Xiaoning Du, and Yang Liu. 2019. De-
     vign: Effective Vulnerability Identification by Learning Comprehensive Program
     Semantics via Graph Neural Networks. In Advances in Neural Information Process-
     ing Systems 32: Annual Conference on Neural Information Processing Systems 2019,
     NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada, Hanna M. Wallach,
