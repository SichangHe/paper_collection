                                                Formal Specification and Verification of Smart
                                                       Contracts in Azure Blockchain
                                                    Yuepeng Wang                  Shuvendu K. Lahiri               Shuo Chen                        Rong Pan
                                             University of Texas at Austin         Microsoft Research            Microsoft Research       University of Texas at Austin
                                                ypwang@cs.utexas.edu            shuvendu@microsoft.com        shuochen@microsoft.com          rpan@cs.utexas.edu

                                                            Isil Dillig                              Cody Born                        Immad Naseer
                                                  University of Texas at Austin                   Microsoft Azure                   Microsoft Azure
                                                       isil@cs.utexas.edu                      coborn@microsoft.com              imnaseer@microsoft.com
arXiv:1812.08829v2 [cs.PL] 29 Apr 2019




                                            Abstract—Ensuring correctness of smart contracts is           of the forks back to the state before the incident. However,
                                         paramount to ensuring trust in blockchain-based systems. This    this remedy itself is devastating as it defeats the core values
                                         paper studies the safety and security of smart contracts in      of blockchain, such as immutability, decentralized trust, and
                                         the Azure Blockchain Workbench, an enterprise Blockchain-as-
                                         a-Service offering from Microsoft. As part of this study, we     self-governance. This situation leaves no options for smart
                                         formalize semantic conformance of smart contracts against a      contract programmers other than writing correct code to start
                                         state machine model with access-control policy and develop a     with.
                                         highly-automated formal verifier for Solidity that can produce      Motivated by the serious consequences of bugs in smart
                                         proofs as well as counterexamples. We have applied our verifier  contract code, recent work has studied many types of security
                                         V ERI S OL to analyze all contracts shipped with the Azure
                                         Blockchain Workbench, which includes application samples as      bugs such as reentrancy, integer underflow/overflow, and issues
                                         well as a governance contract for Proof of Authority (PoA).      related to delegatecalls on Ethereum. While these low-level
                                         We have found previously unknown bugs in these published         bugs have drawn much attention due to high-visibility incidents
                                         smart contracts. After fixing these bugs, V ERI S OL was able to on public blockchains, we believe that the BaaS infrastructure
                                         successfully perform full verification for all of these contracts.
                                                                                                          and enterprise scenarios bring a set of interesting, yet less
                                                                                                          well-studied security problems.
                                                                I. I NTRODUCTION
                                                                                                             In this paper, we present our research on smart contract
                                            As a decentralized and distributed consensus protocol to correctness in the context of Azure Blockchain, a BaaS solution
                                         maintain and secure a shared ledger, the blockchain is seen as offered by Microsoft [3]. Specifically, we focus on a cloud
                                         a disruptive technology with far-reaching impact on diverse service named Azure Blockchain Workbench (or Workbench
                                         areas. As a result, major cloud platform companies, including for short) [6], [7]. The Workbench allows an enterprise
                                         Microsoft, IBM, Amazon, SAP, and Oracle, are offering customer to easily build and deploy a smart contract application
                                         Blockchain-as-a-Service (BaaS) solutions, primarily targeting integrating active directory, database, web UI, blob storage, etc.
                                         enterprise scenarios, such as financial services, supply chains, A customer implements the smart contract application (that
                                         escrow, and consortium governance. A recent study by Gartner meets the requirements specified in an application policy) and
                                         predicts that the business value-add of the blockchain has the uploads it onto the Workbench. The code is then deployed
                                         potential to exceed $3.1 trillion by 2030 [16].                  to the underlying blockchain ledger to function as an end-to-
                                            Programs running on the blockchain are known as smart end application. In addition to customer (application) smart
                                         contracts. The popular Ethereum blockchain provides a low- contracts, the Workbench system itself is comprised of smart
                                         level stack-based bytecode language that executes on top of contracts that customize the underlying distributed blockchain
                                         the Ethereum Virtual Machine (EVM). High-level languages consensus protocols. Workbench ships one such smart contract
                                         such as Solidity and Serpent have been developed to enable for the governance of the Ethereum blockchain that uses the
                                         traditional application developers to author smart contracts. Proof-of-Authority (PoA) consensus protocol for validating
                                         However, because blockchain transactions are immutable, bugs transactions. Workbench relies on the correctness of the PoA
                                         in smart contract code have devastating consequences, and governance contract to offer a trusted blockchain on Azure.
                                         vulnerabilities in smart contracts have resulted in several         Customer contracts in the Workbench architecture implement
                                         high-profile exploits that undermine trust in the underlying complex business logic, starting with a high-level finite-state-
                                         blockchain technology. For example, the infamous TheDAO machine (FSM) workflow policy specified in a JSON file.
                                         exploit [1] resulted in the loss of almost $60 million worth of Intuitively, the workflow describes (a) a set of categories of
                                         Ether, and the Parity Wallet bug caused 169 million USD users called roles, (b) the different states of a contract, and
                                         worth of ether to be locked forever [4]. The only remedy for (c) the set of enabled actions (or functions) at each state
                                         these incidents was to hard-fork the blockchain and revert one restricted to each role. The high-level policy is useful to
design contracts around state machine abstractions as well
                                                                        Application Roles:                   Legend
as specify the required access-control for the actions. While
                                                                         Requestor (REQ)                     TF: Transition Function
these state machines offer powerful abstraction patterns during
                                                                         Responder (RES)                     AR: Allowed Role
smart contract design, it is non-trivial to decide whether a
given smart contract faithfully implements the intended FSM.                                                 AIR: Allowed Instance Role
In this paper, we define semantic conformance checking as
the problem of deciding whether a customer contract correctly                                  TF: SendResponse
implements the underlying workflow policy expressed as an                                           AR: RES
FSM. Given a Workbench policy π that describes the workflow                Request                                         Respond
and a contract C, our approach first constructs a new contract
C 0 such that C semantically conforms to π if and only if C 0                                   TF: SendRequest
does not fail any assertions.                                                                       AIR: REQ
   In order to automatically check the correctness of the
                                                                         Fig. 1. Workflow policy diagram for HelloBlockchain application.
assertions in a smart contract (such as C 0 or PoA governance),
we develop a new verifier called V ERI S OL for smart contracts
written in Solidity. V ERI S OL is a general-purpose Solidity                                     II. OVERVIEW
verifier and is not tied to Workbench. The verifier encodes the
semantics of Solidity programs into a low-level intermediate          In this section, we give an example of a Workbench
verification language Boogie and leverages the well-engineered      application policy for a sample contract and describe our
Boogie verification pipeline [14] for both verification and         approach for semantic conformance checking between the
counter-example generation. In particular, V ERI S OL takes ad-     contract and the policy.
vantage of existing bounded model checking tool C ORRAL [24]
                                                                    A. Workbench Application Policy
for Boogie to generate witnesses to assertion violations, and it
leverages practical verification condition generators for Boogie       Workbench requires every customer to provide a policy (or
to automate correctness proofs. In addition, V ERI S OL uses        model) representing the high-level workflow of the application
monomial predicate abstraction [17], [22] to automatically          in a JSON file1 . The policy consists of several attributes such as
infer so-called contract invariants, which we have found to be      the application name and description, a set of roles, as well as
crucial for automatic verification of semantic conformance.         a set of workflows. For example, Figure 1 provides an informal
   To evaluate the effectiveness and efficiency of V ERI S OL, we   pictorial representation of the policy for a simple application
have performed an experiment on all 11 sample applications          called HelloBlockchain. 2 . The application consists of two
that are shipped with the Workbench, as well as the PoA             global roles (see “Application Roles”), namely R EQUESTOR
governance contract for the blockchain itself. V ERI S OL finds 4   and R ESPONDER. Informally, each role represents a set of
previously unknown defects in these published smart contracts,      user addresses and provides access control or permissions for
all of which have been confirmed as true bugs by the developers     various actions exposed by the application. We distinguish a
(many of them fixed at the time of writing). The experimental       global role from an instance role in that the latter applies to a
results also demonstrate the practicality of V ERI S OL in that     specific instance of the workflow. It is expected that the instance
it can perform full verification of all the fixed contracts with    roles are always a subset of the user addresses associated with
modest effort; most notably, V ERI S OL can automatically verify    the global role.
10 out of 11 of the fixed versions of sample smart contracts           As illustrated in Figure 1, the simple HelloBlockchain
within 1.7 seconds on average.                                      application consists of a single workflow with two states,
                                                                    namely Request and Respond. The data members (or fields)
Contributions. This paper makes the following contributions:        include instance role members (Requestor and Responder)
1) We study the safety and security of smart contracts present      that range over user addresses. The workflow consists of two
   in Workbench, a BaaS offering.                                   actions (or functions) in addition to the constructor function,
2) We formalize the Workbench application policy language           SendRequest and SendResponse, both of which take a string
   and define the semantic conformance checking problem             as argument.
   between a contract and a policy.                                    A transition in the workflow consists of a start state, an
3) We develop a new formal verifier V ERI S OL for smart            action or function, an access control list, and a set of successor
   contracts written in Solidity.                                   states. Figure 1 describes two transitions, one from each of the
4) We perform an evaluation of V ERI S OL on all the contracts      two states. For example, the application can transition from
   shipped with Workbench. This includes all the application        Request to Respond if a user belongs to the R ESPONDER role
   samples as well as the highly-trusted PoA governance                1 https://docs.microsoft.com/en-us/azure/blockchain/workbench/
   contract.                                                        configuration
5) We report previously unknown bugs that have been con-               2 The example related details can be found on the associated web page: https:

   firmed and several already fixed.                                //github.com/Azure-Samples/blockchain/tree/master/blockchain-workbench/
                                                                    application-and-smart-contract-samples/hello-blockchain
(AR) and invokes the action SendResponse. An “Application               The Workbench service allows a user to upload the policy, the
Instance Role” (AIR) refers to an instance role data member          Solidity code, and optionally add users and perform various
of the workflow that stores a member of a global role (such          actions permitted by the configuration. Although the smart
as Requestor). For instance, the transition from Respond to          contract drives the application, the policy is used to expose
Request in Figure 1 uses an AIR and is only allowed if the           the set of enabled actions at each state for a given user.
user address matches the value stored in the instance data           Discrepancies between the policy and Solidity code can lead
variable Requestor.                                                  to unexpected state transitions that do not conform to the high-
                                                                     level policy. To ensure the correct functioning and security of
                                                                     the application, it is crucial to verify that the Solidity program
pragma solidity ^0.4.20;
                                                                     semantically conforms to the intended meaning of the policy
contract HelloBlockchain {                                           configuration.
     // Set of States
    enum StateType {Request , Respond }
                                                                     C. Semantic Conformance Verification
     // List of properties
     StateType public State ;                                           Given the application policy and a smart contract, we
                                                                     define the problem of semantic conformance between the
     address public Requestor ;
     address public Responder ;                                      two that ensures that the smart contract respects the policy
     string public RequestMessage ;                                  (Section III-B). Moreover, we reduce the semantic conformance
     string public ResponseMessage ;
     // constructor function                                         verification problem to checking assertions on an instrumented
     function HelloBlockchain ( string message )                     Solidity program. For the HelloBlockchain application, the
                                 constructor_checker()
                                 public
                                                                     instrumentation is provided by adding the underlined modifier
     {                                                               invocations in Figure 2. A modifier is a Solidity language
          Requestor = msg. sender ;
          RequestMessage = message ;
                                                                     construct that allows wrapping a function invocation with code
          State = StateType . Request ;                              that executes before and after the execution.
     }
     // call this function to send a request
     function SendRequest ( string requestMessage )                     function nondet () returns (bool ); // no definition
                            SendRequest_checker() public
     {                                                                   // Checker modifiers
          RequestMessage = requestMessage ;                              modifier constructor_checker ()
          State = StateType . Request ;                                  {
     }                                                                      _;
     // call this function to send a response                              assert ( nondet () /* global role REQUESTOR */
     function SendResponse ( string responseMessage )                                   ==> State == StateType . Request );
                            SendResponse_checker() public                }
     {                                                                   modifier SendRequest_checker ()
          Responder = msg. sender ;                                      {
          ResponseMessage = responseMessage ;                              StateType oldState = State ;
          State = StateType . Respond ;                                    address oldRequestor = Requestor ;
     }                                                                      _;
     <modifier definitions>                                                assert (( msg. sender == oldRequestor &&
 }                                                                                   oldState == StateType . Respond )
                                                                                    ==> State == StateType . Request );
        Fig. 2. Solidity contract for HelloBlockchain application.       }
                                                                         modifier SendResponse_checker ()
                                                                         {
                                                                           StateType oldState = State ;
                                                                            _;
B. Workbench Application Smart Contract                                    assert (( nondet () /* global role RESPONDER */ &&
                                                                                     oldState == StateType . Request )
   After specifying the application policy, a user provides a                       ==> State == StateType . Respond );
                                                                         }
smart contract for the appropriate blockchain ledger to imple-
ment the workflow. Currently, Workbench supports the popular Fig. 3. Modifier definitions for instrumented HelloBlockchain application.
language Solidity for targeting applications on Ethereum.
Figure 2 describes a Solidity smart contract that implements        Figure 3 shows the definition of the modifiers used to
the HelloBlockchain workflow in the HelloBlockchain instrument for conformance checking. Intuitively, we wrap
application. For the purpose of this sub-section, we start by the constructor and functions with checks to ensure that they
ignoring the portions of the code that are underlined. The implement the FSM state transitions correctly. For example,
contract declares the data members present in the configuration if the FSM transitions from a state s1 to a state s2 upon the
as state variables with suitable types. Each contract implement- invocation of function f by a user with access control ac, then
ing a workflow defines an additional state variable State to we instrument the definition of f to ensure that any execution
track the current state of a workflow. The contract consists of starting in s1 with access control satisfying ac should transition
the constructor function along with the two functions defined to s2 .
in the policy, with matching signatures. The functions set the      Finally, given the instrumented Solidity program, we dis-
state variables and update the state variables appropriately to charge the assertions statically using a new formal verifier for
reflect the state transitions.                                   Solidity called V ERI S OL. The verifier can find counterexamples
(in the form of a sequence of transactions involving calls to the    B. Semantic Conformance
constructor and public methods) as well as automatically con-           Given a contract C and a Workbench Application policy
struct proofs of semantic conformance. Note that, even though        π, semantic conformance between C and π requires that the
the simple HelloBlockchain example does not contain any              contract C faithfully implements the policy specified by π. In
unbounded loops or recursion, verifying semantic conformance         this subsection, we first define some syntactic requirements on
still requires reasoning about executions that involve unbounded     the contract, and then formalize what we mean by semantic
numbers of calls to the two public functions. We demonstrate         conformance between a contract and a policy.
that V ERI S OL is able to find deep violations of the conformance
property for well-tested Workbench applications, as well             Syntactic conformance. Given a client contract C and a policy
as automatically construct inductive proofs for most of the          π = (R, W), our syntactic conformance requirement stipulates
application samples shipped with Workbench.                          that the contract for each w ∈ W implements all the instance
                                                                     state variables as well as definitions for each of the functions.
                                                                     Additionally, each contract function has a parameter called
      III. S EMANTIC C ONFORMANCE C HECKING FOR                      sender , which is a blockchain address that denotes the user or
                 W ORKBENCH P OLICIES                                contract invoking this function. Finally, each contract should
                                                                     contain a state variable sw that ranges over Sw , for each
   In this section, we formalize the Workbench application
                                                                     w ∈ W.
policy that we informally introduced in Section II. Our formal-
ization can be seen as a mathematical representation of the          Semantic conformance. We formalize the semantic conformance
official Workbench application JSON schema documentation.            requirement for smart contracts using Floyd-Hoare triples of
                                                                     the form {φ} S {ψ} indicating that any execution of statement
A. Formalization of Workbench Application Policies                   S starting in a state satisfying φ results in a state satisfying
                                                                     ψ (if the execution of S terminates). We can define semantic
   The Workbench policy for an application allows the user to        conformance between a contract C and a policy π as a set of
describe (i) the data members and actions of an application,         Hoare triples, one for each pair (m, s) where m is a method
(ii) a high-level state-machine view of the application, and (iii)   in the contract and s is a state in the Workbench policy. At a
role-based access control for state transitions. The role-based      high-level, the idea is simple: we insist that, when a function is
access control provides security for deploying smart contracts       executed along a transition, the resulting state transition should
in an open and adversarial setting; the high-level state machine     be in accordance with the Workbench policy.
naturally captures the essence of a workflow that progresses            Given an application policy π = (R, W) and workflow
between a set of states based on some actions from the user.         w = hS, s0 , Rw , F, F0 , ac 0 , γi ∈ W, we can formalize this
   More formally, a Workbench Application Policy is a pair           high-level idea by using the following Hoare triples:
(R, W) where R is a set of global roles used for access              1) Initiation.
control, and W is a set of workflows defining a kind of finite
state machine. Specifically, a workflow is defined by a tuple                  {sender ∈ ac 0 } F0 (v1 , . . . , vk ) {sw = s0 }
hS, s0 , Rw , F, F0 , ac 0 , γi where:
                                                                        The Hoare triple states that the creation of an instance of
• S is a finite set of states, and s0 ∈ S is an initial state           the workflow with the appropriate access control ac 0 results
• Rw is a finite set of instance roles of the form (id : t),            in establishing the initial state.
  where id is an identifier and t is a role drawn from R             2) Consecution. Let τ = (s1 , f, ac , S2 ) be a transition in
• F(id 0 , . . . , id k ) is a set of actions (functions), with F0      γ. Then, for each such transition, semantic conformance
  denoting an initial action (constructor)                              requires the following Hoare triple to be valid:
• ac 0 ⊆ R is the initiator role for restricting users that can
  create an instance of the contract                                       {sender ∈ ac ∧ sw = s1 } f(v1 , . . . , vk ) {sw ∈ S2 }
                                     S
• γ ⊆ S × F × (Rw ∪ R) × 2 is a set of transitions. Given
                                                                        Here, the precondition checks two facts: First, the sender
  a transition τ = (s, f, ac, S), we write τ.s, τ.f, τ.ac, τ.S to       must satisfy the access control, and, second, the start
  denote s, f, ac, and S respectively                                   state must be s1 . The post-condition asserts that the
Intuitively, S defines the different “states” that the contract         implementation of method f in the contract results in a
can be in, and γ describes which state can transition to what           state that is valid according to policy π.
other states by performing certain actions. The transitions are
additionally “guarded” by roles (which can be either global or       C. Instrumentation for Semantic Conformance Checking
instance roles) that qualify which users are allowed to perform         As mentioned in Section II, our approach checks semantic
those actions. As mentioned earlier in Section II, each “role”       conformance of Solidity contracts by (a) instrumenting the
corresponds to a set of users (i.e., addresses on the blockchain).   contract with assertions, and (b) using a verification tool to
The use of instance roles in the workbench policy allows             check that none of the assertions can fail. We explain our
different instances of the contract to authorize different users     instrumentation strategy in this subsection and refer the reader
to perform certain actions.                                          to Section IV for a description of our verification tool chain.
   Our instrumentation methodology heavily relies on the                 call f0 (*);
modifier construct in Solidity. A modifier has syntax very               while (true) {
similar to a function definition in Solidity with a name and                 if (*) call f1 (*);
list of parameters and a body that can refer to parameters and               else if (*) call f2 (*);
globals in scope. The general structure of a modifier definition             ...
                                                                             else if (*) call fn (*);
without any parameters is [2]:                                           }
modifier Foo () {
   pre -stmt;                                                                          Fig. 4. Harness for Solidity contracts
   _;
   post -stmt;
}                                                                       modifier g_checker () {
where pre-stmt and post-stmt are Solidity statements.                      // copy old State
                                                                           StateType oldState = sw ;
When this modifier is applied to a function Bar,                           // copy old instance role vars
function Bar(int x) Foo (){                                                ...
   Bar -stmt;                                                              _;     V
}                                                                          assert   τ ∈γ g (old (P (τ.ac ) ∧ α({τ.s})) ⇒ α(τ.S));
                                                                        }
the Solidity compiler transforms the body of Bar to execute
pre-stmt (respectively, post-stmt) before (respectively, af-         Here, the instrumented code first copies the sw variable
ter) Bar-stmt. This provides a convenient way to inject code      and   all of the variables in Rw into corresponding “old”
at multiple return sites from a procedure and also inject code    copies.   Next, the assertion checks that if the function is
before the execution of the constructor code (since a constructor executed   in a transition τ , then state transitions to one of
may invoke other base class constructors implicitly).             the  successor  states in τ.S. The notation old(e) replaces
   We now define a couple of helper predicates before describ-    any  occurrences   of a state variable (such as sw ) with the
ing the actual checks. Let P (ac ) be a predicate that encodes    “old”  copy  that holds  the value at the entry to the function.
the membership of sender in the set ac :                          Figure  3 shows the modifier definitions for our running example
                                                                  HelloBlockchain described in Section II Although we show
                                                                  the nondet() to highlight the issue of global roles, one can
                       false,             ac = {}
                    
                .
                    
                    
                       msg.sender = q, ac = {q ∈ Rw }             safely replace nondet() with true since the function only
      P (ac ) =                           ac = {r ∈ R}            appears negatively in any assertion. In fact, this observation
                     nondet()
                    
                             1        2            1     2
                       P (ac ) ∨ P (ac ) ac = ac ∪ ac             allows us to add the simplified assertions for runtime checking
                                                                  as well. Finally, since conjunction distributes over assertions,
Here nondet is a side-effect free Solidity function that returns
                                                                  we can replace the single assertion with an assertion for each
a non-deterministic Boolean value at each invocation. For the
                                                                  transition in the implementation.
sake of static verification, one can declare a function without
any definition. This allows us to model the membership check               IV. F ORMAL V ERIFICATION USING V ERI S OL
sender ∈ ac conservatively in the absence of global roles on         In this section, we present our formal verifier called
the blockchain.                                                   V ERI S OL for checking the correctness of assertions in Solidity
   Next, we define a predicate for membership of a contract smart contracts. Since our verifier is built on top of the
state in a set of states S 0 ⊆ S using α(S 0 ) as follows:        Boogie tool chain, it can be used for both verification and
                                                                        counterexample generation.
                      
                       false,              S 0 = {}
                 .
        α(S )0
                 =      sw = s,             S 0 = {s ∈ S}
                       α(S ) ∨ α(S ),      S 0 = S1 ∪ S2
                                                                        A. General Methodology
                            1      2
                                                                           Let C = {λx~0 .f0 , λx~1 .f1 , . . . , λx~n .fn } be a smart
   We can now use these predicates to define the source code            contract annotated with assertions where:
transformations below:
                                                                           • λx~0 .f0 is the constructor
Constructor. We add the following modifier to constructors:                • λx~i .fi for i ∈ [1, n] are public functions
modifier constructor_checker () {                                       Our verification methodology is based on finding a contract
   _;                                                                   invariant I satisfying the following Hoare triples:
   assert (P (ac 0 ) ⇒ α({s0 }));
}                                                                                             |= {true} f0 {I}                      (1)
Here, the assertion ensures that the constructor sets up the                           |= {I} fi {I} for all i ∈ [1, n]             (2)
correct initial state when executed by a user with access control
                                                                           Here, the first condition states the contract invariant is
ac 0 .
                                                                        established by the constructor, and the second condition states
                                                   .
Other functions. For a function g, let γ g = {τ ∈ γ | τ =               that I is inductive — i.e., it is preserved by every public
(s1 , g, ac , S2 )} be the set of all transitions where g is invoked.   function in C. Note that such a contract invariant suffices to
                  VeriSol                     Invariant                           ct ∈ ContractNames
                                             Generation        Fully Veriﬁed      et ∈ SolElemTypes            ::= integer | string | address
                          Boogie                                                  st ∈ SolTypes                ::= et | ct | et ⇒ st
Smart Contract          Translation                           Veriﬁed Up To
with Assertions                               Bounded         K Transactions    se ∈ SolExprs ::= c | x | op(se, . . . , se) | se[se]
                                               Model
                                              Checking                                           | msg.sender | x.length
                                                              Counterexample    sst ∈ SolStmts ::= x := se | x[se] . . . [se] := y | sst; sst
                                                                                                 | require(se) | assert(se)
                                                                                                 | if (se) {sst} else {sst}
                  Fig. 5. Schematic workflow of V ERI S OL.
                                                                                                 | while (se) do {sst} | x.push(se)
                                                                                                 | se := f(se)
                                                                                                            ~ | se := se.f(se)  ~
                                                                                                 | se := new C(se)
                                                                                                                 ~ | se := new t[](se)
establish the validity of all assertions in the contract under
                                                                                                 | se := new (t1 ⇒ t2 ⇒ . . . ⇒ tk ⇒ t)()
any possible sequence of function invocations of the contract.
To see why this is the case, consider a “harness” that invokes
the functions in C as in Figure 4. This harness first creates                  Fig. 6. A subset of Solidity language. C denotes a contract name, t denotes
                                                                               an elementary Solidity type, and f denotes a function name.
an instance of the contract by calling the constructor, and
then repeatedly and non-deterministically invokes one of the
public functions of C. Observe that the Hoare triples (1) and
(2) listed above essentially state that I is an inductive invariant            C. Solidity to Boogie Translation
of the loop in this harness; thus, the contract invariant I
overapproximates the state of the contract under any sequence                     In this subsection, we formally describe our translation of
of the contract’s function invocations. Furthermore, when the                  Solidity source code to the Boogie intermediate verification
functions contain assertions, the Hoare triple {I} fi {I} can                  language. We start with a brief description of Solidity and
only be proven if I is strong enough to imply the assertion                    Boogie, and then discuss our translation.
conditions. Thus, the validity of the Hoare triples in (1) and
(2) establishes correctness under all possible usage patterns of Solidity Language. Figure 6 shows a core subset of Solidity
the contract.                                                    that we use for our formalization. At a high level, Solidity is
                                                                 a typed object-oriented programming language with built-in
                                                                 support for basic verification constructs, such as the require
B. Overview                                                      construct for expressing pre-conditions.
                                                                    Types in our core language include integers, strings, contracts,
   We now describe the design of our tool called V ERI S OL for
                                                                 addresses, and mappings. We use the notation τ1 ⇒ τ2 to
checking safety of smart contracts. V ERI S OL is based on the
                                                                 denote a mapping from a value of type τ1 to a value of type
proof methodology outlined in Section IV-A, and its workflow
                                                                 τ2 (where τ2 can be a nested map type). Since arrays can be
is illustrated in Figure 5. At a high-level, V ERI S OL takes as
                                                                 viewed as a special form of mapping integer ⇒ τ , we do not
input a Solidity contract C annotated with assertions and yields
                                                                 introduce a separate array type to simplify presentation.
one of the following three outcomes:
                                                                    As standard, expressions in Solidity include constants, local
• Fully verified: This means that the assertions in C are        variables, state variables (i.e., fields in standard object-oriented
   guaranteed not to fail under any usage scenario.              language terminology), unary/binary operators (denoted op),
• Refuted: This indicates that C was able to find at least one   and array/map lookup e[e0 ]. Given an array x, the expression
   input and invocation sequence of the contract functions under x.length yields the length of that array, and msg.sender
   which one of the assertions is guaranteed to fail.            yields the address of the contract or user that initiates the
• Partially verified: When V ERI S OL can neither verify nor     current function invocation.
   refute contract correctness, it performs bounded verification
                                                                    Statements in our core Solidity language include assignments,
   to establish that the contract is safe up to k transactions.
                                                                 conditional statements, loops, sequential composition, array
   This essentially corresponds to unrolling the ”harness” loop
                                                                 insertion (push), internal and external function calls, contract
   from Figure 4 k times and then verifying that the assertions
                                                                 instance creation, and dynamic allocations. The construct
   do not fail in the unrolled version.
                                                                 require is used to specify the precondition of a function, and
   V ERI S OL consists of three modules, namely (a) Boogie assert checks that its input evaluates to true and terminates
Translation from a Solidity program, (b) Invariant Generation execution otherwise. Solidity differentiates between two types
to infer a contract invariant as well as loop invariants and of function calls: internal and external. An internal call
procedure summaries, and (c) Bounded Model Checking to se := f(se)         ~ invokes the function f and keeps msg.sender
explore assertion failures within all transactions up to a user- unchanged. An external call se := se0 .f(se)   ~ invokes function
specified depth k. In the remaining subsections, we discuss f in the contract instance pointed by se0 (which may include
each of these components in more detail.                         this), and uses this as the msg.sender for the callee.
        bbt ∈ BoogieElemTypes           ::=     int | Ref                                                    v = msg_sender
                                                                              x ∈ LocalVars
        bt ∈ BoogieTypes                ::=     bbt | [bbt]bt                               (Var1)                            (Sender)
                                                                                 ` x ,→ x                   ` msg.sender ,→ v
 e ∈ Exprs ::= c | x | op(e, . . . , e) | uf(e, . . . , e)
              | x[e] . . . [e] | ∀i : bbt :: e                                 Type(c) 6= string                    x ∈ StateVars(C)
                                                                                                 (Const1)                            (Var2)
 st ∈ Stmts ::= skip | havoc x | x := e                                            ` c ,→ c                         ` x ,→ xC [this]
              | x[e] . . . [e] := e
              | assume e | assert e                                                   Type(c) = string c0 = Hash(c)
                                                                                                                    (Const2)
              | call ~x := f(e, . . . , e) | st; st                                          ` c ,→ StrToInt(c0 )
              | if (e) {st} else {st} | while (e) do {st}
                                                                                                    ` x ,→ χ
                                                                                                                     (Len)
                                                                                             ` x.length ,→ Length[χ]
                  Fig. 7. A subset of Boogie language.

                                                                                           ` e1 ,→ χ1 ` e2 ,→ χ2
   We omit several aspects of the language that are desugared                          Type(e2 ) = t1 Type(e1 [e2 ]) = t2
                                                                                                            µ(t )
                                                                                                                                 (Map)
into our core Solidity language. This includes fairly compre-                              ` e1 [e2 ] ,→ Mµ(t12) [χ1 ][χ2 ]
hensive support for modifiers, libraries and structs.
Boogie Language. Since our goal is to translate Solidity                               ` ei ,→ χi i = 1, . . . , n
                                                                                                                                  (Op)
to Boogie, we also give a brief overview of the Boogie                            ` op(e1 , . . . , en ) ,→ op(χ1 , . . . , χn )
intermediate verification language. As shown in Figure 7, Fig. 8. Inference rules for encoding Solidity expressions to Boogie expressions.
types in Boogie include integers (int), references (Ref ), Type(e) is a function that returns the static type of Solidity expression e.
and nested maps. Expressions (Exprs) consist of constants,
variables, arithmetic and logical operators (op), uninterpreted
functions (uf), map lookups, and quantified expressions. to the value stored in its state variable x. Thus, reads from
                                                                                                              C
Standard statements (Stmts) in Boogie consist of skip, variable state variable x are modeled as x [this] in Boogie. Next, we
and array/map assignment, sequential composition, conditional translate string constants in Solidity to Boogie integers using
statements, and loops. The havoc x statement assigns an an uninterpreted function called StrToInt that is applied to a
                                                                                          3
arbitrary value of appropriate type to a variable x. A procedure hash of the string . As mentioned earlier, this string-to-integer
call (call ~x := f(e, . . . , e)) returns a vector of values that translation does not cause imprecision because Solidity only
can be stored in local variables. The assert and assume allows equality checks between variables of type string.
statements behave as no-ops when their arguments evaluate to            Similar to our handling of state variables, our Boogie
true and terminate execution otherwise. An assertion failure is encoding also introduces an array called Length to map each
considered a failing execution, whereas an assumption failure Solidity array to its corresponding length. Thus, a Solidity
blocks.                                                             expression x.length is translated as Length[χ] where χ is
                                                                    the Boogie encoding of x.
From Solidity to Boogie types. We define a function µ :                 The translation of array/map look-up is somewhat more
SolTypes → BoogieTypes that translates a Solidity type to a involved due to potential aliasing issues. First, the basic idea
type in Boogie as follows:                                          is that for each map of type t1 ⇒ t2 , we introduce a Boogie
                                                                                0
                                                                    map Mττ where τ is the Boogie encoding of type t1 (i.e.,
                
                 int,       st ∈ {integer , string}
            .
    µ(st) =         Ref , st ∈ {address} ∪ ContractNames            τ = µ(t1 )) and τ 0 is the Boogie encoding of type t2 (i.e.,
                                 .                                                                        0
                                   et ⇒ st                          τ 0 = µ(t2 )). Intuitively, Mττ maps each array/map object to
                 Ref , st =
                                                                    its contents, which are in turn represented as a map. Thus, we
Specifically, we translate Solidity integers and strings to Boogie                      0
                                                                    can think of Mττ as a two-dimensional mapping where the first
integers; addresses, contract names, and mappings to Boogie
                                                                    dimension is the address of the Solidity map and the second
references. Note that we represent Solidity strings as integers in
                                                                    dimension is the look-up key. For a nested map expression e1
Boogie because Solidity only allows equality checks between
                                                                    of type t1 ⇒ t2 where t2 is a nested map/array, observe that
strings in the core language.                                                                   Ref
                                                                    we look up e1 in Mµ(t           1)
                                                                                                        since maps and arrays in Solidity
From Solidity to Boogie expressions. We present our trans- are dynamically allocated. Intuitively, everything that can be
lation from Solidity to Boogie expressions using judgments dynamically allocated is represented with type Ref in our
of the form ` e ,→ χ in Figure 8, where e is a Solidity encoding to allow for potential aliasing.
expression and χ is the corresponding Boogie expression. While
                                                                    Example 1. Suppose that contract C has a state variable x of
Solidity local variables and the expression msg.sender are
                                                                    Solidity type mapping(int => int[]), which corresponds to
mapped directly into Boogie local variables and parameters
                                                                    the type int => (int => int) in our core Solidity language.
respectively, state variables in Solidity are translated into array
lookups. Specifically, for each state variable x for contract          3 We assume that the hash function is collision-free. In our implementation,
C, we introduce a mapping xC from contract instances o we enforce this by keeping a mapping from each string constant to a counter.
The expression x[0][1] will be translated into the Boogie               is translated into the following Boogie code:
              int                    Ref
expression Mint   [e][1] where e is Mint [ xC [this] ][0] using     1    call v := New (); assume Length [v] = 0;
                                                                                                 Ref
the rules from Figure 8.                                            2    assume ∀i :: Length [Mint   [v][i]] = 0;
                                                                                                 Ref
                                                                    3    assume ∀i :: ¬Alloc [Mint   [v][i]];
                                                                    4    call NewUnbounded ();
From Solidity to Boogie statements. Figure 9 presents the           5
                                                                                                Ref
                                                                         assume ∀i :: Alloc [Mint [v][i]];
                                                                                                   Ref            Ref
translation from Solidity to Boogie statements using judgments      6    assume ∀i,j :: i=j ∨ Mint     [v][i] 6= Mint [v][j];
                                                                                           int   Ref
                                                                    7    assume ∀i,j :: Mint   [Mint [v][i]][j] = 0;
of the form ` s        ω indicating that Solidity statement s       8    xC [this] := v;
is translated to Boogie statement(s) ω. Since most rules in
Figure 9 are self-explanatory, we only explain our translation     First of all, we allocate a fresh reference v and initialize the
for assignments, function calls, and dynamic allocations.          length of v and every inner map v[i] to zero (lines 1 - 2).
                                                                   Second, we allocate fresh references for every inner map v[i]
Function calls. Functions in Solidity have two implicit parame- (lines 3 - 5), and ensure the references of inner maps v[i]
ters, namely this for the receiver object and msg.sender for and v[j] do not alias if i 6= j (line 6). Finally, we initialize
the Blockchain address of the caller. Thus, when translating every element v[i][j] to zero and assign reference v to the state
Solidity calls to their corresponding Boogie version, we variable x (lines 7 - 8).
explicitly pass these parameters in the Boogie version. However,
                                                                   D. Invariant Generation
recall that the value of the implicit msg.sender parameter
varies depending on whether the call is external or internal. For     As mentioned earlier, translating Solidity code into Boogie al-
internal calls, msg.sender remains unchanged, whereas for lows V ERI S OL to leverage the existing ecosystem around Boo-
external calls, msg.sender becomes the current receiver object. gie, including efficient verification condition generation [25].
For both types of calls, our translation introduces a conditional However, in order to completely automate verification (even
statement to deal with dynamic dispatch. Specifically, our for loop and recursion-free contracts), we still need to infer
Boogie encoding introduces a map τ to store the dynamic type a suitable contract invariant as discussed in Section IV-B.
of receiver objects at allocation sites, and the translation of Specifically, recall that the contract invariant must satisfy the
function calls invokes the correct version of the method based following two properties:
on the content of τ for the receiver object.                         1) |= {true} f0 {I}
                                                                     2) |= {I} fi {I} for all i ∈ [1, n]
Dynamic allocation. Dynamic memory allocations in Solidity
                                                                      V ERI S OL uses monomial predicate abstraction ( [17], [22],
are translated into Boogie code with the aid of a helper
                                                                   [23]) to automatically infer contract invariants satisfying the
procedure New (shown in Figure 10) which always returns a
                                                                   above properties. Specifically, the contract invariant inference
fresh reference. As shown in Figure 10, the New procedure is
                                                                   algorithm conjectures the conjunction of all candidate predi-
implemented using a global map Alloc to indicate whether
                                                                   cates as an inductive invariant and progressively weakens it
a reference is allocated or not. All three types of dynamic
                                                                   based on failure to prove a candidate predicate inductive. This
memory allocation (contract, array, and map) use this helper
                                                                   algorithm converges fairly fast even on large examples but
New procedure to generate Boogie code.
                                                                   relies on starting with a superset of necessary predicates. In
   In the case of contract creation (labeled NewCont in
                                                                   the current implementation of V ERI S OL, we obtain candidate
Figure 9), the Boogie code we generate updates the τ map
                                                                   invariants by instantiating the predicate template e1 ./ e2 where
mentioned previously in addition to allocating new memory.
                                                                   ./ is either equality or disequality. Here, expressions e1 , e2
Specifically, given the freshly allocated reference v returned by
                                                                   can be instantiated with variables corresponding to roles and
New, we initialize τ [v] to be C and also call C’s constructor
                                                                   states in the Workbench policy as well as constants. We have
as required by Solidity semantics.
                                                                   found these candidate predicates to be sufficiently general for
   Next, let us consider the allocation of array objects described
                                                                   automatically verifying semantic conformance of Workbench
in rule NewArr in Figure 9. Recall that our Boogie encoding
                                                                   contracts; however, additional predicates may be required for
uses a map called Length to keep track of the size of
                                                                   other types of contracts.
every array. Thus, in addition to allocating new memory, the
translation of array allocation also updates the Length array E. Bounded Model Checking
and initializes all elements in the array to be zero (or null).       If V ERI S OL fails to verify contract correctness using
   Finally, the rule NewMap shows how to translate map alloca- monomial predicate abstraction, it employs an assertion-
tions in Solidity to Boogie using an auxiliary Boogie procedure directed bounded verifier, namely C ORRAL [24], to look
called MapInit (shown in Figure 10) for map initialization. for a transaction sequence leading to an assertion violation.
Given an n-dimensional map, the MapInit procedure iteratively C ORRAL analyzes the harness in Figure 4 by unrolling the
allocates lower dimensional maps and ensures that values loop k times and uses a combination of abstraction refinement
stored in the map do not alias each other as well as any techniques (including lazy inlining of nested procedures) to
other previously allocated reference.                              look for counterexamples in a scalable manner. Thus, when
Example 2. The Solidity code                                       V ERI S OL fails to verify the property, it either successfully finds
                                                                   a counterexample or verifies the lack of any counterexample
              x := new (int => int => int)()                       with k transactions.
                ` e1 ,→ χ1            ` e2 ,→ χ2                                  ` e ,→ χ                                           ` e ,→ χ
                                                 (Asgn)                                            (Req)                                              (Asrt)
                 ` e1 := e2            χ1 := χ2                           ` require(e)    assume χ                            ` assert(e)    assert χ

                  ` e ,→ χ ` s1      ω1 ` s2      ω2                                                                    ` e ,→ χ      `s   ω
                                                              (Cond)                                                                                   (Loop)
           ` if (e) {s1 } else {s2 }  if (χ) {ω1 } else {ω2 }                                                 ` while (e) do {s}      while (χ) do {ω}

                     ` er ,→ χr ` ei ,→ χi i = 0, . . . , n fresh v Cj <: Type(this) j = 1, . . . , m
                 ω ≡ if (τ [this] = C1 ) {call v := f C1 (this, χ1 , . . . , χn , msg_sender); χr := v} else if . . .
                     else if (τ [this] = Cm ) {call v := f Cm (this, χ1 , . . . , χn , msg_sender); χr := v}
                                                                                                                                                         (IntCall)
                                                  ` er := f (e1 , . . . , en )    ω

                            ` er ,→ χr ` ei ,→ χi i = 0, . . . , n fresh v Cj <: Type(e0 ) j = 1, . . . , m
                           ω ≡ if (τ [χ0 ] = C1 ) {call v := f C1 (χ0 , χ1 , . . . , χn , this); χr := v} else if . . .
                                  else if (τ [χ0 ] = Cm ) {call v := f Cm (χ0 , χ1 , . . . , χn , this); χr := v}
                                                                                                                                                  (ExtCall)
                                                       ` er := e0 .f (e1 , . . . , en )   ω

                                          ` er ,→ χr ` ei ,→ χi i = 1, . . . , n fresh v
                           ω ≡ call v := New(); assume τ [v] = C; call f0C (v, χ1 , . . . , χn , this); χr := v
                                                                                                                (NewCont)
                                                  ` er := new C(e1 , . . . , en ) ω

                                                                               ` er ,→ χr ` e ,→ χ fresh v ` v[i] ,→ χi
     ` x[x.Length++] := e                     ω
                                                  (Push)           ω ≡ call v := New(); Length[v] := χ; assume ∀i :: χi = 0; χr := v
          ` x.push(e)   ω                                                                                                            (NewArr)
                                                                                         ` er := new t[](e) ω

       ` s1            ω1                                          ` er ,→ χr fresh v ` v[i1 ] . . . [in ] ,→ χ
       ` s2            ω2                         ω ≡ call v := New(); call MapInit(v, n); assume ∀i1 , . . . , in :: χ = 0; χr := v
                               (Seq)                                                                                                 (NewMap)
    ` s1 ; s2          ω1 ; ω2                                       ` er := new (t1 ⇒ . . . ⇒ tn ⇒ t)()     ω
Fig. 9. Inference rules for encoding Solidity statements to Boogie statements. Type(e) is a function that returns the static type of Solidity expression e. Symbol
f C denotes the function f in contract C, and f0C denotes the constructor of contract C. The <: relation represents the sub-typing relationship. τ is a global
Boogie map that maps receiver objects to their dynamic types. Types for universally quantified Boogie variables are omitted for brevity.



var Alloc: [Ref]bool;                                                                                  properties for the PoA governance contract. The goal of our
procedure New () returns (ret: Ref) {                                                                  evaluation is to answer the following research questions:
  havoc ret; assume (! Alloc [ret ]);
  Alloc[ret] := true;                                                                                  RQ1 How does V ERI S OL perform when checking semantic
}                                                                                                            conformance of Workbench application policies?
procedure NewUnbounded () {
  var oldAlloc : [Ref]bool;                                                                            RQ2 How applicable is V ERI S OL on smart contracts with
  oldAlloc := Alloc ; havoc Alloc ;                                                                          complex data structures (such as PoA)?
  assume ∀i:: oldAlloc [i] ==> Alloc [i];
}
procedure MapInit (v: Ref , n: int) {                                                                  Experimental Setup. Due to limited resources, we set our
  var j: int; j := 1; Length [v] := 0;                                                                 timeout as one hour for every benchmark. All experiments
  while (j < n) {
    assume ∀i1 , . . . , ij :: Length [χ(v, i1 , . . . , ij )]=0;                                      are conducted on a machine with Intel Xeon(R) E5-1620 v3
    assume ∀i1 , . . . , ij ::¬Alloc [χ(v, i1 , . . . , ij )];                                         CPU and 32GB of physical memory, running the Ubuntu 14.04
    call NewUnbounded ();
    assume ∀i1 , . . . , ij :: Alloc [χ(v, i1 , . . . , ij )];                                         operating system.
    assume ∀i1 , . . . , ij , i0j ::(ij = i0j ) ∨ χ(v, i1 , . . . , ij ) 6= χ(v, i1 , . . . , i0j );
    j := j + 1; }                                                                                      A. Semantic Conformance for Workbench Application Policies
}

Fig. 10. Auxiliary Boogie procedures. The term χ(v, i1 , . . . , ij ) denotes the                      Benchmarks. We have collected all sample smart contracts that
translation result of Solidity expression v[i1 ] . . . [ij ]. Types for universally                    are shipped with Workbench and their corresponding applica-
quantified Boogie variables are omitted for brevity.
                                                                                                       tion policies on the Github repository of Azure Blockchain [5].
                                                                                                       These smart contracts and their policies depict various workflow
                                   V. E VALUATION
                                                                                                       scenarios that are representative in real-world enterprise use
   We evaluate the effectiveness and efficiency of V ERI S OL                                          cases. The smart contracts exercise various features of Solidity
by performing two sets of experiments on smart contracts                                               such as arrays, nested contract creation, external calls, enum
shipped with Workbench: (i) semantic conformance checking                                              types, and mutual-recursion. For each smart contract C and its
for Workbench samples, and (ii) checking safety and security                                           application policy π, we perform program instrumentation as
                                                                TABLE I
                      E XPERIMENTAL R ESULTS OF S EMANTIC C ONFORMANCE AGAINST W ORKBENCH A PPLICATION P OLICIES .

                                                                           Orig      Inst
        Name            Description                                                           Init Status        Status after Fix       Time (s)
                                                                          SLOC      SLOC
    AssetTransfer       Selling high-value assets                          192       444        Refuted            Fully Verified          2.1
   BasicProvenance      Keeping record of ownership                         43        95     Fully Verified        Fully Verified          1.5
  BazaarItemListing     Multiple workflow scenario for selling items        98       175        Refuted            Fully Verified          2.3
  DefectCompCounter     Product counting using arrays for manufacturers     31        68     Fully Verified        Fully Verified          1.3
    DigitalLocker       Sharing digitally locked files                     129       260        Refuted            Fully Verified          1.7
  FreqFlyerRewards      Calculating frequent flyer rewards using arrays     47        90     Fully Verified        Fully Verified          1.3
   HelloBlockchain      Request and response (Figure 1)                     32        78     Fully Verified        Fully Verified          1.3
    PingPongGame        Multiple workflow for two-player games              74       136        Refuted       Fully Verified (manual)      2.1
   RefrigTransport      Provenance scenario with IoT monitoring            118       187     Fully Verified        Fully Verified          2.2
   RoomThermostat       Thermostat installation and use                     42        99     Fully Verified        Fully Verified          1.3
  SimpleMarketplace     Owner and buyer transactions                        62       118     Fully Verified        Fully Verified          1.4
       Average          -                                                   79       159           -                      -                1.7



explained in Section III-C to obtain contract C 0 . Note that no          function Accept () public
assertion failure of C 0 is equivalent to the semantic conformance        {
                                                                            if (msg. sender != InstanceBuyer &&
between C and π, so we include such instrumented smart                           msg. sender != InstanceOwner ) {
contracts in our benchmark set.                                                 revert ();
                                                                            }
                                                                            ...
Main Results. Table I summarizes the results of our first
experimental evaluation. Here, the “Name” column gives the                    if (msg. sender == InstanceBuyer ) {
                                                                                  ...
name of the contract, and the “Description” column describes                  }
the contract’s usage scenario. The next two columns give                      else {
                                                                                  // msg. sender has to be InstanceOwner
the number of lines of Solidity code before and after the                         // from the revert earlier
instrumentation described in Section III-C. The last three                        if ( State == StateType . NotionalAcceptance ) {
                                                                                      State = StateType . SellerAccepted ;
columns present the main verification results: In particular,                     }
“Init Status” shows the result of applying V ERI S OL on the                      else if ( State == StateType . BuyerAccepted ) {
                                                                                      // NON - CONFORMANCE : JSON transitions
original smart contract, and “Status after Fix” presents the                          // to StateType . SellerAccepted
result of V ERI S OL after we manually fix the bug (if any).                          State = StateType . Accepted ;
                                                                                  }
The fix may require changing either the policy or the contract,               }
depending on the contract author’s feedback. Finally, “Time”                  ...
                                                                          }
shows the running time of V ERI S OL in seconds when applied
to the fixed contracts.                                                              Fig. 11. Buggy function Accept of AssetTransfer.

   Our experimental results demonstrate that V ERI S OL is
useful for checking semantic conformance between Workbench                overhead. We are currently working on extending the templates
contracts and the policies they are supposed to implement.                for contract invariant inference to richer templates for inferring
In particular, V ERI S OL finds bugs in 4 of 11 well-tested               postconditions for recursive procedures.
contracts and precisely pinpoints the trace leading to the
violation. Our results also demonstrate that V ERI S OL can               Bug Analysis. We report and analyze the five bugs that
effectively automate semantic conformance proofs, as it can               V ERI S OL found in the Azure Blockchain Workbench sample
successfully verify all the contracts after fixing the original           contracts. These bugs can be categorized into two classes: (i)
bug. Moreover, for 10 out of the 11 contracts with the                    incorrect state transition, and (ii) incorrect initial state. We
exception of PingPongGame, the invariant inference techniques             briefly discuss these two classes of bugs.
sufficed to make the proofs completely push-button. Our                   Incorrect state transition. This class of bugs arises when
candidate templates for contract invariant did not suffice for the        the implementation of a function in the contract violates the
PingPongGame contract mainly due to the presence of mutually              state transition stated by the policy. V ERI S OL has found such
recursive functions between two contracts. This required us to            non-conformance in the AssetTransfer and PingPongGame
manually provide a function summary for the mutually recursive            contracts. For instance, let us consider AssetTransfer 4 as a
procedures that states an invariant over the state variable sw            concrete example. In this contract, actions are guarded by the
of the sender contract represented by the msg.sender (e.g.                membership of msg.sender within one of the roles or instance
sw [msg.sender] = s1 ∨ sw [msg.sender] = s2 where si are                  role variables (see Figure 11). V ERI S OL found the transition
states of the sender contract). This illustrates that we can
achieve the power of the underlying sound Boogie modular                    4 https://github.com/Azure-Samples/blockchain/tree/master/
verification to perform non-trivial proofs with modest manual             blockchain-workbench/application-and-smart-contract-samples/asset-transfer
from state BuyerAccepted to state Accepted in the Accept              • The contracts maintain deeply nested mappings and arrays
function had no matching transitions in the policy. Specif-             to store the set of validators for different admins.
ically, the policy allows a transition from BuyerAccepted             • The contracts use nested loops and procedures to iterate
to SellerAccepted when invoking the function Accept and                 over the arrays and use arithmetic operations to reason about
msg.sender equals the instance role variable InstanceOwner.             majority voting.
However, the implementation of function Accept transitions
to the state Accepted instead of SellerAccepted. From                 Properties. We examined three key properties of the PoA
the perspective of the bounded verifier, this is a fairly deep        contract:
bug, as it requires at least 6 transactions to reach the state
BuyerAccepted from the initial state.                                 P1: At least one admin: The network starts out with a single
                                                                          admin at bootstrapping, but the set of admins should
Incorrect initial state. This class of bugs arises when the initial       never become empty. If this property is violated, the
state of a smart contract is not established as instructed by the         entire network will enter into a frozen state where any
corresponding policy. We have found such non-conformance                  subsequent transaction will revert.
in DigitalLocker and BazaarItemListing. For instance,                 P2: Correctness of AdminSet: The AdminSet is a contract
the policy of DigitalLocker requires the initial state of the             that exposes a set interface to perform constant time
smart contract to be Requested, but the implementation ends               operations such as lookup. Since Solidity does not
up incorrectly setting the initial state to DocumentReview. In            permit enumerating all the keys in a mapping, the set
the BazaarItemListing benchmark, the developer fails to                   is implemented as a combination of an array of members
set the initial state of the contract despite the policy requiring        addressList and a Boolean mapping inSet to map
it to be set to ItemAvailable.                                            the members to true. The property checks the coupling
                                                                          between these two data structures — (i) addressList
B. Security Properties of PoA Governance Contract                         has no repeated elements, (ii) inSet[a] is true iff there
                                                                          is an index j such that addressList[j] == a.
   In this section, we discuss our experience applying V ERI S OL
                                                                      P3: Element removal: Deleting an element from an array
to PoA governance contracts. We first give some background
                                                                          is a commonly used operation for PoA contracts. PoA
on PoA and then discuss experimental results.
                                                                          correctness relies on invoking this procedure only for an
Background on PoA governance contracts. In addition                       element that is a member of the array.
to application samples, Workbench also ships a core smart
contract that constitutes an integral part of the Workbench Bugs found. To check the three correctness properties (P1),
system stack. PoA is an alternative to the popular Proof-of- (P2), (P3) described above, we first annotated the PoA
Work (PoW) consensus protocol for permissioned blockchains, governance contracts with appropriate assertions and then
which consist of a set of nodes running the protocol and analyzed them using V ERI S OL. In addition to uncovering a
validating transactions to be appended to a block that will be previously known violation of the “at least one admin” property,
committed on the ledger [9]. Validators belong to different V ERI S OL identified a few other bugs that have been confirmed
organizations, where each organization is represented by an and fixed by the developers. In particular, V ERI S OL found a
administrator. The protocol for admin addition, removal, voting, bug that results in the violation of property (P3): When an
and validator set management is implemented as the PoA admin issues a transaction to remove a validator x from its
governance contract. It implements the Parity Ethereum’s list of validators, a call to event InitiateChange will be
ValidatorSet contract interface and is distributed on the Azure emitted after removing x (using deleteArrayElement). To
Blockchain github [8]. The smart contract consists of five persist the change, another call to finalizeChange is needed.
component contracts (ValidatorSet, SimpleValidatorSet, However, the implementation actually allows two consecutive
AdminValidatorSet, Admin, AdminSet) totaling around 600 calls InitiateChange without a call to finalizeChange.
lines of Solidity code. The correctness of the PoA governance As a result, this bug can result in the PoA contract to fail to
contract underpins the trust on Workbench as well the rest of remove validators that are initiated to be removed.
Azure Blockchain offering.                                             In addition to the manually-added assertions that check the
   The smart contract uses several features that make it a three afore-mentioned properties, the PoA governance contracts
challenging benchmark for Solidity smart contract reasoning. contain additional assertions that were added by the original
We outline some of them here:                                       developers. Interestingly, V ERI S OL also found violations of
• The contracts use multiple levels of inheritance since the        these original assertions. However, these assertion failures
   top-level contract AdminValidatorSet derives from the were due to developers mistakenly using assert instead of
   contract SimpleValidatorSet which in turn derives from require. Although both require and assert failures revert
   ValidatorSet interface.                                          an execution, Solidity recommends using assert only for
• It uses sophisticated access control using Solidity modifiers to  violations of internal invariants that are not expected to fail
   restrict which users and contracts can alter states of different at runtime. V ERI S OL found five such instances of assertion
   contracts.                                                       misuse.
Unbounded verification. Unlike the semantic conformance                     Zeus does not address. Second, unlike our formal treatment
checking problem for client contracts, verifying properties (P1),           of the translation to Boogie, Zeus only provides an informal
(P2), (P3) of the PoA contracts requires non-trivial quantified             description of the translation to LLVM and does not define the
invariants and reasoning about deeply nested arrays. Thus, we               memory model in the presence of nested arrays and mappings.
attempted semi-automated verification of the PoA contracts by               Unfortunately, we were unable to obtain a copy of Zeus to
manually coming up with contract/loop invariants and method                 try on our examples, making it difficult for us to perform an
pre- and post-conditions. In addition, inductive proof of some of           experimental comparison for discharging assertions in Solidity
the properties also requires introducing ghost variables that are           code.
not present in the original code. Fully automated verification of
                                                                 Other approaches. In addition to static analyzers and formal
these properties in PoA governance contracts is an ambitious,
                                                                 verification tools, there are also other approaches that enforce
yet exciting area for future work.
                                                                 safe reentrancy patterns at runtime by borrowing ideas from
                     VI. R ELATED W ORK                          linearizability [19]. Another work that is related to this paper
                                                                 is FSolidM [27], which provides an approach to specify smart
   In this section, we discuss prior work on ensuring the contracts using a finite state machine with actions written in
safety and security of smart contracts. Existing techniques for Solidity. Although there is a similarity in their state machine
smart contract security can be roughly categorized into various model with our Workbench policies, they do not consider
categories, including static approaches for finding vulnerable access control, and the actions do not have nested procedure
patterns, formal verification techniques, and runtime checking. calls or loops. Finally, the FSolidM tool does not provide any
In addition, there has been work on formalizing the semantics static or dynamic verification support.
of EVM in a formal language such as the K Framework [20].
Finally, there are several works that discuss a survey and                              VII. C ONCLUSION
taxonomy of vulnerabilities in smart contracts [13], [26], [28].    In this work, we described one of the first uses of automated
Static analysis. The set of static analysis tools are based on formal verification for smart contracts in an industrial setting.
a choice of data-flow analysis or symbolic execution to find We provided formal semantics to the Workbench application
variants of known vulnerable patterns. Such patterns include the configuration, and performed automatic program instrumenta-
use of reentrancy, transaction ordering dependencies, sending tion to enforce such specifications. We described a new formal
ether to unconstrained addresses that may lead to lost ether, use verification tool V ERI S OL using the Boogie tool chain, and
of block time-stamps, mishandled exceptions, calling suicide illustrated its application towards non-trivial smart contract
on an unconstrained address, etc. Tools based on symbolic verification and bug-finding. For the immediate future, we are
execution include Oyente [26], MAIAN [28], Manticore [10], working on adding more features of the Solidity language that
and Mythril++ [11]. On the other hand, several data-flow are used in common enterprise workflows and exploring more
based tools also exist such as Securify [29] and Slither [12]. sophisticated inference for inferring more complex contract
Finally, the MadMax tool [18] performs static analysis to invariants.
find vulnerabilities related to out-of-gas exceptions. These
                                                                                                  R EFERENCES
tools neither check semantic conformance nor verify assertions.
Instead, they mostly find instances of known vulnerable patterns   [1] Explaining       the    dao     exploit    for     beginners     in    solid-
                                                                       ity.                    https://medium.com/\spacefactor\@m{}MyPaoG/
and do not provide any soundness or completeness guarantees.           explaining-the-dao-exploit-for-beginners-in-solidity-80ee84f0d470,
On the other hand, V ERI S OL does not reason about gas                2016.
consumption since it analyzes Solidity code, and it also needs     [2] Solidity: Function modifiers. https://solidity.readthedocs.io/en/v0.4.24/
                                                                       structure-of-a-contract.html#function-modifiers, 2016.
the vulnerabilities to be expressed as formal specifications.      [3] Azure blockchain.             https://azure.microsoft.com/en-us/solutions/
Formal verification. F* [15] and Zeus [21] use formal verifi-          blockchain/, 2017.
                                                                   [4] Parity: The bug that put $169m of ethereum on ice? yeah, it was on the
cation for checking correctness of smart contracts. These ap-          todo list for months. https://www.theregister.co.uk/2017/11/16/parity_
proaches translate Solidity to the formal verification languages       flaw_not_fixed, 2017.
of F* and LLVM respectively and then apply F*-based verifiers      [5] Applications and smart contract samples for workbench.
                                                                       https://github.com/Azure-Samples/blockchain/tree/master/
and constrained horn clause solvers to check the correctness           blockchain-workbench/application-and-smart-contract-samples, 2018.
of the translated program. Although the F* based approach          [6] Azure blockchain content and samples.                   https://github.com/
is fairly expressive, the tool only covers a small subset of           Azure-Samples/blockchain, 2018.
                                                                   [7] Azure blockchain workbench. https://azure.microsoft.com/en-us/features/
Solidity without loops and requires substantial user guidance          blockchain-workbench/, 2018.
to discharge proofs of user-specified assertions. The design       [8] Ethereum on azure. https://github.com/Azure-Samples/blockchain/tree/
of Zeus shares similarities with V ERI S OL in that it translates      master/ledger/template/ethereum-on-azure, 2018.
                                                                   [9] Ethereum proof-of-authority on azure. https://azure.microsoft.com/en-us/
Solidity to an intermediate language and uses SMT based                blog/ethereum-proof-of-authority-on-azure/, 2018.
solvers to discharge the verification problem. However, there [10] Manticore. https://github.com/trailofbits/manticore, 2018.
are several differences in the capabilities of the two works. [11] Mythril classic: Security analysis tool for ethereum smart contracts.
                                                                       https://mythril.ai, 2018.
First, one of the key contributions of this paper is the semantic [12] Slither, the solidity source analyzer. https://github.com/trailofbits/slither,
conformance checking problem for smart contracts, which                2018.
[13] Nicola Atzei, Massimo Bartoletti, and Tiziana Cimoli. A survey of
     attacks on ethereum smart contracts (sok). In Principles of Security and
     Trust - 6th International Conference, POST , Uppsala, Sweden, April
     22-29, 2017, Proceedings, pages 164–186, 2017.
[14] Michael Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and
     K. Rustan M. Leino. Boogie: A modular reusable verifier for object-
     oriented programs. In Formal Methods for Components and Objects, 4th
     International Symposium, FMCO 2005, Amsterdam, The Netherlands,
     November 1-4, 2005, Revised Lectures, pages 364–387, 2005.
[15] Karthikeyan Bhargavan, Antoine Delignat-Lavaud, Cédric Fournet, Anitha
     Gollamudi, Georges Gonthier, Nadim Kobeissi, Natalia Kulatova, Aseem
     Rastogi, Thomas Sibut-Pinote, Nikhil Swamy, and Santiago Zanella
     Béguelin. Formal verification of smart contracts: Short paper. In
     Proceedings of the 2016 ACM Workshop on Programming Languages
     and Analysis for Security, PLAS@CCS 2016, Vienna, Austria, October
     24, 2016, pages 91–96, 2016.
[16] ComputerWorld.                  Blockchain      to     generate      more
     than     $10.6b     in    revenue     by     2023.           https://www.
     computerworld.com/article/3237465/enterprise-applications/
     blockchain-to-generate-more-than-106b-in-revenue-by-2023.html.
[17] Cormac Flanagan and K Rustan M Leino. Houdini, an annotation
     assistant for esc/java. In International Symposium of Formal Methods
     Europe, pages 500–517. Springer, 2001.
[18] Neville Grech, Michael Kong, Anton Jurisevic, Lexi Brent, Bernhard
     Scholz, and Yannis Smaragdakis. Madmax: surviving out-of-gas
     conditions in ethereum smart contracts. PACMPL, 2(OOPSLA):116:1–
     116:27, 2018.
[19] Shelly Grossman, Ittai Abraham, Guy Golan-Gueta, Yan Michalevsky,
     Noam Rinetzky, Mooly Sagiv, and Yoni Zohar. Online detection of
     effectively callback free objects with applications to smart contracts.
     PACMPL, 2(POPL):48:1–48:28, 2018.
[20] Everett Hildenbrandt, Manasvi Saxena, Nishant Rodrigues, Xiaoran Zhu,
     Philip Daian, Dwight Guth, Brandon M. Moore, Daejun Park, Yi Zhang,
     Andrei Stefanescu, and Grigore Rosu. KEVM: A complete formal
     semantics of the ethereum virtual machine. In 31st IEEE Computer
     Security Foundations Symposium, CSF 2018, Oxford, United Kingdom,
     July 9-12, 2018, pages 204–217, 2018.
[21] Sukrit Kalra, Seep Goel, Mohan Dhawan, and Subodh Sharma. ZEUS:
     analyzing safety of smart contracts. In 25th Annual Network and Dis-
     tributed System Security Symposium, NDSS 2018, San Diego, California,
     USA, February 18-21, 2018, 2018.
[22] Shuvendu Lahiri and Shaz Qadeer. Complexity and algorithms for
     monomial and clausal predicate abstraction. In International Conference
     on Automated Deduction (CADE ’09). Springer Verlag, March 2009.
[23] Shuvendu K. Lahiri, Shaz Qadeer, Juan P. Galeotti, Jan W. Voung, and
     Thomas Wies. Intra-module inference. In Computer Aided Verification,
     21st International Conference, CAV 2009, Grenoble, France, June 26 -
     July 2, 2009. Proceedings, pages 493–508, 2009.
[24] Akash Lal, Shaz Qadeer, and Shuvendu K. Lahiri. A solver for
     reachability modulo theories. In Computer Aided Verification - 24th
     International Conference, CAV 2012, Berkeley, CA, USA, July 7-13, 2012
     Proceedings, volume 7358, pages 427–443. Springer, 2012.
[25] K. Rustan M. Leino. Efficient weakest preconditions. Inf. Process. Lett.,
     93(6):281–288, 2005.
[26] Loi Luu, Duc-Hiep Chu, Hrishi Olickel, Prateek Saxena, and Aquinas
     Hobor. Making smart contracts smarter. In Proceedings of the 2016
     ACM SIGSAC Conference on Computer and Communications Security,
     Vienna, Austria, October 24-28, 2016, pages 254–269, 2016.
[27] Anastasia Mavridou and Aron Laszka. Tool demonstration: Fsolidm for
     designing secure ethereum smart contracts. In Principles of Security
     and Trust - 7th International Conference, POST 2018, Held as Part of
     the European Joint Conferences on Theory and Practice of Software,
     ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings,
     pages 270–277, 2018.
[28] Ivica Nikolic, Aashish Kolluri, Ilya Sergey, Prateek Saxena, and Aquinas
     Hobor. Finding the greedy, prodigal, and suicidal contracts at scale.
     In Proceedings of the 34th Annual Computer Security Applications
     Conference, ACSAC 2018, San Juan, PR, USA, December 03-07, 2018,
     pages 653–663, 2018.
[29] Petar Tsankov, Andrei Marian Dan, Dana Drachsler-Cohen, Arthur
     Gervais, Florian Bünzli, and Martin T. Vechev. Securify: Practical
     security analysis of smart contracts. In Proceedings of the 2018 ACM
     SIGSAC Conference on Computer and Communications Security, CCS
     2018, Toronto, ON, Canada, October 15-19, 2018, pages 67–82, 2018.
