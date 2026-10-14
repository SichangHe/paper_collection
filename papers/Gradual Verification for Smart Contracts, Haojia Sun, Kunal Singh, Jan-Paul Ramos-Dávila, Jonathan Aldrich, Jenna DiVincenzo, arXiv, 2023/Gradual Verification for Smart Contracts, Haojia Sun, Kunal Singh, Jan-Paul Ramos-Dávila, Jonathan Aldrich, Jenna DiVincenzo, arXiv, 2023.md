                                                          Gradual Verification for Smart Contracts
                                                          Haojia Sun                                  Kunal Singh                          Jan-Paul Ramos-Dávila
                                               Shanghai Jiao Tong University                    Carnegie Mellon University                      Cornell University

                                                                              Jonathan Aldrich                          Jenna DiVincenzo
                                                                         Carnegie Mellon University                       Purdue University

                                        Abstract                                                                  they can only uncover vulnerabilities in executed program
                                        Blockchains facilitate secure resource transactions through               paths at run time. Moreover, run-time checks incur substan-
                                        smart contracts, yet these digital agreements are prone to                tial transaction fees on blockchains, increasing the monetary
                                        vulnerabilities, particularly when interacting with external              cost of executing smart contracts.
                                        contracts, leading to substantial monetary losses. Traditional               Given these constraints, gradual verification [1, 14] emerges
arXiv:2311.13351v2 [cs.CR] 3 Jul 2024




                                        verification techniques fall short in providing comprehen-                as a compelling solution for securing smart contracts. Grad-
                                        sive security assurances, especially against re-entrancy at-              ual verification supports partial specifications and incremen-
                                        tacks, due to the unavailable implementations of external                 tal verification of code by applying static verification where
                                        contracts. This paper introduces an incremental approach:                 possible and dynamic verification where necessary. This
                                        gradual verification. We combine static and dynamic verifi-               gives developers control over the trade-offs between static
                                        cation techniques to enhance security, guarantee soundness                and dynamic verification. They can write more static specifi-
                                        and flexibility, and optimize resource usage in smart contract            cations and get stronger guarantees and less run time over-
                                        interactions. By implementing a prototype for gradually veri-             head; or, they can write fewer specifications—saving on hu-
                                        fying Algorand smart contracts via the pyTEAL language, we                man effort —and rely more on run-time checking and its cost.
                                        demonstrate the effectiveness of our approach, contributing               The spectrum of trade-offs is formally guaranteed [1, 14]. We
                                        to the safe and efficient execution of smart contracts.                   present a prototype for gradually verifying smart contracts
                                                                                                                  via TEAL, the programming language used for creating Al-
                                        Keywords Logic, Gradual Verification, Smart Contracts                     gorand smart contracts. By extending a gradual verification
                                                                                                                  architecture from prior work [3, 14], we can provide the
                                        1    Introduction                                                         following benefits to smart contracts and their developers:
                                        Smart contracts, self-executing programs on blockchains like              Protecting Against Unverified Code & Re-entrancy. Tra-
                                        Algorand and Ethereum, facilitate secure resource transac-                ditional static verification techniques are unsound in the
                                        tions among mutually untrusted parties [4, 13]. Despite their             face of unverified code and arbitrary re-entrancy. In contrast,
                                        potential, bugs in smart contracts come with serious conse-               gradual verification soundly guards against undefined behav-
                                        quences, such as substantial monetary loss [10]. Therefore,               ior in unverified code and from arbitrary re-entrancy by run-
                                        it is important to ensure the correctness of smart contracts.             time checking pre- and postconditions—that may be partially
                                            Verification is particularly challenging when one smart               specified—on current and external contracts. Furthermore,
                                        contract calls another, which is external. The external con-              for critical sections of available code, static verification can
                                        tract may not be verified and may break the assumptions its               be employed proactively to identify potential issues.
                                        caller makes, particularly in the case of re-entrant calls like
                                        those at the root of the DAO attack on Ethereum [9].                      Balancing Precision and Flexibility. The incremental ap-
                                            Recent verification approaches have been introduced to                proach to verification supported by gradual verification is
                                        tackle this problem. Bräm et al. [2], Hajdu and Jovanović                 well-suited for the fast-paced and ever-changing blockchain
                                        [5], Hildenbrandt et al. [6], and Kalra et al. [7] introduce static       environment. It also makes verification more accessible to
                                        verification techniques capable of verifying the functional               novice developers of smart contracts. Gradual verification
                                        properties of Ethereum smart contracts, even when they in-                suppresses static verification errors from missing specifi-
                                        volve calls to external contracts. These approaches provide               cations allowing developers to specify only the software
                                        strong guarantees, but they burden developers by demanding                components and properties they care about! Only true static
                                        exhaustive and meticulous specifications. Rodler et al. [11],             and dynamic errors are reported, allowing bugs and vul-
                                        Shyamasundar [12], and Li et al. [8] introduce approaches                 nerabilities in smart contracts and their specifications to be
                                        that dynamically monitor and enforce user-specified invari-               detected earlier than static or dynamic verification alone [3].
                                        ants in smart contracts that call external contracts. While
                                        these dynamic techniques offer flexibility and ease of use,               Reducing Run-time Overhead. The transaction fees and
                                                                                                                  computational resources required for executing smart con-
                                        PriSC’24, January 17–19, 2024, London, United Kingdom                     tracts can accumulate quickly, like the Ethereum gas fee,
                                        2024.                                                                     which increases with dynamic verification alone. Gradual
                                                                                                              1
PriSC’24, January 17–19, 2024, London, United Kingdom                                                                             Sun, Singh, Ramos-Dávila, Aldrich and DiVincenzo

verification minimizes this cost by minimizing run-time                                                              Dynamic Verification. We then identify the locations where
checks with statically available information—when a proof                                                            run-time checks should be inserted, based on the placement
obligation has been statically verified, no run-time check is                                                        of ? embedded in our pyTEAL specifications. We developed
generated for it. Therefore, developers may choose to spend                                                          the Weaver module to perform this step and encode the
more time incrementally specifying their software to reduce                                                          checks in the original pyTEAL program at the identified lo-
dynamic checking overhead.                                                                                           cations. Finally, the pyTEAL program with run-time checks
                                                                                                                     is transformed into an executable contract with the pyTEAL
2      Architecture: Gradual pyTEAL                                                                                  compiler, which is subsequently executed on the Algorand
We present a pipeline (see Fig. 1) implementing the gradual                                                          platform. In the event of run-time check failures, correspond-
verification of pyTEAL smart contracts, part of the Algorand                                                         ing error messages are reported. In practice, run-time checks
platform. pyTEAL contracts are written in a domain-specific                                                          may contain simple logical expressions, accessibility pred-
subset of Python, to which we added pre- and post-condition                                                          icates denoting ownership of contract state, and complex
assertions. Our approach converts pyTEAL programs to                                                                 predicates implemented as recursive boolean functions.
Gradual C0, the only previously implemented gradual ver-
ifier [3]. Internally, Gradual C0 uses a variant of the Viper                                                        2.1     Example
toolchain [2] to statically verify functions, treating partial                                                       1 #@ global Count;
specifications optimistically. The modified Viper back-end                                                           2 @router.method
generates run-time checks wherever static verification could                                                         3 def sell(quantity: abi.Uint64):
not assure specifications; these run-time checks are added                                                           4    #@ requires ? and quantity>=0 and acc(Count);
to the original smart contract before compilation to the Al-                                                         5    #@ ensures Count >=0;
gorand platform.                                                                                                     6    scratchCount = ScratchVar(TealType.uint64)
    Frontend                           Type Inference
                                                                                                                     7    return Seq(
        pyTEAL                Unresolved            Unresolved        Resolved                                        8            scratchCount.store(App.globalGet(
                                                    pyTEAL AST                                  C0 IR
        parser                pyTEAL AST                               C0 AST
                                                    with types                                                        9                Bytes("Count"))),
                                                                                                                     10            App.globalPut(Bytes("Count"), scratchCount.
                                                                        Gradual
                               Unresolved                               Viper IR
                                                                                                                                       load() - quantity.get())
        Gradual                                    Type checker/                             Optimistic static
      Viper parser
                              Gradual Viper
                                                   Resolved AST                             success or failure       11       )
                                  AST                                   Optimistic
     Gradual Viper Translation                                        Static Verifier


              Collection of              Map C0              Add runtime
                                                                                                                          Figure 2. A gradually verified Algorand smart contract
                runtime                 optimistic             checks to             TEAL compiler
               assertions             checks with ?          pyTEAL holes                                               In Figure 2, a segment of an Algorand smart contract de-
     Back to TEAL Translation                                               Weaver                                   picts a selling transaction, where a specified quantity is sub-
                                                                             Gradual Verification                    tracted from a global state variable Count. In Algorand smart
                                                                                                                     contracts, global state refers to storage that persists across
         Figure 1. Gradual pyTEAL verification pipeline                                                              different contract calls and is accessible to all instances of the
Front-end. We construct a parser using the FastParse Scala                                                           contract. The //@requires annotation in the code ensures
library to parse pyTEAL source code with specifications                                                              that quantity is non-negative and verifies access to the Count
into an unresolved pyTEAL Abstract Syntax Tree (AST).                                                                variable. A ? indicates that this specification is partial. By
Since Python supports dynamic typing but we are trans-                                                               specifying access permissions, the contract ensures that func-
lating to a typed intermediate language (C0), we use type                                                            tions interact with the global state as intended, safeguarding
inference to assign static types to all variables in the pyTEAL                                                      against unauthorized modifications and security threats, thus
AST, resulting in an unresolved pyTEAL AST with inferred                                                             maintaining the integrity of the state management.
types. We perform type checking and other well-formedness                                                               Statically, the //@ensures annotation specifies a postcon-
checks, then translate this "resolved AST" to C0. The C0 AST                                                         dition, asserting that Count remains non-negative after the
makes some operations more explicit, aiding verification and                                                         transaction. This postcondition cannot be proven statically
connecting to the intermediate representation supported by                                                           because an additional precondition, quantity <= Count, would
Gradual C0.                                                                                                          be required. However, the verifier optimistically assumes this
                                                                                                                     property can be derived from the ?, and a run-time check
Static Verification. During static verification, the verifier                                                        is added to make sure the property is obeyed at run time.
optimistically interprets imprecise formulas to satisfy a con-                                                       By requiring the developer to explicitly specify data types,
tract (denoted by ?), with a promise that these holes in the                                                         access controls, and preconditions/postconditions, the grad-
specification will be dealt with at run time. When optimistic                                                        ual verification architecture ensures that these specifications
static verification succeeds, a set of run-time checks are pro-                                                      can be optimistically statically checked before the run time,
duced that must be executed at run time for soundness.                                                               while ensuring run-time soundness.
                                                                                                                 2
Gradual Verification for Smart Contracts                                                PriSC’24, January 17–19, 2024, London, United Kingdom

3    Acknowledgements                                                                 [14] Jenna Wise, Johannes Bader, Cameron Wong, Jonathan Aldrich, Éric
                                                                                           Tanter, and Joshua Sunshine. 2020. Gradual verification of recursive
The authors thank the PriSC reviewers for their helpful com-                               heap data structures. Proceedings of the ACM on Programming Lan-
ments. This research was supported by the National Science                                 guages 4, OOPSLA (2020), 1–28.
Foundation under Grant No. CCF-1901033 (https://www.nsf.
gov/awardsearch/showAward?AWD_ID=1901033) and by a
Google PhD Fellowship. Any opinions, findings, and con-
clusions or recommendations expressed in this material are
those of the authors and do not necessarily reflect the views
of the National Science Foundation or Google.

References
 [1] Johannes Bader, Jonathan Aldrich, and Éric Tanter. 2018. Gradual
     program verification. In Verification, Model Checking, and Abstract
     Interpretation: 19th International Conference, VMCAI 2018, Los Angeles,
     CA, USA, January 7-9, 2018, Proceedings 19. Springer, 25–46.
 [2] Christian Bräm, Marco Eilers, Peter Müller, Robin Sierra, and Alexan-
     der J Summers. 2021. Rich specifications for Ethereum smart contract
     verification. Proceedings of the ACM on Programming Languages 5,
     OOPSLA (2021), 1–30.
 [3] Jenna DiVincenzo, Ian McCormack, Hemant Gouni, Jacob Gorenburg,
     Mona Zhang, Conrad Zimmerman, Joshua Sunshine, Éric Tanter, and
     Jonathan Aldrich. 2022. Gradual C0: Symbolic Execution for Efficient
     Gradual Verification. arXiv preprint arXiv:2210.02428 (2022).
 [4] Ilya Grishchenko, Matteo Maffei, and Clara Schneidewind. 2018. A
     semantic framework for the security analysis of ethereum smart con-
     tracts. In Principles of Security and Trust: 7th International Conference,
     POST 2018, Held as Part of the European Joint Conferences on Theory
     and Practice of Software, ETAPS 2018, Thessaloniki, Greece, April 14-20,
     2018, Proceedings 7. Springer, 243–269.
 [5] Ákos Hajdu and Dejan Jovanović. 2020. solc-verify: A modular verifier
     for solidity smart contracts. In Verified Software. Theories, Tools, and
     Experiments: 11th International Conference, VSTTE 2019, New York City,
     NY, USA, July 13–14, 2019, Revised Selected Papers 11. Springer, 161–
     179.
 [6] Everett Hildenbrandt, Manasvi Saxena, Nishant Rodrigues, Xiaoran
     Zhu, Philip Daian, Dwight Guth, Brandon Moore, Daejun Park, Yi
     Zhang, Andrei Stefanescu, et al. 2018. Kevm: A complete formal
     semantics of the ethereum virtual machine. In 2018 IEEE 31st Computer
     Security Foundations Symposium (CSF). IEEE, 204–217.
 [7] Sukrit Kalra, Seep Goel, Mohan Dhawan, and Subodh Sharma. 2018.
     Zeus: analyzing safety of smart contracts.. In Ndss. 1–12.
 [8] Ao Li, Jemin Andrew Choi, and Fan Long. 2020. Securing smart con-
     tract with runtime validation. In Proceedings of the 41st ACM SIGPLAN
     Conference on Programming Language Design and Implementation. 438–
     453.
 [9] Muhammad Izhar Mehar, Charles Louis Shier, Alana Giambattista,
     Elgar Gong, Gabrielle Fletcher, Ryan Sanayhie, Henry M Kim, and
     Marek Laskowski. 2019. Understanding a revolutionary and flawed
     grand experiment in blockchain: the DAO attack. Journal of Cases on
     Information Technology (JCIT) 21, 1 (2019), 19–32.
[10] Malaw Ndiaye and Pr Karim Konate. 2021. Cryptocurrency crime:
     Behaviors of malicious smart contracts in blockchain. In 2021 Inter-
     national Symposium on Networks, Computers and Communications
     (ISNCC). IEEE, 1–8.
[11] Michael Rodler, Wenting Li, Ghassan O Karame, and Lucas Davi. 2018.
     Sereum: Protecting existing smart contracts against re-entrancy at-
     tacks. arXiv preprint arXiv:1812.05934 (2018).
[12] RK Shyamasundar. 2022. A Framework of Runtime Monitoring for
     Correct Execution of Smart Contracts. In International Conference on
     Blockchain. Springer, 92–116.
[13] Nick Szabo. 1997. Formalizing and securing relationships on public
     networks. First monday (1997).
                                                                                  3
