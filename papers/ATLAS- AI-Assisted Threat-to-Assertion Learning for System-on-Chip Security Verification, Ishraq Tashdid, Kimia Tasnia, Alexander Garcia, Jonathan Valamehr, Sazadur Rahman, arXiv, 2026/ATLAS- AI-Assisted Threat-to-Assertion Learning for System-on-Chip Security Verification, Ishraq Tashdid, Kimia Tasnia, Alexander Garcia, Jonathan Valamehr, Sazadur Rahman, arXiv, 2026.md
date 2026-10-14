                                                          ATLAS: AI-Assisted Threat-to-Assertion Learning for
                                                                System-on-Chip Security Verification
                                                                          Ishraq Tashdid1∗ , Kimia Tasnia1∗ , Alexander Garcia1 , Jonathan Valamehr2 , and Sazadur Rahman1
                                                                        1 Department of Electrical and Computer Engineering, University of Central Florida; 2 Intel Corporation

                                                                 1 {ishraq.tashdid, kimia.tasnia, alexander.garcia, mohammad.rahman}@ucf.edu, 2 jonathan.k.valamehr@intel.com

                                                                                                                                                 (a)                                   (b)
                                         Abstract
                                         This work presents ATLAS, an LLM-driven framework that bridges
                                         standardized threat modeling and property-based formal verifi-
                                         cation for System-on-Chip (SoC) security. Starting from vulnera-
                                         bility knowledge bases such as Common Weakness Enumeration
arXiv:2603.01170v2 [cs.CR] 23 Apr 2026




                                         (CWE), the framework identifies SoC-specific assets, maps relevant
                                         weaknesses, and generates assertion-based security properties and
                                         JasperGold scripts for verification. By combining asset-centric anal-
                                         ysis with standardized threat model templates, it automates the
                                         transformation from vulnerability reasoning to formal proof. Eval-                      Figure 1: (a) Increasing hardware security vulnerabilities in RISC-V
                                         uated on three HACK@DAC benchmarks, ATLAS detected 39/48                                based SoCs. (b) Trend in CWE [47] and CVE [11] over the years.
                                         CWEs and, out of that 39, ATLAS was able to generate correct prop-                      CAPEC [7], catalogs over 200,000 hardware and software flaws, yet
                                         erties for 33 of the bugs, advancing automated, knowledge-driven                        current methods do not systematically use this knowledge for SoC
                                         SoC security verification toward a secure-by-design paradigm.                           security. Although recent efforts have leveraged these databases
                                         Keywords                                                                                for threat modeling [15, 45], they still lack the comprehensiveness
                                         Security verification, Threat Modeling, LLM for Security.                               required for SoC security verification. Likewise, existing security
                                                                                                                                 verification techniques, including formal verification [16, 18, 48],
                                         1     Introduction                                                                      code analysis [2, 31], hardware fuzzing [6, 17, 22, 56], and penetra-
                                         Integrated circuits (ICs) form the backbone of modern technolo-                         tion testing [4, 45, 46], remain fragmented, manual, and hard to scale.
                                         gies spanning artificial intelligence (AI), healthcare, autonomous                      In particular, they rely on handcrafted security constraints that are
                                         systems, and defense, powering secure communication, precision-                         labor-intensive, error-prone, and require deep expertise [30]. Re-
                                         guided platforms, and advanced computing [20]. Modern ICs have                          cent LLM-assisted property generation methods are also ad hoc,
                                         evolved into highly integrated and interconnected Systems-on-Chip                       covering only a small subset of vulnerabilities and lacking gener-
                                         (SoCs) composed of diverse pre-designed intellectual property (IP)                      alization across the full CWE space [4, 5, 46, 52]. With reported
                                         blocks. Due to the complexity, horizontally distributed business                        security issues increasing rapidly each year (Fig. 1), manual assess-
                                         models involving untrusted supply chain entities, and the use of                        ment is no longer feasible, making scalable and automated threat
                                         potentially malicious third-party IPs, every stage of SoC design                        modeling and security verification essential.
                                         can face a spectrum of security vulnerabilities [20]. Moreover, the                        To address these limitations, we present ATLAS, a unified frame-
                                         semiconductor industry faces inherent risks from non-security-                          work that transforms vulnerability knowledge into formal proof
                                         aware specifications, implementation flaws, and aggressive time-                        through contextual reasoning. First, ATLAS standardizes threat
                                         to-market demands [20]. As semiconductor systems underpin criti-                        modeling using a comprehensive template that explicitly captures
                                         cal infrastructure, ensuring their resilience demands a proactive,                      attack vectors ensuring consistency and completeness across de-
                                         secure-by-design approach. With post-silicon vulnerability remedi-                      signs. Second, we achieve scalability and adaptability by generating
                                         ation costs rising sharply [21], early identification of threats and                    a threat model database of the common security weaknesses using
                                         integration of countermeasures are essential to protect national,                       standard template, LLM, and publicly available vulnerability repos-
                                         system-level and organizational integrity.                                              itories CWE [47], CVE [11], and CAPEC [10] as a continuously
                                            While functional verification relies on established behavioral                       evolving knowledge base. We have made this database open source
                                         rules from hardware descriptions, security verification remains chal-                   for helping research community. Third, ATLAS can automatically
                                         lenging because it lacks standardized security rules and policies. As                   identify the SoC specifics assets and relevant threat models by ana-
                                         a result, much of the process depends on threat modeling. However,                      lyzing generic asset definition, threat model database, and buggy
                                         conventional threat modeling approaches [14, 36, 40, 49, 50, 53] are                    SoC register transfer level (RTL) code. Fourth, through contextual
                                         largely manual, error-prone, and unable to keep pace with grow-                         reasoning with abstract syntax tree (AST), RTL summary, and SoC
                                         ing design complexity and evolving attack vectors. The National                         specification document, ATLAS guides LLM in generating accu-
                                         Vulnerability Database [55], including CWE [47], CVE [11], and                          rate, design-specific assertion-based security properties for formal
                                         ∗ Equal contribution.                                                                   verification. Evaluated on three HACK@DAC [23, 25, 26] bench-
                                                                                                                                 marks, ATLAS identified 39/48 relevant CWEs and produced correct
                                                                                                                                 properties for 33 of those cases (> 82%), detecting violations and
                                                                                                                                 demonstrating vulnerability knowledge to formal proof.
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.      The rest of the paper is organized as follows - Sec. 2 discusses
                                         DAC ’26, Long Beach, CA, USA
                                                                                                                                 the publicly available vulnerability databases, related works in SoC
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2254-7/2026/07                                                      security verification, and their limitations. Sec. 3 describes the asset
                                         https://doi.org/10.1145/3770743.3804400
DAC ’26, July 26–29, 2026, Long Beach, CA, USA                                                                                             Tashdid et al.


centric threat modeling approach using standard template, adver-           Table 2: Adversary models in ATLAS with different capabilities.
sary models, security knowledge base, and generic asset definition.           Adversary Model       Capabilities
Sec. 4 outlines assertion based security prorpty generation using             Unprivileged Software Limited capability to run user-code
SoC contexts and threat models from Sec. 3. Experimental results              System Software       Admin/root access to system software
are presented in Sec. 5 before concluding the paper in Sec. 6.                Startup code/SMM1     Can tamper the boot or SMM1 code
                                                                              Network               Can communicate with confidential services
2     Background                                                              Software Side Channel Can monitor/extract confidential metadata
In this section we provide a brief summary of the publicly known              Simple Hardware       Physical access w/o expensive equipment/training
vulnerability databases that serves as the security knowledge for             Skilled Hardware      Physical access with skilled training and FA2 tools
ATLAS, existing security verification methods, and their limitations.         Insider Threat        Anyone within the trusted supply chain
                                                                           1 System management mode, 2 Failure analysis.

2.1     Vulnerability Databases
                                                                          flows, SoC security design lacks standardized constraints or rules
To ensure SoC security, one of the first thing required is finding
                                                                          to guide verification, which in turn limits emerging approaches
a comprehensive repository of real-world vulnerability incidents.
                                                                          such as fuzzing and formal verification [30]. Recent assertion-based
The vulnerability databases maintained by the MITRE Corporation,
                                                                          and large language model (LLM)-generated property methods tar-
specifically, CWE [47] and CVE [11] represent the most comprehen-
                                                                          get specific CWEs, but remain ad hoc, unscalable, and unable to
sive and reliable crowd-sourced repositories for security incidents
                                                                          generalize across the broader vulnerability space [4, 5, 45, 46, 52].
across hardware and software domains. The CWE catalog defines
and classifies abstract security weaknesses, such as improper privi-
lege checks or insecure data paths, while CVEs document concrete          3      Asset Centric Threat Modeling
instances of these weaknesses in specific products or platforms [37].     In this section we discuss how ATLAS performs asset centric threat
Fig. 1(b) shows that over the years, the number of identified CWEs        modeling by defining a template and adversary models, leveraging
and CVEs has grown significantly, reflecting both the increasing          vulnerability databases, and utilizing LLM to address the limitations
complexity of modern hardware systems and the expanding attack            of existing threat modeling methods highlighted in Sec. 2.2.
surface they present. For hardware security in particular, this rise
underscores the urgent need for systematic, design-time mitiga-           3.1      Threat Model Template
tion strategies. By standardizing and disseminating vulnerability         The need for a universal standard is one of the most critical lim-
knowledge, these databases form a foundational resource for future        itations of existing threat modeling methods. Therefore, ATLAS
security-aware SoC development.                                           standardizes a set of elements as a template that must be defined
2.2     Related works and their limitations                               for SoC threat modeling. Table. 1 shows the threat model template
As stated previously, threat modeling is the foundation of secu-          elements and an example for CWE-1245 [12]. The example threat
rity verification, providing a systematic way to identify and miti-       model is kept concise for brevity. To the best of our knowledge, this
gate vulnerabilities before they propagate to downstream design           is the first attempt to standardize threat modeling.
stages. Despite its importance, existing methodologies suffer from
several limitations. 1 Manual approaches are becoming increas-            • Adversaries: Different systems have a diverse threat landscape
ingly ineffective as design complexity and attack sophistication            based on the entities involved in the design and development. Ad-
grow [27, 32, 39, 42, 54]. As attack methods evolve and the range           versary models categorize different types of potential attackers by
of weaknesses expands, as shown in Fig. 1(a), these approaches fail         defining their scopes, capabilities, and access levels. The selected
to scale, limiting coverage and slowing response to new threats.            adversary model helps to decide whether a type of vulnerability
 2 The CWE and CVE databases discussed in Sec. 2.1 collectively             can be exploited in a particular system. ATLAS utilizes the adver-
contain over 200,000 hardware and software vulnerabilities, yet             sary models [41] summarized in Table 2 to provide a structured
few techniques comprehensively leverage this knowledge to im-               framework to identify attack scenarios and vulnerabilities.
prove SoC security. 3 The lack of comprehensive threat modeling           • Assets: It is the secret data, process, or element that must be
further reduces the effectiveness of security verification. Existing        protected. Any secondary asset utilized to protect a primary asset
techniques can be broadly divided into static and dynamic methods.          also worth to protect. Utilizing the asset definitions in Table 3,
 4 Static methods, including formal verification [16, 18, 48], con-         ATLAS performs an asset centric threat modeling in Sec. 3.5.
colic testing [34, 35], and code analysis [2, 31], require engineers to   • Attack Surfaces: The adversary is expected to utilize an inter-
translate high-level security requirements into formal assertions,          face to interact with or access an asset to exploit a vulnerability. It
creating substantial manual overhead and increasing susceptibility          greatly depends on the type of the system, and adversary model.
to human error. 5 Dynamic methods such as fuzzing [6, 17, 22, 56]           For instance, an unprivileged software adversary may leverage
and penetration testing [3, 51] improve runtime coverage but still          command prompt as an attack surface, wherever, debug interface
depend on manually crafted feedback functions, limiting automa-             could be more appealing for a simple hardware adversary.
tion. More importantly, current methods do not adapt well to an           • Vulnerabilities: A vulnerability is a weakness or flaw in a sys-
evolving threat landscape. Unlike area, power, and performance              tem that can be exploited to compromise its security. For instance,
                                                                            a lack of bound checking (vulnerability) exploited by an adversary
            Table 1: Threat model template and example.
                                                                            may result in a buffer overflow attack (threat).
    Template        CWE-1245 Threat Model                                 • Threats: When an adversary exploits a vulnerability it becomes
    Adversary       Simple Hardware Adversary                               a threat. For instance, in the previous example, buffer overflow
    Assets          Hardware State and Logic Integrity                      attack is the threat in this scenario. Please note that many existing
    Attack surface Hardware Interfaces and State Machine Logic              threat models confuse vulnerabilities with threats [28]. ATLAS
    Vulnerabilities Improper or insecure FSM design                         recognizes them as distinct elements in the threat model.
    Threats         Exploiting undefined or insecure FSM transitions
ATLAS: AI-Assisted Threat-to-Assertion Learning for System-on-Chip Security Verification                                                       DAC ’26, July 26–29, 2026, Long Beach, CA, USA


3.2     Security Knowledge Source                                                          links to generate additional threat models for selected hardware
In ATLAS, we generate a threat model database (TMDB) that serves                           CWEs, and each output was reviewed and refined through human
as the knowledge base for security verification in Sec. 4. Several                         feedback. The manually validated models were consolidated into a
factors motivate the need for such a database. 1 Functional verifi-                        JSON-formatted dataset that included instructions, template fields,
cation has testbenches, coverage metrics, and well-defined correct-                        adversary descriptions, and exemplar input–output mappings. After
ness properties [20], whereas security verification lacks comparable                       providing GPT-5 with this context dataset, the model consistently
structure. Designers must still manually infer which threats apply                         produced complete and accurate threat models verified by human
to an SoC, leading to the limitations discussed in Sec. 2.2. 2 The                         expert, enabling us to automatically generate the remaining Hard-
National Vulnerability Database [55] contains rich security knowl-                         ware Design CWEs and assemble a comprehensive TMDB covering
edge, but it is too abstract, scattered, and unstructured for direct                       all known hardware weaknesses [13]. We utilize this TMDB for SoC
use in verification. 3 Human-driven threat modeling cannot keep                            specific asset identification (Sec. 3.4) and threat modeling (Sec. 3.5).
pace with SoC complexity, diverse IP blocks, and the rapidly ex-                           3.4        SoC Specific Assets Detection
panding hardware attack surface, which is why existing works                               ATLAS utilizes threat model database (TMDB) and a set of generic
cover only a limited subset of CWEs [16, 45]. 4 Identifying as-                            asset definition, to identify design assets and conduct an asset
sets in RTL is only part of the task; engineers must also determine                        centric threat modeling. Fig. 3 shows the flow of detecting SoC
which CWEs apply to each asset class. 5 Security verification [30]                         assets and relevant threat models for security verification in Sec. 4.
depends on accurate, repeatable mappings from weaknesses to                                • In an SoC, assets refer to sensitive information and data that
assertion templates, making ad hoc generation error-prone and                                require protection from unauthorized access and safeguarding
incomplete. A threat model database standardizes and organizes                               against various threats. ATLAS identifies these security critical
vulnerability knowledge into actionable, reusable vectors, enabling                          assets in the RTL by providing GPT-5 a list of generic asset def-
automated and consistent mapping of assets to relevant weaknesses                            initions. We categorized 7 types of generic assets as shown in
and their corresponding property families. By providing repeatable                           Table. 3 by analyzing the NVD [10, 11, 47] that exploits various
security criteria and scalable coverage across designs and evolving                          types of assets in it’s database. And also the probable keywords
threats, it becomes the foundation for automated, comprehensive                              connecting these assets in an SoC by conducting literature sur-
SoC security verification. We have published this threat model                               vey [9, 44]. The Table. 3 is kept concise due to brevity.
database (https://github.com/KimiaTasnia/Threat-Model-Database-                            • With the help of TMDB and generic asset definition, LLM as-
for-Hardware-Security) for security professionals and researchers.                           sisted in finding the potential security assets in the given buggy
                                                                                             SoC RTL. Fig. 3(a) shows an example of “Runtime Integrity &
                                                                                             State Resources” with its generic definition and LLM’s response
3.3     Threat Model Database Generation                                                     to identify the associated assets in the OpenTitan Direct Mem-
Several attack patterns                                                                      ory Access (DMA) module [33] utilized in several HACK@DAC
(CAPEC) can exploit                                                                          competition [26]. Fig. 3(b) is the identified assets in the dma mod-
a product vulnerabil-                                                                        ule which lists the assets type, specific signal names, role of the
                            Threat Adversary    Example Threat      Human
ity (CVE) which suf- Model Models                   Model          Feedback                  signals and reasoning behind it to be asset.
fers from a fundamen- Template                                                             3.5        Threat Modeling with ATLAS
tal weakness (CWE).
For instance, both ‘CAPEC-                                                                 Once ATLAS detects the SoC assets that designer must protect, it
1: Accessing Functional- Vulnerability Database     LLM        Threat Models
                                                                                           performs asset centric threat modeling at the RTL abstraction layer.
ity Not Properly Con- Figure 2: LLM assisted threat model data-                            First, we provide LLM both the SoC asset list from Sec. 3.4 and
strained by ACLs’ and base generation in ATLAS.                                            threat model database (TMDB) from Sec. 3.3 as shown in Fig. 4(a).
‘CAPEC-180: Exploiting                                                                     The TMDB already has threat models for every hardware CWEs.
Incorrectly Configured Access Control Security Levels’ exploits the                        This way ATLAS covers all known hardware security threats.
‘CWE-1191: On-Chip Debug and Test Interface With Improper Access                           Query1: You are a hardware               Generic Asset Definition- Runtime Integrity & State assets:
                                                                                           security engineer expert in secrity      1. These assets relate to the ongoing, correct, and secure operation of the SoC after it
Control’ derived from CVE-2019-18827. Therefore, resistance to a                           analysis of the RTL designs. You are
                                                                                                                                    has successfully booted. Their purpose is to maintain and prove the device’s
                                                                                                                                    trustworthiness during operation.
specific attack pattern (e.g., CAPEC-1) does not necessarily make                          going to help in developing an asset     2. Device Integrity and Operation: The overall goal of ensuring the system runs as
                                                                                           centric threat modeling of an SoC.       intended without crashing or being compromised.
                                                                                                                                    3. Hardware State and Logic Integrity: The correctness of internal hardware
the developed hardware resilient against remaining attacks (e.g.,                                                                   components, like Finite State Machines, that control secure operations.
                                                                                            First you need to identify the assets   4. Keywords may include- "state_*", "defult_*", "measurement_*"
CAPEC-180) exploiting the same weakness (CWE-1191). Hence, in                               from a buggy RTL code. Here is the
                                                                                                                                                                                                                        LLM’s Response1
ATLAS we develop individual threat model for each CWE [47] by                               generic asset definition you need
                                                                                            to look for in this buggy RTL code-
                                                                                                                                     A) DMA control / FSM (hardware state & logic integrity)
                                                                                                                                    1) name: dma_ctrl_fsm
                                                                                                                                    signals: [dma_ctrl_reg, dma_ctrl_new, dma_ctrl_en]
following the template discussed in Sec. 3.1 to generate a threat                           // module dma {
                                                                                                                                    role: "Drives the whole DMA lifecycle"
                                                                                                                                    why_sensitive: "Corrupting/forcing state can skip PMP checks,
model database (TMDB) of known security weaknesses. However,                                …
                                                                                                                                    double-execute, or stall system."
                                                                                                       endmodule                    2) name: dma_phase_vector
we include all the associated CVEs and CAPECs in prompts to cover                                                                   signals: [valid_reg, valid_new, valid_en, valid_o]
                                                                                                                                    role: "Runtime progress/attestation of what the DMA is doing right now."
                                                                                           Query2: Now I will provide you a
known vulnerabilities connected to that CWE.                                                                                        why_sensitive: "Downstream logic trusts it; spoofing can hide illegal transfers."
                                                                                           threat model database. This threat       # B) Security enforcement state (PMP gate for DMA)
   Fig. 2 shows how we leverages GPT-5 to assist in threat model                           model database is generated from         ...................................................................................
                                                                                           CWEs, where for each CWE there is        # D) Handshake / abort control (system-wide operation integrity)
                                                                                                                                    ...................................................................................
database generation using template (Sec. 3.1), security knowledge                          a threat model. You need to find out
                                                                                           the applicable CWEs from the threat                                                                      LLM’s Response2
source (Sec. 3.2), example threat models, and human feedback. To                           model database which are pruned to
                                                                                                                                    Most applicable CWE threat models from your database-
                                                                                                                                    CWE-1257: Improper Access Control Applied to Mirrored or Aliased Memory Regions
construct the threat model database (TMDB), we began by man-                               affect these sensitive assets that       CWE-1245: Improper Finite State Machines (FSMs) in Hardware Logic
                                                                                           you listed.                              CWE-1221: Incorrect Register Defaults or Module Parameters
ually creating a small set of high-quality example threat models                            Provided: Threat Model Database
                                                                                                                                    ……………………………………………………………….
                                                                                                                                    *
                                                                                                                                    Ordering does not matter
using the standardized threat model template and adversary def-
initions. These examples established the expected structure and                            Figure 3: Asset-centric threat modeling from generic asset defini-
depth of analysis. GPT-5 was then prompted with these examples                             tions (Table 3) to SoC-specific asset detection, then CWE identifica-
along with CWE [47] and its associated CVE [11], and CAPEC [10]                            tion using the Threat Model Database (TMDB).
DAC ’26, July 26–29, 2026, Long Beach, CA, USA                                                                                                                      Tashdid et al.


Table 3: Generic assets definition for SoC specific assets detection.
                                                                                                           (a) Section 3
 Asset Type          Definition                            Keywords
                     Confidential information.             keys_*, pass_*, secret_*                            LLM                                  Abstract    SoC RTL Design
 Sensitive Data                                                                                                            Buggy RTL      Yosys/
                     IP, firmware, or personal data.       protected_*, user_*             Generic Asset
                                                                                                                                         PyVerilog Syntax Tree Summary Document
                     Verifies and loads boot.              boot_*, hash_*, rom_*            Definition
 Boot Integrity                                                                                                                                       SoC Context (b) Section 4
                     Establishes hardware root of trust.   otp_*, key_*
 Attestation Data &  Signed measurements of states.        pcr_*, measurement_*
 Measurement Reports Stored in dedicated registers.        idev_*
                     Device-specific non-volatile values.  otp_*, trim_*, nvm_cfg_*
 Parametric Data                                                                           Threat Model               SoC Threat Model             Security Property,    Security
                     Used for identity and calibration.    uid_*, device_id_*, serial_*                  SoC Assets                         LLM
 Privileged System   Privileged control registers.         debug_* , *_mode                DB (All CWEs)               (Relevant CWE)              Verification Script Vulnerability
 Resources           Accessible in trusted modes.          *_level
                     Shared buses or memories.             ready_*, valid_*, dma_*
                                                                                          Figure 4: Overview of AI-assisted security verification flow by AT-
 Shared Resources
                     Arbitration to prevent leakage.       req_*, grant_*, crossbar_*     LAS. (a) Asset-centric threat modeling, discussed in Sec. 3, using a
 Runtime Integrity & Correctness of runtime states.        state_*, default_*             generic asset definition, threat model database, and buggy SoC RTL
 State Resources     FSM integrity and policy enforcement. pcr_*, measurement_*           code. The outcome of this step is SoC threat model of relevant CWEs.
                                                                                          (b) Property-based security verification using SoC context (AST, RTL
Second, LLM runs a keyword mapping in the TMDB to match those
                                                                                          summary, and design document), threat model of the relevant CWEs.
assets in the database. For instance, for the DMA control/FSM assets
in Fig. 3(b), ATLAS searched with the keywords (fsm, finite state                         At the end of the section, we pair each objective (Obj) with a
machine, state, control flow, transition, deadlock) in the TMDB. It                       corresponding resolution (Res).
mapped these keywords in every CWE threat models and identified
the most critical CWEs which are pruned to exploit those assets as                        4.2      Why SoC Context Matters
shown in Fig. 3(d). The threat model database helped tremendously                         Formal proofs are only as strong as the properties they verify, and
in this step since it has a detailed threat model with critical compo-                    those properties must be grounded in the correct design context [30].
nents like assets, threats, vulnerabilities explaining the scenarios                      While ATLAS leverages LLMs to reduce human error, minimize
for any potential weakness in a system.                                                   reliance on domain-specific expertise, and improve scalability, an
Finally, along with listing all the potential weaknesses, ATLAS                           SoC RTL and threat model from Sec. 3 alone cannot provide the
identified the corresponding threat models for the detected CWEs                          intent required to derive sound security constraints [19, 43]. To
present in the TMDB. In this way, ATLAS was able to generate                              produce meaningful assertions, the LLM must understand where
threat models for all the possible hardware CWEs in an SoC.                               an attacker interacts (attack surfaces), who controls inputs (ad-
                                                                                          versary/controllability), what assets must be protected, and how
4     Security Verification using Formal Proof                                            the design behaves across modes, resets, and handshakes. Without
                                                                                          these contexts, LLM-generated assertions risk being out-of-scoped,
With the CWE-based SoC threat models generated in Sec. 3, here
                                                                                          under-constrained, or misleading.
we use formal proof to identify the vulnerabilities in a buggy SoC.
                                                                                             Hence, to enhance the SoC design context, we combine three
                                                                                          complementary sources. First, the design documentation of the
4.1     Rationale for Formal Verification                                                 SoC, which contains the specifications, interface specs, register
Security bugs are often hidden or masked in rare input combina-                           maps, mode semantics, and trust boundaries. Second, the abstract
tions, resets, or corner-cases. Constraint Random Verification (CRV)                      syntax tree (AST) of the RTL that contains topological and struc-
covers only a small subset of those cases, and when it triggers them,                     tural details of the hardware (e.g., inputs, outputs, wires, registers,
it takes long time to observe the impact. On the other hand, formal                       parameters, states, clock/reset style). And third, a general summary
verification translates the design into a formal (logic-based) model                      of the SoC RTL, generated by LLM with security in mind. In the
and exhaustively checks whether it satisfies given properties. If a                       following subsections we discuss the role of each of the sources
violating execution exists, the formal tool returns a minimal coun-                       and perform an ablation study in Sec. 5 (Fig. 6).
terexample trace, otherwise, it produces a proof or correctness. This                     4.2.1 Design Documents (DD). Design documents are developed
aligns with our security objective of turning each SoC threat model                       by architects, designers, and verification engineers and provide a
into a property that is either formally proven or demonstrated to                         rich view of intended behavior of the SoC that the base RTL cannot
be vulnerable through a concrete counterexample.                                          capture. They describe the human intended architecture, name the
    Sec. 3 yields the SoC threat model with a set of relevant CWEs,                       assets to be protected, and spell out privilege and lifecycle rules,
however, not all are exploited in the RTL under review. To distin-                        interface semantics, and behavior [38]. For instance, as shown in
guish actionable vulnerabilities from non-issues, ATLAS generates                         Fig. 5, once we provide the OpenTitan Direct Memory Access (DMA)
an assertion based security property for each relevant CWE, cap-                          documentation [33] to LLM, it infers that the specification requires
turing its corresponding attack vectors in a form suitable for formal                     the DMA to enforce bounded memory ranges and Physical Memory
proof. A failing property indicates that the weakness represented                         Protection (PMP) checks and that the design must uphold a defined
by that CWE is concretely exploitable in the design, whereas a                            level of access control granularity. Additionally, this context lets
proven property suggests that the RTL upholds the corresponding                           us align the asset-centric CWE threat model from Sec. 3 with the
security requirement under the stated assumptions. We therefore                           design under review. One of the identified CWE in the DMA module
define three objectives for formal security verification. Obj1) Map                       is CWE-1190. Moreover, LLM can correlate that this is a potential
each relevant CWE to one or more assertion property guided by the                         violation since the module had no enable and it will trigger the
threat model (i.e., asset, attack surface). Obj2) Generate concrete                       start port whenever SoC is driven. Therefore, the documentation
SystemVerilog Assertions (SVA) and formal properties bound to                             shows where the attack-surface lies for the RTL.
real signals, modes, and resets. Obj3) Execute the properties in                          4.2.2 AST. As specified previously, ATLAS provides an AST of
JasperGold, review proofs/counterexamples, and record outcomes.                           the SoC RTL code during assertion property generation by LLM.
ATLAS: AI-Assisted Threat-to-Assertion Learning for System-on-Chip Security Verification                                                                   DAC ’26, July 26–29, 2026, Long Beach, CA, USA


                                                     Human Query                  LLM Response
 Query: Act like a formal verification                                                                                       a security-centric RTL summary helps bind assets, policies, and
 engineer, and you are going to help                LLM Formal Property Generation with Contextual Files*
 generate security properties.                                                        - Provided: AST + DD + RTL Summ
                                                                                                                             states, and provides the key cue to condition ATLAS on the adver-
                                                     - Provided: AST
  Provided: Buggy RTL + Threat Model       1. CWE-1245: Improper FSM..             1. There is policy gating for
                                                                                                                             sary model. Using all three sources, the LLM performs an initial
 // module dma {
 …
                                           2. Accessing FSM States..               LOAD/STORE; no debug waiver.              pruning {asset(Summary) ∩ attack-surface(DD) ∩ path(AST)}, or
                                           3. dma_ctrl_reg states: IDLE,           2. abort, done_i are possible
 endmodule                          (a)                                                                                      at minimum forms concrete hypotheses about how sensitive as-
                                           CHECK_LOAD, LOAD,                       security sensitive registers
  LLM Formal Property Generation           CHECK_STORE, STORE, DONE,               3. I need to check if we use abort
                                           ABORT                                   properly..
                                                                                                                             sets should behave in the RTL. Our experiments also showed that
        without Contextual Files                                         (c)                                        (e)
 1. Assessing RTL security features                                                                                          the ordering of these contexts has little to no effect. Res2) With
                                               Binds CWE-1245 to FSM control.         Maps security sensitive registers.
 2. CWE-1245: Improper FSM..
 3. I need to assess FSM states..              Captures RTL FSM States.               Decisive cue on “what” to protect.     the detailed signal names, state encodings, logical semantics, and
 4. If abort is issued when there is no        Answers “who” drives the inputs.                                              interface rules, ATLAS then instantiates non-vacuity covers so an-
 active command running in dma,                                                   property abort_escape;
 the dma gets stuck in a unknown                   - Provided: AST + DD             @(posedge clk_i) disable iff (!rst_ni)
                                                                                                                             tecedents are exercised, providing guideposts for SVA generation.
 state.                                                                              (dma_ctrl_reg == CTRL_ABORT &&
                                           1. Reading Document..           (d)    !done_i) |=> (dma_ctrl_reg !=              Res3) Finally, the resulting properties act as design-rule checks for
property no_unreachable_states;                                                   CTRL_ABORT);
  @(posedge clk_i) disable iff (!rst_ni)                                          endproperty                                JasperGold [8]: the properties are emitted as assertion files together
                                               Masters trust boundaries and
   (dma_ctrl_reg !=
CTRL_START_LOAD) && (dma_ctrl_reg
                                               privileges for DMA RTL.
                                               Learns about designer intended         Rightfully captures that if we’re in
                                                                                                                             with a .tcl harness that compiles the DUT, applies constraints, and
!= CTRL_START_STORE);
endproperty                                    FSM flow and escape behavior.          CTRL_ABORT while done_i is 0, then
                                                                                      we must not be in CTRL_ABORT (i.e.,
                                                                                                                             runs proofs. This yields the outcome targeted in Fig. 4. Inconclusive
    Does not understand the FSM                Answers “where” is the attack-
                                               surface.                               we must leave ABORT); matching         results can be refined by tightening or relaxing assumptions, adding
    states and security context
                                (b)        *
                                            Ordering does not matter                  with golden reference.
    behind the RTL.
                                                                                                                             clarification, and rerunning twice. Persistently inconclusive cases
Figure 5: LLM–assisted security property generation. (a) The same                                                            are flagged for manual review.
prompt (buggy SoC RTL and Threat Model) is given to both methods.
(b) Plain LLM: without context, LLM misreads the design intent and                                                           5     Results & Evaluation
fails to derive the correct security property. (c) ATLAS: adding AST                                                         In this section, we evaluate ATLAS on three industry scale RISC-
provides control and structural knowledge of the FSM behavior. (d)                                                           V based SoC designs. We report detection coverage, properties,
The design documents (DD) then highlight the trust boundaries                                                                and formal proof outcomes, compare against a manual proof base-
and attack-surface. (e) RTL summary exposes the sensitive registers.                                                         line [43] as golden reference, and then ablate the three contexts.
Taken together, ATLAS is able to generate the correct property.                                                              5.1     Experimental Setting
Treating this structure as a graph lets the LLM reason about control                                                         OpenTitan SoC [1] featured in the HACK@DAC benchmarks (’18,
and data flow [29]. In practice, this guides LLM to verify who                                                               ’19, ’21) [23–25] offers a rich set of real-world security bugs, making
drives the signals in which conditions, trace fan-in/fan-out to policy                                                       it an ideal benchmark for assessing ATLAS. ATLAS is assisted by
gates, and enumerate legal state transitions before it ever writes an                                                        GPT-5 as the base LLM. Design documents for the buggy RTL are
assertion. For example, with the DMA AST, the LLM matches CWE-                                                               sourced from the OpenTitan documentation and repository [33].
1245 from SoC threat model on improper finite state machines (FSM)                                                           ASTs are generated using Yosys [57] or PyVerilog with Slang for
usage with the abort signal (See Fig. 5.(b)). Hence, the AST guides                                                          SystemVerilog support. RTL summary is generated by the LLM to
LLM to flag that abort could persist or be X in paths that should be                                                         minimize human bias. JasperGold is used for formal verification.
clean when done_i is low. This matches a known vulnerability that                                                            5.2     Evaluation
was actually exploited in the HACK@DAC 21 [25].                                                                              5.2.1 Benchmark Results. ATLAS runs automatically on each bench-
4.2.3 RTL Summary. The RTL summary is a security-centric syn-                                                                mark in Table 4. To keep the process fast and predictable, we limit
opsis produced by the LLM directly from the source code. It gives                                                            the search to at most three iterations per bug; unresolved cases are
LLM an objective perspective during property generation by high-                                                             flagged for manual review. Most failures within this budget follow a
lighting security critical assets, guardrails, rules and checks without                                                      common pattern: either the bug depends on subtle functional intent
relying on human hints. This reduces the bias, a concept similar to                                                          not stated in the public documentation, or the specification omits
why we do CRV instead of directed verification. The summary also                                                             the exact corner case the property must capture. Across the three
surfaces code-level nuances that are easy to miss in a non-security-                                                         HACK@DAC [26] benchmarks, ATLAS shows strong performance.
centric design document. Revisiting the DMA example from Fig. 5,                                                             The Detected CWEs column in Table 4 lists the CWE-based SoC
LLM is able to note what are the critical registers and assets that                                                          threat models generated by ATLAS as discussed in Sec. 3. For each
are vulnerable, (not explicitly stated in the design documentation).                                                         bug, ATLAS often identifies multiple relevant CWEs. During secu-
4.3        CWE to Property Generation                                                                                        rity verification (Sec. 4), it then detects the correct exploited CWE
After obtaining the CWE-based SoC threat model from Sec. 3, we                                                               (shown in bold in Table 4) by generating assertion-based security
map it to assertion-based security properties using the contexts                                                             properties and checking them in JasperGold for formal proof.
discussed in Sec. 4.2. Fig. 5 compares two pathways that start from                                                             A checkmark (✓) in the property (Prop.) and formal verification
the same prompt (Fig. 5(a)). In (b), the LLM uses only buggy SoC                                                             (FV) columns of Table 4 indicates that ATLAS successfully generated
                                                                                                                                    (a)                             (b)
RTL and the TMDB and fails to generate the correct property.
In contrast, under the ATLAS flow, when the same buggy SoC
RTL and threat model from (a) are augmented with the additional
contexts ((c) AST, (d) Design Documents, and (e) RTL summary),
the LLM produces the correct security property in almost every
case, and these map cleanly to formal proofs (Sec. 5.2.1). Res1)
For CWE-1245 in Fig. 5, the LLM first reviews the general sys-
tem behavior, register map, RTL scope, and I/O connectivity from
the DD. The AST then reveals where policy/privilege gating, re-                                                              Figure 6: TMDB ablation across HACK@DAC’18, ’19, and ’21. (a)
set/initialization hygiene, FSM integrity, ordering, and control flow                                                        Number of correct CWEs identified by an LLM without TMDB versus
are implemented, including RTL details not explicit in the DD. Next,                                                         ATLAS with TMDB. (b) Context ablation on accurate properties.
DAC ’26, July 26–29, 2026, Long Beach, CA, USA                                                                                                                                     Tashdid et al.


 Table 4: Security verification by ATLAS across three HACK@DAC [26] benchmarks by detecting relevant CWE threat models, generating
                                  corresponding assertion based security properties, and performing verification by JasperGold.
                     HACK@DAC18 [23]                                                   HACK@DAC19 [24]                                                 HACK@DAC21 [25]
Module           Bugs                Detected CWEs Prop. FV Module             Bugs                 Detected CWEs Prop.       FV   Module          Bugs                Detected CWEs Prop. FV
adbg_tap         Logic bug          1221, 1191, 1271     ✓   ✓ csr_regfile     Debug exit issue      1244, 1191, 1243     ×   ×    dmi_jtag        Pass flag reset   1239, 1271, 1191      ×   ×
                 Checks 31/32 bits 1298, 1221, 1191      ✓   ✓                 Read/Write access     1262, 1220, 269      ✓   ✓                    Write w/o pass     1245, 1191, 1244     ✓   ✓
                 Pwd not reset      1329, 1271, 276      ✓   ✓                 Incorrect M-mode      1262, 1220, 269      ✓   ✓                    Hardcoded key      1329, 321, 798       ✓   ✓
                 Reset broken      1419, 1271, 1191      ×   ×                 Incorrect update      1256, 200, 203       ✓   ✓                    Unreachable state 1245, 1191, 1221      ✓   ✓
mux_func         Wrong mux           1240, 1245, 1221    ✓   ✓ commit_stage Interrupt                1281, 1262, 1220     ×   ×    csr_regfile     Debug open          1220, 1191, 1243    ✓   ✓
                 Out uncleared       325, 226, 1271      ✓   ✓              ×2 Commit                1281, 1241, 1271     ×   ×                    Privilege leak      1262, 1220, 269     ✓   ✓
riscv_cs_reg     Wrong privilege      1207, 1262, 269    ✓   ✓ axi_node        Improper bypass       1220, 1191, 269      ×   ×    aes_192         Counter stuck        1240, 323, 330     ✓   ✓
apb_gpio         Lock writable        1207, 1220, 276    ×   × ariane          No flush after atomic 1281, 1206, 1271     ✓   ✓    reglk_wrapp.    Locks disabled      1232, 1221, 276     ×    ×
                 Reset clears lock    1206, 276, 1271    ✓   ✓                 No flush after priv   1281, 1191, 1241     ✓   ✓                    Locks dropped       1234, 1232, 1221    ×    ×
axi_address_dec. Errors ignored        20, 703, 388      ×   × controller      Halt w/o exception    1207, 1419, 1271     ✓   ×    sha256_wrapp. Input uncleared        1239, 226, 1271    ×    ×
periph_bus       Dual overlap        1260, 1203, 1257    ✓   ✓                                                                     aes0_wrapp.     Input uncleared      226, 1243, 1271    ✓   ✓
                 GPIO range alias    1257, 1203, 1260    ✓   ✓                                                                                     Ungated debug        1243, 1191, 1243   ✓   ✓
                 Triple overlap      1260, 1257, 1203    ✓   ✓                                                                                     Uncleared debug     1258, 1243, 226     ×   ×
riscv_core       Halted access       1298, 1191, 1262    ×   ×                         How to Read the Table                       acct_wrapp.     Reset full access    276, 1221, 1220    ×    ×
                 FSM hanged           1245, 1241, 1271   ✓   ✓ CWE formatting:
                 Incomplete case      1245, 1241, 1271   ✓   ✓
                 Insecure req         1220, 1262, 269    ✓   ✓ • Green = Correct;
                                                               • Strikethrough = Undetected by ATLAS;
rtc_clock        RTC time bug         1247, 682, 1271    ✓   ✓ • Blue Texts = Assumed correct (no baseline for 5 CWEs).            dma             Abort sticky        1245, 1271, 1221    ✓   ✓
soc_intercon.    Out-of-range        1203, 1260, 1257    ×   × • Unbolded CWEs = Relevant CWEs (Sec. 5.2.3)                        rsa_wrapp.      Output uncleared     226, 1271, 1271    ✓   ✓
                                                               • ✓ / × Indicate pass/fail (Prop. and FV).
jtag_tap_top     No password         1262, 1191, 1220    ✓   ×                                                                     riscv_periph.   Hardcoded ROM       1310, 1323, 1312    ×    ×

the assertion-based security property and detected the weakness                                     which is less than 30% detection rate. In contrast, ATLAS identifies
in the given HACK@DAC [26] module. With our threat model                                            17/20, 11/11, and 11/17, respectively, with the TMDB, highlighting
database (TMDB), ATLAS detected 39/48 security weaknesses                                           how structured threat modeling can improve LLM performance.
(CWEs) across the three HACK@DAC [26] benchmarks. More                                                 Moreover, what makes ATLAS capable lies in the three SoC con-
importantly, when the correct CWE was identified, ATLAS                                             texts. Ablation on Fig. 6(b) shows the same trend. When provided
generated the correct property in more than 82% of the cases.                                       only one SoC context, formal verification detects ≤ 5 accurate
When ATLAS does not detect the exact CWE, it still produces “rele-                                  properties. ATLAS detects +10, +4, and +6 additional correct prop-
vant” CWEs from the SoC threat model in Sec. 3. Even when formal                                    erties in HACK@DAC18, 19, and 21 benchmarks corresponding
verification fails, the generated property is often still useful. Such                              to roughly 3×, 2.3×, and 2.5× improvement. It is appearant that,
failures often occur because the harness does not exercise the exact                                TMDB is the root of identifying the CWEs, which then, with the
exploit path or because internal guards mask the issue under nomi-                                  help of three SoC contexts, results to accurate property generation.
nal stimuli. In these cases, the property can still point to a real SoC                             5.2.3 Relevant CWE and Property Generation. During CWE gener-
weakness. For example, several control and privilege checks gener-                                  ation from TMDB, ATLAS often lists more than one relevant CWE
ated by ATLAS were not proven in the given environment, yet they                                    because the same asset can have multiple weaknesses. One may
revealed missing controls or incomplete resets that require fixes,                                  be truly exploited while a nearby rule on that asset still holds. In
consistent with the golden reference [43]. We treat these cases as ac-                              HACK@DAC’18 apb_gpio, a real weakness exists in the lock register
tionable warnings rather than false alarms. When ATLAS succeeds,                                    where the key can be overwritten. ATLAS also proposed a related
high-quality context greatly improves security verification: contexts                               property for the same lock-register asset that checks whether the
with clear interface and state descriptions yield higher first-pass                                 address decoding for the key is correct. Furthermore, our experi-
success rates. This is visible in Table 4, where ATLAS consistently                                 ments showed strong correlation among CWEs. A single weakness
detected the correct CWE and generated the appropriate prop-                                        can overlap with two CWEs that describe nearly the same rule using
erty for well-documented blocks such as aes_192 and rsa_wrapper.                                    different terms. For instance, in csr_regfile from HACK@DAC’21,
By contrast, missed CWE detections usually correspond to under-                                     ATLAS detected CWE-1220 and CWE-1262 together for the same
specified designs. For example, in HACK@DAC’18 [23], the first                                      debug scenario. One emphasizes access control policy, while the
adbg_tap bug is described only as a generic logic error, and the                                    other focuses on privilege enforcement. In practice, both capture
documentation does not specify the intended latch and mask be-                                      the idea that entering debug must not weaken privilege. Hence,
havior. Similarly, in HACK@DAC’21 [25], the reset behavior of the                                   ATLAS reports both CWEs together.
dmi_jtag pass flag is not specified. In both cases, the lack of ex-                                  6     Conclusion and Future Directions
plicit functional contracts makes automatic property construction                                   ATLAS bridges standardized threat modeling and property-based
difficult for ATLAS.                                                                                formal verification for SoC security. It builds a CWE-driven threat
   To understand deeper into how contexts help, in the following                                    model database and combines design documents, AST, and RTL
subsection, we show how the TMDB and three SoC contexts remain                                      summaries to generate design-specific security assertions end-to-
essential to steer the LLM towards meaningful assertions.                                           end, from asset identification to weakness mapping to formal proof.
5.2.2 Ablation Study. We quantify the effect of TMDB and each                                       Across three HACK@DAC benchmark suites, ATLAS reliably iden-
contexts (DD, AST, RTL Summ) across HACK@DAC’18, ’19, and                                           tifies vulnerabilities and produces correct formal properties with
’21. Looking at Fig. 6(a), removing TMDB completely collapses                                       minimal human intervention, outperforming prior approaches and
threat modeling and security verification. For CWE detection, an                                    showing meaningful progress in SoC design and security verifica-
LLM-only baseline detects 6/20 on ’18, 3/11 on ’19, and 4/17 on ’21,                                tion.
ATLAS: AI-Assisted Threat-to-Assertion Learning for System-on-Chip Security Verification                                                  DAC ’26, July 26–29, 2026, Long Beach, CA, USA


References                                                                                             Code Generation. arXiv:2508.03558 [cs.PL] https://arxiv.org/abs/2508.03558
 [1] Joey Ah-kiow and Benjamin Tan. 2024. An Investigation of Hardware Security Bug               [30] Rasheed Kibria, Farimah Farahmandi, and Mark Tehranipoor. 2024. A Survey on
     Characteristics in Open-Source Projects. arXiv preprint arXiv:2402.00684 (2024).                  SoC Security Verification Methods at the Pre-silicon Stage. Cryptology ePrint Archive
 [2] Hasan Al Shaikh, Mohammad Bin Monjil, Kimia Zamiri Azar, Farimah Farahmandi,                      (2024).
     Mark Tehranipoor, and Fahim Rahman. 2023. Quardtropy: Detecting and quantifying              [31] Rasheed Kibria, M Sazadur Rahman, Farimah Farahmandi, and Mark Tehranipoor.
     unauthorized information leakage in hardware designs using g-entropy. In 2023 IEEE                2022. Rtl-fsmx: Fast and accurate finite state machine extraction at the rtl for security
     International Symposium on Defect and Fault Tolerance in VLSI and Nanotechnology                  applications. In 2022 IEEE International Test Conference (ITC). IEEE, 165–174.
     Systems (DFT). IEEE, 1–6.                                                                    [32] Paul Kocher, Jann Horn, Anders Fogh, Daniel Genkin, Daniel Gruss, Werner Haas,
 [3] Hasan Al-Shaikh, Arash Vafaei, Mridha Md Mashahedur Rahman, Kimia Zamiri Azar,                    Mike Hamburg, Moritz Lipp, Stefan Mangard, Thomas Prescher, et al. 2020. Spectre
     Fahim Rahman, Farimah Farahmandi, and Mark Tehranipoor. 2023. Sharpen: Soc                        attacks: Exploiting speculative execution. Commun. ACM 63, 7 (2020), 93–101.
     security verification by hardware penetration test. In Proceedings of the 28th Asia and      [33] lowRISC C.I.C. 2025. OpenTitan: Open source silicon root of trust (RoT) project.
     South Pacific Design Automation Conference. 579–584.                                              https://opentitan.org/. Accessed: 2025-11-12.
 [4] Avinash Ayalasomayajula, Rui Guo, Jingbo Zhou, Sujan Kumar Saha, and Farimah                 [34] Yangdi Lyu, Alif Ahmed, and Prabhat Mishra. 2019. Automated activation of multiple
     Farahmandi. 2024. Lasp: Llm assisted security property generation for soc verification.           targets in RTL models using concolic testing. In 2019 Design, Automation & Test in
     In Proceedings of the 2024 ACM/IEEE International Symposium on Machine Learning for               Europe Conference & Exhibition (DATE). IEEE, 354–359.
     CAD. 1–7.                                                                                    [35] Yangdi Lyu and Prabhat Mishra. 2020. Scalable concolic testing of RTL models. IEEE
 [5] Avinash Ayalasomayajula, Rui Guo, Jingbo Zhou, Sujan Kumar Saha, and Farimah                      Trans. Comput. 70, 7 (2020), 979–991.
     Farahmandi. 2024. Lasp: Llm assisted security property generation for soc verification.      [36] Russ McRee. 2014. Microsoft threat modeling tool 2014: identify & mitigate. ISSA
     In Proceedings of the 2024 ACM/IEEE International Symposium on Machine Learning for               Journal 39 (2014), 42.
     CAD. 1–7.                                                                                    [37] Peter Mell and Irena Bojanova. 2024. Hardware Security Failure Scenarios: Potential
 [6] Kimia Zamiri Azar, Muhammad Monir Hossain, Arash Vafaei, Hasan Al Shaikh, Nu-                     Weaknesses in Hardware Design. Technical Report. National Institute of Standards and
     run N Mondol, Fahim Rahman, Mark Tehranipoor, and Farimah Farahmandi. 2022.                       Technology.
     Fuzz, penetration, and ai testing for soc security verification: Challenges and solutions.   [38] Xingyu Meng, Amisha Srivastava, Ayush Arunachalam, Avik Ray, Pedro Henrique
     Cryptology ePrint Archive (2022).                                                                 Silva, Rafail Psiakis, Yiorgos Makris, and Kanad Basu. 2024. Nspg: Natural language
 [7] S Barnum. 2008. Common attack pattern enumeration and classification (CAPEC)                      processing-based security property generator for hardware security assurance. In
     schema. Department of Homeland Security (2008).                                                   Proceedings of the 61st ACM/IEEE Design Automation Conference. 1–6.
 [8] Cadence Design Systems, Inc. 2025. JasperGold Formal Verification Platform. Cadence          [39] Microsoft Unveils Emergency Windows Update That Disables Intel’s Spectre Fix.
     Design Systems, San Jose, California, USA. Commercial formal verification tool suite              [n. d.]. https://fortune.com/2018/01/29/microsoft-windows-intel-spectre-fix/.
     for property checking, equivalence, and static verification.                                 [40] The MITRE EMB3D Threat Model. 2024. https://emb3d.mitre.org/.
 [9] Paul E. Calzada, Zahin Ibnat, Mark Tehranipoor, and Farimah Farahmandi. 2025.                [41] Intel        Secure         Development:         Threat         Modeling.          [n. d.].
     VerilogDB: The Largest, Highest-Quality Dataset with a Preprocessing Framework for                https://www.intel.com/content/www/us/en/security/security-practices/secure-
     LLM-based RTL Generation. https://arxiv.org/abs/2507.13369                                        development-practices/threat-modeling.html.
[10] Common Attack Pattern Enumerations and Classifications. [n. d.].                             [42] Researchers Point to an AMD Backdoor—And Face Their Own Backlash. [n. d.].
     https://capec.mitre.org/.                                                                         https://www.wired.com/story/amd-backdoor-cts-labs-backlash/.
[11] Common Vulnerabilities and Exposures. [n. d.]. https://www.cve.org/.                         [43] Jayden Rogers, Niyaz Shakeel, Divya Mankani, Samantha Espinosa, Cade Chabra,
[12] CWE-1245: Improper Finite State Machines (FSMs) in Hardware Logic. [n. d.].                       Kaki Ryan, and Cynthia Sturton. 2024. Security Properties for Open-Source Hardware
     https://cwe.mitre.org/data/definitions/1245.html.                                                 Designs. arXiv:2412.08769 [cs.CR] https://arxiv.org/abs/2412.08769
[13] CWE VIEW: Hardware Design. [n. d.]. https://cwe.mitre.org/data/definitions/1194.html.        [44] Dipayan Saha, Sujan Kumar Saha, Mark Tehranipoor, and Farimah Farahmandi. 2024.
                                                                                                       Empowering Hardware Security with LLM: The Development of a Vulnerable Hard-
[14] Fabio De Rosa, Nicolò Maunero, Paolo Prinetto, Federico Talentino, and Martina                    ware Database.
     Trussoni. 2022. Threma: Ontology-based automated threat modeling for ict infrastruc-         [45] Dipayan Saha, Hasan Al Shaikh, Shams Tarek, and Farimah Farahmandi. 2025.
     tures. IEEE Access 10 (2022), 116514–116526.                                                      ThreatLens: LLM-guided Threat Modeling and Test Plan Generation for Hardware
[15] Isra Elsharef, Zhen Zeng, and Zhongshu Gu. 2024. Facilitating threat modeling                     Security Verification. arXiv preprint arXiv:2505.06821 (2025).
     by leveraging large language models. In Workshop on AI Systems with Confidential             [46] Dipayan Saha, Shams Tarek, Hasan Al Shaikh, Khan Thamid Hasan, Pavan Sai Nal-
     Computing.                                                                                        luri, Md Ajoad Hasan, Nashmin Alam, Jingbo Zhou, Sujan Kumar Saha, and Mark
[16] Baleegh Ahmad et. al. 2022. Don’t cweat it: Toward cwe analysis techniques in early               Tehranipoor. 2025. SV-LLM: An Agentic Approach for SoC Security Verification using
     stages of hardware design. In Proceedings of the 41st IEEE/ACM International Conference           Large Language Models. arXiv preprint arXiv:2506.20415 (2025).
     on Computer-Aided Design. 1–9.                                                               [47] MITRE          Software       and       Hardware       Design        CWEs.         [n. d.].
[17] Muhammad Monir Hossain et. al. 2023. Socfuzzer: Soc vulnerability detection us-                   https://cwe.mitre.org/index.html.
     ing cost function enabled fuzz testing. In 2023 Design, Automation & Test in Europe          [48] Pramod Subramanyan and Divya Arora. 2014. Formal verification of taint-propagation
     Conference & Exhibition (DATE). IEEE, 1–6.                                                        security properties in a commercial SoC design. In 2014 Design, Automation & Test in
[18] Jeyavijayan Rajendran et.al. 2016. Formal security verification of third party intellec-          Europe Conference & Exhibition (DATE). IEEE, 1–2.
     tual property cores for information leakage. In 2016 29th International conference on        [49] Ishraq Tashdid, Tasnuva Farheen, and Sazadur Rahman. 2025. SAFE-SiP: Secure
     VLSI design and 2016 15th international conference on embedded systems (VLSID). IEEE,             Authentication Framework for System-in-Package Using Multi-party Computation. In
     547–552.                                                                                          Proceedings of the Great Lakes Symposium on VLSI 2025 (GLSVLSI ’25). Association for
[19] Kaiyan Chang et.al. 2024. Natural language is not enough: Benchmarking multi-modal                Computing Machinery, New York, NY, USA, 391–396. doi:10.1145/3716368.3735248
     generative AI for Verilog generation. In Proceedings of the 43rd IEEE/ACM International      [50] Ishraq Tashdid, Tasnuva Farheen, and Sazadur Rahman. 2026. InterPUF: Distributed
     Conference on Computer-Aided Design. 1–9.                                                         Authentication via Physically Unclonable Functions and Multi-party Computation for
[20] Farimah Farahmandi, M Sazadur Rahman, Sree Ranjani Rajendran, and Mark Tehra-                     Reconfigurable Interposers. arXiv:2601.11368 [cs.CR] https://arxiv.org/abs/2601.11368
     nipoor. 2023. CAD for High-Level Synthesis. In CAD for Hardware Security. Springer           [51] Ishraq Tashdid, Valentina Terry, Jordan Merkel, Tasnuva Farheen, and Sazadur Rahman.
     International Publishing Cham.                                                                    2025. BeyondPPA: Human-Inspired Reinforcement Learning for Post-Route Reliability-
[21] Nusrat Farzana, Fahim Rahman, Mark Tehranipoor, and Farimah Farahmandi. 2019.                     Aware Macro Placement. In 2025 ACM/IEEE 7th Symposium on Machine Learning for
     Soc security verification using property checking. In 2019 IEEE International Test                CAD (MLCAD). 1–12. doi:10.1109/MLCAD65511.2025.11189164
     Conference (ITC). IEEE, 1–10.                                                                [52] Kimia Tasnia, Alexander Garcia, Tasnuva Farheen, and Sazadur Rahman. 2025. VeriOpt:
[22] Vasudev Gohil, Rahul Kande, Chen Chen, Ahmad-Reza Sadeghi, and Jeyavijayan                        PPA-Aware High-Quality Verilog Generation via Multi-Role LLMs. In 2025 IEEE/ACM
     Rajendran. 2024. MABFuzz: Multi-armed bandit algorithms for fuzzing processors. In                International Conference on Computer Aided Design (ICCAD). IEEE.
     2024 Design, Automation & Test in Europe Conference & Exhibition (DATE). IEEE, 1–6.          [53] Kimia Tasnia and Sazadur Rahman. 2025. OPL4GPT: An Application Space Exploration
[23] HACK-EVENT. 2019. HACK@DAC 2018: SoC Security Benchmark. https://github.                          of Optimal Programming Language for Hardware Design by LLM. Association for
     com/HACK-EVENT/hackatdac18 Accessed: 2025-11-14.                                                  Computing Machinery, New York, NY, USA, 981–987. https://doi.org/10.1145/3658617.
[24] HACK-EVENT. 2019. HACK@DAC 2019: SoC Security Benchmark. https://github.                          3697621
     com/HACK-EVENT/hackatdac19 Accessed: 2025-11-14.                                             [54] This ’Demonically Clever’ Backdoor Hides In a Tiny Slice of a Computer Chip.
[25] HACK-EVENT. 2021. HACK@DAC 2021: OpenTitan SoC Benchmark. https://github.                         [n. d.]. https://www.wired.com/2016/06/demonically-clever-backdoor-hides-inside-
     com/HACK-EVENT/hackatdac21 Accessed: 2025-11-14.                                                  computer-chip/.
[26] Hardware security challenge contest. [n. d.]. https://hackthesilicon.com/hackdac24/.         [55] CVSS            Severity         Distribution        Over          Time.           [n. d.].
[27] Intel’s stock drops 30% overnight - company sheds $39 billion in market cap.                      https://nvd.nist.gov/general/visualizations/vulnerability-visualizations/cvss-
     [n. d.]. https://www.tomshardware.com/pc-components/cpus/intels-stock-drops-30-                   severity-distribution-over-time.
     overnight-company-sheds-dollar39-billion-in-market-cap.                                      [56] Timothy Trippel, Kang G Shin, Alex Chernyakhovsky, Garret Kelly, Dominic Rizzo,
[28] Roger G Johnston. 2010. Being vulnerable to the threat of confusing threats with                  and Matthew Hicks. 2022. Fuzzing hardware like software. In 31st USENIX Security
     vulnerabilities. The Journal of Physical Security 4, 2 (2010), 30–34.                             Symposium (USENIX Security 22). 3237–3254.
[29] M Zafir Sadik Khan, Nowfel Mashnoor, Mohammad Akyash, Kimia Azar, and Hadi                   [57] Clifford Wolf and Johann Glaser. 2013. Yosys – A Free Verilog Synthesis Suite. In
     Kamali. 2025. SAGE-HLS: Syntax-Aware AST-Guided LLM for High-Level Synthesis                      Proceedings of the 21st Austrian Workshop on Microelectronics (Austrochip). Linz, Austria,
                                                                                                       47–52.
