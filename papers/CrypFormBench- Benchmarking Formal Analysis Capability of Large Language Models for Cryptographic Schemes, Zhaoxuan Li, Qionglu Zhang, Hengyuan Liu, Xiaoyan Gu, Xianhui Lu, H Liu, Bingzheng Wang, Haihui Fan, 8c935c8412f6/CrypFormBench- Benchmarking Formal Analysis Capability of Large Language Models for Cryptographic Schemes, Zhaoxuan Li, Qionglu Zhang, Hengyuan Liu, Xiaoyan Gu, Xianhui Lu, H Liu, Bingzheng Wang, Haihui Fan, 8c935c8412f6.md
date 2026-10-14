                                         CrypFormBench: Benchmarking Formal Analysis Capability
                                         of Large Language Models for Cryptographic Schemes
                                         ZHAOXUAN LI, Institute of Information Engineering, CAS, China
                                         QIONGLU ZHANG, Institute of Information Engineering, CAS, China
                                         HENGYUAN LIU, Institute of Information Engineering, CAS, China
                                         XIAOYAN GU, Institute of Information Engineering, CAS, China
                                         XIANHUI LU, Institute of Information Engineering, CAS, China
arXiv:2606.25561v1 [cs.CR] 24 Jun 2026




                                         HONGBO LIU, Institute of Information Engineering, CAS, China
                                         BINGZHENG WANG, Institute of Information Engineering, CAS, China
                                         HAIHUI FAN, Institute of Information Engineering, CAS, China
                                         ZIMING ZHAO, Zhejiang University, China
                                         RUI ZHANG, Institute of Information Engineering, CAS, China
                                         LI ZHOU, Institute of Software, CAS, China
                                         Manual formal analysis of cryptographic schemes is labor-intensive and requires substantial expertise. While
                                         model-checking tools (e.g., Scyther and Tamarin) and computational-security tools (e.g., CryptoVerif and
                                         EasyCrypt) improve the automation of security proofs, they still rely on experts to abstract schemes and
                                         write tool-specific formal descriptions. Large language models (LLMs) are a promising alternative, but their
                                         effectiveness in this domain remains unexplored due to the absence of standardized evaluation methodologies.
                                         To fill this gap, we introduce CrypFormBench (C.F.B for short), a comprehensive benchmark jointly cover-
                                         ing symbolic and computational security to evaluate five core LLM capabilities: interpretation, generation,
                                         completion, transformation, and correction. It comprises 700 instances spanning 677 schemes, 7 mainstream
                                         formal verifier languages, and 160 security properties. The evaluation of 9 state-of-the-art LLMs reveals
                                         that most of them perform well on interpretation and completion, given their code-awareness advantages,
                                         but struggle with generation, transformation, and correction. Overall, their performance remains limited,
                                         with Claude-3.5 achieving the highest score at 48.7 out of 100. We further provide practical guidance, e.g.,
                                         few-shot prompting, Pass@K sampling, and lightweight fine-tuning, to mitigate the executability bottleneck
                                         and improve tool-usable outputs. Taken together, our benchmark and analyses offer a grounded view of
                                         current progress and concrete directions toward reliable LLM-assisted formal cryptographic analysis.

                                         Authors’ Contact Information: Zhaoxuan Li, State Key Laboratory of Cyberspace Security Defense, Institute of Information
                                         Engineering, CAS, Beijing, China, lizhaoxuan@iie.ac.cn; Qionglu Zhang, State Key Laboratory of Cyberspace Security
                                         Defense, Institute of Information Engineering, CAS, Beijing, China, zhangqionglu@iie.ac.cn; Hengyuan Liu, State Key
                                         Laboratory of Cyberspace Security Defense, Institute of Information Engineering, CAS, Beijing, China, liuhengyuan@iie.ac.
                                         cn; Xiaoyan Gu, State Key Laboratory of Cyberspace Security Defense, Institute of Information Engineering, CAS, Beijing,
                                         China, guxiaoyan@iie.ac.cn; Xianhui Lu, State Key Laboratory of Cyberspace Security Defense, Institute of Information
                                         Engineering, CAS, Beijing, China, luxianhui@iie.ac.cn; Hongbo Liu, State Key Laboratory of Cyberspace Security Defense,
                                         Institute of Information Engineering, CAS, Beijing, China, liuhongbo@iie.ac.cn; Bingzheng Wang, State Key Laboratory
                                         of Cyberspace Security Defense, Institute of Information Engineering, CAS, Beijing, China, wangbingzheng@iie.ac.cn;
                                         Haihui Fan, State Key Laboratory of Cyberspace Security Defense, Institute of Information Engineering, CAS, Beijing, China,
                                         fanhaihui@iie.ac.cn; Ziming Zhao, Zhejiang University, Hangzhou, China, zhaoziming@zju.edu.cn; Rui Zhang, State Key
                                         Laboratory of Cyberspace Security Defense, Institute of Information Engineering, CAS, Beijing, China, zhangrui@iie.ac.cn;
                                         Li Zhou, Institute of Software, CAS, Beijing, China, zhouli@ios.ac.cn.




                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM 2994-970X/2026/7-ARTFSE177
                                         https://doi.org/10.1145/3808184


                                                                               Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:2                    Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou


CCS Concepts: • Software and its engineering → Formal language definitions; • Theory of computation
→ Formal languages and automata theory; • Security and privacy → Formal security models.

Additional Key Words and Phrases: Formal analysis, cryptographic schemes, LLMs, and benchmark

ACM Reference Format:
Zhaoxuan Li, Qionglu Zhang, Hengyuan Liu, Xiaoyan Gu, Xianhui Lu, Hongbo Liu, Bingzheng Wang, Haihui
Fan, Ziming Zhao, Rui Zhang, and Li Zhou. 2026. CrypFormBench: Benchmarking Formal Analysis Capability
of Large Language Models for Cryptographic Schemes. Proc. ACM Softw. Eng. 3, FSE, Article FSE177 (July 2026),
23 pages. https://doi.org/10.1145/3808184


1   Introduction
Verifying the security of cryptographic schemes and primitives is a long-standing but challenging
task in formal methods [5, 47, 48]. Even widely deployed schemes such as TLS [22], 5G-AKA [9],
SSH [67], and OAuth 2.0 [35] have exhibited subtle flaws discovered years after deployment [46,
53]. Automated formal methods provide a rigorous way to uncover such vulnerabilities before
deployment. Existing approaches fall into two categories: (i) model-checking tools (e.g., Scyther [21],
AVISPA [4], ProVerif [11], and Tamarin [51]) for symbolic verification, and (ii) computational
frameworks (e.g., CryptoVerif [12] and EasyCrypt [8]) for cryptographic proof-level assurance.
   Nevertheless, these methods require substantial manual effort: abstracting scheme logic into spe-
cialized, error-prone, and tool-compatible languages (e.g., HLPSL and applied 𝜋-calculus) demands
expertise in both cryptography and formal specification. This bottleneck motivates exploring large
language models (LLMs) [40, 68] to assist in formal analysis by automatically deriving formal
specifications from natural-language descriptions, as depicted in Fig. 1. The current LLMs, particu-
larly code-oriented variants, have shown promising capabilities in code generation [15], symbolic
reasoning [14], and even guiding proof assistants like Coq [10] and Lean [6, 65, 66]. Yet crypto-
graphic scheme specifications remain a uniquely challenging domain due to their combination of
strict syntax, security-critical semantics, and long contextual dependencies, where small errors
can break verification. Prior studies indicate that LLMs often struggle with such highly structured,
domain-specific languages [5, 30], and may miss critical information in long inputs [45]. Thus, their
end-to-end formal capability for formal cryptographic analysis remains unclear.
   Recently, a preliminary benchmark [49] was proposed to evaluate automatic modeling tasks that
support only symbolic security, with 18 real-world protocols and excluding computational security,
advanced primitives, and diverse threat models. Unlike general-purpose code benchmarks [15, 36],
constructing a benchmark for cryptographic scheme analysis poses unique challenges: complex
semantics, multiple formal languages, and various adversarial assumptions. These gaps call for a
more comprehensive and systematic evaluation framework.
   To address these challenges, we design CrypFormBench (C.F.B for short), the first benchmark
that jointly covers symbolic and computational security, providing a unified platform for evaluating
LLMs in cryptographic scheme analysis. It spans five core tasks, namely interpretation, generation,
completion, transformation, and correction, reflecting the essential capabilities required for tool-usable
formal specification. It includes 700 curated instances (filtered from 4549 projects on GitHub or web
sources) across seven verifiers’ languages, covering 677 schemes and 160 security properties, from
classical authentication scenarios to modern MPC, ZK, and post-quantum designs. Furthermore, we
built an automated evaluation pipeline that standardizes model interactions, integrates cross-tool
verification, and applies a multidimensional scoring framework that combines task-level metrics
with overall rankings. This enables scalable and fine-grained assessment of LLM performance.
   In summary, we make the following main contributions.

Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                                                                                                                                      FSE177:3


                Crypto Scheme Doc                             Formal Models                                                                                    Protocol Verifiers
            Primitives (Signature, PKE)
               Zero Knowledge Proof                                                                                                                                                              Formal model is the first
           Authentication & Key Exchange                                                                                                                                                       step for scheme verification,
               Secure Communication                                                                                                                                                            but it is labour-intensive and
                                                               Symbolic Security
                   Access Control                           Computational Security
                                                                                                                                                                                                        difficult for me.
                Anonymity & Voting                                                                                                                                                              Q1: Can LLMs help me?
                              …

                                                                                                                                                                                                 A: Yes, but they need
               Classical &        Simple &                  Verified     Adversary                                                                        Attack                   Security
               Emerging           Complex                  Properties    Capabilities                                                                     Paths                     Proof         to be strengthened.

               LLM Comparison                        Formal Model Benchmark for LLMs                                                                                         Q2: Why and how?        Large Language Models
          Model A    Interpretation Completion                                                             Small schemes         Medium schemes       Large schemes



          Model B
                                                        Interpretation                       700

                                                                                             600                                                                              A: The first step is
                                                                                                                                                                                to construct a

                                                                           Instance counts
          Model C
                                                                                             500


                    Overall             Correction       Generation                          400

          Model D
          Model E                                       Completion
                                                                                             300

                                                                                             200
                                                                                                                                                                                 formal model
           …        Generation     Transformation
                                                                                             100
                                                                                                                                                                               benchmark for
                                                       Transformation
                                                                                               0


                                                                                                                                                                               LLM capability
                                                                                                   Interpretation   Generation    Completion   Transformation   Correction


           Suggestions: Few-shot, fine-                                                       Crypto schemes: 677
            tune, Pass@K, and Agent.                     Correction                          Security properties: 160                                                            assessment.

            Fig. 1. Motivation for benchmarking LLM-assisted Cryptographic Scheme analysis.
                          Table 1. Representative formal tools and their specification languages.
         Tool                           Language           Key Characteristics / Advantages
         Scyther [21]     SPDL        Lightweight and efficient symbolic model for secrecy/authentication claims.
         Tamarin [51]     SPTHY       Support stateful protocols and observational equivalence.
         AVISPA [4]       HLPSL       Supports multiple parallelized back-end engines (OFMC, CL-AtSe, SATMC).
         ProVerif [11]    PV/HORN/... Handle unbounded sessions, and support for secrecy/equivalence properties.
         Maude-NPA [23] MAUDE         Analyze algebraic properties, and handle timeouts and internal errors.
         CryptoVerif [12] CV/OCV      Computational soundness under both classical and random oracle models.
         EasyCrypt [8]    EC          Higher-order logic for computational proofs, and has machine-checked rigor.


    • We introduce C.F.B, a large-scale benchmark across seven verifier languages, enabling system-
      atic evaluation of LLMs in cryptographic scheme analysis (c.f., § 3).
    • We propose a unified evaluation methodology that integrates automated model interaction,
      multi-tool verification, and a weighted scoring framework (c.f., § 4).
    • We conduct the first comprehensive evaluation of nine state-of-the-art LLMs (e.g., GPT-
      4o, Claude-3.5, and DeepSeek-Coder), revealing strengths in interpretation/completion and
      weaknesses in generation/transformation/correction (c.f., § 5), highlighting the challenges of
      domain-specific language generation. Also, we present robustness/optimization analyses and
      fine-grained property-level evaluation (c.f., § 6), demonstrating the stability of our findings.

2     Preliminaries
2.1    Formal Language of Cryptographic Scheme Analysis Tools
Automatic cryptographic-scheme analysis is driven by the formal languages of verification tools,
whose assumptions range from symbolic (Dolev-Yao) models to computational proofs under stan-
dard assumptions [7]. Table 1 lists representative, widely adopted tools and languages spanning
diverse techniques. Scyther [21] and AVISPA [4] offer efficient and accessible analysis of classical
authentication schemes. ProVerif [11] and Tamarin [51] enable deep reasoning about equivalence
and unbounded behaviors. Maude-NPA [23] supports algebraic reasoning. CryptoVerif [12] and
EasyCrypt [8] provide computational guarantees aligned with security properties. As surveyed
in [19], these tools constitute the SOTAs for the formal analysis of cryptographic schemes.

2.2    A Generative Example for Automatic Formal Analysis
Natural-language scheme descriptions can be mapped into formal languages required by analysis
tools [59]. For example, “the client sends a hash value of 𝑛 to the server” can be expressed as:
  SPDL (Scyther): send_1(C, S, h(n));         HLPSL (AVISPA): C → S : hash(n);
  PV/HORN/... (ProVerif): out(c, hash(n)); SPTHY (Tamarin): [ Fr(n) ] –[ Out(hash(n)) ]-> []

                                                       Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:4                                              Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou




                                                                  Project Files
                Project Collection                                                                     Dataset Formation                                                    LLM Evaluation                                 Testbeds
                                                  Built-in                                                                                                                        Task
  Online
                                               Datasets for
                                                                                                                               v Name                                   Prompt              Prompt                     Formal Verifiers
 Resources                                                                                                                     v Roles                                Engineering Data     Templates
                                               Formal Tools                                                                    v Interaction




                                                                                                                                                   Datasets
                                                                                                                               v Goals
                                                                                                                                                                                       LLM Inputs
     Searching & Filtering Selected Projects                                                     Formal                Project v Adversaries
    Open-sourced Projects                                                                       Model Files          Documents v Notes/Tips                           LLM Calling Multiple Versions
                                        Formal Model Files




                                                                                                                                                                                                        Formal Code
                                                                  Description Documents
                                      for Seven Tools (7*100)
      Initial Projects         ...
                                      ✓ Distinct Schemes                                                Logic Describing
                                      ✓ Multiple Scenarios
     Formal Model Files for           ✓ Various Properties                                Formal Model Logic Files Generated by Fusing
       Seven Tools (4549)             ✓ Appropriate Ratios                                Multiple LLM Outputs and Manual Verification                                                 LLM Outputs
                                                                                                                                                                                                                      Multiple Commands
                                                                                                                                                                      Context Matching Information
 Removing Repeat Items                Selecting Schemes                                   Task Data Constructing (* means labels)                                     Parsing Patterns Extraction                      Multiple Versions




                                                                                                                                                   Quality Feedback
                               ...
                                                                                                                       Transformation (100)
                                                                                                                                                                                                                      Adaptive Operations
                                                                                           Interpretation (20*2*7)
     Filtered Projects               Labeled Projects                                     Original Code, Notation*   Logic Description, Labels*,
     Formal Model Files with          Formal Model Files with                              and Logic Description*    and Transferred Code-pair                           Model      Metric Statistics
     Various Contents (3590)         Labels (safe/unsafe)(1837)                                                                                                                                                        Result Analyzer
                                                                                            Generation (100*7)           Completion (100*7)
                                                                                                                                                                        Scoring     Weighted Sum




                                                                                                                                                                                                        Results
      Runnable Check                      Tool Labeling                                      Logic Description       Logic Description, Labels*,                                      Model Scores                    q Analyzable Ratio
                                                                                               and Labels*           Original* and Masked Code
                                                                                                                                                                                                                      q ACC/P/R/F1
                                                                                                                                                                                    Score Ranking
      Candidate        Formal Model Runnable (1837)                                                         Correction (20*2*7)                                        Result                                         q Code Similarity
                         Files for    Error (972)                                                                                                                     Analyzing     ▪ Conclusion
       Projects        Seven Tools   Timeout (781)
                                                                                             Logic Description, Error and False-report Code,
                                                                                                  Error and False-report Notes, Labels*                                             ▪ Suggestions                     q Semantic Similarity


                                                    Fig. 2. The workflow of C.F.B (Crypto Formal Benchmark).

    Once generated, these specifications can be analyzed by their tools under the adversaries such as
Dolev-Yao [19]. This enables a practical pipeline: LLMs translate natural-language descriptions into
tool-compatible formal code, which is checked for properties such as secrecy/authentication [51].
    Q1. How does formal code generation differ from traditional code generation? Unlike
traditional code generation, formal specifications require strict syntax and semantics [17]: small
omissions (e.g., missing claims or wrong role bindings) can break compilation or yield misleading
analysis outcomes [19]. Also, the same scheme often maps into multiple formal languages (e.g., SPDL,
HLPSL, PV, and SPTHY) [38], increasing manual effort and stressing cross-language generalization.
    Q2. Can LLMs directly discover scheme flaws? Despite producing formal-looking specifica-
tions, LLMs cannot effectively verify schemes on their own, as this typically requires symbolic or
computational security reasoning [49]. They often generate look-valid but incorrect results, and
fail to capture freshness conditions, role bindings, or subtle attacks such as replay and man-in-the-
middle [46]. Thus, LLMs are better for bootstrapping models, while verifiers must validate and
refine the results, motivating systematic benchmarking to measure gaps and guide improvements.
    Q3. What makes benchmarking LLMs hard in formal analysis? Nevertheless, building
such a benchmark remains non-trivial. (i) Dataset scarcity: despite the abundance of cryptographic
schemes, formal specifications are rarely available [5], and scheme diversity complicates unification.
(ii) Cross-tool heterogeneity: tools span different languages/paradigms, challenging integration [22].
(iii) Outcome variability: tool outputs range from safe/unsafe to attack traces [21, 51], complicating
automatic scoring. (iv) Evaluation at scale: metrics must capture semantic soundness (beyond
analyzability), while timeouts/explosions hinder scalability [49]. These challenges motivate a
replicable benchmark for fair comparison and practical automation of formal cryptographic analysis.

2.3 Adversarial Assumptions
Security analysis critically depends on the underlying adversary model [19, 46]. (i) Passive DY only
observes traffic (no interception or injection), mainly used for secrecy analysis [11]. (ii) Active
DY controls the network (intercept/replay/forge/block), enabling checks of authentication and
replay-style attacks [21, 51]. (iii) Extended adversaries capture domain-specific powers, e.g., password-
guessing in Internet-of-Things (IoT) or device-capture scenarios with key exposure [17, 38].

3       C.F.B Benchmark
3.1         Corpus Overview
Figure 2 depicts the end-to-end workflow of C.F.B for automatic LLM evaluation on formal crypto-
graphic scheme analysis. Given a model, C.F.B runs unified tasks and outputs capability scores and

Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                                                                                                       FSE177:5

                                       Normalized frequency of top 20 properties/goals across languages   Number of distinct security propeties per language   Total security properties (per 100 schemes)
Verified security property/goal




                                                    Language of formal files in dataset                             Logic length distribution by language          File length distribution by language


                                                      Fig. 3. The property and length distribution for various languages.

overall rankings as follows. (i) Project collection. We gather formal model files from open-source
projects and tool-built datasets. After deduplication, executability checks, and tool-based labeling,
we obtain a set of items that involve diverse schemes, scenarios, and security properties across
the formal languages of seven tools, as detailed in Table 1. (ii) Dataset formation. We unify
and verify formal code and scheme logic descriptions (LLM-assisted with manual checks), then
build task datasets (interpretation, generation, completion, transformation, and correction) with
paired code, labels, and annotations. (iii) LLM evaluation. We query multiple LLMs with prompts,
normalize/parse outputs, and verify them via formal tools (e.g., Scyther, Tamarin, and EasyCrypt)
on testbeds to further compute metrics such as analyzability, accuracy, F1 score, and similarity.
Five capability scores are aggregated into overall results and rankings.

3.2                               Project Collection
3.2.1 Pipeline. The first stage of C.F.B is to prepare formal model files as the benchmark foundation
in three steps: (i) project sourcing. We collect formal specification projects from open repositories
(e.g., GitHub/Google) and tool-provided datasets. This yields 4,549 model files across seven tools.
After deduplication and basic format checks, 3,590 unique projects remain. (ii) Project Labeling.
We execute each file with its corresponding verifier and standardize outcomes as: safe (1,280),
unsafe (557), error (972), and timeout (781). We treat safe/unsafe as analyzable runs and use them for
benchmark construction. (iii) Project Selection. We further curate a balanced subset with diverse
schemes, communication scenarios, and security properties (e.g., secrecy and authentication), while
controlling the safe/unsafe ratio. Meanwhile, we assign a canonical security label to each selected
scheme from the relevant cryptographic literature/standards. The unsafe instances have established
attacks (often with traces), whereas safe instances have no known attacks (sometimes with proof
sketches) under the specified threat model. Then, we align tool outputs with these labels, treat
disagreements as modeling bugs, and discard instances that cannot be fixed. Finally, we sample 100
representative analyzable files per tool, yielding 700 reference files in total (safe 415/unsafe 285).
3.2.2 Dataset Composition. The 700 instances span seven formal languages and 677 distinct
schemes across two-party/multiparty settings with diverse adversaries, forming a representative
benchmark for both syntactic robustness and semantic correctness.
   Schemes. The dataset includes classical and modern schemes for authentication, key exchange,
zero-knowledge proofs, multiparty computation, and post-quantum designs, across domains such
as Internet/IoT and blockchain. It also contains multi-language files of protocols such as Needham-
Schroeder [53], Yahalom [11], and Diffie-Hellman [46]. Their variants (e.g., Paulson’s inductive and
Lowe’s corrected versions [46]) encode subtle differences that challenge fine-grained understanding.

                                                                                   Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:6                               Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou


           Logic [NSPK]                Interpretation




                                                                                   Notation
                                                         Code        [SPDL]                        Noted Code                    Protocol Verifiers
        [Interaction] Initiator (I):       Logic        protocol nspk(I,R,S){                   protocol nspk(I,R,S){ //
        1.Generate nonce Ni.            Description     role I{ fresh Ni: Nonce;                Define protocol name.
        2.Request R's public                            … send_1(I,S,(I,R)); …                  role I{ fresh Ni: Nonce; //
        key from Server. ….                              claim_R1(R,Secret,Nr);                 Define the nonce Ni.            Safe/Unsafe/Error/Timeout
        Responder (R):                                  … } role S{ … } }                       … send_1(I,S,(I,R)); //
        1.Generate nonce Nr.             Generation                                             Send (I,R) to S. …              True results False results
        2.Receive encrypted Ni
        from Initiator. …                                 Transformation                                                      Correction
        [Adversaries] Dolev-Yao            Logic          Code      [SPTHY]                     Incomplete Code                    Incorrect Code




                                                                                   Completion
        [Goals] Ni, Nr are secret        Description                                                                                   Compile errors!
                                                        functions: pk/1, sk/1,                  functions: pk/1, sk/1,
        [SPDL Tips] Define the                            aenc/2, adec/2 …                        ____(FUN_1)____, …              Function(s): pk/1, sk/1,
        protocol with (I, R, S) …                       rule nspk1_A:                           rule nspk1_A:                      aenc/2, adec/2 …
        [SPTHY Tips] Register                                                                     [ … ] --[ … ]->[ … ]                Wrong verified goal!
                                         Generation       [ … ] --[ … ]->[ … ]
        key !Pk(A,pk(~ltkA)) …                          lemma sec_of_B: "…"                     lemma sec_of_B: "…"               lemma sec_of_A: "…"


Fig. 4. Concrete examples for five benchmark tasks in C.F.B.2 The tips only exist for the relevant language.

   Security properties/goals. We deduplicate 241 raw tool-specific goals into 160 distinct properties,
covering secrecy, authentication, integrity, correctness, and equivalence.1 As depicted in Fig. 3,
although secrecy and authentication dominate, C.F.B still includes long-tail advanced goals (e.g.,
forward secrecy, IND-CPA/CCA indistinguishability, and zero-knowledge). Each scheme has 2-3
verified properties on average, with complex cases (e.g., multiparty key exchange) exceeding 10 prop-
erties. More importantly, different tools emphasize different properties. For instance, Scyther [21]
and ProVerif [11] focus on secrecy/authentication, while EasyCrypt [8] highlights indistinguishabil-
ity and reductionist proofs. This complementarity underscores the necessity of involving multiple
tools in scheme analysis, motivates evaluating LLMs across diverse formal languages, and further
calls for a unified score that enables fair cross-model comparison by summarizing end-to-end tool-
usable capability across heterogeneous verifiers/tasks under analyzability-correctness trade-offs.
   Adversary models. The dataset covers Dolev-Yao, CK, eCK, and application-specific adver-
saries [19], including replay, man-in-the-middle, KCI, and key-recovery attacks [46]. For example,
NAXOS_eCK.spthy models passive/active adversaries, while EasyCrypt [8] and CryptoVerif [12]
encode computational assumptions such as CDH/DDH in the Random Oracle Model. This diversity
ensures evaluation beyond syntax, capturing adversarial reasoning.
   Cross-language coverage. A large portion of schemes in C.F.B are formalized in multiple verifier
languages, involving the same tool family (e.g., CV→OCV) or across tools (e.g., SPDL→SPTHY),
which enables controlled cross-tool translation evaluation. For example, Needham-Schroeder
appears in HORN, HORNTYPE, PI, and PV, while Diffie-Hellman is available in both PV and CV.

3.3    Dataset Formation
3.3.1 Logic Description. To enable systematic evaluation, each instance is paired with a unified
logic description distilled from project documents, normalized across tools, and manually reviewed.
It consistently captures scheme roles, message flows, and security goals, bridging natural-language
description narratives and tool-specific formal code.
3.3.2 Task Data Construction. Building on the logic descriptions, we design five tasks that probe
complementary capabilities of LLMs in formal analysis, as an example shown in Fig. 4. (i) Formal
Code Interpretation (20*2*7 instances). Given the original code, LLMs are asked to produce
notation-level comments and global scheme summaries. Ground truth includes annotated notations
and logic descriptions. (ii) Formal Code Generation (100*7 instances). From a natural-language
logic description, LLMs generate complete formal code in the target language. Correctness is
assessed by compiling the code and verifying whether the intended security goals are met in our
testbed. (iii) Formal Code Completion (100*7 instances). Given partially masked specifications,
1 The full taxonomy of deduplicated properties refers to https://github.com/Secbrain/CrypFormBench/tree/main/datasets.
2 The interactive and step-by-step examples are available on https://Secbrain.github.io/CrypFormBench.



Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                                         FSE177:7


                           Table 2. Comparison of our dataset with existing benchmarks.
        Benchmark                    Languages                          Scales                                Objects
        AVISPA suite [4]              HLPSL (1)            ∼100 (Authentication, secrecy)             Tool-specific verification
        Tamarin case studies [51]     SPTHY (1)               ∼80 (Secrecy, agreement)                Tool-specific verification
        ProVerif examples [11]         PV/... (1)            ∼60 (Secrecy, equivalence)               Tool-specific verification
        EasyCrypt examples [8]          EC (1)           ∼50 (Indistinguishability, reduction)         Computational proofs
        LLM-aided [49]              SPTHY/PV (2)            18 (Multi-party, secrecy, IoT)            Tool-specific verification
        C.F.B (ours)                SPDL/EC/...(7) 677 (Multi-party, 160 properties, ZK, PQ, ...)   Multi-task LLM evaluation


LLMs fill in missing fragments. Masks are applied at different levels (e.g., lemmas, type variables,
statements) using grammar analyzers aligned with each tool’s syntax. Inputs include the masked
code and logic description, while outputs are compared against the original files. (iv) Formal
Code Transformation (100 instances). LLMs are tasked with translating a scheme specification
from one formal language to another for the same scheme and security properties under matched
adversary assumptions, based on the source language and its logic description.3 A translation is
considered correct if the verdict of transformed contents is consistent with that of the sources.
(v) Formal Code Correction (20*2*7 instances). LLMs repair code that either fails to compile
or produces incorrect verification results. For compile errors, the inputs include the code, error
message, and logic description, yet tips on wrong results are provided for false reports. Outputs are
the corrected, analyzable specifications. Note that the instance counts are computed as a product:
the first factor specifies the sample size (100 or 20), the second denotes the number of sub-tasks (if
applicable), and the third indicates the number of languages (7, if any).
3.3.3 Dataset Comparison. To emphasize the novelty of our dataset, we compare C.F.B with existing
formal datasets of cryptographic schemes and LLM evaluation benchmarks, as shown in Table 2. (i)
Multi-language coverage. Seven mainstream formal languages are included, supporting both
language-specific evaluation and cross-language transformation. (ii) Scale and diversity. 677
non-duplicated protocols cover classical (e.g., Needham-Schroeder, Diffie-Hellman) and modern
schemes (e.g., MPC, ZK, post-quantum). (iii) Properties and adversaries. 160 distinct security
properties and multiple attacker models (DY, CK, eCK, algebraic) extend well beyond tool demos.
(iv) LLM orientation. Explicit labeling supports five tasks, making it the first dataset designed for
systematic LLM evaluation in formal protocol analysis.

4     End-to-End Evaluation Pipeline and Multi-Verifier Testbed
4.1    Input Preparation and LLM Interaction
Each task is instantiated with a task-specific prompt constructed from our dataset. For example,
in completion, the prompt specifies the target language, provides an incomplete scheme file with
placeholders (e.g., ```____()____```), and attaches its logic description. The model is explicitly
instructed to fill only the missing parts, preserve all existing content, and ensure the output compiles
in the designated tool (e.g., Scyther). This template-based prompting enforces consistency across
tasks/languages and matches realistic analyst workflows.

4.2    LLM Output Pre-processing
Raw outputs of LLMs often contain formatting noise or inconsistent styles, so we apply a stan-
dardized pre-processing pipeline: (i) code extraction. LLMs sometimes wrap formal code in
various delimiters (e.g., ```spdl```, Markdown fences, or plain text). Only the relevant code seg-
ments are extracted, discarding commentary or formatting artifacts. (ii) Description filtering. For

3 The transformation cases refer to https://github.com/Secbrain/CrypFormBench/tree/main/datasets/transformation.



                                          Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:8                     Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou


interpretation, keep only structured logic fields aligned with the reference template. (iii) Normal-
ization. Canonicalize whitespace/indentation and variable aliases to avoid spurious mismatches.
(iv) Validity checks. Filter empty or corrupted outputs before tool execution.

4.3    Testbed Construction and Verification
To maximize coverage and reliability, the verification testbed integrates multiple tools, versions,
and execution commands. (i) Multiple Tools. As detailed in § 2.1, seven representative tools are
assembled to cover a broad spectrum of security properties and adversarial models. (ii) Multiple
Versions. For tools with unstable grammar across releases (e.g., Maude-NPA v2.0/v3.0.1, CryptoVerif
v1.25/v2.07, EasyCrypt 1.0/dev), we execute multiple versions from high to low. Stable tools such as
Scyther, Tamarin, ProVerif, and AVISPA are run with a canonical version. (iii) Multiple Commands.
To account for varying call behaviors, we employ alternative command sets. For instance, AVISPA
invokes multiple engines (ofmc, cl-atse) sequentially, as a single engine may miss unsafe cases.
Maude-NPA executes both “red initials(0,12)” and “red initials(0,5)”. The former offers more precise
results but risks timeout or internal errors, while the latter provides a fallback. Similarly, Tamarin
enables observational equivalence via adaptive operation detection, and CryptoVerif automatically
selects between classic and random-oracle models depending on file type (CV and OCV).

4.4    Evaluation Metrics
Our framework evaluates model performance along five dimensions: (i) Syntactic correctness.
Whether the generated code can be parsed and compiled by the testbed. The analyzability 𝑎 ∈ [0, 1]
refers to the analyzed ratio of generated formal files. (ii) Functional correctness. Whether the
verified security properties (e.g., secrecy and authentication) hold as intended, which is computed
by matching scheme-level verdicts with the ground truth (SAFE/UNSAFE)4 , as tools such as AVISPA
provide only binary results. We compute the accuracy ACC over all files, count the TP/TN/FP/FN on
analyzable files, and further calculate ACCA, F1A ∈ [0, 1]. Also, the fine-grained property evaluation
is discussed in § 6.4. (iii) Execution efficiency. Time required for verification, reflecting practical
usability. (iv) Code similarity. Overlap between completed code and ground truth, used mainly in
completion tasks. (v) Semantic similarity. Following prior work [1, 2, 29, 58] on sentence-semantic
similarity using vector representations, we quantify the quality of logic interpretation and code
annotation by computing the cosine similarity 𝑠 logic, 𝑠 anno ∈ [0, 1] between the embedding vectors
of model output and human-verified reference extracted by the Qwen3-Embedding-8B model [28].

4.5    Overall Capability Scoring Method
To enable a fair and unified evaluation of LLMs across the five capabilities tested in C.F.B, we design
a comprehensive scoring scheme that integrates performance across tasks, languages, and LLMs.
It balances executability (𝑎) and correctness (ACCA /F1A on analyzable outputs), with task-specific
auxiliary signals such as code similarity (completion) and semantic similarity (interpretation).
  Executable tasks. For each task 𝑡, language 𝐿, and model 𝑀, we compute metrics defined in §4.4
and test effectiveness via a two-level harmonic task score that penalizes imbalanced performance:
                                                                                        2𝑥𝑦
            𝑆 t = HM(𝑎𝛾 , 𝑄),        𝑄 = HM(ACCA, F1A ),              HM(𝑥, 𝑦) =              ,      𝜀 = 10−6,            (1)
                                                                                      𝑥 +𝑦 +𝜀
where 𝛾 is a tunable parameter (default 𝛾 = 1) to penalize low analyzability. On this basis, correction
task consists of two sub-tasks: error correction (syntactic/compilation errors) and false correction

4 The ground-truth is supported by established analyses and aligns with the results of reference models, as detailed in § 3.2.



Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                   FSE177:9


(semantic mis-specifications). Their scores are combined as:
                                        𝑆 corr = 𝜆err 𝑆 err + 𝜆false 𝑆 false,                                     (2)
where 𝜆err = 0.4 and 𝜆false = 0.6 (default), reflecting the greater difficulty of semantic repair. In
addition to executability-based correctness on annotated code, interpretation also evaluates the
semantic fidelity of the logic description and code annotations via embedding-based similarity. We
combine them with default weights 𝛼 = 𝛽 = 0.3 by considering the importance of code availability.
                              𝑆 interp = 𝛼 𝑠 logic + 𝛽 𝑠 anno + (1 − 𝛼 − 𝛽) 𝑆 anno .                              (3)
  Language aggregation. To avoid dominance of high-frequency languages, we adopt the macro-
averaging method. Optionally, difficulty weights 𝑤 𝐿 can be applied to focus on specific languages.
                                              1 ∑︁
                                   𝑆𝑡 (𝑀) =           𝑆𝑡 (𝑀, 𝐿).                                (4)
                                             |L| 𝐿∈ L

    Task aggregation. We assign task-level weights to reflect importance and difficulty.
                                                 ∑︁
                          𝑆 overall (𝑀) =                       𝑤𝑡 𝑆𝑡 (𝑀),                                        (5)
                                            𝑡 ∈ {interp,gen,comp,trans,corr}

where the default setting is 𝑤 interp = 0.15, 𝑤 gen = 0.25, 𝑤 comp = 0.20, 𝑤 trans = 0.25, and 𝑤 corr = 0.15,
motivated by task difficulty. For easier tasks (e.g., interpretation and error correction), executability
has fewer limitations. In contrast, small analyzability drops strongly affect usefulness for genera-
tion/transformation, so we upweight them. These weights are adjustable to match the evaluation
focus and typically maintain stable ranking conclusions, which is discussed in § 6.1.

5     Benchmark Results and Analysis
5.1    Baseline Evaluation
We comprehensively assess C.F.B with nine representative LLM baselines spanning proprietary
and open-source, general-purpose and code- or reasoning-oriented models.
  • GPT-4o [37] and GPT-4o-mini[37] (OpenAI): widely used proprietary models with strong
    reasoning and code understanding capabilities. Also, the latter follows a lightweight design.
  • LLaMA4-Instruct [52] (Meta): a representative open-source model for reproducibility.
  • GLM-4[32] (ZhipuAI): a large-scale bilingual LLM optimized for reasoning and domain tasks.
  • Gemini-2.5-Pro[60] (Google DeepMind): the latest frontier proprietary model with multi-
    modal and cross-lingual reasoning abilities, included to benchmark formal-spec performance.
  • DeepSeek-R1 [33] and DeepSeek-Coder[73]: a family of open-source models specialized in
    reasoning (R1) and programming/code generation (Coder).
  • Claude-3.5-Sonnet-Coder [3] (Anthropic): a SOTA commercial model with enhanced code
    reasoning and safety alignment, suitable for formal specification tasks.
  • Grok-3 [64]: an emerging commercial LLM focusing on reasoning-intensive applications.
  Experimental Setup. All experiments and our testbeds were conducted on Ubuntu 22.04 with an
AMD EPYC 9554P (64 cores), 512GB RAM, and 4×NVIDIA L40 GPUs (192GB total). The Qwen3-
Embedding-8B embedding encoder and Qwen2.5-Coder-3B model are run with transformers library.

5.2    The Overall Capability
In this section, we present an integrated discussion of the five key capabilities evaluated in C.F.B:
generation, completion, correction, transformation, and interpretation. Table 3 summarizes the
performance of the evaluated models in terms of overall and task levels. Several insights stand
out: (i) Claude-3.5-Sonnet-Coder consistently ranks highest across all tasks, demonstrating strong

                                  Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:10                        Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou


   Table 3. Capability of LLMs evaluated on C.F.B according to the calculation method detailed in § 4.5.
                               Generation                  Completion               Correction           Transformation                 Interpretation
Model                                                                                                                                                         𝑆 overall
                         𝑎 ACCA F1A 𝑆 gen               𝑎 ACCA F1A 𝑆 comp 𝑎 ACCA F1A 𝑆 corr 𝑎 ACCA F1A 𝑆 trans 𝑎 ACCA F1A 𝑆 interp
Open-source Models
GLM-4                   0.01   0.50   0.00 0.0 0.13        0.94   0.92 22.8 0.11     0.29   0.17 14.5 0.05   0.00   0.00   0.0   0.26    0.91   0.90   62.3    16.1
LLaMA4-Instruct         0.03   0.79   0.77 5.8 0.41        0.88   0.84 55.6 0.56     0.59   0.58 57.2 0.00   0.00   0.00   0.0   0.15    0.95   0.94   44.4    27.8
DeepSeek-Coder          0.03   0.85   0.80 5.8 0.55        0.89   0.89 68.0 0.61     0.67   0.67 63.9 0.04   0.00   0.00   0.0   0.86    1.00   1.00   93.2    38.6
DeepSeek-R1             0.03   0.93   0.91 5.8 0.50        0.94   0.93 65.2 0.50     0.67   0.65 56.9 0.08   0.00   0.00   0.0   0.41    1.00   1.00   77.4    34.6
Closed-source Models
GPT-4o-mini             0.06   0.00   0.00 0.0 0.06        0.64   0.53 10.9 0.41     0.51   0.48 44.8 0.04   0.00   0.00 0.0 0.79        1.00   1.00   93.8    23.0
Gemini-2.5-Pro          0.04   1.00   1.00 7.7 0.15        0.94   0.94 25.9 0.22     0.93   0.93 35.6 0.03   0.00   0.00 0.0 0.34        0.89   0.90   69.1    22.8
GPT-4o                  0.05   1.00   1.00 9.5 0.36        0.91   0.90 51.5 0.48     0.65   0.62 54.7 0.07   0.00   0.00 0.0 0.81        1.00   1.00   94.1    35.0
Claude-3.5-Sonnet-Coder 0.15   0.62   0.63 24.2 0.62       0.93   0.93 74.4 0.67     0.75   0.77 71.2 0.14   0.07   0.62 13.3 0.78       0.99   0.99   91.7    48.7
Grok-3                  0.07   0.74   0.71 12.8 0.23       0.91   0.90 36.7 0.12     0.50   0.00 0.0 0.17    0.00   0.00 0.0 0.01        0.00   0.00   49.6    18.0




                                       Analyzed ratio
  ACC                                                                              F1A


Fig. 5. Results of the generation experiment. Different colors represent different formal languages. Among
them, light bars represent the analyzed ratio, dark colors represent ACC, and scattered dots represent F1A .

robustness in both syntactic validity and semantic reasoning. (ii) DeepSeek-Coder excels in error
correction and completion, and occasionally matches top models in interpretation and generation.
(iii) GPT-4o performs strongly in interpretation but struggles in generation and transformation,
while its smaller variant GPT-4o-mini is less stable yet competitive in some simpler languages. (iv)
General-purpose models such as Gemini-2.5-Pro and GLM-4 generally underperform, highlighting
the importance of code- and reasoning-oriented optimization. (v) Weaker baselines (LLaMA4-
Instruct and Grok-3) consistently fail across most tasks, rarely producing analyzable outputs. These
complementary strengths suggest an agentic workflow that routes tasks to the most suitable model.
    A cross-task comparison highlights clear patterns. Interpretation and completion are generally
easier for most models, yielding a higher analyzed ratio and better accuracy. By contrast, transfor-
mation and generation remain the most difficult tasks: even the strongest models achieve only low
analyzed ratio and limited correctness, underscoring the persistent challenges in these tasks.
    Overall, LLMs show tractable performance on interpretation and error correction, but code
generation, especially cross-language transformation, remains a major bottleneck. Outcomes are
shaped by model specialization and language complexity: domain-optimized models such as Claude-
3.5-Sonnet-Coder and DeepSeek-Coder lead, yet reliable end-to-end automation remains unresolved.
 Can current LLMs provide end-to-end automation for formal scheme analysis? LLMs
 can be regarded as strong assistants for interpretation and localized correction, but not yet
 reliable for full generation or cross-language transformation. Future work should prioritize
 grammar-constrained decoding, domain-specific fine-tuning, agentic model orchestration, and
 tool-in-the-loop workflows to bridge the gap toward practical end-to-end automation.

5.3     The Generation Capability
We compare LLM code generation across seven formal languages using three metrics: analyzed ratio,
ACC, and F1A , as shown in Fig. 5. We observe four consistent patterns: (i) closed-source models
lead overall. Claude-3.5-Sonnet-Coder, GPT-4o, and Grok-3 follow prompts more reliably and achieve

Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                 FSE177:11




   Analyzed ratio

            ACC

            F1A


Fig. 6. Results of completion experiment. The last sub-figure shows ACC improvement of completion over
generation across languages for each model. Other sub-figures report per-language performance: light bars
indicate analyzed ratio, dark bars denote ACC, and scatter points show F1A .

higher analyzability, verification success, and F1A than most open-source models, indicating stronger
end-to-end usability. (ii) Strong intra-model variability across languages. Performance differs
sharply by language within the same model: Gemini-2.5-Pro is stronger on CV/EC (computational-
security-oriented), GPT-4o performs best on PV, while Claude-3.5-Sonnet-Coder degrades on EC and
Maude. This likely reflects uneven training coverage and language-specific grammatical/semantic
complexity. (iii) Stable language-level trends across models. Except for GLM-4 and GPT-4o-mini,
most models obtain a higher analyzed ratio and ACC on PV than on SPTHY/SPDL/Maude, consistent
with PV being closer to mainstream programming syntax (e.g., Java/C). Maude is a broad failure
mode: some outputs compile, but none satisfy target properties, suggesting sparse data and stronger
contextual dependencies. (iv) Reasoning/coder models excel on computational proof languages
(CV/EC). Reasoning/coder-oriented models (Gemini-2.5-Pro, DeepSeek-R1, Claude-3.5-Sonnet-Coder,
and DeepSeek-Coder) consistently achieve a higher analyzed ratio, ACC, and F1A on CV/EC, showing
advantages in structured generation and computational reasoning.
  In sum, performance varies across languages due to scarce/uneven data, language complexity,
and model biases, making generation less reliable than for mainstream programming (e.g., Python).
Question. Can LLMs directly generate analyzable and correct formal scheme models?
Current LLMs often fail to satisfy strict formal syntax/semantics, especially in complex languages.
such as EC and PV/HORN. Practical improvement likely requires grammar-constrained decoding
and tool-guided feedback/repair to reduce invalid outputs and improve usability.

5.4        The Completion Capability
Figure 6 reports the completion task, where models fill missing segments of formal code. Compared
with full generation, completion provides a partially correct context, reducing the burden of
producing valid syntax/semantics from scratch. We report the analyzed ratio, ACC, and F1A .
   Overall performance. Most models improve ACC across languages in the completion setting,
confirming that partial context alleviates syntactic/structural burdens compared to generation.
Notably, weaker models (e.g., GPT-4o-mini) break the near-zero barrier on EC/SPDL/SPTHY. For
Maude, stronger models (e.g., Claude-3.5-Sonnet-Coder) can complete and verify a subset of cases.
We further observe an all-or-nothing pattern: once outputs become analyzable, correctness is
typically high (notably on EC/CV), making executability/analyzability the primary bottleneck.
   Language comparison. Most models (except GPT-4o-mini and Gemini-2.5-Pro) perform best on
SPDL, likely due to its shorter instances and constrained, redundant syntax that provides stronger

                                  Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:12                               Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou

                                                                                                         Results Breakdown - Error correction




                                                                                                         Results Breakdown - False correction




            F1A range by model on error correction              F1A range by model on false correction

Fig. 7. Results of the correction experiment. The left two show the F1A range per model on correction error
and false, with colored dots denoting languages, and black markers indicating the mean ± range. The right
stacked bars summarize categorical outcomes aggregated over all languages.


completion cues. Performance drops on complex languages: Maude and EC remain challenging,
as in generation. LLaMA-Instruct is an exception on Maude, plausibly due to greater pretraining
exposure, while EC gains are smaller due to longer code and larger masked fragments.
   Model comparison. Code-specialized models consistently outperform general-purpose LLMs.
Claude-3.5-Sonnet-Coder achieves the strongest overall results with both high analyzed ratio and
ACC. DeepSeek-R1/DeepSeek-Coder also improve substantially, reaching ACC above 30% on most
languages (while < 5% in generation). In contrast, GPT-4o-mini and GLM-4 pass only a limited
number of cases, reflecting limited formal-code capability.
   Overall, completion is easier than full generation, and context boosts analyzability, but producing
syntactically valid code for complex formal languages still limits reliability.
 Can LLMs reliably complete partial scheme specifications into analyzable formal mod-
 els? Context substantially improves analyzability, and once code is valid, correctness is typically
 high. However, syntactic validity in complex languages (e.g., Maude and EC) remains the main
 obstacle, motivating grammar-aware or tool-guided completion strategies.

5.5    The Correction Capability
We evaluate correction capability under (i) correction error, where the specification fails to compile,
and the model fixes it by handling compiler errors and the intended logic. (ii) correction false, where
the code compiles but violates expected properties, requiring semantic repair guided by the logic.
   Error correction. Figure 7 shows a clear difficulty gap. In correction error, models benefit from
explicit diagnostics and typically localized syntactic issues. Code-specialized models (e.g., Claude-
3.5-Sonnet-Coder and DeepSeek-Coder) achieve an analyzed ratio around 0.6 across languages,
benefiting from the compiler feedback and formal-syntax adherence. Performance degrades on
complex languages (e.g., EC/Maude), where multiple interdependent fixes are required. Moreover,
once outputs are analyzable, most models achieve high F1A (often > 0.9), indicating that compiler-
guided structural repair is largely within current LLM capabilities.
   False correction. This task is harder than error correction: although faulty code and logic are
provided, models identify subtle semantic faults (e.g., mis-specified properties or missing adversary
actions) while preserving syntactic validity. Most models have low analyzed ratios and modest
ACCA . Claude-3.5-Sonnet-Coder performs well, yet still trails error correction.
   Overall, LLMs can reliably fix localized, compiler-reported errors, but semantic-level debugging
remains difficult, motivating tool-guided repair and human-in-the-loop validation.
 Question. Can LLMs reliably correct syntactic and semantic errors in formal models?
 Compiler-guided fixes are largely reliable and achieve high accuracy once analyzable, but
 semantic-level false corrections remain challenging, motivating tool feedback/human validation.

Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                                                                FSE177:13


                                    ACCA=0.00,F1A=0.00

                                    ACCA=0.00,F1A=0.00

                                    ACCA=0.00,F1A=0.00

                                    ACCA=0.00,F1A=0.00

                                    ACCA=0.00,F1A=0.00

                             ACCA=0.00          F1A=0.00

                                    ACCA=0.00,F1A=0.00

                               ACCA=0.50,F1A=0.62

                               ACCA=0.00,F1A=0.00


                                                             Analyzed ratio (#analyzed, #all, #failed generation, #timeout)   ACCA (#TP, #TN, #FP, #FN)


Fig. 8. Results of transformation experiment from model and language perspectives. The source→target
direction corresponds to y→x in heatmaps, and the symbol “-” refers to no transformation instances.


5.6   The Transformation Capability
Figure 8 summarizes the transformation results. At the model level (left), we break down outcomes
into failed generation, failed analysis, timeout, and the TP/TN/FP/FN on analyzable cases. At the
language level, we report the directed source→target analyzable ratio and the corresponding ACCA .
   Cross-language interference and timeout bottleneck. A major failure mode is cross-language
interference: given both source code and logic, models often copy source fragments into the target
file, but equivalent operations use incompatible idioms across tools (e.g., Out(msg) in SPTHY and
send_1(A,B,msg) in SPDL), causing early parse/type failures. Even among compilable translations,
timeouts are frequent, indicating a semantic/structural mismatch. Manual inspection confirms that
compiled outputs are often redundant or ill-structured: in rewriting-based tools (e.g., Maude-NPA),
unnecessary nesting (e.g., enc(enc(a,k1),k2)) can trigger exponential rewriting/non-termination,
while missing mandatory clauses (e.g., ::nil::[+(null),nil]& in Maude) can also induce infinite
loops. Additional recurring errors are summarized in § 5.8. The middle/right heatmaps further
show that only a few source→target directions achieve non-zero analyzability, and even fewer
preserve correctness (non-trivial ACCA ), suggesting the core difficulty is robust cross-tool semantic
mapping across heterogeneous formalisms, not just “hard languages” in isolation.
   Superiority of specialized models. Among all LLMs, Claude-3.5-Sonnet-Coder achieves the highest
analyzed ratio (14%) and meaningful correctness on analyzable cases (e.g., F1A = 61.54%), suggesting
that coding-oriented models retain limited but promising cross-tool transformation ability.
   In sum, translation is the most challenging setting because models must align source semantics
with target syntax, causing only a small fraction of analyzable outputs (typically <10%), even for
powerful models (e.g., GPT-4o and DeepSeek-Coder). We further discuss practical directions such as
grammar-constrained decoding and tool-in-the-loop feedback in § 6.
Question. Can LLMs directly transform scheme specifications across different formal
languages? Analyzable outputs are scarce, with dominant failures from cross-language interfer-
ence, syntactic incompatibility, and semantic/structural mismatch (timeouts/incorrect goals).
Promising directions include grammar-constrained decoding to align semantics across tools.

5.7   The Interpretation Capability
The evaluation of interpretation capability is summarized in Figure 9. We assess two aspects: (i) logic
illustration, measuring semantic similarity between generated logic description and ground-truth
references, and (ii) code annotation, evaluating both notation similarity and code executability.
   Logic interpretation. Most models reconstruct interaction logic with high similarity. In the left
heatmap, GPT-4o and Claude-3.5-Sonnet-Coder consistently exceed 0.95 on average, while DeepSeek-
R1 and DeepSeek-Coder remain competitive. In contrast, general-purpose or lightweight models
LLaMA4-Instruct and Grok-3 struggle to capture subtle adversary behaviors and security goals.

                                         Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:14                                Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou
Model




               Logic description similarity by model and language         Formal code notation similarity by model and language                 Valid Commented Code Count by Model and Language


Fig. 9. Interpretation results across models and languages. The left heatmap shows the similarities between
the logic description and the intended logic. The middle reports annotation similarity with ground-truth
explanations. The right presents the count of valid commented code blocks.
               Generate Error (e.g., GPT-4o-mini)                       Compile Error (e.g., GLM-4)                                Timeout (e.g., Gemini-2.5-Pro)
               【EC KEM_ROM】                                         【EC Cramer Shoup-Encryption】                                  【Maude NSPK3】
               Based on your protocol description, I'll             var m0, m1, b, e, f, h, r; //Naming Error!                    eq STRANDS-DOLEVYAO
               generate a formal analysis code in                   【PV/HORN Denning Sacco-Orig】                                  = :: nil :: [ nil | -(X), -(Y), +(X ; Y), nil ] &
               EasyCrypt's ec language that captures                forall s1:skey, s2:skey;... sign((host(s2),                     :: nil :: [ nil | -(X ; Y), +(X), nil ] &
               the Key Encapsulation Mechanism (KEM)                pk(s2)), sS[])));                                               :: nil :: [ nil | -(X ; Y), +(Y), nil ] &
               with its security properties. Here's the             (*Woo and Lam public-key auth protocol                          :: nil :: [ nil | -(X), +(sk(i,X)), nil ] &
               implementation::\n\n``ec``. //Empty Code!                                                                            :: nil :: [ nil | -(X), +(pk(A,X)), nil ] &
                                                                    (1997) (*…*) … *) //Notation Error!
               【CV Hash Elgamal-CDH】                                                                                                :: nil :: [ +(null), nil ] & //Redundant
               Based on the protocol description and                【PV/PI Yahalom】                                                 :: r :: [ nil | +(n(i,r)), nil ] &
               analysis requirements, I've completed the            (* Shared key cryptography *)                                   :: nil :: [ nil | +(A), nil ]
               CryptoVerif formal analysis code. //None             // Missing function definition!                               [nonexec] .

               False negative (e.g., DeepSeek-R1)                     False positive (e.g., Grok-3-Re)                            Normal (e.g., Claude-3.5-Coder)
              【SPDL isoiec-9798-2-3 Secrecy】                        【SPTHY NAXOS_eCK Secrecy】                                     【HLPSL DH Secrecy, Authentication】
              protocol isoiec-9798-2-1(A,B){                        rule Resp_1:                                                  role environment()
                role A {                                             let KA = 'g'^~lkI, exp = h1(< ~ey, ~eb >),                   def=const
                                                                          Y = 'g'^exp, key = h2(< KA^exp,                           hash_0:hash_func,b:agent,a:agent,f:
                  fresh TNA: Nonce;                                                                                               text,sec_1:protocol_id,sec_2:protocol_id
                  fresh Text1,Text2: Ticket;                                   X^~eb, X^exp, $A, $B >)
                                                                     in [ Fr(~ey), !Ltk($B,~eb),                                    intruder_knowledge = {a,b,f}
                  claim(A,Running,B,TNA,Text1);                           !Pk($A,KA), In(X) ]                                       composition session1(a,b,f)
                  send_1(A,B,Text2,{TNA,B,Text1}k(A,B));              --[ Accept( ~ey, key ), Sid(~ey, <$B, $A,                   end role
                  //Missing the receiving steps and claims!               Y, X, 'Resp' >) ]->                                     goal
                 }                                                    [ Out( key ), //Incorrectly output the key                    secrecy_of sec_1,secrecy_of sec_2
              }                                                        !Ephk(~ey, ~ey), !Sessk( ~ey, key) ]                       end goal

    Fig. 10. Representative cases of LLM outputs across evaluation tasks, highlighting typical error patterns.

   Code annotation and executability. The middle/right heatmaps show that leading proprietary
models (GPT-4o, GPT-4o-mini, and Claude-3.5-Sonnet-Coder) produce highly similar comments
(typically > 0.98) while preserving tool-required syntax. In contrast, Gemini-2.5-Pro and GLM-4
exhibit a gap: despite moderate comment similarity, their annotated files often fail to compile or
execute, showing that fluent explanations do not guarantee tool compatibility. LLaMA4-Instruct
and Grok-3 underperform on both similarity and executability (near-zero executable outputs).
   Leading proprietary models produce highly similar comments (typically > 0.98) while preserv-
ing tool-required syntax. Gemini-2.5-Pro and GLM-4 show that fluent comments do not ensure
compilability/executability, and LLaMA4-Instruct/Grok-3 underperform on both.
   Overall, executability is a necessary complement to similarity-based evaluation: annotations
must be semantically faithful and satisfy strict formal-tool constraints. Thus, current LLMs are
reliable for scheme interpretation but remain a bottleneck for machine-verifiable specifications.
  Question. Can LLMs generate scheme models that are both interpretable and tool-
  executable? Similar-looking outputs are only useful for verification when they satisfy formal
  tool constraints; in practice this still often needs guidance, repair, or hybrid pipelines.

5.8     Case Studies of Evaluation Tasks
Figure 10 summarizes representative LLM outputs across our five tasks and highlights five typical
error patterns.5 (i) Generation errors. Models sometimes fail at the first step, producing either empty
code or placeholder text (e.g., EC of KEM_ROM scheme generated by GPT-4o-mini), indicating weak
grounding in the target syntax. (ii) Compilation errors. Even with near-correct syntax, outputs may
still contain name conflicts, missing declarations, or misused keywords (e.g., EC of Cramer-Shoup
encryption scheme completed by GLM-4), where minor deviations break executability. (iii) Timeouts.
5 Language-specific error modes are summarized on https://github.com/Secbrain/CrypFormBench/tree/main/experiments.



Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                                                                                                                                                                                             FSE177:15

      Analyzed ratio

       Size diff (KB)




        Time diff (s)
                        Difference in size and analysis time between generated formal files and datasets (model level)   Difference in size and analysis time between generated formal files and datasets (language level)   Size and analysis time of formal files in datasets (language level)



                          Fig. 11. Execution efficiency (analysis time and file size) of successfully analyzed files.

Syntactically valid files can still diverge during analysis due to redundant or ill-structured rules
(e.g., MAUDE of NSPK3 protocol corrected by Gemini-2.5-Pro), reflecting that model-generated
code may introduce hidden inefficiencies that degrade analysis performance. (iv) False negatives.
Under-approximating the adversary or omitting critical claims can cause insecure schemes to
be reported as SAFE (e.g., SPDL of ISO/IEC-9798 transformed by DeepSeek-R1), highlighting the
importance of scheme process consistency. (v) False positives. Conversely, models may generate
spurious outputs that violate claims (e.g., SPTHY of NAXOS_eCK protocol completed by Grok-3),
which may mislead users into believing a secure scheme is vulnerable.
   In contrast, strong code-oriented models (e.g., Claude-3.5-Sonnet-Coder) can produce valid speci-
fications, correctly capturing both secrecy and authentication goals in HLPSL, demonstrating the
potential of LLMs when guided properly. These findings reflect that existing LLMs are partially
aware of the writing conventions of formal languages but fall short of producing fully correct,
tool-compatible specifications. Nevertheless, such outputs are not worthless: with minor manual
corrections, many of them can be repaired into valid specifications. This observation motivates
three directions: (i) employing refined and few-shot prompting to guide models toward stricter
formal syntax, (ii) Pass@K generation to increase the probability of obtaining a correct specification,
and (iii) post-processing to reduce trivial errors. These strategies are further discussed in § 6.3.
Are LLMs reliable enough for direct verification? Generated models often contain syntactic
or semantic errors in one pass. Thus, it is suggested to treat their outputs as drafts, and apply
strategies such as few-shot guidance and Pass@K to improve reliability before tool verification.

5.9         The Execution Efficiency
Besides correctness, we evaluate execution efficiency using the verifier runtime and file size on suc-
cessfully analyzed outputs. Figure 11 reports model-/language- level differences between generated
and reference formal files, as well as baseline time/size distributions of the benchmark.
   Intrinsic cost of different verifiers (dataset baseline). The right panel shows distinct runtime profiles
across verifier languages. Lightweight tools such as Scyther and Tamarin usually finish within
tens of seconds (mostly below ∼20s), whereas proof-/rewriting-heavy backends have heavy tails:
AVISPA reaches ∼180s, and Maude-NPA/EasyCrypt exceed ∼400s. File length follows similarly,
with EC up to ∼120KB and Maude up to ∼90KB, indicating higher complexity and overhead.
   Extra cost induced by LLM analyzable outputs. For most models and languages, median analysis-
time differences stay near 0 (roughly within ±0.1-0.2s), and file-size differences are small (typically
a few KB), suggesting that executable LLM outputs are usually comparable to human-curated
scripts. Still, redundant declarations, over-nested terms, or ill-structured rules can inflate size and
slow verification, causing timeouts even after compilation. Thus, efficiency is mainly dominated by
intrinsic tool/language difficulty, while analyzability remains the key bottleneck for hard backends;
it also indicates whether models learn verifier-friendly structure rather than merely valid syntax.
   For most models and languages, median analysis-time differences stay near 0 (within ±0.1-
0.2s), and file-size differences are small (typically a few KB), suggesting executable LLM outputs

                                                                                                   Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:16                      Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou


    Table 4. Alternative scoring configurations (C1-C4).
 Config 𝑤 gen 𝑤 comp 𝑤 trans 𝑤 corr 𝑤 interp    𝛼    𝛽   𝜆err 𝜆false 𝛾

    C1    0.25   0.20   0.25   0.15   0.15     0.30 0.30 0.40 0.60 1.0
    C2    0.20   0.20   0.20   0.20   0.20     0.30 0.30 0.40 0.60 1.0
    C3    0.30   0.15   0.30   0.10   0.15     0.30 0.30 0.40 0.60 1.0
    C4    0.25   0.20   0.20   0.15   0.20     0.40 0.20 0.50 0.50 0.5
                                                                         Fig. 12. Overall ranks of LLMs under C1-C4.

are usually comparable to human-curated scripts. However, redundant declarations, over-nested
terms, or ill-structured rules can inflate size and cause timeouts even after compilation. Thus,
efficiency is mainly governed by intrinsic tool/language difficulty, while analyzability remains the
key bottleneck. It also reveals whether models learn verifier-friendly structure beyond valid syntax.
 Question. Do analyzable LLM-generated scripts run efficiently on formal verifiers?
 Efficiency differs sharply by backend: lightweight symbolic tools (e.g., Scyther and Tamarin)
 usually complete within ∼20s, while complex tools (e.g., EasyCrypt and Maude-NPA) may
 exceed ∼400s and remain timeout-prone. In practice, reliable workflows should combine guided
 prompting/repair with timeout-aware constraints to keep outputs both executable and efficient.

6     Discussion and Suggestions
We summarize several insights and practical recommendations derived from our experiments,
focusing on prompt strategies, model training, evaluation mechanisms, and security extensions.

6.1      Sensitivity for Tunable Parameters in Metric Design
To validate that our conclusions are not artifacts of a particular setting, we evaluate four alternative
parameter configurations shown in Table 4, covering (C1) default difficulty task weights, (C2)
uniform weights, (C3) heavier weights on generation/transformation, and (C4) modified sub-
weights of interpretation and correction with a weaker analyzability penalty. As shown in Fig. 12,
across these settings, model rankings are highly stable: the top models remain unchanged, and
only a swap between the two lowest-ranked models (GLM-4/Grok-3) under uniform weights. Also,
C1 has a high ranking correlation with other settings (Spearman 𝜌 ≥ 0.98 and Kendall 𝜏 ≥ 0.94),
indicating that our main findings are robust to reasonable variations of tunable parameters.

6.2      Validation of Embedding-Based Similarity
For interpretation, we use embedding-based cosine similarity (𝑠 logic and 𝑠 anno ) for logic descriptions
and code annotations (c.f., § 4.4), and validate it from two aspects. (i) Cross-encoder robustness.
Besides the default Qwen3-Embedding-8B, we recompute all scores with BGE-large [25] and E5-large-
v2 [26]. Over 1,260 interpretation instances, Qwen3 shows strong agreement with BGE/E5, with
Pearson correlation ≥ 0.98 and Spearman correlation ≥ 0.88, indicating that model comparisons
and rankings are insensitive to encoder choice. Table 5 further demonstrates case-level consistency.
(ii) Human audit on high-/low-similarity cases. We identify 711 high-similarity (≥ 0.9) and 40 low-
similarity (≤ 0.3) instances, and manually inspect 20 random cases from each group. High-similarity
outputs generally preserve roles, message flows, and security goals, supporting valid formal-
model reconstruction, whereas low-similarity outputs often miss or mis-specify key semantics,
such as secrecy goals, nonce bindings, or adversary assumptions. Table 5 gives examples.6 Rare
divergences, e.g., nsl3.spdl, show that annotation similarity alone can be misleading, motivating
6 Additional rare cases are available at https://github.com/Secbrain/CrypFormBench/tree/main/examples.



Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                       FSE177:17


              Table 5. Representative high-/low-consensus interpretation cases for human audit.
Aspect File                LLM       Qwen3 BGE E5 Human Aspect File                   LLM     Qwen3 BGE E5        Human
Notation andrew-lowe-ban.spdl Claude-3.5 0.98 0.96 0.982 Correct Logic   woo-lam.spdl    LLaMA4 0.02 0.022 0.019 Incorrect
Logic    TLS-PSK.spthy        GPT-4o     0.96 0.94 0.95 Correct Notation OtwayRees.pv    LLaMA4 0.12 0.18 0.15 Miss secrecy
Logic    IKEv2-DS.hlpsl       GPT-4o     0.96 0.97 0.96 Correct Logic    Anonymous.hlpsl Grok-3 0.38 0.361 0.364 Incorrect
Notation IKEv2-DS.hlpsl       GPT-4o     0.98 0.97 0.97 Correct Notation Anonymous.hlpsl Grok-3 0.01 0.02 0.01 Miss code
Notation nsl3.spdl            LLaMA4     0.975 0.981 0.983 Correct Logic nsl3.spdl       LLaMA4 0.019 0.027 0.022 Incorrect



                                                                              ACC                        F1A




Fig. 13. Effects of 𝐾-shot prompting strategy (𝐾 ∈ {0, 1, 2, 3}) in task and language perspectives. Transforma-
tion is omitted since it does not yield analyzable outputs for all 𝐾 in this experiment.

our multi-signal interpretation score that combines logic similarity, annotation similarity, and
tool-executability/verification outcomes (c.f., Eq. (3)). The natural-language references derived
from formal specifications were also manually reviewed during benchmark construction, while
MT-Bench/Chatbot Arena [72] suggests LLM-as-judge as an additional future signal.

6.3   Few-Shot and Fine-Tuning Optimizations
Few-shot strategy. We evaluate 𝐾-shot prompting (𝐾 ∈ {0, 1, 2, 3}) as a simple retrieval-augmented
strategy [39, 71] on a 10% dataset subset, averaging results across models. As shown in Fig. 13,
few-shot markedly improves analyzability for generation (6.6% at 0-shot → 24.9% at 3-shot) and
moderately for completion (42.9% → 50.9%) while keeping ACC > 92%. For correction and interpre-
tation, analyzability is stable, but ACC increases notably (e.g., 55.6% → 72.9% at 3-shot). Exemplars
mainly help reproduce tool-specific scaffolding, e.g., imports/modules, role/environment blocks, and
event/query declarations, improving parsing and execution. Remaining failures are mostly semantic
or tool-specific, such as Maude-NPA timeouts from divergent rewriting and EasyCrypt/CryptoVerif
failures from inconsistent game transitions or event definitions. Thus, few-shot improves analyz-
ability and correctness, but does not close the gap between easy tasks (interpretation/completion)
and hard tasks (generation/transformation) [13, 62].
   LLM Fine-tuning. We fine-tune Qwen2.5-Coder-3B [27] with LoRA to assess task-specific model
improvement. For each task and verifier language, we use a 90%/10% train/evaluation split and
train for 3 epochs. Figure 14 reports task- and language-level changes in analyzability, timeout
ratio, and correctness on analyzable outputs (ACCA /F1A ). LoRA substantially improves completion
(analyzable outputs 5→23, TP 0→8, TN 0→15) and modestly improves correction (analyzable
9→11, TP 1→2, TN 0→1, FN 4→3). Generation only slightly improves in analyzability (4→5),
interpretation is largely unchanged, and transformation still yields zero analyzable outputs. We
also observe language-dependent gains: LoRA helps easier languages such as SPDL, but remains
limited for harder ones such as HLPSL and EC, where failures stem from tool-specific constraints,
e.g., divergence/timeouts or proof inconsistencies. task-specific LoRA can improve analyzability
and correctness for completion (and to a lesser extent correction), while the difficulty ordering
remains stable: interpretation/completion is much easier than generation/transformation.
  PASS@K mechanism. We query the LLM up to 𝐾 times per instance, verify each candidate, and
aggregate the best outcome: an instance is analyzable if any attempt is analyzable, and correctness

                                      Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:18                                Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou




         Analyzed ratio (#analyzed, #generated) / timeout ratio

Fig. 14. Effects of LoRA fine-tuning on Qwen2.5-Coder-3B from task- and language-level views. The timeout
ratio is computed as #timeout/#analyzed, and the transformation is omitted as it has no analyzable outputs.




                                                                                          ACCA Timeout/Analyzed ratio
                                                                                          F1A
                   Fig. 15. Effects of PASS@K (𝐾 = 1, 2, 3) mechanism on task- and language-levels.

is computed on this analyzable set [15]. Figure 15 shows task- and language-level changes as 𝐾
increases from 1 to 3. Larger 𝐾 consistently improves the analyzed ratio, especially for hard tasks
such as generation and transformation, where single-shot outputs often fail parsing or verification.
Timeout ratios usually decrease, though some later attempts reach the verifier but trigger expensive
or non-terminating analyses. On analyzable outputs, ACCA and F1A remain mostly stable or
improve mildly, indicating that Pass@K mainly alleviates the executability bottleneck rather than
improving already-analyzable candidate quality. Language-level results show larger analyzability
gains for stricter or more brittle pipelines, and higher timeout growth for timeout-prone backends.
Thus, Pass@K is a practical complement to single-shot evaluation, but some candidates remain
semantically ill-posed even after becoming analyzable.
   Other optimizations. Beyond the above methods, promising directions include structured prompts
that separate roles/assumptions/goals to reduce ambiguity, multilingual prompting to better align
natural reasoning with formal syntax [69], and Chain-of-Thought (CoT) prompting [63] to encourage
step-wise decomposition of verification logic. Also, adaptive tool invocation for backends, where
LLMs synthesize tool-specific run commands from scheme logic and target properties, especially
for non-default adversary settings such as KCI or (weak) perfect forward secrecy (wPFS/PFS).

6.4    Fine-Grained Property-Level Evaluation
Although property-level evaluation is important [19], C.F.B uses a scheme-level label: a scheme
is UNSAFE if any checked goal is violated, and SAFE otherwise. This supports uniform evaluation
across heterogeneous tools and end-to-end usability. Since each instance typically has 2-4 goals
(§ 3.2.2), fully automatic property-level scoring is difficult for tools with only summary verdicts (e.g.,
AVISPA) or requiring trace/proof parsing to attribute failures to goals (Maude-NPA, EasyCrypt,
and CryptoVerif). We therefore analyze SPDL and SPTHY, whose verifiers expose clear per-goal
outcomes. Each (scheme, goal) pair is a judgment: TP if the goal is correctly verified, FP if a satisfied
goal is spuriously reported as UNSAFE, FN if an expected goal is missing or incorrect, and TN if
a SAFE goal is correctly verified. A scheme is fully correct only when all goals are covered and
correct. Figure 16 reports Δ = Fine − Coarse for ACCA and F1A . Generation drops most due to
low analyzability and missing/mis-modeled goals. For completion and correction, the reduction is
moderate (about 10% on average), while interpretation is nearly unchanged. Model rankings remain

Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                      FSE177:19




      Fig. 16. Performance of LLMs on fine-grained (property-level) evaluation, where Δ = Fine − Coarse.




                                                                                                Soverall=39.2




                         Fig. 17. Performance of GPT-5.1 on language and task levels.

highly stable, showing that our conclusions are insensitive to aggregation granularity. Extending
property-level evaluation to all seven verifiers requires dataset refactoring, e.g., splitting multi-goal
scripts, and tool-specific parsers for per-goal verdicts, which we leave as future work.

6.5     Other Considerations
Improving analyzability bottlenecks. Low analyzability mainly comes from tool-level failures (parse/-
type errors) and timeouts, especially in transformation. Non-analyzable outputs often miss manda-
tory scaffolding (imports/roles/queries) or contain typing/scope mismatches, while analyzable-but-
wrong cases usually mis-encode adversaries/goals, e.g., freshness, binding, and correspondence.
Promising directions include: (i) grammar-constrained decoding or schema-guided generation to
enforce target-language structure and avoid mixed-language fragments. (ii) Two-stage transla-
tion via a tool-agnostic IR of roles, message flows, and goals. (iii) Tool-in-the-loop repair using
parser/type-checker errors and verifier diagnostics, optionally with few-shot scaffolding examples.
   Inconsistent results of various verifiers. Verifiers may disagree on the same scheme due to different
abstractions, supported primitives, and threat/property models. For example, AVISPA can detect
the UKS attack of STS, while tools such as Scyther cannot faithfully encode the required adversary
behaviors. In C.F.B, we resolve such conflicts using canonical labels from cryptographic litera-
ture/standards under specified threat models (§ 3.2). Although resolving cross-tool disagreement
is beyond our scope, C.F.B enables future study through transformation tasks and the multi-tool
harness, which collect verdicts and attack traces to analyze whether disagreements arise from
modeling choices, property definitions, or semantic gaps. False reports may also be reduced by
LLM-assisted attack-path verification with explicit attack scenarios.
   Scalability of model and dimension. We evaluate the newly released GPT-5.1 [55] to show that
C.F.B can incorporate emerging LLMs without changing the pipeline. Figure 17 reports its task-
and language-level results, including execution outcomes, interpretation similarity, and 𝑆 overall .
Compared with GPT-4o-mini and GPT-4o, GPT-5.1 improves the overall score (23.0→35.0→39.2),
likely due to stronger instruction following and adaptive reasoning, but keeps a similar profile:
interpretation/completion are strong, while generation/transformation remain limited by analyz-
ability and timeouts. Beyond model scaling, the same framework can be extended to more verifiers
(e.g., Verifpal [38] and SAPIC+ [17]) and richer protocol families (e.g., 6G and blockchain [43, 70]),
improving coverage and realism.

                                   Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:20                   Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou


   Model contamination. C.F.B includes standard schemes (e.g., Needham-Schroeder, TLS/SSH-style
handshakes, and 5G-AKA) whose descriptions or partial formalizations may appear online, so we
cannot guarantee zero pre-training overlap. However, exposure to high-level schemes is unlikely
to solve our tasks: transformation and correction require tool- and language-specific reasoning.
As experimented in § 5, models perform well on interpretation/completion but still struggle with
generation/transformation across tools. This consistent pattern across open/closed models suggests
that C.F.B mainly probes genuine capability gaps rather than memorized code.

7     Related Work
7.1    Program Synthesis and Symbolic Models
Symbolic models can be viewed as a domain-specific form of programs. Prior work on program
synthesis has studied translating natural language into executable artifacts such as SQL queries [34],
bash commands [44], or general-purpose code [15, 18, 41, 54]. These advances demonstrate that
LLMs can generate structured outputs across domains [42]. However, symbolic specifications differ
fundamentally from SQL or Python. They demand strict grammar, security-critical semantics,
and high precision, while training data is extremely scarce. Multi-stage pipelines for scheme
modeling have been proposed [50], yet systematic evaluation of LLMs on formal security protocols
is still missing. Our work addresses this gap by constructing a large-scale benchmark, enabling
standardized and reproducible evaluation of LLMs on symbolic protocol analysis tasks.

7.2    LLM-Aided Formal Verification
Formal verification has long been used to analyze security properties such as authentication, secrecy,
and replay resistance. Symbolic models (e.g., Dolev-Yao) capture message flows, while computational
proofs provide stronger guarantees under cryptographic assumptions. Recent work applies LLMs
to verification-related tasks, including temporal-logic generation from natural language [16], fine-
tuned specification synthesis [57], interactive correction [20, 31, 50], and proof guidance with
Coq/Lean [56, 61, 65]. However, these studies mainly target logic synthesis or proof assistance. We
instead evaluate end-to-end LLM capabilities across five tasks and seven formal tools, bridging
natural-language scheme descriptions and automated verification.

8     Conclusion and Future Work
This paper presents the first comprehensive and well-designed benchmark C.F.B for formal crypto-
graphic scheme analysis supporting both symbolic and computational security. C.F.B establishes a
unified evaluation framework and comprises 700 cryptographic instances covering 677 distinct
schemes and primitives, encompassing both classical and modern designs, as well as simple and
complex cases. It supports 160 security property verifications and enables systematic measurement
of five LLM capabilities in formal cryptographic scheme analysis. Also, C.F.B incorporates a multi-
dimensional scoring mechanism, offering a comprehensive evaluation of mainstream LLMs. In the
future, we will extend C.F.B with more verifiers and schemes, and develop a verifier-in-the-loop
and agentic LLM framework that integrates the explored strategies for tool-usable formal analysis.

9     Data Availability
We release both the source code and the curated dataset of C.F.B at our online repository [24].

Acknowledgements
This work was partially funded by the National Cryptologic Science Fund of China (2025NCSF01008)
and the fund of Laboratory for Advanced Computing and Intelligence Engineering.


Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                           FSE177:21


References
 [1] Nada AlMarwani and Mona T. Diab. 2021. Discrete Cosine Transform as Universal Sentence Encoder. In ACL/IJCNLP
     (2). Association for Computational Linguistics, 419–426. doi:10.18653/V1/2021.ACL-SHORT.53
 [2] Uri Alon, Shaked Brody, Omer Levy, and Eran Yahav. 2019. code2seq: Generating Sequences from Structured Repre-
     sentations of Code. In ICLR (Poster). OpenReview.net.
 [3] Anthropic. 2024. Claude 3.5 Sonnet. https://www.anthropic.com/news/claude-3-5-sonnet
 [4] Alessandro Armando, David A. Basin, Yohan Boichut, Yannick Chevalier, Luca Compagna, Jorge Cuéllar, Paul Hankes
     Drielsma, Pierre-Cyrille Héam, Olga Kouchnarenko, Jacopo Mantovani, Sebastian Mödersheim, David von Oheimb,
     Michaël Rusinowitch, Judson Santiago, Mathieu Turuani, Luca Viganò, and Laurent Vigneron. 2005. The AVISPA
     Tool for the Automated Validation of Internet Security Protocols and Applications. In CAV (Lecture Notes in Computer
     Science, Vol. 3576). Springer, 281–285. doi:10.1007/11513988_27
 [5] Matteo Avalle, Alfredo Pironti, and Riccardo Sisto. 2014. Formal verification of security protocol implementations: a
     survey. Formal Aspects Comput. 26, 1 (2014), 99–123. doi:10.1007/S00165-012-0269-9
 [6] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev, and Jeremy Avigad.
     2023. ProofNet: Autoformalizing and Formally Proving Undergraduate-Level Mathematics. CoRR abs/2302.12433
     (2023). doi:10.48550/ARXIV.2302.12433
 [7] Manuel Barbosa, Gilles Barthe, Karthik Bhargavan, Bruno Blanchet, Cas Cremers, Kevin Liao, and Bryan Parno. 2021.
     SoK: Computer-Aided Cryptography. In SP. IEEE, 777–795. doi:10.1109/SP40001.2021.00008
 [8] Gilles Barthe, Benjamin Grégoire, Sylvain Heraud, and Santiago Zanella-Béguelin. 2011. Computer-Aided Security
     Proofs for the Working Cryptographer. In CRYPTO (Lecture Notes in Computer Science, Vol. 6841). Springer, 71–90.
     doi:10.1007/978-3-642-22792-9_5
 [9] David A. Basin, Jannik Dreier, Lucca Hirschi, Sasa Radomirovic, Ralf Sasse, and Vincent Stettler. 2018. A Formal
     Analysis of 5G Authentication. In CCS. ACM, 1383–1396. doi:10.1145/3243734.3243846
[10] Yves Bertot and Pierre Castéran. 2004. Interactive Theorem Proving and Program Development - Coq’Art: The Calculus of
     Inductive Constructions. Springer.
[11] Bruno Blanchet. 2001. An Efficient Cryptographic Protocol Verifier Based on Prolog Rules. In CSFW. IEEE Computer
     Society, 82–96. doi:10.1109/CSFW.2001.930138
[12] Bruno Blanchet. 2006. A Computationally Sound Mechanized Prover for Security Protocols. In S&P. IEEE Computer
     Society, 140–154. doi:10.1109/SP.2006.1
[13] Tom Brown, Benjamin Mann, et al. 2020. Language Models are Few-Shot Learners. In Advances in Neural Information
     Processing Systems, Vol. 33. 1877–1901.
[14] Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, et al. 2023. Sparks of Artificial General Intelligence: Early
     experiments with GPT-4. CoRR abs/2303.12712 (2023). doi:10.48550/ARXIV.2303.12712
[15] Mark Chen, Jerry Tworek, Heewoo Jun, et al. 2021. Evaluating Large Language Models Trained on Code. CoRR
     abs/2107.03374 (2021).
[16] Yongchao Chen, Rujul Gandhi, Yang Zhang, and Chuchu Fan. 2023. NL2TL: Transforming Natural Languages to
     Temporal Logics using Large Language Models. In EMNLP. Association for Computational Linguistics, 15880–15903.
     doi:10.18653/V1/2023.EMNLP-MAIN.985
[17] Vincent Cheval, Charlie Jacomme, Steve Kremer, and Robert Künnemann. 2022. SAPIC+: protocol verifiers of the
     world, unite!. In USENIX Security Symposium. USENIX Association, 3935–3952.
[18] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, et al. 2023. PaLM: Scaling Language Modeling with Pathways.
     J. Mach. Learn. Res. 24 (2023), 240:1–240:113.
[19] Véronique Cortier, Steve Kremer, and Bogdan Warinschi. 2011. A Survey of Symbolic Methods in Computational
     Analysis of Cryptographic Systems. J. Autom. Reason. 46, 3-4 (2011), 225–259. doi:10.1007/S10817-010-9187-9
[20] Matthias Cosler, Christopher Hahn, Daniel Mendoza, Frederik Schmitt, and Caroline Trippel. 2023. nl2spec: Interactively
     Translating Unstructured Natural Language to Temporal Logics with Large Language Models. In CAV (2) (Lecture
     Notes in Computer Science, Vol. 13965). Springer, 383–396. doi:10.1007/978-3-031-37703-7_18
[21] Cas J. F. Cremers. 2008. The Scyther Tool: Verification, Falsification, and Analysis of Security Protocols. In CAV (Lecture
     Notes in Computer Science, Vol. 5123). Springer, 414–418. doi:10.1007/978-3-540-70545-1_38
[22] Tim Dierks and Eric Rescorla. 2008. The Transport Layer Security (TLS) Protocol Version 1.2. RFC 5246 (2008), 1–104.
     doi:10.17487/RFC5246
[23] Santiago Escobar, Catherine Meadows, and José Meseguer. 2007. Maude-NPA: Cryptographic Protocol Analysis Modulo
     Equational Properties. In FOSAD (Lecture Notes in Computer Science, Vol. 5705). Springer, 1–50. doi:10.1007/978-3-642-
     03829-7_1
[24] Eval4LLMs. 2025. The code and experiment results of CrypFormBench. [EB/OL]. https://github.com/Eval4LLMs/
     CrypFormBench/tree/main.
[25] Hugging Face. 2025. BAAI/bge-large-en-v1.5. https://huggingface.co/BAAI/bge-large-en-v1.5


                                        Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
FSE177:22                   Z. Li, Q. Zhang, H. Liu, X. Gu, X. Lu, H. Liu, B. Wang, H. Fan, Z. Zhao, R. Zhang, and L. Zhou


[26] Hugging Face. 2025. intfloat/e5-large-v2. https://huggingface.co/intfloat/e5-large-v2
[27] Hugging Face. 2025. Qwen/Qwen2.5-Coder-3B. https://huggingface.co/Qwen/Qwen2.5-Coder-3B
[28] Hugging Face. 2025. Qwen/Qwen3-Embedding-8B. https://huggingface.co/Qwen/Qwen3-Embedding-8B
[29] Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xiaocheng Feng, Ming Gong, Linjun Shou, Bing Qin, Ting Liu,
     Daxin Jiang, and Ming Zhou. 2020. CodeBERT: A Pre-Trained Model for Programming and Natural Languages.
     In EMNLP (Findings) (Findings of ACL, Vol. EMNLP 2020). Association for Computational Linguistics, 1536–1547.
     doi:10.18653/V1/2020.FINDINGS-EMNLP.139
[30] Luyu Gao, Aman Madaan, Shuyan Zhou, et al. 2023. PAL: Program-aided Language Models. In ICML (Proceedings of
     Machine Learning Research, Vol. 202). PMLR, 10764–10799.
[31] Ivan Gavran, Eva Darulova, and Rupak Majumdar. 2020. Interactive synthesis of temporal specifications from examples
     and natural language. Proc. ACM Program. Lang. 4, OOPSLA (2020), 201:1–201:26. doi:10.1145/3428269
[32] Team GLM, Aohan Zeng, Bin Xu, Bowen Wang, Chenhui Zhang, Da Yin, Dan Zhang, Diego Rojas, Guanyu Feng,
     Hanlin Zhao, et al. 2024. Chatglm: A family of large language models from glm-130b to glm-4 all tools. arXiv preprint
     arXiv:2406.12793 (2024). doi:10.48550/ARXIV.2406.12793
[33] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang,
     Xiao Bi, et al. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint
     arXiv:2501.12948 (2025). doi:10.48550/ARXIV.2501.12948
[34] Jiaqi Guo, Zecheng Zhan, Yan Gao, Yan Xiao, Jian-Guang Lou, Ting Liu, and Dongmei Zhang. 2019. Towards Complex
     Text-to-SQL in Cross-Domain Database with Intermediate Representation. In ACL (1). Association for Computational
     Linguistics, 4524–4535. doi:10.18653/V1/P19-1444
[35] Dick Hardt. 2012. The OAuth 2.0 Authorization Framework. RFC 6749 (2012), 1–76. doi:10.17487/RFC6749
[36] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. 2021.
     Measuring Massive Multitask Language Understanding. In ICLR. OpenReview.net.
[37] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda,
     Alan Hayes, Alec Radford, et al. 2024. Gpt-4o system card. arXiv preprint arXiv:2410.21276 (2024). doi:10.48550/ARXIV.
     2410.21276
[38] Nadim Kobeissi, Georgio Nicolas, and Mukesh Tiwari. 2020. Verifpal: Cryptographic Protocol Analysis for the Real
     World. In INDOCRYPT (Lecture Notes in Computer Science, Vol. 12578). Springer, 151–202. doi:10.1007/978-3-030-65277-
     7_8
[39] Patrick Lewis, Ethan Perez, Aleksandra Piktus, et al. 2020. Retrieval-Augmented Generation for Knowledge-Intensive
     NLP Tasks. In NeurIPS. 1–16.
[40] Tingting Li, Ziming Zhao, Zhaoxuan Li, Xiaofei Yue, and Jiongchi Yu. 2026. Fair and Carbon-Aware LLM Routing for
     Web Services. In WWW. ACM, 9563–9571. doi:10.1145/3774904.3793001
[41] Yujia Li, David Choi, Junyoung Chung, et al. 2022. Competition-level code generation with alphacode. Science 378,
     6624 (2022), 1092–1097. doi:10.48550/ARXIV.2203.07814
[42] Yixuan Li, Julian Parsert, and Elizabeth Polgreen. 2024. Guiding Enumerative Program Synthesis with Large Language
     Models. In CAV (2) (Lecture Notes in Computer Science, Vol. 14682). Springer, 280–301. doi:10.1007/978-3-031-65630-9_15
[43] Zhaoxuan Li, Rui Zhang, and Pengchao Li. 2020. A Secure and Efficient Smart Contract Execution Scheme. In ICWS
     (Lecture Notes in Computer Science). Springer, 17–32. doi:10.1007/978-3-030-59618-7_2
[44] Xi Victoria Lin, Chenglong Wang, Deric Pang, Kevin Vu, and Michael D Ernst. 2017. Program synthesis from natural
     language using recurrent neural networks. University of Washington Department of Computer Science and Engineering,
     Seattle, WA, USA, Tech. Rep. UW-CSE-17-03 1 (2017), 1–12.
[45] Nelson F. Liu, Kevin Lin, John Hewitt, et al. 2024. Lost in the Middle: How Language Models Use Long Contexts. Trans.
     Assoc. Comput. Linguistics 12 (2024), 157–173. doi:10.1162/TACL_A_00638
[46] Gavin Lowe. 1995. An Attack on the Needham-Schroeder Public-Key Authentication Protocol. Inf. Process. Lett. 56, 3
     (1995), 131–133. doi:10.1016/0020-0190(95)00144-2
[47] Siqi Lu, Hanjie Dong, Zhaoxuan Li, and Laurence T. Yang. 2024. Not Just Summing: The Identifier Leakage of
     Private-Join-and-Compute and its Improvement. IEEE Trans. Dependable Secur. Comput. 21, 6 (2024), 5143–5155.
     doi:10.1109/TDSC.2024.3371569
[48] Siqi Lu, Zhaoxuan Li, Xuyang Miao, Qingdi Han, and Jianhua Zheng. 2023. PIWS: Private Intersection Weighted Sum
     Protocol for Privacy-Preserving Score-Based Voting With Perfect Ballot Secrecy. IEEE Trans. Comput. Soc. Syst. 10, 3
     (2023), 1039–1056. doi:10.1109/TCSS.2022.3162869
[49] Ziyu Mao, Jingyi Wang, Jun Sun, et al. 2025. LLM-Aided Automatic Modeling for Security Protocol Verification. In
     ICSE. IEEE, 642–654. doi:10.1109/ICSE55347.2025.00197
[50] Ziyu Mao, Jingyi Wang, Jun Sun, Shengchao Qin, and Jiawen Xiong. 2025. LLM-aided Automatic Modeling for Security
     Protocol Verification. In ICSE. doi:10.1109/ICSE55347.2025.00197



Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
Benchmarking Formal Analysis Capability of Large Language Models for Cryptographic Schemes                          FSE177:23


[51] Simon Meier, Benedikt Schmidt, Cas Cremers, and David A. Basin. 2013. The TAMARIN Prover for the Symbolic
     Analysis of Security Protocols. In CAV (Lecture Notes in Computer Science, Vol. 8044). Springer, 696–701. doi:10.1007/978-
     3-642-39799-8_48
[52] Meta. 2025. Llama 4. https://www.llama.com/models/llama-4/
[53] Roger M. Needham and Michael D. Schroeder. 1978. Using Encryption for Authentication in Large Networks of
     Computers. Commun. ACM 21, 12 (1978), 993–999. doi:10.1145/359657.359659
[54] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, et al. 2023. CodeGen: An Open Large Language Model for Code with
     Multi-Turn Program Synthesis. In ICLR. OpenReview.net.
[55] OpenAI. 2025. GPT-5.1: A smarter, more conversational ChatGPT. https://openai.com/index/gpt-5-1/
[56] Stanislas Polu and Ilya Sutskever. 2020. Generative Language Modeling for Automated Theorem Proving. CoRR
     abs/2009.03393 (2020).
[57] Colin Raffel, Noam Shazeer, Adam Roberts, et al. 2020. Exploring the Limits of Transfer Learning with a Unified
     Text-to-Text Transformer. J. Mach. Learn. Res. 21 (2020), 140:1–140:67.
[58] Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In
     EMNLP/IJCNLP (1). Association for Computational Linguistics, 3980–3990. doi:10.18653/V1/D19-1410
[59] Raúl Rojas. 2015. A Tutorial Introduction to the Lambda Calculus. CoRR abs/1503.09060 (2015).
[60] Gemini Team. 2025. Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and
     Next Generation Agentic Capabilities. CoRR abs/2507.06261 (2025). doi:10.48550/ARXIV.2507.06261
[61] Haiming Wang, Ye Yuan, Zhengying Liu, et al. 2023. DT-Solver: Automated Theorem Proving with Dynamic-Tree
     Sampling Guided by Proof-level Value Function. In ACL (1). Association for Computational Linguistics, 12632–12646.
     doi:10.18653/V1/2023.ACL-LONG.706
[62] Jason Wei, Yi Tay, Rishi Bommasani, et al. 2022. Emergent Abilities of Large Language Models. Trans. Mach. Learn.
     Res. 2022 (2022).
[63] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny
     Zhou. 2022. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. In NeurIPS.
[64] xAI. 2025. Grok 3. https://x.ai/grok
[65] Kaiyu Yang, Aidan M. Swope, Alex Gu, et al. 2023. LeanDojo: Theorem Proving with Retrieval-Augmented Language
     Models. In NeurIPS.
[66] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. 2023. Tree of
     Thoughts: Deliberate Problem Solving with Large Language Models. In NeurIPS.
[67] Tatu Ylönen and Chris Lonvick. 2006. The Secure Shell (SSH) Authentication Protocol. RFC 4252 (2006), 1–17.
     doi:10.17487/RFC4252
[68] Xiaofei Yue, Fangming Zhao, Fulun Ye, Jiongchi Yu, Zhaoxuan Li, Tingting Li, Ziming Zhao, and Jianwei Yin. 2026.
     HeteroSim: Towards High-Fidelity Heterogeneous LLM Training Simulation on GPUs. In WWW. ACM, 5189–5197.
     doi:10.1145/3774904.3792254
[69] Jiyang Zhang, Pengyu Nie, Junyi Jessy Li, and Milos Gligoric. 2023. Multilingual Code Co-evolution using Large
     Language Models. In ESEC/SIGSOFT FSE. ACM, 695–707. doi:10.1145/3611643.3616350
[70] Rui Zhang, Zhaoxuan Li, and Lijuan Zheng. 2021. Secure and Efficient Key Hierarchical Management and Collaborative
     Signature Schemes of Blockchain. In ICAIS (2) (Lecture Notes in Computer Science). Springer, 332–345. doi:10.1007/978-
     3-030-78612-0_27
[71] Ziming Zhao, Zhaoxuan Li, Tingting Li, and Fan Zhang. 2025. CyberLLM: Enable Mapping CVE to Tactics and
     Techniques of Cyber Threats via LLM. In DASFAA (5) (Lecture Notes in Computer Science). Springer, 473–488. doi:10.
     1007/978-981-95-4155-3_33
[72] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan
     Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. 2023. Judging LLM-as-a-Judge with
     MT-Bench and Chatbot Arena. In NeurIPS.
[73] Qihao Zhu, Daya Guo, Zhihong Shao, Dejian Yang, Peiyi Wang, Runxin Xu, Y Wu, Yukun Li, Huazuo Gao, Shirong
     Ma, et al. 2024. Deepseek-coder-v2: Breaking the barrier of closed-source models in code intelligence. arXiv preprint
     arXiv:2406.11931 (2024). doi:10.48550/ARXIV.2406.11931

Received 2025-09-12; accepted 2026-03-24




                                       Proc. ACM Softw. Eng., Vol. 3, No. FSE, Article FSE177. Publication date: July 2026.
