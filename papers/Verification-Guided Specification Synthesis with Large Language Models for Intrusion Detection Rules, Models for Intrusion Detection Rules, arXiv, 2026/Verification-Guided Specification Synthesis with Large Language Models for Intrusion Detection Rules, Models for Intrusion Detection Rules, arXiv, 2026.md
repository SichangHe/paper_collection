                                         Verification-Guided Specification Synthesis with Large Language
                                                       Models for Intrusion Detection Rules
                                                                        Kohei Yamamoto                                                                     Marie Katsurai
                                                              yamamoto26@mm.doshisha.ac.jp                                                            katsurai@mm.doshisha.ac.jp
                                                                   Doshisha University                                                                    Doshisha University
                                                                Kyotanabe-shi, Kyoto, Japan                                                           Kyotanabe-shi, Kyoto, Japan

                                         Abstract                                                                                protection through intrusion detection systems (IDSs) remains an
                                         Attacks against Internet-connected IoT devices continue to increase;                    important defense mechanism. In practice, transforming newly
                                         however, transforming observed attack traffic into deployable intru-                    observed attack traffic into deployable IDS rules remains largely a
                                         sion detection system (IDS) rules remains largely a manual process.                     manual process requiring substantial security expertise and rule-
arXiv:2608.22889v1 [cs.CR] 24 Aug 2026




                                         Recent studies have explored using large language models (LLMs)                         authoring effort [5, 15], creating a delay between attack observation
                                         to generate IDS rules; nonetheless, existing approaches often re-                       and rule deployment.
                                         quire auxiliary information beyond observed traffic or generate                            Recent advances in large language models (LLMs) have demon-
                                         rules without validating their detection logic against benign traffic.                  strated their potential to assist security analysts in extracting knowl-
                                         This study presents a verification-guided specification synthesis                       edge from unstructured security observations [2]. Several studies
                                         framework for generating Suricata rules directly from HTTP re-                          have explored using LLMs with attack-related sources, such as
                                         quest traces. Instead of having an LLM generate IDS rules in a single                   vulnerability descriptions, cyber threat intelligence (CTI) reports,
                                         step, an LLM first identifies a vulnerable parameter and synthesizes                    exploit code, and attack traces [7, 9, 14] to construct deployable de-
                                         a semantic detection specification. These specifications are itera-                     tection rules for signature-based IDSs, such as Suricata1 . However,
                                         tively refined through counterexample-guided inductive synthesis                        although attack requests themselves are easily available from hon-
                                         (CEGIS), in which benign traffic samples serve as counterexam-                          eypots and monitoring systems [12, 13], the auxiliary information
                                         ples during synthesis and verification. Verified specifications are                     required by existing approaches is often unavailable immediately
                                         then deterministically compiled into Suricata rules. Experiments                        after an attack is observed. Furthermore, because LLMs are typi-
                                         on 281 real-world CVEs and benign traffic collected from real IoT                       cally prompted to generate Suricata rules in a single step, without
                                         devices show that the proposed method achieves a detection rate                         validating the generated detection logic against benign traffic [7],
                                         of 81.5% while maintaining a false positive rate of 0.0%. An ablation                   generated rules may overfit the observed attack examples and pro-
                                         study also demonstrates that CEGIS-based verification improves                          duce false positives on legitimate communications. In operational
                                         detection performance while maintaining a low false positive rate.                      settings, IDS rules are expected not only to detect attacks but also
                                                                                                                                 to avoid triggering on benign traffic. Therefore, before a rule is
                                         CCS Concepts                                                                            deployed, the underlying detection condition should be verified
                                                                                                                                 against examples that represent legitimate behavior.
                                         • Security and privacy → Artificial immune systems; • Com-
                                                                                                                                    This paper presents a verification-guided framework that gener-
                                         puting methodologies → Information extraction.
                                                                                                                                 ates intrusion detection rules directly from HTTP request traces.
                                                                                                                                 Instead of prompting an LLM to generate Suricata syntax, we use
                                         Keywords
                                                                                                                                 the LLM to synthesize semantic detection specifications that char-
                                         IoT attacks, verification, intrusion detection rules, large language                    acterize attack behavior, including vulnerable parameters and at-
                                         models, counterexample-guided inductive synthesis                                       tack mechanisms. The specifications are iteratively refined through
                                         ACM Reference Format:                                                                   counterexample-guided inductive synthesis (CEGIS) [16], where
                                         Kohei Yamamoto and Marie Katsurai. 2026. Verification-Guided Specifica-                 benign traffic samples serve as counterexamples during synthe-
                                         tion Synthesis with Large Language Models for Intrusion Detection Rules.                sis and verification. Only verified specifications are compiled into
                                         In Proceedings of the 35th ACM International Conference on Information                  deployable Suricata rules. Experiments on 281 real-world CVEs
                                         and Knowledge Management (CIKM ’26), November 07–11, 2026, Rome, Italy.                 and benign traffic collected from real IoT environments demon-
                                         ACM, New York, NY, USA, 5 pages. https://doi.org/10.1145/3799682.3840077
                                                                                                                                 strate that the proposed framework achieves high attack detection
                                                                                                                                 performance while effectively suppressing false positives. Further-
                                         1    Introduction                                                                       more, comparisons with direct LLM-based rule generation meth-
                                         Large-scale attacks on Internet-connected IoT devices continue to                       ods and ablation studies confirm the effectiveness of separating
                                         be observed [11]. Since many vulnerable IoT devices have reached                        specification synthesis from rule compilation and of incorporating
                                         end-of-life and no longer receive firmware updates, network-based                       counterexample-guided verification.
                                                                                                                                    The main contributions of this paper are twofold: (i) we propose
                                                                                                                                 a novel LLM-based framework that extracts vulnerable parameters
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   and attack mechanisms directly from HTTP request traces and
                                         CIKM ’26, Rome, Italy                                                                   refines synthesized specifications through counterexample-guided
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2539-5/2026/11
                                         https://doi.org/10.1145/3799682.3840077                                                 1 https://suricata.io/
CIKM ’26, November 07–11, 2026, Rome, Italy                                                                                                                                                     Yamamoto and Katsurai



                                     Phase 1: Specification synthesis and verification (LLM-based)
                                                                                                                                                        Phase 2: Rule compilation (no LLM)
                                                       Propose a candidate          Mock-server         Pass                 HTTP request,                                                            Verified
                                                         specification as a         verification                         vulnerable parameter,
                                                                                                                         attack characteristics
                                                                                                                                                        Compiler        Rule-specificity test       Suricata rule
                             (LLM)                       Python predicate
        HTTP trace                                                                           Fail
      (requests only)    Analyze the                    Diagnose why the
                        attack request                      candidate              Counterexample
                                                       specification failed
                                                           verification
                                                                                                                                                                                   Too broad
                                                                                         The framework extends CEGIS by having the LLM diagnose                               Rejected
                                     Iteration limit reached (generation failed)         failure causes, not just add counterexamples as constraints.
                                                                     No rule generated

                                                                         Figure 1: Overview of the proposed method.


verification before compiling them into Suricata rules; and (ii) we                                                  3       Proposed Method
introduce an evaluation protocol that separates benign traffic used                                                  In operational IDS settings, attack requests are often the only arti-
for specification synthesis from benign traffic used for evaluation                                                  facts immediately available after an attack is observed. Thus, the
and evaluates all methods using identical attack traces, IDS settings,                                               proposed framework operates directly on HTTP request traces and
and LLM configurations. The experiments reveal distinct limitations                                                  generates verified Suricata rules without requiring HTTP responses,
across approaches: conventional non-LLM methods frequently fail                                                      firmware images, or vulnerability descriptions. As illustrated in
to generate rules that correctly detect their target attacks, while                                                  Figure 1, the framework consists of two phases: (1) specification
LLM-based methods often produce rules that fail to trigger correctly                                                 synthesis and verification and (2) rule compilation. The key design
in Suricata.                                                                                                         principle is to separate specification synthesis from rule compila-
                                                                                                                     tion. LLMs are used to derive detection specifications from HTTP
                                                                                                                     attack requests, while a compiler deterministically translates the
                                                                                                                     HTTP request and the corresponding analysis result into deploy-
                                                                                                                     able Suricata rules. This separation avoids relying on LLMs for
                                                                                                                     generating syntax-sensitive Suricata rules and enables verification
2    Related Work
                                                                                                                     at the specification level before rule compilation.
Automatic IDS rule generation has been studied using a variety of
signature synthesis techniques. For example, Syrius [1] prepares
overly specific seed rules and refines them using benign traffic,
whereas CMIRGen [18] and AutoCombo [3] generate signatures                                                           3.1         Verification-Guided Specification Synthesis
through clustering, rule mining, and frequent-pattern discovery                                                      The LLM first analyzes an HTTP attack request and identifies a
techniques. Because these approaches derive signatures from sta-                                                     parameter that is likely to serve as the attack entry point. Many
tistical differences between attack and benign traffic, they may                                                     requests contain both security-relevant and irrelevant fields, and
fail to identify attacks whose syntax closely resembles legitimate                                                   directly generating rules from the entire request often leads to
communications.                                                                                                      overly general detection logic. Therefore, the parameter is selected
   Among recent LLM-based approaches, FALCON [9] generates                                                           according to its likely operational role within the target service,
IDS and malware detection rules from CTI reports, while RuleX-                                                       such as command execution, data access, path construction, or
ploit [14] generates Suricata rules from exploit code and iteratively                                                access control. The analysis relies solely on the observed HTTP
repairs them using attack traffic. GRIDAI [7] directly generates and                                                 request and does not require external vulnerability information.
repairs Suricata rules from HTTP attack requests using multiple                                                      For requests that do not contain a plausible attack entry point, no
cooperating LLM agents; this is the most closely related to ours                                                     rule is generated.
in terms of inputs. RuleForge [4] generates detection rules from                                                        After identifying a vulnerable parameter, the LLM proposes a
templates in an open-source vulnerability scanner, while UniR-                                                       candidate semantic detection specification. Specifically, rather than
ule [8] generates detection rules from natural-language require-                                                     generating IDS rules in a single step, the LLM is instructed to
ments. These LLM-based methods generate detection rules in a                                                         characterize the conditions under which a parameter value should
single step, without incorporating benign traffic as counterexam-                                                    be considered malicious. To guide synthesis, benign values collected
ples during rule construction.                                                                                       from public IoT traffic datasets (e.g., [11, 17]) and the attack value
   Our study differs from the above studies in several aspects. The                                                  observed in the target request are provided as negative and positive
proposed method requires neither CTI reports, exploit code, at-                                                      examples, respectively. Specifically, we choose representative values
tacker labels, nor labeled benign corpora. It operates directly on                                                   of a parameter by applying 𝑘-medoids clustering to its values in
HTTP request traces. Instead of generating Suricata rules in a single                                                benign traffic data. In our preliminary experiments, the choice of 𝑘
step, an LLM synthesizes semantic detection specifications, which                                                    does not significantly change the overall performance. The LLM
are refined and verified using benign traffic as counterexamples                                                     then generates a Python predicate that distinguishes the attack
through CEGIS before being compiled into Suricata rules.                                                             value from benign ones. This intermediate representation captures
Verification-Guided Specification Synthesis with Large Language Models for Intrusion Detection Rules                          CIKM ’26, November 07–11, 2026, Rome, Italy


the attack semantics while remaining independent of any IDS-                              Table 1: Attack Dataset Used for Suricata Rule Generation
specific syntax.
    The generated specification is verified using the CEGIS strategy,                                  Vulnerability class            Count      Ratio (%)
a program-synthesis framework in which candidate solutions are
                                                                                                       Command injection                  132             47.0
iteratively refined using counterexamples produced by a verifier.
                                                                                                       Other                               51             18.1
In the proposed framework, the LLM acts as the synthesizer by
                                                                                                       Authentication bypass               45             16.0
generating candidate detection specifications, while a verifier eval-
                                                                                                       Information disclosure              30             10.7
uates them on a mock server that emulates the target service. The
                                                                                                       Path traversal                      23              8.2
mock server is a lightweight web server generated by the LLM; it
receives attack requests at the same endpoint paths as the target                                      Total attacks                      281         100.0
service and processes the identified vulnerable parameter, eliminat-
ing the need to access real vulnerable devices. This setup enables
the framework to determine whether the identified parameter in-                          is entirely deterministic, identical inputs always produce identical
fluences server behavior and whether the synthesized specification                       outputs without additional LLM-based repair or syntax correction.
distinguishes attack inputs from benign values. Verification consists                    Implementation details, prompts, source code, and additional rule
of four checks: (1) the attack request elicits a valid server response,                  generation examples are publicly available.2
(2) modifying the identified parameter changes server behavior, (3)
multiple benign values extracted from real traffic do not satisfy the                    4 Experiments
specification, and (4) the processing of the vulnerable parameter
is observable in server logs. The first two checks confirm that the                      4.1 Experimental Settings
attack affects the emulated service as intended, the third ensures                       We collected 281 distinct CVEs, comprising 36 CVEs represented by
that benign values are not falsely classified as malicious, and the                      attack traces from an open research dataset [13] and 245 CVEs from
fourth verifies that the parameter is actually processed by the server.                  the CISA Known Exploited Vulnerabilities catalog3 . For the 245
Any failed check is treated as a counterexample and returned to                          KEV vulnerabilities, we manually reconstructed each attack request
the synthesizer.                                                                         from public exploit code or advisory descriptions. We selected only
    When a specification fails verification, the framework diagnoses                     vulnerabilities affecting IoT or network devices that can be exploited
the cause of the failure and then generates a revised specification ac-                  through a single HTTP request. Table 1 summarizes the resulting
cordingly. Candidate specifications, counterexamples, and diagnos-                       attack dataset, covering 49 vendors and five vulnerability categories.
tic results are stored in memory and reused in subsequent iterations                        To evaluate false positives under realistic deployment condi-
to avoid repeating previous mistakes. The synthesis-verification                         tions, we used 281 benign communications in the UNSW-IoTraffic
loop is repeated for at most 13 iterations, a limit determined em-                       dataset [17], collected from real IoT devices, using stratified sam-
pirically in this study. If no valid specification is obtained within                    pling over device types and HTTP methods. For specification syn-
the iteration limit, the attack is discarded and no Suricata rule is                     thesis, representative benign parameter values were calculated us-
generated. Our method favors explicit non-generation over deploy-                        ing CICIoT2023 [11] in addition to UNSW-IoTraffic. CICIoT2023
ing unverified rules, which may either miss attacks or trigger on                        provides benign body-parameter values that are insufficiently repre-
benign traffic. The synthesized detection specification is used only                     sented in UNSW-IoTraffic. To avoid data leakage, the 281 evaluation
during CEGIS-based verification and is not embedded in the final                         samples were excluded from this calculation. Although the synthe-
rule. Instead, verification establishes that the identified vulnerable                   sis and evaluation sets originate from the same datasets and may
parameter is consistent with the observed attack behavior.                               share some parameter values, the proposed method restricts rule
                                                                                         matching to specific endpoints and parameter names, reducing the
                                                                                         risk that such overlap directly affects evaluation on benign traffic.
3.2     Rule Compilation                                                                    We compare the proposed method against GRIDAI [7], RuleX-
Once a specification is verified, the compiler constructs a Suricata                     ploit [14], Moreno [10], CMIRGen [18], and AutoCombo [3]. Meth-
rule from the analysis results. Specifically, the compiler receives                      ods other than GRIDAI and the proposed method used the auxiliary
the original HTTP request and the LLM’s analysis result, which                           information obtained for each attack. All LLM-based methods, in-
includes the identified vulnerable parameter and attack charac-                          cluding the proposed method, used Qwen3-8B-BF16 running locally.
teristics, such as the payload syntax. It deterministically extracts                     Each method was evaluated on 281 attacks over three random seeds,
the HTTP method, request path, attack value, and parameter loca-                         yielding 843 attack instances per method. Results were averaged
tion from the request, and maps the parameter to the appropriate                         over the three random seeds. Generated rules were evaluated using
Suricata matching buffer according to the request structure. For                         Suricata 6.0.4.
example, parameters are matched in the request body for POST
requests and in the URI for GET requests.                                                4.2      Detection and False-Positive Performance
   To avoid overly broad signatures, generated rules are subjected                       We evaluate generated rules using detection rate (DR) and false
to a rule-specificity test. Rules that match only generic request                        positive rate (FPR), both measured at the actual Suricata triggering
properties, such as the HTTP method and path, are discarded be-
cause they are likely to trigger on benign traffic. The remaining                        2 https://github.com/mm-doshisha/CIKM2026-iot-vuln-pipeline

rules are emitted as verified Suricata rules. Since rule compilation                     3 https://www.cisa.gov/known-exploited-vulnerabilities-catalog
CIKM ’26, November 07–11, 2026, Rome, Italy                                                                                       Yamamoto and Katsurai


Table 2: Detection Rate (DR) and False Positive Rate (FPR)                      degradation, reducing DR from 81.5% to 41.3%. This result indicates
for All Methods                                                                 that attack understanding alone is insufficient for generating effec-
                                                                                tive rules; iterative refinement using counterexamples is the main
 Method                Category                             DR (%)    FPR (%)   contribution of the proposed method. Removing counterexample
                                                                                diagnosis reduces DR to 57.8%, suggesting that counterexamples
 Proposed              LLM Specification + Compiler            81.5       0.0
                                                                                are useful not only for rejecting incorrect specifications but also for
 RuleXploit [14]       Direct LLM rule generation              72.7       5.3
                                                                                guiding synthesis toward more discriminative attack descriptions.
 GRIDAI [7]            Direct LLM rule generation              69.5       0.5
                                                                                Notably, counterexample diagnosis accounts for a substantial por-
 CMIRGen [18]          Signature generation                    54.9      10.3
                                                                                tion of the performance gain provided by the CEGIS-based refine-
 AutoCombo [3]         Signature generation                    40.9       4.3
                                                                                ment process. The compiler also contributes substantially, reducing
 Moreno+ [10]          Direct LLM rule generation              14.7       0.0
                                                                                DR by 10.7 percentage points when removed. In this configuration,
                                                                                the LLM generates Suricata rules directly from the analysis result,
                  Table 3: Ablation Study Results                               bypassing rule compilation. Interestingly, none of the ablations in-
                                                                                crease deployment-time FPR, which remains 0.0% in all cases. This
 Configuration                           DR (%)      ΔDR (percentage points)    observation suggests that the synthesis-verification loop primarily
                                                                                contributes to improving detection performance, while rule com-
 Full system (proposed)                       81.5                        —     pilation provides deterministic and operationally consistent rule
 w/o CEGIS loop                               41.3                     -40.2    construction. Overall, the ablation results indicate complementary
 w/o counterexample diagnosis                 57.8                     -23.7    roles within the framework: counterexample-guided verification im-
 w/o compiler                                 70.8                     -10.7    proves attack detection, while rule compilation supports consistent
                                                                                rule generation.

layer. DR is the percentage of attack instances detected by gener-
                                                                                4.4    Failure Analysis
ated rules. Attacks for which no rule can be generated are counted
as misses. FPR is the percentage of benign IoT communications that              We analyze why DR does not reach 100% even when evaluated on
incorrectly trigger generated rules and directly reflects operational           the same attacks used for rule generation. The failure modes differ
false alarms. DR is evaluated using the same attack traces from                 across methods. The LLM-based baselines (RuleXploit, GRIDAI, and
which rules are generated. Although this corresponds to evaluation              Moreno) generate rules for most attacks, but many of these rules
on the generation data rather than unseen attacks, the objective of             fail to trigger in Suricata because of incorrect matching strings
IDS rule generation is to construct rules that correctly detect the             or buffer specifications. In contrast, the primary failure mode of
given attack when deployed in Suricata. Therefore, DR measures                  CMIRGen and AutoCombo is the inability to generate rules for
the success rate of rule generation rather than generalization per-             attacks that lack discriminative tokens or attributes. The proposed
formance. Similar evaluation protocols are commonly adopted in                  method exhibits a different behavior: almost all generated rules
prior work [1, 10, 14].                                                         function correctly, and failures occur primarily when no valid detec-
    Table 2 shows the results of all methods. The proposed method               tion specification can be synthesized. Specifically, there are attacks
achieves a DR of 81.5% while maintaining an FPR of 0.0%, making                 for which CEGIS fails to identify a specification that matches the
it the only method that simultaneously achieves high detection per-             attack value while rejecting all benign values.
formance and zero false positives among all evaluated approaches.                  Failure rates vary across vulnerability classes. Command-injection
The remaining 18.5% of attack instances correspond to cases where               and path-traversal attacks are usually detected because they contain
no Suricata rule could be generated. RuleXploit and GRIDAI achieve              distinctive syntactic patterns such as shell metacharacters or tra-
competitive detection rates, but incur substantially higher false-              versal strings. In contrast, authentication-bypass and information-
positive rates because generated rules often match broader request              disclosure vulnerabilities often lack distinguishing request-level fea-
patterns. In contrast, Moreno achieves an FPR of 0.0% but detects               tures. Since the proposed framework relies solely on HTTP requests,
only 14.7% of attacks. CMIRGen and AutoCombo rely on benign                     attacks whose maliciousness depends primarily on server-side state
data during rule generation; when evaluated on previously unseen                or response content remain difficult to characterize. Solving this
benign traffic, both methods exhibit substantially lower detection              limitation will be an important direction for future work.
rates and higher false-positive rates than the proposed method.
    The low FPR of the proposed framework can be attributed to                  5     Conclusion and Future Work
deterministic rule construction. Generated rules restrict matching              This paper presented a CEGIS-based framework for generating in-
to specific endpoints and vulnerable parameters and apply matching              trusion detection rules from HTTP request traces. Experiments on
conditions derived from the observed attack value only within those             281 real-world CVEs and 281 benign IoT communications demon-
contexts. Consequently, unrelated benign traffic rarely satisfies the           strated that the proposed method achieves an 81.5% detection
matching conditions.                                                            rate while maintaining an FPR of 0.0%. The ablation study further
                                                                                showed that counterexample-guided verification is the primary
4.3     Ablation Study                                                          contributor to detection performance, whereas rule compilation
Table 3 reports the contribution of individual components. Remov-               supports deterministic and operationally consistent rule construc-
ing the CEGIS refinement loop causes the largest performance                    tion.
Verification-Guided Specification Synthesis with Large Language Models for Intrusion Detection Rules                            CIKM ’26, November 07–11, 2026, Rome, Italy


   Several directions remain for future work. First, while the current                        for Revealing Current IoT Threats. Journal of Information Processing 24, 3 (2016),
evaluation measures rule-generation success on observed attacks,                              522–533. doi:10.2197/ipsjjip.24.522
                                                                                         [13] Yumingzhi Pan, Zhen Ling, Yue Zhang, Hongze Wang, Guangchi Liu, Junzhou
future benchmarks should include multiple attack variants for the                             Luo, and Xinwen Fu. 2025. TORCHLIGHT: Shedding LIGHT on Real-World
same vulnerability to evaluate generalization to unseen payloads                              Attacks on Cloudless IoT Devices Concealed within the Tor Network. In 34th
                                                                                              USENIX Security Symposium (USENIX Security 25). 1053–1072.
and encodings. Second, extending verification with real devices or                       [14] Angelos Papoutsis, Athanasios Dimitriadis, Ilias Koritsas, Dimitrios Kavallieros,
emulation environments [6] may enable detection of attack classes                             Theodora Tsikrika, Stefanos Vrochidis, and Ioannis Kompatsiaris. 2025. RuleX-
whose maliciousness depends primarily on server-side state, such                              ploit: A Framework for Generating Suricata Rules from Exploits Using Generative
                                                                                              AI. In Proc. IEEE Int. Conf. on Cyber Security and Resilience (CSR). IEEE, 267–274.
as authentication bypass and information disclosure vulnerabili-                              doi:10.1109/CSR64739.2025.11130010
ties. Finally, the current framework assumes attack traffic collected                    [15] Karen Scarfone, Peter Mell, et al. 2007. Guide to intrusion detection and preven-
from honeypots or monitoring points; evaluating its robustness                                tion systems (IDPS). NIST Special Publication 800, 2007 (2007), 94.
                                                                                         [16] Armando Solar-Lezama, Rodric Rabbah, Rastislav Bodík, and Kemal Ebcioğlu.
in environments where attack and benign traffic are mixed is an                               2005. Programming by sketching for bit-streaming programs. In Proceedings of
important direction for practical deployment.                                                 the 2005 ACM SIGPLAN conference on Programming language design and imple-
                                                                                              mentation. 281–294.
                                                                                         [17] Savindu Wannigama, Arunan Sivanathan, and Hassan Habibi Gharakheili. 2025.
6    GenAI Usage Disclosure                                                                   Descriptor: UNSW IoT Traffic Data With Packets, Flows, and Protocols (UNSW-
                                                                                              IoTraffic). IEEE Data Descriptions 2 (2025), 311–323. doi:10.1109/IEEEDATA.2025.
The authors used ChatGPT and Claude to assist with manuscript                                 3602010
editing, language translation, and code development. All outputs                         [18] Runzi Zhang, Mingkai Tong, Lei Chen, Jianxin Xue, Wenmao Liu, and Feng
                                                                                              Xie. 2020. CMIRGen: Automatic Signature Generation Algorithm for Malicious
produced by these tools were verified and modified by the authors.                            Network Traffic. In 2020 IEEE 19th International Conference on Trust, Security and
ChatGPT was also used to generate decorative icon images that                                 Privacy in Computing and Communications (TrustCom). 736–743. doi:10.1109/
                                                                                              TrustCom50675.2020.00101
appear in Figure 1. The generated icons were used only for vi-
sualization purposes. The authors are solely responsible for the
manuscript content, methodology, experimental results, and con-
clusions presented in this paper.

References
 [1] L. R. P. de Alcântara, G. R. N. A. de Barros Padilha, Rui Abreu, and Marcelo
     d’Amorim. 2022. Syrius: Synthesis of Rules for Intrusion Detectors. IEEE Trans-
     actions on Reliability 71, 1 (2022), 370–381. doi:10.1109/TR.2021.3061297
 [2] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu,
     Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. 2024. PentestGPT:
     Evaluating and Harnessing Large Language Models for Automated Penetration
     Testing. In 33rd USENIX Security Symposium (USENIX Security 24). 847–864.
 [3] Min Du, Wenjun Hu, and William Hewlett. 2021. AutoCombo: Automatic Mal-
     ware Signature Generation Through Combination Rule Mining. In Proc. 30th
     ACM Int. Conf. on Information and Knowledge Management (CIKM). 3777–3786.
     doi:10.1145/3459637.3481896
 [4] Ayush Garg, Sophia Hager, Jacob Montiel, Aditya Tiwari, Michael Gentile,
     Zach Reavis, David Magnotti, and Wayne Fullen. 2026. RuleForge: Auto-
     mated Generation and Validation for Web Vulnerability Detection at Scale.
     arXiv:2604.01977 [cs.CR] https://arxiv.org/abs/2604.01977
 [5] Mohammad Akidul Hoque, Anuradha Choudhury, Jaime Acosta, M. Shahriar
     Hossain, and Monika Akbar. 2025. Data-Driven IDS Rule Generation for Detecting
     Malicious Traffic. In 2025 IEEE International Conference on Data Mining Workshops
     (ICDMW). 1357–1365. doi:10.1109/ICDMW69685.2025.00161
 [6] Mingeun Kim, Dongkwan Kim, Eunsoo Kim, Suryeon Kim, Yeongjin Jang, and
     Yongdae Kim. 2020. FirmAE: Towards Large-Scale Emulation of IoT Firmware
     for Dynamic Analysis. In Proc. Annual Computer Security Applications Conference
     (ACSAC). 733–745. doi:10.1145/3427228.3427294
 [7] Jiarui Li, Yuhan Chai, Lei Du, Chenyun Duan, Hao Yan, and Zhaoquan Gu. 2025.
     GRIDAI: Generating and Repairing Intrusion Detection Rules via Collaboration
     among Multiple LLM-based Agents. arXiv:2510.13257 [cs.CR] https://arxiv.org/
     abs/2510.13257
 [8] Cheng Meng, Wenxin Le, Xinyi Li, Qiuyun Wang, Fangli Ren, Zhengwei Jiang,
     and Baoxu Liu. 2026. From Context to Rules: Toward Unified Detection Rule
     Generation. arXiv:2604.11078 [cs.CR] https://arxiv.org/abs/2604.11078
 [9] Shaswata Mitra, Azim Bazarov, Martin Duclos, Sudip Mittal, Aritran Piplai,
     Md Rayhanur Rahman, Edward Zieglar, and Shahram Rahimi. 2025. FALCON: Au-
     tonomous Cyber Threat Intelligence Mining with LLMs for IDS Rule Generation.
     arXiv:2508.18684 [cs.CR] https://arxiv.org/abs/2508.18684
[10] Manez Moreno, Xabier Sáez de Cámara, Aitor Urbieta, and Mikel Iturbe. 2025.
     Leveraging LLMs for Automated IDS Rule Generation: A Novel Methodology
     for Securing Industrial Environments. In Actas de las X Jornadas Nacionales de
     Investigación en Ciberseguridad (JNIC). 113–120. ISBN 978-84-10169-61-6.
[11] Euclides Carlos Pinto Neto, Sajjad Dadkhah, Raphael Ferreira, Alireza Zohourian,
     Rongxing Lu, and Ali A. Ghorbani. 2023. CICIoT2023: A Real-Time Dataset and
     Benchmark for Large-Scale Attacks in IoT Environment. Sensors 23, 13 (2023),
     5941. doi:10.3390/s23135941
[12] Yin Minn Pa Pa, Shogo Suzuki, Katsunari Yoshioka, Tsutomu Matsumoto,
     Takahiro Kasama, and Christian Rossow. 2016. IoTPOT: A Novel Honeypot
