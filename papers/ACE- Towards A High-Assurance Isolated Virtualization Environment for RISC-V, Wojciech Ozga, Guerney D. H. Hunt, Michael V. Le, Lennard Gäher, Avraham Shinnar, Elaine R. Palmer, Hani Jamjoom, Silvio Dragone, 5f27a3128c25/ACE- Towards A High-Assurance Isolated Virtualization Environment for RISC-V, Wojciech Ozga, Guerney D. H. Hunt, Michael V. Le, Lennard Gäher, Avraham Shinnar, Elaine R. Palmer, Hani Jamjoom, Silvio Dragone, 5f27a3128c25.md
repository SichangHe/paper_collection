                                             ACE: Towards A High-Assurance Isolated Virtualization Environment
                                                                      for RISC-V
                                                Wojciech Ozga                         Guerney D. H. Hunt                                      Michael V. Le
                                             IBM Research — Zürich             IBM T.J. Watson Research Center                      IBM T.J. Watson Research Center

                                               Lennard Gäher                       Avraham Shinnar                                        Elaine R. Palmer
                                              MPI-SWS, Germany               IBM T.J. Watson Research Center                       IBM T.J. Watson Research Center
                                                                          Hani Jamjoom                                       Silvio Dragone
                                                                 IBM T.J. Watson Research Center                          IBM Research — Zürich
                                                                                                August 11, 2026
arXiv:2505.12995v2 [cs.CR] 10 Aug 2026




                                         Abstract                                                                dresses both problems (confidentiality and verification effi-
                                                                                                                 cacy) simultaneously. By compartmentalizing software into
                                         Confidential computing has proven its value in cloud environ-           isolated security domains with narrow, well-defined interfaces,
                                         ments, but its potential for securing edge and high-end embed-          it confines the impact of any compromise to a single domain
                                         ded systems (e.g., automotive controllers, cryptographic accel-         and reduces the scope of what must be verified to each domain
                                         erators, telco infrastructure) remains largely unexplored. We           individually.
                                         present ACE, an open-source, royalty-free virtualization-based             Safety- and security-critical systems that must conform with
                                         confidential computing system for RISC-V targeting these en-            regulations [28, 57, 20, 23] can directly benefit, because these
                                         vironments. ACE isolates software into confidential virtual             regulations mandate extensive testing and recommend or re-
                                         machines with narrow, well-defined interfaces, building ex-             quire formal methods. For example, EAL7, the most stringent
                                         clusively on commodity RISC-V hardware without specialized              Common Criteria [20] evaluation level, requires mathematical
                                         hardware extensions or licensing fees. Our prototype evalua-            proofs of system security properties that are hard to achieve
                                         tion on the first commercially available RISC-V hardware sup-           for complex systems because proof sizes grow with the square
                                         porting virtualization shows that ACE is a viable candidate for         of the specification size [52], which itself grows with the code-
                                         our target systems.                                                     base. Compartmentalization reduces this cost by limiting what
                                                                                                                 must be proved per domain.
                                         1     Introduction                                                         This benefit, however, only materializes if the components
                                                                                                                 enforcing isolation are themselves verifiable. The challenge
                                         Building mission-critical systems and confirming their safety           here is foundational: security proofs are not flat but layered,
                                         and security properties has become increasingly challenging             with each property depending on those below. A single in-
                                         due to growing software size, shrinking budgets, time-to-               struction in a memory-unsafe language can violate memory
                                         market pressures, and talent shortages. The growing frequency           safety and collapse every security argument built on top of it.
                                         of cyberattacks [74, 77, 65, 21, 76, 11] confirms the urgency.          Achieving high assurance therefore requires a system designed
                                         Modern systems are composed of hundreds to thousands of                 from the ground up to keep each layer tractable. We observe
                                         software and hardware components from different vendors,                that a common isolation mechanism designed for verifiability,
                                         making it difficult to not only protect confidential IPs but also       with a small, extendable core, narrow interfaces, and memory-
                                         reason about correctness of the whole system. During verifi-            safe implementation, can serve as a reusable foundation that
                                         cation, all interactions between components must be checked,            different mission-critical systems build upon, inheriting its se-
                                         causing verification costs to explode or even make the verifi-          curity guarantees rather than reproving them from scratch, di-
                                         cation process infeasible.                                              rectly reducing costs and accelerating the certification process.
                                            Consequently, the verification phase may be shortened or                Realizing this vision on RISC-V, however, requires closing
                                         eliminated to meet deadlines or cost targets, leaving unde-             a gap. Despite rapid expansion of RISC-V into safety-critical
                                         tected memory safety bugs or security backdoors in the sys-             infrastructure, e.g., automotive and telco [60, 50, 79, 72], the
                                         tem [58, 55]. We argue that confidential computing [17] ad-             ecosystem still lacks confidential computing technology suited


                                                                                                             1
                                                                                                            3                                  4 TEE virtual machine VU
for these edge and high-end embedded RISC-V systems that                                                        virtual machine                            (TVM)                 VS
operate with limited power and silicon budgets. We introduce                                                3
                                                                                                                  hypervisor                                                     HS
ACE to close this gap. Commercial confidential computing for
x86 [14, 71], IBM Z [7], or IBM POWER [39] targets high-                          2         TSM                                2 TEE security manager
                                                                                                                                                                                  M
end server processors in data centers, while ARM’s solution                        initialization code                                      (TSM)

requires dedicated hardware and additional licensing costs [1].        1                                       RISC-V hardware
                                                                          [Processor with root of trust, memory access control, interrupt handler, hypervisor extension]
ACE, by contrast, is open-source and royalty-free, and runs on
                                                                             - trusted                   - untrusted      - isolation enforced by TSM          - control ow direction
commodity RISC-V hardware. ACE’s design has contributed                        component             fl
                                                                                                           component

to the RISC-V CoVE specification [9]. The page management Figure 1: High-level overview of ACE, a VM-based confi-
subsystem (8% of the codebase) has been formally verified for dential computing targeting RISC-V. The TSM (➋) leverages
memory safety and functional correctness.                           hardware features (➊) to multiplex execution of different secu-
    As part of our work on ACE, we developed a set of prin- rity domains (➌) and (➍) on top of the same hardware while
ciples and a methodology that we believe are universal and preserving security guarantees.
provide a basis for the design and development of firmware
that requires verification. These principles enable system de- 2 Overview of ACE
signers and developers to choose a tradeoff between resources
invested in verification and the obtained assurance level. For ACE brings virtual machine (VM)-based confidential comput-
example, they might rely on strongly typed, memory-safe pro- ing capabilities to edge and high-end embedded RISC-V sys-
gramming languages and their compilers for memory safety tems. Like in other such architectures, a hypervisor manages
while harnessing proper encapsulation techniques with deduc- the VM’s lifecycle but is not part of the trusted computing base
tive verification to prove correctness of a small set of tradition- (TCB). ACE utilizes firmware and hardware to build a trusted
ally error-prone unsafe operations. We applied these principles execution environment (TEE) [29].
during the design and development of ACE, achieving a rela-            Figure 1 shows a high-level overview of the architecture,
tively high level of trust by design, even before the full formal which consists of four components: (➊) hardware, (➋) TEE
verification is complete.                                           security manager (TSM), (➌) hypervisor with virtual machines
                                                                                                                                                                1
    To demonstrate maturity and functional readiness of the (VMs), and (➍) TEE virtual machines (TVMs). The TSM’s
ACE implementation, we ran and evaluated multi-processor goal is to isolate security domains from each other. The hy-
Linux-based confidential virtual machines (VMs) on the first pervisor and normal VMs constitute one security domain and
RISC-V hardware available on the market that supports vir- each TVM constitutes a distinct security domain. The TSM is
tualization. The results show that ACE incurs low perfor- a piece of code that switches execution of a security domain’s
mance overhead for CPU-intensive workloads and up to 48% (a TVM or the hypervisor) context and ensures that only al-
overhead for multi-vCPU network-intensive workloads, re- lowed information is exchanged. It achieves this by reconfig-
sults in line with commercial confidential computing technolo- uring the hardware to enable proper access controls and clear-
gies [54, 83]. I/O performance could further be improved ing the execution state so that there are no execution traces left
with dedicated hardware extensions to avoid extra copies via when another security domain resumes.
bounce buffers.                                                        To maintain full control over the hardware’s state and con-
                                                                    figuration, the TSM asserts control of the system during the
Our contributions:                                                  early boot process and retains its privileged role during the sys-
• Define principles and methodology to guide design of high- tem’s lifetime. This role allows it to enforce access controls by
   assurance low-level systems (§3) and applied them to build switching processor privilege modes, applying memory access
   ACE, an open-source, royalty-free, virtualization-based con- controls, and taking control over interrupts.
   fidential computing for edge and high-end embedded RISC-
   V systems (§3.2, §4).                                            2.1 Open Source and Compliance
                                                                 ACE complies with the RISC-V CoVE specification [9] and
• Provide the first evaluation of virtualization-based confiden- builds on top of the canonical architecture [62], which speci-
  tial computing on the first commercially available RISC-V fies the minimal set of features needed for a confidential com-
  hardware supporting virtualization (§5).                       puting system. The simplicity of this design aims to streamline
                                                                 the formal verification process, while compliance with stan-
                                                                 dards should facilitate adoption. The project’s open-source
• Extend the RISC-V CoVE specification with the ACE’s
                                                                    1 We follow the nomenclature used in the RISC-V CoVE [9] and
  unique design points, such as single-step TVM promotion,
                                                                 TDISP [63] specifications. In the literature, one can also find the terms CVMs,
  static memory partitioning, and local attestation. We extend SVMs, or enclaves, as well as security monitor, security manager, or isolation
  the Linux CoVE patches to support these features.              monitor.


                                                                                         2
                                                                                                 Requirements
nature encourages community participation, leading to exten-                               e.g., hardware constraints
                                                                                                  & threat model
                                                                                                                                           Proofs
sions that improve use-case-specific performance.                            Informal                                    simplify      (Proof engineer)
                                                                           invariants &                                                                             Formal model
                                                                          speci cations                                 interfaces                                 & proof checking
                                                                                                                                                              x
                                                                           e.g., memory                                                                     bugs
                                                                            partitioning
                                                                                                    System
2.2   Threat Model                                                                                  design                           Implementation                   Continuous
                                                                                                                                                                    integration with
                                                                                 Software                                                                              veri cation
                                                                               architecture
We assume a software-level adversary whose goal is to com-                    e.g., nite state
                                                                                 machine
promise a victim’s TVM, specifically (1) by tampering with                                       Modularization              Software              Formal              Binary
                                                                                                 e.g., page token          development          speci cations        compilation
                                                                                                                         (system engineer)     (proof engineer)
the TVM’s execution integrity by modifying its control or data           fi    fi fi
                                                                                   fi




flow execution, (2) by reading the confidential TVM’s data, or         Figure 2: Our methodology to develop formally verified low-
(3) by impersonating the victim’s TVM to its owner. ACE’s              level computing systems.
security goal is that the adversary learns nothing about the
TVM’s state beyond what passes through an explicitly reclas-           capabilities of target systems, it also poses greater challenges
sified channel.                                                        for ensuring the desired security.
   We assume an adversary who has root access to the hyper-
visor and might run her own TVMs concurrently and in paral-            Formal verification scales best when the verification can be
lel with victim’s TVMs. She can also control the lifecycle of          modularized with clear abstraction boundaries, making rea-
victim’s TVMs and input data via hypervisor-controlled regis-          soning about system invariants local. More complex represen-
ters, shared memory buffers, virtual I/O devices, or the initial       tation invariants (e.g., due to low-level memory hacks) com-
TVM’s image state and the flattened device tree (FDT).                 plicate reasoning.
   We exclude micro-architectural side-channel attacks [43,               Achieving ACE’s goal while satisfying the above con-
10] because these attacks require separate hardware miti-              straints requires tradeoffs. We define the following guiding
gations such as speculation barriers and cache partitioning,           principles to navigate these tradeoffs effectively and justify the
which are orthogonal to ACE’s isolation mechanisms and can             design decisions described in §3.2.
be applied independently. We also exclude from the threat
model physical attacks on memory, buses, and processors,               P1: Design a small modular core that targets a simple, well-
because of the existence of well-known counter-measures,                   defined hardware baseline, while remaining extensible to
e.g., fault-detection mechanisms like lockstep, error correction           more complex use cases and hardware.
code-protected memory, or encrypted buses. These technolo-
gies should be implemented separately for target systems and           P2: Minimize cross-domain interactions to make formal ver-
do not require changes to the TSM.                                         ification achievable.

                                                                       P3: Encapsulate complex operations with clearly defined
                                                                           boundaries (modularity, extensibility to satisfy formal
3     Design                                                               verification requirements).
The design principles outlined below arise from the need to            P4: Treat verification as a first-class citizen, designing and
satisfy three competing constraints: resource limitations of               implementing with verification in the loop, using verifica-
edge and high-end embedded systems, complex security needs                 tion considerations to guide the system design to reduce
of confidential computing, and tractability of formal verifica-            verification time and improve coverage.
tion.
Edge and high-end embedded systems have limited power
and silicon budget and are designed to execute specific work-
loads with predictable runtime requirements. They may or               3.1              Design Methodology
may not be network-connected. In contrast to low-end embed-            Figure 2 shows our methodology for designing and devel-
ded systems, e.g., sensors, our target systems contain multi-          oping ACE, consisting of three phases interacting with each
ple security domains and use hardware-based isolation mecha-           other: system design, implementation, and continuous inte-
nisms. Examples are: (1) Automotive systems [36], software-            gration with proofs. For the remainder of this section we will
defined vehicles [8], (2) PCIe crypto and AI accelerators [56],        focus on the system design decisions, the other two phases in
and (3) Telco infrastructure [50, 79].                                 our process will be discussed in Section 4.
Confidential computing, which enables isolation of secu-                  We started our design phase by evaluating the requirements
rity domains on the same hardware, builds on hardware and              such as hardware constraints and the threat model (Subsec-
firmware components whose implementation and composition               tion 2.2). Those requirements, together with our design prin-
require rigorous security analysis. While increased complex-           ciples, then motivated our key design decisions and high-level
ity of these components might enhance the performance and              invariants (Subsection 3.2).


                                                                   3
3.2    Key Design Choices & Invariants
                                                                                                        security
                                                                                                                         e.g., con dentiality of VM data




                                                                                            s
By adhering to our design principles and applying our method-




                                                                                           cie
                                                                                                       guarantees




                                                                                        n
                                                                                     de
ology, we made design decisions that distinguish ACE: (1) pre-                                         invariants           e.g., two VMs cannot access the same page




                                                                                      n
                                                                                   pe
fer commonly used, simple hardware primitives with easily ab-




                                                                               de
                                                                                                  execution safety             e.g., no unde ned system states




                                                                              of
                                                                             pro
stracted functionality, (2) favor static versus dynamic config-                              functional correctness               e.g., page tables correctly con gured

urations for simplified reasoning about system state, (3) avoid                            memory safety guarantees                 e.g., bu er over ows, multi-threaded execution

unnecessarily complex interfaces to reduce intermediate states,                hardware properties and correctness
                                                                                    fffi     fi   fl                fi
                                                                                                                                        e.g., leaks via µ-architectural state

(4) prioritize simplicity over performance and memory usage
                                                                                             Figure 3: Pyramid of proof dependencies.
to facilitate formal verification.
Simple hardware and abstractions. Since ACE primar-                       configuration setup and runtime walks. Alternatively, sim-
ily targets edge and high-end embedded systems, its design                pler mechanisms generally have a limited number of coarse-
emphasizes compatibility with widely available, standardized              grained access control rules for physical memory but are sim-
hardware components for broad adoption. Following princi-                 ple to set up, implement, and consequently verify.
ple P1, we do not require the presence of specialized TEE-                   Following P1 and P2, ACE statically partitions memory into
optimized hardware elements, like sophisticated memory iso-               non-confidential and confidential memory. This one-time op-
lation, interrupt delivery, or IO mapping mechanisms, typical             eration utilizes simple hardware that performs address range
for high-end application servers, like in Intel TDX, AMD SEV,             checking, simplifying the mathematical modeling and verifica-
or ARM CCA. Instead, our goal is to build on simple, general-             tion of the system due to easier ownership reasoning. This ad-
purpose hardware mechanisms [48, 25, 62], while allowing                  vantage comes at the cost of potential memory over- or under-
additional hardware and software extensions to enhance per-               allocation, which is acceptable for our target systems. Their re-
formance of use-case-specific functionality when scaling from             source requirements and applications are known upfront, mak-
high-end embedded to edge or beyond.                                      ing static allocation practical.
   We lay ACE’s design on a virtualization layer because
it provides a good abstraction over the execution environ-                 Single-step TVM creation. ACE requires only a single hy-
ment (P3) and is a natural boundary for isolation with a smaller           pervisor call to instantiate a TVM. The hypervisor first creates
attack surface (P2) compared with process-based TEEs [19,                  a standard VM in memory from a TVM image and then re-
48, 41]. We expect our targeted systems to be powerful enough              quests the TSM to promote it to a TVM. This design adheres
to support a RISC-V processor with virtualization capabilities,            to principles P2 and P3, offering advantages over the multi-
i.e., the hypervisor extension and a two-level address transla-            step procedures employed by existing confidential computing
tion.2 These assumptions are met by today’s operational tech-              frameworks. In particular, the attack surface is reduced be-
nology (OT) systems [70, 82], automotive-grade SoCs [36], AI               cause: (1) The adversary cannot influence the physical allo-
accelerators [56], and cryptographic coprocessors [51]. Sys-               cation of TVM pages, a vulnerability previously exploited to
tems with requirements for better I/O performance, memory                  compromise confidentiality [22, 16]. (2) There is no interme-
utilization, or lower power consumption can extend hardware                diate or partially initialized TVM state that could be targeted
with dynamical memory partitioning [67], directly injected in-             for rollback, an attack analogous to a TPM reset attack. (3)
terrupts [5], and directly assigned IO devices [61, 63].                   The absence of multiple calls eliminates the risk of reaching
   While the concept of ACE can also be applied to high-end                an unsafe state with specific combinations of request order and
application servers (not restricted to only edge/embedded sys-             parameter values.
tems), we think it is less practical and effective given the larger           Since the TSM execution is non-interruptible, the hardware
TCBs and hardware complexity needed to support the wide                    thread (a hart in RISC-V terminology) remains blocked while
class of workloads demanded by such systems.                               the TSM copies the VM into confidential memory. This over-
                                                                           head is generally acceptable because most TVM memory con-
Statically partitioned confidential memory. The TSM uses sists of zeroed pages, which are skipped during promotion and
memory access control hardware to prevent unauthorized ac- lazily mapped at runtime.
cesses to protected memory regions. Embedded systems usu-
                                                                           Formal Verification and Rust. Our target systems might op-
ally run a fixed well-understood set of applications. This
                                                                           erate in regulated industries that require formal proofs. Fig-
makes them uniquely suited to static memory partitioning be-
                                                                           ure 3 shows the hierarchy of properties the TSM must establish
cause the memory requirements are predictable.
                                                                           in order to achieve the security goal stated in §2.2. These are
   There are different hardware-based mechanisms used for
                                                                           presented in the form of a pyramid: to reason about properties
memory access control. More complex mechanisms enable
                                                                           in one layer, one must first prove the properties in layers be-
fine (page-level) access control at the cost of more complex
                                                                           low. At the base lies hardware correctness and memory safety,
   2 The RISC-V hypervisor extension can be emulated in firmware [80], al- necessary preconditions for any higher-level argument. Above
lowing ACE to run on simpler hardware at the cost of reduced performance.  those sit functional correctness and execution safety, and at the


                                                                      4
top sits the security guarantee: a TVM’s execution state and            al. [12]. We use Linux KVM and QEMU as the hypervisor.
memory contents remain confidential and unmodified except               We patched the Linux kernel with the CoVE patches, which
through explicitly declassified channels. For the top-level se-         we co-developed with the RISC-V community.
curity property, we target a relaxed version of non-interference           The TSM’s core implementation consists of: (1) initializa-
which accounts for the intentional information flows that a             tion code executing during secure boot (§4.1) and (2) runtime
strict non-interference property would not permit.                      code that drives a finite state machine (§4.2), which reacts to
   We assume hardware correctness [46, 13] and focus on ver-            interrupts. In (§4.5), we discuss how formal verification is im-
ification of higher layers. Memory safety errors continue to            bued in the TSM’s design and implementation.
make up a large part of security-related bugs [15, 30]. Thus,
following P4, we decided to drastically reduce the potential            4.1   System Initialization
surface for memory safety errors by using Rust [53] as the
TSM implementation language. Rust has a rich type system                At power-on, the hardware root of trust initializes the secure
that statically eliminates memory-safety issues for the vast ma-        boot process [3], and transfers control to the TSM initializa-
jority of the code (written in safe Rust) without getting formal        tion code. This code initiates the device identifier composition
verification engineers involved, thus shifting a significant part       engine (DICE) chain and locks access to the unique device
of the verification burden to the compiler. By applying soft-           secret. It also configures the system such that the TSM main-
ware engineering practices such as encapsulating unsafe Rust            tains full control until the next power-cycle by reconfiguring
and creating well-defined abstractions with the help of modu-           hardware to protect the TSM’s code, data, and hardware con-
larization (P3), developers gain greater confidence in the pro-         figuration from tampering by less-privileged software. Finally,
gram’s correctness, even in multi-threaded environments.                it also ensures that execution of less-privileged software traps
   While ensuring memory safety eliminates many common                  to the TSM at well-defined entry points.
bugs, it is just a step towards the top-level security property         Memory partitioning. During the system initialization, the
in §2.2. To formally state such a hyperproperty and mechani-            TSM divides main memory into two contiguous regions: non-
cally prove it we need the high expressiveness offered by de-           confidential memory and confidential memory.3 Later, at run-
ductive verification frameworks like Rocq [75]. We use the              time, the hypervisor will have complete ownership of the non-
RefinedRust [35] framework to prove properties about Rust               confidential memory but will not be able to access the con-
code in the Rocq prover and continuously check proofs for ev-           fidential memory. That allows the TSM to store security-
ery code change in a continuous integration (CI) system.                sensitive data required to maintain confidential computing
Local attestation. It is essential for ACE to detect unautho-           functionality in confidential memory, for instance the TSM’s
rized modifications to the firmware, the TSM, or a TVM. Be-             stack areas (for every physical hart), the TSM’s heap area,
cause embedded systems might operate in environments with               save-state areas (for every physical and virtual hart), and code
limited or no network access (e.g., controllers used in opera-          and data of TVMs.
tional technology or automobile industry), ACE employs local               To enforce memory access protection to confidential mem-
attestation [39]. This mechanism relies on information bun-             ory, the TSM configures hardware-based memory access con-
dled with a TVM’s image to verify the TVM’s integrity and               trol mechanisms. Specifically, it uses RISC-V physical mem-
authenticity at creation time. A TVM owner uses an encap-               ory protection (PMP) [40] and IOPMP [44].4 The RISC-V
sulation key of a target device to cryptographically protect            architecture guarantees that only software running in M-mode
a TVM attestation payload (TAP), which is a file that stores            is authorized to reconfigure it.
TVM integrity measurements and TVM-specific secrets. Only       Page allocator and page tokens. Confidential memory is
the expected TSM running on the correct hardware can read       further partitioned into pages that the TSM assigns to TVMs
the contents of a TAP by accessing the decapsulation key. Fol-  to store their code and data, as well as pages to manage the
lowing P1, the presence of local attestation does not exclude   TSM’s internal data structures. To ensure correct allocation of
remote attestation for systems with network connectivity.       pages, i.e., that pages belong to confidential memory and have
                                                                a single owner, the TSM instantiates a component called the
                                                                page allocator. The page allocator is a software submodule of
4 Implementation                                                the TSM. During system initialization, for every confidential
                                                                memory region corresponding to a physical page, it creates a
We implemented the TSM in Rust [53] and open sourced logical page token, a Rust object that lives on the TSM’s heap.
it. The TSM is statically linked against the OpenSBI [66] Initially, the page allocator owns all page tokens. Whenever
firmware to which it delegates some requests, like handling un-
                                                                    3 A TSM supporting RISC-V Smmtt might enable a hypervisor to dynami-
aligned memory accesses or inter-processor interrupts (IPIs).
                                                                cally convert non-confidential memory to confidential memory at runtime.
Both OpenSBI and the TSM run in the most-privileged RISC-           4 The current implementation of ACE runs on a RISC-V evaluation board
V M mode. OpenSBI is used as a library to simplify its fu- that does not support IOPMP because IOPMP had not been ratified yet at the
ture replacement or de-privileging as reported by Castes et time when the board was designed.


                                                                    5
                                                                               TEE security monitor (TSM)




                                                                                                                                                  non-con dential ow
the TSM allocates a new page of memory, for example to cre- 1




                                                                                                ABI call
                                                                                2         enter from hypervisor          3
                                                                                                                            router
ate a TVM’s data page, the TSM retrieves a free page token hypervisor                 (lightweight context switch)
                                                                                5              exit to hypervisor                           4
from the page allocator and stores it within the Rust data type                       (lightweight context switch)
                                                                                                                     apply transformation     handlers
corresponding to the final entity, e.g., a page table associated                                                                 declassify
                                                                                                              6 security domain
with the TVM. In the above example, the ownership transfer                                                      context switch




                                                                                                                                                  con dential ow
would correspond to the move of the page token’s self refer- 1                                                                   declassify
                                                                                2     exit to con dential hart                              4
                                                                     TEE                                             apply transformation     handlers
ence from the page allocator to the object of the TVM’s page        virtual           (lightweight  context switch)




                                                                                               interrupt
                                                                                               /ABI call
                                                                   machine     5 enter from con dential hart             3
table type. Rust’s type system ensures that a page token is         (TVM)               (lightweight context switch)
                                                                                                                            router

not spent twice. In the above example, it would statically en-
                                                                                fi   fi   fi
                                                                                          fl        fi
                                                                                                    fl




sure that every physical memory region is only assigned to one Figure 4: Finite state machine (FSM) showing the execution
TVM.                                                             flow of the TSM on a single physical core on which the hyper-
                                                                 visor and a TVM execute concurrently.

4.2     Runtime
                                                                              ured to enforce access permissions of a TVM. When the TVM
The firmware executing the secure boot eventually transfers                   resumes execution, the memory management unit (MMU) is
control to the hypervisor, marking the transition of the device               using the page tables associated with the TVM which allows
into its operational state—runtime. During runtime, the hy-                   the TVM to access only memory pages it owns. If there is a
pervisor, running in the HS-mode, manages which software                      need to switch from the current TVM, the TSM switches ex-
runs on the processor and for how long. The hypervisor has                    ecution to the hypervisor as the hypervisor retains scheduling
limited privileges and requests the TSM to perform security-                  responsibility.
sensitive operations, for example, accessing certain memory-
mapped input/output (MMIO) or running TVMs.                     Lightweight context switch. The TSM executes only in re-
   To limit the attack surface, the TSM exposes only a narrow   sponse to interrupts and ABI calls from the hypervisor and
ABI to the hypervisor. In addition to the standardized RISC-    TVMs (➊). The lightweight context switch (➋) starts by stor-
V ABI calls, such as read-only calls to discover the system     ing the minimal set of the architectural state that the TSM
configuration and a call to shutdown/reboot the system, the     could overwrite during its execution (i.e., general-purpose reg-
TSM adds three calls to manage a TVM: promote, run, and         isters (GPRs) and control status registers (CSRs)) in the save-
destroy. By contrast, a full RISC-V CoVE defines sixteen ad-    state area in main memory. Then, the router component (➌)
ditional complex calls for page table management and two ex-    parses the request and invokes the appropriate handler. The
tra calls for constructing a TVM in multiple steps. Following   handler (➍) decides if the request will return to the same se-
P1, the TSM supports optional symmetrical multiprocessing       curity domain or a different security domain. Handlers im-
calls (like start/stop/suspend hart, execute remote fence), ac- plement the logic that decides how to transform the architec-
cess to hardware devices via MMIO, and emulated access to       tural state to fulfill the request. This transformation is then
misaligned load/stores.                                         applied to the hardware architectural state and/or state in the
                                                                save-state area. If the security domain will not be changed, the
Finite state machine. To enhance the correctness of the lightweight context switch (➎) is called to return to the secu-
TSM’s implementation and simplify the verification process, rity domain.
the TSM operates as a finite state machine (FSM), as shown in
Figure 4. The hart that the TSM executes upon taking control Security domain context switch. One security domain can
is in one of two states: executing a non-confidential flow (up- request assistance from another security domain to perform an
per part) or executing a confidential flow (bottom part). This operation. For example, a TVM that cannot access a phys-
split simplifies the analysis of information flow between the ical network card directly uses the VirtIO protocol, so that
hypervisor and the TVM, while minimizing the potential for the hypervisor emulates such access. The corresponding han-
programming errors. We leverage Rust’s modularization ca- dler (➍) then routes the call to the security domain context
pabilities to statically ensure that the TSM’s functionality is switch (➏) and the TSM crosses the boundary between the
accessible exclusively to the hypervisor or a TVM.              non-confidential and confidential security domains.
   In the non-confidential flow (upper part of the FSM), the       The security domain context switch is a piece of code that
TSM handles requests on behalf of the hypervisor and the reconfigures the hardware to prepare for execution of a dif-
hardware remains configured to enforce hypervisor-specific ferent security domain. It saves all architectural state of one
access control permissions. For example, the memory access security domain in the save-state area in the main memory
control mechanism enforces that the hypervisor can access and loads the architectural state of the other security domain
only non-confidential memory. Therefore, no additional secu- from the main memory into hardware. All state for this con-
rity measures must be taken to return execution to the hyper- text switch is stored to or read from confidential memory. The
visor. Analogously, in the confidential flow (bottom part), the security domain context switch also reconfigures the memory
TSM processes requests of a TVM and the hardware is config- access control mechanism to protect the current security do-


                                                                          6
main from the one that will execute next, and clears micro-             running TVM retrieves secrets from the TSM, such as a Linux
architectural caches, e.g., translation lookaside buffers (TLBs).       unified key setup (LUKS) key to decrypt the root filesystem,
The Rust implementation ensures that every execution path               using a dedicated ABI call.
between non-confidential and confidential flows goes through
                                                                        Local attestation. Local attestation provides attestation for
this context switch.
                                                                        TVMs that execute with limited network access. When the
Handlers and Reclassification. Handlers implement the                   hypervisor requests the TSM to create a TVM, it passes to the
TSM’s functionality exposed to the hypervisor and TVMs via              TSM both the TVM’s image and a file called TVM attestation
the ABI. To reduce the risk of implementation errors creating           payload (TAP). The TSM verifies the TVM’s integrity by com-
security bugs, each handler operates only on a subset of the ar-        paring the TVM’s measurements with reference measurements
chitectural state of a security domain. For example, a TVM’s            from the TAP and stores the TVM’s secrets retrieved from the
attestation handler will never have write access to the hyper-          TAP in confidential memory. A verified TVM uses a dedicated
visor’s state, so that it can never leak attestation-related data       ABI call to retrieve secrets from the TSM.
to the hypervisor. To do so, we leverage Rust’s encapsulation              The TVM’s integrity measurement includes the crypto-
to ensure a limited visibility scope and privacy of data struc-         graphic hashes of the TVM’s code and data, flattened device
tures in the implementations of handlers. Specifically, each            tree, and the initial boot hart’s state. This is stored in ded-
handler consists of three phases: a constructor, a transforma-          icated registers analogous to platform configuration registers
tion method, and a destructor. The constructor has read-only            (PCRs) [4]. The TVM’s data integrity is a single hash, the
access to the hart state, which permits it to read information          value of which uniquely represents the initial content of the
required to process the request. The transformation method              TVM’s code and data pages.
has access only to the TSM’s core functionality, such as the               The TVM’s owner creates a TAP by encrypting a payload,
page allocator, the interrupt controller or the TVM’s metadata          which contains integrity measurements and secrets, and con-
storage. Finally, the destructor has write access to the tar-           catenates it with a lockbox. A lockbox stores the symmetric
get security domain’s architectural state to which it can apply         key encrypted with the public portion of the TSM’s attesta-
or reclassify processed information. The Rust-enforced con-             tion key, which is an asymmetric cryptographic key associated
straints placed on handlers and accessibility of each domain’s          with the hardware and derived with DICE [33], as defined in
architectural state simplify how a TVM’s owners and verifica-           CoVE [9]. Only the TSM running in the target hardware can
tion tools can certify that the TSM correctly implements the            decrypt the symmetric key and payload.
specification.                                                             The TAP supports post-quantum cryptography (PQC), so
   Importantly, it is the responsibility of a security domain to        that an adversary possessing a powerful enough quantum com-
use handlers securely. For example, for VirtIO, the TSM en-             puter is not able to decrypt the TAP. Specifically, the TSM uses
ables a TVM to have a shared page with the hypervisor, but              quantum-safe algorithms such as ML-KEM [59] to encapsu-
does not enforce any form of data secrecy. Thus, to maintain            late the TAP symmetric key in the lockbox, SHA-384 to cal-
security, a TVM itself must encrypt data before sending them            culate the TVM’s integrity measurements, and AES-GCM-256
to disk over VirtIO and decrypt when reading back.                      to encrypt the payload. The TAP also supports cryptographic
                                                                        agility, because each lockbox defines the type of algorithm that
                                                                        encrypts the TAP symmetric key to allow a TVM owner to
4.3    Selected Non-confidential Flow Handlers                          choose a PQC algorithm of their choice.

Promote to TVM. As explained in Subsection 3.2, the TSM
implements a novel single-step TVM creation procedure in                4.4   Selected Confidential Flow Handlers
which it atomically converts an instance of a VM into a TVM
as part of the process called promotion. In contrast to other           Symmetrical multiprocessing. ACE supports symmetrical
architectures [14, 39, 7] which convert the VM memory page-             multiprocessing which enables a TVM to have multiple con-
by-page, there are no intermediate states corresponding to a            fidential harts. When creating a TVM, the TSM enables only
TVM that could be exploited by an adversary [22, 16].                   the TVM’s boot hart and sets other confidential harts to the
   As part of the promote request, the TSM receives as input            powered off state. The boot hart can then request the TSM to
the initial state of the VM: the registers and a program counter        start another confidential hart at the indicated guest physical
for the boot hart, a pointer to the root page table, a pointer to       address and with specific initial arguments. The TSM follows
the flattened device tree, and a pointer to the attestation pay-        the finite state machine defined in the hart state management
load. It then creates save-state areas for the new confidential         (HSM) extension to the RISC-V supervisor binary interface
harts and traverses the VM’s page table hierarchy copying non-          (SBI) [31] to track and ensure proper lifecycle state changes.
zeroed pages from non-confidential memory into confidential             The TSM also permits confidential harts to send inter proces-
memory. After measuring the initial TVM state, the TSM per-             sor interrupts (IPIs), as well as dedicated commands to clear
forms local attestation to authorize the TVM’s execution. A             remote caches, to other confidential harts as defined in the re-


                                                                    7
spective SBI extensions [31].                                             Thus, we argue that effective low-level systems programming
                                                                          is possible with relatively little unsafe code.
Timer programming and interrupt handling. The ACE
implementation relies on the hypervisor to manage a TVM’s                 ABI design. The primary attack surface of the TSM is the
external interrupts and on hardware to provide the per-hart               ABI. For that reason, in our design we minimized the ABI
timers. ACE also supports systems with a basic hardware in-               between the TSM and hypervisor, and between the TSM and
terrupt controller [32] without requiring support for the more            a TVM. The promote call is the most complex ABI with the
complex RISC-V AIA specification [5].                                     largest input. To handle this call, the TSM must traverse the
   During the TVM’s execution, all of the guest’s interrupts              multi-level page table hierarchy and parse individual interme-
(RISC-V VS-mode) trap directly into the TVM, owing to the                 diate page tables. Because the hypervisor creates these page
TSM’s interrupt delegation setup. Other interrupts (e.g., ex-             tables, it can maliciously craft the content of these page tables
ternal or software interrupts) trap into the TSM. For external            to exploit a buggy TSM implementation.
interrupts, the TSM returns execution to the hypervisor so that              For example, one of the attacks consists of defining a pointer
it can delegate to the recipient of the interrupt. If the interrupt       to a data page that resides in the confidential memory. During
targets a TVM, the hypervisor requests the TSM to resume the              a TVM promotion, an incorrectly implemented TSM would
TVM’s execution and inject the interrupt whose identifier is in           copy the contents of an arbitrary confidential memory region
a dedicated CSR. After the security domain context switch, the            to a new confidential page mapped to the attacker’s TVM. To
TSM decides whether to inject the interrupt to a TVM based                mitigate this class of attacks, the TSM allows a hypervisor and
on the interrupts the TVM agreed to receive. If the TSM is not            a TVM to pass as input arguments only memory addresses
executing, all interrupts go either to the hypervisor or the VM           they own, i.e., non-confidential memory and guest physical
as indicated by the configuration.                                        addresses, respectively. To enforce this requirement statically
   A TVM manages its own timer by programming a dedicated                 during compile time, we define dedicated Rust types for each
CSR specified by the RISC-V Sstc extension [80]. The TSM                  type of memory address. At ABI entry points, all memory ad-
ensures proper resumption of the timer after the security do-             dresses are validated in order to obtain valid (non-)confidential
main context switch. Following the CoVE spec, the TSM dis-                memory addresses that can be trusted in the rest of the secu-
closes the timer value to the hypervisor for scheduling pur-              rity monitor. Such protections are possible thanks to Rust’s
poses.                                                                    rich type system which guarantees non-trivial properties even
                                                                          before applying complex deductive verification tools.

4.5    Formal Verification                                                Methodology. We integrated formal verification methodology
                                                                          into our design and implementation using RefinedRust [35].
We have designed ACE with the goal of providing a high-                   RefinedRust is a modular verification tool in which individual
trust implementation in mind. This influenced the design of               functions are given a specification and are verified indepen-
the ABI, as well as its implementation, where unsafe code is              dently of each other to then compose to a verification result for
minimized and safely encapsulated.                                        the whole program. RefinedRust verifies functional correct-
Rust memory safety. Rust aims to provide memory safety                    ness of the code against the specification, and memory safety
guarantees, which hold as long as only the safe fragment of               of safe and unsafe code as well as absence of panics.
the language is used. However, for low-level software like the               During the design phase, we stated individual module in-
TSM, unsafe code is inherently necessary to interface with the            variants that the implementation has to uphold. After the mod-
hardware and do low-level memory manipulation. Unfortu-                   ule implementation, we annotated the Rust code with specifi-
nately, a memory safety error in a piece of unsafe code can               cations for individual functions and data structures. If it turned
nullify the memory safety guarantees of all other code, includ-           out that writing the specifications for interfaces was overly
ing safe Rust code. Thus, it is important to both minimize the            complex, the proof engineer and system engineer iterated to
amount of unsafe code and to scrutinize it.                               simplify the code, making it more amenable to formal specifi-
   The TSM implementation minimizes unsafe code by devel-                 cation.
oping safe abstractions over core sources of unsafety that are               RefinedRust generates a formal model of the Rust code and
re-used across the code. One such abstraction are the page                specifications in the Rocq prover as well as a proof template
tokens mentioned earlier. In total, the TSM codebase has 55               using RefinedRust’s automation tactics. If the automatic proof
unsafe blocks, each of which is usually very short, with an av-           does not succeed, the proof engineer interactively adds hints
erage size of just over 4 lines. Of these unsafe blocks, 12 are           to the proof template. The specification and proof are then
part of the TSM’s core memory management, 11 are for inter-               checked into continuous verification, where RefinedRust con-
facing with the hardware (e.g. reading CSRs), and 20 for flow             tinuously updates the model of the changing code, and checks
handling and managing the TVM’s state. In total, about 240 of             the specifications and proofs against the model. If a change to
the 8000 lines of Rust code are unsafe; about 90 of the unsafe            the code breaks the proof, the continuous verification rejects
lines are for inline assembly backing up or modifying registers.          the code. For unsafe code, we use RefinedRust to verify that


                                                                      8
functions adhere to Rust’s safety contract for all inputs, en-   1          #[rr::refined_by("p" : "page")]
suring that all clients only using safe Rust code cannot trigger 2          /// Invariant: A Page exclusively owns its memory region.
                                                                 3          #[rr::invariant(#type "p.(page_loc)" : "p.(page_val)" @
memory unsafety.                                                 4            "array usize (page_sz_in_words p.(page_sz))")]
                                                                 5          /// Invariant: The page is well-formed.
Example: Page Tokens. As a simple but illustrative example 6                #[rr::invariant("page_wf p")]
of how our verification with RefinedRust works, we consider 78              /// Omitted: the page resides in confidential memory
                                                                            #[rr::invariant("...")]
page tokens. Page tokens are crucial to ensure memory isola- 9              pub struct Page {
tion between security domains, i.e., no two security domains 10 11
                                                                                #[rr::field("p.(page_loc)")]
                                                                                address: ConfidentialMemoryAddress,
have access to the same page in confidential memory. Figure 5 12                #[rr::field("p.(page_sz)")]
shows excerpts of the invariant on page tokens, which specifies 13
                                                                14          }
                                                                                size: PageSize,

that page tokens are mathematically modeled by a type page 15               impl Page {
(defined in Rocq) with the following components: the memory 16  17
                                                                            /// Precond: offset is divisible by the size of usize.
                                                                            #[rr::requires("size_of usize | off_bytes")]
location page_loc, the stored sequence of words page_val, 18                /// Precond: a usize fits at the offset within page bounds
                                                                            #[rr::requires("off_bytes + size_of usize ≤
and the size page_sz. Then, the core invariant is that a page 1920              page_sz_in_bytes p.(page_sz)")]
token exclusively owns the memory region it spans, containing 21            /// Postcond (omitted): return value is read from page
the list of words page_val; for this, we provide a RefinedRust 22
                                                                23
                                                                            #[rr::ensures("...")]
                                                                            fn read(&self, off_bytes: usize) -> Result<usize, Error> {
type assignment for the page_loc location. (Note that it is not 24              unsafe { .. }
                                                                25          }}
possible to state this invariant directly in Rust’s type system.)
   The function read on Pages reads one machine word from               Figure 5: Definition of the page token invariant in the
the page by using unsafe code to read from the underlying               RefinedRust specification language.
memory. Nevertheless, the function as a whole is safe (i.e. not
marked as unsafe), as read does appropriate bounds and align-
                                                                        prior code review or testing, underscoring the value of formal
ment checks (e.g., that the read word is in confidential memory
                                                                        methods for security-critical code.
and inside the page) before performing the read, returning an
                                                                           Ongoing work focuses on establishing correspondence be-
error in case of an invalid input. The function’s specification
                                                                        tween the page table configuration and the RISC-V authori-
defines the conditions under which the read succeeds and the
                                                                        tative semantics and integrating information-flow tracking to
expected result value.
                                                                        enable non-interference proofs with explicit reclassification to
   The page token abstraction is useful as it safely abstracts          eventually reach the top of the pyramid in Figure 3. Spec and
from the low-level memory operations that it is implemented             proof artifacts are part of the open source repository and veri-
with. With RefinedRust, we can verify once and for all that             fication is integrated with CI.
this abstraction is sound and upholds the safety guarantees of
Rust’s type system. Other components of ACE not using un-
safe code (e.g., most of the page allocator) are thus automati-         5     Evaluation
cally free of memory safety errors, even before fully verifying
them for functional correctness and security – and once we              We next evaluate whether ACE’s runtime performance and
fully verify them, Rust’s safety proof can be re-used to sim-           memory overhead of a TVM over a normal VM is similar to
plify the full security verification.                                   other confidential computing systems. We seek to answer the
                                                                        following key questions:
Formal Verification Results and Bug Discovery. [26] shows
how to formally verify memory safety and functional cor-                    • What is the overhead of the TSM on TVM execution?
rectness (the two bottom layers of the pyramid above hard-
ware in Figure 3) of the TSM’s page management subsystem.                   • How efficient is I/O in TVMs?
The page token abstraction and the page allocator cover ˜600                • What is the impact on a TVM’s boot time?
lines of code, ˜8% of the total TSM codebase. The verifi-
cation consists of 340 lines of expressive specifications writ-             • What is the implementation complexity and memory
ten in RefinedRust, 1300 lines of shared Rocq specifications                  overhead of the page token mechanism?
and 1400 lines of manually written Rocq proofs on top of the
automatically-generated proofs.                                         Evaluation setup. The evaluation hardware, which is the first
   The verification process uncovered two bugs in the unsafe            commercially available RISC-V hardware supporting virtual-
parts of the page allocator implementation. The first bug was           ization, implements a pre-ratified version of the hypervisor ex-
caused by incorrect bounds checking after pointer arithmetic            tension and does not fully conform to the CoVE specification.
in the procedure that creates the initial page tokens. The sec-         Specifically, three features require emulation in the TSM: VS-
ond was a logical error, identified during functional verifica-         level timer virtualization, instruction fetch on trap, and clock
tion of the procedure responsible for assigning a new memory            access. These emulated paths introduce additional TSM exe-
region to the page allocator. Neither bug was detected during           cution overhead not present in CoVE-compliant hardware. We


                                                                    9
                        2
                                                                                                                       NormalVM_NOAEE       NormalVM
(relative to NOAEE)
     Runtime




                        1


                        0
                  fo ad
                ge ild



          big ig id




         thr big cv
                   ate d
                            ild
        hu hug ref
               pa ead
                            ap

                     ge ll

               pa fork

          hu mid ult




                 ag pu




                    p cv
                  for ite
                            ild
                hu send
         co ig m ork
                 xt ap


                             ig




         hu uge ult
         sm mu rite
        sm ll m map




                 mu ult
               pa ap
                              lt
                   d m ll
                              p



                    all p
                   big ad

                   all ig



                  e hild
                 all big
                      sel e
                  for ct



                  big ap
           mi big w d
                     un e
                              p
                thr fork
                           ate
                sel wtch
                          po




              mi epo




                            it




              d m rit
              cre rea




                        ma



               sm nma




                        sen


                        ma
                        fau
                          tp




                        tb




              sm oll b


                           e
                         re




                         re
            hu rkch




                        ch
                      kch
            big id re




                        re
                     mm




            nte m




           all unm




                     mm
            dp c
             ge wr




                       wr
                        fa




              h fa




            big e fa
               b f




                      cre
            ge w




                      kc
           ge e r




            sm poll
             a n
                     ec
                    ge


                     si
                   ge




                   ge




                   ge
                    b
                 m




         mi
              Figure 6: Overhead of running LEBench in a normal VM on system with ACE to a system without ACE. (higher=better)
                        2
                                                                                                                                 NormalVM       TVM
(relative to NormalVM
       Runtime




                        1


                        0
                  fo ad
                ge ild



          big ig id




         thr big cv
                   ate d
                            ild
        hu hug ref
               pa ead
                            ap

                     ge ll

               pa fork

          hu mid ult
                  for ite
                            ild
                hu send
         co ig m ork
                 xt ap


                             ig




         hu uge ult
         sm mu rite
        sm ll m map




                 mu ult
               pa ap
                              lt
                   d m ll
                              p
                 ag pu


                    all p
                   big ad
                    p cv
                   all ig



                  e hild
                 all big
                      sel e
                  for ct



                  big ap
           mi big w d
                     un e


                           ate
                              p
                thr fork
                sel wtch
                          po




              mi epo




                            it




              d m rit
              cre rea




                        ma



               sm nma




                        sen


                        ma
                        fau
                          tp




                        tb




              sm oll b


                           e
                         re




                         re
            hu rkch




                        ch
                      kch
            big id re




                        re
                     mm




            nte m




           all unm




                     mm
            dp c
             ge wr




                       wr
                        fa




              h fa




            big e fa
               b f




                      cre
            ge w




                      kc
           ge e r




            sm poll
             a n
                     ec
                    ge


                     si
                   ge




                   ge




                   ge
                    b
                 m




         mi
                             Figure 7: Overhead of running LEBench in a TVM vs a normal VM running on top of ACE. (higher=better)

therefore treat our measurements as conservative upper bounds                   ilar performance for a TVM and a normal VM, except for
on ACE’s overhead: hardware conforming to CoVE will elim-                       mmap and page fault operations for which we observed be-
inate these emulation paths and reduce overhead.                                tween 5% and 16% performance increase for a TVM com-
   Evaluation runs on a HiFive Premier P550 board equipped                      pared with a normal VM. It might be caused by the way the
with an ESWIN EIC7700X SOC with four 64 bit RISC-V                              TSM manages TVM’s address translation, timers, and caches.
1.4 GHz imafdch cores. The board has 16 GB RAM, 8 PMPs,                         The TSM never pages out confidential memory pages, prevent-
and a Sv48x4 MMU. The host operating system runs Linux                          ing G-stage page faults. Moreover, timer interrupt handling
kernel 6.6.21 with CoVE and ESWIN patches that enable sup-                      and scheduling happens directly in the TSM (M mode) while
port for CoVE and P550 hardware. Since hardware does not                        the regular VM’s timer interrupts must be handled by KVM
implement a root-of-trust for attestation, we hard coded an at-                 (HS mode) with the help of OpenSBI (M mode).
testation key to evaluate the local attestation mechanism.
                                                                                   The ref benchmark, which measures kernel-managed clock
5.1                         ACE’s Overhead                                      reads, shows higher latency for TVMs. This is a consequence
                                                                                of the VS-level timer and clock access emulation in the TSM,
To evaluate the CoVE patches’ impact on the hypervisor and                      both of which are absent from the evaluation hardware but
the TSM’s runtime, we ran LEBench [64] on VMs and TVMs                          mandated by the CoVE specification. Each clock read in a
with and without ACE. As the evaluation board’s hardware                        TVM triggers an additional trap through the TSM’s emulation
clock does not support nanosecond accuracy, we modified                         path, adding latency proportional to the TSM’s context switch
LEBench to batch operations into a single timed measurement,                    cost. This overhead is therefore a result of the evaluation plat-
ensuring a single measurement exceeds 1 µs.                                     form and not a limitation of ACE’s design. CoVE-compliant
   Figure 6 shows that a normal VM executing on Linux KVM                       hardware with Sstc support should eliminate this trap path.
with CoVE patches and OpenSBI with the TSM performs
mostly similarly to a normal VM running without a TSM. With
the TSM, the normal VM has lower performance for read-                          ACE’s multi-vCPU overhead. To get a better idea of whether
/write, page fault, and context switch operations. This could                   the TSM causes any overhead when multiplexing between
be a result of additional execution paths and branches inside                   vCPUs within a VM, we use the parallel mode of Core-
Linux KVM that were added by the experimental patch with                        Mark [18] to launch different numbers of instances of the
support for the RISC-V nested acceleration extension (NACL)                     benchmark inside a multi-VCPU VM. Each VM is given 4,
and a level of indirection introduced by the TSM. The CoVE                      8, and 16 vCPUs to match the benchmark’s level of concur-
spec requires NACL to share CSR values between the TSM                          rency (number of parallel processes). Table 1 shows that the
and KVM and the current implementation affects both normal                      TSM does not introduce any significant performance differ-
VMs and TVMs.                                                                   ences when multiplexing the different vCPUs within a VM
   Figure 7 shows that core Linux kernel operations have sim-                   across the different configurations.


                                                                             10
5.2    Network I/O                                                                                         1800
                                                                                                                          VM_NOAEE_LAT                  VM_NOAEE
We analyzed ACE’s impact on Virtio device performance by                                                   1600           VM_LAT                        VM
                                                                                                                          TVM_LAT                       TVM      80
measuring network I/O overhead in a TVM. We measured                                                       1400
throughput and latency of an Nginx server for each VM type




                                                                                     Requests per second
                                                                                                           1200
and varying numbers of vCPUs. The Nginx server and the ab




                                                                                                                                                                        Latency (ms)
                                                                                                           1000                                                        60
benchmarking tool [2] run on separate machines connected to
the same switch. ab used 8 threads to generate 10k requests                                                800
for the same 615 B file. VMs were configured with 5 GB of                                                  600                                                         40
memory and run Nginx with the number of workers matching
                                                                                                           400
the number of vCPUs. We ran each experiment 5 times and
present the average with standard deviation.                                                               200                                                         20
   Figure 8 shows that TVMs achieve 48% of normal VM net-                                                       0
work throughput, the overhead consistent with the bounce-                                                             1     2     3        4   5   6     7       8
                                                                                                                                           VCPUs
buffer-based DMA isolation common to VM-based confiden-
tial computing architectures (related work reports between          Figure 8: Network I/O performance when hosting Nginx
36% [83] and 60% [54] performance overhead for network              server in VMs with different numbers of VCPUs.
virtio operations on AMD SEV-SNP and Intel TDX). This I/O
overhead is architecturally inherent to any system that prevents
the hypervisor and peripheral devices from directly accessing                        35                                                       35
                                                                                                                                VM 1VCPU               VM 1G
confidential memory resulting in an extra buffer copy for vir-                       30                                         TVM 1VCPU     30       TVM 1G
tio. On the evaluation board, we observe large throughput vari-      Boot time (s)
                                                                                     25                                                       25
ation for normal VMs (between 550 to 1350 req/sec) and drop                          20                                                       20
in throughput when adding more than 2 vCPUs. We attribute                            15                                                       15
it to immature driver and firmware support on the evaluation                         10                                                       10
board, which is the first RISC-V board on the market with
                                                                                      5                                                        5
early virtualization support.
                                                                                      0                                                        0
   There exist techniques to improve I/O performance in VM-                                                 1        2    3       4    5           1      2        3          4
based confidential computing system. One approach is to                                                             Memory size (GB)                          VCPUs
map a peripheral device (or a virtual function) directly into
                                                                    Figure 9: Avg VMs and TVMs boot time with different mem-
the TVM’s address space, allowing the TVM to communi-
                                                                    ory size and vCPUs numbers. Bars show standard deviation.
cate with the device and enabling the device to read from
and write to selected TVM pages without mediation by the
hypervisor [63, 61]. An alternative approach avoids copy-
ing via bounce buffers by logically reassigning pages between          Figure 9 presents boot times of normal VMs and TVMs
confidential and non-confidential memory using hardware-            for different memory sizes and numbers of vCPUs. Since a
supported, page-based memory isolation [67]. At present, no         TVM’s zeroed pages are lazily loaded, boot times for TVMs
RISC-V hardware supports these mechanisms.                          scale with the memory size. TVMs boot up more slowly than
                                                                    normal VMs, 15 sec vs 10 sec. This slower boot time is due
                                                                    to the Linux kernel creating thousands of shared pages needed
5.3    Boot Time                                                    for virtIO in an inefficient page-by-page approach, slower I/O
We measured a VM boot time from the point we request its            caused by bounce buffers, and the local attestation check that
creation to the point we established an SSH connection to in-       performs signature check using a slow software implementa-
clude overhead of local attestation, initialization of virtio de-   tion of ML-KEM cryptography. The boot time latency can be
vices, and network communication. The results show an aver-         thus improved with more efficient implementation (i.e., shar-
age time calculated over eight measurements.                        ing multiple pages in a batch as allowed by the CoVE spec
                                                                    instead of ACE’s simpler implementation that does it page by
Table 1: CoreMark benchmark results when running inside the         page, hardware acceleration of cryptography operations) and
respective VMs. Reported values are means from three runs           more advanced mechanisms for improving I/O performance,
along with standard deviation.                                      as discussed in §5.2. The increased boot time (up to 30 sec)
                                                                    when adding more vCPUs to a TVM can be caused by the
 # of proc      VM ACE              VM              TVM
                                                                    vCPUs synchronization: additional IPIs trigger more context
 4            30003 ± 776      30387 ± 1172      29373 ± 713        switches resulting in cache misses due to security domain con-
 8            32191 ± 325       32368 ± 148      31614 ± 497        text switches. ACE does not impact a normal VM boot time
 16            32952 ± 91       33055 ± 14       32822 ± 40         compared to a non ACE system.


                                                                11
5.4   Page Token Memory Overhead                                   specific hardware requirements. As demonstrated by our eval-
                                                                   uation, ACE is deployable on commercially available silicon
A single page token occupies 9 B in main memory regard-
                                                                   today. By contrast, Salus, which also implements the RISC-V
less of the page size it represents. The page allocator stores
                                                                   CoVE spec [9], targets server-class environments and requires
page tokens in a tree data structure in which every level corre-
                                                                   hardware extensions for scalable resource isolation (RISC-V
sponds to a different architectural page size, adding extra 32 B
                                                                   Smmtt) and direct injection of VM interrupts (RISC-V AIA),
of information per not-empty node. The presence of a page
                                                                   limiting its current execution to simulation environments [68].
token in the tree indicates that a page can be allocated. To
allow allocation of smaller pages, large page tokens are split        ARM CCA [1] is a commercial VM-based confidential
into smaller ones. An analogous operation, merging, occurs         computing that targets application-class systems for ARM pro-
when pages are deallocated and returned to the page alloca-        cessors and requires dedicated hardware extensions. It offers
tor. In such cases, multiple contiguous smaller page tokens        a more flexible architecture than ACE that enables execution
are merged into a larger single page token, reducing the num-      of multiple realm management monitor (RMM) instances, a
ber of nodes in the tree. Thus, the latency of (de-)allocation     firmware component analogous to ACE’s TSM. ARM CCA
operations is independent of fragmentation of the confidential     also is subject to licensing fees. In contrast, ACE focuses on
memory, and the number of unallocated page tokens is mini-         a simple but extensible design that brings confidential com-
mized. In more detail, 1 GiB of unallocated confidential mem-      puting capabilities to commodity RISC-V hardware. To avoid
ory can be represented as a single 1 GiB page token, taking 9 B    adoption barriers in cost-sensitive regulated markets, ACE is
of the ACE heap. If all page tokens representing the smallest      open-source and royalty-free.
architectural page size (4 KiB) are allocated, then the page al-      Several academic and commercial systems target process-
locator’s tree is empty but allocated page tokens are stored in    based confidential computing: Cerberus [47], Keystone [48],
the structures of a specific TVM. Then, the overhead of page       OP-TEE [78], Penglai [24], Timber-V [81], Sanctum [19],
tokens is the largest and results in occupancy of 2.25 MiB of      SPEAR-V [69], and Elasticlave [84]. However, none of these
ACE heap for every 1 GiB of confidential memory (0.23% of          fit our target systems because they do not scale above low-
confidential memory).                                              end to mid-range embedded systems due to limited architec-
   Compared to other systems, Intel TDX and AMD SEV-SNP            tural and hardware capabilities. Example of target systems
require, in the pessimistic case, 16 B of metadata per 4 KiB       are smart meters, electronic control units, sensors, or single-
physical page to track page assignment to confidential mem-        purpose devices that must protect sensitive material, like cryp-
ory. This metadata is stored in hardware-protected data struc-     tographic keys. In contrast, ACE targets systems that sup-
tures known as the Physical Address Metadata Table (PAMT)          port multiple security domains (e.g., multi-tenancy), run more
and the Reverse Map Table (RMP), respectively. Overall, this       complex workloads with custom multi-threading or IO re-
corresponds to approximately 0.4% of system memory [42, 6].        quirements (e.g., automotive [36], software defined vehicles,
                                                                   crypto and AI accelerators [56], telco [50, 79]).
Summary. Evaluation shows that ACE is practical for our
primary targets: compute-intensive, purpose-specific work-            Some of the confidential computing designs are subject to
loads such as automotive controllers, PCIe cryptographic ac-       formal verification. CertiKOS [34] is a framework for veri-
celerators, and telco infrastructure. We expect next-generation    fied kernels that was used to verify the mCertiKOS hypervi-
CoVE-compliant hardware to reduce the I/O and boot over-           sor. It is written in an inherently unsafe combination of C and
head by eliminating the emulation paths described above.           assembly, putting greater needs for abstraction on the verifi-
                                                                   cation methodology. The verification proceeds in layers that
                                                                   progressively abstract implementation details in Rocq. Li et
6     Related Work                                                 al. [49] verify an early snapshot of the ARM CCA’s RMM
                                                                   implementation using the CertiKOS approach, incrementally
Commercial VM-based TEEs for x86 [14, 71], IBM Z [7], and          abstracting to a small top-level specification in Rocq. [27]
OpenPOWER [39] primarily target high-end server processors         propose continuous verification of the RMM using interactive
in data centers. In contrast, ACE is tailored for edge and high-   theorem proving (HOL4) for a core model and bounded model
end embedded RISC-V systems, a target space largely unad-          checking and concurrency-aware testing for the actual system
dressed by existing confidential computing solutions. ACE          to achieve practical coverage at the cost of weaker assurances.
also introduces (1) a novel single-step TVM promotion mech-        ACE carries spec and proofs along the code and continuously
anism that simplifies the ABI and eliminates intermediate at-      verifies the changes in CI. Verismo [85] functionally verifies
tack surfaces [22, 16], (2) static memory partitioning coupled     firmware implemented in Rust and running inside a TVM on
with formal verification as a way to build trust in the de-        AMD SEV-SNP [71]. It relies on the isolation boundary pro-
sign and implementation, and (3) an attestation primitive for      vided by the AMD platform security processor (PSP), while
RISC-V systems with unreliable network access. At the hard-        ACE’s TSM is functionally closer to firmware running inside
ware level, the canonical design of ACE runs on commod-            the PSP. Their approach to formal verification differs from
ity RISC-V platforms while remaining extensible to use-case-       ours by using Verus [45]: Verus is faster and more automated


                                                               12
for proving functional specifications, while RefinedRust offers     [4] Will Arthur and David Challener. A Practical Guide to
higher assurances due to its foundational verifier and smaller          TPM 2.0: Using the Trusted Platform Module in the New
TCB. Verus trusts unsafe Rust code, whereas we verify unsafe            Age of Security. Apress, 2015.
code. Additionally, Verus’s proofs require significant modifi-
cations to the Rust source code, while we verify idiomatic Rust     [5] Krste Asanovic, Paul Donahue, Greg Favor, John
code.                                                                   Hauser, James Kenney, David Kruckemyer, Shubu
   Komodo [25], ARM’s process-based TEE, has limited po-                Mukherjee, Stefan O’ear, Vernon Pang, Anup Pa-
tential to scale in terms of verification for VM-based TEE              tel, Josh Scheid, Ved Shanbhogue, and Andrew
because of its assembly implementation. Like ACE, the                   Waterman.       The risc-v advanced interrupt archi-
NOVA [73] microhypervisor minimizes the TCB by reduc-                   tecture, version 1.0.     https://github.com/riscv/riscv-
ing to the core functionality. Ongoing work [37] is verifying           aia/releases/download/1.0/riscv-interrupts-1.0.pdf, 2023.
a variant of NOVA. GlobalPlatform [29] publishes security           [6] Alexis Bagia, Vincent Quentin Ulitzsch, Daniël Trujillo,
standards for IoT devices through its Common Criteria Protec-           Mengyuan Li, Mengjia Yan, and Jean-Pierre Seifert. A
tion Profile (PP) for TEEs. ProveriT [38] is a verified formal          close look at rmp entry caching and its security impli-
specification of the GlobalPlatform PP for TEEs. In contrast,           cations in sev-snp. In Proceedings of the 14th Interna-
we do not aim to just verify the specification, but the concrete        tional Workshop on Hardware and Architectural Support
implementation of ACE.                                                  for Security and Privacy, pages 10–18, 2025.
                                                                    [7] Christian Bornträger, Jonathan D Bradbury, Reinhard
7    Conclusion                                                         Bündgen, Fadi Busaba, Lisa Cranton Heller, and Vik-
                                                                        tor Mihajlovski. Secure your cloud workloads with ibm
We have introduced principles and a methodology to design               secure execution for linux on ibm z15 and linuxone iii.
and implement high-assurance low-level systems. We have ap-             IBM Journal of Research and Development, 64(5/6):2–1,
plied these to build ACE, an open-source and royalty-free con-          2020.
fidential computing for edge and high-end embedded RISC-V
systems. Thus far we have formally verified the memory safety       [8] Bosch.   The next step in e/e architectures.
of a core part of the ACE implementation. The formal verifica-          https://www.bosch-mobility.com/en/
tion of the rest of the implementation and security properties          mobility-topics/ee-architecture/
is work in progress. Our work on ACE extends the RISC-V                 download-ee-architecture/, 2025.
CoVE spec with a deployment model targeting edge and high-
end embedded systems.                                               [9] Andrew Bresticker, Andy Dellow, Atish Patra, Atul
   We provide the first evaluation of VM-based confidential             Khare, Beeman Strong, Christian Bolis, Dingji Li, Dong
computing on commercially available RISC-V hardware. The                Du, Dylan Reid, Eckhard Delfs, Fabrice Marinet, Guer-
results show that a confidential VM running on this hardware            ney Hunt, Jiewen Yao, Kailun Qin, Manuel Offenberg,
(which does not have confidential computing-specific exten-             Nicholas Wood, Nick Kossifidis, Osman Koyuncu, Qing
sions) is practical. ACE incurs low performance overhead for            Li, Rajnesh Kanwal, Ravi Sahita, Rob Bradford, Samuel
process-intensive workloads and a competitive overhead up to            Ortiz, Steven Bellock, Vedvyas Shanbhogue, Wojciech
48% for multi-vCPU network-intensive workloads.                         Ozga, and Yann Loisel. Confidential vm extension (cove)
                                                                        for confidential computing. https://github.com/
                                                                        riscv-non-isa/riscv-ap-tee/releases/
References                                                              download/v0.7/riscv-cove.pdf, Last access
                                                                        May 2026.
 [1] Arm         confidential      compute         architec-
     ture.                    https://www.arm.com/ [10] Jo Van Bulck, Marina Minkin, Ofir Weisse, Daniel
     architecture/security-features/                              Genkin, Baris Kasikci, Frank Piessens, Mark Silber-
     arm-confidential-compute-architecture.                       stein, Thomas F. Wenisch, Yuval Yarom, and Raoul
     Last access May 2026.                                        Strackx. Foreshadow: Extracting the keys to the in-
                                                                  tel SGX kingdom with transient Out-of-Order execution.
 [2] https://httpd.apache.org/docs/2.4/                           In 27th USENIX Security Symposium (USENIX Secu-
     programs/ab.html, Last access May 2026.                      rity 18), page 991–1008, Baltimore, MD, August 2018.
                                                                  USENIX Association.
 [3] William A Arbaugh, David J Farber, and Jonathan M
     Smith. A secure and reliable bootstrap architecture. In [11] Fabiana Cambricoli.        Nova falha do Ministe-
     Proceedings. 1997 IEEE Symposium on Security and             rio da Saude expoe dados pessoais de mais
     Privacy (Cat. No. 97CB36097), pages 65–71. IEEE,             de 200 milhoes de brasileiros.            https://
     1997.                                                        saude.estadao.com.br/noticias/geral,


                                                               13
                                                               [22] Jesse De Meulemeester, David Oswald, Ingrid Ver-
     nova-falha-do-ministerio-da-saude-expoe-dados-pessoais-de-mais-de-200-milhoes,
     70003536340, Last access May 2026.                             bauwhede, and Jo Van Bulck. Battering RAM: Low-cost
                                                                    interposer attacks on confidential computing via dynamic
[12] Charly Castes, Neelu S. Kalani, Sofia Saltovskaia, Noé
                                                                    memory aliasing. In 47th IEEE Symposium on Security
     Terrier, Abel Vexina Wilkinson, and Edouard Bugnion.
                                                                    and Privacy (S&P), May 2026.
     Kicking the firmware out of the tcb with the miralis vir-
     tual firmware monitor. In Proceedings of the 2nd Work- [23] RTCA / EUROCAE. Formal methods supplement to do-
     shop on Kernel Isolation, Safety and Verification, KISV        178c [ed-12c] and do-178a [ed-109a]. DO-333/ED-218,
     ’24, 2024.                                                     2011.
[13] Katharina Ceesay-Seitz, Flavien Solt, and Kaveh Razavi. [24] Erhu Feng, Xu Lu, Dong Du, Bicheng Yang, Xueqiang
     uCFI: Formal Verification of Microarchitectural Control-      Jiang, Yubin Xia, Binyu Zang, and Haibo Chen. Scalable
     flow Integrity. In CCS, October 2024.                         memory protection in the PENGLAI enclave. In 15th
                                                                   USENIX Symposium on Operating Systems Design and
[14] Pau-Chen Cheng, Wojciech Ozga, Enriquillo Valdez,
                                                                   Implementation (OSDI 21), pages 275–294. USENIX
     Salman Ahmed, Zhongshu Gu, Hani Jamjoom, Huber-
                                                                   Association, July 2021.
     tus Franke, and James Bottomley. Intel tdx demystified:
     A top-down approach. arXiv preprint arXiv:2303.15540, [25] Andrew Ferraiuolo, Andrew Baumann, Chris Haw-
     2023.                                                         blitzel, and Bryan Parno. Komodo: Using verification
[15] Chromium.         The chromium projects - memory              to disentangle secure-enclave hardware from software.
     safety.     https://www.chromium.org/Home/                    In 26th ACM Symposium on Operating Systems Princi-
     chromium-security/memory-safety/, Last                        ples, pages 287–305. ACM, October 2017. The Komodo
     access May 2026.                                              specification, prototype implementation, and proofs are
                                                                   available at https://github.com/Microsoft/Komodo.
[16] Jalen Chuang, Alex Seto, Nicolas Berrios, Stephan van
     Schaik, Christina Garman, and Daniel Genkin. Tee.fail: [26] (Accepted) Anonymized for double-blindness purposes.
     Breaking trusted execution environments via ddr5 mem-         Bringing foundational verification to real-world rust
     ory bus interposition. In 47th IEEE Symposium on Secu-        code. In Object-oriented Programming, Systems, Lan-
     rity and Privacy (IEEE S&P ’26). IEEE Computer Soci-          guages, and Applications (OOPSLA), 2026.
     ety, 2026.                                               [27] Anthony C. J. Fox, Gareth Stockwell, Shale Xiong,
[17] Confidential Computing Consortium et al. A technical           Hanno Becker, Dominic P. Mulligan, Gustavo Petri, and
     analysis of confidential computing. Confidential Com-          Nathan Chong. A verification methodology for the arm®
     puting Consortium–Linux Foundation, Technical Report           confidential computing architecture: From a secure spec-
     v1, 3, 2022.                                                   ification to safe implementations. Proc. ACM Program.
                                                                    Lang., 7(OOPSLA1):376–405, 2023.
[18] Embedded Microprocessor Benchmark Consortium.
     coremark.           https://github.com/eembc/ [28] BSI Bundesamt für Sicherheit in der Informationstech-
     coremark, 2025.                                               nik. Railway applications -communication, signalling
                                                                   and processing systems - software for railway control and
[19] Victor Costan, Ilia Lebedev, and Srinivas Devadas. Sanc-      protection systems. In European Standard EN 50128,
     tum: Minimal hardware extensions for strong software          2011.
     isolation. In 25th USENIX Security Symposium (USENIX
     Security 16), 2016.                                      [29] GlobalPlatform. TEE protection profile v1.3. https:
                                                                   //globalplatform.org/specs-library/
[20] Common Criteria.         Common criteria for infor-           tee-protection-profile-v1-3.
     mation technology security evaluation:          Part 5:
     Pre-defined packages of security requirements. [30] Google.                   Google security blog - memory
     https://www.commoncriteriaportal.                             safe languages in android 13.                   https:
     org/files/ccfiles/CC2022PART5R1.pdf,                          //security.googleblog.com/2022/12/
     2022.                                                         memory-safe-languages-in-android-13.
                                                                   html, Last access May 2026.
[21] Natasha Dailey.          The hackers that attacked
     a major US oil pipeline say it was only for [31] RISC-V Platform Runtime Services Task Group.
     money — here’s what to know about DarkSide.                   Risc-v supervisor binary interface specification.
     https://www.businessinsider.com/                              https://github.com/riscv-non-isa/
     pipeline-cyber-attack-darkside-hacker-group-shutdown-ransomware-money-politics-oil-2021-5
                                                                   riscv-sbi-doc/releases/download/v2.0/
     op=1&r=US&IR=T, Last access May 2026.                         riscv-sbi.pdf, 2024.


                                                            14
[32] RISC-V Task Group. Risc-v platform-level interrupt con- [41] Intel.       Intel software guard extensions (in-
     troller specification, version 1.0. https://github.          tel    sgx).           https://www.intel.com/
     com/riscv/riscv-plic-spec/releases/                          content/www/us/en/developer/tools/
     download/1.0.0/riscv-plic-1.0.0.pdf,                         software-guard-extensions/overview.
     2023.                                                        html, Last access May 2026.

[33] Trusted Computing Group. DICE attestation architec- [42] Kirill A. Shutemov. Tdx: Enable dynamic pamt.
     ture. In TCG Resources, 2020.                                  https://lwn.net/Articles/1024661/, Last
                                                                    accessed May 2026.
[34] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (New-
     man) Wu, Jieung Kim, Vilhelm Sjöberg, and David [43] Paul Kocher, Jann Horn, Anders Fogh, , Daniel
     Costanzo. CertiKOS: An extensible architecture for             Genkin, Daniel Gruss, Werner Haas, Mike Hamburg,
     building certified concurrent os kernels. In OSDI, pages       Moritz Lipp, Stefan Mangard, Thomas Prescher, Michael
     653–669. USENIX Association, 2016.                             Schwarz, and Yuval Yarom. Spectre attacks: Exploiting
                                                                    speculative execution. In 40th IEEE Symposium on Se-
[35] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert            curity and Privacy (S&P’19), 2019.
     Krebbers, and Derek Dreyer. RefinedRust: Towards
     high-assurance verification of unsafe Rust programs. In [44] Pau Ku and Channing Tang.                 RISC-V IOPMP
     Rust Verification Workshop, 2023.                              Specification Document:            version 1.0.0-draft1.
                                                                    https://github.com/riscv-admin/iopmp/
[36] Red Hat.        Red hat in-vehicle operating system.           blob/main/specification/riscv_iopmp_
     https://www.redhat.com/en/resources/                           specification.pdf, Last access May 2026.
     in-vehicle-operating-system-datasheet,
     2025.                                                     [45] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias
                                                                    Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan
[37] Hoang-Hai Dang,          David Swasey,        and Gre-         Parno, and Chris Hawblitzel. Verus: Verifying rust pro-
     gory Malecha.            Towards modular specifica-            grams using linear ghost types. Proc. ACM Program.
     tion and verification of concurrent hypervisor-                Lang., 7(OOPSLA1):286–315, 2023.
     based isolation.          https://www.bluerock.
     io/formal-methods-publications/                           [46] Stella Lau, Thomas Bourgeat, Clément Pit-Claudel, and
     towards-modular-specification, 2024.                           Adam Chlipala. Specification and verification of strong
                                                                    timing isolation of hardware enclaves. In Proceedings of
[38] Jilin Hu, Fanlang Zeng, Yongwang Zhao, Zhuoruo                 the 2024 on ACM SIGSAC Conference on Computer and
     Zhang, Leping Zhang, Jianhong Zhao, Rui Chang, and             Communications Security, CCS ’24, 2024.
     Kui Ren. Proverit: A parameterized, composable, and
     verified model of tee protection profile. IEEE Trans. De- [47] Dayeol Lee, Kevin Cheang, Alexander Thomas,
     pendable Secur. Comput., 21(6):5341–5358, November             Catherine Lu, Pranav Gaddamadugu, Anjo Vahldiek-
     2024.                                                          Oberwagner, Mona Vij, Dawn Song, Sanjit A. Seshia,
                                                                    and Krste Asanovic. Cerberus: A formal approach to
[39] Guerney D. H. Hunt, Ramachandra Pai, Michael V. Le,            secure and efficient enclave memory sharing. In Pro-
     Hani Jamjoom, Sukadev Bhattiprolu, Rick Boivie, Lau-           ceedings of the 2022 ACM SIGSAC Conference on Com-
     rent Dufour, Brad Frey, Mohit Kapur, Kenneth A. Gold-          puter and Communications Security, CCS ’22, page
     man, Ryan Grimm, Janani Janakirman, John M. Lud-               1871–1885, New York, NY, USA, 2022. Association for
     den, Paul Mackerras, Cathy May, Elaine R. Palmer,              Computing Machinery.
     Bharata Bhasker Rao, Lawrence Roy, William A. Starke,
     Jeff Stuecheli, Enriquillo Valdez, and Wendel Voigt. [48] Dayeol Lee, David Kohlbrenner, Shweta Shinde, Krste
     Confidential Computing for OpenPOWER. In Proceed-              Asanović, and Dawn Song. Keystone: An open frame-
     ings of the Sixteenth European Conference on Computer          work for architecting trusted execution environments.
     Systems, EuroSys ’21, 2021.                                    In Proceedings of the Fifteenth European Conference
                                                                    on Computer Systems, pages 1–16, 2020. Repository:
[40] Sander Huyghebaert, Steven Keuchel, Coen De Roover,            https://github.com/orgs/keystone-enclave/repositories.
     and Dominique Devriese. Formalizing, verifying and ap-
     plying isa security guarantees as universal contracts. In [49] Xupeng Li, Xuheng Li, Christoffer Dall, Ronghui Gu, Ja-
     Proceedings of the 2023 ACM SIGSAC Conference on               son Nieh, Yousuf Sait, and Gareth Stockwell. Design and
     Computer and Communications Security, pages 2083–              verification of the arm confidential compute architecture.
     2097, 2023.                                                    In OSDI, pages 465–484. USENIX Association, 2022.


                                                             15
[50] Arthur D Little.    Virtualizing mobile networks.             i/o (cove-io) for confidential computing on risc-
     the silver bullet for operators to master 5g?                 v platforms.       https://lists.riscv.org/
     https://www.adlittle.com/sites/                               g/tech-ap-tee-io/attachment/47/0/
     default/files/reports/adl_mobile_                             riscv-cove-io-0.1.0_comments_QCOM.pdf,
     network_architecture.pdf, 2020.                               Last access May 2026.

[51] Marvell.    Liquidsecurity® 2 hsm adapter. a uni- [62] Wojciech Ozga, Guerney D. H. Hunt, Michael V. Le,
     fied hsm for the multi-cloud era. https://www.         Elaine R. Palmer, and Avraham Shinnar. Towards a for-
     marvell.com/content/dam/marvell/en/                    mally verified security monitor for vm-based confiden-
     public-collateral/security-solutions/                  tial computing. In Proceedings of the 12th International
     marvell-liquidsecurity2-hsm-adapters-product-brief.    Workshop on Hardware and Architectural Support for
     pdf, 2024.                                             Security and Privacy, HASP2023, 2023.
[52] Daniel Matichuk, Toby Murray, June Andronick, Ross [63] PCI-SIG.           Tee device interface security protocol
     Jeffery, Gerwin Klein, and Mark Staples. Empirical           (tdisp).    https://members.pcisig.com/wg/
     study towards a leading indicator for cost of formal         PCI-SIG/document/18268, 2022.
     software verification. In International Conference on
     Software Engineering, page 11, Firenze, Italy, February [64] Xiang (Jenny) Ren, Kirk Rodrigues, Luyuan Chen,
     2015.                                                        Camilo Vega, Michael Stumm, and Ding Yuan. An anal-
                                                                  ysis of performance evolution of linux’s core operations.
[53] Nicholas D. Matsakis and Felix S. Klock, II. The rust        Huntsville, Ontario, Canada, October 2019.
     language. In Proceedings of HILT, 2014.
                                                             [65] Reuters.         Foreign Hackers Probe European
[54] Masanori Misono, Dimitrios Stavrakakis, Nuno Santos,
                                                                  Critical    Infrastructure   Networks:          Sources.
     and Pramod Bhatotia. Confidential vms explained: An
                                                                  https://www.reuters.com/article/
     empirical analysis of amd sev-snp and intel tdx. Pro-
                                                                  us-britain-cyber-idINKBN19V1C7,                      Last
     ceedings of the ACM on Measurement and Analysis of
                                                                  access May 2026.
     Computing Systems, 8(3):1–42, 2024.

[55] NIST. Cve-2021-44228 detail. https://nvd.nist. [66] RISC-V International, Western Digital Corporation or
     gov/vuln/detail/cve-2021-44228, 2021.                       its affiliates. RISC-V Open Source Supervisor Bi-
                                                                 nary Interface (OpenSBI). https://github.com/
[56] Nvidia.     Nvidia multi-instance gpu.        https:        riscv-software-src/opensbi, Last access May
     //www.nvidia.com/en-us/technologies/                        2026.
     multi-instance-gpu, Last access May 2026.
                                                            [67] Ravi Sahita, Andy Dellow, Dean Liberty, Deepak
[57] National Institute of Standards and Technology              Gupta, Guerney Hunt, Krste Asanovic, Mark Hill, Nick
     (NIST). Security requirements for cryptographic mod-        Wood, Osman Koyuncu, Paul Elliott, Ved Ortiz, Samuel
     ules.   https://csrc.nist.gov/pubs/fips/                    abd Shanbhogue, and Wojciech Ozga. RISC-V SmmTT:
     140-3/final, 2019.                                          Supervisor Domain Access Protection. https://
                                                                 github.com/riscv/riscv-smmtt/, Last access
[58] National Institute of Standards and Technology (NIST).
                                                                 May 2026.
     Cve-2024-3094 detail. https://nvd.nist.gov/
     vuln/detail/cve-2024-3094, 2024.                       [68] Ravi Sahita, Vedvyas Shanbhogue, Andrew Bresticker,
                                                                 Atul Khare, Atish Patra, Samuel Ortiz, Dylan Reid, and
[59] National Institute of Standards and Technology (NIST).
                                                                 Rajnesh Kanwal. Cove: Towards confidential computing
     Fips 203:      Module-lattice-based key-encapsulation
                                                                 on RISC-V platforms. In Proceedings of the 20th ACM
     mechanism standard. https://csrc.nist.gov/
                                                                 International Conference on Computing Frontiers, pages
     pubs/fips/203/final, 2024.
                                                                 315–321, 2023.
[60] Omdia.      Risc-v adoption will be accelerated by
     ai, according to new omdia research.          https: [69] David Schrammel, Moritz Waser, Lukas Lamster, Mar-
     //omdia.tech.informa.com/pr/2024/may/                       tin Unterguggenberger, and Stefan Mangard. Spear-v:
                                                                 Secure and practical enclave architecture for risc-v. In
     risc-v-adoption-will-be-accelerated-by-ai-according-to-new-omdia-research,
     Last accessed May 2026.                                     Proceedings of the 2023 ACM Asia Conference on Com-
                                                                 puter and Communications Security, ASIA CCS ’23,
[61] Samuel Ortiz, Jiewen Yao, Ravi Sahita, and Ved-             page 457–468, New York, NY, USA, 2023. Association
     vyas Shanbhogue.           Confidential vm extension        for Computing Machinery.


                                                            16
[70] Sandro Schönborn, Thanikesavan Sivanthi, Anna                 20241101.           https://github.com/riscv/
     Kulmala,     Henry Niveri,       and Robert Birke.             riscv-isa-manual/releases/download/
     The virtues of virtualization:        Enhancing effi-          riscv-isa-release-f32140c-2025-05-05/
     ciency in medium-voltage substations.          https:          riscv-privileged.pdf, Last access May 2026.
     //global.abb/group/en/innovation/
     news/the-virtues-of-virtualization,                       [81] Samuel Weiser, Mario Werner, Ferdinand Brasser, Maja
     2023.                                                          Malenko, Stefan Mangard, and Ahmad-Reza Sadeghi.
                                                                    Timber-v: Tag-isolated memory bringing fine-grained
[71] AMD Sev-Snp. Strengthening vm isolation with in-               enclaves to risc-v. 01 2019.
     tegrity protection and more. White Paper, January,
     53(2020):1450–1465, 2020.                                 [82] Inc. Wind River Systems. Requirements for virtu-
                                                                    alization in next-generation industrial control sys-
[72] Frans Sijstermans.     Risc-v at nvidia: One archi-            tems. https://www.windriver.com/sites/
     tecture, dozens of applications, billions of pro-              default/files/2022-02/438822677.pdf,
     cessors. keynote, risc-v summit north america,                 2018.
     october 2024.        https://riscv.org/blog/
     how-nvidia-shipped-one-billion-risc-v-cores-in-2024/,     [83] Mingjie Yan and Kartik Gopalan. Performance over-
     Last accessed May 2026.                                        heads of confidential virtual machines. In 2023 31st
                                                                    International Symposium on Modeling, Analysis, and
[73] Udo Steinberg and Bernhard Kauer.             NOVA: a          Simulation of Computer and Telecommunication Systems
     microhypervisor-based secure virtualization architecture.      (MASCOTS), pages 1–8. IEEE, 2023.
     In EuroSys, pages 209–222. ACM, 2010.
                                                               [84] Jason Zhijingcheng Yu, Shweta Shinde, Trevor E. Carl-
[74] Dina Temple-Raston. A ’worst nightmare’ cyberattack:           son, and Prateek Saxena. Elasticlave: An efficient mem-
     The untold story of the solarwinds hack. https:                ory model for enclaves. In 31st USENIX Security Sympo-
     //www.npr.org/2021/04/16/985439655/                            sium (USENIX Security 22), pages 4111–4128, Boston,
                                                                    MA, August 2022. USENIX Association.
     a-worst-nightmare-cyberattack-the-untold-story-of-the-solarwinds-hack,
     Last access May 2026.
                                                               [85] Ziqiao Zhou, Anjali, Weiteng Chen, Sishuai Gong, Chris
[75] The Coq Team. The Coq proof assistant. https://                Hawblitzel, and Weidong Cui. Verismo: A verified secu-
     coq.inria.fr/, Last access May 2026.                           rity module for confidential vms. In OSDI, pages 599–
                                                                    614. USENIX Association, 2024.
[76] The New York Times.           Hack of Saudi Petro-
     chemical Plant Was Coordinated From Rus-
     sian Institute.           https://www.nytimes.
     com/2018/10/23/us/politics/
     russian-hackers-saudi-chemical-plant.
     html, Last access May 2026.
[77] The New York Times. Hackers Are Targeting Nuclear
     Facilities, Homeland Security Dept. and F.B.I. Say.
     https://www.nytimes.com/2017/07/06/
     technology/nuclear-plant-hack-report.
     html, Last access May 2026.
[78] TrustedFirmware.org. About OP-TEE. https:
     //optee.readthedocs.io/en/latest/
     general/about.html#about-op-tee.
[79] VMWare.      Intelligent operations for new
     5g and edge ecosystems:    A game changer?
     https://www.vmware.com/docs/
     vmware-intelligent-operations-for-new-five-g-and-edge-ecosystems-a-game-changer,
     2021.
[80] Andrew Waterman, Krste Asanovi, and John
     Hauser. The RISC-V Instruction Set Manual, Vol-
     ume II: Privileged Architecture, Document Version


                                                            17
