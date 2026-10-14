                                                                                                                                                          (Special Session)
                                                                      This paper will be presented at IEEE VLSI Test Symposium (VTS) 2026

                                                AI-Assisted Hardware Security Verification: A
                                                   Survey and AI Accelerator Case Study
                                                      Khan Thamid Hasan, Md Ajoad Hasan, Nashmin Alam, Md. Touhidul Islam, Upoma Das, Farimah Farahmandi
                                                           Department of Electrical and Computer Engineering, University of Florida, Gainesville, FL, USA
                                                        {khanthamidhasan, md.hasan, nashminalam, mdtouhidul.islam, upoma.das}@ufl.edu, farimah@ece.ufl.edu

                                           Abstract—As hardware systems grow in complexity, security               they also warn that trust, grounding, and hallucination remain
                                        verification must keep up with them. Recently, artificial intel-           central concerns [28]–[31]. In parallel, LLMs have already
                                        ligence (AI) and large language models (LLMs) have started                 shown strong utility in adjacent hardware-design tasks such
                                        to play an important role in automating several stages of
                                        the verification workflow by helping engineers analyze designs,            as register-transfer level (RTL) generation, domain adapta-
                                                                                                                   tion, self-correcting testbench generation, coverage-oriented
arXiv:2604.01572v1 [cs.CR] 2 Apr 2026




                                        reason about potential threats, and generate verification artifacts.
                                        This survey synthesizes recent advances in AI-assisted hardware            prompting, and hallucination mitigation [32]–[38]. Those ca-
                                        security verification and organizes the literature along key               pabilities naturally motivate their extension into security-
                                        stages of the workflow: asset identification, threat modeling,             oriented planning, property generation, vulnerability analysis,
                                        security test-plan generation, simulation-driven analysis, formal
                                        verification, and countermeasure reasoning. To illustrate how              and workflow orchestration.
                                        these techniques can be applied in practice, we present a case                This paper surveys AI/LLM-based security verification
                                        study using the open-source NVIDIA Deep Learning Accelerator               along the key stages commonly followed by verification engi-
                                        (NVDLA), a representative modern hardware design. Throughout               neers: asset identification, threat modeling, security test-plan
                                        this study, we emphasize that while AI/LLM-based automation                generation, construction of simulation and formal verification
                                        can significantly accelerate verification tasks, its outputs must
                                        remain grounded in simulation evidence, formal reasoning, and              artifacts, and reasoning about potential countermeasures. We
                                        benchmark-driven evaluation to ensure trustworthy hardware                 keep AI accelerators as the motivating domain throughout
                                        security assurance.                                                        and use the open-source NVIDIA Deep Learning Accelerator
                                           Index Terms—Hardware Security Verification, LLMs, AI Ac-                (NVDLA) as a case-study platform, focusing on the CSB mas-
                                        celerators, Formal Verification, Threat Modeling, NVDLA                    ter module [39]. Figure 1 illustrates the end-to-end verification
                                                                                                                   pipeline that organizes both the survey and the case study.
                                                                I. I NTRODUCTION
                                           Hardware security verification remains a high-stakes re-                II. S URVEY OF AI/LLM-BASED S ECURITY V ERIFICATION
                                        quirement for modern digital systems, as vulnerabilities intro-
                                                                                                                      Recent research shows that AI/LLM-based techniques are
                                        duced before fabrication can remain undetected into deploy-
                                                                                                                   increasingly applied across the hardware security verification
                                        ment. The threat landscape covers hardware Trojans, power
                                                                                                                   workflow, from high-level threat reasoning to low-level asser-
                                        and timing side channels, unauthorized information flows,
                                                                                                                   tion generation and debugging. Open hardware platforms and
                                        and attacks against logic locking and obfuscation, while the
                                                                                                                   benchmark suites are also emerging to support evaluation of
                                        verification toolbox still depends on labor-intensive simulation,
                                                                                                                   these approaches [39], [76]–[81].
                                        assertion-based verification, model checking, and leakage as-
                                        sessment methodologies [1]–[16].                                           A. Asset Identification
                                           These challenges appear across a wide range of hardware
                                        platforms. For instance, AI accelerators embody valuable                      Asset identification is the starting point of security verifica-
                                        model parameters, sensitive activations, privileged control                tion [82] because it determines what must be protected before
                                        paths, and rich microarchitectural side effects, making them               threats, properties, and tests can be defined. Prior hardware-
                                        attractive targets for side-channel extraction, fault injection,           security research consistently places asset discovery at the
                                        neural Trojan insertion, and accelerator-specific intellectual             front of the verification process, especially for confidentiality,
                                        property (IP) theft [17]–[27]. As AI accelerators are integrated           integrity, and availability analysis, and shows that delayed
                                        into edge, datacenter, and safety-critical platforms, scalable             identification often shifts security fixes to the far more costly
                                        pre-silicon assurance becomes increasingly important.                      post-silicon stage [83]–[86]. Similar importance is reflected in
                                           Recent progress in AI and LLMs has also changed the                     broader cybersecurity and risk-analysis literature, where asset
                                        way hardware security verification can be organized and                    identification is treated as a prerequisite for systematic threat
                                        executed. Early surveys and position papers argue that LLMs                and vulnerability assessment [87], [88].
                                        can assist security reasoning across the verification stack, but              Despite its importance, hardware asset identification has
                                                                                                                   traditionally remained manual or dependent on predefined
                                         We thank the U.S. National Science Foundation (NSF) for support through   asset sets. Many prior works either assume assets are al-
                                        CAREER Award No. 2339971.                                                  ready known, begin from manually selected security-critical
                                        979-8-3315-6337-0/26/$31.00 ©2026 IEEE                                     structures, or derive secondary assets only after being seeded
                                                                                     Security Verification Pipeline

                                                                Threat                                                                                                                Evidence-backed
        RTL, specs,             Asset                                                             Test Plan                 Simulation &                     Counter-                 claims and mitiga-
 and security intent        Identification                     Modeling                          Generation                 Formal Verif.                    measures                 tions




                              Asset extraction,              Threat synthesis,               Threat-to-test translation,        Assertion and             Repair and patching,
                               refinement, and             CWE-aware reasoning,             coverage-guided generation,      property synthesis,     leakage analysis, red-teaming,
                       specification-guided reasoning      vulnerability analysis,          and context-aware planning      proof assistance, etc.      and mitigation co-design
                                   [40]–[42]                   and planning                  [35], [42], [47], [49], [50]      [41], [45], [46],            [31], [42], [44],
                                                                 [41]–[48]                                                     [48], [51]–[71]              [46], [72]–[75]



                                                                           Some LLM-based approaches discussed in this survey
                                                        Fig. 1. End-to-end AI/LLM-assisted security verification pipeline.
with a small set of primary assets [66], [89]–[92]. Standards-                                        direction to agentic threat modeling, test-plan generation, and
oriented efforts such as SA-EDI and IEEE P3164 provide                                                security property generation. Overall, these works show the
a principled vocabulary for conceptual and structural assets,                                         growing role of LLM-driven automation in scalable hardware
but still leave substantial manual effort to the engineer [82],                                       security verification, while challenges remain in accurate CWE
[93]. More recent methods move toward partial automation                                              mapping, large design reasoning, and reliable security analysis.
through threat-informed or specification-guided reasoning, yet
they remain sensitive to incomplete context and hand-crafted                                          C. Test Plan Generation
assumptions [41], [94]–[96].                                                                             Traditional security test planning converts assets, threat
   The challenge becomes even greater in sophisticated sys-                                           hypotheses, and security objectives into executable stimuli,
tems such as AI accelerators, where assets extend beyond                                              coverage targets, and measurement criteria. In established ver-
registers and control state to datasets, model parameters,                                            ification flows, the backbone remains SystemVerilog and the
intermediate activations, memory-resident data, and execution                                         Universal Verification Methodology (UVM), while Portable
pathways that may leak or be manipulated through physical                                             Stimulus enables reuse of test intent across simulation and
or logical attacks [97]–[100]. This growing complexity has                                            other execution platforms. Additional techniques such as
motivated LLM-assisted asset-identification frameworks, with                                          coverage-directed exploration, test vector leakage assessment
LAsset emerging as a representative effort to automate asset                                          (TVLA), and learned automatic test pattern generation (ATPG)
extraction and refinement across SoC and IP designs [40].                                             further extend these flows toward coverage closure, leakage
B. Threat Modeling                                                                                    evaluation, and activation of rare security conditions [11], [12],
   Threat modeling translates an asset inventory into adver-                                          [15], [103]–[105].
sarial scenarios that guide executable verification objectives.                                          AI/LLM-based planning approaches aim to bridge the gap
In hardware systems, this process is difficult because modern                                         between manual textual design intent and executable secu-
SoCs combine heterogeneous IPs, complex interconnects, and                                            rity tests. For example, ThreatLens and SV-LLM explicitly
multiple privilege boundaries, creating a large and difficult-to-                                     link threat reasoning to security test plan generation, while
analyze attack surface. To structure this reasoning, researchers                                      LLM4DV closes the loop by using coverage feedback to
often use vulnerability taxonomies such as the Common                                                 generate new stimuli for uncovered behaviors [42], [47],
Weakness Enumeration (CWE), which categorize weaknesses                                               [49]. ChipNeMo [35] and GPT4AIGChip [50] further suggest
that may lead to exploitable vulnerabilities [101]. Mapping                                           that domain-adapted or accelerator-aware LLM workflows can
assets or design components to CWE categories helps engi-                                             improve planning quality when test intent is inferred primar-
neers reason about likely attack vectors and their impact on                                          ily from architecture documents rather than mature security
confidentiality, integrity, and availability.                                                         specifications. Taken together, these works make test-plan
   Earlier efforts explored automated vulnerability detection                                         generation one of the most practical near-term uses of AI/LLM
using CWE knowledge bases. Ahmad et al. proposed a static-                                            methods because the outputs remain structured, reviewable,
analysis framework [102] that scans Verilog RTL to detect                                             and closely tied to the threat model.
potential CWE instances using rule-based scanners derived
from abstract syntax trees. However, such approaches de-                                              D. Simulation-Driven and Formal Verification
pend heavily on handcrafted rules and expert-defined patterns,                                           Simulation and formal verification remain at the core of
which limit scalability.                                                                              trustworthy security verification. Conventional practice relies
   Recent advances in LLMs have opened new opportunities                                              on SystemVerilog simulation infrastructure [13], assertion-
for automating hardware security analysis [41], [42], [45],                                           based verification [7], model checking [6], information-flow
[47]. For example, DIVAS [45] analyzes SoC specifications to                                          tracking [11], and coverage-guided exploration [104] to de-
identify vulnerabilities, map them to CWE entries, and gen-                                           termine whether suspected weaknesses can actually manifest
erate security assertions, while LASHED [41] combines static                                          in design. In AI/LLM-based verification, generated properties,
analysis with LLM reasoning for RTL vulnerability detection.                                          monitors, and hypotheses are useful only when they compile,
More broadly, ThreatLens [47] and SV-LLM [42] extend this                                             execute correctly, and meaningfully constrain the design.
   Recent work increasingly explores LLM-assisted assertion         3) RQ3. What benchmarks, evaluation criteria, and
generation. Early frameworks such as AutoSVA [63] and                  accelerator-specific abstractions are required to make
its later extension [62] automate formal property genera-              AI/LLM-based security verification practical and
tion from RTL and verification feedback. Methods such as               trustworthy at scale?
LISA [60] and STELLAR [57] improve assertion quality
through retrieval-augmented reasoning, structural grounding,                              IV. C ASE S TUDY OF NVDLA
and guided prompting, while AssertionLLM [61] highlights               To demonstrate the practical application of the research
the limitations of off-the-shelf models and proposes a fine-        questions, we present a case study on the open-source NVDLA
tuned alternative.                                                  accelerator, focusing on the NV_NVDLA_csb_master IP.
   Beyond assertion synthesis, AI/LLM methods are increas-          As the configuration ingress point for CSB requests before
ingly integrated into broader verification workflows. DI-           decoding and forwarding, this module provides a natural pre-
VAS [45], LASA [65], and LLM-IFT [67] move toward                   silicon boundary for access-control analysis, where unautho-
end-to-end security analysis by generating properties and           rized requests can be examined before downstream effects
structured information-flow reasoning from RTL, specifica-          occur. This case study does not claim that every NVDLA
tions, and design documents. Bug-detection and debugging            deployment is exploitable; rather, it evaluates whether the CSB
frameworks such as BugWhisperer [48], LASHED [41], and              master, viewed in isolation, lacks local privilege enforcement,
MEIC [70] further incorporate iterative tool-in-the-loop refine-    and therefore relies on trusted integration or upstream filtering.
ment to localize, explain, and repair RTL vulnerabilities.          The analysis is thus intentionally scoped to this IP boundary.
                                                                    The tables and artifacts reported here are condensed outputs
E. Countermeasures                                                  of an automated agentic workflow. All RTL line references
                                                                    correspond to the public nvdlav1 snapshot of the NVDLA
   Countermeasures form the defensive endpoint of the veri-
                                                                    CSB master1 .
fication pipeline, because discovered vulnerabilities must ul-
timately be prevented, detected, or tolerated in deployment.        A. Asset Identification
Classical hardware-security defenses include masking and               Given the CSB master boundary defined above, the next
hiding for side-channel resistance [106], fault detection and       step is to identify the assets that govern request acceptance
redundancy against active fault injection [107] and logic           and forwarding. For this case study, the most relevant assets
locking for IP protection [8].                                      are the CSB handshake, the request payload fields, the internal
   Recent research suggests that AI/LLMs can also support           address-decode logic, and the decoded DMA-facing interfaces.
mitigation generation by helping engineers identify RTL vul-        Together, these determine whether an unauthorized requester
nerabilities, reason about their root causes, and explore design-   can influence security-critical behavior. Table I summarizes
level repair options. Ahmad et al. show that prompted LLM           the assets considered in the threat analysis. Although the
ensembles can generate candidate fixes that outperform prior        exercised assets are primarily control and integrity-oriented,
automated hardware-repair baselines on a set of security            unauthorized control of DMA-facing paths can also create
bugs [44]. At a broader level, frameworks such as LLM-              confidentiality risk by enabling exposure or redirection of
Sec [108] illustrate how LLMs can assist with vulnerability         memory-resident model parameters, activations, or outputs.
analysis, policy reasoning, and remediation planning. Overall,      Additionally, the concentration of CWE-1220 mappings across
the emerging direction is a closed-loop hardware-security           the request and decode boundary motivates the threat framing
workflow in which AI not only helps expose weaknesses, but          summarized next in Table II.
                                                                                                TABLE I
also supports continuous security-aware design refinement.                  LLM- GENERATED SECURITY ASSETS FOR THE CSB MASTER

                 III. R ESEARCH Q UESTIONS                          Asset                               Obj.     Mapped CWEs
                                                                    CSB valid/ready                      A       CWE-1318, CWE-440, CWE-1429
   Recent benchmark efforts and open hardware platforms             handshake
have begun to establish an initial foundation for evaluating        CSB write data                           I   CWE-1262, CWE-1220, CWE-1318
AI/LLM-based security verification. At the same time, they ex-      CSB write control                        I   CWE-1262, CWE-1220, CWE-1318
                                                                    Internal address select                  I   CWE-1276, CWE-1262, CWE-1220
pose unresolved challenges in accelerator-aware abstractions,       logic
reliable ground truth, and rigorous artifact validation [76]–       CSB-to-CVIF interface                I, A    CWE-1262, CWE-1220, CWE-1318
[81]. Having viewed collectively, the survey literature points      Obj.: I = Integrity, A = Availability.
not only to emerging capabilities, but also to a set of broader     B. Threat Modeling
questions that remain open for the community.
                                                                      At this boundary, the central question is whether any
1) RQ1. How can AI/LLM-based methods automate the end-              requester reaching the CSB master can access decoded sub-
    to-end security verification workflow for hardware and AI       unit paths without a privilege context. This is a meaningful
    accelerators?                                                   module-level concern because core_req_prdy is perma-
2) RQ2. How can simulation, formal methods, and structured          nently asserted (line 468), while no local authorization check
    security knowledge ground AI/LLM-generated verification
    artifacts and reduce hallucination?                               1 https://github.com/nvdla/hw/tree/nvdlav1/vmod/nvdla/csb_master
is applied to source privilege information at this boundary.                  these tasks drive requests through an async FIFO modeling
Table II summarizes this condition in terms of the request                    the Falcon–core clock-domain crossing, while monitors track
format, threat agent, attack vector, STRIDE mapping, and                      ingress acceptance and decoded forwarding.
scope. This threat framing directly determines the directed
                                                                              D. Simulation Driven Verification
tests summarized in Table III.
                            TABLE II                                             The test plan is then evaluated through simulation. The
           LLM- GENERATED THREAT MODEL FOR CWE-1220.                          exploit-oriented bench drives the planned transactions at the
                                                                              CSB ingress and records handshake activity and decoded
Field          Detail
CWE ID         CWE-1220: Insufficient Granularity of Access Control           forwarding using a driver, request monitor, sub-unit monitor,
Root Cause     core_req_prdy = 1’b1; no privilege check in decode             and scoreboard. Of the 31 exercised transactions, 30 were
               logic                                                          observed at decoded sub-unit ports and flagged as security
Format         50-bit packet: {nposted, write, addr[15:0], wdata[31:0]}; no   violations (29 writes and 1 read). The remaining transaction
               security field
Threat         Untrusted requester can issue accepted CSB read/write re-      targeted the unmapped address (0x7C00); it was accepted
               quests                                                         at ingress, but routed to an internal dummy client that is
Scenario       Discover address map, issue unprivileged writes, observe       not externally monitored. Across all valid requests, the ready
               forwarding
                                                                              signal never deasserted, indicating zero back-pressure in the
STRIDE         Tampering, Information Disclosure, Elevation of Privilege
Scope          Module boundary only; downstream effects not claimed           exercised cases. These results support a module-scoped con-
                                                                              clusion: at this boundary, the CSB master accepts and forwards
C. Test Plan Generation                                                       the tested requests without a local privilege check; whether this
   The threat model leads to a small set of directed tests                    becomes a system-level vulnerability or not depends on SoC
centered on a single question: does the CSB master accept                     integration and reachability of the CSB path.
and forward the exercised requests? Table III summarizes                      E. Countermeasures
the executed plan, focusing on DMA-facing targets and the
broader decoded address space. All addresses follow the CSB                      This behavior points to mitigation at the request-admission
master’s word-address convention, and each test maps directly                 boundary. Because the issue arises before decoded forwarding
to a SystemVerilog testbench task.                                            begins, the most direct response is to constrain request admis-
                           TABLE III                                          sion in the CSB master rather than retrofit each downstream
             LLM- GENERATED TEST PLAN FOR CWE-1220.                           target independently. Table IV summarizes the relevant control
#    Target / Op     Check                                                    point and corresponding design options.
1    MCIF write      Forwarding of 0x0800, 0xDEAD_BEEF to                                               TABLE IV
                     MCIF                                                           RTL CONTROL POINT AND SUGGESTED COUNTERMEASURES
2    BDMA/CVIF/CDMA Forwarding to decoded DMA-facing targets
                                                                               Item               Detail
     write           without privilege check
                                                                               Control Point      core_req_prdy is permanently high (line 468),
3    MCIF read       Request accepted at the same boundary
                                                                                                  so all requests are accepted and may be forwarded
4    Full scan (18)  Acceptance across 17 mapped targets + 1 un-                                  downstream.
                     mapped
                                                                               Recommendations
5    Rapid-fire (×8) No throttling or back-pressure on MCIF writes
                                                                               R1                 Enforce interconnect-level access control before
                                                                                                  this module.
// Test 1: Unprivileged MCIF write                                             R2                 Add privilege or source-ID metadata for local au-
task automatic test1_unpriv_write_mcif();                                                         thorization.
  u_drv.drive_txn(                                                             R3                 Gate core_req_prdy on an authorization check.
    .addr(ADDR_MCIF),           // 16’h0800
    .wdata(32’hDEAD_BEEF),
    .write(1’b1), .nposted(1’b1),                                                These recommendations matter when the CSB path may be
    .description("UNPRIV WRITE forwarded to MCIF"));                          reachable by untrusted requesters in a larger SoC integration.
endtask
                                                                                                     V. C ONCLUSION
// Test 4: Full 18-target address scan
task automatic test4_full_address_scan();                                        In this paper, we’ve surveyed AI/LLM-based methods for
  localparam logic [15:0] test_addrs [18] =                                   hardware security verification, with AI accelerators as the
    ’{ADDR_GLB, ADDR_GEC, ADDR_MCIF, ADDR_CVIF,
    ADDR_BDMA, ADDR_CDMA, ADDR_CSC, ADDR_CMAC_A,
                                                                              motivating domain. Although the literature increasingly spans
    ADDR_CMAC_B, ADDR_CACC, ADDR_SDP_RDMA, ADDR_SDP,                          the workflow from asset identification and threat modeling
     ADDR_PDP_RDMA, ADDR_PDP, ADDR_CDP_RDMA,                                  to test generation, verification artifacts, and countermeasure
    ADDR_CDP, ADDR_RBK, ADDR_UNMAPPED};
  for (int i = 0; i < 18; i++)
                                                                              support, practical adoption still depends on grounding through
    u_drv.drive_txn(.addr(test_addrs[i]), ...);                               executable evidence, formal methods, benchmark quality, and
endtask                                                                       accelerator-aware evaluation. The NVDLA case study demon-
Artifact 1. Representative LLM-generated stimuli corresponding to the LLM-    strates that an automated agentic workflow can support a
generated plan.                                                               scoped, simulation-grounded RTL security analysis and pro-
Artifact 1 shows representative task code for the direct MCIF                 duce localized mitigation guidance.
write and the broader address scan. In the executed bench,
                            R EFERENCES                                        [26] H. Xu, D. Liu, C. Merkel, and M. Zuzak, “Exploiting logic
                                                                                    locking for a neural trojan attack on machine learning accelerators,”
 [1] M. Tehranipoor and F. Koushanfar, “A survey of hardware trojan                 in Proceedings of the Great Lakes Symposium on VLSI 2023,
     taxonomy and detection,” IEEE Design & Test of Computers, vol. 27,             ser. GLSVLSI ’23. New York, NY, USA: Association for
     no. 1, pp. 10–25, 2010.                                                        Computing Machinery, 2023, p. 351–356. [Online]. Available:
 [2] S. Bhunia, M. S. Hsiao, M. Banga, and S. Narasimhan, “Hardware                 https://doi.org/10.1145/3583781.3590242
     trojan attacks: Threat analysis and countermeasures,” Proceedings of      [27] Y. Li, G. Zhao, Y. He, and H. Zhou, “Evaluating the security of logic
     the IEEE, vol. 102, no. 8, pp. 1229–1247, 2014.                                locking on deep neural networks,” in DAC, 2024.
 [3] P. Kocher, J. Jaffe, and B. Jun, “Differential power analysis,” in        [28] D. Saha, S. Tarek, K. Yahyaei, S. K. Saha, J. Zhou, M. Tehranipoor,
     CRYPTO ’99, ser. LNCS, vol. 1666. Springer, 1999, pp. 388–397.                 and F. Farahmandi, “LLM for SoC security: A paradigm shift,”
 [4] S. Mangard, E. Oswald, and T. Popp, Power analysis attacks: Revealing          arXiv:2310.06046, 2023.
     the secrets of smart cards. Springer, 2007.                               [29] M. Akyash and H. M. Kamali, “Evolutionary large language models
 [5] W. Hua, Z. Zhang, and G. E. Suh, “Reverse engineering convolutional            for hardware security: A comparative survey,” in GLSVLSI, 2024.
     neural networks through side-channel information leaks,” in DAC.          [30] M. Abdollahi, S. F. Yeganli, M. Baharloo, and A. Baniasadi, “Hardware
     ACM, 2018.                                                                     design and verification with large language models: A scoping review,
 [6] W. Hu, J. Oberg, A. Irturk, M. Tiwari, T. Sherwood, D. Mu, and                 challenges, and open issues,” Electronics, vol. 14, no. 1, p. 120, 2024.
     R. Kastner, “Theoretical fundamentals of gate level information flow      [31] Z. Wang, L. Alrahis, L. Mankali, J. Knechtel, and O. Sinanoglu, “Llms
     tracking,” IEEE Transactions on Computer-Aided Design of Integrated            and the future of chip design: Unveiling security risks and building
     Circuits and Systems, vol. 30, no. 8, pp. 1128–1140, 2011.                     trust,” in 2024 IEEE Computer Society Annual Symposium on VLSI
 [7] M. Tiwari, H. M. G. Wassel, B. Mazloom, S. Mysore, F. T. Chong,                (ISVLSI). IEEE, 2024, pp. 385–390.
     and T. Sherwood, “Complete information flow tracking from the gates       [32] S. Thakur, B. Ahmad, H. Pearce, B. Tan, B. Dolan-Gavitt, R. Karri,
     up,” in ASPLOS, 2009, pp. 109–120.                                             and S. Garg, “VeriGen: A large language model for Verilog code
 [8] J. Rajendran, Y. Pino, O. Sinanoglu, and R. Karri, “Logic encryption:          generation,” ACM TODAES, vol. 29, no. 3, 2024.
     A fault analysis perspective,” in 2012 Design, Automation & Test in       [33] Y. Lu, S. Liu, Q. Zhang, and Z. Xie, “Rtllm: An open-source bench-
     Europe Conference & Exhibition (DATE). IEEE, 2012, pp. 953–958.                mark for design rtl generation with large language model,” in 2024 29th
 [9] P. Subramanyan, S. Ray, and S. Malik, “Evaluating the security of logic        Asia and South Pacific Design Automation Conference (ASP-DAC).
     encryption algorithms,” in IEEE HOST, 2015, pp. 137–143.                       IEEE, 2024, pp. 722–727.
[10] M. L. Bushnell and V. D. Agrawal, Essentials of electronic testing for    [34] S. Liu, W. Fang, Y. Lu, Q. Zhang, H. Zhang, and Z. Xie, “Rtlcoder:
     digital, memory and mixed-signal VLSI circuits. Springer, 2002.                Outperforming gpt-3.5 in design rtl generation with our open-source
[11] IEEE Std 1800-2017: SystemVerilog Unified Hardware Design, Speci-              dataset and lightweight solution,” in 2024 IEEE LLM Aided Design
     fication, and Verification Language, IEEE Std., 2017.                          Workshop (LAD). IEEE, 2024, pp. 1–5.
[12] “IEEE 1800.2 for UVM approved as an IEEE standard,” Accellera,            [35] M. Liu, T.-D. Ene, R. Kirby, C. Cheng et al., “ChipNeMo: Domain-
     2017.                                                                          adapted LLMs for chip design,” arXiv:2311.00176, 2023.
[13] E. M. Clarke, O. Grumberg, and D. A. Peled, Model Checking. MIT           [36] R. Qiu, G. L. Zhang, R. Drechsler, U. Schlichtmann, and B. Li,
     Press, 1999.                                                                   “Correctbench: Automatic testbench generation with functional self-
[14] S. Vijayaraghavan and M. Ramanathan, A Practical Guide for Sys-                correction using llms for hdl design,” in 2025 Design, Automation &
     temVerilog Assertions. Springer, 2005.                                         Test in Europe Conference (DATE), 2025, pp. 1–7.
[15] G. Goodwill, B. Jun, J. Jaffe, and P. Rohatgi, “A testing methodology     [37] H. Zhang, Z. Yu, C.-T. Ho, H. Ren, B. Khailany, and J. Zhao,
     for side-channel resistance validation,” NIST, Tech. Rep., 2011.               “Llm4cov: Execution-aware agentic learning for high-coverage test-
[16] T. Schneider and A. Moradi, “Leakage assessment methodology,” in               bench generation,” arXiv preprint arXiv:2602.16953, 2026.
     CHES 2015, ser. LNCS, vol. 9293, 2015, pp. 495–513.                       [38] Y. Yang, F. Teng, P. Liu, M. Qi, C. Lv, J. Li, X. Zhang, and
[17] S. Mittal, H. Gupta, and S. Srivastava, “A survey on hardware security         Z. He, “Haven: Hallucination-mitigated llm for verilog code generation
     of DNN models and accelerators,” Journal of Systems Architecture, vol.         aligned with hdl engineers,” in 2025 Design, Automation & Test in
     117, p. 102111, 2021.                                                          Europe Conference (DATE), 2025, pp. 1–7.
[18] K. Lee, A. N. Ashok, S. Maji, A. Agrawal, A. Joshi, M. Yan, J. S. Emer,   [39] “NVIDIA deep learning accelerator (NVDLA),” https://nvdla.org/,
     and A. P. Chandrakasan, “Secure machine learning hardware: Chal-               2026, accessed: 2026-03-04.
     lenges and progress,” IEEE Circuits and Systems Magazine, vol. 25,        [40] M. A. Hasan, D. Saha, K. T. Hasan, N. Alam, A. Uddin, S. K. Saha,
     no. 1, 2025.                                                                   M. Tehranipoor, and F. Farahmandi, “Lasset: An llm-assisted security
[19] L. Batina, S. Bhasin, D. Jap, and S. Picek, “CSI NN: Reverse                   asset identification framework for system-on-chip (soc) verification,”
     engineering of neural network architectures through electromagnetic            2026. [Online]. Available: https://arxiv.org/abs/2601.02624
     side channel,” in USENIX Security, 2019, pp. 515–532.                     [41] B. Ahmad, H. Pearce, R. Karri, and B. Tan, “Lashed: Llms and
[20] X. Yan, X. Lou, G. Xu, H. Qiu, S. Guo, C. H. Chang, and T. Zhang,              static hardware analysis for early detection of rtl bugs,” arXiv preprint
     “MERCURY: An automated remote side-channel attack to Nvidia deep               arXiv:2504.21770, 2025.
     learning accelerator,” in IEEE FPT, 2023.                                 [42] D. Saha, S. Tarek, H. A. Shaikh, K. T. Hasan, P. S. Nalluri, M. A.
[21] P. Horvath, L. Chmielewski, L. Weissbart, L. Batina, and Y. Yarom,             Hasan, N. Alam, J. Zhou, S. K. Saha, M. Tehranipoor et al., “Sv-llm:
     “Barracuda: Edge gpus do leak dnn weights,” in Proceedings of the              An agentic approach for soc security verification using large language
     34th USENIX Security Symposium (USENIX Security ’25). Seattle,                 models,” arXiv preprint arXiv:2506.20415, 2025.
     WA, USA: USENIX Association, Aug. 2025. [Online]. Available: https:       [43] J. Blocklove et al., “Chip-chat: Challenges and opportunities in con-
     //www.usenix.org/conference/usenixsecurity25/presentation/horvath              versational hardware design,” arXiv preprint arXiv:2305.13243, 2023.
[22] Z. Wang, Y. Wu, Y. Park, S. Yoo, X. Wang, J. K. Eshraghian,               [44] B. Ahmad, S. Thakur, B. Tan, R. Karri, and H. Pearce, “On hardware
     and W. D. Lu, “Powergan: a machine learning approach for power                 security bug code fixes by prompting large language models,” IEEE
     side-channel attack on compute-in-memory accelerators,” Advanced               Transactions on Information Forensics and Security, vol. 19, pp. 4043–
     Intelligent Systems, vol. 5, no. 12, p. 2300313, 2023.                         4057, 2024.
[23] N. Gupta, A. Jati, and A. Chattopadhyay, “Ai attacks ai: Recovering       [45] S. Paria, A. Dasgupta, and S. Bhunia, “Divas: An llm-based end-to-
     neural network architecture from nvdla using ai-assisted side channel          end framework for soc security analysis and policy-based protection,”
     attack,” ACM Transactions on Embedded Computing Systems, vol. 24,              arXiv preprint arXiv:2308.06932, 2023.
     no. 5, pp. 1–29, 2025.                                                    [46] S. Tarek, D. Saha, S. K. Saha, M. Tehranipoor, and F. Farahmandi,
[24] A. S. Rakin, Z. He, and D. Fan, “Bit-flip attack: Crushing neural              “Socurellm: An llm-driven approach for large-scale system-on-chip
     network with progressive bit search,” in ICCV, 2019, pp. 1211–1220.            security verification and policy generation,” in 2025 IEEE International
[25] J. Ordoñez and C. Yang, “Derailed: Arbitrarily controlling dnn outputs         Symposium on Hardware Oriented Security and Trust (HOST), 2025,
     with targeted fault injection attacks,” in 2024 Design, Automation &           pp. 335–345.
     Test in Europe Conference & Exhibition (DATE). IEEE, 2024, pp.            [47] D. Saha, H. Al Shaikh, S. Tarek, and F. Farahmandi, “Special session:
     1–6.                                                                           Threatlens: Llm-guided threat modeling and test plan generation for
                                                                                    hardware security verification,” in 2025 IEEE 43rd VLSI Test Sympo-
                                                                                    sium (VTS), 2025, pp. 1–5.
[48] S. Tarek, D. Saha, S. K. Saha, and F. Farahmandi, “Bugwhisperer:                 ging,” in 2023 Asian hardware oriented security and trust symposium
     Fine-tuning llms for soc hardware vulnerability detection,” in 2025              (AsianHOST). IEEE, 2023, pp. 1–6.
     IEEE 43rd VLSI Test Symposium (VTS), 2025, pp. 1–5.                         [69] M. Akyash and H. M. Kamali, “ Self-HWDebug: Automation
[49] Z. Zhang, B. Szekely, P. Gimenes, G. Chadwick, H. McNally, J. Cheng,             of LLM Self-Instructing for Hardware Security Verification ,” in
     R. Mullins, and Y. Zhao, “LLM4DV: Using large language models for                2024 IEEE Computer Society Annual Symposium on VLSI (ISVLSI).
     hardware test stimuli generation,” arXiv:2310.04535, 2023.                       Los Alamitos, CA, USA: IEEE Computer Society, Jul. 2024, pp.
[50] Y. Fu, Y. Zhang, Z. Yu, S. Li, Z. Ye, C. Li, C. Wan, and Y. C.                   391–396. [Online]. Available: https://doi.ieeecomputersociety.org/10.
     Lin, “Gpt4aigchip: Towards next-generation ai accelerator design au-             1109/ISVLSI61997.2024.00077
     tomation via large language models,” in 2023 IEEE/ACM International         [70] K. Xu, J. Sun, Y. Hu, X. Fang, W. Shan, X. Wang, and Z. Jiang,
     Conference on Computer Aided Design (ICCAD), 2023, pp. 1–9.                      “MEIC: Re-thinking RTL debug automation using LLMs,” in ICCAD,
[51] W. Fang, M. Li, M. Li, Z. Yan, S. Liu, Z. Xie, and H. Zhang,                     2024.
     “Assertllm: Generating and evaluating hardware verification asser-          [71] M. Rostami, M. Chilese, S. Zeitouni, R. Kande, J. Rajendran, and
     tions from design specifications via multi-llms,” arXiv preprint                 A.-R. Sadeghi, “Beyond random inputs: A novel ML-based hardware
     arXiv:2402.00386, 2024.                                                          fuzzing,” arXiv:2404.06856, 2024.
[52] R. Kande, H. Pearce, B. Tan, B. Dolan-Gavitt, S. Thakur, R. Karri, and      [72] H. Pearce, B. Tan, B. Ahmad, R. Karri, and B. Dolan-Gavitt, “Ex-
     J. Rajendran, “(security) assertions by large language models,” IEEE             amining zero-shot vulnerability repair with large language models,” in
     Transactions on Information Forensics and Security, vol. 19, pp. 4374–           2023 IEEE symposium on security and privacy (SP). IEEE, 2023, pp.
     4389, 2024.                                                                      2339–2356.
[53] K. Maddala, B. Mali, and C. Karfa, “Laag-rv: Llm assisted assertion         [73] M. Nair, R. Sadhukhan, H. Pearce, D. Mukhopadhyay, and R. Karri,
     generation for rtl design verification,” in 2024 IEEE 8th International          “Netlist whisperer: Ai and nlp fight circuit leakage!” in Proceedings
     Test Conference India (ITC India). IEEE, 2024, pp. 1–6.                          of the 2023 Workshop on Attacks and Solutions in Hardware Security,
[54] Y. Bai, G. B. Hamad, S. Suhaib, and H. Ren, “Assertionforge:                     2023, pp. 83–92.
     Enhancing formal verification assertion generation with structured          [74] M. O. Faruque, P. Jamieson, A. Patooghy, and A.-H. A. Badawy, “Un-
     representation of specifications and rtl,” in 2025 IEEE International            leashing ghost: An llm-powered framework for automated hardware
     Conference on LLM-Aided Design (ICLAD). IEEE, 2025, pp. 85–92.                   trojan design,” Electronics, vol. 14, no. 23, p. 4745, 2025.
[55] H. Lyu, Y. Wang, Y. Du, M. Shi, Z. Chao, W. Li, T. Wang, and H. Li,         [75] G. Kokolakis, A. Moschos, and A. D. Keromytis, “Harnessing the
     “Assertgen: Enhancement of llm-aided assertion generation through                power of general-purpose llms in hardware trojan design,” in Inter-
     cross-layer signal bridging,” in Proceedings of the 34th IEEE Asian              national conference on applied cryptography and network security.
     Test Symposium and the 9th IEEE International Test Conference                    Springer, 2024, pp. 176–194.
     in Asia (ATS/ITC-Asia). Tokyo, Japan: IEEE, Dec. 2025. [Online].            [76] “NVDLA open source hardware,” GitHub: https://github.com/nvdla/
     Available: https://www.ieee-ats.org/                                             hw, 2018.
[56] F. Wu, E. Pan, R. Kande, M. Quinn, A. Tyagi, D. K. Houngninou,              [77] “Gemmini: Berkeley spatial array generator,” GitHub: https://github.
     J. Rajendran, and J. Hu, “Spec2assertion: Automatic pre-rtl assertion            com/ucb-bar/gemmini, 2025.
     generation using large language models with progressive regulariza-         [78] “OpenTitan: Open source silicon root of trust,” https://opentitan.org/,
     tion,” arXiv preprint arXiv:2505.07995, 2025.                                    2024.
[57] S. Rajabi, C. Yang, and S. Patnaik, “Stellar: Structure-guided llm as-      [79] Q. Chen, J. Shuai, S. Chen, S. Ye, Z. Wen, X. Su, J. Jin, J. Li, J. Chen,
     sertion retrieval and generation for formal verification,” arXiv preprint        X. Tan et al., “Hardsecbench: Benchmarking the security awareness of
     arXiv:2601.19903, 2025.                                                          llms for hardware code generation,” arXiv preprint arXiv:2601.13864,
[58] Y. Wang, J. Zhou, H. Lyu, Z. Chao, T. Wang, and H. Li, “Deepassert:              2026.
     An llm-aided verification framework with fine-grained assertion gener-      [80] W. Fu, S. Li, Y. Jin, and X. Guo, “HWFixBench: Benchmarking tools
     ation for modules with extracted module specifications,” arXiv preprint          for hardware understanding and fault repair,” in GLSVLSI, 2025.
     arXiv:2509.14668, 2025.                                                     [81] S. Li, W. Fu, Y. Zhao, X. Guo, and Y. Jin, “Fixbench-rtl: A com-
[59] H. Lyu, Y. Wang, J. Zhou, Z. Chao, T. Wang, and H. Li, “Assertminer:             prehensive benchmark for evaluating llms on rtl debugging,” in 2025
     Module-level spec generation and assertion mining using static analysis          Asian Hardware Oriented Security and Trust Symposium (AsianHOST).
     guided llms,” in Proceedings of the Asia and South Pacific Design                IEEE, 2025, pp. 1–6.
     Automation Conference (ASP-DAC). Hong Kong: IEEE, Jan. 2026.                [82] Accellera Systems Initiative, “Security Annotation for Electronic
[60] S. Paul, A. Banerjee, S. Ghosh, and S. Surendran, “LISA: LLM                     Design Integration Standard,” https://www.accellera.org/images/
     informed SystemVerilog assertion generation with RAG and chain-of-               downloads/standards/Accellera_SA-EDI_Standard_v10.pdf, apr. 2021.
     thought,” in ISVLSI, 2025.                                                       [Online]. Accessed: 2024-02-04.
[61] V. Pulavarthi, D. Nandal, S. Dan, and D. Pal, “Are llms ready for prac-     [83] J. Portillo, E. John, and S. Narasimhan, “Building trust in 3pip using
     tical adoption for assertion generation?” in 2025 Design, Automation             asset-based security property verification,” in 2016 IEEE 34th VLSI
     & Test in Europe Conference (DATE). IEEE, 2025, pp. 1–7.                         Test Symposium (VTS), 2016, pp. 1–6.
[62] M. Orenes-Vera, M. Martonosi, and D. Wentzlaff, “Using LLMs to              [84] S. Ray, E. Peeters, M. M. Tehranipoor, and S. Bhunia, “System-on-chip
     facilitate formal verification of RTL,” arXiv:2309.09437, 2023.                  platform security assurance: Architecture and validation,” Proceedings
[63] M. Orenes-Vera, A. Manocha, D. Wentzlaff, and M. Martonosi, “Au-                 of the IEEE, vol. 106, no. 1, pp. 21–37, 2018.
     tosva: Democratizing formal verification of rtl module interactions,” in    [85] W. Chen, S. Ray, J. Bhadra, M. Abadir, and L.-C. Wang, “Challenges
     2021 58th ACM/IEEE Design Automation Conference (DAC). IEEE,                     and trends in modern soc design verification,” IEEE Design & Test,
     2021, pp. 535–540.                                                               vol. 34, no. 5, pp. 7–22, 2017.
[64] K. Qayyum, M. Hassan, S. Ahmadi-Pour, C. K. Jha, and R. Drech-              [86] S. Mitra, S. A. Seshia, and N. Nicolici, “Post-silicon validation
     sler, “Late breaking results: Llm-assisted automated incremental proof           opportunities, challenges and recent advances,” in Proceedings of the
     generation for hardware verification,” in Proceedings of the 61st                47th Design Automation Conference, 2010, pp. 12–17.
     ACM/IEEE Design Automation Conference, 2024, pp. 1–2.                       [87] E. Yunizal, J. Santoso, and K. Surendro, “Asset identification in
[65] D. R. Ankireddy, S. Paria, A. Dasgupta, S. Ray, and S. Bhunia,                   information security risk assessment using process mining,” Int. J. Adv.
     “Lasa: Enhancing soc security verification with llm-aided property               Sci. Eng. Inf. Technol., vol. 12, no. 4, pp. 1441–1448, Jul. 2022.
     generation,” arXiv preprint arXiv:2506.17865, 2025.                         [88] F. Farzan, M. Jafari, D. Wei, and Y. Lu, “Cyber-related risk assessment
[66] A. Ayalasomayajula, R. Guo, J. Zhou, S. K. Saha, and F. Farahmandi,              and critical asset identification in power grids,” in ISGT 2014, 2014,
     “Lasp: Llm assisted security property generation for soc verification,”          pp. 1–5.
     in Proceedings of the 2024 ACM/IEEE International Symposium on              [89] A. Meza and R. Kastner, “Information flow coverage metrics
     Machine Learning for CAD, 2024, pp. 1–7.                                         for hardware security verification,” 2023. [Online]. Available:
[67] N. Mashnoor, M. Akyash, H. Kamali, and K. Azar, “Llm-ift: Llm-                   https://arxiv.org/abs/2304.08263
     powered information flow tracking for secure hardware,” in 2025 IEEE        [90] G. K. Contreras, A. Nahiyan, S. Bhunia, D. Forte, and M. Tehranipoor,
     43rd VLSI Test Symposium (VTS), 2025, pp. 1–5.                                   “Security vulnerability analysis of design-for-test exploits for asset
[68] W. Fu, K. Yang, R. G. Dutta, X. Guo, and G. Qu, “Llm4sechw:                      protection in socs,” in 2017 22nd Asia and South Pacific Design
     Leveraging domain-specific large language model for hardware debug-              Automation Conference (ASP-DAC), 2017, pp. 617–622.
[91] N. Farzana, A. Ayalasomayajula, F. Rahman, F. Farahmandi, and                [100] D. Gnad, M. Gotthard, J. Krautter, A. Kritikakou, V. Meyers, P. Rech,
     M. Tehranipoor, “Saif: Automated asset identification for security                 J. E. Rodriguez Condia, A. Ruospo, E. Sanchez, F. F. Dos Santos,
     verification at the register transfer level,” in 2021 IEEE 39th VLSI               O. Sentieys, M. Tahoori, R. Tessier, and M. Traiola, “Reliability and
     Test Symposium (VTS), 2021, pp. 1–7.                                               security of ai hardware,” in 2024 IEEE European Test Symposium
[92] A. Nahiyan, M. Sadi, R. Vittal, G. Contreras, D. Forte, and M. Tehra-              (ETS), 2024, pp. 1–10.
     nipoor, “Hardware trojan detection through information flow security         [101] T. M. Corporation, “Common weakness enumeration,” 2025. [Online].
     verification,” in 2017 IEEE International Test Conference (ITC), 2017,             Available: https://cwe.mitre.org/
     pp. 1–10.                                                                    [102] B. Ahmad et al., “Don’t cweat it: Toward cwe analysis techniques
[93] IEEE P3164 Working Group, “Asset Identification for Electronic De-                 in early stages of hardware design,” in Proceedings of the 41st
     sign IP,” https://ieeexplore.ieee.org/document/10496567, pp. 1–26, apr.            IEEE/ACM International Conference on Computer-Aided Design.
     2024. [Online]. Accessed: 2024-02-04.                                              ACM, Oct. 2022, p. 1–9. [Online]. Available: http://dx.doi.org/10.
[94] W.-K. Liu, B. Tan, and K. Chakrabarty, “Identifying system-on-chip                 1145/3508352.3549369
     security assets with structure-based analysis,” in 2025 62nd ACM/IEEE        [103] “Portable test and stimulus standard 3.0,” Accellera, 2024.
     Design Automation Conference (DAC), 2025, pp. 1–7.                           [104] K. Laeufer, J. Koenig, D. Kim, J. Bachrach, and K. Sen, “RFUZZ:
[95] A. Ayalasomayajula, N. Farzana Dipu, M. M. Tehranipoor, and                        Coverage-directed fuzz testing of RTL on FPGAs,” in ICCAD, 2018.
     F. Farahmandi, “Automatic asset identification for assertion-based soc       [105] L. Zhang and A. Davoodi, “Efficient and effective neural networks
     security verification,” IEEE Transactions on Computer-Aided Design                 for automatic test pattern generation,” in Proceedings of the 2024
     of Integrated Circuits and Systems, vol. 43, no. 10, pp. 3264–3277,                ACM/IEEE International Symposium on Machine Learning for CAD,
     2024.                                                                              2024, pp. 1–7.
[96] S. K. Deb Nath and B. Tan, “Toward automated potential primary               [106] Y. Ishai, A. Sahai, and D. Wagner, “Private circuits: Securing hardware
     asset identification in verilog designs,” in 2025 26th International               against probing attacks,” in CRYPTO 2003, ser. LNCS, vol. 2729.
     Symposium on Quality Electronic Design (ISQED), 2025, pp. 1–7.                     Springer, 2003, pp. 463–481.
[97] R. Mukherjee, S. Swaroopa, and R. S. Chakraborty, “Security vulner-          [107] A. Barenghi, L. Breveglieri, I. Koren, and D. Naccache, “Fault injection
     abilities in ai hardware: Threats and countermeasures,” in 2024 IEEE               attacks on cryptographic devices: Theory, practice, and countermea-
     33rd Asian Test Symposium (ATS), 2024, pp. 1–6.                                    sures,” Proceedings of the IEEE, vol. 100, no. 11, pp. 3056–3076,
[98] S. Kundu, S. Das, A. Menon, S. Bhattacharya, A. Raha, and K. Basu,                 2012.
     “The fault in our chips: A survey on edge ai accelerator vulnerabilities,”   [108] J. Talukdar, S. Banerjee, and F. Firouzi, “ LLM-Sec: Closing the
     IEEE Design & Test, pp. 1–1, 2025.                                                 Security Loop using LLMs for Hardware Design ,” in 2025 IEEE
[99] K. I. Gubbi, I. Kaur, A. Hashem, S. M. P D, H. Homayoun, A. Sasan,                 International Conference on Omni-layer Intelligent Systems (COINS).
     and S. Salehi, “Securing ai hardware: Challenges in detecting and                  Los Alamitos, CA, USA: IEEE Computer Society, Aug. 2025, pp.
     mitigating hardware trojans in ml accelerators,” in 2023 IEEE 66th                 1–6. [Online]. Available: https://doi.ieeecomputersociety.org/10.1109/
     International Midwest Symposium on Circuits and Systems (MWSCAS),                  COINS65080.2025.11125787
     2023, pp. 821–825.
