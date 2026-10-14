                                             ESBMC-Solidity: An SMT-Based Model Checker for
                                                        Solidity Smart Contracts
                                                        Kunjian Song                                     Eddie B. de Lima Filho                        Lucas C. Cordeiro
                                                      Nedas Matulevicius                                TPV Vision Innovator, Brazil              University of Manchester, UK
                                                University of Manchester, UK                            eddie_batista@yahoo.com.br              lucas.cordeiro@manchester.ac.uk
                                             kunjian.song@postgrad.manchester.ac.uk
                                             nedas.matulevicius@postgrad.manchester.ac.uk

                                         Abstract                                                                          as a state machine whose global state is updated by those
                                                                                                                           transactions, which indeed constitute state transitions.
arXiv:2111.13117v1 [cs.LO] 25 Nov 2021




                                         Smart contracts written in Solidity are programs used in
                                         blockchain networks, such as Etherium, for performing trans-                         The transactions are performed by smart contracts, which
                                         actions. However, as with any piece of software, they are                         are programs automatically executed on blockchain net-
                                         prone to errors and may present vulnerabilities, which mali-                      works when specific conditions are met [1], which encode
                                         cious attackers could then use. This paper proposes a solidity                    business logic. For instance, such conditions can be an ex-
                                         frontend for the efficient SMT-based context-bounded model                        change of cryptocurrency or even a process of content un-
                                         checker (ESBMC), named ESBMC-Solidity, which provides a                           locking if a digital rights management system is involved.
                                         way of verifying such contracts with its framework. A bench-                      Indeed, transactions act as stimuli to smart contracts. Never-
                                         mark suite with vulnerable smart contracts was also devel-                        theless, such contracts must first be written in a given lan-
                                         oped for evaluation and comparison with other verification                        guage. In the case of Etherium, smart contracts are written in
                                         tools. The experiments performed here showed that ESBMC-                          Solidity, which is an object-oriented language for programs
                                         Solidity detected all vulnerabilities, was the fastest tool, and                  to be run on the Ethereum virtual machine (EVM) [2].
                                         provided a counterexample for each benchmark. A demon-                               Once deployed, there is no way to update a smart con-
                                         stration is available at https://youtu.be/3UH8_1QAVN0.                            tract except for deleting it entirely and re-deploying a new
                                                                                                                           one. Even a smart contract’s author cannot modify the corre-
                                         CCS Concepts: • Software and its engineering → Model                              sponding source code or fix bugs after that [4]. Due to such
                                         checking; Software verification.                                                  immutability, it is critical to ensure that a smart contract is
                                         Keywords: formal verification, Solidity.                                          secure before its deployment on a blockchain network, such
                                                                                                                           as Ethereum. However, as usually happens to software, smart
                                         ACM Reference Format:                                                             contracts suffer from vulnerabilities, which represent a risk
                                         Kunjian Song, Nedas Matulevicius, Eddie B. de Lima Filho, and Lu-                 as malicious attackers often exploit them. As an example,
                                         cas C. Cordeiro. 2021. ESBMC-Solidity: An SMT-Based Model Checker
                                                                                                                           the DAO attack, in 2016, resulted in a monetary loss of more
                                         for Solidity Smart Contracts. In Proceedings of ACM Conference (Con-
                                         ference’22). ACM, New York, NY, USA, 4 pages. https://doi.org/10.
                                                                                                                           than $50 million dollars, which forced Ethereum to be hard
                                         1145/nnnnnnn.nnnnnnn                                                              forked and then rolled back to a previous state [5].
                                                                                                                              If there can be vulnerabilities, software testing becomes
                                         1     Introduction                                                                paramount, and the community has already begun to tackle
                                                                                                                           the related problems [6, 7]. However, most approaches tar-
                                         The blockchain system is a distributed ledger technology that                     get only a limited number of errors, which worsens as new
                                         forms the primary mechanism behind Bitcoin, Ethereum, and                         applications appear and the need for specific aspects arises.
                                         alternative cryptocurrencies [1]. It can be considered as a                       Consequently, it is essential to employ mature and flexible
                                         singly linked list of blocks [2], where each of them contains                     verifiers, e.g., based on model checking and satisfiability
                                         a set of unmodifiable transactions. This way, such a technol-                     modulo theories (SMT), to check smart contracts. This way,
                                         ogy serves as a distributed tamper-resistant record of such                       a myriad of problems is already handled, and consequent
                                         transactions [3]. Ethereum, for instance, can be regarded                         methodology advancements can then be devised faster, in-
                                         Permission to make digital or hard copies of all or part of this work for         cluding behavior models and specific properties [8].
                                         personal or classroom use is granted without fee provided that copies are not        In that sense, the efficient SMT-based context-bounded
                                         made or distributed for profit or commercial advantage and that copies bear       model checker (ESBMC) is a good candidate. It is a state-of-
                                         this notice and the full citation on the first page. Copyrights for components    the-art (SOTA) checker, which can be extended to support
                                         of this work owned by others than ACM must be honored. Abstracting with           different programming languages and target systems, such
                                         credit is permitted. To copy otherwise, or republish, to post on servers or to
                                         redistribute to lists, requires prior specific permission and/or a fee. Request   as digital filters and controllers, even incorporating behav-
                                         permissions from permissions@acm.org.                                             ior models and companion tools [8–10]. In addition, it was
                                         Conference’22, May 2022, Pittsburgh, PA, USA                                      initially devised as a C-language model checker and has
                                         © 2021 Association for Computing Machinery.                                       been evaluated using standard benchmarks and embedded
                                         ACM ISBN 978-x-xxxx-xxxx-x/YY/MM. . . $15.00                                      applications in the telecommunication industry [11, 12].
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn
Conference’22, May 2022, Pittsburgh, PA, USA                                                                                      Song et al.




             Figure 1. Architectural overview of ESBMC with its extension for verifying Solidity smart contracts.

   This paper tackles the problem raised here, i.e., smart-         detects it, a counterexample is provided, in the form of state
contract evaluation, and proposes a frontend for ESBMC              traces, to allow its reproduction. It is worth noticing that
based on the newly developed Grammar-based Hybrid Con-              ESBMC supports several SMT solvers, including Z3, Bitwuzla,
version methodology. It enables ESBMC to verify Solidity            Boolector, MathSAT, CVC4, and Yices [17].
contracts via two steps. First, we convert Solidity JavaScript
object notation (JSON) abstract syntax trees (AST) into the         2.2    The Grammar-Based Hybrid Conversion
ESBMC’s intermediate representation (IR). Second, we inte-                 Methodology
grate with ESBMC’s infrastructure to reuse its existing SMT-        Given an input smart contract, the goal of the proposed fron-
based verification strategies (incremental and k-induction).        tend is to populate the resulting symbol table, where each
   In order to evaluate the proposed framework, named ESBMC-        symbol is represented by the ESBMC’s symbolt data struc-
Solidity, a benchmark suite with vulnerable smart contracts         ture [17]. Furthermore, it shall complete the type-checking
was created and used as input for it and other SOTA Solidity        procedure of Solidity AST nodes and transform each JSON
verification tools: Smartcheck [13], Slither [14], Oyente [15],     AST node into its equivalent ESBMC’s irept one while pre-
and Mythril [16]. As a result, ESBMC-Solidity outperformed          serving the associated semantic information. To achieve this
the mentioned verification tools in soundness and perfor-           goal, we developed this frontend based on the Grammar-
mance. Besides, it identified all vulnerabilities, with a coun-     Based Hybrid Conversion methodology, as an approach specif-
terexample for each, and proved the fastest approach.               ically devised for that during the development of this work.
                                                                       Grammar-Based Conversion. The proposed frontend
2    Tool description                                               uses the library nlohmann/json1 to process Solidity ASTs in
                                                                    JSON format. When traversing Solidity AST nodes, it uses
2.1 Tool Overview
                                                                    different functions to transform them into equivalent 𝑖𝑟𝑒𝑝_𝑡
Fig. 1 illustrates the architecture of ESBMC-Solidity, where        ones, e.g., get_var_decl_stmt, get_expr, and get_statement,
the gray box with solid border represents the new frontend,         for variable-declaration-statement, expression, and statement
and the white ones constitute the existing ESBMC’s com-             nodes, respectively. Besides, each AST node may contain mul-
ponents. The gray box with a dashed border indicates an             tiple child ones, e.g., the AST node of a for loop contains four
external element for preprocessing smart contracts: the Solid-      child nodes: initialisation, condition, increment, and loop body.
ity compiler. It is used for lexical analysis and parsing, taking   So, during their conversion, the production rules in Solidity
a smart contract as input and then transforming it into JSON        grammar documentation2 are followed, so that they are vis-
AST, which is done with the argument --ast-compact-json.            ited in correct order. For instance, the variable-initialisation
   The proposed approach takes JSON AST and converts each           node of a for loop must be visited before the body one, as it
of its nodes into an equivalent IR one, using the ESBMC’s           may be referenced by the latter. If the node for a body loop is
irept, a tree-structured IR that preserves a program’s seman-       converted before its variable initialisation, the type checker
tics.Next, each irept node is converted into the corresponding      will fail to handle any reference to it.
symbol and then added to a table, which is translated into             Hybrid conversion. Three functions must be supported:
a GOTO program. Then, the latter is processed by the sym-           (1) 𝑎𝑠𝑠𝑒𝑟𝑡 () for defining safety properties; (2) 𝑎𝑠𝑠𝑢𝑚𝑒 () for
bolic execution engine (SymEx) to generate its static single        defining constraints; and (3) 𝑛𝑜𝑛𝑑𝑒𝑡 () for assigning non-
assignment (SSA) form, which is used to generate verification       deterministic values to variables. Consequently, they are
condition (VCs) 𝐶 ∧ ¬𝑃, where 𝐶 represents constraints and          implemented by ESBMC as C-style declarations. However,
𝑃 denotes a safety property. Lastly, ESBMC uses off-the-shelf       the new frontend works with JSON AST nodes. Besides, since
SMT solvers for verifying the satisfiability of those VCs.
   If a property is satisfiable, an execution path leads to a bug   1 JSON for Modern C++ - https://github.com/nlohmann/json

in an original Solidity smart contract. Then, when ESBMC            2 Solidity Grammar - https://docs.soliditylang.org/en/v0.8.6/grammar.html
 ESBMC-Solidity: An SMT-Based Model Checker for Solidity Smart Contracts                               Conference’22, May 2022, Pittsburgh, PA, USA


 there are more than 70 intrinsic declarations, e.g., forward              showing the set of assignments and the breaking values that
 declarations for nondeterministic types, we instantiate the               trigger such violation, where 𝑦 is set with a value 240.
 existing ESBMC’s clang frontend to convert those into irept                      𝑦 = 𝑛𝑜𝑛𝑑𝑒𝑡 ()   
 nodes to avoid replication, hence generating the symbol table
                                                                                  ∧ 𝑠𝑢𝑚 = 𝑦
                                                                                                                                                 
 mentioned before. Finally, the latter is further merged with                  𝐶=                                    (1) 𝑃 =       𝑡𝑒𝑚𝑝 ! = 0
                                                                                                   
                                                                                                                                                        (2)
                                                                                  ∧ 𝑦 ! = 224
                                                                                                   
 the symbol table generated from the original Solidity AST.
                                                                                                   
                                                                                  ∧ 𝑡𝑒𝑚𝑝 = 𝑠𝑢𝑚%16 
                                                                                                  
 2.3   Illustrative Example
                                                                           3    Evaluation and Benchmarks
 1 pragma solidity >=0.4.26;                                               ESBMC-Solidity, though an early prototype, can detect vul-
 2 contract MyContract {
 3   uint8 x;
                                                                           nerabilities listed in the smart-contract weakness classifica-
 4   uint8 sum ;                                                           tion (SWC) registry [19]. So, our evaluation aims to answer
 5   function nondet () public pure                                        three questions. EQ1: is our approach able to report a con-
 6     returns ( uint8 ) {
 7     uint8 i;                                                            firmed bug? (soundness). EQ2: does our approach find a
 8     return i;                                                           bug in a reasonable amount of time? (performance). EQ3:
 9   }
10   function __ESBMC_assume ( bool )                                      is our approach able to provide a counterexample to help
11     internal pure { }                                                   reproduce a specific bug? (bug reproduction).
12   function func_sat () external {
13     x = 0;
14     uint8 y = nondet () ;                                               3.1 Benchmark Suite Design
15     sum = x + y;                                                        A benchmark suite that contains bugs in smart contracts was
16     __ESBMC_assume ( y < 255) ;
17     __ESBMC_assume ( y > 220) ;                                         developed to evaluate ESBMC-Solidity and compare it with
18     __ESBMC_assume ( y != 224) ;                                        other SOTA verification tools. The design of each test case
19     assert ( sum % 16 != 0) ;
20   }                                                                     (TC) was guided by the SWC registry [19], as shown in Ta-
21 }                                                                       ble 2, while Table 1 shows that all bugs in TCs were detected
                                                                           and confirmed by at least one of the non-ESBMC tools. The
  Figure 2. An example smart contract written in Solidity.                 test suite and logs are publicly available in Zenodo3 .

   Fig. 2 shows an example of smart-contract verification                  3.2 Results
with ESBMC-Solidity. Indeed, developers can instrument                     Table 1 shows results for ESBMC-Solidity and other tools.
code, e.g., nondet for nondeterministic integers between 0                 The former found bugs in all TCs confirmed by Mythril,
and 255 and __ESBMC_assume for additional constraints.                     which affirms EQ1. SmartCheck and Slither were able to
Those help developers narrow down the scope for triggering                 confirm TC5, which contains a vulnerability reported in the
a bug, hence identifying a set of breaking inputs. Function                security considerations4 , while detected none for the other
func_sat is the one we need to verify, where two state vari-               TCs. Oyente did not find any bug. Mythril, a tool used in the
ables x and sum are defined in lines 3 and 4, respectively,                service MythXTM [16], also reported bugs in all TCs.
while a safety property indicates that x + y should not be                    Apart from TC5, Mythril and the other non-ESBMC tools
a multiple of 16. In addition, constraints are added using                 failed to provide a counterexample for each TC. However,
__ESBMC_assume, in lines 16, 17, and 18, which restrict 𝑦 as               ESBMC-Solidity did, which affirms EQ3. For TC5, a coun-
any integer between 220 and 255, but 224. Then, ESBMC will                 terexample is not needed, as a tool should only inform that
check whether there exists an execution path that satisfies                authorization via 𝑡𝑥 .𝑜𝑟𝑖𝑔𝑖𝑛 must be avoided. One possible
its negation. This way, the verification of func_sat becomes a             reason for the missing counterexamples could be loss of the
satisfiability problem: given the binary operation expression              original Solidity syntax, as tools either use EVM bytecode,
“sum = x + y”, where x is 0 and y is a constrained nondeter-               e.g., Oyente and Mythril or rely on various forms of IR that
ministic value, find an execution state where the negation                 do not preserve the original Solidity declaration references
of “𝑠𝑢𝑚%16! = 0” is satisfied. ESBMC is then invoked with                  needed for state tracing, e.g., SmartCheck and Slither.
esbmc <JSON AST> --function func_sat --z3.                                    ESBMC-Solidity is the fastest tool, as can be seen in the
                                                                           last line of Table 1, which thus affirms EQ2. Oyente and
   For the smart contract in Fig. 2, ESBMC generates the 𝐶
                                                                           Mythril work on EVM bytecode and employ simulation for
and 𝑃 equations as described in (1) for constraints and (2) for
                                                                           execution path-exploration [20], which might be the rea-
property. Eq. (1) shows a conjunction of the constraints and
                                                                           son why they are slower than ESBMC-Solidity. Apart from
assignments. When generating its SSA form, ESBMC uses
                                                                           bug detection, Slither also provides code optimization [14],
the temporary variable temp to represent the left-hand-side
                                                                           which might add to the total verification time. To the best of
of the safety property specified in line 19, which corresponds
                                                                           our knowledge, there is no option in Slither to disable the
to the assignment 𝑡𝑒𝑚𝑝 = 𝑠𝑢𝑚%16 in Eq. 1. The resulting VC
                                                                           optimization. SmartCheck is implemented in Java, converts
for satisfiability verification, via SMT solver, is then formed
by 𝐶∧¬𝑃. Consequently, ESBMC reports a property violation                  3 https://doi.org/10.5281/zenodo.5721726

and provides a counterexample that contains a trace of states              4 https://docs.soliditylang.org/en/v0.8.6/security-considerations.html
Conference’22, May 2022, Pittsburgh, PA, USA                                                                                        Song et al.


                                  SmartCheck      Slither      Oyente         Mythril       ESBMC-Solidity
                       TC
                                  Found CE     Found CE     Found CE Found CE Found                    CE
                  TC1              No     -     No        -   No       -     Yes     No      Yes       Yes
                  TC2              No     -     No        -   No       -     Yes     No      Yes       Yes
                  TC3              No     -     No        -   No       -     Yes     No      Yes       Yes
                  TC4              No     -     No        -   No       -     Yes     No      Yes       Yes
                                                           Failed to
                  TC5          Yes    N/A     Yes    N/A compile       -     Yes    N/A      Yes      N/A
                  TC6          No       -     No       -      No       -     Yes     No      Yes       Yes
                  TC7          No       -     No       -      No       -     Yes     No      Yes       Yes
                  TC8          No       -     No       -      No       -     Yes     No      Yes       Yes
               Total Time        1.160s         0.519s         1.116s          3.106s            0.183s
Table 1. Experimental results, where column “Found” indicates whether a bug was detected, followed by column “CE” showing
whether a counterexample was provided. The line “Total Time” represents the CPU time [18] used for verification.



    SWC Bug ID               Vulnerability             TC         prototype, it shows promising results. Our current focus is
                           Integer Overflow           TC1,2       on providing 100% coverage for the language Solidity, in-
     SWC-101                                                      cluding polymorphism, inheritance, special crypto functions,
                          Integer Underflow           TC3,4
     SWC-115        Authorization through tx.origin    TC5        such as Keccak256 and sha256, and multiple returns.
                      Static array out-of-bounds       TC6
     SWC-110
                     Dynamic array out-of-bounds      TC7,8
                                                                  References
                                                                   [1] I Bashir. 2017. Mastering Blockchain. Packt Publishing Ltd.
    Table 2. Test case design based on SWC registry [19].          [2] K Soloro et al. 2019. Hands-On Smart Contract Development With
                                                                       Solidity and Ethereum. California, USA: O’Reilly.
                                                                   [3] D Yaga et al. 2019. Blockchain technology overview. CoRR
                                                                       arXiv:1906.11078 (2019).
Solidity code into an XML-based IR, and uses XPath to query        [4] A Antonopoulos et al. 2018. Mastering ethereum. O’reilly Media.
                                                                   [5] M Mehar et al. 2019. Understanding a revolutionary and flawed grand
it, while ESBMC-Solidity is implemented purely in C++.
                                                                       experiment in blockchain: the DAO attack. JCIT 21, 1 (2019), 19–32.
                                                                   [6] Á Hajdu et al. 2019. solc-verify: A modular verifier for Solidity smart
4     Related Work                                                     contracts. CoRR arXiv:1907.04262 (2019).
Among the tools we evaluated, Mythril and Oyente use SMT-          [7] I Garfatta et al. 2021. A Survey on Formal Verification for Solidity
                                                                       Smart Contracts. In ACSW 2021. 1–10.
based symbolic execution to check EVM bytecode and also
                                                                   [8] L Cordeiro et al. 2020. Survey on automated symbolic verification
simulate a virtual machine for execution-path exploration,             and its application for synthesising cyber-physical systems. IET
which might lead to performance degradation [20]. ESBMC-               Cyper-Phys. Syst.: Theory & Appl. 5, 1 (2020), 1–24.
Solidity also uses SMT solvers as backends, but it processes       [9] O Alhawi et al. 2021. Verification and refutation of C programs based
ASTs, so there is no need for environment simulation.                  on k-induction and invariant inference. STTT 23, 2 (2021), 115–135.
                                                                  [10] L Chaves et al. 2019. Verifying fragility in digital systems with uncer-
   A tool that also adopts SMT encoding and solvers to find
                                                                       tainties using DSVerifier v2. 0. JSS 153 (2019), 22–43.
satisfiability for a property violation is discussed by Alt and   [11] M Gadelha et al. 2018. ESBMC 5.0: an industrial-strength C model
Reitwiessner [20]. They developed a component to trans-                checker. In ASE 2018. 888–891.
late programs into smtlib2 formulae to interface with SMT         [12] L Cordeiro et al. 2011. SMT-based bounded model checking for em-
solvers [20]. The main difference between it and ESBMC-                bedded ANSI-C software. TSE 38, 4 (2011), 957–974.
                                                                  [13] S Tikhomirov et al. 2018. Smartcheck: Static analysis of ethereum
Solidity is that the latter supports code instrumentation,
                                                                       smart contracts. In WETSEB 2018. 9–16.
which narrows down the scope of inputs that trigger viola-        [14] J Feist et al. 2019. Slither: a static analysis framework for smart con-
tions. In addition, ESBMC-Solidity can also be extended on             tracts. In WETSEB 2019. IEEE, 8–15.
top of various existing verification strategies and reasoning     [15] L Luu et al. 2016. Making smart contracts smarter. In ACM SIGSAC
techniques provided by ESBMC, such as k-induction.                     CCS 2016. 254–269.
                                                                  [16] ConsenSys/mythril. v0.22.1. Github. Retrieved Nov 24, 2021 from
                                                                       https://github.com/ConsenSys/mythril
5     Conclusions                                                 [17] esbmc/esbmc. v6.8. Github. Retrieved Nov 24, 2021 from https:
We presented ESBMC-Solidity that checks memory safety                  //github.com/esbmc/esbmc
and user-defined properties in smart contracts written in         [18] linux.org. 2019. time(1) — Linux manual page. Retrieved Nov 24, 2021
                                                                       from https://man7.org/linux/man-pages/man1/time.1.html
the Solidity programming language. We evaluated ESBMC-            [19] SWC Registry. 2020. SmartContractSecurity. Retrieved Nov 24, 2021
Solidity against other SOTA verification tools and overcame            from https://swcregistry.io/
them, confirming all presented bugs and providing the associ-     [20] L Alt et al. 2018. SMT-based verification of solidity smart contracts. In
ated counterexamples. Although ESBMC-Solidity is an early              ISoLa. Springer, 376–388.
