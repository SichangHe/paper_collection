                                         When Passing Tests Hides Vulnerabilities: An Empirical Study of
                                         Silent Failures in Agentic Systems⋆
                                         Wenji Baia,∗ , Muhammad Waseema , Zeeshan Rasheeda , Jaakko Peltonena and Pekka Abrahamssona
                                         a Faculty of Information Technology and Communication Sciences, Tampere University, Tampere, Finland



                                         ARTICLE INFO                                       ABSTRACT
                                         Keywords:                                          LLM-based agents for automated code repair have received significant attention in recent years from
                                         Agentic AI                                         both research and software engineering practice perspectives. However, limited attention has been
                                         Silent failures                                    paid to patches that pass syntactic and functional verification but still retain or introduce security
                                         LLM-based agents                                   vulnerabilities. The aim of this research is to systematically identify and categorize such silent failures
                                         Software security                                  in LLM-based agentic code repair.
                                         Empirical study                                        We conducted an empirical study using 1,030 valid execution traces produced by seven agent
arXiv:2609.10548v1 [cs.SE] 25 Jun 2026




                                         Multi-Agent systems                                frameworks with GPT-4o-mini across two security-focused datasets, SecurityEval and CVEfixes.
                                                                                            Through three iterations of qualitative coding and manual verification, 170 confirmed silent failures
                                                                                            were identified. The key results are: (i) Three main categories of silent failures were identified:
                                                                                            Omission, Introduction, and Inadequacy. Omission accounts for 48.2% of the confirmed failures,
                                                                                            Introduction for 30.6%, and Inadequacy for 21.2%. (ii) Ten fine-grained failure codes were classified
                                                                                            under these three categories, showing how agents omit required security controls, apply incomplete
                                                                                            defenses, or introduce new vulnerabilities during repair. (iii) Current test-passing evaluation and LLM-
                                                                                            based reviewer roles were insufficient to expose or intercept these failures in the confirmed cases. (iv)
                                                                                            Similar insecure solutions appeared across different frameworks, suggesting possible shared model-,
                                                                                            prompt-, or task-level influences, while single-agent and multi-agent systems showed different failure
                                                                                            profiles.
                                                                                                The results of this study will assist researchers and practitioners in improving the evaluation
                                                                                            of LLM-based agentic code repair and developing targeted verification methods that go beyond
                                                                                            functional correctness and cover all generated artifacts.



                                         1. Introduction                                                               code completion assistants [4–6]. Furthermore, multi-agent
                                                                                                                       frameworks organize multiple LLMs into role-specialized
                                             Silent failures in automated software repair refer to
                                                                                                                       pipelines that mirror human development teams [7–9].
                                         patches that pass functional validation but still contain                     These architectures use role specialization and interaction
                                         flaws, in particular security vulnerabilities. In automated                   to improve output quality. However, recent studies report
                                         program repair, a patch that compiles and passes all available                that multi-agent systems do not consistently outperform
                                         test cases is conventionally termed plausible, but plausible                  single-agent approaches, and their failure modes are not
                                         patches are not necessarily correct [1]. We extend this con-
                                                                                                                       well characterized [10, 11]. These systems are increasingly
                                         cept into the security domain, and to systematically make the
                                                                                                                       deployed for security-sensitive tasks, including vulnerability
                                         distinction explicit, we adopt a four-level verification hierar-              patching and authentication repair [12], which increases the
                                         chy: syntactic validity (L0), functional validation (L1), static              risk of undetected vulnerabilities.
                                         security analysis (L2), and exploitability assessment (L3).                       Current evaluation practices can reinforce this risk.
                                         Thus, a patch may compile without errors (L0) and pass unit
                                                                                                                       Benchmarks such as SWE-bench evaluate success primarily
                                         tests (L1), while still containing a vulnerability detectable
                                                                                                                       through test passing [13, 14]. In Continuous Integration and
                                         through static security analysis (L2) or exploitability testing               Continuous Delivery (CI/CD) pipelines, results are typically
                                         (L3) [2, 3]. Unlike overt errors such as compilation failures                 reported based solely on test passing criteria. When patches
                                         or test breakages, silent failures evade standard quality gates               pass, reviewers may reasonably assume that agents have
                                         and can remain undetected and reach production systems.                       produced functionally correct repairs. However, an agent-
                                             This issue has become increasingly relevant with the
                                                                                                                       generated patch can satisfy a narrowly scoped test case while
                                         rise of LLM-based agentic systems. Recent tools can handle
                                                                                                                       retaining an exploitable vulnerability. For instance, an agent
                                         multiple steps of the repair workflow, from fault diagno-                     might resolve a data processing error to pass a functional
                                         sis to patch implementation, marking a shift from earlier                     test, yet continue to process untrusted user input without
                                            ⋆
                                                                                                                       proper sanitization, a well-known vulnerability pattern [15,
                                             ∗ Corresponding author
                                                                                                                       16].
                                                   wenji.bai@tuni.fi (W. Bai); muhammad.waseem@tuni.fi (M.                 Prior work has explored related issues, but a system-
                                         Waseem); zeeshan.rasheed@tuni.fi (Z. Rasheed); jaakko.peltonen@tuni.fi
                                                                                                                       atic account of silent failures remains absent. Existing tax-
                                         (J. Peltonen); pekka.abrahamsson@tuni.fi (P. Abrahamsson)
                                               ORCID (s): 0000-0002-3283-3483 (W. Bai); 0000-0001-7488-2577 (M.        onomies categorize observable failure modes in multi-agent
                                         Waseem); 0000-0001-9655-3096 (Z. Rasheed); 0000-0003-3485-8585 (J.            systems, yet they rely on explicit easily noticeable signals
                                         Peltonen); 0000-0002-4360-2226 (P. Abrahamsson)                               like system crashes or task non-completion; failures that
                                             1
                                                                                                                       produce no such obvious signals fall outside their scope [11].

                                         : Preprint submitted to Elsevier                                                                                                             Page 1 of 22
Similarly, current attribution frameworks offer mechanisms         an empirically grounded taxonomy centered on security-
for identifying fault-inducing steps but still assume that fail-   compliance decoupling from mere unit-test passing. Specif-
ures are externally visible [17, 18]. In automated program re-     ically, this paper makes the following contributions:
pair, recent work has advocated for multi-dimensional evalu-
ation incorporating security benchmarks and static analysis,          • An empirically grounded taxonomy of silent fail-
yet these approaches have not been applied to characterize              ures. We propose an empirically grounded taxonomy
failures within multi-agent repair pipelines [19, 20].                  that classifies silent failures along four dimensions
     Motivated by this gap, we formulate the following three            (failure type, originator role, injection stage, and code
research questions:                                                     location), extending beyond existing failure classi-
                                                                        fications by explicitly modeling failures that evade
    • RQ1: What types of silent failures occur in LLM-based             standard detection mechanisms.
      agent code repair, and how prevalent are they?
                                                                      • A cross-framework empirical analysis. We analyze
      Rationale: Existing taxonomies classify observable
                                                                        1,030 execution traces from seven agent frameworks
      failure modes in multi-agent systems, but they pri-
                                                                        across two security-focused datasets, providing quan-
      marily address explicit indications such as crashes,
                                                                        titative evidence on the prevalence, distribution, and
      errors, or task non-completion. Silent failures, defined
                                                                        characteristics of silent failures.
      as patches that pass functional verification yet contain
      security deficiencies, remain insufficiently character-         • Failure propagation analysis across agent roles. By
      ized. This question develops an empirically grounded              tracing silent failures through multi-agent execution
      taxonomy of silent failure types and quantifies their             logs, we identify how security omissions introduced
      prevalence across frameworks and datasets, thereby                at one pipeline stage propagate through subsequent
      establishing the basis for the subsequent vulnerability-          stages, and compare propagation patterns between
      context analyses.                                                 multi-agent and single-agent systems.
    • RQ2: How do silent failures propagate through agent             • A public dataset. We publicly release the study
      pipelines, and what role do architectural differences             dataset online [21], including execution traces, gener-
      play?                                                             ated patches, verification results, and taxonomy codes,
      Rationale: Multi-agent frameworks employ special-                 to enable researchers and practitioners to access,
      ized roles such as planners, engineers, and reviewers,            replicate, and validate our findings.
      but it remains unclear whether these role structures
      intercept security deficiencies or allow them to propa-          The remainder of this paper is organized as follows.
      gate across pipeline stages. This question traces silent     Section 2 describes our research methodology. Section 3
      failures through agent roles and pipeline stages, exam-      presents the empirical results. Section 4 discusses implica-
      ines whether reviewer roles detect them, and compares        tions, and Section 5 addresses threats to validity. Section 6
      propagation patterns between multi-agent and single-         reviews related work. Section 7 concludes with directions for
      agent architectures. The goal is to clarify how archi-       future work.
      tectural structure shapes the emergence, propagation,
      and interception of silent failures.                         2. Research Methodology
    • RQ3: Which vulnerability types and code contexts are             This section describes the research methodology used
      most susceptible to silent failures, and what severity       to identify, verify, and analyze silent failures in LLM-based
      and exploitability levels do they exhibit?                   agentic code repair. We first present the overall research de-
                                                                   sign, followed by the dataset and agent framework selection
      Rationale: Vulnerability characteristics may shape
                                                                   criteria. We then describe the experimental setup, the multi-
      both the form silent failures take and their severity and
                                                                   level verification framework, the manual review process,
      exploitability, yet this relationship has received lim-
                                                                   and the qualitative coding and reliability procedures used to
      ited empirical attention. This question examines how
                                                                   construct and validate the taxonomy.
      silent failures distribute across CWE families, code
      locations, severity levels, and exploitability scores.
                                                                   2.1. Research Design Overview
      The goal is to identify cross-dimensional patterns that
                                                                        The study consists of two phases, as illustrated in Fig-
      can support targeted verification strategies rather than
                                                                   ure 1: (i) preparation of the shared experimental infrastruc-
      treating silent failures as a homogeneous defect class.
                                                                   ture, and (ii) iterative data collection and analysis. This de-
    To address these research questions, we conduct an em-         sign supports our three research questions on failure catego-
pirical study of silent failures across seven LLM-based agent      rization, propagation mechanisms, and vulnerability suscep-
frameworks and two security-focused datasets. Our analysis         tibility, while enabling consistent comparison across seven
encompasses 1,030 execution traces, from which we identify         agent frameworks. The first phase covers dataset selection,
170 confirmed silent failures. Through iterative qualitative       framework selection, model configuration, the multi-level
coding of execution traces and related artifacts, we develop       verification pipeline, and manual review criteria. The second

: Preprint submitted to Elsevier                                                                                    Page 2 of 22
                                                                    Phase 1. Preparation: Shared Experimental Infrastructure

         Dataset Selection                     Agent Framework Selection                   Model Configuration & Hardware                 Verification Pipeline                    Manual Review Criteria
                                                                                                                                             L0: Syntactic validity
                   • SecurityEval                            7 agent                              • Base model: GPT-4o-mini                                                                • True Positive (TP)
                   • CVEfixes                                frameworks                           • Temperature: 0.2                         L1: Functional validation                     • Partial
                                                                                                  • Timeout: 600s                            L2: Static security analysis
                                                                                                                                                                                           • False Positive (FP)
   · Security relevance · CW E annotations     · Code-repair relevance · O pen-source      · A 5 GB NVIDIA A100 GPU slice via M IG
   · Python-only tasks · public availability   · Released 2023–2026                        · 8 CPU cores · 17.5GB RAM · 512GB storage        L3: Exploitability assessm ent




                                                                              Phase 2. Iterative Data Collection and Analysis
   One iteration cycle
            A. Sample Tasks                       B. Execute 7 Frameworks                      C. Multi-level Verification                 D. Manual Review                           E. Qualitative Coding
      Sample a batch from the                    Run all frameworks on each                   Evaluate generated patches                Review flagged candidates                  Code confirmed cases
      task pool                                  task                                         across four levels                        and assign labels                          through iterative qualitative
                                                                                                                                                                                   coding
                                                                                                                     inform
      Configurations of the A–E cycle across three iterations
                                Iteration 1                                                           Iteration 2                                                            Iteration33
                                                                                                                                                                            Iteration
       Sam pling
       Focus
                   Proportional sampling from                                 Sam pling
                                                                              Focus
                                                                                            Targeted sampling based on                          Sam pling
                                                                                                                                                Focus
                                                                                                                                                              Sampling of underrepresented failure
                   SecurityEval                                                             Iteration 1 findings                                              patterns
       Coding                                                                  Coding                                                           Coding
       Focus       Open coding                                                 Focus        Axial coding                                        Focus         Selective coding

      Iteration
                   Initial set of codes and preliminary                        Iteration    Refined categories and                              Iteration
                                                                                                                                                              Core category integration
      O utput                                                                                                                                   O utput
                   patterns                                                    O utput      relationships


                                                                                                  Quantitative Analysis
                                                                   Descriptive and cross-dimensional analysis of confirmed cases

                                                                    Figure 1: Overview of the research methodology.



Table 1                                                                                                             tasks. Table 1 summarizes the selected datasets, which are
Summary of selected datasets. Pool denotes the eligible task                                                        described below.
count after language and format filtering; Sampled denotes the
number of tasks drawn across three iterations.                                                                            • SecurityEval [22] provides 130 predefined code gen-
                 SecurityEval            CVEfixes        Total                                                              eration prompts across 69 CWE categories. We re-
 Task Type Code generation Vulnerability repair              –                                                              tained the 121 Python tasks and excluded non-Python
 Original             130                  5,365        5,495                                                               entries. Each task presents an insecure code context
 Pool                 121                  1,115        1,236                                                               and requires the agent to generate a secure version,
 Sampled               85                    65            150                                                              serving as a benchmark for initial pattern discovery
 Labels              CWE                CVE/CWE              –                                                              and cross-framework comparison.
                                                                                                                          • CVEfixes [23] contains 5,365 real-world vulnerabil-
phase repeats the same procedure across three iterations:                                                                   ity fixes linking Common Vulnerabilities and Expo-
sampling tasks, executing all seven frameworks, evaluat-                                                                    sures (CVE) records to code changes in open-source
ing generated patches through L0–L3 verification, manually                                                                  projects. We filtered for Python single-file fixes with
reviewing flagged candidates, and qualitatively coding the                                                                  CWE annotations, yielding 1,115 tasks. CVEfixes
confirmed cases. Observations from each iteration informed                                                                  tasks involve patching known vulnerabilities in exist-
the sampling and analytical focus of the next.                                                                              ing production code and often require adding entirely
                                                                                                                            new security logic rather than merely substituting an
2.2. Dataset Selection                                                                                                      insecure API, representing real-world repair condi-
     To construct our dataset pool, we first defined four                                                                   tions.
selection criteria: (i) security relevance, (ii) the availabil-
ity of Common Weakness Enumeration (CWE) annotations                                                                2.3. Agent Framework Selection
to enable verification against expected vulnerability types,                                                             To select the agent frameworks for this study, we first
(iii) uniform execution conditions, requiring Python-only                                                           defined three criteria: (i) relevance to code repair, requiring
tasks so that all seven frameworks could be evaluated under                                                         that each framework be applicable to vulnerability repair
identical conditions, and (iv) public availability. Based on                                                        tasks either by design or through reasonable adaptation;
these criteria, we selected two security-focused datasets,                                                          (ii) open-source availability; and (iii) recency, requiring that
which together provided a combined pool of 1,236 Python                                                             each framework has been released between 2023 and 2026 to

: Preprint submitted to Elsevier                                                                                                                                                                    Page 3 of 22
Table 2
Selected agent frameworks and their coordination architectures.
   Framework                           Type     Architecture               Selection Rationale
   Multi-Agent Systems
   MetaGPT [8]                         Multi    Assembly Line              Sequential role handoffs enable stage-level failure
                                                                           tracing
   ChatDev [7]                         Multi    Hierarchical Workflow      Phase-based workflow with explicit role transitions;
                                                                           validates pattern generalization across pipeline ar-
                                                                           chitectures
   AutoGen [9]                         Multi    Dynamic Conversation       Flexible orchestration with runtime role assignment;
                                                                           captures emergent failure patterns in less structured
                                                                           collaboration
   AgentCoder [24]                     Multi    Test-driven Loop           Independent test designer and coder roles; tests
                                                                           whether agent-generated tests mask vulnerabilities
   Single-Agent Systems
   Mini SWE-Agent (MiniSWE) [4]        Single   ReAct Loop                 Lightweight single-agent baseline; isolates coordina-
                                                                           tion effects by removing inter-agent communication
   Aider [25]                          Single   Edit-feedback Loop         Structured diff output with lint/test feedback loops;
                                                                           represents developer-tool-style interaction
   OpenHands [26]                      Single   Edit-feedback Loop         CLI-based sandbox with file editing and shell execu-
                                                                           tion in a single generalist loop


reflect recent advances in the field. Based on these criteria,     paired the vulnerable code with a repair instruction specify-
we systematically selected seven agent frameworks repre-           ing the target CVE/CWE. Beyond these dataset-specific dif-
senting distinct coordination patterns. Table 2 provides an        ferences, no additional security prompts were injected unless
overview of the selected frameworks and their coordination         the task itself explicitly implied a security requirement.
architectures.
                                                                   2.4.2. Multi-Level Verification Framework
2.4. Experimental Setup                                                As outlined in Section 1, passing functional tests does
    This section outlines the model and prompt configura-          not guarantee security correctness [1, 27]. We therefore eval-
tion, hardware platform, four-level verification framework,        uate every generated patch through a four-level verification
and manual review and confirmation criteria used in our            pipeline:
study. In this setup, each task is independently processed
by all frameworks to produce generated patches under a                  • Level 0 (L0), Syntactic validity. The generated code
standardized configuration; every patch is then evaluated                 parses without syntax errors.
through a four-level verification pipeline (L0 to L3); finally,         • Level 1 (L1), Functional validation. The generated
patches flagged at L2 or L3 are manually reviewed and                     code passes available functional checks, including
confirmed as True Positive, Partial, or False Positive.                   import resolution, structural correctness verification,
2.4.1. Model Configuration and Hardware                                   and execution of associated test cases.
    To reduce variability due to model differences, all frame-          • Level 2 (L2), Static security analysis. The generated
works used GPT-4o-mini (temperature 0.2) and were ex-                     code is analyzed with Bandit (a tool to find Python
ecuted in isolated environments with a shared verification                code security issues, maintained by the Python Code
toolchain. We chose this model to balance response quality,               Quality Authority). We run Bandit and map its find-
cost, and scalability across the evaluation of seven frame-               ings to CWE identifiers using a predefined lookup
works. Experiments were run on a 5 GB NVIDIA A100 MIG                     table. A generated patch fails L2 if it contains any
slice with 8 CPU cores, 17.5 GB RAM, and 512 GB storage,                  HIGH-severity finding, where severity is assigned
with a 600-second timeout.                                                based on CWE type.
    To maintain comparability across frameworks, we stan-
dardized the prompts by keeping the task content identical              • Level 3 (L3), Exploitability assessment. To sup-
while adapting the format to each framework’s input schema.               port exploitability-oriented candidate screening, we
For example, ChatDev takes the task as a single project-                  apply a heuristic scoring mechanism that estimates
level requirement string passed to its task parameter, while              risk based on the co-occurrence of user input sources
MiniSWE takes the same content as a user message inside a                 and dangerous sinks, weighted by CWE severity [2].
ReAct loop; in both cases, the core task description and code             Concretely, the score is computed from four signal
context remain identical, and only the input schema differs.              groups extracted by pattern matching: (i) user-input
At the dataset level, SecurityEval prompts included the                   sources, such as external inputs received from users,
original insecure code context, whereas CVEfixes prompts                  requests, or command-line arguments; (ii) dangerous

: Preprint submitted to Elsevier                                                                                     Page 4 of 22
      sinks, such as dynamic execution, shell invocation,        security-oriented checks indicate that they may still contain
      unsafe deserialization, or security-sensitive database     or introduce a vulnerability. More formally, this is defined
      operations, each assigned a base weight reflecting its     as:
      exploitation severity; (iii) indicators that the origi-
      nal vulnerability pattern targeted by the task is still                            pass       pass
      present; and (iv) context-aware indicators capturing              𝑆𝐹 candidate = (𝐿0      ∧ 𝐿1 ) ∧ (𝐿fail
                                                                                                           2
                                                                                                                ∨ 𝐿fail
                                                                                                                   3
                                                                                                                        )     (2)
      risky co-occurrences, such as a hard-coded credential
      near authentication logic. The total score increases            In other words, a patch is considered a silent failure
      when a user-input source and a dangerous sink co-          candidate if it appears valid and passes available functional
      occur in the same patch, and is further increased          checks, but still raises concerns in later security checks.
      when the sink matches the target CWE of the task.               As an illustrative case, consider a SecurityEval command-
      The score is reduced when safe coding practices are        injection task that required repairing code that built and
      present. In particular, bounded discounts are applied      executed a shell command from external input. The agent-
      for safeguards such as input validation and sanitiza-      generated patch added a length check and renamed surround-
      tion, parameterized query construction, certificate or     ing variables, but retained the original shell-execution call.
      host verification, and secure replacement of known         The patch passed L0 and L1 because it parsed successfully
      unsafe operations. The exploitability score 𝑅 is com-      and the available tests used only benign inputs that produced
      puted as follows, clipped to the range [0, 100]:           the expected output. However, L2 still flagged the reachable
                                                                 unsafe shell execution, and L3 assigned a high score because
                                                                 a user-controlled source co-occurred with a dangerous sink
          ∑            ∑                                         matching the task CWE. Manual review therefore confirmed
    𝑅 = 𝑠∈ 𝑤𝑠 + 𝑗∈ 𝑏𝑗 𝑐 𝑡𝑗 +10 𝛿vuln −min(2𝑛safe , 10),
                                                                 the patch as a silent failure: it appeared successful under
                                                             (1) functional evaluation but preserved the original injection
       where  and  are the input-source types and dangerous- path.
       sink matches detected in the patch, weighted by 𝑤𝑠
       and 𝑏𝑗 respectively; 𝑐 = 1.5 when an input source         2.4.3. Manual Review and Confirmation Criteria
       co-occurs with a sink and 1.0 otherwise; 𝑡𝑗 = 1.3              The L2/L3 pipeline flags candidates automatically, but
       when the sink CWE matches the task target CWE and         static   analysis can produce irrelevant or non-actionable
       1.0 otherwise; 𝛿vuln = 1 when the original target-        warnings.     The first author conducted the initial manual
       CWE pattern is still present; and 𝑛safe ∈ {0, … , 5}      review    of every  flagged case following a structured coding
       is the number of safe-practice categories detected.       procedure.    To reduce  individual bias, a subset of cases was
       The weights 𝑤𝑠 follow three tiers by controllability      independently     reviewed   by another author as part of the
       (web request data 4, interactive and standard input 3,    reliability  assessment  described  in Section 2.5.3.
       environment or file reads 2), and the weights 𝑏𝑗 span
                                                                 Review Process and Consistency Mechanisms To main-
       6 to 12 by exploitation severity, with dynamic code
                                                                 tain consistency across the entire dataset, we applied an
       execution highest (12), command execution next (10),
                                                                 iterative review protocol:
       template rendering (9) and unsafe deserialization (8)
       in the middle, and formatted-string operations lowest         (i) Standardized Annotation: The first author examined
       (7 and 6). For patches spanning multiple files, 𝑅 is              the generated patch, L2/L3 findings, and original task
       taken as the maximum across files.                                description for each case. Judgments and metadata
       A generated patch whose total score reaches the                   (e.g., failure type, severity) were recorded using a
       threshold of 15 is treated as a silent failure candidate.         codebook [28], which strictly defined the admissible
       We set the threshold to 15 and the associated signal              values for each dimension.
       weights in Eq. (1) based on calibration with Iteration
                                                                    (ii) Iterative Alignment (Within-iteration): The review
       1 candidates. This configuration retained the high-
                                                                         was conducted iteration-by-iteration. At the end of
       risk source-sink co-occurrences observed during the
                                                                         each iteration, iteration-level summaries were com-
       initial calibration while reducing isolated low-severity
                                                                         piled to analyze the distribution of judgments and re-
       patterns. Since all candidates undergo manual review
                                                                         examine borderline cases.
       before confirmation, the threshold serves as a sensi-
       tivity parameter for candidate selection rather than a      (iii) Retrospective Revision (Across iterations): Follow-
       final classification boundary.                                    ing iteration 3, all codes were consolidated to ensure
    We define patches that fail L0 or L1 as explicit failures,           uniformity. If a newly observed case prompted a re-
since their deficiencies are visible through standard quality            finement to the coding scheme, earlier judgments were
gates. Patches that pass both levels but are flagged at L2 or            retrospectively updated. Adjustments were recorded
L3 are treated as silent failure candidates: on the surface,             during the coding process to support transparency and
they look like successful repairs because they are syntac-               consistency.
tically valid and pass available functional checks, yet later

: Preprint submitted to Elsevier                                                                                     Page 5 of 22
Table 3
Iteration-based data collection plan.
             Iteration    Tasks    Source                     Sampling Logic                       Coding Activity
             Iteration 1      50   SecurityEval               Proportional by CWE                  Open Coding
             Iteration 2      50   SecurityEval + CVEfixes Targeted framework–dataset pairs        Axial Coding
             Iteration 3      50   SecurityEval + CVEfixes Underrepresented patterns               Selective Coding
             Total: 150 tasks      × 7 agents = 1,050 target traces


 (iv) Independent Validation: To assess inter-rater relia-               execution and preliminary verification-based screen-
      bility, another author independently recoded 20% of                ing. Each iteration involved: (i) selecting a batch of
      the corpus (reliability measures reported in Section               tasks; (ii) executing the selected agent frameworks
      2.5.3).                                                            on these tasks; (iii) normalizing the outputs into the
                                                                         common trace schema; (iv) screening the resulting
                                                                         traces through the Multi-Level Verification Frame-
Category Definitions Based on the review, each candidate
                                                                         work; and (v) reviewing the resulting candidate cases
was assigned to exactly one of the following categories:
                                                                         to guide the sampling focus of the next round [30, 31].
    • True Positive (TP): The patch contains a clear in-                 The three iterations served different purposes. (i) It-
      stance of the target vulnerability. The agent either               eration 1 sampled from SecurityEval proportionally
      made no attempt to fix it or applied a superficial fix             across CWE categories to obtain broad initial cover-
      that entirely failed to address the root cause. For ex-            age. (ii) Iteration 2 used targeted sampling based on
      ample, validating input length while leaving an unsafe             the patterns observed in Iteration 1, especially recur-
      call intact.                                                       ring or ambiguous failure patterns that required fur-
                                                                         ther evidence. (iii) Iteration 3 focused on underrepre-
    • Partial: The patch contains a visible and relevant                 sented open codes and boundary cases to supplement
      mitigation attempt, but the defense remains incom-                 missing failure patterns and refine category coverage.
      plete and a plausible exploit path is still present in the         This iterative strategy was intended to support pro-
      code. Unlike TP, a defense against the target CWE is               gressive coverage of silent-failure patterns rather than
      visibly attempted; unlike FP, the defense does not fully           statistical representativeness. Table 3 summarizes the
      neutralize the weakness. For instance, the patch blocks            sampling details.
      one specific bypass while leaving the sink reachable            2. Preprocessing. To address the inconsistencies in ex-
      through another path, or constrains a symptom rather               ecution trace formats across different frameworks,
      than the underlying sink.                                          we normalized all data into a unified schema to en-
    • False Positive (FP): The patch does not contain a                  able cross-framework comparison. This step was in-
      genuine security weakness relevant to the task, even               formed by recent multi-agent failure dataset construc-
      though it was flagged by the pipeline. This typically              tion practice, where cross-framework trace analysis
      occurs when the flagged pattern appears only in non-               requires standardized representations to support con-
      deployable test code, when an effective safeguard                  sistent annotation and comparison [11]. After normal-
      already neutralizes the risky operation, or when the               ization, we excluded 20 traces that did not produce
      static tool matches code that appears dangerous syn-               valid outputs due to timeouts, runtime crashes, or
      tactically but is harmless in context.                             incomplete generation, leaving 1,030 valid traces. We
                                                                         then evaluated each valid trace through the multi-level
    Both TP and Partial cases are retained in the confirmed              verification framework described in Section 2.4.2.
corpus. We include Partial cases because they exhibit the                Generated patches that failed at L0 or L1 were clas-
same code-level failure patterns as TPs and are relevant for             sified as explicit failures. Those that passed both L0
taxonomy construction, which focuses on what the agent did               and L1 but were flagged at L2 or L3 yielded 252 silent
wrong rather than on exploitability severity. In our corpus,             failure candidates. After manual review, 170 cases
Partial cases account for 39 of 170 confirmed failures.                  were confirmed as silent failures. These 170 cases
                                                                         form the corpus for the coding procedure described
2.5. Data Collection and Analysis                                        next.
2.5.1. Data Collection
   Data collection consisted of two steps: sampling and            2.5.2. Coding Procedure
preprocessing.                                                         We analyzed confirmed cases using an iterative thematic
                                                                   coding process inspired by Grounded Theory [32]. Coding
   1. Sampling. We purposively sampled 150 tasks in three          was conducted in three stages, using individual execution
      iterations of 50 each [29], drawn without replacement        traces (one framework’s output per task) as the unit of
      from a pool of 1,236 eligible tasks. In this study, an it-   analysis.
      eration refers to one sampling round followed by agent

: Preprint submitted to Elsevier                                                                                    Page 6 of 22
Table 4
Inter-rater agreement across coding dimensions.
                   (a) D0 triage verdict                                                                         (b) D1 axial category                                                                                          (c) Composite D0×D1

       R1 ∖ R2 TP Partial FP Total                                                               R1 ∖ R2 Om. Inad. Intro. FP Total                                                               R1 ∖ R2 FP P-I P-O T-I T-Intro T-O Total
       TP                       19              2             2           23                     Om.                  8              0            0         1            9                       FP                         6        1   0          0               0                 1             8
       Partial                  0               3             1            4                     Inad.                0              7            0         2            9                       P-I                        1        2   0          0               0                 0             3
       FP                        1              1             6            8                     Intro.               0              2            7         0            9                       P-O                        0        0   1          0               0                 0             1
                                                                                                 FP                   1              1            0         0            2                       T-I                        1        1   0          4               0                 0             6
       Total                    20              6             9           35                                                                                                                     T-Intro                    0        1   0          1               7                 0             9
                                                                                                 Total                9              10           7         3          29                        T-O                        1        0   0          0               0                 7             8
                                                                                                                                                                                                 Total                      9        5   1          5               7                 8            35

Note: Om. = Omission; Inad. = Inadequacy; Intro. = Introduction; P-I = Partial-Inadequacy; P-O = Partial-Omission; T-I =
TP-Inadequacy; T-Intro = TP-Introduction; T-O = TP-Omission.

 7    Deserialization / Input
 6    Weak Crypto
                                                                                                                                           Taxonomy Legend
 5    Code Injection                                                                                                                                                                                                                              Subcategory                             Type of Common
 5    Path Traversal
                                                          7       Path Traversal                                                                      Taxonomy                                      Category                                 (Number of silent failures)                  Weakness
                                                          5       Auth Bypass                                                                                                                                                                                                             Enumeration (CWE)
 4    Weak Random                                                                                    2     Sensitive Log
 4    XML External Entity (XXE)                           2       XXE                                2     Server-Side Request Forgery (SSRF)
                                                                                                     1    Weak Random                                                                                        2      Config / Debug
 3    Command Injection                                   2       Command Injection
 3    Injection (Generic)                                                                            1     Auth Bypass                                                                                       1      Weak Crypto
                                                          2       Injection (Generic)
  5   Other singleton CWE families                                                                                                                         4    Query Injection                              1      Other                                 1       Weak Crypto
                                                                  Other singleton CWE families       3    Other singleton CWE families
                                                          4

      Insecure API Preserved                                            Missing Mitigation                Deployment Context Risk                                   Missing Sanitization                           Unsafe Default Retained                        Ambiguous Repair Intent
               (42)                                                            (22)                                (9)                                                      (4)                                              (4)                                           (1)


                                                                                                                                                Omission
                                                                                                                                                       82 (48.2%)



                                                                                   Taxonomy of silent failures in LLM-based agent code repair
                                             36 (21.2%)                                                                                                                                                     52 (30.6%)


                                          Inadequacy                                                                                                                                      Introduction
                                          Weak Mitigation                                                    Introduced New Vulnerability                                                 Hardcoded Secret                                                          Vulnerable Test Code
                                               (36)                                                                      (41)                                                                   (10)                                                                         (1)
                   14    Path Traversal                                                                      8     Info Disclosure                                                2   Cross-Site Scripting (XSS)                                              1    Deserialization / Input
                   7     Cross-Site Scripting (XSS)                                                          7     Open Redirect                                                  2   Weak Password
                   6     Open Redirect                                                                      5      Path Traversal                                                 1   Auth Bypass
                   5     Code Injection                                                                     5      ReDoS                                                          1   SQL Injection
                   2     SQL Injection                                                                      3      Cleartext                                                      1   Hardcoded Creds
                         Command Injection                                                                  3      Sensitive Log                                                  3   Other singleton CWE families
                   1
                                                                                                            2      Code Injection
                   1     SSRF
                                                                                                            8      Other singleton CWE families




Figure 2: Taxonomy of silent failures in LLM-based agent code repair. The taxonomy classifies failure mechanisms rather than
CWE families; therefore, the same CWE family may appear under different open codes when it arises through different mechanisms.
“Other singleton CWE families” denotes one-off CWE families grouped only for visualization to avoid over-fragmenting the figure.



      1. Open coding. The first author examined each con-                                                                                                  check for consistency. We considered coding complete when
         firmed case, including the generated code, L2/L3 find-                                                                                            no new codes emerged in two consecutive batches of 50
         ings, and the original task context, and assigned de-                                                                                             traces [30].
         scriptive labels to observed failure patterns. No codes
         were predefined. Each case was also annotated with                                                                                                2.5.3. Reliability Measures
         a propagation chain, a severity rating reflecting the                                                                                                 To ensure the consistency of the qualitative coding pro-
         coder’s overall assessment of the weakness (Critical,                                                                                             cess and mitigate individual bias, we performed an Inter-
         High, Medium, Low), and candidate detection mech-                                                                                                 Rater Reliability (IRR) analysis using Cohen’s Kappa [33].
         anisms.                                                                                                                                           A random subset of 35 cases was independently coded by
      2. Axial coding. The first author analyzed the initial                                                                                               another author (R2), in parallel with the primary coder (R1).
         codes and organized them along four dimensions:                                                                                                   Each case was assessed along two coding dimensions: (i) D0
         failure type, originator role, injection stage, and code                                                                                          (triage verdict), classifying the case as TP, PARTIAL, or FP;
         location. Relationships between dimensions were ex-                                                                                               and (ii) D1 (axial category), recording the axial category
         amined and documented.                                                                                                                            assigned by a rater, with FP retained as an exclusion label
      3. Selective coding. The first author reviewed and re-                                                                                               for cases a rater did not treat as a silent failure.
         fined the coding results. We identified an overarching                                                                                                Agreement was evaluated at three levels, as shown in Ta-
         theme, security-compliance decoupling, that connects                                                                                              ble 4. First, we measured agreement on the D0 triage verdict,
         the categories into a unified explanation of silent fail-                                                                                         which distinguishes true positives, partial cases, and false
         ures. Categories were merged, split, or dropped based                                                                                             positives. Second, we measured agreement on the D1 axial
         on discussion among all authors.                                                                                                                  category, which assigns non-false-positive cases to the main
                                                                                                                                                           silent-failure categories. This analysis included 29 cases
   Throughout this process, each newly coded case was
                                                                                                                                                           because cases coded as FP by both raters were excluded
compared against earlier cases in the same category to

: Preprint submitted to Elsevier                                                                                                                                                                                                                                                  Page 7 of 22
Table 5
Distribution and exploitability profile of silent failure open codes.
  Axial Category Open Code                            Description                                         𝑛 % in Total Mean L3
                                                                                                                 24.7
  Omission           Insecure API Preserved           Dangerous API retained without secure sub-         42                     16.7
                                                      stitution
                                                                                                                 12.9
                     Missing Mitigation               Required security control entirely absent          22                      5.8
                                                                                                                  5.3
                     Deployment Context Risk          Security adequacy depends on deployment             9                      4.2
                                                      context
                                                                                                                  2.4
                     Missing Sanitization             Input sanitization absent at a critical point       4                      2.0
                                                                                                                  2.4
                     Unsafe Default Retained          Insecure configuration value left unchanged         4                      1.0
                                                                                                                  0.6
                     Ambiguous Repair Intent          Repair intent ambiguous; security effect in-        1                      0.0
                                                      determinate
                     Subtotal                                                                            82      48.2           10.7
                                                                                                                 21.2
  Inadequacy         Weak Mitigation                  Defense attempted but bypassable or incom-         36                     17.7
                                                      plete
                     Subtotal                                                                            36      21.2           17.7
                                                                                                                 24.1
  Introduction       Introduced New Vulnerability Repair introduced a vulnerability not origi-           41                      6.9
                                                  nally present
                                                                                                                  5.9
                     Hardcoded Secret                 Cryptographic secret embedded as string            10                     10.4
                                                      literal
                                                                                                                  0.6
                     Vulnerable Test Code             Test code reintroduced a fixed vulnerability        1                     29.0
                     Subtotal                                                                            52     30.6             8.0
  Total                                                                                                 170     100.0           11.4


from the axial-category calculation. Third, we computed a               Figure 2 and Table 5), propagation patterns across agent
composite D0×D1 agreement score, which combines the                     architectures in Section 3.2 (see Table 6 and Figure 4),
triage decision and the axial category into a single coding             and the distribution of silent failures across vulnerability
decision. We report the composite score as the primary inter-           types, code locations, and severity or exploitability levels in
rater reliability metric because it captures both whether a             Section 3.3 (see Figure 6 and Table 8).
candidate was treated as a confirmed silent failure and how
it was categorized.                                                     3.1. Silent Failure (RQ1)
    The primary composite agreement was 𝜅 = 0.71, in-                       Figure 2 provides the complete taxonomy of silent fail-
dicating substantial agreement. The D0 triage verdict and               ures identified in this study. The taxonomy was derived
D1 axial category also reached substantial agreement, with              through qualitative coding of 170 confirmed silent failures
𝜅 = 0.63 and 𝜅 = 0.66, respectively. All disagreements                  and consists of three axial categories: Omission, Inadequacy,
were resolved through discussion among the authors. These               and Introduction with ten open codes. Table 5 complements
discussions were used to clarify ambiguous coding rules,                the figure by reporting the quantitative distribution and mean
refine category boundaries, and update the final codebook               L3 exploitability risk score for each open code and category.
before applying it consistently to the full corpus. In addition,            The results show that Omission is the most frequently
each newly coded case was compared against prior cases                  observed category (82/170, 48.2%), followed by Introduc-
in the same category to reduce category drift during the                tion (52/170, 30.6%) and Inadequacy (36/170, 21.2%). A
iterative coding process.                                               silent failure may exhibit more than one security symptom.
                                                                        However, we assign each case to the dominant failure mech-
                                                                        anism, namely the mechanism most directly responsible for
3. Results
                                                                        the failure to satisfy the security intent of the task. Figure 3
     This section presents the results of our empirical in-             further shows how the open codes differ in both prevalence
vestigation, addressing the three research questions outlined           and exploitability risk.
in Section 1: RQ1 on failure taxonomy and prevalence,                       1. Omission (82/170, 48.2%). Omission refers to cases
RQ2 on propagation patterns across agent architectures, and             in which the agent fails to implement a necessary secu-
RQ3 on the distribution of silent failures across vulnera-              rity measure despite the task context indicating that such
bility types, code locations, and severity or exploitability            a measure is required. This is the largest category in the
levels. Throughout this section, we present axial categories            taxonomy of silent failures. We identified and classified six
in boldface, open codes in Title Case (e.g., Insecure API               open codes under Omission (see Table 5). Each of them is
Preserved), and conceptual terms in italics. We report the              briefly described below.
silent failure taxonomy and prevalence in Section 3.1 (see

: Preprint submitted to Elsevier                                                                                          Page 8 of 22
                                                    28%                                                                             Insecure API Preserved
                                                                                                           Overall mean L3 = 11.4   n=42 . 24.7% . L3=16.7                                Axial Category
                                                                                                                                    most frequent failure
                                                                                                                                                                                            Omission (6)
                                                                                                                                                                                            Inadequacy (1)
   Prevalence among confirmed silent failures (%)




                                                    24%
                                                                                                                                                                                            Introduction (3)


                                                    20% Introduced New Vulnerability
                                                          n=41 . 24.1% . L3=6.9                                                              Weak Mitigation
                                                          scaffolding-driven                                                                 n=36 . 21.2% . L3=17.7
                                                                                                                                             highest mean risk
                                                    16%

                                                                                                                 Vulnerable Test Code
                                                                                            Missing Mitigation
                                                                                                                 n=1 . 0.6% . L3=29.0
                                                    12%                                                                                                                                       Bubble scale (n)
                                                                                                                 rare but extreme outlier

                                                                                                                                                                                                           n=1
                                                                                    Deployment Context Risk
                                                     8%
                                                                                                            Hardcoded Secret                                                                               n=10
                                                                                                                                                                 median prevalence 5.6%


                                                     4% Unsafe Default Retained                                                                                                                            n=22


                                                                                    Missing Sanitization
                                                     0%
                                                          Ambiguous Repair Intent                                                                                                                          n=42

                                                                   0                5               10               15                     20               25                  30
                                                                                                 Mean exploitability risk score (L3)



Figure 3: Risk-prevalence landscape of silent failure codes. Each bubble represents one open code; horizontal axis shows mean
L3 exploitability risk, vertical axis shows prevalence (%) among the 𝑛 = 170 confirmed silent failures, bubble size encodes the
absolute count 𝑛, and color encodes the axial category. Reference lines mark the overall mean L3 (11.4) and median prevalence
across codes.


    • Insecure API Preserved (42, 24.7%): The agent retains                                                                                 pattern appeared without overlapping with other Omission
a dangerous API call from the input context without substi-                                                                                 codes.
tuting a secure alternative. This is the dominant code within                                                                                    • Unsafe Default Retained (4, 2.4%): An insecure con-
Omission and the most frequent code in the entire corpus.                                                                                   figuration value present in the input is left unchanged in the
We observed that agents often applied cosmetic adjustments                                                                                  generated code. Observed instances include retained debug
such as renaming variables or adding length checks, while                                                                                   flags and default credentials in authentication-related tasks.
leaving the vulnerable call intact.                                                                                                              • Ambiguous Repair Intent (1, 0.6%): The repair intent
    • Missing Mitigation (22, 12.9%): The agent omits an                                                                                    is ambiguous and the security effect cannot be determined
entire security control that the task requires but the existing                                                                             from the generated artifact alone. We retained this code to
code does not suggest. This code appeared predominantly                                                                                     mark a boundary case rather than discard the trace, but it
in CVEfixes tasks, which more frequently require adding                                                                                     represents an edge case in our corpus.
new security logic rather than substituting an API. Unlike                                                                                       2. Inadequacy (36/170, 21.2%). Inadequacy refers to
Insecure API Preserved, which reflects insecure pattern re-                                                                                 cases in which the agent appears to recognize the secu-
production, Missing Mitigation captures cases where the                                                                                     rity requirement and attempts a defense, but the resulting
required defense must be inferred from task intent rather than                                                                              mechanism remains incomplete or bypassable. This cate-
copied from the input context.                                                                                                              gory differs from Omission in that a security-relevant action
    • Deployment Context Risk (9, 5.3%): The generated                                                                                      is present in the generated code; what is missing is its suffi-
code may appear secure in isolation, but its security ad-                                                                                   ciency. We identified a single open code under Inadequacy.
equacy depends on deployment-time conditions that the                                                                                       It is briefly described below.
task does not specify. The agent leaves these conditions                                                                                         • Weak Mitigation (36, 21.2%): The agent implements
unaddressed, transferring the security burden to downstream                                                                                 a defense that is partial, bypassable, or built on an incorrect
operators. Examples include hardcoded permissive CORS                                                                                       security primitive. Among the open codes occurring in more
policies and unverified trust assumptions about upstream                                                                                    than one case, Weak Mitigation carries the highest mean
input sources.                                                                                                                              L3 exploitability risk (17.7), suggesting that partially imple-
    • Missing Sanitization (4, 2.4%): Input sanitization is                                                                                 mented defenses are associated with a viable attack surface
absent at a critical point along the data flow. This code                                                                                   in the confirmed cases. Cases concentrated in vulnerability
differs from Missing Mitigation in that the required defense                                                                                types such as path traversal, command injection, and eval-
is specifically input validation or escaping at an identifiable                                                                             based execution. For example, one agent implemented path
sink. The small count reflects how seldom this isolated                                                                                     traversal prevention using a string-level comparison func-
                                                                                                                                            tion rather than a path-aware alternative; another added a

: Preprint submitted to Elsevier                                                                                                                                                                               Page 9 of 22
                                                          Planner               Architect                   Engineer             Reviewer          Failure Split

            Planning-Stage Security Omission              No Security                                       Implements          Not Detected
                                                          Requirement
                          (Reviewer Non-Detection)
                                                                                                                                                      22 / 9 / 0
                 Design-Originated Omission                                       Specifies                 Implements          Not Detected
                          (Reviewer Non-Detection)
                                                                                                                                                      22 / 6 / 1
              Design-Originated Introduction                                      Specifies                  Introduces          Not Flagged
                                                                                                            Vulnerability
                        (Reviewer Non-Intervention)
                                                                                                                                                      0 / 0 / 27
                      Direct Implementation                                                                Generates Code       Not Engaged
                                       (No Review)
                                                                                                                                                      10 / 4 / 6
           Implementation-Originated Failure                                                                 Introduces         Not Detected
                                                                                                            Vulnerability
                          (Reviewer Non-Detection)
                                                                                                                                                      0/0/6
                        QA-Involved Patterns                                                                   Fixes          QA: Reintroduces /
                                                                                                                                 Insufficient
                             (QA Acts As Reviewer)
                                                                                                                                                      0/1/1
              Single-Agent Direct Generation                                                  Generates Code
                               (No Review Handoff)
                                                                                                                                                     28 / 16 / 11




                                                 Action   Reviewer Fails / Not Engaged          Omission         Inadequacy     Introduction

Figure 4: Propagation chain patterns of silent failures by origin, failure mechanism, and review outcome. Color-coded bars on the
right show the axial category split for each pattern.



command allowlist but retained an injection-prone execution                                         • Vulnerable Test Code (1, 0.6%): The agent introduces
mode; a third constructed a restricted evaluation sandbox                                       a vulnerability through generated test code rather than pro-
whose filtering rules were too permissive to prevent known                                      duction code. Although rare, this case stands out with an
escape techniques.                                                                              L3 score of 29.0, far above the Introduction category mean
    3. Introduction (52/170, 30.6%). Introduction refers to                                     of 8.0, since the test artifact reintroduced a previously fixed
cases in which the repair process itself injects a vulnerability                                vulnerability into the project workspace.
that was not present in the original code. Unlike Omission                                          Taken together, the three axial categories share a com-
and Inadequacy, which describe what the agent failed to                                         mon characteristic: in every confirmed case, the agent pro-
do, Introduction describes a new defect arising from agent                                      duced code that satisfied L0 and L1 verification criteria yet
action. We identified and classified three open codes under                                     failed to achieve the security intent of the task. We refer
Introduction. Each of them is briefly described below.                                          to this recurring pattern as security-compliance decoupling:
    • Introduced New Vulnerability (41, 24.1%): The agent                                       the observed disconnect between an agent’s externally ob-
generates code that introduces a vulnerability absent from                                      servable compliance signals and the actual security prop-
the original input. This code is the dominant pattern within                                    erties of the generated artifact. The three categories corre-
Introduction (41/52, 78.8%). Multi-agent frameworks con-                                        spond to distinct points at which this disconnect appears:
tributed a higher share, concentrated in ChatDev and MetaGPT.                                   Omission involves a gap between the task and appropriate
These frameworks also generated additional artifacts, such                                      API selection; Inadequacy involves a gap between identify-
as configuration files, build scripts, and test scaffolding,                                    ing the security requirement and implementing a complete
where some of these introduced vulnerabilities appeared.                                        defense; Introduction involves a gap between addressing
    • Hardcoded Secret (10, 5.9%): The agent embeds cryp-                                       the primary task and managing the security context of all
tographic secrets (e.g., signing keys, tokens, passwords)                                       generated artifacts.
as string literals in the generated code. The surrounding
authentication or session logic is often otherwise correct,
which makes this pattern particularly easy to overlook in
functional review.




: Preprint submitted to Elsevier                                                                                                                            Page 10 of 22
                                                    Sample Size                              Composition (% of Cases)                        Absolute Counts
                                                                                                                                           Om     Inad Intro
                       AutoGen                                       39                      64%                        23%    13%
                       M, n = 39
                                                                                                                                           25     9      5
                       MetaGPT                                  30                37%              13%                  50%
Multi-agent




                       M, n = 30
                                                                                                                                           11     4      15

                       ChatDev                                 27                  44%                                  48%
                       M, n = 27                                                                                                           12     2      13

                       AgentCoder                      19                        32%                26%                  42%
                       M, n = 19                                                                                                           6      5      8

                       MiniSWE                            21                      38%                19%                 43%
                       S, n = 21                                                                                                           8      4      9
Single-agent




                       Aider                           19                                    63%                         32%               12     6      1
                       S, n = 19

                       OpenHands                     15                                 53%                          40%                   8      6      1
                       S, n = 15

                                                                          0             25               50             75           100



                                                                      Omission          Inadequacy            Introduction

                                      Figure 5: Distribution of silent failure categories across agent frameworks.



               Key Findings from RQ1                                                   Table 7, and the distribution of categories across frameworks
                                                                                       is shown in Figure 5. Each aspect is discussed below.
               We identified three recurring mechanisms of silent                          Originator attribution was assigned during manual cod-
               failures: Omission, Introduction, and Inadequacy.                       ing (see Section 2.5). For each confirmed case, coders in-
               These mechanisms share a common pattern of                              spected the per-role trace outputs and identified the earliest
               security-compliance decoupling, where generated                         role whose output made the security deficiency observable
               patches appear to satisfy functional requirements                       in the trajectory. When the deficiency first appeared in a
               but fail to preserve security properties. We further                    planning or design artifact, the corresponding Planner or
               derived ten open codes to capture the specific failure                  Architect role was coded as the originator; when it first ap-
               patterns, with Insecure API Preserved and Intro-                        peared in generated code, the Engineer role was coded as the
               duced New Vulnerability being the most frequent.                        originator. Disagreements were resolved through discussion.
               Among the three mechanisms, Inadequacy showed                           For instance, in one path traversal task, the Planner decom-
               the highest mean exploitability risk, suggesting that                   posed the request into file-reading and response-formatting
               partially implemented defenses may be especially                        steps but omitted the need to constrain user-provided paths to
               dangerous because they create an appearance of                          a safe base directory. The Engineer implemented the under-
               security while remaining bypassable.                                    specified plan by joining user input with a base path without
                                                                                       canonicalization, and the Reviewer approved the output after
                                                                                       checking functional completeness rather than path-handling
3.2. Propagation Patterns Across Agent                                                 security. Because the first observable deficiency appeared in
     Architectures (RQ2)                                                               the planning artifact and persisted through implementation
    We use the same three axial categories as in Section 3.1:                          and review, we coded the Planner as the originator and the
Omission, Inadequacy, and Introduction, denoting absent                                propagation pattern as a planning-stage omission cascade.
defenses, incomplete defenses, and newly introduced vul-                                   Among multi-agent systems, the three most frequent
nerabilities, respectively. The propagation patterns are sum-                          patterns all involve a Reviewer role that does not intercept
marized in Table 6, and Figure 4 illustrates the operational                           the security deficiency. The most common is the planning-
chain of each pattern by origin stage, failure mechanism, and                          stage omission cascade, in which the Planner decomposes
review outcome. The architectural comparison is reported in

: Preprint submitted to Elsevier                                                                                                                 Page 11 of 22
Table 6                                                           each produced a silent failure that shared the same con-
Propagation chain patterns of silent failures.                    firmed CWE; these comparable failures account for 62.9%
                                                                  (107/170) of all confirmed cases. We treated failures as com-
 Propagation Pattern                      Om     Inad    Intro
                                                                  parable when they occurred on the same task and shared the
 Multi-Agent
                                                                  same confirmed CWE. Four of the tasks were particularly
 Planning-Stage Omission Cascade           22        9      0     convergent in that six of the seven frameworks produced a
 Design-Originated Omission                22        6      1     silent failure with the same CWE. This shows that a subset of
 Design-Originated Introduction             0        0     27     tasks elicited similar silent-failure patterns across otherwise
 Direct Implementation (No Review)         10        4      6     distinct frameworks, rather than isolated framework-specific
 QA-Involved Patterns                       0        1      1     failures. However, because all experiments used the same
 Implementation-Originated                  0        0      6     base model and related task prompts, this convergence
 Single-Agent                                                     should not be attributed to framework architecture alone.
                                                                  The present design does not isolate model effects from
 Single-Agent Direct Generation            28       16     11
                                                                  other shared factors, such as task design, prompt content, or
 Total                                     82       36     52
                                                                  dataset-specific vulnerability patterns. We therefore report
                                                                  cross-framework convergence as an empirical pattern in our
Table 7                                                           corpus.
Axial category distribution by architecture type.
                                                                      Key Findings from RQ2
                      Om.       Inad.     Intro. Total
  Multi-agent 54 (47.0%) 20 (17.4%) 41 (35.7%) 115
                                                                      We observed that silent failures propagate through
  Single-agent 28 (50.9%) 16 (29.1%) 11 (20.0%)    55
                                                                      three primary multi-agent mechanisms: planning-
  Total                82          36        52 170
                                                                      stage security omission cascades, design-originated
                                                                      omissions, and design-originated introductions. In
the task without including security requirements, the En-             the multi-agent cases we reviewed, the Reviewer
gineer implements code consistent with the underspecified             rarely flagged a security deficiency before it reached
plan, and the Reviewer does not flag the issue. Following             the final output. We further observed different fail-
closely is design-originated omission, where the Architect            ure profiles across agent architectures: multi-agent
specifies a design that the Engineer implements and the Re-           systems produced more INTRODUCTION failures,
viewer evaluates without detecting the deficiency. The third          consistent with their additional artifact generation,
is design-originated introduction; ChatDev and MetaGPT                whereas single-agent systems produced more INAD-
accounted for all instances of this pattern, as their pipelines       EQUACY failures, consistent with attempted but in-
produce configuration templates and scaffolding that expand           complete defenses. Finally, similar failures recurred
the attack surface.                                                   across frameworks on the same tasks, indicating
     A Reviewer role was active in most multi-agent cases.            cross-framework convergence within the observed
In the confirmed cases we reviewed, the Reviewer rarely               corpus.
flagged the relevant security deficiency before it reached the
final output. This pattern appeared across the multi-agent        3.3. Distribution Across Vulnerability Types, Code
frameworks in our corpus, despite their differing coordina-
                                                                       Locations, and Risk Levels (RQ3)
tion architectures.
                                                                      The distribution across CWE families is shown in Fig-
     Beyond these multi-agent patterns, Table 7 shows dis-
                                                                  ure 6, the distribution across code locations is reported in
tinct failure distributions between the two architectural fam-
                                                                  Table 8, and the severity and risk profiles are reported in
ilies. For instance, Introduction failures are more common
                                                                  Table 9. These three views capture, respectively, what kind
in multi-agent systems (41/115, 35.7%) than in single-agent
                                                                  of vulnerability is affected, where in the code the failure
ones (11/55, 20.0%), reflecting the additional configuration
                                                                  resides, and how severe and exploitable it is. Across all three,
and scaffolding artifacts their pipelines produce. By con-
                                                                  the axial categories align with distinct profiles rather than
trast, Inadequacy accounts for a higher share of single-agent
                                                                  spreading evenly, as detailed below.
failures (16/55, 29.1%) than of multi-agent ones (20/115,
                                                                      Specifically, as Figure 6 illustrates, Omission accounts
17.4%). This indicates that the observed failure profile dif-
                                                                  for the large majority of cases in families where the fix
fers between the two architecture groups: Introduction is
                                                                  involves substituting a known insecure API with a secure
more frequent in multi-agent systems, whereas Inadequacy
                                                                  alternative: weak cryptography (8/9, 88.9%), deserialization
represents a larger share of single-agent failures. However,
                                                                  (7/8, 87.5%), XXE (7/8, 87.5%), and command injection
the proportion of Omission is nearly identical across archi-
                                                                  (5/6, 83.3%). These families share a common trait: the
tectures (54/115, 47.0% and 28/55, 50.9% respectively).
                                                                  insecure pattern is visible in the code, and its secure coun-
     Further, we observed task-level convergence across frame-
                                                                  terpart is well-documented. Conversely, Inadequacy clusters
works. Specifically, on 26 tasks, three or more frameworks
                                                                  in families whose fix must cover multiple input cases or
                                                                  bypass routes, including XSS and path traversal. Finally,

: Preprint submitted to Elsevier                                                                                   Page 12 of 22
                                            Weak Crypto                                           89%                                               11%
                                          Deserialization                                        88%                                                12%
        API-substitution                            XXE                                          88%                                                12%
    (Omission-dominant)
                                       Command Injection                                        83%                                               17%
                                             Auth Bypass                                  75%                                               25%

         Logic-intensive                             XSS                                   78%                                               22%
  (Inadequacy-dominant)                                                39%                                           45%                          16%
                                           Path Traversal

        Newly introduced                  Info Disclosure                                               100%
 (Introduction-dominant)                   Open Redirect                  46%                                                   54%
                                           Code Injection               42%                                          42%                          17%
                  Mixed
                                            SQL Injection               40%                                      40%                          20%

                                                            0                 25                         50                       75                      100
                                                                                       Proportion within CWE family (%)
                                                                                   Omission        Inadequacy         Introduction

                                        Figure 6: Silent failure category distribution by CWE family.



Table 8                                                                       Table 9
Silent failure distribution by code location and axial category.              Severity distribution and L3 risk by axial category.
   Code Location Om. Inad. Intro. Total In Total                                                              Om.      Inad.     Intro.     Total
   Input Handling          26    33           2       61        35.9                     Severity
                                                                21.8                       Critical            17           5           0     22
   Configuration            5      0        32        37                                   High                31          17           5     53
                                                                20.6                       Medium              34          14          46     94
   API Call                35      0          0       35
                                                                11.2                       Low                  0           0           1      1
   Business Logic           7      3          9       19
                                                                5.3                      L3 Risk
   Authentication           2      0          7        9                                   Mean               10.7      17.7        8.0      11.4
                                                          5.3                              Max                60.8     100.0       58.0     100.0
   Other                    7     0          2        9
   Total                   82    36         52      170 100.0%                  Note. Color intensity encodes magnitude per row. Mean L3 and
Note. The In Total column shows each code location’s share of the               Max L3 denote the mean and maximum exploitability risk score
170-case corpus, with bar length proportional to that share. Three                             under L3 verification, respectively.
 locations (Input handling, Configuration, and API call) together
account for over three-quarters of all confirmed silent failures, and
 each is the dominant location for one axial category respectively                The severity and exploitability profiles further differenti-
            (Inadequacy, Introduction, and Omission).                         ate the three categories. Severity follows the rating assigned
                                                                              during the coding procedure (see Section 2.5.2), and the L3
                                                                              risk score is the exploitability estimate produced by our L3
Introduction is associated with newly created flaws, such as
                                                                              procedure (see Section 2.4.2). With these definitions, Table 9
information disclosure and open redirect.
                                                                              reports the severity distribution and L3 risk by category.
    Besides vulnerability family, code location provides a
                                                                              Omission contains the largest number of critical-severity
complementary view of where silent failures reside. Table 8
                                                                              cases, predominantly involving unrestricted code execution
presents the distribution across code locations. Omission is
                                                                              and insecure deserialization. Introduction has the lowest
most frequent in API calls and input handling, corresponding
                                                                              severity profile, with most cases rated as medium (46/52,
to cases where the agent retained a dangerous function call
                                                                              88.5%), reflecting that introduced vulnerabilities tend to
or omitted required validation logic. Inadequacy is predom-
                                                                              be configuration-level issues rather than direct execution
inantly located in input handling (33/36), reflecting cases
                                                                              paths. However, Inadequacy shows the highest mean L3 risk
where agents attempted validation or sanitization but imple-
                                                                              (17.7), above Omission (10.7) and Introduction (8.0). Many
mented it incorrectly. Introduction is highly concentrated in
                                                                              Inadequacy cases occur in logic-intensive families such as
configuration and business logic, corresponding to vulner-
                                                                              XSS and path traversal, where partial defenses can leave
abilities added through scaffolding generation or auxiliary
                                                                              bypass routes open.
functionality. The alignment between code location and axial
                                                                                  Overall, these distributions reveal three cross-dimensional
category suggests that the taxonomy dimensions capture
                                                                              relationships. First, CWE family is associated with axial
relatively distinct aspects of the failure phenomenon.
                                                                              category: API-substitution vulnerabilities such as weak

: Preprint submitted to Elsevier                                                                                                            Page 13 of 22
cryptography and deserialization map predominantly to             not necessarily correct [1]. The cases we identify, however,
Omission, logic-intensive vulnerabilities such as path traver-    go a step further: the patches are not merely plausible but
sal and XSS map to Inadequacy, and vulnerability types            also pass the available functional checks, yet remain insecure
such as information disclosure and open redirect map to           at the semantic level. As LLM-based agents become more
Introduction. This association indicates that vulnerability       capable of satisfying increasingly demanding test cases, this
type helps characterize how silent failures manifest in the ob-   gap between functional adequacy and security correctness
served corpus. Second, each axial category was concentrated       may widen rather than narrow.
in a characteristic code location: Omission concentrates in            The two prominent open codes reflect different rea-
API calls, Inadequacy in input handling, and Introduction         soning gaps. At the axial level, the cases concentrate in
in configuration artifacts. This separation is consistent with    a small part of the taxonomy: among the ten open codes,
the taxonomy dimensions capturing distinct aspects of the         the two prominent codes, Insecure API Preserved (42) and
failure phenomenon. Finally, severity does not follow a           Weak Mitigation (36), together account for nearly half of
simple gradient across the three categories; instead, Inade-      the corpus (78/170, 45.9%). This concentration suggests that
quacy is associated with the highest exploitation risk despite    security-compliance decoupling is driven by a few recurring
representing attempted rather than absent defenses.               failure mechanisms rather than by many isolated factors.
                                                                       Of the two, Insecure API Preserved is the more prevalent
    Key Findings from RQ3                                         (42 cases) and illustrates the decoupling in its most direct
                                                                  form: the agent completes the functional task while leaving
    We found that different vulnerability contexts are as-
                                                                  in place a dangerous API call that was already present in the
    sociated with different types of silent failures in our
                                                                  input context. One plausible explanation is insecure pattern
    corpus. API-substitution vulnerabilities are predom-
                                                                  reproduction: the agent appears to treat the surrounding code
    inantly associated with Omission, logic-intensive
                                                                  as authoritative and edits around the insecure call rather
    vulnerabilities with Inadequacy, and vulnerabilities
                                                                  than replacing it, particularly when that call is not the direct
    introduced during repair with Introduction. Among
                                                                  subject of a failing test. As a result, the inherited insecure
    these categories, Inadequacy exhibits the highest
                                                                  construct remains in the repaired code, even though the task
    estimated exploitability risk. These results indicate
                                                                  itself calls for a security fix.
    that CWE family and code location help characterize
                                                                       Weak Mitigation, by contrast, reflects a different dy-
    the types of silent failures observed in this study.
                                                                  namic, an attempted but incomplete defense. In our taxon-
                                                                  omy, Weak Mitigation is the sole open code under Inade-
                                                                  quacy, and among the recurring open codes it has the highest
4. Discussion                                                     mean exploitability score (L3 = 17.7), which challenges the
    This section discusses the key findings for each research     intuition that any defense is better than none. A plausible
question and outlines their implications for research and         reading is that this gap lies between recognizing a vulnera-
practice. It examines why patches that pass functional val-       bility and implementing a robust defense: producing a partial
idation can remain insecure (RQ1), why current evaluation         defense requires the agent to recognize the vulnerability
and review practices do not surface these cases (RQ2), and        class, but not necessarily to reason about the conditions
how the observed failure patterns can inform more targeted        under which the defense actually holds. For example, the
verification (RQ3).                                               agent may recognize that an input should be constrained, yet
                                                                  implement a check that known bypass strategies can evade.
4.1. Security-Compliance Decoupling as a Distinct                 Consequently, such a visible control can create an appear-
     Failure Phenomenon (RQ1)                                     ance of safety that the underlying code does not support.
    Silent failures as a structurally distinct class of de-            The remaining open codes further indicate when the
fects. The security-compliance decoupling we identified in        dominant mechanisms change. Missing Mitigation appears
our results (see Section 3.1) is structurally distinct from       when the required security control must be inferred from
conventional software defects. In an ordinary bug, the code       task intent rather than substituted from the input, which
fails to produce expected behavior, and this failure is in        is more demanding than replacing a visibly unsafe API.
principle detectable through functional testing. In a silent      Deployment Context Risk and Unsafe Default Retained sug-
failure, by contrast, the code not only runs but produces the     gest that agents tend to treat deployment assumptions as
expected result; the deficiency lies in a non-functional di-      peripheral rather than as part of the repair obligation, while
mension, namely the security property of the output, that the     Hardcoded Secret points to a related tendency to produce
evaluation oracle was not designed to assess. This distinction    runnable examples rather than production-safe security ar-
matters because it implies that silent failures are unlikely      tifacts. Missing Sanitization and Ambiguous Repair Intent
to be eliminated by improving test coverage alone. Instead,       appear in only a few cases and mark boundary conditions
they appear to require evaluation criteria that extend beyond     rather than recurring mechanisms. Taken together, these
functional correctness into security semantics.                   lower-frequency codes suggest that future agent design may
    This observation aligns with a long-standing finding in       need to distinguish API-substitution tasks from tasks that
automated program repair, namely that plausible patches are

: Preprint submitted to Elsevier                                                                                   Page 14 of 22
instead require new security reasoning, deployment-context          4.2. Why Current Assurance Pipelines Miss Silent
reasoning, or secure-default generation.                                 Failures (RQ2)
     These two dominant mechanisms are consistent with                  Current evaluation paradigms may leave security-
prior evidence on the structural limitations of LLMs. The           relevant gaps. Industry-standard benchmarks such as SWE-
tendency to preserve insecure context aligns with reported          bench [13] and HumanEval [14] treat test-passing as the
difficulties of agentic systems in reliably interpreting user       primary success criterion. Under these criteria, every con-
intent [34, 35]: the observed behavior is consistent with           firmed case in our corpus would have been classified as a
satisfying the literal task while failing to address its broader    successful repair. This does not diminish the value of func-
security purpose. Likewise, the incompleteness of attempted         tional benchmarks as operational baselines, but it suggests
defenses aligns with evidence that LLM-based vulnerability          that benchmark-reported success rates for security-sensitive
repair depends on context when applied to real-world vulner-        tasks may overestimate actual repair quality. Complement-
abilities [36], and with the long-standing automated program        ing functional checks with security-oriented verification ap-
repair finding that a test-passing patch may mask rather than       pears necessary to surface deficiencies that tests alone were
resolve the underlying defect [1].                                  not designed to capture. This concern is consistent with re-
     Different decoupling modes may call for different              cent APR surveys, which note that current benchmarks offer
remediation strategies. The three axial categories appear           few metrics for vulnerabilities introduced during repair [38].
to represent qualitatively different points at which the de-            Failures often originate early and survive to the fi-
coupling occurs. Omission involves a gap between under-             nal patch. The propagation analysis suggests that reviewer
standing the task and selecting an appropriate API or control.      failure is only one part of a broader chain-level problem.
Inadequacy involves a gap between identifying the security          In many cases, the deficiency originated upstream and then
requirement and implementing a complete defense. Intro-             passed through subsequent roles without security-focused
duction involves a gap between addressing the primary task          re-evaluation. Although reviewer agents rarely intercepted
and managing the security context of all generated artifacts.       confirmed deficiencies in our corpus, treating this solely as
The heterogeneity of these failure modes is consistent with         a reviewer limitation would understate the role of earlier
the MAST taxonomy, which likewise finds that failures in            pipeline stages, because the deficiency was already present
multi-agent systems fall into qualitatively distinct categories     before review, and later roles tended to assess task progress
rather than a single defect type [11]. In the verification liter-   rather than reconsider the security adequacy of prior de-
ature, hybrid pipelines that combine LLM-based generation           cisions. A plausible interpretation is that agent handoffs
with static analysis or formal methods [20, 37] similarly           preserve functional intent more reliably than security intent:
indicate that a single class of checks may not be sufficient        once a security control is omitted or weakened at design or
for all deficiency types. If these distinctions hold, no single     implementation time, subsequent roles rarely reconstruct the
mitigation strategy would suffice: Omission may respond to          missing requirement in our cases.
API substitution rules or secure-by-default libraries; Inad-            This lifecycle pattern relates closely to prior work on fail-
equacy may require deeper security reasoning or defense             ure dynamics in multi-agent systems. Studies of cascading
completeness verification; Introduction may require extend-         failures and problem drift describe how errors compound
ing the verification boundary to all artifacts generated during     across interaction steps [39], and attribution frameworks
the repair, rather than only the prompted target.                   such as AgenTracer localize fault-inducing steps within
     Implications. Taken together, these results suggest that       agent trajectories [18]. These approaches, however, share a
security deficiencies should not be treated as a monolithic         common limitation: they often assume an observable failure
category, and that verification pipelines may benefit from          signal, such as an explicit error or a failing test, to define
mode-specific checks matched to the expected failure profile        and trace the fault. Our propagation analysis, by contrast,
of a given task. For researchers, the dominance of a single,        suggests that similar cross-step dynamics can also arise
mechanically simple code indicates that a substantial por-          when no such signal is present. This extends the study of
tion of silent failures may be addressable through targeted,        multi-agent failure to latent deficiencies that remain invisible
rule-based interventions, while the risk concentration in           to functional evaluation.
Weak Mitigation points to completeness-oriented verifica-               Convergence patterns are consistent with shared ex-
tion, such as differential testing against known bypasses,          perimental factors, while failure profiles differ across
as a priority for evaluation. For agent developers, safe-           architectures. Convergence is a common pattern in our cor-
API substitution rules or curated secure-default mappings,          pus: 107 of the 170 confirmed failures fall within convergent
applied before a patch is accepted, could remove a large            cases, in which 26 tasks triggered comparable failures across
share of the most common failures. For security engineers,          three or more frameworks. Since the frameworks differ in
agent-generated controls should be evaluated for complete-          orchestration and coordination architecture, this recurrence
ness against known bypass techniques, not merely for pres-          is consistent with shared factors across the experimental
ence, because a bypassable defense can lead downstream              setup, including the base model, prompt content, task design,
reviewers to assume that the issue has been closed and may          and recurring vulnerability patterns. This reading is further
therefore carry greater practical risk than an absent one.          supported by the earlier observation that agents across the
                                                                    examined architectures tended to reproduce insecure APIs

: Preprint submitted to Elsevier                                                                                      Page 15 of 22
present in the task context. We do not, however, attribute the   a newly introduced weakness often appears in configuration
convergence to the model alone: because our design fixes         or auxiliary artifacts generated by the pipeline. Both asso-
the base model and varies the frameworks, it cannot sepa-        ciations are consistent with prior evidence that LLM-based
rate model-level effects from shared factors such as prompt      repair performs more reliably on well-specified, pattern-like
content, dataset characteristics, and recurring vulnerability    fixes than on vulnerabilities whose correct handling depends
patterns.                                                        on context [36].
     Architecture is nevertheless associated with differences         Multi-agent pipelines can introduce vulnerabilities
in how these failures manifest. The orchestration of each        outside the originally targeted patch scope. The co-
system appears to be associated with how shared failure          occurrence of multi-agent architecture, the Introduction
patterns surface in the generated artifacts: multi-agent sys-    category, and configuration-level locations is one of the
tems, which involve more inter-agent interaction and addi-       more distinctive patterns in our data. During execution,
tional artifact generation, exhibited more Introduction fail-    multi-agent frameworks may emit scaffolding beyond the
ures, whereas single-agent systems exhibited more Inad-          requested patch, such as build files, container definitions,
equacy failures, consistent with attempted but incomplete        runtime settings, and other auxiliary artifacts. These artifacts
defenses.                                                        can contain weaknesses that were absent from the original
     This pattern extends prior evidence on the reliability      task. Two factors make such weaknesses difficult to detect:
of LLM-based repair. Earlier work reports that weaknesses        they are not the explicit target of the prompt, so functional
recur across prompts and scenarios rather than as isolated,      tests may not exercise them, and pipeline roles are typically
framework-specific errors [36]; our results carry this ob-       not assigned to review every generated artifact for security.
servation from individual models to agentic repair systems.      Existing failure taxonomies for multi-agent systems [11] and
They suggest that, as long as these recurring security lim-      vulnerability classifications such as CWE help characterize
itations remain unaddressed, similar insecure behavior can       failures or vulnerabilities once they are observed, but they
recur even under different coordination mechanisms.              do not address the possibility that the analysis boundary
     Implications. These findings imply that security assur-     itself may be too narrow. Our results extend this picture by
ance for agentic repair should be evaluated and designed         showing that the set of security-relevant artifacts can grow
beyond functional pass rates. For benchmark designers,           with pipeline complexity.
security-oriented criteria need to be reported alongside              Silent failures are not confined to low-severity issues.
functional outcomes so that test-passing is not mistaken for     The severity distribution shows that security-compliance
successful security repair. For system designers, assurance      decoupling is not limited to minor weaknesses: 22 of the
mechanisms should move upstream: because silent failures         170 confirmed cases were rated as critical severity, yet they
can originate during planning, design, or implementation         remained undetected by functional testing in the same way
and persist through subsequent handoffs, tool-supported          as lower-severity cases. This result indicates that functional
checks should be deployed where defects first arise rather       success does not provide a severity-sensitive assurance sig-
than only at the final review stage. For researchers, the        nal, because a patch may pass all available tests while
convergent subset identified in this study offers a useful       still preserving or introducing high-impact vulnerabilities.
basis for controlled experiments that vary base models under     This observation aligns with arguments in the verification
fixed architectures, or architectures under fixed models, to     literature for security-oriented test suites that assess repairs
separate model-level vulnerabilities from architecture-level     beyond functional correctness [19, 40].
effects.                                                              Implications. For practitioners, the family and location
                                                                 associations indicate that verification effort can be routed
4.3. Structured Failure Patterns as a Basis for                  rather than applied uniformly: rule-based API checks at
     Targeted Verification (RQ3)                                 call sites for API-substitution families, deeper logic analysis
    Vulnerability family and code location jointly indi-         on input-handling code for logic-intensive families, and
cate the expected failure category. The observed asso-           scanning that covers generated configuration and auxiliary
ciation between CWE family and axial category suggests           artifacts for newly introduced vulnerability types. Moreover,
that vulnerability type may help anticipate the type of silent   because multi-agent pipelines can introduce weaknesses out-
failure an agent is likely to produce. API-substitution vul-     side the prompted target, vulnerability analysis of agent
nerabilities were predominantly associated with Omission;        output should enumerate and scan every artifact the pipeline
logic-intensive vulnerabilities with Inadequacy; and vulner-     produces, rather than only the file or component named in
abilities introduced during repair with Introduction.            the task prompt. For reviewers, the presence of critical-
    A parallel pattern appears at the level of code location:    severity cases among silent failures argues against taking a
Omission is concentrated in API calls, Inadequacy in input-      passing test suite as evidence of a secure repair or of accept-
handling logic, and Introduction in configuration artifacts.     able residual risk; independent security verification should
A plausible explanation is that each category’s gap surfaces     therefore precede any decision to trust an agent-generated
where its work happens. An unsubstituted dangerous call          patch. For researchers, how the set of at-risk artifacts scales
remains visible at the call site; an incomplete defense ap-      with pipeline complexity remains unquantified and could
pears in the input-handling code intended to enforce it; and


: Preprint submitted to Elsevier                                                                                  Page 16 of 22
be measured directly or through iterative re-analysis of the       Because originator attribution was derived from qualitative
patched code.                                                      trace analysis, alternative interpretations of complex agent
                                                                   interactions could lead to different role assignments. This
                                                                   threat may influence the reported originator distributions and
5. Threats to Validity                                             the propagation-chain frequencies. To mitigate this threat,
    We organize threats to validity following the standard         we relied on observable trace evidence, predefined coding
validity categories in empirical software engineering [41].        rules, and consensus-based discussion of ambiguous cases.
                                                                       A related threat concerns the classification of propa-
5.1. Construct Validity                                            gation patterns. Patterns such as planning-stage omission,
    Our operational definition identifies silent failures as       design-originated omission, design-originated introduction,
patches that satisfy both syntactic and functional verification    and implementation-originated failure were derived through
yet are flagged by static security analysis or exploitabil-        qualitative analysis of the traces, and some cases could
ity assessment. This definition focuses on security-relevant       reasonably be assigned to more than one pattern, especially
silent failures. Silent failures involving performance, pri-       when underspecified requirements and implementation-level
vacy, maintainability, usability, reliability under load, or       omissions occurred in the same trace. Because the fre-
other non-security qualities are outside the scope of this         quency of each pattern feeds into our findings, ambiguous
study, and our counts should not be read as estimates of           assignments could shift the reported pattern distribution. To
failures in those dimensions. Similarly, security properties       reduce this threat, we recorded the trace evidence behind
requiring dynamic analysis, runtime monitoring, environ-           each assignment, compared each newly coded case against
mental configuration, or domain-specific knowledge may not         earlier cases in the same pattern to limit category drift, and
be captured by our verification framework.                         discussed boundary cases jointly before assigning a single
    Our taxonomy was derived from all 170 confirmed cases,         final pattern.
which include 39 (22.9%) classified as Partial alongside               The L3 exploitability score is a verification level separate
131 (77.1%) true positives. Including Partial cases may            from L2. It relies on predefined signal weights, bounded
affect precision, because a Partial verdict reflects less direct   safe-practice discounts, and a fixed candidate threshold (see
evidence of exploitability than a true-positive verdict. As a      Section 2.4.2). The fixed threshold therefore affects which
sensitivity check, we re-examined the taxonomy using only          cases are judged as silent failure candidates. For example,
the 131 true positives. All three axial categories and seven       a true silent failure scoring below the threshold would not
of the ten open codes remain represented in this subset. The       enter manual review and would be missed. The score mag-
three omitted codes occurred only as Partial cases: Deploy-        nitude, in turn, affects the reported exploitability patterns,
ment Context Risk (9 cases), Ambiguous Repair Intent (1            so the weighting and discount choices, together with any
case), and Vulnerable Test Code (1 case). This is expected,        imprecision in the pattern matching of sources and sinks,
since their exploitability could not be confirmed from static      contribute to these patterns and to the results that build on
evidence alone, which is the same property that placed them        them.
in the Partial category. Although this restriction reduced             To reduce this threat, every candidate above the thresh-
counts across all three categories, the main taxonomy struc-       old was manually reviewed before confirmation, so the
ture remained stable.                                              threshold acts as a screening sensitivity parameter rather
    The distinction between Omission and Inadequacy de-            than a final classification boundary, and over-inclusion
pends on whether the agent made any attempt at mitigation.         at screening is removed by review. We also applied the
Because the two categories are reported separately, mis-           same scoring procedure uniformly across all frameworks,
classifying boundary cases would shift their relative sizes.       so comparative claims rely on the ordering of scores rather
We used any observable mitigation attempt in the trace as          than their absolute values.
the deciding criterion and resolved the small number of
boundary cases through discussion between coders.                  5.3. External Validity
                                                                        Both datasets are Python-focused and may not represent
5.2. Internal Validity                                             the full diversity of security-sensitive repair tasks encoun-
    The L2 verification level relies on Bandit, which is           tered in practice. Tasks involving multi-file repositories,
subject to both false positives and false negatives. False         complex dependency chains, or language-specific security
positives were addressed through manual review, which              idioms are underrepresented. We therefore limit our claims
excluded 82 candidates from the confirmed corpus. False            to Python repair tasks, and do not generalize to other lan-
negatives are inherently difficult to quantify; the confirmed      guages or to repository-scale repair.
corpus should be interpreted as a conservative estimate of              The seven frameworks (four multi-agent, three single-
the silent failures detectable by our multi-level verification     agent) span a range of coordination architectures, but the
framework (see Section 2.4.2), not as an estimate of all           landscape of agent systems is evolving rapidly. Our sample
possible silent failures in agentic code repair.                   of seven frameworks may therefore not generalize to propri-
    Attributing a silent failure to a specific agent role and      etary systems. Despite this architectural diversity, because
pipeline stage requires interpretive judgment, particularly        all frameworks were instantiated using GPT-4o-mini, some
where role boundaries are ambiguous in multi-agent traces.

: Preprint submitted to Elsevier                                                                                    Page 17 of 22
observed failure patterns may reflect characteristics of the     Web of Science, and SpringerLink. To the best of our knowl-
underlying model rather than the framework architecture          edge, we found no prior work that traces how patches that
itself. The cross-framework convergence we observed sharp-       pass available functional checks but remain insecure orig-
ens this concern: it is consistent with shared model-related     inate in agent roles and propagate through agentic repair
factors, but it may also be influenced by prompt templates,      pipelines. We discuss the existing research in four cat-
the characteristics of the two benchmarks, the structure of      egories: (i) benchmark-based evaluation of LLM agents
the repair tasks, recurring vulnerability patterns, or other     (Section 6.1), (ii) failure analysis in multi-agent systems
experimental factors. We therefore treat the source of this      (Section 6.2), (iii) the plausible-versus-correct distinction
convergence as an open question rather than evidence of a        in APR (Section 6.3), and (iv) security verification of gen-
single cause, and we cannot fully separate model-specific        erated repairs (Section 6.4). A concluding summary and
effects from framework-specific ones. Future studies should      comparative analysis (Section 6.5) position the present study
replicate the analysis using additional foundation models.       at the intersection of these lines and justify its scope and
                                                                 contributions.
5.4. Conclusion Validity
    Conclusion validity concerns whether our results pro-        6.1. Benchmark-Based Evaluation of LLM Agents
vide support for the conclusions we draw. In this study,             Evaluation of LLM-based agentic systems is often driven
the analysis is primarily qualitative and descriptive, so the    by benchmarks. SWE-bench has become a widely used
conclusions are based on repeated patterns and frequency         benchmark for assessing automated repair, with related ef-
distributions within the confirmed corpus. Several design        forts adopting similar outcome-focused metrics that measure
choices support these conclusions. First, all cases were         whether a generated patch passes existing unit tests [13, 42,
processed through the same multi-level verification and          43]. These metrics provide a useful operational baseline,
manual review procedure before entering the confirmed            but they treat a passing result as success without assessing
corpus. Second, each confirmed case was assigned to one          whether the generated patch satisfies the security intent of
dominant axial category, which makes the category-level          the repair task. As a result, a patch that passes existing tests
distributions mutually exclusive. Third, the coding criteria     may still preserve the vulnerable behavior in the original
were applied consistently across iterations, with boundary       code. Outcome-level evaluations therefore offer limited
cases discussed before final assignment. Lastly, comparisons     insight into failure mechanisms or non-functional properties
across frameworks are based on executions conducted under        of the output. Beyond these outcome metrics, researchers de-
a shared model configuration, timeout, and verification          ploying agentic systems in increasingly complex workflows
pipeline. These choices reduce threats to conclusion validity.   have begun examining broader limitations such as misalign-
The reported counts are still corpus-dependent, and small        ment, coordination breakdowns, and difficulty in reliably
differences between adjacent categories, frameworks, or          interpreting user intent [34, 35, 44]. These perspectives have
open codes should not be interpreted as stable rankings.         helped frame the challenge landscape but remain primarily
We therefore report raw counts together with percentages,        qualitative, with limited empirical analysis of specific failure
describe the results as patterns observed in our corpus, and     patterns.
avoid drawing causal or population-level conclusions from
descriptive differences alone.                                   6.2. Failure Analysis in Multi-Agent Systems
                                                                     A growing body of work has moved toward empirical
5.5. Reliability                                                 failure analysis in multi-agent systems. Agentic systems vary
    Qualitative coding was performed by the first author         in architecture, including single-agent and multi-agent de-
across all three iterations. A random sample of 35 cases was     signs with different role structures and coordination patterns,
independently coded by another author, yielding a composite      which may influence where failures appear [45]. The MAST
Cohen’s 𝜅 of 0.71. This composite requires agreement on          taxonomy provides a systematic categorization of observ-
both the manual review label (TP, PARTIAL, or FP) and            able failure modes [11], while complementary work has
the axial category (Omission, Inadequacy, or Introduction),      formalized dynamics such as cascading failures and problem
with per-dimension values of 0.63 and 0.66 respectively; the     drift at the system level [39, 46, 47]. These efforts character-
procedure is detailed in Section 2.5.3. Disagreements were       ize failures that surface as errors or task non-completion, but
resolved through structured consensus discussion.                they do not address failures that give no such outward indi-
    The verification pipeline is deterministic given the same    cation. Attribution frameworks have advanced toward more
input. Framework execution involves stochastic LLM infer-        granular diagnosis: Who&When and AgenTracer introduced
ence, meaning that exact trace reproduction is not guaran-       fine-grained annotation and counterfactual replay to identify
teed.                                                            fault-inducing steps within complex trajectories [17, 18].
                                                                 Their localization, however, depends on an observable fail-
                                                                 ure signal to define the fault being traced. Beyond diag-
6. Related Work                                                  nosis, resilience mechanisms such as challenger roles and
    To reduce the risk of overlooking relevant studies, we       courtroom-inspired inter-agent debate have been proposed to
searched seven major digital libraries: Google Scholar, IEEE     improve reliability [48, 49]. These approaches demonstrate
Xplore, the ACM Digital Library, ScienceDirect, Scopus,          the potential of role-based specialization, though they rely

: Preprint submitted to Elsevier                                                                                  Page 18 of 22
      Table 10
      Positioning of representative prior work relative to the present study. Y = explicitly addressed; P = partially addressed; – = not
      a primary focus.
      Representative work                 Bench.   Taxon.   Prop.   Role attr.   Sec. verif.   Silent fail.   Main gap relative to this study

      Outcome benchmarks         (e.g.,     Y        –       –          –            –              –         Evaluate whether patches pass existing tests,
      SWE-bench) [13]                                                                                         but do not assess security-semantic correct-
                                                                                                              ness or explain latent security failures.

      Multi-agent failure taxonomies        P        Y       P          –            –              –         Characterize observable multi-agent failures,
      (e.g., MAST) [11]                                                                                       but do not cover failures that leave no ex-
                                                                                                              ternal signal such as a crash, error, or failed
                                                                                                              task.

      Trajectory attribution frame-         –        –       Y          Y            –              –         Localize fault-inducing steps in agent trajec-
      works (e.g., AgenTracer) [17,                                                                           tories, but require an observable failure signal
      18]                                                                                                     to define what should be traced.

      APR      plausible-versus-correct     P        P       –          –            P              P         Establish that test-passing patches may be
      studies [1, 38, 50]                                                                                     incorrect, but do not analyze security-specific
                                                                                                              silent failures in role-based agentic repair
                                                                                                              pipelines.

      LLM security repair and verifica-     P        –       –          –            Y              P         Assess the security of generated repairs at
      tion [20, 27, 36, 51, 52]                                                                               the artifact level, but do not explain how
                                                                                                              deficiencies originate, propagate, or evade
                                                                                                              review across agent roles.

      This study                            Y        Y       Y          Y            Y              Y         Provides an empirical taxonomy of silent
                                                                                                              failures, analyzes their role-level origins and
                                                                                                              propagation chains, and verifies security de-
                                                                                                              ficiencies that remain hidden after syntactic
                                                                                                              and functional success.

       Dimensions. Bench.: benchmark-based evaluation of repair outcomes; Taxon.: classification of failure types; Prop.: how failures
      propagate across pipeline stages; Role attr.: attribution of a failure to a specific agent role; Sec. verif.: verification of the security
      of generated code beyond functional correctness; Silent fail.: coverage of failures that pass syntactic and functional checks yet
      retain or introduce a vulnerability.


predominantly on explicit failure signals such as crashes,                        do not observe: the generated patch passes syntactic and
error messages, or task non-completion. Failures that do not                      functional validation, but still leaves the target vulnerability
produce such signals remain largely outside their scope. This                     unaddressed or introduces a new one. This security-oriented
gap motivates the present study.                                                  reading of plausibility has begun to appear in repair eval-
                                                                                  uations: when a patch is counted as plausibly fixed once it
6.3. APR and the Plausible-versus-Correct                                         passes the project test cases, neural and LLM-based repair
     Distinction                                                                  models still fail to address many vulnerability types, includ-
    While the preceding work examines failure dynamics                            ing cryptographic and request-handling weaknesses [50].
within agentic pipelines, the failures themselves ultimately                      Such cases show that test passage and security correctness
materialize in repair artifacts whose quality must also be                        can diverge even when the repair target is a known vulner-
assessed against established standards in Automated Pro-                          ability. This limitation is also reflected in LLM-based vul-
gram Repair (APR) and software security. A central concern                        nerability repair, where prior evaluations show that models
in APR is the distinction between plausible and correct                           perform reasonably well in controlled settings but remain
patches. A plausible patch passes all tests in the validation                     unreliable when applied to real-world vulnerabilities [36].
suite yet may not correct the defect, and can eliminate                           However, these studies primarily evaluate individual patches
desirable functionality or even introduce new security vul-                       generated by off-the-shelf models and do not examine how
nerabilities [1]. Recent APR surveys characterize the field                       such deficiencies arise and propagate across the roles of a
as having evolved from template-based and constraint-based                        multi-agent repair pipeline. Our study addresses this gap.
repair methods to machine learning, deep learning, and more
recently large-language-model-based approaches [27, 38].                          6.4. Security Verification of Generated Repairs
In this evaluation-driven setting, the security of the resulting                      A separate line of work addresses this gap through
patches has received comparatively limited attention, and                         security-oriented verification. Established security test suites
current benchmarks offer few metrics for vulnerabilities                          have been used for assessment beyond functional correct-
introduced during repair [38].                                                    ness [19, 40], while hybrid pipelines combine LLM-based
    This distinction is the conceptual basis for the silent                       generation with formal verification or static analysis [20,
failures we study, narrowed to the security setting. In APR,                      37]. In industrial practice, such verification is increasingly
the plausibility gap concerns whether a test-passing patch                        embedded in CI/CD pipelines [53]. Even where such ver-
actually fixes the target defect. In our setting, the gap con-                    ification is applied, however, generated fixes can satisfy
cerns a security property that the available functional tests                     the surface checks while leaving the underlying weakness

: Preprint submitted to Elsevier                                                                                                                   Page 19 of 22
in place; in infrastructure-as-code repair, for instance, a       code locations. Based on the analysis of the results, the key
notable share of LLM-generated fixes passed configuration         findings of this study are as follows:
checks yet did not resolve the security issue and escaped
scanner detection [52]. This indicates that artifact-level           • Our results show that silent failures should be treated
verification reduces, but does not remove, the risk of security        as a separate form of security-compliance decoupling
deficiencies that survive functional and tool-based checks.            rather than as ordinary functional defects alone. The
Adversarial evaluation sharpens this point: under systematic           confirmed cases support a three-part structure consist-
bypass testing, AI-generated patches were found to rely                ing of Omission, Inadequacy, and Introduction.
on minimalistic input validation and to remain exploitable           • We also observed that current assurance pipelines
through simple attack techniques, in contrast to the more              centered on test passage and LLM-based review were
structural corrections in human-written patches [51]. These            insufficient to detect these failures. At the same time,
approaches assess the security of a patch as a finished arti-          the recurrence of similar insecure solutions across
fact, but they do not model how the deficiency arose within            frameworks is consistent with shared factors in the ex-
the repair process, nor which role in a multi-agent pipeline           perimental setup, including the base model, prompts,
produced it. As a result, security verification and multi-agent        tasks, and vulnerability patterns, alongside differences
repair remain insufficiently connected, with no account of             in how failures appear across agent architectures.
how a vulnerability passes through agent interactions and
evades review.                                                       • Our results show that silent failures exhibit recurring
                                                                       patterns across vulnerability families, code locations,
6.5. Conclusive Summary                                                and generated artifact types in our corpus. These
    These complementary lines of work have each advanced               patterns suggest that security assurance for agentic
substantially but remain only partially connected. Bench-              repair should move toward targeted verification that
mark studies treat test success as the primary quality indi-           covers the full repair scope rather than general post
cator and do not examine the security semantics of a passing           hoc inspection.
patch. Failure-analysis studies focus on breakdowns that
surface as explicit signals and do not account for outputs            These findings have implications for both research and
that appear correct yet contain latent vulnerabilities. APR       practice. For research, they suggest that success in agentic
research establishes the distinction between plausible and        repair should no longer be defined solely by whether code
correct patches, and recent work shows that LLM-based             compiles and passes tests. Future benchmarks and evalua-
security repair remains unreliable, but it analyzes individual    tion protocols should assess both functional validation and
patches rather than the roles that produce them. Security-        security-semantic correctness, and should examine base-
verification studies assess patch quality at the artifact level   model effects and orchestration effects through controlled
without modeling how the internal role interactions of a          experimental designs. For practice, they indicate the need
multi-agent pipeline contributed to the deficiency. What          to extend verification beyond the primary patched file to all
remains unaddressed is the intersection of these concerns:        generated artifacts and to augment reviewer roles with tool-
how patches that pass functional evaluation yet preserve or       backed security checks.
introduce exploitable vulnerabilities originate within agent          Future work should replicate these findings across mod-
role structures, propagate through pipeline stages, and evade     els, languages, and tool-supported agent designs, and test
review mechanisms. The present study targets this inter-          whether targeted verification strategies meaningfully reduce
section. Table 10 positions our study against representative      silent failure rates in deployment settings. Another direc-
prior work along these dimensions and illustrates that the        tion is to examine agent execution traces to better explain
representative prior work considered here does not jointly        how these silent failures arise, including where security
address agent-role attribution, propagation, security verifi-     considerations are weakened or dropped during the repair
cation, and silent-failure coverage.                              pipeline. This line of work may help shift assurance from
                                                                  post hoc detection toward earlier intervention before patches
                                                                  are accepted.
7. Conclusion
    We present an empirical study of silent failures in LLM-
based agentic code repair. To investigate this phenomenon,        CRediT authorship contribution statement
we analyzed 170 confirmed silent failure cases identified             Wenji Bai: Conceptualization, Methodology, Software,
from 1,030 valid execution traces produced by seven agent         Formal analysis, Investigation, Data curation, Writing - orig-
frameworks across two security-focused datasets. The pri-         inal draft, Visualization. Muhammad Waseem: Concep-
mary contribution of this study is an empirical character-        tualization, Methodology, Validation, Review, Editing, Su-
ization of these failures along three dimensions: a three-        pervision, Project administration. Zeeshan Rasheed: For-
part taxonomy (Omission, Inadequacy, and Introduction)            mal analysis, Investigation. Jaakko Peltonen: Validation,
grounded in confirmed cases, an account of how they propa-        Review, Editing, Supervision. Pekka Abrahamsson: Re-
gate through agent pipelines, and an analysis of how they         sources, Supervision, Review, Editing.
distribute across frameworks, vulnerability families, and

: Preprint submitted to Elsevier                                                                                 Page 20 of 22
Acknowledgments                                                                [12] Y. Zhang, H. Ruan, Z. Fan, A. Roychoudhury, Autocoderover: Au-
                                                                                    tonomous program improvement, in: Proceedings of the 33rd ACM
    This research is funded as part of Finland’s Ministry                           SIGSOFT International Symposium on Software Testing and Analy-
of Education and Culture’s Doctoral Education Pilot under                           sis (ISSTA), 2024, pp. 1592–1604.
Decision No. VN/3137/2024-OKM-6 (The Finnish Doctoral                          [13] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, K. R.
                                                                                    Narasimhan, SWE-bench: Can language models resolve real-world
Program Network in Artificial Intelligence, AI-DOC).
                                                                                    GitHub issues?, in: Proceedings of the 12th International Conference
                                                                                    on Learning Representations (ICLR), 2024.
                                                                               [14] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Ka-
Data availability                                                                   plan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al.,
    Link to our dataset is in the reference [21].                                   Evaluating large language models trained on code, arXiv preprint
                                                                                    arXiv:2107.03374 (2021).
                                                                               [15] S. Chen, Y. He, S. Jana, B. Ray, Red teaming program repair
Declaration of AI Assistance                                                        agents: When correct patches can hide vulnerabilities, arXiv preprint
                                                                                    arXiv:2509.25894 (2025).
    During the preparation of this work, the author(s) used                    [16] W. Wang, W. Ma, Q. Hu, Y. Zhang, J. Sun, B. Wu, Y. Liu, G. Xu,
ChatGPT to refine grammar, improve sentence structure,                              L. Jiang, VulnRepairEval: An exploit-based evaluation framework for
and resolve formatting issues. After utilizing this tool, the                       assessing large language model vulnerability repair capabilities, arXiv
author(s) thoroughly reviewed and edited the content as                             preprint arXiv:2509.03331 (2025).
                                                                               [17] S. Zhang, M. Yin, J. Zhang, J. Liu, Z. Han, J. Zhang, B. Li, C. Wang,
needed, taking full responsibility for the final publication.                       H. Wang, Y. Chen, Q. Wu, Which agent causes task failures and
                                                                                    when? on automated failure attribution of LLM multi-agent systems,
                                                                                    in: Proceedings of the 42nd International Conference on Machine
References                                                                          Learning (ICML), 2025.
 [1] Z. Qi, F. Long, S. Achour, M. Rinard, An analysis of patch plausibility   [18] G. Zhang, J. Wang, J. Chen, W. Zhou, K. Wang, S. Yan, AgenTracer:
     and correctness for generate-and-validate patch generation systems,            Who is inducing failure in the LLM agentic systems?, in: Proceedings
     in: Proceedings of the 2015 International Symposium on Software                of the 14th International Conference on Learning Representations
     Testing and Analysis (ISSTA), 2015, pp. 24–36.                                 (ICLR), 2026.
 [2] N. Perry, M. Srivastava, D. Kumar, D. Boneh, Do users write more          [19] E. Kuzmina, S. Pervez, S. E. Hosseini, M. Shahbaz, A. Akhunzada,
     insecure code with AI assistants?, in: Proceedings of the 2023 ACM             Spring framework benchmarking utility for static application security
     SIGSAC Conference on Computer and Communications Security                      testing (SAST) tools, IEEE Internet of Things Journal 12 (22) (2025)
     (CCS), 2023, pp. 2785–2799.                                                    46863–46877.
 [3] J. Peng, L. Cui, K. Huang, J. Yang, B. Ray, Cweval: Outcome-driven        [20] N. Tihanyi, T. Bisztray, M. A. Ferrag, B. Cherif, R. A. Dubniczky,
     evaluation on functionality and security of LLM code generation, in:           R. Jain, L. C. Cordeiro, Vulnerability detection: From formal verifi-
     2025 IEEE/ACM International Workshop on Large Language Models                  cation to large language models and hybrid approaches: A compre-
     for Code (LLM4Code), IEEE, 2025, pp. 33–40.                                    hensive overview, in: Adversarial Example Detection and Mitigation
 [4] J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. Narasimhan,           Using Machine Learning, Springer, 2026, pp. 33–47. doi:10.1007/
     O. Press, Swe-agent: Agent-computer interfaces enable automated                978-3-031-99447-0_3.
     software engineering, Advances in Neural Information Processing           [21] W. Bai, W. Muhammad, Z. Rasheed, J. Peltonen, P. Abrahamsson,
     Systems 37 (2024) 50528–50652.                                                 Dataset for the Paper: When Passing Tests Hides Vulnerabilities:
 [5] D. Chen, S. Lin, M. Zeng, D. Zan, J.-G. Wang, A. Cheshkov, J. Sun,             An Empirical Study of Silent Failures in Agentic Systems (2026).
     H. Yu, G. Dong, A. Aliev, et al., Coder: Issue resolving with multi-           doi:10.5281/zenodo.20831595.
     agent and task graphs, arXiv preprint arXiv:2406.01304 (2024).            [22] M. L. Siddiq, J. C. Santos, SecurityEval dataset: mining vulnera-
 [6] I. Bouzenia, P. Devanbu, M. Pradel, RepairAgent: An autonomous,                bility examples to evaluate machine learning-based code generation
     LLM-based agent for program repair, in: Proceedings of the                     techniques, in: Proceedings of the 1st International Workshop on
     IEEE/ACM 47th International Conference on Software Engineering                 Mining Software Repositories Applications for Privacy and Security
     (ICSE), 2025, pp. 2188–2200. doi:10.1109/ICSE55347.2025.00157.                 (MSR4P&S), 2022, pp. 29–33.
 [7] C. Qian, W. Liu, H. Liu, N. Chen, Y. Dang, J. Li, C. Yang, W. Chen,       [23] G. Bhandari, A. Naseer, L. Moonen, CVEfixes: automated collection
     Y. Su, X. Cong, et al., Chatdev: Communicative agents for software             of vulnerabilities and their fixes from open-source software, in: Pro-
     development, in: Proceedings of the 62nd Annual Meeting of the                 ceedings of the 17th International Conference on Predictive Models
     Association for Computational Linguistics (Volume 1: Long Papers),             and Data Analytics in Software Engineering (PROMISE), 2021, pp.
     2024, pp. 15174–15186.                                                         30–39.
 [8] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, J. Wang, C. Zhang,        [24] D. Huang, J. M. Zhang, M. Luck, Q. Bu, Y. Qing, H. Cui, Agentcoder:
     Z. Wang, S. K. S. Yau, Z. Lin, et al., MetaGPT: Meta programming               Multi-agent-based code generation with iterative testing and optimi-
     for a multi-agent collaborative framework, in: Proceedings of the 12th         sation, arXiv preprint arXiv:2312.13010 (2023).
     International Conference on Learning Representations (ICLR), 2024.        [25] P. Gauthier, Aider: AI pair programming in your terminal, https:
 [9] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,          //aider.chat, accessed: 2026-06-17 (2024).
     S. Zhang, J. Liu, et al., Autogen: Enabling next-gen LLM applications     [26] X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan,
     via multi-agent conversations, in: Proceedings of the 1st Conference           Y. Song, B. Li, J. Singh, H. H. Tran, F. Li, R. Ma, M. Zheng, B. Qian,
     on Language Modeling (COLM), 2024.                                             Y. Shao, N. Muennighoff, Y. Zhang, B. Hui, J. Lin, R. Brennan,
[10] C. S. Xia, Y. Deng, S. Dunn, L. Zhang, Demystifying LLM-based                  H. Peng, H. Ji, G. Neubig, OpenHands: An open platform for AI
     software engineering agents, Proceedings of the ACM on Software                software developers as generalist agents, in: Proceedings of the 13th
     Engineering 2 (FSE) (2025) 801–824. doi:10.1145/3715754.                       International Conference on Learning Representations (ICLR), 2025.
[11] M. Cemri, M. Z. Pan, S. Yang, L. A. Agrawal, B. Chopra, R. Tiwari,        [27] G. Dolcetti, V. Arceri, E. Iotti, S. Maffeis, A. Cortesi, E. Zaffanella,
     K. Keutzer, A. Parameswaran, D. Klein, K. Ramchandran, M. Za-                  Helping LLMs improve code generation using feedback from testing
     haria, J. E. Gonzalez, I. Stoica, Why do multi-agent LLM systems               and static analysis, Discover Artificial Intelligence 6 (1) (2026) 314.
     fail?, in: Proceedings of the 39th Conference on Neural Informa-          [28] K. M. MacQueen, E. McLellan, K. Kay, B. Milstein, Codebook
     tion Processing Systems Datasets and Benchmarks Track (NeurIPS),               development for team-based qualitative analysis, Cam Journal 10 (2)
     2025.

: Preprint submitted to Elsevier                                                                                                          Page 21 of 22
     (1998) 31–36.                                                                  in: Proceedings of the IEEE/ACM 48th International Conference on
[29] M. Q. Patton, Qualitative research & evaluation methods: Integrating           Software Engineering (ICSE), 2026.
     theory and practice, Sage publications, 2014.                             [50] Y. Wu, N. Jiang, H. V. Pham, T. Lutellier, J. Davis, L. Tan, P. Babkin,
[30] J. Corbin, A. Strauss, Basics of Qualitative Research: Techniques              S. Shah, How effective are neural networks for fixing security vulner-
     and Procedures for Developing Grounded Theory, 4th Edition, Sage               abilities, in: Proceedings of the 32nd ACM SIGSOFT International
     Publications, 2014.                                                            Symposium on Software Testing and Analysis (ISSTA), 2023, pp.
[31] K.-J. Stol, P. Ralph, B. Fitzgerald, Grounded theory in software               1282–1294.
     engineering research: a critical review and guidelines, in: Proceedings   [51] A. Mahmud, Y. Rawajfih, F. Wu, A systematic evaluation of AI-
     of the 38th International Conference on Software Engineering (ICSE),           generated security patches: Analyzing and exploiting AI-generated
     2016, pp. 120–131.                                                             fixes, in: 2025 IEEE International Conference on Artificial Intelli-
[32] B. Glaser, A. Strauss, Discovery of grounded theory: Strategies for            gence Testing (AITest), IEEE, 2025, pp. 224–231.
     qualitative research, Routledge, 2017.                                    [52] E. Low, C. Cheh, B. Chen, Repairing infrastructure-as-code using
[33] J. Cohen, A coefficient of agreement for nominal scales, Educational           large language models, in: 2024 IEEE Secure Development Confer-
     and Psychological Measurement 20 (1) (1960) 37–46.                             ence (SecDev), IEEE, 2024, pp. 20–27.
[34] S. Han, Q. Zhang, Y. Yao, W. Jin, Z. Xu, LLM multi-agent systems:         [53] R. Meliala, C. Lim, J. Andreas, Integrating security testing in CI/CD
     Challenges and open problems, arXiv preprint arXiv:2402.03578                  pipelines: Current trends from literature and market, in: Proceedings
     (2024).                                                                        of the 9th International Conference on Informatics and Computing
[35] G. Bansal, J. W. Vaughan, S. Amershi, E. Horvitz, A. Fourney,                  (ICIC), IEEE, 2024, pp. 1–6.
     H. Mozannar, V. Dibia, D. S. Weld, Challenges in human-agent
     communication, arXiv preprint arXiv:2412.10380 (2024).
[36] H. Pearce, B. Tan, B. Ahmad, R. Karri, B. Dolan-Gavitt, Examining
     zero-shot vulnerability repair with large language models, in: 2023
     IEEE Symposium on Security and Privacy (SP), IEEE, 2023, pp.
     2339–2356.
[37] G. Dolcetti, E. Iotti, A dual perspective review on large language
     models and code verification, Frontiers in Computer Science 7 (2025)
     1655469.
[38] M. Puvvadi, S. K. Arava, A. Santoria, S. S. P. Chennupati, H. V.
     Puvvadi, Coding agents: A comprehensive survey of automated bug
     fixing systems and benchmarks, in: 2025 IEEE 14th International
     Conference on Communication Systems and Network Technologies
     (CSNT), IEEE, 2025, pp. 680–686.
[39] P. Bisconti, M. Galisai, F. Pierucci, M. Bracale, M. Prandi, Beyond
     single-agent safety: A taxonomy of risks in LLM-to-LLM interac-
     tions, arXiv preprint arXiv:2512.02682 (2025).
[40] S. Kaniewski, F. Schmidt, M. Enzweiler, M. Menth, T. Heer, A
     systematic literature review on detecting software vulnerabilities with
     large language models, ACM Trans. Softw. Eng. Methodol. (May
     2026). doi:10.1145/3815425.
[41] C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell,
     A. Wesslén, et al., Experimentation in software engineering, Vol. 236,
     Springer, 2012.
[42] J.-L. Peng, S. Cheng, E. Diau, Y.-Y. Shih, P.-H. Chen, Y.-T. Lin,
     Y.-N. Chen, A survey of useful LLM evaluation, arXiv preprint
     arXiv:2406.00936 (2024).
[43] W. Wang, D. Zhang, T. Feng, B. Wang, J. Tang, Battleagentbench:
     A benchmark for evaluating cooperation and competition capabil-
     ities of language models in multi-agent systems, arXiv preprint
     arXiv:2408.15971 (2024).
[44] L. Hammond, A. Chan, J. Clifton, J. Hoelscher-Obermaier, A. Khan,
     E. McLean, C. Smith, W. Barfuss, J. Foerster, T. Gavenčiak,
     et al., Multi-agent risks from advanced AI, arXiv preprint
     arXiv:2502.14143 (2025).
[45] T. Masterman, S. Besen, M. Sawtell, A. Chao, The landscape of
     emerging AI agent architectures for reasoning, planning, and tool
     calling: A survey, arXiv preprint arXiv:2404.11584 (2024).
[46] A. Reid, S. O’Callaghan, L. Carroll, T. Caetano, Risk analysis tech-
     niques for governed LLM-based multi-agent systems, arXiv preprint
     arXiv:2508.05687 (2025).
[47] J. Becker, Multi-agent large language models for conversational task-
     solving, arXiv preprint arXiv:2410.22932 (2024).
[48] J. tse Huang, J. Zhou, T. Jin, X. Zhou, Z. Chen, W. Wang, Y. Yuan,
     M. Lyu, M. Sap, On the resilience of LLM-based multi-agent collab-
     oration with faulty agents, in: Proceedings of the 42nd International
     Conference on Machine Learning (ICML), 2025.
[49] R. Widyasari, M. Weyssow, I. C. Irsan, H. W. Ang, F. Liauw, E. L.
     Ouh, L. K. Shar, H. J. Kang, D. Lo, Let the trial begin: A mock-
     court approach to vulnerability detection using LLM-based agents,



: Preprint submitted to Elsevier                                                                                                         Page 22 of 22
