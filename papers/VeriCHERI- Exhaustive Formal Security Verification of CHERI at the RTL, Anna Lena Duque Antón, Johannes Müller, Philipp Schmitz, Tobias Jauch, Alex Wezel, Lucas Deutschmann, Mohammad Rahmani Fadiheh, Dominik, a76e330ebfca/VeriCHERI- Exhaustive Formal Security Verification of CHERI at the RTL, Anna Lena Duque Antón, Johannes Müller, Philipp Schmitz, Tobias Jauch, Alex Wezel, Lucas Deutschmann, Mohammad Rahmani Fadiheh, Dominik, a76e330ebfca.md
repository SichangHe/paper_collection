                                                                     VeriCHERI:
                                              Exhaustive Formal Security Verification of CHERI at the RTL
                                                  Anna Lena Duque Antón∗                                         Johannes Müller∗                                Philipp Schmitz
                                                   RPTU Kaiserslautern-Landau                              RPTU Kaiserslautern-Landau                     RPTU Kaiserslautern-Landau
                                                     Kaiserslautern, Germany                                 Kaiserslautern, Germany                        Kaiserslautern, Germany
                                                    anna.duqueanton@rptu.de                                 johannes.mueller@rptu.de                           schmitzp@rptu.de

                                                             Tobias Jauch                                             Alex Wezel                             Lucas Deutschmann
                                                   RPTU Kaiserslautern-Landau                              RPTU Kaiserslautern-Landau                     RPTU Kaiserslautern-Landau
                                                     Kaiserslautern, Germany                                 Kaiserslautern, Germany                        Kaiserslautern, Germany
arXiv:2407.18679v1 [cs.CR] 26 Jul 2024




                                                      tobias.jauch@rptu.de                                        wezel@rptu.de                           lucas.deutschmann@rptu.de

                                                    Mohammad R. Fadiheh                                           Dominik Stoffel                                Wolfgang Kunz
                                                         Stanford University                               RPTU Kaiserslautern-Landau                     RPTU Kaiserslautern-Landau
                                                       Stanford, United States                               Kaiserslautern, Germany                        Kaiserslautern, Germany
                                                       fadiheh@stanford.edu                                  dominik.stoffel@rptu.de                        wolfgang.kunz@rptu.de

                                         ABSTRACT                                                                              Enhanced RISC Instructions (CHERI) [25]. CHERI is designed to en-
                                         Protecting data in memory from attackers continues to be a con-                       hance RISC instruction set architectures (ISAs) with fine-grained
                                         cern in computing systems. CHERI is a promising approach to                           memory protection directly implemented and enforced in the hard-
                                         achieve such protection, by providing and enforcing fine-grained                      ware (HW). Its architectural concept enables the memory isolation
                                         memory protection directly in the hardware. Creating trust for the                    infrastructure to enforce memory compartmentalization [22, 24].
                                         entire system stack, however, requires a gap-free verification of                        Establishing trust in the proposed mechanisms is particularly
                                         CHERI’s hardware-based protection mechanisms. Existing verifi-                        important for security-focused solutions, and the path to build this
                                         cation methods for CHERI target the abstract ISA model rather                         trust is exhaustive verification.
                                         than the underlying hardware implementation. Fully ensuring the                          In previous work, considerable effort has been put into formal
                                         CHERI security guarantees for a concrete RTL implementation is a                      verification of CHERI at the ISA level. In [15, 19] an HOL model
                                         challenge in previous flows and demands high manual efforts.                          of the CHERI ISA based on SAIL [3] is subjected to security veri-
                                             This paper presents VeriCHERI, a novel approach to security ver-                  fication. Multiple security objectives are formulated and exhaus-
                                         ification. It is conceptionally different from previous works in that                 tively proven on the SAIL model. This is an important contribution
                                         it does not require any ISA specification. Instead of checking com-                   towards establishing trust in the security architecture. However,
                                         pliance with a golden ISA model, we check against well-established                    verification results obtained for the ISA level do not translate into
                                         global security objectives of confidentiality and integrity. Fully cov-               security guarantees for a HW implementation of the ISA. Addi-
                                         ering these objectives, VeriCHERI uses as few as four unbounded                       tional functional verification is required to prove compliance of the
                                         properties to exhaustively prove or disprove any vulnerability. We                    implementation with the previously verified ISA.
                                         demonstrate the effectiveness and scalability of VeriCHERI on a                          In an attempt to bridge this gap, [12] proposes to verify the
                                         RISC-V based processor implementing a CHERI variant.                                  CHERI-related subset of the ISA by translating the corresponding
                                                                                                                               parts of the SAIL ISA model to SystemVerilog Assertions (SVA)
                                         KEYWORDS                                                                              properties to be checked against the register transfer level (RTL)
                                                                                                                               implementation of a processor. This is a significant improvement
                                         Memory Isolation, Formal Verification, Hardware Security
                                                                                                                               over previous flows. However, even if all security features, as given
                                                                                                                               by the considered ISA subset, are proven to be functionally correct,
                                         1    INTRODUCTION                                                                     other parts of the design, not included in the proofs, may still violate
                                         In a world full of complex computing systems, rigid and trustworthy                   security. Therefore, this approach, in spite of high manual effort,
                                         security mechanisms are in high demand. A promising contribution                      may still fall short of guaranteeing security for the design under
                                         to making systems more secure is proposed by Capability Hardware                      verification.
                                                                                                                                  Apparently, a gap-free formal verification of the processor at
                                         ∗ Both authors contributed equally to this research.
                                                                                                                               the RTL is desirable. While methods for so called “complete” [23]
                                                                                                                               formal verification of processors exist and are practiced in industry,
                                         To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ                            for many vendors the involved efforts and cost remain, until today,
                                         © 2024 Copyright held by the owner/author(s).
                                         This is the author’s version of the work. It is posted here for your personal use.    prohibitively high.
                                         Not for redistribution. The definitive Version of Record was published in IEEE/ACM       An additional concern is that security verification referring to a
                                         International Conference on Computer-Aided Design (ICCAD ’24), October 27–31, 2024,
                                         New York, NY, USA, https://doi.org/10.1145/3676536.3676841.
                                                                                                                               time-abstract ISA model misses non-functional security vulnerabili-
                                                                                                                               ties like timing side channels. Consequently, a HW implementation
To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ                                                            A. Duque Antón, J. Müller et al.


proven to be fully compliant with the ISA model may well contain          them to a special purpose, e.g., context switches. Legal memory
such vulnerabilities.                                                     accesses require valid capabilities that hold corresponding permis-
   In comparison to formal verification procedures carried out            sions and whose bounds include the accessed address. Instruction
for CHERI previously, the methodology proposed in this paper,             fetches are protected by the Program Counter Capability (PCC)
VeriCHERI, uses a conceptually different approach. We start with          which extends the normal PC with corresponding capability infor-
a general, formalized notion of security w.r.t. confidentiality and       mation.
integrity, and derive unbounded properties from it. By no longer             Handling capabilities instead of plain integer pointers requires
deriving properties from the abstract ISA model but directly target-      changes to the ISA as well as to the HW. The ISA is extended by ad-
ing the global security objectives, we eliminate the risk of missing      ditional instructions that are needed for manipulating capabilities
security issues. In addition, VeriCHERI detects vulnerabilities that      such as loading, storing or modifying them. Legal capability modifi-
can only be observed on the timing-accurate RTL implementation            cations may only restrict but never expand the access permissions
and which are not represented on the high-level ISA model.                or address bounds. Attempts to broaden the access rights result
   Our contributions are, in particular:                                  in clearing the valid tag of the capability and therefore invalidat-
     • We propose VeriCHERI, a verification framework that ex-            ing it for further use. This important principle is called capability
        haustively detects all confidentiality and integrity vulnera-     monotonicity. The HW implementation of the ISA changes includes
        bilities due to functional bugs. In addition, the framework       adaptation of the register file to enable the storage of capabilities
        covers all vulnerabilities to Meltdown-style attacks. At its      and augmentation of the memory locations with a tag bit indicating
        core, VeriCHERI consists of only four SVA properties, which       the integrity of the memory content. Software (SW) running on a
        are checked against the RTL model of the design under veri-       capability-enhanced processor starts with a set of initial capabilities
        fication (DUV).                                                   provided by the architecture. All other capabilities can be derived
     • VeriCHERI is a “spec-free” approach: The security properties       by SW according to the capability monotonicity property. CHERI
        are derived from well-established, general security objectives    supports two modes: pure capability and hybrid. In hybrid mode
        rather than from a specification or formalized ISA model. Se-     memory accesses using plain “legacy” integer pointers are legal
        curity guarantees are established directly on the RTL model       to support legacy code. Pure capability mode only allows memory
        and do not have to be imported and rewritten from a higher-       accesses using capabilities.
        level model. This has the key advantage of avoiding the high
        costs involved in complete formal verification — and of still
        being exhaustive w.r.t. our security goals.
                                                                          2.2    Related Work
     • From the general security objectives we derive scalable prop-      Several works exist that verify security properties on the architec-
        erties by developing a symbolic representation of all possi-      ture definition of CHERI. In [19] the CHERI-MIPS ISA is formulated
        ble tasks potentially violating the security objectives. This     in the instruction set architecture description languages L3 [9] and
        step significantly improves scalability since it allows us to     SAIL [3]. Security properties are then formally proven with the-
        formulate unbounded properties considering only a single          orem provers, e.g., Isabelle [20], on the ISA model. Similarly, [4]
        execution trace over a finite number of clock cycles, as op-      and [15] verify security properties on the capability-enhanced ARM
        posed to the security objectives describing infinite behavior     Morello architecture specification. The resulting ISA formalization
        by comparing two execution traces. Our methodology leads          helped to discover security issues and can be used to generate test
        to proofs that are independent of any specific application or     cases for pre-silicon validation.
        capability configuration.                                            For both, CHERI-MIPS, as well as ARM Morello, ISA verifica-
     • We present a case study on the CHERIoT Ibex core [2] and           tion took a significant effort of three to four person-years. The
        demonstrate the efficacy and scalability of VeriCHERI. We         conducted proofs verify security aspects only for the architectural
        detected security bugs including a vulnerability to a potential   ISA model — they do not verify security properties on an actual
        Meltdown-style timing attack. This emphasizes the need for        microarchitectural implementation of the ISA. Proving a microar-
        exhaustive security verification techniques.                      chitectural implementation secure requires additional verification
   The remainder of the paper provides background on CHERI                steps and a sound translation of the ISA properties to microarchitec-
in Sec. 2.1 and compares the proposed work to related work in             tural properties of a specific HW implementation. This may involve
Sec. 2.2. We then derive a set of properties from our abstract security   high manual effort and is prone to errors. Furthermore, certain
objective in Sec. 3 and use the properties in the novel VeriCHERI         classes of vulnerabilities are not captured by the ISA model due to
verification flow presented in Sec. 4. In Sec. 5, we present a case       missing information, such as side channels based on timing. Re-
study and conclude the paper with Sec. 6.                                 garding transient execution side channel attacks, [11] shows that a
                                                                          CHERI-RISC-V HW implementation is vulnerable to several classes
2 BACKGROUND                                                              of Spectre attacks. In addition, further analysis [10] has identified a
                                                                          vulnerability of CHERI systems to specific Meltdown-style attacks
2.1 CHERI Protection                                                      and transient privilege escalation. Although this type of vulnera-
CHERI introduces capability-based pointer protection in HW [25].          bility can be mitigated by dedicated security mechanisms, other
Capabilities extend classical address pointers (i.e., plain integers)     work has shown that even minor changes in implementation can
with access permissions (e.g., read, write and execute), address          (re-)open microarchitectural side channels [7]. This drives the need
bounds and a valid tag. Capabilities are typed to support restricting     for exhaustive security verification at the microarchitectural level.
VeriCHERI:
Exhaustive Formal Security Verification of CHERI at the RTL
                                                                                                 To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ

   Techniques for processor verification at the microarchitectural           may be initiated by exceptions or interrupts or by dedicated control-
level have been proposed for various architectures. In [21] formal           flow transfers through specially typed capabilites. Each task has
properties are machine-translated from the ARM ISA specification             at its disposal a set of CHERI capabilities which grant access to a
and checked on commercial ARM processors. A verification frame-              subset of the memory. For each task running on the processor, we
work is also proposed for x86, handling the complexity posed by a            partition 𝑀 into:
microcoded processors [13]. The work of [12] verifies properties on               • 𝑀pub : denoting all public memory locations, i.e., all mem-
CHERI Flute [8], a HW implementation of a capability-enhanced                        ory locations which are accessible with the attacker task’s
processor. Here, the properties are translated manually from the                     capabilities;
SAIL specification of the CHERI-specific instructions in the CHERI-               • 𝑀prot : denoting all memory locations protected from the
RISC-V ISA to SystemVerilog Assertions. As discussed above, prop-                    attacker task, i.e., all memory locations which are not acces-
erties derived from the ISA specification may miss security vulner-                  sible with the attacker task’s capabilities.
abilities due to the semantic gap between the specification and the
                                                                                Among the tasks, we assume an attacker with the objective to
HW implementation. In contrast, the methodology presented in this
                                                                             breach the memory isolation created by the CHERI capabilities.
paper verifies global security properties based on a well-defined
                                                                             In particular, the attacker tries to read protected data or execute
security objective (cf. Sec. 3.1). Our proofs cover all security as-
                                                                             protected instructions, i.e., violate confidentiality, or manipulate
pects w.r.t. our security objective, including vulnerabilities that are
                                                                             protected data, i.e., violate integrity. Confidentiality and integrity
not visible at the ISA level and therefore not captured by previous
                                                                             can be expressed as properties of the HW under SW constraints
works.
                                                                             as given by capabilities. We formulate these properties based on
   As an alternative, complete formal verification [23] can be used
                                                                             the strong and well-established notion of non-interference [14].
to cover all possible operations within a HW implementation by
                                                                             Non-interference defines high and low locations in the design and
operation-level properties. For example, CS2QED [6] provides a
                                                                             requires that the low locations are not affected by the high loca-
highly automated and complete verification technique that can
                                                                             tions [5]. We formulate a 2-safety non-interference computation
detect both single- and multiple-instruction bugs in in-order pro-
                                                                             tree logic (CTL) property for confidentiality (Eq. 1) and integrity
cessor designs. The drawback of this and related approaches with
                                                                             (Eq. 2) of protected data. We extend our notation of state variables
regards to security is that even complete functional verification
                                                                             by the $-operator to denote the valuation of a state variable set, i.e.,
cannot detect security vulnerabilities that are not caused by bugs
                                                                             the set of value assignments to the state variables.
in the implementation, such as side channels. To cope with such
                                                                                For any task that can run on the system, i.e., for any choice of
threats, Unique Program Execution Checking (UPEC) [7] enables
                                                                             𝑀prot and 𝑀pub , it must hold:
spec-free security verification based on formalized threat models.
The global security guarantee provided by UPEC depends on the                            AG ( $𝑀pub = $𝑀pub
                                                                                                        ′
                                                                                                            ∧ $𝑃 = $𝑃 ′
underlying threat model. So far, this verification methodology has                                                                                     (1)
                                                                                               → AG ( $𝑀pub = $𝑀pub
                                                                                                                ′
                                                                                                                    ∧ $𝑃 = $𝑃 ′ ) )
not been extended to verify CHERI.
   The work of [16] introduces a HW verification approach based
on information flow properties. Information flow tracking models                      AG ( $𝑀prot = $𝑀prot
                                                                                                      ′
                                                                                                           → AG ( $𝑀prot = $𝑀prot
                                                                                                                             ′
                                                                                                                                  ))                   (2)
are tailored to specific security properties, including confidential-
                                                                                In accordance to their 2-safety nature, both properties take two
ity and integrity properties. However, application of this method
                                                                             instances (primed′ and non-primed) of the HW model into con-
requires a priori knowledge of potential vulnerabilities. Therefore,
                                                                             sideration. For the confidentiality property in Eq. 1, the memory
the method is not exhaustive.
                                                                             locations in 𝑀prot are considered high locations, while the locations
                                                                             accessible by the attacker 𝑀pub and 𝑃 are considered low locations.
3 FORMAL MODEL
                                                                             By assuming $𝑀pub = $𝑀pub     ′   and $𝑃 = $𝑃 ′ we ensure that the
3.1 Security Objective                                                       corresponding state variables are equal between the two model in-
In this paper we assume a single-threaded capability-enhanced                stances. The only difference between the two instances consists in
single-core processor with a memory for instructions and data. We            state variables of 𝑀prot . The property expresses that this difference
model the HW as a finite state machine (FSM), (𝑆, 𝑆 0, 𝐼, 𝑂, 𝜆, 𝜎), with     never affects the low locations, 𝑀pub and 𝑃, of the attacker task.
a set of states 𝑆, an initial state 𝑆 0 , a set of inputs 𝐼 and outputs 𝑂,   No protected information should ever become accessible to the
a state transition function 𝜆 : 𝑆 × 𝐼 → 𝑆 and an output function             attacker task. The integrity property in Eq. 2 expresses interference
𝜎 : 𝑆 × 𝐼 → 𝑂. We consider 𝑆 to be valuations of the state variables         in the opposite direction, by considering 𝑀prot to be the locations
and denote 𝑍 as the set of all state variables. In the RTL model, 𝑍          that must not be influenced by the locations 𝑀pub and 𝑃. In other
corresponds to all state-holding elements, i.e., registers, microar-         words, the attacker task must never be able to modify protected
chitectural buffers, caches, and memory locations. We partition 𝑍            information.
into two disjoint subsets:
     • 𝑃: containing all state variables in the processor;                   3.2    Modeling Confidentiality and Integrity
     • 𝑀: containing all memory locations.                                   Proving the CTL properties of Eq. 1 and Eq. 2 on realistic designs
   We further assume the processor to be executing (mutually dis-            poses two major challenges. The first challenge consists in modeling
trusting) tasks and a trusted entity, such as an operating system, to        𝑀pub and 𝑀prot . As defined in Sec. 3.1, the partitioning of all memory
securely manage context switches between tasks. Context switches             locations into 𝑀pub and 𝑀prot is determined by the capabilities
To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ                                                           A. Duque Antón, J. Müller et al.


available to the attacker task. In the RTL model of the HW, these         1   1 - safety - confidentiality :
capabilities are specified by configurations of address ranges, access    2   assume :
permissions and additional information in capability registers and        3       at t : cheri_protected ( symbolic_addr ) ;
                                                                          4   prove :
buffers. This means, we need to express 𝑀pub and 𝑀prot in terms of        5       at t : read_mem_access → mem_addr ≠ symbolic_addr ;
capabilities in the RTL.
   The second challenge is posed by creating a proof that considers                     (a) Interval property for confidentiality
all possible attacker tasks. This requires considering all possible di-
                                                                          1   1 - safety - integrity :
visions of memory locations into 𝑀pub and 𝑀prot , without rendering       2   assume :
the proof unscalable.                                                     3       at t : cheri_protected ( symbolic_addr ) ;
   Our key idea to overcome these challenges is the following: In-        4   prove :
stead of modeling 𝑀pub and 𝑀prot explicitly by using state variables      5       at t : write_mem_access → mem_addr ≠ symbolic_addr ;
for memory locations, we model memory locations implicitly by
their unique addresses. This is possible because a violation of the                        (b) Interval property for integrity
two non-interference properties Eq. 1 (confidentiality) and Eq. 2 (in-
tegrity) can only happen if the processor performs a memory access
to 𝑀prot , assuming a correct memory implementation. (Note that               Figure 1: 1-safety non-interference interval properties
this is true even though 𝑀prot does not appear in Eq. 1.) As a result,
we replace the consequent of the implication in the CTL proper-
ties from Eq. 1 and Eq. 2 by checking if the processor performs
a memory access to an address belonging to 𝑀prot . We introduce           1   Monotonicity :
                                                                          2   assume :
the following macros, which are formulated using the processor’s          3     at t :     cheri_protected ( symbolic_addr ) ;
memory port signals:                                                      4   prove :
     • read_mem_access: is true when the processor requests a read        5     at t + 1 : cheri_protected ( symbolic_addr ) ;

       access to the memory.
     • write_mem_access: is true when the processor requests a
                                                                                   Figure 2: Interval property for monotonicity
       write access to the memory.
     • mem_addr: is the address for which the processor requests
       the memory access (read or write)                                  the properties do not contain a universal quantifier, i.e., 𝐴𝐺, in
    This leaves the challenge of covering all possible partitions of      the consequent of the implication. Instead, the properties describe
memory locations into 𝑀pub and 𝑀prot without enumerating all              behavior without transitioning between states. With regard to the
possible configurations explicitly. We solve this problem by intro-       RTL model, this means that the property formulates behavior in a
ducing a new symbolic address for memory locations in 𝑀prot , which       single clock cycle. Properties describing behavior spanning a finite
is not connected to or constrained by the HW model and can thus           number of clock cycles can be formulated as interval properties [23].
freely be chosen by the solver of a property checking tool. Further-      This includes the CTL properties in Eq. 3 and Eq. 4.
more, we introduce a new macro cheri_protected(symbolic_addr).               Interval properties can deliver an unbounded proof result due to
This macro constrains all registers and microarchitectural buffers        their symbolic starting state. In interval property checking (IPC),
holding capabilities to deny accesses to the symbolic address. How        the property checker can fast-forward to any starting state violating
cheri_protected is determined systematically is described in Sec. 4.      the property without the need to unroll from reset. The interval
The described modifications simplify the properties of Eq. 1 and Eq. 2    properties for our confidentiality and integrity security objectives
to:                                                                       are presented in Fig. 1a and Fig. 1b.

 AG ( cheri_protected(symbolic_addr)                                      3.3     Proving Monotonicity
        → ( read_mem_access → mem_addr ≠ symbolic_addr ) )                A successful proof of the interval properties in Fig. 1a and Fig. 1b
                                                         (3)              verifies that an attacker task cannot violate the confidentiality and
                                                                          integrity objectives of our threat model — as long as the attacker
 AG ( cheri_protected(symbolic_addr)                                      task’s capabilities comply with the cheri_protected macro. There-
                                                                          fore, in order to achieve global proof validity, we need to prove
        → ( write_mem_access → mem_addr ≠ symbolic_addr ) )
                                                                          that cheri_protected holds for the design during any attacker task
                                                         (4)
                                                                          execution.
   Apart from the symbolic address, the properties in Eq. 3 and Eq. 4        We can easily prove this invariant by induction. For proving the
have two notable differences compared to the non-interference             induction base, we have to show that the state space constrained by
properties of Eq. 1 and Eq. 2. Firstly, by modeling memory locations      cheri_protected is reachable from reset. (We omit the induction base
as addresses, the properties no longer need to explicitly compare         property for reasons of space.) The induction step is performed by
two design instances to detect a security violation. This allows us       the interval property depicted in Fig. 2.
to formulate the properties in Eq. 3 and Eq. 4 as 1-safety proper-           As introduced in Sec. 3.2, the cheri_protected(symbolic_addr)
ties, proving the absence of any illegal memory access. Secondly,         macro consists of constraints for all registers or microarchitectural
VeriCHERI:
Exhaustive Formal Security Verification of CHERI at the RTL
                                                                                                To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ


buffers that are accessible by the current task and that hold a ca-            It may happen that accesses to protected data are executed in
pability. Each constraint specifies that the respective capability          parallel with an access control check evaluating legality of the ac-
does not grant access to the symbolic address, i.e., to any address         cess. In case it is not legal, an exception is raised and the loaded
pointing to a memory location in 𝑀prot . The macro also includes            data is discarded. However, if the discarded data leaves a footprint
constraints for capabilities loaded from and stored to memory by            in the microarchitecture, e.g., in a data cache, and the timing of
restricting the memory port signals in an analogous manner.                 any subsequent operations in the processor depends on this foot-
   The property of Fig. 2 describes a monotonicity requirement              print, then a timing side channel violating confidentiality exists. In
similar to the one CHERI adheres to (cf. Sec. 2). This becomes ap-          accordance with [7], we call the corresponding attack Meltdown-
parent when expressing monotonicity with the notations used in              style attack. Such vulnerabilities can be detected using the Unique
this paper. For the given disjoint sets of state variables, 𝑃, 𝑀pub , and   Program Execution Checking (UPEC) [7] verification method.
𝑀prot , it is required that no state transition can change capabilities        UPEC was introduced to detect vulnerabilities to Transient Exe-
to grant access to previously protected memory locations, i.e., mov-        cution Attacks in processors. UPEC verifies security using a 2-safety
ing them from 𝑀prot to 𝑀pub . We call this notion weak capability           property running on a miter model. This miter instantiates two
monotonicity.                                                               instances of the design under verification and constrains the public
   We denote:                                                               inputs as well as the symbolic initial state to be equal. Hence, any
                                                                            difference between the two instances must originate in the differ-
          𝑡
      • 𝑀prot  as the set of protected memory locations before a state
                                                                            ence caused by the protected data. UPEC distinguishes between
        transition and
          𝑡 +1 as the set of protected memory locations after a state       propagation of protected data to microarchitectural buffers (P-alert)
      • 𝑀prot
                                                                            and actual leakage of the protected data to the architectural state
        transition.                                                         (L-alert).
Weak capability monotonicity requires that 𝑀prot    𝑡 +1 ⊆ 𝑀 𝑡 , i.e.,
                                                               prot
                                                                               In the following, we adapt UPEC to designs featuring CHERI
𝑀prot \ 𝑀prot = ∅. In other words, state transitions never add to
   𝑡 +1      𝑡                                                              protection and use it in addition to proving the properties of the
                                                                            previous sections. This serves two purposes. Firstly, we remove
the set 𝑀𝑝𝑟𝑜𝑡 . The connection to the interval property in Fig. 2 is
                                                                            the above-mentioned conservatism of Eq. 1 by taking into account
apparent when considering a case where monotonicity is violated,
                                                                            whether or not protected data can propagate to an attacker-visible
i.e., 𝑀𝑝𝑟𝑜𝑡     𝑝𝑟𝑜𝑡 = 𝑀vio ≠ ∅. In such a case, the property checker
        𝑡 +1 \ 𝑀 𝑡       𝑡 +1
                                                                            state. Secondly, we detect also Meltdown-style side channels.
would create a counterexample and choose a symbolic address
                                                                               As a first step, we further divide the set of microarchitectural
pointing to a memory location in 𝑀vio  𝑡 +1 .
                                                                            state variables 𝑃 into the two disjoint subsets 𝑃arch and 𝑃 𝜇-arch :
    There is a special case which we have omitted in Fig. 2 for clarity
of presentation, but which nevertheless must be treated in the                   • 𝑃arch : containing all architectural state variables in the pro-
practical implementation of the property. The case occurs when                     cessor, i.e., all registers visible to the attacker task;
there is a context switch to another task and monotonicity “ends”                • 𝑃 𝜇-arch : containing all but the architectural state variables in
for the considered current task. In CHERI, the task uses a specially               the processor, i.e., all microarchitectural registers and buffers
typed capability to perform a jump to an address in 𝑀prot , handing                not visible to the attacker task.
over control of the processor to the trusted operating system (OS),           With this addition to our model, we formulate UPEC as a 2-safety
as specified in our security objective (cf. Sec. 3.1).                      CTL property.
    Weak capability monotonicity is a weaker version of CHERI’s               For any task that can run on the system, i.e., for any choice of
capability monotonicity. While capability monotonicity forbids indi-        𝑀prot and 𝑀pub , it must hold:
vidual capabilities to grow to more access rights, e.g., larger bounds,
weak capability monotonicity only asks whether the set of capa-               AG ( $𝑃arch = $𝑃arch
                                                                                              ′
                                                                                                   ∧ $𝑃 𝜇-arch = $𝑃 𝜇-arch
                                                                                                                    ′
                                                                                                                           ∧ $𝑀pub = $𝑀pub
                                                                                                                                       ′
bilities controlled by a task can obtain more access rights overall.                                                                                  (5)
For our formulation of properties, weak capability monotonicity is                   → AG ( $𝑃arch = $𝑃arch
                                                                                                       ′
                                                                                                            ))
a sufficiently strong invariant. It is easier to formulate than capa-
                                                                               The property only allows a difference between the two model
bility monotonicity and it synergizes well with the concept of the
                                                                            instances in the protected memory locations 𝑀prot ; all other state
symbolic address. A notion similar to weak capability monotonicity
                                                                            variables are equal between the two instances. The property then
called reachable capability monotonicity is discussed in [19] for the
                                                                            verifies that the architectural state variables 𝑃arch , i.e., the attacker-
ISA model.
                                                                            visible part of the processor, are never influenced by contents of
                                                                            𝑀prot . In other words, the protected information is allowed to enter
3.4     Reformulating UPEC for CHERI                                        the processor core, but must not influence the architectural state
The three properties in Fig. 1a, 1b and 2 are sufficient to prove non-      variables.
interference and consider every access to protected data a security            The property in Eq. 5 takes the same perspective as the 1-safety
violation. This is reasonable for integrity, i.e., every write access to    property in Eq. 3. The parititioning of memory locations into 𝑀pub
protected data can be considered a security breach. However, for            and 𝑀prot is specified for a generic attacker task running on the
confidentiality, this can be too conservative. Preventing every read        processor. This is an important difference compared to the UPEC
access to protected memory is a sufficient condition for security           property presented in [7]. In [7], UPEC is formulated globally for a
while preventing the actual propagation to an attacker-visible state        design and independently of the running task. As a result, our UPEC
is both, a necessary and sufficient condition.                              formulation does not require any sound approximation excluding
To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ                                                                 A. Duque Antón, J. Müller et al.



1   UPEC - CHERI :
2   assume :                                                                      check:                                                 check:
3     at t:      cheri_protected ( symbolic_addr ) ;                           1-safety-int                  hold?                     monotonicity
                                                                                                   yes
4     at t:      $𝑀pub = $𝑀pub
                            ′ ∧ $𝑃 = $𝑃 ′ ;

5   prove :                                                                                                 no
6     at t+k: $𝑃 arch = $𝑃 arch
                           ′    ;

                                                                                                            missing                       update
                                                                                  hold?                  capability reg?
                                                                                              no                             yes     cheri_protected
                Figure 3: UPEC property for CHERI
                                                                                                                 no
                                                                                      yes
the case that protected data is leaked intentionally (cf. equivalence
of architectural observations in [7]).                                                                     vulnerable

   Analogously to [7], we prove Eq. 5 by an inductive proof pro-
cedure based on the interval property of Fig. 3 formulated for a
time window of 𝑘 clock cycles. To this end, we model 𝑃 and 𝑃 ′ as                 check:                                                 check:
two instances of the processor, but model 𝑀pub and 𝑀pub     ′ by their
                                                                              1-safety-conf        yes
                                                                                                             hold?                     monotonicity
addresses, similar as for the 1-safety properties in Eq. 3. This allows                                     no
us to use the same macro cheri_protected and the symbolic address
to model protection by CHERI capabilities.
                                                                                                            missing                       update
                                                                                  hold?                  capability reg?
                                                                                              no                             yes     cheri_protected
4    FORMAL VERIFICATION FLOW
We propose VeriCHERI, a novel formal verification flow based                                                     no
                                                                                      yes
on the interval properties introduced in Sec. 3. The verification
flow exhaustively detects all violations to the security objectives                                         check:
formulated in Sec. 3.1 and provides formal security guarantees after                                     UPEC-CHERI

removing all detected vulnerabilities in the design. As a part of the
flow, the macro cheri_protected is determined iteratively. The flow
is illustrated in Fig. 4.
                                                                                 secure                      hold?                       vulnerable
    VeriCHERI starts by proving the 1-safety integrity property                                    yes                     no
(cf. Fig. 1b). If the property fails, a counterexample is returned and
the verification engineer must decide whether it is a false or true                    Figure 4: VeriCHERI Verification Flow
one. A false counterexample can occur if the macro cheri_protected
misses to constrain a register or buffer holding a capability such
that, spuriously, access to protected data is granted. This reflects
behavior that is unreachable for the current settings of 𝑀prot . We
                                                                          is otherwise not accessible by the task), no iteration to update
remove this false counterexample by refining cheri_protected with
                                                                          cheri_protected is needed.
a constraint on the concerned register or buffer, as described in
                                                                             If both 1-safety properties hold, the design is guaranteed to
Sec. 3.3.
                                                                          be free of vulnerabilities violating our security objective. How-
    In the next step, by proving the property in Fig. 2, we verify
                                                                          ever, if the 1-safety-confidentiality property detects a vulnerabil-
that the updated macro cheri_protected remains an invariant, i.e.,
                                                                          ity, we know that protected data is accessed. In this case UPEC-
weak capability monotonicity is preserved. If monotonicity fails,
                                                                          CHERI (cf. Fig. 3) is used to further investigate the counterexample
the verification engineer must inspect the new counterexample to
                                                                          and check whether the protected data indeed propagates to some
modify or further refine cheri_protected.
                                                                          attacker-visible state.
    The verification engineer detects a true security vulnerability if
the counterexample shows the execution of a task that creates a
capability granting access to protected data or that accesses pro-        5   CASE STUDY
tected data without a legal capability. This reflects behavior that is    We conducted a case study on the CHERIoT Ibex processor im-
reachable for the current settings of 𝑀prot .                             plementing the CHERIoT architecture [2]. CHERIoT is a variant
    In case the monotonicity property holds, the integrity property       of CHERI that aims to provide memory safety for embedded In-
can be run again with the updated cheri_protected macro. This step        ternet of Things (IoT) real-time devices based on a compartmen-
is repeated until a vulnerability is detected or the 1-safety integrity   talization model. Compartments are mutually distrusting address
property holds successfully.                                              spaces containing code and data, isolated from each other by ca-
    Once the 1-safety integrity property holds, the confidentiality       pabilities. All code is run in pure capability mode (cf. Sec. 2.1). In
property (cf. Fig. 1a) is checked. In principle, the same iterative       CHERIoT, threads are individual instances of execution, owning a
procedure as discussed above must be followed. However, in prac-          stack pointer and register file contents, and are scheduled to run in
tice, (unless there is a capability used only in read accesses that       compartments. Compartment and context switches are performed
VeriCHERI:
Exhaustive Formal Security Verification of CHERI at the RTL
                                                                                               To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ


by designated procedures administered by a trusted OS. Capabili-            demonstrates that such timing side channels may well be present
ties stored in registers and memory are compressed to address the           even in small processors such as CHERIoT Ibex, which can be a
resource limitations for embedded IoT devices.                              significant risk in general. Exhaustive formal verification target-
   All experiments were conducted on a workstation PC featuring             ing such vulnerabilities is required for creating trust. We reported
an Intel i9-13900k with 128 GB of RAM running Linux and using the           this vulnerability and received confirmation from the development
commercial property checker OneSpin 360 DV by Siemens EDA.                  team.
                                                                               We applied a conservative fix that prevents all illegally fetched
                                                                            instructions to enter the core. With this fix, the UPEC property
5.1     Applying VeriCHERI                                                  holds.
We applied the formal verification flow presented in Sec. 4 to the             The runtimes of the individual properties range from a few sec-
CHERIoT Ibex RTL design [17]. The results are summarized in Tab. 1.         onds to 31 minutes.
In accordance with the flow, we started with the setup and proof
of the 1-safety integrity property (cf. Fig. 1b). In the first iteration,   5.2    Invariants as Reusable Verification IPs
the property failed due to the initially incomplete specification of
                                                                            Verifying unbounded interval properties may produce false coun-
the cheri_protected macro. We updated the cheri_protected macro
                                                                            terexamples. This happens when the property checker assumes
in several iterations until we successfully verified the monotonicity
                                                                            unreachable states as symbolic starting states. If a false counterex-
property (cf. Fig. 2). Overall, the iterations detected 40 locations
                                                                            ample is identified, invariants can be formulated to exclude such
in the core which hold capabilities, including the 31 capabilities in
                                                                            unreachable states from consideration. The invariants are then
the general purpose register file, seven special control registers, the
                                                                            proven by induction. This is standard practice in IPC, as supported
PCC and one pipeline buffer in the writeback stage.
                                                                            by commercial property checking tools.
   During this process, we detected two security bugs. The first bug
                                                                                While running the formal verification flow we formulated several
was related to a primary input pin responsible for globally enabling
                                                                            invariants. Most of the formulated invariants are not specific to
CHERI protection. In the setup guide, the pin was specified as active
                                                                            CHERI and exclude unreachable states in microarchitectural buffers
low, but implemented as active high in the RTL. We reported the
                                                                            such as control FSM registers. The formulated invariants were easy
bug to the CHERIoT developer team who updated the setup guide
                                                                            to prove and required only little manual effort. These invariants
accordingly.
                                                                            are implementation-specific and are, most likely, of limited use for
   For the second bug, the property checker produced a counterex-
                                                                            another CHERIoT (or CHERI) processor. However, our flow of Fig. 4
ample where the first memory access of a capability store lies within
                                                                            produces also two invariants that bear significance beyond this case
the allowed address bounds, but the second memory access goes
                                                                            study.
outside the bounds. On capability loads and stores, the bounds
                                                                                The first one is the weak capability monotonicity invariant in-
were only compared to the address of the first memory access and
                                                                            troduced in Sec. 3.3. The invariant constrains a set of capability
failed to prohibit the second address. During our experiments, this
                                                                            registers and buffers holding capabilities to deny accesses to pro-
bug was discovered independently also by the development team
                                                                            tected data. While the locations of these registers and buffers have
and fixed by checking whether the address of the second memory
                                                                            to be re-determined for another processor, the constraints them-
access, i.e., the address of the first access incremented by 4, also lies
                                                                            selves can be reused. Depending on the similarity in register layout,
within bounds.
                                                                            the constraints require minimal to no modifications.
   After successfully proving the 1-safety-integrity property, we
                                                                                The second invariant worth reporting is necessary to accom-
proceeded to checking the 1-safety-confidentiality property (cf. Fig.
                                                                            modate for CHERIoT’s compression scheme used to store capabil-
1a). For convenience, we split the property into two sub-properties,
                                                                            ities in registers and memory. It consists of multiple conditions
one property considering the data memory interface and one prop-
                                                                            describing legal configurations of the capabilities in the system.
erty for the instruction memory interface. While the data memory
                                                                            The CHERIoT architecture requires the processor HW to enforce
property held, the instruction memory property failed and pro-
                                                                            a similar set of conditions for compressed capabilities. This set is
duced a counterexample. The counterexample describes a scenario
                                                                            called representability [1]. Most of the complexity in formulating the
where instructions are fetched outside of legal capability bounds.
                                                                            invariant comes from the interdependence between the compressed
We ran the UPEC-CHERI property (cf. Fig. 3) to further investigate
                                                                            capability bounds and the corresponding addresses. However, the
this problem.
                                                                            formulation of the invariant benefits from a synergy with weak
   UPEC detected a vulnerability to a potential Meltdown-style at-
                                                                            capability monotonicity. We specify an additional constraint for
tack. In this particular case, an attacker tries to jump to an address
                                                                            each register or buffer holding a compressed capability. In essence,
pointing to a memory location in 𝑀prot . This starts a race with an
                                                                            it can be formulated as a function for any such register or buffer
exception which ultimately flushes the pipeline before the instruc-
                                                                            identified during the monotonicity proof.
tion is executed. However, depending on the content of two specific
                                                                                Both invariants are formulated in SVA and are published open-
bits of the fetched data, the pipeline flush is delayed. By measuring
                                                                            source [18].
the (overall) execution time, an attacker can probe the two bits for
an arbitrary protected address. In addition, the content of the two
bits is reflected in an offset of a performance counter. While, in this     5.3    Discussion
particular case, the detected timing side channel can only leak a           Although VeriCHERI uses an abstract security objective as starting
small amount of information per probed memory word, the example             point of our verification procedures, the resulting guarantees can
To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ                                                                          A. Duque Antón, J. Müller et al.



     Property                        Iteration       Result   Runtime     Memory     Description

     1-safety-integrity                    1          fail      < 1 min    4.3 GB    Bug: setup guide specification of protection enable pin
                                           2          fail      < 1 min    4.7 GB    Bug: capability stores across capability bounds
                                           3          hold        7 min    4.8 GB    -

     Monotonicity                        1-9          fail     ≤ 1 min     4-5 GB    Missing capability register or pipeline buffer
                                         10           hold      15 min     6.2 GB    -

     1-safety-confidentiality
     −→ data                               1          hold        7 min    7.3 GB    -
     −→ instructions                       1          fail      < 1 min    4.8 GB    Instruction fetched from outside PCC bounds

     UPEC-CHERI                            1          fail      31 min     3.7 GB    Side channel: exception timing depends on fetched data
                                           2          hold      18 min     6.3 GB    -

                                                              Table 1: CHERIoT Properties



be related directly to the CHERI security requirements. For the               EDA and by Deutsche Forschungsgemeinschaft SPP NanoSecu-
CHERIoT architecture used in our case study, mutually distrusting             rity, reference number KU 1051/11-2. We thank the CHERIoT Ibex
compartments can be modeled by assuming all memory locations                  development team for their valuable feedback.
within a compartment as 𝑀pub and all memory locations outside
the compartment as 𝑀prot (cf. Sec. 3.1). A task in our abstract threat
model corresponds to a thread executing code in a compartment.                REFERENCES
The task’s execution ends upon a context or compartment switch.                [1] Saar Amar, Tony Chen, David Chisnall, Felix Domke, Nathaniel Filardo, Kunyan
   In industrial practice, we intend VeriCHERI to be used in concert               Liu, Robert Norton-Wright, Yucong Tao, Robert NM Watson, and Hongyan Xia.
                                                                                   2023. CHERIoT: Rethinking security for low-cost embedded systems. Technical
with established verification flows for functional correctness based               Report MSR-TR-2023-6 (2023).
on simulation or (non-complete) formal verification. We think that             [2] Saar Amar, David Chisnall, Tony Chen, Nathaniel Wesley Filardo, Ben Laurie,
augmenting such existing flows with formal security guarantees is                  Kunyan Liu, Robert Norton, Simon W. Moore, Yucong Tao, Robert N. M. Watson,
                                                                                   and Hongyan Xia. 2023. CHERIoT: Complete Memory Safety for Embedded
a “sweet spot” for VeriCHERI.                                                      Devices. In Proceedings of the 56th Annual IEEE/ACM International Symposium on
   The manual effort involved in this case study approximates to                   Microarchitecture. 641–653.
two person months. This number includes the development and                    [3] Alasdair Armstrong, Thomas Bauereiss, Brian Campbell, Alastair Reid, Kathryn E.
                                                                                   Gray, Robert M. Norton, Prashanth Mundkur, Mark Wassell, Jon French, Christo-
refinement of the monotonicity and representability invariants.                    pher Pulte, Shaked Flur, Ian Stark, Neel Krishnaswami, and Peter Sewell. 2019.
Since they are reusable, this will significantly reduce effort in future           ISA semantics for ARMv8-a, RISC-v, and CHERI-MIPS. In Proceedings of the ACM
                                                                                   on Programming Languages, Vol. 3 (POPL). 1–31.
applications of VeriCHERI.                                                     [4] Thomas Bauereiss, Brian Campbell, Thomas Sewell, Alasdair Armstrong,
                                                                                   Lawrence Esswood, Ian Stark, Graeme Barnes, Robert N. M. Watson, and Peter
                                                                                   Sewell. 2022. Verified security for the Morello capability-enhanced prototype
6    CONCLUSION                                                                    Arm architecture. In Proceedings of the 31st European Symposium on Programming
                                                                                   (ESOP). Springer International Publishing, 174–203.
We present VeriCHERI, a formal security verification method tai-               [5] Michael R. Clarkson and Fred B. Schneider. 2010. Hyperproperties. Journal of
lored to CHERI processors. It exhaustively detects confidentiality                 Computer Security 18, 6 (2010), 1157–1210.
                                                                               [6] Keerthikumara Devarajegowda, Mohammad R. Fadiheh, Eshan Singh, Clark
and integrity vulnerabilities w.r.t. a global security objective based             Barrett, Subhasish Mitra, Wolfgang Ecker, Dominik Stoffel, and Wolfgang Kunz.
on non-interference. In a case study on the CHERIoT Ibex core,                     2020. Gap-free Processor Verification by S2QED and Property Generation. In 2020
VeriCHERI detected three security bugs, including a vulnerability                  Design, Automation & Test in Europe Conference & Exhibition (DATE). 526–531.
                                                                               [7] Mohammad R. Fadiheh, Alex Wezel, Johannes Müller, Jörg Bormann, Sayak Ray,
to a potential Meltdown-style timing side channel attack. Such a                   Jason M. Fung, Subhasish Mitra, Dominik Stoffel, and Wolfgang Kunz. 2023. An
vulnerability does not violate functional correctness and is thus                  Exhaustive Approach to Detecting Transient Execution Side Channels in RTL
not detected by previous verification methods based on verifying                   Designs of Processors. IEEE Transactions on Computers 72, 1 (2023), 222–235.
                                                                               [8] CHERI Flute. accessed in May 2024. [online]. GitHub. https://github.com/CTSRD-
an ISA specification. We also demonstrated that VeriCHERI is scal-                 CHERI/Flute.
able and feasible in terms of manual effort. Future work will apply            [9] Anthony Fox. 2012. Directions in ISA specification. Interactive Theorem Proving
                                                                                   (2012), 338–344.
VeriCHERI to more CHERI designs, including out-of-order proces-               [10] Franz Anton Fuchs. 2021. Analysis of Transient-Execution Attacks on the out-of-
sors.                                                                              order CHERI-RISC-V Microprocessor Toooba. Master Report. KTH Royal Institute
                                                                                   of Technology Tech. Rep.
                                                                              [11] Franz A. Fuchs, Jonathan Woodruff, Simon W. Moore, Peter G. Neumann, and
                                                                                   Robert N. M. Watson. 2021. Developing a test suite for transient-execution attacks
ACKNOWLEDGMENTS                                                                    on RISC-V and CHERI-RISC-V. In Workshop on Computer Architecture Research
This work was supported partly by Bundesministerium für Bil-                       with RISC-V (CARRV).
                                                                              [12] Dapeng Gao and Tom Melham. 2021. End-to-end formal verification of a risc-v
dung und Forschung Scale4Edge, grant no. 16ME0122K-16ME0140+                       processor extended with capability pointers. In 2021 Formal Methods in Computer
16ME0465, by Intel Corp., Scalable Assurance Program, by Siemens                   Aided Design (FMCAD). IEEE, 24–33.
VeriCHERI:
Exhaustive Formal Security Verification of CHERI at the RTL
                                                                                                               To appear in ICCAD ’24, October 27–31,2024, New Jersey, NJ


[13] Shilpi Goel, Anna Slobodova, Rob Sumners, and Sol Swords. 2020. Verifying x86      [20] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. 2002. Isabelle / HOL:
     instruction implementations. In Proceedings of the 9th ACM SIGPLAN International        A Proof Assistant for Higher-Order Logic. Springer.
     Conference on Certified Programs and Proofs (New Orleans, LA, USA) (CPP 2020).     [21] A. Reid, R. Chen, A. Deligiannis, D. Gilday, D. Hoyes, W. Keen, A. Pathirane,
     Association for Computing Machinery, New York, NY, USA, 47–60.                          O. Shepherd, P. Vrabel, and A. Zaidi. 2016. End-to-End Verification of ARM ®
[14] J. A. Goguen and J. Meseguer. 1982. Security Policies and Security Models. In           Processors with ISA-Formal. In Proceedings of 28th International Conference on
     1982 IEEE Symposium on Security and Privacy (SP). 11–20.                                Computer Aided Verification.
[15] Richard Grisenthwaite, Graeme Barnes, Robert NM Watson, Simon W Moore, Pe-         [22] Vasily A. Sartakov, Lluís Vilanova, David Eyers, Takahiro Shinagawa, and Peter
     ter Sewell, and Jonathan Woodruff. 2023. The Arm Morello Evaluation Platform–           Pietzuch. 2022. CAP-VMs: Capability-Based Isolation and Sharing in the Cloud.
     Validating CHERI-Based Security in a High-Performance System. IEEE Micro 43,            In 16th USENIX Symposium on Operating Systems Design and Implementation
     3 (2023), 50–57.                                                                        (OSDI ’22). 597–612.
[16] Wei Hu, Armaiti Ardeshiricham, Mustafa S Gobulukoglu, Xinmu Wang, and Ryan         [23] Joakim Urdahl, Dominik Stoffel, and Wolfgang Kunz. 2014. Path Predicate Ab-
     Kastner. 2018. Property specific information flow analysis for hardware security        straction for Sound System-Level Models of RT-Level Circuit Designs. IEEE
     verification. In Proceedings of the International Conference on Computer-Aided          Transactions on Computer-Aided Design of Integrated Circuits and Systems 33, 2
     Design. 1–8.                                                                            (2014), 291–304.
[17] CHERIoT Ibex. accessed in March 2024.                         [online]. GitHub.    [24] Robert N. M. Watson, Jonathan Woodruff, Peter G. Neumann, Simon W. Moore,
     https://github.com/microsoft/cheriot-ibex.                                              Jonathan Anderson, David Chisnall, Nirav Dave, Brooks Davis, Khilan Gudka,
[18] VeriCHERI invariants. 2024. [online]. GitHub. https://github.com/RPTU-                  Ben Laurie, Steven J. Murdoch, Robert Norton, Michael Roe, Stacey Son, and
     EIS/VeriCHERI.                                                                          Munraj Vadera. 2015. CHERI: A hybrid capability-system architecture for scalable
[19] Kyndylan Nienhuis, Alexandre Joannou, Thomas Bauereiss, Anthony Fox,                    software compartmentalization. In 2015 IEEE Symposium on Security and Privacy
     Michael Roe, Brian Campbell, Matthew Naylor, Robert N. M. Norton, Simon W.              (SP). IEEE, 20–37.
     Moore, Peter G. Neumann, Ian Stark, Robert N. M. Watson, and Peter Sewell.         [25] Jonathan Woodruff, Robert N. M. Watson, David Chisnall, Simon W. Moore,
     2020. Rigorous engineering for hardware security: Formal modelling and proof            Jonathan Anderson, Brooks Davis, Ben Laurie, Peter G. Neumann, Robert Norton,
     in the CHERI design and implementation process. In 2020 IEEE Symposium on               and Michael Roe. 2014. The CHERI capability model: Revisiting RISC in an age
     Security and Privacy (SP). IEEE, 1003–1020.                                             of risk. ACM SIGARCH Computer Architecture News 42, 3 (2014), 457–468.
