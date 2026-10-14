                                                                                                                                                                                         1




                                                 Enhancing Reliability in LLM-Based Secure Code Generation
                                             Mohammed F. Kharma, Mohammad Alkhanafseh, Ahmed Sabbah, David Mohaisen, Senior Member, IEEE



                                            Abstract—Large language models (LLMs) are widely used for                      The risks of LLM-generated code extend beyond isolated er-
                                         code generation, but their security reliability remains inconsistent           rors. Asare et al. demonstrated that current LLMs have notable
                                         across languages and prompting strategies. Existing prompt                     limitations in enforcing context-dependent security constraints,
                                         engineering improves functional correctness but rarely ensures
                                         consistent security outcomes. We introduce the Mitigation-Aware                often generating code that appears reliable in isolation but fails
                                         Chain-of-Thought (MA-CoT) framework, which embeds task-                        to satisfy system-level security requirements [12]. Ullah et al.
                                         specific CWE mitigation guidance and language-aware safe-                      reported similar findings via benchmark tests, showing that
                                         guards to reduce recurring vulnerabilities in generated code.                  even explicit prompts rarely enable models to consistently
arXiv:2605.24300v1 [cs.CR] 22 May 2026




                                         We evaluate MA-CoT across three LLMs (gpt-5, claude-4.5,                       identify or reason about vulnerabilities [13]. These results
                                         gemini-2.5), three programming languages (C, Java, Python),
                                         and four prompting strategies (Vanilla, Zero-shot, CoT, MA-                    indicate fundamental gaps in how LLMs represent and apply
                                         CoT) on a 200-task primary dataset, with external validation on                security knowledge during code generation, undermining the
                                         LLMSecEval. Using static analysis with expert validation, MA-                  overall reliability of generated software.
                                         CoT reduces total security findings from 92 to 39 (57.6%) on the                  Prompt engineering offers a method to steer model behavior
                                         primary dataset and from 73 to 4 (94.5%) on LLMSecEval. High-                  without retraining. Techniques such as zero-shot, few-shot
                                         severity findings (Blocker + Critical) drop from 90 to 39 (56.7%)
                                         and from 45 to 2 (95.6%), respectively. Across both datasets,                  prompting, and chain-of-thought (CoT) reasoning can im-
                                         MA-CoT is the only strategy that consistently improves security                prove functional correctness and logical consistency [14], [15].
                                         reliability; Zero-shot and CoT are less reliable and may increase              However, security and reliability considerations are mostly
                                         vulnerability, especially in C. We further introduce a strict lay-             incidental. Broad instructions like “write secure code” are too
                                         ered attribution of vulnerability drivers (language-core vs. stack             unspecific to consistently improve reliability, and they provide
                                         layers) and show that residual risk concentrates in hardening-
                                         oriented patterns (e.g., OS- and toolchain-dependent), motivating              limited guidance for mitigating concrete vulnerabilities [16].
                                         secure-by-construction primitives alongside prompting. Code and                   Our previous work [17] introduced the Weaknesses-Aware
                                         data are available at GitHub.                                                  Chain-of-Thought (WA-CoT) method, which mapped pro-
                                           Index Terms—reliability, dependability, robustness, secure code              gramming tasks to relevant Common Weakness Enumeration
                                         generation, LLM, mitigation framework                                          (CWE) entries and embedded them in prompt guidance to
                                                                                                                        inform the LLM of potential security flows. While promis-
                                                                                                                        ing, a broader evaluation revealed several reliability-related
                                                                   I. I NTRODUCTION                                     limitations: ① Information Overload. Large CWE catalogs
                                               ARGE language models (LLMs) are transforming soft-                       can increase, rather than reduce, failure occurrences [18].
                                         L     ware development by translating plain-language specifi-
                                         cations into functionally correct code [1]–[6]. Tools such as
                                                                                                                        ② Coarse-Grained Integration. Listing CWE identifiers and
                                                                                                                        descriptions without concrete remediation steps seldom trans-
                                         GitHub Copilot, OpenAI Codex, and Google Gemini are now                        lates into secure and reliable code. ③ Language Agnosticism.
                                         used daily by over 50% of developers, providing productivity                   Uniform treatment of all programming languages overlooks
                                         gains of 30–50% on routine programming tasks [7], [8].                         differences in type safety, memory management, and language-
                                            These efficiency gains are accompanied by concerns re-                      specific reliability risks. ④ Lack of Reasoning Support Without
                                         garding the reliability of LLM-generated code. Empirical                       Clear Mitigation. Models may recognize vulnerabilities in
                                         evidence indicates that code produced by LLMs frequently                       principle but fail to apply security logic during actual code
                                         contains security vulnerabilities, which can undermine sys-                    synthesis, compromising dependable code generation.
                                         tem dependability. For example, Pearce et al. found that                          Motivated by these observations, we design MA-CoT, a
                                         Copilot generated insecure implementations in roughly 40%                      prompt-based method that improves the reliability of LLM-
                                         of security-critical scenarios, including mismanaged buffer                    generated code while remaining lightweight enough for practi-
                                         boundaries, SQL queries, and cryptographic routines [9]. Fu                    cal deployment. MA-CoT embeds reliability-oriented reason-
                                         et al. observed similar vulnerability patterns in Python and                   ing directly into the code generation process through three
                                         C++, which persisted even as model size and training data                      components: mitigation-focused CWE integration, a baseline
                                         increased [10]. Sandoval et al. further showed that developers                 security ruleset, and language-aware prompting.
                                         often accept insecure suggestions without sufficient review,                      Rather than providing extensive vulnerability descriptions,
                                         particularly under time pressure, highlighting risks to the                    MA-CoT uses mitigation-focused CWE integration to ex-
                                         reliability and robustness of automated code generation [11].                  tract concise, actionable countermeasures from a structured
                                                                                                                        CWE mitigation knowledge base. For each programming task,
                                           M. Kharma, M. Alkhanafseh, A. Sabbah, and D. Mohaisen are with with          relevant security domains (e.g., cryptography, authentication,
                                         the Department of Computer Science, Birzeit University, Ramallah, Palestine.   input validation) are identified, and targeted safeguards are
                                         D. Mohaisen is also with the Department of Computer Science, University
                                         of Central Florida, Orlando, FL 32816 USA. E-mail: mohaisen@ucf.edu            incorporated into the prompt. For example, cryptographic op-
                                         (Corresponding author)                                                         erations trigger recommendations such as AES-256-GCM with
                                                                                                                                  2



AEAD guarantees, Argon2id key derivation with at least 128-             toolchain factors, providing actionable, layer-specific se-
bit salt, and nonce generation using a cryptographically secure         curity strengthening recommendations.
random number generator. This approach ensures consistent          Organization. Section II reviews the related work followed
reliability across tasks without introducing prompt overload.      by our methodology in section III, the dataset in section IV,
   MA-CoT further includes a baseline security ruleset, a          the results in section V, discussion in section VI, threat to
universal set of secure coding principles applied across all       validity in section VII, and concluding remarks and future
tasks regardless of language. These include strict input vali-     work in section VIII.
dation, robust error handling, safe memory management, and
defensive programming. Together, they provide a foundational                            II. R ELATED W ORK
reliability layer that reinforces dependable code generation          LLM-based code generation is now used in end-to-end
independently of prompt specifics.                                 development workflow. However, security outcomes remain
   Finally, MA-CoT employs a language-aware prompting              inconsistent across languages and prompt designs [9], [21]–
strategy. Vulnerabilities manifest differently across program-     [24]. Prior work [16], [25]–[34] has shown that prompting can
ming languages, so the system augments a language-agnostic         steer functional behavior, yet security improvements are often
checklist with language-specific safeguards. In C, emphasis is     inconsistent, model-dependent, and rarely driven by structured,
placed on pointer initialization, bounds checking, and explicit    task-specific mitigation knowledge.
memory clearing; in Python, the focus is input sanitization,          Prompt engineering has evolved into a systematic discipline
safe deserialization, and proper exception handling. This align-   for shaping model behavior without parameter updates. Sa-
ment improves reliability across diverse language contexts.        hoo et al. [25] surveyed 41 prompt engineering techniques
   A common source of confusion in language-aware secure           and highlighted the need for more application-centric prompt
generation is defining what constitutes a “language feature.”      designs and combined prompting approaches beyond general-
Many weaknesses arise not from the core language speci-            purpose ones. Chen et al. [26] systematized prompting meth-
fication but from the surrounding stack, including standard        ods and described how structural prompt changes (e.g., decom-
libraries, third-party APIs, OS interfaces, and toolchains. To     position and multi-step prompting programs) can alter model
avoid over-attribution and ensure actionable guidance, we          behavior. In the context of secure coding, another review of
adopt a strict layered framework that separates language-core      the literature [27] emphasizes that security flaws in LLM-
mechanisms from language-adjacent drivers, allowing us to          generated code cover a wide range of vulnerability types and
identify and mitigate residual failure modes effectively.          cannot be fully mitigated by generic warnings alone. These
Research Questions. We evaluated the MA-CoT using the              works motivate security-specific prompt structures that inject
following research questions:                                      actionable guidance rather than relying on broad reminders.
                                                                      A major line of research treats LLMs as both generators
RQ1: To what extent does targeted CWE-based mitigation
                                                                   and reviewers. Tony et al. [16] provided a systematic investi-
   reduce the severity of vulnerabilities in LLM-generated
                                                                   gation of prompting techniques for secure code generation and
   code compared to standard prompting techniques?
                                                                   reported that Recursive Criticism and Improvement (RCI) can
RQ2: How do programming language characteristics influ-
                                                                   reduce weakness density (e.g., lowered the average weakness
   ence the effectiveness of mitigation-aware prompting?
                                                                   by 77.55% compared with GPT-4), while also noting that
RQ3: What vulnerability patterns emerge across models, and
                                                                   some weakness families (e.g., command injection patterns)
   how can they inform model-specific security?
                                                                   may remain persistent under prompting. Their analysis showed
Contributions. The contributions of this study are as follows:     that reductions are more reliable for certain CWEs (e.g., CWE-
 1) MA-CoT Prompt Method. A prompting method that in-              94, CWE-259, and CWE-330) than for others. More broadly,
    tegrates actionable CWE mitigation guidance, a baseline        the RCI paradigm was introduced as a general strategy for
    security ruleset, and language-specific adaptations.           improving LLM task performance via iterative critique and
 2) Comprehensive Empirical Evaluation. An extensive study         revision [30]. Datta et al. [29] studied reflection-style secure
    across three state-of-the-art LLMs, three programming          code generation at scale and quantified both improvements
    languages, four prompting strategies, and 200 security-        and potential regressions, reinforcing that multi-round repair
    relevant tasks, yielding 7,200 generated programs. Ef-         pipelines require careful evaluation to avoid trading one
    fectiveness is validated using LLMSecEval, a widely            weakness for another. Complementary evidence from manual
    adopted benchmark for code generation [16], [19]–[21].         reviews also suggests that repeated review cycles can increase
 3) Security Metrics and Analysis. A detailed assessment of        secure output ratios when the reviewer is security-aware [28].
    vulnerability density, severity distribution, and CWE cate-    These results motivate MA-CoT’s design choice to embed
    gory across models, languages, and prompting strategies.       mitigation guidance directly into the reasoning process rather
 4) Open Benchmark and Reproducibility. A publicly re-             than relying on unconstrained self-correction.
    leased benchmark including task specifications, CWE               Several approaches injected external security knowledge
    mappings, and experimental artifacts to support replica-       into generation. PromSec [34] optimizes prompts for secure
    tion and future research on secure code generation.            code generation and reports an order-of-magnitude reduction
 5) Layered Language-Aware Attribution and Hardening               in operational time while improving security outcomes. Se-
    Guidance. A conservative attribution framework that dis-       cureCoder [33] maps tasks to CWE-aligned security knowl-
    tinguishes language-core, runtime, ecosystem, OS, and          edge and reports more than 65% of vulnerability mitigation
                                                                                                                                                                 3



by aligning generation with CWE guidance. RESCUE [32]                            Input                ④ Code Generation                     ⑤ Evaluation
addresses noise in raw security documents by constructing a
                                                                         Programming Tasks                   LLM Models                      Quality Review
distilled knowledge base and hierarchical retrieval, reporting                                        GPT-5, Claude-4.5, Gemini-2.5               SAST, Expert
                                                                      Write a program that create a
a 4.8-point average improvement. Related recipes “secure-by-                socket server ……                  Language                        Benchmark
instruction” proposed a systematic use of CWE documentation               Prompt Methods                     C, Java, Python                      LLMSecEval
during training or data synthesis, but typically operate at the         • Vanilla
dataset or fine-tuning time rather than as lightweight inference-       • Zero-Shot                            ③ Prompt Construction
                                                                        • Chain-of-Thought
time controls [31]. In contrast, MA-CoT targets a portable                                                     • Baseline Security Principles
                                                                        • MA-CoT (Proposed)                    • Domain-Specific Mitigations
inference-time mechanism: concise, task-specific CWE miti-
                                                                                                               • Language-Specific Safeguards
gation snippets, and language-aware safeguards.
   Another direction aligns the model reasoning with the vul-        ① Task Analysis                           ② Mitigation Knowledge
nerability semantics. Nong et al. [35] proposed vulnerability-       • Semantic Analysis
                                                                                                               • Security mitigation strategies
semantics-guided prompting and reported large gains in vul-          • Categorical Classification
                                                                                                               • Best practices and guidelines
nerability identification accuracy by steering multi-step reason-                                              • Code review checklists
                                                                       Mitigation Knowledge Base
ing toward root causes rather than surface patterns. Separately,
self-planning decomposes coding intent into subproblems prior
                                                                    Fig. 1: Mitigation-Aware                       Chain-of-Thought                  (MA-CoT)
to implementation, improving the correctness of complex
                                                                    prompting method pipeline.
generation tasks [36]. These methods motivate MA-CoT’s
reasoning-centric design; however, MA-CoT differs from them
by grounding the reasoning steps in explicit CWE mitigation         Secure Coding. Tasks grounded in known software weak-
actions and language-specific secure defaults.                      nesses based on MITRE’s CWE taxonomy, e.g., injection
   Security behavior varies across languages and bench-             flaws, cryptographic misuse, and insecure data handling. ❷
marks, making cross-language evaluations essential for general      Data Structures and Algorithms. Problems focusing on core
claims. Recent multi-language analyses have reported uneven         computing concepts such as array manipulation, recursion,
security and quality in LLM-generated code [37], [38]. Bench-       sorting, searching, and graph traversal. ❸ Parsing and Val-
marking has also shifted to joint functionality and security        idation. Tasks requiring careful input processing, constraint
metrics. CWEval evaluates whether the generated programs            enforcement, and boundary checking to assess robustness and
are correct and secure, highlighting that passing tests does not    correctness. ❹ Networking. Scenarios emulating networked
imply security [39]. BaxBench evaluates backend generation          systems, e.g., authentication errors and protocol misuse. ❺
under exploit-driven assessment and shows that security fail-       Mathematics and Logic. Challenges evaluating numerical rea-
ures remain common under realistic threat models, even when         soning, precision, and logical flow. ❻Programming Systems
functional correctness is achieved [40]. SecureAgentBench           and Utilities. Utility tasks involving file handling, scripting,
extends the evaluation to realistic vulnerability scenarios and     system configuration, and general-purpose workflows. ❼ Con-
reports that explicit security instructions alone do not reliably   currency and Synchronization. Tasks targeting race conditions,
yield secure codes [41]. MA-CoT is positioned within this           thread safety, and synchronization in parallel execution tasks.
landscape as a prompt-level control designed to generalize          Stage 2: Mitigation Retrieval. For each identified domain, the
across models, languages, and evaluation settings by integrat-      pipeline queries the code-security weakness mitigation dataset
ing mitigation knowledge into the generation rationale.             in Section IV-B to retrieve mitigation strategies for the task.
                                                                    This database contains mitigation entries mapped to security
                     III. M ETHODOLOGY                              categories and annotated with general rules, language-agnostic
                                                                    guidance, code review checklists, and/or fine-tuning examples.
   The proposed Mitigation-Aware Chain-of-Thought (MA-
                                                                    For example, authentication-related tasks retrieve mitigation
CoT) framework is designed to enhance the reliability of
                                                                    for Weak Password Requirements: “Implement strong pass-
LLM-generated code. As illustrated in Figure 1, the framework
                                                                    word policies, including requirements for length, complexity,
operates via a multi-stage pipeline that progressively enriches
                                                                    and expiration. Use password hashing and salting techniques
prompts with security context and mitigation guidance. Each
                                                                    to protect stored passwords.”
stage is intended to reduce recurring vulnerabilities and en-
                                                                    Stage 3: Prompt Construction. The final prompt combines
sure consistent, dependable code generation across models,
                                                                    three components: ❶ the baseline security principles applica-
languages, and prompting strategies, thereby systematically
                                                                    ble to all code, ❷ the mitigation strategies, and ❸ the specific
improving the reliability of LLM-based software synthesis.
                                                                    security checklist for the task and the programming language
                                                                    based on the aforementioned Stage 2. This structured approach
A. Pipeline Design                                                  provides the LLM with knowledge related to secure code to
                                                                    improve the security of LLM-generated code.
Stage 1: Task Analysis and Domain Classification. For
a given programming task description, MA-CoT determines
relevant security domains by referencing the predefined cate-       B. Task Dataset
gories below. It uses LLM-based semantic analysis to classify         This work builds on the dataset in section IV, created to
the task and assign one or more categories as follows: ❶            evaluate the security and quality of LLM-generated code. In
                                                                                                                                          4



TABLE I: Configurations: model, short name (SN), tempera-                line rules, task-specific mitigation, and a language checklist.
ture (Temp), max tokens (MT), and context window (CW).                   Rather than correcting code after generation, it encourages
     Model                                 SN       Temp   MT     CW
     gpt-5-2025-08-07 [42]               gpt-5        1    32k    400k
                                                                         models to surface potential weaknesses during reasoning.
     claude-sonnet-4-5-20250929 [43]   claude-4.5     1    32k    200k      2) Code Generation and Collection: For each combination
     gemini-2.5-pro [44]               gemini-2.5     1    32k   1000k
                                                                         of (LLM, language, prompting method, task), we generated
                                                                         one code sample, resulting in 7,200 total implementations
addition, we developed a code weakness mitigation dataset                (3 LLMs × 3 languages × 4 methods × 200 tasks). The
capturing practical knowledge on how vulnerabilities should              generation used API access to the respective model endpoints
be mitigated rather than merely identified, translating it into a        with consistent parameters. The output code was extracted,
structure from which language models can directly learn.                 compiled/syntax-checked, and stored with associated metadata
                                                                         (model, language, prompt method, task ID).

C. Experimental Design
                                                                         D. Evaluation Methodology
   1) LLM, Language, and Prompt Selection: To examine how
securely LLMs generate code under different conditions, we                  We used SonarQube as our main automated analysis plat-
narrowed our evaluation to a representative set of models,               form [45]. It provides language-specific analyzers, and for
programming languages, and prompt styles reflecting common               each generated code sample we collected detected security
practice rather than idealized setups. The choices were guided           vulnerabilities and their severity (Blocker, Critical, Major, Mi-
by practicality and coverage, including tools developers rely            nor). We also mapped vulnerabilities to corresponding CWEs
on while capturing meaningful architectural variation.                   to identify common weakness types.
   This study focuses on three LLM families: ChatGPT, Gem-
ini, and Claude. These models are widely deployed and rank               E. Benchmarking
among the strongest in code generation, user base, credibility,             To examine how the proposed prompting method influences
and support. They differ in training scale, context-window               code security, we used LLMSecEval (Section IV-C) as an ex-
limits, and safety alignment strategies, often leading to behav-         ternal reference. This benchmark centers on coding scenarios
ioral differences when handling code mixing functionality with           where security failures are likely, rather than tasks focused
security requirements. Table I lists the selected configurations.        only on functional output. This distinction is critical: models
Max_tokens specifies the maximum tokens produced in                      may produce code that compiles and behaves as expected
completion. The temperature regulates output randomness. The             yet includes unsafe operations, weak validation, or designs
CW is the largest token limit processed in a single forward              contradicting secure-coding practices. LLMSecEval captures
pass, including prompt and generated responses, dictating how            these issues through tasks mapped to common CWE patterns,
much text the LLM can handle at once.                                    offering a clearer view of how models handle vulnerability-
Programming Languages. The evaluation spanned three lan-                 prone situations. The benchmark also fits the multi-language
guages: C, Java, and Python, each with distinct risks and                setup of our study. Because our experiments cover C, Java,
features, allowing us to observe how LLMs adapt across                   and Python, a shared set of security-oriented tasks helps main-
languages. C is a low-level, memory-unsafe language exposing             tain consistency across languages with different programming
buffer overflows, use-after-free, and pointer-related vulnerabil-        paradigms and risk profiles. LLMSecEval provides consistency
ities. Manual memory management requires careful discipline.             by framing each task to highlight the underlying security
Java is a managed language with garbage collection and strong            concerns rather than the surface-level syntax.
typing, shifting vulnerabilities toward logic errors, injection
flaws, and improper API usage. Python is a dynamically typed,
interpreted language with an extensive standard library, where           F. Language-Aware Vulnerability Attribution
vulnerabilities involve input validation, insecure deserializa-             A recurring source of confusion in language-aware security
tion, and cryptographic misuse. Evaluating all three provides            analysis is the term language feature. Many vulnerability
a balanced view of how models handle low- and high-level                 drivers are not properties of the programming language specifi-
security concerns and reflects real-world software diversity.            cation itself, but of the language stack that developers typically
Prompting Methods. We compare four prompting methods                     use: standard libraries, primary third-party libraries, platform
reflecting common LLM use: ❶ Vanilla prompting provides                  APIs, and compiler toolchains. To avoid over-claiming, we use
only the task description without security guidance as a                 a strict, layered attribution scheme that separates language-
baseline. ❷ Zero-shot prompting introduces minimal structure             core mechanisms from language-adjacent mechanisms.
by encouraging secure reasoning as “Write secure code for the            Attribution Layers. We label an attributed mechanism as
following task”. ❸ Chain-of-Thought (CoT) extends this by                language-core only when it follows directly from the lan-
requesting step-wise reasoning: (1) Understand requirements,             guage specification or mandatory runtime semantics (e.g., C
(2) Identify security considerations, (3) Implement the solution         raw buffers without bounds checks, Python default-argument
securely, and (4) Verify correctness. Although this improves             evaluation timing). All other drivers are classified as language-
correctness, it may overlook minor security concerns. ❹ The              adjacent and attributed to the closest layer: (1) standard
mitigation-aware CoT prompt, proposed in this work, inte-                runtime/library defaults, (2) ecosystem library/framework API
grates security signals into the reasoning stage through base-           design, (3) platform/OS API design, (4) toolchain/optimization
                                                                                                                                      5



TABLE II: Layered attribution used to interpret "language-             and instructed them to generate code from this dataset using
aware" vulnerability drivers.                                          four prompting methods across three programming languages,
 Language-core (strict): Properties required by the language           producing in 7,200 samples for evaluation.
 spec or mandatory runtime semantics (e.g., C raw memory and
 unchecked buffers; Python default-argument evaluation; Python
 string literal semantics relevant to header injection).               B. Mitigation-Aware Dataset
 Standard runtime/library: Defaults and APIs shipped with the             While the first dataset evaluated model outputs, the second
 standard platform (e.g., Java JCE/JSSE/JAXP configuration sur-        serves a complementary purpose. It captures practical knowl-
 faces).
                                                                       edge on how vulnerabilities should be mitigated rather than
 Ecosystem library/framework: Third-party or dominant frame-
 works and their secure-by-default posture (e.g., crypto/TLS li-       merely identified, translating it into a structure from which
 braries, web frameworks).                                             language models can learn. Each record represents a security
 Platform/OS API: System call semantics and filesystem/network         category or specific CWE identifier, linking a problem domain
 primitives (e.g., POSIX check-then-use patterns driving TOCTOU).      to language-agnostic or language-specific mitigation guidance,
 Toolchain/optimization: Compiler/linker/runtime optimizations
                                                                       review checklists, and, in some cases, fine-tuning examples.
 that affect security idioms (e.g., non-guaranteed memory wiping
 without a secure zeroization primitive).                              Dataset Composition. Each entry in the Mitigation-Aware
 Application security logic/policy: Input validation, password poli-   dataset contains four core components. First, General Rules
 cies, and configuration choices that are not determined by the        outline baseline security practices across languages, empha-
 language itself.                                                      sizing input validation, secret handling, cryptography, TLS
                                                                       configuration, and concurrency safeguards. Second, Language-
                                                                       Specific Guidelines tailor this guidance to languages such as
behavior, or (5) application-level security logic/policy. This         C, C++, Python, and Java, highlighting defensive techniques
distinction is essential; e.g., TOCTOU (CWE-367) is an OS/-            like safe memory handling in C or secure resource man-
POSIX check-use issue that can occur in any language using             agement in Java. Third, the Code Review Checklist provides
the same syscalls, not a C language feature in the strict sense.       a concise reference to confirm that generated code meets
Attribution Procedure. For each SonarQube-reported                     essential safety requirements. Finally, the dataset includes
weakness, we use the standardized analysis fields                      a few Fine-tuning Examples, each in a three-part format:
(language_feature, feature_category, feature_mechanism,                an instruction, an insecure input, and a secure output, il-
and comparative_analysis) to assign one primary layer.                 lustrating correct remediation steps for models to learn. We
When the same vulnerability could plausibly be attributed              include representative entries in the appendix. These examples
to multiple layers, we apply a conservative tie-break rule:            show how each record integrates general mitigation principles,
we assign it to the lowest layer that is necessary to produce          language-specific guidance, review checklists, and fine-tuning
the risk (e.g., if the risk exists because a library API allows        examples. They demonstrate the hierarchical organization of
insecure options, we assign it to the library layer rather than        the Mitigation-Aware dataset and how security concepts are
to the language). This results in a reproducible mapping from          translated into practical, language-aware rules suitable for
observed vulnerabilities to language-core versus language-             evaluation and model alignment.
adjacent mechanisms, enabling a clearer interpretation of              Purpose and Applications. The Mitigation-Aware dataset op-
RQ2. Table II summarizes the attribution layers and the strict         erates at two complementary levels. First, it serves as a knowl-
criteria used to avoid mislabeling OS, library, or toolchain           edge base combining mitigation strategies, language-aware
mechanisms as language-core features.                                  guidance, and reasoning that supports secure-programming
                                                                       decisions. This structure helps trace how coding practices
                          IV. DATASET                                  reduce risk, especially when a vulnerability appears correct
A. Prompt Description                                                  in isolation but fails upon review. Second, it acts as a broader
                                                                       training corpus. Although it lacks explicit input-output pairs,
   This study builds on our dataset [37] developed to evaluate
                                                                       its rules and rationales shape model behavior by encouraging
the functional quality and security of LLM-generated code.
                                                                       secure design patterns. This dual role supports both model
The dataset contains 200 language-agnostic programming
                                                                       analysis and security-aware tuning. The modular structure
tasks organized into seven functional categories. Each task
                                                                       further allows additional languages, evolving weaknesses, or
includes a neutral problem statement, and generated code was
                                                                       CWE domains to be incorporated with minimal disruption as
evaluated using unit tests and manual and automated (tool-
                                                                       security expectations change.
based) reviews, such as SonarQube. This dataset also serves
as the basis for the prompt descriptions used in this study.
   The reuse of this dataset offers two advantages. First, it          C. LLMSecEval Benchmark Dataset
preserves continuity with our earlier analysis, enabling us to            LLMSecEval [46] is widely used to evaluate language
assess whether changes in prompting or model capabilities              models in security-sensitive coding tasks [16], [47]–[49]. The
yield measurable improvements in secure code generation.               benchmark is built from prompts derived from real C and
Second, because the dataset was reviewed and refined by mul-           Python examples associated with the MITRE CWE Top 25,
tiple practitioners, it remains suitable for evaluating the prompt     rewritten in neutral language so the task intent remains clear
methods explored here, including Vanilla, Zero-shot, CoT, and          without revealing the vulnerability. Each prompt is paired with
the mitigation-aware CoT approach. We selected three LLMs              a secure reference solution, enabling consistent comparison of
                                                                                                                                      6



TABLE III: Number of vulnerabilities by programming lan-            TABLE IV: Vulnerabilities by programming language, model,
guage, model, and prompting strategy (200-task dataset).            and prompting strategy (LLMSecEval, 150 tasks).
      Language   Model        Vanilla   ZeroShot   CoT   MA-CoT           Language   Model        Vanilla   ZeroShot   CoT   MA-CoT
                 gpt-5          17         23       24     13                        gpt-5           4         7        10     0
      C          claude-4.5     19         20       27     11             C          claude-4.5      3         3        7      0
                 gemini-2.5     16         20       16      7                        gemini-2.5      4         5        1      1
                 gpt-5           2          3        3      2                        gpt-5           2         0        0      0
      Java       claude-4.5     20         13       12      1             Java       claude-4.5     46         28       6      2
                 gemini-2.5      5          6        6      1                        gemini-2.5      5         3        3      1
                 gpt-5           3          2        2      2                        gpt-5           1         0        1      0
      Python     claude-4.5      7         10        4      2             Python     claude-4.5      4         2        3      0
                 gemini-2.5      3          3        4      0                        gemini-2.5      4         6        3      0



model outputs and highlighting meaningful gaps in secure rea-       52 (vanilla) to 31 (MA-CoT), a 40% decrease. Java shows
soning. The dataset is particularly useful for evaluating prompt    more dramatic results, dropping from 27 to 4 vulnerabilities
methods, as many of its tasks resemble routine programming          (85% reduction). Python achieved similar success, with a 69%
problems in which security issues often go unnoticed. By            reduction from 13 to 4 issues. These differences reflect how
covering a range of weakness categories rather than a single        cryptographic algorithms, memory management, and certifi-
CWE, LLMSecEval helps to expose recurring model errors              cate validation affect baseline code security.
and provides a stable baseline for measuring improvement.              claude-4.5 shows notable behavior. It produces the
This makes it a practical benchmark for assessing whether a         highest Vanilla vulnerability count (46 across all languages),
prompt strategy genuinely enhances a model’s ability to avoid       but achieves the largest relative improvement under MA-CoT,
risky patterns and follow safer design choices.                     reducing issues to 14 in total. This 70% reduction indicates
                                                                    a strong instruction-following capability paired with weak
                 V. R ESULTS AND D ISCUSSION                        security priors. The model appears to lack internal safeguards
                                                                    that would prevent vulnerabilities in unconstrained generation
   We present findings from evaluating MA-CoT on three
                                                                    but can effectively apply explicit mitigation guidance when
LLMs (gpt-5, claude-4.5, gemini-2.5), three pro-
                                                                    provided with such safeguards.
gramming languages (C, Java, Python), and two bench-
                                                                       Takeaway 2: claude-4.5 demonstrates limited built-in
mark datasets, totaling 350 security-relevant programming
                                                                    security safeguards, yet it shows strong responsiveness to
tasks. The analysis combines automated static analysis using
                                                                    structured mitigation prompts, resulting in a marked reduction
SonarQube with manual expert review to assess vulnerabil-
                                                                    in vulnerability cases under guided conditions.
ity patterns, severity distributions, and the effectiveness of
mitigation-aware prompting compared to other approaches.
                                                                    B. Benchmarking using LLMSecEval
A. Performance on Primary Dataset                                      Table IV presents the results of the LLMSecEval bench-
   Table III presents the vulnerability counts from the 200-task    mark, which contains 150 security-focused tasks designed
dataset across all evaluated configurations. The results indicate   independently from our primary dataset. This external vali-
substantial variation in baseline security behavior and the way     dation tests whether MA-CoT generalizes beyond the specific
different models respond to prompting interventions.                characteristics of the evaluation dataset.
   Several patterns emerged from this evaluation. First, MA-           The LLMSecEval results validated the patterns observed in
CoT consistently produced the fewest vulnerabilities in seven       our primary dataset. MA-CoT achieved complete vulnerability
of the nine configurations. The exceptions occur with gpt-5         elimination in six of the nine configurations. When vulnera-
in Java, where Vanilla and MA-CoT both generate two vul-            bilities persist, they remain minimal (one or two instances)
nerabilities, and with gpt-5 in Python, where ZeroShot,             and outperform all other prompting approaches. The method
CoT, and MA-CoT all generate two vulnerabilities. Second,           is effective even for tasks explicitly constructed to expose
the ZeroShot and CoT prompting methods frequently fail to           weaknesses in automated code generation.
improve security over the Vanilla baseline, except in Java and         A comparison of the two datasets shows both consistency
partially in Python for claude-4.5. In C, ZeroShot and              and instructive differences. The relative ranking of the prompt-
CoT increase the vulnerability counts for all three models,         ing methods remained stable: MA-CoT consistently outper-
with CoT generating 27 issues for claude-4.5 compared to            formed the alternatives, while ZeroShot, CoT, and Vanilla
19 in Vanilla. This surprising result suggests that encouraging     showed no consistency in their security quality. However, the
step-by-step reasoning without concrete security knowledge          absolute vulnerability counts differed substantially. LLMSecE-
can degrade code security.                                          val produces a higher vulnerability ratio using Vanilla in Java
   Takeaway 1: MA-CoT delivers the most consistent security         than our dataset (53 versus 27 in our dataset), but lower C
gains, whereas ZeroShot and CoT often fail to help and can          counts (11 versus 52). These variations reflect differences in
even increase vulnerabilities, particularly in C, suggesting that   tasks and programming languages rather than evaluation meth-
unguided reasoning may unintentionally weaken code security.        ods. LLMSecEval emphasizes web security patterns common
   The magnitude of improvement in MA-CoT varied by                 in Java applications, while our dataset includes more system
language. C shows clear gains, reducing vulnerabilities from        programming scenarios typical of C development.
                                                                                                                                                                         7



  Severity
  Blocker                                                   C                                         Java                                    Python
  Critical                           50    gpt-5      claude-4.5    gemini-2.5         gpt-5      claude-4.5     gemini-2.5        gpt-5     claude-4.5    gemini-2.5
  Major
  Minor      Primary Vul. Count      40
                                     30
                                     20                                                           2
                                           14 14              22                                  8
                                     10                     3                                            1
                                      8 16       11   18 17         14 20 14                          10 5
                                      6     9 10                                                 10
                                      4                   5 8                  7                                 2 4 4                       7 10 4
                                      2 1
                                      0           2   1 3           2     2        2 21 21 2           3 6   1   3 2 2 1       3 2 2 2              2      21 3 31
                                        V ZS CoT MA   V ZS CoT MA   V ZS CoT MA    V ZS CoT MA   V ZS CoT MA     V ZS CoT MA   V ZS CoT MA   V ZS CoT MA   V ZS CoT MA
                                     50
             LLMSecEval Vul. Count




                                     40
                                                                                                 24
                                     30
                                     20                                                           2 15
                                     10
                                      8      5                                                   20 13
                                      6
                                      4 4 34 5                  7   4 5 1 1                              6       2 1
                                                                                                                                             4 2 21        4 51 3
                                      2               3 3                          2                         2   3 2 3 1       1      1
                                      0
                                        V ZS CoT MA   V ZS CoT MA   V ZS CoT MA    V ZS CoT MA   V ZS CoT MA     V ZS CoT MA   V ZS CoT MA   V ZS CoT MA   V ZS CoT MA

Fig. 2: Vulnerability severity counts across two datasets. Panels are organized by dataset (rows) and language (columns). Within
each panel, bars are grouped by LLM and ordered by prompting method (V=Vanilla, ZS=Zero-shot, CoT=Chain-of-Thought,
MA=MA-CoT). Stacks show severity counts (Blocker, Critical, Major, Minor).


   Takeaway 3: MA-CoT is consistently the most secure                                            a buffer immediately before releasing it, because the compiler
prompting method: it removes vulnerabilities in most settings,                                   may optimize the write operation. In other words, MA-CoT
and when issues remain, they are few and fewer than all                                          reduces the overall high-severity burden in C, but it also in-
alternatives. Across both datasets, MA-CoT maintained the                                        troduces more attempted buffer-sanitization steps that must be
top rank, while ZeroShot, CoT, and Vanilla were unstable.                                        implemented with a guaranteed-wipe primitive to be correct.
Differences in raw vulnerability counts stem mainly from task                                    Therefore, we treat c:S5798 rule as an implementation-level
types and language focus, not evaluation flaws.                                                  hardening issue rather than evidence of weaker security, and
   The consistent and counterintuitive CoT behavior across                                       document the remediation in the appendix.
both datasets warrants closer examination. In C, CoT yields                                      Benchmark Dataset (LLMSecEval). The benchmark shows
higher vulnerability rates than Vanilla in five model-dataset                                    a broader severity distribution than the primary dataset, in-
pairs. When given general reasoning instructions without ex-                                     cluding non-zero Major and Minor findings. Under Vanilla, we
plicit security guidance, models fail to avoid vulnerabilities                                   recorded 73 findings in total (34 Blocker, 11 Critical, 4 Major,
that are sometimes prevented in Vanilla and ZeroShot settings.                                   24 Minor), of which 45 were high-severity (Blocker+Critical).
                                                                                                 MA-CoT reduces this to 4 findings (1 Blocker, 1 Critical, 0
                                                                                                 Major, 2 Minor), reducing high-severity by 95.6% (45 to 2)
C. Vulnerability Severity Analysis
                                                                                                 and total findings by 94.5% (73 to 4). The same pattern holds
   Severity reflects the likely impact of the identified vulner-                                 across languages: in C, Critical decreases from 11 to 1; in
abilities and provides more insight than raw counts alone.                                       Java, Blocker decreases from 25 to 1, and Major is eliminated
SonarQube categorizes each issue into one of four levels                                         (4 to 0); and in Python, Blocker decreases from 9 to 0, with
(Blocker, Critical, Major, Minor). We present severity distribu-                                 no remaining findings under MA-CoT.
tions by language, LLM, and prompting strategy in Figure 2.                                      Cross-Dataset Interpretation. Figure 2 provides four com-
Primary Dataset. The findings were concentrated almost                                           parisons: (1) severity composition for a fixed configuration
exclusively at the two highest severity levels. In the Vanilla                                   (stack segments), (2) differences between prompting methods
setting, we observed 92 total findings, of which 90 were                                         within each LLM (bar order per group), (3) variation across
Blocker or Critical (18 Blocker, 72 Critical, 2 Minor). With                                     languages (C, Java, Python), and (4) stability across datasets
MA-CoT, the total decreases to 39 findings, all of them high-                                    (Primary on top, LLMSecEval on bottom). In the primary
severity (11 Blocker, 28 Critical), corresponding to a 56.7%                                     dataset, findings concentrate in Blocker and Critical, whereas
reduction in Blocker and Critical issues (from 90 to 39). This                                   LLMSecEval includes Major and Minor findings. MA-CoT
improvement is consistent across languages: in Java, high-                                       reduces Blocker and Critical in both datasets and also lowers
severity findings fall from 25 (13 Blocker, 12 Critical) to 4                                    low-severity findings in LLMSecEval. We report per-category
(1 Blocker, 3 Critical), and in Python from 13 (1 Blocker, 12                                    counts rather than totals to avoid masking shifts between
Critical) to 4 (0 Blocker, 4 Critical). C shows a category shift                                 severity levels and to keep improvements visible per language,
under MA-CoT: Critical findings drop from 48 to 21, while                                        model, and prompting method.
Blocker increases from 4 to 10, the combined high-severity                                          Takeaway 4: MA-CoT lowers high-severity vulnerabilities
total (Blocker plus Critical) still decreases from 52 to 31. The                                 (Blocker and Critical) across both datasets: by 56.7% in the
Blocker increase is dominated by c:S5798 rule (“memset                                           primary dataset (90 to 39) and by 95.6% in LLMSecEval (45
should not be used to delete sensitive data”). This rule flags                                   to 2). On LLMSecEval, it also reduces total findings by 94.5%
a specific insecure-erasure idiom, using memset() to scrub                                       (73 to 4), indicating robustness under dataset shift.
                                                                                                                                                                                                               8



                                             C                                                     Java                                                                Python
                             gpt-5       claude-4.5 gemini-2.5                      gpt-5       claude-4.5 gemini-2.5                                gpt-5           claude-4.5 gemini-2.5
CWE count (Top-2)
                    34
                    24
    Primary


                                       327 295          297 327
                    14 327 327 327 295  4 4 327 367 119
                                                     2 4 2 297
                                                                                                 79 295
                                                                                                  4 2 20                                                                295
                                6   2          8 2                                611 611 521            3             611 79 259                                        1                79 256 113
                          6 6                              295 295 295 2                                                2 2 1
                         295 14 14 367   295 327 367 14                            1 1 1        327 327 327                                                         327 327 327            1 1 1
                    2     7 7 8 6         9 7 9 8           9 8 10 295                            7 7 4                                                              7 7 4
                                                                       3      327 327 327 327               521        327 327 327 79          327 327 327 327                     327   327 327 327
                    0                                                          2 2 2 1                          1       2 3 3 1                 3 2 2 2                             2      2 2 3
                         V ZS CoT MA     V ZS CoT MA       V ZS CoT MA        V ZS CoT MA       V ZS CoT MA             V ZS CoT MA             V ZS CoT MA          V ZS CoT MA          V ZS CoT MA
CWE count (Top-2)




                    34                                                                          259
                                                                                                 13
  LLMSecEval




                    24                                                                              259
                                                                                                     10
                    14       367 367                           295                              600
                                                                                                 24 600                259 600 259                                   79                      259
                              3 5                               1             521                                                                                           259           20 1
                                                 367                           1                     15 259              2 1 1                                        1      1             1 256
                    2    367 14 14       367 367 7         367 367                                       6 600                                                      259 259 327
                          4 3 5           3 3               4 4 367 367       20                                        20 259 521 259         259       259          3 2 2              259 5 259
                                                                                                                                                                                                 3
                    0                                              1   1      1                             2            2 2 2 1                1         1                                2
                         V ZS CoT MA     V ZS CoT MA        V ZS CoT MA         V ZS CoT MA V ZS CoT MA V ZS CoT MA                   V ZS CoT MA                    V ZS CoT MA          V ZS CoT MA
                                                                                         Stack interpretation
                                                          Top-1 CWE (label shows CWE-ID and count)     Top-2 CWE (label shows CWE-ID and count)

Fig. 3: Common Weakness Enumeration (CWE) patterns across datasets, languages, LLMs, and prompting methods. Rows
correspond to datasets (top: Primary, bottom: LLMSecEval). The columns correspond to the languages (C, Java, and Python).
Within each panel, bars are grouped by LLM and ordered by prompting method (V=Vanilla, ZS=Zero-shot, CoT=Chain-of-
Thought, MA=MA-CoT).


   Takeaway 5: In C of the primary dataset, MA-CoT reduces                                            TABLE V: Top-5 CWE categories per language, LLM, and
Blocker and Critical (52 to 31) while increasing Blocker due                                          prompting method across datasets. Each cell lists up to five
to strict secure-erasure enforcement, dominated by c:S5798                                            categories as CWE-ID (count), without the CWE- prefix.
                                                                                                       Lang.        LLM        Method Primary (Top-5 CWEs)                    LLMSecEval (Top-5 CWEs)
rule. This reflects increased use of hardening patterns imple-                                                                 V      295(7), 327(6), 367(2), 119(1), 297(1) 367(4)
mented with a non-guaranteed primitive (plain memset), not                                                          GPT-5
                                                                                                                               ZS
                                                                                                                               CoT
                                                                                                                                      14(7), 327(6), 367(5), 119(2), 295(2) 14(3), 367(3), 119(1)
                                                                                                                                      14(8), 327(6), 295(4), 367(3), 119(2) 14(5), 367(5)
weaker security: the net high-severity burden decreases, and                                                                   MA     367(6), 295(2), 327(2), 14(1), 119(1) –
                                                                                                                               V      295(9), 327(4), 297(3), 367(2), 119(1) 367(3)
remaining issues are concentrated in a small set of cases.                                             C            Claude-4.5
                                                                                                                               ZS     327(7), 295(4), 367(4), 119(3), 297(2) 367(3)
                                                                                                                               CoT    367(9), 327(8), 14(5), 295(4), 297(1) 367(7)
                                                                                                                               MA     14(8), 367(2), 295(1)                   –
                                                                                                                               V      295(9), 119(2), 297(2), 327(2), 367(1) 367(4)
D. Common Weakness Enumeration Patterns                                                                             Gemini-2.5
                                                                                                                               ZS     295(8), 297(4), 367(4), 120(2), 327(2) 367(4), 295(1)
                                                                                                                               CoT    295(10), 327(2), 119(1), 297(1), 367(1) 367(1)
                                                                                                                               MA     295(3), 297(2), 367(2)                  367(1)
   Severity counts quantify impact but do not explain recur-                                                                   V      327(2)                                  20(1), 521(1)
ring weakness classes. We therefore analyzed the Common                                                             GPT-5
                                                                                                                               ZS     327(2), 611(1)                          –
                                                                                                                               CoT    327(2), 611(1)                          –
Weakness Enumeration (CWE) categories reported by Sonar-                                                                       MA     327(1), 521(1)                          –
                                                                                                                               V      327(7), 79(4), 20(3), 600(2), 611(2)    600(24), 259(13), 20(9)
Qube to characterize recurring vulnerability types by dataset,                                                                 ZS     327(7), 79(2), 295(2), 521(2)           600(15),    259(10),    79(2),
                                                                                                       Java         Claude-4.5
                                                                                                                                                                              521(1)
language, LLM, and prompting method. Figure 3 summarizes                                                                       CoT    327(4), 20(3), 259(2), 79(1), 521(1)    259(6)
the two most frequent CWE categories per configuration, while                                                                  MA
                                                                                                                               V
                                                                                                                                      521(1)
                                                                                                                                      327(2), 611(2), 521(1)
                                                                                                                                                                              600(2)
                                                                                                                                                                              20(2), 259(2), 521(1)
Table V reports the top five CWEs, providing a fine-grained                                                         Gemini-2.5
                                                                                                                               ZS     327(3), 79(2), 521(1)                   259(2), 600(1)
                                                                                                                               CoT    327(3), 79(1), 259(1), 323(1)           521(2), 259(1)
view of which classes MA-CoT removes and which remain.                                                                         MA     79(1)                                   259(1)
                                                                                                                               V      327(3)                                  259(1)
Primary Dataset. In C, baseline prompting is marked by                                                                         ZS     327(2)                                  –
                                                                                                                    GPT-5
certificate-validation and cryptography issues, mainly CWE-                                                                    CoT
                                                                                                                               MA
                                                                                                                                      327(2)
                                                                                                                                      327(2)
                                                                                                                                                                              259(1)
                                                                                                                                                                              –
295 (Improper Certificate Validation) and CWE-327 (Broken                                                                      V      327(7)                                  259(3), 79(1)
                                                                                                       Python                  ZS     327(7), 295(1), 297(1), 521(1)          259(2)
or Risky Cryptographic Algorithm). Aggregated across LLMs,                                                          Claude-4.5
                                                                                                                               CoT    327(4)                                  327(2), 259(1)
                                                                                                                               V      327(2), 79(1)                           259(2), 20(1), 79(1)
these remain frequent under Vanilla, Zero-shot, and CoT                                                             Gemini-2.5 ZS     327(2), 256(1)                          256(5), 259(1)
(CWE-295: 25, 14, 18; CWE-327: 12, 15, 16). Under MA-                                                                          CoT
                                                                                                                               MA
                                                                                                                                      327(3), 113(1)
                                                                                                                                      –
                                                                                                                                                                              259(3)
                                                                                                                                                                              –
CoT, both drop sharply (CWE-295=6; CWE-327=2). Residual
findings concentrate on CWE-367 (TOCTOU Race Condition)
and CWE-14 (Compiler Removal of Code to Clear Buffers),
linked to specific idioms: TOCTOU arises from check-then-                                             the compiler can optimize the write, motivating guaranteed-
use flows, while CWE-14 is triggered when a wipe such                                                 wipe primitives (appendix B). We therefore treat these residual
as memset is not guaranteed under compiler optimization                                               findings as implementation-level hardening issues rather than
(appendix).                                                                                           baseline cryptographic or certificate-validation failures.
   The appearance of CWE-367 and CWE-14 under MA-CoT                                                    Java shows a different profile: CWE-327 persists under
requires careful interpretation. In our outputs, these reflect                                        baseline alongside web and API-misuse patterns such as CWE-
security hardening that triggers stricter static analysis. For                                        611 (Improper Restriction of XML External Entity Reference)
example, file-existence checks before opening can create a                                            and CWE-79 (Cross-site Scripting). Under MA-CoT, CWE-
time-of-check time-of-use window (CWE-367). Similarly, ex-                                            611 is absent in the primary dataset, and CWE-79 is strongly
plicit buffer scrubbing with memset may be flagged because                                            reduced, indicating that explicit configuration-level guidance is
                                                                                                                                9



most effective when security depends on correct API defaults     TABLE VI: Total vulnerabilities by model aggregated across
rather than syntactic correctness alone.                         languages. Prompting methods: V=Vanilla, ZS=Zero-shot,
   Python shows the most concentrated weaknesses in the          CoT=Chain-of-Thought, MA=MA-CoT.
primary dataset, with CWE-327 leading in multiple baseline                              Primary Dataset    LLMSecEval Dataset
configurations. This aligns with Python’s memory safety by           Model         V      ZS   CoT    MA   V    ZS   CoT   MA
design, where security failures cluster around cryptographic         gpt-5         22     28    29    17    7    7    11    0
                                                                     claude-4.5    46     43    43    14   53   33    16    2
misuse and unsafe parameter choices. Under MA-CoT, Python            gemini-2.5    24     29    26     8   13   14     7    2
findings are minimized and eliminated in some settings.
   Cryptographic weaknesses (CWE-327) appear in all three
languages, suggesting that secure cryptography remains chal-     ness to mitigation-aware constraints: when guidance specifies
lenging, regardless of the language design. In the primary       safeguards, the model produces measurably safer code.
dataset, the reductions in CWE-327 under MA-CoT were             Gemini. gemini-2.5 achieves the lowest MA-CoT total in
substantial when measured against the Vanilla baseline: in       the primary dataset (8), improving from Vanilla=24 (67%).
C, 12 to 2 (83%); in Java, 11 to 1 (91%); and in Python,         In LLMSecEval, MA-CoT reduced the findings from 13 to 2
12 to 4 (67%). These reductions are consistent with MA-          (85%). In particular, gemini-2.5 also shows less degrada-
CoT prompts that constrain algorithm choices and parameters      tion under CoT in the reference dataset (7) than in the primary
toward modern, safe defaults. The appendix provides a task-      dataset (26), suggesting that its performance is more sensitive
level qualitative example for claude-4.5, showing this           to task composition than to model capacity alone.
shift from ECB/CBC-style implementations under baseline          ChatGPT. gpt-5 is comparatively stable but less responsive
prompts to AEAD-based designs under MA-CoT for the same          in the primary dataset: Vanilla, Zero-shot, and CoT are close
encryption task.                                                 (22, 28, 29), and MA-CoT reduces to 17 (23%). In LLM-
   Takeaway 6: MA-CoT suppresses recurring high-impact           SecEval, however, MA-CoT eliminates all detected findings.
CWE classes across languages and LLMs, indicating a con-         This suggests that mitigation-aware prompting effectiveness
sistent reduction in systematic security failure modes rather    depends on the task vulnerability mix.
than only a drop in total results.                                  These results support two conclusions: First, model selec-
                                                                 tion and prompt design should be considered jointly; a weaker
LLMSecEval Benchmark. The benchmark preserves the
                                                                 baseline model can still be effective when mitigation-aware
ranking observed in the primary dataset while altering the
                                                                 prompting is consistently applied. Second, relying on generic
prevalent CWE mix for some languages. In C, findings are
                                                                 “be secure” or reasoning prompts alone is risky; structured,
mainly race and timing issues (CWE-367), and MA-CoT
                                                                 actionable mitigations are needed for reliable security im-
removes them in most configurations, leaving one residual
                                                                 provements across models and datasets.
case. In Java, the benchmark exposes uncaught exceptions and
                                                                    Takeaway 7: Prompt design is a first-order factor: across
authentication and credential-management weaknesses (i.e.,
                                                                 models and datasets, MA-CoT is the only method that con-
CWE-600 and CWE-259), which MA-CoT substantially re-
                                                                 sistently reduces vulnerabilities, while Zero-shot and CoT are
duces compared to baseline prompts. In Python, findings also
                                                                 unreliable and can increase findings relative to Vanilla.
concentrate on few categories, and MA-CoT eliminates them
                                                                    Takeaway 8: The results reveal an interaction between model
across configurations. Overall, MA-CoT not only lowers total
                                                                 behavior and task vulnerability mix. MA-CoT is most effective
counts but filters high-risk, frequent CWE categories, leaving
                                                                 when dominant weaknesses arise from API configuration and
a smaller set tied to specific implementations and easier to
                                                                 mitigation choices (e.g., cryptography, credential handling),
mitigate with focused hardening.
                                                                 whereas residual findings concentrate on implementation-level
                                                                 hardening (e.g., race conditions, secure wiping). This explains
E. Model-Specific Security Characteristics                       why the same model shows modest gains on one dataset and
   Table VI compares the three models by aggregating vulner-     near elimination on another under the same prompting strategy.
abilities in C, Java, and Python, reported separately for the
Primary (200 tasks) and LLMSecEval (150 tasks) datasets.         F. Language-Core/Stack Vulnerabilities Drivers
Because the datasets differ in size and composition, we             This subsection addresses RQ2 using a strict definition of
interpret cross-dataset differences qualitatively and focus on   language-specificity. We separate (i) language-core drivers
within-dataset changes across prompting methods. Across          (required by the language specification or mandatory runtime
both datasets, MA-CoT was the only prompting strategy that       semantics) from (ii) language-stack drivers, including standard
consistently reduced vulnerability counts for every model.       runtime, ecosystem libraries/frameworks, platform/OS APIs,
In contrast, generic security phrasing (Zero-shot) and basic     and toolchains. The attribution layers are defined in Table II.
reasoning (CoT) are not dependable: on the primary dataset,      Cross-Language Distribution of Drivers. Table VII summa-
they increase findings for all models relative to Vanilla, and   rizes each layer’s contribution to attributed weakness instances
on LLMSecEval, they remain less effective than MA-CoT.           per language, with primary CWE evidence. The key result is
Claude. claude-4.5 has the weakest baseline in the pri-          that C security outcomes are shaped mainly by the surrounding
mary dataset (Vanilla=46) but the strongest improvement under    stack: OS-level check-then-use filesystem patterns (TOCTOU,
MA-CoT (14), a 70% reduction. The same pattern appears in        CWE-367) and library-level crypto/TLS configuration free-
LLMSecEval (53 to 2, 96%). This indicates high responsive-       dom, with language-core memory/bounds issues forming a
                                                                                                                                  10



TABLE VII: Layer contributions per language with the dom-           and O_NOFOLLOW where applicable). ③ Crypto/TLS library
inant CWE signal per layer. Percentages are computed over           layer: Reduce insecure configuration freedom by using safe
the attributed weakness instances for each language.                wrappers and secure defaults. In MA-CoT, require certificate
   Lang.    Layer Contribution                                      and hostname verification (no verification bypass) and con-
    C       Platform/OS API (38.0%, dominated by CWE-367);          strain cryptography to modern AEAD with safe parameter
            Ecosystem crypto/TLS library API (31.2%, domi-          handling. ④ Toolchain/optimization layer (secure wiping): Use
            nated by CWE-327 and certificate validation CWEs).      guaranteed-wipe primitives rather than plain memset-based
            Language-core memory and bounds (27.1%, dom-
            inated by CWE-119/120). Toolchain/optimization          scrubbing that compilers may remove (e.g., memset_s where
            (1.8%, dominated by CWE-14). Remaining cases are        available, or platform-provided secure-zero functions such as
            sparse or uncategorized.                                explicit_bzero/SecureZeroMemory).
    Java    Application security logic/policy (27.6%, input             Takeaway 9: Based on Table II, many high-frequency C
            validation, output encoding, auth configuration).       findings (e.g., TOCTOU and crypto/TLS misconfiguration) are
            Language-core error model exposure (27.1%, dom-
            inated by CWE-600). Standard runtime cryp-              attributed to platform and library layers rather than the C
            to/TLS surfaces (21.2%, dominated by CWE-327).          language-core, while true language-core risk remains concen-
            Language-core secret representation gaps (13.5%,        trated in memory and bounds handling (Table VII).
            dominated by CWE-259). XML/runtime configura-           Java: Security failures concentrate in exception bound-
            tion surfaces and other categories contribute the       aries and string-configured security APIs. Java’s managed
            remainder.
  Python    Generation-prone patterns and community idioms
                                                                    runtime reduces memory-corruption weaknesses, shifting risk
            (30.8%, e.g., placeholder constants and repeti-         toward configuration-heavy security and error-driven failures.
            tion). Language-core semantics (21.5%, e.g., default-   In Table VII, Java shows a strong error-handling contribution
            argument timing and string literal behavior rele-       dominated by CWE-600, indicating that LLM-generated code
            vant to injection). Application security logic/policy   often mishandles exceptional control flow (e.g., uncaught
            (21.5%). Ecosystem library/framework API permis-
            siveness (16.9%, dominated by CWE-327/329 pat-
                                                                    exceptions, overly broad catches, error propagation bypassing
            terns). Runtime/module-state exposure (9.2%).           checks). A second signal is hardcoded secrets (CWE-259),
                                                                    as security-sensitive values are expressed as string literals
                                                                    without a first-class secret type. Cryptographic weaknesses
smaller but important component. Java and Python shift toward       (CWE-327) persist because Java exposes algorithm and mode
exception boundaries, secret representation, configuration sur-     choices through string-based configuration (e.g., transforma-
faces, and permissive APIs. This explains why MA-CoT is             tion strings, provider selection), making insecure options easy
strongest in Java and Python, where weaknesses are largely          to select without guardrails.
configuration/API-driven, while C retains residual risk from        Java Strengthening Actions by Layer. The mitigation goal
OS/toolchain semantics and language-core memory issues.             varies by layer: ① Language-core error boundaries: Enforce
C: Separating language-core memory hazards from, li-                fail-closed exception handling, avoid catch-all swallowing,
brary, OS, and toolchain exposures. C shows a split between         ensure security checks and authorization decisions are not
language-core and language-stack risk. The language-core            bypassed on exceptional paths, and prevent sensitive inter-
driver is the lack of intrinsic bounds checking with pervasive      nal error details from leaking through exception messages.
raw buffers and pointer arithmetic, consistent with memory-         ② Secret representation and lifetime: Avoid embedding se-
safety CWEs (CWE-119/120) in Table VII. In contrast, several        crets as string literals or long-lived Strings (which cannot
high-frequency issues are not strictly C-specific (Table II):       be reliably cleared and are easily propagated). Prefer typed
(1) TOCTOU (CWE-367) stems from POSIX check-then-use                secret carriers where feasible (e.g., key objects, keystores, or
semantics and can arise in any language using the same OS           short-lived byte[] buffers with best-effort zeroization) and
APIs. (2) Cryptographic and TLS weaknesses are driven by            never log or include secrets in exception text. ③ Standard
library configuration surfaces (e.g., algorithm/mode selection,     runtime crypto/TLS surfaces: Constrain algorithm selection to
verification settings) rather than C syntax. (3) Secure wiping      modern AEAD by default and require cryptographically secure
failures (e.g., CWE-14 and related rules) stem from toolchain       randomness and standard KDFs for derived keys. For TLS, cer-
optimization when non-guaranteed zeroization is used.               tificate and hostname verifications are required, and verifica-
C Strengthening Actions by Layer. The mitigation target de-         tion-bypass patterns are forbidden. ④ Application/framework
pends on the layer (Table VII): ① Language-core (memory and         layer: Use output encoding or safe templating defaults to pre-
bounds): Prefer bounded abstractions (length-carrying buffers       vent CWE-79, validate all untrusted inputs to reduce CWE-20,
and checked wrappers), ban unbounded copies, and validate           and enforce authentication and password policies (CWE-521)
sizes at every boundary. Where feasible, adopt safer subsets        explicitly via configuration and centralized validation.
(e.g., CERT C / MISRA guidance) and enable sanitizers in            Python: Expressiveness amplifies configuration risk and
testing to expose overflow- and lifetime-related defects early.     parameter reuse. Python’s memory safety reduces low-
② Platform/OS API (TOCTOU): Avoid check-then-use flows              level memory-corruption risk, but cryptographic misuse and
and prefer atomic, descriptor-based patterns (open-and-check        input-driven vulnerabilities (e.g., insufficient validation, un-
rather than pre-check, fd (file descriptor)-based validation).      safe string construction) remain common. As shown in Ta-
Avoid separate existence checks and use primitives that re-         ble VII, Python weaknesses stem from permissive APIs and
duce race windows (e.g., openat, O_CREAT| O_EXCL,                   generation-prone idioms, alongside language-core semantics
                                                                                                                                11



that make insecure patterns concise (e.g., module-level state,     mitigation constraints, models often select insecure defaults
default-argument evaluation reusing values across calls). Mod-     while producing plausible explanations. In C, this effect is
els often encode security-critical parameters as copyable con-     amplified because added planning steps introduce check-then-
stants (e.g., static IVs/nonces, placeholder secrets), and many    use file flows and low-level plumbing, where TOCTOU and
APIs accept them without enforcing freshness or entropy. This      verification bypass patterns appear. In contrast, MA-CoT nar-
interaction motivates guidance requiring nonce/IV uniqueness,      rows these degrees of freedom by prescribing safe primitives
secure randomness, and non-literal secret sourcing.                and explicit prohibitions, reducing risky configurations.
Python Strengthening Actions by Layer. The following               Layered attribution explains the cross-language gap. The
actions target Python-specific risks across language and stack     layered attribution in subsection III-F clarifies why improve-
layers. ① Language-core semantics and state: Avoid mod-            ments differ by language. In C, residual risk is largely driven
ule-level security-critical constants and avoid default-argument   by language-stack layers, including OS-level filesystem se-
traps by requiring per-operation runtime initialization of non-    mantics (e.g., TOCTOU) and toolchain behavior (e.g., non-
ces/IVs/tokens using a CSPRNG. Treat all external inputs as        guaranteed wiping), which prompts alone cannot eliminate. In
untrusted and apply validation/encoding at security-sensitive      Java and Python, weaknesses are more configuration and API-
sinks (e.g., HTML output, command execution, and query             driven (crypto choices, exception boundaries, secret handling),
construction). ② Library/framework APIs: Prefer high-level         making them more responsive to MA-CoT constraints that
cryptographic APIs that enforce randomness and safe modes          enforce secure defaults and fail-closed behavior.
by construction; explicitly forbid insecure modes and static          Dataset shift explains why the same prompting strategy ap-
parameters (e.g., fixed IVs/nonces). For web frameworks,           pears moderate in one dataset and nearly eliminated in another.
require safe templating/auto-escaping by default and explicit      LLMSecEval emphasizes different task families (i.e., Java web
content-type handling.                                             patterns), whereas our dataset includes more systems-oriented
   Takeaway 10: Java and Python weaknesses are characterized       C scenarios; differences in raw counts reflect task composition
by configuration, exception boundaries, and API choices,           and language mix, not evaluation artifacts. Prompt effective-
so MA-CoT is most effective when it constrains these sur-          ness should be assessed by which CWE classes dominate in a
faces with secure defaults and fail-closed policies. C retains     benchmark, not only aggregate totals.
more residual risk because a larger fraction is driven by             Our study provides three practical and testable insights.
OS/toolchain semantics and language-core memory hazards,           ❶ treat prompt design as a security control (MA-CoT is
which require atomic OS patterns and secure-by-construction        consistently strongest, whereas generic CoT/Zero-shot is not
primitives in addition to prompt guidance.                         reliable); ❷ report severity and CWE distributions to avoid
   Takeaway 11: Language-core rules are necessary but in-          masking category shifts behind totals; and ❸ view residual
sufficient; secure generation must also include stack-level        MA-CoT findings as hardening opportunities best addressed
constraints (library defaults, OS-safe patterns, etc.).            with secure-by-construction primitives (i.e., guaranteed-wipe
                                                                   routines) rather than expecting the model to consistently
                                                                   implement subtle rules from memory.
                      VI. D ISCUSSION
   Our results suggest that LLM-generated code security de-                         VII. T HREATS TO VALIDITY
pends less on "more reasoning" and more on whether prompts         Construct. We measured security using SAST findings
provide actionable mitigations aligned with dominant weak-         (SonarQube rules), which capture likely weakness patterns
ness types. Across both datasets, MA-CoT was the most secure       but not exploitability. SAST is pattern-sensitive: some rules
method, while Zero-shot and CoT were unstable. This stability      trigger only for specific idioms. For example, c:S5798 rule
appears at the severity level: high-severity findings (Blocker     flags memset() before free() because the write may be
plus Critical) drop from 90 to 39 in the primary dataset           optimized away. MA-CoT introduces explicit scrubbing more
(56.7%) and from 45 to 2 in LLMSecEval (95.6%).                    often, increasing c:S5798 rule counts even when overall
   A key technical signal is that MA-CoT reduces recurring,        high-severity burden decreases. We interpret such cases as
high-impact CWE classes rather than totals alone. In the           implementation-level hardening signals and document reme-
primary dataset, C was dominated by CWE-295 and CWE-               diation (e.g., guaranteed-wipe primitives). To reduce false
327, and MA-CoT reduced both (CWE-295=6; CWE-327=2).               positives, two security researchers independently reviewed
Remaining issues shift toward implementation-level hardening       SonarQube findings and resolved disagreements by consensus.
(i.e., TOCTOU and secure wiping). This is most apparent in         Internal. LLM outputs vary with decoding, prompts, and
C, where the Blocker increase is driven by c:S5798 rule,           provider updates. We mitigated this by applying an identical
flagging insecure-erasure with memset() before free()              generation and analysis pipeline across models and prompting
due to compiler optimization; the net high-severity burden still   methods and using the same analyzer configuration per dataset.
decreases (52 to 31). The appendix provides a concrete cross-      External. The evaluation covered three languages, three mod-
language illustration of this mechanism for a representative       els, and two datasets. While the benchmark provides an exter-
encryption task.                                                   nal check, results may differ for other languages, domains, or
Why generic CoT can increase findings (especially in C).           task mixes emphasizing different CWE families. Our claims
The underperformance of generic CoT is not accidental. CoT         are therefore comparative: under tested conditions, MA-CoT
expands intermediate design choices, and without concrete          is more reliable than Vanilla, Zero-shot, and CoT.
                                                                                                                                                          12



Conclusion. Aggregated counts can hide variance across tasks                   [2] J. Lin and D. Mohaisen, “From large to mammoth: A comparative
and mask category shifts. To improve interpretability, we                          evaluation of large language models in vulnerability detection,” in 32nd
                                                                                   Annual Network and Distributed System Security Symposium, NDSS
reported totals alongside severity and CWE distributions and                       2025, San Diego, California, USA, February 24-28, 2025. The Internet
used expert reviews to validate the findings and explain rule-                     Society, 2025.
level effects rather than using aggregate metrics alone.                       [3] O. Asare, M. Nagappan, and N. Asokan, “A user-centered security
                                                                                   evaluation of copilot,” in ICSE, 2024.
                                                                               [4] M. B. Messaoud, A. Miladi, I. Jenhani, M. W. Mkaouer, and L. Ghadhab,
           VIII. C ONCLUSION AND F UTURE W ORK                                     “Duplicate bug report detection using an attention-based neural language
                                                                                   model,” IEEE Trans. Reliab., vol. 72, no. 2, pp. 846–858, 2023.
   This study evaluates mitigation-aware prompting for secure                      [Online]. Available: https://doi.org/10.1109/TR.2022.3193645
code generation across three LLMs, three languages (C, Java,                   [5] I. Medeiros, N. Neves, and M. Correia, “Statically detecting
                                                                                   vulnerabilities by processing programming languages as natural
Python), and four prompting strategies on a 200-task primary                       languages,” IEEE Trans. Reliab., vol. 71, no. 2, pp. 1033–1056, 2022.
dataset, with external validation on LLMSecEval. The key                           [Online]. Available: https://doi.org/10.1109/TR.2021.3137314
finding is that mitigation-aware prompting (MA-CoT) yields                     [6] N. O. Jaffal, M. Alkhanafseh, and D. Mohaisen, “Large language
                                                                                   models in cybersecurity: A survey of applications, vulnerabilities, and
the most reliable security improvements and generalizes under                      defense techniques,” AI, vol. 6, no. 9, 2025. [Online]. Available:
dataset shift. In the primary dataset, high-severity findings                      https://www.mdpi.com/2673-2688/6/9/216
(Blocker + Critical) decreased from 90 to 39 (56.7%) across                    [7] —, “Adoption of developer ai tools (copilot, etc) 2022 -
                                                                                   2025: Data & graphs show increase in ai use as developers
all models and languages. On LLMSecEval, high-severity                             evolve - gitclear,” 12 2025, [Online; accessed 2025-12-27].
findings dropped from 45 to 2 (95.6%), and total findings                          [Online]. Available: https://www.gitclear.com/research/developer_ai_
from 73 to 4 (94.5%). These results indicate that: (RQ1) MA-                       assistant_adoption_by_year_with_ai_delegation_buckets
                                                                               [8] B. Yetistiren, I. Özsoy, M. Ayerdem, and E. Tüzün, “Evaluating the
CoT consistently outperforms baselines; (RQ2) improvements                         code quality of ai-assisted code generation tools: An empirical study
hold across languages and models; and (RQ3) residual risk                          on github copilot, amazon codewhisperer, and chatgpt,” CoRR, vol.
concentrates in narrower hardening-oriented CWE patterns.                          abs/2304.10778, 2023.
                                                                               [9] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri, “Asleep
   A practical contribution of this work is the distinction                        at the keyboard? assessing the security of github copilot’s code contri-
between language-core and language-stack causes, which pre-                        butions,” in IEEE Symp. on Security & Privacy, 2022.
vents overstatement of what is truly “language-specific.” This                [10] Y. Fu, P. Liang, A. Tahir, Z. Li, M. Shahin, J. Yu, and J. Chen, “Security
                                                                                   weaknesses of copilot-generated code in github projects: An empirical
distinction is critical for mitigation: language-core issues de-                   study,” CoRR, vol. abs/2310.02059, 2025.
mand safer constructs and bounded memory handling, whereas                    [11] G. Sandoval, H. Pearce, T. Nys, R. Karri, S. Garg, and B. Dolan-Gavitt,
stack-driven issues require secure-by-default libraries, OS-                       “Lost at c: A user study on the security implications of large language
                                                                                   model code assistants,” in Proceedings of the 32nd USENIX Security
atomic file patterns, and toolchain-safe primitives. Positioning                   Symposium, 2023, pp. 2205–2222.
mitigation at the appropriate layer transforms cross-language                 [12] O. Asare, M. Nagappan, and N. Asokan, “Is github’s copilot
comparisons into actionable guidance, enhancing system reli-                       as bad as humans at introducing vulnerabilities in code?” Empir.
                                                                                   Softw. Eng., vol. 28, no. 6, p. 129, 2023. [Online]. Available:
ability rather than yielding broad claims.                                         https://doi.org/10.1007/s10664-023-10380-1
   Beyond aggregate reductions, the results clarify what                      [13] S. Ullah, M. Han, S. Pujar, H. Pearce, A. Coskun, and G. Stringhini,
changes. MA-CoT removes recurring high-risk patterns while                         “Llms cannot reliably identify and reason about security vulnerabilities
                                                                                   (yet?): A comprehensive evaluation, framework, and benchmarks,” in
shifting residual issues toward implementation-level harden-                       IEEE Symposium on Security and Privacy, 2024.
ing. In C, the net high-severity burden decreases (52 to 31)                  [14] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi,
even though Blocker increases due to strict secure-erasure                         Q. V. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning
                                                                                   in large language models,” in Proceedings of the 36th Conference on
enforcement (dominated by c:S5798 rule), which flags                               Neural Information Processing Systems (NeurIPS), 2022.
non-guaranteed wiping with memset. At the model level,                        [15] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa,
Table VI shows that responsiveness to mitigation guidance                          “Large language models are zero-shot reasoners,” in Advances in
                                                                                   Neural Information Processing Systems 35: Annual Conference on
varies (i.e.,claude-4.5 benefits strongly, while gpt-5 is                          Neural Information Processing Systems 2022, NeurIPS 2022, New
more stable on the primary dataset), reinforcing that model                        Orleans, LA, USA, November 28 - December 9, 2022, S. Koyejo,
selection and prompting policy should be evaluated jointly for                     S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, Eds.,
                                                                                   2022. [Online]. Available: http://papers.nips.cc/paper_files/paper/2022/
dependable code generation.                                                        hash/8bb0d291acd4acf06ef112099c16f326-Abstract-Conference.html
   For researchers, the main contribution is evidence that                    [16] C. Tony, N. E. D. Ferreyra, M. Mutas, S. Dhif, and R. Scandariato,
prompt design is a first-order reliability control: generic                        “Prompting techniques for secure code generation: A systematic
                                                                                   investigation,” ACM TOSEM, vol. 34, no. 8, pp. 225:1–225:53, 2025.
prompting and unguided reasoning are inconsistent, whereas                         [Online]. Available: https://doi.org/10.1145/3722108
mitigation-aware constraints yield consistent reductions across               [17] M. Kharma, A. Sabbah, M. AlKhanafseh, M. Hammoudeh, and D. Mo-
datasets. Future work should extend evaluation beyond static                       haisen, “An empirical evaluation of llm-generated code security across
                                                                                   prompting methods,” 2026, submitted to Empirical Software Engineer-
analysis by combining static and dynamic validation and                            ing.
standardizing secure-by-construction primitives and wrappers                  [18] C. An, J. Zhang, M. Zhong, L. Li, S. Gong, Y. Luo, J. Xu, and L. Kong,
(e.g., guaranteed wiping, safe file-open patterns) to eliminate                    “Why does the effective context length of llms fall short?” CoRR, vol.
                                                                                   abs/2410.18745, 2024.
residual hardening-oriented failure modes under MA-CoT.                       [19] S.-C. Dai, J. Xu, and G. Tao, “Rethinking the evaluation of secure code
                                                                                   generation,” 2025. [Online]. Available: https://arxiv.org/abs/2503.15554
                             R EFERENCES                                      [20] D. Cotroneo, R. D. Luca, and P. Liguori, “Devaic: A tool for security
                                                                                   assessment of ai-generated code,” Inf. Softw. Technol., vol. 177, p.
 [1] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. de Oliveira Pinto, J. Kaplan,         107572, 2025. [Online]. Available: https://doi.org/10.1016/j.infsof.2024.
     H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large        107572
     language models trained on code,” arXiv preprint arXiv:2107.03374,       [21] B. Lin, S. Wang, Y. Qin, L. Chen, and X. Mao, “Give llms a
     2021.                                                                         security course: Securing retrieval-augmented code generation via
                                                                                                                                                     13



     knowledge injection,” in CCS, C. Huang, J. Chen, S. Shieh, D. Lie,            Canada, May 3, 2025. IEEE, 2025, pp. 33–40. [Online]. Available:
     and V. Cortier, Eds. ACM, 2025, pp. 3356–3370. [Online]. Available:           https://doi.org/10.1109/LLM4Code66737.2025.00009
     https://doi.org/10.1145/3719027.3765049                                  [40] M. Vero, N. Mündler, V. Chibotaru, V. Raychev, M. Baader,
[22] N. Huynh and B. Lin, “Large language models for code generation:              N. Jovanovic, J. He, and M. T. Vechev, “Baxbench: Can llms generate
     A comprehensive survey of challenges, techniques, evaluation, and             correct and secure backends?” in ICML. OpenReview.net, 2025.
     applications,” CoRR, vol. abs/2503.01245, 2025. [Online]. Available:          [Online]. Available: https://openreview.net/forum?id=il3KRr4H9u
     https://doi.org/10.48550/arXiv.2503.01245                                [41] J. Chen, H. Huang, Y. Lyu, J. An, J. Shi, C. Yang, T. Zhang,
[23] J. H. Klemmer, S. A. Horstmann, N. Patnaik, C. Ludden, C. B.                  H. Tian, Y. Li, Z. Li, X. Zhou, X. Hu, and D. Lo, “Secureagentbench:
     Jr., C. Powers, F. Massacci, A. Rahman, D. Votipka, H. R. Lipford,            Benchmarking secure code generation under realistic vulnerability
     A. Rashid, A. Naiakshina, and S. Fahl, “Using AI assistants in                scenarios,” CoRR, vol. abs/2509.22097, 2025. [Online]. Available:
     software development: A qualitative study on security practices and           https://doi.org/10.48550/arXiv.2509.22097
     concerns,” in CCS. ACM, 2024, pp. 2726–2740. [Online]. Available:        [42] —, “Gpt-5 model | openai api,” https://platform.openai.com/docs/
     https://doi.org/10.1145/3658644.3690283                                       models/gpt-5, 09 2025, (Accessed on 2025-09-24).
[24] N. Tihanyi, T. Bisztray, M. A. Ferrag, R. Jain, and L. C. Cordeiro,      [43] ——, “What’s new in claude 4.5 - claude doc,” https://platform.claude.
     “How secure is ai-generated code: a large-scale comparison of large           com/docs/en/about-claude/models/whats-new-claude-4-5, 09 2025, (Ac-
     language models,” Empir. Softw. Eng., vol. 30, no. 2, p. 47, 2025.            cessed on 2025-09-24).
     [Online]. Available: https://doi.org/10.1007/s10664-024-10590-1          [44] ——, “Gemini models | gemini api | google ai for developers,” https:
[25] P. Sahoo, A. K. Singh, S. Saha, V. Jain, S. Mondal, and A. Chadha,            //ai.google.dev/gemini-api/docs/models, 09 2025, (Accessed on 2025-
     “A systematic survey of prompt engineering in large language models:          09-24).
     Techniques and applications,” CoRR, vol. abs/2402.07927, 2024.           [45] ——, “Code quality, security & static analysis tool with SonarQube,”
     [Online]. Available: https://doi.org/10.48550/arXiv.2402.07927                https://www.sonarsource.com/products/sonarqube/, 05 2024, (Accessed
[26] B. Chen, Z. Zhang, N. Langrené, and S. Zhu, “Unleashing the potential         on 05/12/2024).
     of prompt engineering in large language models: a comprehensive          [46] C. Tony, M. Mutas, N. E. D. Ferreyra, and R. Scandariato,
     review,” CoRR, vol. abs/2310.14735, 2023. [Online]. Available:                “Llmseceval: A dataset of natural language prompts for security
     https://doi.org/10.48550/arXiv.2310.14735                                     evaluations,” in MSR. IEEE, 2023, pp. 588–592. [Online]. Available:
[27] E. Basic and A. Giaretta, “Large language models and code security:           https://doi.org/10.1109/MSR59073.2023.00084
     A systematic literature review,” CoRR, vol. abs/2412.15004, 2024.        [47] M. Bruni, F. Gabrielli, M. Ghafari, and M. Kropp, “Benchmarking
     [Online]. Available: https://doi.org/10.48550/arXiv.2412.15004                prompt engineering techniques for secure code generation with
[28] A. Schaad, S. Götz, and D. Binder, “You still have to study on                GPT models,” in Forge@ICSE. IEEE, 2025, pp. 93–103. [Online].
     the security of LLM generated code,” in ICT Systems Security                  Available: https://doi.org/10.1109/Forge66646.2025.00018
     and Privacy Protection - 40th IFIP International Conference, SEC         [48] M. L. Siddiq, J. C. da Silva Santos, S. Devareddy, and A. Muller,
     2025, Maribor, Slovenia, May 21-23, 2025, Proceedings, Part II,               “SALLM: security assessment of generated code,” in ASE Workshops.
     ser. IFIP Advances in Information and Communication Technology,               ACM, 2024, pp. 54–65. [Online]. Available: https://doi.org/10.1145/
     L. N. Zlatolas, K. Rannenberg, T. Welzer, and J. García-Alfaro,               3691621.3694934
     Eds., vol. 746. Springer, 2025, pp. 111–124. [Online]. Available:        [49] S. Liu, B. Sabir, S. I. Jang, Y. Kansal, Y. Gao, K. Moore,
     https://doi.org/10.1007/978-3-031-92886-4_8                                   A. Abuadbba, and S. Nepal, “From solitary directives to interactive
[29] A. Datta, A. Aljohani, and H. Do, “Secure code generation at scale            encouragement! LLM secure code generation by natural language
     with reflexion,” CoRR, vol. abs/2511.03898, 2025. [Online]. Available:        prompting,” CoRR, vol. abs/2410.14321, 2024. [Online]. Available:
     https://doi.org/10.48550/arXiv.2511.03898                                     https://doi.org/10.48550/arXiv.2410.14321
[30] G. Kim, P. Baldi, and S. McAleer, “Language models can solve computer
     tasks,” in Proceedings of the 37th Conference on Neural Information
     Processing Systems (NeurIPS), 2023.
                                                                                                       A PPENDIX A
[31] J. Li, F. Rabbi, B. Yang, S. Wang, and J. Yang, “Secure-instruct:            E XAMPLE E NTRIES FROM THE M ITIGATION -AWARE
     An automated pipeline for synthesizing instruction-tuning datasets                                  DATASET
     using llms for secure code generation,” 2025. [Online]. Available:
     https://arxiv.org/abs/2510.07189                                            This appendix provides two representative records from the
[32] J. Shi and T. Zhang, “RESCUE: retrieval augmented secure code            Mitigation-Aware dataset. Each entry connects a category to
     generation,” CoRR, vol. abs/2510.18204, 2025. [Online]. Available:
     https://doi.org/10.48550/arXiv.2510.18204
                                                                              its mitigation rules, language-specific guidance, code review
[33] J. Zhao, Y. Sun, C. Huang, C. Liu, Y. Guan, Y. Zeng, and Y. Liu,         checklist, and fine-tuning examples. The format shows how
     “Towards secure code generation with llms: A study on common             the dataset structures both general and implementation-level
     weakness enumeration,” IEEE Transactions on Software Engineering,
     vol. 51, no. 12, pp. 3507–3523, 2025.
                                                                              secure-coding practices.
[34] M. Nazzal, I. Khalil, A. Khreishah, and N. Phan, “Promsec: Prompt
     optimization for secure generation of functional source code with        A. Example 1: Language Basics
     large language models (llms),” in CCS. ACM, 2024, pp. 2266–2280.
     [Online]. Available: https://doi.org/10.1145/3658644.3690298             Scope. Baseline security and quality rules.
[35] Y. Nong, M. Aldeen, L. Cheng, H. Hu, F. Chen, and H. Cai,                Applicable Languages. Language-agnostic.
     “Chain-of-thought prompting of large language models for discovering
     and fixing software vulnerabilities,” CoRR, vol. abs/2402.17230, 2024.
                                                                              General Rules.
     [Online]. Available: https://doi.org/10.48550/arXiv.2402.17230             • Default to secure coding patterns. Treat all inputs as
[36] X. Jiang, Y. Dong, L. Wang, Z. Fang, Q. Shang, G. Li, Z. Jin, and            untrusted and fail closed with clear error messages.
     W. Jiao, “Self-planning code generation with large language models,”
     ACM Trans. Softw. Eng. Methodol., vol. 33, no. 7, pp. 182:1–182:30,        • Validate type, length, range, and encoding. Sanitize or
     2024. [Online]. Available: https://doi.org/10.1145/3672456                   reject early. Normalize paths and prevent traversal.
[37] M. F. Kharma, S. Choi, M. Alkhanafseh, and D. Mohaisen,                    • Never hard code passwords or secrets. Use configuration
     “Security and quality in llm-generated code: a multi-language,
     multi-model analysis,” IEEE Transactions on Dependable and Secure            files or a secret manager.
     Computing, no. 01, pp. 1–15, 2026. [Online]. Available: https:             • Avoid dynamic code loading and insecure deserialization.
     //doi.org/10.1109/TDSC.2026.3672745                                        • Use trusted cryptographic libraries. Prefer AEAD (AES-
[38] M. U. Shahid, C. M. Ahmed, and R. Ranjan, “Llm-csec: Empirical
     evaluation of security in c/c++ code generated by large language             GCM or ChaCha20-Poly1305). Derive keys with Ar-
     models,” 2025. [Online]. Available: https://arxiv.org/abs/2511.18966         gon2id, scrypt, or PBKDF2-HMAC-SHA-256 using
[39] J. Peng, L. Cui, K. Huang, J. Yang, and B. Ray, “Cweval:                     unique salts.
     Outcome-driven evaluation on functionality and security of LLM
     code generation,” in IEEE/ACM International Workshop on Large              • Enforce TLS 1.2 or TLS 1.3 with certificate and hostname
     Language Models for Code, LLM4Code@ICSE 2025, Ottawa, ON,                    verification.
                                                                                                                              14



  • Use safe file operations, atomic writes, and restrictive      B. Example 2: Cryptography
    permissions.                                                  Scope. Encryption, hashing, key management, and TLS usage.
  • Maintain memory safety by checking allocation results,        Applicable Languages. Language-agnostic.
    bounding copies, ensuring null termination, and freeing       Additional Tag. Data safety and security.
    memory exactly once.                                          General Rules.
  • Zeroize sensitive data with a reliable API before freeing
                                                                     • Use vetted cryptographic libraries and modern algo-
    memory.                                                             rithms. Never implement cryptography manually.
  • Never log secrets, tokens, or plaintext. Use constant
                                                                     • Ban MD5, SHA-1, DES/3DES, RC4, and ECB
    format strings and redact sensitive data.                           mode. Use AEAD encryption (AES-GCM/ChaCha20-
  • Prevent internal error details from leaking to external
                                                                        Poly1305).
    users.                                                           • Derive keys with Argon2id, scrypt, or PBKDF2-HMAC-
  • Use atomic operations and thread-safe APIs to prevent
                                                                        SHA-256 and a random salt.
    race conditions.                                                 • Use secure random generators for keys, salts, and nonces.
  • Enable compiler hardening flags, run static analysis, and
                                                                        For RSA, prefer OAEP (≥2048 bits) or modern curves
    verify dependencies.                                                (X25519, Ed25519).
  • Limit network activity to secure protocols and minimal
                                                                     • Enforce TLS 1.2 or TLS 1.3 and never disable certificate
    exposure.                                                           validation.
Language-Specific Guidance.                                       Language-Specific Guidance. C - use OpenSSL EVP, lib-
   C - avoid gets, strcpy, sprintf, and unbounded                 sodium, or Botan for encryption, KDFs, and random genera-
scanf. Use fgets and snprintf, check return values, use           tion. When using libcurl:
one cleanup label, and clear secrets with memset_s. Enforce
TLS verification when using libcurl.                              curl_easy_setopt(curl,
   C++ - prefer std::string, std::vector, RAII, and                       CURLOPT_SSL_VERIFYPEER, 1L);
smart pointers. Use std::span for safe access and avoid           curl_easy_setopt(curl,
std::rand for security.                                                   CURLOPT_SSL_VERIFYHOST, 2L);
                                                                  curl_easy_setopt(curl, CURLOPT_SSLVERSION,
   Python - use context managers and type hints.
                                                                              CURL_SSLVERSION_TLSv1_2
Prefer the secrets module and the cryptography
                                                                              | CURL_SSLVERSION_MAX_TLSv1_3);
library. Avoid eval and unsafe pickle. Use
ssl.create_default_context with TLS 1.2+                          Check return values, use bounds-checked buffers, clear key
and enable certificate checks.                                    material with memset_s, and never disable certificate checks.
   Java - use StandardCharsets.UTF_8 and try-                       C++ - use vetted cryptographic libraries. Ensure HTTP-
with-resources. Apply safe deserialization patterns.              S/TLS clients enforce TLS 1.2+ with hostname verification
For encryption, use AES/GCM /NoPadding with                       and avoid deprecated cipher suites.
GCMParameterSpec(128, iv) and derive keys via                       Python - use the cryptography library. Enforce TLS 1.2
PBKDF2WithHmacSHA256. Never disable certificate                   or higher:
validation.                                                        1   import ssl
Code Review Checklist. Inputs validated; no hard coded se-         2   ctx = ssl.create_default_context()
crets; no unsafe reflection or insecure deserialization; modern    3   ctx.check_hostname = True
KDFs and AEAD in crypto; TLS verification enforced; safe           4   ctx.verify_mode = ssl.CERT_REQUIRED
                                                                   5   if hasattr(ssl, "TLSVersion"):
file operations; logs redact sensitive data; no internal error     6       ctx.minimum_version = ssl.TLSVersion.
leakage; memory and overflow checks present; concurrency                       TLSv1_2
hazards mitigated; build hardening flags and testing active.       7   else:
Fine-tuning examples. Generic - respond to any request to          8       ctx.options |= ssl.OP_NO_SSLv2 | ssl.
hard code a password by showing secure credential handling                     OP_NO_SSLv3
                                                                   9       ctx.options |= ssl.OP_NO_TLSv1 | ssl.
with environment variables or a secret manager.                                OP_NO_TLSv1_1
   Python -
                                                                    Java    -   use    Cipher("AES/GCM/NoPadding")
token = random.random()                                           with    GCMParame -terSpec(128, iv).      Generate
requests.get(url, verify=false)                                   IVs and salts with SecureRandom, derive keys using
Secure alternative: use secrets.token_urlsafe for ran-            PBKDF2WithHmacSHA256, use try-with-resources, and
domness and a verified SSL context enforcing TLS 1.2 or           enforce TLS 1.2 or higher.
higher.
   Java - authenticated encryption with proper IV han-                                 A PPENDIX B
dling. Use AES/GCM with a 12-byte random IV from                   I NTERPRETING C :S5798 RULE IN MA-C OT C O UTPUTS
SecureRandom, paired with GCMParameterSpec(128,                   What c:S5798 rule Reports. c:S5798 rule (“memset
iv), and keys derived via PBKDF2-HMAC-SHA-256 with a              should not be used to delete sensitive data”) flags cases
unique salt.                                                      where a program attempts to scrub a buffer using memset()
                                                                     15



immediately before destroying it (i.e., via free()). The
warning reflects that such writes may be removed by compiler
optimization, so the intended zeroization is not guaranteed.
Why Vanilla Can Appear "cleaner". Vanilla triggered
c:S5798 rule zero times in our reports because it typi-
cally does not introduce explicit buffer-scrubbing calls (i.e.,
memset() before free()), which are the specific patterns
targeted by the rule. The absence of c:S5798 rule findings
should not be interpreted as a guarantee of secure data lifetime
handling, as it only indicates that the insecure-erasure pattern
is not present.
Actionable Remediation. When explicit zeroization is re-
quired, memset() should be replaced with a guaranteed-wipe
primitive (i.e., memset_s where available, or an equivalent
secure-zero routine) so that scrubbing cannot be optimized
away. This removes c:S5798 rule while preserving the
intended defense, and explains why MA-CoT can reduce high-
severity findings while shifting a small subset of residual issues
into Blocker due to strict secure-erasure rules.
                         A PPENDIX C
 C ROSS -P ROMPT AND C ROSS -L ANGUAGE C ODE S NIPPETS
                  FOR O NE TASK E XAMPLE
   This appendix provides a qualitative case study to com-
plement the aggregate results in section V. We select one
representative task from the primary dataset (Task 79: Encrypt
a Message Using Secret Key, associated with CWE-327) and
show code snippets generated by claude-4.5 across all
prompting methods (Vanilla, ZeroShot, CoT, and MA-CoT)
and three programming languages (Java, Python, and C). The
goal is to illustrate how prompt design changes concrete
security-relevant implementation choices (e.g., cipher mode,
key derivation, IV handling, and cleanup behavior), which
aligns with the CWE-level findings.

A. Task and Setup
Task. Task 79 asks the model to create a cipher and encrypt
a message using a secret key.
Scope. All snippets referenced in this appendix were generated
by claude-4.5 for the same task under the four prompting
methods evaluated in this paper. The snippets are reproduced
as generated and are shown as excerpts to highlight security-
relevant implementation choices. To preserve space, the full
code snippets are available at GitHub.

B. Takeaways
   The analysis provided in this section mirrors the aggregate
CWE findings in section V-D: Vanilla and ZeroShot often
preserve insecure cryptographic defaults (e.g., ECB), CoT
improves structure but may still use non-AEAD modes (e.g.,
CBC), and MA-CoT consistently shifts implementations to-
ward AEAD-based designs with stronger parameter handling.
   The change under MA-CoT is not only stylistic. It alters
implementation choices that directly affect security (cipher
mode, Key Derivation Function (KDF) usage, random salt/IV
generation, validation, and secure cleanup), which explains
the observed reductions in recurring cryptographic weakness
patterns.
