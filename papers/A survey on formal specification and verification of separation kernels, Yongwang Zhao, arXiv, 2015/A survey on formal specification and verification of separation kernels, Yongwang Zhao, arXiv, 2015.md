                                            A survey on formal specification and verification of separation
                                                                       kernels

                                                                                       Yongwang Zhaoa,∗
                                                              a National Key Laboratory of Software Development Environment (NLSDE)

                                                           School of Computer Science and Engineering, Beihang Univerisity, Beijing, China
arXiv:1508.07066v3 [cs.SE] 10 Jul 2016




                                         Abstract
                                         Separation kernels are fundamental software of safety and security-critical systems, which pro-
                                         vide to their hosted applications spatial and temporal separation as well as controlled information
                                         flows among partitions. The application of separation kernels in critical domain demands the cor-
                                         rectness of the kernel by formal verification. To the best of our knowledge, there is no survey
                                         paper on this topic. This paper presents an overview of formal specification and verification of
                                         separation kernels. We first present the background including the concept of separation kernel
                                         and the comparisons among different kernels. Then, we survey the state of the art on this topic
                                         since 2000. Finally, we summarize research work by detailed comparison and discussion.
                                         Keywords: real-time operating systems, separation kernel, survey, formal specification, formal
                                         verification



                                         1. Introduction

                                             The concept of “Separation Kernel” was introduced by John Rushby in 1981 [1] to create
                                         a secure environment by providing temporal and spatial separation of applications as well as to
                                         ensure that there are no unintended channels for information flows between partitions other than
                                         those explicitly provided. Separation kernels decouple the verification of the trusted functions
                                         in the separated components from the verification of the kernels themselves. They are often
                                         sufficiently small and straightforward to allow formal verification of their correctness.
                                             The concept of separation kernel originates the concept of Multiple Independent Levels of
                                         Security/Safety (MILS) [2]. MILS is a high-assurance security architecture based on the con-
                                         cepts of separation [1] and controlled information flow [3]. MILS provides means to have several
                                         strongly separated partitions on the same physical computer/device and enables existing of differ-
                                         ent security/safety level components in the same system. The MILS architecture is particularly
                                         well suited to embedded systems which must provide guaranteed safety or security properties.
                                         An MILS system employs the separation mechanism to maintain the assured data and process
                                         separation, and supports enforced security/safety policies by authorizing information flows be-
                                         tween system components.

                                            ∗ Corresponding author

                                             Email address: zhaoyw@buaa.edu.cn (Yongwang Zhao)

                                         Preprint submitted to Journal                                                                       July 12, 2016
Figure 1: The MILS architecture. Notation: Unclassified (U), confidential (C), secret (S), top secret (TS), single level
(SL), multi level security (MLS) [4]




    The MILS architecture is layered and consists of separation kernels, middleware and appli-
cations. The MILS separation kernels are small pieces of software that divide the system into
separate partitions where the middleware and applications are located, as shown in Fig. 1. The
middleware provides an interface to applications or a virtual machine enabling operating systems
to be executed within partitions. The strong separation between partitions both prevents informa-
tion leakage from one partition to another and provides fault-containment by preventing a fault in
one partition from affecting another. MILS also enables communication channels (unidirectional
or bidirectional) to be selectively configured between partitions.
    Separation kernels are first applied in embedded systems. For instance, they have been ac-
cepted in the avionics community and are required by ARINC 653 [5] compliant systems. Many
implementations of separation kernels for safety and security-critical systems have been devel-
oped, such as VxWorks MILS [6], INTEGRITY-178B [7], LynxSecure [8], LynxOS-178 [9],
PikeOS [10], and open-source implementations, such as POK [11] and Xtratum [12].
    In safety and security-critical domains, the correctness of separation kernels is significant for
the whole system. Formal verification is an rigorous approach to proving or disproving the cor-
rectness of the system w.r.t. a certain formal specification or property. The work in [13] presents
62 industrial projects using formal methods over 20 years and the effects of formal methods on
time, cost and quality of systems. The successful applications of formal methods in software
development are increasing in academic and industries. Security and safety are traditionally
governed by well-established standards.
(1) In the security domain, verified security is achieved by Common Criteria (CC) [14] evalua-
    tion, where EAL 7 is the highest assurance level. EAL 7 certification demands that formal
    methods are applied in requirements, functional specification, and high-level design. The
    low-level design may be treated semi-formally. The correspondence between the low-level
    design and the implementation is usually confirmed in an informal way. But for the purpose
    of fully formal verification, the verification chain should reach the implementation level. In
    2007, the Information Assurance Directorate of the U.S. National Security Agency (NSA)
    published the Separation Kernel Protection Profile (SKPP) [15] within the framework estab-
    lished by the CC [14]. SKPP is a security requirements specification for separation kernels.
                                                           2
    SKPP mandates formal methods application to demonstrate the correspondence between se-
    curity policies and the functional specification of separation kernels.
(2) In the safety domain, safety of software deployed in airborne systems is governed by RTCA
    DO-178B [16], where Level A is the highest level. The new version DO-178C [17] was pub-
    lished in 2011 to replace DO-178B. The technology supplements of DO-178C recommend
    formal methods application to complement testing.
     Although most of commercial products of separation kernels have been certified through DO-
178B Level A and CC, we only find two CC EAL 7 certified separation kernels, i.e., LynxSecure
and the AAMP7G Microprocessor [18] (a separation kernel implemented as hardware). Without
fully verification, the correctness of the separation kernels can not be fully assured.
     Many efforts have been paid on achieving verified separation kernels in this decade, such
as formal verification of SYSGO PikeOS [19, 20, 21, 22], INTEGRITY-178B kernel [23], ED
(Embedded Devices) separation kernel of Naval Research Laboratory [24, 25], and Honeywell
DEOS [26, 27, 28]. Using logic reduction to create high dependable and safety-critical software
was one of 10 breakthrough technologies selected by MIT Technology Review in 2011 [29].
They reported the L4.verified project in NICTA (National ICT Australia). The seL4 (secure em-
bedded L4) micro-kernel, which comprises 8,700 lines of C code and 600 lines of assembler
code, is fully formally verified by the Isabelle/HOL theorem prover [30, 31]. They found 160
bugs in the C code in total, 16 of which are found during testing and 144 bugs during the C ver-
ification phase. This work provides successful experiences for formal verification of separation
kernels and proves the feasibility of fully formal verification on small kernels. We could find a
survey on formal verification of micro-kernels of general purpose operating systems [32], but a
survey of separation kernel verification for safety and security-critical systems does not exist in
the literature to date.
     Considering that the correctness of separation kernels is crucial for safety and security-critical
systems, this survey covers the research work on formal specification and verification of sepa-
ration kernels ever since 2000. We outline them in high-level including formal specification,
models, and verification approaches. By comparing and discussing research work in detail, this
survey aims at proving an useful reference for separation kernel verification projects.
     In the next section, we first introduce the concept of separation kernels and compare it to
other types of kernels to clarity the relationship. In Section 3, literatures on formal specification
and verification of separation kernels are surveyed including three categories: formalization of
security policies and properties, formal specification and model of separation kernels, and for-
mal verification of separation kernels. In Section 4, we summarize research work by detailed
comparison and discussion. Finally, we conclude this paper in Section 5.


2. Background

   This section first introduces the concept of separation kernel, and then gives the comparisons
among different kernels such security kernels, partition kernels and hypervisors.

2.1. What’s the Separation Kernel
    Separation kernel is a type of security kernels [33] to simulate a distributed environment. Sep-
aration kernels are proposed as a solution to develop and verify the large and complex security
kernels that are intended to “provide multilevel secure operation on general-purpose multi-user

                                                  3
systems.” “The task of a separation kernel is to create an environment which is indistinguish-
able from that provided by a physically distributed system: it must appear as if each regime is
a separate, isolated machine and that information can only flow from one machine to another
along known external communication lines. One of the properties we must prove of a separation
kernel, therefore, is that there are no channels for information flow between regimes other than
those explicitly provided. [1]” Based on separation kernels, the system security is archived par-
tially through physical separation of individual components and mediation of trusted functions
performed within some components. Separation kernels decouple the verification of compo-
nents from the kernels themselves. Separation kernels provide their hosted software applications
high-assurance partitioning and controlled information flow that are both tamperproof and non-
bypassable [34, 35].
     Untrusted software in one partition may contain malicious code that attacks other partitions
and separation kernels. Kernels in general purpose operating systems usually cannot represent
these security policies and cannot provide adequate protection against these attacks. In 2007,
the Information Assurance Directorate of the U.S. National Security Agency (NSA) published
the SKPP [15] to describe, in CC [14] parlance, a class of modern products that provide the
foundational properties of Rushby’s conceptual separation kernel. The SKPP defines separation
kernels as “hardware and/or firmware and/or software mechanisms whose primary function is
to establish, isolate and separate multiple partitions and control information flow between the
subjects and exported resources allocated to those partitions.”
     Unlike traditional operating systems services such as device drivers, file systems, network
stacks, etc., separation kernels provide very specific functionalities including enforcing data sep-
aration and information flow controls within a single microprocessor and providing both time and
space partitioning. The security properties that must be enforced in separation kernels are rel-
ative simple. The security requirements for MILS include four foundational security properties
[34]:
    - Data Separation: each partition is implemented as a separated resource. Applications in
      one partition can neither change applications or private data of other partitions nor com-
      mand the private devices or actuators in other partitions. This property is also known as
      “Data Isolation”.
    - Information Flow Security: information flows from one partition to others are from an
      authenticated source to authenticated recipients; the source of information is authenticated
      to the recipients. This property is also known as “Control of Information Flow”.
    - Temporal Separation: it allows different components to share the same physical resource
      in different time slices. A resource is dedicated to one component for a period, then
      scrubbed clean and allocated to another component and so on. Services received from
      shared resources by applications in one partition cannot be affected by others. This prop-
      erty is also known as “Periods Processing”.
    - Fault Isolation: damage is limited by preventing a failure in one partition from cascading
      to any other partition.
    The properties of data separation, information flow security and fault isolation are all spatial
properties. They are collectively called “spatial separation” properties. The data separation re-
quires that memory address spaces/objects of a partition must be completely independent with
other partitions. The information flow security is a modification of data separation. Pure data
                                                4
separation is not practical and separation kernels define authorized communication channels be-
tween partitions for inter-partition communication. Pure data isolation is permitted to be violated
only through these channels. The consequences of a fault or security breach in one partition are
limited by the data separation mechanisms. A faulty process in one partition does not affect
processes in other partitions because addresses spaces of partitions are separated.
    Separation kernels allow partitions to cause information flows, each of which comprises a
flow between partitions. The allowed inter-partition information flows can be modeled as a
“partition flow matrix” whose entries indicate the mode of the flow, such as read and write.
The “flow” rules are passed to separation kernels in the form of configuration data interpreted
during kernel initialization. For instance, a notional set of allowable information flows between
partitions is illustrated in Fig. 1.
    NEAT are famous properties considered for separation kernels. NEAT is the abbreviation of
Non-bypassable, Evaluatable, Always invoked and Tamper proof [34, 35]:
    - Non-bypassable: security functions cannot be circumvented. It means that a component
      cannot use another communication path, including lower-level mechanisms, to bypass the
      security monitor.

    - Evaluatable: security functions are small and simple enough to enable rigorous proof of
      correctness through mathematical verification. It means that components are modular, well
      designed, well specified, well implemented, small, and low complex, etc.
    - Always-invoked: security functions are always invoked. It means each access/message
      is checked by the appropriate security monitors. Security monitors check on not only the
      first access but also all subsequent accesses/messages.
    - Tamper proof: the system controls “modify” rights to the security monitor code, config-
      uration and data. It prevents unauthorized changes, either by subversive or poorly written
      code.
    These concepts, although intuitive, are not necessarily easy to be formalised and proved di-
rectly. Separation kernels are usually verified by proving properties of data separation, temporal
separation, information flow security and fault isolation.
    The concern of the original separation kernel proposed by John Rushby [1] is security. The
reason that the concept is first applied in embedded systems, in particular the avionic systems, is
the acceptance of Integrated Modular Avionics (IMA) [36] in 1990s. IMA is the integration of
physically separated functions on common hardware platforms. The integration is furthermore
supported by the trend of more powerful multicore computers. The IMA can decrease the weight
and power consumption of currently implemented systems while concurrently create new space
for new functional components such as on-board entertainment. Current embedded systems in
avionics are already built in an IMA fashion. A major foundation of the IMA concept for op-
erating systems and computing platforms is the separation of computer system resources into
isolated computation compartments - called partitions. Computations in partitions have to run
concurrently in a way that any unintended interference and interaction between them are impos-
sible. Thus, a partition is considered as a process with guaranteed processing performance and
system resources. It is very similar to separation kernels. Therefore, the concept of separation
kernel is adopted in avionics as the kernel of partitioning operating systems for IMA. Separation
kernels in the community are also called “partitioning kernels” [35]. The ARINC 653 standard

                                                5
[5] defines the standard interfaces of partitioning kernels. Besides the security, partitioning ker-
nels concern safety, which means a failure in one partition must not propagate to cause failure in
other partitions.

2.2. Comparison of Different Kernels
    There are a set of kernel concepts similar to the separation kernel, which need to be clarified
here. They are security kernel, partitioning kernel, and hypervisor.

    • Security Kernel [33]
Security kernels manage hardware resources, from which they create, export and protect abstrac-
tions (e.g., subjects/processes and memory objects) and related operations. Security kernels bind
internal sensitivity labels to exported resources and mediate access by subjects to other resources
according to a partial ordering of the labels defined in an internal policy module. Separation ker-
nels extend security kernels by partitions. Separation kernels map the set of exported resources
into partitions. Resources in a given partition are treated equivalently w.r.t. the inter-partition
flow policy. Subjects in one partition are allowed to access resources in another partition. Sepa-
ration kernels enforce the separation of partitions and allow (subjects in those) partitions to cause
flows, each of which, when projected to partition space, comprises a flow between partitions [37].

     • Partitioning Kernel [38, 35, 39]
Partitioning kernels concern safety separation largely based on an ARINC 653-style separation
scheme. Besides the information flow control, partitioning kernels concentrate on spatial and
temporal partitioning. Partitioning kernels provide a reliable protection mechanism for the in-
tegration of different application subsystems. They split a system into execution spaces that
prohibit unintended interference of different application subsystems. Reliable protection in both
spatial domain and temporal domain is particularly relevant for systems where the co-existence
of safety-critical and non safety-critical application subsystems shall be supported. Partitioning
on node level enforces fault containment, and thereby enables simplified replacement/update and
increases reusability of software components.
     In order to provide an execution environment that allows the execution of software compo-
nents without unintended interference, temporal and spatial partitioning for both computational
and communication resources are required. Spatial partitioning ensures that a software compo-
nent cannot alter the code or private data of other software components. Temporal partitioning
ensures that a software component cannot affect the ability of other software components to ac-
cess shared resources. For the purpose of spatial partitioning, system memory is divided among
partitions in a fixed manner. The idea is to take a processor to pretend several processors by
completely isolating the subsystems. Hard partitions are set up for each part of the system, and
each partition has certain amount of memory allocated to it. Each partition is forever limited to
its initial fixed memory allocation, which can neither be increased nor decreased after system
initialization. For the purpose of temporal partitioning, partitioning kernels run in a static style.
They typically support a static table-driven scheduling approach [40] that is very well suited for
safety-critical and hard real-time systems since its static nature makes it possible to check the
feasibility of the scheduling in advance.
     Typical partitioning kernels are WindRiver VxWorks 653, GreenHill INTEGRITY-178B,
LynxOS-178, and PikeOS. All these products are compliant with ARINC 653. In the follow-
ing sections, the notion “separation kernel” covers the original concept [1] and the concept of
partitioning kernel.
                                                  6
   • Hypervisor [41]
Hypervisors or virtual machine monitors (VMMs) provide a software virtualization environment
in which other software, including operating systems, can run with the appearance of full ac-
cess to the underlying system hardware, but in fact such access is under the complete control
of hypervisors. In general, hypervisors are classified into two types [41]: Type 1 (or native,
bare metal) hypervisor and Type 2 (or hosted) hypervisor. Hypervisors virtualize the hardware
(processor, memory, devices, etc.) for hosted operating systems. Therefore, general purpose
operating systems can run on top of hypervisors directly. Similar to the Type I hypervisors, sep-
aration kernels achieve isolation of resources in different partitions by virtualization of shared
resources, such that each partition is assigned as a set of resources that appear to be entirely its
own. But traditional hypervisors are specifically designed for secure separation, and typically
do not provide services for explicit memory sharing. Moreover, traditional hypervisors support
interprocess communication only via emulated communication devices. Hypervisors permit the
deployment of legacy applications (within a VM) and new applications on the same platform.
Whilst separation kernels typically only support specific APIs (e.g., ARINC 653) for hosted
applications. Hypervisors have been introduced into embedded systems, so called embedded
hypervisors in IMA systems. The application of embedded hypervisors are increasing. PikeOS,
Wind River Hypervisor and LynuxWorks’s LynxSecure are typical embedded hypervisors for
safety and security-critical systems.
    Because of the overlapped functionalities between separation kernels and hypervisors, we
also survey typical verification work of embedded hypervisors in this paper.


3. The State of the Art

     Due to the importance of security policies in MILS architectures, we highlight typical def-
initions of security policies supported by separation kernels. In this section, we first survey the
formalizations of security policies and properties. Then, we present formal specification and
models of separation kernels. Finally, we survey the formal verification of separation kernels.
     Firstly, we distinguish the concepts of “security policy”, “security property” and “security
model”. Security policies or properties define security requirements of separation kernels. Sep-
aration kernels are represented by security models [42], which are the abstraction of concrete
kernel implementations. Thus, security models of separation kernels are the formal models. Se-
curity policies and properties are formulas represented in first- or high-order logics. Preservation
of them on security models means the security of separation kernels.

3.1. Formalization of Security Policies and Properties
    This subsection presents the formalizations of security policies (e.g., MILS and SKPP) and
security properties (e.g., data separation, information flow security, and temporal separation).

3.1.1. MILS and SKPP Security Policies
    A formal specification of what the system allows, needs and guards against is called a formal
policy. Two typical security policies for MILS architecture based on separation kernels are the
inter-partition flow policy (IPFP) and the partitioned information flow policy (PIFP). The inter-
partition flow policy is a sort of security policies for original separation kernel [1] on MILS.
Separation kernels map the set of exported resources into partitions: resource map : resource →
partition. The inter-partition flow policy [37] can be expressed abstractly in a partition flow
                                                 7
                               U.S. Government Protection Profile for Separation Kernels in Environments Requiring High Robustness
                               Version 1.03 – 29 June 2007




                                          Partition A                            Partition B                            Partition C

                                      Subject 1         Subject 2                     Subject 3




                                                                                              Resource             Resource
                                                                                                 7                    9
                                                                          Resource 6
                                                        Resource                                                                     Resource
                                    Resource 4             5                                                                            10
                                                                                              Resource 8




                                                                     TSF Security Functions


                                                                Figure 2-3. Allocation of TOE Resources
                        46     The TOE rules for   isolation
                                                Figure      2:areAllocation
                                                                  referred to asof
                                                                                 theTOE
                                                                                     Partitioned Information
                                                                                           Resources     [15]Flow Policy (PIFP).
                               The PIFP defines the authorizations for information flow between partitions and between
                               subjects and exported resources. The mode or direction of the flow – such as send, receive, read
                               (including execute-only, which could be further restricted by the ST author), write or read-write
                               – indicates whether information flows from the subject to the exported resource (e.g., write) or
                               from the resource to the subject (e.g., read), or both. Thus, an information flow is defined as a
                               <partition/subject, partition/exported resource, mode> triplet. Note that the exported resource
matrix, whose entries indicate the mode of the flow, partition f low : partition × partition →
                               may be another subject. By default, the TOE allows no information flow between partitions or
mode. The mode indicates the direction of the flow, for instance partition f low(P1 , P2 ) = W
                               between subjects and exported resources.
                  47   Figure 2-3 shows a hypothetical example of the allocation of subjects and other exported
means that the partition               is allowed
                       resourcesPto1 partitions.              to write
                                                    The resources    inside ofto eachany     resource
                                                                                       rectangle  are bound in          . Resources in a given
                                                                                                                    P2partition.
                                                                                                              to that
                       Allowed information flow is indicated by the directed arrows. Inter-partition flows are also
partition are treated equivalently             w.r.t.      the   inter-partition             flow     policy.
                       shown, for example, Subject 2 is allowed to write Resource 6, and Subject 3 is allowed to read
    “SKPP specifies Resource
                        the security           functional
                                 9. This example     is intended toand      assurance
                                                                    illustrate                  requirements
                                                                               the application the                       for a class of separation
                                                                                                    Least Privilege Abstraction
                       of the PIFP (see Section 2.3.2). With this policy abstraction, subject(s) in a partition can have
kernels. Unlike thosedifferent
                          traditional
                                access rightssecurity
                                                to resources inkernels
                                                                 the same orwhich         perform
                                                                               different partitions.      all trusted
                                                                                                     Resources                functions for a secure
                                                                                                                 7, 8 and 10 are
                       included to illustrate this finer grained control of information flow.
operating system, 48
                     a separation           kernel’s         primary
                       The configuration data may be comprised of:            security         function        is   to   partition   (viz. separate)
the subjects and resources       of aof system
                       • Definition                      into
                                          partitions, both       security
                                                             in terms             policy-equivalence
                                                                       of the allocation   of exported resources toclasses,
                                                                                                                       partitions and to enforce the
rules for authorized information flows between and within partitions. [15]” It mainly addresses
security evaluations of separation kernels at EAL                          29 6 and EAL 7 of CC.

    The SKPP enforces PIFP with requirements at the gross partition level as well as at the
granularity of individual subjects and resources. A subset of the exported resources are active
and are commonly referred to as subjects. Flows occur between a subject and a resource, and
between the subject’s partition and the resource’s partition, in a direction defined by a mode. In
read mode, the subject is the destination of the flow. In write mode the subject is the source of the
flow. Fig. 2 illustrates an allocation of TOE (Target of Evaluation, a concept in CC) resources.
The resources inside of each rectangle are bound to that partition. Allowed information flows
are indicated by the directed arrows. For instance, Subject 2 is allowed to write Resource 6 and
Subject 3 is allowed to read Resource 9. By this policy abstraction, subjects in a partition can
have different access rights to resources in another partition. Resources 7, 8 and 10 illustrate this
finer grained control of information flows.
    SKPP defines a partition-to-partition policy (P2P p ) and a subject-to-resource (S 2R p ) policy
(also known as a least privilege policy). Flow rules, P2P and S2R, are associated with each
policy:

                                 S 2R : [s : sub ject, r : resource, m : mode]
                                                                                                                                                (1)
                                 P2P : [sub p : partition, res p : partition, m : mode]
     The PIFP policy of SKPP is:


                                                                                          8
                     ALLOWED([s : sub ject, r : resource, m : mode]) =
                         S 2R p ∈ sys.policy → (
                            S 2R(s, r).m = allow ∨                                             (2)
                            (S 2R(s, r).m = null ∧ P2P(s.p, r.p).m = allow)
                        ) ∧ P2P p ∈ sys.policy → P2P(s.p, r.p).m = allow
    where sys.policy indicates which policies are configured to be active. In the S 2R p policy,
the S 2R rules override the P2P rules everywhere except there is a null entry in the S 2R rule set.
Note that the S 2R p policy is defined to reference the P2P values regardless of whether the P2P p
policy itself is active.
    The separation kernels of VxWorks MILS, LynxSecure, INTEGRITY-178B and PikeOS
meet the security functionalities and security assurance requirements in SKPP.

3.1.2. Data Separation Properties
    Data separation requires that resources of a partition must be completely independent of other
partitions.

   • MASK Separation Properties
The DoD of USA set out in 1997 to formally construct a separation kernel, a Mathematically
Analyzed Separation Kernel (MASK) [43, 44], which has been used by Motorola on its smart
cards. MASK regulates communication between processes based on separation policies. The
separation policies of MASK include two separation axioms: the communication policy and an
anonymous policy. In the abstraction of the MASK separation kernel, Multiple Cell Abstraction
(MCA) describes the system. The Init and Next operations evolve the system. Cells and Single
Cell Abstraction (SCA) are domains of execution or a context, which consist of a collection of
strands. Each strand is a stream of instructions to be executed when a message is input to a strand
of a cell. The communication policy is as follows.

                             Fibery (MCA) , Fibery (Next x (MCA))
                                                                                               (3)
                                             ⇒ Communicates(x, y)
    where Fibery determines the SCA corresponding to the CellID y in the subscript, Next x
advances the system state by advancing the cell indicated by the subscript x. The policy states
that if the fiber of cell y changes as the result of advancing the state of cell x, it must be the
case that x is permitted to communicate with y. The second separation constraint upon cells is as
follows.

                                     Fiber x (MCA1 ) = Fiber x (MCA2 ) ⇒
                                     Fibery (MCA1 ) = Fibery (MCA2 ) ⇒                         (4)
                        Fibery (Next x (MCA1 )) = Fibery (Next x (MCA2 ))
     The policy represents that if an action by cell x is going to change the state of cell y, the
change in the state of y depends only on the states of x and y. In other words, the new state of y
is a function of the previous states of x and y.

   • ED Data Separation Properties
                                                9
To provide evidence for a CC evaluation of the ED (Embedded Devices) separation kernel to
enforce data separation, five subproperties, namely, No-Exfiltration, No-Infiltration, Temporal
Separation, Separation of Control, and Kernel Integrity are proposed to verify the kernel [24, 25].
The Top-Level Specification (TLS) is used to provide a precise and understandable description of
the allowed security-relevant external behavior and to make the assumptions on which the TLS
is explicitly based. TLS is also to provide a formal context and precise vocabulary to define data
separation properties. In TLS, the state machine representing the kernel behavior is defined in
terms of an input alphabet, a set of states, an initial state and a transform relation describing the
allowed state transitions. The input alphabet contains internal events (cause the kernel to invoke
some process) and external events (performed by an external host). The state consists of the id
of a partition processing data, the values of the partition’s memory areas and a flag to indicate
sanitization of each memory area.
    The No-Exfiltration Property states that data processing in any partition cannot influence data
stored outside the partition, which is formulated as follows.

                                         s, s0 ∈ S ∧ s0 = T (s, e) ∧
                                         e ∈ P j ∪ E In   Out
                                                     j ∪ Ej   ∧
                                                                                                    (5)
                                         a ∈ M ∧ a s , a s0
                                         ⇒ a ∈ Aj
                   0                 0
    where s and s are states and s is the next state of s transited by an event e in the partition
j. P j is the internal event set of the partition j. E In
                                                       j is the set of external events writing into or
                                                   Out
clearing the input buffers of the partition j. E j is the set of external events reading from or
clearing the output buffers of the partition j. For any memory area a of the system (M), a is a
memory area in the partition j (A j ), if the value of a in state s and s0 are not equal.
    The No-Infiltration Property states that data processing in a partition is not influenced by data
outside that partition, which is formulated as follows.
                                 s1 , s2 , s01 , s02 ∈ S ∧ s01 = T (s1 , e)∧
                                 s02 = T (s2 , e) ∧ (∀a ∈ Ai ) a s1 = a s2                          (6)
                                  ⇒ (∀a ∈ Ai )a s01 = a s02
    The Separation of Control Property states that when data processing is in progress in a parti-
tion, no data is being processed in other partitions until processing in the first partition terminates,
which is formulated as follows.
                                         s, s0 ∈ S ∧ s0 = T (s, e) ∧
                                         c s , j ∧ c s0 , j                                         (7)
                                         ⇒ (∀a ∈ A j ) a s01 = a s02
where c s is the id of the partition that is processing data in state s.
    The Kernel Integrity Property states when data processing is in progress in a partition, the
data stored in the shared memory area do not change, which is formulated as follows.
                                   s, s0 ∈ S ∧ s0 = T (s, e) ∧ e ∈ Pi
                                                                                                    (8)
                                                              ⇒ G s = G s0
where G is the single shared memory area and contains all programs and data not residing in any
memory area of partitions, Pi is the internal event set of the partition i.
                                                10
3.1.3. Information Flow Security Properties
    In the domain of operating systems, state-event based information flow security properties
are often applied [45]. We present two major categories of information flow security properties:
the GWV policy and noninterference.

    • GWV Policy
Greve, Wilding and Vanfleet propose the GWV security policy in [46] to model separation ker-
nels. The separation axiom of this policy is as follows.

                           selectlist(segs, st1) = selectlist(segs, st2) ∧
                           current(st1) = current(st2) ∧
                           select(seg, st1) = select(seg, st2)                                     (9)
                            ⇒
                           select(seg, next(st1)) = select(seg, next(st2))
     where segs = dia(seg) ∩ segso f partition(current(st1)). The security policy requires that the
effect on an arbitrary memory segment seg of the execution of one machine step is a function of
the set of memory segments that are both allowed to interact with seg and are associated with the
current partition. In this formula, the function select extracts the values in a machine state that are
associated with a memory segment. The function selectlist takes a list of segments and returns
a list of segment values in a machine state. The function current calculates the current partition
given a machine state. The function next models one step of computation of the machine state. It
takes a machine state as the argument and returns a machine state that represents the effect of the
single step. The function dia takes a memory segment name as the argument and returns a list of
memory segments that are allowed to affect it. The function segso f partition returns names of
the memory segments associated with a particular partition. The detailed information about the
meaning of a machine state and the next function of states are explained in [47].
     The GWV security policy has been well known and accepted in industry [48, 49, 50]. The
PVS formalization of GWV policy has been provided by Rushby [51]. The GWV policy is
changed/extended in [47, 52]. The dia function is weakened by allowing communication be-
tween segments of the same partition in [47] as follows.

                                     seg ∈ segso f partition(p) ⇒
                                                                                                  (10)
                                   segso f partition(p) ∈ dia(seg)
    The dia function is extended by a restriction considering partition names, diaS trong(seg, p) ⊂
dia(seg), in [52]. In addition, the GWV policy is extended by the sub ject. A subject is an active
entity which operates on segments of a GWV partition. The extended GWV policy is as follows.

                           current(st1) = current(st2) ∧
                           currentsub ject(st1) = currentsub ject(st2) ∧
                           select(seg, st1) = select(seg, st2) ∧
                                                                                                  (11)
                           selectlist(segs, st1) = selectlist(segs, st2)
                            ⇒
                           select(seg, next(st1)) = select(seg, next(st2))

                                                  11
     where segs = diastrong(seg, current(st1)) ∩ segso f partition(current(st1)). The extended
GWV policy has been applied to formally specify the PikeOS [52].
     The GWV policy is only applicable to a class of systems in which strict temporal partition-
ing is utilized and kernel state cannot be influenced by execution of code within partitions. The
GWV theorem has been shown to hold for the AAMP7G’s hardware-based separation kernel
[18]. The original GWV theorem is only applicable to such strict static schedulers. The GWV
policy is sound but not complete [53]. In GWV, dia function only expresses the direct interaction
between segments. It is extended by multiple active “Agent” in GWVr1 [53] that moving data
from one segment to another segment is under control of one agent. GWVr1 is similar to the
diaS trong function in [52]. For more dynamic models, a more general GWV theorem, GWVr2
[53], uses a more generalized influence between segments, the information flow graph, to spec-
ify the formal security policy. The information flow graph enables system analysis and can be
used as foundation for application-level policies. The GWVr2 is used to formal analysis for the
INTEGRITY-178B separation kernel [23]. More theoretical discussion of GWVr1 and GWVr2
is in [50].

   • Noninterference
    The concept of noninterference is introduced in [42] to provide a formal foundation for the
specification and analysis of security policies and the mechanisms to enforce them. The intuitive
meaning of noninterference is that a security domain u cannot interfere with a domain v if no
action performed by u can influence subsequent outputs seen by v. The system is divided into a
number of domains, and the allowed information flows between domains are specified by means
of an information flow policy , such that u       v if information is allowed to flow from a domain
u to a domain v. The standard noninterference is too strong and not able to model channel-control
policies. Thus, the intransitive noninterference is introduced, which uses a sources(α, u) function
to identify those actions in an action sequence α that their domain may influence the domain u.
Rushby [54] gives a standard definition of intransitive noninterference as follows.
                                                         u
                      noninter f erence ≡ ∀α u.(s0 C α l s0 C ipurge(α, u))                    (12)
    where ipurge(α, u), defined based on sources(α, u), removes the actions from the action
sequence α that their domains cannot interfere with u directly or indirectly. A system is secure
for the policy , if for each domain u and each action sequence α, the final states of executing α
and α0 (α0 is the result of removing actions that their domain can not influence u) from the initial
state s0 are observed equivalently for u.
    The intransitive noninterference is usually chosen to formally verify information flow secu-
rity of general purpose operating systems or separation kernels [45].
    Classical noninterference is concerned with the secrets that events introduce in the system
state and that are possibly observed via outputs [55]. Although noninterference is adequate for
some sorts of applications, there are many others considering the prevention of secret information
leakage out of the domains it is intended to be confined to. Language-based information flow
security typically considers information leakage and has two domains: High and Low. It is
generalized to arbitrary multi-domain policies in [55] as a new notion nonleakage. As pointed
out in [56] that it is important to combine language-based and state-event based security, and
a new notion noninfluence which is combination of nonleakage with traditional noninterference
[54] is proposed in [55].

                                                12
    A system is nonleaking if and only if for any states s and t and a domain u, the final states
after executing any action sequence α in s and t are indistinguishable for u if s and t are indistin-
guishable for all domains (sources(α, u)) that may interfere with u directly or indirectly during
the execution of α. The nonleakage is defined as follows.
                                                         sources(α,u)
                              nonleakage ≡ ∀α s u t.s        ≈          t −→
                                                                  u
                                                                                                   (13)
                                                          sCαltCα
   Combination of noninterference and nonleakage introduces the notion noninfluence as fol-
lows.
                                                    sources(α,u)
                        nonin f luence ≡ ∀α s u t.s      ≈       t −→
                                                u
                                                                                      (14)
                                         s C α l t C ipurge(α, u)
    The nonleakage and noninfluence are applied in formal verification of seL4 separation kernel
in [57].

3.1.4. Temporal Separation Properties
    Temporal separation usually concerns sanitization/period processing. A sanitization property
(called Temporal Separation) on ED separation kernel is defined in [25] as follows to guarantee
that the data areas in a partition are clear when the system is not processing data in that partition.

                                      (∀s ∈ S , 1 ≤ i ≤ n) c s = 0
                                                                                                   (15)
                                     ⇒ D1i,s = 0 ∧ ... ∧ Dki,s = 0
    where c s is the id of a partition that is processing data in state s. When c s is 0, it means that
no data processing in any partition is in progress. D1i,s = 0, ..., Dki,s = 0 means that all data areas
in the partition i are clear. Satisfaction of this property implies that no data stored in the partition
during one configuration of this partition can remain in any memory area of a later configuration.

3.1.5. Formal Comparison of Policies and Properties
    As presented in previous subsections, security policies and properties for separation kernels
have been studied in literature. They are formalized in different specification and verification
systems, such as ACL2, Isabelle/HOL, and PVS. Formal comparison of them to clarify the
relationships can establish a substantial foundation for formal specification and verification of
separation kernels.
    In [55], the notions of noninterference, nonleakage, and noninfluence are defined based on the
same state machine and formally compared. The author states that noninfluence is semantically
equal to the conjunction of noninterference and nonleakage.
    In [58], the GWV policy and Rushby’s noninterference are formally compared in detail. The
authors present a mapping between the objects and relations of the two models. The conclu-
sion is that GWV is stronger than Rushby’s noninterference, i.e., all systems satisfying GWV’s
separation also satisfy Rushby’s noninterference.




                                                  13
3.2. Formal Specification and Models of Separation Kernels
    The formal specification and models of separation kernels present a significant contribution
to formal verification. Here, we only discuss the models for formally developing separation
kernels. Models targeted at formal verification are surveyed in the next subsection. In formal
development, the specification may be used as a guide while the concrete implementation is
developed during the design process. We present typical specification and models of separation
kernels in turn.

   • Craig’s Z model of separation kernel
    Following the earlier book on modeling operating system kernels [59] that shows it is possible
and relatively easy to specify small kernels and refine them to the running code, Craig [60]
concerns entirely with the specification, design and refinement in Z [61] to executable code of
operating system kernels, one of which is a separation kernel, to demonstrate that the refinement
of formal specification of kernels is possible and quite tractable.
    Craig provides a substantial work on a formal separation kernel model which delivers the
majority of separation kernel requirements and functionalities [62], such as (1) Process table for
basic process management; (2) Process spatial separation in terms of non-overlapping address
space allocation; (3) Communication channels by the means of an asynchronous kernel-based
messaging system; and (4) Process temporal separation using a non-preemptive scheduler and
the messaging system.
    The formal specification is relatively complete and the refinements reach the level at which
executable code in a language such as C or Ada can be read off from the Z specification. Sepa-
ration kernels frequently need threads/tasks inside each partition. In the Craig’s model, it makes
no mention of threads. It is considered that threads can be included by simple modifications
to the specification. Hardware is not the emphasis in their work. The Intel IA32/64 hardware
operations at a level of detail are specified in the model, which are adequate for the production
of the tiny amounts of assembly code required to complete the kernel. Finally, all of the work in
their book is done by hand including the specification and proofs.

   • Z model of separation kernel in Verified Software project
Formalization of separation kernels [63, 62] is part of a pilot project in modeling OS kernels
within an international Grand Challenge (GC) in Verified Software [64, 13]. The objective is to
provide proofs of the correctness of a formal specification and design of separation kernels. They
start from Craig’s formal model [60] and take into account separation kernel requirements in [1]
and SKPP [15].
    The Craig’s original model is typeset by hand and includes several manual proofs. The
specification is augmented in [63, 62] using Z notation [65] by mechanising it in the Z/Eves
theorem prover. All proofs in [60] are also declared and proved using the Z/Eves prover. As a
result, syntax errors in Craig’s specification are eliminated, model feasibility and API robustness
are verified, and missing invariants and new security properties to guarantee correct operations
are found. The upgraded formal model is fully proved mechanically.
    The upgraded formal model focuses on the core data structures within a separation kernel,
such as the process table, queue and scheduler. Craig’s scheduler model is significantly im-
proved. Certain properties about the scheduler (e.g., the scheduler deadlock analysis) are able
to be formulated and proved by translating verbal requirements to mathematical invariants and
improving design of the specification.
                                                14
    • B model of a secure partitioning kernel
The B Method [66] has been used for the formal development of a secure partitioning kernel
(SPK) in the Critical Software company [67]. The novelty of this work in the formal methods
community is an extra challenge to apply the B Method outside its usual application domains
(railway and automotive).
    Initially, a complete development of a high-level model of the SPK is built. The high-level
model constitutes a complete architectural design of the system, and is animated and validated by
ProB [68]. Abstract model of SPK in high-level consists of memory management, scheduling,
kernel communication, flow policy, and clock. The validated high-level model can be refined for
a completely and formally developed SPK. As a first step, the PIFP policy, which is part of the
SPK, is refined to a level from where C code can be automatically generated. The refinement
process that leads to the implementation of the PIFP is carried out with the assistance of Atelier
B. Finally, an open source micro kernel, PREX, is adopted to integrate the proposed PIFP. They
demonstrate the feasibility of applying formal methods only to parts of the system.
    • B model of OS-K separation kernel
A separation kernel based operating system, OS-K [69], has been designed for use in secure
embedded systems by applying formal methods. The separation kernel layer and the additional
OS services on top of it are prototyped on the Intel IA-32 architecture. The separation kernel is
designed using two formal methods: the B method and the Spin model checker. The B method
is adopted as formal design, and Spin for verification via model checking.
    The separation kernel layer provides several functions: partition management, inter-partition
communication, access control for inter-partition communication, memory management, timer
management, processor scheduling, I/O interrupt synchronization for device driver operation,
and interrupt handling. The separation kernel provides the access-control function for inter-
partition communication, which provides the only linkage between separated partitions. In the
IA-32 architecture based implementation, two memory-protection features of the IA-32 architec-
ture are utilized: the ring protection feature is used to protect the memory area of the separation
kernel against access by the processes and the partition OSs; each partition is assigned a local
descriptor table in which the partition segments are registered to isolate the partition memory
spaces.
    The B models are also refined to an implementation by converting the non-deterministic
sections to sequential processing. Proof obligations of their B model are generated and verified
in B4free tools. There are more than 2,700 proof obligations and almost all of them are proved
automatically in B4free tools.
    • Event-B model of ARINC 653
    The kernel interface defines operating system services provided to applications. Formal-
ization of the kernel interface could support formally modeling and verification of application
software on top of separation kernels. ARINC 653 [5] aims at providing a standardized inter-
face between separation kernels and application software, as well as a set of functionalities to
improve safety and certification process of safety-critical systems. Therefore, formalization and
verification of ARINC 653 has been considered in recent years. In [70], system functionality and
all of 57 services specified in ARINC 653 Part 1 are formalized using Event-B [71]. They use
the refinement structure in Event-B to formalize ARINC 653 in a stepwise manner and a semi-
automatic translation from service requirements of ARINC 653 into the low-level specification.
The Event-B specification has 2,700 LOC. A set of safety properties are defined as invariants in
Event-B and verified on the specification.
                                               15
    • Formal API Specification of PikeOS separation kernel
Aiming at a precise model of PikeOS and a precise formulation of the PikeOS security policy,
the EURO-MILS project1 releases a new generic specification of separation kernels – Controlled
Interruptible Separation Kernel (CISK) [72]. This specification contains several facets that are
useful to implement separation kernels, such as interrupts, context switches between domains,
and control. The initial specification is close to a Mealy machine. The second-level specification
adds the notion of separation and security policy. At the third-level, “interruptible” is introduced
and calls to the kernel are no longer considered atomic. The final-level specification provides
an interpretation of control that allows atomic kernel actions to be aborted or delayed. The
specification is rich in detail, making it suitable for formal verification of realistic and industrial
systems. The specification and proofs have been formalized in Isabelle/HOL. Based on the CISK
specification, the formal API specification of the PikeOS separation kernel has been provided
aiming at the certification of PikeOS up to CC EAL7 [73]. The formal API specification covers
the IPC, memory, file provider, port, and event, etc.

3.3. Formal Verification of Separation Kernels
    As introduced in Section 2, the typical properties of separation kernels are data separation,
information flow security, fault isolation, and temporal separation. The first three properties are
collectively called “spatial separation” properties. Therefore, we categorize formal verification
work on separation kernels into spatial and temporal separation verification in this subsection.

3.3.1. Spatial Separation Verification
    Most related work on formally verifying separation kernels consider both the data separation
and information flow security. Here, we present significant research work of spatial separation
verification. Due to the importance of data separation and information flow security properties
for separation kernels, we finally highlight a general verification approach for these properties.

    • ED Separation Kenrel
     A novel and practical approach to verify security of separation kernels code which substan-
tially reduces the cost of verification is presented in [24, 25]. The objective of this project is to
provide evidence for a CC evaluation of the ED (Embedded Devices) separation kernel to enforce
data separation. The ED separation kernel contains 3,000 lines of C and assembly code.
     The code verification process consists of five steps: (1) Producing a Top-Level Specification
(TLS) using a state machine model. (2) Formally expressing the security property as the data
separation property of the state machine model. (3) Formally verifying that the TLS enforces data
separation in TAME (Timed Automata Modeling Environment), a front end to the PVS theorem
prover. (4) Partitioning the code into three categories, in which it is identified as “Other Code”
such code not corresponding to any behavior defined by the TLS; “Other Code” is ignored in the
verification, therefore greatly simplifying the process. (5) Demonstrating that the kernel code
conforms to the TLS. They define two mapping functions to establish correspondence between
the TLS and kernel code. A mapping establishes correspondence between concrete states in the
code and abstract states in the TLS. Another maps the preconditions and postconditions of the
TLS events to the preconditions and postconditions that annotate the corresponding Event Code.


  1 http://www.euromils.eu/


                                                  16
    They adopt the natural language representation of the TLS and the size of the TLS is very
small, which only takes 15 pages. It can simplify communication with the other stakeholders,
changing the specification when the kernel behavior changed, translating the specification into
TAME and proving that the TLS enforced data separation. They use 2.5 weeks to formulate the
TLS and the data separation property, 3.5 weeks to produce the TAME model and formally verify
that the TLS enforces data separation, and 5 weeks to establish conformance between code and
TLS. The cost of formal verification is much lower than the verification effort on seL4 kernel
[30, 31] where they translated almost all of source code to the Isabelle/HOL description.
     • AAMP7G microprocessor
     The AAMP7G and its previous version AAMP7 microprocessor of Rockwell Collins are
hardware implementation of separation kernels. The AAMP7 and AAMP7G design is mathe-
matically proved to achieve MILS using formal methods techniques as specified by EAL 7 of
CC [49, 18].
     The AAMP7G provides a novel architectural feature, intrinsic partitioning, that enables the
microprocessor to enforce an explicit communication policy between applications. Rockwell
Collins has performed a formal verification of the AAMP7G partitioning system using the ACL2
theorem prover. They first establish a formal security specification, AAMP7G GWV theorem,
which is the intrinsic partitioning separation theorem [49]. This theorem is an instantiation of
GWV policy [46]. Then, they produce an abstract model of the AAMP7G’s partitioning system
and a low-level model that directly corresponds with the AAMP7G microcode. In the low-level
model, each line of microcode is modeled by how it updates the state of the partition-relevant
machine. The entire AAMP7G model is approximately 3,000 lines of ACL2 definitions. The
AAMP7G GWV theorem is proved using ACL2. The proofs are decomposed into three main
pieces: proofs to validate the correctness theorem, proofs to show that the abstract model meets
the security specification, and proofs to show that the low-level model corresponds with the
abstract model.
     The AAMP7G GWV theorem is shown as follows. The theorem involves abstract and func-
tional (low-level) models of the AAMP7G. The theorem is about the behavior of the functional
model, but they express the theorem about an abstract model of the AAMP7G that has been
“lifted” from a functional model. In this way, the expression of the theorem is simplified. More-
over, the behavior of the most concrete model of the AAMP7G is also presented to ensure that
the theorem is about the “real” AAMP7G.

secure con f ig(spex) ∧
spex hyp(spex, f un st1) ∧
spex hyp(spex, f un st2) ⇒

                      (raw selectlist(segs, abs st1)
                       = raw selectlist(segs, abs st2) ∧
                      current(abs st1) = current(abs st2) ∧
                      raw select(seg, abs st1) = raw select(seg, abs st2)
                    ⇒
                    raw select(seg, li f t raw(spex, next(spex, f un st1)))
                    = raw select(seg, li f t raw(spex, next(spex, f un st2))))
                                                17
   where abs st1 = li f t raw(spex, f un st1), abs st2 = li f t raw(spex, f un st2) and segs =
dia f s(seg, abs st1) ∩ segs f s(current(abs st1), abs st1).

   • PikeOS
    PikeOS [74] is a powerful and efficient para-virtualization real-time operating system based
on a separation microkernel. The Verisoft XT 2 project has an Avionics subproject [19, 20, 75]
to prove functional correctness of all system calls of the PikeOS at the source code level using
the VCC verification tool 3 . They propose a simulation theorem between a top-level abstract
model and the system consisting of the kernel and user programs running in alternation on the
real machine. They identify the correctness properties of all components in the trace that are
needed for the overall correctness proofs of the microkernel.
    Memory separation of the PikeOS separation kernel has been formally verified on the source
code level [22] also using VCC. The desired memory separation property is easy to describe
informally but infeasible to define directly in the specification language. Therefore, they break
down the high-level, non-functional requirement into functional memory manager properties that
can be presented as a set of assertions for function contracts.
    The GWV property has been applied to verify the PikeOS separation kernel in [52]. They
extend the GVW property with subjects to resolve the problem that the same current partition can
have different active tasks. They present a modular way to apply the GWV property for the two
layers of PikeOS. In the micro-kernel model, the major abstractions are tasks and threads, which
are corresponding to subjects and partitions in the extended GWV theorem respectively. The
segment is instantiated as the physical address in the memory. In the separation kernel model,
they add “partitions” and separated the tasks of micro-kernel model and physical address of the
memory into different partitions. The modular and reusable application of the security policy
reduces the number of formal models and hence the number of artefacts to certify. All models
are formalised in Isabelle/HOL.

   • INTEGRITY-178B
The INTEGRITY-178B separation kernel of Green Hills Software was formally analysed and ob-
tained a CC Certificate at the EAL 6+ level on September 1, 2008 [23]. The INTEGRITY-178B
evaluation requirements for EAL 6+ specify five elements that are either formal or semi-formal:
(1) The Security Policy Model which is a formal specification of the relevant security properties
of the system; (2) Functional Specification which is a formal representation of the functional in-
terfaces of the system; (3) High-Level Design which is a semi-formal and abstract representation
of the system; (4) Low-Level Design which is a semi-formal, but detailed representation of the
system; (5) Representation Correspondence to demonstrate the correspondence between pairs of
the above four elements.
    Considering that the original GWV theorem [46] is only applicable to strict static kernels,
they adopt the GWVr2 [50] theorem as the Security Policy Model because INTEGRITY-178B’s
scheduling model is much more dynamic. The GWVr2 theorem is system(state) = system∗ (graph, state).
This theorem means that the system and system∗ produce identical results for all inputs of in-
terest. It implies that the graph used by system∗ completely captures information flows of the
system.


  2 http://www.verisoftxt.de/StartPage.html
  3 http://research.microsoft.com/en-us/projects/vcc/

                                                        18
    The system is modeled as a state transition system that receives the current state of the system
as inputs, as well as any external inputs, and produces a new system state, as well as any external
outputs. This state transition is expressed as state0 = system(state), where the external inputs
and outputs are also contained in the system state structure.
    The hardware-independent portion of the INTEGRITY-178B kernel is implemented in C
code and formally modeled in ACL2 which has one-to-one correspondence with the C source
code. This simplifies the “code-to-spec” review during CC certification. The hardware-dependent
code is not modeled and is subjected to a rigorous by hand review. In order to prove the GWVr2
theorem on the ACL2 model, they first prove two lemmas w.r.t. each function in this model. The
Workhorse Lemma states that the function’s graph sufficiently captures the dependencies in the
data flows of the function. The ClearP Lemma states that all of the changes to state performed
by a function are captured by the function’s graph. Once these two lemmas are proved, it is
straightforward to prove the GWVr2 theorem.

   • PROSPER separation kernel
    The information flow security for a simple ARM-based separation kernel, PROSPER, has
been formally verified by proving the bisimulation between the abstraction specification and the
kernel binary code, where communication between partitions is explicit and information flow is
analyzed in presence of such communication channels [76].
    The PROSPER kernel consists of 150 lines of assembly code and 600 lines of C code. Their
system model only considers two partitions that are respectively executed on two separate special
ARMv7 machines communicating via asynchronous message passing, a logical component, and
a shared timer. The goal of verification is to show that there is no way for the partitions to affect
each other directly or indirectly, except through the communication channel. It is assured by that
a partition can not access the memory or register contents, by reading or writing, of the other
partition, except that the communication is realized by explicit usage of the intended channel.
The isolation theorem of their kernel is as follows.

                              trg,r (mem1 , mem2 ) = trg,i (mem1 , mem2 )                       (16)
     where g ∈ 1, 2 indicates the partition, mem1 and mem2 are initial memories of the two par-
titions respectively. r (real system) indicates the implementation and i (ideal system) is the
abstraction model. The theorem means that the traces of each partition in abstraction and imple-
mentation layers are equivalent.
     The theorem is reduced to subsidiary properties: isolation lemmas of ARM and User/Han-
dler. Their three ARM lemmas concerning the ARM instruction set architecture assure that (1)
behavior of the active partition is influenced only by those resources allowed to do so if an ARM
machine executes in user mode in a memory protected configuration, (2) the non-accessible re-
sources not allocated to the active partition in user mode are not modified by the execution of
this partition, (3) if an ARM machine switches from a state in user mode to another in privileged
mode, the conditions for the execution of the handler are prepared properly. Their models are
built on top of the Cambridge ARM HOL4 model which is extended by a simple MMU unit. The
isolation lemmas of ARM are proved using the ARM-prover, which is developed for the purpose
in HOL4.
     The model of the ideal system, the formalization of the verification procedure, and the proofs
of the theorems consist of 21k lines of HOL4 code. During verification process, several bugs
are identified and fixed, such as the registers are not sanitized after the bootstrap, some of the
                                                 19
execution flags are not correctly restored during the context switch. They verify the entire kernel
at machine code level and avoid reliance on a C compiler. This approach can transparently verify
code that mix C and assembly.

    • seL4 separation kernel
The seL4 microkernel, which is fully and formally verified in NICTA [30, 31], is extended as a
separation kernel for security-critical domains in [57]. The information flow security property is
formally proved [45, 57] based on the results of verifying seL4 kernel [30, 31].
    To provide a separation kernel, they minimally extend seL4 by adding a static partition-based
scheduler and enforce requiring that seL4 be configured to prevent asynchronous interrupt deliv-
ery to user-space partitions which would introduce an information channel. The priority-based
scheduling is changed to the partitioning scheduling that follows a static round-robin scheduling
between partitions, with fixed-length time slices per partition, while doing dynamic priority-
based round-robin scheduling of threads within each partition.
    For information flow security, they adopt an extension of von Oheimb’s notion of nonleakage
[55] which is a variant of intransitive noninterference [45]. Nonleakage is defined as follows.

                        nonleakage ≡ ∀n s t p.reachable s ∧ reachable t ∧
                                                  PS ched         sources n s p          p              (17)
                                              s     ∼       t∧s        ≈          t −→ s ∼n t
    It states that for two arbitrary and reachable states s and t, if the two states agree on the private
                                              PS ched
state of the separation kernel scheduler (s ∼ t), and for each entity in partition’s extent in a
                                                                                            sources n s p
partition set (sources n s p), the entity’s state is identical in the two state s and t (s       ≈        t),
then after performing n transitions from s and t, the entities of partition p in the new two states
                   p
are identical (s ∼n t). The partition set (sources n s p) includes partitions that are permitted to
send information to a specific partition p when a sequence of n transitions occur from a state s.
    The security property assures that seL4’s C implementation enforces information flow se-
curity (Formula 17). Because information flow security is preserved by refinement, it allows
to prove information flow security on seL4’s abstract specification and then concludes that it
holds for seL4’s C implementation by the refinement relation between abstraction specifica-
tion and implementation proved in [30, 31]. When proving information flow security on the
abstract specification, they simplify the proofs by discharging proof obligations of nonleakage,
unwinding conditions, that examines individual execution steps. The unwinding condition, called
confidentiality-u as follows, is equivalent to nonleakage
                     confidentiality − u ≡ ∀p s t.reachable s ∧ reachable t ∧
                        p        PS ched                                   part s            p          (18)
                     s∼t ∧ s        ∼      t ∧ (part s        p −→ s ∼ t) −→ s ∼1 t
    It means that the contents of each partition p after each step depend only on the contents of
the following partitions before the step: p, PSched and the currently running partition part s
when it is allowed to send information to p. In other words, information may flow to p only
from PSched and the current partition in accordance with the information flow policy . The
information flow policy p1          p2 holds if the access control policy allows the partition p1 to
affect any subject in p2 ’s extent. This condition has been proven for the execution steps of their
transition system in abstraction specification.
    They state that it is the first complete, formal, machine-checked verification of information
flow security for the implementation of a general-purpose microkernel. Unlike previous proofs
                                                   20
of information flow security for separation kernels, their verification is applied to the actual 8,830
lines of C code of seL4, and so rule out the possibility of invalidation by implementation errors
in this code. The proofs of information flow security are done in Isabelle/HOL by 27,756 lines
of proof, and take a total effort of roughly 51 person-months. The proofs precisely describe how
the general purpose kernel should be configured to enforce isolation and mandatory information
flow control.

   • ARINC 653 compliant separation kernels
A trend is to integrate safe and secure functionalities into one separation kernel. In order to
develop ARINC 653 compliant secure separation kernels, it is necessary to assure security of
the functionalities defined in ARINC 653. In [77], authors present a formal specification and
its security proofs of separation kernels with ARINC 653 channel-based communication in
Isabelle/HOL. They provide a mechanically checked formal specification which comprises a
generic execution model for separation kernels and an event specification which models all IPC
services defined in ARINC 653. A set of information flow security properties and an inference
framework to sketch out the implications of them are provided. Finally, they find some covert
channels to leak information in the ARINC 653 standard and in two open-source ARINC 653
compliant separation kernels, i.e. XtratuM and POK.

   • Spatial separation of hypervisors
Hypervisors provide a software virtualization environment in which operating systems can run
with the appearance of full access to the underlying system hardware, but in fact such access is
under the complete control of hypervisors. Hypervisors support COTS operating systems and
legacy/diverse applications on specific operating systems. Hypervisors for safety and security-
critical systems have been widely discussed [78, 79]. For instance, Xtratum [80] is a typical
hypervisor for safety-critical embedded systems.
     Similar to separation kernels, hypervisors mainly provide the memory separation for hosted
operating systems. Address separation protects the memory regions of one execution context
by preventing other context from accessing these regions. It is a crucial property - in essence
requiring that disjoint source addresses spaces be mapped to disjoint destination address spaces.
Separation is achieved by an address translation subsystem and sophisticated address translation
schemes use multi-level page tables. Separation kernels can employ shadow paging to isolate
critical memory regions from an untrusted guest OS. The kernel maintains its own trusted ver-
sion of the guest’s page table, called the shadow page table. The guest is allowed to modify its
page table. However, the kernel interposes on such modifications and checks that the guest’s
modifications do not violate memory separation. A parametric verification technique [81, 82]
is able to handle separation mechanisms operating over multi-level data structures of arbitrary
size and with arbitrary number of levels. They develop a parametric guarded command lan-
guage (PGCL+ ) for modeling hypervisors and a parametric specification formalism, PT S L+ , for
expressing security policies of separation mechanisms modeled in PGCL+ . The separation prop-
erty states that the physical addresses accessible by the guest OS must be less than the lowest
address of the hypervisor protected memory. Models of Xen and ShadowVisor are created in C
and two properties are verified using CBMC (a model checker for C): (1) the initial state of the
system ensures separation; (2) if the system started in a state that ensures separation, executing
any of the guarded commands also preserves separation.
     Hypervisors allow multiple guest operating systems to run on shared hardware and offer a
compelling means of improving the security and the flexibility of software systems. In [83], the
                                                21
strong isolation properties ensure an operating system can only read and modify its own memory
and its behavior is independent of the state of other operating systems. The read isolation captures
the intuition that no OS can read memories that do not belong to it. The write isolation captures
the intuition that an OS cannot modify memories that it does not own. The OS isolation captures
the intuition that the behavior of any OS does not depend on other OSs states. They formalize
in the Coq proof assistant an idealized model of a hypervisor and formally establish that the
hypervisor ensures strong isolation properties.
    Xenon [84] is a high-assurance separation hypervisor built by Naval Research Laboratory
based on re-engineering the Xen open-source hypervisor. The information flow security has
been proposed for the Xenon hypervisor [85] as a the basis for formal policy-to-code modeling
and evidence for a CC security evaluation. Their security policy is an independence policy
[86], which is preserved by refinement. Considering that the original independence policy is
defined in a purely event-based formalism that does not directly support refinement into state-
rich implementations like hypervisor internals, they use the Circus language to formalize the
security policy. The Xenon security policy defines separation between Low and High as the
independence of Low’s view from anything High might do. Low and High are domains that
contain the guest operating systems hosted by Xenon. High guest operating systems can not
only perform all possible sequences of High events including event sequences a well-behaved
user would not generate, but also arbitrarily refuse to perform any of them as well. If this kind
of arbitrary behavior by the High part of the system cannot cause the Low part of the system
to behave in a non-deterministic way, High cannot influence what Low sees and there are no
information flows from High to Low. The formal security policy model is in heuristic use for
re-engineering the internal design of Xen into the internal design of Xenon. Mechanical proofs
of the refinement between the Circus security policy model and the Xenon implementation have
not been constructed.

   • A General Verification Approach for Spatial Separation Properties
From the literature of spatial separation verification, we could see that spatial separation proper-
ties are mostly formally verified using theorem proving technique. The data separation properties
and GWV policy are formulated on individual execution steps of the system to observe the pre-
or post-conditions of the execution step. They use the next function (see Equation 3, 4 and 9) to
represent one individual execution step. Properties of noninterference, nonleakage and noninflu-
ence are expressed in terms of sequences of actions and state transitions. In order to verifying the
security of systems, the standard proofs of information flow security properties are discharged by
proving a set of unwinding conditions [54] that examine individual execution steps of the system.
     The unwinding theorem [54] for security policies says if the system is output consistent,
weakly step consistent and locally respects , the system is secure for policy . The three con-
ditions are called unwinding conditions. The unwinding theorem simplifies the security proofs
by decomposing the global properties into unwinding conditions on each execution step.
     The three unwinding conditions are as follows, and the unwinding theorem states that output consistent∧
weakly step consistent ∧ locally respect −→ noninter f erence.

                                                       u            u
                               output consistent ≡ s ∼ t −→ s l t                              (19)

                                                                        dom(a)
                        weakly step consistent ≡ dom(a)        u∧s ∼ t
                                             u                  u
                                                                                               (20)
                                         ∧s ∼ t −→ step(a, s) ∼ step(a, t)
                                               22
                                                                 u
                      locally respect ≡ ¬(dom(a)        u) −→ s ∼ step(a, s)                   (21)
    The general proofs of information flow security properties and unwinding conditions are
available in [54, 55] and an application of them on a concrete separation kernel is available in
[77].

3.3.2. Temporal Separation Verification
    Temporal separation ensures that the services provided by shared resources to applications in
a partition cannot be affected by applications in other partitions. It includes the performance of
the resources concerned, as well as the rate, latency, jitter, and duration of scheduled access to
them [38]. The temporal separation becomes critical when being applied in safety-critical sys-
tems. The scheduler of separation kernels implements temporal separation since it is responsible
for assigning processor time to partitions. Temporal separation requires a two-level scheduler,
partition level and process level, according to ARINC 653 standard.
    The literature mainly deals with two issues for temporal separation: the schedulability anal-
ysis of two-level scheduling and correct implementation of the scheduler. The first one usually
uses a compositional approach to formally specify and analyze the schedulability of real-time
applications running under the two-level scheduling. The recent work is discussed in [87, 88]. It
considers the application but not the separation kernels. Our survey concerns with verification of
separation kernels and the second one is discussed here.

   • Honeywell DEOS scheduler
     The Honeywell Dynamic Enforcement Operating System (DEOS) is a microkernel-based
real-time operating system that supports flexible IMA applications by providing both space par-
titioning at the process level and time partitioning at the thread level. The model checking and
theorem proving approaches have been applied to the DEOS scheduler to analyze the temporal
separation property [26, 27, 28].
     A core slice of the DEOS scheduling kernel contains 10 classes and over 1000 lines of actual
code are first translated without abstraction from C++ into Promela, which is the input lan-
guage for the Spin model checker. The temporal partitioning property of DEOS scheduler is that
each thread in the kernel is guaranteed to have access to its complete CPU budget during each
scheduling period. They use two approaches to analyze the time partitioning properties in the
DEOS kernel. The first one is to place assertions over program variables to identify potential
errors. The second approach is to use a liveness property, Idle Execution, presented by LTL.
The liveness property specified as [ ](beginperiod− > (! endperiod U idle)), states that if there is
slack in the system (i.e., the main thread does not have 100% CPU utilization), the idle thread
should run during every longest period. This is a necessary condition of time partitioning.
     The size and complexity of this system limit them to analyze only one configuration at a
time. To overcome this limitation and generalize the analysis to arbitrary configurations, they
have turned to theorem proving approach and used the PVS theorem prover to analyze the DEOS
scheduler [28]. They model the operations of the scheduler in PVS and the execution timeline
of DEOS using a discrete time state-transition system. Properties of time partitioning (TP) are
formulated as predicates on the set of states and proved to hold for all reachable states. The
corresponding PVS proofs consist of the base step and the inductive step as follows.

                                init invariant : init(s) −→ T P(s)
                                                23
                  transition invariant : T P(ps) ∧ transition(ps, s) −→ T P(s)
   The T P predicate is defined as follows.

                     goodCommitment(s, period) ≡
                           commitment(s, period) ≤ remainT ime(s, period)


                    T P(s, period) ≡goodCommitment(s, period) ∨
                                     ∀t. period (threadWithId(s, t)) ≤ period
                                     −→ satis f ied(s, t)

                                 T P(s) ≡ ∀period. T P(s, period)
    The entire collection of theories has a total 1648 lines of PVS code and 212 lemmas. In addi-
tion to the inductive proofs of the time partitioning invariants, they use a feature-based technique
to model state-transition systems and formulate inductive invariants. This technique facilitates
an incremental approach to theorem proving that scales well to models of increasing complexity.

   • A two-level scheduler for VxWorks kernel
    In [89], a hierarchical scheduler executing in the WindRiver VxWorks kernel has been mod-
eled using task automata and model checked using the Times tool. The two-level hierarchical
scheduler uses periodic/polling servers (PS) and fixed priority preemptive scheduling (FPPS) of
periodic tasks for integrating real-time applications. In their framework, the Global scheduler
responds for distributing the CPU capacity to the servers (the schedulable entity of a subsystem).
Servers are allocated a defined time (budget) of every predefined period. Each server comprises a
Local scheduler which schedules the workload inside it, i.e. its tasks, when the server is selected
for execution by the global scheduler.
    They use the task automata [90] (timed automata with tasks) supported by the Times tool
to model the global scheduler, event handler, and each local scheduler for partitions. The event
handler decouples the global scheduler from the variability of partition amount. They specify 5
and 4 properties in TCTL (Timed Computation Tree Logic) for the global and local scheduler,
respectively.

   • An ARINC653 scheduler modeled in AADL
In [91], AADL (Architecture Analysis and Design Language) is used to model an ARINC653 hi-
erarchical scheduler for critical systems and Cheddar is used to analyze the scheduling simulation
on AADL specifications with hierarchical schedulers. AADL is a textual and graphical language
support for model-based engineering of embedded real time systems that has been approved and
published as SAE Standard. Cheddar is a set of Ada packages which aim at performing analysis
of real time applications. The Cheddar language allows the designer to define new schedulers
into the Cheddar framework.
    In their ARINC 653’s two-levels hierarchical scheduling, the first-level static scheduling is
fixed at design time, and the second scheduling level is related to the task scheduling where tasks
of a given partition are scheduled with a fixed priority scheduler. In the AADL model, ARINC
653 kernel, partitions, and tasks are modeled as a processor, processes, and threads, respectively.
The specific Cheddar properties are extended to the AADL model in order to describe the be-
havior of each AADL component in Cheddar language and apply real time scheduling analysis
                                                24
tools. The behavior of each scheduler is modeled as a timed automaton in Cheddar language.
With the meta CASE tool Platypus, they have designed a meta-model of Ada 95 for Cheddar and
a model of the Cheddar language. From these models, they generate Ada packages which are
part of the Cheddar scheduling simulation engine. These Ada packages implement a Cheddar
program compiler and interpreter. Then scheduling simulation analysis is performed on AADL
specifications with hierarchical schedulers.

   • A two-level scheduler for RTSJ
     The Real-Time Specification for Java (RTSJ) is a set of interfaces and behavioral specifi-
cations that allow for real-time computer programming in the Java programming language. It
is modified to allow applications to implement two-level scheduling mechanism where the first
level is the RTSJ priority scheduler and the second level is under application control [92, 93].
They also verify the two-level scheduler for RTSJ using Timed Automata in the UPPAAL tool
[94]. The Thread, BaseScheduler (global scheduler), EDFScheduler(local scheduler) and other
components are presented by timed automata. Five properties are verified on their model. Three
of them are to check the correctness of their model: (1) a thread’s priority never takes an invalid
value, (2) no thread can block due to locking after it starts, and (3) the system will always select
a thread to run with higher absolute preemption level than the system ceiling, unless the selected
thread is either currently locking a resource with higher ceiling than its apl or a thread that has
just been released. The other two are liveness and deadlock free properties that state the system
is livelock free and can never deadlock.

4. Summary

4.1. Comparison of Related Work
    We summarize the research work on formal specification and verification of separation ker-
nels in Table 4.1. In this table, “>” means that the evidence for the data is not available and empty
cells mean that the feature is not considered in the work. We compare seven features of them.
The column “Target Kernel” is the object specified or verified in each work. The “Objective”
shows the concerns of each work, in which Specification indicates that the work concentrates on
formal specifying/developing/modeling separation kernels and Verification on formally verifying
separation kernels. Some work aims at these two aspects together. The “Property” indicates the
policies or properties specified or verified in each work. The “Formal Language” indicates what’s
the formal language used when specifying or verifying the separation kernels. The “Approach”
indicates the formal specification or verification approaches used. The “Size” shows the scale
of the formal specification or verification proofs. The “Tools” shows the software tools used in
each work.

4.2. Discussion and Issues
4.2.1. Relationship of Security Properties
    We have classified the properties of separation kernels as four categories: data separation,
information flow security, temporal separation and fault isolation. The relationship among these
properties is very important for formal specification and verification of separation kernels. We
discuss the relationship here.
    The separation security properties, infiltration, mediation and exfiltration [95] can be repre-
sented by the GWV separation axiom [46]. Exfiltration specifies that the private data of executing
                                                 25
                                                                      Table 1: Comparison of Related Work
Related Work                         Target Kernel                    Objective       Property               Formal Language          Approach              Size                 Tools
                                                                      Specification                                                   Refinement
Department of Defense [43, 44]       MASK separation kernel                           Data separation        SPECWARE                                       >                    SPECWARE environment
                                                                      Verification                                                    Theorem proving
GWV, GWVr2 and extensions [46,       Applicable for generic separa-   Specification   Information flow se-   ACL2, PVS                Theorem proving       >                    ACL2, PVS theorem prover
51, 47, 52, 23]                      tion kernels                                     curity
                                                                      Specification                                                   Refinement
Naval Research Lab [24, 25]          ED separation kernel                             Data separation        TAME                                           368 LOC         of   TAME, PVS theorem prover
                                                                      Verification                                                    Theorem proving
                                                                                                                                                            TAME spec.
Craig’s book [59, 60]                A separation kernel              Specification                          Z notation               Refinement            ≈100 pages           By hand
                                                                      Specification                                                   Refinement
Verified software project [63, 62]   A separation kernel                              PIFP                   Z notation                                     ≈50 pages            Z/Eves prover
                                                                      Verification                                                    Theorem proving
Critical Software company [67]       A secure partitioning kernel     Specification   PIFP                   B                        Refinement            >                    Atelier B
                                                                                                                                      Refinement
                                                                      Specification
OS-K [69]                            A separation-kernel-based OS                                            B, Promela               Theorem proving       2,700 proof obli-    B4free, Spin
                                                                      Verification
                                                                                                                                      Model checking        gations
                                                                                                                                      Refinement
ARINC 653 [70]                       ARINC 653 standard               Specification   Safety                 Event-B                                        2,700 LOC of         RODIN
                                                                                                                                      Theorem proving
                                                                                                                                                            Event-B spec.
EURO-MILS [73]                       PikeOS separation kernel         Specification   PIFP                   HOL                      Theorem proving       ¿ 4,000 LOC of       Isabelle/HOL
                                                                                                                                                            spec.
Rockwell Collins [49, 18]            AAMP7G microprocessor            Verification    GWV                    ACL2                     Theorem proving       3000 LOC ACL2        ACL2 theorem prover
                                                                                                                                                            definitions
Verisoft XT project [22]             PikeOS separation kernel         Verification    Data separation        Annotated C code         Theorem proving       >                    VCC tool
SYSGO AG [52]                        PikeOS separation kernel         Verification    GWV                    HOL                      Theorem proving




                                                                                                                                                                                 26
                                                                                                                                                            >                    Isabelle/HOL theorem prover
Green Hills [23]                     INTEGRITY-178B separation        Verification    GWVr2                  ACL2                     Theorem proving       >                    ACL2 theorem prover
                                     kernel
PROSPER [76]                         A Simple ARM-Based Separa-       Verification    Information flow se-   HOL4                     Theorem proving       21,000 LOC           HOL4
                                     tion Kernel                                      curity
NICTA [45, 57]                       seL4 separation kernel           Verification    Information flow se-   HOL                      Theorem proving       4970 LOC of          Isabelle/HOL theorem prover
                                                                                      curity                                                                spec.,    27,756
                                                                                                                                                            LOC of proof
                                                                      Specification
CMU [81, 82]                         Hypervisor (Xen and Shadowvi-                    Data separation        PGCL+ ,PT S L+           Model checking        >                    CBMC
                                                                      Verification
                                     sor)
VirtualCert project [83]             A simple hypervisor (from Mi-    Verification    Data separation        Coq                      Theorem proving       21,000 LOC           Coq proof assistant
                                     crosoft Hyper-V)
                                                                      Specification
Securify project [77]                ARINC 653 separation kernel                      Information flow se-   HOL                      Theorem proving       1,000 LOC of         Isabelle/HOL
                                                                      Verification
                                                                                      curity                                                                spec., 7,000 LOC
                                                                                                                                                            of proof
                                                                                                                                      Refinement
Xenon project [85]                   Xenon hypervisor                 Specification   IPFP                   Circus language                                ≈ 4,500 pages        CZT Circus tools
                                                                                                                                      Theorem proving
Honeywell [26, 27]                   DEOS scheduler                   Verification    Temporal separation    Promela                  Model checking        >                    Spin
Honeywell [28]                       DEOS scheduler                   Verification    Temporal separation    PVS                      Theorem proving       1648 LOC of          PVS theorem prover
                                                                                                                                                            PVS, 212 lemmas
Malardalen Univ. (Sweden) [89]       A two-level scheduler for Vx-    Verification    Temporal separation    Task automata, TCTL      Model checking        >                    Times tool
                                     Works kernel
Brest Univ. (France) [91]            An ARINC653 scheduler            Verification    Temporal separation    AADL, Cheddar language   Simulation analysis   >                    Cheddar
York Univ. (UK) [94]                 A two-level scheduler for RTSJ   Verification    Temporal separation    Timed automata           Model checking        >                    UPPAAL tool
partition cannot be written by or modify the private data of other partitions. Mediation specifies
that an executing partition cannot use private data of one partition to modify private data of
other partitions. Infiltration specifies that an executing partition cannot read private data of other
partitions.
    The GWV policy implies the basic separation axioms of MASK [43, 44]. The MASK data
separation properties consider the dependency of data in different partitions indirectly. They are
based on a shared memory by which partitions influence with each other by external event. The
MASK data separation properties can be represented by the GWV policy, except the Temporal
Separation Property. The No-Exfiltration property is a special case of exfiltration theorem in [46]
without the dia function. The No-Infiltration property is equivalent to the infiltration theorem
in [46] on different abstract models. The Separation of Control property means that one step
execution in a partition cannot affect data on other partitions. Its external event may affect the
shared memory, but not memory areas in other partitions. It is a special case of exfiltration
theorem in [46] in the situation that partitions exchange data indirectly by the shared memory.
For the Kernel Integrity property, the shared memory is the data area of a special partition, then
one step internal execution of other partitions could not affect this shared memory. This is a
special case of the exfiltration theorem in [46].
    Noninfluence is semantically equal to the conjunction of noninterference and nonleakage
[55]. GWV is stronger than noninterference [58].
    Finally, the shared resources and communication channels, etc., among partitions can affect
the scheduling in separation kernels. But the relationship among spatial separation and temporal
separation is complicated and not clear now. It needs further study.

4.2.2. Information Flow Security Policy
    The GWV policy proposed by Rockwell Collins has been considered as the security policy
to provide evidence for the CC evaluation and is used in verification of industrial separation
kernels, such as AAMP7G microprocessor, INTEGRITY-178B separation kernel and PikeOS
separation kernel. The separation security policies: infiltration, mediation and exfiltration [95]
can be presented by the GWV separation axiom [46]. GWV is stronger than noninterference [42]
and supports intransitive noninterference [54] as proved in [47]. As an industrially applicable and
practically proved security policy, the GWV policy is a useful property for verifying separation
kernels and proving the policy could be considered as a trusted way for certification.

4.2.3. Theorem Proving vs. Model Checking Separation Kernels
    From Table 4.1, we could see that most of verification work on spatial separation use the
theorem proving approach. The reasons are (1) separation kernels for safety and security-critical
systems need fully formal verification. Whilst model checking approach is not competent be-
cause of its state space explosion problem; (2) separation kernels usually are small and have
thousands of lines of source code that make it is possible to be fully verified and theorem prov-
ing approach can be applied without too much cost; (3) it is difficult to represent separation
properties of separation kernels in property languages, such as LTL and CTL, in model checking
approach; (4) theorem proving approach on verifying operating system kernels exhibits good
results. For instance, more than 140 bugs are found in the project of verifying the seL4 kernel.
    Different to the theorem proving approach on spatial separation, verifying the temporal sepa-
ration usually uses the model checking approach. The reason is that it is difficult to express time
by logics in the theorem provers. However, the time can be conveniently represented in model
checkers, such as the timed automata in the UPPAAL tool. The problem of model checking
                                                27
temporal separation is that size and complexity of separation kernels limit the approach to ana-
lyze only one configuration at a time. The global scheduler is verified with the local scheduler
together and the verification result relies on the number of partitions. Honeywell has faced this
problem and uses the PVS theorem prover to analyze the DEOS scheduler [28]. Our opinion is
that verifying temporal separation needs more study of theorem proving approach in the future.
     The capability and automation of specification and verification systems play key roles in en-
forcing security of separation kernels. Theorem provers, such as Isabelle/HOL, HOL4 and PVS,
have been applied in formal verification of spatial separation properties. The expressiveness of
formal notations in these provers is enough for spatial separation. A shortage is the low degree
of verification automation. In model checking approach, efforts have been paid on automatically
formal verification of spatial separation properties on security systems. Security policies are clas-
sified in [96]. Information flow security properties are not trace properties, but hyperproperties.
They have developed a prototype model checker for hyperproperties in [97] using the OCaml
program language. The prototype is very preliminary and currently does not scale up to 1,000
states. It is even not applicable to formally verify abstract specification of separation kernels
now. Thus, automatically formal verification of separation kernels is attractive in the future.

4.2.4. Correctness of Separation Kernels
    As studied in [21], correctness properties of the PikeOS kernel are formulated as a simulation
relation between the concrete system and an abstract model. As well as the functional properties,
correctness properties of address translation, memory separation, techniques to handle assembly
code, and assumptions on various components like the compiler, hardware and implementation
policies are identified as ingredients of operating system kernel correctness. For separation ker-
nels, the paper [63] has summarized the separation kernel requirements according to the original
definition [1] and SKPP extensions [15], which includes functionalities and security, separation
and information flow, configuration, principle of least privilege, memory management, execution
and scheduling, and platform considerations. We consider that properties of security, separation,
information flow, memory, scheduling, etc., are typical and important correctness properties of
separation kernels, and there are still other correctness properties to be taken into account.

4.2.5. Developing Correct Separation Kernels
     The two primary approaches to developing correct separation kernel are (1) formal devel-
opment from top-level specification to low-level implementation by refinement and (2) formal
verification of low-level implementation according to its specification. In formal methods, re-
finement is the verifiable transformation of high-level formal specification into low-level imple-
mentation and then into executable code. B [66] and Z [65] are typical formal development
methods for software. Correctness of models in different abstract levels and correspondence be-
tween models of two neighboring levels assure the correctness of the design. The certifiable code
generation guarantees the correspondence between the low-level implementation and the source
code. The work [67, 63, 62, 60] employ this approach to develop correct separation kernels.
Due to the successful application in industrial projects [13, 98], formal development of sepa-
ration kernels by refinement into the low-level implementation can alleviate the manual review
between the design and the implementation in safety and security certification.
     In formal verification of separation kernels, the EAL 7 of CC does not enforce formal ver-
ification on the source code level. Therefore, many verification efforts on separation kernels
are carried out on the abstract- or low-level models. Establishing correspondence between the
model and the source code of the implementation is typically by code review and not formally
                                                 28
assured, such as CC evaluation of the INTEGRITY-178B separation kernel [23]. Others, such
as [24, 25, 22], annotate the source code of separation kernels for formal verification. The work
[45, 57, 28] translates the source code manually/automatically to formal languages in theorem
provers for reasoning. While the work [49, 18, 76] verifies separation kernels on binary or as-
semble code level.
    As illustrated by the project of verifying seL4 kernel, fully formal verification shows better
result and less certification cost (for example EAL 7 certification) [30]. Due to the feasibility and
successful experiences, our opinion is to recommend fully formal verification on source code
level. Formal development based on B, Z and other formal methods is recommended to develop
new separation kernels.


5. Conclusion

    In this paper, we surveyed the research work on formal specification and verification of sepa-
ration kernels, which covered the concepts, security policies, properties, formal specification and
formal verification approaches. We aimed at presenting the framework and focuses of related
work, so the details were not touched. Future work includes the formal comparison of correct-
ness properties, a formal model for separation kernels and efforts on fully formal verification.


References
 [1] Rushby J. Design and verification of secure systems. ACM SIGOPS Operating Systems Review, 1981, 15(5):12–21.
 [2] Alves-FossJ , Oman PW, Taylor C, and Harrison WS. The mils architecture for high-assurance embedded systems.
     International journal of embedded systems, 2006, 2(3-4):239–247.
 [3] Denning DE. A lattice model of secure information flow. Communications of the ACM, 1976, 19(5):236–243.
 [4] Gjertsen T and Nordbotten NA. Multiple independent levels of security (mils)–a high assurance architecture for
     handling information of different classification levels. Technical report, FFI report, 2008.
 [5] Airlines Electronic Engineering Committee et al. Arinc 653 - avionics application software standard interface.
     2003.
 [6] Wind river vxworks mils platform. Technical report, 2013.
 [7] Safety-critical products: Integrity-178b real-time operationg system. Technical report, Green Hills Software, Inc.,
     2005.
 [8] Lynxsecure: software security driven by an embedded hypervisor. Technical report, LynuxWorks, Inc., 2012.
 [9] Lynxos-se: Time- and space-partitioned rtos with open-standards apis. Technical report, LynuxWorks, Inc., 2008.
[10] Robert K and Stephan W. The pikeos concept – history and design. Technical report, SYSGO AG, 2007.
[11] Delange J and Lec L. Pok, an arinc653-compliant operating system released under the bsd license. In: Proceedings
     of 13th Real-Time Linux Workshop, 2011.
[12] Masmano M, Ripoll I, Crespo A, and Metge J. Xtratum: a hypervisor for safety critical embedded systems. In:
     Proceedings of 11th Real-Time Linux Workshop, 2009.
[13] Woodcock J, Larsen PG, Bicarregui J, and Fitzgerald J. Formal methods: Practice and experience. ACM Computing
     Surveys, 2009, 41(4):19:1–19:36.
[14] National Security Agency. Common criteria for information technology security evaluation, 3.1 r4 edition, 2012.
[15] U.s. government protection profile for separation kernels in environments requiring high robustness. Technical
     report, National Security Agency, June 2007.
[16] Federal Aviation Authority. Software considerations in airborne systems and equipment certification, 1992. docu-
     ment no. Technical report, RTCA/DO-178B, RTCA, Inc.
[17] Federal Aviation Authority. Software considerations in airborne systems and equipment certification, 2011. docu-
     ment no. Technical report, RTCA/DO-178C, RTCA, Inc.
[18] Wilding MM, Greve DA, Richards RJ, and Hardin DS. Formal verification of partition management for the aamp7g
     microprocessor. In: Design and Verification of Microprocessor Systems for High-Assurance Applications, Springer,
     2010, 175–191.
[19] Baumann C, Beckert B, Blasum H, and Bormer T. Formal verification of a microkernel used in dependable software
     systems. In: Computer Safety, Reliability, and Security Springer, 2009, 187–200.
                                                          29
[20] Baumann C and Bormer T. Verifying the pikeos microkernel: first results in the verisoft xt avionics project. In:
     Proceedings of Doctoral Symposium on Systems Software Verification, 2009, 20–20.
[21] Baumann C, Beckert B, Blasum H, and Bormer T. Ingredients of operating system correctness. In: Proceedings of
     Embedded World Conference, 2010.
[22] Baumann C, Bormer T, Blasum H, and Tverdyshev S. Proving memory separation in a microkernel by code level
     verification. In: Proceedings of 14th IEEE International Symposium on Object/Component/Service-Oriented Real-
     Time Distributed Computing Workshops, 2011, 25–32.
[23] Richards RJ. Modeling and security analysis of a commercial real-time operating system kernel. In: Design and
     Verification of Microprocessor Systems for High-Assurance Applications, Springer, 2010, 301–322.
[24] Heitmeyer CL, Archer M, Leonard EI, and McLean J. Formal specification and verification of data separation
     in a separation kernel for an embedded system. In: Proceedings of the 13th ACM conference on Computer and
     communications security, 2006, 346–355.
[25] Heitmeyer CL, Archer M, Leonard EI, and McLean J. Applying formal methods to a certifiably secure software
     system. IEEE Transactions on Software Engineering, 2008, 34(1):82–98.
[26] Penix J, Visser W, Engstrom E, Larson A, and Weininger N. Verification of time partitioning in the deos scheduler
     kernel. In: Proceedings of the 22nd international conference on Software engineering, 2000, 488–497.
[27] Penix J, Visser W, Park S, Pasareanu C, Engstrom E, Larson A, and Weininger N. Verifying time partitioning in
     the deos scheduling kernel. Formal Methods in System Design, 2005, 26(2):103–135.
[28] Ha V, Rangarajan M, Cofer D, Rues H, and Dutertre B. Feature-based decomposition of inductive proofs applied
     to real-time avionics software: An experience report. In: Proceedings of the 26th International Conference on
     Software Engineering, 2004, 304–313.
[29] Bulkeley W. Crash-proof code. MIT Technology Review, 2011, 114(3):53–54.
[30] Klein G, Elphinstone K, Heiser G, Andronick J, Cock D, Derrin P, Elkaduwe D, Engelhardt K, Kolanski R, Norrish
     M, et al. sel4: Formal verification of an os kernel. In: Proceedings of the ACM SIGOPS 22nd symposium on
     Operating systems principles, 2009, 207–220.
[31] Klein G, Andronick J, Elphinstone K, Heiser G, Cock D, Derrin P, Elkaduwe D, Engelhardt K, Kolanski R, Norrish
     M, et al. sel4: formal verification of an operating-system kernel. Communications of the ACM, 2010, 53(6):107–
     115.
[32] Klein G. Operating system verification - an overview. Sadhana, 2009, 34(1):27–69.
[33] Ames SR, Gasser M, and Schell RR. Security kernel design and implementation: An introduction. Computer,
     1983, 16(7):14–22.
[34] Mark V, William B, Ben C, Jahn L, Carol T, and Gordon U. Mils:architecture for high-assurance embedded
     computing. CrossTalk: The Journal of Defense Software Engineering, 2005, 12–16.
[35] Protection profile for partitioning kernels in environments requiring augmented high robustness. Technical report,
     The Open Group, 2003.
[36] Parr GR and Edwards R. Integrated modular avionics. Air & Space Europe, 1999, 1(2):72 – 75.
[37] Levin TE, Irvine CE, Weissman C, and Nguyen TD. Analysis of three multilevel security architectures. In:
     Proceedings of the 2007 ACM workshop on Computer security architecture, 2007, 37–46.
[38] Rushby J. Partitioning in avionics architectures: Requirements, mechanisms, and assurance. Technical report,
     DTIC Document, 2000.
[39] Leiner B, Schlager M, Obermaisser R, and Huber B. A comparison of partitioning operating systems for integrated
     systems. In: Computer Safety, Reliability, and Security, 2007, 342–355.
[40] Ramamritham K and Stankovic JA. Scheduling algorithms and operating systems support for real-time systems.
     Proceedings of the IEEE, 1994, 82(1):55–67.
[41] Popek GJ and Goldberg RP. Formal requirements for virtualizable third generation architectures. Communication
     of ACM, 1974, 17(7):412–421.
[42] Goguen JA and Meseguer J. Security policies and security models. In: Proceedings of IEEE Symposium on Security
     and privacy, 1982.
[43] Martin W, White P, Taylor FS, and Goldberg A. Formal construction of the mathematically analyzed separation
     kernel. In: Proceedings of IEEE International Conference on Automated Software Engineering, 2000, 133–141.
[44] Martin WB, White PD, and Taylor FS. Creating high confidence in a separation kernel. Automated Software
     Engineering, 2002, 9(3):263–284.
[45] Murray T, Matichuk D, Brassil M, Gammie P, and Klein G. Noninterference for operating system kernels. In:
     Certified Programs and Proofs, Springer, 2012, 126–142.
[46] Greve D and Wilding M. A separation kernel formal security policy. In: Proceedings of the ACL2 Workshop, 2003.
[47] Alves-foss J and Taylor C. An analysis of the gwv security policy. In: Proceedings of the ACL2 Workshop, 2004.
[48] Integrity-178b separation kernel security target. Technical report, Green Hills Software, 2008.
[49] Greve D, Richards R, and Wilding M. A summary of intrinsic partitioning verification. In: Proceedings of the
     ACL2 Workshop, 2004.
                                                         30
[50] Greve D. Information security modeling and analysis. In: Design and Verification of Microprocessor Systems for
     High-Assurance Applications, Springer, 2010, 249–299.
[51] Rushby J. A separation kernel formal security policy in pvs. Technical report, CSL Technical Note, SRI Interna-
     tional, 2004.
[52] Tverdyshev S. Extending the gwv security policy and its modular application to a separation kernel. In: NASA
     Formal Methods, Springer, 2011, 391–405.
[53] Greve D, Wilding M, and Vanfleet WM. High assurance formal security policy modeling. In: Proceedings of the
     17th Systems and Software Technology Conference, 2005.
[54] Rushby J. Noninterference, transitivity, and channel-control security policies. Technical report, SRI International,
     Computer Science Laboratory, 1992.
[55] Oheimb D. Information flow control revisited: Noninfluence= noninterference+ nonleakage. In: Proceedings of
     9th European Symposium on Research Computer Security, 2004, 225–243.
[56] Mantel H and Sabelfeld A. A generic approach to the security of multi-threaded programs. In: Proceedings of the
     14th IEEE Workshop on Computer Security Foundations, 2001, 126–142.
[57] Murray T, Matichuk D, Brassil M, Gammie P, Bourke T, Seefried S, Lewis C, Gao X, and Klein G. sel4: from
     general purpose to a proof of information flow enforcement. In: Proceedings of 34th IEEE Symposium on Security
     and Privacy, 2013, 415-429.
[58] Ramirez A, Schmaltz J, Verbeek F, Langenstein B, and Blasum H. On two models of noninterference: Rushby and
     greve, wilding, and vanfleet. In: Proceedings of Computer Safety, Reliability, and Security, 2014, 246–261.
[59] Craig I. Formal Models of Operating System Kernels. Springer, 2006.
[60] Craig I. Formal Refinement for Operating System Kernels. Springer, 2007.
[61] Abrial JR, Schuman S, and Meyer B. Specification language. In: On the Construction of Programs, Cambridge
     University Press, 1980, 343–410.
[62] Velykis A and Freitas L. Formal modelling of separation kernel components. In: Proceedings of the 7th Interna-
     tional colloquium conference on Theoretical aspects of computing, 2010, 230–244.
[63] Velykis A. Formal modelling of separation kernels. Master’s thesis, Department of Computer Science, University
     of York, 2009.
[64] Jones C, O’Hearn P, and Woodcock J. Verified software: A grand challenge. Computer, 2006, 39(4):93–95.
[65] Woodcock J and Davies J. Using Z: Specification, Refinement, and Proof. Prentice-Hall, 1996.
[66] Abrial JR. The B-Book: assigning programs to meanings. Cambridge University, 1996.
[67] André P. Assessing the formal development of a secure partitioning kernel with the b method. In: Proceedings of
     ESA Workshop on Avionics Data, Control and Software Systems, 2009.
[68] Leuschel M and Butler M. Prob: A model checker for b. In: Proceedings of International Symposium of Formal
     Methods Europe, 2003, 855–874.
[69] Kawamorita K, Kasahara R, Mochizuki Y, and Noguchi K. Application of formal methods for designing a sepa-
     ration kernel for embedded systems. WORLD ACADEMY OF SCIENCE, ENGINEERING AND TECHNOLOGY,
     2010, 506–514.
[70] Zhao Y, Yang Z, Sanan D, and Liu Y. Event-based formalization of safety-critical operating system standards: An
     experience report on arinc 653 using event-b. In: Proceedings of IEEE 26th International Symposium on Software
     Reliability Engineering, 2015, 281–292.
[71] Abrial JR and Hallerstede S. Refinement, decomposition, and instantiation of discrete models: Application to
     event-b. Fundamenta Informaticae, 2007, 77(1-2):1–28.
[72] Verbeek F, Tverdyshev S, Havle O, Blasum H, Langenstein B, et al. Formal specification of a generic separation
     kernel. Archive of Formal Proofs, 2014.
[73] Verbeek F, Havle O, Schmaltz J, Tverdyshev S, Blasum H, et al. Formal api specification of the pikeos separation
     kernel. In: NASA Formal Methods, Springer, 2015, 375–389.
[74] Kaiser R and Wagner S. Evolution of the pikeos microkernel. In: Proceedings of First International Workshop on
     Microkernels for Embedded Systems, 2007, 50–50.
[75] Baumann C, Beckert B, Blasum H, and Bormer T. Better avionics software reliability by code verification. In:
     Proceedings of Embedded World Conference, 2009.
[76] Dam M, Guanciale R, Khakpour N, Nemati H, and Schwarz O. Formal verification of information flow secu-
     rity for a simple arm-based separation kernel. In: Proceedings of the ACM SIGSAC Conference on Computer &
     Communications Security, 2013, 223–234.
[77] Zhao Y, Sanan D, Zhang F, and Liu Y. Reasoning about information flow security of separation kernels with
     channel-based communication. In: Proceedings of the 22nd International Conference on Tools and Algorithms for
     the Construction and Analysis of Systems, 2016, 791–810.
[78] Heiser G. The role of virtualization in embedded systems. In: Proceedings of the 1st workshop on Isolation and
     integration in embedded systems, 2008, 11–16.
[79] McDermott J, Montrose B, Li M, Kirby J, and Kang M. Separation virtual machine monitors. In: Proceedings of
                                                          31
     the 28th Annual Computer Security Applications Conference, 2012, 419–428.
[80] Crespo A, Ripoll I, and Masmano M. Partitioned embedded architecture based on hypervisor: the xtratum approach.
     In: Proceedings of European Dependable Computing Conference (EDCC), 2010, 67–72.
[81] Franklin J, Chaki S, Datta A, and Seshadri A. Scalable parametric verification of secure systems: How to verify
     reference monitors without worrying about data structure size. In: Proceedings of the 2010 IEEE Symposium on
     Security and Privacy, 2010, 365–379.
[82] Franklin J, Chaki S, Datta A, McCune J, and Vasudevan A. Parametric verification of address space separation. In:
     Principles of Security and Trust, Springer, 2012, 51–68.
[83] Barthe G, Betarte G, Campo JD, and Luna C. Formally verifying isolation and availability in an idealized model
     of virtualization. In: Proceedings of International Symposium on Formal Methods, 2011, 231–245.
[84] McDermott J, Kirby J, Montrose B, Johnson T, and Kang M. Re-engineering xen internals for higher-assurance
     security. Information Security Technical Report, 2008, 13(1):17 – 24.
[85] McDermott J and Freitas L. A formal security policy for xenon. In: Proceedings of the 6th ACM workshop on
     Formal methods in security engineering, 2008, 43–52.
[86] Roscoe A, Woodcock J, and Wulf L. Non-interference through determinism. In: Proceedings of the Third European
     Symposium on Research in Computer Security, 1994, 33–53.
[87] Carnevali L, Lipari G, Pinzuti A, and Vicario E. A formal approach to design and verification of two-level hierar-
     chical scheduling systems. In: Proceedings of the 16th Ada-Europe international conference on Reliable software
     technologies, 2011, 118–131.
[88] Carnevali L, Pinzuti A, and Vicario E. Compositional verification for hierarchical scheduling of real-time systems.
     IEEE Transactions on Software Engineering, 2013, 39(5):638–657.
[89] Asberg M, Pettersson P, and Nolte T. Modelling, verification and synthesis of two-tier hierarchical fixed-priority
     preemptive scheduling. In: Proceedings of 23rd Euromicro Conference on Real-Time Systems (ECRTS), 2011 ,
     2011, 172–181.
[90] Fersman E, Krcal P, Pettersson P, and Wang Y. Task automata: Schedulability, decidability and undecidability.
     Information and Computation, 2007, 205(8):1149–1172.
[91] Singhoff F and Plantec A. Aadl modeling and analysis of hierarchical schedulers. ACM SIGAda Ada Letters, 2007,
     27(3):41–50.
[92] Zerzelidis A and Wellings A. Getting more flexible scheduling in the rtsj. In: Proceedings of the 9th IEEE
     International Symposium on Object and Component-Oriented Real-Time Distributed Computing, 2006, 8–8.
[93] Zerzelidis A and Wellings A. A framework for flexible scheduling in the rtsj. ACM Transactions on Embedded
     Computing Systems, 2010, 10(1):3:1–3:44.
[94] Zerzelidis A and Wellings A. Model-based verification of a framework for flexible scheduling in the real-time
     specification for java. In: Proceedings of the 4th international workshop on Java technologies for real-time and
     embedded systems, 2006, 20–29.
[95] Alves-Foss J. Multiple independent levels of security. In: Encyclopedia of Cryptography and Security, Springer
     US, 2011, 815–818.
[96] Clarkson M and Schneider F. Hyperproperties. Journal of Computer Security, 2010, 18(6):1157–1210.
[97] Clarkson M, Finkbeiner B, Koleini M, Micinski K, Rabe M, and Sánchez C. Temporal logics for hyperproperties.
     In: Proceedings of International Conference on Principles of Security and Trust, 2014, 265–284.
[98] Abrial JR. Formal methods in industry: Achievements, problems, future. In: Proceedings of the 28th International
     Conference on Software Engineering, 2006, 761–768.




                                                          32
