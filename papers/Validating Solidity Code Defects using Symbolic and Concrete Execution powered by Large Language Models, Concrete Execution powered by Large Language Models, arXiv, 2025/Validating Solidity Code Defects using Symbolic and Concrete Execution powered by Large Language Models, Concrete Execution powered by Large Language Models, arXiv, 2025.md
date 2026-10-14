     Validating Solidity Code Defects using Symbolic and
    Concrete Execution powered by Large Language Models

                      S, tefan-Claudiu Susan                                Andrei Arusoaie
                 Alexandru Ioan Cuza University of Ias, i,         Alexandru Ioan Cuza University of Ias, i,
                    Department of Computer Science                    Department of Computer Science
                             Ias, i, România                                   Ias, i, România
                     claudiu_susan@yahoo.com                           andrei.arusoaie@uaic.ro

                                                     Dorel Lucanu
                                          Alexandru Ioan Cuza University of Ias, i,
                                             Department of Computer Science
                                                      Ias, i, România
                                               dorel.lucanu@gmail.com


       The high rate of false alarms from static analysis tools and Large Language Models (LLMs) com-
       plicates vulnerability detection in Solidity Smart Contracts, demanding methods that can formally
       or empirically prove the presence of defects. This paper introduces a novel detection pipeline that
       integrates custom Slither-based detectors, LLMs, Kontrol, and Forge. Our approach is designed to
       reliably detect defects and generate proofs.
            We currently perform experiments with promising results for seven types of critical defects. We
       demonstrate the pipeline’s efficacy by presenting our findings for three vulnerabilities—Reentrancy,
       Complex Fallback, and Faulty Access Control Policies—that are challenging for current verification
       solutions, which often generate false alarms or fail to detect them entirely. We highlight the potential
       of either symbolic or concrete execution in correctly classifying such code faults. By chaining these
       instruments, our method effectively validates true positives, significantly reducing the manual veri-
       fication burden. Although we identify potential limitations, such as the inconsistency and the cost
       of LLMs, our findings establish a robust framework for combining heuristic analysis with formal
       verification to achieve more reliable and automated smart contract auditing.


1    Introduction
Since the emergence of blockchain platforms like Ethereum [7], developers have implemented numer-
ous Decentralized Applications (DApps) across diverse domains, from gaming to decentralized finance.
Solidity [31] remains the most widely adopted programming language for the Ethereum ecosystem. How-
ever, like any emerging technology, this development paradigm introduced critical shortcomings. The
impact of these defects is magnified by two of blockchain’s core pillars: immutability, which historically
prevented faulty code from being replaced, and public bytecode, which allows malicious actors to easily
search for exploits. The devastating potential of such vulnerabilities was demonstrated by catastrophic
events, including the “DAO Hack” [19] and the “Parity Wallet Hack” [23], which resulted in hundreds
of millions of dollars in losses.
    The issues identified in Smart Contracts feature unique categories specific to the Blockchain environ-
ment. For instance, prominent examples include Reentrancy, a critical vulnerability where an external
call allows an attacker’s contract to repeatedly re-enter a function before its state has been updated, often
leading to the complete draining of the contract’s funds. Another distinct category involves Gas-Costly
Patterns, which are not traditional security flaws but rather inefficient coding practices. These patterns,

                                                                                  © S.C. Susan, A. Arusoaie, and D. Lucanu
Andrei Arusoaie, Horaţiu Cheval, Radu Iosif: FROM 2025
                                                                                  This work is licensed under the
EPTCS 427, 2025, pp. 98–116, doi:10.4204/EPTCS.427.7
                                                                                  Creative Commons Attribution License.
     S.C. Susan, A. Arusoaie, and D. Lucanu                                                                     99


     such as unbounded loops or excessive data storage, result in prohibitively high transaction fees (gas) for
     users, potentially rendering the contract economically unviable or unusable. In addition to these new
     types of defects, Solidity still features code faults that are common among most programming languages
     and software development paradigms, such as Division by Zero or Integer Overflow/Underflow. A cru-
     cial step in addressing smart contract flaws has been the development of vulnerability taxonomies. Prior
     efforts in this area include both formal academic classifications aimed at creating a comprehensive un-
     derstanding of bug types [25], and dynamic, community-led efforts (e.g., “SWC Registry” [35], “DASP
     Top 10” [9]), which serve as practical guides for developers.
         State-of-the-art detection tools for smart contract vulnerabilities remain however limited. They often
     miss real flaws or raise false alarms. The types of vulnerabilities range from coding mistakes to chal-
     lenges inherent to the execution model of smart contracts inside the blockchain ecosystem. For instance,
     the gas system constrains execution by attaching a cost to every instruction, and insufficient gas may
     alter the expected behavior of a contract. The transactional nature, where failures revert the entire execu-
     tion, can be abused to mount various attacks (e.g., denial-of-service). In addition, the entities executing
     transactions, such as miners (in proof of work [20]) or validators (in proof of stake [6]), may themselves
     act maliciously. Therefore, it is difficult for a detection tool to address this diversity of vulnerabilities.
         A simple example of a scenario falsely detected as a possible vulnerability is shown in Listing 1. This
     contract allows users to either deposit or withdraw Ether, essentially simulating a bank. The deposit
     function receives Ether and records the balance of the caller in a mapping called balance. The with-
     drawal operation uses transfer() — a function that sends Ether from a contract to a specified address.
         Many detection tools (e.g., Slither [11]) flag this contract as “reentrant” because the balance is up-
     dated after the call to transfer(). More specifically, if the withdraw() function is called from another
     contract C, the transfer() call triggers a callback to C. This happens because, in Ethereum, whenever
     a smart contract is called, there is a default function named receive() that is executed automatically.
     If C is malicious, it can exploit the behavior of this default function to immediately invoke another call
     to withdraw(). As a result, the balance mapping may not be updated in time, allowing the attacker to
     drain funds from ReentrancySimple as long as funds remain available.
         However, in newer versions of Solidity, the transfer() function enforces a fixed gas limit of 2300
     units. If this gas is exceeded, the entire transaction is reverted. Since 2300 gas is insufficient for C to
     reinitiate a second call to withdraw(), Reentrancy is no longer possible.
 1   // SPDX - License - Identifier : MIT
 2   pragma solidity 0.8.29;
 3
 4   contract ReentrancySimple {
 5       mapping ( address = > uint ) private balance ;
 6
 7        function deposit () external payable {
 8            balance [ msg . sender ] = msg . value ;
 9        }
10
11        function withdraw () external {
12            uint addrBal = balance [ msg . sender ];
13            // transfer does not trigger Reentrancy
14            payable ( msg . sender ) . transfer ( addrBal ) ;
15            balance [ msg . sender ] = 0;
16        }
17   }
                          Listing 1: An example of a Reentrancy vulnerability false alarm
100                                                                         Proving Solidity Code Defects




                            Figure 1: Output provided by Slither for Listing 1

     During a previous study [3], we noticed that Slither flags this example as vulnerable to Reentrancy
attacks, which is a false alarm. Its exact output can be seen in Figure 1. The detection mechanisms
employed by Slither do not feature concrete or symbolic execution. Being able to perform one of these
two techniques on the contract would have shown that a Reentrancy attempt always fails. For exam-
ple, Mythril [29], a tool that uses symbolic execution, was able to correctly mark this contract as “not
vulnerable”. However, it was unable to yield valid detections for other instances of different types of
vulnerabilities, where Slither performed considerably better. Thus, we conjecture that a mixture of these
two approaches might produce the best overall results.
     If we switch the context to the detection capabilities of the large language models, Google Gemini 2.5
Flash [14] and other popular models were also tricked by this scenario. Exactly as Slither, they signaled
that the contract presented in Listing 1 was vulnerable to Reentrancy exploits. When further questioned,
Gemini 2.5 Flash falsely stated that 2300 gas is enough to call a function. Since the popularization of
LLMs, multiple studies (see, e.g., [33, 8, 40]) on their potential for identifying Solidity defects have been
conducted. Even though these studies used different datasets, did not use the same AI models, and varied
in some methodological aspects, a consistent conclusion emerged: LLMs can detect many issues that
traditional tools cannot detect, but their usefulness is limited by false alarms and consistency issues.
     This paper introduces a novel, three-stage mechanism to validate potential smart contract vulnerabil-
ities and eliminate false positives. First, we employ a custom static analysis tool built on Slither modules
to scan for specific coding patterns that are prerequisites for certain bugs. For example, a Reentrancy
analysis is only triggered if the contract contains logic for handling Ether or tokens, as this vulnerabil-
ity’s callbacks typically occur during currency transfers. If these prerequisite patterns are present, our
second stage uses a Large Language Model (LLM) to generate a concrete proof-of-exploit. To improve
the accuracy of this output, we guide the LLM using bespoke “testing patterns” tailored to each defect
class. For the third and final stage, we execute the tests using Kontrol [24, 16] or Forge [12] (depending
on the issue type) to verify the presence of a defect, or its absence within the scope of our test scenarios,
through either concrete or symbolic execution. A successfully generated and executed test serves as a
formal proof, if Kontrol is used, or as an empirical proof, if Forge is used. The primary limitation of this
experimental approach is its dependency on the underlying LLM’s capability to accurately follow our
structured prompts.

Summary of contributions
   1. We identify some shortcomings that are present in state-of-the-art defect detection tools, such as
      not identifying or providing false alarms for the code defects that are discussed in this paper, and
      present a list of examples that highlight the potential of our approach in Section 3.
   2. We propose an approach that is custom-made for each of the seven defect types that we have
      experimented with so far in Section 4. The use of the proposed approach is illustrated on an
      example in Section 5
S.C. Susan, A. Arusoaie, and D. Lucanu                                                                   101


    3. We present the challenges and limitations of the proposed approach in Section 6.

Paper organization In Section 2, we briefly recall information about the blockchain and smart con-
tracts, foundational tools (Forge, Kontrol, Slither), some of our previous work, and related approaches.
To validate our proposal, we present multiple case studies in Section 3 that analyze scenarios where
other tools fail. We detail our novel detection pipeline in Section 4. We provide an example of how our
pipeline analyzes a contract to check for a specific defect category in Section 5. A discussion of our ap-
proach’s future potential and the challenges that we might encounter follows in Section 6. We conclude
in Section 7.


2     Background & Motivation
2.1    Blockchain & Smart Contracts
A blockchain is a decentralized, distributed, and cryptographically secured digital ledger. Its architecture,
first conceptualized for a peer-to-peer electronic cash system [20], creates a trustless environment where
participants can interact directly without a central intermediary. This is achieved through a combination
of core properties: decentralization, which distributes control across a network; transparency, where all
participants share a common view of the ledger; and immutability, which ensures that transactions, once
recorded in a block and added to the chain, are computationally infeasible to alter.
     The capabilities of blockchain technology were significantly expanded with the introduction of smart
contracts. The concept, which predates blockchain, describes computer-observable and enforceable pro-
tocols that can self-execute the terms of an agreement [36]. The Ethereum platform was the first to realize
this vision on a global scale, providing a permissionless blockchain with a Turing-complete virtual ma-
chine known as the Ethereum Virtual Machine (EVM) [7, 39]. This innovation enabled the creation of
complex Decentralized Applications (DApps) for a wide range of use cases beyond currency transfers.
     However, the “code is law” paradigm of smart contracts presents a double-edged sword. The prin-
ciple of immutability, while fundamental to the security and integrity of the ledger, means that bugs and
vulnerabilities in deployed contract code are permanent. A flawed contract cannot be easily patched
or updated, leaving it open to perpetual exploitation. This high-stakes environment, where simple cod-
ing errors can lead to catastrophic financial losses, requires the use of advanced and rigorous analysis
techniques to ensure the security and correctness of smart contracts before they are deployed [4].

2.2    Tools that Might be Used for the Development and Analysis of Smart Contracts
Slither [11] is a powerful and widely adopted static analysis framework for Solidity. It converts smart
contract source code into an intermediate representation called SlithIR, which provides a high-level view
of the contract’s logic and control flow. Upon this representation, Slither executes a comprehensive suite
of vulnerability detectors, which are designed to identify a broad spectrum of issues, ranging from critical
security flaws like Reentrancy and incorrect access control to code quality and optimization problems.
Besides these strong points, Slither is an open-source tool that encourages the community to build their
tools using the modules that it provides or contribute to improving Slither itself. This allows developers
to focus on implementing useful and innovative analysis techniques, building upon the information that
is accessible through importing Slither modules into their code. For example, using Slither modules,
one can extract the CFG, the parameters of a function, the state variables of a contract, or the variables
read/written by each statement.
102                                                                          Proving Solidity Code Defects


    Foundry [13] is a modern, high-performance toolkit for Ethereum application development, written
entirely in Rust. Unlike traditional JavaScript-based frameworks, Foundry provides a comprehensive
and cohesive development environment that allows for faster and more efficient workflows. It consists
of several core components: Forge, a testing framework that enables developers to write tests directly in
Solidity; Cast, a versatile command-line tool for performing RPC calls to interact with smart contracts
and query blockchain data; Anvil, a fast local testnet node for development and debugging; and Chisel,
an interactive Solidity shell for rapid prototyping. By combining blazing-fast compilation and execution
speeds with a Solidity-centric design, Foundry empowers developers to build, test, and deploy smart
contracts with greater productivity and confidence.
    Forge [12] is renowned for its exceptional speed in compiling contracts and executing tests. It offers a
rich set of features designed for robust contract verification, including native fuzz testing to automatically
discover edge-case vulnerabilities with random inputs, detailed gas reports to help optimize transaction
costs, and a powerful set of “cheatcodes” that allow developers to manipulate the blockchain state (e.g.,
block number, msg.sender) for simulating complex scenarios. This combination of speed, usability, and
advanced testing capabilities makes Forge an essential tool for modern smart contract development and
auditing.
    Kontrol [24] is a formal verification tool designed for EVM-based smart contracts and integrated
within the Foundry ecosystem. It enables developers to prove the correctness of their code with mathe-
matical certainty, moving beyond the limitations of conventional testing. At its core, Kontrol leverages
K-EVM [16], a formal and executable specification of the Ethereum Virtual Machine written in the K
Framework [27]. By employing symbolic execution, Kontrol analyzes all possible execution paths of
a contract simultaneously. Developers write properties, or “lemmas”, as functions directly within their
Solidity test files, specifying invariants that must always hold true, such as the absence of Reentrancy or
the correctness of token accounting. Kontrol then attempts to formally prove that these properties are un-
breakable under any circumstance, providing a powerful method for verifying the security and functional
correctness of high-value smart contracts.

2.3   Related Work
We are building upon our prior efforts [32, 34], in which we enhanced the detection capabilities of
Slither by integrating Interval Analysis enriched with constraints. This enhancement enabled the detec-
tion of several critical issues not natively flagged by Slither, including Unreachable Code, Insufficient
Parameter Validation, and Locked Ether. A primary challenge of this approach remains the considerable
effort required to formally model the complete semantics of the Solidity language. While we previously
evaluated the full scope of vulnerabilities detectable via Interval Analysis, the current work extends our
methodology to new categories, such as Access Control. To achieve this, we leverage our existing so-
lution for Interval Analysis and Constraint Gathering to compute rich contextual data, which serves to
improve the performance of Large Language Models (LLMs) in identifying issues and then generating
scenarios in the form of tests. These tests can then be validated using either Forge or Kontrol, depending
on whether symbolic or concrete execution is more appropriate for that specific defect type.
    The work presented in [28] addresses the challenge of establishing correctness, particularly for access
control aspects, in smart contracts. The authors undertake a case study using an existing smart contract
application called Palinodia, which focuses on decentralized identity management and access control for
binary file integrity. Their approach involves formally specifying and verifying correctness at both the
single-function level and for temporal properties of the overall application, demonstrating how verified
low-level properties can support higher-level correctness. They developed natural language specifications
S.C. Susan, A. Arusoaie, and D. Lucanu                                                                    103


for Palinodia’s functions and translated them for verification using the solc-verify [15] tool, finding it
straightforward and fast for single functions. One flaw of current analysis tools that the authors point out
is the lack of support for application-specific properties and verifying interacting contracts. However,
their study took place before the popularization of LLMs. We believe that AI models have the potential
to assist in automatically generating contract-specific properties if given enough context.
     Many other notable solutions that leverage LLMs to assist in traditional static analysis approaches
have recently emerged. One such notable solution is IRIS [18], which integrates LLMs with traditional
static analysis tools like CodeQL to overcome the challenges of manual taint specification crafting. A
taint specification defines security-relevant data flows by identifying data sources (untrusted input), sinks
(vulnerable functions), and sanitizers (functions that make data safe). IRIS leverages an LLM to auto-
matically infer these specifications and then uses a tool like CodeQL to find vulnerable program paths.
Finally, it uses the LLM again as a post-analysis filter to reduce false alarms by asking it to validate the
findings. While both our approach and IRIS use an LLM to reason about the code, our methodologies
differ significantly. IRIS uses the LLM to generate configurations for a traditional static analyzer and to
filter its results, whereas our pipeline uses the LLM to generate executable tests that are then formally or
empirically verified by a symbolic or concrete execution engine like Kontrol or Forge.
     In the area of Smart Contracts vulnerability detection, LLM-SmartAudit [38] is an innovative frame-
work that leverages a multi-agent conversational approach with LLMs. Designed to overcome the limi-
tations of traditional tools, its core methodology is built upon role specialization, deploying specialized
agents such as a “Project Manager”, “Auditor”, and “Solidity Programming Expert”. These agents en-
gage in structured conversations to analyze code and identify weaknesses, enhancing factual accuracy.
While both our work and LLM-SmartAudit use LLMs to reason about Solidity code, the application and
architecture are fundamentally different. LLM-SmartAudit relies on a conversational, multi-agent system
to directly identify vulnerabilities, whereas our pipeline uses a single LLM for a targeted code generation
task: populating test templates. In our approach, the final verdict of whether a defect exists comes from
an external execution engine, not the LLM itself.


3    Case Studies
Initially, we identified several scenarios that are not adequately handled by either traditional analysis tools
or LLMs. AI models and analysis tools that do not leverage symbolic or concrete execution appear to
struggle with accurately identifying or ruling out more "dynamic" issues. These fault categories involve
the gas system, user balances, access policies, or the contract’s intended logical behavior. Consequently,
we decided to employ either symbolic or concrete execution, depending on the issue type. We selected
Forge for the concrete execution approach and Kontrol for the symbolic execution approach. The draw-
back of using these tools lies in their requirement for manual interaction to write tests. We propose that
LLMs can perform this task if provided with sufficient context and a test template. Thus, we designed
a testing methodology and template for each of the issue types we initially identified, generating tests
for them using LLMs. We used Google Gemini 2.5 Pro via its official chat application for this purpose.
Currently, we have experimented with seven defect types: Reentrancy, Insufficient parameter validation,
Block Environment Dependency, Faulty Assert or Reverts, Gas Costly Pattern, Access Control, and
Possible Division by Zero.
     Each of the following subsections is dedicated to a specific defect. We first provide a brief definition,
followed by a representative smart contract that either contains the defect or illustrates a scenario prone
to false alarms from traditional tools. Finally, we present the corresponding Kontrol/Forge test, which
     104                                                                           Proving Solidity Code Defects


     we generated using Gemini 2.5 Pro based on our test templates.
        Before introducing our examples, we must establish basic concepts regarding Kontrol and Forge:
           • Forge fuzzes test parameters when running tests; the number of fuzz runs is customizable. Addi-
             tional variables with arbitrary values can also be defined within the test method.
           • Kontrol replaces test parameters with symbolic values. Other symbolic variables can also be de-
             fined within the test method.
           • The method vm.deal adds a specified amount of currency to an address’s balance.
           • The function vm.prank ensures all subsequent calls are performed by the designated address.
           • When using vm.expectRevert, we assert that the next executed method will throw an exception.
             If this does not occur, the statement will throw an exception, causing the test to fail.
           • Using vm.assume enforces a constraint. Forge discards fuzzing attempts for which the condition
             is not valid. When using Kontrol, condition will be attached to the existing condition path.


     3.1    Reentrancy – False Positive
     Reentrancy is a critical vulnerability where an external call within a function allows an attacker’s contract
     to repeatedly re-enter that function before its state has been updated. This exploit can often lead to the
     complete draining of the contract’s funds. This section examines a scenario that appears vulnerable but
     is actually a false positive.
         For our first case study, we highlight an example of a contract that might seem vulnerable to Reen-
     trancy at first glance, but in reality, is not. The code is shown in Listing 1. As mentioned in Section 1,
     due to its use of the transfer primitive instead of call, the function that sends Ether is not reentrant.
         Our process for proving that the withdraw function is not vulnerable to Reentrancy involves two
     steps. The test contract implemented to prove this aspect is displayed in Listing 2. We first need to
     prove that the function being tested works in usual scenarios. To prove this aspect, we implement the
     test_proofWithdrawUsuallyWorks function. This function validates that a normal flow—where an
     address deposits Ether and withdraws it—behaves as expected if no malicious actions are employed.
     For this "positive" scenario, we use the test contract to call the methods for depositing and withdrawing
     Ether. For the second step, we implement a malicious actor that will attempt to perform a Reentrancy
     attack. The code for the attacker contract can be found in Listing 3. The second test method that we
     implemented, test_proofReentrancyExploit, is very similar to the first one. However, this time, an
     instance of the attacker contract calls the suspected "reentrant" method, and we expect the transaction to
     revert every time. Thus, we have proven that the method behaves as expected when used as intended, but
     will revert if the user attempts any malicious actions. If the first test passes and the second fails, then the
     contract is vulnerable to Reentrancy.
 1   contract ReentrancySimpleTest is Test {
 2
 3          ReentrancySimple public _contractUnderTest ;
 4          Attacker public _attacker ;
 5          uint256 constant ETH_UPPER_BOUND = 2 ** 45;
 6
 7          function setUp () public {
 8              _contractUnderTest = new ReentrancySimple () ;
 9              _attacker = new Attacker ( address ( _contractUnderTest ) ) ;
10          }
     S.C. Susan, A. Arusoaie, and D. Lucanu                                                                       105


11
12        function t e s t _ p r o o f W i t h d r a w U s u a l l y W o r k s ( uint initialDeposit ) public {
13            vm . assume ( initialDeposit < ETH_UPPER_BOUND ) ;
14            vm . deal ( address ( _attacker ) , initialDeposit ) ;
15            vm . deal ( address ( _contractUnderTest ) , initialDeposit ) ;
16            // --- ARRANGE ---
17            _contractUnderTest . deposit { value : initialDeposit }() ;
18
19             // --- ACT ---
20             _contractUnderTest . withdraw () ;
21       }
22
23        function t e s t _ p r o o f R e e n t r a n c y E x p l o i t ( uint initialDeposit ) public {
24            vm . assume ( initialDeposit < ETH_UPPER_BOUND ) ;
25            vm . deal ( address ( _attacker ) , initialDeposit ) ;
26            vm . deal ( address ( _contractUnderTest ) , initialDeposit ) ;
27            // --- ARRANGE ---
28            vm . prank ( address ( _attacker ) ) ;
29            _attacker . resetAttackCount () ;
30            _contractUnderTest . deposit { value : initialDeposit }() ;
31
32             // --- ACT ---
33             vm . expectRevert () ;
34             _contractUnderTest . withdraw () ;
35       }
36
37       receive () external payable {
38       }
39   }
             Listing 2: Proving that the contract in Listing 1 is not susceptible to Reentrancy attacks

 1   contract Attacker {
 2       ReentrancySimple private _victim ;
 3       uint256 public attackCallCount ;
 4         constructor (
 5            address victimAddress )
 6       {
 7            _victim = ReentrancySimple ( victimAddress ) ;
 8       }
 9
10       function resetAttackCount () public
11       {
12           attackCallCount =0;
13       }
14
15       receive () external payable {
16           if ( attackCallCount < 1) {
17                attackCallCount ++;
18                _victim . withdraw () ;
19           }
20       }
21   }
                            Listing 3: Attacker helper contract for the proof in Listing 1
     106                                                                          Proving Solidity Code Defects


     3.2   Gas Costly Pattern – Complex Fallback
     Gas Costly Pattern defects are not traditional security flaws but rather inefficient coding practices that
     can result in prohibitively high transaction fees, which are measured in gas, potentially rendering a
     contract unusable. This section explores a specific subtype, which we term Complex Fallback, where an
     expensive operation in a contract’s receive callback causes transactions with a limited gas supply to fail.
         Listing 4 contains a simple crowdfunding contract. While the business logic, contract, and its access
     policies are correctly implemented, an issue could gravely affect the contract’s usability. This issue lies in
     the contract’s receive callback. It assigns a state variable of the contract, an operation that is expensive
     from a gas perspective. This can be problematic because Solidity primitives such as send and transfer
     only attach 2300 gas to the transaction when used to send Ether. Writing to the contract state consumes
     considerably more gas than this amount. Thus, if a contract uses one of these two functions to send
     currency to the example contract, the transaction will always revert.
 1   contract ComplexFallback {
 2       address private _owner ;
 3       address private _latestDonor ;
 4
 5         modifier onlyOwner () {
 6             require (
 7                 msg . sender == _owner ,
 8                 " Only the owner of the contract can access this "
 9             );
10             _;
11         }
12
13         constructor () {
14             _owner = msg . sender ;
15         }
16
17         receive () external payable {
18         // Expensive state change
19              _latestDonor = msg . sender ;
20         }
21
22         function withdrawFunding () external onlyOwner {
23             payable ( msg . sender ) . transfer ( address ( this ) . balance ) ;
24         }
25
26         function getLatestDonor () external view onlyOwner returns ( address ) {
27             return _latestDonor ;
28         }
29   }
                   Listing 4: A contract containing a receive callback that uses too much gas
         We provide a possible solution to confidently prove the presence of such an issue in Listing 5. Since
     the undesired behavior is triggered when receiving Ether, no parameters or contract state need to be
     considered. Consequently, using a tool such as Kontrol to generate a proof through symbolic execution
     is not mandatory. Using Forge to carry out concrete executions on the two test methods is sufficient to
     prove this defect. Each test method needs to be executed once to reveal the code fault; no fuzzing is
     needed. Our approach for proving the presence of this defect involves two steps (test methods).
         The first method, test_proveTransferWorks, validates that sending currency to the contract works
     when all the gas remaining for the transaction is forwarded, thereby allowing the execution of the com-
     S.C. Susan, A. Arusoaie, and D. Lucanu                                                                           107


     plex fallback. To attach this amount of gas, we use the call primitive, which forwards all remaining
     gas by default. It also returns "true" if the transaction was successful; we validate this result through an
     assertion at the end. The second test, test_proveTransferDoesNotWorkWithLimitedGas, is similar.
     The key difference lies in the fact that this time, we use transfer, and we expect the transaction to fail.
     The first test proves that sending currency behaves as expected when all gas is forwarded. The second
     test proves that the transaction reverts if only 2300 gas is forwarded. We can conclude that the receive
     callback can only fail due to an "Out-of-Gas" exception, thus proving the Complex Fallback issue.
          This testing strategy for callbacks that consume too much gas can be easily applied to any contract.
     The two tests remain the same; the only aspect that should be changed is the declared type and the
     initialization of _contractUnderTest. Because this issue is tied to a behavior that all contracts capable
     of receiving currency possess, no other adjustments regarding the contract’s logic are necessary. An
     LLM can perform this data type replacement if given the template. Thus, we believe that this type of
     defect can be identified reliably using our approach.
 1   contract ComplexFallbackTest is Test , KontrolCheats {
 2       ComplexFallback public _contractUnderTest ;
 3
 4             function setUp () public {
 5                _contractUnderTest = new ComplexFallback () ;
 6         }
 7
 8         function te s t_ pr ov e Tr an sf e rW or ks () public
 9         {
10             // --- ARRANGE ---
11             vm . deal ( address ( this ) , 1 ether ) ;
12             // --- ACT ---
13             ( bool success ,) = payable ( address ( _contractUnderTest ) ) . call { value : 1 ether
                     }( " " ) ;
14             // --- ASSERT ---
15             vm . assertTrue ( success , " The transaction should work " ) ;
16         }
17
18         function t e s t _ p r o v e T r a n s f e r D o e s N o t W o r k W i t h L i m i t e d G a s () public
19         {
20             // --- ARRANGE ---
21             vm . deal ( address ( this ) , 1 ether ) ;
22             // --- ASSERT ---
23             vm . expectRevert () ;
24             // --- ACT ---
25             payable ( address ( _contractUnderTest ) ) . transfer (1 ether ) ;
26         }
27   }
                                      Listing 5: Proof for the defect presented in Listing 4


     3.3    Insufficient Implementation & Usage of Access Policies
     Insufficient Access Policies are defects where functions containing critical logic or actions, such as trans-
     ferring Ether or destroying a contract, are not properly secured. This lack of security can permit arbitrary
     and potentially malicious access to sensitive operations that should be restricted.
         We present a basic Access Control issue in Listing 6. While we know that the selfdestruct
     function is deprecated, it serves as an illustrative example, and this type of issue is not limited to this
     108                                                                         Proving Solidity Code Defects


     Solidity primitive. This defect type applies to functions that contain critical logic or actions, such as
     transferring Ether. Usually, these methods should be secured via access policies, preventing arbitrary,
     potentially malicious access. The example presented in this section implements an access modifier that
     only allows the address that deployed the contract to access functions to which onlyOwner is attached.
     However, this modifier is not attached to the function containing the selfdestruct primitive, thus
     making it accessible to any address. Because the logic and recommended access policies of a function are
     hard to determine via traditional static analysis, we believe that using Large Language Models might fill
     the gaps required to reliably prove the insufficient implementation of access policies for some functions.
 1   contract Un p ro te ct e dS el fd e st ru ct {
 2       mapping ( address = > uint256 ) private _employees ;
 3       address private _owner ;
 4
 5         modifier onlyOwner () {
 6             require (
 7                 msg . sender == _owner ,
 8                 " Only the owner of the contract can access this "
 9             );
10             _;
11         }
12
13         constructor () {
14             _owner = msg . sender ;
15         }
16
17         function sendSalary ( address employeeAddress ) external payable onlyOwner {
18             _employees [ employeeAddress ] = msg . value ;
19         }
20
21         function getSalary () external {
22             require (
23                 _employees [ msg . sender ] > 0 ,
24                 " You cannot receive your salary at this moment "
25             );
26             _employees [ msg . sender ] = 0;
27             payable ( msg . sender ) . transfer ( _employees [ msg . sender ]) ;
28         }
29
30         // No access modifier added , every address can call this
31         function cancelContract () external {
32              selfdestruct ( payable ( msg . sender ) ) ;
33         }
34   }
                                 Listing 6: A containing an Access Control defect

     We highlight a test that proves this vulnerability in Listing 7. Our proof contains a single test demonstrat-
     ing that an arbitrary address, not the owner, can call the function containing the selfdestruct primitive.
     By providing the address that will call the function in the caller parameter, we inform Kontrol that it
     should be treated as a symbolic value. We then use vm.assume to attach a constraint to this symbolic
     value, ensuring it has a value different from the owner’s. If access policies are correctly implemented,
     this call should revert for any user who is not the contract’s owner, and the test should pass. However,
     for the example from Listing 6, the function does not revert, thus causing the test to fail.
         We can extract a template from this example. It should contain a function call made by a symbolic
     S.C. Susan, A. Arusoaie, and D. Lucanu                                                                    109


     address, precisely as the caller parameters are used. A crucial point is imposing constraints on the
     symbolic value that reflect the fact that the symbolic address should not be part of the group of users
     typically allowed to access the function. These constraints used to be hard to determine automatically.
     However, we hypothesize that LLMs have potential to find recommended access policies for a function.
 1   contract U n p r o t e c t e d S e l f d e s t r u c t T e s t is Test {
 2
 3         U n p r o te c te dS el f de st ru c t public _contractUnderTest ;
 4
 5         function setUp () public {
 6             _contractUnderTest = new Un pr o te ct ed S el fd es t ru ct () ;
 7         }
 8
 9         function test_accessControl ( address caller ) public {
10             // --- ARRANGE ---
11             vm . assume ( caller != address ( this ) ) ;
12             vm . prank ( caller ) ;
13             // --- ASSERT ---
14             vm . expectRevert () ;
15             // --- ACT ---
16             _contractUnderTest . cancelContract () ;
17         }
18   }
                                    Listing 7: Proof for the defect presented in Listing 6


     4    Towards a Combined Approach
     As discussed in the preceding sections, each technique possesses inherent limitations. Large Language
     Models do not provide consistent responses, particularly when lacking sufficient context and examples.
     Fuzz testing and symbolic execution-based testing necessitate test contracts tailored specifically for the
     contract under analysis. Furthermore, symbolic execution can be slow in terms of analysis time. While
     being fast and capable of detecting an impressive number of faults, Slither is unable to correctly label
     certain defect categories. It also struggles with specific scenarios that highlight defects it otherwise labels
     correctly. These flaws do not stem from implementation issues but rather from the fundamental nature
     of the analysis itself, as each approach has its inherent strengths and weaknesses.
          Consequently, we conjecture that combining all these approaches into a single solution will leverage
     their individual strengths while mitigating some of their weaknesses. Our approach is structured in three
     steps: collecting contract information, generating symbolic or fuzz tests, and executing the tests. We use
     Slither to gather useful contextual information about the contract and other relevant data regarding the
     defect type under investigation. This information, along with a test template, is then forwarded to the
     LLM for test generation. The generated tests are subsequently executed using either Forge or Kontrol.
     Depending on the results, the issue is either signaled or not. If the process fails before test execution
     and result collection, issues are not signaled or are reported with a lower confidence rate. The method
     for reporting error cases depends on the type of vulnerability being investigated. For example, when
     investigating Access Control issues, a lower confidence rate might be reported if the contract contains
     functions with critical operations such as selfdestruct but lacks custom-built access modifiers, even
     if the presence of insufficient access policies cannot be definitively proven as shown in Section 3. We
     propose to design custom flows for each defect type, as we believe this is the optimal decision given that
     each defect type requires specific information from Slither and a distinct number of tests with their own
    110                                                                         Proving Solidity Code Defects


    unique testing template. It is important to note that when we prove the presence or absence of a defect,
    we are formally or empirically proving that the contract is vulnerable or not vulnerable to the specific
    attack scenarios encoded in our test templates, not all possible variations of an attack.


    Stage 1: Contract preprocessing We begin our analysis process by using custom-built implemen-
    tations based on Slither modules to extract specific information. Each defect type necessitates a dif-
    ferent set of characteristics to be extracted, therefore requiring its own custom implementation. We
    chose Slither because its modules provide rich, structured data about the smart contract at various lev-
    els of abstraction. While we only mention a few examples—such as contract-level details like state
    variables, method-level information like parameters, and statement-level data like the variables in an
    instruction—the framework exposes far more granular information. This comprehensive access to the
    contract’s structure allows us to efficiently check for the specific prerequisite patterns of each defect
    type. Thus, by analyzing the data provided by Slither, we can verify the prerequisites for each defect
    type through a process similar to pattern matching. For example, when investigating Block Environ-
    ment Dependency, we search for methods that read block information, such as block.timestamp. If
    any such functions are found, we return the statements where those built-in variables are used. This
    initial step effectively rules out scenarios where a certain issue is not present. Continuing with the Block
    Environment Dependency example, if no block-related built-in variables are detected in the contract’s
    code, there is no need to continue the analysis process, as we can confidently state that this defect is not
    present. Similarly, for Reentrancy, we identify functions containing external calls and check if they are
    followed by state-modifying instructions.


    Stage 2: Test generation using LLMs After retrieving relevant information for the defect type under
    analysis, we proceed to the test generation step. We provide the gathered information along with a test
    template to the LLM. The LLM is tasked with populating this template with contract-specific informa-
    tion. The complexity of inserting the required information into the template varies depending on the
    issue type. For some issues, such as Complex Fallback, the model only needs to replace the type of the
    contract being tested. For other defects, more complex "reasoning" is required; examples of these more
    difficult tasks include inferring recommended access policies for a contract or handling intricate function
    calls and setups. So far, LLMs have been capable of creating tests for our examples. For some exper-
    iments, the tests generated were correct, and some required minimal adjustments. As expected, more
    complex generation tasks yield tests that need adjusting. A core aspect of our template implementation
    methodology is using code comments to provide direct instructions to the LLM, leveraging its powerful
    instruction-following capabilities. The template for the Complex Fallback defect, shown in Listing 8,
    exemplifies this approach. While the test methods and assertions are already complete, the comments
    guide the LLM to generate the final, contract-specific code.
1   // SPDX - License - Identifier : MIT
2   pragma solidity 0.8.29;
3   import { Test } from " ../../ lib / forge - std / src / Test . sol " ;
4   // Replace this import with one corresponding to the contract type being tested ,
         the file has the same name as the contract and is located in the same folder
          path as the example
5   import { ContractUnderTest } from " ../../ src / ContractUnderTest . sol " ;
6
7   // Append the type of the contract being tested to the name of the Test contract
8   contract Test is Test {
     S.C. Susan, A. Arusoaie, and D. Lucanu                                                                      111


9        // Replace the type " ContractUnderTest " of _contractUnderTest with the type of
              the contract that is currently being analyzed "
10                ContractUnderTest public _contractUnderTest ;
11
12          // If the constructor of the contract under test has parameters , the " setUp "
                 function should have the same parameters
13           function setUp () public {
14              // Initialize the contract being tested with the correct constructor , use
                      the correct parameters
15
16               // If the constructor is payable , use " vm . deal " to add balance to the
                      current contract before initializing the contract under test
17
18               _contractUnderTest = new ContractUnderTest () ;
19          }
20
21          // We will use this method to prove that the transfer works when all gas is
                 forwarded to the transaction
22          function te s t_ pr ov e Tr an sf e rW or ks () public
23          {
24               address sender = makeAddr ( " sender " ) ;
25               vm . deal ( sender , 1 ether ) ;
26               vm . prank ( sender ) ;
27               ( bool success ,) = payable ( address ( _contractUnderTest ) ) . call { value : 1 ether
                       }( " " ) ;
28               vm . assertTrue ( success , " The transaction should work " ) ;
29          }
30
31          // We will use this method to prove that the transfer fails when a hardcoded
                 amount of 2300 gas is attached to the transaction
32          function t e s t _ p r o v e T r a n s f e r D o e s N o t W o r k W i t h L i m i t e d G a s () public
33          {
34               address sender = makeAddr ( " sender " ) ;
35               vm . deal ( sender , 1 ether ) ;
36               vm . prank ( sender ) ;
37               vm . expectRevert () ;
38               payable ( address ( _contractUnderTest ) ) . transfer (1 ether ) ;
39          }
40   }
                        Listing 8: The template used to generate the test presented in Listing 5


     Stage 3: Test execution After obtaining the tests, we integrate them into a pre-configured Forge/Kon-
     trol environment. We then execute the tests and retrieve the success or failure result for each test method.
     The number of tests and the interpretation of their results vary depending on the issue type. For instance,
     as presented in Section 3, Reentrancy requires two tests, while Access Control requires only one. Fur-
     thermore, in our example, if both tests pass for Reentrancy, the contract is not vulnerable. The opposite
     is true for Access Control and Complex Fallback: if their respective tests pass, then the issue is present.
     If the process fails during this stage, we may provide lower confidence detections or no detections at all.
          While we have not yet implemented a complete practical solution for our proposed workflow, our
     previous experiments and existing implementations enable us to evaluate its feasibility and implementa-
     tion complexity. We have already experimented with extending Slither for new analysis types and use
     cases [34, 32], and we plan to implement the preprocessing stage soon. Furthermore, our prior experi-
112                                                                          Proving Solidity Code Defects


ence with programmatically interacting with LLMs [33] will significantly accelerate the development of
the second stage. Kontrol and Forge are the newest additions to our toolbox; however, we have already
manually executed meaningful scenarios that demonstrate their potential.


5     The Proposed Approach at Work on an Example
To illustrate our pipeline’s workflow, this section details the analysis of the contract from Listing 4 for a
Complex Fallback vulnerability. The process is described step-by-step, corresponding to the three stages
outlined in Section 4.

Stage 1 In the first stage, our pipeline checks the primary prerequisite for a ComplexFallback defect:
the contract’s ability to receive Ether through a simple transfer. The vulnerability specifically arises
when a contract’s receive() function, which is automatically executed upon a direct Ether transfer, is too
gas-intensive. Therefore, our Slither-based tool scans the contract from Listing 4 to confirm a receive()
function is implemented. Since the function is present, the contract is a candidate for this vulnerability,
and the analysis proceeds. If a receive() function were absent, the contract could not be affected by this
specific defect, and the analysis would terminate here with a negative finding.

Stage 2 In the second stage, we use the template from Listing 8 to generate the final test. The pipeline
sends this template to an LLM, such as Gemini 2.5 Pro, with instructions to populate it using the con-
tract’s specific details. For this example, the primary instruction is to replace the placeholder Contrac-
tUnderTest with ComplexFallback. The LLM then returns a complete and compilable Forge test file,
ready for execution. If this generation step fails, the analysis is terminated, and the contract is flagged as
potentially vulnerable, albeit with a lower confidence rating.

Stage 3 In the final stage, the generated test is executed using Forge. We chose Forge for this defect
because the analysis only requires two concrete executions, not the complex path exploration for which
Kontrol is designed. The pipeline runs the test and interprets the results:
      • test_proveTransferWorks() is expected to pass, confirming that the contract can receive Ether
        when sufficient gas is provided via call().
      • test_proveTransferDoesNotWorkWithLimitedGas() is also expected to pass, as it correctly
        anticipates that the transfer() call (with its 2300 gas limit) will revert.
Since both tests pass, our pipeline confidently flags the contract as vulnerable to the Complex Fallback
defect. This confirms that the contract’s receive() function is too gas-intensive for simple Ether transfers.


6     Challenges & Limitations
The consistency of LLMs Since LLMs are at the core of our implementation, many of our solution’s
challenges and limitations are inherently tied to their performance in test generation and the difficulty
of obtaining consistent responses. Obtaining consistent and structured output from LLMs has been a
challenge since their integration into various software solutions a few years ago. While some model de-
velopers, such as OpenAI, now offer options to define output structure in requests [22], our experiments
showed that this feature is still not mature, despite providing a noticeable improvement in structural
S.C. Susan, A. Arusoaie, and D. Lucanu                                                                  113


consistency. Regarding response content consistency, we have mitigated this issue by providing test tem-
plates and contextual information. Although the generated test code was not always identical, variations
were limited to aspects that did not affect correctness, such as test method parameter names, local vari-
able names, and assertion messages. We did not experiment much with top-tier reasoning models such
as OpenAI O3 [21], but we expect them to handle more complex scenarios compared to regular models.

The cost of using LLMs Another limitation of our solution is how software systems interact with
models. Most state-of-the-art models are proprietary and cannot be deployed locally. Instead, they are
accessed via APIs offered by developers, which can raise cost concerns depending on the model and the
number of tokens used. An alternative is open-source models like the DeepSeek models [1] and Llama
models [2]. Even though these models are publicly available and can be deployed locally, they still
demand considerable computational power. A traditional consumer system is usually not nearly enough
to run their larger variants. While the smaller variants offer satisfactory performance in general-purpose
tasks, there is still a noticeable gap when performing specialized tasks like ours.

Forge & Kontrol integration Another challenge lies in reliably integrating Forge and Kontrol into
our solution. Our use case would ideally require an “API mode” for these tools. Even though this
feature is not currently available, both tools are open source, so it could be implemented, though it would
demand additional development time. While automatically using them from the command line would
yield results, capturing the output via string matching might not be consistent, and it is not our preferred
approach. Currently, we have been able to overcome this limitation by using an LLM to convert the
unstructured CLI output into a structured format while also stripping away details that do not aid our
process. However, having a direct integration with Kontrol and Forge via an API would still be the
preferred approach due to its considerably greater robustness.


7    Conclusions
In this paper, we propose a combined approach aimed at accurately classifying code faults previously
misidentified by state-of-the-art tools or Large Language Models (LLMs) independently. While still in its
incipient phase, we hypothesize that this approach holds significant potential to enhance the accuracy of
code defect detection in Smart Contracts, particularly for issues currently undetected in most cases. Our
approach follows a three-step workflow that integrates the strengths of Slither, LLMs, and Forge/Kontrol.
    We manually conducted experiments across seven defect categories to evaluate the potential of LLMs
in generating specialized Smart Contract tests. Our results demonstrate that AI models are capable of
generating tests that accurately determine a contract’s vulnerability status. We presented three such sce-
narios in greater detail, which were initially misclassified by traditional analysis tools or LLMs. Through
our experiments, we reliably proved the presence of specific defects in these cases, and their absence for
the tested attack scenarios.
    For future work, we aim to develop a practical implementation of this concept. Our prior experience
in building custom detectors based on Slither will be invaluable for implementing the first step of our
approach. Subsequently, we intend to experiment with additional vulnerability types and design cor-
responding test templates. Regarding LLM interaction, we will explore various prompting techniques
and model variants to identify those yielding the most optimal and consistent results for our use case.
Moving to the next step, we will investigate methods for programmatic interaction with Forge/Kontrol.
If a direct API is unavailable, our fallback option will be command-line integration. Should this prove
114                                                                             Proving Solidity Code Defects


unreliable, we will consider extending these tools by implementing the necessary features. Regardless
of the integration method, we perceive substantial potential in automatically generating input for testing
tools, viewing it as a highly powerful approach from a detection capability perspective.

Acknowledgements

Part of this work was supported by a grant from the Romanian Ministry of Research, Innovation and
Digitization, CNCS/CCCDI - UEFISCDI, project 86/2025 ERANET-CHISTERA-IV-SCEAL, within
PNCDI IV.


References
 [1] DeepSeek-AI et al. (2025): DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement
     Learning, doi:10.48550/arXiv.2501.12948.
 [2] Hugo Touvronm Thibaut Lavril et al. (2023): LLaMA: Open and Efficient Foundation Language Models,
     doi:10.48550/arXiv.2302.13971.
 [3] Andrei Arusoaie & S, tefan-Claudiu Susan (2024): Towards Trusted Smart Contracts: A Comprehensive Test
     Suite For Vulnerability Detection. Empirical Software Engineering 29(5), p. 117, doi:10.1007/s10664-024-
     10509-w.
 [4] Nicola Atzei, Massimo Bartoletti & Tiziana Cimoli (2017): A Survey of Attacks on Ethereum Smart Contracts
     SoK. In: Proceedings of the 6th International Conference on Principles of Security and Trust - Volume 10204,
     Springer-Verlag, Berlin, Heidelberg, p. 164–186, doi:10.1007/978-3-662-54455-6_8.
 [5] Roberto Baldoni, Emilio Coppa, Daniele Cono D’Elia, Camil Demetrescu & Irene Finocchi (2018): A Survey
     of Symbolic Execution Techniques. ACM Computing Surveys 51, doi:10.1145/3182657.
 [6] Vitalik Buterin (2022): Proof of stake: The making of Ethereum and the philosophy of blockchains. Seven
     Stories Press.
 [7] Vitalik Buterin et al. (2014): A next-generation smart contract and decentralized application platform. white
     paper 3(37), pp. 2–1.
 [8] Chong Chen, Jianzhong Su, Jiachi Chen, Yanlin Wang, Tingting Bi, Jianxing Yu, Yanli Wang, Xingwei Lin,
     Ting Chen & Zibin Zheng (2024): When ChatGPT Meets Smart Contract Vulnerability Detection: How Far
     Are We? ACM Transactions on Software Engineering and Methodology 34, doi:10.1145/3702973.
 [9] DASP Top 10. https://dasp.co/.
[10] Dxo, Mate Soos, Zoe Paraskevopoulou, Martin Lundfall & Mikael Brockman (2024): Hevm, a Fast
     Symbolic Execution Framework for EVM Bytecode, pp. 453–465. Springer Nature Switzerland, Cham,
     doi:10.1007/978-3-031-65627-9_22.
[11] Josselin Feist, Gustavo Grieco & Alex Groce (2019): Slither: a static analysis framework for smart con-
     tracts. In: 2019 IEEE/ACM 2nd International Workshop on Emerging Trends in Software Engineering for
     Blockchain (WETSEB), IEEE, pp. 8–15, doi:10.1109/WETSEB.2019.00008.
[12] Forge Documentation. https://getfoundry.sh/forge/reference/forge-doc/.
[13] Foundry Documentation. https://getfoundry.sh/introduction/overview.
[14] Gemini Team (2024): Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context,
     doi:10.48550/arXiv.2403.05530. Available at https://arxiv.org/abs/2403.05530.
[15] Ákos Hajdu & Dejan Jovanović (2019): solc-verify: A Modular Verifier for Solidity Smart Contracts.
     In: Working conference on verified software: theories, tools, and experiments, Springer, pp. 161–179,
     doi:10.48550/arXiv.1907.04262.
S.C. Susan, A. Arusoaie, and D. Lucanu                                                                      115


[16] Everett Hildenbrandt, Manasvi Saxena, Nishant Rodrigues, Xiaoran Zhu, Philip Daian, Dwight Guth, Bran-
     don Moore, Daejun Park, Yi Zhang, Andrei Stefanescu & Grigore Roşu (2018): KEVM: A Complete Formal
     Semantics of the Ethereum Virtual Machine. pp. 204–217, doi:10.1109/CSF.2018.00022.
[17] James King (1976): Symbolic Execution and Program Testing.             Commun. ACM 19, pp. 385–394,
     doi:10.1145/360248.360252.
[18] Ziyang Li, Saikat Dutta & Mayur Naik (2025): LLM-Assisted Static Analysis for Detecting Security Vul-
     nerabilities. In: International Conference on Learning Representations, doi:10.48550/arXiv.2405.17238.
     Available at https://arxiv.org/abs/2405.17238.
[19] Muhammad Izhar Mehar, Charles Louis Shier, Alana Giambattista, Elgar Gong, Gabrielle Fletcher, Ryan
     Sanayhie, Henry M Kim & Marek Laskowski (2019): Understanding a revolutionary and flawed grand
     experiment in blockchain: the DAO attack. Journal of Cases on Information Technology (JCIT) 21(1), pp.
     19–32, doi:10.4018/JCIT.2019010102.
[20] Satoshi Nakamoto (2008): Bitcoin: A peer-to-peer electronic cash system.
[21] Introducting O3 and O4-Mini. https://openai.com/index/introducing-o3-and-o4-mini/.
[22] OpenAI Structured Outputs. https://openai.com/index/introducing-structured-outputs-in-the-api/.
[23] Santiago Palladino: The Parity Wallet Hack Explained.               https://blog.openzeppelin.com/
     on-the-parity-wallet-multisig-hack-405a8c12e8f7.
[24] Daejun Park, Yi Zhang, Manasvi Saxena, Philip Daian & Grigore Roşu (2018): A formal verification tool for
     Ethereum VM bytecode. ESEC/FSE 2018, Association for Computing Machinery, New York, NY, USA, p.
     912–915, doi:10.1145/3236024.3264591.
[25] Heidelinde Rameder, Monika Di Angelo & Gernot Salzer (2022): Review of automated vulnerability analysis
     of smart contracts on Ethereum. Frontiers in Blockchain 5, p. 814977, doi:10.3389/fbloc.2022.814977.s001.
[26] Remix IDE. https://remix-ide.readthedocs.io/en/latest/.
[27] Grigore Roşu & Traian Şerbănuţă (2010): An Overview of the K Semantic Framework. The Journal of Logic
     and Algebraic Programming 79, p. 397–434, doi:10.1016/j.jlap.2010.03.012.
[28] Jonas Schiffl, Matthias Grundmann, Marc Leinweber, Oliver Stengele, Sebastian Friebe & Bernhard Beckert
     (2021): Towards Correct Smart Contracts: A Case Study on Formal Verification of Access Control. In:
     Proceedings of the 26th ACM Symposium on Access Control Models and Technologies, SACMAT ’21,
     Association for Computing Machinery, New York, NY, USA, p. 125–130, doi:10.1145/3450569.3463574.
[29] Nipun Sharma, Swati Sharma et al. (2022): A survey of Mythril, a smart contract security analysis tool for
     EVM bytecode. Indian Journal of Natural Sciences 13(75), pp. 51003–51010.
[30] Solhint — An open source project for linting Solidity code. https://protofire.github.io/solhint/.
[31] Solidity documentation. https://docs.soliditylang.org/en/v0.8.29/. Accessed: 2025-06-15.
[32] Stefan-Claudiu Susan (2024): Leveraging Slither and Interval Analysis to build a Static Analysis Tool. Elec-
     tronic Proceedings in Theoretical Computer Science 410, p. 150–166, doi:10.4204/eptcs.410.10.
[33] Stefan-Claudiu Susan, Andrei Arusoaie & Dorel Lucanu (2025): Evaluating the Effectiveness of LLMs for
     Static Analysis: A Smart Contracts Case Study. Submitted.
[34] Ştefan-Claudiu Susan & Andrei Arusoaie (2023): Identifying Vulnerabilities in Smart Contracts us-
     ing Interval Analysis. Electronic Proceedings in Theoretical Computer Science 389, p. 144–151,
     doi:10.4204/eptcs.389.12.
[35] SWC Registry. https://swcregistry.io/.
[36] Nick Szabo (1996): Smart contracts: building blocks for digital markets. EXTROPY: The Journal of Tran-
     shumanist Thought,(16) 18(2), p. 28.
[37] Petar Tsankov, Andrei Dan, Dana Drachsler-Cohen, Arthur Gervais, Florian Buenzli & Martin Vechev
     (2018): Securify: Practical security analysis of smart contracts. In: Proceedings of the 2018 ACM SIGSAC
     Conference on Computer and Communications Security, pp. 67–82, doi:10.1145/3243734.3243780.
116                                                                      Proving Solidity Code Defects


[38] Zhiyuan Wei, Jing Sun, Zijiang Zhang, Xianhao Zhang, Meng Li & Zhe Hou (2024): LLM-
     SmartAudit: Advanced Smart Contract Vulnerability Detection. arXiv preprint arXiv:2410.09381,
     doi:10.48550/arXiv.2410.09381.
[39] Gavin Wood et al. (2014): Ethereum: A secure decentralised generalised transaction ledger. Ethereum
     project yellow paper 151(2014), pp. 1–32.
[40] ZeKe Xiao, Qin Wang, Hammond Pearce & Shiping Chen (2025): Logic meets magic: Llms cracking smart
     contract vulnerabilities. arXiv preprint arXiv:2501.07058, doi:10.48550/arXiv.2501.07058.
