Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000.

Digital Object Identifier 10.1109/ACCESS.2019.Doi Number




A Hybrid Formal Verification System in Coq for
Ensuring the Reliability and Security of
Ethereum-based Service Smart Contracts
                      1                                       1                           1
Zheng Yang , Member, IEEE, Hang Lei , Weizhong Qian
1
School of Information and Software Engineering, University of Electronic Science and Technology of China, No.4 Section 2 North Jianshe Road,
Chengdu 610054, P.R. China

Corresponding author: Zheng Yang (e-mail: zyang.uestc@gmail.com).

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.



ABSTRACT This paper reports a formal symbolic process virtual machine (FSPVM) denoted as
FSPVM-E for verifying the reliability and security of Ethereum-based services at the source code level of
smart contracts. A Coq proof assistant is employed for programming the system and for proving its
correctness. The current version of FSPVM-E adopts execution-verification isomorphism, which is an
application extension of Curry-Howard isomorphism, as its fundamental theoretical framework to
combine symbolic execution and higher-order logic theorem proving. The four primary components of
FSPVM-E include a general, extensible, and reusable formal memory framework, an extensible and
universal formal intermediate programming language denoted as Lolisa, which is a large subset of the
Solidity programming language using generalized algebraic datatypes, the corresponding formally
verified interpreter of Lolisa, denoted as FEther, and assistant tools and libraries. The self-correctness of
all components is certified in Coq. FSPVM-E supports the ERC20 token standard, and can automatically
and symbolically execute Ethereum-based smart contracts, scan their standard vulnerabilities, and verify
their reliability and security properties with Hoare-style logic in Coq.

INDEX TERMS Blockchain, theorem proving, distributed systems, security, verification



I. INTRODUCTION
Blockchain [1] is one of the emerging technologies                                     Kaleido the first managed BaaS offering that is available on
developed to address a wide range of disparate problems,                               Amazon web service (AWS) regions across the world.
such as those associated with cryptocurrency [2] and                                        While BaaS is certainaly a rapidly emerging service, the
distributed storage [3]. Recently, Blockchain-as-a-Service                             continued rapid development of BaaS is limited by security
(BaaS), where blockchain services are obtained from third-                             issues like those affecting Software-as-a-Service (SaaS)
party providers, has established a strong market presence,                             products. Presently, one of the security issues of greatest
and is a promising means of utilizing the blockchain                                   interest for researchers is the reliability and security of
technology. Organizations like Oracle, Microsoft, and IBM                              blockchain smart contracts. Here, blockchain smart contracts
have launched BaaS offerings. Many BaaS offerings are                                  are script programs that provide a kind of special digital
based on or have been inspired by the Ethereum platform                                contract where the code is the law, which enables blockchain
[4], which is one of the most powerful 2.0 blockchain                                  transactions to be conducted automatically [5]. One of the
platforms presently available. For example, Amazon                                     challenges that must be confronted in the development of
partnered with Kaleido to offer cloud services on which to                             secure and reliable smart contracts is that the programming
host an Enterprise Ethereum-based architecture. That makes                             process for these programs differs from that of conventional
                                                                                       programs. Here, the source code of smart contracts must




                                                                                                                                                   1
                                                                                 Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



represent legal considerations in a manner similar to contracts              satisfies both reliability and completeness simultaneously.
written in natural languages. Therefore, obligations and terms               Hence, formal verification is one of the most rigorous
should be presented in smart contracts explicitly. However,                  theoretical technologies available for ensuring the security
smart contract developers are generally programmers, rather                  and reliability of software systems. Consequently, the
than legal experts, and their grasp of legal obligations and                 Ethereum community has focused on the formal verification
terms is secondary to their grasp of programming. As a result,               of smart contracts, issuing open calls for formal verification
the programming habits of programmers introduce legal                        proposals [9] as part of what has been described as a “push
loopholes in smart contracts. These loopholes introduce many                 for formal verification” [10].
classes of subtle bugs in smart contracts, ranging from                          While formal verification is a rigorous approach, different
transaction-ordering dependencies to mishandled exceptions                   formal verification technologies have their own peculiar
[6], that differ significantly from common bugs because,                     strengths and weaknesses. Among these, higher-order logic
while common bugs are easily detected owing to faulty                        theorem proving is one of the most rigorous and flexible
program execution, these legal loopholes can result in                       technologies for verifying the properties of programs.
unintended operations, and can also be maliciously exploited                 However, numerous problems regarding reusability,
to circumvent obligation limitations without affecting the                   consistency, and automation have been encountered when
normal execution of the contract procedure, and ultimately                   applying theorem-proving technology to program verification
result in direct economic loss to users. For example, some of                [11]. Moreover, the process of model checking is only
the largest and best known attacks on smart contracts                        applicable to finite state programs. In addition, a number of
involved those based on the Ethereum platform, such as the                   well-known frameworks and tools, focused on Solidity
attack on the decentralized autonomous organization (DAO)                    bytecode on the Ethereum virtual machine (EVM) platform,
[7] and the Parity wallet attack [8]. A partial summary of                   have been developed recently for the verification of Ethereum
Ethereum-based smart contract attacks are listed in Table 1,                 smart contracts by symbolic execution. For example, the
which indicates that Ethereum attack cases have already                      formal semantic known as KEVM was developed for the
resulted in the loss of billions of dollars worth of virtual                 formal low-level programming verification of EVM using the
currency. Moreover, due to the unique feature of these                       K-framework [12]. Since KEVM is executable, it can run the
vulnerabilities, standard software engineering techniques                    validation test suite provided by the Ethereum foundation.
employing such static and dynamic analysis tools as                          Similarly, a Lem [13] implementation of EVM provides an
Manticore (https://github.com/trailofbits/manticore) and                     executable semantics of EVM for the formal verification of
Mythril (https://mythx.io/) have not yet been proven to be                   smart contracts at the bytecode level. Grishchenko et al.'s
effective at increasing the security and reliability of smart                [14] and Amani et al.'s [15] applied F* and Isabell/HOL to
contracts. Thus, an urgent need exists for a verification and                abstractly formalize the semantics of EVM bytecode.
validation technology that can guarantee the security and                    Unfortunately, few of these works formalized the syntax and
reliability of Ethereum-based services in the most rigorous                  semantics of Solidity source code, and verified the
manner available.                                                            compilation process from Solidity to respective bytecode.
                          TABLE 1                                            Oyente (https://www.comp.nus.edu.sg/˜loiluu/ oyente.html) is
  PARTIAL SUMMARY OF RECENT ETHEREUM-BASED SMART CONTRACT
                        ATTACK CASES
                                                                             an EVM symbolic execution engine written in Python
                                                                             supporting most of the EVM opcodes. Several heuristics-
Attack Date       Contract Name         Result
                                                                             based drivers of the symbolic execution engine are built into
06/17/2016        The DAO               3.6 million ETH lost [7]
                                                                             the tool for finding common bugs in EVM programs.
07/19/2017        Parity                150 thousand ETH lost [8]
11/06/2017        Parity                500 thousand ETH frozen              However, these heuristics may introduce false positives in
04/22/2018        BEC                   Crashed to zero value1               many cases, and they have not been rigorously proven to
04/26/2018        SMT                   16 million SMT lost2                 accurately capture their bug classes. In addition, it must be
05/24/2018        EDU                   Crashed to zero value                noted that most of the many recent tools based on symbolic
05/24/2018        BAI                   Crashed to zero value                execution adopt model checking technology as their
06/16/2018        ICX                   All ICX frozen3                      foundation, and few are developed in a higher-order logic
   A brief comparison of existing verification and validation                theorem proving system to enable real-world programs to be
technologies is presented in the Table 2. We note from this                  symbolically executed. In addition, conventional symbolic
table that formal verification is the only technology that                   execution approaches also suffer from limitations such as
                                                                             path explosion, where the number of feasible paths in a
  1
     BEC: https://medium.com/@peckshield/alert-new-batchoverflow-bug-in-
                                                                             program grows exponentially, program-dependent efficiency,
multiple-erc20-smart-contracts-cve-2018-10299-511067db6536                   and memory, environment, and constraint solving problems
  2
    SMT: https://medium.com/wolf-crypto/batchoverflow-erc20-vulnerability-   [16]. Moreover, nearly all of these methods have high
5691e42940de
  3
     ICX: https://medium.com/@tozex/cryptoasset-industry-problems-smart-     learning thresholds. These problems obstruct formal
contract-security-challenge-cb6aee69d5ef                                     verification technologies from being applied commercially.




                                                                                                                                                     2
                                                                       Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



                           TABLE 2                                to prove Java type soundness [26]. In addition, the
     COMPARISONS OF DIFFERENT VERIFICATION AND VALIDATION
                        TECHNOLOGIES
                                                                  operational semantics of JavaScript have been investigated
                                                                  [27], which is of particular interest in the present work
Technology                     Reliability    Completeness
                                                                  because Solidity is similar to JavaScript. However, most of
Traditional code testing       Reliable       Non-complete
                                                                  these studies focused on specific domains and programming
Symbolic execution             Reliable       Non-complete
Traditional static analysis    Unreliable     Non-complete        languages, and cannot be readily extended for the verification
Formal verification            Reliable       Complete            of blockchain smart contracts.
                                                                      This paper addresses the above issues by developing a
                                                                  formal symbolic process virtual machine (FSPVM) denoted
    One of the most important features of the Ethereum
                                                                  as FSPVM-E for verifying the reliability and security of
platform is that it implements a general-purpose Turing-
                                                                  Ethereum-based services at the source code level of smart
complete programming language denoted as Solidity that
                                                                  contracts. The work of this paper was primarily inspired by
allows for the development of arbitrary applications and
                                                                  the symbolic process virtual machine KLEE [28], which is a
scripts that can be executed in the EVM to conduct
                                                                  well-known and successful certification tool based on
blockchain transactions automatically. However, most
                                                                  symbolic execution. The proposed FSPVM-E is formulated
prominent studies have focused on the formal verification of
                                                                  in Coq because it is one of the most highly regarded and
the bytecode of the EVM, and the development of high-level
                                                                  widely employed proof assistants [29]. The present study
formal specifications for Solidity and relevant formal
                                                                  capitalizes on our progress over the past year for developing a
verification tools has attracted considerably less interest
                                                                  powerful hybrid FSPVM system in Coq to verify smart
despite its importance in programming and debugging smart
                                                                  contract properties on multiple blockchain platforms [11],
contract software. Although some intermediate specification
                                                                  [30], [31], [32], [33]. The proposed system combines the
languages between Solidity and EVM bytecode have been
                                                                  advantages of virtual machine platforms, static vulnerability
developed, such as Scilla [17], Simplicity [18] and Bhargavan
                                                                  scanning, higher-order logic theorem proving, and symbolic
et al.'s [19], the Solidity syntax and semantics have not been
                                                                  execution technology based on an extension of Curry-Howard
formalized in a manner that is consistent with official
                                                                  isomorphism (CHI) [34], denoted as execution-verification
documentation. However, the formal syntax and semantics of
                                                                  isomorphism (EVI) [11], and avoids their respective
programming languages actually play a crucial role in several
                                                                  disadvantages, to symbolically execute real-world programs
areas of computer science, particularly in program
                                                                  and automatically verify the smart contracts of Ethereum-
verification. For advanced programmers and compiler
                                                                  based services. The present report systematically illustrates
developers, formal semantics provide a more precise
                                                                  the FSPVM-E architecture, elaborates on the novel features
alternative to the informal English descriptions that typically
                                                                  of each component, presents experimental results, and
pass as language standards. In the context of formal methods,
                                                                  introduces real world application examples. Specifically, the
such as static analysis, model checking, and program proving,
                                                                  present work makes the following contributions.
formal semantics are required to validate the abstract
                                                                       Formal memory model: We design and implement
interpretations and program logic (e.g., axiomatic semantics)
                                                                           a general, extensible, and reusable formal memory
used to analyze and verify programs. Formal semantics for
                                                                           framework denoted as the GERM framework to
the involved languages are also a prerequisite for verifying
                                                                           virtualize the real-world memory hardware, basic
programming tools, such as compilers, type checkers, static
                                                                           memory operations, and pointer arithmetic in Coq.
analyzers, and program verifiers. In other computer science
                                                                       Formal specification language for Solidity: We
fields, several studies have focused on developing
                                                                           formalize and mechanize an extensible and
mechanized formalizations of operational semantics for
                                                                           universal large subset of the Solidity programming
different high-level programming languages. For example, the
                                                                           language in Coq with generalized algebraic
Cholera project [20] formalized the static and dynamic
                                                                           datatypes (GADTs) [35]. This represents a formal
semantics of a large subset of the C language using the HOL
                                                                           intermediate programming language denoted as
proof assistant. The CompCert project [21] has conducted
                                                                           Lolisa. The supported subset of Solidity is
influential verification work for C and GCC, and a formal
                                                                           comparable to the subsets commonly recommended
semantics denoted as Clight was developed for a subset of C.
                                                                           for writing common Ethereum-based smart
This formed the basis for VST [22] and CompCertX [23]. In
                                                                           contracts, and includes the built-in functions of the
addition, several interesting formal verification studies have
                                                                           EVM. It also solves the consistency problem
been conducted for operating systems based on the CompCert
                                                                           associated with existing higher-order logic theorem
project. Tews et al. [24] developed denotational semantics for
                                                                           proving technologies.
a subset of the C++ language that were presented as shallow
                                                                       Execution and proof engine: An optimized formal
embedding in the PVS prover. Igarashi et al. [25] presented a
                                                                           verified interpreter is developed in Coq for Lolisa,
minimal core calculus for Java and Generic Java, and verified
                                                                           denoted as FEther, which connects the GERM
the important core properties. A similar study was conducted




                                                                                                                                          3
                                                                     Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



         framework and Lolisa, and serves as an execution        architecture. Section IV discusses the methods by which the
         engine to symbolically execute and verify the smart     self-correctness of FSPVM-E is ensured, and also defines
         contracts of Ethereum written in Lolisa within Coq      the non-aftereffect property to guarantee the correctness of
         with high level evaluation efficiency [33].             assistant tools that are not programmed in Coq. Section V
     Assistant tools and libraries: We provide assistant        presents simple case studies to illustrate the advantages and
         tools and libraries, including a specification          novel features of FSPVM-E for verifying the security and
         generator, a language translator, a static analysis     reliability of smart contracts. Section VI discusses the
         library, and an automatic tactic library, which are     extensibility and universality of FSPVM-E, and provides a
         respectively applied to generate dynamic                preliminary scheme for systematically extending FSPVM-E
         specifications, translate Solidity into Lolisa, store   to support different blockchain platforms. Section VII
         the specifications of standard smart contract           provides a comparison of FSPVM-E with related work for
         vulnerabilities, and provide an automatic evaluation    the formal verification for Ethereum smart contracts. Finally,
         strategy. These tools and libraries significantly       Section VIII presents conclusions and future directions of
         improve the degree of automation and the                research.
         validation efficiency of FSPVM-E.
   The above core components of FSPVM-E are applied to           II. FUNDAMENTAL CONCEPTS
virtualize Coq as an extensible and general-purpose toolchain    Prior to defining the formal specifications of FSPVM-E, it
for Ethereum smart contract verification, which reduces the      is necessary first to define the fundamental environment
verification workload and learning threshold. In addition,       FSPVM-E.
FSPVM-E has the following novel features.                                                    TABLE 3
                                                                                    STATE FUNCTIONS OF FSPVM-E
    Executable and Provable: Defining FSPVM-E
         based on the GERM framework allows,                     𝛭    Memory space                 ℰ     Environment information
         theoretically, for formal smart contracts to be         𝛬    Memory address set           𝛺     Native value set
                                                                 𝒱    Verified logic term          ℱ     Overall formal system
         symbolically executed, and their properties
                                                                 𝛤    Proof context                𝒞     Code segments
         simultaneously and automatically verified using
         higher-order logic theorem-proving assistants,             Table 3 lists the state functions used to calculate
         which, when conducted in conjunction with a             commonly needed values from the current state of the
         formal interpreter, is comparable to the execution      program. All of these state functions will be encountered in
         of real-world programs.                                 the following discussion. Components of specific states will
    Extensible and Universal: Although FSPVM-E is               be denoted using the appropriate Greek letter subscripted
         designed specifically for the Ethereum platform,        by the state of interest. As shown in Table 3, the proof
         each component includes many general features           context [29, 36] (denoted as 𝛤, 𝛤1 , etc.) refers to the proof
         applicable to other blockchain platforms. Thus, the     environment or local proof theory which contains proved
         core functions can be extended to formalize similar     local propositions as additional information, and decorate
         programming languages.                                  assumptions by discharge rules that are applied when
    Trusted and Certified: The self-correctness of              leaving a context, and the 𝛤𝑐 is adoped as the current logic
         FSPVM-E core components is verified in Coq              context. In the following contents, we will use context to
         completely, and the correctness of assistant tools      represent proof context. The formal memory space in the
         not programmed in Coq is also guaranteed.               context is denoted as M , and σ represents specific
    Hybrid verification system: In conjunction with             memory states. The context of the execution environment is
         Lolisa and the static analysis library, FSPVM-E         represented as ℰ, and the env and fenv are adopted as the
         supports basic static analysis to automatically scan    current environment that stores the current execution
         standard vulnerabilities hidden in source code. In      environment information, and the super-environment that
         addition, FEther supports multiple types of             which stores the super environment information before the
         symbolic execution for verification using FSPVM-        execution environment transformation. The symbol ⊳
         E. Finally, FSPVM-E provides a debugging                represents the abstract binary relationship that left logic
         mechanism for general programmers to identify the       definition could be unfolded as the right logic expression to
         vulnerabilities of source code. In this manner, users   get more information in the proof context. This meaning of
         of FSPVM-E can flexibly select the most suitable        the symbol will be specified in different specific rules. We
         method for analyzing and verifying their programs.      assign Λ to denote a set of memory addresses, and we
   The remainder of this paper is organized as follows.          adopt 𝒱 to represent the verified logic terms in the proof
Section II briefly presents the essential concepts of            assistant.
FSPVM-E. Section III describes the overall FSPVM-E




                                                                                                                                         4
                                                                                                           Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



                                                                         Translator


                                                                                                                             Certification and
                                                                                          Formal Smart                         Test Library
                                                     Syntactic Sugar Layer
                                                                                          Contract Model
                                                                                                                              Static Analyzing
                                                                                                                                 Theorems
                                                     Formal Specification              Execution Engine                         Self-correctness
                                                      Language (Lolisa)                    (FEther)                                Theorems

                                                     Solidity Syntax Formal
                                                                                      Formal Syntax Parser
                                                         Specifications
                                                     Inductive Operational          Executable Operational                       Property
                                                          Semantics                       Semantics                              Theorems
                                                     EVM Built-in Function            Execution Results
                                                       Standard Library             Validation Mechanism


                                                         Formal Memory
                                    Generator




                                                         Model (GERM)
                                                                                           Trusted Core
                                                          Basic Memory
                                                                                              of Coq
                                                           Operations
                                                                                                                     Automatic Tactic
                                                     Formal Memory Value                                             Strategy Library
                                                        Specifications
                                                                                                                     Verification Tactic
                                                     Formal Memory Space                        OB                    Memory Tactic
                                                                                                                     Execution Tactic
                                                Trusted Domain in Coq



Fig.1. Architecture of the FSPVM-E verification system.


                                                                              𝑎𝑟
                                                                                            Formal                                    Formal Memory
                                                             Translator
                                                                                            Syntax                                      Operations
                                                                              𝑜
                                                                    ℱ𝒫             𝑎 𝑎               𝑟     𝑟                𝑜               𝑚            𝑎 𝑎
                                                 𝑚                                                               𝑜                            𝑎 𝑎
                        Formal Memory                                                       Formal                         Formal                   Trusted
                                                            𝑚           ℱ𝒫
                            Space                                                         Interpreter                     Semantic                   Core
                                                     𝑎                                                       𝑚                                𝑚
                                                                                      𝑜

                                                                                            𝑚


Fig.2. General workflow of the FSPVM-E.


                                                                                                verified components of the FSPVM-E framework. The
   Furthermore, we assign Ω as the native value set of the
                                                                                                specification language of Coq includes a small, purely
basic logic system. For brevity in the following discussion,
                                                                                                functional language denoted as Gallina, which features
we will assign ℱ to represent the overall formal system.
                                                                                                recursive functions that operate by pattern matching over
The operational semantics of Lolisa is abbreviated as 𝑆,
                                                                                                inductive types (i.e., ML- or Haskell-style tree-shaped data
and the evaluation process is denoted as ⇓. In addition, to
                                                                                                types). With some ingenuity, Gallina is sufficiently
avoid ambiguity in the following discussion, we employ the
                                                                                                sophisticated for programming a process virtual machine.
term 𝒫𝑟𝑜𝑔𝑟𝑎𝑚 to represent a generic program written in a
                                                                                                However, the highly imperative algorithms found in
functional specification language, such as Coq, the term
                                                                                                programming language and interpreter textbooks must
programrw represents a generic program written in a
                                                                                                rewrite in a purely functional style.
general-purpose programming language ℒ , and
                                                                                                   The overall architecture of FSPVM-E is illustrated in
programformal represents the formal version of
                                                                                                Fig.1, where a dashed arrow ( ⇢) represents a logical
programrw written using the formalized version of ℒ ,
                                                                                                dependency relation, and a solid arrow (⟶) represents data
denoted as ℱℒ.
                                                                                                transmission. Here, FSPVM-E is designed according to Von
                                                                                                Neuman architecture, and it is logically constructed based
III. FSPVM-E ARCHITECTURE AND IMPLEMENTATION
                                                                                                on two sectors: a foundational sector and an extensible
The kernel of the FSPVM-E framework was developed                                               sector. In the foundational sector, the higher-order logic
entirely in Coq, and Coq was employed as the trusted                                            proof environment of Coq is virtualized as the FSPVM-E
computation base (TCB) [37]. Here, Coq served not only as                                       execution environment, which serves as the logic operating
a prover for conducting semantic preservation proofs, but                                       environment, and the trusted core of Coq (TCOC) is
also as a programming language for programming all                                              virtualized as a central processing unit, and takes Gallina as




                                                                                                                                                                              5
                                                                       Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



the logic machine-level language.                                   basis for arbitrary high-level specifications in different
    The extensible sector consists of four components. The          formal models for program verification.
first component is the GERM framework. The second                      The overall GERM framework structure is illustrated in
component is Lolisa. The third component is FEther. The             Fig.3. The first component of the formal memory model is
final component is the set of assistant tools and libraries,        the formal memory space, which is modeled as a collection
including translator and generator that are developed in            of disjoint blocks, and we adopt persistent data structures
untrusted domain using C++. The fundamental component               that support efficient updates without modifying data
is the formal memory model GERM. It serves as logic                 inplace. Likewise, a monadic programming style enables us
memory states to support operational semantics                      to encode exceptions and states in a legible, compositional
formalization and record all intermediate states during             manner. According to the figure, the GERM framework is
symbolic execution and verification. Based on this formal           based on the TCOC, and can be used as a basis for high-
memory model, the second component, a formal                        level formal specifications.
intermediate specification language Lolisa, is able to be
defined. It formalizes the selected abstract syntax and
corresponding semantics of Solidity language into Coq.
Finally, based on the GERM and Lolisa, we can construct
the third component that is a formal interpreter FEther. It is
used to symbolically execute the formal programs model
written in Lolisa.
    The general workflow is shown in Fig.2. First of all,
FEther will take the initial memory state and formal
programs as parameters. Next, the FEther will parse the
formal programs according to the syntax of Lolisa. Finally,
FEther will invoke the formal operational semantics and
interact with GERM to generate a new formal memory state.
    These components in the current version of FSPVM-E
include about 16,000 lines of Coq source code and 4,000
lines of C++ source code. The specific workload for
constructing the FSPVM-E framework is itemized in the
                                                                      Fig.3. Architecture of the GERM memory model.
Table 4. In this manner, FSPVM-E simulates the process of               The data structure of the formal memory space is
program execution in the real world, in that a program              illustrated by the example given in Fig.4, where each
written in a high-level programming language is interpreted
                                                                    memory record field specifies a logic memory block with
into machine code and executed on the hardware of the
                                                                    type value. Users can define specific memory sizes
operating environment in Coq. The details of these four
                                                                    according to their requirements with the help of assistant
components are respectively discussed in Subsections III.A
                                                                    tools, which are introduced in Subsection III.D. The details
to III.D.
                          TABLE 4                                   regarding the formal memory space of the GERM
WORKLOAD STATISTICS FOR CONSTRUCTING THE FSPVM-E FRAMEWORK          framework are presented as follows.
                                        Lines in      Lines in          According to the definition of record datatype given by
           Classification
                                          Coq           C++         Coq’s reference manual [29], each field block 𝑏 𝑑 in Coq
Formal memory model (GERM)            3,849          0              has a unique corresponding field name 𝑑, and the data
Specification language (Lolisa)       1,004          0              stored in the 𝑏 𝑑 block of a specific record value 𝑟𝑣 can
Executable interpreter (FEther)       7,726          0              be directly accessed by its corresponding 𝑑. In memory,
Automatic tactic library              427            0              𝑏 𝑑 represents the logic memory block, and the
Self-correctness library              1,883          0              corresponding 𝑑 is formalized as the memory absolute
Static analysis library               1,053          0              address 𝑀 𝑑𝑑𝑟 . In this manner, the GERM framework
Generator                             0              1,476          statically guarantees that each memory block has a unique
Translator                            0              2,743
                                                                    𝑀 𝑑𝑑𝑟      at the type level. Additionally, in contrast to
                                                                    relevant data structures based on a tree or graph structure
A. GENERAL FORMAL MEMORY MODEL                                      [38], which must search all nodes individually to modify a
The GERM framework simulates physical memory                        memory block, the GERM framework can access and
hardware structure, including a low-level formal memory             modify the block directly through its corresponding
space, and provides a set of simple, nonintrusive application       𝑀 𝑑𝑑𝑟 .
programming interfaces using Coq that can support
different formal verification specifications simultaneously,
particularly at the code level. In theory, it is well suited as a




                                                                                                                                               6
                                                                           Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



Record memory: Type: = new {        Memory Address     Data Value      In conjunction with logic memory value 𝑏 𝑜 𝑣 , as shown
    m_0xinit: value                     m_0xinit         value         in rule 1, the corresponding block size, the current and
    m_0x00000000: value              m_0x00000000        value         super logic execution environment information            and
    m_0x00000001: value              m_0x00000001        value         𝑓      , respectively, block allocation flag 𝑜         , and
    m_0x00000002: value              m_0x00000002        value         modification authority 𝑎       . Currently, 𝑏 𝑜 𝑣 supports
    m_0x00000003: value              m_0x00000003        value         14 datatypes, including basic arithmetic data values (undef,
    …                                      …              …            integer, float, Boolean, string, byte, structure, array, and
    m_0x0000000F: value              m_0x0000000F        value         mapping), program instructions (statement), and pointer
}
                                                                       objects (variable pointer, parameter pointer, function
Fig.4. Formal memory space, including the formal specification of      pointer, and contract pointer). One of the benefits of the
memory space in Coq (left), and the real-world physical memory space   type constructor of 𝑎         is that the safety of memory
structure (right).
                                                                       specifications can be readily ensured in the GERM
                                                                       framework. For example, a 𝑏 𝑜 𝑣 corresponding to an
    To improve the flexibility of memory operations, the               uninitialized memory block will be initialized as
GERM framework in its current form also provides a label               𝑈 𝑑 𝑓( ) rather than as a random value. Similarly, all
memory address level. In detail, this level first provides a           information regarding the current memory state is explicitly
special identifier denoted as a label address 𝐿 𝑑𝑑𝑟 , which            stored by the corresponding typing constructors. In this
is a metavariable defined as an enumeration type in Coq as             manner, in 𝛤𝑐 , the env and fenv record the execution
follows.                                                               environment information, and the block information
𝐿 𝑑𝑑𝑟 ∶∶ = _0x00000000 | […] | _0xFFFFFFFF | 𝛬 𝑝 𝑐                     indexed by an address can be accessed from current
Special address: 𝛬 𝑝 𝑐 ∶∶ = _0xinit | _0xsend | _0xsend_re |           memory state. As abstracted in rule 2, a memory operation
_0xcall | _0xmsg | _0xaddress | _0xblock                               𝑜 𝑐ℎ 𝑐𝑘 can modify a specific block by taking current states,
    Here, 𝛬 𝑝 𝑐      is used as the reference for data                 address, env and fenv as parameters, and generated a new
structures and functions in the EVM standard library.                  optional memory state, where ⊳ represents the binary
Accordingly, programmers can define custom mapping                     relation that for an arbitrary memory address 𝑎𝑑𝑑𝑟 can
strategies 𝑀𝑎 𝑐 to map 𝐿 𝑑𝑑𝑟                to 𝑀 𝑑𝑑𝑟        as         access a defined logic memory block from the memory state
follows.                                                               𝑚        of 𝛤𝑐 , and ↪ is represented the evaluation process
𝑀𝑎 (𝐿 𝑑𝑑𝑟 ) =                                                          of 𝑜 𝑐ℎ 𝑐𝑘 .
                                                                                       ℰ⊢ 𝑣 ℰ⊢        𝑣
𝑚𝑎      𝑀𝑎 𝑐 (𝐿 𝑑𝑑𝑟 )𝑤                                                  𝛤𝑐 (𝑚𝑠𝑡𝑎𝑡𝑒 . 𝑑𝑑𝑟)⊳(𝑏 𝑜𝑐𝑘𝑣 ,  𝑜𝑟1 ,…,  𝑜𝑟𝑛)
| 𝐸𝑟𝑟𝑜𝑟 → 𝐸𝑟𝑟𝑜𝑟                                                                                                                             (2)
                                                                            𝑜𝑝𝑐ℎ𝑒𝑐𝑘 (𝑚𝑠𝑡𝑎𝑡𝑒 . 𝑑𝑑𝑟, 𝑣,     𝑣)↪⟦𝑚𝑣 ⟧
| 𝑂𝐾(𝑀 𝑑𝑑𝑟 ) → 𝑀 𝑑𝑑𝑟                                                       As such, conventional memory safety problems, such as
   𝑑.                                                                  buffer overflows and dangling pointers, can be readily
    Here, if the return value is 𝐸𝑟𝑟𝑜𝑟, the mapping is                 exposed in the GERM framework by symbolic execution.
deemed to have failed, and the mapping is successful if the                Although the current version of the GERM framework is
return value is 𝑂𝐾(𝑀 𝑑𝑑𝑟 ). Similarly, 𝐿 𝑑𝑑𝑟           can be          adjusted to support FSPVM-E, users can extend the 𝑎
employed in the GERM framework to accurately model                     specifications because the GERM framework can function
pointer arithmetic. Briefly, users can define pointer objects          independently with other formal models. Here, as the
in high-level specifications, apply 𝑀𝑎 (𝐿 𝑑𝑑𝑟 ) to                     abstraction of the 𝑎           definition defined in rule 3
reference a location in memory, and obtain the logic                   programmers can add new specifications 𝑓𝑜𝑟 into the
expressions stored at that location. The pointer arithmetic              𝑎      constructor to represent and store new logic
mechanism defined in Lolisa based on 𝐿 𝑑𝑑𝑟          is briefly         information according to the specific requirements of
introduced in Subsection III.B. Moreover, the label address            different projects and situations.
level reserves the extension space for simulating virtual                𝑎 : 𝑏 𝑜 𝑣 → 𝑓𝑜𝑟0 → 𝑓𝑜𝑟1 → [… ]
memory and memory isolation mechanisms, such as a                      → 𝑓𝑜𝑟 → 𝑎 ,                                                (3)
memory management unit and a TrustZone.                                    Finally, we provide 9 classes of basic operations in the
    A benefit of designing FSPVM-E according to von                    GERM framework, which include map, initialize, read,
Neumann architecture is that the GERM framework                        write, address offset, search, allocate, and free. Any higher-
memory space is able to store the program instructions and             order specifications can take the GERM framework as their
data values simultaneously and thereby accurately simulate             fundamental logic state, and apply memory operation APIs
a real-world memory space and guarantee the reliability of             to formalize memory-based or memory-related higher level
the formal memory model. Hence, the memory value type                  specifications in Coq, such as formal semantics and
  𝑎     is inductively defined as rule 1.                              operating systems.
  𝑎    ∶∶ = 𝑏 𝑜 𝑣 →          →       →𝑓      →𝑜          →
𝑎     → 𝑎                                                  (1)         B. LOLISA




                                                                                                                                                   7
                                                                             Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



Following the process illustrated in Fig.5, most of the                        consistently. As explained above, due to limitation of length,
syntax and respective semantics of Lolisa are formalized                       the details about formalizations and properties have been
strictly following the official Ethereum documentation of                      presented in our online report [11].
Solidity version 0.4. Due to limitation of length, the details                     In particular, different from other FSLs of Solidity, such
of Lolisa’s formalization have been presented in our online                    as       K     framework         based     Solidity   semantics
report (https://arxiv.org/abs/1803.09885).                                     (https://github.com/kframework/solidity-semantics)           the
                                                                               formal syntax of Lolisa [11] is defined using generalized
                          map                         yields
       Solidity Syntax            Solidity Semantics         Smart Contracts   algebraic datatypes (GADTs). As indicated by the rule 5, a
                                                                               syntax token T is specified by static type annotations 𝜏 for
     equivalent                    abstract                  translate
                                                                               all values and expressions of Lolisa.
    Syntactic Sugar Layer
                          map   Inductive Operational yields Formal Smart      𝑇 ∷ 𝜏0 → [… ] → 𝜏 → 𝑇              ,                         (5)
                                      Semantics                  Contracts
     equivalent                  equivalent                                    This     ensures   that    the  formal   syntax  of values  and
   Solidity Syntax Formal      Executable Operational                          expressions is more clear and abstract, and facilitates the
        Specifications                Semantics                                strict maintenance of type safety for Lolisa expressions. In
                                                                               addition, employing a combination of type annotations
       GADTs Typing
          Judgement                                                            facilitates the definition of a very large number of different
                                                        Trusted Domain in Coq
                                                                               expressions based on equivalent constructors. The
Fig.5. Relationships between Solidity and Lolisa.
                                                                               application scope of different statements is limited by
                                                                               different combinations of 𝜏 and 𝜏𝑜𝑢 . For example, in
                                                                               the specification of If statement defined in rule 6, the input
    The specific syntax and semantics of Lolisa are type 𝜏 of the condition expression has no limitation, but
separated as four layers, from bottom to top, including types, the return type 𝜏
                                                                                                    𝑜𝑢 of the condition expression must be
values, expressions and statements. All reference data Boolean type 𝑇𝑏𝑜𝑜 . Different from If statement, in the
structures can be formalized in Lolisa because each variable specification of Assign statement defined in rule 7, the input
identifier 𝑑 is allocated a memory address based on the type 𝜏 and 𝜏 of the left and right expressions have no
                                                                                                0
GERM framework, and can be abstracted as an 𝜆 - limitation, but the 𝜏
                                                                                                         𝑜𝑢 of the left and right expressions
application form according to the rule 4 where 𝑥 is a 𝜆- must be equivalent 𝜏 .
                                                                                                         1
bounded parameter and 𝑎 is a label address.                                    𝐼𝑓: ∀ (𝜏:        ), 𝑥 𝑟𝜏 𝑇𝑏𝑜𝑜 → 𝑎 𝑚             → 𝑎 𝑚         →
  𝑑 ≔ (𝜆 (𝑥: 𝐿 𝑑𝑑𝑟         ). 𝑥)(𝑎: 𝐿 𝑑𝑑𝑟 )                                (4)    𝑎 𝑚 ,                                                     (6)
As such, the syntax of Lolisa not only includes nearly all the 𝐴 𝑔 : ∀ (𝜏 𝜏 𝜏 :                              ), 𝑥 𝑟𝜏 𝜏1 → 𝑥 𝑟𝜏0 𝜏1 →
                                                                                                 0 1
characteristic components of Solidity, such as array,
                                                                                  𝑎 𝑚 ,                                                     (7)
mapping, message, send, transfer, address, modifier,
                                                                               However, the application of GADTs provides Lolisa with a
contract, and gas types, but it also contains general-purpose
                                                                               stronger static type system than Solidity because the type
programming language features, such as multiple return
                                                                               system of Lolisa strictly defines the syntax rules and
values, pointer arithmetic, struct, field access, module, and
                                                                               relevant limitations in the formal specifications as typing
the full power of functions, including recursive functions
                                                                               judgments. For example, in the If statement defined in rule
and function pointers. These abstract syntax components
                                                                               6, its condition expression is limited by type 𝑥 𝑟𝜏 𝑇𝑏𝑜𝑜 ,
are defined as an inductive type statement, and connected
                                                                               which specifies that the normal form of a specific condition
by a list type. However, there are still some challenges in
                                                                               must be a Boolean type. As such, an ill-typed If statement,
current version of Lolisa. The first challenge is inline
                                                                               such                                                          as
assembly. The formalization of inline assembly needs
                                                                                     ′                                                 ′
accurate formal models of hardware such as registers that ∀                            : 𝑎 𝑚         , (𝐼𝑓 (𝐸 𝑜 (𝑉 𝑑 𝑓( )))              )    ,
has not been supported in current FSPVM-E. Besides, would be disclosed by the type-checking mechanism of Coq,
according to our experimental results, the precision of which would then present the error message shown in Fig.6.
formal floating-point datatype will be lost during unit An additional benefit to the use of GADTs in Lolisa is that
conversion. Therefore, inline assembly and the explicit the resulting strong static type-checking system assists in
ether unit of Solidity are omitted in Lolisa which are the discovering errors imported when translating Solidity into
limitations of current version Lolisa. Currently, if a code Lolisa. This is particularly beneficial because, although
segment includes inline assembly and explicit ether unit, syntax errors would be discovered during compilation in the
the code needs to be rebuilt manually. We have planned to EVM, implementing a compiler mechanism in Coq to check
overcome these two challenges in our future work. In for syntactical correctness when translating Solidity into
addition, to guarantee structural verification, the goto Lolisa would be an extremely challenging task. Moreover,
statement, and non-structured forms of switching such as such errors can seriously affect the evaluation of programs
Duff’s device [39] are not supported in Lolisa. In this in higher-order theorem-proving assistants.
manner, the Solidity can be translated into Lolisa



                                                                                                                                                     8
                                                                            Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)




Fig.6. Simple example of an error message generated by the type-checking mechanism of Coq in response to the ill-typed If statement
∀ 𝐬 𝐬′ : 𝐬𝐭𝐚𝐭𝐞𝐦𝐞𝐧𝐭, (𝐈𝐟 (𝐄𝐜𝐨𝐧𝐬𝐭(𝐕𝐮𝐧𝐝𝐞𝐟(𝐭𝐭))) 𝐬 𝐬′ ) in Lolisa.


In addition, because Solidity can be translated into Lolisa              adhere to the following program counter axiom.
line-by-line, the strong static type-checking system also                Axiom      (Program Counter): Suppose that, for all
assists in discovering ill-typed terms in Solidity source code.          statements s, if s is the next execution statement, it must be
To our knowledge, Lolisa is the first formal specification               the head of the statement sequence in the next execution
language of Solidity using GADTs.                                        iteration.
   The semantics of Lolisa are formally defined as big-step
operational semantics with two forms: inductive relational                  It must also be noted that the formal syntax of Lolisa
forms and executable function forms. The operational                     contains numerous typing limitations, and is overly complex
semantics of Lolisa defined as the relational form are                   to accommodate its adoption by general users, as illustrated
unified with symbol 𝑆𝑟 , and the executable operational                  by the example If statement given in Fig.8a and 8b.
semantics are represented as symbol 𝑆 𝑥 . 𝑆𝑟 is applied                  Therefore, Lolisa is made more intuitive by encapsulating
to verify properties of Solidity, and 𝑆 𝑥 is developed as                the abstract syntax tree of Lolisa into symbol abbreviations
the kernel of symbolic execution engine that can be invoked              based on the macro-mechanism of Coq, which is denoted as
by FEther. Because Lolisa is employed as a formal                        the notation mechanism. A notation is a symbolic
intermediate language for Solidity, which should be able to              abbreviation denoting some term or term pattern, which can
be parsed, executed, and verified in Coq or a similar proof              be parsed by Coq automatically. For example, the notation
assistant, the semantics of Lolisa are deterministic, and are            shown in Fig.8c can be employed to encapsulate the If
also based on the GERM framework. The equivalence                        statement given in Fig.8b, with the result shown in Fig.8d.
between the inductive relational forms 𝑆𝑟 and the                        The use of the notation mechanism in Lolisa is illustrated
executable function forms 𝑆 𝑥 of the operational                         by the components enclosed within the dashed-line box in
semantics of Lolisa is certified by the following simulation             Fig.5. As a result, the fixed formal syntax components of
diagram theorem, where the n represents the step limitation              Lolisa used in verification are transparent to users, and
which will be explained in the next section.                             thereby provide users with a simpler syntax. Moreover, this
                                                                         mechanism makes the consistency between real-world
Theorem             (simulation       diagram):       Let                languages and Lolisa far more intuitive and user friendly.
ℰ, 𝛭, ℱ ⊢      𝜎, 𝑜 𝑎𝑟 ,     ,𝑓   , 𝑏 𝑜𝑟 be the initial                  An additional benefit of this mechanism is that it provides
evaluation environment, and let 𝑅 𝑞 represent an                         for improved automation of the formalization process. Here,
equivalence relationship between any two terms. Then, any                as was conducted when converting Fig.8b to Fig.8d, the
relational semantic 𝑆𝑟 and executable semantic 𝑆 𝑥                       syntactic sugar is the interface to connect the translator. The
must satisfy the simulation diagram (Fig.7).                             translator is constructed by three modules: lexical analysis
          ℰ, 𝛭, ℱ ⊢      𝜎, 𝑜 𝑎𝑟 ,        ,𝑓      ,𝑏       𝑜𝑟
                                                                         module, syntax analysis module and program specification
  𝑆𝑟                                                            𝑟        generation module. The lexical analysis module consists of
               𝜎,      ,𝑓     ,𝑏     𝑜𝑟 , 𝑜   𝑎𝑟 , ⇓   𝑒                 two components: pattern matching sub-module and
       𝑅𝑞                                                           𝑅𝑞   behavior matching sub-module. The kernel of this module is
                                                                         Flex lexical analysis generator that uses regular expression
          ℰ, 𝛭, ℱ ⊢      𝜎, 𝑜 𝑎𝑟 ,        ,𝑓      ,𝑏       𝑜𝑟
  𝑆𝑥                                                            𝑟        mechanism to form morphemes of characters in source
              𝑆𝑥      , 𝜎, 𝑜 𝑎𝑟 ,       ,𝑓      ,𝑏     𝑜𝑟                programs. The syntax analysis module is used to generate
                                                                         the abstract syntax tree based on left-child right-sibling
Fig.7. Diagram for the correctness certification of Lolisa semantics.    binary tree algorithm. Finally, the program specification
                                                                         generation module converts the abstract syntax tree from
   In addition, the development of FEther in Coq and its                 C++ into the corresponding syntax sugar notations of Lolisa.
verification process will be simplified if a 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚                  In addition, these macro-definitions are helpful for
written in Lolisa is maintained as a structural program. To              promoting extensibility to other programming languages,
ensure this condition, the semantics of Lolisa are made to               the details of which are discussed in Section VI.




                                                                                                                                                    9
                                                                                               Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)




Fig.8. Example of macro definitions of the Lolisa formal abstract syntax tree.



               Formal Interpreter
               Parser                                        Formal ISA                              Validation
                                             token                                                                          invoke
               Type and Value Abstract                         Formal Type and                          Memory State                  Formal Memory
                    Syntax Parser
                                            𝑚𝑣                 Value Semantics                           Validating                       Model
                                                 𝑢 0                                                                        𝑚′
                  parse      𝑚𝑣   𝑢 0
                                                                                   require, invoke                                    𝑚′         𝑚
                                         token, 𝑚𝑣     𝑢 0                         fenv, env, gas                           require
                Expression Abstract                           Formal Expression                                                         Trusted Core
                                                                                               ′       Value Validating
                  Syntax Parser             𝑚𝑣                   Semantics         𝑚𝑣   𝑢 ,𝑚                                               of Coq
                                                 𝑢 1                                                                        𝑚𝑣
                 parse     𝑚𝑣 𝑢 1                                                                                                𝑢
                                         token, 𝑚𝑣   𝑢 1
                Statement Abstract                             Formal Statement
                                                                                                        Gas Checking
                  Syntax Parser                                   Semantics
                                            𝑚′

             preconditions execute                                                𝑚        verify

              Formal Smart Contracts
                                                                                  Property
                                                                                  Theorems
                                                                                                                                  Trusted Domain of Coq

Fig.9. Architecture of FEther.


   Finally, we have developed a small standard library in                               completely developed in Coq based on the GERM
Coq that incorporates the built-in data structures and                                  framework and Lolisa. The overall FEther structure is
functions of the EVM to facilitate the execution and                                    illustrated in Fig.9. FEther is entirely constructed in the
verification of Solidity programs rewritten in Lolisa using                             TCOC, and logically comprises three main components
higher-order logic theorem-proving assistants directly.                                 from left to right: a parser, an instruction set architecture
Currently, this standard library is a small subset that                                 (ISA) based on Lolisa semantics, and a validation checking
includes the syntax components msg, address, block, send,                               mechanism.
call, and requires. Lolisa is the first mechanized and                                      The parser is employed to analyze the syntax of a
validated formal syntax and semantics developed for                                       𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 written in Lolisa, extract the tokens from
Solidity. The consistency relationship between Solidity and                               𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 , and invoke corresponding semantics. As
Lolisa is defined according to the following rule 8, where                              mentioned above, Lolisa types are used as the type
is the statement of Solidity and 𝒯 reprents the translation                             signatures in Lolisa value and expression layers, and are
process from Solidity into Lolisa.                                                      dependent on corresponding Lolisa values. Therefore, the
∀ , ∈ 𝑆𝑜 𝑑        ∧ 𝒯( ) ∈ 𝐿𝑜 𝑎 ⊢ ≡ 𝒯( )                  (8)                           parsing and execution processes of types and values are
                                                                                        combined together.
C. FETHER
FEther is an extensible definitional interpreter that is




                                                                                                                                                                   10
                                                                                                                     Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)


               ℰ⊢     𝑣,    𝑣          𝛭⊢𝜎,𝑏𝑖𝑛𝑓𝑜             ℱ ⊢ 𝑜𝑝 𝑟             ℰ,𝛭,ℱ ⊢ 𝑃(        )          ℰ,𝛭,ℱ ⊢ 𝑏
                                  𝑣=     𝑔𝑎𝑠 (     𝑒𝑛𝑣 (𝑃(      )))               𝑣=      𝑒𝑛𝑣 (𝑃(       ))
                                                   𝜎=        𝑚𝑒𝑚 (𝑃(       ), 𝑏)
                                     ′                                                 𝑒𝑥𝑒𝑐𝑢𝑡𝑒,𝑇                                                                                      (9)
                    ℰ,𝛭,ℱ ⊢ 𝐹𝐸 ℎ 𝑟(⟦𝑚𝑠𝑡𝑎𝑡𝑒 ⟧,         𝑣′,       𝑣, 𝑟𝑔 ,𝑃(          )) ⇒            〈𝜎 ′ ,      𝑣,     𝑣〉
                                 ℰ⊢     𝑣,   𝑣        𝛭⊢𝜎,𝑏𝑖𝑛𝑓𝑜             ℱ ⊢ 𝑜𝑝 𝑟             ℰ,𝛭,ℱ ⊢ 𝑃(           )     ℰ,𝛭,ℱ ⊢ 𝑏
                                                 𝑣=     𝑔𝑎𝑠 (         𝑒𝑛𝑣 (𝑃(     )))            𝑣=          𝑒𝑛𝑣 (𝑃(       ))
                                                                  𝜎=            𝑚𝑒𝑚 (𝑃(     ), 𝑏)
                 ′
                                                        𝑒𝑥𝑒𝑐𝑢𝑡𝑒,∞                                                                             𝑒𝑥𝑒𝑐𝑢𝑡𝑒,𝑇                               (10)
ℰ,𝛭,ℱ ⊢ 𝐹𝐸 ℎ 𝑟(⟦𝑚𝑠𝑡𝑎𝑡𝑒 ⟧,       𝑣′,    𝑣, 𝑟𝑔 ,𝑃(      )) ⇒             〈𝜎 ′ ,    𝑣′,      𝑣〉 ∨       𝑣 ′ .(𝑔        )→(¬        𝑣.(𝑔   𝐿 𝑚 )) ⇒           〈𝜎 ′ ,   𝑣′,   𝑣〉



    Because FEther is a very large function written in the                                                  environment            and super-environment 𝑓               are
Gallina specification language, FEther differs from the                                                     equivalent, except for their gas values, which are initialized
kernel of other real-world virtual machines of high-level                                                   by the helper function          𝑣 , and the initial gas value of
programming languages, such as Smalltalk, Java, and Net,                                                          is set by    𝑔  . Finally, the initial memory state is set
which support bytecode as their ISA, and are implemented                                                    by      𝑚 𝑚 , considering 𝑃(       ) and the standard library
by translating the bytecode for commonly used code paths                                                      𝑏 as arguments.
into native machine code. In our work, FEther takes the                                                        In addition, according to the construction of Lolisa
executable semantics of Lolisa as the ISA, which is                                                         mentioned previously, FEther is also separated as four
employed to specify the semantics of the syntax tokens to                                                   levels, and it benefits from Lolisa by achieving low
represent their execution behaviors accurately. Currently,                                                  coupling between the executable semantics at same layers
FEther fully supports all semantics of Lolisa.                                                              and at different layers. Specifically, the executable
    The validation checking mechanism includes both                                                         semantics at same levels are independent of each other, and
checking the validation of the results (including memory                                                    are encapsulated as modules with a set of interfaces. At
states and memory values) and checking the execution                                                        different layers, higher-layers’ semantics can only access
condition. Because all functions are vulnerable to undefined                                                lower-layers’ semantics via interfaces, and the
conditions due to various causes, we develop functions with                                                 implementation details of lower-layer semantics are
the help of a monad [40]. Here, all functions are tagged by                                                 transparent to higher-layer semantics, which is represented
an option type. If a function generates a valid result, the                                                 by the dashed-line box in Fig.5. The implementation of
result will be returned in the form of Some t. Otherwise, it                                                higher-layer semantics is also not dependent on the details
will be returned as an undefined value None. In addition,                                                   of lower-layer semantics. In this manner, FEther can be
the symbol ⟦ ⟧ represents a term t tagged by the option                                                     extended, as is discussed in Section VI.
type.
    To avoid the execution of infinite loops in programs,                                                   D.ASSISTANT TOOLS AND LIBRARIES
FSPVM-E also adopts a K-step limitation mechanism,                                                          The assistant tools and automation-assisting libraries of
where, similar to Bounded Model Checking (BMC) [41],                                                        FSPVM-E are used to reduce the manual workload and
we limit FEther to executing a 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 K times at                                                        increase the degree of automation when users deploy
most. This gas mechanism design well suits the BMC                                                          FSPVM-E, formalize target smart contracts, and verify
approach. Therefore, our implementation uses gas to limit                                                   properties.
the execution of Lolisa programs in FEther. To be specific,
The semantics governing the execution of a Lolisa program                                                   Assistant Tools. As discussed previously, FSPVM-E
  𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 (abbreviated as 𝑃( )) are defined by                                                           includes customizable components for implementing the
the rule 9 and 10, where ∞ refers to infinite execution and                                                 specific requirements of users, such as memory space and
T represents the set of termination conditions for finite                                                   label addresses, that must be defined dynamically. Taking
execution. These rules represent two conditions of 𝑃( )                                                     the memory space given in Fig.4 as an example, the size of
execution. Under the first condition governed by the rule 9,                                                the specific formal memory space depends on the size that
𝑃( ) terminates once a finite number of steps owing to                                                      users require. The enumeration of memory blocks is
some reasons, such as exception or natural termination. And                                                 conducted manually as rule 11.
the 𝐹𝐸 𝑟(⟦𝑚′ ⟧,             ′, 𝑓
                                  , 𝑎𝑟𝑔 , 𝑃( )) represents                                                  memory ≡ Record⟨maddr ∗ , mvalue ∗ ⟩                      (11)
the specific enter point of the whole FEther interpreter.                                                      Clearly, defining a specific memory space by
Under the second condition governed by the rule 10,                                                         enumerating blocks manually would be very tedious work.
𝑃( ) cannot terminate via its internal logic and would                                                      Fortunately, all dynamic specifications like rule 11 above
undergo an infinite number of steps. Therefore, 𝑃( ) is                                                     have fixed abstract models. Therefore, these dynamic
deliberately stopped via the gas limitation checking                                                        specifications can be generated recursively by a generator
mechanism that the execution will be terminated after the                                                   written in a high-level programming language such as Java
gas balance is reduced to zero. Here, 𝑜 𝑎𝑟 represents a                                                     or C++. In addition, smart contracts written in Solidity can
list of optional arguments. In addition, the initial                                                        be translated into Lolisa, and vice versa, with a line-by-line



                                                                                                                                                                                        11
                                                                     Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



correspondence, which are operations that can negatively        pre conditions and post conditions and complete the
impact consistency. Similar to the process of converting        mathematical reasoning during property verification. The
Fig.8a--d, we develop a translator as a compiler front end to   workflow of the tactic modeling is also defined in Fig.10.
automatically convert Solidity programs into the macro          For Coq operating in the proof pattern, the 𝑜𝑏 𝑟       (OB)
definitions of the Lolisa abstract syntax tree. The             function scans the current context 𝐶 to obtain the current
abstraction process is given formally by the rule 12.           goal. Each component in sequence attempts to capture the
                                  𝑦   𝑑                         operational characteristic of the current goal and select the
Г ⊢ 𝑇𝑜𝑜 (𝑟) ↪           𝑓 𝑎 𝑜 →        . 𝑓              (12)
                                                                matching tactics. The selected tactics are combined into a
    Here, in the rule 12, assistant tools function Tools
                                                                solution tactic 𝐿 𝑎 that solves the goal in the TCOC. The
employs a specific user requirement 𝑟 with type ℛ as a
                                                                new context 𝐶 is compared with 𝐶 in 𝑜 𝑥 𝑑 𝑐 . If 𝐶
parameter within the proof context 𝛤. Assistant tools then
                                                                and 𝐶 are identical, the current tactics cannot solve the
generate the respective formal specifications and export
                                                                goal automatically, and the tactic modeling process is
them as .v files that can be loaded in Coq directly. In this
                                                                terminated. Otherwise, the tactic modeling continuously
manner, the mechanical processes of FSPVM-E
                                                                attempts to simplify the goal of 𝐶 .
initialization and translation from Solidity into Lolisa can
                                                                    An example of the Ltac-based tactic modeling is given as
be completed automatically. However, as introduced above,
                                                                rule 15.
the assistant tools of current framework are developed in
                                                                𝐿𝑎       𝑓𝑜 𝑑𝑚𝑜𝑑 𝑦 ≔
C++ without certification. This limitation will be resovled
in our next version by developing them in Coq directly.         𝑚𝑎      𝑔𝑜𝑎 𝑤
                                                                | [ |− 𝑜 𝑥 [? 𝑌 (? 𝑋: 𝑚 𝑚𝑜𝑟 )(? 𝑍: 𝑎 )]] ⇒
Assistant Libraries. In standard manual modeling                    𝑓𝑜 𝑑 𝑌     ∗; 𝑏      ∗
technology, different formal models with significantly              𝑑.                                            (15)
different structures and verification processes can be              Here, the unfold_modify tactic is a sub-tactic of a
constructed in various programs. Hence, designing a set of      memory operation that captures parts of the operational
tactics that automatically verifies models in different         characteristics of a specific 𝑤𝑟 𝑑 𝑟 function, and
programs is nearly impossible. However, symbolic                evaluates 𝑤𝑟 𝑑 𝑟 using basic built-in tactics.
execution in FSPVM-E corresponds to both function
evaluation and program verification, as indicated by the rule    𝑓    𝑟 𝑇 𝑔𝑜𝑎      ↪ 𝐿𝑎      𝑇 𝑖

13.
                                                                                                       𝐿 𝑎 , 𝑔𝑜𝑎
𝛺, 𝛭, ℱ ⊢ 𝑃 𝑥 ≡ 𝑃 𝑣 ≡ 𝑃𝑣 𝑟 𝑦                      (13)           𝑓    𝑟𝐸𝑇 𝑔𝑜𝑎      ↪ 𝐿 𝑎 𝐸𝑇 𝑖                      𝑇𝐶𝑂𝐶 𝐿 𝑎 , 𝑔𝑜𝑎
   Specifically, the verification process 𝑃𝑣 𝑟 𝑦 of different
programs is equivalent with the respective symbolic              𝑓    𝑟 𝑇 𝑔𝑜𝑎      ↪ 𝐿𝑎     𝑇 𝑖                             𝐶′
execution process 𝑃 𝑥 in FSPVM-E. In other words, the
                                                                                                   𝐶     𝐶
symbolic execution process unifies the verification                        𝑜𝑏 𝑟     𝐶                               𝑜   𝑥 𝑑 𝑐 𝐶, 𝐶 ⇒ 𝐶 ′
processes of different programs in higher-order theorem-
proving assistants by simplifying the program evaluation        Fig.10. Automatic tactic modeling process based on the Ltac mechanism
                                                                provided by Coq. The process is constructed from three components:
process of FEther with different 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 in                  memory operating tactics (MTS), execution tactics (ETS), and verification
FSPVM-E. Because FEther takes the executable semantics          tactics (VTS), where each component in sequence attempts to capture
of Lolisa as the ISA, FEther execution constitutes a fixed      the operational characteristic of the current goal and select the matching
                                                                tactics that are combined into a solution tactic 𝐋𝐭𝐚𝐜𝐢 .
and finite semantics set {𝒮 𝑥 0 , 𝒮 𝑥 1 , … , 𝒮 𝑥 𝑛 } .
Accordingly, we can design a corresponding automatic
tactic set   for each executable semantic 𝒮 𝑥 𝑖 , as rule 14.      Another assistant library is the static analysis library that
                                                                is used to collect the formal specifications of standard
∀ , 𝒮 𝑥 𝑖 ↔ ⊲ 𝑇 { 0, 1, … ,           }           (14)
                                                                vulnerabilities relevant to coding conventions. This static
   This can be expanded to accommodate all possible             analysis module is an independent auxiliary module besides
semantic conditions. We exploit this advantage for              the core hybrid verification module. This module is used to
designing primitive automatic tactics to automatically          check the basic and common vulnerabilities, such as such as
execute and verify the properties of smart contracts using      integer overflow, unchecked send bug4 and divide zero, to
the Ltac mechanism provided by Coq. As shown in Fig.10,         reduce workload of hybrid verification and improve
the Ltac-based tactic modeling is constructed from three        efficiency of FSPVM-E. These formal specifications are
components: memory operating tactics (MTS), execution           used to construct a static analysis mechanism to quickly
tactics (ETS), and verification tactics (VTS). As the           scan for bugs in the source code. The details of this library
component names suggest, MTS is applied to evaluate the
                                                                   4
requests of GERM APIs, ETS is used to simplify the                   unchecked send bug: http://hackingdistributed.com/2016/06/16/scanning-
                                                                live-ethereum-contracts-for-bugs/
executable semantics of Lolisa, and VTS can simplify the




                                                                                                                                        12
                                                                       Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



are discussed in Subsection V.A.                                      Besides, another benefit is that the self-correctness of
                                                                  functions and programs developed in Coq using native logic
IV. SELF-CORRECTNESS CERTIFICATION                                language Gallina, denoted as ℱ(𝑃𝑟𝑜𝑔𝑟𝑎𝑚) , can be
An essential issue that must be addressed before we can           certified in Coq directly.
verify smart contracts in FSPVM-E is the self-correctness             Taking a very simple example, when we develop an
of FSPVM-E. Because FSPVM-E is employed as the TCB                addition add in Coq using Gallina language shown as below,
solver for the evaluation and derivation of the formal            we can directly define critical properties in Coq by applying
specification models and properties of smart contracts, the       add function, such as associative property of addition
credibility of the analysis results is strongly associated with   plus_assoc shown below, to certify the self-correctness of
the correctness of the TCB. Similarly, ensuring the self-         this function directly.
correctness of the verification TCB for all static analysis       add = fix add (n m : nat) {struct n} : nat :=
tools is an unavoidable issue. However, the work of Gödel            match n with
has established that a logic cannot prove its own                    | 0 => m
consistency. As such, the fact that verifiers cannot verify          | S p => S (add p m)
themselves presents a paradox. Actually, most theorem                end.
proving assistants based on satisfiability modulo theories        Theorem plus_assoc : ∀ n m p : nat, add n (add m p) = add
(SMT) [42] and other types of static analysis tools based on      (add n m) p.
symbolic execution technologies assume that their                     Accordingly, FSPVM-E has a natural advantage
computation cores are correct, although correctness has not       compared with other program verification or analysis tools
been certified. Therefore, these tools are classified as          in that its three essential components are wholly developed
untrusted in many studies. In contrast, one of the most           in Coq, and it employs the TCOC as the TCB. In addition,
important features of FSPVM-E is that its self-correctness        the core components of FSPVM-E, including the GERM
can be ensured with a very high degree. This is explained in      framework, Lolisa, and FEther, are all implemented using
the following subsections. Here, we first demonstrate that        the Gallina specification language. Therefore, these are
the components of FSPVM-E in the trusted domain of Coq            respectively denoted as ℱ(𝐺𝐸𝑅𝑀) , ℱ(𝐿𝑜 𝑎) , and
can be verified directly. Secondly, we demonstrate that the       ℱ(𝐹𝐸 𝑟) . As such, the correctness of these three
components in the untrusted domain have no effect on the          components can be directly certified in Coq. Thus,
self-correctness of FSPVM-E from the perspectives of the          compared with other static analysis tools that must assume
minimum trusted computational base and the non-aftereffect        the correctness of the TCB, the smart contract verifications
property.                                                         that take the proposed FSPVM-E as the TCB must only
                                                                  trust the TCOC. The corresponding verification details are
A. MINIMUM TRUSTED COMPUTATIONAL BASE                             given elsewhere [11, 31, 32]. At present, the core functions
The development of methods to avoid the above-discussed           of FSPVM-E, which includes 74 theorems and 183 lemmas
paradox has been conducted since the 1940s, and these             in Coq, have been completely verified.
approaches have been summarized for proof assistants [37].
Briefly, the manual review of a very small kernel by experts
and the de Bruijn criterion [43] are two key approaches for
ensuring the trustworthiness of a proof assistant. However,
the TCB of most static analysis tools is an untrusted black
box with a very large kernel that cannot be certified
                                                                  Fig.11. Non-aftereffect relation between the dynamically generated
mathematically. Nor does it satisfy the de Bruijn criterion.      specifications of assistant tools with the direct certification of their self-
This has been addressed by the Coq team by making the             correctness in Coq.
TCOC very small, which has enabled the correctness of the
core code to be verified by the manual review of experts.         B. NON-AFTEREFFECT PROPERTY
Moreover, the TCOC also completely satisfies the de Bruijn        Although the kernel of FSPVM-E in Coq is verified, the
criterion. In addition, Harrison [44] has proven the              assistant tools are developed in the untrusted domain using
consistency of the HOL Light logical core (or, strictly           general-purpose programming languages. Therefore, these
speaking, a subset of the logical core) using HOL Light           tools are obviously vulnerable to incorrect specifications
itself based on the self-verification concept denoted as          that can have an impact on the correctness of FSPVM-E.
reflection, which is also supported in the TCOC. This proof       However, the correctness of assistant tools is difficult to
is also completed supported by Coq. Therefore, the TCOC,          audit and certify. Fortunately, the relationship between the
including the fundamental theory and specific                     assistant tools and their respective results satisfies the non-
implementation, is currently widely recognized as one of          aftereffect property. Here, although the assistant tools are
the most reliable trusted cores available.                        developed in the untrusted world to automatically generate




                                                                                                                                             13
                                                                                                Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)




                          provide                             depend                              depend        Execution
                                        Smart Contract                     User Requirements
                                                                                                               Environment
                                                                                                                                   Preliminary Requirements Analysis


                                                input                               manually define                    input

                                          Translator                                                             Generator

                                                translate                                                              generate


                                         Formal Smart       parameterize     Property                        Generated Formal
                          deploy        Contract Model                       Theorems                         Specifications
                                                                                                                                   Deployment and Formalization
                                                scan                                verify                             certify


                                       Static Analysis                       Hybrid Proof         initialize Self-correctness
                                         Theorems                           Virtual Machine                     Theorems



                                                                                    open proof universe
                                                              update
                                                                              Proof Goal
                                                                                    observe
                          launch
                                                  Trusted Core of      evaluate              invoke   Automatic Tactic             Automatic Verification
                                                                                  OB
                                                        Coq                                               Library

                                                                                                           Trusted Domain in Coq

Fig.12. Summary of FSPVM-E workflow.

the dynamic situation-dependent specifications of FSPVM-                               personal computers with equivalent hardware, including 8
E, these generated specifications are defined using Gallina,                           GB RAM and a 3.20 GHz CPU, and equivalent software,
and therefore can be verified in Coq straightly. Hence, as                             including Windows 10 and CoqIDE 8.6.
illustrated in Fig.11, the self-correctness of generated
specifications can be certified in Coq directly. As such, we                           A. CASE STUDY: HYBRID VERIFICATION SYSTEM
can conclude that the component of FSPVM-E affected by                                 Workflow. The general workflow of FSPVM-E can be
generated specifications is correct if the generated                                   defined in conjunction with Fig.12 that is explained as
specifications pass their correctness certifications. As such,                         follows. First, users should provide a smart contract.
the correctness of FSPVM-E is not influenced by the means                              According to the design requirements of smart contracts,
through which the assistant tools are implemented.                                     users should abstract them as pre and post conditions of
                                                                                       Hoare style properties. Next, users deploy this system in a
V. EXPERIMENT                                                                          specific circumstance by applying the generator and
We demonstrate the workflow and novel features of our                                  translator provided by the assistant tools. The generated
new toolchain in real-world practice by applying FSPVM-E                               formal specifications are certified by the self-correctness
to formalize and verify a Smart Sponsor Contract (SSC). An                             theorems stored in the assistant libraries before initializing.
SSC is a simple but classic Ethereum sponsor contract                                  These specifications are adopted in FSPVM-E if they
demo for new users on the IBM Cloud Laboratory website                                 satisfy the self-correctness theorems; otherwise, the
(https://developer.ibm.com/clouddataservices/2016/05/19/bl                             verification process is terminated. The translator
ock-chain-technology-smart-contracts-and-ethereum/). Its                               automatically reads the .sol file, translates the Solidity smart
simplicity makes it an ideal example in the present work.                              contract into the respective formal form in Lolisa, defines
This example offers an additional benefit, in that we have                             the program model, and allocates logic memory blocks for
verified this smart contract in our past work using a                                  all variables. Next, the static analysis module will apply the
standard theorem proving approach in Coq [45], and the                                 predefined theorems about basic vulnerabilities to scan the
source code can be downloaded from our Gitee site                                      formal version source code of target smart contracts. The
(https://gitee.com/zyangFV/SSC-manual-verification).                                   analysis results will be printed in the proof goals directly.
Therefore, we can clearly illustrate the advantages of                                 After that, the formal specification of smart contracts will
FSPVM-E by comparison with our past work. Only the                                     be parameterized into the properties of program
necessary code segments are presented in the following                                 requirements which are defined by users manually. Finally,
discussion to enhance the readability; however, the                                    the users need to open the proof universe, and the hybrid
complete code of this example is given in the Appendix,                                verification engine will finish the verification automatically.
and can also be downloaded from the cited IBM website.
The experimental environment employed 5 identical




                                                                                                                                                                       14
                                                                                 Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



      𝑺𝒚𝒏𝒕𝒂𝒙                                                                 hybrid verification, and a debugging mechanism. In Static
                                                                             Analysis Mechanism subsection, we will introduce the
     𝛤[𝒞]: : = 𝐷 | 𝑑 , ( ≥ 0)                                                process that static analysis module analyzes the pledge
     𝒞: : = 𝐷 | 𝑑̅ | 𝑑 | [ 0 , … , ]                                         function and finds out the basic vulnerabilities. In Hybrid
     𝐷: : = 𝐷 | 𝑑̅ | 𝑑                                                       Property Verification with Hoare Style subsection, we will
     𝑑: : = [ 0 , … , ], ( ≥ 0)                                              illustrate the details that hybrid verification engine verifies
Fig.13. Abstract syntax of a code segment definition in FSPVM-E, where
𝓒 represents the code segment, 𝚪[𝓒] denotes the current global context       important properties of SSC smart contract.
of 𝓒, 𝐜𝐢 represents a single instruction, 𝐝 represents a child definition,
𝐝̅ denotes possible sequences 𝐝𝟎 ,…, 𝐝𝐧 , and 𝐃 is a set of definitions.     Static Analysis Mechanism. The static analysis mechanism
                                                                             is an independent module, which is embedded within
                                                                             FSPVM-E to identify standard vulnerabilities related to
                                                                             coding conventions and coding mechanisms in smart
                                                                             contracts, such as integer overflow and unchecked send bug,
                                                                             rather than the logic of the service design. Of course, these
                                                                             vulnerabilities can be accurately identified by defining and
                                                                             verifying corresponding theorems, but this process
                                                                             generates a heavy and tedious workload. However, these
                                                                             vulnerabilities have distinct features that clearly distinguish
                                                                             them from logical vulnerabilities, and are accordingly
                                                                             identified easily and quickly using conventional static
                                                                             analysis technology. Therefore, static analysis is a better
                                                                             choice for supporting this type of security. Moreover, the
                                                                             line-by-line translation between Lolisa and Solidity ensures
                                                                             the consistency between smart contracts and corresponding
                                                                             formal models.
Fig.14. Partial Smart Sponsor Contract (SSC) model.                             As introduced in Subsection III.D, FSPVM-E includes a
   A section of the SSC generadted by the translator is                      static analysis library that contains standard vulnerability
shown in Fig.13, where 𝒞 represents the code segment,                        features and scanning functions. The abstract definition of
𝛤[𝒞] denotes the current global context of 𝒞 ,                                  𝑎 function is defined in rule 16. Here, a 𝑎 function
represents a single instruction, 𝑑 represents a child                        takes a signed by option type that the all code segments of
definition, 𝑑̅ denotes possible sequences 𝑑0 ,…, 𝑑 , and                     context 𝛤 will be scanned in the static analysis module.
𝐷 is a set of definitions. It should be noted that the essence               𝛤[𝒞] ⊢ 𝑎 ( 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 , 𝑓 𝑎 𝑟 ) ⇒ ⟦ ⟧                       (16)
of smart contract segment specifications in Coq is a logic                      If the      𝑎 function locates vulnerabilities, it will
term with a specific logic type list statement declared by a                 return 𝑆𝑜𝑚       𝑟𝑟𝑜𝑟 . Otherwise, it will return 𝑁𝑜      . For
definition, and FEther is driven by the executable semantics                 example, if we want to check if an unchecked send bug
of each abstract syntax. The abstract syntax of code                         problem exists in the pledge function, we need only apply
segment definition is also summarized in Fig.13. Hence,                      the corresponding scan function to validate the source code,
FEther has no limitations on the size and continuity of an                   as shown in Fig.16. A scanning result of None indicates that
input 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 , and even a single statement can be                        the target 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 contains no code segment with
defined in the proof context of FSPVM-E and symbolically                     a potential risk of the corresponding feature 𝑓 𝑎 𝑟 .
executed by FEther. As an example of the translation                         Otherwise, the code segment with the potential vulnerability
process, a formal model of a partial SSC (please see the                     will be located in the proof context. We have encapsulated
Appendix) is shown in Fig.14. In addition, the formal                        rule 16 in the current version of FSPVM-E with fixed
version of the pledge function of the SSC is presented in                    features to obtain the following particular scan functions.
Fig.15. We note that the formal version of the pledge                           𝑎      𝑢𝑟 𝑖 ∷        𝑎 𝑚       →𝑜 𝑜         𝑎 𝑚
function is very intuitive, and the critical requirement is the                 𝑎      𝑢𝑟 𝑖 ≔ 𝜆 ( :        𝑎 𝑚 ). 𝑎 ( , 𝑓 𝑎 𝑟 )
pledge operation succeeds if the input value is not 0, and                      In this manner, the generator can automatically replace
the closed flags complete and refunded are false. Finally,                      with the target 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 in all feature scanning
users need only operate Coq in its proof pattern, and launch
                                                                             functions, and automatically analyze 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚
FSPVM-E to automatically analyze and verify the smart
                                                                             according to all of its vulnerability features. This
contracts based on the requirements specified by the user.
                                                                             mechanism
We provide the following three basic analysis and
verification mechanisms in FSPVM-E: static analysis,




                                                                                                                                                    15
                                                                                 Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)




Fig.15. Formal version of the pledge function of the SSC.




Fig.16. Simple case study of scanning send check vulnerability.




Fig.17. Static symbolic execution process for verifying the pledge function with abstract symbol arguments.




Fig.18. Concolic symbolic execution process for verifying the pledge function.


provides FSPVM-E with the following advantages. First, it                   send bug.
provides an optional choice for users to check individual                      Of course, like similar conventional mechanisms, this
security vulnerabilities efficiently. Second, higher-order                  mechanism also has the potential for issuing false alarms
logic can be employed to formalize specifications that are                  and providing insufficient error reporting. Therefore, it is
more complex than standard specifications. Thirdly, the                     provided only as an optional and independent assistant
static analysis library can be extended by adding new                       mechanism for users to employ prior to property
specifications and functions for new vulnerabilities. Finally,              verification. To our best knowledge, this is the first time
as discussed in Subsection IV.A, this mechanism is                          that a static analysis mechanism has been embedded within
completely developed in Coq, so its correctness can be                      a Coq proof system for Ethereum validation.
certified in Coq. Currently, the demo version of FSPVM-E
can scan integer overflow, stack overflow and unchecked                     Hybrid Property Verification with Hoare Style. As




                                                                                                                                                    16
                                                                               Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



discussed in Section I, potential legal loopholes in smart                 and 𝑄{𝑚         }. If the equivalence is true, 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚
contracts represent subtle bugs that cannot be detected by                 satisfies the respective property theorem.
standard scanning technologies because these loopholes are                    Because the FEther is a black box for users, general
closely related to the logic of the specific source code.                  programmers need only be familiar with the mechanical
Solving this problem by means of automated theorem                         process of applying assistant tools and defining the initial
proving represents the most important core function of                     and final memory states with Hoare style logic. Therefore,
FSPVM-E. Here, FSPVM-E automatically verifies the                          FSPVM-E reduces the difficulty with which general
requirement properties defined by users based on higher-                   programmers can apply higher-order theorem proving
order logic using Hoare style proof derivations according to               technology to verify their smart contracts in Coq. In
the rule 17 which contains three parts.                                    addition, users can alter the symbolic execution process
P{minit }FEther(minit , programformal ,∗)Q{mfinal }        (17)            (including static, concolic, and selective symbolic execution)
    First, the precondition 𝑃 is defined by the initial                    during the verification process by defining the
memory state 𝑚          . The 𝑚          stores the essential              preconditions in different ways. This is explained in the
constraints that are formalized based on smart contracts                   following subsections taking the pledge function of the SSC
design requirements.                                                       as an example.
    Second, the 𝐹𝐸 𝑟 (𝑚 , 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 ,∗) is the
entry point of the symbolic execution engine. 𝐹𝐸 𝑟                         1) Static Symbolic Execution. The basic verification
should take 𝑚            , the target smart contract                       process is based on conventional symbolic execution. When
  𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 , and other inputs as parameters.                             the initial arguments are inductively defined with
    Third, the postcondition 𝑄 is defined by the expected                  quantifiers such as ∀ and ∃, the verification engine FEther
final memory state 𝑚        , which represents the expected                will follow the logic of the source code to traverse all cases
obligation of 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 .                                                 that satisfy the preconditions. Specifically, according to the
    This method has no strict restrictions on the specification            requirement given in Workflow subsection, if one of the
form of initial and final memory state definitions. The                    sponsor termination flags 𝑜𝑚           and 𝑟 𝑓 𝑑 is set as
property formalization process will be given as a case study               true or the donation amount is zero, the smart contract must
in the next subsection.                                                    be discarded. Following this requirement, the property
                                                                           formalization is given bellow.
    Because the Hoare logic derivation is equivalent to the
                                                                               First, the Lemma pledge_false defined in Fig.17
trusted execution of operational semantics, the execution of
FEther can be seen as a derivation process based on Hoare                  initializes (Bool (Some ? 𝑋)) , (Bool (Some ? 𝑌)) , and
logic following the executable semantics of Lolisa.                        (INT I64 Signed? 𝑍) by specifying ? 𝑋 , ? 𝑌, and ? 𝑍 as
                                   𝐹𝐸 ℎ 𝑟(𝑚𝑖𝑛𝑖𝑡 ,𝑐0 ,∗)                    inductive values representing all possible conditions of
                                   →                      𝑄00 {𝑚00 } 1     initial termination flags and the donation amount, namely,
                                   𝐹𝐸 ℎ 𝑟(𝑚𝑖𝑛𝑖𝑡 ,𝑐0 ,∗)
        } 0→
            𝐹𝐸 ℎ 𝑟(𝑚𝑖𝑛𝑖𝑡 ,𝑐0 ,∗)
                                   →                      𝑄01 {𝑚10 } 1 ↠   as               ∀ ( : 𝑏𝑜𝑜 )(𝐵𝑜𝑜 (𝑆𝑜𝑚          ))            ,
𝑃{𝑚
                                                  …                        ∀ (𝑟𝑓: 𝑏𝑜𝑜 )(𝐵𝑜𝑜 (𝑆𝑜𝑚 𝑟𝑓))                   ,            and
                                   𝐹𝐸 ℎ 𝑟(𝑚𝑖𝑛𝑖𝑡 ,𝑐0 ,∗)
                                                                           ∀ ( 𝑚: )(𝐼𝑁𝑇 𝐼64 𝑆 𝑔 𝑑? 𝑍), respectively.
                              {→             𝑄0 {𝑚0 } 1
                                                                           Specifically, the initial memory states 𝑚 to 𝑚4 that
     𝑄0 {𝑚0 }
                                                                           satisfy the pledge function and other essential preconditions
     Q1n {m1n } ?
               ↔ 𝑄{𝑚      }, ≥ 0, 𝑗 ≥ 0                 (18)               are defined first.
       …                                                                       Second, according to the requirement, the constraint of
       𝑗    𝑗
{ 𝑄 {𝑚 }                                                                   donation amont, 𝑜𝑚             and 𝑟 𝑓 𝑑 are defined as
   The inference process is given by the rule 18. Beginning                money = 0 ∨ 𝑜𝑚              = 𝑟 ∨ 𝑟 𝑓 𝑑 = true.
with 𝑚         as the precondition of program verification,                    Third, the formal specification fun_pledge and
FEther generates all possible proof subgoals, and logically                preconditions are given into the entry pointer of FEther,
                                                 𝑗
modifies the current memory state 𝑚 −1 , (𝑗 ∈ ℕ)                           denoted as test. Next, the expected postcondition that the
according to the semantics of each statement ci to generate                pledge function is not applied successfully is defined as
                                          𝑗   𝑗
all possible new postconditions 𝑄 {𝑚 } (i.e., the                          𝑆𝑜𝑚         _𝑚 in Fig.17.
preconditions of ci ). The theorems need only judge                            Finally, users need only mechanically apply the
whether the final output memory state 𝑚 obtained after                     compositive automatic tactics to initialize the preconditions
executing the final statement matches the correct memory                   as the initial execution environment, symbolically execute
state 𝑚         . Specifically, users need only apply the                  fun_pledge, and verify the equivalence between the
automatic tactics to automatically complete the symbolic                   execution result and the postcondition by forward reasoning.
execution of 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 , and prove the equivalence                        This represents the complete property verification process.
between the results of 𝐹𝐸 𝑟 (𝑚 , 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 ,∗)                            Programmers can execute and complete this property
                                                                           verification using the automatic tactics of FEther within




                                                                                                                                                  17
                                                                                   Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



0.861 s (right-hand side of Fig.17).                                         +[ 𝑚 , . . ,   ] ⊳ 𝛤 ′ (𝑑 ≝ [ 𝑗 , . . , 𝑘 ], 𝑑𝑗 ≝ [ 𝑚 , . . ,   ])
                                                                                                                                       ′
                                                                             = [ 0 , . . , ] + + ⋯ + +𝑑 + + ⋯ + +𝐷𝑘 ⊳ 𝛤 (𝑑 ≝
2) Concolic Symbolic Execution. Because Coq is also a
kind of functional programming language, it supports the                     [ 𝑗 , . . , 𝑘 ], 𝐷𝑘 ≝ 𝑑𝑗 ⊳ 𝛤 ′′ (𝑑𝑗 ≝ [ 𝑚 , . . , ]))
evaluation of specific real inputs. As shown in Fig.18, the                  𝑉 𝑟 𝑓 (𝒞) = 𝑉 𝑟 𝑓 ([ 0 , . . , ] + + ⋯ + +𝑑 + + ⋯ +
entry points test and code pledge are unmodified, and                        +𝐷𝑘 )
complete and refunded are replaced with specific values                          Therefore, the key point is whether 𝑉 𝑟 𝑓 ([ 0 , . . , ] +
true and false, respectively. The other constraints are still                + ⋯ + +𝑑 + + ⋯ + +𝐷𝑘 )                  is        equivalent to
inductively defined as abstract symbols. The functional                      𝑉 𝑟 𝑓 ([ 0 , . . , ]) + + ⋯ + +𝑉 𝑟 𝑓 (𝑑 ) + + ⋯ +
correctness with the specific inputs is then proven by the                   +𝑉 𝑟 𝑓 (𝐷𝑘 ).
lemma pledge_false. Because the inputs are specified, the                        First of all, any code segment 𝑑 that satisfies the syntax
number of possible execution paths is limited, and the                       given in Fig.13 will not be unfolded and executed and
execution time is reduced to 0.222 s (right-hand side of                     verified in FEther according to the rule 19.
Fig.18). This mechanism leaves extensible space support                                     𝐹𝐸 ℎ 𝑟(𝑚𝑖𝑛𝑖𝑡 ,𝑐0 ,∗)
                                                                             𝑃{𝑚       } 0→                        𝑄0 {𝑚0 }𝑑
for standard testing. Users can extend the generator or                      𝐹𝐸 ℎ 𝑟(𝑚0 ,𝑑,∗)                         ?
implement a new test mechanism to automatically generate                     →             𝑄1 {𝑚1 } ↠ ⋯ ↔ 𝑄{𝑚         }                (19)
test script to modify the initial arguments and validate target                 Obviously, we obtain the result 𝑃𝑑 {𝑚𝑑 } 𝑑 𝑄𝑑 {𝑚𝑑 } ,
programs.                                                                    which means that, according to the purposed precondition
                                                                             𝑃𝑑 {𝑚𝑑 }, 𝐹𝐸 𝑟(𝑚𝑑 , 𝑑,∗) will obtain the expected logic
3) Selective Symbolic Execution. This verification process                   state 𝑄{𝑚𝑑 }. In addition, because Coq employs a call-by-
allows programmers to extract segments of code from target                   name evaluation strategy [46], the bodies of all definitions,
programs, verify the properties of the selected code                         including functions and values, are stored in their own
segments separately, and apply these verified properties to                  contexts, and are not evaluated until they are needed in the
simplify the verification process of target programs. For                    current proof context 𝛤𝑐 . Therefore, any segment 𝑑 of the
example, a code segment 𝒞 can be redefined as follows.                       logic expression 𝜀 in the current proof context will not be
𝒞 ≝ 𝑑𝑐 = [ 0 , . . , ] + + ⋯ + +[ 𝑗 , . . , 𝑘 ] + + ⋯ +                      unfolded during the proof process until all instructions prior
+[ 𝑚 , . . , ] + + ⋯ + +[ 𝑦 , . . , 𝑧 ]                                      to 𝑑 have been executed in the proof context, as indicated
= [ 0 , . . , ] + + ⋯ + +𝑑 + + ⋯ + +𝑑𝑗 + + ⋯ +                               by the rule 20, where ⊳ denotes the binary




Fig.19. Selective symbolic execution process for verifying the pledge function.




                                                                                                                                                      18
                                                                         Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



relationship that each context has subcontext with                   +𝑉 𝑟 𝑓 (𝐷𝑘 ).
enscapluated definitions recursively.                                    As shown by the example in Fig.19, the pledge function
                                          𝑒𝑑𝑢𝑐𝑡𝑖𝑜𝑛
𝛤⊳𝒟(𝑑𝛤,𝛤 ′⊳𝒟(𝑑𝛤′ ,𝛤 ′′⊳𝒟(𝑑𝛤′′ ,… )))⊢𝜀 →         𝜀𝑛𝑓                 can be varied by exploiting the selective symbolic execution
                                                              (20)   of FEther. Programmers can extract the core code segment
       𝛤 ′⊳𝒟(𝑑𝛤′ ,𝛤 ′′⊳𝒟(𝑑𝛤′′ ,… ))⊢𝜀𝑛𝑓    𝑑𝛤
                                                                      𝑓 (𝑚 𝑔. 𝑎        = 0 || 𝑜𝑚        ||𝑟 𝑓 𝑑) { 𝑟𝑜𝑤(); }
   Moreover, if a proposition 𝑄 is a subset of a
                                                                     from the pledge function and redefine it as a new formal
proposition 𝑃 , 𝑃 can imply 𝑄 , which is denoted as
                                                                     definition 𝑑 denoted as fun_pledge_if, as shown in the red
∀ 𝑄. 𝑄 ⊆ 𝑃 ⊢ 𝑃 → 𝑄. This is formalized as the rule 21.
                                                                     box, which can in turn be independently verified by the
𝑃{𝑚 } ↠ 𝑄𝑐 {𝑚𝑐 }⊆𝑃𝑑{𝑚𝑑} 𝑑 𝑄𝑑 {𝑚𝑑 }
 𝑝 𝑐 𝑦                           ?
                                                                     pledge_false_select lemma. After combining the verified
→       𝑄𝑑𝑐 {𝑚𝑑 𝑐 } ↠ ⋯ ↔ 𝑄{𝑚           }                 (21)       fun_pledge_if code segment into the pledge function, the
   Here, if the final logic memory state 𝑄𝑐 {𝑚𝑐 } of the             verification of the pledge_false theorem can be completed
instruction set     prior to 𝑑 is a subset of the precondition       by invoking the pledge_false_select lemma. Clearly, the
𝑃𝑑 {𝑚𝑑 }, which has already been verified, 𝑃𝑑 {𝑚𝑑 } can be           pledge_false_select lemma can also assist in any other
specified as 𝑄𝑐 {𝑚𝑐 } by applying 𝑃𝑑 {𝑚𝑑 } → 𝑄𝑐 {𝑚𝑐 }, and           proofs that use the fun_pledge_if code segment.
𝑄𝑑 {𝑚𝑑 } can also be determined according to the specific            Capitalizing on this feature, FSPVM-E is able to improve
𝑃𝑑 {𝑚𝑑 }. This process is executed, and can be automatically         its reusability and mitigate the effects of path explosion by
completed in Coq using the eapply, eauto, and Hint Resolve           extracting important or universal code segments, and
tactics. As introduced previously, FSPVM-E takes the                 verifying them separately. The details of this process are
GERM logic memory state as the pre and post conditions in            discussed in Subsection V.D.
the Hoare triple. Therefore, the excepted abstract or specific
final memory state of can be taken as the initial memory             4) Debugging Mechanism. Finally, FEther provides an
state of 𝑑 . Obviously, if         is correct, its final logic       interactive debugging mechanism for users. Because FEther
memory state is a subset of its expected logic memory state.         is developed based on the GERM memory model, the
The same procedure can be adapted to an arbitrary                    formal intermediate memory states record the proof
definition set 𝐷. Hence, specifying all preconditions of 𝑑           information, such as logic invariants and expressions, of all
and 𝐷 by the input post conditions yields                            variables during the execution and verification process. The
𝑉 𝑟 𝑓 ([ 0 , . . , ] + + ⋯ + +𝑑 + + ⋯ + +𝐷𝑘 ) =                      proposed mechanism employs the debugging tactic
𝑉 𝑟 𝑓 ([ 0 , . . , ]) + + ⋯ + +𝑉 𝑟 𝑓 (𝑑 ) + + ⋯ +                    step_debug to enable the




Fig.20. Example of the debugging mechanism provided by FSPVM-E.




                                                                                                                                            19
                                                                                  Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)




Fig.21. Formal intermediate memory states during the verification process of the pledge function.


step-by-step debugging of a smart contract by manually                      program cannot be ensured formally, which represents one
tracing these intermediate memory states. As shown in                       of the most troubling problems associated with higher-order
Fig.20, the states of all memory blocks at the current break                theorem proving technology. As shown in Fig.22, which
point are printed in the proof context. Programmers can                     was extracted from our previous work [33], the abstract
extract a target code segment using selective symbolic                      formal specification of the pledge function in the Gallina
execution with debugging tactics, and trace the intermediate                specification language is far different from the
memory states to locate bugs. Fig.21 shows the formal                       corresponding source code given in Fig.15 and the
intermediate memory states obtained during the execution                    Appendix, even though it accurately defines the behavior of
and verification of the pledge function using FEther in the                 the pledge function. This flexibility in the abstraction and
proof context. Then, we can compare the mechanized                          translation processes leads to a general lack of consistency
verification results and the manually obtained results to                   between the formalization results obtained by different
validate the semantics of Lolisa. In addition, the application              researchers, and the consistency between formal
of FEther based on Lolisa and the GERM framework also                       specifications and corresponding source programs is also
certifies that our proposed FSPVM-E is feasible. Here, the                  very difficult to certify. As a result, the formal model runs
logic memory states during execution can be observed in                     the risk of misunderstanding the source program logic and
the proof context.                                                          implementation, and may import vulnerabilities not existing
                                                                            in the original program, or remove vulnerabilities existing
B. ADVANCED FSPVM-E FEATURES                                                in the source code as an unintended result of the abstraction
The advanced features of the purposed FSPVM-E include                       and translation processes.
consistency, automation, and evaluation efficiency, which
are summarized individually in the following subsections.

Consistency. The consistency feature of FSPVM-E includes
language formalization consistency and execution and
verification consistency.                                                   Fig.22. Manually translated version of the formalized pledge function [45].
1) Language Formalization Consistency. This consistency
feature refers to the line-by-line translation between Solidity
and Lolisa following the formalized syntax of Solidity.                        Although, in current FSPVM-E, the translator is
Many well known higher-order logic theorem proving                          developed in untrusted domain using C++ that we cannot
frameworks, such as deep specifications [23], require                       guarantee the correctness of it, as indicated by the following
researchers to manually abstract or rebuild the resource                    rule
code of target programs as computational formal                              𝑟𝑜𝑔𝑟𝑎𝑚𝑟𝑤 ∈ 𝑆𝑜 𝑑         ∧ 𝒯( 𝑟𝑜𝑔𝑟𝑎𝑚𝑟𝑤 ) ∈ 𝐿𝑜 𝑎 ⊢
specifications in higher-order logic theorem proof assistants,               𝑟𝑜𝑔𝑟𝑎𝑚𝑟𝑤 ≡ 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚                                    (22)
and the overall process depends entirely on the experience,                 where the symbol 𝒯 represents the translation process, in
knowledge, and proficiency of researchers rather than on a                  contrast with conventional approaches, Lolisa has
standardized and mechanized criterion. As a result, the                     mechanized most syntax and corresponding semantics of
consistency between the formal model and the original                       Solidity into Coq. In addition, the formal syntax of Lolisa
                                                                            has also been encapsulated into the syntactic abbreviations



                                                                                                                                                     20
                                                                       Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



using the Notation macro mechanism, and hides the fixed            Automation. As demonstrated by the case studies, another
formal syntactic components. Benefiting from this,                 very important feature of FSPVM-E is its high level
theoretically, the formal version of smart contracts is very       automation of higher-order theorem proving. The ratio of
similar to their original version, so the equivalency of small     source code size to proof code size in many conventional
size smart contracts could be reviewed by experts or third-        higher-order theorem proving approaches (e.g., [23, 47])
party plug-ins. Hence, as demonstrated by Figs.14 and 15,          varies linearly in the range of about 20: 1 to 40: 1, and the
smart contracts can be translated from Solidity into Lolisa        workload can be summarized by the rule 25, including the
line-by-line. Therefore, rule 22 above can be transformed          size of manual formalization and verification.
into the following rule:                                           𝑤𝑜𝑟 𝑜𝑎𝑑𝑚 𝑢 =
  𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 ≡ 𝑟𝑜𝑔𝑟𝑎𝑚𝑚𝑜𝑑                                  (23)          (𝑓𝑜𝑟𝑚𝑎 𝑎 𝑜 ) +             ( 𝑟 𝑓 𝑎 𝑜 )+
and 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 can be directly executed and verified                    ( 𝑟𝑜 𝑟 )                                              (25)
in Coq with the help of FEther. Accordingly,                           Similar to these conventional approaches, properties
  𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚        is actually the corresponding formal           must be manually defined in FSPVM-E. However, the size
specification model 𝑟𝑜𝑔𝑟𝑎𝑚𝑚𝑜𝑑 at the code level.                   of the source code and the size of the proof code no longer
Furthermore, according to logic transitivity, rules 8, 19, and     have any direct relationship in FSPVM-E owing to the high
23 can be combined to obtain the following rule.                   level of automation of the formalization and verification
  𝑟𝑜𝑔𝑟𝑎𝑚𝑟𝑤 ∈ 𝑆𝑜 𝑑          ∧ 𝒯( 𝑟𝑜𝑔𝑟𝑎𝑚𝑟𝑤 ) ∈ 𝐿𝑜 𝑎 ⊢                processes.
  𝑟𝑜𝑔𝑟𝑎𝑚𝑟𝑤 ≡ 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 ≡ 𝑟𝑜𝑔𝑟𝑎𝑚𝑚𝑜𝑑                       (24)         The individual components of the workload for FSPVM-
   Therefore, the target smart contract 𝑟𝑜𝑔𝑟𝑎𝑚𝑟𝑤 is                E (i.e., 𝑤𝑜𝑟 𝑜𝑎𝑑𝐹 𝑃 −𝐸 ) can be analyzed as follows.
consistent with its formal model 𝑟𝑜𝑔𝑟𝑎𝑚𝑚𝑜𝑑 in the                  First, as introduced in the above discussion regarding
proposed FSPVM-E.                                                  language formalization consistency, the formalization
   Because a simple translator can translate Solidity into         process is entirely unified as a line-by-line translation from
Lolisa line-by-line automatically, and researchers can check       Solidity to Lolisa, and we have already implemented a
the     consistency      between        𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚         and     translator to make the translation process fully automatic.
                                                                   Therefore,         (𝑓𝑜𝑟𝑚𝑎 𝑎 𝑜 ) is zero. Second, the
  𝑟𝑜𝑔𝑟𝑎𝑚𝑚𝑜𝑑 , this process ensures the objectivity of the
formal model, and depends in no way on the experience,             ability of most mainstream interactive proof assistants, such
knowledge, and proficiency of researchers. Thus, this              as Coq and Isabelle, to reduce the workload associated with
process guarantees consistency between the source program          verification is limited, despite the fact that they provide
and the respective formal model. Although the equivalence          tactic mechanisms to help users design proving tactics to
between Solidity and Lolisa cannot be totally guaranteed in        simplify the program evaluation process and construct
current version FSPVM-E due to the limitation of the               proofs automatically. This is because the above discussed
translator, this is a best effort to preserve the equivalence      differences among the different formal models derived from
between two languages. Besides, we also have planned to            manual design make it difficult to design tactics that can
develop a trusted translator in Coq directly.                      verify formal models in a fully automatic fashion. However,
                                                                   in contrast to conventional verification approaches and
2) Execution and Verification Consistency. The execution           frameworks, FSPVM-E standardizes the verification
consistency refers to the accuracy with which the symbolic         process as the execution of smart contracts in FSPVM-E
execution of smart contracts in FSPVM-E simulates the              according to rule 13. In addition, as discussed in Subsection
actual behaviors of smart contracts when they are executed         III.D, the finite number of executable semantics and
in the real world. As elaborated by the design and the case        operations in FSPVM-E facilitates the development of
studies given above, this feature is successfully facilitated in   design strategy sets to automatically accommodate all
FSPVM-E by several ways. First, the GERM framework                 possible semantic conditions, and these strategies are
virtualizes the architecture and operations of real world          encapsulated as three basic tactics. The substantial
                                                                   reduction in        ( 𝑟 𝑓 𝑎 𝑜 ) facilitated by FSPVM-E
memory hardware, and the semantics of Solidity has been
mechanized into Coq as the core of FEther. Moreover,               is well illustrated by comparing the verification of the
Ethereum smart contracts written in Lolisa can be directly         pledge_false theorem shown in Fig.17, which requires only
executed in FSPVM-E. Hence, the execution and                      a single line of code, with that obtained by directly
verification level of FEther functions directly on what is         verifying pledge_false using the conventional tactics of Coq,
essentially Solidity code rather than byte code, which             as shown in Fig.23, which requires 20 lines of complex
avoids the risk of errors during compilation. Therefore, the       tactics. dThese three basic tactics can be applied manually
symbolic execution of target smart contracts in FSPVM-E            or invoked automatically with the help of script programs.
accurately reflects their behaviors in the formal systems of       According       to     these     features   of     FSPVM-E,
                                                                        ( 𝑟 𝑓 𝑎 𝑜 ) can be reduced to zero theoretically.
Coq.




                                                                                                                                          21
                                                                                     Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)




Fig.23. Verification of the pledge function using the built-in tactics of Coq.


   Finally, the above discussion indicates that                                  efficiency of the formal verification engine is also an
𝑤𝑜𝑟 𝑜𝑎𝑑𝐹 𝑃 −𝐸 is related only to the size of the                                 essential evaluation criterion. Our previous version of
verification    properties,  i.e.,   𝑤𝑜𝑟 𝑜𝑎𝑑𝐹 𝑃 −𝐸 =                             FEther obtained good computing efficiency during
     ( 𝑟𝑜 𝑟 ), which depends on the complexity of the                            verification relative to most verification tools for which the
requirements of target programs rather than on the size of                       computing efficiency is generally quite low. However, we
their source code.                                                               found that call-by-name termination (CBNT), information
                                                                                 redundancy explosion (IRE), and concurrent reduction (CR)
              Verification Workload Comparation                                  problems could greatly reduce the computational efficiency
                            for SSCs                                             of FEther when verifying large programs. Therefore, we
                1400
                1200                                                             have applied the optimization algorithms in [33] that are
                1000                                                             dedicated to solving these problems to optimize FEther.
  Code size




                 800                                                             Briefly, if the CBNT, IRE, and CR problems are triggered
                 600
                 400                                                             simultaneously, the evaluation strategy of higher-order logic
                 200                                                             proof assistants will cause FEther to employ the entire
                   0
                          Smart                         Draw                     𝑃𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 rather than a single statement as an
                                   Pledge    Refund                Total
                         Sponsor                        Down                     evaluation unit, which generates a very large amount of
              Standard    143       371       377        392       1283          redundant logic information. This condition is summarized
              FSPVM-E      34       52         50        74        210           by the formulae 26 where 𝑜 𝑢𝑏 represents the average
              Source       18       10         9         15         52           number of constructors without sub-branches,                𝑢𝑏
                                                                                 represents the average number of constructors with sub-
                                                                                 branches, 𝑢𝑏𝑗 and 𝑜 𝑢𝑏𝑗 represent the number of sub-
Fig.24. Comparison of the verification workloads of a conventional
                                                                                 branches of 𝑢𝑏𝑖 ( , 𝑗 ∈ ℕ, 0 ≤ ≤ 𝑗), 𝑟0 to 𝑟 represent
theorem proving approach and FSPVM-E for SSCs.                                   the number of values constructed by different datatypes,
                                                                                 and       0 to         represent the number of constructors
   Fig.24 shows that, compared with our previous work for                        for each respective datatype. In addition, 𝑓𝑜𝑟 𝑧 also
SSC verification [45], the workload of FSPVM-E has been                          contains basic expressions and definitions that can be
significantly reduced. Here, the workload of the                                 evaluated directly, and the average number of these basic
formalization and verification processes in our previous                         expressions and definitions are defined as           and 𝑑 ,
work are 1283 lines of Coq, which represents a source code                       respectively.
size to proof code size ratio of about 27: 1. However, the
                                                                                   𝑓𝑜𝑟 𝑧 ≡ (∑ =0 (           +𝑑 +          𝑜 𝑢𝑏𝑖 + [ 0
                                                                                                                                      𝑟     …    𝑟]∗
manual workload in FSPVM-E is only 210 lines of Coq,
which represents a source code size to proof code size ratio                          0
of about 4: 1.                                                                   [ … ]) ∗      𝑢𝑏𝑖−1 !) +         ( 𝑟𝑜𝑔𝑟𝑎𝑚 𝑜𝑟𝑚 )                     (26)

High Evaluation Efficiency. Although high level                                     The previous version of FEther was developed strictly
automated verification is very important, the computing                          following standard interpreter tutorials that explicitly



                                                                                                                                                        22
                                                                                   Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



declare sequence statement semantics. As such, the basic                      was decreased from 92.546 s to 0.035 s. As such, the
functionality of this version can be illustrated by the                       optimized version requires just 3/10000 of the time required
following simple conditional statement of 𝑜𝑏 𝑔𝑎 𝑜 ℎ𝑟𝑜𝑤                        by the non-optimized version. In fact, the entire example
rule 27.                                                                      verifications presented in Subsection V.A required less than
𝑜𝑏 𝑔𝑎 𝑜 ℎ𝑟𝑜𝑤 ≝                                                                1 s. In addition, we also compared the results obtained with
∀( , ′ : 𝑎 𝑚 ), 𝑓 ( 𝑟 ){ h𝑟𝑜𝑤 (); }               { ; } (27)                  the optimized and non-optimized versions of FEther under
    This simple code segment will execute h𝑟𝑜𝑤 () to                          equivalent experimental environments with an equivalent
throw out an executing program and return the initial                         data set extracted from a previous study. Under the
memory state 𝑚         when the condition ( 𝑎         == 0 ∨                  experimental environment given above, each computer
  𝑜𝑚       𝑑 ∨ 𝑟 𝑓 𝑑) is evaluated as true. However, the                      executed the same data set 150 times to obtain the average
evaluation process of 𝑜𝑏 𝑔𝑎 𝑜 ℎ𝑟𝑜𝑤 generates 10,736                           number of executions required by the FEther evaluation
lines of logic expressions, and, as shown in Fig.25,                          process. In addition, we set an execution time limit of 3600
executing (i.e., verifying) this very simple code segment                     s to obtain sufficient experimental data. The experimental
using the non-optimized development of FEther requires an                     environments included a specific initial state and an abstract
execution time of 92.546 s, which is unacceptably long.                       initial state, whose initial arguments of the programs are
    In response to this issue, we optimized FEther [32] by                    defined inductively using quantifiers (such as ∀ and ∃) to
applying three proposed optimization schemes, including                       logically express all possibilities. As shown in Fig.27, the
redefining semantics, deeply embedding, and multiple                          average execution times of the non-optimized version of
pumps. This optimized version of FEther is that employed                      FEther with both the specific initial state (SpecNOp) and
for the proposed FSPVM-E discussed in the present report.                     the abstract initial state (AbsNOp) increase rapidly with an
The current version of FEther takes a single statement as an                  increasing number of program lines, and exceed the time
evaluation unit, as indicated by the rule 28. Here, we assign                 limitation of 3600 s after executing about 30 and 20
   𝛤 as the number of basic optimal expressions in the                        program lines, respectively. Moreover, the ranges of
context 𝛤, and assign 𝑑 𝛤 and 𝑑 𝑔 as the number of all                        fluctuations in the execution times are large, as indicated by
bound names of definitions and general definitions in the                     the error bars. In contrast, the optimized version of FEther
context 𝛤, which are the entry points of the respective                       with both the specific initial state (SpecOp) and the abstract
definition bodies.                                                            initial state (AbsOp) exhibit a steadily increasing average
   𝑓𝑜𝑟 𝑧 ≡ 𝛤 + 𝑑 𝛤 + 𝑑 𝑔 +            ( 𝑎 𝑚 )            (28)                 execution time with respect to an increasing number of
    In this manner, the logic information size of an                          program lines. In addition, the error bars are much smaller
evaluation unit is maintained within a stable range without                   in this case. These results indicate that the execution
being affected by the size of the program. A comparison of                    efficiency of the current version of FEther far exceeded that
the result given in Fig.25 for the verification of                            of the previous non-optimized version of FEther developed
𝑜𝑏 𝑔𝑎 𝑜 ℎ𝑟𝑜𝑤 using the non-optimized version of                               in Coq in accordance with the standard tutorial.
FEther with the result given in Fig.26 using the current
version of FEther indicates that the symbolic execution time




Fig.25. Execution time of the original non-optimized version of FEther for the simple conditional statement pledge obligation given in (35).




Fig.26. Execution time of the optimized version of FEther for the simple conditional statement pledge obligation given in (35).




                                                                                                                                                      23
                                                                                                        Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



                                                                              Comparison of FEther optimization
                                                      10000



                                                       1000

                         Average execution time (s)
                                                        100


                                                                                                                                                 SpecNOp
                                                         10
                                                                                                                                                 AbsNOp
                                                                                                                                                 SpecOp
                                                                                                                                                 AbsOp
                                                          1
                                                                                                                                                 Limitation


                                                        0.1
                                                   0     5     10     15     20     25      30     35    40    45      50      55   60    65
                                      SpecNOp      0  30.574 39.334 59.451 136.45 579.66   3405    N/A   N/A N/A       N/A    N/A N/A N/A
                                      AbsNOp       0  203.53 308.15 723 3393.1 N/A          N/A    N/A   N/A N/A       N/A    N/A N/A N/A
                                      SpecOp       0   0.166 0.291 0.428 0.64 0.729        1.06   1.153 1.202 1.379   1.57   1.703 1.892 2.015
                                      AbsOp        0   0.374 0.606 1.038 1.283 1.509       1.85   2.074 2.306 2.829   3.07    3.22 3.581 3.972
                                      Limitation 3600 3600 3600 3600 3600 3600             3600   3600 3600 3600      3600   3600 3600 3600
                                                                                  Number of program lines
Fig.27. Comparison of the average evaluation times of optimized (Op) and non-optimized (NOp) FEther under specific initial states (Spec) and abstract
initial states (Abs) for previously published example smart contracts [4] as a function of the number of program lines.


                                                                                                  independent types, function specifications, and theorems to
                                                                                                  support new requirements. The means of facilitating this
                                                                                                  extensibility were briefly introduced in previous sections.
                                                                                                  Thus, the extensibility and universality of FSPVM-E are
                                                                                                  highly dependent on the extensibility of Lolisa and FEther.
                                                                                                  We deliberately incorporated sufficient extensible space in
                                                                                                  Lolisa and FEther to extend features, such as pointer
                                                                                                  formalization and the implementation of independent
                                                                                                  operator definitions. The architecture of the proposed
                                                                                                  preliminary scheme for extending Lolisa and FEther to
                                                                                                  other general-purpose programming languages is illustrated
                                                                                                  in Fig.28. Extensibility is further realized by the
                                                                                                  independence of syntax inductive predicates in the same
                                                                                                  level, which is further supported in the definitions of the
                                                                                                  semantics. Therefore, Lolisa can be extended to incorporate
                                                                                                  the features of other languages by adding new typing rule
Fig.28. Architecture for extending the core components of FSPVM-E to                              constructors in the formal abstract syntax and the
support other general-purpose programming languages of multiple                                   corresponding formal semantics in FEther. As shown in
blockchain platforms.
                                                                                                  Fig.28, except for the accommodation of specific Solidity
                                                                                                  data structures, such as contracts and mapping, the
                                                                                                  remainder of the Lolisa syntax definitions and semantics
VI. EXTENSIBILITY AND UNIVERSALITY                                                                were designed to be universally applicable to any other
While ensuring that the developed Ethereum-based                                                  general-purpose programming language. Furthermore,
verification platform faithfully captures the intended service                                    Lolisa and FEther were designed based on the GERM
properties of smart contracts written in Solidity is essential,                                   framework, which are appropriate for the formalization of
further ensuring that this development can be applied to                                          any programming language. Finally, as discussed previously,
multiple blockchain platforms is also of great value.                                             the complex Lolisa formal syntax is hidden in the syntactic
Therefore, implementing extensibility and universality in                                         abbreviations,     which      improves      user-friendliness
the FSPVM-E design was a goal considered from the                                                 significantly.
beginning of its development.                                                                        We treat Lolisa as the core formal language, which is
   First, we note that the implementations of the GERM                                            transparent for real-world users, and we logically classify
framework and the assistant tools and libraries are not                                           the formal syntax and semantics of Lolisa according to a
dependent on high-level specifications. Therefore, these                                          general component 𝒢 and n special components 𝒮 ,
components of FSPVM-E can be extended by adding new



                                                                                                                                                                           24
                                                                         Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



                                                              TABLE 5
                             FEATURE COMPARISONS OF FETHER SEMANTICS AND EXISTING SOFTWARE QUALITY TOOLS
       Tool        Spec.     Exec.       Certif.     Verif.       Debug.      Gas            Level                  Logic            Hybrid
Lem spec           Yes       Yes       Testing       Yes         No           No        Byte code             Higher order          No
Mythril            Yes       Yes       Testing       Yes         Yes          Yes       Byte code             First order           No
Hsevm              No        Yes       Testing       No          Yes          No        Byte code             None                  No
Scilla             Yes       No        Testing       Yes         No           No        Intermediate          Higher order          No
Solidity*          Yes       Yes       Verifying     No          No           No        Intermediate          First order           No
Cpp-ethereum       No        Yes       Testing       No          No           No        Byte code             None                  No
KEVM               Yes       Yes       Testing       Yes         Yes          Yes       Byte code             First order           Yes
FSPVM-E            Yes       Yes       Verifying     Yes         Yes          Yes       Solidity              Higher order          Yes

as defined by the rule 29.                                                  Spec.: suitable as a formal specification of the
𝐿𝑜 𝑎 ≝ 𝒢 ∪ (⋃ =0 𝒮 )                                     (29)                EVM language;
   As a result, a general-purpose programming language ℒ                    Exec.: executable on concrete tests;
can be formalized by the Lolisa subset 𝒢 ∪ 𝒮 by                             Certif.: certifiable self-correctness;
encapsulating the subset using notation as a symbolic                       Verif.: verifiable properties of EVM programs;
abbreviation 𝒩 for ℒ , which adopts syntax symbols that                     Debug.: provision of an interactive EVM debugger;
are nearly equivalent to the original syntax symbols of ℒ .                 Gas: tools for analyzing the gas complexity of an
With this method, each ℒ has a corresponding notation set                    EVM program;
𝒩 that satisfies 𝒩 ⊆ 𝐿𝑜 𝑎. This relation is defined by                      Level: analysis or verification level of code;
the rule 30.                                                                Logic: types of essential logic supported;
∀ ∈ ℕ. ℒ ↔ 𝒩 ≡ 𝒢 ∪ 𝒮                                     (30)               Hybrid: support for hybrid verification methods.
   As the corresponding definitional interpreter of Lolisa,
FEther inherits the extensibility advantages of Lolisa. At the    VIII. CONCLUSIONS AND FUTURE WORK
same level, any executable semantic 𝑆 𝑥 is independent of     We have presented a hybrid formal verification system
any other semantics, and all same-level semantics are         denoted as FSPVM-E, which combines symbolic execution
encapsulated into an independent module Therefore, FEther     and higher-order logic theorem proving for verifying the
is also extendible to new executable semantics to support     security and reliability of Ethereum-based smart contract
new abstract syntax of Lolisa without affecting the old       services. An analysis of past studies indicates that the
semantics.                                                    present work represents the first hybrid formal verification
                                                              system implemented in Coq for Ethereum-based smart
VII. COMPARISON WITH RELATED WORK                             contracts that is applied at the Solidity source code level.
Compared with most recent tools based on symbolic The foundation of FSPVM-E is a general formal memory
execution, FSVPM-E supports symbolic execution in model that simulates real world memory operations and
higher-order logic systems. Benefiting from this feature, provides a basic pointer arithmetic mechanism. The source
FSPVM-E not only can flexibly formalize and verify code of FSPVM-E is Lolisa, which is a large subset of the
properties of Ethereum-based services with Hoare style, but Solidity programming language. Lolisa is strongly typed
also obtains higher evaluation efficiency and degree of according to GADTs, and includes nearly all of the syntax
automation compared to standard higher-order logic in Solidity. Therefore, the two languages are equivalent,
theorem proving technologies. Moreover, FSPVM-E which solves the consistency problem in formalization. The
provides a formal memory model, a virtual symbolic execution engine of FSPVM-E is FEther, which supports
execution environment, and single statement unit evaluation, static, concolic, and selective symbolic execution
which solves the memory, environment, and constraint simultaneously. The execution engine is driven by the
solving problems of conventional tools based on symbolic executable formal semantics of Lolisa, and is able to strictly
execution. Moreover, FSPVM-E is first the verification simulate the service behaviors of smart contracts. In
system that provides a large subset of Solidity formal syntax addition, we provide two assistant tools and two assistant
and semantics with GADTs, and it is also the first proof libraries to increase the degree of automation in the
virtual machine can directly execute and verify Solidity FSPVM-E verification process. Specifically, the two
programs in Coq.                                              assistant tools are a translator and a generator, which are
   To compare differences between FSPVM-E and the respectively applied to automatically translate Solidity into
related works that have pulished open-source tools Lolisa, and generate specific formal specifications based on
introduced in Section I, more intuitively, we summarized a specified execution environment. The two assistant
the differences in Table 5. The compared features are listed libraries include a static analysis library and an automation
and defined as follows:                                       tactic library, which are respectively used to scan for




                                                                                                                                            25
                                                                                                               Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



standard vulnerabilities in smart contracts, and provide                                                  their kind assistance and LetPub (www.letpub.com) for its
fully-automatic execution (verification) tactics. In addition,                                            linguistic assistance during the preparation of this
we ensured that FSPVM-E is a trusted verification engine                                                  manuscript.
by verifying the self-correctness of the core components of
FSPVM-E in Coq. We have also provided simple case                                                         References
studies to demonstrate the novel features of FSPVM-E,                                                     [1] S. Nakamoto, “Bitcoin, A Peer-to-Peer Electronic Cash System,”
which include hybrid analysis functions, consistency,                                                          http://usebitcoins.info/index.php/bitcoin-a-peer-to-peer-electronic-
automation, and high evaluation efficiency. Finally, the                                                       cash-system. 2008.
extensibility and universality of FSPVM-E was                                                             [2] A. Narayanan, J. Bonneau, E. Felten, A. Miller, and S. Goldfede,
demonstrated, and a preliminary scheme was proposed to                                                         Bitcoin and Cryptocurrency Technologies: A Comprehensive
systematically extend FSPVM-E to support the verification                                                      Introduction. New Jersey, Princeton University Press, 2016, pp. 22–
of multiple blockchain platforms. As a result, we can now                                                      76.
directly verify Ethereum-based service contracts with high                                                [3] S. Wilkinson, T. Boshevski, J. Brandoff, J. Prestwich, G. Hall, P.
automation and evaluation efficiency in Coq directly.                                                          Gerbes, P. Hutchins, C. Pollard, “Storj a Peer-to-Peer Cloud Storage
    In the future, the Solidity language is still under                                                        Network,” https://storj.io/storjv2.pdf. 2016.
development and is therefore changing quickly, thus the                                                   [4] Ethereum,             “Ethereum         Solidity       Documentation,”
Lolisa language will be updated quite often in order to cope                                                   https://solidity.readthedocs.io/en/develop/. 2017.
for that. Besides, we expect to further develop FSPVM-E                                                   [5] M.S. Miller, C. Morningstar, and B. Frantz, “Capability-Based
until it is sufficiently powerful and friendly for use by                                                      Financial Instruments," Proc. 4th International Conference on
general programmers to automatically verify the properties                                                     Financial Cryptography Financial Cryptography (FC'00), pp. 349–
of their smart contract programming. First, we are working                                                     378, Feb. 2000, doi:10.1007/3-540-45472-1_24.
to introduce support for other Solidity features, such as                                                 [6] L. Luu, D.H. Chu, H. Olickel, P. Saxena, and A. Hobor, “Making
inline assembly and float datatype. Second, we will develop                                                    Smart Contracts Smarter,” Proc. 2016 ACM SIGSAC Conference on
a trusted translator in Coq directly and certify the                                                           Computer and Communications Security (CCS '16), pp. 254–269,
correctness of it. Third, we will attempt to implement                                                         Oct. 2016, doi:10.1145/2976749.2978309.
support for the EOS (https://eos.io/) blockchain platform.                                                [7] M. del Castillo, “The DAO Attacked: Code Issue Leads to $60
Finally, we will design a new verification strategy to                                                         Million Ether Theft,” https://www.coindesk.com/dao-attacked-code-
improve the automation of modular verification in FSPVM-                                                       issue-leads-60-million-ether-theft/. 2016.
E.                                                                                                        [8] J.D. Alois, “Ethereum Parity Hack May Impact ETH 500,000 or $146
                                                                                                               Million,”          https://www.crowdfundinsider.com/2017/11/124200-
APPENDIX                                                                                                       ethereum-parity-hack-may-impact-eth-500000-146-million/. 2017.
 contract smartSponsor {                          // refund the backers                                   [9] C.       Reitwiessner,       “Dev     Update:     Formal      Methods,”
  address public owner;                            function refund() {
  address public benefactor;                        int i = numPledges − 1;                                    https://blog.ethereum.org/2016/09/01/formal-methods-roadmap/.
  bool public refunded;                             if (msg.sender != owner || complete || refunded)           2016.
  bool public complete;                               throw;
  bool public refnd;                                if (drwbck) throw;                                    [10] P. Rizzo, “In Formal Verification Push, EThereum Seeks Smart
  bool public drwbck;                                 refnd = true;
                                                                                                               Contract Certainty,” http://www.coindesk.com/ethereum-formal-
  uint public numPledges;                           while (0 < numPledges) {
  struct Pledge {                                    if (pledges[i]. address.send(pledges[i].amount)) {        verification-smart-contracts/. 2016.
      uint amount;                                      numPledges--;
      address eth_address;                              i--;
                                                                                                          [11] Z. Yang, and H. Lei, “A General Formal Memory Framework in Coq
      bytes32 message;                               }                                                         for Verifying the Properties of Programs Based on Higher-Order
  }                                                  else throw;
  mapping(uint => Pledge) public pledges;           }                                                          Logic Theorem Proving with Increased Automation, Consistency, and
  // constructor                                    refunded = true;                                           Reusability,”           Compt.          Sci.,       available        at
  function smartSponsor(address _benefactor) {      complete = true;
      owner = msg.sender;                          }                                                           https://arxiv.org/abs/1803.00403, 2018.
      numPledges = 0;                               // send funds to the contract benefactor              [12] E. Hildenbrandt, M. Saxena, X. Zhu, N. Rodrigues, P. Daian, D. Guth,
      refunded = false; complete = false;            function drawdown() {
      refnd = false; drwbck = false;                  if (msg.sender != owner || complete || refunded)         and G. Rosu, “KEVM: A Complete Semantics of the Ethereum
      benefactor = _benefactor;                        throw;
  }                                                   if (refnd) throw;
                                                                                                               Virtual Machine,” http://hdl.handle.net/2142/97207. 2017.
  // add a new pledge                                  drwbck= true;                                      [13] Y. Hirai, “Defining the Ethereum Virtual Machine for Interactive
  function pledge(bytes32 _message) {                 if (benefactor.send(this.balance))
    if (msg.value == 0 || complete || refunded)        complete = true;                                        Theorem Provers,” FC 2017: Financial Cryptography and Data
       throw;                                         else throw;                                              Security, M. Brenner, K. Rohloff, J. Bonneau, A. Miller, P.Y.A. Ryan,
      pledges[numPledges]                             }
    = Pledge(msg.value, msg.sender, _message);     }                                                           V. Teague, A. Bracciali, M. Sala, F. Pintore and M. Jakobsson, eds.,
      numPledges++;                                                                                            FC 2017. Lecture Notes in Computer Science, Cham: Springer, pp.
  }
                                                                                                               520–535, 2017, doi:10.1007/978-3-319-70278-0_33.
Fig.A. 1. The source code of Smart Sponsor contract.
                                                                                                          [14] I. Grishchenko, M. Maffei, and C. Schneidewind, (2018, April). “A
                                                                                                               semantic framework for the security analysis of ethereum smart
Acknowledgment
The authors wish to thank Marisa and Zisheng Wang for




                                                                                                                                                                                   26
     contracts,” In International Conference on Principles of Security and        Programs,” Proc. 8th USENIX Conference on Operating Systems
     Trust (pp. 243-269). Springer, Cham.                                         Design and Implementation (OSDI'08), pp. 209–224, Dec. 2008.
[15] S. Amani, M. Bégel, M. Bortin, and M. Staples, (2018, January).         [29] Coq Development Team, “The Coq Proof Assistant Reference
     “Towards verifying ethereum smart contract bytecode in                       Manual,” https://coq.inria.fr/distrib/current/refman/. 2018.
     Isabelle/HOL,” In Proceedings of the 7th ACM SIGPLAN                    [30] Z. Yang, and H. Lei, “Formal Process Virtual Machine for Smart
     International Conference on Certified Programs and Proofs (pp. 66-           Contracts Verification,” Compt. Sci., vol. 14, no. 8, pp. 1726–1734,
     77). ACM.                                                                    Aug. 2018, doi:10.23940/ijpe.18.08.p9.17261734.
[16] R. Baldoni, E. Coppa, D. C. D’Elia, C. Demetrescu, and I. Finocchi,     [31] Z. Yang, and H. Lei, “Lolisa: Formal Syntax and Semantics for a
     “A Survey of Symbolic Execution Techniques,”. Compt. Sci.,                   Subset of the Solidity Programming Language,” Compt. Sci.,
     available at https://arxiv.org/abs/1610.00502, 2018.                         available at https://arxiv.org/abs/1803.09885, Apr. 2018.
[17] I. Sergey, A. Kumar, and A. Hobor, “Scilla: A Smart Contract            [32] Z. Yang, and H. Lei, “FEther: An Extensible Definitional Interpreter
     Intermediate-Level Language,” Compt. Sci., available at                      for Smart-Contract Verifications in Coq,” IEEE Access, vol. 7, pp.
     https://arxiv.org/abs/1801.00687, 2018.                                      37770-37791, doi: 10.1109/ACCESS.2019.2905428.
[18] R. O'Connor, “Simplicity: A New Language for Blockchains,” Proc.        [33] Z. Yang, and H. Lei, “Optimization of Executable Formal Interpreters
     2017 Workshop on Programming Languages and Analysis for                      Developed in Higher-Order Logic Theorem Proving Systems,” IEEE
     Security       (PLAS'17),        pp.     107–120,      Oct.     2017,        Access,      vol.      6,     pp.    70331–70348,        Nov.    2018,
     doi:10.1145/3139337.3139340.                                                 doi:10.1109/access.2018.2880692.
[19] K. Bhargavan, A. Delignat-Lavaud, C. Fournet, A. Gollamudi, G.          [34] P. Wadler, “Propositions as Types,” Commun. ACM, vol. 58, pp. 75–
     Gonthier, N. Kobeissi, et al. (2016, October). Formal verification of        84, Dec. 2015, doi:10.1145/2699407.
     smart contracts: Short paper. In Proceedings of the 2016 ACM            [35] H. Xi, C. Chen, and G. Chen, “Guarded Recursive Datatype
     Workshop on Programming Languages and Analysis for Security (pp.             Constructors,” ACM SIGPLAN Notices, vol. 38, pp. 224–235, Jan.
     91-96). ACM.                                                                 2003, doi:10.1145/640128.604150.
[20] M.         Norrish,         “C       Formalised       in       HOL,”    [36] C. Ballarin, Interpretation of locales in Isabelle: Theories and proof
     http://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-453.pdf. 1998.                 contexts. In International Conference on Mathematical Knowledge
[21] X. Leroy, “The CompCert C Verified Compiler: Documentation and                Management (pp. 31-43). Springer, Berlin, Heidelberg. (2006,
     User’s Manual,” http://compcert.inria.fr/man/manual.pdf. 2018.                August)
[22] A.W. Appel, “Verified Software Toolchain,” ESOP 2011:                   [37] C. Paulin-Mohring, “Introduction to the Coq Proof-Assistant for
     Programming Languages and Systems, G. Barthe, eds., ESOP 2011.               Practical Software Verification,” Tools for Practical Software
     Lecture Notes in Computer Science, Berlin: Springer, pp. 1–17, 2011,         Verification, B. Meyer and M. Nordio, eds., LASER 2011. Lecture
     doi:10.1007/978-3-642-19718-5_1.                                             Notes in Computer Science, Berlin: Springer, pp. 45–95, 2012,
[23] R. Gu, J. Koenig, T. Ramananandro, Z. Shao, X. Wu, S.C. Weng, H.             doi:10.1007/978-3-642-35746-6_3.
     Zhang, and Y. Guo, “Deep Specifications and Certified Abstraction       [38] X. Leroy, and S. Blazy, “Formal Verification of A C-Like Memory
     Layers,” Proc. 42nd Annual ACM SIGPLAN-SIGACT Symposium                      Model and Its Uses for Verifying Program Transformations,” J.
     on Principles of Programming Languages (POPL'15), pp. 595–608,               Autom. Reason., vol. 41, pp. 1–31, Sep. 2007, doi:10.1007/s10817-
     Jan. 2015, doi:10.1145/2676726.2676975.                                      008-9099-0.
[24] H. Tews, T. Weber, and M. Völp, “A Formal Model of Memory               [39] T. Duff, “Message to the Comp.lang.c Usenet Group,”
     Peculiarities for the Verification of Low-Level Operating-System             http://www.lysator.liu.se/c/duffs-device.html. 1988.
     Code,” Electron. Notes Theor. Comput. Sci., vol. 217, pp. 79–96, Jul.   [40] P. Wadler, “Monads for Functional Programming,” Proc. Advanced
     2008, doi:10.1016/j.entcs.2008.06.043.                                       Functional Programming, First International Spring School on
[25] A. Igarashi, B. Pierce, and P. Wadler, “Featherweight Java: A                Advanced Functional Programming Techniques-Tutorial Text, pp.
     Minimal Core Calculus for Java and GJ,” Proc. 14th ACM SIGPLAN               24–52, May 1995.
     Conference on Object-Oriented Programming, Systems, Languages,          [41] A. Biere, A. Cimatti, E. Clarke, and Y. Zhu, “Symbolic model
     and Applications (OOPSLA'99), pp. 132–146, Nov. 1999,                        checking without BDDs,” Tools and Algorithms for the Construction
     doi:10.1145/320384.320395.                                                   and Analysis of Systems, W.R. Cleaveland, eds., TACAS 1999.
[26] D. Syme, “Proving Java Type Soundness,” Formal Syntax and                    Lecture Notes in Computer Science, Berlin: Springer, pp. 193–207,
     Semantics of Java, J. Alves-Foss, eds., Lecture Notes in Computer            1999, doi:10.1007/3-540-49059-0_14.
     Science, Berlin: Springer, pp. 83–118, 1999, doi:10.1007/3-540-         [42] C. Barrett, and C. Tinelli, “Satisfiability Modulo Theories,”
     48737-9_3.                                                                   Handbook of Model Checking, E. Clarke, T. Henzinger, H. Veith, R.
[27] S. Maffeis, J.C. Mitchell, and A. Taly, “An Operational Semantics for        Bloem, eds., Cham: Springer, pp. 305–343, 2018, doi:10.1007/978-3-
     JavaScript,” Programming Languages and Systems, G. Ramalingam                319-10575-8_11.
     eds., APLAS 2008. Lecture Notes in Computer Science, Berlin: A          [43] H. Barendregt, and E. Barendsen, “Autarkic Computations in Formal
     Springer, pp. 307–325, 2008, doi:10.1007/978-3-540-89330-1_22.               Proofs,” J. Autom. Reason., vol. 28, pp. 321–336, Apr. 2002,
[28] C. Cadar, D. Dunbar, and D. Engler, “KLEE: Unassisted and                    doi:10.1023/A:1015761529444.
     Automatic Generation of High-Coverage Tests for Complex Systems




                                                                                                                                                     27
                                                                              Z. Yang, et al: Preparation of Papers for IEEE Access (December 2019)



[44] J. Harrison, “HOL Light: An Overview,” Theorem Proving in Higher
     Order Logics, S. Berghofer, T. Nipkow, C. Urban, W. Wenzel, eds.,
     TPHOLs 2009. Lecture Notes in Computer Science, Berlin: Springer,
     pp. 60–66, doi:10.1007/978-3-642-03359-9_4.
[45] X. Yang, Z. Yang, and H. Y. Sun, “Formal Verification for Ethereum
     Smart Contract Using Coq,” Int. J. Perform. Eng., vol. 14, no. 8, Aug.
     2018, doi:10.23940/ijpe.18.08.p9.17261734.
[46] G.D. Plotkin, “ Call-by-Name, Call-by-Value and the λ -
     Calculus,” Theor. Comput. Sci., vol. 1, no. 2, pp. 125–159, Dec.
     1957, doi:10.1016/0304-3975(75)90017-1.
[47] G. Klein, K. Elphinstone, G. Heiser, J. Andronick, D. Cock, P. Derrin,
     D. Elkaduwe, K. Engelhardt, R. Kolanski, M. Norrish, T. Sewell, H.
     Tuch, and S. Winwood, “seL4: Formal Verification of an OS Kernel,”
     Proc. ACM SIGOPS 22nd Symposium on Operating Systems
     Principles     (SOSP'09),      pp.       207–220,     Oct.     2009,
     doi:0.1145/1629575.1629596.




                                                                                                                                                 28
                Zheng Yang is a Ph.D. student in
                School of Information and Software
                Engineering, University of Electronic
                Science and Technology of China. He
                received his Bachelor Degree, and
                became a Ph.D. candidate at School of
                Information and Software Engineering,
                University of Electronic Science and
Technology of China in 2017. His research interests
include programming language theory, formal methods
and program verification.

                Hang Lei received his Ph.D. degree in
                computer science from the University
                of Electronic Science and Technology of
                China, China, in 1997. After graduation,
                he conducted research in the fields of
                real-time embedded operating system,
                operating system security, and program
                verification, as a professor with the
                Department of Computer Science,
University of Electronic Science and Technology of
China. He is currently a professor (doctoral supervisor)
in School of Information and Software Engineering,
University of Electronic Science and Technology of
China. His research interests include big data analytics,
machine learning and program verification.

                  Weizhong Qian received his Ph.D.
                  degree in computer science from the
                  University of Electronic Science and
                  Technology of China, China, in 2001.
                  After graduation, he conducted
                  research in the fields of machine
                  learning, software security, and
                  program verification, as an associate
                  professor with the Department of
Computer Science, University of Electronic Science and
Technology of China. He is currently an assistant
professor in School of Information and Software
Engineering, University of Electronic Science and
Technology of China. His research interests include big
data analytics, machine learning and software security.




                                                            29
