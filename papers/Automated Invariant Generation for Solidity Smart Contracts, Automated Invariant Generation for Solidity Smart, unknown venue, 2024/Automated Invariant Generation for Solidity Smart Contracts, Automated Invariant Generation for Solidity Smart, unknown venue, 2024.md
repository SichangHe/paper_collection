                                                                                                                                                                        1




                                         Automated Invariant Generation for Solidity Smart
                                                             Contracts
                                                                                        Ye Liu, Chengxuan Zhang, Yi Li
                                                                                   Nanyang Technological University, Singapore
                                                                                    {ye.liu, chengxua001, yi li}@ntu.edu.sg



                                           Abstract—Smart contracts are computer programs running on     different versions of the same implementation. For instance,
                                        blockchains to automate the transaction execution between users. the widely used ERC20 implementation from OpenZeppelin
                                        The absence of contract specifications poses a real challenge to the
arXiv:2401.00650v1 [cs.SE] 1 Jan 2024




                                                                                                         initially did not permit a return value for the transfer
                                        correctness verification of smart contracts. Program invariants
                                                                                                         function until a later commit,1 causing incompatibility issues
                                        are properties that are always preserved throughout the execution,
                                        which characterize an important aspect of the program behaviors. with renowned tokens like BNB, as reported by the reputable
                                        In this paper, we propose a novel invariant generation framework,security company SECBIT [4]. In cases where a contract
                                        I NV C ON +, for Solidity smart contracts. I NV C ON + extends the
                                                                                                         necessitates checking the return value of an external call
                                        existing invariant detector, InvCon, to automatically produce    to a transfer function of ERC20 contracts, even if the
                                        verified contract invariants based on both dynamic inference and
                                                                                                         transfer is successful, it may revert due to the absence of a
                                        static verification. Unlike I NV C ON +, InvCon only produces likely
                                                                                                         return value, resulting in compatibility problems [6]. However,
                                        invariants, which have a high probability to hold, yet are still not
                                                                                                         removing the return value check exposes contracts to a potential
                                        verified against the contract code. Particularly, I NV C ON + is able
                                        to infer more expressive invariants that capture richer semantic vulnerability known as the fake deposit attack [7].
                                        relations of contract code. We evaluate I NV C ON + on 361 ERC20    Ensuring the correctness of smart contracts poses a sig-
                                        and 10 ERC721 real-world contracts, as well as common ERC20
                                        vulnerability benchmarks. The experimental results indicate that nificant challenge, especially in the absence of contract
                                                                                                         specifications. On the one hand, the documentation for most
                                        I NV C ON + efficiently produces high-quality invariant specifications,
                                        which can be used to secure smart contracts from common          smart contracts is scant, with even widely recognized smart
                                        vulnerabilities.                                                 contract libraries like OpenZeppelin [8], [9] found to have
                                           Index Terms—Smart contract, invariant detection.              errors and deficiencies in their documentation [10]. On the
                                                                                                         other hand, the absence of contract specifications hampers
                                                                                                         the widespread adoption of formal verification tools in the
                                                               I. I NTRODUCTION                          realm of smart contracts. To address this issue, the commercial
                                           Smart contracts are computer programs that operate on formal verification company Certora2 has adopted a crowd
                                        blockchain networks. They are used to facilitate the manage- sourcing approach—they hosted numerous competitions on
                                        ment of substantial financial assets and the automated execution well-known bug bounty platforms, such as Code4Rena,3 to en-
                                        of agreements among multiple parties who lack inherent gage third-party security experts in the formulation of contract
                                        trust. Notably, blockchain networks such as Ethereum [1] specifications. Yet, manual creation of formal specifications
                                        and BSC [2] are widely recognized as leading platforms for smart contracts remains costly and error-prune.
                                        supporting smart contracts, with applications spanning diverse      Many automated techniques [11], [12] have been proposed
                                        domains such as supply-chain management, finance, energy, to generate formal specifications in various forms to support
                                        games, and digital artworks. While smart contracts hold the testing, verification, and validation of software programs.
                                        promise for facilitating value transfer among users, those Among them, program invariants, which are enduring prop-
                                        that deviate from their specifications may harbor bugs or erties maintained throughout program execution, inherently
                                        vulnerabilities. Numerous implementations of ERC20 contracts serve as excellent candidates for enhancing and reinforcing
                                        diverge from common expectations, as exemplified by standard program specifications. Program invariants have been used
                                        non-compliance of ERC20 [3], particularly concerning event for vulnerability detection [13], conformance checking [3],
                                        emission, balance updates, and the transaction fee mechanisms. runtime protection [14], type checking [15], and formal
                                           Even well-established standard ERC20 implementations verification [16], [17] for smart contracts. Established tools,
                                        exhibit inconsistencies [4]. The root cause lies in the limited such as Daikon [11], can identify likely program invariants for
                                        semantic specifications outlined in the ERC20 standard proposal Java programs through the execution of their test cases. The
                                        document [5]. Take the transfer function as an illustration— process involves statistically inferring the invariants that hold
                                        it is designed to move a specified amount of tokens from the based on predefined templates, while discarding those refuted
                                        sender to the recipient while triggering the Transfer event by the data trace records. The complete historical transaction
                                        and should throw an error if the sender lacks adequate tokens      1 https://github.com/OpenZeppelin/openzeppelin-solidity/commit/
                                        for the transfer. Nevertheless, the ERC20 proposal provides only 6331dd125d8e8429480b2630f49781f3e1ed49cd
                                        simple textual descriptions of the function, leading to semantic   2 https://www.certora.com/

                                        disparities across various ERC implementations and even            3 https://code4rena.com/
                                                                                                                                       2



data of smart contracts is consistently stored on blockchains,
                                                                       a, v ∈ V ariable ::= address | uint | int | string | bytes |
encapsulating all execution data since contract deployment,
serving as a valuable data source for mining invariants.                                     byte | bool | array | mapping | struct{⃗v }
   In our prior work, I NV C ON [18] utilized Daikon to identify        f ∈ F unction ::= f unc(⃗a) {⃗s}
likely invariants for smart contracts, all of which are primitive      s ∈ Statement ::= v | v := e | if (e) {⃗s} else {⃗s}|
predicates hold throughout the existing transaction histories.                               call(⃗e) | return e |
Moreover, Liu et al. [19] employed reinforcement learning to                                 require(e) | assert(e) | revert
learn contract invariants critical to safely performing arithmetic            e ∈ Expr ::= v | const | e[e] | e.v | e ▷◁ e
operations, with focus on preventing integer overflow and
underflow. Despite their usefulness, the correctness of such                Fig. 1: The core grammar of the Solidity language.
inferred invariants remains unverified. In particular, an invariant
which holds in past transactions may not always hold in the Organizations. The rest of the paper is organized as follows.
future—this may be due to the limited contract interactions Section II provides the background about smart contracts and
observed in the transaction histories so far.                        invariant inference. Section III defines the invariant specification
   In this paper, we expand upon I NV C ON to generate verified language. Then, Sect. IV introduces our invariant generation
contract invariants utilizing both dynamic inference and static approach. Section V describes our implementation framework,
verification. We introduce a specialized invariant specification I NV C ON +, and Sect. VI demonstrates our evaluation results.
language tailored for Solidity smart contracts and propose a The related work is discussed in Sect. VII and we conclude
novel approach for inferring high-quality verified invariants. the paper in Sect. VIII.
Specifically, we design a Houdini-like [12] algorithm to
generate verified invariants for smart contracts. To address the                              II. BACKGROUND
explosion problem in searching for richer invariant candidates, A. Solidity Smart Contracts
such as implications that prevail in ERC20 and ERC721 [20],
                                                                        Figure 1 presents the foundational grammar of the Solid-
[21], [22] specifications, we introduce an iterative and incre-
                                                                     ity language, with certain features, such as event emission,
mental process for exploring these candidates on demand. We
                                                                     intentionally excluded for the sake of clarity. Solidity encom-
also apply control- and data-flow analyses to eliminate mean-
                                                                     passes various primitive data types, including integer, string,
ingless candidates and further improve the invariant generation
                                                                     and Boolean. Distinguishing itself from other programming
efficiency. Our approach is implemented as an automated
                                                                     languages like Java, Solidity does not permit floating-point
tool called I NV C ON +. Through evaluation on 361 ERC20
                                                                     numbers and incorporates a distinctive address type. This design
contracts and 10 ERC721 real-world Solidity contracts, we
                                                                     choice is rooted in the interaction pattern between contracts and
demonstrate that I NV C ON + produces comprehensive contract
                                                                     blockchain users, each possessing a unique address. Moreover,
invariant specifications with no false positives. Furthermore, our
                                                                     the majority of contracts are developed with the primary goal
analysis of real-world vulnerable ERC20 contracts underscores
                                                                     of tokenizing digital assets.
the potential of I NV C ON + in safeguarding these contracts
                                                                        A Solidity smart contract comprises a collection of state
through the application of mined invariant specifications.
                                                                     variables and a set of functions. Statements within each
   In summary, we make the following contributions:
                                                                     function can take the form of variable assignments, conditional
   • We introduce a comprehensive invariant specification
                                                                     statements, internal or external function calls, requirement
      language designed for expressing operational semantics
                                                                     or assertion statements, and reversion or return statements.
      in Solidity smart contracts. This language enables logical
                                                                     Notably, the require and assert statements can be employed
      operations on variables of primitive types and commonly
                                                                     to enforce program invariants at runtime. In the realm
      used data structures like structs, arrays, and mappings in
                                                                     of expressions, ▷◁ denotes a binary operator encompassing
      Solidity.
                                                                     {+, −, ∗, /, >, <, ≥, ≤, =, ̸=, ∧, ∨}.
   • We present a unified framework for generating verified
      invariants in Solidity smart contracts, combining dynamic Smart Contract Execution. The execution of a smart contract
      invariant detection and static invariant verification. Specif- function can be triggered by sending a blockchain transaction
      ically, we develop a custom algorithm inspired by the to the contract address. Typically, each transaction incorporates
      Houdini algorithm to verify invariants for smart contracts one or more contract calls, potentially leading to alterations
      and introduce an iterative process to derive a richer class in contract state variables unless the transaction undergoes a
      of invariants.                                                 reversion. To ease the discussion in this paper, we model a
   • Our proposed approach is implemented in I NV C ON +,            smart contract SC as a tuple (⃗v , f⃗), where ⃗v is a vector of
                                                                                           ⃗
      and its effectiveness is evaluated on 361 ERC20 con- state variables and f is a list of public functions.
      tracts and 10 ERC721 contracts, along with vulnerable Definition II.1 (Contract Execution). Let Dom(v) be the
      ERC20 contracts involving 25 types of vulnerabilities. domain of a variable v and Dom(⃗v ) = Q Dom(v). Then,
      The results demonstrate that I NV C ON + can generate                                                           v∈⃗v
                                                                          ′
      high-quality and comprehensive invariant specifications δ, δ ∈ Dom(⃗v ) represent two reachable contract states. For a
      for smart contracts. The dataset, raw results, and the function invocation f (⃗a), calling function f with parameters
      prototype used in our experiments are available online at: values ⃗a, we define its high-level execution semantics as a state
                                                                                    f (⃗
                                                                                       a)
      https://sites.google.com/view/invconplus/.                     transition δ −−−→ δ ′ .
                                                                                                                                          3



                                                                    in Fig. 1. We facilitate two types of variables. The first, denoted
     const ∈ Int, Bool, Addr, Str x ∈ FreeVar v ∈ Var
                                                                    as v, pertains to function input parameters or contract state
     e ∈ Expr ::= const | v | old(v) | len(v) | SumM ap(v) |        variables maintained in the persistent storage of the blockchain.
                    e.x | e[x] | e ▷◁ e                             The second, denoted as x, is reserved for free variables
     p ∈ Predicate ::= ⊥ | e | e =⇒ e                               exclusively utilized to index structure members or items within
     Statement ::= Requires p | Ensures p | ContractInv p           arrays and mappings. Each invariant predicate is expressed as
                                                                    either a primitive logical expression or an implication expres-
          Fig. 2: The invariant specification language.             sion. Furthermore, valid specification statements encompass
                                                                    function-level precondition invariant predicates (Requires) and
   Note that since a contract execution is triggered by a postcondition invariant predicates (Ensures), and contract-level
transaction recorded into a specific block of the blokchain, invariant predicates (ContractInv).
the parameter values ⃗a also includes implicit transaction and         The expressions within the language may take the form of
block parameters, e.g., msg.sender and block.number. constants, variables, structure members, array items, and binary
Transaction Histories. The execution of a smart contract is expressions. The old(·) notation is employed to differentiate
intricately linked to its transaction histories on the blockchain. between the value of a variable before entering the function
The transaction histories record every contract execution, and its value upon exiting the function, while len(·) refers to
capturing function calls, state transitions, and modification the array length or mapping size. Additionally, the language in-
to state variables from the contract deployment onward. It corporates the widely used SumMap(·) operator for computing
encapsulates the evolution of the contract state, reflecting the the arithmetic sum over mapping items. The notation “e ▷◁ e”
cumulative effect of all transactions. This historical traceability represents arithmetic or logical binary operations, where the
is fundamental for auditing, debugging, and understanding the operator “▷◁” corresponds to the set defined in Solidity as
operational dynamics of smart contracts on the blockchain.          shown in Fig. 1.
                                                                       Utilizing this invariant language, we can articulate a diverse
B. Invariant Inference                                              range  of function
                                                                       and contract invariants. To exemplify its application, we
   In this paper, we aim to mine contract-level and function- present a simple illustration. In Fig. 3, a basic ERC20 contract
level invariant specifications.                                     is depicted, featuring three state variables—totalSupply,
Definition II.2 (Function Pre/Post-conditions). Let f be a balances, allows (standing for allowances)—and a func-
contract function, and predicates p and q be the pre/post- tion, transferFrom. The purpose of the transferFrom
conditions of f , respectively, which can be represented as function is to transfer a specified amount of tokens from the
a Hoare triple {p}f {q}. Then the following condition should account addressed at from to another account at to. An
be satisfied.                                                       extensively studied ERC20 contract invariant of this example
                                   f (⃗
                                      a)                            can be succinctly expressed as: “SumM ap(balances) =
             ∀δ, ∀⃗a · δ |= p ∧ δ −−−→ δ ′ =⇒ δ ′ |= q          (1) totalSupply”. This assertion signifies that the total sum of
Definition II.3 (Contract Invariant). Given a smart contract items within the mapping variable balances must be equal
SC, its contract invariant I is a predicate that must hold for to the value of totalSupply. Additionally, the function
any contract function execution. More formally, we have ∀f ∈ pre/post-conditions can be articulated as follows.
SC · {I}f {I}.                                                         Requires ⊥
   Invariant inference techniques can be broadly categorized           ⃝
                                                                       1 Ensures to ̸= 0 =⇒ allows[f rom][msg.sender] =
as static and dynamic. Static invariant inference (e.g., Hou-                      old(allows[f rom][msg.sender]) − tokens
dini [12]) identifies function pre/post-conditions and contract        ⃝
                                                                       2 Ensures to ̸= 0 ∧ f rom ̸= to =⇒ balance[f rom] = old(balance[
invariants that hold for any program execution. On the other               f rom]) − tokens ∧ balance[to] = old(balance[to]) + tokens
hand, dynamic invariant inference (e.g., Daikon [11]) identifies       ⃝
                                                                       3 Ensures to ̸= 0 ∧ f rom = to =⇒ balance[f rom] =
likely invariants that hold for specific contract executions (e.g.,           old(balance[f rom]) ∧ balance[to] = old(balance[to])
executions of a test case).
                                                                        In this instance, it is straightforward to ascertain that there are
   Let ∆ denotes a set of program executions {(δ, f (⃗a), δ ′ )},
                                                                      no preconditions for the transferFrom function, assuming
which bring the contract state from δ to δ ′ . The likely
                                                                      that all function preconditions are primitive predicates. The
function pre/post-conditions of f , i.e., {p̂}f {q̂}, hold for ∆ if
                                     f (⃗
                                        a)                            function is characterized by three postconditions. The first
∀(δ, f (⃗a), δ ′ ) ∈ ∆, δ |= p̂ ∧ δ −−−→ δ ′ =⇒ δ ′ |= q̂. The likely postcondition ⃝ 1 specifies that allows will undergo an update
contract invariants of a smart contract is defined in a similar (Line 11) when to is a non-zero address. Additionally, in cases
way, which is omitted here for brevity.                               where from and to represent distinct addresses, the second
                                                                      postcondition ⃝ 2 dictates that the balances should be adjusted
          III. I NVARIANT S PECIFICATION L ANGUAGE                    accordingly (Lines 12–13). Conversely, when from and to
  Figure 2 introduces our invariant specification language are identical, the last postcondition ⃝               3 emphasizes that the
designed for Solidity smart contracts. The language accom- net effect on balance changes should be nullified. A detailed
modates variables of four types: integer, Boolean, address, exploration of how these invariants are mined will be provided
and string, encompassing all primitive Solidity types illustrated in Sect. IV-E.
                                                                                                                                              4



 1 contract ERC20 {                                                     Algorithm 1: Contract Invariant Inference
 2  // state variables
 3  uint totalSupply;                                                     Inputs : SC = {⃗v , f⃗}, where each element vi ∈ ⃗v is a
 4  mapping(address=>uint) balances;                                                  contract state variable and each element fi ∈ f⃗ is a
 5  mapping(address=>mapping(address=>uint)) allows;                                  public contract function;
 6  ...
 7  function transferFrom(address from, address to,
                                                                                    : T = {ti |1 ≤ i ≤ n}, where each element ti is a
     ,→    uint tokens) public returns (bool) {                                       contract transaction;
 8     if (to == address(0)){                                                       : Q, a set of invariant templates.
 9               return false;                                            Outputs : Invs, a set of verified invariants.
10     }                                                                1 Invs := ∅;
11     allows[from][msg.sender] =                                       2 C := I NITIALIZE C ANDIDATES (⃗      v , f⃗, Q) ; //primitive
        ,→   allows[from][msg.sender].sub(tokens);                         candidates
12     balances[from] = balances[from].sub(tokens);
                                                                        3 ∆ := ∅ ; //execution trace set
13     balances[to] = balances[to].add(tokens);
                                                                        4 foreach ti ∈ T do
14     return true;
15  }                                                                   5     (δ, f (⃗a), δ ′ ) ← PARSE(ti ) ;
16 }                                                                    6     ∆ ← ∆ ∪ (δ, f (−    →a ), δ ′ );
                                                                        7 end foreach
               Fig. 3: A simple ERC20 contract.                         8 Clikely , Cpartial ←I NV D ETECT (∆, C);
                                                                        9 Invs ← S TATIC I NFER (Clikely ) ;
                                                                       10 Cimp ← FIND I MPLICATIONS (Clikely \ Invs, Cpartial ) ;
          IV. I NVARIANT G ENERATION A PPROACH
                                                                           //implication candidates
   In this section, we present our algorithm for generating            11 while Cimp ̸= ∅ do
verified invariants in smart contracts and elaborate on the tech-      12     Invs ← Invs ∪ S TATIC I NFER(Cimp ) ;
niques employed to infer implication invariants. For simplicity        13     Cimp ← WEAKEN I MPLICATIONS(Cimp \ Invs);
                                                                       14 end while
in presentation, we use the term “invariants” to collectively          15 return Invs
denote both function pre/post-conditions and contract invariants
when explicit characterization is unnecessary.                                                     ⊥
                                                                                                                                       Init
                                                                       Cimp := {(η =⇒ τ ) |η, τ ∈ Clikely \ Invs ∪ Cpartial , η ̸= τ }
A. Algorithm
                                                                                                    ∀a ∈ vars(η), ∀b ∈ vars(τ ).
    Algorithm 1 outlines our approach to invariant generation.            (η =⇒ τ ) ∈ Cimp
                                                                                                            ¬ dep(a, b)
The algorithm takes a smart contract SC , a sequence of contract                                                                     Delete
transactions T , and a set of invariant templates Q as input. The                       Cimp ← Cimp \ (η =⇒ τ )
output, denoted as Invs, comprises a set of verified invariants,                          Fig. 4: F IND I MPLICATIONS
encompassing both primitive and implication invariants.
    In this algorithm, Invs is initialized as an empty set (Line 1).   Subsequently, a primitive invariant inference technique, detailed
Subsequently, we initialize a set C that encompasses all poten-        in Sect. IV-B, is applied to infer the standing invariants out
tial invariant candidates under the given input (Line 2), similar      of Clikely , and all the verified invariants are included in Invs
to Daikon’s initialization process [11], which instantiates all the    (Line 9). The unverified likely invariant candidates, Clikely \
parameterized invariant templates with concrete contract state         Invs, and Cpartial are used to derive implication candidates
variables and function input variables. For example, “X = Y ”          assigned to Cimp (Line 10) via F IND I MPLICATIONS, which will
is a binary equation template where X and Y are placeholders           be detailed in Sect. IV-C. Additionally, it is important to note
that can be filled by two concrete variables: vx and vy whenever       that the found implications may not always hold. An iterative
Dom(vx ) ≡ Dom(vy ). It is important to note that here C               process is in place to validate these implications (Line 12)
excludes implication invariant candidates due to the exponential       or weaken these implications via W EAKEN I MPLICATIONS
complexity of traversing all implication candidates. Instead,          (Line 13) to identify new ones. This iterative process continues
implication invariants will be generated on demand. Moreover,          until all valid candidates are examined (Line 11). Finally, the
the execution trace set ∆ is initialized as an empty set (Line 3).     algorithm returns Invs, which includes all the correctly mined
    The algorithm processes the transaction histories to extract       invariants from transaction histories (Line 15).
corresponding execution traces. For each transaction ti , the
algorithm parses it to extract the invoked function f and
parameters values ⃗a (Line 5). Additionally, the old and present       B. Primitive Invariant Inference
contract states (i.e., values of the contract state variables),           Algorithm 2 illustrates our Houdini-like algorithm to infer
denoted as δ and δ ′ , respectively, are recorded. The tuple (δ,       verified primitive invariants from the candidates mined from
f (⃗a), δ ′ ) is added to the execution trace set ∆ (Line 6).          contract transaction histories. First, we enable all the candidates
    Next, the algorithm executes the dynamic invariant detection       in SC via contract instrumentation (Line 1); each candidate is
procedure I NV D ETECT (Line 8) to obtain two classes of               explicitly labeled by the added keywords, e.g., ContractInv
invariant candidates:                                                  for contract invariant, Requires for function precondition,
    • Clikely , likely invariant candidates that hold for the entire   and Ensures for function postcondition. Next, we invoke a
       transaction histories.                                          modular verifier to statically verify these enabled candidates
    • Cpartial , partially supported invariant candidates that hold    (Line 3), i.e., verifying each function in isolation where all the
       for a subset of transaction histories.                          corresponding candidates are examined against the function
                                                                                                                                           5



                            ⊥                                            we leverage the well-known static analysis tool Slither [23] to
                                   Init
                          ˆ
                         Cimp := ∅                                       trace data-flow and control-flow in smart contract functions.
                                                                         Therefore, in Fig. 4, a Delete rule is applied to eliminate
(η1 =⇒ τ ), (η2 =⇒ τ ) ∈ Cimp \ Invs      η1 ∧ η2 ̸≡ f alse
                                                              Append-1   implications that do not adhere to the data-flow and control-
             ˆ ← Cimp
            Cimp  ˆ ∪ (η1 ∧ η2 =⇒ τ )                                    flow relationship. This rule is iteratively applied until no further
(η =⇒ τ1 ), (η =⇒ τ2 ) ∈ Cimp \ Invs      τ1 ∨ τ2 ̸≡ true                implications can be eliminated.
                                                              Append-2      Some implication candidates may be too strong and cannot
             ˆ ← Cimp
            Cimp  ˆ ∪ (η =⇒ τ1 ∨ τ2 )
                                                                         be proved. Figure 5 illustrates how we derive a weaker
               Fig. 5: W EAKEN I MPLICATIONS.                            set of implication candidates Cimp    ˆ from those unverified
                                                                         implication candidates denoted as Cimp \ Invs. In Fig. 5,
 Algorithm 2: S TATIC I NFER(Candidates)                                 W EAKEN I MPLICATIONS comprises three inference rules. It
                                                                                         ˆ to an empty set. Then the rules Append-1
                                                                         initially sets Cimp
1  Instrument SC to enable each candidate from Candidates;
2  while true do                                                         and Append-2 generate weaker implications by combing two
 3      result = M ODULARV ERIFY(SC) ;                                   unverified implication candidates. In essence, η1 ∧ η2 =⇒ τ
 4      if result = CORRECT then                                         is weaker than either η1 =⇒ τ or η2 =⇒ τ . Similarly,
 5           return enabled candidates ; //verified                      η =⇒ τ1 ∨ τ2 is weaker than both η =⇒ τ1 and
              invariants
 6      else if result = INCORRECT due to failed candidate c             η =⇒ τ2 . To eliminate useless implications that are
          then                                                           tautologies, we impose restrictions on the original implications,
 7           disable c in SC;                                            such as η1 ∧ η2 ̸≡ false and τ1 ∨ τ2 ̸≡ true. It is evident that
 8      else                                                             the weaker implications are also relevant as they satisfy the
 9           raise Error ; //INCORRECT due to failed                     same control/data-flow dependencies as the original ones.
              assertion in SC
10      end if
11 end while                                                             D. Termination
                                                                            The termination of Alg. 1 can be ensured by the fact that
implementation. When there is a failed invariant candidate               I NV C ON + can only produce a finite set of primitive invariant
c violating the verification condition, c will be disabled in            predicates. The conclusion regarding the termination of Alg. 1
SC (Line 7). This process will continue until all the enabled            hinges on whether the loop (Lines 11-14) comes to an end. In
candidates are verified successfully (Line 4) and then returned          each iteration of the loop, we possess at least one implication
(Line 5). Particularly, whenever there is a failed assertion in          candidate, constructed by W EAKEN I MPLICATIONS (refer to
SC, i.e., a violated condition e in the assert(e) statement, the         Sect. IV-C). Regarding W EAKEN I MPLICATIONS, it consistently
algorithm terminates with an error raised (Line 9). This happens         generates weaker implication candidates than the previous
in Solidity contracts, because assert(e) is often misused to             ones, utilizing conjunctions over premises or disjunctions
replace require(e) that enforces program requirements due                over consequences. Assuming I NV D ETECT yields n primi-
to their similar effects on transaction reversion. For smart             tive invariant predicates Clikely ∪ Cpartial = {p1 , . . . , pn },
contracts without failed assertions, the verified invariants is          then the weakest implication will be at least as strong as
a maximal subset of the candidates whose conjunction is an               p1 ∧ · · · ∧ pn =⇒ p1 ∨ · · · ∨ pn . Consequently, the loop
inductive invariant.                                                     will finish in no more than 2 × n iterations, establishing the
                                                                         termination of this algorithm.
C. Implication Invariant Inference
   Figures 4 and 5 illustrate the two procedures for identifying E. Running Example
implication candidates, respectively. In Fig. 4, F IND I MPLICA -     We illustrate our algorithm using the example presented
TIONS employs two straightforward inference rules. The first       in Fig. 3. The details regarding our transaction parsing and
rule explores all the potential implication candidates from the invariant detection will be elaborated in Sect. V. For the sake
unverified likely invariants Clikely \ Invs and partial invariant of simplicity in the illustration, assume that we have already
candidates Cpartial , including them in Cimp . An implication acquired a set of likely and partially supported invariants
invariant takes the form of η =⇒ τ , where η and τ comes through invariant detection on the transaction histories. In
from the existing the unverified and partial invariant candidates. Table I, the invariants labeled with ✓ are successfully verified
   However, not all of the implication candidates constructed by the static verifier, while the ones with ✗ are unverified.
this way are relevant in terms of the contract semantics. An In Step ⃝,      1 we perform a Houdini-like static inference on
implication can possibly hold (i.e., relevant) if its precondition these detected invariant candidates. Consequently, three likely
and postcondition align with the data/control-flow of the invariants are verified, excluding to ̸= 0. In the subsequent
contracts, and irrelevant implications should be discarded. The step (Step ⃝), 2 nine additional implication invariant candidates
notation vars(p) represents variables appearing in an invariant are generated from the previously unverified likely invariants
predicate p; for instance, vars(p) = {f rom, to} when p is and partially supported invariants, according to the rules in
“f rom ̸= to”. Additionally, dep(a, b) denotes whether variable F IND I MPLICATIONS (see Fig. 4). However, after the modular
a depends on variable b in terms of control-flow or data-flow in verification, only one implication is confirmed. Furthermore,
smart contract functions. To determine the valid implications, we weaken these unverified implication invariants in Step ⃝       3
                                                                                                                                                  6




                  ∆       Dynamic                                                 is denoted as (status, storageChanges). Here, status signifies the
   Data Parser            Invariant                                               transaction’s success or failure, while storageChanges details
                          Detector
                                         Clikely                                  the alterations in the contract’s storage across various slots. By
                                                                                  aligning storage slots with the contract’s storage layout, one
                      Cpartial                                                    can effectively interpret these storage modifications as changes
                                  Cimp        Modular         Invs
                                              Invariant              Suppressor   in the values of the contract’s state variables. Employing
   Transactions                                Verifier
                                                                                  the previously described preprocessing technique enables the
                        Implication                                               extraction of a sequence of data triples (i.e., execution traces).
                          Learner         Clikely \ Invs or
      Smart                               Cimp \ Invs                             These triples consist of the actual values of state variables and
     Contract                                                                     function input variables at the point of function entry, as well
                                                                     Invariants
                                                                                  as the most recent values of state variables at the point of
Contract & History                                                                function exit. It is important to note that any misrecognition
       Fig. 6: The architecture overview of I NV C ON +.                          of variables can lead to incorrect invariant results. We have
                                                                                  implemented measures to ensure the accuracy of variable
using W EAKEN I MPLICATIONS (see Fig. 5) to derive four new                       recognition. For state variables of primitive types, we directly
implication candidates for further validation. Eventually, all                    ascertain their values, as the storage layout for these variables
the invariants listed in Sect. III are successfully recovered (in a               remains constant during runtime. In the case of non-primitive,
logically equivalent form). Moreover, two other invariants,                       dynamic state variables, to reduce computational cost, we
balances[to] ≥ old(balances[to]) and balances[f rom] ≤                            initially utilize the known variable values to hypothesize a
old(balances[f rom]), are verified, which provide additional                      correlation between the altered storage slots and the dynamic
insights on how the balances of the sender and the receiver                       state variables. However, if this approach fails to produce
should change when transferFrom is called, beyond the                             an accurate mapping, it becomes necessary to replay the
standard specifications.                                                          entire transaction. This replay process enables us to track
                                                                                  the comprehensive execution information, including storage
                                                                                  modifications, thus allowing for the accurate determination of
                        V. I MPLEMENTATION                                        the correct mapping.
A. Overview
   Figure 6 demonstrates the high-level architecture of I N -                     C. Dynamic Invariant Detector
V C ON +, our automated invariant detection tool for Solidity
smart contracts. The inputs to I NV C ON + include a set of           The effectiveness of dynamic invariant detection largely
historical transactions and the corresponding contract source      depends    on the diversity and scale of the customized invariant
code, while its output is a collection of smart contract invariant templates    used. In our methodology, these invariant templates
specifications or the accordingly annotated contract code.         are  required   to conform to the invariant specification language
I NV C ON + comprises four modules: (1) a data parser that         outlined   in Fig.  2. However, it is both impossible and impracti-
decodes contract code and transaction histories to extract         cal to cover   every  conceivable invariant template. Our approach,
concrete execution trace set; (2) a dynamic invariant detector     akin   to  that   of  I NV C ON [18], limits the scope to unary,
that generates a set of likely and partially supported invariants; binary,   and  ternary   invariant templates. Unlike I NV C ON, our
(3) a modular invariant verifier and an implication learner        templates    are specifically  designed for Solidity smart contracts,
that verify and learn contract invariants, respectively; and (4)   which   are  predominantly    used  for financial applications. These
a suppressor that simplifies the results by removing redundant     contracts    often   entail  intricate  scientific computations on
invariants. Notably, the implication learner has already been      scalar  variables.    Furthermore,    Solidity  features an array of
detailed in Sect. IV-C.                                            complex     data   structures,  such   as  mapping    and struct. To
                                                                   effectively infer invariants related to these structures, we have
                                                                   incorporated several derivation templates, such as MemberItem
B. Data Parser                                                     and MappingItem, which facilitate access to elements within
   Given a contract, we first collect all of its historical these data structures. Additionally, drawing inspiration from
transactions. For each transaction, we decode the specific the significance of balance invariants as highlighted by Wang
function input based on the contract’s Application Binary et al. [24], we have introduced a SumMap derivation template.
Interface (ABI), and we interpret the transaction output in This template is specifically designed to aggregate the values
accordance with the contract’s storage layout specifications. contained within a mapping variable.
This layout dictates where each state variable is stored in the       Dynamic invariant detection employs a statistical methodol-
blockchain database. For instance, as shown in Fig. 1, the first ogy to generate likely primitive invariants with a certain degree
declared state variable totalSupply is stored at the first of statistical confidence. Contrasting with the approach of I N -
slot (0x0) in the contract’s blockchain database.                  V C ON, our method retains invariants that are refuted by certain
   The input of a contract transaction is represented as a transactions in the final results. This is because less stringent
tuple (sender, function, parameters), which encapsulates the forms of these invariants, expressed as implications, may still
transaction’s sender, the invoked function’s name, and the corre- hold true for certain contracts. Both the likely invariants and
sponding input parameters. Conversely, the transaction’s output the falsified ones constitute a high-quality set of primitive
                                                                                                                                    7



                                      TABLE I: Illustration example of invariant verification.
       Step    Invariants
       ⃝
       1       Likely Contract Invariants:                     Partially Supported Function Pre/post-conditions:
               totalSupply = SumMap(balances) ✓                from ̸= to
               Likely Function Pre/post-conditions:            from = to
               to ̸=0 ✗                                        balances[from] = old(balances[from]) - tokens
               balances[to] ≥ old(balances[to]) ✓              balances[to] = old(balances[to]) + tokens
               balances[from] ≤ old(balances[from]) ✓          allows[from][msg.sender] = old(allows[from][msg.sender]) - tokens
                                                               balances[from] = old(balances[from])
                                                               balances[to] = old(balances[to])
       ⃝
       2       Implication Invariant Candidates:
               to ̸=0 =⇒ allows[from][msg.sender] = old(allows[from][msg.sender]) - tokens ✓
               to ̸=0 =⇒ balances[from] = old(balances[from]) - tokens ✗
               to ̸=0 =⇒ balances[to] = old(balances[to]) + tokens ✗
               to ̸=0 =⇒ balances[from] = old(balances[from] ✗
               to ̸=0 =⇒ balances[to] = old(balances[to]) ✗
               from ̸=to =⇒ balances[from] = old(balances[from]) - tokens ✗
               from ̸=to =⇒ balances[to] = old(balances[to]) + tokens ✗
               from = to =⇒ balances[from] = old(balances[from] ✗
               from = to =⇒ balances[to] = old(balances[to]) ✗
       ⃝
       3       Weakened Implication Invariant Candidates:
               to ̸=0 ∧ from ̸=to =⇒ balances[from] = old(balances[from]) - tokens ✓
               to ̸=0 ∧ from ̸=to =⇒ balances[to] = old(balances[to]) + tokens ✓
               to ̸=0 ∧ from = to =⇒ balances[from] = old(balances[from]) ✓
               to ̸=0 ∧ from = to =⇒ balances[to] = old(balances[to]) ✓

predicates. Each of these predicates has been empirically does), we only remove redundancies from the invariants that
verified through historical transaction data of smart contracts. are successfully verified. This design leaves more choices to the
In our evaluation setting, each valid primitive invariant must implication learner, when synthesizing implication invariants.
be supported by at least three historical transactions.             Among the verified invariants, we utilize the Z3 solver [27]
                                                                    to determine if one invariant predicate can be deduced from
D. Modular Invariant Verifier                                       another. Following this analysis, we retain only the strongest
                                                                    invariant predicates in our final results.
   The Houdini algorithm [12] is a widely recognized technique
commonly used in program annotation and validation processes.
Its primary objective is to automatically generate invariant                               VI. E VALUATION
annotations from a group of candidates. To adapt Houdini               In this section, we evaluate I NV C ON + to answer the
algorithm for Solidity contracts, we initially instrument the following research questions:
contracts with the mined invariants. This entails converting the      1) RQ1: How effectively does I NV C ON + generate invariants
invariants into a compatible format and then embedding them              for smart contracts?
into the contract. The annotations are strategically placed at        2) RQ2: How does the length of transaction histories used
the beginning of functions to align with their specific names            affect the performance of I NV C ON +?
and arguments. Subsequently, we transform the instrumented            3) RQ3: How effective are the invariants detected by I N -
contracts into Boogie [25] programs, leveraging the existing             V C ON + in preventing real-world security attacks?
formal verification tool VeriSol [26] for Solidity smart contracts.
We have refined the Boogie translator in VeriSol to better
accommodate contracts with inheritance and polymorphism A. Methodology
features. For instance, the original translator lacked support
                                                                    Benchmark. To answer RQ1 and RQ2, we collected real-world
for unnamed parent contract calls using the “super” keyword
                                                                    smart contracts implementing the most popular ERC20 and
in Solidity, and it did not handle function overloading where
                                                                    ERC721 standards, which have been studied extensively in
a contract includes multiple functions with the same name.
                                                                    previous works [3], [4], [14], [28], [29]. The most important
We have enhanced its translation rules to effectively translate
                                                                    reason of choosing smart contracts implementing common
these complex contracts into Boogie programs. Finally, we
                                                                    standards is that their invariant specifications are better under-
utilize Boogie’s own Houdini modular verifier to infer among
                                                                    stood, making it easier to obtain the ground truth. First, we
the aforementioned invariant annotations, resulting in a set of
                                                                    queried the public Ethereum ETL dataset hosted on the Google
verified invariants.
                                                                    BigQuery platform [30] and then identified 13,116 contract
                                                                    addresses flagged as ERC20 deployed between 2021 and 2022.
E. Suppressor                                                       Then, we identified 2,689 ERC721 contract addresses deployed
   An invariant is deemed redundant if it can be derived from between 2020 and 2022. To facilitate our analysis, we kept
another invariant. The invariants verified by I NV C ON + may only open-source contracts written in Solidity versions ranging
contain such redundancies. Instead of eliminating redundancies between 0.5.0 and 0.5.17, which are currently supported by
in the dynamically detected invariants (as what Daikon [11] V ERI S OL. Finally, we obtained 361 ERC20 contracts and 10
                                                                                                                                          8



ERC721 contracts for the experimental evaluation, where each           and useful in describing unique smart contract behaviors.
contract has at least 50 historical transactions as of June 2023.
   To establish the ground truth for ERC20 and ERC721 B. Experiment Setup
contract specifications and ensure the included invariants             All the experiments were conducted on a desktop computer
are comprehensive, we investigated multiple external sources. with the Ubuntu 20.04 OS, an Intel Core Xeon 3.50GHx
These include the formal specifications referenced in the processor, and 32GB of RAM. To facilitate the evaluation, we
existing literature [4], [14], popular smart contract libraries, have crawled and cached all transaction histories in advance
such as OpenZeppelin [8], and online documentations provided for the contracts used in our experiments.
by smart contract formal verification companies. We list
the collected ERC20 and ERC721 invariant specifications in C. RQ1: Effectiveness of Invariant Generation
Table II and Table III, respectively. These specifications are
mainly based on Certora [20], [21], [31], KEVM [22], [28], and Baseline. To evaluate the performance of I NV C ON +, we used
OpenZeppelin API documentations [32], [33]. We analyzed I NV C ON as our baseline. I NV C ON uses Daikon as the back-end
each of the collected invariants and manually translated it invariant detection engine and more implementation details
into our own specification language (C.f. Fig. 2), which is can be found in the previous work [18]. To the best of
a straightforward exercise in most cases. We categorized our knowledge, Cider [19] is the only automated invariant
these invariant specification into contract invariants, function generation tool for smart contracts besides I NV C ON. We have
                                                                                                                                           4
preconditions and postconditions in Tables II and III. The contacted the authors of Cider to obtain a copy of the tool,
functions listed in each table are the most commonly used but failed to set it up. We will discuss and compare with this
standard functions for ERC20 and ERC721 contracts. Some work in Sect. VII.
specifications documented in external sources were omitted,            Additionally, we compared I NV C ON + with its two variants:
e.g., “Emitting a Transfer event” for the transfer I NV C ON + Naive, which performs only dynamic invariant
function, because the particular language features are not detection tailored to Solidity contracts, and I NV C ON + Primitive,
supported by our specification language.                           which employs the Houdini algorithm to generate verified invari-
                                                                   ants based only on dynamically detected invariant candidates.
Evaluation Metrics. We use two evaluation metrics to evaluate
                                                                   Results. Table IV presents the comparison results for 361
I NV C ON + on the ERC20 and ERC721 contracts. Particularly,
                                                                   ERC20 contracts, with a constraint of utilizing a maximum of
we use Precision and RecallERC20 (RecallERC721 ) to measure
                                                                   200 transactions per contract. The first column displays the
the effectiveness of the generated invariants, denoted as
                                                                   names of the tools, while the second column enumerates the
Xproved . We denote the ground truth invariants (e.g., ERC20)
                                                                   averaged number of invariants generated by each respective
as Y . Formally,
                                                                   tool per contract. The middle two columns showcase the overall
                                   |Xproved |
                      Precision =             ,                (2) Precision and RecallERC20 scores, and the last column provides
                                      |X|                          the averaged time usage for each tool.
                                         |Xproved ∩ Y |                I NV C ON + achieves the highest recall score, reaching 0.80,
          RecallERC20 (RecallERC721 ) =                 ,      (3)
                                                |Y |               and    generates approximately 46 invariants per contract, all of
where precision refers to the proportion of the generated          which      are successfully verified by VeriSol. Notably, I NV C ON
invariants which are correct and recall is the proportion of the   performs      the least favorably in terms of the invariants generated,
ground truth invariants which can be successfully generated.       even      when     compared with I NV C ON + Naive. Specifically,
Since the contract execution trace set ∆ from transaction          I NV   C  ON   produces     the second-highest number of invariants,
histories may only contain a subset of functions invocations,      yet   its recall   score  is significantly lower than that of I NV C ON +
i.e., some functions are never invoked. For a fair comparison,     Naive,      while    maintaining    a similar precision score of less
let Y ⇂ ∆ represent the ground truth invariants for the functions  than     0.1.   The   poor    performance    is primarily attributed to
appeared in the histories, and we use the adjusted recall in our   the   fact   that  I NV C ON  ’s underlying   invariant detection engine,
experiments:
               |Xproved ∩Y |
                             .                                     Daikon,      supports   only    Boolean,  integer/float, and string types
                  |Y ⇂∆|
                                                                   native to Java. Consequently, the address type (20 bytes
   Note that although the ground truth invariants are derived long) in the Solidity language cannot be seamlessly converted
based on multiple external sources and widely deemed to into a Java integer (8 bytes long). Its conversion to the
be standard, they may still be incomplete, as there are Java string type discards semantic information, rendering
infinitely many correct invariants in theory. The purpose of the straightforward production of common invariants (e.g.,
collecting the ground truth invariants is to include the list of a1, a2 in Table II) unattainable for I NV C ON. Additionally,
common expectations that are needed for contract safety and Daikon employs floating-point operations in arithmetic invariant
reliability. On the other hand, certain smart contracts may not templates (e.g., linear equation templates), which is not allowed
faithfully implement the ERC standards, and as a result, either in the Solidity semantics, leading to incorrect invariants for
some ground-truth invariants may not hold for them or they b6, b10 in Table II.
satisfy additional invariants not included in the ground truth.        I NV C ON + Primitive exhibits a slightly lower recall score
Nevertheless, an ideal invariant generation tool should be able than I NV C ON + Naive, because some ground truth invariants
to recover as many ground-truth invariants as possible, and
meanwhile, recover other relevant invariants that are correct         4 https://github.com/UCSB-PLSE/Cider
                                                                                                                                                                     9



                                                          TABLE II: Common ERC20 Invariants.
  Categories                Preconditions                                                Postconditions
  transfer(to, amount)      [a1] msg.sender ̸= 0                                         [b1] to ̸= msg.sender     =⇒      balances[msg.sender] =
                            [a2] to ̸= address(0)                                        old(balances[msg.sender]) - amount
                            [a3] amount ≥ 0                                              [b2] to ̸= msg.sender =⇒ balances[to] = old(balances[to]) + amount
                            [a4] amount ≤ balances[msg.sender]                           [b3] to = msg.sender =⇒ balances[to] = old(balances[to])
                            [a5] balances[to] + amount ≤ MAXVALUE                        [b4] to = msg.sender =⇒ balances[msg.sender] = old(balances[msg.sender])
                                                                                         [b5] totalSupply = old(totalSupply)
  transferFrom (from, to,   [a6] from ̸= address(0)                                      [b6] allowed[from][msg.sender] = old(allowed[from][msg.sender]) - amount
  amount)                   [a7] to ̸= address(0)                                        [b7] from ̸= to =⇒ balances[from] = old(balances[from]) - amount
                            [a8] amount ≥ 0                                              [b8] from ̸= to =⇒ balances[to] = old(balances[to]) + amount
                            [a9] amount ≤ balances[from]                                 [b9] from = to =⇒ balances[from] = old(balances[from])
                            [a10] amt ≤ allowed[from][msg.sender]                        [b10] allowed[from][msg.sender] = old(allowed[from][msg.sender]) - amount
                            [a11] balances[to] + amount ≤ MAXVALUE                       [b11] totalSupply = old(totalSupply)
  approve(spender,          [a12] amount ≥ 0                                             [b12] allowed[msg.sender][spender] = amount
  amount)                   [a13] spender ̸= address(0)                                  [b13] totalSupply = old(totalSupply)
  increaseAllowance(        [a14] spender ̸= address(0)                                  [b14] allowed[msg.sender][spender] = old(allowed[msg.sender][spender]) +
  spender, amount)          [a15] amount ≥ 0                                             amount
                            [a16] allowed[msg.sender][spender] + amount ≤                [b15] totalSupply = old(totalSupply)
                            MAXVALUE
  decreaseAllowance(        [a17] spender ̸= address(0)                                  [b16] allowed[msg.sender][spender] = old(allowed[msg.sender][spender]) -
  spender, amount)          [a18] amount ≥ 0                                             amount
                            [a19] allowed[msg.sender][spender] ≥ amount                  [b17] totalSupply = old(totalSupply)
  mint(account, amount)     [a20] account ̸= address(0)                                  [b18] balances[account] = old(balances[account]) + amount
                            [a21] amount ≥ 0                                             [b19] totalSupply = old(totalSupply) + amount
                            [a22] balances[account] + amount ≤ MAXVALUE
  burn(from, amount)        [a23] from ̸= address(0)                                     [b20] balances[from] = old(balances[from]) - amount
                            [a24] amount ≥ 0                                             [b21] totalSupply = old(totalSupply) + amount
                            [a25] balances[from] ≥ amount
  pause()                   [a26] paused = false                                         [b22] paused = true
  unpause()                 [a27] paused = true                                          [b23] paused = false
  Contract Invariant                                                           [c1] totalSupply = SumMap(balances)


                                                       TABLE III: Common ERC721 Invariants.
  Categories                Preconditions                                                Postconditions
  (safe)-                   [a28] from = tokenOwner[tokenId]                             [b24] from ̸= to =⇒     ownedTokensCount[from] = old( ownedToken-
  transferFrom(from,        [a29] from ̸= address(0)                                     sCount[from]) - 1
  to, tokenId)              [a30] to ̸= address(0)                                       [b25] from ̸= to =⇒      ownedTokensCount[to] = old( ownedToken-
                            [a31] (msg.sender = from ∨ msg.sender =                      sCount[to]) + 1
                              tokenApprovals[tokenId] ∨                                  [b26] from = to =⇒     ownedTokensCount[from] = old( ownedToken-
                              operatorApprovals[from][msg.sender] = true)                sCount[from])
                                                                                         [b27] from = to =⇒      ownedTokensCount[to] = old( ownedToken-
                                                                                         sCount[to])
                                                                                         [b28] tokenOwner[tokenId] = to
                                                                                         [b29] tokenApprovals[tokenId] = address(0)
  approve(to, tokenId)      [a32] tokenOwner[tokenId] ̸= address(0)                      [b30]   tokenApprovals[tokenId] = to
                            [a33] (msg.sender = tokenOwner[tokenId] ∨
                              operatorApprovals[ tokenOwner[tokenId] ][msg.sender]
                            = true)
  setApproveForAll(         [a34] operator ̸= msg.sender                                 [b31]   operatorApprovals[msg.sender][operator] =     approved
  operator, approved)
  Contract Invariant                                                 [c2] len( tokenOwner) = SumMap( ownerTokenCount)


 TABLE IV: The comparison results on ERC20 contracts.                                the token burning functionality. The verified invariants are a
                                                                                     more accurate reflection of the actual contract implementations,
  Tool                       #Inv     Prec.        RecERC20    Avg.time (s)          compared with the likely invariants. Leveraging an algorithm
  I NV C ON                 413.23    0.095            0.19            13.99         capable of producing implications that widely exist in ERC20
  I NV C ON + Naive         480.89    0.094            0.63            15.25         invariants (C.f. Table II), I NV C ON + outperforms all the baseline
  I NV C ON + Primitive      22.49    1.000            0.61            20.57
  I NV C ON +                46.12    1.000            0.80           250.25         tools, yielding 100% precise invariant results.

                                                                                        Regarding the time usage, it is unsurprising that I NV C ON +
that are inferred as likely invariants by I NV C ON + Naive
                                                                                     takes the most time, whereas I NV C ON and I NV C ON + Naive
may not be verified by I NV C ON + Primitive. This may be
                                                                                     finish the fastest. In our experiments, we observed that the
due to contract implementations slightly deviating from the
                                                                                     static inference process consumes the majority of the time,
standard. For example, many ERC20 tokens do not enforce the
                                                                                     constituting nearly 53% of the overall time usage, as depicted
precondition a2 of the transfer function in Table II, because
                                                                                     in Fig. 9. This is primarily due to the iterative application
transferring token to zero address could be used to implement
                                                                                     of static inference until no more implication candidates are
                                                                                                                                             10



 1    /** @dev Creates `amount` tokens and assigns them to                  1   function _transfer(address sender, address recipient,
      ,→   `account`,                                                           ,→  uint256 amount) internal {
 2    *    increasing the total supply.                                     2    require(sender!=address(0), "zero address");
 3    * Requirements                                                        3    require(recipient!=address(0), "zero address");
 4    * - `to` cannot be the zero address.*/                                4
 5    function _mint(address account, uint256 amount) internal              5    _balances[sender]=_balances[sender].sub(amount);
      ,→   {                                                                6    _balances[recipient]=_balances[recipient].add(amount);
 6      require(account != address(0), "ERC20: mint to the zero             7    emit Transfer(sender, recipient, amount);
        ,→   address");                                                     8   }
 7      _totalSupply = _totalSupply.add(amount);                            9   function _approve(address owner, address spender,
 8      _balances[account] = _balances[account].add(amount);                    ,→  uint256 value) internal {
 9      _balances[Account] = _totalSupply/100;                             10    require(owner!=address(0), "zero address");
10    }                                                                    11    require(spender!=address(0), "zero address");
                                                                           12
     Fig. 7: TokenMintERC20Token contract violating c1.                    13    _allowances[owner][spender] = value;
                                                                           14    emit Approval(owner, spender, value);
                                                                           15   }
                                                                           16
TABLE V: The mutation testing results on ERC20 contracts                   17   function transferFrom(address sender, address recipient,
against the verified invariants by I NV C ON +.                                 ,→   uint256 amount) public returns (bool) {
                                                                           18    _transfer(sender, recipient, amount);
  Categories                     approve        transfer   transferFrom    19    _approve(sender, msg.sender,
                                                                                  ,→  _allowances[sender][msg.sender].sub(amount));
  No. total mutants                 1,539          1,141            297    20    return true;
  No. killed mutants         998 (64.8 %)   624 (54.6 %)   101 (34.0 %)    21   }
  P1. Contract invariants    245 (24.5 %)   344 (55.1 %)    55 (54.4 %)
  P2. Function pre/post      763 (76.4 %)   465 (74.5 %)    61 (60.4 %)   Fig. 8: Illustration of the overprotected transferFrom function.
  P3. ERC20 standard         751 (75.2 %)   266 (42.6 %)    43 (42.5 %)
  P4. Non-ERC20 standard     995 (99.7 %)   601 (96.3 %)    98 (97.0 %)   approve, transfer, and transferFrom are successfully killed,
                                                                          respectively.
provided. Moreover, implication invariants generated in later it-            To delve into those killed mutants, in Table V, we use P1,
erations tend to be more intricate, resulting in more complicated         P2, P3, and P4 to denote different types of invariants and
SMT formulas which take more time to solve. To enhance the                the corresponding rows show the number of killed mutants
efficiency of I NV C ON +, we recommend capping the iterations            by these invariants. Although the contract invariants (P1)
used in the verification process to four; under such a setting,           accounts for 24.5 % to 54,4 % of the killed mutants, function
I NV C ON + demonstrates an averaged time savings of one minute           pre/post-conditions (P2) demonstrate a more substantial impact
in the entire verification process without compromising the               occupying at most 76.4 % of the killed mutants. Moreover,
quality of resulting invariants.                                          non-ERC20 standard invariants successfully eliminate nearly
   Additionally, we investigated further on the contracts for             the entire set (96 % more) of the total killed mutants. In
which I NV C ON + generated additional invariants deviating               contrast, ERC20 standard invariants eliminate a smaller set
from the ground-truth ones. Many of these contracts are                   of mutants. This suggests that the invariants generated by
found to be non-compliant with ERC20 specifications. As                   I NV C ON + capture richer program semantics, contributing to a
illustrated in Fig. 7, we examined a real-world contract,                 more comprehensive set of invariant specifications for smart
TokenMintERC20Token5 , where the mint function de-                        contracts.
viates from the contract invariant c1—the sum of account
                                                                             Interestingly, Table V reveals that only 34% of mutants
balances always equals to the total supply—indicating non-
                                                                          related to the transferFrom function are successfully elimi-
compliance with the standard. This discrepancy arises because
                                                                          nated. Upon investigation, we discovered that transferFrom is
only 1% of the total supply tokens have been distributed to
                                                                          overprotected, where one of its function-level preconditions
the Account (Line 9).
                                                                          is redundant. Figure 8 depicts a common implementation of
Invariant Quality. Furthermore, to assess the significance of             transferFrom, facilitating token transfer on behalf of the token
the invariants generated by I NV C ON +, we conducted mutation            owner through two internal functions, transfer and approve.
testing on the same benchmark and computed the corresponding              This design rationale primarily aims at direct code reuse for
mutation scores against these invariants. Table V presents                the other two public functions, transfer and approve. However,
the mutation testing results on ERC20 contracts, specifically             in the transferFrom function, both requirements (Line 2 and
focusing on the three most important functions: approve, trans-           Line 10) check if the sender parameter is a zero address.
fer, and transferFrom. We introduced six mutation operators,              Consequently, mutations on either Line 2 or Line 10 do not
such as binary/unary-op-mutation and require-mutation, along              diminish the requirements that transferFrom should adhere
with the others, based on the mutation generator Gambit [34]              to, resulting in a low mutation score for transferFrom. It is
developed by Certora.6 This mutation-based approach was also              noteworthy that redundant requirements in smart contracts lead
adopted by Certora to evaluate the quality of smart contract              to higher gas consumption during transaction execution and
specifications.7 In total, we generated 1, 539, 1, 141, and 297           should be minimized whenever possible.
mutants for approve, transfer, and transferFrom, respectively.
                                                                               Invariant Crowdsourcing. Less popular smart contracts
Table V shows that 64.8 %, 54.6 %, and 34.0 % mutants of
                                                                               may have scarce transaction histories. For example, many
     5 https://etherscan.io/address/0x62c23c5f75940c2275dd3cb9300289dd30992e59 ERC721 contract instances may not have enough transactions
     6 https://www.certora.com/                                                to infer high-quality invariants. Each contract instance can
     7 https://docs.certora.com/en/latest/docs/gambit/index.html               slightly deviate from the standard specifications, therefore, we
                                                                                                                                                                                                                                                                         11



  TABLE VI: ERC721 invariants generated by I NV C ON +.                                                      InvCon+                     InvCon+ w/o Partial                                                     InvCon+ Primitive
                                                                                                          100.00
  Category             Preconditions            Postconditions
  (safe)-              [a28, a29, a30]          [b24, b25, b26, b27, b28,
                                                                                                           75.00




                                                                                       invariant number
  transferFrom                                  b29]
  approve              [a32]                    [b30]                                                      50.00
  setApproveForAll     [a34]                    [b31]
                                                                                                           25.00
  Contract Invariant                            [c2]

                                                                                                            0.00
       Static Inference




                                                                                                                         200
                                                                                                                         400
                                                                                                                         600
                                                                                                                         800
                                                                                                                       1,000
                                                                                                                       1,200
                                                                                                                       1,400
                                                                                                                       1,600
                                                                                                                       1,800
                                                                                                                       2,000
                                                                                                                       2,200
                                                                                                                       2,400
                                                                                                                       2,600
                                                                                                                       2,800
                                                                                                                       3,000
                                                                                                                       3,200
                                                                                                                       3,400
                                                                                                                       3,600
                                                                                                                       3,800
                                                                                                                       4,000
                          53.03%                Invariant Detection                                                                                      transaction number
                                        6.32%
                                                                            Fig. 10: The averaged number of invariants generated with
                               40.63%                                       different number of transactions.


                                    Implication Inference                                                   InvCon+                      InvCon+ w/o Partial                                                      InvCon+ Primitive
                                                                                                          0.90
Fig. 9: The time usage by different components of I NV C ON +.                                            0.80
                                                                                                          0.70



                                                                              ERC20 recall score
hypothesize that reverse engineering invariants from a single                                             0.60
                                                                                                          0.50
contract and its limited transaction histories is inferior to that
                                                                                                          0.40
from multiple contracts. We validate this hypothesize on a set                                            0.30
of 10 ERC721 contracts, restricting the evaluation to at most                                             0.20
200 transactions per contract. The objective is to examine I N -                                          0.10
V C ON +’s effectiveness in recovering the ground truth invariants                                        0.00
                                                                                                                 200
                                                                                                                       400
                                                                                                                             600
                                                                                                                                   800
                                                                                                                                         1,000
                                                                                                                                                 1,200
                                                                                                                                                         1,400
                                                                                                                                                                 1,600
                                                                                                                                                                         1,800
                                                                                                                                                                                 2,000
                                                                                                                                                                                         2,200
                                                                                                                                                                                                 2,400
                                                                                                                                                                                                         2,600
                                                                                                                                                                                                                 2,800
                                                                                                                                                                                                                         3,000
                                                                                                                                                                                                                                 3,200
                                                                                                                                                                                                                                         3,400
                                                                                                                                                                                                                                                 3,600
                                                                                                                                                                                                                                                         3,800
                                                                                                                                                                                                                                                                 4,000
listed in Table III by combining invariant results from multiple
contracts. Notably, to achieve meaningful combination, every
invariant result will be normalized according to a universal                                                                                       transaction number
ERC721 definition on the name of state variables and the name               Fig. 11: The averaged ERC20 recall score of the invariant
of function input variables.                                                results generated with different number of transactions.
   Table VI presents the combined invariant results from all
ERC721 contracts. It demonstrates that I NV C ON + success-                 transactions and divided them into 20 groups, each subsequent
fully recovers the contract invariants, all postconditions, and             group having 200 more transactions than the previous one.
nearly all preconditions except a31 and a33, which contain                     We utilized I NV C ON + Primitive as the baseline and com-
disjunctions over predicates. Consequently, the combination of              pared with it on the number of verified invariants and the
invariant results from multiple contracts significantly improves            corresponding recall score. Additionally, to explore the effect
the overall recall rate (14/16).                                            of applying the detected partially supported invariant candidates,
                                                                            which hold for a subset of the transaction histories, we
  Answer to RQ1: I NV C ON + is able to reverse engineer
                                                                            compared I NV C ON + with a variant, I NV C ON + w/o Partial,
  standard invariant specifications from contract transaction
                                                                            that does not use these partial candidates. In this experiment,
  histories and takes no more than five minutes per contract.
                                                                            we considered the ground truth invariants from the functions
  Additionally, the uncommon invariants generated for
                                                                            which are observed in the earliest 4,000 transactions, when
  ERC20 contracts capture important program semantics
                                                                            computing the recall score, i.e., RecallERC20 .
  beyond the established standards. Moreover, the evaluation
                                                                               Figure 10 illustrates the number of verified invariants per
  on ERC721 contracts demonstrates the advantage to mine
                                                                            contract corresponding to the use of different transaction history
  common invariants from multiple contracts and their
                                                                            lengths. The impact of transaction history size on the number
  transaction histories.
                                                                            of verified invariants is evident, with I NV C ON + generating
                                                                            the most invariants, followed by I NV C ON + I NV C ON + w/o
                                                                            Partial. This demonstrates that the partially supported invariant
D. RQ2: Impact of Transaction Histories                                     candidates, although do not hold on their own, may be useful
   The length of the transaction histories used can influence               in constructing richer implication invariants. By incorporating
the effectiveness of I NV C ON +. To investigate this impact, we            partial invariant candidates, I NV C ON + captures subtle contract
selected the top 10 ERC20 contracts with the longest transaction            behaviors more effectively, resulting in more comprehensive
histories, ensuring that all the chosen contracts have a history            invariant specifications—approximately two times and one time
of at least 10,000 transactions. In evaluating the influence                more than I NV C ON + w/o Partial and I NV C ON + Primitive,
of transaction history length, we employed the earliest 4,000               respectively.
                                                                                                                               12



   In Fig. 11, the recall score of invariant results is presented     1 function batchTransfer(address[] _receivers,
                                                                        ,→  uint256 _value) public whenNotPaused returns
for varying transaction history lengths. Clearly, all recall scores     ,→  (bool) {
increase with longer transaction histories, as more function          2 uint cnt = _receivers.length;

invocations are observed. Notably, I NV C ON + achieves a higher      3 uint256 amount = uint256(cnt) * _value;
                                                                      4 require(cnt > 0 && cnt <= 20);
recall score compared to the baselines. The figure also indicates     5 require(_value > 0 && balances[msg.sender] >=
a more significant gain in recall score from 200 to 400                 ,→  amount);
transactions, with negligible gains after 400, 1,000, and 2,200       6
                                                                      7  [msg.sender] = balances[msg.sender].sub(amount);
transactions for I NV C ON + Primitive, I NV C ON + w/o Partial,      8  for (uint i = 0; i < cnt; i++) {
and I NV C ON +, respectively. This observed difference suggests       9 balances[_receivers[i]] =

that I NV C ON + has a higher chance of capturing more com-              ,→  balances[_receivers[i]].add(_value);
                                                                      10 Transfer(msg.sender, _receivers[i], _value);
prehensive invariant specifications with increased transaction        11 }
histories. Additionally, to effectively apply I NV C ON +, it is      12 return true;

recommended to use around 2,000 transactions for invariant            13 }

detection.                                                                Fig. 12: batchTransfer function in BEC contract.
  Answer to RQ2: The scale of transaction histories affect
  the invariant results of I NV C ON +, while longer histories    vulnerability is caused by the unchecked multiplication of cnt
  empower I NV C ON + to generate more comprehensive              and value in Line 3. If an attacker calls batchTransfer
  invariant specifications.                                       with a large cnt value, the unsigned integer amount will
                                                                  overflow, potentially allowing the attacker to receive more
                                                                  tokens than intended. However, such a transaction would violate
E. RQ3: Application in Securing Smart Contracts                   invariant c1 in Table II, as the totalSupply would no longer
                                                                  equal to the sum of all balances. Thus, such an attack can be
   The invariants generated by I NV C ON + capture the key
                                                                  effectively prevented, if the generated invariants are enforced
semantics of smart contracts under normal executions, which
                                                                  for each function execution.
may serve as a basis for formal contract specifications. High-
                                                                     I NV C ON + is unable to detect some remarkable mistakes
quality contract specifications have been shown to be effective
                                                                  that totally deviate from programmer expectations. For ex-
in securing smart contracts through runtime validation [14]
                                                                  ample, v11 is a vulnerability that allows any party to
and static verification [26]. To answer RQ3, we evaluated
                                                                  halt the token transfer process. This issue arises from the
I NV C ON + on a set of benchmark contracts from SECBIT [35],
                                                                  modification of the onlyFromWallet modifier, wherein
which contains 25 types of vulnerabilities in real-world ERC20
                                                                  “==” was mistakenly replaced with “!=”. Consequently,
contracts exposed to security attacks that have resulted in
                                                                  anyone other than walletAddress can arbitrarily invoke
significant financial losses.
                                                                  the two permissioned functions: enableTokenTransfer
   Table VII provides an overview of the verification results for
                                                                  and disableTokenTransfer. I NV C ON + failed to de-
the evaluated ERC20 contracts, categorized by vulnerability
                                                                  tect this vulnerability for two primary reasons. First, the
types. It contains information about the overall count of vul-
                                                                  onlyFromWallet function is not specified in the ERC20
nerabilities and the effectiveness of our generated invariants in
                                                                  standard, preventing the application of the existing invariant
detecting them. The benchmark contracts used in our evaluation
                                                                  templates. Second, the contract histories contain many irregular
encompass 9 instances of integer overflow vulnerabilities and
                                                                  behaviors exploiting these functions, hindering I NV C ON + from
16 other vulnerability types. However, certain vulnerabilities
                                                                  inferring correct invariants related to onlyFromWallet.
are beyond the scope of formal specifications, such as v14,
v21, and v24 which are related to constructor naming, v15 and        Answer to RQ3: I NV C ON + is able to detect invariants
v16 which are associated with different Solidity versions, and       that are useful for preventing real-world smart contract
v23 which pertains to function visibility. We focused on the         vulnerabilities. Enforcing invariants in contract executions
remaining 18 types of vulnerabilities. Note that some of the         may ensure the security and reliability of smart contracts.
vulnerabilities identified are beyond the specifications outlined
in the ERC20 standard (see Table II) and they can only be
detected using richer customized specifications.                                       VII. R ELATED W ORK
   For each of vulnerability types, we evaluated the verification    The related works can be broadly categorized into smart
results of the invariants generated by I NV C ON + on the contract security analysis and invariant inference.
corresponding benchmark contracts. We selected the top three
contracts with the highest occurrence of each vulnerability
type and assessed whether the invariants detected by I NV C ON + A. Smart Contract Security Analysis
could prevent the corresponding attacks on these contracts. The      The security analysis primarily focuses on detecting smart
results are shown in Table VII. We found that I NV C ON + was contract vulnerabilities. Common vulnerabilities in smart con-
able to detect all overflow vulnerabilities in the benchmark tracts include integer overflow/underflow [36], reentrancy [37],
contracts. For instance, Fig. 12 demonstrated that I NV C ON + and dangerous delegatecall operations [38]. For instance, in
detected the integer overflow vulnerability (CVE-2018-10299) 2017, the Parity wallet contract was hacked due to missing
in the batchTransfer function of the BEC contract. This protection for the delegatecall operation, a feature that allows
                                                                                                                                      13



        TABLE VII: Common ERC20 vulnerabilities.                    projects still fall victim to security breaches [57]. In our opinion,
                                                                    one root cause is that contract developers and the corresponding
  ID     Vulnerability Types                  Total   Detected      auditors may have divergent expectations on smart contracts,
  v1     batchTransfer-overflow                  13      Yes        which are not easy to pinpoint without sufficient contract specifi-
  v2     totalsupply-overflow                   521      Yes        cations. Therefore, apart from enhancing existing security tools,
  v3     verify-invalid-by-overflow               2      Yes        the invariants generated by I NV C ON + can reinforce contract
  v4     owner-control-sell-price-for-            1      Yes
                                                                    specifications to mitigate the incompleteness and inaccuracy
         overflow
  v5     owner-overweight-token-by-               9      Yes        issues of automated verification and contract auditing.
         overflow
  v6     owner-decrease-balance-by-mint-        487      Yes        B. Invariant Inference
         by-overflow
  v7     excess-allocation-by-overflow            1      Yes            The static and dynamic invariant inference have been well-
  v8     excess-mint-token-by-overflow            9      Yes         studied for traditional programs. ESC/Java [58] is a well-
  v9     excess-buy-token-by-overflow             4      Yes         known static checking tool for Java programs. It leverages
   v10 verify-reverse-in-transferFrom              79       Yes      invariant annotations to define properties in the code, improving
   v11 pauseTransfer-anyone                         1       No       the precision of static checking. ESC/Java’s emphasis on
   v12 transferProxy-keccak256                     10       Yes      invariants helps developers express expectations precisely,
   v13 approveProxy-keccak256                      10       Yes      allowing potential issues to be detected early in development.
   v14 constructor-case-insensitive                 4      N/A
   v15 custom-fallback-bypass-ds-auth               1      N/A       Daikon [11] is a well-known dynamic invariant detection
   v16 custom-call-abuse                          144      N/A       tool to automatically infer likely invariants from program
   v17 setowner-anyone                              3       Yes      executions. Daikon takes program execution traces as input,
   v18 allowAnyone                                  4       Yes      which are typically obtained through testing. These execution
   v19 approve-with-balance-verify                 18       Yes      traces consist of sequences of program states and variable
   v20 check-effect-inconsistency                   1       Yes
                                                                     values observed during the program’s runtime. InvCon [18]
   v21 constructor-mistyping                        4      N/A
   v22 fake-burn                                    2       Yes      was the first tool that generates likely invariants for smart
   v23 getToken-anyone                              3      N/A       contracts. With Daikon as the back-end invariant detection
   v24 constructor-naming-error                     1      N/A       engine, InvCon implemented an intermediary input transformer
                                                                     that coverts historic contract transactions to the compatible
one contract to securely delegate part of its functionality to data trace files accepted by Daikon. In addition, some invariant
another contract. As a result, the attacker gained control of the templates are customized to support unique Solidity features,
wallet and stole 150,000 ETH, valued at approximately $30 e.g., MappingItem.
million USD at the time.                                                There also exist other works related to invariant generation
   These common vulnerabilities have been extensively studied for smart contracts. SolType [15] is a type checking tool
in [13], [39], [40], [41], [42], [43], [44], [45], [46], [47], [48], for Solidity smart contracts. It enables developers to add
[49], [50]. Most static analysis tools, such as Slither [23], refinement type annotations to smart contracts, incorporating
Securify [42], Zeus [47], and Ethainter [40], utilize control- static analysis to prove that arithmetic operations are safe from
flow, data-flow, or taint-flow analysis for vulnerability detection, integer overflows or underflows. SolType can infer useful type
usually achieving a high recall but low precision rate. In annotations, but they are limited to only contract-level invariants
contrast, the others [45], [46], [51] use symbolic execution for related to arithmetic operation. Using SolType as a verifier to
program path exploration to identify contract vulnerabilities, learn a policy, Cider [19] applys deep reinforcement learning
along with a higher precision but lower recall rate. There are to automatically learn contract invariants. The learned contract
also formal verification tools for ensuring the correctness of invariants are mainly used to guard arithmetic operations in
functional properties [16], [17], [52], and workflow policy [26] smart contracts to avoid integer overflows and underflows.
in smart contracts. The dynamic analyses [48], [50], [53], [54], However, the correctness of the learned contract invariants is
[55] perform random or model-based testing on smart contracts still not formally verified.
and then check execution result against predefined oracles for          Distinguished from the aforementioned works, I NV C ON + is
finding a wide range of vulnerabilities. Although these tools the first to implement a unified invariant generation framework
have been proven effective in detecting common vulnerabilities, for Solidity contracts encompassing techniques from both
unfortunately, Zhang et al. [56] found that only 20.5% of real- dynamic detection and static inference, where the the generated
world smart contract bugs can be successfully detected by invariants are verified against the contract code.
state-of-the-art tools. This is because the existing tools use
simple, generic, and hard-coded security patterns or oracles,                              VIII. C ONCLUSION
which are ineffective to recognize subtle logic bugs on specific        We have presented I NV C ON +, a novel invariant generation
contracts.                                                           framework for Solidity smart contracts where the invariants
   Because there is no one-for-all patterns or oracles for          result from the integration between dynamic invariant detec-
identifying contract logic bugs, most valued Web3 projects hire     tion and static inference. Because implication invariants are
third-party security auditing companies to manually review their    important to capture more fine-grained program semantics
contracts. Despite undergoing costly code auditing, numerous        of smart contracts, I NV C ON + devises an iterative process to
                                                                                                                                                                 14



repeat the generation and verification of implications to over-                   [20] “Openzeppelin erc20 contract specifications.” [Online]. Avail-
come its combination explosion problem. We have evaluated                              able: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/
                                                                                       master/certora/specs/ERC20.spec
I NV C ON + on real-world ERC20 and ERC721 contracts and                          [21] “Openzeppelin erc721 contract specifications.” [Online]. Avail-
demonstrated that I NV C ON + is able to achieve good recall to                        able: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/
recover common specifications. In addition, the experiments                            master/certora/specs/ERC721.spec
                                                                                  [22] G. Ros, u, “ERC20-K: Formal Executable Specification of ERC20,”
on mutation testing and vulnerable benchmark contracts have                            Mar. 2023, original-date: 2017-11-20T22:28:46Z. [Online]. Available:
shown that the invariant specifications generated are effective                        https://github.com/runtimeverification/erc20-semantics
to exclude program mistakes and make contracts secure from                        [23] “Slither,” https://github.com/crytic/slither, 2021, the Solidity Source
                                                                                       Analyzer.
vulnerabilities.                                                                  [24] H. Wang, Y. Li, S.-W. Lin, L. Ma, and Y. Liu, “VULTRON: Catching
                                                                                       vulnerable smart contracts once and for all,” in Proceedings of the
                                                                                       41st International Conference on Software Engineering: New Ideas and
                              R EFERENCES                                              Emerging Results (ICSE-NIER). IEEE Press, 5 2019, pp. 1–4.
                                                                                  [25] M. Barnett, B.-Y. E. Chang, R. DeLine, B. Jacobs, and K. R. M. Leino,
 [1] G. Wood, “Ethereum: A secure decentralised generalised transaction                “Boogie: A modular reusable verifier for object-oriented programs,”
     ledger,” Ethereum project yellow paper, vol. 151, pp. 1–32, 2014.                 in Formal Methods for Components and Objects: 4th International
 [2] “Binance Smart Chain,” https://docs.binance.org/smart-chain/guides/bsc-           Symposium, FMCO 2005, Amsterdam, The Netherlands, November 1-4,
     intro.html, 2020, introduction of Binance Smart Chain.                            2005, Revised Lectures 4. Springer, 2006, pp. 364–387.
 [3] T. Chen, Y. Zhang, Z. Li, X. Luo, T. Wang, R. Cao, X. Xiao, and              [26] Y. Wang, S. K. Lahiri, S. Chen, R. Pan, I. Dillig, C. Born, and I. Naseer,
     X. Zhang, “Tokenscope: Automatically detecting inconsistent behaviors             “Formal specification and verification of smart contracts for Azure
     of cryptocurrency tokens in Ethereum,” in Proceedings of the 2019 ACM             blockchain,” arXiv preprint arXiv:1812.08829, 2018.
     SIGSAC conference on computer and communications security, 2019,             [27] M. Research, “Z3,” https://github.com/Z3Prover/z3, 2022, accessed:
     pp. 1503–1520.                                                                    December 15, 2023.
 [4] H.-A. Moon and S. Park, “Conformance evaluation of the top-100               [28] E. Hildenbrandt, M. Saxena, N. Rodrigues, X. Zhu, P. Daian, D. Guth,
     Ethereum token smart contracts with Ethereum Request for Comment-20               B. Moore, D. Park, Y. Zhang, A. Stefanescu et al., “KEVM: A complete
     functional specifications,” IET Software, vol. 16, no. 2, pp. 233–249,            formal semantics of the Ethereum virtual machine,” in 2018 IEEE 31st
     2022.                                                                             Computer Security Foundations Symposium (CSF). IEEE, 2018, pp.
 [5] “EIP-20: A standard interface for tokens,” https://eips.ethereum.org/EIPS/        204–217.
     eip-20, 2015.                                                                [29] X. Li, C. Su, Y. Xiong, W. Huang, and W. Wang, “Formal verification of
 [6] Y. Guo, An Incompatibility in Ethereum Smart Con-                                 bnb smart contract,” in 2019 5th International Conference on Big Data
     tract Threatening dApp Ecosystem, 2018. [Online]. Avail-                          Computing and Communications (BIGCOM). IEEE, 2019, pp. 74–78.
     able: https://medium.loopring.io/an-incompatibility-in-smart-contract-       [30] E. ETL, “Ethereum in BigQuery: a public dataset for smart contract an-
     threatening-dapp-ecosystem-72b8ca5db4da                                           alytics,” https://cloud.google.com/blog/products/data-analytics/ethereum-
 [7] A. Hui, “Ethereum tokens worth $1b vulnerable to ‘Fake Deposit Attack’,”          bigquery-public-dataset-smart-contract-analytics, 2017.
     2020. [Online]. Available: https://www.coindesk.com/tech/2020/08/25/         [31] “Openzeppelin        pausable     contract     specifications.”   [Online].
     ethereum-tokens-worth-1b-vulnerable-to-fake-deposit-attack/                       Available: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/
 [8] “OpenZeppelin,”          https://github.com/OpenZeppelin/openzeppelin-            master/certora/specs/Pausable.spec
     contracts, 2022, openZeppelin contracts.                                     [32] OpenZeppelin, “ERC 20 - OpenZeppelin Docs.” [Online]. Available:
 [9] “Inconsistency between the code and the doc of VestingWal-                        https://docs.openzeppelin.com/contracts/3.x/api/token/ERC20
     let.release,” https://github.com/OpenZeppelin/openzeppelin-contracts/        [33] “ERC 721 - OpenZeppelin Docs.” [Online]. Available: https:
     issues/3368, 2022.                                                                //docs.openzeppelin.com/contracts/2.x/api/token/ERC721
[10] C. Zhu, Y. Liu, X. Wu, and Y. Li, “Identifying Solidity smart contract       [34] Certora, “Gambit: Mutant generation for Solidity,” https://github.com/
     API documentation errors,” in Proceedings of the 37th IEEE/ACM                    Certora/gambit, 2022, accessed: December 9, 2023.
     International Conference on Automated Software Engineering (ASE),            [35] S. Labs, “sec-bit/awesome-buggy-erc20-tokens: A Collection of
     Oct. 2022.                                                                        Vulnerabilities in ERC20 Smart Contracts With Tokens Affected,” Aug.
[11] “Daikon,” http://plse.cs.washington.edu/daikon/, 2021, the Daikon invari-         2018. [Online]. Available: https://github.com/sec-bit/awesome-buggy-
     ant detector.                                                                     erc20-tokens
[12] C. Flanagan and K. R. M. Leino, “Houdini, an annotation assistant            [36] Blockchain-Projects, “Overflow attack in Ethereum smart contracts,”
     for esc/java,” in International Symposium of Formal Methods Europe.               https://blockchain-projects.readthedocs.io/overflow.html, 2020.
     Springer, 2001, pp. 500–517.                                                 [37] D. Siegel, Understanding The DAO Attack, 2016. [Online]. Available:
[13] H. Wang, Y. Liu, Y. Li, S.-W. Lin, C. Artho, L. Ma, and Y. Liu,                   https://www.coindesk.com/understanding-dao-hack-journalists
     “Oracle-supported dynamic exploit generation for smart contracts,” IEEE      [38] P. Santiago, The Parity Wallet Hack Explained, 2017. [Online].
     Transactions on Dependable and Secure Computing, 2020.                            Available: https://blog.openzeppelin.com/on-the-parity-wallet-multisig-
[14] A. Li, J. A. Choi, and F. Long, “Securing smart contract with runtime             hack-405a8c12e8f7/
     validation,” in Proceedings of the 41st ACM SIGPLAN Conference on            [39] J. Feist, G. Grieco, and A. Groce, “Slither: A static analysis framework
     Programming Language Design and Implementation, 2020, pp. 438–453.                for smart contracts,” in 2019 IEEE/ACM 2nd International Workshop
[15] B. Tan, B. Mariano, S. K. Lahiri, I. Dillig, and Y. Feng, “Soltype:               on Emerging Trends in Software Engineering for Blockchain (WETSEB).
     refinement types for arithmetic overflow in solidity,” Proceedings of the         IEEE, 2019, pp. 8–15.
     ACM on Programming Languages, vol. 6, no. POPL, pp. 1–29, 2022.              [40] L. Brent, N. Grech, S. Lagouvardos, B. Scholz, and Y. Smaragdakis,
[16] S. So, M. Lee, J. Park, H. Lee, and H. Oh, “VeriSmart: A highly precise           “Ethainter: a smart contract security analyzer for composite vulnerabilities,”
     safety verifier for Ethereum smart contracts,” in 2020 IEEE Symposium             in Proceedings of the 41st ACM SIGPLAN Conference on Programming
     on Security and Privacy (SP). IEEE, 2020, pp. 1678–1694.                          Language Design and Implementation, 2020, pp. 454–469.
[17] Á. Hajdu and D. Jovanović, “solc-verify: A modular verifier for solidity   [41] S. Tikhomirov, E. Voskresenskaya, I. Ivanitskiy, R. Takhaviev,
     smart contracts,” in Verified Software. Theories, Tools, and Experiments:         E. Marchenko, and Y. Alexandrov, “Smartcheck: Static analysis of
     11th International Conference, VSTTE 2019, New York City, NY, USA,                Ethereum smart contracts,” in Proceedings of the 1st International
     July 13–14, 2019, Revised Selected Papers 11. Springer, 2020, pp.                 Workshop on Emerging Trends in Software Engineering for Blockchain,
     161–179.                                                                          2018, pp. 9–16.
[18] Y. Liu and Y. Li, “Invcon: A dynamic invariant detector for ethereum         [42] Securify, Sofware Reliability Lab, 2019. [Online]. Available: https:
     smart contracts,” in Proceedings of the 37th IEEE/ACM International               //securify.ch/
     Conference on Automated Software Engineering, 2022, pp. 1–4.                 [43] Y. Feng, E. Torlak, and R. Bodik, “Precise Attack Synthesis for Smart
[19] J. Liu, Y. Chen, B. Tan, I. Dillig, and Y. Feng, “Learning contract               Contracts,” arXiv preprint arXiv:1902.06067, 2019.
     invariants using reinforcement learning,” in Proceedings of the 37th         [44] L. Luu, D.-H. Chu, H. Olickel, P. Saxena, and A. Hobor, “Making smart
     IEEE/ACM International Conference on Automated Software Engineering,              contracts smarter,” in Proceedings of the 2016 ACM SIGSAC conference
     2022, pp. 1–11.                                                                   on computer and communications security. ACM, 2016, pp. 254–269.
                                                                                  15



[45] “Manticore,” https://github.com/trailofbits/manticore, 2019, symbolic
     Execution Tool for Smart Contracts.
[46] “Mythril,” https://github.com/ConsenSys/mythril, 2019, a Security Anal-
     ysis Tool for EVM Bytecode.
[47] S. Kalra, S. Goel, M. Dhawan, and S. Sharma, “Zeus: Analyzing safety
     of smart contracts,” in Ndss, 2018, pp. 1–12.
[48] B. Jiang, Y. Liu, and W. Chan, “Contractfuzzer: Fuzzing smart contracts
     for vulnerability detection,” in Proceedings of the 33rd ACM/IEEE
     International Conference on Automated Software Engineering. ACM,
     2018, pp. 259–269.
[49] V. Wüstholz and M. Christakis, “Harvey: A greybox fuzzer for smart
     contracts,” in Proceedings of the 28th ACM Joint Meeting on European
     Software Engineering Conference and Symposium on the Foundations of
     Software Engineering, 2020, pp. 1398–1409.
[50] Echidna, Trail of Bits, 2019. [Online]. Available: https://github.com/
     trailofbits/echidna
[51] “Oyente,” https://github.com/melonproject/oyente, 2019, an Analysis Tool
     for Smart Contracts.
[52] A. Permenev, D. Dimitrov, P. Tsankov, D. Drachsler-Cohen, and
     M. Vechev, “Verx: Safety verification of smart contracts,” in 2020 IEEE
     symposium on security and privacy (SP). IEEE, 2020, pp. 1661–1677.
[53] H. Wang, Y. Liu, Y. Li, S.-W. Lin, C. Artho, L. Ma, and Y. Liu,
     “Oracle-supported dynamic exploit generation for smart contracts,” IEEE
     Transactions on Dependable and Secure Computing, 2020.
[54] T. D. Nguyen, L. H. Pham, J. Sun, Y. Lin, and Q. T. Minh, “sfuzz: An
     efficient adaptive fuzzer for solidity smart contracts,” in Proceedings of
     the ACM/IEEE 42nd International Conference on Software Engineering,
     2020, pp. 778–788.
[55] Y. Liu, Y. Li, S.-W. Lin, and C. Artho, “Finding permission bugs in
     smart contracts with role mining,” in Proceedings of the 31st ACM
     SIGSOFT International Symposium on Software Testing and Analysis
     (ISSTA). New York, NY, USA: ACM, Jul. 2022, pp. 716–727.
[56] Z. Zhang, B. Zhang, W. Xu, and Z. Lin, “Demystifying exploitable bugs
     in smart contracts.” ICSE, 2023.
[57] Sayfer, “3 Hacks an Audit Could Not Find,” https://sayfer.io/blog/3-
     hacks-an-audit-could-not-find/, 2023, accessed: December 18, 2023.
[58] C. Flanagan, K. R. M. Leino, M. Lillibridge, G. Nelson, J. B. Saxe,
     and R. Stata, “Extended static checking for java,” in Proceedings of the
     ACM SIGPLAN 2002 Conference on Programming language design and
     implementation, 2002, pp. 234–245.
