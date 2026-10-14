                                        Under consideration for publication in Formal Aspects of Computing




                                        A Survey of Practical Formal
arXiv:2109.01362v1 [cs.FL] 3 Sep 2021




                                        Methods for Security
                                        Tomas Kulik1 , Brijesh Dongol2 , Peter Gorm Larsen1 , Hugo Daniel Macedo1 ,
                                        Steve Schneider2 , Peter Würtz Vinther Tran-Jørgensen3 and Jim Woodcock1,4
                                        1 Aarhus University
                                        2 University of Surrey
                                        3 Bankdata
                                        4 University of York




                                        Abstract. In today’s world, critical infrastructure is often controlled by computing systems. This introduces
                                        new risks for cyber attacks, which can compromise the security and disrupt the functionality of these systems.
                                        It is therefore necessary to build such systems with strong guarantees of resiliency against cyber attacks.
                                        One way to achieve this level of assurance is using formal verification, which provides proofs of system
                                        compliance with desired cyber security properties. The use of Formal Methods (FM) in aspects of cyber
                                        security and safety-critical systems are reviewed in this article. We split FM into the three main classes:
                                        theorem proving, model checking and lightweight FM. To allow the different uses of FM to be compared,
                                        we define a common set of terms. We further develop categories based on the type of computing system FM
                                        are applied in. Solutions in each class and category are presented, discussed, compared and summarised.
                                        We describe historical highlights and developments and present a state-of-the-art review in the area of FM
                                        in cyber security. This review is presented from the point of view of FM practitioners and researchers,
                                        commenting on the trends in each of the classes and categories. This is achieved by considering all types
                                        of FM, several types of security and safety critical systems and by structuring the taxonomy accordingly.
                                        The article hence provides a comprehensive overview of FM and techniques available to system designers of
                                        security-critical systems, simplifying the process of choosing the right tool for the task. The article concludes
                                        by summarising the discussion of the review, focusing on best practices, challenges, general future trends
                                        and directions of research within this field.

                                        Keywords: Formal methods, model checking, theorem proving, cyber security.




                                        Correspondence and offprint requests to: Tomas Kulik, Aarhus University, Department of Electrical and Computer Engineering,
                                        Finlandsgade 22, 8200, Aarhus, Denmark. e-mail: tomaskulik@ece.au.dk
2                    T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



1. Introduction
Digital services are currently spreading to all aspects of society [RSB+ 15]. This in turn causes dependence of
society on the cyber infrastructure needed to support these services. The heavy reliance on cyber infrastruc-
ture poses new challenges in the form of cyber attacks and potentially cyber terrorism [Ken15], with threat
actors encompassing the full range from interpersonal offenders, cyber criminals and “hacktivists” through to
well-resourced state actors [RCD+ 19]. Disturbances in financial, industrial or day-to-day consumer services
could lead to significant financial and societal costs. As digitisation spreads further, the potential attack sur-
faces only grow larger, increasing the challenge of protecting digital services [UA19, WANC16]. As systems
grow larger and more complex, significant resources have to be spent to secure these system against known
cyber attacks. Often the protection mechanisms are incorporated to close vulnerabilities uncovered after a
successful cyber attack, and hence are of a reactive nature. This approach relegates cyber security from a
primary challenge to be solved within the system to an afterthought [SWA+ 12].
    Due to the wide spectrum of cyber attacks, it is difficult to directly quantify their impact on soci-
ety [GSM+ 11], however very often they involve significant financial costs as well as potential disruptions in
quality of life. One example is a potential cyber attack against electricity infrastructure, including electricity
marketplace, which could lead to destruction of generators and disclosure of confidential data [NPYG09].
Another example is attacks against manufacturing facilities causing delays or decrease in quality of pro-
duction [BSW+ 18], [QPP+ 17]. These examples demonstrate that cyber threats should be considered as
significant as physical threats against societal infrastructure.
    The earlier the potential cyber security threats are discovered within new systems, the cheaper the
mitigation for these threats will be [WMPO16]. Formal Methods (FM) provide an opportunity for discovery
and mitigation of cyber threats at all stages of the lifecycle of a system. Using FM brings mathematical
rigour to the field of cyber security assurance. This is possible since FM are techniques that use model-
based approaches, where the models are rigorously specified [Win90]. These models represent the software,
hardware or a combination of the two for the system in question. The primary benefit of using FM stems from
the mathematical proof of the internal consistency of the system design [Hal05]. This proof provides strong
assurances since it considers the entire system behaviour, and once proven true it remains true, whereas
in traditional testing it is only possible to cover specific scenarios. FM can be seen as a tool well suited
for providing assurances of cyber security for digital society [Win98]. Beyond the assurance of behavioural
correctness of a system, the adoption of a fully fledged formal approach is known to reduce the number of
implementation errors, which are the building blocks of exploits.
    Within the area of FM there are distinct approaches. The main categories we consider are:
    • Theorem Proving, analysing a formal description for important properties based on computer-based
      proofs.
    • Model Checking, checking whether a finite-state model of a system meets a given specification in an
      exhaustive manner.
    • Lightweight FM, using formal techniques to analyse a system either statically or dynamically (this concept
      was coined in [JW96] but we have extracted the model checking from their characterisation into a category
      of its own).
    In all cases, the methods are applied to determine if a system behaves in a correct way and many
approaches have received significant tool support for automation of the verification and validation pro-
cess [ADKT11]. In this survey we consider all of the approaches and their application to specific areas of
digital society. We further consider FM as applied to the specific level of abstraction of system behaviour
ranging from the application level to the hardware level. By considering the state-of-the-art research in
formal verification across these dimensions, we provide a non-exhaustive overview of application of FM in
specific disciplines. The aim of this survey is to allow practitioners to identify a proven method applicable
to a system in their domain, hence increasing the adoption of FM in the field of cyber security.


1.1. Methodology
The amount of research publications within the area of applying FM towards cyber security challenges is
significant. Therefore several constraints have been placed on the choice of research publications to be consid-
ered within this survey. The first important constraint is the recency of the research reported, considering the
A Survey of Practical Formal Methods for Security                                                            3



landscape of the last decade, limiting the publication date to be no earlier than 2012. Furthermore all of the
research work need to be published in scientific venues such as journals, conferences or workshops. The next
constraint is focus on computer-based tool supported formal methods, i.e. only formal methods with tools
that can provide computer-based analysis and often guide users on performing this analysis are considered.
This consideration is in order to focus more on the FM that could be potentially applied outside of academia,
bringing the benefits of the formal security analysis to industry. This goes hand in hand with our focus on
the applied FM, searching for research publications, where a tool supported FM is utilised to deal with a
concrete cyber security problem. Hence this survey does not focus on theoretical advances of FM in security
or proposed processes that briefly mention use of formal methods, such as theoretical approaches to model
checking algorithms, specification of hyperproperties and similar. Furthermore our survey does not cover the
approach to security commonly referred to as provable security. This refers to a mathematical approach to
analysing the security of cryptographic mechanisms or systems. The approach considers the system in the
context of an attacker model, and expresses the security requirements within that model as a limitation on
what the attacker should be able to achieve. A proof consists of establishing that the attacker would need
to break a known hard problem (such as the Quadratic Residuosity Problem [GM84]) in order to break the
security of the system. Thus the security of the system is reduced to the difficulty of the underpinning hard
problem. This approach is typically used within the field of cryptography rather than secure systems, and
so falls outside the scope of our survey. We point the reader to [BBB+ 19] providing the report within the
area of FM in cryptography. Finally, we constrain our search to research that considers aspects of security
explicitly, and not as a by-product of safety or correctness. The search for the research publications was
carried out as a cross database search using Google Scholar, while focusing on research papers, excluding
research abstracts or extended abstracts.
    As this survey shall provide a reader with a quick overview of the research conducted, we have further
decided to categorise different research publications by the industry (domain) on which they focus as well as
the level of abstraction on which the formal method is utilised. In this way researchers and also potentially
industrial users can quickly find the area of their interest within this survey. Furthermore, we classify the
research based on the cyber security problem classification as elicited from the discovered research papers
and inspired by existing literature [RCD+ 19].


1.2. History

This section presents a history of impactful research works within FM in security over the last 40 years. We
choose four case studies where formal methods have been applied to secure systems:
1. The Needham-Schroeder Public-Key Protocol. Lowe used a refinement model checker to find a triangular
   attack on the protocol. This was a new attack on a protocol that had previously been proven correct by
   Burrows et al. [BAN90].
2. The Mondex smartcard. This was the first commercial product to be certified to ITSEC Level E6. There
   was considerable discussion at the time as to whether this was even possible.
3. The Tokeneer ID Station. There were similar questions about the feasibility of using FM to achieve the
   level of rigour required by the higher assurance levels of the Common Criteria. Tokeneer settled this
   matter.
4. The seL4 Microkernel. This system has the reputation of being the world’s most assured microkernel.
   Significantly, it demonstrates that security and the use of formal methods do not lead to poor performance.

The Needham-Schroeder Public-Key Protocol The Needham-Schroeder Public-Key Protocol is a
transport-level protocol for communication between network devices [NS78], providing mutual authenti-
cation between two parties in a network. The protocol is visualised in Figure 1(a). Simple and well known,
it has become a popular benchmark for testing security protocol verification technology. We discuss it here
because it is an important security protocol that nevertheless contained a significant error. This error was
found using automated FM.
    [Low95] showed that, contrary to its intention, the protocol fails to ensure authentication. In particular,
he demonstrated that an intruder can impersonate an agent A during a run of the protocol. The impersonator
tricks another agent B into thinking that they are talking to A.
    The protocol uses public key cryptography. Each agent A possesses a public key, which any other agent
4                       T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock

      A                  B                                    A                   I                B
            {A, NA }pkB                                            {A, NA }pkI
                       -                                                         - {A, NA }pkB-
       {N , N }                                                {N , N }    {NA , NB }pkA
        A B pkA                                                A B pkA 
             {NB }pkB                                            {NB }pkI
                        -                                                 - {NB }pkB -

       ?                    ?                                  ?                  ?                 ?

                (a)                                                              (b)
                        Fig. 1. (a) Needham-Schroeder authentication protocol, and (b) attack

can get from a server. A also possesses a secret key that is the inverse of its public key. Any agent can encrypt
a message using A’s public key, but only A can decrypt it, ensuring secrecy. The protocol also uses nonces:
random numbers coined for single runs of the protocol.
    Lowe encoded the protocol in CSP [Hoa85] and analysed it using CSP’s model checker, FDR [GR19].
Lowe did not know in advance that an attack was possible, although he may have suspected it. He did not
know where to look in the protocol for a vulnerability, but the exhaustive search carried out by the model
checker found an attack in spite of this.
    Suppose that I (an intruder) is a network user who can take part in network sessions. I can also intercept
messages and inject new ones, but is not able to decrypt messages without the key. I can produce a new
message in two circumstances: if I invents the nonce, or if I already understands the message’s contents. This
intruder can also replay complete encrypted messages, even without understanding the contents [RSG+ 01].
This approach is commonly known as the Dolev-Yao model [DY81].
    The attack involves two simultaneous runs of the protocol, as shown in Figure 1(b). A establishes a valid
session with I. At the same time, I impersonates A to establish a fake session with B. The flawed run of the
protocol could be explained as follows. A sends a message with nonce NA to I, who decrypts the message
with I’s secret key. I relays the message to B, pretending to B that A is communicating. B sends NB in
response, encrypted for A, and so I relays this encrypted nonce to A. A decrypts NB and confirms it to I,
who learns it. I re-encrypts NB and returns it to B, which convinces B that A is the other party. At the end
of the attack, B falsely believes that A is the communication partner, and that only A and B know NA and
NB . This shows that the protocol is insecure. Protocol analysts call this a man-in-the-middle attack. Here,
it has been discovered automatically.

Mondex The Mondex application consists of smart cards with electronic purses (wallets) for electronic
commerce [SCW00]. Customers use Mondex smart cards for low-value, cash-like transactions that need no
third-party involvement. The Bank of England (the financial regulator in this instance) considered the re-
quirements for Mondex to be security critical: Mondex must have no implementation or design bugs that could
allow electronic counterfeiting. So the developers certified Mondex to the highest standard available at the
time. This was ITSEC Level E6 [ITS91], equal to Common Criteria Evaluation Assurance Level 7 [CCR06].1
Mondex was the first commercial product to achieve ITSEC Level E6 (EAL7).
    [SCW00] further describe the development of the Mondex application, with its abstract and concrete
models. The abstract model describes the world of electronic purses: atomic transactions exchange value and
the abstract model expresses their required security properties. The concrete model is the purse design and
the message protocol for value exchange.
    The design team used the Z notation [Spi89, WD96] to specify both models. They proved that the
concrete model is formally a refinement of the abstract one. This means that the concrete model respects
all the abstract security requirements. The abstract model and its security properties is often easier to

1   The levels of the Common Criteria are:
    EAL1:     Functional testing.                          EAL5:    Semi-formal design and testing.
    EAL2:     Structural testing.                          EAL6:    Semi-formally verified design and testing.
    EAL3:     Methodical testing and checking.             EAL7:    Formally verified design and testing.
    EAL4:     Methodical design, testing, and reviewing.
A Survey of Practical Formal Methods for Security                                                                             5



understand than the concrete model. Developers wrote manual proofs, believing that no efficient automated
tools existed for such a large task. Instead, proof steps were type-checked using the f uzz2 and Formaliser
tools [FHB89]. Proofs were also checked by independent external evaluators.
   There were four principal security properties:
    • The system and its users may not create value.
    • The system must account for all value.
    • Purses must have enough value for their intended transaction.
    • All transfers must be between authentic purses.
The design team changed a secondary protocol after the proof revealed a bug. A detailed account of the
project is given in [WSC+ 08]. Mondex has proved to be a dependably secure system, guaranteed by its
formal development.

Tokeneer The Tokeneer system was developed by the US National Security Agency (NSA) [BCJ+ 06].3 It
provides secure access to an enclave of workstations with controlled physical entry. Access control requires
biometric checks and security tokens. These tokens describe a user’s permitted actions within a particular
visit to the enclave.
    Developers needed to assure the security properties. They did this by conformance with the Common
Criteria Evaluation Assurance Level 5 [CCR06]. They also needed to show they could do this in a cost-effective
way. NSA invited bids to use FM to develop a component of the Tokeneer system, and then monitored this
experiment to measure the effort and skills needed to perform the development.
    Praxis (a UK company) won the contract and wrote a formal specification in Z [Spi89, WD96], formally
refining the specification to a SPARK program. SPARK is a subset of Ada with an accompanying tool-
set [Bar12]. They proved key system properties and the absence of run-time errors, using traditional methods
to develop extra software. These extra Ada programs provided interfaces with peripherals.
    The project required 260 person-days, three people part-time, and nine months’ elapsed time. It produced
about 10k lines of SPARK code with about 16.5k contracts. About 200loc were written on average per day
during the implementation phase, with about 40loc through the entire project. A further 3.5k lines of standard
Ada code were produced, with about 200loc per day in the implementation phase or 90loc throughout the
project. System testing took about 4% of the project effort, much smaller than usual.
    Two defects were found in Tokeneer. One was found using formal analysis, another was found by code
inspection.4 The testing team discovered two in-scope failures: missing items in the user manual.
    The task set by NSA was to conform to Common Criteria EAL5. The Tokeneer development actually
exceeded EAL5 requirements in several areas: configuration control, fault management, and testing. Although
the main body of the core development work was carried out to EAL5, the development areas covering
specification, design, implementation, correspondence were accomplished to EAL6 and EAL7. Why? Because
it was cheaper!

The seL4 Microkernel The third-generation microkernel seL4 provides abstractions for virtual address
spaces, threads, and inter-process communication. It provides an explicit memory management model and
capabilities for authorisation. There is a guarantee that the binary code of the ARM version of the seL4
microkernel is a correct implementation.5 seL4 meets its abstract specification and does nothing else. In
particular, the seL4 ARM binary meets the classic security properties of integrity and confidentiality.
   The seL4 micro-kernel has a formal proof of its C code against its abstract specification [KAE+ 10]. This


2  See spivey.oriel.ox.ac.uk/corner/Fuzz_typechecker_for_Z.
3  For comprehensive information on Tokeneer, see the AdaCore webpages www.adacore.com/tokeneer, where the entire project
archive can be downloaded. AdaCore distribute the material generated by Altran under contract to the NSA under the terms
of the Technology Transfer Agreement agreed between Praxis and the NSA. This material consists of all the core and support
software for the Tokeneer ID Station, project documents, test cases derived from the system test specification, test tokens, and
biometric data.
4 Diomidis Spinelli: www.spinellis.gr/blog/20081018/.
5 On the ARM platform, there is a further proof that the binary code that executes on the hardware is a correct translation of
the C code for sel4. This means that the compiler does not have to be trusted, and extends the functional correctness property
to the binary. See docs.sel4.systems/FrequentlyAskedQuestions.html.
6                  T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



proof is machine checked in Isabelle/HOL [NK14]. This assumes correctness of boot code, cache management,
hardware, and hand-written assembly code.
    The developers claim seL4 to be the only verified general-purpose operating system (OS) kernel. An
operational model of the system forms as an abstract specification. A Haskell program prototypes the kernel.
This prototype provides an automatic translation into Isabelle/HOL. The Isabelle code is then an executable,
design-level specification of the kernel. This is hand coded in C to form a high-performance C implementation
of seL4. Refinement proofs link the specifications and the C code. Developers proved that attackers cannot
subvert the kernel. Not even if they use buggy encodings, spurious calls, or buffer overflow attacks.




1.3. Definitions/Background

Here we provide a set of common terms and definitions used throughout this article. This is particularly
important since the fields of formal verification and security developed independently for many years, and
hence, some terms are overloaded and have slightly different meanings depending on the context in which
they are used. For example, in security (particularly cryptography), a certificate refers to a document that
is used to bind an entity to a cryptographic key. On the other hand, within FM, certificate is used as a
proof of correctness of a system or protocol.
   Throughout this article, we use authentication to refer to the process of identifying and validating
whether a user (an entity or individual) accessing a system is who the user claims to be. This is in contrast
with authorisation, which is the process of allowing a user access to a system based on their identity.
    The systems under consideration typically comprise a set of coordinated processes, which are program
instances defining a set of instructions that are executed by one or more threads. We think of processes as
being active entities in a system, as opposed to programs which are passive entities. Formal frameworks to
describe the behaviour of processes include CSP, CCS, ACP, π-calculus, etc. Processes typically implement
protocols, i.e., a set of rules for transmission of data, and may synchronise over shared memory or
communicate over a channel, which is an abstraction of a physical communication network. Shared memory
implementations are increasingly complex due to the use of intermediate processor caches and may implement
many different consistency models [AG96]. Similarly, one may place many different assumptions on a channel,
e.g., FIFO ordering of messages; whether the channel guarantees integrity, availability and confidentiality;
whether the channel is error free; whether message types can be distinguished, etc. Security protocols are
often designed to provide specific properties such as isolation, which is a design principle in which processes
are separated and given privileged access to shared resources, e.g., shared memory (typically using techniques
such as containerisation or virtualisation).
    In general, verification is with respect to a specification, which is an abstract (formal or informal)
description of the allowable behaviours of an entity, e.g., hardware, a system, computer program, data
structure etc. Formal verification often proceeds with respect to a model of a system, which provides a
precise formal description of an entity, capturing the key characteristics of the entity being modelled. One
must ensure that every feature described by a model is an actual feature of the entity. Different models of
the same entity may be developed depending on the properties that are of interest; a computer program for
example may be modelled by relations between pre/post state; traces of states; functions between inputs and
outputs, etc. A model may describe behavioural functionality, protocols etc. In FM, one typically develops
models at several levels of abstraction, with precise descriptions of the relationship between these levels. FM
for security also requires a model of an attacker, e.g., the Dolev-Yao model, which is used in the context of
communicating systems. Within hardware verification, the term co-verification is used to prove that system
software executes correctly on a representation of the underlying hardware design. It enables integration of
software with hardware, before any physical devices (e.g., chips or boards) are available.
   The aim of verification is to ensure that it meets its implementation (of a specification), i.e., the
physical manifestation of an entity. In some instances, one may refer to an implementation as a model that
provides enough detail about an entity for the corresponding physical entity to be readily obtained.
A Survey of Practical Formal Methods for Security                                                            7



2. Survey
2.1. Categorisation and overview
Since the FM in security are applied across many domains, we structure the scope of the survey by presenting
a categorisation based on a domain and a level of abstraction. This is done in order to provide a systematic
overview of the wide field of FM in security. The labels for the four domains we have selected are:
Financial: Aggregates the works applying FM in the area of finance/money as payment systems, home
   banking, financial markets, crypto-currencies. Examples are mobile banking apps, ATM infrastructures,
   the FIX stock exchange protocol, smart-cards/hardware wallets. The financial domain is represented in
   section 2.2.
Industrial: This label agglomerates works dealing with computing systems applied in the production of
   goods or services, manufacturing and industrial control. Examples are a Water Treatment Management
   Panels, PLC control networks, Modbus/TCP, motor controllers. The industrial domain is represented in
   section 2.3.
Consumer: It categorises works focusing on the security of end-user/individuals personal computation
   devices and applications such as a command-line shell, a home operating system, a Voice over IP protocol,
   and an exercise smart appliance. The consumer domain is represented in section 2.4.
Enterprise: This is the dual of the Consumer category, as it is used to group the works focusing on the
   security of corporate systems providing computing services satisfying the needs of organisations instead of
   individuals. Examples are email services, e-government systems, the sn2 protocol, data servers warehouses.
   The enterprise domain is represented in section 2.5.
   As presenting the four domains would only separate the FM in security research by the field of application,
we further present five levels of abstraction at which the formal verification is carried out. These levels of
abstraction are:
Application: Used for works that apply FM for security at the application or purpose of computation level.
System: Used for works that apply FM for security within the architectural level, often encompassing
   multiple subsystems.
Protocols: It is used to apply FM to assert properties or analyse communication protocols between system
   components level.
Implementation: This is a cross-cutting category encompassing all the works that focus on applica-
   tion/usage of FM directly on the resulting system (e.g.: run-time monitoring) instead of emphasis on
   designs and specifications.
Hardware: Used to classify works applying FM in the process of hardware development.
This categorisation allows us to systematically review the state-of-the-art-research and provide an overview
based on this. In order to provide a clear overview of FM in security we further apply a third dimension,
defining the type of the FM used, i.e. model checking, theorem proving and lightweight FM. This provides
a quantitative overview of different research works within Figure 2.
    The sections within this survey follow a logical organisation, where the research works are grouped to-
gether by the type of the application, system, protocol, implementation or hardware that they are applied
to. Within this grouping, the research works are further organised into paragraphs following logical cate-
gorisation. As an example the first paragraph could consider works related to manufacturing while the next
paragraph considers works related to industrial control. In both cases the research is aimed at industrial
domain but with a different scope. Each section within the survey represents a single domain, where we
present a systematic summary of research works belonging to different levels of abstraction.


2.2. Financial
Financial computing including banking systems, independent budgeting applications and mobile payment
applications is a rapidly developing field. This section provides an overview of how FM have been used
to analyse the security of banking mobile applications, alternative currencies, such as cryptocurrencies,
smart contracts, banking backend systems, electronic trading systems, payment protocols, cryptocurrency
8                       T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock




                                                        LW
     Financial        MC                                                                     LW             MC
                                                                 MC
                                            MC                                                      TP
                                TP                                                                                  TP
                                                                              TP      MC


                                                        LW                                        TP
     Industrial                                                               LW                            TP
                        MC
                                            MC                 MC                        MC
                                                                              TP                    LW              MC



                                LW                 TP                    TP                                          LW
     Consumer                                                                                TP            MC
                                            MC
                      MC                                         MC                                 LW              TP
                                 TP                                                   MC


                                                 TP                                          TP           MC
                                TP                              MC                                                   LW
     Enterprise       MC                                                                            MC
                                           MC         LW                      TP        LW                     TP



                  Application           System               Protocols             Implementation        Hardware



    Legend:                                     Area of the circles is
    MC-> Model Checking                         proportional to the
    TP-> Theorem Proving                        corresponding amount
    LW-> Lightweight FM                         of works using the
                                                technology.

                                     Fig. 2. Classification of formal methods in security

hardware and wallets. On a different levels of abstraction it could be seen within this section that the system
level consists of most research works. This section also mentions the legal challenges when applying FM to
financial systems. These legal challenges arise from limited access to these systems and a certain level of
avoidance of publication of potential vulnerabilities by vendors of these systems, i.e. often making it difficult
for researchers to get deep insight into these systems.
    The method most used to analyse security within the financial domain is model checking, and authors
apply different model checkers to specific problems. This could be attributed to the fact that the different
entities whose security is being analysed lend themselves well to be modelled in a state transition represen-
tation and also that their state space is sufficiently limited to be analysed without issues such as the state
space explosion. The cyber security topics present within the financial section are shown in Figure 3.
A Survey of Practical Formal Methods for Security                                                            9




                               Fig. 3. Cyber security topics in the financial section


2.2.1. Application

The field of financial applications is expanding rapidly. Not only do banks provide mobile applications,
but whole alternative currencies are being developed. This rapid growth provides many opportunities for
application of FM to security on an application level.
    The introduction of apps and reliance on web-based security paves the way to the application of FM to
them. A recent example of that is found within [CGHS17]. The authors discovered several vulnerabilities
while analysing apps from 15 leading UK banks. The usage of ProVerif to formally verify their proposed
correction to one of the identified flaws markets the usage of the techniques in the optimal approach. Applying
FM to banking apps provides potential for further research, but legal restrictions apply.
    Another area of FM applicability is banking malware. The major cybersecurity companies report an in-
crease in financial malware, and expect to see more attacks and growth in this area. One of the main categories
is banking Trojans, which hide in subsystems such as the Android Accessibility Service API and may steal
users’ credentials. The authors of [KKG19] have analysed Android applications by first using the Krakatau
bytecode tool6 to generate the Java byte-code of the application, then generating the Calculus of Commu-
nicating Systems (CCS) [Mil89] model from the byte-code and finally dispatching it to the Concurrency
Workbench of New Century (CWB-NC) model checker [CS96], searching for malware properties. The au-
thors note that their approach provides over 98% malware detection rate. Similarly the authors of [IMMS19]
applied model checking to the CCS models generated from Java byte-code of mobile banking Android ap-
plications. The authors have used the µ-calculus [Koz83] to further specify malware behavioural properties
such as stealing money in background operations, intercepting Short Message Service (SMS) messages and
password resetting. The model was then verified against the malware properties using the CWB-NC model
checker. The authors carried out a case study determining if an application exhibits an overlay malware
behaviour, where the application overlays a screen indistinguishable from an honest application screen with
intent of stealing banking information, demonstrating the viability of their approach.
    In the alternative currency area, participants access the currency exchange network via applications, serv-
ing as virtual wallets storing the funds and authentication secrets (private keys) that prove fund ownership.
The authors of [TVR16] analyse the properties of the Electrum Bitcoin wallet. Specifically the authors focus
on the two-factor authentication used by this wallet. The authors have created a model in ASLan++ [vOM12]
and verified the behaviour of the two-factor authentication scheme using the Cl-Atse protocol analyser [Tur06]


6   github.com/Storyyeller/Krakatau
10                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



for a bounded number of sessions. The analysis has uncovered a potential vulnerability in the user registration
process.
    New applications include smart contracts, which are contracts between two parties written in a program-
ming language. They define the flow of money based on rules and conditions that, when met, trigger the
underlying financial infrastructure to perform an exchange of funds. The automatic contract enforcement
feature opens the way to great losses if the program or the execution platform contains exploitable bugs,
thus one finds an expanding number of FM applications in this field, specifically use of certified contract
languages [AE18] and the certification of the virtual machine byte-code [PZS+ 18a]. For a more detailed
account, and a specific survey on the area and the current opportunities for FM we refer the readers to the
work [MCJ18].

2.2.2. System

The financial systems area evolves at two speeds. The legacy core banking systems delivering services such as
in-house internal bookkeeping, the SWIFT inter-bank network system, and the Europay Master Visa (EMV)
standard that underpin the world economy progress slowly. On the other hand, fierce competition by outsiders
or new regulatory demands [WNH17] push the sector to move faster. A sign of the two speeds appears in the
discrepancy between the percentages of COBOL running the systems. In 2017, Reuters reported that while
only 43% of the general US banking systems are built on top of COBOL, it is a staggering 95% in legacy
based subsystems such as ATM swipes or in-person transactions.
    The two speeds are also apparent in the application of FM. Most of the FM references mentioning legacy
systems are decades old as the case of the CICS Z specification or the applications of BAN logic. Few newer
works exist in this area, as for example, the case of the reuse of BAN logic to verify a mobile payment
system [AUS12] and the use of the SPIN tool to model check networks of ATM systems, as the case of 1-link
in Pakistan [OKQ17]. Furthermore, the authors of [ZMSZ12] also apply SPIN to verify a model of internet
payment systems.
    Finally, we highlight the work in [SIR13], as it shows the legal barriers faced by the proposer of FM in the
domain. While the work has potential for security improvemets in the financial field by finding vulnerabilities
within the banking processes, wide acceptance is yet to be observed. Another exception to the standstill in
legacy systems is the domain of traditional Electronic Trading Systems (ETSs).
    Within the ETS domain, we also observe a boom in the application of FM, specifically in non-traditional
areas of blockchain-based cryptocurrencies and unregulated/decentralised systems. There exists a large num-
ber of works in the area of blockchain-based financial services. The scope of such works range from the
verification of an algorithm in a cryptocurrency platform [YJS+ 19] and the verification of the Etherium
virtual machine system underlying the smart contract concept [HSR+ 18], to the formal verification of a
whole blockchain system [DMC+ 18].
    We must further mention outstanding works that illustrate the usage of FM beyond plain system analysis.
For instance, the authors of [ADRP13] provide an example on how to build the usually labour intensive
models of systems by applying automata learning techniques, in this case applied to the EMV standard.
Another pattern is the adoption of formal models as components in fraud detection such as within the work
of [RZR+ 13] by use of a lightweight formal specification.

2.2.3. Protocols

The world of financial transactions forms a pillar of modern society. To protect these transactions FM could
be used to provide strong security assurances.
    Near Field Communication (NFC) is a short range radio technology often used within smartphones,
bank cards and payment terminals, to facilitate contactless payments. These transactions are secured by use
of the EMV protocol [KsM02], which has been found to contain significant security vulnerabilities where
the attacker can obtain user’s payment details, present within the NFC payments [MAHvM16]. To address
this, the authors of [MGP16] have proposed a new protocol, specifically aimed at mitigating the vulnera-
bilities of the NFC part of the EMV protocol. The proposed protocol provides mutual authentication with
non-repudiation between the bank card and the terminal, the integrity of the banking data and ensures
that the bank card is valid. In order to ensure that the protocol provides the expected security the authors
specify the protocol in the Security Protocol Description Language [CM12] and express confidentiality and
authentication claims within the Scyther tool [Cre08]. The verification has demonstrated that the specifi-
A Survey of Practical Formal Methods for Security                                                             11



cation satisfies both claims. Moreover, the proposed solution is applicable for online and offline payments.
Similarly, the authors of [AMM14] have proposed a protocol for securing of NFC enabled mobile payments.
This is important as vulnerabilities such as a possibility of relay attacks [RLS13] have been discovered in
the popular NFC payment system Google Wallet. The proposed protocol uses mutual authentication be-
tween entities involved in transactions and leverages single-use passwords. In order to verify security of the
protocol, the authors create a high-level description of the protocol, translate it to CSP and express several
security requirements as formal properties. The verification is then carried out using the FDR model checker.
The protocol was shown to be resistant to replay attacks and no feasible attack was found against mutual
authentication and tag anonymity. The authors note that they plan to implement the protocol and again
use formal verification against the implementation. Similarly [ABSW13] provided the first formal analysis
of the NFC mobile coupon application proposed by [DA07]. The analysis used the Casper tool to translate
the protocols directly into CSP for direct model-checking with FDR, to consider security with respect to the
security requirements of forgery protection and user authentication. The formal analysis identified attacks
against the authentication properties, giving rise to a proposed solution for which the analysis in [ABSW13]
found no further attacks.
    One of the most widely used e-commerce transaction protocols is the secure electronic protocol. The
authors of [XWL14] have modelled a simplified version of the protocol [LS99] in Promela and verified mu-
tual authentication properties using the SPIN model checker. The authors have expressed authentication
properties as LTL formulas and discovered several vulnerabilities. The authors further proposed an improve-
ment to the protocol addressing the vulnerabilities and note the effectiveness of model checking in security
analysis of protocols. Similarly, the authors of [HB12a] have analysed a biometric transaction authentica-
tion protocol [HB12b] providing authentication and non-repudiation of the origin in insecure environments.
The protocol uses a biometric transaction device, providing the biometric data of the user, where the au-
thors have created an idealised model of this device. Furthermore, the authors have modelled the proto-
col in π-calculus [AG99] and verified the security properties of authentication and non-repudiation using
ProVerif [BSCS18]. The analysis uncovered that in case a malware on the client blocks messages from the
server, the user would not know if the transaction was successful. The authors proposed an extension to the
protocol addressing this issue.
    SMS is also often used to facilitate mobile payments. To secure these payments [BS15] have proposed a
secure SMS based protocol. The protocol utilises elliptic curve cryptography providing signatures and encryp-
tion. In order to demonstrate that the protocol is secure the authors have verified it using AVISPA [ABB+ 05],
specifically model checking AVISPA endpoints and BAN logic. The analysis has shown the protocol complies
with properties of confidentiality, message freshness and third party trust while utilising the current SMS
infrastructure.

2.2.4. Implementation

Vulnerabilities in financial software could lead to financial losses or disclosure of sensitive information. Pre-
venting these vulnerabilities at the implementation level is an area where FM could be of substantial benefit.
    The spread of smartphones has allowed for rapid introduction of digital financial services in the devel-
oping countries. The authors of [ISCM17] have considered static code analysis as a tool for assessing the
vulnerabilities of the Android applications used to access the financial services. The authors have selected
seven applications from developing countries and three applications from developed countries. The appli-
cations have been analysed by three static analysis tools, MobSF7 , Quark [KI16] and AndroBugs [Lin15].
Each of the tools could analyse the applications against a predetermined set of vulnerabilities. The analyses
have considered thirteen vulnerabilities and has shown that the applications from developing countries suf-
fer from more vulnerabilities than those from developed countries. The authors recommend development of
static analysis tools aimed specifically at financial applications. Similarly, the authors of [TM17] have used
static analysis on 10400 Android applications in order to determine how security of financial applications
compares to other applications. The authors have collected quarterly snapshots of the Google Play Store for
two years in order to analyse the evolution of security of financial applications by use of the AndroBugs and
MobSF tools. The selected vulnerabilities were based on the top ten OWASP list8 . The results show that the

7   github.com/MobSF/Mobile-Security-Framework-MobSF
8   owasp.org/www-project-mobile-top-10/
12                   T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



financial applications have been gaining more vulnerabilities over time. The authors note this is a worrying
trend and suggest that the developers further employ static and dynamic analysis tools.
    EMV 2, the next generation of EMV, integrates new security schemes, such as biometric security. The
author of [Fre18] has modelled 80% of the EMV 2 specification using VDM in order to determine possible
security issues and provide a formal model for implementation. The size of the model (50 KLOC) has brought
difficulties to the VDM IDE Overture [LBF+ 10]. Furthermore in order to model EMV 2 with a high level
of fidelity the author had to solve several corner cases brought by the VDM SL semantics. The author has
attempted automatic Java code generation, finding that the code generator needs improvements in order to
handle such models, opting instead for manual implementation. The author has created a wish-list of nine
improvements that can improve the modelling and validation experience of VDM tools.
    The financial industry is moving towards the use of open APIs, where third party companies can access
banking data. To this extent, the authors of [FHK19] have created a highly detailed, close to implementation
formal model of the popular OpenID Financial-grade API. The model is based on the Web Infrastructure
Model proposed in [FKS14], where the behaviours are captured as a set of theorems. Within the model the
authors have considered security properties covering the authorisation, authentication and session integrity.
Manual theorem proving has uncovered several vulnerabilities, specifically the ability of an attacker to access
protected resources owned by legitimate actors. The authors have proposed several fixes based on the analysis.
    Bitcoin is a peer to peer cryptographic currency system allowing for mutually distrusting parties to
perform financial transactions. This property of Bitcoin contracts could lead to their wider use. One thing
that makes security assurance hard in this setting is the difficulty in analysing security of these contracts.
The authors of [ADMM14] have modelled and analysed two types of these contracts in UPPAAL against
several security properties. One of the results was the determination of a time limit after which the contract
protocol shall abort in order to remain secure. The authors note that UPPAAL is a suitable tool for analysing
the different types of Bitcoin contracts.

2.2.5. Hardware

The rise of cryptocurrencies and financial technology have led to creation of a specific financial hardware.
While this field is in its infancy, FM have been utilised to improve security of these devices.
    One of the important aspects of technology in finance is the ability to securely approve transactions.
This is invaluable in the field of cryptocurrencies where $1B has been stolen in 2018 alone9 mainly due
to the theft of private keys from users’ computers. The authors of [ABK+ 19] have proposed the NOTARY
hardware device used for approval of security critical operations. The device provides multi-agent capabilities,
allowing for different approval agents. The authors demonstrate this, by implementing a Bitcoin wallet and
a general-purpose approval agent. In order to switch between the agents without potential leak of sensitive
information, the device is based on principles of reset based switching, ensuring that the device always
enters a deterministic start state and provides resiliency against side-channel attacks [KHF+ 19]. The authors
designed the device by continuously verifying the property of a deterministic start by modelling the RTL
description of the device then dispatching the model to a SMT solver. In the case where the SMT solver
found a counterexample the authors tweaked the design to ensure no counterexample is found. The authors
note that while the multi-agent device provides higher security than single-purpose hardware wallets, it is
comparable in retail cost. The hardware wallets are often considered more secure than software wallets. This
is due to the assumption that the hardware device contains low complexity firmware making it less prone to
bugs and vulnerabilities.The authors of [MPS19] asked a question: what if the hardware wallet manufacturer
cannot be trusted? It could be that the manufacturer installs a back-door to the pseudorandom generator.
The authors suggest use of a two-out-of-two signature scheme [DF89] using signatures partially generated
by the hardware wallet and partially known by the user (password). The authors focus on the unforgeability
property, where an adversary corrupting the hardware wallet cannot forge the signature, while considering
a malicious client, a malicious hardware token and selective access to legitimate tokens. The authors verify
the property against their scheme using theorem proving, while suggesting that the scheme allows for use
of untrusted hardware wallets. Also within the area of hardware wallets the authors of [AGKK19] have
attempted to formally prove security properties of several wallets. The authors note that the wallets are
the only means to interact with the cryptocurrency assets and as such, FM shall be used to verify their

9   ciphertrace.com/wp-content/uploads/2018/10/crypto_aml_report_2018q3.pdf
A Survey of Practical Formal Methods for Security                                                             13



security. To do this the authors create a formal model of a hardware wallet in the universal composable
framework [Can01] and identify “all potential attack vectors” and conditions under which the wallet is secure.
Furthermore the authors analyse implementations of three popular hardware wallets by mapping them to
their model and prove theorems about the essential security properties. This has shown that these hardware
wallets are only secure under specific assumptions with an important note that perfect cryptography alone
does not guarantee security.
    Falling costs of hardware such as NFC-enabled mobile phones and off-the-shelf NFC USB readers create
security challenges for contactless card payments. One of the potential attacks is a relay attack where
an attacker relays communication between the card and a terminal to another terminal using commodity
hardware. To mitigate this attack, the authors of [CGDR+ 15] have introduced a time bounding scheme into
the payment process. In order for the attack to be successful the attacker has to relay messages at the speed
of light from any large distance. This is prevented by the proposed scheme, based on a distance bounding
protocol [BMV14]. The authors model their scheme in applied π-calculus and verify it using ProVerif. The
authors note that their scheme offers good protection against attacks using commodity hardware.


2.3. Industrial

Industrial processes are a backbone of a modern society as they provide control not only for production of
necessary goods, but also utilities such as electricity and water treatment. This section provides an overview of
how FM have been utilised in security analysis of automotive control applications, robotic applications, PLC
software, industrial communication protocols such as Modbus and OPC UA, SCADA systems and hardware
devices underpinning industrial computing. An interesting note is that the research works are distributed
uniformly across the different levels of abstraction, demonstrating that all aspects of industrial computing
have been scrutinised using FM in order to provide either security analysis or security assurances. In the
industrial application of FM the problem is often considered domain specific, i.e. cyber security properties
are based on whether the considered industrial system is for example an automotive controller or a water
treatment plan.
    As within the financial section, the most used FM to analyse the security properties is model checking.
This could once again be attributed to the nature of the problem where for example PLC programs and
industrial processes lend themselves to be easily modelled using state transition systems. As some of the
industrial computing is complex, the problems are often modelled more abstractly in order to avoid the state
space explosion problem. Within the hardware level of abstraction however in industrial computing, theorem
proving is often the FM of choice, as it allows description of the hardware in more detail. The cyber security
topics within the industrial section are shown in Figure 4.

2.3.1. Application

Industrial applications often control a critical industrial process, where security assurance provided by FM
could bring massive benefits.
    In the automotive area, the authors of [HSB+ 19] have proposed a model checking approach to security as-
surance of the Electronic Control Units (ECUs) in order to provide secure advanced driver assistance systems.
The authors have proposed a method for automated translation of the ECU applications to CSP [Hoa78]. The
CSP model is then dispatched to the FDR model checker, verified against several cyber-security properties
and potential counter examples are fed back to the ECU application developers. The automated translation
approach was developed for the proprietary programming language CAPL. The approach has indicated large
cost reduction in security assurance, however the authors state the need to extend their work with the notion
of timing.
    Industry 4.0 is a concept bringing interconnectivity and data sharing to production facilities. It is in this
area that the authors of [NT19] have investigated formalisation of the behaviour of industry 4.0 applications
to formally analyse their security. The application that was formalised was controlling a cap attaching robot.
The authors have created a model using Maude [Mes00] and provided two models of an attacker. The first
model is a symbolic intruder capable of injecting messages, while the second model is of a symbolic intruder
capable of tampering with messages. The analysis found four distinct messages an attacker can inject that
would put the system into an undesired state. This has been used to update the security policies, preventing
these attacks. The use of FM for the security of robotic applications was also investigated by [WGS+ 19] in
14                T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock




                           Fig. 4. Cyber security topics in the industrial section


order to enable model based design for robotics. The authors consider applications based on the Robotic
Operating System (ROS) [QCG+ 09]. The first step in the method is the creation of timed automata models
based on the specification of the application and security, safety and liveness properties expressed in CTL.
The UPPAAL model checker [LPY97] is then used to verify the model against the defined properties. The
authors further create a code generator to generate the implementation of the application using the ROS
C++ code.
    SCADA systems consist of several applications, including the SCADA application itself or applications
distributed on PLCs and micro controllers. The authors of [MMS19] have proposed a method based on model
checking for security analysis of water treatment system SCADA logs. The method consists of modelling the
system behaviour using timed automata and expressing the properties based on the logs in timed temporal
logic [ACD90]. The authors express the properties representing the overflow and underflow attacks and
validated their method against predetermined scenarios with 100% attack detection rate based on the log
data. On the PLC component level, attacks are often created as a self-propagating malware. The authors
of [ZRM14] have proposed a method for malware detection by providing a symbolic execution of a PLC scan
cycle and then combining multiple scan cycles into a temporal execution graph. The Z3 SMT solver [dMB08]
is then used as a model checker, verifying security and safety properties related to application genuinity.
The counter-examples generated by the model checker are used for application debugging purposes. The
authors of [KKHE17] consider an application created in the graphical Ladder Logic (LL) PLC programming
language. Due to the graphical nature of LL it is difficult to find intruder code, which could find its way
to the PLC due to the connected nature of modern PLCs. To find the intruder code, the authors model
the application and use the NuSMV model checker [CCGR99] while expressing six possible intrusions as
CTL properties. The verification shows that applications created in LL could be checked automatically for
intrusion code within the PLC application.

2.3.2. System

Industrial systems are often used to control critical infrastructures requiring strong guarantees of security
and safety. Cyber attacks against these systems could have severe consequences [Wei11]. It is possible to
decrease the attack surface of the industrial systems. The authors of [RT17] have used formal design and
analysis to verify security properties of a real world industrial control system. They have created a model
in ASLan++ covering the system database, network, PLC and SCADA logic. Further the attacker was
modelled as a Cyber Physical Dolev-Yao attacker [RT16]. The verification was carried out using the CL-Atse
protocol analyser. As the target was an existing water treatment plant, the author has compared the formal
A Survey of Practical Formal Methods for Security                                                             15



analysis with practical assessment results, finding that the formal analysis discovered seven out of eight
possible attacks, while the last one was not discovered due to the chosen level of abstraction. Due to the
specialised nature of the PLCs, running anti-virus solutions is not possible. In [DRR17] the authors proposed
a framework for malware-tolerant, self-healing control systems. The main idea is to distribute trust to ensure
that a single compromised component does not break the security policy. The authors have added specialised
reset circuits with two out of three voting to determine if a PLC is producing correct results. If the result
is incorrect the system reloads the image to the PLC from network storage. To asses their framework, the
authors have modelled the reset and voting protocol using ProVerif and utilized a Dolev-Yao attacker with
access to different devices and carried out formal analysis to determine if the system remains compliant
with the security policy. The analysis has proven the security aspects of the system. The authors of [HH18]
have considered verification of the PLC network within an industrial control system by creating graphs of
the potentially compromised PLC program and a trusted version of this program. They do this by first
creating a formal model of both programs in UPPAAL, then translating this model into attribut graphs.
The matching comparison of the graphs provides guarantees that the system has not been compromised.
The approach has been demonstrated on a case study of industrial water level control system. Similarly
the authors of [WSC17] have chosen formal methods as an effective technology to avoid errors in security
design of cyber-physical systems. The authors utilised timed automata to model a water treatment system
consisting of multiple layers. The considered layers were the supervision layer, monitoring the controllers,
the real-time control layer, executing the control and a physical layer consisting of a water tank, pump
and necessary sensors. This was carried out as different layers are prone to different attacks. The authors
further modelled recovery mechanisms for different attacks and the attacker. The system was then analysed
against several cyber security properties using the PAT model checker [SLD08], showing that the recovery
mechanisms can bring the system under control if the attack frequency is lower than a detection frequency
of the recovery mechanism. The authors further plan to apply their method to more complex systems.
    Since modern industrial control systems connect to multiple networks such as the PLC control network,
enterprise network and even the Internet, firewall configuration is an important area of system security assur-
ance. The authors of [RRS13] have demonstrated formalisation of firewall rules to rule tuples representing
the actions firewall should take in communication. Further, these rules and policies have been translated
into logical formulas that were verified using the Z3 SMT solver. The authors note that the formal analysis
has high potential to improve the error-prone process of firewall configuration. As control systems become
more interconnected, connectivity towards cloud systems is often considered. In [KTJB19], the authors have
verified several proposed mitigation strategies against attacks on cloud connected industrial control systems
such as attacks where a remote client tries to push a malicious firmware update or execute brute force attack
against the login system. A system architecture consisting of the control system, remote clients and a cloud
intermediary was modelled in PlusCal [Lam09] and TLA+ [Lam02], while the properties have been expressed
using LTL. The verification has shown the effectiveness of the mitigation strategies. Since the cloud con-
nected architectures grow in complexity, using model checking is often difficult as verification at high level of
detail leads to state space explosion. The authors of [TJKBL19] analysed several cyber security properties of
a cloud connected industrial control system corresponding to validity of system access tokens and firmware
update files using combinatorial testing in conjunction with formal modelling. The model was created using
VDM-SL [LHB+ 96, FL09] and properties expressed as a set of invariants, pre and post-conditions. Using
the combinatorial testing feature of VDMJ [LLB10], the authors have generated 145 million tests, with a
practical execution time of less than 20 hours.

2.3.3. Protocols

Industrial communication protocols often carry critical data and commands, hence require a high level of
security. One of these protocols is Modbus/TCP. The authors of [SPSK17] have formally investigated the
security aspects of the Modbus/TCP using Coloured Petri Nets (CPN) [JK09] in conjunction with Formal
Component Analysis (FCA) [Pri06]. The authors have created a formal model of the client, server and an
attacker, where the attacker has the capability to tamper with the messages using an iterative approach,
where they first create a CPN block diagram of the protocol. Based on the block diagram the authors create
an initial model used to validate the protocol functionality without any threats present. Finally, the authors
add the attacker model and carry out several protocol runs with normal and malicious behaviours. Data
collected from these runs were used in an FCA with the ConExp tool [JRVP08]. The authors discovered a
possible attack and implemented it against a test bed to demonstrate the viability of the approach. Similarly,
16                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



in [NRM16] the authors have focused on the security of the Modbus protocol by modeling several aspects
of the protocol as a Dynamic State Machine [NGP+ 15], which was then automatically translated [NGB+ 16]
to Promela for verification using the SPIN model checker. The authors have expressed the impossibility
of a man-in-the-middle attack and data tampering as an LTL property. The verification showed that this
property is broken and the authors investigated the counter-examples provided by the model checker. The
authors note that compaction of counter-examples would simplify their analysis.
    OPC UA is another widespread industrial protocol. The authors of [PPL16] have formally analysed the
sub-protocols of the OPC UA responsible for authentication and secrecy. The authors have modelled both
sub-protocols in ProVerif and analysed them against the Dolev-Yao intruder model. The authentication sub-
protocol has been shown to contain a vulnerability since even in the sign and encrypt mode, the message
does not contain explicit identity of the receiver. The authors have proposed a fix by adding the public key
of the receiver to the message and rerun their analysis without any security violations. The secrecy sub-
protocol has only been proven secure if credential encryption is used, however authors note that this is not
the case for all implementations of OPC UA. The authors of [DPP+ 17] provide a formal definition of flow
integrity, ensuring security by preserving a flow order of messages. The authors express the OPC-UA and
Modbus protocols as a set of theorems and define nine authenticity and integrity properties expressed as trace
formulas within the TAMARIN theorem prover [MSCB13]. The authors demonstrate that the flow integrity
can only be satisfied if the channels are assumed secure, i.e. the attacker cannot simply delete all messages
and also note a weakness within the secure version of the Modbus protocol due to the insufficient use of
cryptography. The DNP3 protocol is used to facilitate communication within the electrical grid. In [ACF16]
the authors have formally analysed the authentication properties of the secure authentication for the DNP3
protocol, the DNP3-SA. The authors have used CPN and security properties expressed in CTL within the
CPN state space analysis tool [JKW07] to verify that the system against several cyber attacks. The authors
have uncovered a flaw in one of the protocol modes, allowing for successful replay attack and proposed two
potential fixes. The fixes were then verified using CPN and have demonstrated the capability of withstanding
the attack. The authors note that the benefits of verification outweigh the time spent on modelling.
    CAN is a broadcast, real-time protocol used in modern vehicles. The authors of [BSNRN14] have analysed
MaCAN, an authenticated CAN protocol, using ProVerif, discovering a flaw in session initiation key exchange
and a possibility of replay attack with partially modified data due to limited use of cryptography. The authors
have proposed improvements limiting the impact of discovered flaws, noting that their security solution is
applicable within the bandwidth limitations of the CAN network.

2.3.4. Implementation

Due to the critical nature of some of the industrial control systems, formal verification has been used to
verify the security properties of their underlying implementations. One of the major obstacles to formal
verification of an implementation is often the size of the source code.
    The authors of [ALR16] propose a method using SysML-Sec, a modelling system based on UML, for
working with large code bases. The authors suggest creating models in SysML and iteratively refining be-
haviour of the model by adding more behavioural and security properties using SysML-Sec. The model can
be automatically translated to π-calculus by use of the TTool [EAP14] and formally analysed by ProVerif.
In case that the refinement leads to a behaviour with a level of detail that cannot be practically formally
verified the authors suggest usage of model to code transformations to perform security and safety code
analysis. The authors note that their approach can lead to integration of formal verification into a software
design and development process.
    In the aeronautics industry, a successful cyber attack could lead to loss of life. The authors of [CGB+ 18]
have created an implementation for unmanned air vehicle verified by FM. The focus was set on four as-
sumptions, 1. the architecture is correct, 2. the components are correct, 3. the system execution semantics
matches the model and 4. the system implementation corresponds to the model. To satisfy 1, the authors
have developed a model using the Architecture Analysis and Design Language (AADL) to capture the im-
portant behavioural contracts and verified them using the jKind model checker [GBW+ 17]. To satisfy 2,
the authors have created a domain specific language Ivory following the principles of memory safety and
avoiding undefined behaviour. To satisfy 3, the authors have used the seL4 microkernel, which was verified
using the Isabelle/HOL theorem prover [NK14]. Finally to satisfy 4, the authors have created a tool that
generates system images from the AADL models. Once the implementation has concluded, the attempts to
attack the vehicle by a separate team were unsuccessful.
A Survey of Practical Formal Methods for Security                                                             17



    Software present on PLCs directly impacts the control process. In [SMX18], the authors propose a method
for formal security verification of PLC control programs. The authors create state transition diagrams based
on the control program and define the desired control loop security properties. The state diagrams are
then manually translated to formal specification for the NuSMV model checker and the security properties
are expressed in LTL. The authors have demonstrated their approach on a simple temperature control
module design and express the need for automated translation of the PLC program specification to a formal
specification in order to bring model checking to technicians for simple module design. The authors of [TSS16]
have considered the nature of PLC programs and their affinity to Petri Nets. The authors consider falsified
software being loaded onto the PLC and present a method using Petri Net modelling followed by Kalman
Decomposition (KD) to determine the properties of falsification. The authors then demonstrate automatic
detection of falsification using the SPIN model checker, where the Petri Net was translated to Promela
specification and falsification properties were expressed using LTL.

2.3.5. Hardware

FM for hardware verification is well established, with numerous tools and domain-specific description lan-
guages, e.g., Verilog and VHDL regularly used in industry. Hardware specifications and the safety properties
they must satisfy translate naturally to satisfiability problems, which is the type of problem that is amenable
to automation. Is this also true for security properties? This section considers this question in the context
of industrial hardware.
    The authors of [HRG+ 18] study co-verification of Intellectual Property Blocks (IPs) within System on
Chip (SoC) architectures. Each IP comprises firmware accessing hardware through a memory-mapped in-
put/output interface. The authors assume that an attacker can spoof commands, but that the attacker
has no physical access to internal registers etc, i.e., the attacker can only attack the system through the
communication interface. Multiple security considerations were taken in to account including secure boot
(all components of the firmware image must be authenticated), concurrency (in particular time-of-check-to-
time-of-use considerations [BDSS08]), and integrity and confidentiality of on-device firmware.
    The main challenges encountered are the scalability of reasoning via suitable abstractions, the inherent
concurrency of the systems, and extension of standard techniques to cover bit-precise reasoning (e.g., to
handle shifting and masking, which is used to access hardware states stored in aligned hardware registers).
Moreover, standard model checking tools (e.g., CBMC) could not be used since such tools do not naturally
capture the behaviour of hardware. Their solution is a semi-automatic co-verification methodology that
proceeds via instruction level abstraction, which is combined with a toolchain comprising of Boogie [BCD+ 05]
(an intermediate verification language) to Corral software verifier [LQL12] together with SMACK [RE14] to
support bit-precise checking.
    The authors of [LFBP14] consider hardware security verification for Industrial Control Systems (ICS),
e.g., as present in factories. They cover a threat model that assumes all software layers can be compromised
and are capable of attacking the system while keeping the attacks hidden from human operators. The aim
is to develop an application-specific hardware monitor, TECEP (Trust Enhancement of Critical Embedded
Processes), that acts as the final authority. TECEP includes two trusted components: an FPGA-based
hardware monitor (synthesised from formally analysed C code) and a junction box that is validated in a
hardware description language. The monitor’s job is to test whether the outputs (of the physical plant,
plant model and prediction unit) are compatible (with respect to predetermined tolerances). If not, a backup
controller is used to override the production controller. Their framework models the hardware monitor in
Frama-C [CKK+ 12] with the Jessie plugin to enable automatic deductive verification via Why [FM07].
    There are several works on the formal verification of security of integrated circuits. The authors of [LJM11]
consider the trustworthiness of hardware using the proof carrying code (PCC) [Nec11]. The authors extend the
semantic model of permissible Verilog at the, so-called, register-transfer level, then derive Coq definitions
and theorems for the hardware descriptions extended with PCC annotations. More recently, the authors
of [GDMJ16a] develop a notion called proof carrying hardware, which is used to verify security properties
of IP cores that may be supplied by untrusted vendors. Their techniques extend VHDL and is built on
top of Gallina (the functional programming language of Coq). Their tool supports translation of informal
security specifications into Coq and their case study examines a proof of correctness of AES encryption core.
In [ALKH17], the authors consider the introduction of hardware trojans within Integrated Circuits (ICs)
during manufacturing. To this end they use the nuXmv model checker with hardware properties specified
18                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock




                            Fig. 5. Cyber security topics in the consumer section


using LTL reduced to behavioural traces indicating attack paths potentially exposing side channels in the
analysis.


2.4. Consumer

Consumer computing such as use of personal computer, smartphones and underlying connected services is
an integral part of modern life. Consumer computing has been often characterised as of less critical nature
than for example industrial systems, however this view is changing as the society introduces more digital
technologies to everyday life. This section provides an overview of use of FM in analysis of cyber security
of consumer computing, ranging from consumer electronics for fitness equipment, mobile operating systems,
web browsers, consumer Internet of Things (IoT) devices to commodity hardware for devices such as personal
electricity meters. An interesting fact within the consumer domain is significant use of so called lightweight
FM, utilised often not only on the application level of abstraction, but also considering implementation
and hardware. One challenge in formal analysis of consumer systems is a rapid nature of evolution of these
systems, where the competition in consumer markets often forces fast adoption of new technologies.
    Once again the most utilised FM is model checking. It could be argued that this is due to the significant
model checking experience gained in other domains. Many consumer computing entities are however complex,
interconnected chains of services, which could explain wider utilisation of lightweight FM, especially as some
of these are used directly to build chains used to construct the consumer computing entities. It should also
however be stated that theorem proving has also been utilised on all the different levels of abstraction within
the consumer computing domain. The cyber security topics present within the consumer section are shown
in Figure 5.

2.4.1. Application

Sound infrastructure for security applications is an enabling technology for secure consumer electronics. For
example, Peloton is an American exercise equipment and media company, launched with Kickstarter funding
in 2013. They produce consumer electronics for personal fitness, particularly exercise bikes. They couple the
physical equipment with live exercise classes held in New York and they have a large library of past exercise
classes. All this brings significant challenges, such as handling latency problems operating at such a large
scale. They are particularly concerned about upgrade rollouts affecting different versions of their equipment.
A Survey of Practical Formal Methods for Security                                                            19



Their business model requires that this whole operation is secure. To achieve this, their infrastructure is
based on Amazon Web Services (AWS), with its guarantees of security and scalability10 .
    FM thrives in checking consumer applications for malware. A practical definition of malware (one that
can be used to classify executable files) intersects the perspective shift FM advocate: focus on “what” is
computed instead of the “how”. Quoting [KB10]: “any (formal) definition of the concept of malware depends
on the definition of the concept of software system correctness”. Also, a majority of malware is the product
of tools generating variants of known vulnerabilities/attacks or known malware. The authors of [CMN+ 18]
show variants are easy to hide syntactically, but not semantically.
    Model checking based approaches provide malicious behaviour semantic signatures by providing coun-
terexamples. Recent approaches as in [ST12, ST14b] extract push-down automata as models. A promising
area is the application of the techniques to the realm of the Android operating system [ST14a]. The suc-
cessful recipe is to choose a mathematical model of the executables and a logical formalism to describe the
malicious behaviours in terms of the semantics of the program.
    There are a few works where theorem proving is applied in malware [SC16], but the number of publications
is small, and it is difficult to ascertain if there is an effective gain from it. Perhaps model checking is more
appropriate to the domain due to its non-interactive nature since malware is inherently a game between
attackers and an algorithm.
    Although successful, the FM techniques provide no panacea to consumer malware protection. The mal-
ware game advances with discovery of zero-day (latent) vulnerabilities. FM have been argued to avoid these
vulnerabilities in the first place [MAH15], but practically, new malicious behaviours are expected to appear,
thus the problem becomes to learn malicious behaviours. There have been several successful proofs of concept
where FM leverage the signature learning either in terms of or using push-down automata reachability in
the process [MT13, DT17, DT18].
    Beyond detection, alternative approaches work to prevent attacks and malware to reach consumer systems
in the first place. For instance, the adoption of the software marketplace paradigm reduces trivial attacks
based on luring end-users to inadvertently install malware or on gross software implementation malpractice.
FM backed approaches are also being applied in the field of marketplace vetting and attack mitigation
[MNSV16]. In addition, automated checks to user settings enforcing security policies and reducing the attack
surface are already in place. This is a field with a lot of potential for FM approaches [BSGM15].

2.4.2. System

As consumer digital systems become more prevalent, formal verification has potential to provide the neces-
sary security assurances. Android is one of the most popular OSs in the world. Android enforces permissions
at the application level, allowing applications to combine their privileges, which could potentially lead to a
privilege escalation [DDSW11]. The authors of [BSGM15] propose a tool-based approach, called COVERT,
for compositional analysis of Android inter-app permission leakage. COVERT assesses the security of a sys-
tem as a whole by inferring the security properties of the individual applications. The tool uses a model
extractor, generating Alloy specifications [Jac12], capturing the security properties of the applications. The
Alloy analyser is then used to verify these properties against a manually created model of a specific Android
framework. The authors have analysed more than 500 real world applications and have confirmed the findings
previously found within [FCH+ 11, AZHL12], showing that many Android applications are over-privileged.
The authors of [BKMJ18] have moved towards analysing the permission protocol itself, leading to identi-
fication of design flaws. The authors have specified the permission protocol in Alloy and, among others,
the analysis has discovered a previously theorised design flaw where two applications can apply the same
custom permission, leading to the application which was installed first being able to access the resources of
the application installed second. The authors have also discovered that many popular Android applications
contain this vulnerability.
    Operating systems usually contain an underlying security model. In [DKK+ 14] the authors have verified
an proposed access and integrity control for a Linux-like OS. The authors have formalised the security model
in Alloy and Event-B [Abr10], where the Alloy analyser was used to provide constraint based checking of
operation contracts within the security model. While the authors have experienced scalability issues with
Alloy, the analysis have uncovered bugs that could become more serious if discovered in the implementation

10   aws.amazon.com/solutions/case-studies/Peloton/
20                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



phase. The authors of [MPX+ 13] present the ExpressOS, a secure OS alternative to Android. The aim of
this OS is to provide formally verified mechanisms used to enforce the security policies. This is achieved by
expressing invariants representing security properties of the OS and annotating the source code of the OS
with formal specification, mainly using code contracts. These abstractions are then discharged for verification
using automated theorem provers. The authors note that the approach is feasible for verification of security
invariants with only 2.8% source code annotation overhead.
    Consumer expectations on the digital technology led to the rise of a smart home, an ecosystem of small
connected devices, often remotely controllable, bringing security vulnerabilities. The authors of [KBG+ 17]
have proposed Anonymous Secure Framework (ASF), a framework for ensuring anonymity, authentication
and integrity in smart home environments. The authors have verified their framework for its security strength
and anonymity using the model checking tools within AVISPA and by BAN logic. The ASF demonstrated
resilience against several well-known attacks against smart home environments and demonstrated suitability
of their framework for next-generation secure smart-home environments. In [MSHA17] the authors have
developed the IoTRiskAnalyzer tool used to help the IoT engineers apply the most fitting security policies
for their IoT environment. This has been achieved using a Markov Decision Process [Put94], formalisation of
risk properties as probabilistic CTL formulas and verification using the PRISM model checker [KNP11]. Car
manufacturers are also taking advantage of connected devices, especially smartphones. Finally, the authors
of [BTW+ 13] have developed a smartphone based immobiliser with formally verified protocol and hardware
fulfilling specific security assumptions. The protocol has been verified using ProVerif against a Dolev-Yao
attacker model to ensure strong guarantees of security requirements.

2.4.3. Protocols

The area of consumer communication protocols covers text and multimedia communication lending itself to
formal verification of security.
    In [CCD+ 17] the authors have created a formal model of the Signal protocol in terms of predicates and
theorems and have applied theorem proving, resulting in improvements in the use of the protocol’s random
generator.
    Security of the consumer communication systems often depends on the mechanisms introduced in the
Needham-Schroeder [NS78] authentication protocol and the Denning Sacco protocol [DS81] for secret key
distribution. The authors of [CFM16] have created a simplified model of the Needham-Schroeder NPSK
protocol and the Denning Sacco protocol and expressed security properties using LTL. The authors have
provided an efficient model for model checking of the security properties using the Spin model checker.

2.4.4. Implementation

The recent adoption of FM tools by large technology companies has shaken up the field. If in the past FM
were tied to niche safety critical domains (e.g., aerospace, railway, medical), “big government regulation”,
the current panorama shows that the future brings the usage of FM tools in the daily practice of soft-
ware engineering. No matter the intention behind the usage of FM tools, the outcome has demonstrated a
contribution to increasingly secure implementations.
    According to recent reports, when a developer commits a code modification to one of the large technology
companies’ codebases, a static analysis tool is invoked and a code review is provided. The author of [OH18]
describes the process as continuous reasoning, and any change to a Facebook product is analysed by the
Infer static analysis tool, which checks “small theorems” on large codebases. This approach has been shown
to improve the security of the company’s own codebase and library implementations (e.g., OpenSSL). The
same is reported about the software engineering practice inside Google [SAE+ 18], although it is not clear
whether FM is used by Project Zero, its elite security team. However, the authors of [BBC+ 19b] report on
how numerous security vulnerabilities were fixed by applying FUDGE, a static analysis tool based on fuzzing
developed in house.
    Particularly targeted to the security domain, the authors of [DFLO19] report a static analysis tool,
Zoncolan, in collaboration with the Facebook App Security team. Zoncolan uses abstract interpretation to
analyse and issue security alerts for the implementations of the applications in the company’s codebase:
Messenger, WhatsApp, Instagram, or Facebook. This level of application of FM shows the implementations
of software used by millions of consumers has been swept by a FM tool.
    FM is also being applied to secure implementations of web browsers, which are designed with security
A Survey of Practical Formal Methods for Security                                                                     21



in mind because they mediate a vast amount of personal information (e.g., credentials, banking details).
Nevertheless, due to a large attack surface of a web browser, attacks are possible, and implementation flaws
are not uncommon. In a bolder move, the authors of [JTL12a] propose a new browser, QUARK, that follows
the “kernel architecture”11 of modern browsers, but QUARK’s kernel is formally verified. The formal verifi-
cation yields to the Coq theorems to assert properties as tab non-interference, or cookie confidentiality and
integrity. According to work in [FLR17], the price to pay for such a prime example of functional correctness
verification (above airline runtime error-free level) is 25% increase in overhead, affecting performance.
    Increasing browsers’ security risks, users demand and make use of various browser extensions. Browser
extensions are developed using web technologies, but, when compared with a traditional web page, have access
to more APIs and features therefore extensions can spy and exploit users as demonstrated in [GFLS11]. In
the same vein, but beyond verifying extensions, the authors of [MTT+ 12] show that x86 native code executed
by arbitrary clients conforms with a predefined sandbox policy when using Google Chrome’s Native Client
service.
    To complete the coverage of research on browsers developed using FM, we must mention the case of
the Illinois browser operating system. In [SKMT12] the authors report a verified design of an experimental
browser and operating system reducing the size of the trusted code base to 42K lines. The work provides
proven routing guarantees and anti-spoofing of the address bar URL relying on the Maude tool and rewriting
logic to achieve this.

2.4.5. Hardware
In contrast to critical-system hardware (e.g., fly-by-wire hardware) attackers cannot be prevented from
physical access to the consumer hardware, which provides a large attack surface.
    Modern consumer hardware provides hardware-level protections for critical software components. An
example of this is ARM TrustZone [NMB+ 16] providing separation between trusted and rich software pro-
viding potentially untrusted interfaces. The authors of [FXZ+ 17] propose verification of hardware security
properties by use of information flow control at the level of the Hardware Description Language (HDL) such
as SecVeriLog [ZWSM15]. The authors create SecVeriLogBL, an extension to SecVeriLog, by adding new
types for security labels defined in SecVeriLog. This allows for static analysis at the design time, providing
a lightweight verification with small effects on the hardware performance. To demonstrate this approach,
the authors have designed an implementation of TrustZone, including 10+ security bugs. The analysis has
detected most of these bugs with exception of bugs that required type lowering, i.e., downgrading, to be
expressed. The authors note that vulnerabilities that are not affected by downgrading are always detected.
Similarly the authors of [LCH+ 16] present a formally defined hardware security enforcement for x86 architec-
ture. In this setting, the software relies on underlying hardware for security enforcement, for example memory
paging features of an x86 CPU. The authors note that incorrect implementations of hardware enforcement
policies often lead to vulnerabilities [KCKB14]. In order to avoid this, a formal framework SpecCert is intro-
duced to model the hardware architecture and then specify the software security requirements to be satisfied
by the trusted software components that implement the hardware security enforcement mechanisms. The
authors then use the framework to prove that the hardware provides the security assurances provided by
the security policy. The authors use Coq to model the architecture and the Coq theorem prover to prove
the soundness of the security policy. As an example they verify security policies regarding code execution
isolation against an abstract minimal model of an x86 architecture. The authors note that in the future they
plan to extend the proofs to physical hardware platform.
    In the area of commodity hardware the authors of [TP16] have used model checking to determine possible
attacks on smart meters, which are considered critical devices [KHLF10]. The authors have created a model
of the smart meter using rewriting logic, formal definition of the attacker’s actions and used the Maude tool
to check that the attacker’s actions are not able to break the security invariants. The discovered attacks were
then mapped to an implementation of a smart meter, the SEGMeter, to investigate the practicality of these
attacks. The authors determined that many attacks discovered by the model checker are indeed practical,
despite the model being abstract and not specifically refined towards the SEGMeter implementation.
    Today, hardware is often packaged as an SoC. In [GDMJ16b] the authors proposed a method for combining
integrated theorem proving and model checking in order to verify security properties of complex SoCs. Due

11  Termed multi-process architecture in Google Chrome with sandboxing of untrusted code which accesses resources through
a trusted broker.
22                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



to the hierarchical nature of SoCs the authors propose that the design expressed in HDL is decomposed into
sub-modules and security specifications into sub-specifications. The sub-specifications are then verified using
the Cadence IFV model checker [Cad20]. These verified sub-specifications are then used as proven lemmas
in the Coq theorem prover [Tea19], removing the need to prove these lemmas by hand. This simplifies the
model checking as well by providing only a small specification to the model checker, avoiding the state
space explosion. The authors present their approach on a case study of a 32-bit CPU and note that their
method provides significant reduction in the amount of effort compared to manual theorem proving. The
authors extend their method by automated code conversion from HDL to verifiable specification [GDMJ17].
SoC complexity increases in Multi Processor SoCs (MPSoC), where multiple processors exchange data via
Network on a Chip (NoC) routers. The authors of [SAS+ 18] have used unbounded model checking to verify
security properties of an NoC, which was practical due to the highly sequential behaviour of NoCs. The
authors formalise the security and functionality correctness properties using LTL and use the CIP unbounded
model checker [KLSB11] to verify them. As a proof of concept, the authors have analysed six different router
implementations, determining the feasibility of their approach for NoC security analysis in early design
stages.


2.5. Enterprise

Enterprise and large corporate computing is the backbone of large international business. In recent years,
there is a trend in enterprise computing to utilise cloud solutions, while still often operating on premises
data centers. These data centers and cloud clusters are utilised for a plethora of enterprise tasks such as
virtualisation of collaboration platforms, company management and hosting of corporate web portals. This
section provides an overview of utilisation of FM to address security challenges of enterprise computing,
ranging from secure data storage through virtualisation and software-defined networking security to strong
authentication using hardware tokens. As enterprises are larger entities changes are often slower and need
to be well managed. To this end, the FM have been utilised as a booster in cloud adoption by enterprises as
several FM-based solutions have been proposed to enable enterprises secure switch from on premises data
centers to federated cloud solutions.
    Similarly to previous sections, model checking is the most used tool in formal analysis of security in
enterprise computing. Theorem proving is however not far behind especially within analysis of hardware such
as Trusted Platform Module chips within enterprise servers. Lightweight FM have also been significantly
utilised on the implementation level of abstraction, since they are often provided as plugins to software
development environments, making them easily accessible. The cyber security topics present within the
enterprise section are shown in Figure 6.

2.5.1. Application

Enterprise applications often process and store data critical for an organisation. The data between these
applications is often carried by networks defined in software, known as Software-Defined Networking (SDN).
The authors of [SLBK14] have created a verification platform for SDN-enabled applications, i.e., applica-
tions capable of adjusting their network performance via APIs. The proposed verification platform Verificare
provides a modelling language VML, for composition of the application with the SDN. The tool translates
the VML models to a LTS that is understood by the PRISM, Spin and Alloy model checkers. The counterex-
amples generated by the model checkers are translated back to statements about the VML model. The tool
can use security requirements from a variety of formal libraries. The authors note that Verificare can handle
complexities above those that a single tool could. Like SDN, Service-Oriented Architectures (SOAs) are be-
coming a standard in deployment of enterprise applications. In SOA, applications are seen as interconnected
services, increasing the deployment complexity. In [AAA+ 12], the authors have created the AVANTSSAR
platform for automated validation of security in SOAs, which provides a formal specification language ASLan
and is proposed as a successor of the AVISPA tool. The platform dispatches the models to CL-Atse, OFMC
and SATMC tools and model checkers while providing the properties as LTL formulas. The authors have
applied the platform to a large number of industrial case studies and discovered several security issues and
vulnerabilities, most notably an issue with SAML SSO integration with Google Apps.
    Relational databases are often used as a data storage for enterprise applications. In recent years, it has
become popular to deploy these databases to untrusted clouds. The authors of [CLW+ 14] have proposed
A Survey of Practical Formal Methods for Security                                                              23




                              Fig. 6. Cyber security topics in the enterprise section


a construction based on cryptography for secure outsourcing of databases to untrusted servers. While the
notion of Verifiable Databases was coined in [BGV11], the authors expand on it by providing an efficiency
improvement based on a notion of incremental updates. Furthermore, the authors introduce an accountability
property, expressing the ability of the server to tamper with the database. In order to demonstrate that the
proposed construction is secure, the authors use theorem proving, providing proofs for several security and
correctness properties. The authors note that their construction does not support all of the update operations.
    In order to rationalise the use of resources, enterprise applications are often deployed using virtualisation.
The virtualisation is controlled by hypervisors, applications providing virtual hardware and orchestration.
Similarly, the authors of [SLZ13] propose a formal analysis scheme for security of a Xen hypervisor called
UVHM. The authors introduce a known bug, previously reported to the Xen team and using their scheme
(re)discover this vulnerability. The scheme consists of four steps, combining static analysis and model check-
ing.
    The work within [Coo18], provides an interesting overview of how a leading cloud provider uses several
FM tools for security assurance, many of which are used on the application level. As the adoption of cloud
computing increases, the author notes the benefits, such as privacy protection, that the formal security
analysis brings to the customer.

2.5.2. System

As enterprise computing systems are of a significant importance to modern life, formal verification could
enable secure enterprise computing minimising financial and safety risks.
    Rather than developing their own infrastructure, companies often choose to host their systems using
third-party cloud platforms. Sometimes however, there are instances where companies prefer to keep part of
the data in their private datacenters, creating federated cloud systems [MML12]. The authors of [ZKWG16]
have proposed an approach for analysing the dynamic behaviour of federated clouds. This was done by
creation of formal models describing the security of information flow within federated clouds. The authors
have used CPN to model the behaviour and carried out the formal analysis using CPN Tools [JKW07]. The
authors have created different models for federated cloud security verification and stress the ability to use
existing tools. Some of the benefits of using a public cloud for enterprise computing are high performance
and scalability. The scaling is often carried out via live migration of virtual machines between different
hosts to balance the load. This operation however also needs to guarantee consistency of security policy
post migration. Similarly the authors of [WZM12] have proposed a formal security assurance framework
combining formal verification with security functional testing. The framework provides assurance by formal
24                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



analysis of a security model and then utilises functional testing against this model once the system is
implemented. In the first phase the security requirements are formalised in Z and the Z/EVES theorem
prover is utilised to carry out the formal analysis. In the second phase, the authors automatically generate
functional tests based on their formal security model. To assess their framework the authors apply it to
a case study of an enterprise data exchange system, analysing properties of confidentiality and integrity.
The authors further compare their test generation scheme to domain theory based [BCB01] test generation
and random test generation. The authors conclude that the case study has demonstrated feasibility and
efficiency of their framework, when compared to other functional test generation methods and plan on
utilising their framework to assess security of more advanced systems such as Z specified role based access
control. In [JED+ 12] the authors have created Cloud Calculus, a formal approach for expression of firewall
security rules and cloud topology. The approach is build on top of the Mobile Ambients [CG00] and the
non-interfering Boxed Ambients calculus [BCMS05]. The authors demonstrate security policy verification by
a test of equivalence relations. Furthermore, the authors apply their approach to a case study inspired by
Amazon Cloud. The authors express a desire to extend their system to take into account intrusion detection
and secure tunnelling. Another benefit of a public cloud is the cost of operation enabled by resource sharing
among multiple tenants. This could lead to Virtual Network (VN) isolation failures where non authorised
tenants could obtain secret information. Furthermore, the authors of [MJA+ 18] created an offline framework
capable of auditing the cloud infrastructure management system, detecting VN isolation failures. The authors
have expressed security properties based on cyber security standards and created a model of multi layered
VNs within a cloud system. This was done by expressing the model in first order logic, formally expressing
11 VN isolation properties and with use of data from an actual system verifying the model against the
properties. The verification was carried out using the constraint satisfaction solver Sugar [TTB08]. The
authors have further integrated their auditing system to the OpenStack cloud infrastructure management
system and note that their solution is the only one that works among multiple cloud layers. The large
amount of subcomponents that the clouds consist of leads to significant complexity. In order to manage this
complexity, the cloud often uses agent systems [GGS10], where software agents are used from implementation
of intelligence within the cloud system. To this end the authors of [MLHK14] propose a security framework
for agent based cloud systems consisting of three steps. First the authors model the NIST [BML+ 11] cloud
reference architecture using the agent paradigm, then the authors enrich this model with security concepts
for cloud computing in Z and finally the authors analyse the architecture against the security concepts using
the Z/EVES theorem prover. The authors have so far considered three agents, the consumer, the cloud broker
and the provider and included considerations for communication between these agents. Within their work
the authors focus on analysing the property of isolation, i.e. ensuring that the data is not communicated to
unauthorised agents. The authors conclude that their framework can feasibly improve security of agent based
cloud systems and plan to extend it to consider more security properties. Similarly the authors of [SBL18]
propose a broker solution, where the broker finds a cloud provider satisfying security requirements defined by
customers. The security requirements are defined using first order relational logic [Jac00] and the broker then
analyses the requirements while matching it against the offers from different cloud providers. This is based
on customers specifying the functional requirements, such as OS, memory, etc. and security requirements in
terms of relations between virtual machines and cloud clusters. The analyses of these relations against the
cloud offers is carried out using KODKOD finite model finder [TJ07]. The authors currently focus on security
challenges related to virtualisation and state that currently the approach is viable for smaller deployments.

   Virtualisation is a key technology in cloud computing allowing the enterprise users to save costs on deploy-
ment. One of the downsides of virtualisation is the large attack surface it presents. The authors of [HLC+ 13]
have proposed vTRUST, a formal framework for verification of trust and security of virtualised systems. The
framework is used to compose a hardware model together with model of an adversary, which then combined
with the software model is verified against these properties that stem from service requirements. The models
are expressed in CSP# [SLDC09], an extension of CSP and verified using the PAT model checker. The
authors have used their framework to analyse a real world cloud system, where they discovered a subtle
but critical bug and proposed a fix. Similarly, in [BVGM15] the authors have proposed a security system,
Weatherman, analysing changes in virtualised infrastructures with respect to security policies. The author
achieve that by formalising the cloud management operations by use of graphs and graph transformations.
Graphs representing the information flow are dispatched to GROOVE model checker [GdR+ 10] for analysis
against security policy properties. The authors note the graph based method provides an intuitive way of
formalising cloud management operations, information flow and security policies.
A Survey of Practical Formal Methods for Security                                                            25



2.5.3. Protocols
Enterprise computing has been moving towards the cloud. The move brought a need for secure infrastructure,
identity and access management, improved connectivity (5G mobile networks), and new communication
protocols. As shown in this section, FM have been widely applied in securing the protocols involved in the
delivery of cloud services.
    Amazon, the large cloud service provider, has used FM in security analysis of the Transport Layer
Security (TLS) protocol. Amazon cloud services such as the AWS and Amazon S3 [Ama19a] use an open
source version of TLS, the s2n [Ama19b]. In order to provide the enterprise customers with the high level
of security assurance, Amazon has employed FM to prove the correctness of the s2n protocol. The s2n/TLS
protocol uses the Hashed based Message Authentication Code (HMAC) to handle authentication of a message
given a shared secret key to ensure that modifications to data in transit can be detected. In [CCC+ 18] the
authors prove that HMAC is indistinguishable from a random generator given that the key is not known.
The authors describe HMAC in the Cryptol specification language [EM09] and use the Coq theorem prover
to carry out the verification. The results of the verification are then connected to the implementation using
the Software Analysis Workbench [Gal19]. Similar proofs have been also made for other parts of the s2n
protocol. It is important to note that the formal verification process at Amazon is applied continuously for
components under constant development such as the s2n protocol.
    Continuing in the domain of cloud, but with a focus on defining networks, the authors of [JBOK14] have
created SecGuru, a tool for automated analysis and debugging of connectivity protocols. The authors created
the tool in order to help with the error-prone task of maintaining the network policy for large data centers.
This is carried out by expressing the connectivity policies as logical formulas and using the Z3 SMT solver.
SecGuru is used by Microsoft to continuously check the integrity of hundreds of firewalls and routers within
the Azure platform. The tool supports two modes of operation, 1) contract validation, where a network
traffic pattern is accepted or rejected by a policy and 2) change impact, where the tool is used to compute
a semantic difference between two network policies, determining an impact of a policy change. The authors
note that SecGuru is an important security component of the Azure platform.
    Regarding new protocols, the work of [Kum14] exemplifies how the application of FM tools, in the
particular case the Alloy analyser, is able to identify vulnerabilities in SAML, one of the modern identity
and access management protocols. SAML, which stands for Security Assertion Markup Language, enables
different cloud providers to provide a single sign-on service. Similar to OAuth and OpenID, the protocol
emerged as a web-based workflow and pose challenges to traditional analyses. The authors extend BAN logic
to cover this, and were able to devise an attack on SAML ID linking.
    Data centers and cloud systems are being increasingly used by enterprises to process data from small
IoT devices with limited capabilities [MW08]. In order to secure IoT device connectivity with the cloud,
the authors of [KS15] have proposed a mutual authentication protocol based on a lightweight Elliptic Curve
Cryptography (ECC). The secured protocol uses encrypted HTTP cookies within three stages. First, the
device registers itself with the cloud. When computation is required, the device sends a login request. Finally,
the device and the cloud mutually authenticate using ECC parameters. The authors have modelled the
proposed protocol in the HLPSL language and used the AVISPA tools, OFMC and CL-AtSe to verify the
security of their protocol against seven attacks ranging from eavesdropping to cookie theft. The verification
showed that the protocol remains secure, increasing confidence that the protocol is ready for practical
application. Similar to IoT devices, many enterprises are deploying mobile devices to connect to the cloud
for their enterprise services. In [RCD+ 17] the authors propose a lightweight mobile authentication scheme
for mobile cloud computing. The scheme contains four properties, first a trusted third party is not involved
during login phase, second a mobile user only has one set of unique credentials, third the authentication
process avoids costly operations on a mobile device and fourth the mutual authentication uses lightweight
cryptography. The authors provide a mutual authentication proof using BAN logic and verify their scheme
against a Dolev-Yao attacker using ProVerif. The authors note that the scheme’s high security and low cost
is well suited for practical application. A significant improvement to IoT infrastructure is the emergence of
5G, the fifth generation of mobile networks. We foresee several applications in this domain, given the novelty
and the safety-critical aspect of such infrastructure. The work of [BDH+ 18] shows how to use Tamarin, a
protocol verification tool, to find and issues and suggest fixes to an Authentication Key Exchange protocol.
Furthermore the author of [Aia15] analyses proposed authentication protocols for mobile devices. These
protocols need to satisfy requirements of mutual authentication of a SIM card and a device and a user
authentication against the device, preferably by biometric means. The author has considered two protocols,
26                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



the authentication framework protocol [YHXH05] and the mobile Ethernet protocol [IK06]. The author
has specified six security properties ranging from mutual authentication to key freshness and modelled the
protocols in CSP for analysis using the FDR model checker. In order to analyse more than the existing
protocols, the author has proposed two protocols of their own. The analysis has discovered that the mobile
Ethernet protocol is vulnerable to replay attacks, the authentication framework protocol did not show any
vulnerabilities, however the author notes that due to large overhead of the protocol it might not be suitable
for mobile devices. From the two protocols proposed by the author, one did not show any vulnerabilities
and the author considers it a good candidate for mobile networks authentication, while the second proposed
protocol did not satisfy the property of mutual authentication.


2.5.4. Implementation

Enterprise computing of today consists of many applications that are implemented using different languages,
technologies and frameworks. As the works below show, FM are a good fit for this heterogeneous landscape.
    One of the examples of modern technologies in the enterprise domain is blockchain smart contracts
as defined in [BHBLT17]. These smart contracts are digital contracts that provide verifiable and perma-
nent agreement for satisfaction of common contractual conditions. The authors of [PZS+ 18b] have verified
smart contracts within the blockchain network, Ethereum, where the smart contracts were compiled to the
Ethereum Virtual Machine (EVM) bytecode. The authors have verified the functional correctness of high-
profile smart contracts such as ERC20 token contracts [Fab20] to ensure security properties of these contracts.
The verification has been carried out using the K-framework’s reachability logic theorem prover [SPY+ 16],
while the authors have introduced specific EVM lemmas to optimise the verification time. The authors dis-
covered that the token implementation that diverges from the ERC20 specification contains several security
vulnerabilities.
    Web technology also finds a lot of utilisation in enterprise computing. Web applications and web services
often rely on third-party frameworks and plugins to add new features. In [NFV15] the authors have developed
a static code analysis tool for PHP plugins, called phpSAFE. This tool is used to detect cross-site scripting
and SQL injection vulnerabilities by creating a model using lexical and semantic analysis of the abstract
syntax tree of the PHP code and following the flow of uncontrolled environment variables. The authors have
applied their tool to 35 PHP plugins discovering over 580 vulnerabilities and note that about 40% of the
vulnerabilities discovered within the analysed PHP plugins are still present in their updated versions. Due
to this, the authors encourage use of analysis tools on third party component integrations. Similarly, web
applications can integrate third party APIs. The authors of [XCWC13] have created a tool, InteGuard that
uses invariant analysis [Ham05] for in-the-loop malicious behaviour detection. This tool generates several
types of invariants based on network traffic including the content of HTML files and Javascript code and
analyses the traffic against these invariants. The authors have validated their tool against 11 real world
exploits based on subtle logic flaws in hybrid web applications and note that the tool effectively detected
these flaws without generation of false positives.
    Security of hypervisors also stems from their implementation. The authors of [VCM+ 16] created a frame-
work, überSpark, for implementation of hypervisors written in C and Assembly with verified security prop-
erties. The framework uses logical components to express functionality and provide behavioural contracts.
The implementation is carried out in CASM, a dialect of C with embedded assembly, and verified using
FRAMA-C [SCK+ 12] for static analysis of behavioural contracts, abstract variable assertions and control
flow integrity. The authors reason formally about their framework by expressing its security properties as
theorems and use it to construct a reference hypervisor demonstrating that a security verified hypervisor
can have a performance close to unverified hypervisor. A few years prior, in [VCJ+ 13] the authors have cre-
ated the eXtensible and Modular Hypervisor Framework (XMHF). The goal of this framework was to verify
the security property of memory integrity within single-guest hypervisors. As a first step, the authors have
expressed security properties and invariants. These properties were then dispatched to the CBMC model
checker [CKL04] verifying the actual C implementation. As the CBMC model checker could not handle all
C constructs, the authors automatically verified 5208 out of 6018 lines of code and audited the rest of the
code manually. The authors have validated their framework by comparing its performance against general
purpose hypervisors demonstrating similar performance values and note that the XMHF provides a good
starting point for implementation of secure hypervisors.
A Survey of Practical Formal Methods for Security                                                           27



2.5.5. Hardware
Enterprise computing requires significant hardware infrastructure and must provide assurances such as data
confidentiality and computational security. This provides an opportunity to use FM to satisfy the required
assurances.
    Enterprise customers often consider a cloud provider as an untrusted entity, where the cloud adminis-
trators themselves could pose a security threat [SGR09]. In this regard, the authors of [SJL+ 15] created a
cloud isolation system, isolating the user data from cloud administrators and limiting the operations that
the administrators could take against a user’s virtual machine. This is based on a hardware module, that the
authors named Trusted Cloud Module (TCM) that provides a limited set of interfaces to the cloud administra-
tor, manages encryption keys and provides secure storage for the user. The module is built from off-the-shelf
hardware components using the Scyther verification tool. They verify the security of communication between
the TCM and the other components and the attestation that the TCM provides. Their analysis considered
seven attack vectors, excluding the DoS attacks. The authors state that their system increases security
for users while demonstrating reasonable I/O throughput. The basis of trusted computing is the Trusted
Platform Module (TPM) co-processor providing secure storage and computing environment. Unfortunately
the security of platforms using TPM is often not formally verified leading to vulnerabilities [BCLM05]. To
mitigate this, the authors of [BHW+ 14] have proposed TRUSTFOUND a formal modelling framework for
model checking of trusted computing platforms. This framework provides a model of the TPM; a formalism
for modelling hardware, communications, cryptography and trusted computing techniques. Furthermore the
framework contains models of several attackers including a hardware attacker, network attacker and a sys-
tem attacker. The formalisms used within the framework are a Trusted CSP#, an extension of CSP#, and
LS2 [DFGK09], where the PAT model checker is used for verification. The authors used their framework to
analyse a cloud computing platform and an envelope protocol, focusing on attestation and confidentiality,
detecting six implied assumptions and two severe logic flaws. The authors are also working on supporting
the specification of TPM 2.0.
    Sometimes, in order to provide strong authentication, small One Time Password (OTP) generation hard-
ware is used by enterprises to authenticate users towards cloud services [BHvOS12]. One such device is Yu-
bikey, a USB OTP generator. In [KS13], the authors have formally analysed the security of the Yubikey
OTP and also a security of Hardware Security Module (HSM), developed by the same company in order
to prevent attacks in case that the authentication server itself has been compromised. The authors first
analyse the Yubikey OTP while the authentication server is not compromised proving the security of the
OTP scheme. Secondly the verification included a case where the authentication server is compromised and
secured using the HSM, uncovering two potential attacks that could lead to release of all secure keys. The
verification has been carried out using the Tamarin theorem prover, where the authors provided several
intermediate lemmas. Furthermore the authors proposed a scheme and changes to the HSM resolving the
discovered security issues.
    Another challenging issue of enterprise computing within the cloud is addressing CPU side-channel at-
tacks. One of these attacks is a timing channel attack, where an attacker, possibly a virtual machine, could
determine the algorithm executed by another virtual machine in a shared environment. To solve this, the
authors of [FWX+ 17] have proposed Timing Compartments, an isolation scheme implemented in hardware
isolating timing information between parties sharing the resources. The authors have implemented their
scheme to a quad-core CPU and performed information flow analysis using SecVerilog, demonstrating the
effectiveness of their scheme. The authors note that while their scheme is effective, performance optimisations
were needed in order to extract reasonable performance from the CPU.


3. Future Outlook
The survey has provided an overview of use of FM within security in several domains. Based on the research
conducted within these domains it is expected that in some cases the use of FM will accelerate while, in other
cases the use will increase with a slower pace. There is however a general trend of increase of adoption. In
cases within the financial domain, it is clear that the use of FM comes with new financial technologies such as
cryptocurrencies and smart contracts. This adoption could be seen in a survey aimed specifically at the smart
contracts domain [HK18]. The use of mobile applications in the financial domain is also spurring a demand
for high security assurance, that could be delivered by use of FM. Finally with the rise of cryptocurrencies,
28                 T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



the hardware within the financial domain is being specialised to facilitate transactions. It is expected that the
security of this hardware will continue to be scrutinised formally with increasing coverage and complexity.
    The industrial domain faces its own set of unique challenges in the area of cyber security. It is expected
that with increase in automation complexity and use of digital technologies in critical industrial installations,
FM will play a crucial role. The trend was already presented in 2015 by [KPCBH15] who have surveyed
approaches for security and safety of industrial control systems, including informal approaches. As of now
most works within this domain are of reactive nature, i.e. analysis of existing systems and protocols. However
several works within the survey show a trend towards utilisation of FM early in the design process of new
industrial installations and protocols. Another emerging trend within the industrial domain is integration
of formal verification tools with the software development processes, this is clear primarily in terms of
robotic applications and PLC code. It is expected that with increasing complexity of robotic applications
and underlying hardware, FM will play a significant role in the future.
    The domain of consumer computation is a rapidly evolving one. The consumer trends move fast, however a
somewhat surprising amount of work is already put forward to use of FM in malware protection [BGWL+ 18],
going as far as creation of formally verified Internet browsers. Also, the shift of computation from computers
to smartphones has brought new security challenges. In this area a lot of focus has already been put on
analysis of the Android OS permission system. This area shows an increase in the amount of research and as
long as the mobile OSs are in use by millions of users the formal verification will accelerate, possibly leading to
full formal security verification of a popular mobile OS. Consumer hardware such as smartphones is putting
into use TPMs, securing mobile computation. Also in this area the use of FM is increasing, specifically to
ensure the properties of the secure TPM enclave.
    Finally the domain of enterprise computation has uncovered several interesting trends. The first of these is
a trend to use FM against virtualisation hypervisors in order to analyse security properties of existing virtual
environments as well as use the knowledge to build fully formally verified hypervisors. Another important
trend is the significant investment that major cloud computation providers are putting into formal verification
of security of their products. To this end not only have existing tools been applied, but the cloud providers
have turned towards development of their own FM tools. Both of these trends are expected not only to
continue but also to accelerate due to the ever increasing popularity of cloud computing and virtualisation.
Several of these trends were already mentioned in 2002 by [Jül02].
    It is important to note that several authors have expressed a wish for improvement of automated formal
verification tools. This is in order to allow for simplified entry of non-practitioners to the world of FM.
Both academia and industry is moving towards addressing this wish, with tools becoming similar to software
development IDEs and in some cases integration of FM toolkit directly to an existing IDE. It is expected
that knowledge of FM will become important for system and software engineering disciplines in the future
and therefore collaborative projects between industry and academia shall provide experts in this domain.
These issues have been discussed for several years now [DCC+ 13].
    When it comes to FM techniques, static analysis tools are becoming popular in software development,
while model checking is moving strongly towards system design and protocol verification with model checking
being designed for specific problems. Theorem proving is also showing a promise of playing a crucial role in
the future, given that the perceived large learning curve could be minimised.
    As the use of FM is accelerating within all of the different domains considered in this survey, it is
imperative that a new survey is carried out as soon as in five to ten years. By then it is expected that the tools
will reach the quality of commercial grade IDEs and integration with a wide variety of text editors [TJK19]
and the techniques will become a known factor when developing and designing a new system, application or
a hardware component.


4. Conclusions
More than 30 years ago, Burrows et al. published their pioneering work on the BAN logic for security protocol
analysis [BAN90]. Their work was not fully formal and was shown to permit approval of dangerous protocols.
Nevertheless, they showed that their logic was good at revealing various subtle security flaws and drawbacks,
specifically in authentication protocols. They set out to answer five questions:
1. Does this protocol work?
2. Can it be made to work?
A Survey of Practical Formal Methods for Security                                                           29



3. Exactly what does this protocol achieve?
4. Does this protocol need more assumptions than another protocol?
5. Does this protocol do anything unnecessary?
Their important paper inspired a generation of security researchers to use FM to devise and analyse security
protocols and to answer similar questions. Furthermore in describing the benefits of formal verification
for software engineering, Dijkstra famously quoted “Testing shows the presence, not the absence of bugs”.
More than 50 years later, in the setting of computer security, we might now have sufficient evidence to
claim “Formal methods show the presence, not the absence of security flaws” [BR70]. That is, although FM
provides rigorous tools and techniques for proving the absence of security flaws, this rigour comes with a
proviso: proofs are only possible if the security flaw is documented and specified within a formal framework.
Current limitations mean that FM cannot uncover any new flaws since we may not actually be looking for
them.
    Take for instance the recent Spectre and Meltdown attacks [KHF+ 19]. Like many vulnerabilities, both
attacks have been shown to exist for a range of processors that make use of speculative execution, and
mitigation against these requires software-side interventions. However, despite the widespread nature of these
vulnerabilities, the attacks themselves were not discovered through formal verification, but rather through
a series of experiments over the training and timing of micro-architectural components. Fortunately, once
a security flaw has been uncovered, even complex attacks such as Spectre and Meltdown can be formally
characterised and isolated [CRSS19]. Once this has been done, the next phase is a formal framework for
reasoning about such issues, followed by more streamlined tools to scale verification to larger scale systems.
Thus, as important as it is to continue research into the practical use of FM in security, it is equally
important to expand our reasoning capabilities for FM in security through the study of theoretical aspects
of the discipline. Without this, there is a possibility of a new type of security flaw that falls outside the
realms of current day logics. Spectre and Meltdown, for instance, are instances of subset-closed hyper-
properties [CRSS19]. Hence without existing works on hyper-properties [CS10] and subsequent works on
their verification, the specification and therefore use of FM to protect against Spectre and Meltdown would
have been much more difficult.
    In this paper, we have shown how FM have had an impact on society so far and how this impact will
increase in the future. In the past, security has been an optional extra that industry does not want to
invest in during development. But times are changing. For example, security has become a core selling point
for Amazon Web Services (see Section 2.4.1). FM have been used successfully in the financial, industrial,
consumer, and enterprise sectors (see Section 2).


Specification Languages and Associated Tools

Our survey covers more than a decade of the use of FM in security. It reveals the rich variety of formal
specification languages and their tools, theorem provers, model checkers, and verification frameworks. We
have recorded more than 40 different specification languages and more than 40 different verification tools.
These include the following.

Specification languages AADL (Architecture Analysis & Design Language) [CGB+ 18, ALR16], ASF
(Anonymous Secure Framework) [KBG+ 17], ASLan++ (AVANTSSAR Specification Language) [AAA+ 12],
BAN logic [BAN90, Sne91], Boogie [BCD+ 05], Boxed Ambients [JED+ 12], CASM (ASM-based SL for com-
pilers) [VCM+ 16], CCS (Calculus of Communicating Systems) [KKG19], COVERT (compositional analysis
of Android apps) [BSGM15], CSP (Communicating Sequential Systems) [HSB+ 19], CSP# (shared vari-
ables CSP) [SLD08], CTL (Computation tree temporal logic) [ST12], Cloud Calculus [JED+ 12], Cryptol
[EM09], Dynamic State Machine [NRM16], ERC20 token contracts [PZS+ 18b], Event-B [DKK+ 14], HLPSL
(High Level Protocol Specification Language) [BS15], Hoare logic [GNDB16], LS2 (Logic of Secure Sys-
tems) [BHW+ 14], LTL (linear-time temporal logic) [XWL14], Markov Decision Process [MSHA17], Petri
nets [ACF16], π-calculus [Bla16], PlusCal [AZP17], Promela [MMN18], RTL (real-time logic) [GDMJ16a],
SPDL (Security Protocol Description Language) [MGP16], SysML-Sec [ALR16], TLA+ (Temporal Logic of
Actions) [Coo18], Trusted CSP# [BHW+ 14], überSpark [VCM+ 16], VDM [Fre18], Verilog [LJM11], VHDL
[GDMJ16b], VML [SLBK14], vTRUST [HLC+ 13], XMHF (eXtensible and Modular Hypervisor Framework)
[VCJ+ 13], Z [WSC+ 08].
30                   T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



Model checkers AVISPA (Automated Validation of Internet Security Protocols and Applications) [ABB+ 05],
Alloy [DKK+ 14], CBMC (Bounded Model Checker for C and C++) [CR18], CWB-NC (Concurrency Work-
bench of New Century) [KKG19], Cadence IFV (RTL block-level verifier) [GDMJ16b], FDR [GR19], GROOVE
[GdR+ 10], jKind [GBW+ 17], NuSMV [CCGR99], OFMC (on-the-fly model checker) [BMV05], PAT (Process
Analysis Toolkit for CSP#) [SLD08], PRISM (probabilistic model checker) [MSHA17], SATMC (SAT-based
model checker for security protocols) [BS15], SPIN [TSS16], TRUSTFOUND [BHW+ 14], UPPAAL [MMS19],
UVHM (formal analysis scheme for hypervisors) [VCJ+ 13].

Theorem provers Coq [Coo18], Isabelle/HOL [KAE+ 10], K-framework [PZS+ 18b], TAMARIN [KS13],
Why [FM07].

Verification tools and frameworks AndroBugs (Framework For Android Vulnerability Scanning) [TM17],
Cl-Atse (protocol analyser) [KS15], FUDGE (Fuzz driver generator) [BBC+ 19a], Frama-C [VCM+ 16], Kraka-
tau [KKG19], Maude (rewrite engine) [NT19], MobSF (mobile security framework) [ISCM17], phpSAFE
[NFV15], ProVerif [Bla16], Quark [JTL12b], SAW (Software Analysis Workbench) [Coo18], SMACK [Coo18],
SecGuru [JBOK14], SecVeriLog [FWX+ 17], Sugar (SAT-based) [MJA+ 18], TTool (translator from SysML-
Sec to π-calculus) [ALR16], Z3 [ABK+ 19].
    This shows how research and application in FM for security has developed since Burrows et al.’s seminal
paper [BAN90]. Our survey concentrated in particular on the practical application of these techniques,
especially on an industrial scale. Today, it seems inconceivable that a company would produce a commercial
secure system without subjecting it to formal analysis. We also suspect that hackers use formal techniques
to crack supposedly secure systems.
    As a final statement we need to acknowledge that a survey provides a snapshot in time within a developing
field. It is therefore necessary to return to a survey work every decade, something we are planning on doing.
Despite this shortcoming it is the opinion of the authors that a survey work is an important part of the
research as it provides a starting point and a direction indicator for new and experienced practitioners looking
for works under the large field of formal methods in security.


5. Acknowledgements
This work is supported by the Manufacturing Academy of Denmark, for more information see www.made.
dk. Brijesh Dongol is supported by grants “FaCT: Faithful Composition of Trust” and EPSRC grant
EP/R032556/1. Steve Schneider is supported by EPSRC grants EP/P031811/1 and EP/R006938/1. Jim
Woodcock is supported by the Poul Due Jensen Foundation and grants EP/M025756/1, EP/R025479/1,
and IEC/NSFC/170319. We would also like to thank Nick Battle, Jaco van de Pol and Bas Spitters for
reviews of earlier versions of this article. Finally, we would very much like to thank the anonymous reviewers
of an earlier version of this article for their valuable input which definitely has improved it.


References
[AAA+ 12]   Alessandro Armando, Wihem Arsac, Tigran Avanesov, Michele Barletta, Alberto Calvi, Alessandro Cappai,
            Roberto Carbone, Yannick Chevalier, Luca Compagna, Jorge Cuéllar, Gabriel Erzse, Simone Frau, Marius Minea,
            Sebastian Mödersheim, David von Oheimb, Giancarlo Pellegrino, Serena Elisa Ponta, Marco Rocchetto, Michael
            Rusinowitch, Mohammad Torabi Dashti, Mathieu Turuani, and Luca Viganò. The AVANTSSAR platform for
            the automated validation of trust and security of service-oriented architectures. In Cormac Flanagan and Bar-
            bara König, editors, Tools and Algorithms for the Construction and Analysis of Systems, pages 267–282, Berlin,
            Heidelberg, 2012. Springer Berlin Heidelberg.
[ABB+ 05]   A. Armando, D. Basin, Y. Boichut, Y. Chevalier, L. Compagna, J. Cuellar, P. Hankes Drielsma, P. C. Heám,
            O. Kouchnarenko, J. Mantovani, S. Mödersheim, D. von Oheimb, M. Rusinowitch, J. Santiago, M. Turuani, L. Vi-
            ganò, and L. Vigneron. The AVISPA tool for the automated validation of internet security protocols and applica-
            tions. In Kousha Etessami and Sriram K. Rajamani, editors, Computer Aided Verification, pages 281–285, Berlin,
            Heidelberg, 2005. Springer Berlin Heidelberg.
[ABK+ 19]   Anish Athalye, Adam Belay, M. Frans Kaashoek, Robert Morris, and Nickolai Zeldovich. Notary: A device for
            secure transaction approval. In Proceedings of the 27th ACM Symposium on Operating Systems Principles, SOSP
            ’19, page 97–113, New York, NY, USA, 2019. Association for Computing Machinery.
[Abr10]     Jean-Raymond Abrial. Modeling in Event-B: System and Software Engineering. Cambridge University Press,
            Cambridge, UK, 2010.
A Survey of Practical Formal Methods for Security                                                                         31



[ABSW13] A. Alshehri, J. A. Briffa, S. Schneider, and S. Wesemeyer. Formal security analysis of NFC M-coupon protocols
           using Casper/FDR. In 2013 5th International Workshop on Near Field Communication (NFC), pages 1–6, 2013.
[ACD90]    R. Alur, C. Courcoubetis, and D. Dill. Model-checking for real-time systems. In [1990] Proceedings. Fifth Annual
           IEEE Symposium on Logic in Computer Science, pages 414–425, 445 Hoes Lane Piscataway, NJ 08854 USA, June
           1990. IEEE.
[ACF16]    Raphael Amoah, Seyit Camtepe, and Ernest Foo. Formal modelling and analysis of DNP3 secure authentication.
           Journal of Network and Computer Applications, 59:345 – 360, 2016.
[ADKT11] Jade Alglave, Alastair F. Donaldson, Daniel Kroening, and Michael Tautschnig. Making software verification tools
           really work. In Tevfik Bultan and Pao-Ann Hsiung, editors, Automated Technology for Verification and Analysis,
           pages 28–42, Berlin, Heidelberg, 2011. Springer Berlin Heidelberg.
[ADMM14] Marcin Andrychowicz, Stefan Dziembowski, Daniel Malinowski, and Lukasz Mazurek. Modeling bitcoin contracts
           by timed automata. In Axel Legay and Marius Bozga, editors, Formal Modeling and Analysis of Timed Systems,
           pages 7–22, Cham, 2014. Springer International Publishing.
[ADRP13] Fides Aarts, Joeri De Ruiter, and Erik Poll. Formal models of bank cards for free. In 2013 IEEE Sixth International
           Conference on Software Testing, Verification and Validation Workshops, pages 461–468, 445 Hoes Lane Piscataway,
           NJ 08854 USA, 2013. IEEE.
[AE18]     Danil Annenkov and Martin Elsman. Certified compilation of financial contracts. In Proceedings of the 20th
           International Symposium on Principles and Practice of Declarative Programming, PPDP ’18, New York, NY,
           USA, 2018. Association for Computing Machinery.
[AG96]     Sarita V. Adve and Kourosh Gharachorloo. Shared memory consistency models: A tutorial. IEEE Computer,
           29(12):66–76, 1996.
[AG99]     Martı́n Abadi and Andrew D. Gordon. A calculus for cryptographic protocols: The Spi calculus. Information and
           Computation, 148(1):1 – 70, 1999.
[AGKK19] Myrto Arapinis, Andriana Gkaniatsou, Dimitris Karakostas, and Aggelos Kiayias. A formal treatment of hardware
           wallets. In Ian Goldberg and Tyler Moore, editors, Financial Cryptography and Data Security, pages 426–445,
           Cham, 2019. Springer International Publishing.
[Aia15]    Mahdi Aiash. A formal analysis of authentication protocols for mobile devices in next generation networks.
           Concurrency and Computation: Practice and Experience, 27(12):2938–2953, 2015.
[ALKH17] Imran Hafeez Abbasi, Faiq Khalid Lodhi, Awais Mehmood Kamboh, and Osman Hasan. Formal verification
           of gate-level multiple side channel parameters to detect hardware trojans. In Cyrille Artho and Peter Csaba
           Ölveczky, editors, Formal Techniques for Safety-Critical Systems, pages 75–92, Cham, 2017. Springer International
           Publishing.
[ALR16]    L. Apvrille, L. Li, and Y. Roudier. Model-driven engineering for designing safe and secure embedded systems.
           In 2016 Architecture-Centric Virtual Integration (ACVI), pages 4–7, 445 Hoes Lane Piscataway, NJ 08854 USA,
           April 2016. IEEE.
[Ama19a] Amazon.com Inc. Amazon Simple Storage Service (S3). aws.amazon.com/s3/, 2019. Accessed February 7 2019.
[Ama19b] Amazon.com Inc. s2n. github.com/awslabs/s2n, 2019. Accessed February 7 2019.
[AMM14] S. Abughazalah, K. Markantonakis, and K. Mayes. Secure mobile payment on NFC-enabled mobile phones formally
           analysed using CasperFDR. In 2014 IEEE 13th International Conference on Trust, Security and Privacy in
           Computing and Communications, pages 422–431, 445 Hoes Lane Piscataway, NJ 08854 USA, 2014. IEEE.
[AUS12]    Shakeel Ahamad, Siba Udgata, and V Sastry. A new mobile payment system with formal verification. International
           Journal of Internet Technology and Secured Transactions, 4:71–103, 01 2012.
[AZHL12] Kathy Wain Yee Au, Yi Fan Zhou, Zhen Huang, and David Lie. PScout: Analyzing the Android permission
           specification. In Proceedings of the 2012 ACM Conference on Computer and Communications Security, CCS ’12,
           pages 217–228, New York, NY, USA, 2012. ACM.
[AZP17]    Sabina Akhtar, Ehtesham Zahoor, and Olivier Perrin. Formal verification of authorization policies for enterprise
           social networks using pluscal-2. In Imed Romdhani, Lei Shu, Takahiro Hara, Zhangbing Zhou, Timothy J. Gordon,
           and Deze Zeng, editors, Collaborative Computing: Networking, Applications and Worksharing - 13th International
           Conference, CollaborateCom 2017, Edinburgh, UK, December 11-13, 2017, Proceedings, volume 252 of Lecture
           Notes of the Institute for Computer Sciences, Social Informatics and Telecommunications Engineering, pages
           530–540. Springer, 2017.
[BAN90]    Michael Burrows, Martı́n Abadi, and Roger M. Needham. A logic of authentication. ACM Trans. Comput. Syst.,
           8(1):18–36, 1990.
[Bar12]    John Barnes. Spark: The Proven Approach to High Integrity Software. Altran Praxis, UK, 2012.
[BBB+ 19] Manuel Barbosa, Gilles Barthe, Karthik Bhargavan, Bruno Blanchet, Cas Cremers, Kevin Liao, and Bryan Parno.
           SoK: Computer-aided cryptography. Cryptology ePrint Archive, Report 2019/1393, 2019. eprint.iacr.org/2019/
           1393.
[BBC+ 19a] Domagoj Babic, Stefan Bucur, Yaohui Chen, Franjo Ivancic, Tim King, Markus Kusano, Caroline Lemieux, László
           Szekeres, and Wei Wang. FUDGE: fuzz driver generation at scale. In Marlon Dumas, Dietmar Pfahl, Sven
           Apel, and Alessandra Russo, editors, Proceedings of the ACM Joint Meeting on European Software Engineering
           Conference and Symposium on the Foundations of Software Engineering, ESEC/SIGSOFT FSE 2019, Tallinn,
           Estonia, August 26-30, 2019, pages 975–985. ACM, 2019.
[BBC+ 19b] Domagoj Babić, Stefan Bucur, Yaohui Chen, Franjo Ivančić, Tim King, Markus Kusano, Caroline Lemieux, László
           Szekeres, and Wei Wang. FUDGE: Fuzz driver generation at scale. In Proceedings of the 2019 27th ACM Joint
           Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineer-
           ing, ESEC/FSE 2019, page 975–985, New York, NY, USA, 2019. Association for Computing Machinery.
32                   T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



[BCB01]    M.R. Blackburn, Ramaswamy Chandramouli, and Robert Busser. Model-based approach to security test automa-
           tion. Quality Week, 01 2001.
[BCD+ 05] Michael Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and K. Rustan M. Leino. Boogie: A modular
           reusable verifier for object-oriented programs. In Frank S. de Boer, Marcello M. Bonsangue, Susanne Graf, and
           Willem P. de Roever, editors, Formal Methods for Components and Objects, 4th International Symposium, FMCO
           2005, Amsterdam, The Netherlands, November 1-4, 2005, Revised Lectures, volume 4111 of Lecture Notes in
           Computer Science, pages 364–387, Berlin, Heidelberg, 2005. Springer.
[BCJ+ 06] Janet Barnes, Rod Chapman, Randy Johnson, James Widmaier, David Cooper, and Bill Everett. Engineering the
           Tokeneer enclave protection system. In Proceedings of the 1st IEEE International Symposium on Secure Software
           Engineering, page 10, 445 Hoes Lane Piscataway, NJ 08854 USA, 2006. IEEE Computer Society Press.
[BCLM05] D. Bruschi, L. Cavallaro, A. Lanzi, and M. Monga. Replay attack in TCG specification and solution. In 21st
           Annual Computer Security Applications Conference (ACSAC’05), pages 11 pp.–137, 445 Hoes Lane Piscataway,
           NJ 08854 USA, Dec 2005. IEEE.
[BCMS05] Michele Bugliesi, Silvia Crafa, Massimo Merro, and V. Sassone. Communication and mobility control in boxed
           ambients. Information and Computation, 202:39–86, 10 2005.
[BDH+ 18] David Basin, Jannik Dreier, Lucca Hirschi, Saša Radomirovic, Ralf Sasse, and Vincent Stettler. A formal analysis
           of 5G authentication. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications
           Security, pages 1383–1396, 2018.
[BDSS08] Sergey Bratus, Nihal D’Cunha, Evan R. Sparks, and Sean W. Smith. TOCTOU, traps, and trusted computing.
           In Peter Lipp, Ahmad-Reza Sadeghi, and Klaus-Michael Koch, editors, Trusted Computing - Challenges and
           Applications, First International Conference on Trusted Computing and Trust in Information Technologies, Trust
           2008, Villach, Austria, March 11-12, 2008, Proceedings, volume 4968 of Lecture Notes in Computer Science, pages
           14–32, Berlin, Heidelberg, 2008. Springer.
[BGV11]    Siavosh Benabbas, Rosario Gennaro, and Yevgeniy Vahlis. Verifiable delegation of computation over large datasets.
           In Phillip Rogaway, editor, Advances in Cryptology – CRYPTO 2011, pages 111–131, Berlin, Heidelberg, 2011.
           Springer Berlin Heidelberg.
[BGWL+ 18] Fabrizio Biondi, Thomas Given-Wilson, Axel Legay, Cassius Puodzius, and Jean Quilbeuf. Tutorial: An overview
           of malware detection and evasion techniques. In Tiziana Margaria and Bernhard Steffen, editors, Leveraging
           Applications of Formal Methods, Verification and Validation. Modeling, pages 565–586, Cham, 2018. Springer
           International Publishing.
[BHBLT17] Elyes Ben Hamida, Kei Leo Brousmiche, Hugo Levard, and Eric Thea. Blockchain for Enterprise: Overview, Op-
           portunities and Challenges. In The Thirteenth International Conference on Wireless and Mobile Communications
           (ICWMC 2017), page 17, Nice, France, July 2017. IARIA XPS Press.
[BHvOS12] J. Bonneau, C. Herley, P. C. v. Oorschot, and F. Stajano. The quest to replace passwords: A framework for
           comparative evaluation of web authentication schemes. In 2012 IEEE Symposium on Security and Privacy, pages
           553–567, 445 Hoes Lane Piscataway, NJ 08854 USA, 2012. IEEE.
[BHW+ 14] Guangdong Bai, Jianan Hao, Jianliang Wu, Yang Liu, Zhenkai Liang, and Andrew Martin. TrustFound: Towards
           a formal foundation for model checking trusted computing platforms. In Cliff Jones, Pekka Pihlajasaari, and Jun
           Sun, editors, FM 2014: Formal Methods, pages 110–126, Cham, 2014. Springer International Publishing.
[BKMJ18] Hamid Bagheri, Eunsuk Kang, Sam Malek, and Daniel Jackson. A formal approach for detection of security flaws
           in the Android permission system. Formal Aspects of Computing, 30(5):525–544, Sep 2018.
[Bla16]    Bruno Blanchet. Modeling and verifying security protocols with the applied pi calculus and proverif. Found. Trends
           Priv. Secur., 1(1-2):1–135, 2016.
[BML+ 11] R. Bohn, John Messina, Fang Liu, Jin Tong, and Jian Mao. NIST cloud computing reference architecture. pages
           594–596, 07 2011.
[BMV05]    David A. Basin, Sebastian Mödersheim, and Luca Viganò. OFMC: A symbolic model checker for security protocols.
           Int. J. Inf. Sec., 4(3):181–208, 2005.
[BMV14]    Ioana Boureanu, Aikaterini Mitrokotsa, and Serge Vaudenay. Towards secure distance bounding. In Shiho Moriai,
           editor, Fast Software Encryption, pages 55–67, Berlin, Heidelberg, 2014. Springer Berlin Heidelberg.
[BR70]     J. N. Buxton and B. Randell. Software Engineering Techniques: Report of a Conference Sponsored by the NATO
           Science Committee, Rome, Italy, 27-31 Oct. 1969, Brussels, Scientific Affairs Division, NATO. 1970.
[BS15]     Sriramulu Bojjagani and V. N. Sastry. SSMBP: A secure SMS-based mobile banking protocol with formal verifi-
           cation. In WiMob, pages 252–259, 445 Hoes Lane Piscataway, NJ 08854 USA, 2015. IEEE Computer Society.
[BSCS18]   Bruno Blanchet, Ben Smyth, Vincent Cheval, and Marc Sylvestre. ProVerif 2.00: Automatic Cryptographic Protocol
           Verifier, User Manual and Tutorial. INRIA, 2018. Originally appeared as Bruno Blanchet and Ben Smyth (2011)
           ProVerif 1.85: Automatic Cryptographic Protocol Verifier, User Manual and Tutorial.
[BSGM15] H. Bagheri, A. Sadeghi, J. Garcia, and S. Malek. COVERT: Compositional analysis of Android inter-app permission
           leakage. IEEE Transactions on Software Engineering, 41(9):866–886, September 2015.
[BSNRN14] Alessandro Bruni, Michal Sojka, Flemming Nielson, and Hanne Riis Nielson. Formal security analysis of the MaCAN
           protocol. In Elvira Albert and Emil Sekerinski, editors, Integrated Formal Methods, pages 241–255, Cham, 2014.
           Springer International Publishing.
[BSW+ 18] Alejandro Bracho, Can Saygin, HungDa Wan, Yooneun Lee, and Alireza Zarreh. A simulation-based platform for
           assessing the impact of cyber-threats on smart manufacturing systems. Procedia Manufacturing, 26:1116–1127,
           2018. 46th SME North American Manufacturing Research Conference, NAMRC 46, Texas, USA.
[BTW+ 13] Christoph Busold, Ahmed Taha, Christian Wachsmann, Alexandra Dmitrienko, Hervé Seudié, Majid Sobhani, and
           Ahmad-Reza Sadeghi. Smart keys for cyber-cars: Secure smartphone-based NFC-enabled car immobilizer. In
A Survey of Practical Formal Methods for Security                                                                           33



           Proceedings of the Third ACM Conference on Data and Application Security and Privacy, CODASPY ’13, page
           233–242, New York, NY, USA, 2013. Association for Computing Machinery.
[BVGM15] Sören Bleikertz, Carsten Vogel, Thomas Groß, and Sebastian Mödersheim. Proactive security analysis of changes in
           virtualized infrastructures. In Proceedings of the 31st Annual Computer Security Applications Conference, ACSAC
           2015, page 51–60, New York, NY, USA, 2015. Association for Computing Machinery.
[Cad20]    Cadence IFV model checker.                www.cadence.com/en_US/home/tools/system-design-and-verification/
           formal-and-static-verification/jasper-gold-verification-platform.html, 2020. Accessed: 2020-02-21.
[Can01]    R. Canetti. Universally composable security: A new paradigm for cryptographic protocols. In Proceedings 42nd
           IEEE Symposium on Foundations of Computer Science, pages 136–145, 445 Hoes Lane Piscataway, NJ 08854 USA,
           2001. IEEE.
[CCC+ 18] Andrey Chudnov, Nathan Collins, Byron Cook, Joey Dodds, Brian Huffman, Colm MacCárthaigh, Stephen Magill,
           Eric Mertens, Eric Mullen, Serdar Tasiran, Aaron Tomb, and Eddy Westbrook. Continuous formal verification of
           Amazon s2n. In Hana Chockler and Georg Weissenbacher, editors, Computer Aided Verification, pages 430–446,
           Cham, 2018. Springer International Publishing.
[CCD+ 17] K. Cohn-Gordon, C. Cremers, B. Dowling, L. Garratt, and D. Stebila. A formal security analysis of the Signal
           Messaging Protocol. In 2017 IEEE European Symposium on Security and Privacy (EuroS P), pages 451–466, 445
           Hoes Lane Piscataway, NJ 08854 USA, April 2017. IEEE.
[CCGR99] Alessandro Cimatti, Edmund M. Clarke, Fausto Giunchiglia, and Marco Roveri. NUSMV: A new symbolic model
           verifier. In Proceedings of the 11th International Conference on Computer Aided Verification, CAV ’99, page
           495–499, Berlin, Heidelberg, 1999. Springer-Verlag.
[CCR06]    Common Criteria Recognition Agreement CCRA. Common criteria for information technology security evaluation.
           Part 1: Introduction and general model. Tech. Rep. CCMB-2006-09-001, Version 3.1, Revision 1, Sept 2006.
[CFM16]    S. Chen, H. Fu, and H. Miao. Formal verification of security protocols using Spin. In 2016 IEEE/ACIS 15th
           International Conference on Computer and Information Science (ICIS), pages 1–6, 445 Hoes Lane Piscataway,
           NJ 08854 USA, June 2016. IEEE.
[CG00]     Luca Cardelli and Andrew D. Gordon. Mobile ambients. Theoretical Computer Science, 240(1):177 – 213, 2000.
[CGB+ 18] D. Cofer, A. Gacek, J. Backes, M. W. Whalen, L. Pike, A. Foltzer, M. Podhradsky, G. Klein, I. Kuz, J. Andronick,
           G. Heiser, and D. Stuart. A formal approach to constructing secure air vehicle software. Computer, 51(11):14–23,
           Nov 2018.
[CGDR+ 15] Tom Chothia, Flavio D Garcia, Joeri De Ruiter, Jordi Van Den Breekel, and Matthew Thompson. Relay cost
           bounding for contactless EMV payments. In International Conference on Financial Cryptography and Data Se-
           curity, pages 189–206, Berlin, Heidelberg, 2015. Springer.
[CGHS17] Tom Chothia, Flavio D Garcia, Chris Heppel, and Chris McMahon Stone. Why banker bob (still) can’t get
           TLS right: A security analysis of TLS in leading UK banking apps. In International Conference on Financial
           Cryptography and Data Security, pages 579–597, Berlin, Heidelberg, 2017. Springer.
[CKK+ 12] Pascal Cuoq, Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. Frama-
           C — A software analysis perspective. In George Eleftherakis, Mike Hinchey, and Mike Holcombe, editors, Software
           Engineering and Formal Methods - 10th International Conference, SEFM 2012, Thessaloniki, Greece, October
           1-5, 2012. Proceedings, volume 7504 of Lecture Notes in Computer Science, pages 233–247, Berlin, Heidelberg,
           2012. Springer.
[CKL04]    Edmund Clarke, Daniel Kroening, and Flavio Lerda. A tool for checking ANSI-C programs. In Kurt Jensen and
           Andreas Podelski, editors, Tools and Algorithms for the Construction and Analysis of Systems, pages 168–176,
           Berlin, Heidelberg, 2004. Springer Berlin Heidelberg.
[CLW+ 14] Xiaofeng Chen, Jin Li, Jian Weng, Jianfeng Ma, and Wenjing Lou. Verifiable computation over large database
           with incremental updates. In Miroslaw Kutylowski and Jaideep Vaidya, editors, Computer Security - ESORICS
           2014, pages 148–162, Cham, 2014. Springer International Publishing.
[CM12]     Cas Cremers and Sjouke Mauw. Operational Semantics and Verification of Security Protocols. Springer, Berlin,
           Heidelberg, 2012.
[CMN+ 18] Aniello Cimitile, Francesco Mercaldo, Vittoria Nardone, Antonella Santone, and Corrado Aaron Visaggio. Talos:
           No more ransomware victims with formal methods. International Journal of Information Security, 17(6):719–738,
           November 2018.
[Coo18]    Byron Cook. Formal Reasoning About the Security of Amazon Web Services. In Hana Chockler and Georg
           Weissenbacher, editors, Computer Aided Verification, pages 38–47, Cham, 2018. Springer International Publishing.
[CR18]     Sudipta Chattopadhyay and Abhik Roychoudhury. Symbolic verification of cache side-channel freedom. IEEE
           Trans. Comput. Aided Des. Integr. Circuits Syst., 37(11):2812–2823, 2018.
[Cre08]    Cas J. F. Cremers. The Scyther tool: Verification, falsification, and analysis of security protocols. In Aarti Gupta
           and Sharad Malik, editors, Computer Aided Verification, pages 414–418, Berlin, Heidelberg, 2008. Springer Berlin
           Heidelberg.
[CRSS19] K. Cheang, C. Rasmussen, S. Seshia, and P. Subramanyan. A formal approach to secure speculation. In 2019
           IEEE 32nd Computer Security Foundations Symposium (CSF), pages 288–28815, 2019.
[CS96]     Rance Cleaveland and Steve Sims. The NCSU concurrency workbench. In Rajeev Alur and Thomas A. Henzinger,
           editors, Computer Aided Verification, pages 394–397, Berlin, Heidelberg, 1996. Springer Berlin Heidelberg.
[CS10]     Michael R. Clarkson and Fred B. Schneider. Hyperproperties. J. Comput. Secur., 18(6):1157–1210, September
           2010.
[DA07]     S. Dominikus and M. Aigner. mCoupons: An application for near field communication (NFC). In 21st International
           Conference on Advanced Information Networking and Applications Workshops (AINAW’07), volume 2, pages 421–
           428, 2007.
34                   T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



[DCC+ 13] Jennifer A. Davis, Matthew Clark, Darren Cofer, Aaron Fifarek, Jacob Hinchman, Jonathan Hoffman, Brian
          Hulbert, Steven P. Miller, and Lucas Wagner. Study on the barriers to the industrial adoption of formal methods.
          In Charles Pecheur and Michael Dierkes, editors, Formal Methods for Industrial Critical Systems, pages 63–77,
          Berlin, Heidelberg, 2013. Springer Berlin Heidelberg.
[DDSW11] Lucas Davi, Alexandra Dmitrienko, Ahmad-Reza Sadeghi, and Marcel Winandy. Privilege escalation attacks on
          Android. In Mike Burmester, Gene Tsudik, Spyros Magliveras, and Ivana Ilić, editors, Information Security, pages
          346–360, Berlin, Heidelberg, 2011. Springer Berlin Heidelberg.
[DF89]    Yvo Desmedt and Yair Frankel. Threshold cryptosystems. In Conference on the Theory and Application of
          Cryptology, pages 307–315, Berlin, Heidelberg, 1989. Springer.
[DFGK09] Anupam Datta, Jason Franklin, Deepak Garg, and Dilsun Kaynar. A logic of secure systems and its application
          to trusted computing. In Proceedings - IEEE Symposium on Security and Privacy, pages 221–236, 445 Hoes Lane
          Piscataway, NJ 08854 USA, 10 2009. IEEE.
[DFLO19] Dino Distefano, Manuel Fähndrich, Francesco Logozzo, and Peter W O’Hearn. Scaling static analyses at Facebook.
          Communications of the ACM, 62(8):62–70, 2019.
[DKK+ 14] Petr N. Devyanin, Alexey V. Khoroshilov, Victor V. Kuliamin, Alexander K. Petrenko, and Ilya V. Shchepetkov.
          Formal verification of OS security model with Alloy and Event-B. In Yamine Ait Ameur and Klaus-Dieter Schewe,
          editors, Abstract State Machines, Alloy, B, TLA, VDM, and Z, pages 309–313, Berlin, Heidelberg, 2014. Springer
          Berlin Heidelberg.
[dMB08]   Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In C. R. Ramakrishnan and Jakob Rehof,
          editors, Tools and Algorithms for the Construction and Analysis of Systems, pages 337–340, Berlin, Heidelberg,
          2008. Springer Berlin Heidelberg.
[DMC+ 18] Zhangbo Duan, Hongliang Mao, Zhidong Chen, Xiaomin Bai, Kai Hu, and Jean-Pierre Talpin. Formal modeling
          and verification of blockchain system. In Proceedings of the 10th International Conference on Computer Modeling
          and Simulation, ICCMS 2018, page 231–235, New York, NY, USA, 2018. Association for Computing Machinery.
[DPP+ 17] Jannik Dreier, Maxime Puys, Marie-Laure Potet, Pascal Lafourcade, and Jean-Louis Roch. Formally verifying flow
          properties in industrial systems. In SECRYPT 2017 - 14th International Conference on Security and Cryptography,
          Proceedings of the 14th International Joint Conference on e-Business and Telecommunications (ICETE 2017) -
          Volume 4: SECRYPT, Madrid, Spain, July 24-26, 2017., pages 55–66, Portugal, July 2017. SCITEPRESS Science
          And Technology Publications.
[DRR17]   Michael Denzel, Mark Ryan, and Eike Ritter. A malware-tolerant, self-healing industrial control system framework.
          In Sabrina De Capitani di Vimercati and Fabio Martinelli, editors, ICT Systems Security and Privacy Protection,
          pages 46–60, Cham, 2017. Springer International Publishing.
[DS81]    Dorothy E. Denning and Giovanni Maria Sacco. Timestamps in key distribution protocols. Commun. ACM,
          24(8):533–536, August 1981.
[DT17]    Khanh-Huu-The Dam and Tayssir Touili. Learning Android malware. In Proceedings of the 12th International
          Conference on Availability, Reliability and Security, ARES ’17, pages 59:1–59:9, New York, NY, USA, 2017. ACM.
[DT18]    Khanh Huu The Dam and Tayssir Touili. Learning malware using generalized graph kernels. In Proceedings of the
          13th International Conference on Availability, Reliability and Security, ARES 2018, pages 28:1–28:6, New York,
          NY, USA, 2018. ACM.
[DY81]    Danny Dolev and Andrew Chi-Chih Yao. On the security of public key protocols (extended abstract). In 22nd
          Annual Symposium on Foundations of Computer Science, Nashville, Tennessee, USA, 28-30 October 1981, pages
          350–357, 445 Hoes Lane Piscataway, NJ 08854 USA, 1981. IEEE Computer Society.
[EAP14]   Andrea Enrici, Ludovic Apvrille, and Renaud Pacalet. TTool/DiplodocusDF: A UML environment for hard-
          ware/software co-design of data-dominated systems-on-chip, 2014.
[EM09]    Levent Erkök and John Matthews. Pragmatic equivalence and safety checking in Cryptol. In Proceedings of the
          3rd workshop on Programming Languages meets Program Verification, pages 73–82, New York, NY, USA, 2009.
          ACM, ACM.
[Fab20]   Fabian Vogelsteller and Vitalik Buterin. ERC20 Token Standard. github.com/ethereum/EIPs/blob/master/EIPS/
          eip-20.md, 2020. Accessed March 24 2020.
[FCH+ 11] Adrienne Porter Felt, Erika Chin, Steve Hanna, Dawn Song, and David Wagner. Android permissions demystified.
          In Proceedings of the 18th ACM Conference on Computer and Communications Security, CCS ’11, pages 627–638,
          New York, NY, USA, 2011. ACM.
[FHB89]   Mike Flynn, Tim Hoverd, and David Brazier. Formaliser — An interactive support tool for Z. In John E.
          Nicholls, editor, Proceedings of the Fourth Annual Z User Meeting, Oxford, UK, December 15, 1989, Workshops
          in Computing, pages 128–141, Berlin, Heidelberg, 1989. Springer.
[FHK19]   D. Fett, P. Hosseyni, and R. Küsters. An extensive formal security analysis of the OpenID financial-grade API. In
          2019 IEEE Symposium on Security and Privacy (SP), pages 453–471, 445 Hoes Lane Piscataway, NJ 08854 USA,
          May 2019. IEEE.
[FKS14]   D. Fett, R. Küsters, and G. Schmitz. An expressive model for the web infrastructure: Definition and application to
          the Browser ID SSO System. In 2014 IEEE Symposium on Security and Privacy, pages 673–688, 445 Hoes Lane
          Piscataway, NJ 08854 USA, 2014. IEEE.
[FL09]    John Fitzgerald and Peter Gorm Larsen. Modelling Systems – Practical Tools and Techniques in Software Devel-
          opment. Cambridge University Press, The Edinburgh Building, Cambridge CB2 2RU, UK, Second edition, 2009.
          ISBN 0-521-62348-0.
[FLR17]   Kathleen Fisher, John Launchbury, and Raymond Richards. The HACMS program: Using formal methods to elimi-
          nate exploitable bugs. Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering
          Sciences, 375(2104):20150401, 2017.
A Survey of Practical Formal Methods for Security                                                                        35



[FM07]    Jean-Christophe Filliâtre and Claude Marché. The Why/Krakatoa/Caduceus platform for deductive program
          verification. In Werner Damm and Holger Hermanns, editors, Computer Aided Verification, 19th International
          Conference, CAV 2007, Berlin, Germany, July 3-7, 2007, Proceedings, volume 4590 of Lecture Notes in Computer
          Science, pages 173–177, Berlin, Heidelberg, 2007. Springer.
[Fre18]   Leo Freitas. VDM at large: Modelling the EMV® 2nd generation kernel. In Brazilian Symposium on Formal
          Methods, pages 109–125, Berlin, Heidelberg, 2018. Springer.
[FWX+ 17] Andrew Ferraiuolo, Yao Wang, Rui Xu, Danfeng Zhang, Andrew C. Myers, and G. Edward Suh. Full-processor
          timing channel protection with applications to secure hardware compartments. Technical report, Cornell University
          Library, 2017.
[FXZ+ 17] Andrew Ferraiuolo, Rui Xu, Danfeng Zhang, Andrew C. Myers, and G. Edward Suh. Verification of a practi-
          cal hardware security architecture through static information flow analysis. SIGARCH Comput. Archit. News,
          45(1):555–568, April 2017.
[Gal19]   Galois Inc. The Software Analysis Workbench. saw.galois.com/index.html, 2019. Accessed February 7 2019.
[GBW+ 17] Andrew Gacek, John Backes, Mike Whalen, Lucas G. Wagner, and Elaheh Ghassabani. The JKind model checker,
          2017.
[GDMJ16a] X. Guo, R. G. Dutta, P. Mishra, and Y. Jin. Automatic RTL-to-formal code converter for IP security formal
          verification. In 2016 17th International Workshop on Microprocessor and SOC Test and Verification (MTV),
          pages 35–38, 445 Hoes Lane Piscataway, NJ 08854 USA, Dec 2016. IEEE.
[GDMJ16b] X. Guo, R. G. Dutta, P. Mishra, and Y. Jin. Scalable SoC trust verification using integrated theorem proving
          and model checking. In 2016 IEEE International Symposium on Hardware Oriented Security and Trust (HOST),
          pages 124–129, 445 Hoes Lane Piscataway, NJ 08854 USA, May 2016. IEEE.
[GDMJ17] X. Guo, R. G. Dutta, P. Mishra, and Y. Jin. Automatic code converter enhanced PCH framework for SoC trust
          verification. IEEE Transactions on Very Large Scale Integration (VLSI) Systems, 25(12):3390–3400, Dec 2017.
[GdR+ 10] A.H. Ghamarian, M.J. de Mol, Arend Rensink, Eduardo Zambon, and M.V. Zimakova. Modelling and Analysis
          Using GROOVE. Number TR-CTIT-10-18 in CTIT Technical Report Series. Centre for Telematics and Information
          Technology (CTIT), Netherlands, 4 2010.
[GFLS11] Arjun Guha, Matthew Fredrikson, Benjamin Livshits, and Nikhil Swamy. Verified security for browser extensions.
          In 2011 IEEE symposium on security and privacy, pages 115–130, 445 Hoes Lane Piscataway, NJ 08854 USA,
          2011. IEEE.
[GGS10]   J. Octavio Gutierrez-Garcia and Kwang Sim. Agent-based service composition in cloud computing. volume 121,
          pages 1–10, 01 2010.
[GM84]    Shafi Goldwasser and Silvio Micali. Probabilistic encryption. Journal of computer and system sciences, 28(2):270–
          299, 1984.
[GNDB16] Roberto Guanciale, Hamed Nemati, Mads Dam, and Christoph Baumann. Provably secure memory isolation for
          Linux on ARM: Submission to special issue on verified information flow security. Journal of Computer Security,
          24:793–837, 12 2016.
[GR19]    Thomas Gibson-Robinson. FDR4: The CSP Refinement Checker. Oxford University Department of Computer
          Science, www.cs.ox.ac.uk/projects/fdr/, 2019.
[GSM+ 11] R. Gandhi, A. Sharma, W. Mahoney, W. Sousan, Q. Zhu, and P. Laplante. Dimensions of cyber-attacks: Cultural,
          social, economic, and political. IEEE Technology and Society Magazine, 30(1):28–38, Spring 2011.
[Hal05]   Anthony Hall. Realising the benefits of formal methods. In Kung-Kiu Lau and Richard Banach, editors, Formal
          Methods and Software Engineering, pages 1–4, Berlin, Heidelberg, 2005. Springer Berlin Heidelberg.
[Ham05]   Dick Hamlet. Invariants and state in testing and formal methods. SIGSOFT Softw. Eng. Notes, 31(1):48–51,
          September 2005.
[HB12a]   Daniel Hartung and Christoph Busch. Biometric transaction authentication protocol: Formal model verification and
          “four-eyes” principle extension. In George Danezis, Sven Dietrich, and Kazue Sako, editors, Financial Cryptography
          and Data Security, pages 88–103, Berlin, Heidelberg, 2012. Springer Berlin Heidelberg.
[HB12b]   Daniel Hartung and Christoph Busch. Biometric transaction authentication protocol: Formal model verification and
          “four-eyes” principle extension. In George Danezis, Sven Dietrich, and Kazue Sako, editors, Financial Cryptography
          and Data Security, pages 88–103, Berlin, Heidelberg, 2012. Springer Berlin Heidelberg.
[HH18]    Muluken Hailesellasie and Syed Rafay Hasan. Intrusion detection in PLC-based industrial control systems using
          formal verification approach in conjunction with graphs. Journal of Hardware and Systems Security, 2(1):1–14,
          Mar 2018.
[HK18]    Dominik Harz and William Knottenbelt. Towards safer smart contracts: A survey of languages and verification
          methods, 2018.
[HLC+ 13] Jianan Hao, Yang Liu, Wentong Cai, Guangdong Bai, and Jun Sun. vTRUST: A formal modeling and verification
          framework for virtualization systems. In Lindsay Groves and Jing Sun, editors, Formal Methods and Software
          Engineering, pages 329–346, Berlin, Heidelberg, 2013. Springer Berlin Heidelberg.
[Hoa78]   C. A. R. Hoare. Communicating Sequential Processes. Commun. ACM, 21(8):666–677, August 1978.
[Hoa85]   C. A. R. Hoare. Communicating Sequential Processes. Prentice-Hall, USA, 1985.
[HRG+ 18] Bo-Yuan Huang, Sayak Ray, Aarti Gupta, Jason M. Fung, and Sharad Malik. Formal security verification of
          concurrent firmware in SoCs using instruction-level abstraction for hardware. In Proceedings of the 55th Annual
          Design Automation Conference, DAC ’18, pages 91:1–91:6, New York, NY, USA, 2018. ACM.
[HSB+ 19] J. Heneghan, S. A. Shaikh, J. Bryans, M. Cheah, and P. Wooderson. Enabling security checking of automotive
          ECUs with formal CSP models. In 2019 49th Annual IEEE/IFIP International Conference on Dependable Systems
          and Networks Workshops (DSN-W), pages 90–97, 445 Hoes Lane Piscataway, NJ 08854 USA, June 2019. IEEE.
[HSR+ 18] E. Hildenbrandt, M. Saxena, N. Rodrigues, X. Zhu, P. Daian, D. Guth, B. Moore, D. Park, Y. Zhang, A. Stefanescu,
36                   T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



            and G. Rosu. KEVM: A complete formal semantics of the Ethereum virtual machine. In 2018 IEEE 31st Computer
            Security Foundations Symposium (CSF), pages 204–217, 445 Hoes Lane Piscataway, NJ 08854 USA, 2018. IEEE.
[IK06]      Daisuke Inoue and Masahiro Kuroda. Secure service framework on mobile ethernet. Journal of the National
            Institute of Information and Communications Technology, 53:61–71, 12 2006.
[IMMS19]    G. Iadarola, F. Martinelli, F. Mercaldo, and A. Santone. Formal methods for Android banking malware analysis
            and detection. In 2019 Sixth International Conference on Internet of Things: Systems, Management and Security
            (IOTSMS), pages 331–336, 445 Hoes Lane Piscataway, NJ 08854 USA, 2019. IEEE.
[ISCM17]    Fahad Ibrar, Hamza Saleem, Sam Castle, and Muhammad Zubair Malik. A study of static analysis tools to detect
            vulnerabilities of branchless banking applications in developing countries. In Proceedings of the Ninth International
            Conference on Information and Communication Technologies and Development, ICTD ’17, New York, NY, USA,
            2017. Association for Computing Machinery.
[ITS91]     ITSEC. Information Technology Security Evaluation Criteria (ITSEC): Preliminary harmonised criteria. Document
            COM(90) 314, Version 1.2, Commission of the European Communities, June 1991.
[Jac00]     Daniel Jackson. Automating first-order relational logic. Proceedings of the ACM SIGSOFT Symposium on the
            Foundations of Software Engineering, 25, 09 2000.
[Jac12]     Daniel Jackson. Software Abstractions: Logic, Language, and Analysis. The MIT Press, Cambridge, Massachusetts,
            United States, 2012.
[JBOK14]    Karthick Jayaraman, Nikolaj Bjørner, Geoff Outhred, and Charlie Kaufman. Automated Analysis and Debugging
            of Network Connectivity Policies. Technical report, MSR, Seattle, WA, USA, Tech. Rep. MSR-TR-2014-102, 2014.
[JED+ 12]   Y. Jarraya, A. Eghtesadi, M. Debbabi, Y. Zhang, and M. Pourzandi. Cloud calculus: Security verification in elastic
            cloud computing platform. In 2012 International Conference on Collaboration Technologies and Systems (CTS),
            pages 447–454, 445 Hoes Lane Piscataway, NJ 08854 USA, May 2012. IEEE.
[JK09]      Kurt Jensen and Lars M. Kristensen. Coloured Petri Nets: Modelling and Validation of Concurrent Systems.
            Springer Publishing Company, Incorporated, Berlin, Heidelberg, 1st edition, 2009.
[JKW07]     Kurt Jensen, Lars Michael Kristensen, and Lisa Marie Wells. Coloured Petri nets and CPN tools for modelling and
            validation of concurrent systems. International Journal on Software Tools for Technology Transfer, 9(3/4):213–254,
            2007.
[JRVP08]    Katalin Tünde Jánosi-Rancz, Viorica Varga, and Janos Puskas. A software tool for data analysis based on formal
            concept analysis. Studia Univ. Babes-Bolyai, Informatica, 53(2):67–78, 01 2008.
[JTL12a]    Dongseok Jang, Zachary Tatlock, and Sorin Lerner. Establishing browser security guarantees through formal shim
            verification. In Proceedings of the 21st USENIX Conference on Security Symposium, Security’12, page 8, USA,
            2012. USENIX Association.
[JTL12b]    Dongseok Jang, Zachary Tatlock, and Sorin Lerner. Establishing browser security guarantees through formal shim
            verification. In Presented as part of the 21st USENIX Security Symposium (USENIX Security 12), pages 113–128,
            Bellevue, WA, 2012. USENIX.
[Jül02]    Richard Jüllig. Formal methods in enterprise computing. In Chris George and Huaikou Miao, editors, Formal
            Methods and Software Engineering, pages 22–23, Berlin, Heidelberg, 2002. Springer Berlin Heidelberg.
[JW96]      Daniel Jackson and Jeanette Wing. Lightweight formal methods. IEEE Computer, 29(4):22–23, April 1996.
[KAE+ 10]   Gerwin Klein, June Andronick, Kevin Elphinstone, Gernot Heiser, David Cock, Philip Derrin, Dhammika Elkaduwe,
            Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and Simon Winwood. seL4: Formal
            verification of an operating-system kernel. Commun. ACM, 53(6):107–115, 2010.
[KB10]      Simon Kramer and Julian C Bradfield. A general definition of malware. Journal in computer virology, 6(2):105–114,
            2010.
[KBG+ 17]   P. Kumar, A. Braeken, A. Gurtov, J. Iinatti, and P. H. Ha. Anonymous secure framework in connected smart
            home environments. IEEE Transactions on Information Forensics and Security, 12(4):968–979, April 2017.
[KCKB14]    Corey Kallenberg, Sam Cornwell, Xeno Kovah, and John Butterworth. Setup for failure: Defeating secure boot.
            The MITRE Corporation, 2014.
[Ken15]     Michael Kenney. Cyber-terrorism in a post-Stuxnet world. Orbis, 59, 12 2015.
[KHF+ 19]   P. Kocher, J. Horn, A. Fogh, D. Genkin, D. Gruss, W. Haas, M. Hamburg, M. Lipp, S. Mangard, T. Prescher,
            M. Schwarz, and Y. Yarom. Spectre attacks: Exploiting speculative execution. In 2019 IEEE Symposium on
            Security and Privacy (SP), pages 1–19, 445 Hoes Lane Piscataway, NJ 08854 USA, 2019. IEEE.
[KHLF10]    H. Khurana, M. Hadley, N. Lu, and D. A. Frincke. Smart-grid security issues. IEEE Security Privacy, 8(1):81–85,
            Jan 2010.
[KI16]      Srinivasa Rao Kotipalli and Mohammed A Imran. Hacking Android. Packt Publishing Ltd, UK, 2016.
[KKG19]     N. Kumar, V. Kumar, and M. Gaur. Banking trojans APK detection using formal methods. In 2019 4th Inter-
            national Conference on Information Systems and Computer Networks (ISCON), pages 606–609, 445 Hoes Lane
            Piscataway, NJ 08854 USA, 2019. IEEE.
[KKHE17]    S. Kottler, M. Khayamy, S. R. Hasan, and O. Elkeelany. Formal verification of ladder logic programs using NuSMV.
            In SoutheastCon 2017, pages 1–5, 445 Hoes Lane Piscataway, NJ 08854 USA, March 2017. IEEE.
[KLSB11]    Stefan Kupferschmid, Matthew Lewis, Tobias Schubert, and Bernd Becker. Incremental preprocessing methods for
            use in BMC. Formal Methods in System Design, 39(2):185–204, 2011.
[KNP11]     M. Kwiatkowska, G. Norman, and D. Parker. PRISM 4.0: Verification of probabilistic real-time systems. In
            G. Gopalakrishnan and S. Qadeer, editors, Proc. 23rd International Conference on Computer Aided Verification
            (CAV’11), volume 6806 of LNCS, pages 585–591. Springer, 2011.
[Koz83]     Dexter Kozen. Results on the propositional µ-calculus. Theoretical Computer Science, 27(3):333 – 354, 1983. Special
            Issue Ninth International Colloquium on Automata, Languages and Programming (ICALP) Aarhus, Summer 1982.
A Survey of Practical Formal Methods for Security                                                                        37



[KPCBH15] Siwar Kriaa, Ludovic Pietre-Cambacedes, Marc Bouissou, and Yoran Halgand. A survey of approaches combining
          safety and security for industrial control systems. Reliability Engineering & System Safety, 139:156 – 178, 2015.
[KS13]    Robert Künnemann and Graham Steel. YubiSecure? Formal security analysis results for the Yubikey and YubiHSM.
          In Audun Jøsang, Pierangela Samarati, and Marinella Petrocchi, editors, Security and Trust Management, pages
          257–272, Berlin, Heidelberg, 2013. Springer Berlin Heidelberg.
[KS15]    Sheetal Kalra and Sandeep K. Sood. Secure authentication scheme for IoT and cloud servers. Pervasive and Mobile
          Computing, 24:210 – 223, 2015. Special Issue on Secure Ubiquitous Computing.
[KsM02]   Vorapranee Khu-smith and Chris J. Mitchell. Using EMV cards to protect e-commerce transactions. In Proceedings
          of the Third International Conference on E-Commerce and Web Technologies, EC-WEB ’02, page 388–399, Berlin,
          Heidelberg, 2002. Springer-Verlag.
[KTJB19] Tomas Kulik, Peter W. V. Tran-Jørgensen, and Jalil Boudjadar. Formal security analysis of cloud-connected
          industrial control systems. In Jean-Louis Lanet and Cristian Toma, editors, Innovative Security Solutions for
          Information Technology and Communications, pages 71–84, Cham, 2019. Springer International Publishing.
[Kum14]   Apurva Kumar. A lightweight formal approach for analyzing security of web protocols. In International Workshop
          on Recent Advances in Intrusion Detection, pages 192–211. Springer, 2014.
[Lam02]   Leslie Lamport. Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers.
          Addison-Wesley Longman Publishing Co., Inc., Boston, MA, USA, 2002.
[Lam09]   Leslie Lamport. The PlusCal Algorithm Language. In Martin Leucker and Carroll Morgan, editors, Theoretical
          Aspects of Computing - ICTAC 2009, pages 36–60, Berlin, Heidelberg, 2009. Springer Berlin Heidelberg.
[LBF+ 10] Peter Gorm Larsen, Nick Battle, Miguel Ferreira, John Fitzgerald, Kenneth Lausdahl, and Marcel Verhoef. The
          Overture initiative integrating tools for VDM. ACM SIGSOFT Software Engineering Notes, 35(1):1–6, 2010.
[LCH+ 16] Thomas Letan, Pierre Chifflier, Guillaume Hiet, Pierre Neron, and Benjamin Morin. SpecCert: Specifying and
          verifying hardware-based security enforcement. volume 9995, pages 496–512, 11 2016.
[LFBP14] Lee W. Lerner, Zane R. Franklin, William T. Baumann, and Cameron D. Patterson. Using high-level synthesis
          and formal analysis to predict and preempt attacks on industrial control systems. In Proceedings of the 2014
          ACM/SIGDA International Symposium on Field-Programmable Gate Arrays, FPGA ’14, page 209–212, New
          York, NY, USA, 2014. Association for Computing Machinery.
[LHB+ 96] P. G. Larsen, B. S. Hansen, H. Brunn, N. Plat, H. Toetenel, D. J. Andrews, J. Dawes, G. Parkin, et al. Information
          technology – Programming languages, their environments and system software interfaces – Vienna Development
          Method – Specification Language – Part 1: Base language, December 1996.
[Lin15]   Yu-Cheng Lin. Androbugs framework: An android application security vulnerability scanner, 2015.
[LJM11]   E. Love, Y. Jin, and Y. Makris. Enhancing security via provably trustworthy hardware intellectual property.
          In 2011 IEEE International Symposium on Hardware-Oriented Security and Trust, pages 12–17, 445 Hoes Lane
          Piscataway, NJ 08854 USA, June 2011. IEEE.
[LLB10]   Peter Gorm Larsen, Kenneth Lausdahl, and Nick Battle. Combinatorial Testing for VDM. In Proceedings of the
          2010 8th IEEE International Conference on Software Engineering and Formal Methods, SEFM ’10, pages 278–285,
          Washington, DC, USA, September 2010. IEEE Computer Society. ISBN 978-0-7695-4153-2.
[Low95]   Gavin Lowe. An attack on the Needham-Schroeder public-key authentication protocol. Inf. Process. Lett.,
          56(3):131–133, 1995.
[LPY97]   Kim G. Larsen, Paul Pettersson, and Wang Yi. Uppaal in a nutshell. International Journal on Software Tools for
          Technology Transfer, 1(1):134–152, Dec 1997.
[LQL12]   Akash Lal, Shaz Qadeer, and Shuvendu K. Lahiri. A solver for reachability modulo theories. In P. Madhusudan
          and Sanjit A. Seshia, editors, Computer Aided Verification - 24th International Conference, CAV 2012, Berkeley,
          CA, USA, July 7-13, 2012 Proceedings, volume 7358 of Lecture Notes in Computer Science, pages 427–443, Berlin,
          Heidelberg, 2012. Springer.
[LS99]    S. Lu and S. A. Smolka. Model checking the secure electronic transaction (SET) protocol. In MASCOTS ’99.
          Proceedings of the Seventh International Symposium on Modeling, Analysis and Simulation of Computer and
          Telecommunication Systems, pages 358–364, 445 Hoes Lane Piscataway, NJ 08854 USA, 1999. IEEE.
[MAH15]   Jackson R Mayo, Robert C Armstrong, and Geoffrey C Hulette. Digital system robustness via design constraints:
          The lesson of formal methods. In 2015 Annual IEEE Systems Conference (SysCon) Proceedings, pages 109–114,
          445 Hoes Lane Piscataway, NJ 08854 USA, 2015. IEEE.
[MAHvM16] Maryam Mehrnezhad, Mohammed Aamir Ali, Feng Hao, and Aad van Moorsel. NFC payment spy: A privacy attack
          on contactless payments. In Lidong Chen, David McGrew, and Chris Mitchell, editors, Security Standardisation
          Research, pages 92–111, Cham, 2016. Springer International Publishing.
[MCJ18]   Andrew Miller, Zhicheng Cai, and Somesh Jha. Smart contracts and opportunities for formal methods. In Tiziana
          Margaria and Bernhard Steffen, editors, Leveraging Applications of Formal Methods, Verification and Validation.
          Industrial Practice, pages 280–299, Cham, 2018. Springer International Publishing.
[Mes00]   José Meseguer. Rewriting logic and Maude: A wide-spectrum semantic framework for object-based distributed
          systems. In Scott F. Smith and Carolyn L. Talcott, editors, Formal Methods for Open Object-Based Distributed
          Systems IV, pages 89–117, Boston, MA, 2000. Springer US.
[MGP16]   N. E. Madhoun, F. Guenane, and G. Pujolle. An online security protocol for NFC payment: Formally analyzed by
          the Scyther tool. In 2016 Second International Conference on Mobile and Secure Services (MobiSecServ), pages
          1–7, 445 Hoes Lane Piscataway, NJ 08854 USA, 2016. IEEE.
[Mil89]   R. Milner. Communication and Concurrency. Prentice-Hall, Inc., USA, 1989.
[MJA+ 18] Taous Madi, Yosr Jarraya, Amir Alimohammadifar, Suryadipta Majumdar, Yushun Wang, Makan Pourzandi,
          Lingyu Wang, and Mourad Debbabi. ISOTOP: Auditing virtual networks isolation across cloud layers in OpenStack.
          ACM Trans. Priv. Secur., 22(1), October 2018.
38                   T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



[MLHK14] Fatma Masmoudi, Monia Loulou, and Ahmed Hadj Kacem. Formal security framework for agent based cloud
          systems. 11 2014.
[MML12]   R. Moreno-Vozmediano, R. S. Montero, and I. M. Llorente. IaaS cloud architecture: From virtualized datacenters
          to federated cloud infrastructures. Computer, 45(12):65–72, 2012.
[MMN18] Fabio Martinelli, Francesco Mercaldo, and Vittoria Nardone. Identifying insecure features in android applications
          using model checking. In Paolo Mori, Steven Furnell, and Olivier Camp, editors, Proceedings of the 4th International
          Conference on Information Systems Security and Privacy, ICISSP 2018, Funchal, Madeira - Portugal, January
          22-24, 2018, pages 589–596. SciTePress, 2018.
[MMS19]   F. Mercaldo, F. Martinelli, and A. Santone. Real-time SCADA attack detection by means of formal methods. In
          2019 IEEE 28th International Conference on Enabling Technologies: Infrastructure for Collaborative Enterprises
          (WETICE), pages 231–236, 445 Hoes Lane Piscataway, NJ 08854 USA, June 2019. IEEE.
[MNSV16] Francesco Mercaldo, Vittoria Nardone, Antonella Santone, and Corrado Aaron Visaggio. Download malware? No,
          thanks: How formal methods can block update attacks. In Proceedings of the 4th FME Workshop on Formal
          Methods in Software Engineering, FormaliSE ’16, pages 22–28, New York, NY, USA, 2016. ACM.
[MO15]    Hugo Daniel Macedo and José Nuno Oliveira. A linear algebra approach to OLAP. Formal Aspects of Computing,
          27(2):283–307, 2015.
[MPS19]   Antonio Marcedone, Rafael Pass, and Abhi Shelat. Minimizing trust in hardware wallets with two factor signatures.
          In Ian Goldberg and Tyler Moore, editors, Financial Cryptography and Data Security, pages 407–425, Cham, 2019.
          Springer International Publishing.
[MPX+ 13] Haohui Mai, Edgar Pek, Hui Xue, Samuel Talmadge King, and Parthasarathy Madhusudan. Verifying security
          invariants in ExpressOS. In Proceedings of the Eighteenth International Conference on Architectural Support
          for Programming Languages and Operating Systems, ASPLOS ’13, page 293–304, New York, NY, USA, 2013.
          Association for Computing Machinery.
[MSCB13] Simon Meier, Benedikt Schmidt, Cas Cremers, and David Basin. The TAMARIN prover for the symbolic anal-
          ysis of security protocols. In Natasha Sharygina and Helmut Veith, editors, Computer Aided Verification: 25th
          International Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013, Proceedings, volume 8044 of
          Lecture Notes in Computer Science, pages 696 – 701, Berlin, 2013. Springer. Computer Aided Verification: 25th
          International Conference (CAV 2013); Conference Location: Saint Petersburg, Russia; Conference Date: July 13-19,
          2013; .
[MSHA17] M. Mohsin, M. U. Sardar, O. Hasan, and Z. Anwar. IoTRiskAnalyzer: A probabilistic model checking based
          framework for formal risk analytics of the internet of things. IEEE Access, 5:5494–5505, 2017.
[MT13]    Hugo Daniel Macedo and Tayssir Touili. Mining malware specifications through static reachability analysis. In Eu-
          ropean Symposium on Research in Computer Security, pages 517–535, Berlin, Heidelberg, 2013. Springer, Springer
          Berlin Heidelberg.
[MTT+ 12] Greg Morrisett, Gang Tan, Joseph Tassarotti, Jean-Baptiste Tristan, and Edward Gan. RockSalt: Better, faster,
          stronger SFI for the X86. In Proceedings of the 33rd ACM SIGPLAN Conference on Programming Language
          Design and Implementation, PLDI ’12, page 395–404, New York, NY, USA, 2012. Association for Computing
          Machinery.
[MW08]    Sascha Mühlbach and Sebastian Wallner. Secure communication in microcomputer bus systems for embedded
          devices. Journal of Systems Architecture, 54(11):1065 – 1076, 2008. Embedded Systems: Architectures, Modeling
          and Simulation.
[Nec11]   George C. Necula. Proof-carrying code. In Henk C. A. van Tilborg and Sushil Jajodia, editors, Encyclopedia of
          Cryptography and Security, 2nd Ed, pages 984–986. Springer, Berlin, Heidelberg, 2011.
[NFV15]   P. J. C. Nunes, J. Fonseca, and M. Vieira. phpSAFE: A security analysis tool for OOP web application plugins.
          In 2015 45th Annual IEEE/IFIP International Conference on Dependable Systems and Networks, pages 299–306,
          445 Hoes Lane Piscataway, NJ 08854 USA, June 2015. IEEE.
[NGB+ 16] Roberto Nardone, Ugo Gentile, Massimo Benerecetti, Adriano Peron, Valeria Vittorini, Stefano Marrone, and
          Nicola Mazzocca. Modeling railway control systems in Promela. In Cyrille Artho and Peter Csaba Ölveczky, editors,
          Formal Techniques for Safety-Critical Systems, pages 121–136, Cham, 2016. Springer International Publishing.
[NGP+ 15] Roberto Nardone, Ugo Gentile, Adriano Peron, Massimo Benerecetti, Valeria Vittorini, Stefano Marrone, Renato
          De Guglielmo, Nicola Mazzocca, and Luigi Velardi. Dynamic state machines for formalizing railway control system
          specifications. In Cyrille Artho and Peter Csaba Ölveczky, editors, Formal Techniques for Safety-Critical Systems,
          pages 93–109, Cham, 2015. Springer International Publishing.
[NK14]    Tobias Nipkow and Gerwin Klein. Concrete Semantics — With Isabelle/HOL. Springer, Berlin, 2014.
[NMB+ 16] B. Ngabonziza, D. Martin, A. Bailey, H. Cho, and S. Martin. Trustzone explained: Architectural features and
          use cases. In 2016 IEEE 2nd International Conference on Collaboration and Internet Computing (CIC), pages
          445–451, 445 Hoes Lane Piscataway, NJ 08854 USA, Nov 2016. IEEE.
[NPYG09] Matias Negrete-Pincetic, Felipe Yoshida, and George Gross. Towards quantifying the impacts of cyber attacks in
          the competitive electricity market environment. In 2009 IEEE Bucharest PowerTech, pages 1–8, 445 Hoes Lane
          Piscataway, NJ 08854 USA, 08 2009. IEEE.
[NRM16]   R. Nardone, R. J. Rodrı́guez, and S. Marrone. Formal security assessment of Modbus protocol. In 2016 11th
          International Conference for Internet Technology and Secured Transactions (ICITST), pages 142–147, 445 Hoes
          Lane Piscataway, NJ 08854 USA, Dec 2016. IEEE.
[NS78]    Roger M. Needham and Michael D. Schroeder. Using encryption for authentication in large networks of computers.
          Commun. ACM, 21(12):993–999, 1978.
[NT19]    V. Nigam and C. Talcott. Formal security verification of Industry 4.0 applications. In 2019 24th IEEE International
A Survey of Practical Formal Methods for Security                                                                          39



           Conference on Emerging Technologies and Factory Automation (ETFA), pages 1043–1050, Zaragoza, Spain, Sep.
           2019. IEEE.
[OH18]     Peter W. O Hearn. Continuous reasoning: Scaling the impact of formal methods. In Proceedings of the 33rd
           Annual ACM/IEEE Symposium on Logic in Computer Science, LICS ’18, page 13–25, New York, NY, USA, 2018.
           Association for Computing Machinery.
[OKQ17]    Iqra Obaid, Syed Kazmi, and Awais Qasim. Modeling and verification of payment system in E-banking. Interna-
           tional Journal of Advanced Computer Science and Applications, 8, 01 2017.
[PPL16]    Maxime Puys, Marie-Laure Potet, and Pascal Lafourcade. Formal analysis of security properties on the OPC-UA
           SCADA protocol. In Amund Skavhaug, Jérémie Guiochet, and Friedemann Bitsch, editors, Computer Safety,
           Reliability, and Security, pages 67–75, Cham, 2016. Springer International Publishing.
[Pri06]    Uta Priss. Formal concept analysis in information science. Annual Review of Information Science and Technology,
           40, 01 2006.
[Put94]    Martin L. Puterman. Markov Decision Processes: Discrete Stochastic Dynamic Programming. John Wiley & Sons,
           Inc., USA, 1st edition, 1994.
[PZS+ 18a] Daejun Park, Yi Zhang, Manasvi Saxena, Philip Daian, and Grigore Roşu. A formal verification tool for Ethereum
           VM bytecode. In Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference
           and Symposium on the Foundations of Software Engineering, ESEC/FSE 2018, page 912–915, New York, NY,
           USA, 2018. Association for Computing Machinery.
[PZS+ 18b] Daejun Park, Yi Zhang, Manasvi Saxena, Philip Daian, and Grigore Roundefinedu. A formal verification tool for
           Ethereum VM bytecode. In Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering
           Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2018, page 912–915, New
           York, NY, USA, 2018. Association for Computing Machinery.
[QCG+ 09] Morgan Quigley, Ken Conley, Brian P. Gerkey, Josh Faust, Tully Foote, Jeremy Leibs, Rob Wheeler, and Andrew Y.
           Ng. ROS: An open-source robot operating system, 2009.
[QPP+ 17] Davide Quarta, Marcello Pogliani, Mario Polino, Federico Maggi, Andrea Maria Zanchettin, and Stefano Zanero.
           An experimental security analysis of an industrial robot controller. In 2017 IEEE Symposium on Security and
           Privacy (SP), pages 268–286, 445 Hoes Lane Piscataway, NJ 08854 USA, 05 2017. IEEE.
[RCD+ 17] S. Roy, S. Chatterjee, A. K. Das, S. Chattopadhyay, N. Kumar, and A. V. Vasilakos. On the design of provably
           secure lightweight remote user authentication scheme for mobile cloud computing services. IEEE Access, 5:25808–
           25825, 2017.
[RCD+ 19] Awais Rashid, Howard Chivers, George Danezis, Emil Lupu, and Andrew Martin, editors. The Cyber Security
           Body of Knowledge. www.cybok.org, 2019.
[RE14]     Zvonimir Rakamaric and Michael Emmi. SMACK: Decoupling source language details from verifier implementa-
           tions. In Armin Biere and Roderick Bloem, editors, Computer Aided Verification - 26th International Conference,
           CAV 2014, Held as Part of the Vienna Summer of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014. Proceed-
           ings, volume 8559 of Lecture Notes in Computer Science, pages 106–113, Berlin, Heidelberg, 2014. Springer.
[RLS13]    M. Roland, J. Langer, and J. Scharinger. Applying relay attacks to Google Wallet. In 2013 5th International
           Workshop on Near Field Communication (NFC), pages 1–6, 445 Hoes Lane Piscataway, NJ 08854 USA, 2013.
           IEEE.
[RRS13]    O. Rysavy, J. Rab, and M. Sveda. Improving security in SCADA systems through firewall policy analysis. In 2013
           Federated Conference on Computer Science and Information Systems, pages 1435–1440, 445 Hoes Lane Piscataway,
           NJ 08854 USA, Sep. 2013. IEEE.
[RSB+ 15] R. Rana, M. Staron, C. Berger, A. Nilsson, R. Scandariato, A. Weilenmann, and M. Rydmark. On the role of
           cross-disciplinary research and SSE in addressing the challenges of the digitalization of society. In 2015 6th IEEE
           International Conference on Software Engineering and Service Science (ICSESS), pages 1106–1109, Beijing, China,
           September 2015. IEEE.
[RSG+ 01] Peter Y. A. Ryan, Steve Schneider, Michael Goldsmith, Gavin Lowe, and Bill Roscoe. Modelling and analysis of
           security protocols. Addison-Wesley-Longman, USA, 2001.
[RT16]     Marco Rocchetto and Nils Ole Tippenhauer. CPDY: extending the dolev-yao attacker with physical-layer interac-
           tions, 2016.
[RT17]     Marco Rocchetto and Nils Ole Tippenhauer. Towards formal security analysis of industrial control systems. In
           Proceedings of the 2017 ACM on Asia Conference on Computer and Communications Security, ASIA CCS ’17,
           pages 114–126, New York, NY, USA, 2017. ACM.
[RZR+ 13] R. Rieke, M. Zhdanova, J. Repp, R. Giot, and C. Gaber. Fraud detection in mobile payments utilizing process
           behavior analysis. In 2013 International Conference on Availability, Reliability and Security, pages 662–669, 445
           Hoes Lane Piscataway, NJ 08854 USA, 2013. IEEE.
[SAE+ 18] Caitlin Sadowski, Edward Aftandilian, Alex Eagle, Liam Miller-Cushon, and Ciera Jaspan. Lessons from building
           static analysis tools at Google. Commun. ACM, 61(4):58–66, March 2018.
[SAS+ 18] J. Sepulveda, D. Aboul-Hassan, G. Sigl, B. Becker, and M. Sauer. Towards the formal verification of security
           properties of a network-on-chip router. In 2018 IEEE 23rd European Test Symposium (ETS), pages 1–6, 445 Hoes
           Lane Piscataway, NJ 08854 USA, May 2018. IEEE.
[SBL18]    S. Souaf, P. Berthome, and F. Loulergue. A cloud brokerage solution: Formal methods meet security in cloud
           federations. In 2018 International Conference on High Performance Computing Simulation (HPCS), pages 691–
           699, 2018.
[SC16]     Eric Smith and Alessandro Coglio. Android platform modeling and Android app verification in the ACL2 theorem
           prover. In Arie Gurfinkel and Sanjit A. Seshia, editors, Verified Software: Theories, Tools, and Experiments, pages
           183–201, Cham, 2016. Springer International Publishing.
40                   T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



[SCK+ 12] Julien Signoles, Pascal Cuoq, Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, and Boris Yakobowski. Frama-
          C: A software analysis perspective. Formal Aspects of Computing, 27, 10 2012.
[SCW00]   Susan Stepney, David Cooper, and Jim Woodcock. An electronic purse: Specification, refinement, and proof.
          Technical Monograph PRG-126, Oxford University Computing Laboratory, July 2000.
[SGR09]   N. Santos, Krishna P. Gummadi, and Rodrigo Rodrigues. Towards trusted cloud computing. In HotCloud’09:
          Proceedings of the 2009 Conference on Hot Topics in Cloud Computing, number 9, page 3, USA, 01 2009. USENIX
          Association.
[SIR13]   Antonella Santone, Valentina Intilangelo, and Domenico Raucci. Efficient formal verification in banking processes.
          In 2013 IEEE Ninth World Congress on Services, pages 325–332, 445 Hoes Lane Piscataway, NJ 08854 USA, 2013.
          IEEE.
[SJL+ 15] Jinho Seol, Seongwook Jin, Daewoo Lee, Jaehyuk Huh, and Seungryoul Maeng. A trusted iaas environment with
          hardware security module. IEEE Transactions on Services Computing, 9:1–1, 01 2015.
[SKMT12] Ralf Sasse, Samuel T King, José Meseguer, and Shuo Tang. IBOS: A correct-by-construction modular browser.
          In International Workshop on Formal Aspects of Component Software, pages 224–241, Berlin, Heidelberg, 2012.
          Springer.
[SLBK14] R. Skowyra, A. Lapets, A. Bestavros, and A. Kfoury. A verification platform for SDN-enabled applications. In
          2014 IEEE International Conference on Cloud Engineering, pages 337–342, 445 Hoes Lane Piscataway, NJ 08854
          USA, March 2014. IEEE.
[SLD08]   Jun Sun, Yang Liu, and Jin Song Dong. Model checking CSP revisited: Introducing a process analysis toolkit.
          In Tiziana Margaria and Bernhard Steffen, editors, Leveraging Applications of Formal Methods, Verification and
          Validation, pages 307–322, Berlin, Heidelberg, 2008. Springer Berlin Heidelberg.
[SLDC09] J. Sun, Y. Liu, J. S. Dong, and C. Chen. Integrating specification and programs for system modeling and verification.
          In 2009 Third IEEE International Symposium on Theoretical Aspects of Software Engineering, pages 127–135, 445
          Hoes Lane Piscataway, NJ 08854 USA, 2009. IEEE.
[SLZ13]   Yuchao She, Hui Li, and Hui Zhu. UVHM: Model checking based formal analysis scheme for hypervisors. In Khabib
          Mustofa, Erich J. Neuhold, A. Min Tjoa, Edgar Weippl, and Ilsun You, editors, Information and Communication
          Technology, pages 300–305, Berlin, Heidelberg, 2013. Springer Berlin Heidelberg.
[SMX18]   Roshan Shrestha, Hoda Mehrpouyan, and Dianxiang Xu. Model checking of security properties in industrial
          control systems (ICS). In Proceedings of the Eighth ACM Conference on Data and Application Security and
          Privacy, CODASPY ’18, page 164–166, New York, NY, USA, 2018. Association for Computing Machinery.
[Sne91]   E. Snekkenes. Exploring the BAN approach to protocol analysis. In Proceedings. 1991 IEEE Computer Society
          Symposium on Research in Security and Privacy, pages 171–181, Oakland, CA, USA, may 1991. IEEE.
[Spi89]   J.M. Spivey. The Z Notation: A Reference Manual. Prentice-Hall, USA, 1989.
[SPSK17] Irfan Siddavatam, Sachin Parekh, Tanay Shah, and Faruk Kazi. Testing and validation of Modbus/TCP protocol
          for secure SCADA communication in CPS using formal methods. Scalable Computing: Practice and Experience,
          18, 11 2017.
[SPY+ 16] Andrei Stefanescu, Daejun Park, Shijiao Yuwen, Yilong Li, and Grigore Roundefinedu. Semantics-based program
          verifiers for all languages. In Proceedings of the 2016 ACM SIGPLAN International Conference on Object-Oriented
          Programming, Systems, Languages, and Applications, OOPSLA 2016, page 74–91, New York, NY, USA, 2016.
          Association for Computing Machinery.
[ST12]    Fu Song and Tayssir Touili. Efficient malware detection using model-checking. In International Symposium on
          Formal Methods, pages 418–433, Berlin, Heidelberg, 2012. Springer, Springer Berlin Heidelberg.
[ST14a]   Fu Song and Tayssir Touili. Model-checking for Android malware detection. In Jacques Garrigue, editor, Program-
          ming Languages and Systems, pages 216–235, Cham, 2014. Springer International Publishing.
[ST14b]   Fu Song and Tayssir Touili. Pushdown model checking for malware detection. International Journal on Software
          Tools for Technology Transfer, 16(2):147–173, 2014.
[SWA+ 12] C. Steward Jr., L. A. Wahsheh, A. Ahmad, J. M. Graham, C. V. Hinds, A. T. Williams, and S. J. DeLoatch. Software
          security: The dangerous afterthought. In 2012 Ninth International Conference on Information Technology - New
          Generations, pages 815–818, 445 Hoes Lane Piscataway, NJ 08854 USA, April 2012. IEEE.
[Tea19]   The Coq Development Team. The Coq Reference Manual. LogiCal Project, January 2019. Version 8.9.1.
[TJ07]    Emina Torlak and Daniel Jackson. Kodkod: A relational model finder. In Orna Grumberg and Michael Huth,
          editors, Tools and Algorithms for the Construction and Analysis of Systems, pages 632–647, Berlin, Heidelberg,
          2007. Springer Berlin Heidelberg.
[TJK19]   Peter Würtz Vinther Tran-Jørgensen and Tomas Kulik. Migrating Overture to a different IDE. In Carl Gamble and
          Luis Diogo Couto, editors, Proceedings of the 17th Overture Workshop, number CS-TR- 1530 - 2019 in Technical
          Report Series, pages 32–47, UK, 2019. Newcastle University.
[TJKBL19] Peter W. V. Tran-Jørgensen, Tomas Kulik, Jalil Boudjadar, and Peter Gorm Larsen. Security analysis of cloud-
          connected industrial control systems using combinatorial testing. In Proceedings of the 17th ACM-IEEE Interna-
          tional Conference on Formal Methods and Models for System Design, MEMOCODE ’19, New York, NY, USA,
          2019. Association for Computing Machinery.
[TM17]    Vincent F. Taylor and Ivan Martinovic. Short paper: A longitudinal study of financial apps in the Google Play
          Store. In Aggelos Kiayias, editor, Financial Cryptography and Data Security, pages 302–309, Cham, 2017. Springer
          International Publishing.
[TP16]    Farid Molazem Tabrizi and Karthik Pattabiraman. Formal security analysis of smart embedded systems. In
          Proceedings of the 32nd Annual Conference on Computer Security Applications, ACSAC ’16, page 1–15, New
          York, NY, USA, 2016. Association for Computing Machinery.
[TSS16]   K. Tsukada, K. Sawada, and S. Shin. A toolchain on model checking SPIN via Kalman decomposition for control
A Survey of Practical Formal Methods for Security                                                                       41



          system software. In 2016 IEEE International Conference on Automation Science and Engineering (CASE), pages
          300–305, 445 Hoes Lane Piscataway, NJ 08854 USA, Aug 2016. IEEE.
[TTB08]   Naoyuki Tamura, Tomoya Tanjo, and Mutsunori Banbara. System description of a SAT-based CSP solver Sugar,
          01 2008.
[Tur06]   Mathieu Turuani. The CL-Atse protocol analyser. In Frank Pfenning, editor, Term Rewriting and Applications,
          pages 277–286, Berlin, Heidelberg, 2006. Springer Berlin Heidelberg.
[TVR16]   Mathieu Turuani, Thomas Voegtlin, and Michael Rusinowitch. Automated verification of Electrum wallet. In
          International Conference on Financial Cryptography and Data Security, pages 27–42, Berlin, Heidelberg, 2016.
          Springer.
[UA19]    Nils Urbach and Frederik Ahlemann. Digitalization as a Risk: Security and Business Continuity Management Are
          Central Cross-Divisional Functions of the Company, pages 85–92. Springer International Publishing, Cham, 2019.
     +
[VCJ 13] A. Vasudevan, S. Chaki, L. Jia, J. McCune, J. Newsome, and A. Datta. Design, implementation and verification
          of an eXtensible and modular hypervisor framework. In 2013 IEEE Symposium on Security and Privacy, pages
          430–444, 445 Hoes Lane Piscataway, NJ 08854 USA, May 2013. IEEE.
[VCM+ 16] Amit Vasudevan, Sagar Chaki, Petros Maniatis, Limin Jia, and Anupam Datta. überSpark: Enforcing verifiable
          object abstractions for automated compositional security analysis of a hypervisor. In 25th USENIX Security
          Symposium (USENIX Security 16), pages 87–104, Austin, TX, August 2016. USENIX Association.
[vOM12]   David von Oheimb and Sebastian Mödersheim. ASLan++ — A formal security specification language for dis-
          tributed systems. In Bernhard K. Aichernig, Frank S. de Boer, and Marcello M. Bonsangue, editors, Formal
          Methods for Components and Objects, pages 1–22, Berlin, Heidelberg, 2012. Springer Berlin Heidelberg.
[WANC16] M. Williams, L. Axon, J. R. C. Nurse, and S. Creese. Future scenarios and challenges for security and privacy. In
          2016 IEEE 2nd International Forum on Research and Technologies for Society and Industry Leveraging a better
          tomorrow (RTSI), pages 1–6, 445 Hoes Lane Piscataway, NJ 08854 USA, September 2016. IEEE.
[WD96]    Jim Woodcock and Jim Davies. Using Z: Specification, Refinement, and Proof. Prentice-Hall, USA, 1996.
[Wei11]   Sharon Weinberger. Computer security: Is this the start of cyberwarfare? Nature, 474:142–5, 06 2011.
[WGS+ 19] R. Wang, Y. Guan, H. Song, X. Li, X. Li, Z. Shi, and X. Song. A formal model-based design method for robotic
          systems. IEEE Systems Journal, 13(1):1096–1107, March 2019.
[Win90]   J. M. Wing. A specifier’s introduction to formal methods. Computer, 23(9):8–22, September 1990.
[Win98]   Jeannette M Wing. A symbiotic relationship between formal methods and security. In Proceedings Computer
          Security, Dependability, and Assurance: From Needs to Solutions (Cat. No. 98EX358), pages 26–38, 445 Hoes
          Lane Piscataway, NJ 08854 USA, 1998. IEEE.
[WMPO16] Dean C. Wardell, Robert F. Mills, Gilbert L. Peterson, and Mark E. Oxley. A Method for Revealing and Ad-
          dressing Security Vulnerabilities in Cyber-physical Systems by Modeling Malicious Agent Interactions with Formal
          Verification. Procedia Computer Science, 95:24–31, 2016. Complex Adaptive Systems Los Angeles, CA November
          2-4, 2016.
[WNH17]   Tobias Wich, Daniel Nemmert, and Detlef Hühnlein. Towards secure and standard-compliant implementations of
          the PSD2 directive. In Lothar Fritsch, Heiko Roßnagel, and Detlef Hühnlein, editors, Open Identity Summit 2017,
          October 5-6, 2017, Karlstad University, Sweden, volume P-277 of LNI, pages 63–80, Bonn, DE, 2017. Gesellschaft
          für Informatik.
[WSC+ 08] Jim Woodcock, Susan Stepney, David Cooper, John Clark, and Jeremy Jacob. The certification of the Mondex
          electronic purse to ITSEC Level E6. Formal Asp. Comput., 20(1):5–19, 2008.
[WSC17]   T. Wang, Q. Su, and T. Chen. Formal analysis of security properties of cyber-physical system based on timed
          automata. In 2017 IEEE Second International Conference on Data Science in Cyberspace (DSC), pages 534–540,
          2017.
[WZM12]   W. Wang, Q. Zeng, and A. P. Mathur. A security assurance framework combining formal verification and security
          functional testing. In 2012 12th International Conference on Quality Software, pages 136–139, 2012.
[XCWC13] Luyi Xing, Yangyi Chen, XiaoFeng Wang, and Shuo Chen. InteGuard: Toward automatic protection of third-party
          web service integrations. In 20th Annual Network and Distributed System Security Symposium, NDSS 2013, San
          Diego, California, USA, February 24-27, 2013, page 17, USA, 2013. The Internet Society.
[XWL14]   Meihua Xiao, Zilong Wan, and Hongling Liu. The formal verification and improvement of simplified SET protocol.
          Journal of Software, 9, 09 2014.
[YHXH05] Yu Zheng, D. He, Xiaohu Tang, and Hongxia Wang. AKA and authorization scheme for 4G mobile networks
          based on trusted mobile platform. In 2005 5th International Conference on Information Communications Signal
          Processing, pages 976–980, 2005.
[YJS+ 19] J. Yoo, Y. Jung, D. Shin, M. Bae, and E. Jee. Formal modeling and verification of a federated byzantine agreement
          algorithm for blockchain platforms. In 2019 IEEE International Workshop on Blockchain Oriented Software
          Engineering (IWBOSE), pages 11–21, 445 Hoes Lane Piscataway, NJ 08854 USA, 2019. IEEE.
[ZKWG16] Wen Zeng, Maciej Koutny, Paul Watson, and Vasileios Germanos. Formal verification of secure information flow
          in cloud computing. Journal of Information Security and Applications, 27:103–116, 2016.
[ZMSZ12] Wei Zhang, Wenke Ma, Huiling Shi, and Fu-qiang Zhu. Model checking and verification of the internet payment
          system with SPIN. JSW, 7(9):1941–1949, 2012.
[ZRM14]   S. Zonouz, J. Rrushi, and S. McLaughlin. Detecting industrial control malware using automated PLC code analytics.
          IEEE Security Privacy, 12(6):40–47, Nov 2014.
[ZWSM15] Danfeng Zhang, Yao Wang, G. Edward Suh, and Andrew C. Myers. A hardware design language for timing-
          sensitive information-flow security. In Proceedings of the Twentieth International Conference on Architectural
          Support for Programming Languages and Operating Systems, ASPLOS ’15, page 503–516, New York, NY, USA,
          2015. Association for Computing Machinery.
42                    T. Kulik, B. Dongol, P.G. Larsen, H.D. Macedo, S. Schneider, P.W.V. Tran-Jørgensen and J. Woodcock



APPENDIX
This appendix provides an overview of the several surveyed research works in the form of a cross-tabulation
according to [MO15]. We group the 115 covered references by Domain, Level Of Abstraction (LOA) and
Approach (App.).

         Domain         LOA               App.    Works
                                          MC      [CGHS17] [KKG19] [IMMS19] [TVR16]
                        Application
                                          TP      [AE18] [PZS+ 18a]
                                          LW      [ADRP13]
                        System
                                          MC      [AUS12] [OKQ17] [ZMSZ12] [SIR13] [YJS+ 19] [DMC+ 18]
                                          MC      [AMM14] [XWL14] [HB12a] [ABSW13] [BS15]
                        Protocol
         Financial                        TP      [MGP16]
                                          LW      [ISCM17] [TM17] [Fre18]
                        Implementation    MC      [ADMM14]
                                          TP      [FHK19]
                                          MC      [ABK+ 19] [CGDR+ 15]
                        Hardware
                                          TP      [MPS19] [AGKK19]
                        Application       MC      [HSB+ 19] [NT19] [WGS+ 19] [MMS19] [ZRM14] [KKHE17]
                                          LW      [TJKBL19]
                        System
                                          MC      [RT17] [DRR17] [HH18] [RRS13] [KTJB19] [WSC17]
                                          LW      [SPSK17] [ACF16]
                        Protocol          MC      [NRM16] [PPL16] [BSNRN14]
         Industrial
                                          TP      [DPP+ 17]
                                          LW      [OH18]
                        Implementation
                                          MC      [ALR16] [CGB+ 18] [SMX18] [TSS16]
                                          TP      [CGB+ 18]
                                          MC      [ALKH17]
                        Hardware
                                          TP      [HRG+ 18] [LFBP14] [LJM11] [GDMJ16a]
                                          LW      [MT13] [DT17] [DT18] [MAH15]
                        Application       MC      [ST12] [ST14b] [ST14a] [MNSV16]
                                          TP      [SC16]
                                          MC      [BSGM15] [BKMJ18] [DKK+ 14] [KBG+ 17] [MSHA17] [BTW+ 13]
                        System
                                          TP      [MPX+ 13]
                                          MC      [CFM16]
         Consumer       Protocol
                                          TP      [CCD+ 17]
                                          LW      [BBC+ 19b] [DFLO19]
                        Implementation    MC      [SKMT12]
                                          TP      [JTL12a] [GFLS11] [MTT+ 12]
                                          LW      [FXZ+ 17]
                        Hardware          MC      [TP16] [GDMJ16b] [SAS+ 18]
                                          TP      [GDMJ16b] [LCH+ 16]
                                          MC      [SLBK14] [AAA+ 12] [SLZ13] [Coo18]
                        Application
                                          TP      [CLW+ 14] [Coo18]
                                          LW      [ZKWG16]
                        System            MC      [MJA+ 18] [HLC+ 13] [BVGM15] [SBL18]
                                          TP      [WZM12] [JED+ 12] [MLHK14]
                                          MC      [Aia15] [Kum14] [KS15] [RCD+ 17]
         Enterprise     Protocol
                                          TP      [BDH+ 18] [CCC+ 18] [JBOK14]
                                          LW      [NFV15] [XCWC13] [VCM+ 16]
                        Implementation    MC      [VCJ+ 13]
                                          TP      [PZS+ 18b]
                                          LW      [FWX+ 17]
                        Hardware          MC      [BHW+ 14]
                                          TP      [SJL+ 15] [KS13]
                       Table 1: The sorting of the 120 works leading to the taxonomy displayed in Figure
                       2.
