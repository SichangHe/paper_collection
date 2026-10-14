                                         IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. XX, NO. X                                                                     1




                                                 PA-Boot: A Formally Verified Authentication
                                                Protocol for Multiprocessor Secure Boot under
                                                       Hardware Supply-chain Attacks
                                                                     Zhuoruo Zhang , Rui Chang , Mingshuai Chen , Wenbo Shen ,
                                                                    Chenyang Yu , He Huang , Qinming Dai , and Yongwang Zhao
arXiv:2209.07936v3 [cs.CR] 21 Apr 2025




                                            Abstract—Hardware supply-chain attacks are raising signif-         be intercepted and implanted with compromised components
                                         icant security threats to the boot process of multiprocessor          during multiple hands of trade. Such supply-chain attacks raise
                                         systems. In this paper, we investigate critical stages of the         significant security threats and thereby an urgent request in
                                         multiprocessor system boot process and identify a new, prevalent
                                         hardware supply-chain attack surface that can bypass secure boot      identifying device vulnerabilities [14], particularly, in the boot
                                         due to the absence of processor-authentication mechanisms. To         process [15], [16].
                                         defend against such attacks, in this paper, we present PA-Boot,          We focus on new hardware supply-chain attacks that can
                                         the first formally verified processor-authentication protocol for     bypass secure boot of multiprocessor systems. A multiproces-
                                         secure boot in multiprocessor systems. PA-Boot is proved func-
                                         tionally correct and is guaranteed to detect multiple adversarial
                                                                                                               sor system includes a bootstrap processor (BSP) responsible
                                         behaviors, such as processor replacements and man-in-the-middle       for initializing and booting the operating system and multiple
                                         attacks. The fine-grained formalization of PA-Boot and its fully      application processors (APs) activated after the operating sys-
                                         mechanized security proofs are carried out in the Isabelle/HOL        tem is up1 . As instances of hardware supply-chain attacks, an
                                         theorem prover with 306 lemmas/theorems and ∼7,100 LoC. We            attacker can intercept a customer’s multiprocessor device and
                                         further implement in C an instance of PA-Boot. Experiments
                                         on the proof-of-concept implementation indicate that PA-Boot
                                                                                                               either (i) replace an AP with a compromised one, e.g., an AP
                                         can effectively identify boot-process attacks with a considerably     with a pre-installed bootkit; or (ii) implant an extra chip sabo-
                                         minor overhead (4.98% on Linux boot process) and thereby              taging the inter-processor communications (man-in-the-middle
                                         improve the security of multiprocessor systems.                       attacks [17]). Such supply-chain attacks can give attackers
                                           Index Terms—Formal verification, theorem proving, secure            control early in the boot process, allowing them to load a
                                         boot, authentication protocol.                                        malicious bootloader or OS kernel. This enables high-privilege
                                                                                                               arbitrary code execution and evades detection by conventional
                                                                                                               security measures that rely on the OS. For instance, see the
                                                                I. I NTRODUCTION
                                                                                                               proof-of-concept in Bloomberg’s “Big Hack” [18], [19].
                                               TTACKS during the boot process are notoriously hard to
                                         A     detect because at this early stage of a device’s lifecycle,
                                         traditional countermeasures like firewalls and anti-viruses are
                                                                                                                  Existing research efforts focus on firmware integrity and
                                                                                                               provide no countermeasures against hardware supply-chain
                                                                                                               attacks in multiprocessor secure boot. Specifically, both the
                                         not yet in place [1]. A widely adopted defence against boot           authenticity of APs and the inter-processor communications
                                         attacks is known as secure boot [2], [3], which enforces every        are conventionally trusted by default universally across all
                                         boot stage to authenticate the subsequent stage such that only        modern multiprocessor systems. In fact, defending against
                                         the firmware signed by an authorized entity (i.e., the device         this new hardware attack surface is challenging: It is difficult
                                         manufacturer) can be loaded and thereby establishes a chain-          to examine all steps through the global supply chain from
                                         of-trust in the entire boot process. During this process, the         manufacturers to customers; moreover, identifying malicious
                                         processors of a device serve as the root-of-trust (RoT) to            components via hardware tampering detection techniques, e.g.,
                                         bootstrap the trust chain [3]. The authenticity of processors         circuit-based sensors and X-ray imaging, requires expertise
                                         is thus of vital importance to system security.                       and is time consuming [20], [21]. Some work uses runtime
                                            However, the globalized and increasingly complicated hard-         monitors to record external behaviors of CPU chips (i.e.,
                                         ware supply chains are threatening the trustworthiness of pro-        I/O, and memory read/write) and verifies chip integrity [22].
                                         cessors – the RoT in secure boot – therefore exposing various         However, specialized hardware components are required to
                                         modern devices to inevitable supply-chain attacks [4]–[11].           extend the system. It is thus desirable to equip the exist-
                                         Specifically, many original equipment manufacturers (OEMs)            ing multiprocessor secure boot process with a mechanism
                                         nowadays outsource their hardware and/or firmware devel-              for authenticating APs and securing communications without
                                         opment to third-party suppliers without full inspection into          requiring custom hardware changes.
                                         their cybersecurity hygiene [12], [13], where the devices can
                                           The authors are with the Zhejiang University, Hangzhou 310027,        1 The same convention applies to symmetric multiprocessing (SMP):
                                         China. Email: {zhangzhuoruo, crix1021, m.chen, shenwenbo, 22151279,   Whereas all the processors in an SMP system are considered functionally
                                         huanghe3776707, qinm dai, zhaoyw}@zju.edu.cn.                         identical, they are distinguished as two types in the boot process.
2                                                          IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. XX, NO. X



   In this paper, we present a processor-authentication proto-                          BSP                                     AP
col, called PA-Boot, to assure both the authenticity of APs and               ROTPK
                                                                                       private
                                                                                                   BootROM
                                                                                                                      private
                                                                                                                                 BootROM
                                                                                         key                            key
the confidentiality of inter-processor communications in the                     Crypto Accelerators                  Crypto Accelerators   OS kernel
early stage of secure boot process for multiprocessor systems.                                               IPIs                            Image
                                                                                      Local APIC                          Local APIC
PA-Boot is capable of detecting multiple adversarial behaviors
                                                                                                                                            Bootloader
including AP replacements and man-in-the-middle attacks.                                                 Bus System
                                                                      NVM
                                                                                                                                              DDR
The boot process is aborted if any of the adversarial behavior
is detected to prevent the attacker from taking control of the         Fig. 1: Key components in multiprocessor secure boot.
system. The security and functional correctness of PA-Boot
is verified based on deductive reasoning techniques: The            A. Normal flow and limitation of secure boot
formalization of PA-Boot and its fully mechanized security             Secure boot [2] establishes a chain-of-trust (CoT) to ensure
proofs (in terms of the AP authenticity, certificate integrity,     firmware integrity. It serves as a default (or often mandatory)
etc.) are conducted in the (interactive) theorem prover Is-         feature in modern secure devices like laptops, desktops, smart-
abelle/HOL [23]. This fine-grained formalization of PA-Boot         phones, and IoT devices [3], [24]. The process begins with
in Isabelle/HOL succinctly captures its key components, the         the immutable bootloader in read-only storage, considered
system behaviors, and a full range of adversarial capabilities      the hardware root-of-trust (RoT). As the system’s security
against the protocol. To the best of our knowledge, PA-Boot is      foundation, the RoT must be immutable and tamper-resistant.
the first formally verified processor-authentication protocol for   It initializes the hardware, locates the next boot image in
secure boot in multiprocessor systems. We further implement         Non-Volatile Memory (NVM), and loads it into memory. The
in C an instance of PA-Boot called CPA-Boot. Experiments            RoT then verifies the image’s integrity and authenticity using
simulated via ARM Fixed Virtual Platforms (FVP) suggest             the Root of Trust Public Key (RoTPK), an OEM key stored
that CPA-Boot can effectively identify multiple boot-process        immutably as a hash or in full. The image, signed with the
attacks – by either manipulating the APs or tricking the            Root of Trust Private Key, ensures it comes from a trusted
AP-authentication mechanism – with a considerably minor             source. Execution proceeds only if the image is verified.
overhead and thus essentially improve the security of multi-        Each subsequent boot stage follows this process, verifying
processor systems. We have open-sourced our code, available         the next image before transferring control. This chain-of-trust
at https://zenodo.org/records/14513558.                             ensures that only verified components progress through the
                                                                    boot sequence, ultimately loading the kernel image securely.
Contributions. The main contributions are summarized as:
                                                                    Secure boot implementation varies across platforms [25], with
 • Design of PA-Boot: We inspect critical steps in multi-
                                                                    room for platform-specific operations. For enhanced security
   processor secure boot and identify a new, prevalent attack       and efficiency, many systems integrate cryptographic engines
   surface – exhibiting hardware supply-chain attacks – that        for operations like signature verification and hash calculations.
   may bypass secure boot due to the lack of AP authen-
                                                                       Nevertheless, the secure boot’s chain-of-trust (CoT) can be
   tication. To defend against such attacks, we design the
                                                                    undermined by a malicious RoT. The integrity of the system
   first processor-authentication protocol PA-Boot for secure
                                                                    depends on the assumption that the code in the first boot
   boot in multiprocessor systems that is amenable to formal
                                                                    stage (acting as the RoT) is trustworthy or at worst buggy
   verification via theorem proving.
                                                                    but non-malicious. Early systems stored this code on a write-
 • Verification of PA-Boot: We formalize PA-Boot based
                                                                    protected flash memory (e.g., BIOS in PCs), but BIOS ROM
   on multi-level abstraction-refinement in Isabelle/HOL via
                                                                    is poorly protected and easily writable, leading to attacks
   91 locale/definitions. Meanwhile, we formalize multiple
                                                                    exploiting the lack of access control during BIOS reflashing
   properties on both functional correctness and security
                                                                    [26]. In response, modern systems use hardwired bootROM,
   (e.g., authenticity and integrity). The proof that PA-Boot
                                                                    an immutable hardware component integrated into the CPU
   satisfies these properties is then fully mechanized in the
                                                                    [27], [28]. Most research assumes the CPU chip, as part of
   form of 306 lemmas/theorems and ∼7,100 LoC
                                                                    the trusted computing base (TCB), is tamper-resistant and
 • Implementation       and evaluation: We implement
                                                                    trustworthy, while off-chip components are vulnerable [27]–
   CPA-Boot in compliance with the formalization of
                                                                    [29]. However, we show that the hardware supply chain poses
   PA-Boot. To build confidence in their consistency, we
                                                                    a risk, as malicious actors with access to the hardware supply
   introduce a validation framework that extracts executable
                                                                    chain can replace genuine CPU chips, compromising the RoT
   code from our Isabelle/HOL model and validates it
                                                                    and gaining control over the system.
   against CPA-Boot. We integrate CPA-Boot in a real-
   world bootloader and show on FVP that CPA-Boot can
   effectively identify multiple adversarial behaviors like         B. Secure Boot in Multiprocessor Systems
   replacing APs and man-in-the-middle attacks, with a                 Fig. 1 illustrates the key components of a multiprocessor
   considerably minor overhead (4.98% on Linux boot).               secure boot system. Without loss of generality, we assume
                                                                    throughout the paper that the motherboard of a multiprocessor
                      II. BACKGROUND                                device is equipped with two processors, each in physically
  This section recapitulates secure boot in multiprocessor          separate chip sockets: one as the BSP and the other as the
systems and hardware supply-chain attacks.                          AP. Each processor has a unique on-chip private key as its
PA-BOOT: A FORMALLY VERIFIED AUTHENTICATION PROTOCOL FOR MULTIPROCESSOR SECURE BOOT UNDER HARDWARE SUPPLY-CHAIN ATTACKS                          3



                                                                                                                              (a)

                                                          BSP                                               AP
                                               PA-Boot                                           PA-Boot
                                                            RootCertHash                                      RootCertHash
                    AP          NVM            protocol                                          protocol
                certificate                         bootROM                                           bootROM
                                                                                                                                    Memory
                 Root         OS kernel       session key     private key                       session key     private key         OS kernel
                                                                                          (b)
               certificate     image                                                                                                 image
                                               crypto accelerators                               crypto accelerators
                                                                            IPI channel
                  BSP         bootloader                                                                                            bootloader
               certificate


Fig. 2: Threat model of PA-Boot.    marks potential vulnerabilities to adversarial behaviors (a) and (b) in multiprocessor
secure boot. Components of PA-Boot are colored in yellow.
hardware identifier. The processors are connected via a shared detection, like checking credentials, to ensure they receive
bus to a mutable NVM and shared memory. Each processor genuine components from the vendors. In addition, attacks
includes a cryptographic extension module to accelerate opera- at the manufacturing steps can’t easily target a specific end-
tions. Except the shared bus, the BSP and AP communicate via product, making attacks highly unlikely.
a dedicated channel for inter-processor interrupts (IPIs). The      We assume a realistic and powerful attacker who has
motherboard is soldered a baseboard management controller physical access to the target multiprocessor device in the post-
(BMC), which is connected to the BSP and handles initial- manufacturing hardware supply chain, i.e., in-transit from the
ization and monitoring tasks. Note that the roles of BSP and OEM to the end-user or in the field. Therefore, the attacker can
AP are determined by their socket positions on motherboard, intercept the device and then replace the pluggable CPU chips
allowing the BMC to identify them accordingly.                   on board and have malicious modification to the PCB, such
   The multiprocessor secure boot begins by executing the as implanting a interposer chip on the board wires, to launch
immutable code in the processors’ bootROM, considered the the following two attack vectors (see               in Fig. 2) under no
hardware root-of-trust (RoT), which initializes the hardware. awareness of the BSP:
The AP enters a suspended state while the BSP proceeds (a) AP-replacement attack: The attacker replaces the original
with the following steps: (i) Locating the bootloader image in       AP with a malicious one that has, e.g., a factory-installed
the NVM, (ii) Loading it into shared memory, (iii) Verifying         bootkit in its bootROM. Such a malicious AP can obtain
its authenticity and integrity using cryptographic accelerators,     via the shared memory bus secret data or high-privilege
detecting any tampering with the certified images in NVM,            resources. It can also manipulate memory content and
and (iv) Executing the image to load the next firmware stage.        overwrite (parts of) the bootloader to be executed to take
This authentication process propagates through all subsequent        control of the system already at the boot stage.
layers until the OS kernel is loaded. The BSP then broadcasts (b) Man-in-the-middle attack: The attacker implants an extra
an IPI with the address for the next execution via its built-in      interposer chip snooping on the IPI channel for inter-
local advanced programmable interrupt controllers (LAPIC).           processor communications. The chip can sabotage traffic
The AP, which monitors the IPI channel, is activated and runs        along the IPI channel by, e.g., substituting the memory
the OS kernel with the same privileges as the BSP. Variants of       entry pointer encoded in the activation IPI from BSP to
the typical multiprocessor architecture in Fig. 1 may include,       AP, leading to control-flow hijacking and arbitrary code
e.g., different inter-processor communication methods.               executions; moreover, it can sniff the IPI channel to capture
   However, in the context of secure boot, as identified in our      secret data or interfere with runtime inter-processor com-
threat model below, an attacker with access to the hardware          munications concerning, e.g., remote TLB shootdowns.
supply chain may bypass secure boot by exploiting either a
compromised AP or an additional chip sabotaging the IPI Assumptions. We make the following assumptions: (i) The
channel and thus taking control of the target system.            BSP is trusted. Its authenticity is ensured by the onboard
                                                                 baseboard management controller (BMC) before our protocol
              III. OVERVIEW OF O UR A PPROACH                    executes. (ii) The on-chip bootROM is designed to be im-
                                                                 mutable [27], [30] and cannot be modified by an attacker, as
   This section identifies our threat model exhibiting the new
                                                                 modifying it after manufacture is exceptionally difficult [31]
attack surface in multiprocessor secure boot as hardware
                                                                 (see Sect. VIII for potential extension of our approach against
supply-chain attacks, and outlines our defense approach.
                                                                 very powerful attackers able to tampering with the bootROM).
                                                                 While the bootROM inside the AP remains immutable after
A. Threat Model                                                  manufacturing, as discussed in (a), attackers can more feasibly
   In our threat model, we trust the CPU chip manufacturer create a malicious AP by pre-installing malware during chip
(e.g., Qualcomm), PCB board manufacturer, and device OEM production. Later, in the post-manufacturing supply chain,
(e.g., Apple). In other words, the design and fabrication they can replace the genuine AP plugged on device with the
process of original CPU chips and boards are trusted, since malicious one. (iii) Even if an attacker introduces a malicious
they come from reliable hardware supply chains controlled by AP, they cannot extract or replicate the genuine AP’s on-chip
the OEM. The OEMs can also take measures for tampering private key. While advanced physical attacks using techniques
4                                                                           IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. XX, NO. X



                             Threat model      § III-A



                     PA-Boot                        § IV                     Formalization and verification in Isabelle/HOL

                            initiation phase                                       high-level    § V-A refined to            low-level     § V-B
                        [certificates validation]             protocol          specification Sh                          specification Sl
                                                           adv. behaviors                satisfies                                 satisfies
                       challenge-response phase                                    high-level    § VI-A   refined to          low-level       § VI-B
                      [AP authn. & channel encr.]                                  properties                                 properties         ✓

                                     instantiate                                                                extract

                                  Evaluation of CPA-Boot (implementation in C) in terms of security and performance                   § VII


     Fig. 3: The workflow of our approach. ✓ indicates verified properties encoding security and functional correctness.
like scanning electron microscopy (SEM) could theoretically                                               TABLE I: Frequently used notations.
target on-chip data, they are impractical due to their high
                                                                                                     Notation                  Intuitive meaning
demand for knowledge, time and equipment [32]. Modern
hardware protections mitigate these risks by binding the key                             Certroot /CertBSP /CertAP             certificate of root/BSP/AP, resp.
to hardware identities [1] or intrinsic physical properties                                  RootCertHash                      hash value of Certroot
rather than storing it statically. For example, techniques like                           ⟨PubKBSP , PrivKBSP ⟩                public-private key pair of BSP
Physically Unclonable Functions (PUFs) [33] regenerate keys                                ⟨PubKAP , PrivKAP ⟩                 public-private key pair of AP
at runtime using unique physical characteristics. (iv) Crypto-                                  NAP /NBSP                      nonce generated by AP/BSP, resp.
graphic accelerators, like those used for elliptic-curve cryp-                          ⟨EPubKBSP , EPrivKBSP ⟩
                                                                                                                               ephemeral public-private key pair
tography (ECC) and SHA-256 integrity checks, are trusted.                                                                      generated by BSP for Ks
   Note that hardware replacement/modification is a strong                                                                     ephemeral public-private key pair
                                                                                         ⟨EPubKAP , EPrivKAP ⟩
                                                                                                                               generated by AP for Ks
attack model, the adversary can physically tamper with all
                                                                                                                               shared session key for the secure
components on the device. Uniquely in our case, we only focus
                                                                                                       Ks                      channel eventually established be-
on the two new novel attack vectors. For instance, we do not                                                                   tween BSP and AP
consider physical attacks such as cold boot attacks or snooping
attacks of the shared memory bus, given that such attacks                             refinement (e.g., [36], [37]). The high-level specification Sh
have been studied and mitigated as in prior studies [34], [35].                       provides a simple system behavior description, while the low-
Physical attacks other than internal hardware replacement,                            level specification Sl , closer to implementation, details all
such as side-channel attacks are out of our scope.                                    possible protocol executions and attacker interactions. We
                                                                                      verify security properties and functional correctness using Sl ,
B. Workflow of Our Approach                                                           as it captures specific protocol configurations and execution
                                                                                      traces. Sh helps to gain confidence in the correctness of the
   Fig. 3 sketches the overall workflow of our approach. To
                                                                                      system’s specification and its alignment with expectations. Its
defend against the hardware supply-chain attacks (a) and (b)
                                                                                      abstract, declarative nature reduces specification errors and
identified in our threat model, we develop the processor-
                                                                                      facilitates their discovery. The refinement proof between Sl
authentication protocol PA-Boot, which orchestrates the se-
                                                                                      and Sh further extends that confidence to Sl .
cure boot process via an initiation phase to validate the
processor certificates and a challenge-response phase to au-
thenticate the AP identity and to secure the inter-processor                                                     IV. D ESIGN OF PA-B OOT
communication channel. We then formalize it and the possible                             This section details the design of our processor authenti-
(adversarial and normal) behaviors thereof in Isabelle/HOL as                         cation protocol PA-Boot. It augments multiprocessor secure
a high-level specification Sh and a set of high-level properties                      boot with several key components as depicted in Fig. 2.
(encoding security and functional correctness). These high-                           PA-Boot steers the secure boot process in a certificate-based,
level ingredients – capturing the core components of PA-Boot                          two-phase manner: The processor certificates are validated in
– are further refined into their low-level counterparts, i.e., the                    the initiation phase and thereafter, in the challenge-response
low-level specification Sl and a set of low-level properties. We                      phase, the AP identity is authenticated and the inter-processor
then conduct a fully mechanized proof via theorem proving                             communication channel is encrypted. We first explain the
that Sl satisfies the low-level properties. Finally, we derive                        necessary operations to set up the stage for running PA-Boot
an implementation of PA-Boot from the formalized model as                             and then elucidate key message flows in the abovementioned
CPA-Boot based on a code-to-spec review [36]. We show that                            two phases. Frequently used notations are collected in Table I.
CPA-Boot effectively identifies various boot-process attacks                             Our protocol requires each processor to request its certificate
with a considerably minor overhead and thereby improves the                           from the certificate authority (CA) at the OEMs and store the
security of multiprocessor systems.                                                   signed certificate once issued. More concretely, the OEM first
   Separating a protocol’s formalization into high- and low-                          generates authorized certificates CertBSP and CertAP respec-
level specifications is a common strategy for abstraction and                         tively by signing PubKBSP and PubKAP with its own private
PA-BOOT: A FORMALLY VERIFIED AUTHENTICATION PROTOCOL FOR MULTIPROCESSOR SECURE BOOT UNDER HARDWARE SUPPLY-CHAIN ATTACKS                                                                                        5



                                                                                                                   (a)                        checking whether RootCertHash = Hash (Certroot ). If this
          BSP                                                                                                                AP               is indeed the case, then Certroot is used to validate the
                                                                                                                                              certificate of the other processor by applying the function
                 RootCertHash
                                                                                                      (a)
                                                                                                            RootCertHash
                                                                                                                                              validCert (Certroot , ·), which further reveals the public key of
                                            bootROM                               bootROM                                                     the other processor. The non-volatile memory (NVM) is easily
                                                                                                                                              modifiable, giving the attacker the ability to alter its contents.
                   Certroot , Cert BSP , Cert AP                                       Certroot , Cert BSP , Cert AP 
                                                                NVM                                                                           The attacker could replace legitimate certificates with those
                                                                                                                                              associated with a malicious AP, thereby attempting to deceive
     verify hash value
     of root certificate                     RootCertHash ? Hash  Certroot 
                                                                                                                     verify hash value
                                                                                                                     of root certificate
                                                                                                                                              PA-Boot. However, since the forged certificate is not signed
                                                                                                                                              by a trusted certificate authority (CA), the system can detect
                                                   validCert  Certroot , Cert AP 
                                                                                                                                              its invalidity during the certificate validation process.
  validate AP certificate,                                                                                        validate BSP certificate,
    get AP's public key                                                                                            get BSP's public key
                                                   validCert  Cert root , Cert BSP 
   PubK AP                                                                                                                        PubK BSP
                                                                                                                                              B. The Challenge-Response Phase
                                    integrity guarantee of certificates in NVM
                                                                                                                                                 As depicted in (the lower part of) Fig. 4, once confirming
                                                                                                                                              the validity of CertBSP in the initiation phase, the AP sends –
                                                                                                                         generate nonce
                                                                                                                                              via the inter-processor communication channel – a challenge
                                                        challenge packet                                    (b)                    AP
                                                                                                                                              packet (NAP )PubKBSP , that is, a randomly generated nonce NAP
                                                              AP  PubK   BSP                                                               encrypted with PubKBSP . Note that a typical nonce is a 32-byte
     decrypt packet,
   generate ephemeral
   key pair and nonce
                                                                                                                                              random number which is practically infeasible to guess. Upon
      BSP                                                                                                                                    receiving this packet, the BSP decrypts the packet via PrivKBSP
 EPubK BSP
                                                  challenge-response packet                                 (b)                               to get NAP and then sends a challenge-response packet
EPrivK BSP

                                   ,AP     BSP   , Hash  EPubK BSP   PubK , EPubK BSP
                                                                                         AP
                                                                                                                                                    (NAP , NBSP , Hash (EPubKBSP ))PubKAP , EPubKBSP
                                                                                                                   decrypt packet, check
                                                                                                                      nonce, generate         where NAP is the challenge nonce generated by AP, NBSP is
                                                                                                                    ephemeral key pair

                                                                                                                                  EPrivK AP
                                                                                                                                              the response nonce generated by BSP, and EPubKBSP is the
                                                                                                            (b)
                                                         response packet                                                          EPubK AP    ephemeral public key generated by BSP (for computing the
                                          BSP   , Hash  EPubK AP   PubK
                                                                                   BSP
                                                                                         , EPubK AP                                           shared session key Ks later); this challenge-response packet
                                                                                                                                              is encrypted by PubKAP except for the EPubKBSP part. After
     decrypt packet,
      check nonce                                                                                                                             receiving the challenge-response packet, the AP first decrypts
                                         successful processor authentication
                                                                                                                                              the packet and checks its integrity, i.e., checking whether the
                                                                                                                                              received NAP is identical to the previously generated one and
                                        s  CalcSessK  EPubK AP , EPrivK BSP                                          compute shared       whether the decoded Hash (EPubKBSP ) is identical to the hash
     compute shared
       session key                                                                                                         session key
                                        s  CalcSessK  EPubK BSP , EPrivK AP 
                                                                                                                                              value of the received EPubKBSP . If this is indeed the case,
         s                                                                                                                      s
                               inter-processor communication channel secured
                                                                                                                                              the AP stores EPubKBSP and generates its ephemeral key pair
                                                                                                                                              ⟨EPubKAP , EPrivKAP ⟩. Then, analogously, the AP responds to
                                                                                                                                              the BSP with a response packet
Fig. 4: Key message flows in PA-Boot.           marks potential
                                                                                                                                                       (NBSP , Hash (EPubKAP ))PubKBSP , EPubKAP       .
vulnerabilities to adversarial behaviors (a) and (b).
                                                                                                                                              The BSP then decrypts the packet and checks its integrity by
key (these certificates thus can be validated by the OEM’s
                                                                                                                                              similar means as mentioned above.
public key in Certroot ), and then stores all necessary certificates
⟨Certroot , CertBSP , CertAP ⟩ in the NVM. Meanwhile, the hash                                                                                   These message flows by now in the challenge-response
value of the root certificate Certroot is stored in the bootROM                                                                               phase are able to detect the aforementioned attack vector
of the processors. Recall that any attacker that can compromise                                                                               (a), i.e., AP replacements, and (b) man-in-the middle attacks
the BSP’s bootROM is beyond the scope of this paper.                                                                                          attempting to sabotage the communication packets. To protect
                                                                                                                                              the communication channel from future interference, PA-Boot
Remark. PA-Boot is not tailored to dual-processor devices,                                                                                    further produces a shared session key Ks such that subsequent
rather, it applies to the setting of multiple APs where the BSP                                                                               inter-processor communications can be secured using Ks . This
can authenticate these APs in sequence.                       ◁                                                                               concludes the entire challenge-response phase of PA-Boot.
                                                                                                                                              We remark that the (symmetric) shared session key Ks can
A. The Initiation Phase                                                                                                                       be calculated by BSP (resp. AP) based on EPubKAP and
                                                                                                                                              EPrivKBSP (resp. EPubKBSP and EPrivKAP ) using the Diffie-
   The two processors BSP and AP behave symmetrically                                                                                         Hellman (DH) key exchange algorithm [38].
in the initiation phase: As depicted in (the upper part of)
Fig. 4, each processor first reads the precomputed hash value
RootCertHash of Certroot from its bootROM as well as the                                                                                                V. F ORMALIZATION IN I SABELLE /HOL
chain of certificates ⟨Certroot , CertBSP , CertAP ⟩ from the NVM.                                                                              This section presents the formalization of PA-Boot in the
It then checks the validity and integrity of Certroot , namely,                                                                               theorem prover Isabelle/HOL [23]. The formal model consists
6                                                               IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. XX, NO. X



of a high-level specification Sh and a refined low-level specifi-                      TABLE II: The set Λ of events in Sl .
cation Sl . Sh captures core components of PA-Boot and gives
                                                                          ID      Name             Description of the event
the simplest description of the system behavior, whereas Sl is a
symbolic model closer to the implementation layer, encoding a             Processor behaviors (executed by BSP or AP)
more fine-grained characterization of all possible executions of           1      Read ROM         read RootCertHash in bootROM
the system. We opt for deductive verification as implemented               2      Read NVM         read ⟨Certroot , CertBSP , CertAP ⟩ in NVM
in Isabelle/HOL due to its scalability and inherent support of             3      Verify RCHash    verify if RootCertHash = Hash (Certroot )
abstraction refinement [39] and code generation [40].                      4      Verify Cert      verify the other processor’s cert. via Certroot
                                                                           5      Gen Nonce        generate a fresh nonce
Adversary model. For the adversarial behavior (a) identified
                                                                           6      Send Packet      send a packet to the channel
in Sect. III-A, we consider the possibility that the agent AP is
                                                                           7      Receive Packet   receive a packet via the channel
compromised, allowing the compromised agent to manipulate                  8      Parse Packet     decrypt a packet and check its integrity
its long-term keys. For the adversarial behavior (b) identified            9      Gen EpheKey      generate ephemeral public-private key pair
in Sect. III-A, we explicitly model a classical Dolev-Yao-style            10     Gen SessKey      calculate Ks to secure the comm. channel
adversary [41] who has full control over the insecure BSP-AP
communication channel. However, the adversary is limited by               Adversarial behavior (executed by the attacker)
the constraints of the cryptographic methods used: he cannot               11     Attack           perform a man-in-the-middle attack
forge signatures or decrypt messages without knowing the key
(the black box cryptography assumption).                                 for Γ(s). Let B ≜ {true, false}. We employ two indicator
                                                                         functions to witness the presence/absence of security threats:
                                                                         The (partial) benignity function B : C ⇀ B signifies whether
A. High-Level Specification                                              a security context c is benign (in the state that c is associated
   The high-level specification Sh of PA-Boot is encoded as a            with), i.e., whether the AP and the certificates in the NVM are
finite-state acyclic labelled transition system representing the         genuine; the free-of-attack function M : Π → B determines
protocol executions under certain security contexts:                     whether a man-in-the-middle attack has not occurred along a
Definition 1 (High-Level Specification of PA-Boot). The                  run of Sh , i.e., during one possible execution of the protocol.
high-level specification of PA-Boot is a quintuple                          Sh together with, e.g., its indicator functions are formalized
                                                                         as a locale module [39] in Isabelle/HOL – an emerging
                 Sh ≜ ⟨S, s0 , s̄, Λ, ∆⟩ ,     where                     mechanism for abstract reasoning – consisting of abstract types
                                                                         and primitive operations that can be interpreted in different
    • S is a finite set of states encoding the protocol configura-
                                                                         contexts. We omit the detailed locale formulation here.
      tions,
    • s0 ∈ S is the initial state,
    • s̄ ∈ S is the ideal state signifying attack-free authentica-
                                                                         B. Low-Level Specification
      tion,
    • Λ is a finite set of event labels representing actions of the         Next, we refine Sh of PA-Boot to its low-level counterpart
      processors and the attacker, and                                   Sl by instantiating the state space as concrete protocol config-
    • ∆ ⊆ S × Λ × S is a finite set of labelled transitions.             urations and the labelled transitions as event-triggered actions
                                                                   α     of the processors or the attacker. The fact that Sl refines Sh ,
    A labelled transition δ = (s, α, s′ ) ∈ ∆, denoted by s −       →    written as Sh ⊑ Sl , is proved in Isabelle/HOL by interpreting
  ′
s , yields a jump from the source state s to the target state            locales as parametric theory modules [39].
s′ on the occurrence of event α. We consider deterministic                  A state in Sl is encoded as a record construct in Is-
                           α         α
transitions, i.e., if s −  → s′ , s −
                                    → s′′ are both transitions in        abelle/HOL collecting all fields related to the protocol con-
∆, then s′ = s′′ . The set of terminal states is defined as              figuration:
S ↓ ≜ {s ∈ S | ∀α ∈ Λ.∄s′ ∈ S : s ̸= s′ ∧(s, α, s′ ) ∈ ∆}, i.e, a
state s is terminal iff s has no successors other than itself. Note            record State = { bsp :: Processor, ap :: Processor,
that the ideal state s̄ is necessarily a terminal state in S ↓ . A run                          env :: Envir, status :: Status } .
                             A
π of Sh , denoted by s0 ,−   → sn with A = α1 α2 · · · αn ∈ Λ∗ , is
                              α1      α2         αn                      Specifically, Processor encapsulates all the BSP/AP-related
a finite sequence π = s0 −→       s1 −→   · · · −−→ sn with sn ∈ S ↓ ,
       αi                                                                ingredients in PA-Boot (cf. Fig. 4); Envir encodes the environ-
si−1 −→ si ∈ ∆ for any 1 ≤ i ≤ n. We denote by Π the set
                                                         A               ment of the processors, i.e., the NVM storing certificates and
of all possible runs of Sh . Given a run π = s0 ,−       → sn ∈ Π,
                                                                         the inter-processor channel carrying communication packets;
Tail (π) denotes the tail state sn of π.
                                                                         Status signifies the current status of PA-Boot, which can be
Security contexts and indicator functions. Every state                   INIT (initialization), OK (normal execution), ERR (failure in
s ∈ S of Sh encodes, amongst others, the current security con-           certificate validation or packet parsing), ATTK (presence of
text c ∈ C consisting of security-related system configurations          man-in-the middle attacks), END (normal termination), and
of the underlying security assets, including the two processors,         ABORT (abnormal termination). In particular, a man-in-the
the NVM, and the inter-processor communication channel. We               middle attack will be recognized by PA-Boot when parsing
apply the function Γ : S → C to extract the security context             the attacked communication packet and thus leads to an ERR
pertaining to a state; for simplicity, we write Γs as shorthand          state; moreover, once a run visits an ERR state, it raises an
                                    6
       PA-BOOT: A FORMALLY VERIFIED AUTHENTICATION                       IEEE TRANSACTIONS
                                                   PROTOCOL FOR MULTIPROCESSOR             ON DEPENDABLE
                                                                                 SECURE BOOT             AND SECURE
                                                                                               UNDER HARDWARE       COMPUTING, VOL.
                                                                                                                  SUPPLY-CHAIN      XX, NO. X, MONTH
                                                                                                                                 ATTACKS         7 2022
         6                                                                       6                              6                                    IEEEAND
                                                                                                                        IEEE TRANSACTIONS ON DEPENDABLE   TRANSACTIONS
                                                                                                                                                             SECURE
                                                                                                                                                                  IEEE  ON DEPENDABLE
                                                                                                                                                                    COMPUTING,
                                                                                                                                                                       TRANSACTIONS  ONAND
                                                                                                                                                                               VOL. XX, NO. SECURE
                                                                                                                                                                                         TABLE
                                                                                                                                                                                        DEPENDABLE
                                                                                                                                                                                            X, MONTH  2022    Λ of
                                                                                                                                                                                                  2: COMPUTING,
                                                                                                                                                                                                     The
                                                                                                                                                                                                      ANDset
                                                                                                                                                                                                           SECUREVOL.      inX,SVOL.
                                                                                                                                                                                                                      XX, NO.
                                                                                                                                                                                                                   events
                                                                                                                                                                                                                   COMPUTING,   MONTH
                                                                                                                                                                                                                                l.   XX,2022
                                                                                                                                                                                                                                         NO. X, MONTH 202
6                                                                                                      6       IEEE TRANSACTIONS ON DEPENDABLE AND SECURE
                                                                                                                                                TABLE   IEEE
                                                                                                                                                        2: The set Λ of
                                                                                                                                                           COMPUTING,
                                                                                                                                                             TRANSACTIONS
                                                                                                                                                                      VOL. XX, TABLE
                                                                                                                                                                            ONNO.
                                                                                                                                                                        events       l . 2: The
                                                                                                                                                                                inX,SMONTH
                                                                                                                                                                               DEPENDABLE    2022
                                                                                                                                                                                             AND set Λ of
                                                                                                                                                                                                  SECURE
                                                                                                                                                                                               TABLE      events  Λ Sof
                                                                                                                                                                                                              setin
                                                                                                                                                                                                       2: COMPUTING,
                                                                                                                                                                                                          The         l . events
                                                                                                                                                                                                                      VOL.       inX,SMONTH
                                                                                                                                                                                                                            XX, NO.   l.    2022
                                                                              record Processor = {                                                                                       record Envir = {
                                                                       READ_NVM_OK                                                                                                          TABLE                 2: The set                  Λ of events            ID inName         Sl .
                                                                                                                                                                                                                                                                              SEND_RESP_OK                        TABLE        Description
                                                                                                                                                                                                                                                                                                                                      2: The set           ofΛ   the ofevent
                                                                                                                                                                                                                                                                                                                                                                           events in Sl .
          record Processor = {                                       record             Processor
                                                                                     record
                                                                                   root                   Envir
                                                                                                      record
                                                                                                     cert            =hash      {= ?{:: RCHash
                                                                                                                               Processor                        = {ID       , record    Name    nvm Envir ?
                                                                                                                                                                                                              ::record= {, Description
                                                                                                                                                                                                                    Certs               Envir =             ID {of         Name
                                                                                                                                                                                                                                                                          the      event       ID             Name    Description                 ofBSP the or  event
                                                                                                                                                                                                                                                                                                                                                       Description              of the event
                                                ③;④                                                            ③;④                                                                                                                                                Processor               behaviors               (executed               by                     AP)
                                                                                                                            ?                                                                    ?                                                              ⑪                                                    ⑦
  recordroot    Processor cert =hash       { ? :: RCHash,root                recordprivate      Envir
                                                                                           record
                                                                                          cert
                                                                                           nvm        ? hash
                                                                                                           ::rootkey= {cert
                                                                                                                  Processor
                                                                                                                  Certs                  PrivKey
                                                                                                                                  ::, RCHash        =hash      {ID, ? :: Name        nvmchannel
                                                                                                                                                                                RCHash              ,::record
                                                                                                                                                                                                          Certs,nvm       ::Description
                                                                                                                                                                                                                                Packet
                                                                                                                                                                                                                              Envir ?
                                                                                                                                                                                                                                         :: Certs=} {ofProcessor
                                                                                                                                                                                                                                                            ,BSP the or   event      ID
                                                                                                                                                                                                                                                                                    behaviors       Name     (executed             by      BSPDescription
                                                                                                                                                                                                                                                                                                                                                     or     AP)         ofBSPthe or  event
                                                                                                                 ?                      ::hash                             Processor              behaviors                 (executed                by                  1     AP)   Read           ROM
                                                                                                                                                                                                                                                                                               Processor              behaviorsread        RootCertHash
                                                                                                                                                                                                                                                                                                                                              (executed             by  in  bootROM     AP)
       root  private
                  cert hash     key? B_CERTS_ERRPrivKey,
                                            :: RCHash                      private packet
                                                                                  nvm      ? key
                                                                                           channel
                                                                                                ::rootCertsbuffer
                                                                                                            private  ::::PrivKey
                                                                                                                     ,
                                                                                                                    cert       Packet         Packet
                                                                                                                                              key    }, ? ::, RCHash  PrivKey        channel
                                                                                                                                                                                         ,                     :: Packet
                                                                                                                                                                                                              nvm        ?
                                                                                                                                                                                                                         channel
                                                                                                                                                                                                                               ::       } , :: Packet }
                                                                                                                                                                                                                                    Certs                                                 ⑦                        RECEIVE_RESP_
                                                                                   cert              chain        B_CERTS_OK
                                                                                                                          ::     Certs            ,             Processor    1           datatype
                                                                                                                                                                                       behaviors
                                                                                                                                                                                        Read            ROM          Status
                                                                                                                                                                                                                 (executed            read=
                                                                                                                                                                                                                                          RESP_ATTK
                                                                                                                                                                                                                                          by       {
                                                                                                                                                                                                                                                   BSP
                                                                                                                                                                                                                                                  RootCertHashor
                                                                                                                                                                                                                                                               1 AP)     2Read   in  Read ROM
                                                                                                                                                                                                                                                                                     Processor
                                                                                                                                                                                                                                                                                        bootROM  1  NVM     behaviors
                                                                                                                                                                                                                                                                                                              Read    readROM  read
                                                                                                                                                                                                                                                                                                                               OK          hCertroot
                                                                                                                                                                                                                                                                                                                                RootCertHash
                                                                                                                                                                                                                                                                                                                                    (executed              , Cert
                                                                                                                                                                                                                                                                                                                                                          by
                                                                                                                                                                                                                                                                                                                                                       read   in  BSP BSP ,or
                                                                                                                                                                                                                                                                                                                                                                    bootROM
                                                                                                                                                                                                                                                                                                                                                                 RootCertHashCertAP) AP i in
                                                                                                                                                                                                                                                                                                                                                                                           in bootROM
                                                                                                                                                                                                                                                                                                                                                                                                NVM
             packet
       private            key   ?
                              buffer:: PrivKey :: Packet, ,                packet channel        buffer
                                                                                                  private  ::packet
                                                                                                                  Packet         Packet
                                                                                                                                 key          ?
                                                                                                                                         }buffer    ::, PrivKey      :: Packet  , ,                           channel :: Packet2 } 3ReadVerify                                                        RCHash                   verify         if ,RootCertHash                              (Certroot )
             cert         chain       ::   Certs     ,                     cert      datatype
                                                                                   ③;④
                                                                                   local  chain nonce      ::
                                                                                                            cert   Status
                                                                                                                    Certs      ::chainNonce
                                                                                                                                      ,    =          { ,
                                                                                                                                                       ③;④
                                                                                                                                                        ::         1,2Read
                                                                                                                                                               Certs
                                                                                                                                                                                 datatype
                                                                                                                                                                                        ReadROM INIT    NVMStatus |
                                                                                                                                                                                                                  datatype read = read  { Status  hCertroot=
                                                                                                                                                                                                                                       RootCertHash                 , Cert
                                                                                                                                                                                                                                                                        in {  bootROM     NVM
                                                                                                                                                                                                                                                                               BSP ,1Cert2⑧       AP   iin
                                                                                                                                                                                                                                                                                                    Read    Read
                                                                                                                                                                                                                                                                                                                NVM
                                                                                                                                                                                                                                                                                                                 ROM  readNVM   hCertroot     read Cert
                                                                                                                                                                                                                                                                                                                                                   ⑧    
                                                                                                                                                                                                                                                                                                                                                       read BSPh,Cert
                                                                                                                                                                                                                                                                                                                                                        RootCertHash Certroot
                                                                                                                                                                                                                                                                                                                                                                            AP=,iCert
                                                                                                                                                                                                                                                                                                                                                                                   Hash
                                                                                                                                                                                                                                                                                                                                                                                    in bootROM
                                                                                                                                                                                                                                                                                                                                                                                   in   NVM
                                                                                                                                                                                                                                                                                                                                                                                         BSP , CertAP i in NVM
       packet buffer Packet,                                                                      packet buffer Packet,                                                                                                                                                  4Verify     VerifyRCHash     Cert            verify   verify         the other processor’s
                                                                                                                                                                                                                                                                                                                                    if RootCertHash                        Hash (Cert    cert.    via    Cert(root
             local          nonce         :: ,Nonce,                               remote
                                                                             datatype
                                                                           local             nonce
                                                                                           INIT            nonce
                                                                                                       Status   | ::chain
                                                                                                            local        Nonce=::nonce   {Nonce
                                                                                                                                            ,:: Certs        ,:: ,Nonce
                                                                                                                                                                   2         3Read
                                                                                                                                                                                  , INITVerify
                                                                                                                                                                                            NVM           OK |INIT
                                                                                                                                                                                                ok |datatype
                                                                                                                                                                                                          RCHash           readStatus verify
                                                                                                                                                                                                                                       hCert
                                                                                                                                                                                                                                           | root    if=       3
                                                                                                                                                                                                                                                         ,RootCertHash
                                                                                                                                                                                                                                                            Cert  { BSP     , Cert2AP     =      3Read
                                                                                                                                                                                                                                                                                             i Hash
                                                                                                                                                                                                                                                                                                 in   NVM     Cert
                                                                                                                                                                                                                                                                                                            (Verify
                                                                                                                                                                                                                                                                                                                 NVM  root )RCHash            readverifyhCertroot   if=,RootCertHash
                                                                                                                                                                                                                                                                                                                                                                          Cert               root=
                                                                                                                                                                                                                                                                                                                                                                                  BSP , CertAP
                                                                                                                                                                                                                                                                                                                                                                                                  ) i Hash
                                                                                                                                                                                                                                                                                                                                                                                                      in NVM      Certroot )
       cert       chain        :: Certs                                  A_CERTS_ERR
                                                                                                  cert                                A_CERTS_OK                                                                                                                         5Verify     Gen
                                                                                                                                                                                                                                                                                   RESP_ERR       Nonce                        generate  RESP_OK   a   fresh       nonce
                                                                                                                                           ::                                                                ERR                |                              4                           Cert                       verify        the      other       processor’s             cert.    via   Cert
                                                                                                                                                ,::EpheKey               ,, Verify
                                                ⑥                                  local                ephe                key
                                                                                                                      ::|nonce
                                                                                                                             Nonce                                           4          Verify   OK |INITok
                                                                                                                                                                                                err       Cert                        verify   ⑥     the       other        processor’s          4      cert. Verify
                                                                                                                                                                                                                                                                                                                  via     Cert
                                                                                                                                                                                                                                                                                                                            Cert                       verify       the     other      processor’s      rootcert.    ) Certroo
                                                                                                                                                                                                                                                                                                                                                                                                                 rootvia
       local remote  nonce    nonce
                                 :: Nonce   :: Nonce
                                                  ,          ,             remote INIT     oknonce  | OK
                                                                                                  local     remote                        nonce        Nonce     ::3 Nonce          ,ok RCHash                             verify | OKif RootCertHash
                                                                                                                                                                                                                                                   |                           = Hash  3
                                                                                                                                                                                                                                                                                     Send
                                                                                                                                                                                                                                                                                                    Certroot )RCHash
                                                                                                                                                                                                                                                                                                  (Verify                          root verify if RootCertHash = Hash (Cert

                                                 ::                        local   remote    ephe          ephe
                                                                                                         ERR    key           ::
                                                                                                                               |key  EpheKey   ::     EpheKey   ,  4    ::   5, Verify
                                                                                                                                                                                     errGen     attk
                                                                                                                                                                                                Cert Nonce
                                                                                                                                                                                                    ERR          ATTK|     verify      |
                                                                                                                                                                                                                                      generate
                                                                                                                                                                                                                                       ERRthe       other| a   5fresh    6Gen
                                                                                                                                                                                                                                                                  processor’snonce     Nonce
                                                                                                                                                                                                                                                                                       4         5Packet
                                                                                                                                                                                                                                                                                             cert.  Verify
                                                                                                                                                                                                                                                                                                         via  Gen
                                                                                                                                                                                                                                                                                                                Cert  generate
                                                                                                                                                                                                                                                                                                                   Cert  Nonce sendaafresh      packet
                                                                                                                                                                                                                                                                                                                                              verify       the
                                                                                                                                                                                                                                                                                                                                                              to theachannel
                                                                                                                                                                                                                                                                                                                                                          nonce
                                                                                                                                                                                                                                                                                                                                                       generate    other     fresh     nonce
                                                                                                                                                                                                                                                                                                                                                                               processor’s          cert.    via    Cert
       remotelocal     nonceephe:: key  Nonce,EpheKey,⑥ ok OKremote                        err            |local             nonce    ephe:: key           Nonce,EpheKey,                                     ok OK |    err                                                 ⑥
                                                                                                                                                                                                                                                                         7 the Receive                   Packet
                                                                                                                                                                                                                                                                                                                         root
                                                                                                                                                                                                                                                                                                                               receive          a⑩  packet         via    the channel
                                                                                                                                                                                                                                                                                                                                                                                                                         root

       local remote  epheephe   key ::key           :: EpheKey
                                              EpheKey          ,          ,remote  session
                                                                                  err      attk  ephe
                                                                                               ERRlocal      ATTKkey
                                                                                                            remote|key   ephe  ::::SessKey
                                                                                                                                        |EpheKey
                                                                                                                                          ephekey ::key         }EpheKey
                                                                                                                                                                   5, ::6Gen
                                                                                                                                                                                       ,Send
                                                                                                                                                                                     attk
                                                                                                                                                                                EpheKey   Nonce END    Packet
                                                                                                                                                                                                      ,ATTK   err  | attk ABORT
                                                                                                                                                                                                                             |ERR
                                                                                                                                                                                                                           generate   sendATTK | a}afresh
                                                                                                                                                                                                                                                       packet    | toSend
                                                                                                                                                                                                                                                               6 nonce                 5Packet
                                                                                                                                                                                                                                                                                       channel   6Gen         Send
                                                                                                                                                                                                                                                                                                               Nonce  sendPacket a packet            to
                                                                                                                                                                                                                                                                                                                                              generate    theaachannel
                                                                                                                                                                                                                                                                                                                                                       send           packet
                                                                                                                                                                                                                                                                                                                                                                    fresh          to the channel
                                                                                                                                                                                                                                                                                                                                                                               nonce
                                                                                                                 |:: SessKey                        } ::::SessKey                      }Receive          | Packet                      }aingre-
                                                                                                                                                                                                                                      receive                  7 the8Receive via Parse              Packet
                                                                                                                                                                                                                                                                                               Packet                 receive  decrypta packet    a packet
                                                                                                                                                                                                                                                                                                                                                         avia
                                                                                                                                                                                                                                                                                                                                                                    and
                                                                                                                                                                                                                                                                                                                                                                  the        checkvia
                                                                                                                                                                                                                                                                                                                                                                       a channel        its the
                                                                                                                                                                                                                                                                                                                                                                                              integrity
       remotesession   ephekey     key::::SessKey
                                               ABORT
                                                EpheKey         }, session  where attk     END       keysession
                                                                                                   ATTK
                                                                                             Processor
                                                                                                  remote                 ABORT
                                                                                                                            |ephekey
                                                                                                                          encapsulates            key             6 EpheKey 7
                                                                                                                                                                        all SendtheEND     ,Packet
                                                                                                                                                                                         BSP/AP-related        ABORT
                                                                                                                                                                                                              attk         send
                                                                                                                                                                                                                         END     ATTK       packet
                                                                                                                                                                                                                                            | ABORT   |a packet
                                                                                                                                                                                                                                                    ABORT     to          }channel    the
                                                                                                                                                                                                                                                                                       6 channel
                                                                                                                                                                                                                                                                                     Gen
                                                                                                                                                                                                                                                                                                 7Send        Receive
                                                                                                                                                                                                                                                                                                                 Packet         Packet        END receive
                                                                                                                                                                                                                                                                                                                                              send          packet        packet
                                                                                                                                                                                                                                                                                                                                                                           to the channel            channel
                                                                                                                                                                   7         8Receive   ParsePacket     Packet receive                decrypt a   packet       8 via9Parse
                                                                                                                                                                                                                                                         a packet          theand  channel
                                                                                                                                                                                                                                                                                       7  Packet
                                                                                                                                                                                                                                                                                         check   8EpheKey
                                                                                                                                                                                                                                                                                                       its Parse
                                                                                                                                                                                                                                                                                                    Receive           decrypt
                                                                                                                                                                                                                                                                                                              integrity        generate
                                                                                                                                                                                                                                                                                                                           Packet
                                                                                                                                                                                                                                                                                                                       Packet           a packet   ephemeral
                                                                                                                                                                                                                                                                                                                                              receive      and
                                                                                                                                                                                                                                                                                                                                                       decrypt
                                                                                                                                                                                                                                                                                                                                                             a   packet a public-private
                                                                                                                                                                                                                                                                                                                                                                     check packetits the
                                                                                                                                                                                                                                                                                                                                                                               via    integrity
                                                                                                                                                                                                                                                                                                                                                                                        and     check
                                                                                                                                                                                                                                                                                                                                                                                            channel
                                                                                                                                                                                                                                                                                                                                                                                                      keyits pair integrity
       session            key    ::   SessKey          }
        where Processor encapsulates all the BSP/AP-related        where    dientsEND
                                                                                   Processor in      |
                                                                                                  session  ABORT
                                                                                                       PA-Boot
                                                                                                             encapsulates
                                                                                                   where Processor               key    }
                                                                                                                                       (cf.ingre-::    SessKey
                                                                                                                                                     Fig.   all
                                                                                                                                                         encapsulates4);
                                                                                                                                                                      the      }
                                                                                                                                                                              Envir
                                                                                                                                                                                 BSP/AP-relatedencodes
                                                                                                                                                                                               allEpheKey     END       the
                                                                                                                                                                                                        the BSP/AP-related        |
                                                                                                                                                                                                                               ingre-    ABORT
                                                                                                                                                                                                                                     environ-                   }  ingre-
                                                                                                                                                                                                                                                                        10Gen Gen                 SessKey                      calculate            K
                                                                                                                                                                                        Gen                                           generate                 9
                                                                                                                                                                                                                                                           ephemeral                   EpheKey
                                                                                                                                                                                                                                                                                      public-private          Gen     generate
                                                                                                                                                                                                                                                                                                                       key
                                                                                                                                                                                                                                                                                                                         EpheKey
                                                                                                                                                                                                                                                                                                                               pair       ephemeral     s to secure           the
                                                                                                                                                                                                                                                                                                                                                                  public-private     comm.   key  channel
                                                                                                                                                                                                                                                                                                                                                                                                     pair
                                                      (i)    validating     ment        NVM
                                                                                          of      the       certificates
                                                                                                                processors,                             i.e.,                9
                                                                                                                                                                   8 the Parse   NVM          Packet
                                                                                                                                                                                                   storing                 decrypt a packet
                                                                                                                                                                                                                         certificates                  1(ii) and     attack   check    8on       9
                                                                                                                                                                                                                                                                                             itsthe Parse
                                                                                                                                                                                                                                                                                                    integrityresp.Packet    packet            decrypt a packet and check its integritykey pair
                                                                                                                                                                                                                                                                                                                                                       generate           ephemeral           public-private
where   dients       in PA-Boot
             Processor          encapsulates   (cf. Fig.    all 4);dients
                                                                   theEnvir         inwhere
                                                                             BSP/AP-related PA-Boot
                                                                                          encodes  dients   Processorthe  (cf.
                                                                                                                          in  ingre-     Fig.
                                                                                                                                     environ-
                                                                                                                                     PA-Boot            4); Envir
                                                                                                                                             encapsulates            (cf.10Fig.     encodes
                                                                                                                                                                                    allGen  4);       Envir
                                                                                                                                                                                             theSessKey      the encodes
                                                                                                                                                                                                         BSP/AP-related  environ- theingre-                   environ-     Gen         SessKey                        calculate            Kgenerate
                                                                                                                                                                                                                                                                                                                                               s to calculate
                                                                                                                                                            1 9 NVM             Gen       EpheKey                          generate   calculate
                                                                                                                                                                                                                                             1 ephemeral    K10 s to     secure
                                                                                                                                                                                                                                                                           public-private
                                                                                                                                                                                                                                                                                1 9
                                                                                                                                                                                                                                                                      Adversarial         the10comm.Gen key
                                                                                                                                                                                                                                                                                                    behavior  Gen  channel
                                                                                                                                                                                                                                                                                                               EpheKey   SessKey
                                                                                                                                                                                                                                                                                                                      pair
                                                                                                                                                                                                                                                                                                                         (executed              by secure             theKcomm.
                                                                                                                                                                                                                                                                                                                                                                 ephemeral
                                                                                                                                                                                                                                                                                                                                                       the attacker)         s to secure  channelthe comm.
                                                                                                                                                                                                                                                                                                                                                                                      public-private             keychannel
                                                                                                                                                                                                                                                                                                                                                                                                                        pair
dients  ment in5: ofPA-Boot
                        the processors,
                                      (cf.of    Fig.     i.e.,
                                                          4);state the and
                                                                   ment
                                                                  Envir      NVMof
                                                                                encodes the         inter-processor
                                                                                                    processors,
                                                                                                   ment
                                                                                              storing
                                                                                         dients              in of             the i.e.,
                                                                                                                       certificates
                                                                                                                        environ-             processors, channel
                                                                                                                                                         the                       carrying
                                                                                                                                                                                  i.e., storing
                                                                                                                                                                                            the NVM
                                                                                                                                                                                           Envir             communication
                                                                                                                                                                                                              certificates  storing    the Kcertificates
                                                                                                                                                                                                                                                   environ-
     Fig.              Snippets                      the                      machine               ? the  S      l
                                                                                                                        PA-Boot
                                                                                                                         of          PA-Boot.           (cf.      10
                                                                                                                                                                      Fig.  A     4);
                                                                                                                                                                                Gen state SessKey     s     encodes
                                                                                                                                                                                                            is      identified
                                                                                                                                                                                                                           calculate                   byto        its
                                                                                                                                                                                                                                                                secure       status
                                                                                                                                                                                                                                                                               the    10comm.     and
                                                                                                                                                                                                                                                                                                    Gen  channelcolored
                                                                                                                                                                                                                                                                                                               SessKey                    in      light
                                                                                                                                                                                                                                                                                                                                              calculate          K greento  secure  (normal
                                                                                                                                                                                                                                                                                                                                                                                         the    comm. channel
mentand                   inter-processor
           of the processors,                    i.e., channel     and
                                                           the NVMcarrying  packets;
                                                                               the        inter-processor
                                                                                         mentand
                                                                                    storing              marks
                                                                                                         communication
                                                                                                        ofcertificates
                                                                                                                  the processors,  fields     channel
                                                                                                                                               1
                                                                                                                                 inter-processor        that            cannot
                                                                                                                                                                          carrying
                                                                                                                                                                           Adversarial
                                                                                                                                                                        i.e., channel       be
                                                                                                                                                                                   the NVMcarrying    empty
                                                                                                                                                                                                    communication
                                                                                                                                                                                                        behavior          during
                                                                                                                                                                                                                               (executed
                                                                                                                                                                                                                 storing communication            the
                                                                                                                                                                                                                                        certificates
                                                                                                                                                                                                                                                      s Adversarial behavior (executed by the attacker)
                                                                                                                                                                                                                                                        by      the   1  attacker)
                                                                                                                                                                                                                                                                        11           Attack    Adversarial                     perform
                                                                                                                                                                                                                                                                                                                          behavior                a
                                                                                                                                                                                                                                                                                                                                                (executed            s
                                                                                                                                                                                                                                                                                                                                                       man-in-the-middle
                                                                                                                                                                                                                                                                                                                                                                       by   the             attack
                                                                                                                                                                                                                                                                                                                                                                                    attacker)
andtermination),                     redfields (abnormal                    termination),                                                                                                                                                                                                                                                asman-in-the-middle
                                                                                         ? executionor                          ? in               blue,               ;dark
        packets;         ?
          the inter-processormarks                 channelthat packets;
                                                                     cannot entire
                                                                       carrying         be
                                                                                         and   marks
                                                                                                  empty
                                                                                                   packets;
                                                                                               communication         fields
                                                                                                                         during
                                                                                                       the inter-processor      of         PA-Boot
                                                                                                                                            that
                                                                                                                                        marks       thecannot   fields
                                                                                                                                                                Adversarial Status
                                                                                                                                                                            11 that
                                                                                                                                                                          channel  begreen,
                                                                                                                                                                                        Attack signifies
                                                                                                                                                                                           emptycannot
                                                                                                                                                                                            behavior
                                                                                                                                                                                                  carrying    yellow,
                                                                                                                                                                                                               duringbethe
                                                                                                                                                                                                                    (executed  empty   the
                                                                                                                                                                                                                            communication orbyorange
                                                                                                                                                                                                                                      current
                                                                                                                                                                                                                                      perform       during
                                                                                                                                                                                                                                                     thea11    attacker)pthe if Adversarial
                                                                                                                                                                                                                                                                           Attack
                                                                                                                                                                                                                                                               man-in-the-middle     the 11transition                 perform
                                                                                                                                                                                                                                                                                                                 behavior
                                                                                                                                                                                                                                                                                                            attack
                                                                                                                                                                                                                                                                                                              Attack            to(executed     is perform
                                                                                                                                                                                                                                                                                                                                                        triggered
                                                                                                                                                                                                                                                                                                                                                             by thea attacker)     byattackBSP, attack
                                                                                                                                                                                                                                                                                                                                                                            man-in-the-middle
     AP,entire both         BSP
                  ? execution          and
packets; marks fields that cannot be empty of     AP,
                                                 PA-Boot     or    entire
                                                                    the
                                                                    ;       status
                                                                        Status     execution
                                                                               attacker,     of
                                                                                          signifies
                                                                                         packets;     PA-Boot
                                                                                                   entire   during of
                                                                                                            respectively;
                                                                                                                    ?the           ,
                                                                                                                              PA-Boot
                                                                                                                         execution
                                                                                                                            marks       which
                                                                                                                                       current
                                                                                                                                        the fields          ;   can
                                                                                                                                                               ofStatus
                                                                                                                                                                 The        be
                                                                                                                                                                        PA-Boot     INIT
                                                                                                                                                                                    signifies
                                                                                                                                                                                 (condensed)   ;    (initialization),
                                                                                                                                                                                                    Status    the          current
                                                                                                                                                                                                                         transition
                                                                                                                                                                                                                       signifies                 OKthe         current
                                                                                                                                                                                                                                                               p    ;    q   ;  .  .   . →       ⊤    ,   for        p,     q     ∈       {3,       4,     8}        (cf.       Table          II), attack
                                                                                                                                                                  11 that    pAttackcannot be empty                        perform        during                the
                                                                                                                                                                                                                                                 a man-in-the-middle                  11 pattack    Attack                                    perform a man-in-the-middle
                                                                   status   (normalofentire
                                                                                 INIT      PA-Boot  execution),      , of  which            ERR     can
                                                                                                                                                    OKPA-Boot  (failure
                                                                                                                                                                ,be        INITinStatus        certificate
                                                                                                                                                                                          (initialization),  INIT validation          OK                                  OK p ; q ; . . . → ⊥ is triggered.
     isstatus
entire     triggered of PA-Boot
             execution           ifof all   , which
                                         PA-Bootthe checks  ; canStatus be    insignifies
                                                                            or in
                                                                                     the
                                                                                   packet
                                                                                                (initialization),
                                                                                                   status
                                                                                                  event   the
                                                                                                            execution
                                                                                                        parsing),
                                                                                                                          current
                                                                                                                         sequence   PA-Boot
                                                                                                                                         ATTK
                                                                                                                                                  of               pwhich
                                                                                                                                                               (presence
                                                                                                                                                                        , q , .; .can     . are
                                                                                                                                                                                           of INIT
                                                                                                                                                                                                    be successful,
                                                                                                                                                                                                            signifies
                                                                                                                                                                                                    man-in-the
                                                                                                                                                                                                                              (initialization),
                                                                                                                                                                                                                                        the otherwise
                                                                                                                                                                                                                                      middle
                                                                                                                                                                                                                                                     current   q
                                                 ERR               (normal                execution),                          ERR                 (failure                 incancertificate                  invalidation
status  (normal
             of PA-Boot   execution),
                                    , which            can(failure
                                                                 be     INIT              certificate
                                                                                                   (normal
                                                                                      (initialization),
                                                                                         status             of PA-Boot      validation
                                                                                                                                 execution),
                                                                                                                                       OK           , which        q ERR              (failure
                                                                                                                                                                                         be                            certificate
                                                                                                                                                                                                                   (initialization),                   validation
                                                                                                                                                                                                                                                                OK                     q
                                                                                                                                                                                                                                                                               READ_NVM_OK

(normal or   packet         parsing),
                  execution),alarm              ATTK
                                          ERR (failure             or
                                                               (presence    attacks),
                                                                          packet
                                                                        in certificate  of         END
                                                                                             parsing),
                                                                                               man-in-the
                                                                                         (normal   or      packet   (normal
                                                                                                                validation  ATTK
                                                                                                                    execution),       parsing),
                                                                                                                                       middle     termination),
                                                                                                                                                   (presence  ERRABORTATTK        of    and
                                                                                                                                                                                         man-in-the
                                                                                                                                                                                      (presence
                                                                                                                                                                              (failure in before      ABORT         of
                                                                                                                                                                                                            certificate       (abnormal
                                                                                                                                                                                                                           middle
                                                                                                                                                                                                                              man-in-the    validation          middle                                                                                      SEND_RESP_OK

     error-specific                                     and attacks),
                                                                    terminates
                                                                            termination).END
                                                                                                       in
                                                                                                        (normal
                                                                                                                   the
                                                                                                                  In                 (unique)
                                                                                                                            particular,
                                                                                                                                      termination),             a     man-in-theand        ABORT
                                                                                                                                                                                          READ_NVM_OK middle      (abnormal attack the           launch
                                                                                                                                                                                                                                                will                      of PA-Boot,③;④ Property
                                                                                                                                                                                                                                                                         ③;④  
                                                                                                                                                                                                                                                                      READ_NVM_OK
                                                                                                                                                                                                                                                                                                   READ_NVM_OK
                                                                                                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                                                                                                    1 ensures that our
                                                                                                                                                                                                                                                                                                                                                    ⑪                          ⑦
        attacks),
or packet                END (normal
                     parsing),          ATTK termination),
                                                       (presence of and              man-in-the
                                                                                         or packetABORT
                                                                                                   attacks),                    END (normal
                                                                                                                            (abnormal
                                                                                                                         parsing),
                                                                                                                          middle                         ATTK termination),   (presence
                                                                                                                                                                                    ↓                     of      and
                                                                                                                                                                                                                  man-in-the    ABORT                 (abnormal
                                                                                                                                                                                                                                                     middle         SEND_RESP_OK
                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                              SEND_RESP_OK
                                                                                                                                                                                                                                                                                                                                                                                SEND_RESP_OK

     state.        In
        termination).
attacks),
                          fact,
                 END (normal
                                    END
                                 In particular,   and
                                              termination),
                                                             ABORT          be
                                                                a termination).
                                                                    man-in-the      represent
                                                                                   recognized
                                                                            and ABORT    attacks),     In (abnormal
                                                                                                  middle
                                                                                                   termination).   END
                                                                                                                      terminal
                                                                                                                     by
                                                                                                                particular,
                                                                                                                          attackPA-Boot(normal  In       states when
                                                                                                                                                    a particular,
                                                                                                                                                  will     man-in-the
                                                                                                                                                                  termination),
                                                                                                                                                                               S
                                                                                                                                                                              ③;④  
                                                                                                                                                                                 parsing as
                                                                                                                                                                                        amiddle
                                                                                                                                                                                 READ_NVM_OK
                                                                                                                                                                                              man-in-the  protocol
                                                                                                                                                                                                        the
                                                                                                                                                                                                        and
                                                                                                                                                                                                                     ③;④
                                                                                                                                                                                                                 attacked
                                                                                                                                                                                                                 attack
                                                                                                                                                                                                                    ABORT
                                                                                                                                                                                                                               
                                                                                                                                                                                                                                     will
                                                                                                                                                                                                                                middle   per
                                                                                                                                                                                                                                           com-
                                                                                                                                                                                                                                           (abnormal
                                                                                                                                                                                                                                                        se B_CERTS_ERR


                                                                                                                                                                                                                                                     attack will
                                                                                                                                                                                                                                                                ③;④
                                                                                                                                                                                                                                                                  ⑪does
                                                                                                                                                                                                                                                           SEND_RESP_OK    ⑥
                                                                                                                                                                                                                                                                                     not    ⑦
                                                                                                                                                                                                                                                                                                 B_CERTS_OK

                                                                                                                                                                                                                                                                                                     ④
                                                                                                                                                                                                                                                                                                      ③;④
                                                                                                                                                                                                                                                                                                  alter
                                                                                                                                                                                                                                                                                                  ③;④  
                                                                                                                                                                                                                                                                                            READ_NVM_OK          the        benignity
                                                                                                                                                                                                                                                                                                                                 ④   
                                                                                                                                                                                                                                                                                                                                       ③;④  
                                                                                                                                                                                                                                                                                                                                        RESP_ATTK
                                                                                                                                                                                                                                                                                                                                         ⑪                     of the security
                                                                                                                                                                                                                                                                                                                                                                  ⑦
                                                                                                                                                                                                                                                                                                                                                                   ⑦
                                                                                                                                                                                                                                                                                                                                                                  ⑧
                                                                                                                                                                                                                                                                                                                                                                             RECEIVE_RESP_
                                                                                                                                                                                                                                                                                                                                                                             ⑪
                                                                                                                                                                                                                                                                                                                                                                     SEND_RESP_OK
                                                                                                                                                                                                                                                                                                                                                                                  OK
                                                                                                                                                                                                                                                                                                                                                                                                ⑧
                                                                                                                                                                                                                                                                                                                                                                                                      ⑦
                                                                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                  B_CERTS_ERR                          B_CERTS_OK                                            ⑥          ⑦        RECEIVE_RESP_
                                                                                                                                                                                                          ③;④                                                                                                               ③;④  
     defined
        be  recognized  in
termination). In particular,  S  h  ,
                                   by  where
                                           PA-Boot      END    whenbe
                                                        a man-in-the middle munication
                                                                       particularly
                                                                          recognized
                                                                             parsing               be
                                                                                                   the
                                                                                         termination).   bypacket
                                                                                                             marks PA-Boot
                                                                                                           recognized
                                                                                                                attacked
                                                                                                             attack In               andthe
                                                                                                                                      will    com- thus
                                                                                                                                                   when
                                                                                                                                                    by ideal        ③;④  
                                                                                                                                                                  leads
                                                                                                                                                               PA-Boot parsing    to
                                                                                                                                                                          B_CERTS_ERR
                                                                                                                                                                           state       an s̄.
                                                                                                                                                                                       when
                                                                                                                                              particular, a⑥ man-in-the middle attack will  the ERR          state;
                                                                                                                                                                                                              B_CERTS_OK
                                                                                                                                                                                                          context
                                                                                                                                                                                                        attacked
                                                                                                                                                                                                         parsing
                                                                                                                                                                                                         ④     
                                                                                                                                                                                                                              moreover,
                                                                                                                                                                                                                                 the during
                                                                                                                                                                                                                                  com-  ④ attacked
                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                       ⑪      all
                                                                                                                                                                                                                                                      RESP_ATTK

                                                                                                                                                                                                                                                                 ⑥
                                                                                                                                                                                                                                                                        of
                                                                                                                                                                                                                                                                      com-
                                                                                                                                                                                                                                                                               ⑦
                                                                                                                                                                                                                                                                                ⑦its    ③;④  
                                                                                                                                                                                                                                                                                   B_CERTS_ERR
                                                                                                                                                                                                                                                                                A_CERT_ERR
                                                                                                                                                                                                                                                                               ⑧
                                                                                                                                                                                                                                                                                            possible
                                                                                                                                                                                                                                                                                        RECEIVE_RESP_
                                                                                                                                                                                                                                                                                           OK
                                                                                                                                                                                                                                                                                           ④    
                                                                                                                                                                                                                                                                                                   ⑥       ⑧
                                                                                                                                                                                                                                                                                                                      B_CERTS_OK
                                                                                                                                                                                                                                                                                                                        executions.
                                                                                                                                                                                                                                                                                                                        ④
                                                                                                                                                                                                                                                                                                                 A_CERT_OK④
                                                                                                                                                                                                                                                                                                                            RESP_ATTK
                                                                                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                                                                   ⑥
                                                                                                                                                                                                                                                                                                                                                        ④   
                                                                                                                                                                                                                                                                                                                                                              RESP_ATTK
                                                                                                                                                                                                                                                                                                                                                                ⑪
                                                                                                                                                                                                                                                                                                                                                        ⑧   RESP_ERR
                                                                                                                                                                                                                                                                                                                                                                       OK
                                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                                                                                                                  ⑦
                                                                                                                                                                                                                                                                                                                                                                                    ⑦
                                                                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                                      ⑧⑧
                                                                                                                                                                                                                                                                                                                                                                                                     RECEIVE_RESP_

                                                                                                                                                                                                                                                                                                                                                                                                   RESP_OK
                                                                                                                                                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                                                                                                          OK
                                                                                                                                                                                                                                                                                                                                                                                                                         ⑧   

        munication            packet         and and  thus       leads      once
                                                                   munication toareanbe   aERR  run
                                                                                                packet
                                                                                                   municationvisits
                                                                                                         state;       and          an thus     ERR    leads      state,
                                                                                                                                                                B_CERTS_ERR
                                                                                                                                                                              anit ERR
                                                                                                                                                                        to thus         raises     state;  an moreover,
                                                                                                                                                                                                     B_CERTS_OK
                                                                                                                                                                                                                    error-specific
                                                                                                                                                                                                                         ERR
                                                                                                                                                                                                                                                            ⑥         ⑦    B_CERTS_ERR
                                                                                                                                                                                                                                                                                RECEIVE_RESP_
                                                                                                                                                                                                                                                                                           ⑥                  B_CERTS_OK                                              ⑥          ⑦         RECEIVE_RESP_

be Note
      recognized  that OK,   by       ERR,
                                  PA-Boot              when      ATTK
                                                                    parsing              the refined
                                                                                                 recognized
                                                                                                    attacked             tomoreover,
                                                                                                                                   more
                                                                                                                                 com-  by packet  PA-Boot        and
                                                                                                                                                         fine-grained         when       leads ④   to an
                                                                                                                                                                                               parsing
                                                                                                                                                                                              A_CERT_ERR             the      ④     state; moreover,
                                                                                                                                                                                                                                 attacked
                                                                                                                                                                                                                             A_CERT_OK
                                                                                                                                                                                                                                            RESP_ATTK
                                                                                                                                                                                                                                                           com-           A_CERT_ERR
                                                                                                                                                                                                                                                                      ⑧   RESP_ERR
                                                                                                                                                                                                                                                                                       OK
                                                                                                                                                                                                                                                                                         ⑥      ⑧
                                                                                                                                                                                                                                                                                                      A_CERT_OK
                                                                                                                                                                                                                                                                                                      A_CERT_ERR
                                                                                                                                                                                                                                                                                                          RESP_OK
                                                                                                                                                                                                                                                                                                                   ④  
                                                                                                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                                     A_CERT_OK ④ 
                                                                                                                                                                                                                                                                                                                                                    RESP_ATTK
                                                                                                                                                                                                                                                                                                                                                          ⑥
                                                                                                                                                                                                                                                                                                                                                    RESP_ERR                             RESP_OK
                                                                                                                                                                                                                                                                                                                                                                                 ⑧   RESP_ERR
                                                                                                                                                                                                                                                                                                                                                                                                OK ⑩
                                                                                                                                                                                                                                                                                                                                                                                                            ⑧         RESP_OK

        once a run
munication             packet  visitsandan    thus  ERR leads      once
                                                                state,
                                                                     to an  alarm
                                                                              itaERR  run
                                                                                    raises  and
                                                                                         municationonce
                                                                                               state;   terminates
                                                                                                   visits
                                                                                                       an moreover, aanrun
                                                                                                                  error-specific
                                                                                                                             packetERR        in
                                                                                                                                            visits     the
                                                                                                                                                    state,
                                                                                                                                                     and         an(unique)
                                                                                                                                                                      ⑥
                                                                                                                                                                   thus itERR  raises
                                                                                                                                                                                 leads     ABORT
                                                                                                                                                                                        state, ⑥ ananit
                                                                                                                                                                                                to            ERR state.
                                                                                                                                                                                                          error-specific
                                                                                                                                                                                                                 raises     state;   an moreover,
                                                                                                                                                                                                                                                  ⑥
                                                                                                                                                                                                                                               error-specific⑥
                                                                                                                                                                                                                                                            ABNORMAL                                               ⑥                    ABNORMAL
                                                                                                                                                                                                                                                                                                                                                              ⑥
                                                                                                                                                                                                                                                                                                                                                                                                    END

     status         types        using           prefixing,        alarm
                                                                             see   Note
                                                                                  and
                                                                                         examples  that
                                                                                             terminates          OK,          in
                                                                                                                               ERR,      Fig.
                                                                                                                                           theand
                                                                                                                                 interminates
                                                                                                                                                            5.ATTK
                                                                                                                                                       (unique)                  are
                                                                                                                                                                                     A_CERT_ERR
                                                                                                                                                                                  ABORT   further         Security
                                                                                                                                                                                                        state.
                                                                                                                                                                                                                    A_CERT_OK
                                                                                                                                                                                                              refined                to more  property.           RESP_ERR
                                                                                                                                                                                                                                                                           ⑥
                                                                                                                                                                                                                                                                                    PA-Boot
                                                                                                                                                                                                                                                                                               A_CERT_ERR
                                                                                                                                                                                                                                                                                                   RESP_OK
                                                                                                                                                                                                                                                                                                                 ⑩
                                                                                                                                                                                                                                                                                                                    should
                                                                                                                                                                                                                                                                                                                             A_CERT_OK
                                                                                                                                                                                                                                                                                                                                                 ⑥

                                                                                                                                                                                                                                                                                                                                            be able to secure the            RESP_ERR
                                                                                                                                                                                                                                                                                                                                                                                     ⑥       ⑩
                                                                                                                                                                                                                                                                                                                                                                                                             RESP_OK
                                                                                                                                                                                                                                                                                                                                                                                                                              ⑩

oncealarm  a run   and      terminates
                         visits     an ERRinstate,       the (unique) it raises        ABORT
                                                                                         once
                                                                                            an     alarma state.
                                                                                                       error-specific
                                                                                                                 run   and     visits               an          ERRinstate,      the
                                                                                                                                                                           ABNORMAL ⑥ (unique)   it raises          ABORTan error-specific state.  ABNORMAL
                                                                                                                                                                                                                                                                       (i)    validating
                                                                                                                                                                                                                                                                                    ABNORMAL             ⑥
                                                                                                                                                                                                                                                                                                          certs.
                                                                                                                                                                                                                                                                                                              END
                                                                                                                                                                                                                                                                                                                              ABNORMAL
                                                                                                                                                                                                                                                                                                                         in NVM (ii) attack on chal.-resp. packet
                                                                                                                                                                                                                                                                                                                                                                                          END
                                                                                                                                                                                                                                                                                                                                                                                                                          END

                                                                                                                                                                     Sare
                                                                                                                                                                                                                                                      ABNORMAL                                                                                                    ABNORMAL


alarm and
           AsNote  listedthat OK,
                     terminates
                                 in TableERR,
                                           in theand
                                                        II,      the Note
                                                               ATTK
                                                         (unique)
                                                                           set
                                                                             are
                                                                              ABORT
                                                                                     Λ
                                                                            fine-grainedthat
                                                                                      furtherofstate.
                                                                                         alarm       OK,eventstatus
                                                                                                          refined
                                                                                                            Note
                                                                                                          and     ERR,          labels
                                                                                                                               that
                                                                                                                          terminates types
                                                                                                                                     and
                                                                                                                                     to more  OK,  ATTK  inERR,
                                                                                                                                                        by      inmeans  hand
                                                                                                                                                                       the
                                                                                                                                                                                is  ofin-
                                                                                                                                                                                 further
                                                                                                                                                                                      ATTK
                                                                                                                                                                                 (unique)  prefixing,refined
                                                                                                                                                                                                          boot
                                                                                                                                                                                                         are
                                                                                                                                                                                                          ABORT        for
                                                                                                                                                                                                                         to
                                                                                                                                                                                                                   further        instance,
                                                                                                                                                                                                                                  more
                                                                                                                                                                                                                           process,
                                                                                                                                                                                                                                  state.refined         in
                                                                                                                                                                                                                                                                ⑥

                                                                                                                                                                                                                                                              tothe  more    sense              that
                                                                                                                                                                                                                                                                                                        ⑩

                                                                                                                                                                                                                                                                                                              the        successful                       authentication
                                                                                                                                                                                                                                                                                                                                                                           ⑥

                                                                                                                                                                                                                                                                                                                                                                                                 bychal.-resp. packe
                                                                                                                                                                                                                                                                                                                                                                                                                     ⑩



                                                                            CHAL              RESP
                                                                                                                                                                  ABNORMAL
                                                                                                                                                                            (i) prefixing,
                                                                                                                                                                                   validating                 certs.           in NVM       ABNORMAL
                                                                                                                                                                                                                                                             (i) validating
                                                                                                                                                                                                                                                             (ii)
                                                                                                                                                                                                                                                                            ABNORMAL
                                                                                                                                                                                                                                                                      attack on chal.-resp.     certs.
                                                                                                                                                                                                                                                                                                (i)
                                                                                                                                                                                                                                                                                                    END
                                                                                                                                                                                                                                                                                                               in NVM
                                                                                                                                                                                                                                                                                                       validating         packet certs.    (ii)inattack
                                                                                                                                                                                                                                                                                                                                                      NVMon chal.-resp.
                                                                                                                                                                                                                                                                                                                                                     ABNORMAL
                                                                                                                                                                                                                                                                                                                                                                          (ii) attack on        packet         END

     stantiated
        fine-grained
       Note      that OK,         Sl astypes
                             instatus
                                 ERR,           concrete
                                              and        by means
                                                       ATTK         areactions
                                                                   fine-grained of prefixing,
                                                                             further          ofrefined
                                                                                                  Note theATTK
                                                                                                   status
                                                                                                   fine-grained      protocol
                                                                                                                   thattypes
                                                                                                                     for to more  OK,    indicates
                                                                                                                                 instance, bystatus
                                                                                                                                                 ERR,   participants.
                                                                                                                                                      means       types
                                                                                                                                                                  and   theof ATTK occurrence
                                                                                                                                                                                  by     means are further  for
                                                                                                                                                                                                            of
                                                                                                                                                                                                          PA-Boot
                                                                                                                                                                                                                   of     man-in-the
                                                                                                                                                                                                                      instance,
                                                                                                                                                                                                                    prefixing, refined           for
                                                                                                                                                                                                                                                   to more
                                                                                                                                                                                                                                           (indicated     instance,
                                                                                                                                                                                                                                                                  Fig. 5:      by   Snippets
                                                                                                                                                                                                                                                                                          reaching           of the     the state  ideal   machine   state       Ss̄)         PA-Boot. A state s
                                                                                                                                                                                                                                                                                                                                                                     l of guarantees
     TheCHAL
fine-grained   setRESP ∆      ofATTK
                         status      typesindicates
                                   event-triggered
                                                 by means          CHALofmiddle
                                                                     the            RESP
                                                                               occurrence
                                                                            transitions
                                                                              prefixing,       attacks
                                                                                                   CHAL
                                                                                         fine-grained  ATTK
                                                                                                         for   in       attempting
                                                                                                                ofinstance,  indicates
                                                                                                                          RESP
                                                                                                                         man-in-the
                                                                                                                         S           is specified
                                                                                                                               lstatus
                                                                                                                                                 ATTK types    to
                                                                                                                                                              the      read
                                                                                                                                                                 (i)indicates
                                                                                                                                                                         validating
                                                                                                                                                                         occurrence
                                                                                                                                                                        by
                                                                                                                                                                       Fig.    basedor modify
                                                                                                                                                                                 means
                                                                                                                                                                                  5: Snippets   the certs.
                                                                                                                                                                                                   of    of       the
                                                                                                                                                                                                                   in NVM
                                                                                                                                                                                                               man-in-the
                                                                                                                                                                                                           occurrence
                                                                                                                                                                                                          prefixing,
                                                                                                                                                                                                                 of the
                                                                                                                                                                                                                              challenge-
                                                                                                                                                                                                                                   state
                                                                                                                                                                                                                                                  (ii)
                                                                                                                                                                                                                                      forofinstance,
                                                                                                                                                                                                                                                  machine
                                                                                                                                                                                                                                                           attack on chal.-resp.
                                                                                                                                                                                                                                                    man-in-the
                                                                                                                                                                                                                                                        Fig.is5:identifiedSnippets
                                                                                                                                                                                                                                                                                      (i) validating
                                                                                                                                                                                                                                                                           Sl thereafter   Fig.of
                                                                                                                                                                                                                                                                                  of PA-Boot        by5:the  itspacket  certs. and
                                                                                                                                                                                                                                                                                                                     status
                                                                                                                                                                                                                                                                                                                   state
                                                                                                                                                                                                                                                                                                            Snippets
                                                                                                                                                                                                                                                                                                                 . involves
                                                                                                                                                                                                                                                                                                                    A     state
                                                                                                                                                                                                                                                                                                                                      in NVM
                                                                                                                                                                                                                                                                                                                                machine
                                                                                                                                                                                                                                                                                                                                    ofs the      colored         (ii)inattack
                                                                                                                                                                                                                                                                                                                                                        Sl ofmachine
                                                                                                                                                                                                                                                                                                                                                    state                  light Son
                                                                                                                                                                                                                                                                                                                                                                     PA-Boot           green
                                                                                                                                                                                                                                                                                                                                                                                        .l A
                                                                                                                                                                                                                                                                                                                                                                                             chal.-resp.
                                                                                                                                                                                                                                                                                                                                                                                           ofstate  (normal
                                                                                                                                                                                                                                                                                                                                                                                                 PA-Boot
                                                                                                                                                                                                                                                                                                                                                                                                                    packet
                                                                                                                                                                                                                                                                                                                                                                                                           s . A state
CHAL    middle
             RESP      attacks
                            ATTK     attempting
                                        indicates              tomiddle
                                                             the    read    response
                                                                      occurrenceorattacks
                                                                                        modify
                                                                                         CHAL       ofpacket
                                                                                                   middle attempting
                                                                                                                the challenge-
                                                                                                             RESP
                                                                                                            man-in-the        along
                                                                                                                            attacks  ATTK           the
                                                                                                                                                   to       read
                                                                                                                                                      attempting  inter-processor
                                                                                                                                                          indicates        or modify  to
                                                                                                                                                                                     the       read       that
                                                                                                                                                                                                        the
                                                                                                                                                                                                 occurrence or           every
                                                                                                                                                                                                             communication
                                                                                                                                                                                                                  challenge-
                                                                                                                                                                                                                    modify        of       the boot
                                                                                                                                                                                                                                          man-in-the  challenge- flow
                                                                                                                                                                                                                                                                  termination),                         red        (abnormal
                                                                                                                                                                                                                                                                                                                                               only
                                                                                                                                                                                                                                                                                                                                                 termination),
                                                                                                                                                                                                                                                                                                                                                               trusted              security
                                                                                                                                                                                                                                                                                                                                                                                   or   in     blue,       dark
     on                    and Λ.along       Fig. the    5 depicts                   parts              of along   the             state                machine        is5:identified Sinter-processor   bycan   its state
                                                                                                                                                                                                                         status             andincoloredis     identified      in         by
                                                                                                                                                                                                                                                                                       light       its
                                                                                                                                                                                                                                                                                           is5:identified
                                                                                                                                                                                                                                                                                                     green status    (normaland
                                                                                                                                                                                                                                                                                                                            by         colored
                                                                                                                                                                                                                                                                                                                                    its state
                                                                                                                                                                                                                                                                                                                                            status          in     light
                                                                                                                                                                                                                                                                                                                                                            and colored        green        (normal
                                                                                                                                                                                                                                                                                                                                                                                         in light green                (norma
             State packet                                                                                                                                   Fig.              Snippets     l , communication
                                                                                                                                                                                                       of    the                       machine                   Sl of PA-Boot  Fig.              Snippets
                                                                                                                                                                                                                                                                                                       . A state          of s the                      machine               Sl of PA-Boot                 . A state       s
middle  response
              attacks attempting                       to read         orchannel.
                                                                   response
                                                                 inter-processor
                                                                              modify       packet
                                                                                         middle     Other
                                                                                                   response
                                                                                                    thecommunication    fine-grained
                                                                                                                challenge-
                                                                                                                attacks            packetthe
                                                                                                                                          attempting         along  types
                                                                                                                                                       inter-processor
                                                                                                                                                            is validating
                                                                                                                                                                  identified  totheof
                                                                                                                                                                       termination),read  status
                                                                                                                                                                                              by   orits  assets
                                                                                                                                                                                                          modify
                                                                                                                                                                                                            red
                                                                                                                                                                                                              status
                                                                                                                                                                                                                        be
                                                                                                                                                                                                                        (abnormal
                                                                                                                                                                                                                                  found
                                                                                                                                                                                                                                 and
                                                                                                                                                                                                                                  the
                                                                                                                                                                                                                                  and
                                                                                                                                                                                                                                               is free
                                                                                                                                                                                                                                       communication
                                                                                                                                                                                                                                           challenge-
                                                                                                                                                                                                                                               colored  termination),
                                                                                                                                                                                                                                                        termination),
                                                                                                                                                                                                                                                                       of man-in-the-middle
                                                                                                                                                                                                                                                                  green,
                                                                                                                                                                                                                                                                      in light  isyellow,      red        or
                                                                                                                                                                                                                                                                                               or in(abnormal
                                                                                                                                                                                                                                                                                           termination),
                                                                                                                                                                                                                                                                                       identified
                                                                                                                                                                                                                                                                                           green                 orange
                                                                                                                                                                                                                                                                                                               blue,
                                                                                                                                                                                                                                                                                                                  by itsdark
                                                                                                                                                                                                                                                                                                            (normal            redstatus
                                                                                                                                                                                                                                                                                                                                             attacks:
                                                                                                                                                                                                                                                                                                                                    iftermination),
                                                                                                                                                                                                                                                                                                                                          the      transition
                                                                                                                                                                                                                                                                                                                                           (abnormal
                                                                                                                                                                                                                                                                                                                                                   and        colored     ortoin   s is
                                                                                                                                                                                                                                                                                                                                                                       termination),
                                                                                                                                                                                                                                                                                                                                                                                  in       triggered
                                                                                                                                                                                                                                                                                                                                                                                       blue,
                                                                                                                                                                                                                                                                                                                                                                                       light       dark         by
                                                                                                                                                                                                                                                                                                                                                                                                     or in(normal
                                                                                                                                                                                                                                                                                                                                                                                                  green            blue, dark
     which
        channel.      represent
                         Other              typical
                                     fine-grained               scenarios
                                                                   channel. Fig.
                                                                  types of status     5.    in
                                                                                             For
                                                                                         Other       PA-Boot,
                                                                                                        simplicity,
                                                                                                   channel.fine-grained
                                                                                                         can packet   be Other   found        e.g.,
                                                                                                                                              we         omit
                                                                                                                                                       types
                                                                                                                                                       fine-grained
                                                                                                                                                        in the            detailed
                                                                                                                                                                          of     status           declarations
                                                                                                                                                                                                   can
                                                                                                                                                                                          typesProperty      be
                                                                                                                                                                                                            of        found           of  in  low-
response           packet        along          the inter-processor
                                                                            level
                                                                                         response
                                                                                         types
                                                                                               communication
                                                                                                         like            RCHash
                                                                                                                                                along
                                                                                                                                                    and                green,
                                                                                                                                                            termination),
                                                                                                                                                                    Packet
                                                                                                                                                                                 inter-processor
                                                                                                                                                                                        yellow,              orstatus
                                                                                                                                                                                                  red (abnormal
                                                                                                                                                                                           Processor
                                                                                                                                                                                    indeclarations                   orange
                                                                                                                                                                                                                     and
                                                                                                                                                                                                                                      can
                                                                                                                                                                                                                            communication
                                                                                                                                                                                                                                   Envir.
                                                                                                                                                                                                                                                   be
                                                                                                                                                                                                                                                  the      found
                                                                                                                                                                                                                                                        green,
                                                                                                                                                                                                                                           if2termination),
                                                                                                                                                                                                                                                    (Security     BSP,yellow,
                                                                                                                                                                                                                                                            transition       inAP,    w.r.t.both
                                                                                                                                                                                                                                                                                               soris
                                                                                                                                                                                                                                                                                        togreen,
                                                                                                                                                                                                                                                                                termination),
                                                                                                                                                                                                                                                                                     or      in      blue, processors,
                                                                                                                                                                                                                                                                                                        orange
                                                                                                                                                                                                                                                                                                         S    h ).dark
                                                                                                                                                                                                                                                                                                          triggered
                                                                                                                                                                                                                                                                                                             yellow,  red  if theor       or
                                                                                                                                                                                                                                                                                                                                   byorange
                                                                                                                                                                                                                                                                                                                                 (abnormal        the if
                                                                                                                                                                                                                                                                                                                                          transition        attacker,
                                                                                                                                                                                                                                                                                                                                                                 the
                                                                                                                                                                                                                                                                                                                                                             termination),s is respectively;
                                                                                                                                                                                                                                                                                                                                                                    to transition  triggered ortoin   sbyis
                                                                                                                                                                                                                                                                                                                                                                                                          blue,the dark by
                                                                                                                                                                                                                                                                                                                                                                                                               triggered
     NVM
channel.Fig. 5.Other certificates
                     For    simplicity,
                              fine-grained      (Fig.
                                                   wetypes omit5i)Fig.  and
                                                                       of    5. For
                                                                       detailed
                                                                             status  detectingsimplicity,
                                                                                             declarations
                                                                                         channel.
                                                                                              can  Fig.   be5.Other foundForwe
                                                                                                                         AP            of     omit
                                                                                                                                         replacements
                                                                                                                                       simplicity,
                                                                                                                                               low-
                                                                                                                                          fine-grained
                                                                                                                                           in                  detailed
                                                                                                                                                            green,
                                                                                                                                                                          wetypes
                                                                                                                                                                       BSP,        omit
                                                                                                                                                                                    AP,
                                                                                                                                                                               yellow,
                                                                                                                                                                                         or       detailed
                                                                                                                                                                                                  of
                                                                                                                                                                                                bothor   status
                                                                                                                                                                                                              processors,
                                                                                                                                                                                                           orange
                                                                                                                                                                                                                           of
                                                                                                                                                                                                                                 if
                                                                                                                                                                                                                                   low-
                                                                                                                                                                                                                          declarations
                                                                                                                                                                                                                            can         be found
                                                                                                                                                                                                                                      the         or    BSP,
                                                                                                                                                                                                                                                         the
                                                                                                                                                                                                                                                  transition
                                                                                                                                                                                                                                                               of(condensed)
                                                                                                                                                                                                                                                                    in low-both
                                                                                                                                                                                                                                                                      AP,
                                                                                                                                                                                                                                                                     attacker,to     s
                                                                                                                                                                                                                                                                                green,     BSP,
                                                                                                                                                                                                                                                                                          is         transition
                                                                                                                                                                                                                                                                                                 processors,
                                                                                                                                                                                                                                                                                               respectively;
                                                                                                                                                                                                                                                                                                triggeredAP, both
                                                                                                                                                                                                                                                                                                   yellow,              orby   or the
                                                                                                                                                                                                                                                                                                                              orange    the if
                                                                                                                                                                                                                                                                                                                                  processors,     attacker,
                                                                                                                                                                                                                                                                                                                                                       the       or       respectively;
                                                                                                                                                                                                                                                                                                                                                                        the
                                                                                                                                                                                                                                                                                                                                                                 transition      attacker,
                                                                                                                                                                                                                                                                                                                                                                                        to   s   is    the
                                                                                                                                                                                                                                                                                                                                                                                                     respectively;
                                                                                                                                                                                                                                                                                                                                                                                                      triggered          by th
        level     types
Fig.man-in-the-middle
         5. For              like RCHash
                      simplicity,          we omit      anddetailed
                                                   attacks         level types
                                                                  Packet
                                                                       on4.2.2  indeclarations
                                                                                the      Fig.  like
                                                                                       Processor
                                                                                            response 5. RCHash
                                                                                                   level   For     and
                                                                                                                    types of      Envir.
                                                                                                                          simplicity,
                                                                                                                                   low-
                                                                                                                                packet   and RCHash
                                                                                                                                         like          Packet              inand
                                                                                                                                                               we(condensed)
                                                                                                                                                             (Fig.
                                                                                                                                                            BSP,          omit
                                                                                                                                                                           AP,
                                                                                                                                                                                  Processor
                                                                                                                                                                                5ii).     Packettransition
                                                                                                                                                                                      detailed
                                                                                                                                                                                     both
                                                                                                                                                                                                           and
                                                                                                                                                                                                     processors,
                                                                                                                                                                                                                       Envir. and
                                                                                                                                                                                                                    Processor
                                                                                                                                                                                                            indeclarations
                                                                                                                                                                                                                                      or the
                                                                                                                                                                                                                                                           Envir.
                                                                                                                                                                                                                                                     of(condensed)
                                                                                                                                                                                                                                                            low- BSP,
                                                                                                                                                                                                                                                          attacker,                        transition
                                                                                                                                                                                                                                                                                           (condensed)
                                                                                                                                                                                                                                                                                     respectively;
                                                                                                                                                                                                                                                                                               AP, both the                 transition or the attacker, respectively; the
                                                                                                                                                                                                                                                                                                                        processors,
level types like RCHash and Packet in Processor                                               Event-Triggered
                                                                                         level and      types        Envir. like RCHash             Transitions       and Packettransition         in Processor and Envir.        ∀      π       ∈      Π.          Tail              (π)          =       s̄      ⇐⇒               B       (Γ           )   ∧     M         (π)                 (‡)
           The security-related utility                                     Asfunctions
                                                                                   listed            in Table       Γ,          2,BTransitions
                                                                                                                                        the  and               MΛ of as
                                                                                                                                                    set(condensed)            event  de-labels                 in Sh is instan-
                                                                                                                                                                                                                                                                           The           set ∆ of event-triggered
                                                                                                                                                                                                                                                                                (condensed)                        transition s0 transitions in Sl is speci-
        4.2.2 Event-Triggered Transitions                          4.2.2            Event-Triggered4.2.2                  Event-Triggered                                      Transitions
                                                                            tiatedlabels    inTable Sl in  as                                                                   The         set in     ∆ Sof is       event-triggered                             fied
                                                                                                                                                                                                                                                                 The           in
                                                                                                                                                                                                                                                                              set
                                                                                                                                                                                                                                                                     transitions The   an∆      analogous
                                                                                                                                                                                                                                                                                                of      event-triggered
                                                                                                                                                                                                                                                                                                     in Slset       is ∆     way.
                                                                                                                                                                                                                                                                                                                           speci-           Fig.transitions
                                                                                                                                                                                                                                                                                                                                 of event-triggered     5 depicts in            partsSl isofspeci-
                                                                                                                                                                                                                                                                                                                                                                                 transitions       theinlow-    Sl is speci
4.2.2scribed
        As listed        in
             Event-Triggered   the high-level
                          in Table             the set Λ As
                                           2, Transitions           specification
                                                                    of     listed
                                                                          event           in
                                                                                         4.2.2     As           are
                                                                                                            listed  Sconcrete
                                                                                                                   2,    hthe
                                                                                                             Event-Triggered    instantiated
                                                                                                                                         set
                                                                                                                                isininstan-Table    actions
                                                                                                                                                    Λ       of2,eventtheof    in
                                                                                                                                                                     Transitionssetthe Λ protocol
                                                                                                                                                                                      the
                                                                                                                                                                                   labels     of event                participants.
                                                                                                                                                                                                               h labels
                                                                                                                                                                                                          Intuitively,      instan-      in S    Propertyis instan-
                                                                                                                                                                                                                                                     h fied       level
                                                                                                                                                                                                                                                                     in      an2state  ensures
                                                                                                                                                                                                                                                                                      analogous machine          that
                                                                                                                                                                                                                                                                                                                    way.       awhich
                                                                                                                                                                                                                                                                                                                        Sl ,low-  Fig.run5 π       depictsof Fig.
                                                                                                                                                                                                                                                                                                                                                   represent       Shparts   terminates
                                                                                                                                                                                                                                                                                                                                                                           typical   of the scenarios
                                                                                                                                                                                                                                                                                                                                                                                                    low-          inspeci-
                          Sl ascounterpart                         tiated   Given in      S a     state
                                                                                                  as     concrete s      and     S      an
                                                                                                                                        actions    event          of  efied
                                                                                                                                                                      The  in
                                                                                                                                                                         the      Sin
                                                                                                                                                                                  set ,   whether
                                                                                                                                                                                          an
                                                                                                                                                                                   protocol
                                                                                                                                                                                    l       ∆       analogous
                                                                                                                                                                                                    of             e    is
                                                                                                                                                                                                            event-triggered
                                                                                                                                                                                                            participants.       enabled
                                                                                                                                                                                                                                    way.             in
                                                                                                                                                                                                                                                   Fig.         5
                                                                                                                                                                                                                                                           transitionsdepicts              fied
                                                                                                                                                                                                                                                                                            parts
                                                                                                                                                                                                                                                                                          The
                                                                                                                                                                                                                                                                                          in      S     in
                                                                                                                                                                                                                                                                                                      set   of
                                                                                                                                                                                                                                                                                                           is  an
                                                                                                                                                                                                                                                                                                                ∆   the
                                                                                                                                                                                                                                                                                                                 speci- analogous
                                                                                                                                                                                                                                                                                                                        of     event-triggered       way.                    5    depicts
                                                                                                                                                                                                                                                                                                                                                                         transitions               parts
                                                                                                                                                                                                                                                                                                                                                                                                  in    Sl isof       the low
        tiatedin
As lower-level
       listed      inTable        2,concrete
                                       the set Λ        actions
                                                           ofas   event of the
                                                                       well.s   labels
                                                                                or
                                                                                         protocol
                                                                                        For
                                                                                         As
                                                                                       not
                                                                                             l in  tiated
                                                                                                  is  example,
                                                                                                  listedS
                                                                                                        specified
                                                                                                            h
                                                                                                                    participants.
                                                                                                                   is
                                                                                                                    in in instan-
                                                                                                                              Table   l
                                                                                                                                        in
                                                                                                                                           as
                                                                                                                                            for     concrete
                                                                                                                                                   2,      a
                                                                                                                                                         the
                                                                                                                                                Isabelle/HOL      state
                                                                                                                                                                      set      Λ   s
                                                                                                                                                                               actions
                                                                                                                                                                                    of    in
                                                                                                                                                                                           event
                                                                                                                                                                                          as
                                                                                                                                                                                                    of     the
                                                                                                                                                                                                          inlabels    protocol
                                                                                                                                                                                                                    the       Sin     S
                                                                                                                                                                                                                                    ideal h
                                                                                                                                                                                                                                                 participants.
                                                                                                                                                                                                                                                is    instan-
                                                                                                                                                                                                                                                        state
                                                                                                                                                                                                                                                        level     PA-Boot s̄
                                                                                                                                                                                                                                                                       state       ∈      ,
                                                                                                                                                                                                                                                                                      machine e.g.,
                                                                                                                                                                                                                                                                                              S    ↓  l
                                                                                                                                                                                                                                                                                                            validating
                                                                                                                                                                                                                                                                                                           if  S   and
                                                                                                                                                                                                                                                                                                                    ,   which     only  certificates
                                                                                                                                                                                                                                                                                                                                          represent
                                                                                                                                                                                                                                                                                                                                                S  if       M(π)       in
                                                                                                                                                                                                                                                                                                                                                                   typical   the  =   NVM
                                                                                                                                                                                                                                                                                                                                                                                    scenarios
                                                                                                                                                                                                                                                                                                                                                                                          true      and  in    de-
tiated  Given
            in    S al as
                        state    s and an
                             concrete          actionseventofe the Given          a
                                                                       in Sprotocol     state
                                                                                 l , whether
                                                                                         tiated        s
                                                                                                   Given   and   eSisal as
                                                                                                        participants.
                                                                                                          in               an enabled
                                                                                                                              state   event
                                                                                                                                        concrete s and    e fied
                                                                                                                                                        in an   in      S
                                                                                                                                                                       level
                                                                                                                                                                          in
                                                                                                                                                                     actions  ,     state
                                                                                                                                                                                 whether
                                                                                                                                                                                  an
                                                                                                                                                                            leventofe theanalogous  machine
                                                                                                                                                                                                         e   is
                                                                                                                                                                                                   in Sprotocol     enabled
                                                                                                                                                                                                             l , whether way.     l ,   which
                                                                                                                                                                                                                                          in
                                                                                                                                                                                                                                         Fig.         5    represent
                                                                                                                                                                                                                                                           depicts
                                                                                                                                                                                                                                             e is enabled in
                                                                                                                                                                                                                                      participants.                             fied
                                                                                                                                                                                                                                                                                 parts typical
                                                                                                                                                                                                                                                                                           level
                                                                                                                                                                                                                                                                                              in  of an  state
                                                                                                                                                                                                                                                                                                           scenarios
                                                                                                                                                                                                                                                                                                          the  analogous
                                                                                                                                                                                                                                                                                                                  l     machine
                                                                                                                                                                                                                                                                                                                     low-            in     way.   l ,  which
                                                                                                                                                                                                                                                                                                                                                          Fig.       5   represent
                                                                                                                                                                                                                                                                                                                                                                          depicts              typical
                                                                                                                                                                                                                                                                                                                                                                                           parts        of      scenarios
                                                                                                                                                                                                                                                                                                                                                                                                               the    low- in
     Sslor , Γnot s = Γ(s) yields                          the security                          context                  inisassociated                                  with            s,, e.g.,and                                                  PA-Boot   tecting      ,in    man-in-the-middle
                                                                                                                                                                                                                                                                                    e.g.,         validating                              attacks
                                                                                                                                                                                                                                                                                                                               certificates                 on
                                                                                                                                                                                                                                                                                                                                                             in     the challenge-response
                                                                                                                                                                                                                                                                                                                                                                              NVM         inand       de-
Given       a stateis sspecified
                              and an event                 e insSor
                                               in Isabelle/HOL          l ,  not
                                                                             whether   isGiven
                                                                                      as
                                                                                  definition specified
                                                                                                   s e  oris
                                                                                                           a      not
                                                                                                                  enabled
                                                                                                                  state
                                                                                                                  event              Isabelle/HOL
                                                                                                                                     sspecified
                                                                                                                                          and
                                                                                                                                           in
                                                                                                                                        enabled          an level    in
                                                                                                                                                                     ::PA-Boot
                                                                                                                                                                    event ''Statease in
                                                                                                                                                                            Isabelle/HOL
                                                                                                                                                                           state        ⇒machineSEvent
                                                                                                                                                                                                    l ,        validating
                                                                                                                                                                                                         whether⇒  S
                                                                                                                                                                                                                   as  l B(Γ
                                                                                                                                                                                                                         ,
                                                                                                                                                                                                                        B''   whiche
                                                                                                                                                                                                                                  wheresis0   ) certificates
                                                                                                                                                                                                                                                    =
                                                                                                                                                                                                                                                 represent
                                                                                                                                                                                                                                              enabled         true  in
                                                                                                                                                                                                                                                                  packet.
                                                                                                                                                                                                                                                                                 (so
                                                                                                                                                                                                                                                                             typical
                                                                                                                                                                                                                                                                                level
                                                                                                                                                                                                                                                                                        A
                                                                                                                                                                                                                                                                                         the
                                                                                                                                                                                                                                                                                           PA-Boot
                                                                                                                                                                                                                                                                                               is   NVM
                                                                                                                                                                                                                                                                                                state  B(Γ
                                                                                                                                                                                                                                                                                                  scenarios
                                                                                                                                                                                                                                                                                              complete
                                                                                                                                                                                                                                                                                                                  , sand
                                                                                                                                                                                                                                                                                                              machine e.g.,
                                                                                                                                                                                                                                                                                                                        )  in
                                                                                                                                                                                                                                                                                                                        view
                                                                                                                                                                                                                                                                                                                             for de-
                                                                                                                                                                                                                                                                                                                                   validating
                                                                                                                                                                                                                                                                                                                                     S   any
                                                                                                                                                                                                                                                                                                                                          l ,
                                                                                                                                                                                                                                                                                                                                      of Sl on
                                                                                                                                                                                                                                                                                                                                               which
                                                                                                                                                                                                                                                                                                                                                    can
                                                                                                                                                                                                                                                                                                                                                       s       certificates
                                                                                                                                                                                                                                                                                                                                                             along
                                                                                                                                                                                                                                                                                                                                                              be
                                                                                                                                                                                                                                                                                                                                                                represent
                                                                                                                                                                                                                                                                                                                                                                      foundon
                                                                                                                                                                                                                                                                                                                                                                               π,      due
                                                                                                                                                                                                                                                                                                                                                                                       typical  theto    NVM and
                                                                                                                                                                                                                                                                                                                                                                                                       scenarios          in de
s orthat        is,     the components                            ⟨bsp,      asap,          env⟩                  inspecifieds;s moreover,                  PA-Boot    tecting  given
                                                                                                                                                                                ⇒, Event
                                                                                                                                                                                         man-in-the-middle
                                                                                                                                                                                       e.g.,      e)validating                       certificatesattackstecting       in man-in-the-middle
                                                                                                                                                                                                                                                                      on      the
                                                                                                                                                                                                                                                                                PA-Boot challenge-response
                                                                                                                                                                                                                                                                                           tecting
                                                                                                                                                                                                                                                                                          NVM           ,of and                attacks
                                                                                                                                                                                                                                                                                                               man-in-the-middle
                                                                                                                                                                                                                                                                                                            e.g.,       de-
                                                                                                                                                                                                                                                                                                                         validating                       the   attacks
                                                                                                                                                                                                                                                                                                                                                      certificates                ininthe
                                                                                                                                                                                                                                                                                                                                                                    challenge-response    Appx.          A. and de-
                                                                                                                                                                                                                                                                                                                                                                                               challenge-respons
                                                                                                                                                                                                                                                                                                                                                                                                 NVM
         not    is specified
            definition           event in Isabelle/HOL
                                               enabled :: ''State                    ⇒s Event
                                                                                  ''event
                                                                         definition          or not   event  ⇒isB''
                                                                                                       enabled
                                                                                                           definition      enabled
                                                                                                                                 where         ≡ in
                                                                                                                                         e event         ::case  Isabelle/HOL
                                                                                                                                                               ''State  (status
                                                                                                                                                                     enabled                           ⇒
                                                                                                                                                                                            ::s, ''State as
                                                                                                                                                                                                          Property
                                                                                                                                                                                                         of  B''⇒where   Event 1),        ⇒ B''     that  where    is,      π      is      free                   man-in-the-middle
                                                                                                                                                                                                                                                                                                                            of Sl can                                      attacks            and
     adefinition
          run      π ofenabled Sl , M(π)                 determines                      whether                                                            tecting    packet.             A complete view
                                                                                                                                                                                 man-in-the-middle                                    attacksof Spacket.l on canthe     beA        complete
                                                                                                                                                                                                                                                                               found       packet.
                                                                                                                                                                                                                                                                             challenge-response
                                                                                                                                                                                                                                                                                tecting                        view
                                                                                                                                                                                                                                                                                                  inman-in-the-middle
                                                                                                                                                                                                                                                                                                         Appx. A complete A.                    view be     found
                                                                                                                                                                                                                                                                                                                                                             of Sl on
                                                                                                                                                                                                                                                                                                                                                       attacks              inthe
                                                                                                                                                                                                                                                                                                                                                                          can      Appx.         A. in Appx. A.
                                                                                                                                                                                                                                                                                                                                                                                   bechallenge-response
                                                                                                                                                                                                                                                                                                                                                                                         found
                                                                         ''event                 )INIT
                                                                                              e(definition      , Readsor   e event  not
                                                                                                                                     ≡ ROM    case a)enabled
                                                                                                                                                         man-in-the-
                                                                                                                                                               ⇒
                                                                                                                                                             (status                   e| ) of
                                                                                                                                                                                   s, ''State             both        s, ethe
                                                                                                                                                                                                                                   of AP              and     be the             certificates                    A.in theview              NVM     of Slremain                      genuine
            ''event event                    s e ≡ ::case
                                       enabled                 ''State
                                                                     (status⇒ Event      s,enabled⇒  ofB'' ''event  where             enabled                    s etrue    ≡ ::case            (status ⇒      Event           )⇒  ofB'' where
                                                                                                                                                            packet. A complete                                     view                   Sl can                      found     packet. in Appx.      A complete                                                 can be found                   in Appx. A.
     middle
      ''event enabled (attack,
                        INIT, Read   s ei.e.,≡ROM    11), (status
                                                   case       ⇒is absent
                                                                     trues, e|()INIT      along
                                                                                           of(ok         READ
                                                                                                    , Read
                                                                                                ''event         π. enabledROM
                                                                                                                            (INITROM       ), Read⇒  sOK etrue  ,≡  Read
                                                                                                                                                                    ROM   case | )NVM⇒ true
                                                                                                                                                                                    (status       ) ⇒s, true
                                                                                                                                                                                                          along e| ) of π.         |
                                                                                                                                                                                                                                            Moreover,Thethesecurity-related                     established utility                   sharedfunctions        sessionΓ,key               B and    Ks M as
              (INIT   (ok    READ
                         , Read       ROM  ROM   ) ⇒OKtrue      , Read| NVM          (ok)READ  · ·⇒  · true    (INITROM     (ok ,|Read    OK, Read
                                                                                                                                        READ            ROM    ROM      )NVM ⇒  The
                                                                                                                                                                                 OKtrue     ⇒
                                                                                                                                                                                      ), Read          | NVM| ) ⇒ true
                                                                                                                                                                                                      true
                                                                                                                                                                                            security-related                               utility                described
                                                                                                                                                                                                                                                                 The
                                                                                                                                                                                                                                                           | functions         security-related
                                                                                                                                                                                                                                                                                             Γ in, Thetheand
                                                                                                                                                                                                                                                                                                      B          high-level
                                                                                                                                                                                                                                                                                                                          Mutility
                                                                                                                                                                                                                                                                                                                 security-related   as        specification
                                                                                                                                                                                                                                                                                                                                               functions    utility           are
                                                                                                                                                                                                                                                                                                                                                                                B and
                                                                                                                                                                                                                                                                                                                                                                         Γ, functions instantiated
                                                                                                                                                                                                                                                                                                                                                                                                MΓ, as     B and  in M a
                                                                                                                                                                                                          ensures that PA-Boot                          described the              is
                                                                                                                                                                                                                                                                            lower-level
                                                                                                                                                                                                                                                                                     in
                                                                                                                                                                                                                                                                                           able
                                                                                                                                                                                                                                                                                             the
                                                                                                                                                                                                                                                                                                          tocounterpart
                                                                                                                                                                                                                                                                                                       high-level
                                                                                                                                                                                                                                                                                                                  securespecification   the  as    entire
                                                                                                                                                                                                                                                                                                                                                    well.         For boot
                                                                                                                                                                                                                                                                                                                                                                     are   example,process.
                                                                                                                                                                                                                                                                                                                                                                              instantiated      for     ainstate
              (ok READ···          ROM     VI.   OK,FRead  ORMAL       NVMV          ·  · ·    (ok
                                                                                         ⇒ true(ok| READ
                                                                                   ) ERIFICATION         SEND               ···  CHAL                   OK
                                                                                                                                                   ROM The        ,    described
                                                                                                                                                                     Receive
                                                                                                                                                                      OK, Read            Packet
                                                                                                                                                                                   security-relatedin     the
                                                                                                                                                                                                            )
                                                                                                                                                                                                  NVM) ⇒ true    ⇒   high-level
                                                                                                                                                                                                                            true              |      specification
                                                                                                                                                                                                                                  utility| functions Γ, The                               are
                                                                                                                                                                                                                                                                                           described
                                                                                                                                                                                                                                                                                            B and   instantiatedM as  in
                                                                                                                                                                                                                                                                                                       security-related      the     in high-level utility functions Γ, B and M as in
                                                                                                                                                                                                                                                                                                                                                                   specification                 are     instantiated
                                                                                                                                                                       the lower-level                          counterpart                             the            in Sare
                                                                                                                                                                                                                                                                  slower-level         Γinstantiated
                                                                                                                                                                                                                                                                                 l , example,  =counterpart
                                                                                                                                                                                                                                                                                                      Γ(s)         yields           the
                                                                                                                                                                                                                                                                                                                                   as         security
                                                                                                                                                                                                                                                                                                                                           well.        For        context
                                                                                                                                                                                                                                                                                                                                                                   as well.associated
                                                                                                                                                                                                                                                                                                                                                                   example,             for         statewithfor ainstat
                                                                                                                                                                                                                                                                                                                                                                                                ainstantiated
                                                                                                                                                                                                                                           ⇒ as             well.      | For               the       lower-level
                                                                                                                                                                                                                                                                                                             infor  theainstate     counterpart                                       Forareexample,
                                                                                                                                                                                                                                                                                          s
              · · · (ok SEND CHAL OK, Receive (ok                                      Packet  SEND
                                                                                               (ok )SEND       ·⇒ ·CHAL
                                                                                                                     · true (ok  CHAL      OK
                                                                                                                                        SEND   | ,OK        described
                                                                                                                                                         Receive  , Attack
                                                                                                                                                               CHAL                 ) in
                                                                                                                                                                                  Packet
                                                                                                                                                                                  OK     ,⇒      the
                                                                                                                                                                                                  )true
                                                                                                                                                                                            Receive     ⇒high-level
                                                                                                                                                                                                                true |
                                                                                                                                                                                                                   Packet          | ) specification true                       described                                     high-level                  specification
           This section presents the mechanized                                                                   proof                  in        Isabelle/HOL
                                                                                                                                                            the        s   in
                                                                                                                                                                       lower-levelS   ,   Γ        =      Γ(s)
                                                                                                                                                                                                       counterpart     yields             the
                                                                                                                                                                                                                                          as            s
                                                                                                                                                                                                                                                     security
                                                                                                                                                                                                                                                  well.      in   sS, lthat
                                                                                                                                                                                                                                                                 For     ,  Γ
                                                                                                                                                                                                                                                                            context
                                                                                                                                                                                                                                                                            example,
                                                                                                                                                                                                                                                                                the
                                                                                                                                                                                                                                                                                s    is,slower-level
                                                                                                                                                                                                                                                                                     =       the
                                                                                                                                                                                                                                                                                            Γ(s)
                                                                                                                                                                                                                                                                                               in     Scomponents
                                                                                                                                                                                                                                                                                                         yields
                                                                                                                                                                                                                                                                                                  associated
                                                                                                                                                                                                                                                                                                      for   ,  Γa      =
                                                                                                                                                                                                                                                                                                                    state theΓ(s)
                                                                                                                                                                                                                                                                                                                              with
                                                                                                                                                                                                                                                                                                                          counterpart   hbsp,
                                                                                                                                                                                                                                                                                                                                    security
                                                                                                                                                                                                                                                                                                                                          yields       ap, the
                                                                                                                                                                                                                                                                                                                                                          as   envi
                                                                                                                                                                                                                                                                                                                                                          context   security
                                                                                                                                                                                                                                                                                                                                                                 well.      inFor  s. example,
                                                                                                                                                                                                                                                                                                                                                                            associated ...
                                                                                                                                                                                                                                                                                                                                                                                       context      withassociated
                                                                                                                                                                                                                                                                                                                                                                                                           for a statewith
              (ok SEND(ok SEND     CHAL    CHAL  OK,OK    Receive, Attack        ) (ok
                                                                             Packet    ⇒ )SEND (attk
                                                                                                true⇒ true     (ok |CHAL
                                                                                                                  CHAL      (ok| SEND
                                                                                                                           SEND            OKCHAL
                                                                                                                                         ATTK         , Attack
                                                                                                                                                           , Receive
                                                                                                                                                               CHAL     OK  ) ,⇒  OKPacket
                                                                                                                                                                                    l    ,true
                                                                                                                                                                                   Receive    s
                                                                                                                                                                                            Attack         |⇒
                                                                                                                                                                                                      ) Packet
                                                                                                                                                                                                             ) ⇒     true  )true ⇒| true        |            |                                            l       s
     that (ok   PA-Boot                  is     functionally                       correct                    and                 suffices                  s    in to        detect
                                                                                                                                                                       sS,Packet
                                                                                                                                                                             that
                                                                                                                                                                              ,  Γ      is,
                                                                                                                                                                                        =        the
                                                                                                                                                                                                Γ(s)      components
                                                                                                                                                                                                             yields             the             hbsp,
                                                                                                                                                                                                                                          security      s, that ap,       is,sthe
                                                                                                                                                                                                                                                                         envi
                                                                                                                                                                                                                                                                   context           in insScomponents
                                                                                                                                                                                                                                                                                              ,slthat
                                                                                                                                                                                                                                                                                        associated.Γ
                                                                                                                                                                                                                                                                                                  ,  ...s =  is, Γ(s)
                                                                                                                                                                                                                                                                                                                    the
                                                                                                                                                                                                                                                                                                                    with      hbsp,
                                                                                                                                                                                                                                                                                                                              components
                                                                                                                                                                                                                                                                                                                                yields        ap,the   envi    hbsp,
                                                                                                                                                                                                                                                                                                                                                          security  in s.ap,   ... envi associated
                                                                                                                                                                                                                                                                                                                                                                               context         in s. ...              with
                      SEND
                      (attk CHAL   CHAL ATTK     OK, Attack, Receive    ) ⇒Packet    (attk     ·
                                                                                      true) |⇒ (ok·  ·CHAL        true      ATTK
                                                                                                                           SEND
                                                                                                                            (attk       | CHAL,   Receive
                                                                                                                                                   CHAL ATTK                l
                                                                                                                                                                        OK, Attack  s      )
                                                                                                                                                                                   , Receive      ⇒       B.
                                                                                                                                                                                                          true
                                                                                                                                                                                                    ) ⇒Packet        Low-Level
                                                                                                                                                                                                                            |
                                                                                                                                                                                                                   true) |⇒ true | 5 F ORMAL V ERIFICATION Properties
     aforementioned                         adversarial                     behaviors                        (a)                                            sSesskey
                                                                                                                                                               , that           is,  the         components                          hbsp, ap, envi ins,sthat                           . ... is, the components hbsp, ap, envi in s. ...
              (attk   · · ·CHAL ATTK               , Receive Packet                  · )· · ⇒  (oktrue   RESP  (attk       |· and
                                                                                                                              ·OK ·CHAL   , Gen   (b).ATTK         The    ,       )core
                                                                                                                                                                             Receive  ⇒ true
                                                                                                                                                                       5 F ORMAL VNext,            Packet        | ) ⇒ true                           | 5 This      F ORMAL                       V ERIFICATION
     ingredient
              · · · (ok RESP  to theOKproof                  is the )formalization ⇒ (oktrue   RESP
                                                                                               (err RESP      |· ·OK · (ok   , of
                                                                                                                                GenERR     the
                                                                                                                                        RESP     ,Sesskey
                                                                                                                                                    Send correspond-  Packet
                                                                                                                                                                        )Gen  ⇒ Sesskey
                                                                                                                                                                                     ) ⇒ true
                                                                                                                                                                                     true
                                                                                                                                                                                                                    ERIFICATION
                                                                                                                                                                                                        | ) ⇒ | true Properties            |                                    and5 2 first
                                                                                                                                                                                                                                                                          1 section                   F ORMAL
                                                                                                                                                                                                                                                                                                      are        presents
                                                                                                                                                                                                                                                                                                                 refined          V ERIFICATION
                                                                                                                                                                                                                                                                                                                                        a set of security properties on Sl ,
                                                                                                                                                                                                                                                                                                                                        w.r.t. Sl in the form of
                                                , Gen Sesskey                                                                                               5OK,This    F ORMAL    sectionVfirst          ERIFICATIONpresents a set                     This   ofcovering
                                                                                                                                                                                                                                                                      section
                                                                                                                                                                                                                                                                      security  5 This      Fnormal
                                                                                                                                                                                                                                                                                           first ORMAL
                                                                                                                                                                                                                                                                                              propertiespresents
                                                                                                                                                                                                                                                                                                        section    execution
                                                                                                                                                                                                                                                                                                                         Von  aS    set
                                                                                                                                                                                                                                                                                                                             ERIFICATION
                                                                                                                                                                                                                                                                                                                            first       , of   and
                                                                                                                                                                                                                                                                                                                                        presents   securitydifferent        of attack
                                                                                                                                                                                                                                                                                                                                                               a setproperties    security      scenarios.
                                                                                                                                                                                                                                                                                                                                                                                                        S,
                                                                                                                                                                                                                                                                                                                                                                                                 onproperties             on Sl
     ing properties on functional correctness and security
              (ok     RESP
                      (err       OK
                               RESP     ,   ERR
                                           Gen       Sesskey
                                                     , Send         Packet
                                                                     )    ⇒       )  (err
                                                                                  true  ⇒      (  RESP
                                                                                                   |
                                                                                                 true,    )    (ok⇒ |ERR     false
                                                                                                                           RESP
                                                                                                                            (err     ,  Send
                                                                                                                                           RESP''OK .      Packet
                                                                                                                                                           ,    ERR
                                                                                                                                                               Gen    –      )
                                                                                                                                                                            first ⇒
                                                                                                                                                                            Sesskey
                                                                                                                                                                            ,
                                                                                                                                                                       coveringSend       at
                                                                                                                                                                                           true
                                                                                                                                                                                              Packet
                                                                                                                                                                                                )     ⇒
                                                                                                                                                                                                 normal
                                                                                                                                                                                                          Isabelle/HOL
                                                                                                                                                                                                            | )
                                                                                                                                                                                                              true  ⇒            |
                                                                                                                                                                                                                               true
                                                                                                                                                                                                                       execution                 |       lemmas.
                                                                                                                                                                                                                                                        covering
                                                                                                                                                                                                                                                      and         Then,
                                                                                                                                                                                                                                                                    different      an
                                                                                                                                                                                                                                                                                  normal
                                                                                                                                                                                                                                                                                        We  overview
                                                                                                                                                                                                                                                                                           covering
                                                                                                                                                                                                                                                                                              attack
                                                                                                                                                                                                                                                                                                    use          .
                                                                                                                                                                                                                                                                                                         execution
                                                                                                                                                                                                                                                                                                                      to
                                                                                                                                                                                                                                                                                                                       of
                                                                                                                                                                                                                                                                                                                 scenarios.
                                                                                                                                                                                                                                                                                                                    normal
                                                                                                                                                                                                                                                                                                                              extract
                                                                                                                                                                                                                                                                                                                             invariant
                                                                                                                                                                                                                                                                                                                                      l
                                                                                                                                                                                                                                                                                                                                     and
                                                                                                                                                                                                                                                                                                                                                      specific
                                                                                                                                                                                                                                                                                                                                                       proofs
                                                                                                                                                                                                                                                                                                                                                 different
                                                                                                                                                                                                                                                                                                                                          execution                  and is   fields
                                                                                                                                                                                                                                                                                                                                                                              given
                                                                                                                                                                                                                                                                                                                                                                         attack different  to
                                                                                                                                                                                                                                                                                                                                                                                        scenarios.
                                                                                                                                                                                                                                                                                                                                                                                                     a l
                                                                                                                                                                                                                                                                                                                                                                                             ofshowcase
                                                                                                                                                                                                                                                                                                                                                                                                     attack scenarios
                                                                                                                                                            This section first presents a set of securityThis                                                                      properties sectionon            first Slpresents
                                                                                                                                                                                                                                                                                                                              ,                       a set of security properties                                  on Sl ,
     the level(err( RESP  , of) ⇒SERR        , Send '' . Packet) ⇒ (true
                                     h and then at Sl in a refined form. covering
                                        false                                             , ) ⇒         | (err   false           ,'' .) ⇒ERR
                                                                                                                            ( RESP                         false  , Send   '' . Packet
                                                                                                                                                                       Then,          an overview
                                                                                                                                                                                     normal          ) state
                                                                                                                                                                                                          ⇒         true
                                                                                                                                                                                                             execution
                                                                                                                                                                                                                            in       S| land
                                                                                                                                                                                                                            of invariant    , e.g.,     Then,      s. an
                                                                                                                                                                                                                                                                  the
                                                                                                                                                                                                                                                                proofs
                                                                                                                                                                                                                                                         different
                                                                                                                                                                                                                                                                          ap      .isattack
                                                                                                                                                                                                                                                                            functionalprivate
                                                                                                                                                                                                                                                                                 overview
                                                                                                                                                                                                                                                                                covering  given
                                                                                                                                                                                                                                                                                           Then,         correctness
                                                                                                                                                                                                                                                                                                          toan        keyexecution
                                                                                                                                                                                                                                                                                                              ofshowcase
                                                                                                                                                                                                                                                                                                       scenarios.
                                                                                                                                                                                                                                                                                                           normal   invariant
                                                                                                                                                                                                                                                                                                                    overview         denotes   Sl .invariant
                                                                                                                                                                                                                                                                                                                                       of proofs
                                                                                                                                                                                                                                                                                                                                               of      A and  PrivK
                                                                                                                                                                                                                                                                                                                                                            refinement
                                                                                                                                                                                                                                                                                                                                                               is given        APtoin
                                                                                                                                                                                                                                                                                                                                                                            proofs
                                                                                                                                                                                                                                                                                                                                                                        different      proof s.given
                                                                                                                                                                                                                                                                                                                                                                                         showcase
                                                                                                                                                                                                                                                                                                                                                                                            is
                                                                                                                                                                                                                                                                                                                                                                                            attack between     to showcas
                                                                                                                                                                                                                                                                                                                                                                                                           scenarios.
              ( , ) ⇒ false'' .                                               Mingshuai: Polished              ( , ) ⇒ till                   false      here.
                                                                                                                                                            Then,'' .thean       functional
                                                                                                                                                                                     overviewcorrectness         of invariant                         Sthe
                                                                                                                                                                                                                                               of proofs          Srefinement
                                                                                                                                                                                                                                                                      hisand
                                                                                                                                                                                                                                                          l . Afunctional      given
                                                                                                                                                                                                                                                                                Then,   Sthe
                                                                                                                                                                                                                                                                                           l is toan also
                                                                                                                                                                                                                                                                                                correctness
                                                                                                                                                                                                                                                                                                    proof
                                                                                                                                                                                                                                                                                                     functional
                                                                                                                                                                                                                                                                                                        showcase shown
                                                                                                                                                                                                                                                                                                          overview  between         here.
                                                                                                                                                                                                                                                                                                                                    Sl .invariant
                                                                                                                                                                                                                                                                                                                              ofcorrectness
                                                                                                                                                                                                                                                                                                                                    of        A refinement           Sl . Aproof
                                                                                                                                                                                                                                                                                                                                                              of proofs                    between
                                                                                                                                                                                                                                                                                                                                                                                  refinement
                                                                                                                                                                                                                                                                                                                                                                                    is given          toproof
                                                                                                                                                                                                                                                                                                                                                                                                            showcase  between
         Mingshuai: Polished till here.Mingshuai: Polished                                            Mingshuai:                             here.the functional
                                                                                                                                 till Polished                         Still
                                                                                                                                                                           h and   here.   Sl is         also shown
                                                                                                                                                                                                   correctness                             Sl . ASrefinement
                                                                                                                                                                                                                                     of here.              h and Sthe           l is proof also
                                                                                                                                                                                                                                                                                           S   h and
                                                                                                                                                                                                                                                                                           functional   shown  Sl is
                                                                                                                                                                                                                                                                                                          between         here.
                                                                                                                                                                                                                                                                                                                            also shown
                                                                                                                                                                                                                                                                                                                       correctness                   of    here.
                                                                                                                                                                                                                                                                                                                                                           S   l .  A    refinement               proof        between
     A. High-Level Properties                                                                                                                               Still     and   theSbootloader
                                                                                                                                                                                                          Functional                                   correctness.
                                                                                                                                                                                                                                                                  5.1 High-Level
                                                                                                                                                                                                                                                                                Sh and Sl is also shown here. l
                                                                                                                                                                                                                                                                                                                       the level of S , Property 1
                                                                                                                                                                                                                                                                                                            AtProperties
 Mingshuai: Polished till here.                                                 1. Other            contents inPolished
                                                                                           Mingshuai:                                the NVM,                   he.g.,   here.      l is also shown           and thehere.         OS kernel
                                                                            image,         are     not      relevant,                  as     secure             boot  5.1   per    High-Level
                                                                                                                                                                                    se    is    able      boils
                                                                                                                                                                                                          to   detect Properties
                                                                                                                                                                                                                            downadversarial             5.1 Security
                                                                                                                                                                                                                                                 naturally             High-Level
                                                                                                                                                                                                                                                                               to       the Property.
                                                                                                                                                                                                                                                                                           5.1          Properties
                                                                                                                                                                                                                                                                                                         High-Level
                                                                                                                                                                                                                                                                                                    requirement         We aimProperties  that to guarantee
                                                                                                                                                                                                                                                                                                                                                       the private              that keys our of    protocol
     Functional
           1. Other contents       correctness.
                                        in the NVM, e.g.,1.the               We
                                                                            Other
                                                                            behaviors    require
                                                                                bootloadercontents      1.and
                                                                                                   tampering
                                                                                                                 inPA-Boot
                                                                                                               Other  the
                                                                                                                        thewith   NVM,
                                                                                                                                 contents
                                                                                                                                   OS kernel   these
                                                                                                                                                     e.g.,intocertified
                                                                                                                                                            5.1
                                                                                                                                                                  the
                                                                                                                                                                 the  beNVM,     func-
                                                                                                                                                                           bootloader
                                                                                                                                                                           High-Level
                                                                                                                                                                                         e.g., the
                                                                                                                                                                                   contents
                                                                                                                                                                                                     andbootloader
                                                                                                                                                                                                         (see
                                                                                                                                                                                                              the OS kernel
                                                                                                                                                                                                                   Section
                                                                                                                                                                                                            Properties
                                                                                                                                                                                                                                        and the OSonly
                                                                                                                                                                                                                                      2.1).             Security     kernelallows authenticated AP to run on the device later in
                                                                                                                                                                                                                                                                                 Property.
                                                                                                                                                                                                                                                                                5.1            High-Level     We        aim         to
                                                                                                                                                                                                                                                                                                                               Properties   guarantee                   that       our     protocol
        image,     are not relevant,                               image,        areisnot         relevant,               asadversarial
                                                                                                                                 secure             boot per           Security
                                                                                                                                                                           se is able            Property.
                                                                                                                                                                                                toper     the
                                                                                                                                                                                                      detect          two
                                                                                                                                                                                                             se isadversarial We        aim
                                                                                                                                                                                                                                    toprocessors,     to      guarantee       RootCertHash stored in their bootROMs, our protoco
                                                                                                                                                                                                                                                                                            that
                                                                                                                                                                                                                                                                                           Security      our        protocol
                                                                                                                                                                                                                                                                                                                    Property.                  We        aim         to    guarantee               that
   1.tionally
        Other contents   correct,
                                in the NVM,  inas the
                                                   secure
                                                        e.g.,   boot
                                                             sense
                                                                 the     per se
                                                                             that
                                                                       bootloader
                                                                   behaviors
                                                                                           able
                                                                                           the
                                                                                             1.and
                                                                                        tampering
                                                                                                   image,
                                                                                                      to the
                                                                                                    Other  detect
                                                                                                        benignity    are
                                                                                                                    contents
                                                                                                                     OS
                                                                                                                    with
                                                                                                                                not
                                                                                                                                kernel
                                                                                                                                   these
                                                                                                                                           relevant,
                                                                                                                                               ofcertified
                                                                                                                                              in     the  the   NVM,as secure
                                                                                                                                                                        securitye.g., boot
                                                                                                                                                                          contents
                                                                                                                                                                       only
                                                                                                                                                                                         the
                                                                                                                                                                                    allows    (see bootloader
                                                                                                                                                                                                         Section
                                                                                                                                                                                                         authenticated
                                                                                                                                                                                                                        able  and
                                                                                                                                                                                                                           2.1).
                                                                                                                                                                                                                                         detect
                                                                                                                                                                                                                                        the       OSonly adversarial
                                                                                                                                                                                                                                                          kernelallows authenticated AP to run on the device later in
        behaviors       tampering          with     these
image, are not relevant, as secure boot per se is ableimage,   certified        contents           behaviors
                                                                                           to detect (see        Section
                                                                                                         areadversarial        tampering
                                                                                                                                       2.1).
                                                                                                                   not relevant, as secure boot per se is      with
                                                                                                                                                            Security       these       certified
                                                                                                                                                                                     Property.              contents
                                                                                                                                                                                                          and     We
                                                                                                                                                                                                             able to      the aim (see
                                                                                                                                                                                                                               detect          adversarial on
                                                                                                                                                                                                                                                  AP
                                                                                                                                                                                                                                            Section
                                                                                                                                                                                                                                           to       guarantee
                                                                                                                                                                                                                                         certificates        to 2.1).run         thatthe
                                                                                                                                                                                                                                                                                Security
                                                                                                                                                                                                                                                                                stored     onlyour  device
                                                                                                                                                                                                                                                                                                         allows
                                                                                                                                                                                                                                                                                                        in protocol
                                                                                                                                                                                                                                                                                                          Property.
                                                                                                                                                                                                                                                                                                                  the  laterauthenticated
                                                                                                                                                                                                                                                                                                                               NVM   in aim to AP
                                                                                                                                                                                                                                                                                                                                     We              remain               to run on
                                                                                                                                                                                                                                                                                                                                                                   guaranteeunchanged      thattheour     device
                                                                                                                                                                                                                                                                                                                                                                                                               protocol later in
     context
behaviors                remains
                 tampering         with these invariant                 duringbehaviors
                                                       certified contents                 (see any   Section      possible
                                                                                                                   tampering
                                                                                                                          2.1).                       execution
                                                                                                                                                   with     only theseallows  certified  ofauthenticated
                                                                                                                                                                                                  contents (see Section                AP to2.1).         run on the            onlydevice     allowslater        authenticated
                                                                                                                                                                                                                                                                                                                           in                           AP to run on the device later in
       PA-Boot:                                                                                                                                                                                     during all possible executions of PA-Boot:

       Property 1 (Functional Correctness w.r.t. Sh ).                                                                                                                                              Lemma 1 (Functional Correctness w.r.t. Sl ).
                                            A                                                                                                                                                                                         A
             ∀ π = s0 ,−
                       → sn ∈ Π, i ∈ [1, n]. B (Γsi ) ⇐⇒ B (Γs0 ) (†)                                                                                                                                            → sn ∈ Π, i ∈ [1, n]. si . env. nvm = s0 . env. nvm
                                                                                                                                                                                                       ∀ π = s0 ,−
       Recall that B(Γs0 ) = true iff the AP and the certificates                                                                                                                                        ∧ si . ap. private key = s0 . ap. private key
       in the NVM are genuine upon the start of PA-Boot, thereby                                                                                                                                         ∧ si . bsp. private key = s0 . bsp. private key
       witnessing the absence of adversarial behaviors (a). Provided                                                                                                                                     ∧ si . ap. root cert hash = s0 . ap. root cert hash
       a reasonable assumption that these two adversarial behaviors
       can only be conducted during the hardware supply chain, i.e.,                                                                                                                                     ∧ si . bsp. root cert hash = s0 . bsp. root cert hash
8                                                            IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. XX, NO. X



Security properties. In the presence of adversarial behav-              TABLE III: Proof efforts in Isabelle/HOL (∼7,100 LoC).
iors (a) and (b), we aim to establish – by the end of protocol
                                                                                     Specifications                     Proofs
execution – three types of security goals of the underlying            Level
security assets at the level of Sl :                                           #locale/definition     LoC    #property/lemma      LoC
  • Authenticity (against (a)): The identity of AP is validated.        Sh             1              ∼50          2              ∼50
  • Integrity (against (a) and (b)): The inter-processor com-           Sl            90              ∼850        304            ∼6,150
    munication packets and the certificates in NVM remain
    unmodified (even before the execution of PA-Boot).                Mechanized proof in Isabelle/HOL. In our specification
  • Confidentiality (against (b) for future executions): The          Sl , an agent BSP/AP can extend a trace (i.e., a run π of Sl )
    established shared session key Ks (for encrypting future          in any way permitted by the protocol. An adversarial behavior
    communication messages) is known only to BSP and AP.              can also change the current state and extend a trace. Low-level
The above-mentioned security goals are encoded as three               properties on both functional correctness and security are for-
individual lemmas interpreting different protocol-execution           malized as trace properties and proved by induction on traces
scenarios. Specifically, the protocol under normal execution          of Sl . In particular, security properties Lemmas 2.2 and 2.3
(cf. Lemma 2.1) should eventually terminate in the END                both cover different possible traces of Sl (corresponding to
state where the processors are mutually authenticated and             different attack scenarios). Therefore, we further decompose
Ks is established; otherwise, if an adversarial behavior that         these lemmas into a set of auxiliary lemmas to account for
violates either authenticity or certificate integrity is identified   different traces and prove by induction on each trace. Then,
– i.e., the AP has been replaced or the certificates in NVM           by chaining these auxiliary lemmas together in Isabelle/HOL,
have been tampered with (Lemma 2.2), or an inter-processor            we obtain a fully mechanized proof that all possible traces
communication packet has been modified by a man-in-the-               of Sl (i.e., all possible executions of PA-Boot) fulfill the
middle attack (cf. Lemma 2.3) – then the protocol should raise        requirements on functional correctness and security. Table III
error-specific alarms by visiting the ERR states and eventually       collects the statistics with regard to the proof efforts conducted
terminate in the ABORT state.                                         in Isabelle/HOL, which amount roughly to 8 person-months.
Lemma 2.1 (Security w.r.t. Sl under Normal Executions).
                                                                               VII. I MPLEMENTATION AND E VALUATION
∀ π ∈ Π. B (Γs0 ) ∧ M (π) =⇒ Tail (π) . status = END                     This section presents CPA-Boot, a proof-of-concept im-
Lemma 2.1 declares that starting from the initial state s0 where      plementation of PA-Boot embedded in multiprocessor secure
the associated security context is benign, if there is no man-        boot. To build confidence in the consistency of the formal
in-the-middle attack during the execution, PA-Boot must ter-          model and the implementation, we develop a test framework
minate in the END state signifying attack-free authentication         that extracts executable code from our Isabelle model Sl and
and the establishment of Ks .                                         validate it against CPA-Boot. We then evaluate the security
Lemma 2.2 (Security w.r.t. Sl against Tampered Configu-               and performance of CPA-Boot on ARM Fixed Virtual Plat-
rations).                                                             form (FVP) based on Fast Models 11.18 [42]. The tests are
            A                                                         conducted on the Foundation Platform [43] with ARM Cortex-
∀ π = s0 ,−
          → sn ∈ Π. ∃ i ∈ [1, n]. ¬B (Γs0 ) =⇒                        A72 CPUs, with CPU0 performing as BSP and CPU1 as AP.
                                                               
    Tail (π) . status = ABORT ∧ si . status = % ERR
where % matches A CERTS, B CERTS or RESP, see Fig. 5                  A. Proof-of-Concept Implementation
Lemma 2.2 states that in case Γs0 is compromised (due to                 We derive CPA-Boot in C (∼1,400 LoC) for the ARM64
adversarial behaviors (a) and attacker’s possible modification        bare-metal environment as an instance of the (low-level)
to necessary certificates in the NVM to impersonate a benign          formalization of PA-Boot in Isabelle/HOL. This instantiation
AP), PA-Boot should raise an error-specific alarm by visiting         is justified by a code-to-spec review in the same way as [36],
the corresponding ERR state until it eventually terminates in         establishing a near one-to-one correspondence between the
the ABORT state.                                                      formalization and the implementation, e.g., the correspondence
Lemma 2.3 (Security w.r.t. Sl against Man-in-the-Middle               between the events defined in Sl (see Sect. V-B) and the C
Attacks).                                                             functions declared in CPA-Boot. We build CPA-Boot using
                   A
         ∀ π = s0 ,−
                   → sn ∈ Π. ∃ i, j ∈ [1, n] s.t. i < j.              GCC 9.4.0 cross-compiler on a server running 64-bit Ubuntu
                                                                      20.04. CPA-Boot is further embedded in bootwrapper v0.2
         ¬M (π) =⇒        Tail (π) . status = ABORT ∧                 [44], a bootloader for the ARMv8 architecture, to perform
                                                              
         si . status = % ATTK ∧ sj . status = % ERR                   authentication at the initial boot stage. To use cryptographic
   where % matches CHAL, CHALRESP or RESP                             primitives in the boot environment, CPA-Boot adopts wolfSSL
Lemma 2.3 states that if a (challenge, challenge-response, or         5.3.0 [45]. Moreover, CPA-Boot uses Newlib 4.3.0 [46] as
response) packet is modified by a man-in-the-middle attack            the C standard library. Functional correctness of CPA-Boot is
(adversarial behavior (b)), PA-Boot should raise an error-            evaluated on the functional-accurate simulator FVP.
specific alarm by visiting the corresponding ERR state (after
                                                                      CPA-Boot bootloader. We integrate CPA-Boot at a later
the ATTK state) and finally terminate in the ABORT state.
                                                                      phase of bootwrapper such that necessary hardware initial-
                                                                      ization is finished before the execution of CPA-Boot. We
PA-BOOT: A FORMALLY VERIFIED AUTHENTICATION PROTOCOL FOR MULTIPROCESSOR SECURE BOOT UNDER HARDWARE SUPPLY-CHAIN ATTACKS                                              9



refer to the resulting bootloader as the CPA-Boot bootloader.                      Concrete                      CPA-Boot
                                                                                                                                               Output2
Upon the launch of CPA-Boot, both processors concurrently                         Input Test                  protocol_test_c      (C)

validate the other processor’s certificate until the initiation                                   manually implement

phase (cf. Sect. IV-A) is completed, i.e., when both processors                                                  PA-Boot                           compare
                                                                                                                                 (Isabelle/HOL)
have retrieved each other’s public key and the validations are                          instantiate            protocol_test                                 True/False

successful2 . During the challenge-response phase, both pro-                                                           automatically extract
cessors sequentially exchange encrypted packets (as the inter-                     Abstract                      PA-Boot
                                                                                                                                               Output1
processor communications cannot be parallelized) using asym-                      Input Test               protocol_test_OCaml    (OCaml)

metric cryptography, then establish a shared session key (in
                                                                                                        Fig. 6: Validation framework
the concurrent mode) to secure the communication channel.
Since FVP does not support inter-processor communication                          B. Validation Framework
buses, the channel is mimicked by the main memory where                              Here, we present the process to validate the consistency
both processors can read from and write to a pre-defined                          between the C implementation and Isabelle specification. A
memory location. Moreover, CPA-Boot uses Set Event (SEV)                          test framework is developed to extract executable OCaml code
and Wait For Event (WFE) instructions for inter-processor                         from our Isabelle model Sl and validate it against CPA-Boot,
synchronizations: after writing its packet to the channel, a                      covering both normal protocol execution and attack scenarios.
processor executes a SEV instruction to wake the other, then
immediately suspends itself by executing WFE.                                     Consistency validation. The validation is performed using
   CPA-Boot uses ECC for its asymmetric cryptographic                             an executable version generated in OCaml via Isabelle/HOL’s
operations due to its efficiency and security over RSA. It                        built-in extraction mechanism. Based on the extracted OCaml
employs elliptic-curve digital signature algorithm (ECDSA)                        code, as illustrated in Fig. 6, our validation framework operates
for certificate generation and validation, elliptic-curve Diffie-                 as follows. Our focus is on test cases that simulate normal
Hellman (ECDH) for secure key exchange, and ephemeral                             protocol execution as well as the actions of a skilled attacker
ECDH (ECDHE) for session key generation to ensure forward                         carrying out real attack effects, as described in Sect. VII-C.
secrecy. An ephemeral ECC key pair is generated using the P-                      Given an abstract input test case, the extracted OCaml function
256 curve, producing a 256-bit private key and its correspond-                    protocol test OCaml executes the test case and produces
ing public key. The shared session key, derived via ECDHE                         an output. Simultaneously, we instantiate the input test case
between BSP and AP, is also 256 bits. In the challenge-                           as corresponding concrete ones, and CPA-Boot produces an
response phase, each party computes a shared secret using                         output. If the two results match, the test is valid, demonstrating
ECDH with its private key and the other party’s public key.                       consistency between the two implementations. If the results
This shared secret is processed with HKDF-SHA256 to derive                        differ, the framework identifies an inconsistency between the
cryptographic keys. AES-128-CBC is used for data encryption,                      low-level C code and OCaml code (and, by extension, the
and HMAC-SHA256 ensures message authentication. These                             high-level Isabelle/HOL model).
operations, including HKDF-SHA256 and AES-128-CBC, are                               The OCaml implementation extracted from the formal
internally invoked by the wolfSSL library during ECDH                             model acts as a higher-level abstraction of the C implemen-
execution. Private keys, certificates, and hash values are linked                 tation. For instance, private keys are abstractly represented as
to the CPA-Boot bootloader during compilation and loaded                          an enumerated type with cases of ROOT PRIVK, M PRIVK,
into memory alongside it.                                                         S PRIVK and BAD PRIVK in Isabelle/HOL and thereby in
                                                                                  OCaml. The OCaml side uses BAD PRIVK to represent a
Library compatibility. We tune compile-time configurations                        scenario involving a tampered AP. In contrast, the C side
of the invoked libraries for compatibility with the bare-metal                    simulates an AP-replacement attack by statically linking a
environment: bootwrapper, Newlib, and wolfSSL are compiled                        modified private key file of CPU1.
with the flag -mstrict-align to disable unaligned accesses;                          In the OCaml implementation, the output result indicates
For Newlib, we adapt bootwrapper’s linker script to make                          whether the protocol reaches the terminal state with an END
memory-management functions such as malloc and free                               status or ABORT status. Similarly, in CPA-Boot, the result
work correctly, e.g., to avoid heap-memory conflicts; For                         reflects whether the protocol executes successfully and pro-
wolfSSL, we define compile-time macros to fit for the bare-                       gresses to the next boot stage, or aborts with a detected attack.
metal environment, which mainly include                                           The results demonstrate the consistency of the outputs for
  • NO FILESYSTEM to disable loading of keys and certifi-                         matching inputs across various scenarios particularly those
    cates in the system’s file system,                                            covered in Table IV, thereby increasing confidence in the
  • WOLFSSL USER IO to remove automatic setting of de-                            accuracy of our C implementation.
    fault I/O functions, and
  • NO WRITEV to disable writev semantics simulation.                             C. Security Evaluation
We further add macros to enable all ECC-related operations.                          We perform empirical security evaluations of CPA-Boot
The libraries are statically linked to CPA-Boot bootloader as                     to detect aforementioned adversarial behaviors simulated in
the bare-metal environment does not support dynamic load.                         FVP covering (a) and (b). In particular, we introduce an extra
  2 The processor that finishes the validation earlier than the other halts and   processor CPU2 mimicking the interposer chip to launch man-
waits for the other processor.                                                    in-the-middle attacks. As summarized in Table IV, CPA-Boot
10                                                          IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. XX, NO. X



TABLE IV: Instances of adversarial behaviors simulated via           TABLE V: #instructions consumed by the main boot stages,
FVP. Acronyms: APR for AP replacement, RCT for root-                 i.e., bootwrapper (b.w.p.), CPA-Boot, and Linux kernel boot.
certificate tampering, APCT for AP-certificate tampering, CPM
                                                                                            b.w.p.       CPA-Boot            Kernel boot        Overhead
for challenge-packet manipulation, CRPM for chal.-resp.-packet          Processor(s)
                                                                                             (α)            (β)                  (γ)            (β/(α+γ))
manipulation, and RPM for response-packet manipulation.
                                                                          CPU0              4,939        52,091,762         1,683,639,749          3.09%
          Category          (a)              (b)                          CPU1                650        52,181,244         1,759,591,720          2.97%
          Instance    APR RCT APCT     CPM CPRM RPM                    CPU0 ∥ CPU1          4,939⋆       87,570,653⋄        1,759,591,720⋆         4.98%
          Detected     ✓   ✓   ✓        ✓   ✓    ✓
                                                                     α, β, or γ denotes the number of instructions executed at each stage, respectively, e.g.,
                                                                         αCPU0 ∥ CPU1 for bootwrapper executed instructions of the dual-processor system.
succeeds in detecting all different instances of these adversarial     ⋆
                                                                         αCPU0 ∥ CPU1 = max{αCPU0 , αCPU1 } because bootwrapper is assumed to be fully
                                                                                parallelized. The same applies to the boot stage of the Linux kernel.
behaviors where the BSP returns error-specific alarms to             ⋄
                                                                       max{βCPU0 , βCPU1 } < βCPU0 ∥ CPU1 < βCPU0 + βCPU1 since CPA-Boot is partially
abort the boot process. We show below how the adversarial                parallelized, i.e., communications in the chal.-resp. phase must be in sequence.
behaviors are implemented and how CPA-Boot detects them.
AP replacement. We modify the private key PrivKAP of                                                                           ECCValid        ECCEnc
                                                                        CV0                                                    ECCDec          ECDHE
CPU1 to simulate the AP-replacement attack. Such attack does
                                                                                                                                               Others
not trigger alarms in certificate validation and CPA-Boot enters
                                                                        CV1
the challenge-response phase. In this phase, CPU1 attempts
to forge packets to pass the authentication. However, since
                                                                        CR0
the modified private key of CPU1 does not match the stored
certificate CertAP that has been validated in initiation phase,         CR1
CPU0 cannot decrypt the challenge packet and hence raises
an AP-replacement error and aborts the boot process.                          0               1               2                3               4     ·107
Man-in-the-middle attacks. CPU2 attempts to eavesdrop                                                       #instructions
on or tamper with the (challenge, challenge-response or re-          Fig. 7: #instructions by different operations in CPA-Boot.
sponse) packets transmitted over the inter-processor com-            CV0 denotes certificate validation in the initiation phase
munication channel (mimicked by memory) during protocol              performed by CPU0; CR0 denotes the challenge-response
execution. Particularly, for the latter two types of packets,        phase on CPU0. The notations for CPU1 are analogous. EC-
CPU2 acts as a skilled attacker who attempts to replace              CValid: ECC-based certificate verification; ECCEnc/ECCDec:
EPubKBSP in the challenge-response packet and EPubKAP in             ECC-based public-key encryption/decryption via the ECDH
the response packet aiming to establish a shared session key         algorithm; ECDHE: ECC-based key exchange, including the
for future communications. However, as the attacker does not         generation of ephemeral key pairs and Ks ; Others: memory
know the private keys of CPU0 and CPU1, he/she cannot                read/write, SHA-256 processing, etc.
manipulate the encrypted hash values of ephemeral public
keys. As a consequence, CPA-Boot observes unmatched hash             executed on FVP. To assess the impact of CPA-Boot on boot
values and thus raises an alarm and aborts the boot process.         performance, we additionally measure the boot process of a
                                                                     Linux system, namely, the Gentoo Linux distribution (stage
Tampering with certificates. We modify certificates                  archive 3, with systemd as init system, kernel version 5.16.0)
linked to CPA-Boot bootloader to simulate certificate ma-            [49]. Moreover, we disable Linux kernel PMU support to avoid
nipulations. Specifically, the attacker tries to modify the root     kernel’s modification on the PMU counters.
certificate or the AP certificate to bypass the processor authen-       Table V quantifies the experimental performance of the
tication in the challenge-response phase. However, since the         entire boot process averaged over three boot trials, consisting
attacker cannot modify the hash value of the root certificate        of three main boot stages, i.e., bootwrapper, CPA-Boot, and
stored in the bootROM, CPU0 detects the root-certificate             Linux kernel boot. The integration of CPA-Boot adds a 4.98%
manipulation using the hash and terminates the boot process.         overhead to the multiprocessor secure boot, roughly 3% per
For the AP-certificate manipulation, CPU0 uses the validated         CPU, which is relatively small. Moreover, we report the
root certificate to verify the manipulated AP certificate (signed    performance of different operations conducted in CPA-Boot.
by Certroot ) which leads to abortion as well.                       As depicted in Fig. 7, the main overhead of CPA-Boot stems
                                                                     from asymmetric cryptography used for certificate validation,
D. Performance Evaluation                                            packet encryption and decryption, and key exchange.
   we report the performance of CPA-Boot within a complete
boot process from bootloader to shell login on FVP. We                             VIII. D ISCUSSION AND F UTURE W ORK
measure the number of executed instructions rather than CPU            In this section, we briefly discuss some issues pertinent to
cycles of the boot process, as FVP is not cycle-accurate and         our approach and several interesting future directions.
each instruction takes equally one cycle to execute [47]. To
capture this, we enable performance monitor unit (PMU [48])          Hardware Adaptation. We implemented our protocol on
monitoring by setting a PMU control register at key points           FVP to demonstrate its security and usability. Here, we discuss
in the boot stages, recording the total number of instructions       how to deploy it on real hardware. Based on the analysis
PA-BOOT: A FORMALLY VERIFIED AUTHENTICATION PROTOCOL FOR MULTIPROCESSOR SECURE BOOT UNDER HARDWARE SUPPLY-CHAIN ATTACKS           11



of required components (highlighted in yellow in Fig. 2),           not optimal in terms of performance. A promising direction
we identify necessary hardware modifications during manu-           for future work is to derive verified C code. One approach is
facturing. The primary requirement is customizing the CPU           to extend Isabelle’s toolchain to directly synthesize C code, as
during manufacturing, specifically by embedding the PA-Boot         has been observed in [50]. To achieve this, we plan to refine
protocol code into the immutable bootROM. This is feasible          our low-level specification in Isabelle/HOL using the Simpl
since OEMs typically collaborate with silicon vendors for such      language [51] (with C-like syntax) and develop a verified com-
modifications. Additionally, the root certificate hash must be      piler from Simpl to C within Isabelle/HOL. Another option is
stored in the bootROM for processor certificate validation. The     to use the Igloo framework [52] to model our protocol and
OEM must modify the NVM to store certificates, which is             extend it to support our security properties. This would allow
easily reprogrammable. The generated session key does not           us to translate Isabelle’s formal specifications into program
require hardware modifications and can be stored in a CPU           assertions, which can then be verified with existing tools to
register to secure communication during the subsequent boot         ensure the C implementation meets the specified properties.
process. As noted in Sect. III-A, our approach is particularly      Alternatively, we could rewrite our protocol in Low* and use
useful when the OEM is located far from the end-user, such as       the KaRaMeL compiler [53] to generate certified C code.
overseas, and lacks full control over the supply chain. This is
essential for devices performing critical tasks, such as data                           IX. R ELATED W ORK
center servers that support enterprise workloads like cloud
services and big data processing.                                      This section reviews research closely related to our ap-
                                                                    proach, focusing on formal methods in bootstrap authentica-
Protocol Extensions. We envision three key extensions:              tion and protocol verification.
(i) PA-Boot applies to scenarios with multiple APs, allowing
the BSP to authenticate them sequentially. This aligns with         Secure Boot/Authenticated Load Verification. Formal
industrial practices, where systems in critical or embedded         methods have witnessed a spectrum of applications in en-
environments often perform sequential startups where BSP            hancing confidence in boot code security [54]–[56]. More
wakes up APs in sequence, to ensure control and simplify            pertinently to our work, Muduli et al. [57] verified the end-to-
debugging. Specifically, PA-Boot integrates into the boot           end security of authenticated firmware loaders using model-
process using a dedicated IPI channel for inter-processor           checking techniques [58]. The targeted scenarios and security
communication. After hardware initialization, APs enter a           properties are different from ours. Muduli et al. focuses on
suspended state, awaiting a startup signal from the BSP.            vulnerabilities such as protocol-state hijacking, time-of-check
The BSP activates each AP individually by setting its APIC          to time-of-use (TOCTOU), and confused deputy attacks during
ID in the APIC’s ICR register and then authenticates it. In         firmware loading, whereas our protocol ensures processor
contrast, simultaneous startups involve the BSP broadcasting        authenticity and inter-processor communication confidentiality
signals to initialize all APs concurrently, resulting in parallel   before firmware loading. Similar differences apply to [59],
authentication sessions. Addressing this scenario is part of our    which models firmware loading flows in Promela and verifies
future work. (ii) Another direction to extend our protocol is to    the absence of TOCTOU attacks using the Spin model checker
support a dual-return approach. Users can choose a permissive       [60]. Cremers et al. [61] formalized the SPDM 1.2 protocol
mode, which allows the boot process to continue despite             standard in the Tamarin prover [62]. SPDM aims for device
certain failures, and a strict mode, which aborts the process       attestation, authentication and secure communication and can
on any error. In scenarios with multiple APs, the permissive        be used during the boot process. However, due to its size and
mode can disable APs that fail verification, and allowing           complexity, the formalization is not fully verified. Although
the boot process to continue. Since PA-Boot executes before         they split the protocol into four separate models and verified
loading the bootloader or kernel image–when the system is           them separately, they do not analyze cross-protocol attacks or
vulnerable to attacks that could modify these components by         verify security properties on the complete model. In summary,
a malicious AP–disabling the APs at the end of PA-Boot              no existing work addresses defending against the hardware
prevents such attacks. (iii) Another potential extension is to      supply-chain attack surface, as identified in Sect. III-A.
incorporate bootROM integrity into the AP’s key derivation
                                                                    Protocol verification. Formal methods have been widely
process, protecting against very powerful attackers who can
                                                                    applied to ensure security of real-world protocols, like TLS
tamper with the bootROM. For example, the protocol could
                                                                    1.3 [63], messaging protocols [64], and entity authentication
employ Physically Unclonable Functions (PUFs) to dynami-
                                                                    protocols [65], [66]. There are dedicated tools for protocol
cally generate keys at runtime. The PUF response could be
                                                                    verification, such as Tamarin [62] and ProVerif [67]. However,
combined with the bootROM hash (e.g., using XOR or a key
                                                                    protocols verified in these frameworks are abstract models that
derivation function) to form the key. This ensures that any
                                                                    may not guarantee the same properties in actual implementa-
modification to the bootROM alters the AP’s derived private
                                                                    tions [68]. Works using F* [69], Coq, and Isabelle/HOL seek
key, allowing our protocol to detect bootROM compromise
                                                                    to address this limitation. Protocols in F* can be compiled
through a mismatch with the stored certificate CertAP .
                                                                    into OCaml or F# code, while protocols in Low* [70], a
C code generation. Our proof-of-concept prototype is im-            low-level subset of F*, can be translated into C via the
plemented in C to leverage its efficiency. While Isabelle/HOL’s     KaRaMeL compiler. Low* supports the development of high-
can generate executable code (e.g., in OCaml), this code is         assurance cryptographic libraries, such as HACL* [71], and
12                                                          IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, VOL. XX, NO. X



implementations of protocols like TLS 1.3 [72] and protocols                                       R EFERENCES
for measured boot [73] or bootloaders [74]. The DY* symbolic          [1] Z. Tao, A. Rastogi, N. Gupta, K. Vaswani, and A. V. Thakur, “DICE*: A
protocol framework [75], written in F*, combines the precision            formally verified implementation of DICE measured boot,” in USENIX
of dependent types from F* with the automation of symbolic                Security. USENIX Association, 2021, pp. 1091–1107.
                                                                      [2] J. D. Tygar and B. Yee, Dyad: A System for Using Physically Secure
execution in dedicated provers like Tamarin, offering efficient           Coprocessors. Carnegie Mellon University, 1991.
and expressive verification.                                          [3] J. Haj-Yahya, M. M. Wong, V. Pudi, S. Bhasin, and A. Chattopadhyay,
   The following discusses the most closely related works that            “Lightweight secure-boot architecture for RISC-V system-on-chip,” in
                                                                          ISQED. IEEE, 2019, pp. 216–223.
formalize protocols using Isabelle/HOL and probably derive            [4] O. Shwartz, A. Cohen, A. Shabtai, and Y. Oren, “Shattered Trust: When
verified implementation.                                                  replacement smartphone components attack,” in WOOT.             USENIX
   Paulson’s seminal work [76], [77] uses an inductive ap-                Association, 2017.
                                                                      [5] F. Bohling, T. Mueller, M. Eckel, and J. Lindemann, “Subverting Linux’
proach to model network protocols and prove their security                integrity measurement architecture,” in ARES. ACM, 2020, pp. 27:1–
properties. However, it does not verify our security properties           27:10.
Lemma 2.2 and Lemma 2.3, which ensures that once an                   [6] J. P. Skudlarek, T. Katsioulas, and M. Chen, “A platform solution
                                                                          for secure supply-chain and chip life-cycle management,” Computer,
adversarial behavior is performed during protocol execution,              vol. 49, no. 8, pp. 28–34, 2016.
the protocol should detect it at some later state along the trace,    [7] J. Christensen, I. M. Anghel, R. Taglang, M. Chiroiu, and R. Sion,
and ultimately terminate in an error state and trigger an alarm.          “DECAF: Automatic, adaptive de-bloating and hardening of COTS
                                                                          firmware,” in USENIX Security. USENIX Association, 2020, pp. 1713–
These properties are crucial for identifying attack vectors and           1730.
preventing attackers from gaining control of the system.              [8] S. N. Dhanuskodi, X. Li, and D. Holcomb, “COUNTERFOIL: Verifying
                                                                          provenance of integrated circuits using intrinsic package fingerprints
   Igloo [52] also uses Isabelle/HOL with multiple specifica-             and inexpensive cameras,” in USENIX Security. USENIX Association,
tion layers and guides the correctness proof of implementa-               2020, pp. 1255–1272.
tion code but follows a different approach. It establishes a          [9] Z. Han, M. Yasin, and J. J. Rajendran, “Does logic locking work with
                                                                          EDA tools?” in USENIX Security. USENIX Association, 2021, pp.
compositional refinement framework using forward simulation               1055–1072.
to prove refinement between layers. The soundness theorem            [10] J. F. Miller, “Supply chain attack framework and attack patterns,” 2013.
establishes that refinement implies trace inclusion. Igloo shows     [11] M. Gaithersburg, “Guide for conducting risk assessments,” 2012.
                                                                     [12] K. Shiralkar, A. Bongale, S. Kumar, K. Kotecha, and C. Prakash, “As-
that the abstract protocol model satisfies a trace property,              sessment of the benefits of information and communication technologies
while the lower layer, though introducing more events, refines            (ICT) adoption on downstream supply chain performance of the retail
the higher layer and preserves the trace property. In con-                industry,” Logistics, vol. 5, no. 4, p. 80, 2021.
                                                                     [13] R. Naraine, “U.S. gov issues stark warning, calling firmware security
trast, our work leverages Isabelle’s built-in locale module for           a ’single point of failure’,” 2022, accessed: 2025-02-01. [Online].
abstraction-refinement reasoning. Unlike Igloo, which is based            Available: https://www.securityweek.com/us-gov-issues-stark-warning-
on Paulson’s approach, our work verifies security properties              calling-firmware-security-single-point-failure
                                                                     [14] J. Jaeger, “A wake-up call in cyber supply-chain risk,”
Lemma 2.2 and Lemma 2.3. While both link high-level                       COMPLIANCE WEEK 2018, accessed: 2025-02-01. [Online].
models to low-level implementations, Igloo manually converts              Available: https://www.complianceweek.com/a-wake-up-call-in-cyber-
formal requirements defined in Isabelle into program speci-               supply-chain-risk/2106.article
                                                                     [15] J. Frazelle, “Securing the boot process: The hardware root of trust,”
fications annotated in programs and uses tools like VeriFast              Commun. ACM, vol. 63, no. 3, pp. 38–42, 2020.
for verification. Our approach prioritizes automation, ensuring      [16] B. Meadows, N. Edwards, and S.-Y. Chang, “On-Chip randomization for
consistency between formal specification and implementation               memory protection against hardware supply chain attacks to DRAM,”
through extracted executable code and testing.                            in SPW. IEEE, 2020, pp. 171–180.
                                                                     [17] A. C. Sant’Ana, H. M. Medina, K. B. Fiorentin, and F. G. Moraes,
                                                                          “Lightweight security mechanisms for MPSoCs,” in SBCCI. ACM,
                                                                          2019, pp. 1–6.
                       X. C ONCLUSION                                [18] D. Mehta, H. Lu, O. P. Paradis, M. A. M. S., M. T. Rahman, Y. Iskander,
                                                                          P. Chawla, D. L. Woodard, M. M. Tehranipoor, and N. Asadizanjani,
                                                                          “The Big Hack explained: Detection and prevention of PCB supply chain
   We have identified a new, prevalent hardware supply-chain              implants,” ACM J. Emerg. Technol. Comput. Syst., vol. 16, no. 4, pp.
attack surface that can bypass multiprocessor secure boot due             42:1–42:25, 2020.
to the absence of processor-authentication mechanisms. To            [19] T. Hudson, “Lecture: Modchips of the state,” in CCC, 2018.
                                                                     [20] T. Mosavirik, P. Schaumont, and S. Tajik, “Impedanceverif: On-chip
defend against these attacks targeting “assumed-safe” com-                impedance sensing for system-level tampering detection,” TCHES, 2022.
ponents (e.g., processors and inter-processor communication          [21] U. D. O. COMMERCE and U. D. O. H. SECURITY, “Assessment
channels), we presented PA-Boot, the first formally verified              of the critical supply chains supporting the u.s.information
                                                                          and communications technology industry,” accessed: 2025-02-
processor-authentication protocol for multiprocessor secure               01. [Online]. Available: https://www.dhs.gov/sites/default/files/2022-
bootstrap. We showed – using a machine-checked mathemat-                  02/ICT%20Supply%20Chain%20Report 0.pdf
ical proof in Isabelle/HOL – that PA-Boot is functionally            [22] J. Zhu, A. Luo, G. Li, B. Zhang, Y. Wang, G. Shan, Y. Li, J. Pan,
                                                                          C. Deng, S. Yin et al., “Jintide: Utilizing low-cost reconfigurable
correct and is guaranteed to detect multiple adversarial be-              external monitors to substantially enhance hardware security of large-
haviors, e.g., man-in-the-middle attacks and processor replace-           scale cpu clusters,” IEEE Journal of Solid-State Circuits, vol. 56, no. 8,
ments. Experiments on ARM FVP suggested that our proof-                   pp. 2585–2601, 2021.
                                                                     [23] T. Nipkow, L. C. Paulson, and M. Wenzel, Isabelle/HOL - A Proof
of-concept implementation CPA-Boot can effectively identify               Assistant for Higher-Order Logic, ser. LNCS. Springer, 2002, vol.
boot-process attacks with a minor overhead and thereby im-                2283.
prove the bootstrap security of multiprocessor systems.              [24] O. Khalid, C. Rolfes, and A. Ibing, “On implementing trusted boot for
                                                                          embedded systems,” in HOST. IEEE, 2013, pp. 75–80.
   Future work includes expanding the functionality of               [25] A. Marchand, Y. Imine, H. Ouarnoughi, T. Tarridec, and A. Gallais,
PA-Boot and generating verified C code (see Sect. VIII).                  “Firmware integrity protection: A survey,” IEEE Access, 2023.
PA-BOOT: A FORMALLY VERIFIED AUTHENTICATION PROTOCOL FOR MULTIPROCESSOR SECURE BOOT UNDER HARDWARE SUPPLY-CHAIN ATTACKS                                        13



[26] A.      L.      Sacco       and     A.      A.      Ortega,     “Persistent   [53] “KaRaMeL,” accessed: 2025-02-01. [Online]. Available: https://
     bios     infection,”     2009,     accessed:     2025-02-01.      [Online].        github.com/FStarLang/karamel
     Available: https://www.coresecurity.com/sites/default/files/private-files/    [54] Z. Straznickas, “Towards a verified first-stage bootloader in Coq,” Ph.D.
     publications/2016/05/Persistent-BIOS-Infection.pdf                                 dissertation, Massachusetts Institute of Technology, 2020.
[27] “Platform security boot guide,” 2020, accessed: 2025-02-01. [Online].         [55] B. Cook, K. Khazem, D. Kroening, S. Tasiran, M. Tautschnig, and
     Available: https://developer.arm.com/documentation/den0072/0101/                   M. R. Tuttle, “Model checking boot code from AWS data centers,” Form.
[28] E. Paul, M. Andrey, M. Dennis, S. Rob, T. Stefan, and W. David,                    Methods Syst. Des., pp. 1–19, 2020.
     “RIoT–a foundation for trust in the internet of things,” 2020,                [56] B.-Y. Huang, S. Ray, A. Gupta, J. M. Fung, and S. Malik, “Formal
     accessed: 2025-02-01. [Online]. Available: https://www.microsoft.com/              security verification of concurrent firmware in SoCs using instruction-
     en-us/research/wp-content/uploads/2016/06/RIoT20Paper-1.1-1.pdf                    level abstraction for hardware,” in DAC. IEEE, 2018, pp. 1–6.
[29] J. Kirk, “TCG specification TPM 2.0 mobile reference                          [57] S. K. Muduli, P. Subramanyan, and S. Ray, “Verification of authenticated
     architecture,” 2014, accessed: 2025-02-01. [Online]. Avail-                        firmware loaders,” in FMCAD. IEEE, 2019, pp. 110–119.
     able: https://trustedcomputinggroup.org/wp-content/uploads/TPM-2-0-           [58] C. Baier and J. Katoen, Principles of Model Checking. MIT Press,
     Mobile-Reference-Architecture-v2-r142-Specification FINAL2.pdf                     2008.
[30] S. Zhao, Q. Zhang, G. Hu, Y. Qin, and D. Feng, “Providing root of             [59] S. Krstić, J. Yang, D. W. Palmer, R. B. Osborne, and E. Talmor, “Security
     trust for arm trustzone using on-chip sram,” in Proceedings of the 4th             of SoC firmware load protocols,” in HOST. IEEE, 2014, pp. 70–75.
     International Workshop on Trustworthy Embedded Devices, 2014, pp.             [60] G. J. Holzmann, “The model checker SPIN,” IEEE Trans. Software Eng.,
     25–36.                                                                             vol. 23, no. 5, pp. 279–295, 1997.
[31] A. D. Zonenberg, A. Moor, D. Slone, L. Agan, and M. Cop, “Extraction          [61] C. Cremers, A. Dax, and A. Naska, “Formal analysis of SPDM:
     of secrets from 40nm cmos gate dielectric breakdown antifuses by fib               Security protocol and data model version 1.2,” in 32nd USENIX Security
     passive voltage contrast,” arXiv preprint arXiv:2501.13276, 2025.                  Symposium (USENIX Security 23), 2023, pp. 6611–6628.
[32] F. Courbon, “Practical partial hardware reverse engineering analysis: For     [62] B. Schmidt, S. Meier, C. Cremers, and D. A. Basin, “Automated analysis
     local fault injection and authenticity verification,” Journal of Hardware          of Diffie-Hellman protocols and advanced security properties,” in CSF.
     and Systems Security, vol. 4, no. 1, pp. 1–10, 2020.                               IEEE, 2012, pp. 78–94.
[33] B. Gassend, D. Clarke, M. Van Dijk, and S. Devadas, “Silicon physical         [63] C. Cremers, M. Horvat, S. Scott, and T. van der Merwe, “Automated
     random functions,” in Proceedings of the 9th ACM Conference on                     analysis and verification of TLS 1.3: 0-RTT, resumption and delayed
     Computer and Communications Security, 2002, pp. 148–160.                           authentication,” in S&P. IEEE, 2016, pp. 470–485.
[34] V. Young, P. J. Nair, and M. K. Qureshi, “DEUCE: write-efficient              [64] N. Kobeissi, K. Bhargavan, and B. Blanchet, “Automated verification
     encryption for non-volatile memories,” in ASPLOS. ACM, 2015, pp.                   for secure messaging protocols and their implementations: A symbolic
     33–44.                                                                             and computational approach,” in EuroS&P. IEEE, 2017, pp. 435–450.
[35] A. Awad, P. K. Manadhata, S. Haber, Y. Solihin, and W. G. Horne,              [65] D. A. Basin, J. Dreier, L. Hirschi, S. Radomirovic, R. Sasse, and
     “Silent shredder: Zero-cost shredding for secure non-volatile main                 V. Stettler, “A formal analysis of 5G authentication,” in CCS. ACM,
     memory controllers,” in ASPLOS. ACM, 2016, pp. 263–276.                            2018, pp. 1383–1396.
[36] Y. Zhao, D. Sanán, F. Zhang, and Y. Liu, “Refinement-based spec-             [66] C. Sprenger and D. A. Basin, “Developing security protocols by refine-
     ification and security analysis of separation kernels,” IEEE Trans.                ment,” in CCS. ACM, 2010, pp. 361–374.
     Dependable Secure Comput., vol. 16, no. 1, pp. 127–141, 2017.                 [67] B. Blanchet, “An efficient cryptographic protocol verifier based on
[37] C. Hawblitzel, J. Howell, M. Kapritsos, J. R. Lorch, B. Parno, M. L.               Prolog rules,” in CSFW. IEEE, 2001, pp. 82–96.
     Roberts, S. T. V. Setty, and B. Zill, “IronFleet: Proving practical           [68] L. Arquint, F. A. Wolf, J. Lallemand, R. Sasse, C. Sprenger, S. N.
     distributed systems correct,” in SOSP. ACM, 2015, pp. 1–17.                        Wiesner, D. A. Basin, and P. Müller, “Sound verification of security
[38] W. Diffie and M. E. Hellman, “New directions in cryptography,” IEEE                protocols: From design to interoperable implementations,” in SP, CA,
     Trans. Inf. Theory, vol. 22, no. 6, pp. 644–654, 1976.                             USA, May 21-25, 2023. IEEE, 2023, pp. 1077–1093.
[39] C. Ballarin, “Interpretation of locales in Isabelle: Theories and proof       [69] N. Swamy, J. Chen, C. Fournet, P.-Y. Strub, K. Bhargavan, and J. Yang,
     contexts,” in MKM, ser. LNCS, vol. 4108. Springer, 2006, pp. 31–43.                “Secure distributed programming with value-dependent types,” ACM
[40] F. Haftmann and T. Nipkow, “A code generator framework for Is-                     SIGPLAN Notices, vol. 46, no. 9, pp. 266–278, 2011.
     abelle/HOL,” in Theorem Proving in Higher Order Logics: Emerging              [70] J. Protzenko, J.-K. Zinzindohoué, A. Rastogi, T. Ramananandro,
     Trends Proceedings, vol. 8, 2007, p. 121.                                          P. Wang, S. Zanella-Béguelin, A. Delignat-Lavaud, C. Hriţcu, K. Bhar-
[41] D. Dolev and A. C. Yao, “On the security of public key protocols,” in              gavan, C. Fournet et al., “Verified low-level programming embedded in
     SFCS. IEEE Computer Society, 1981, pp. 350–357.                                    f,” Proceedings of the ACM on Programming Languages, vol. 1, no.
[42] “Fast Models Fixed Virtual Platforms reference guide,” accessed: 2025-             ICFP, pp. 1–29, 2017.
     02-01. [Online]. Available: https://developer.arm.com/documentation/          [71] J.-K. Zinzindohoué, K. Bhargavan, J. Protzenko, and B. Beurdouche,
     100966/latest                                                                      “HACL*: A verified modern cryptographic library,” in Proceedings of
[43] “Foundation Platform user guide,” accessed: 2025-02-01. [Online].                  the 2017 ACM SIGSAC Conference on Computer and Communications
     Available: https://developer.arm.com/documentation/100961/1118/                    Security, 2017, pp. 1789–1806.
[44] “Linux kernel bootwrapper,” accessed: 2025-02-01. [Online]. Avail-            [72] A. Delignat-Lavaud, C. Fournet, M. Kohlweiss, J. Protzenko, A. Rastogi,
     able: https://git.kernel.org/pub/scm/linux/kernel/git/mark/boot-wrapper-           N. Swamy, S. Zanella-Béguelin, K. Bhargavan, J. Pan, and J. K.
     aarch64.git/                                                                       Zinzindohoue, “Implementing and proving the TLS 1.3 record layer,”
[45] “wolfSSL embedded SSL/TLS library,” accessed: 2025-02-01. [Online].                in 2017 IEEE Symposium on Security and Privacy (SP). IEEE, 2017,
     Available: https://github.com/wolfSSL/wolfssl                                      pp. 463–482.
[46] “Newlib,” accessed: 2025-02-01. [Online]. Available: https:                   [73] J. Protzenko, B. Beurdouche, D. Merigoux, and K. Bhargavan, “Formally
     //www.sourceware.org/newlib/                                                       verified cryptographic web applications in WebAssembly,” in 2019 IEEE
[47] “FVP       reference     guide,”    accessed:     2025-02-01.     [Online].        Symposium on Security and Privacy (SP). IEEE, 2019, pp. 1256–1274.
     Available: https://developer.arm.com/documentation/100966/1100-00/            [74] S. Yuan and J.-P. Talpin, “Verified functional programming of an iot
     Programming-Reference-for-VE-FVPs/Differences-between-the-VE-                      operating system’s bootloader,” in Proceedings of the 19th ACM-IEEE
     hardware-and-the-system-model/Restrictions-on-the-processor-models                 International Conference on Formal Methods and Models for System
[48] “Performance monitoring unit,” accessed: 2025-02-01. [On-                          Design, 2021, pp. 89–97.
     line]. Available: https://developer.arm.com/documentation/100511/             [75] K. Bhargavan, A. Bichhawat, Q. H. Do, P. Hosseyni, R. Küsters,
     0401/performance-monitoring-unit                                                   G. Schmitz, and T. Würtele, “DY*: A modular symbolic verification
[49] “Gentoo Linux,” accessed: 2025-02-01. [Online]. Available: http:                   framework for executable cryptographic protocol code,” in 2021 IEEE
     //www.gentoo.org/                                                                  European Symposium on Security and Privacy (EuroS&P). IEEE, 2021,
[50] Y. Zhang, Y. Zhao, and D. Sanán, “A verified Timsort C implementation             pp. 523–542.
     in Isabelle/HOL,” CoRR, vol. abs/1812.03318, 2018.                            [76] L. C. Paulson, “The inductive approach to verifying cryptographic
[51] N. Schirmer, “Verification of sequential imperative programs in Is-                protocols,” J. Comput. Secur., vol. 6, no. 1-2, pp. 85–128, 1998.
     abelle/HOL,” Ph.D. dissertation, Technical University Munich, 2006.           [77] ——, “Inductive analysis of the internet protocol TLS,” ACM Trans. Inf.
[52] C. Sprenger, T. Klenze, M. Eilers, F. A. Wolf, P. Müller, M. Clochard,            Syst. Secur., vol. 2, no. 3, pp. 332–351, 1999.
     and D. Basin, “Igloo: soundly linking compositional refinement and
     separation logic for distributed system verification,” Proceedings of the
     ACM on Programming Languages, vol. 4, no. OOPSLA, pp. 1–31, 2020.
