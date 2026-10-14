                                                  Certifying optimal MEV strategies with Lean
                                                        Massimo Bartoletti                        Riccardo Marchesin                          Roberto Zunino
                                                       University of Cagliari                      University of Trento                      University of Trento
                                                          Cagliari, Italy                             Trento, Italy                             Trento, Italy
                                                           bart@unica.it                       riccardo.marchesin@unitn.it                 roberto.zunino@unitn.it




                                            Abstract—Maximal Extractable Value (MEV) refers to a class           In both cases, the adversary wins if the value extracted exceeds
                                         of attacks to decentralized applications where the adversary            the value paid to mount the attack.
                                         profits by manipulating the ordering, inclusion, or exclusion
                                                                                                                    Playing the role of defender is substantially harder: to
                                         of transactions in a blockchain. Decentralized Finance (DeFi)
                                                                                                                 guarantee that the value extractable from a contract is bounded
arXiv:2510.14480v1 [cs.CR] 16 Oct 2025




                                         protocols are a primary target of these attacks, as their logic
                                         depends critically on transaction sequencing. To date, MEV              by a given threshold v, one must ensure that no adversarial
                                         attacks have already extracted billions of dollars in value, under-     strategy — among an infinite set of possible strategies —
                                         scoring their systemic impact on blockchain security. Verifying         can extract more than v. More abstractly, let EV(σ, v) be a
                                         the absence of MEV attacks requires determining suitable upper
                                                                                                                 predicate stating that in system state σ the extractable value is
                                         bounds, i.e. proving that no adversarial strategy can extract
                                         more value (if any) than expected by protocol designers. This           bounded from above by v. Then, the adversary’s task reduces
                                         problem is notoriously difficult: the space of adversarial strategies   to falsification: finding a counterexample to EV(σ, v), by
                                         is extremely vast, making empirical studies and pen-and-paper           exhibiting a strategy that extracts some v ′ > v. Instead, the
                                         reasoning insufficiently rigorous. In this paper, we present the        defender task amounts to verification: constructing a proof that
                                         first mechanized formalization of MEV in the Lean theorem
                                                                                                                 EV(σ, v) indeed holds.
                                         prover. We introduce a methodology to construct machine-
                                         checked proofs of MEV bounds, providing correctness guarantees             From this perspective, establishing MEV requires the same
                                         beyond what is possible with existing techniques. To demonstrate        fundamental ingredients as program verification, namely:
                                         the generality of our approach, we model and analyse the MEV
                                                                                                                  1) a formal model of the system under analysis, i.e., smart
                                         of two paradigmatic DeFi protocols. Notably, we develop the first
                                         machine-checked proof of the optimality of sandwich attacks in              contracts executed on blockchains;
                                         Automated Market Makers, a fundamental DeFi primitive.                   2) a precise formalization of the property of interest, i.e.,
                                            Index Terms—smart contracts, MEV, decentralized finance,                 EV(σ, v);
                                         interactive theorem proving, Lean 4                                      3) a proof technique to determine whether a system satisfies
                                                                                                                     or not the property.
                                                                I. I NTRODUCTION                                    While the literature proposes several formal models of
                                            Public permissionless blockchains such as Ethereum cur-              contracts at different levels of abstraction — ranging from the
                                         rently handle billions of dollars in crypto-assets, controlled by       low-level Ethereum Virtual Machine [8], [9], [10] to the high-
                                         smart contracts that implement increasingly complex financial           level contract language Solidity [11], [12], [13] — the existing
                                         applications. In most cases, the underlying protocols of these          MEV formalizations and the associated proof techniques are
                                         blockchains do not enforce transaction order fairness, instead          not fully adequate for the purpose. The problem is twofold:
                                         delegating the sequencing of user transactions to miners or               • First, most existing definitions [14], [15], [16] lack the
                                         validators. This leaves decentralized applications vulnerable to            precision needed to establish MEV, as they often omit
                                         Maximal Extractable Value (MEV) attacks, where adversaries                  key aspects of adversarial capabilities such as eavesdrop-
                                         manipulate transaction sequencing for profit. While MEV                     ping the transaction mempool [17]. We emphasize that,
                                         extraction may have some beneficial effects — such as reduc-                from a defender’s perspective, the accuracy of a MEV
                                         ing transaction fees [1] — its overall impact is detrimental                formalization is crucial to ensure that no class of attacks
                                         on the affected blockchains, undermining decentralization,                  is overlooked.
                                         transparency, and exacerbating network congestion [2], [3].               • Second, as noted above, establishing precise MEV bounds
                                            MEV can be approached from two different perspectives,                   requires considering all sequences of transactions that
                                         depending on whether one plays the role of attacker or                      an adversary can construct using their private knowledge
                                         defender. For an attacker, the fact that the value extracted is             and the content of the transaction mempool. Although
                                         maximal is not really relevant. What truly matters is having                in many cases this infinite set of adversarial strategies
                                         an efficient algorithm to bundle one’s own transactions with                can be partitioned into a finite number of equivalence
                                         those of other users in a way that guarantees profit. For that              classes, the resulting combinatorial explosion of cases and
                                         purpose, the attacker can exploit known heuristics targeting                subcases quickly becomes unmanageable. This explosion
                                         specific contracts [4], [5], [6], or devise adaptive techniques             occurs even for relatively simple contracts, where just a
                                         that can potentially extract value from arbitrary contracts [7].            handful of system variables already gives rise to a vast
     and intricate strategy space, well beyond the reach of         contract AirDrop {
     reliable pen-and-paper proofs.                                   constructor() payable { // receive tokens from the sender
                                                                          require (msg.value > 0);
   To address these challenges, it is necessary to devise a           }
MEV formalization that is (i) precise enough to capture               function drop(uint v) public {
all possible adversarial strategies, (ii) flexible enough to ac-          address payable rcv = payable(msg.sender);
commodate a wide range of use cases, and (iii) amenable                   rcv.transfer(v); // transfer tokens to the sender
to rigorous, machine-verified proofs that go beyond manual            }
                                                                    }
analysis. Proof assistants provide a natural framework to meet
these requirements, as they enable precise formalizations of                       Fig. 1. An Airdrop contract in Solidity.
software systems and support the construction of machine-
verified proofs whose correctness is guaranteed beyond any
reasonable doubt. In the context of MEV, they offer the               Our Lean implementation, including all the proofs and
potential to reason about adversarial strategies, automate parts    case studies are available online in a public repository [26]
of the verification process, and ensure a level of rigour           consisting of ∼7000 lines of code.
that manual analysis cannot achieve. However, despite its                            II. BACKGROUND ON MEV
central role in the security of decentralized applications, no
                                                                       At an abstract level, we can see a blockchain as a transition
mechanized formalization of MEV has been developed so
                                                                    system, where states represent both users’ wallets (i.e., their
far. Existing studies rely on informal arguments, which are
                                                                    token holdings) and the states of deployed contracts (including
insufficient to provide guarantees of correctness. This leaves a
                                                                    their balances). State transitions are triggered by transactions
critical gap between the theoretical understanding of MEV and
                                                                    sent by users: a transaction may affect the sender’s wallet, the
the practical need for security of decentralized applications.
                                                                    state of the called contracts, and the wallets receiving tokens
      Contributions: This paper addresses the previous re-          from those contracts (if any).
search questions by providing the following key contributions:         As a concrete example, consider an Airdrop contract that
 1) we provide the first fully mechanised formalization of          allows any user to withdraw tokens from its balance. We
    MEV in a proof assistant (§III). To this purpose, we            specify this contract in Solidity in Figure 1. Deploying the
    adopt Lean 4 [18], an open-source theorem prover and            contract requires the sender to transfer any positive amount
    programming language that has been successfully applied         of tokens from its wallet to the contract. In this case, the
    to construct and verify large-scale proofs [19]. Its exten-     tokens correspond to the blockchain native cryptocurrency
    sive mathematical library makes Lean 4 particularly well        (e.g., ETH on Ethereum), and they are quantified by the
    suited for reasoning about DeFi contracts, which often          expression msg.value. Besides the constructor, the contract
    involve complex mathematical manipulations.                     only features another function, drop, which allows any user
 2) we devise a new proof technique for establishing MEV.           (identified by msg.sender) to withdraw an arbitrary fraction
    Roughly, given a system state σ where MEV is to be              of the contract balance. The contract state only consists of its
    estimated, our proof technique requires the defender to         balance, which is implicitly updated when receiving tokens (in
    provide a “guess” function mapping each state to a can-         the constructor) or sending them (in the transfer command).
    didate MEV amount. The defender must then prove that               MEV quantifies the maximal gain that an adversary can
    (i) the guess for the initial state is an under-approximation   obtain by exploiting their power to reorder, drop, or insert
    of MEV, and (ii) any adversarial move affects the guess         transactions in the blockchain. To this end, the adversary can
    by an amount which is bounded by the gain of the move.          play both pending user transactions in the public mempool,
    We establish that our proof technique is sound — i.e.,          and may also inject its own crafted transactions, potentially
    when such a guess function exists, it actually gives the        leveraging knowledge of the mempool contents.
    MEV — and complete — i.e., when the MEV exists, a                  In our working example, assume a system state σ consisting
    guess function exists.                                          of the sole Airdrop contract with a balance of n > 0 tokens,
 3) we apply our proof technique to two paradigmatic case           which for simplicity we assume to have unitary price. Any
    studies. The first is a gambling game in which players          adversary can simply fire a drop(n) transaction to empty the
    can win a prize by depositing suitable amounts of tokens.       contract balance: therefore, the MEV in σ is exactly n. Note
    Despite its apparent simplicity, this case study highlights     that the Airdrop’s MEV is not necessarily “bad MEV”, since
    how different adversarial strategies can emerge depending       the extraction of value is aligned with the intended function-
    on the contents of the transaction mempool (§V). The            ality of the contract. However, an adversary with transaction
    second contract is an Automated Market Maker (AMM),             sequencing powers can always front-run drop transactions of
    one of the cornerstones of Decentralized Finance [20],          honest users, depriving them of any gain. In the rest of the
    [21]. Although the MEV of AMMs has been studied                 section, we will examine cases of “bad MEV” where the
    before [22], [23], [24], [25], our work provides the first      adversary causes a loss to honest users.
    mechanized proof that so-called sandwich attacks extract           In the previous case, the adversary does not need to exploit
    the maximal possible value (§VI).                               the mempool, but just to front-run other users’ transactions
contract CoinPusher {                                              contract AMM {
  function push() public payable {                                   uint r0, r1; // reserves of token types t0, t1
    if (address(this).balance >= 100) {
      address payable rcv = payable(msg.sender);                       constructor(uint n0, uint n1) {
      rcv.transfer(address(this).balance);                               t0.transferFrom(msg.sender, address(this), n0);
    }                                                                    t1.transferFrom(msg.sender, address(this), n1);
  }                                                                      r0 = n0; r1 = n1;
}                                                                      }
                                                                       function swap0(uint n0, uint x1_min) {
              Fig. 2. A CoinPusher contract in Solidity.                 t0.transferFrom(msg.sender, address(this), n0);
                                                                         x1 = (n0 * r1) / (r0 + n0); // compute output tokens
                                                                         require x1>=x1_min && x1<r1;
(this is called displacement attack in [27]). More sophisticated         t1.transfer(msg.sender, x1);
forms of MEV arise when the adversary exploits pending                   r0 = r0 + n0; r1 = r1 - x1;
transactions in the mempool, e.g. by constructing bundles that         }
combine users’ transactions with adversarial ones. We will             function swap1(uint n1, uint x0_min) {
                                                                         // symmetric to swap0
see in the rest of the section how these strategies make the
                                                                       }
estimation of MEV increasingly more complex.                       }
A. The CoinPusher contract                                              Fig. 3. A constant-product AMM contract in Solidity (simplified).
   We now consider a case where extracting MEV requires the
adversary to leverage transactions pending in the mempool.
The CoinPusher contract transfers its entire balance to any           For illustration, we present in Figure 3 a simplified Solidity
user whose deposit causes the balance to exceed 100 tokens         code of the AMM contract (an actual implementation is
( Figure 2). The contract has a single function push, which        substantially more complex, e.g. because it has to deal with
receives from the sender any amount msg.value of tokens (this      rounding of integer operations). The constructor initializes
transfer happens implicitly along with the call). If the incom-    the reserves of tokens t0 and t1 , which are transferred from
ing tokens make the contract balance exceed 100 units, the         the sender’s wallet to the contract. The function swap0 allows
entire balance (including the incoming tokens) is immediately      anyone to send n0 units of t0 and receive at least x1_min units
sent to the caller through the transfer command.                   of t1 . The function swap1 is symmetric: it takes t1 as input
   Let σ be a system state where the contract holds 0 tokens       and outputs t0 . The exchange rate follows the mechanism
and a user A holds 1 token. We assume the adversary Adv to         of Uniswap v2 [30], which maintains the product of reserves
be wealthy, i.e. endowed with enough tokens to mount any           (i.e., r0 · r1) constant across swaps. This guarantees that the
feasible attack (in practice, Adv can also obtain such tokens      marginal exchange rate (i.e., the one applied for infinitesimal
as a very short-term loan, even if that might cost of some         swaps) coincides with the ratio between the reserves.
additional fees). If the mempool in σ is empty, then Adv cannot       When external prices are not aligned with the marginal
extract any value, hence MEV(σ) = 0. Now suppose that the          exchange rate — i.e., when r0 · price(t0 ) ̸= r1 · price(t1 )
mempool contains a transaction sent by A that calls push while     — a strategy to extract value is to perform an arbitrage, i.e. fire
transferring 1 token — written A : push(value=1). In this case,    a swap that realigns the reserves with external prices. For ex-
Adv can atomically execute the transaction bundle:                 ample, let σ be a state where price(t0 ) = 4, price(t1 ) = 9,
                                                                   and the AMM reserves are of 6 units of each token, written:
       A : push(value = 1)        Adv : push(value = 99)
                                                                               σ = AMM[6 : t0 , 6 : t1 ] | Adv[n0 : t0 , n1 : t1 ]
which yields a gain of 1 to Adv. Since no strategy achieves
a higher gain, we conclude that MEV(σ) = 1. Devising an            If the adversary calls swap0(3,0), the state becomes:
optimal strategy for an arbitrary contract when the mempool                  AMM[9 : t0 , 4 : t1 ] | Adv[n0 − 3 : t0 , n1 + 2 : t1 ]
contains many transactions is hard, also due to the combi-
natorial explosion of possible interleavings. In the CoinPusher    The resulting AMM is balanced, and the adversary has paid 3
case, the adversary’s optimal strategy is to include the pending   units of t0 (with value 3 · 4 = 12) to buy 2 units of t1 (with
mempool transactions while interleaving its own push calls. In     value 2 · 9 = 18). So, overall Adv has gained 18 − 12 = 6.
the idealized case where there are no transaction fees, this can   One of our contributions (§VI-A) is a machine-checked proof
yield a gain equal to the contract balance in σ plus the total     that arbitrage is indeed the optimal MEV-extracting strategy
value of those mempool transactions with value < 100.              when the mempool is empty.
                                                                      If the mempool is nonempty, more complex strategies arise,
B. Automated Market Makers                                         which potentially give a higher MEV. A typical strategy is the
   We now consider an Automated Market Maker (AMM), an             so-called sandwich attack [22], which we illustrate in the same
archetypal decentralized finance (DeFi) primitive that enables     state σ as before. Assume that a honest user A has sent an
users to swap between two token types according to an              arbitrage transaction A : swap0(3, 1) to the mempool. Here, A
algorithmically defined exchange rate [20], [28], [29].            has set the parameter x1_min to 1, enforcing a lower bound on
the number of t1 units received from the swap. This safeguard            We parametrize these types by Token, a type representing the
is meant to account for the uncertainty of the state in which a          token types:
transaction will be actually executed — an inherent problem in
account-based blockchains. In a sandwich attack, the adversary           def Wallet    (Token : Type) : Type := Token → R≥0
                                                                         def WalletAdv (Token : Type) : Type := Token → R
has access to the mempool (containing A’s arbitrage), and uses
it to construct the following transaction bundle:
                                                                            We parameterise our model with a type State, which
  1) Adv : swap0(3, 0), an arbitrage transaction performed by
                                                                         represents the state of an arbitrary contract running in an
      the adversary;
                                                                         honest environment. This parameter will be instantiated when
  2) A : swap0(3, 1), the transaction picked from the mempool.
                                                                         defining specific contracts, e.g. in §III-B, §V and §VI. Intu-
      Since A’s transaction is executed in a state where the
                                                                         itively, such State comprises the contract variables, its wallet,
      AMM is in equilibrium, A will not receive the 2 units
                                                                         the wallets of the honest participants, and the mempool.
      they would have expected in σ: rather, they receive the
      minimum of t1 units admitted by the constraint x1_min,                We model the interactions between the adversary, the honest
      i.e. only 1 unit. This causes A to have a negative gain;           participants, and the contract as a state transition system.
  3) Adv : swap1(1, 3). The adversary closes the sandwich                Its states are types SysState, consisting of a State and the
      with another arbitrage transaction, after which the AMM            adversary’s wallet:
      reaches again the equilibrium.
                                                                         structure SysState {Token State : Type} where
   Overall, executing this transaction bundle in σ leads to:               ∆ : WalletAdv Token
                                                                           s : State
         AMM[6 : t0 , 6 : t1 ] | Adv[n0 : t0 , n1 : t1 ] | · · ·
   (1)
  −−→ AMM[9 : t0 , 4 : t1 ] | Adv[n0 − 3 : t0 , n1 + 2 : t1 ] | · · ·       The rules of the transition system are defined by the
   (2)                                                                   structure System (Figure 4), which specifies the types:
  −−→ AMM[12 : t0 , 3 : t1 ] | Adv[n0 − 3 : t0 , n1 + 2 : t1 ] | · · ·
   (3)                                                                     • Token, representing the possible token types exchanged
  −−→ AMM[9 : t0 , 4 : t1 ] | Adv[n0 : t0 , n1 + 1 : t1 ] | · · ·            within the system;
   This gives the adversary a gain of 1 · price(t1 ) = 9,                  • State, mentioned above;

which is greater than the gain obtainable without exploiting               • Move, representing the possible adversarial moves, e.g.,

the mempool, and it actually turns out to be the MEV in σ.                   crafting and executing a transaction, or fetching from the
More in general, devising the optimal MEV-extracting strategy                mempool a transaction sent from an honest participant
depends on a multitude of factors: the AMM reserves, the                     and executing it.
external token prices, the direction of the swap in the mempool             A System must provide a semantics for adversarial moves
(i.e., swap0 vs. swap1), as well as the swap amount and lower            (note that honest participant’s moves are already taken into
bound. The resulting combinatorial explosion of cases and                account by the transactions in the mempool). The semantics
subcases makes manual reasoning about MEV extremely error-               is a partial function, mapping a SysState and a Move to a
prone. Our machine-checked proof in Lean (§VI-B) addresses               new SysState. The semantics is undefined (none) when it
this complexity, by establishing the MEV when the adversary              is impossible to perform the given move. In practice, this
can exploit a transaction from the mempool.                              corresponds to the case where a transaction reverts.
                         III. S YSTEM MODEL                                 In order to prove general properties on Systems — i.e.,
   In this section, we introduce our Lean formalization of smart         properties that do no depend on the specific instantiation of its
contracts executed on blockchains (§III-A). We illustrate it by          semantics — we require a few more fields and assumptions.
formalizing the Airdrop contract presented in §II (§III-B).              First, System must provide a function (honTokens) mapping
                                                                         each State to the cumulative amount of tokens owned by the
A. System state                                                          contract and honest participants (hereafter, referred to as the
   A wallet is a container of tokens, possibly of different              “honest tokens”). Second, we postulate that the semantics
types. We model wallets as functions from token types to real-           preserves tokens: we model this through the assumption
valued amounts. We explicitly separate the adversary from                preserveTokens, which forbids the minting and the burning of
honest users, reflecting the different assumptions we make               tokens. Finally, a System must associate each token type with
about their capabilities. In particular, we assume our adversary         a price: formally, this is modelled as a function tokenValue
to be wealthy, i.e., able to spend arbitrarily large amounts of          that maps any wallet to a real number, denoting the cumulative
tokens when mounting an attack. Honest participants, instead,            price of all the tokens in the wallet. We require this value
own a limited amount of tokens, as in the real world. We                 function to be non-negative and additive.
formalize these assumptions by defining two distinct wallet                 Given sys : System, we can then prove a few basic prop-
types: Wallet, holding a non-negative amount of tokens for               erties. For instance, we establish that the value of the empty
honest participants and contracts, and WalletAdv, holding                wallet is zero, and that the value function preserves subtraction
arbitrary token amounts (possibly negative) for the adversary.           and is monotonic on wallets.
structure System where                                            not malleable, i.e. the adversary cannot alter the parameter v
  Token : Type                                                    without invalidating the signature.
  State : Type                                                       The State type is a structure that denotes the state of
  Move : Type                                                     the blockchain without the adversary. More specifically, the
  semantics : @SysState Token State → Move →
                                                                  field bal represents the contract’s balance, while the field
    Option (@SysState Token State)
  honTokens : State → Wallet Token                                wal denotes the aggregated wallets of all honest participants.
  preserveTokens : ∀ σ m,                                         Since MEV analysis does not require distinguishing between
    match semantics σ m with                                      individual honest users, their holdings are abstracted into this
    | .none    => True                                            single cumulative wallet. The field mempool represents the
    | .some σ’ => ∀ τ , honTokens σ.s τ + σ.∆ τ                   transactions previously broadcast by honest participants but
                     = honTokens σ’.s τ + σ’.∆ τ
                                                                  not yet finalised on-chain. Formally, we represent the mempool
  tokenValue : WalletAdv Token → R
  tokenValue_nonneg : ∀ f, f ≥ 0 → tokenValue f ≥ 0               as an association list mapping transaction identifiers (TxId)
  tokenValue_additive : ∀ f g,                                    with their associated transactions.
    tokenValue (f + g) = tokenValue f + tokenValue g              structure State where
                                                                    bal : Token → R≥0
                  Fig. 4. System model in Lean.
                                                                    wal : Wallet Token
                                                                    mempool : AssocList TxId Tx

theorem tokenValue_zero : sys.tokenValue 0 = 0
                                                                    We abbreviate the associated system state as ADState:
theorem tokenValue_sub (f g : WalletAdv _) :
     sys.tokenValue (f - g)                                       abbrev ADState := @SysState State Token
  = sys.tokenValue f - sys.tokenValue g
theorem tokenValue_monotonic (f g : WalletAdv _) :                   We now turn to defining the type of adversarial moves. To
  f ≤ g → sys.tokenValue f ≤ sys.tokenValue g                     this aim, we start by identifying the subset of transactions
                                                                  that can be crafted by the adversary alone. In our scenario,
   For readability, hereafter we abbreviate SysState, instanti-   the adversary can only craft drop transactions signed by Adv
ated with sys.Token and sys.State, as sys.sysState:               itself. This is formalized by property advTx.
abbrev System.sysState : Type :=                                  inductive advTx : Tx → Prop
  @SysState sys.Token sys.State                                   | drop {v} : advTx (.drop .Adv v)

B. Example: formalization of the Airdrop contract                    The Move type captures all possible adversarial actions,
   We exemplify our Lean formalization to model the Airdrop       namely: (i) craft a transaction using its own knowledge (i.e.,
contract introduced in Section II. We start by providing some     Adv’s private key) and append it directly to the blockchain
general definitions regarding the participants, the exchanged     (adv), or (ii) select a transaction from the mempool and include
tokens, and the the transactions. This skeleton will be reused    it in the blockchain (mempool).
also for the other use cases.                                     inductive Move
   We define a type Participant to describe who can interact      | adv : (t : Tx) → advTx t → Move
with the contract. The type comprises infinitely many honest      | mempool : TxId → Move
participants and an adversary.
                                                                     The semantics of a Move is to cause an ADState update,
inductive Participant                                             or fail, coherently with System.semantics. More precisely,
| Hon : String → Participant
                                                                  an adv move transfers the specified amount of tokens to the
| Adv : Participant
                                                                  adversary, removing tokens from the contract balance (bal)
   The type Token denotes the token types exchangeable            and adding them to the adversary’s (∆, in the system state),
through the contract. Our Airdrop uses a single token type:       accordingly. If there are not enough tokens in bal, the move
                                                                  has no effect.
inductive Token
| τ 0 : Token
                                                                     Instead, a mempool move looks up the corresponding transac-
                                                                  tion in the State.mempool field. If there is no such transaction,
   Coherently with the Solidity code in Figure 1, the Airdrop     the move has no effect. Otherwise, if we find a corresponding
contract features a single function drop, which allows any        drop P v transaction, we attempt to execute it, sending v
participant P to withdraw any amount v > 0 of tokens              tokens to P. If there are not enough tokens in bal, the move has
from the contract, failing if v exceeds the contract balance.     no effect. Otherwise, we update the contract balance (bal) and
Correspondingly, transactions will take the following form:       P’s wallet. We distinguish between two cases: if P is honest,
inductive Tx
                                                                  then we update wal, while if it is the adversary we update ∆.
| drop (P : Participant) (v : R+) : Tx                            If the mempool transaction succeeds, it is removed from the
                                                                  mempool field so that it is not reused later on.
   The argument P in a drop transaction implicitly denotes that      Using the above semantics, we define the Airdrop type
the transaction is signed by P. We assume that transactions are   as a System modelling the whole contract. While doing that,
we define the Airdrop.honTokens field, which counts all the          theorem gainMoves_empty (σ : sys.sysState) :
circulating tokens not owned by Adv, by essentially summing            gainMoves sys s [] = 0
bal and wal. We also price the token type τ0 , thereby
defining the Airdrop.tokenValue function which assigns a             theorem gainMoves_step (σ : sys.sysState)
                                                                       (m : sys.Move) (ms : List sys.Move) :
value to any wallet. We finally prove the required properties            gainMoves sys σ (m :: ms)
according to the other System fields, i.e., preserveTokens,              = match sys.semantics σ m with
tokenValue_nonneg, and tokenValue_additive.                              | .none    => gainMoves sys σ ms
                                                                         | .some σ’ => gainState sys σ σ’ + gainMoves sys σ’ ms
def Airdrop : System where ...
                                                                       The gain of a list of moves is bounded above by the value
   Based on this system model, we will analyse the MEV of            of all the circulating honest tokens. This will be exploited to
the Airdrop contract in §IV-D.                                       obtain an upper bound to the extractable value.
                                                                     theorem gainMoves_bound (σ : sys.sysState)
                                                                         (tr : List sys.Move) :
                           IV. MEV
                                                                       gainMoves sys σ tr ≤ sys.tokenValue (sys.honTokens σ.s)

   In this section we present our Lean formalization of MEV
and a general proof technique for certifying the MEV of              B. MEV definition
contracts. We start in §IV-A by defining the gain of the                A system state σ has MEV equal to v when two conditions
adversary upon performing moves, which is the basis for              are met: (i) there is a list of moves tr that, when performed
defining MEV later in §IV-B. In §IV-C we introduce our proof         in σ , gives the adversary a gain of v; (ii) any list of moves tr,
technique in the form of a MEV characterization theorem.             when performed in σ , gives the adversary a gain of at most v:
We illustrate such technique in §IV-D, by applying it to our
                                                                     structure MEV (σ : sys.sysState) (v : R) : Prop where
Airdrop contract.                                                      trace_reaches_v :    ∃ tr, gainMoves sys σ tr = v
                                                                       other_traces_worse : ∀ tr, gainMoves sys σ tr ≤ v

A. Gain                                                                 We remark that MEV is not always guaranteed to exist. For
                                                                     instance, if the adversary can extract any real value < 1, but
   We define the adversarial gain between two system states as
                                                                     they cannot extract 1, there is no maximum value that can
the difference of the adversarial wallets. A simple transitivity-
                                                                     be extracted, but only a least upper bound. To account for
like property follows.
                                                                     this, we also define the “least upper bound of the extractable
def gainState (σ σ’ : sys.sysState) : R :=                           values” MEVsup. The definition only requires traces whose
  sys.tokenValue σ’.∆ - sys.tokenValue σ.∆
                                                                     gain is arbitrarily close to v. We prove that MEVsup always
theorem gainState_trans (σ σ’ σ’’ : sys.sysState) :
                                                                     exists, is unique, and non-negative. Further, when MEV exists,
  gainState sys σ σ’ + gainState sys σ’ σ’’                          it coincides with MEVsup, so MEV is unique and non-negative.
  = gainState sys σ σ’’                                              structure MEVsup (σ : sys.sysState) (v : R) : Prop where
                                                                       traces_approx : ∀ (ε : R+), ∃ tr,
   In order to define the gain achieved by the adversary by              gainMoves sys σ tr + ε ≥ v
performing a list of moves, we first generalize the semantics          other_traces_worse : ∀ tr, gainMoves sys σ tr ≤ v
of adversarial moves. The effect of a list of moves is the
composition of the individual effect of each move in the list,       C. Proving MEV
discarding those that fail. For brevity, we omit the definition
                                                                        In principle, one could attempt to prove that a system sys
of this function — hereafter, we will similarly omit long
                                                                     in state σ has a given MEV equal to v by directly applying
definitions, referring to [26] for their Lean code.
                                                                     the definition of MEV. Doing that would require to 1) find a
def semMoves (σ : sys.sysState)                                      trace giving Adv a gain v, and 2) show that no other trace can
  (tr : List sys.Move) : sys.sysState                                extract more value. The second task, in particular, is quite
                                                                     hard, as it requires reasoning on all the (infinitely many)
  The adversarial gain of a list of moves is given by compar-        adversarial traces. To address this challenge, we introduce a
ing the initial and final states.                                    MEV characterization theorem that provides a principled proof
                                                                     technique for establishing that a given value indeed coincides
def gainMoves
    (σ : sys.sysState) (tr : List sys.Move) : R :=
                                                                     with the MEV. More precisely, using MEV.characterization
  gainState sys σ (semMoves sys σ tr)                                theorem (Figure 5) requires following these steps:
                                                                       1) Fix the system state σ from which the adversary is going
   We establish a few basic properties of gainMoves: the empty            to extract MEV.
list gives zero gain, and the gain of the first move in a list can     2) Specify an invariant inv on system states. The invariant
be separated from the gain of the rest of the moves.                      must be accompanied with a proof ensuring that it holds
theorem MEV.characterization                                        the only technical difference that one more argument must be
  (σ : sys.sysState)                                                passed to the guess function to ensure the invariant holds.
  (inv : sys.sysState → Prop)                                         Below, we sketch the proof for MEV.characterization.
  (MEV_guess : (σ : sys.sysState) → inv σ → R≥0)
  (invariant_init : inv σ)
  (invariant_sound :                                                Proof (sketch). We have to prove that MEV_guess σ is the
    ∀ {m : sys.Move} {σ 0 σ 1 : sys.sysState},                      MEV in σ . The item traces_reaches_v follows directly from
    sys.semantics σ 0 m = some σ 1 →
                                                                    MEV_guess_coherent. For other_traces_worse, consider an
    inv σ 0 → inv σ 1 )
  (MEV_guess_coherent : ∃ tr : List sys.Move,                       arbitrary trace m0 , . . . , mn−1 of moves starting from σ0 = σ
    gainMoves sys σ tr = MEV_guess σ invariant_init)                and going through states σ1 , σ2 , . . . , σn . We have that:
  (MEV_guess_sound :
    ∀ {m : sys.Move} {σ 0 σ 1 : sys.sysState},
    (hmove : sys.semantics σ 0 m = some σ 1 ) →                         gainMoves σ [m0 , . . . , mn−1 ]
    (σ 0 _inv : inv σ 0 ) →
                                                                       = gainState σ σ1
    let σ 1 _inv := invariant_sound hmove σ 0 _inv
    gainState sys σ 0 σ 1 + MEV_guess σ 1 σ 1 _inv ≤                    + ···
     MEV_guess σ 0 σ 0 _inv) :                                          + gainState σn−2 σn−1
  MEV sys σ (MEV_guess σ invariant_init)                                + gainState σn−1 σn
          Fig. 5. MEV characterization theorem (soundness).            ≤ gainState σ σ1
                                                                        + ···
                                                                        + gainState σn−2 σn−1
    on σ (invariant_init), and that it is preserved by any              + gainState σn−1 σn
    adversarial move (invariant_sound).                                 + MEV_guess σn                     since MEV_guess σn ≥ 0
 3) Specify a guess function MEV_guess that maps any state             ≤ gainState σ σ1
    satisfying the invariant to a value in R≥0, which is a              + ···
    candidate MEV for that state.
                                                                        + gainState σn−2 σn−1
 4) Find an adversarial trace that extracts from σ exactly
                                                                        + MEV_guess σn−1                   by MEV_guess_sound
    MEV_guess σ . This ensures that, on the system state σ ,
                                                                       ≤ gainState σ σ1
    the guess function provides a lower bound to the MEV.
    We call this property coherence (MEV_guess_coherent).               + ···
 5) Prove that the guess function is an upper bound for                 + MEV_guess σn−2                   by MEV_guess_sound
    MEV. More precisely, we must prove that, if σ 0 is any             ≤ ···
    (invariant-abiding) system state, then moving to another           ≤ MEV_guess σ                       by MEV_guess_sound
    state σ 1 cannot induce a gain for the adversary that is
    greater than the difference between the guesses. We call        In the chain of inequalities above we repeatedly apply the
    this property soundness (MEV_guess_sound):                      MEV_guess_sound inequality, replacing at each step the last
                                                                    part of the sum gainState σi σi+1 + MEV_guess σi+1 with
        MEV_guess σ0 ≥ gainState σ0 σ1 + MEV_guess σ1               its upper bound MEV_guess σi . At the end, the whole sum is
                                                                    reduced to MEV_guess σ.
   Once all the steps above are completed, our characterization
theorem establishes MEV σ (MEV_guess σ), proving that the
MEV in σ is indeed the one given by the guess function.                The MEV.characterization theorem ensures that if there
                                                                    exists a sound and coherent guess function, then that function
   The choices of the invariant and of the guess function are
                                                                    actually provides the MEV. We also show that our character-
crucial. Intuitively, the invariant defines an over-approximation
                                                                    ization is complete: whenever MEV exists, there also exists a
of the states that can be reached from σ by the adversary.
                                                                    sound and coherent guess function (Figure 6).
Choosing a suitable invariant is key to simplify the subsequent
steps, since they involve properties that are only required to
hold on invariant-abiding states. In our experience, simple         Proof (sketch). Since by assumption MEV exists, we choose
invariants are enough to this purpose: e.g., both in the Coin-      as guess function the one that maps each (invariant-abiding)
Pusher and in the AMM, it is enough to impose a bound on            state to its MEV. Coherence is straightforward, since the
the size of the mempool. The other crucial step is choosing         definition of MEV (trace_reaches_v) ensures that there is
the guess function. Roughly, this corresponds to estimate the       a trace extracting that value.
value extracted by an adversary following the optimal strategy.        For soundness, let m be a move from state σ 0 to σ 1 . We also
Fortunately, this estimate must only be provided for the states     let tr be the trace providing MEV for σ 1 (trace_reaches_v),
satisfying the invariant, simplifying this task.                    hence gainMoves tr = guess σ 1 . The definition of MEV
   Our Lean formalization of the MEV characterization the-          (other_traces_worse) ensures that the value extracted by any
orem closely follows the previous informal discussion, with         trace tr’ from σ 0 is bounded by the MEV. In particular, choose
theorem MEV.characterization_complete                             inductive Tx
  (σ : sys.sysState)                                              | push (P : Participant) (v : R+) : Tx
  (inv : sys.sysState → Prop)
  (invariant_init : inv σ)                                          A transaction push P v sends v tokens (of type τ 0 ) to the
  (invariant_sound :                                              contract from participant P, causing P to win the entire contract
    ∀ {m : sys.Move} {σ 0 σ 1 : sys.sysState},                    balance if v tips such balance over the threshold.
    sys.semantics σ 0 m = some σ 1 →
    inv σ 0 → inv σ 1 )
                                                                    Then, we let the adversary send only their own tokens:
  (mev : ∀ σ’, inv σ’ → ∃ v, MEV sys σ’ v) :                      inductive advTx : Tx → Prop
  ∃ guess : (σ’ : sys.sysState) → inv σ’ → R≥0,                   | push {x} : advTx (.push .Adv x)
    -- guess is coherent
    (∃ tr : List sys.Move,                                          The contract state contains the same fields as in the Air-
      gainMoves sys σ tr = guess σ invariant_init) ∧              drop contract, plus an additional field to represent a generic
    -- guess is sound                                             threshold (which we chose to be 100 in §II-A).
    (∀ {m : sys.Move} {σ 0 σ 1 : sys.sysState},
      (hmove : sys.semantics σ 0 m = some σ 1 ) →                 structure State where
      (σ 0 _inv : inv σ 0 ) →                                       threshold : R+
      let σ 1 _inv := invariant_sound hmove σ 0 _inv                bal : Token → R≥0
      gainState sys σ 0 σ 1 + guess σ 1 σ 1 _inv ≤                  wal : @Wallet Token
      guess σ 0 σ 0 _inv)                                           mempool : AssocList TxId Tx

        Fig. 6. MEV characterization theorem (completeness).        We denote the associated system state as CPState.
                                                                  abbrev CPState := @SysState Token State
tr’ = m::tr, obtaining gainMoves σ 0 (m::tr) ≤ guess σ 0 .           The type Move of adversarial moves is identical to that
From this and theorem gainMoves_step, we conclude:                for the Aidrop contract: the adversary can append to the
               gainState σ 0 σ 1 + guess σ 1                      blockchain either one of its own transactions or a transaction
                                                                  from the mempool. The semantics of a Move defines the
            = gainState σ 0 σ 1 + gainMoves tr
                                                                  contract behaviour. An adversarial drop sends tokens from
            = gainMoves σ 0 (m::tr)                               the adversary to the contract, possibily making the adversary
            ≤ guess σ 0                                           win the game. This updates ∆ and bal accordingly. Instead, a
                                                                  mempool move sends tokens from honest participants to the
   Overall, formalizing our system model and the MEV-related      contract (if there are enough), possibily making the partici-
theorems required ∼600 lines of Lean code.                        pants win the game. This updates wal and bal accordingly.
D. Example: MEV of the Airdrop contract                           def semTx (tx : Tx) (σ : CPState) : Option CPState := ...
   We now analyse the MEV of the Airdrop contract                 def semMove (σ : CPState) (m : Move) : Option CPState :=...
from §III-B. To this purpose, we exploit our MEV charac-
                                                                    We can finally define the CoinPusher contract
terization theorem. We start by defining an invariant. For this
basic contract, a trivial invariant suffices.                     def CoinPusher: System := ...

def Airdrop_invariant (σ : ADState) : Prop := True                   We now turn to the study of MEV. Unlike for the Aidrop
                                                                  contract, the MEV is now actually affected by the mempool.
  We then define our guess function. As intuition suggests,
                                                                  We therefore choose to establish MEV in two distinct cases:
we guess that the MEV is obtained by transferring the entire
                                                                     • the case where the mempool is empty, and
contract balance to the adversary.
                                                                     • the case where the mempool contains one transaction.
def Airdrop_MEV_guess (σ : ADState)
  (σ_inv : Airdrop_invariant σ) : R≥0 := σ.s.bal .τ 0             As we will see, the general case where the mempool contains
                                                                  N transactions is a simple extension of these two cases:
  Finally, by leveraging our MEV characterization theorem,        roughly, the strategy of the adversary is to apply iteratively
we establish that our guess is indeed the MEV.                    N times the strategy for the singleton mempool. Because of
theorem MEV_Airdrop (σ : ADState) :                               this, we focus on the first two core cases.
  MEV Airdrop σ (Airdrop_MEV_guess σ True.intro)                     For the former case, we declare the following invariant.
                                                                  def CoinPusher_empty_invariant (σ : CPState) : Prop :=
        V. MEV OF THE C OIN P USHER CONTRACT                        σ.s.mempool.isEmpty

   We now formalize the CoinPusher contract we described             If there are no transactions in the mempool, the optimal
in §II-A. Some parts are similar to the Airdrop contract: e.g.,   strategy for the adversary is to push enough tokens to trig-
types Participant and Token are the same, since we use the        ger the win. For the sake of simplicity, below we choose
same participants and token types. Transactions are instead       to send σ.s.threshold tokens, even if a smaller amount
modelled by the new type:                                         (σ.s.threshold - σ.s.bal .τ 0 ) would also suffice.
def CoinPusher_strategy_empty (σ : CPState) :                         def CoinPusher_one_or_less_MEV_guess (σ : CPState)
    List Move := [.adv (.push .Adv σ.s.threshold) .push]                  (σ_inv : CP_one_or_less_invariant σ) : R≥0 :=
                                                                        match σ.s.mempool with
  We define a guess function for the MEV, posing that we
                                                                        | .nil => σ.s.bal .τ 0
can extract the entire contract balance as MEV.                         | .cons id tx .nil =>
def CoinPusher_empty_MEV_guess (σ : CPState)                              if tx.v < σ.s.threshold ∧ tx.v ≤ σ.s.wal .τ 0
    (σ_inv : CoinPusher_empty_invariant σ) : R≥0 :=                       then σ.s.bal .τ 0 + tx.v
  σ.s.bal .τ 0                                                            else σ.s.bal .τ 0
                                                                        | .cons id tx (.cons id2 tx2 rest) => by
  We can prove that our guess function is sound and coherent              exfalso; ... -- contradicts σ_inv
(exploiting our strategy). This makes it possible to invoke
our MEV characterization theorem and establish MEV for the            def CP_strategy_singleton_mempool (σ : CPState)
empty mempool case.                                                       (id : TxId) (tx : Tx) : List Move :=
theorem MEV_CoinPusher_empty (σ : CPState) :                            [ .adv (.push .Adv σ.s.threshold ) .push
  σ.s.mempool = .nil →                                                  , Move.mempool id
  MEV CoinPusher σ (CoinPusher_empty_MEV_guess σ)                       , .adv (.push .Adv σ.s.threshold ) .push ]


   We now turn to the case where the mempool contains one               We can prove that our guess function is sound
transaction, i.e., it is a singleton list. We use the following       and coherent (exploiting our strategy). This makes it
invariant. Note that we have to account for the mempool be-           possible to invoke our MEV characterization theorem
coming empty after its transaction is appended, so the invariant      and establish MEV for the singleton mempool case.
actually requires that the mempool is either a singleton or           theorem MEV_CoinPusher_singleton
empty. For the sake of simplicity, we also require that if the          (σ : CPState) (id : TxId) (tx : Tx)
mempool is a singleton, its transaction is from the honest              (singleton : σ.s.mempool = .cons id tx .nil)
                                                                        (nonadv : tx.part ̸= .Adv) :
participants. Indeed, adversarial transactions in the mempool
                                                                        MEV CoinPusher σ
are irrelevant for the purposes of MEV, so we can ignore them.            (if tx.v < σ.s.threshold ∧ tx.v ≤ σ.s.wal .τ 0
def CP_one_or_less_invariant (σ : CPState) : Prop :=                       then σ.s.bal .τ 0 + tx.v
 σ.s.mempool.isEmpty ∨                                                     else σ.s.bal .τ 0 )
 (∃ idx tx, σ.s.mempool = .cons idx tx .nil ∧ tx.P ̸= .Adv)
                                                                         We remark that this result extends to the general case
  The guess function is more complex w.r.t. the empty mem-            where the mempool contains any number of transactions. The
pool case. We define it by cases, according to the mempool:           optimal strategy here is to attempt to append all the mempool
 1) If the mempool is empty, our guess is σ.s.bal .τ 0 , the          transactions, while interleaving them with an adversarial trans-
     same we mentioned earlier.                                       action that triggers the win and empties the contract balance:
 2) Otherwise, if the mempool is the singleton tx (a push             [trigger0 , tx1 , trigger1 , tx2 , ..., txn , triggern ].
     transaction from the honest participants), the best strategy        Overall, the formalization of the CoinPusher contract and
     for the adversary is (i) first, trigger a win in the contract,   the proofs to establish its MEV amount to ∼1000 lines of
     emptying its balance, (ii) attempt to append tx, (iii) trig-     Lean code. This required more effort than the Airdrop contract,
     ger the win again. The first step extracts σ.s.bal .τ 0          because the value extraction strategy is no longer trivial, but
     tokens, emptying the contract balance.                           did not pose a significant challenge.
     The second step, appending tx, might fail if the honest
                                                                                  VI. MEV OF THE AMM CONTRACT
     participant does not have enough tokens to execute it,
     i.e. if tx.v > σ.s.wal .τ 0 , in which case it has no               We now move to our main contribution, the formalization
     effect. Further, even if tx succeeds, it might send to the       of an Automated Market Maker contract, which we described
     contract enough tokens to immediately trigger the win            in §II-B.
     for the honest participant, if tx.v ≥ σ.s.threshold. In             For this contract, the Participant type is akin to the
     this case, the tokens are immediately sent back to the           previous examples, with one adversary, and infinitely many
     participant, and the transaction has no net effect, since        honest ones. The AMM swaps exchange two different types
     the contract balance was empty. Otherwise, tx succeeds           of tokens:
     and sends fewer tokens than the threshold, loading the           inductive Token
                                                                      | τ 0 : Token
     contract balance with tx.v tokens. Overall, while the
                                                                      | τ 1 : Token
     second step does not make the adversary directly gain
     anything, it can potentially load the contract balance.            The only operations supported by our AMM are tokens
     Finally, the third step extracts the new contract balance.       swaps. We define transactions accordingly.
     This could be tx.v or zero depending on whether tx
                                                                      inductive Tx
     succeeded in loading the contract or not, respectively.          | swap (P : Participant) (v0 : R+)
     Coherently with our strategy, we guess the MEV to be                    (τ : Token) (vmin : R≥0) : Tx
     σ.s.bal .τ 0 + tx.v or just σ.s.bal .τ 0 .
   When a swap P v0 τ vmin is executed, participant P ex-          B. Non-empty mempool
changes v0 of their own τ tokens with at least vmin tokens of         We now turn to the case where the mempool contains one
the other type in the AMM reserves. If such an exchange is         transaction tx. Here, our invariant actually requires that the
impossible, i.e. when P does not own enough tokens or when         mempool contains only tx or is empty, since tx is consumed
the AMM exchange rate would cause fewer than vmin tokens           when it is fired. Further, we also require that tx is owned by
to be exchanged, the transaction has no effect.                    a honest participant (tx.part ̸= .Adv) and that tx requires a
   The contract state features the same fields as the Airdrop      minimum positive amount of tokens in exchange (tx.vmin
contract (i.e. bal, wal, and mempool). The resulting system        > 0). Indeed, adversarial transactions in the mempool are
state is then denoted with with AMMState.                          pointless, since they can be crafted, so we can rule them out.
   Again, the type Move is analogous to the other examples: the    Further, having a mempool transaction with tx.vmin = 0 leads
adversary can either append a transaction from the mempool or      to a corner case in which MEV does not exist(see Section A).
one of their own. Like in the CoinPusher example, an adversar-
                                                                   def inv_one_or_less (σ : AMMState) : Prop :=
ial swap updates △ and bal, while a mempool move exchanges           σ.s.mempool.isEmpty ∨
tokens between a honest participant and the contract, updating       (∃ idx tx, σ.s.mempool = .cons idx tx .nil ∧
wal and bal accordingly.                                                        tx.vmin > 0 ∧ tx.part ̸= .Adv)
   To study the MEV of the AMM contract, we focus on two              We now define our guess function, which turns out to be
cases depending on the initial state of the mempool:               significantly more complex than that for the empty mempool
  •   the mempool is empty, and                                    case. We have to provide a guess for all the states satisfying
  •   the mempool contains one transaction.                        the invariant, so we must handle mempools having size zero or
As we will see, the general case where the mempool contains        one. When the mempool is empty, we guess extractable σ ,
N transactions is a simple extension of these two cases:           coherently with the empty mempool case. When there is one
roughly, the strategy of the adversary is to apply iteratively     transaction tx in the mempool, we proceed as follows.
N times the strategy for the singleton mempool. Because of            We first check if tx can be beneficial to the adversary. This
this, we focus on the first two core cases.                        happens when:
                                                                     1) Transaction tx can actually be executed in some AMM
A. Empty mempool                                                         state, i.e., its honest sender actually owns the tokens tx is
                                                                         trying to swap (tx.inputVal ≤ σ.s.wal tx.inputTok).
  For the empty mempool case, we define a simple invariant:          2) Transaction tx causes its honest sender to transfer to the
def empty_mempool_invariant (σ : AMMState) : Prop :=                     contract an amount of tokens whose value (tx.inputVal
  σ.s.mempool.isEmpty                                                    * pr tx.inputTok) is larger than the value of the min-
                                                                         imum amount of tokens it is requiring in exchange
We easily prove the invariant to be sound.                               (tx.vmin * pr (other_tok tx.inputTok)).
  We now define our guess function for the empty mempool              If either of the above conditions does not hold, tx is useless
case. We start by defining extractable σ as the value that can     for the adversary, who can then disregard tx. In this case, our
be extracted by rebalancing the AMM. This can be expressed         guess is the same as the one for the empty mempool case,
with the following formula, which we derive from [23].             hence extractable σ .
def extractable (σ : AMMState) : R≥0 :=                               Instead, when both of the above conditions hold, we exploit
  ⟨ ( Real.sqrt (pr .τ 0 * σ.s.bal .τ 0 ) -                        tx as follows. First, the adversary employs its unlimited token
      Real.sqrt (pr .τ 1 * σ.s.bal .τ 1 ) )^2, . . . ⟩             reserves and performs a swap move, bringing the AMM to
                                                                   a state σ’ where executing tx will transfer to the honest
  We then define our guess function as extractable σ .             participant exactly tx.vmin tokens. Intuitively, from the point
def AMM_MEV_guess (σ : AMMState)                                   of view of the honest participant, σ’ is the worst state where
    (σ_inv : empty_mempool_invariant σ) : R≥0 :=                   tx still can be executed. Dually, σ’ is also the best state for
  extractable σ
                                                                   the adversary in which to execute tx. We refer to σ’ as the
                                                                   tight state for tx. After the move, having reached the tight state
  We finally prove that our guess is indeed the MEV.
                                                                   the adversary indeed appends tx to the blockchain. After that,
theorem MEV_empty_mempool (σ : AMMState)                           we reach a new state σ’’ where the mempool is empty, so the
  (σ_inv : σ.s.mempool = .nil) :
                                                                   adversary proceeds as in the empty mempool case.
  MEV (AMM pr) σ (AMM_MEV_guess pr σ σ_inv)
                                                                      We coherently define our guess function as the sum of:
This effectively guarantees that the best adversarial strategy,      1) the gain of move (gainMoves (AMM pr) σ [move]);
when the mempool is empty, is to rebalance the AMM.                  2) the gain of tx, which is zero, since it does not directly
Overall, formalizing the AMM contract required ∼700 lines                transfer tokens to or from the adversary;
of Lean code, while establishing MEV in the empty mempool            3) the gain from the rebalancing, i.e., extractable σ’’.
case required further ∼500 lines. The main challenge here was         We remark that the gain of the first step may be negative.
to deal with the mathematical formulas that arise in the proofs.   The adversary can therefore temporarily lose value in that step,
which makes the overall MEV strategy non-trivial. In our Lean      numbers. In practice, however, blockchain platforms use high-
development, we first defined our guess function as having         precision integers to encode such amounts. For instance, in
codomain R. We then showed that its result is always non-          Ethereum it is common to employ the integer type uint256,
negative, allowing its codomain to be restricted to R≥0, as        since floating point types are not supported. As a consequence,
required by our MEV.characterization theorem. This actually        when a financial contract performs its numerical computations
shows how the temporary loss of value for the adversary at         — e.g., calculating the exchange rate in a swap of an AMM
the first step is then compensated by the next steps.              — the result is inevitably affected by a small rounding error.
   We finally remark that, as a corner case, it is possible that      Although these errors usually have a negligible economic
the initial state σ is already tight for tx. If so, no move is     impact on the real-world usage of the contract, it is possible to
needed, and we simply use extractable σ as our guess.              craft artificial scenarios where the MEV differs substantially
def AMM_MEV_guess’ (σ : AMMState)                                  depending on whether rounding errors are present or not. For
    (σ_inv : inv_one_or_less σ) : R :=                             instance, consider a slightly modified CoinPusher where the
  match σ.s.mempool with                                           winning threshold is 9991, and a 0.1% fee is subtracted from
  | .nil => extractable pr σ                                       the value sent to the contract upon each call to push. Consider
  | .cons id tx .nil =>                                            a state where the contract has zero balance and the mempool
    if tx.inputVal ≤ σ.s.wal tx.inputTok ∧
                                                                   contains a push transaction where a honest participant is
       (tx.inputVal * pr tx.inputTok >
        tx.vmin * pr (other_tok tx.inputTok))
                                                                   sending 10001 tokens. Using real numbers, the push would
    then . . .                                                     compute the fee as 10.001 and transfer 9990.999 to the con-
      let σ’ := tight_state_from_mempool σ id tx . . .             tract — so, slightly less than the threshold required to trigger
      let σ’’ := state_after_tight σ id tx . . .                   the win. The adversary could extract a MEV of 9990.999 by
      match move_from_to_state σ σ’ with                           back-running the mempool transaction with another push of
      | .some move =>                                              1.0001 or more, triggering the win. Instead, using integers,
        gainMoves (AMM pr) σ [move] + extractable pr σ’’
      | .none => -- σ = σ’, no move needed
                                                                   the push would round the fee to 10, and transfer 9991 token
        extractable pr σ’’                                         units to the contract balance — i.e. exactly the threshold value.
    else                                                           Here, the MEV is zero, since the mempool transaction would
      extractable pr σ                                             immediately trigger the win for the honest user, hence it is
  | _ => . . . -- contradicts the invariant                        useless for the adversary.
                                                                      Adapting our system model and MEV formalization to
def AMM_MEV_guess (σ : AMMState)
                                                                   use integers instead of reals is easy, but we anticipate that
    (σ_inv : inv_one_or_less σ) : R≥0 :=
  ⟨ AMM_MEV_guess’ pr σ σ_inv , . . . ⟩                            it would significantly complicate the reasoning needed to
                                                                   establish MEV for certain contracts. For instance, in our
  We finally establish MEV for the AMM contract when the           AMM, performing two consecutive adversarial swaps has the
mempool contains a single transaction. To do so, we prove our      same effect as a combined single swap, which simplifies the
guess to be coherent, showing that its value can actually be       treatment. This is no longer the case when rounding errors are
extracted using a trace. We also prove our guess to be sound,      taken into account. On the positive side, using integers would
showing that no adversarial move can extract more value.           ensure that MEV always exists. This does not hold with real
theorem MEV_singleton_mempool (σ : AMMState)
                                                                   numbers: an Airdrop variant which allows to withdraw (drop)
  (id : TxId) (tx : Tx) (vmin_pos : tx.vmin > 0)                   any amount smaller than its balance has no associated MEV.
  (singleton : σ.s.mempool = .cons id tx .nil)                     Indeed, any strategy can be improved by adding one more
  (part_nonAdv : tx.part ̸= .Adv) :                                drop to grab a tiny amount of additional tokens.
  let σ_inv : inv_one_or_less σ := . . .                                 Proof automation: While Lean does provide several
  MEV (AMM pr) σ (AMM_MEV_guess pr σ σ_inv)                        tactics to automate the proof of certain kinds of mathematical
                                                                   goals, in our experience we often wished for more powerful
   Overall, establishing MEV in the singleton mempool case
                                                                   arithmetic simplification tactics. For instance, the proofs for
required ∼3200 lines of Lean code, on top of the base AMM
                                                                   our AMM model often make use of inequalities involving
model (∼700 lines) and the empty mempool case (∼500
                                                                   square roots. We managed to prove these only through several
lines). The main challenge here was dealing with the complex
                                                                   manual algebraic steps, invoking each time a suitable theorem
extraction strategy, requiring the proofs to consider all the
                                                                   from the mathematical library. This could change in the future
possible cases. Further, the involved mathematical formulas
                                                                   as Lean improves its tactics.
were more complex, and required more effort to handle.
                                                                         Adversary model: Our system model keeps the adversary
                                                                   syntactically distinct from honest users. This choice requires
                     VII. L IMITATIONS
                                                                   a certain care when encoding smart contracts into our system
  In this section we discuss how our design choices affect the     model, especially for contracts implementing access control
practical applicability of the proposed Lean formalization.        mechanisms. In general, the system designer must ensure that
     Real vs. integer arithmetic: In our MEV formalization,        the Move type and its associated semantics faithfully capture
we represent token balances and their market values as real        all the possible adversarial actions. Omitting even a single
adversarial move could lead to overlooked attacks.                  not completely equivalent to our wealthiness assumption about
                                                                    adversaries (§III-A), since the token to be distributed may not
                    VIII. R ELATED WORK                             be sufficient for the attack. A wealthiness assumption more
      Analysis tools for MEV: The seminal work [14] was the         similar to ours was used in [31], which introduces the notion of
first to propose a general definition of MEV and a tool to          “MEV of wealthy adversaries” by taking the maximum MEV
estimate MEV upper bounds. Their verification technique is          over all possible adversarial wallets.
based on a symbolic semantics that over-approximates the set              Analysis of the AMM contract: Compared to real-world
of execution paths and their reachable states. Based upon this      AMM implementations such as Uniswap [30], our Lean for-
symbolic semantics, they encode the problem of estimating a         malization introduces a few simplifications, that overall con-
MEV bound as a reachability problem. Compared to our work,          tribute to keeping our proofs manageable. A first simplification
this technique requires less manual effort, since the designer      is that in Uniswap, when a user executes a swap, part of
is only required to provide a specification of the contract         the input tokens are paid to the protocol as a fee. Studying
(in their domain-specific language), and from that point the        the effect of swap fees on MEV would require a further
tool automatically performs the analysis of MEV. A main             complication of the adversarial strategies, who would need
drawback of the approach is the lack of scalability (as observed    to minimize the impact of fees on their own swaps. The
in [7]): even for relatively simple contracts, the exponential      Lean formalization in [32] studies AMMs with swap fees, but
blowup of the generated paths may lead the tool to exhaust          unlike ours, it does not address MEV. The additional burden
the computational resources. Another difference with our work       introduced by swap fees is, however, already visible in [32]
is that our notion of MEV is exact: when MEV sys σ v                in the analysis of arbitrage (i.e., the optimal swap in a zero-
holds, it actually means that v can be extracted, and there         player game). We expect swap fees to impact MEV analysis
is no adversarial strategy that can extract more. The technique     to an even greater extent.
in [14] instead over-approximates MEV, without guaranteeing            Besides swaps, concrete AMM implementations typically
that the verified upper bound can actually be extracted.            allow users to deposit and withdraw tokens from the AMM.
   The work [7] approached the problem of MEV estimation            In particular, deposit transactions can increase the profits
from a different perspective, by proposing a machine-learning       obtainable from subsequent swaps [29], and can thus be lever-
technique to under-approximate MEV. Their algorithm takes           aged by an adversary to amplifly MEV. The work [23] intro-
as input a blockchain state and a mempool, and gives as             duces an extended sandwich attack that combines deposit and
output a sequence of transactions (containing both transactions     swap transactions from the mempool with adversary-crafted
crafted by the adversary and transactions from the mempool)         transactions, showing that this may increase the extractable
that can be played by the adversary to extract value. This          value. Extending our proof to handle mempools containing
approach is more scalable than [14], and allows the adversary       arbitrary combinations of deposit and swap transactions would,
to fine-tune the computational resources used by the algorithm      however, cause a substantial explosion in the number of cases
in order to match the available hardware. Of course this            in our proof of MEV optimality.
technique does not guarantee that the synthesised sequence             A different Lean formalization of constant-product AMMs
of transactions is optimal: instead, our approach pursues the       is presented in [33]. Compared to our work — which proposes
goal of certifying the optimality of the adversarial strategy.      a general framework for analysing MEV of arbitrary smart
      Formalization of the adversary: Our definition of MEV         contracts — the work [33] is specifically targeted on AMMs,
keeps the adversary distinct from the other participants — so       and only deals with arbitrage.
being similar in spirit to [14], where MEV is parameterized by         Sandwich attacks on AMMs were originally analysed
the player who extracts it. As noted in §VII, this requires some    in [22], and later in [23], [24], [34], [35], [25], among the
extra care when modelling the contract behaviour, to avoid the      others. Compared to these works, ours provides the first
risk of omitting some adversarial actions. Some approaches to       machine-checked proof of optimality of sandwich attacks.
avoid fixing the identity of the adversary have been proposed             MEV countermeasures: Given the relevance of MEV on
in literature. The work [15] defines an adversary-agnostic          the blockchain ecosystem, several techniques to mitigate its
MEV by first considering the MEVs that can be extracted by          effects have been proposed in the past few years. Some of these
any individual participant, and then taking the minimum. As         techniques are applicable to arbitrary smart contracts [36],
noted in [15], this definition has some drawbacks when extract-     [37], [38], [39], [40], while some others are specific to certain
ing value requires the adversary to make upfront payments. In       classes of contracts, such as AMMs [41], [42]. Formally
such cases, the MEV is under-estimated as zero, since the           verifying within our Lean framework that some of these
minimum also covers the zero value that can be extracted by         techniques achieves the expected MEV reduction would be
a “poor” adversary. The notion of universal MEV proposed            a challenging extension of our work.
in [17] overcomes this problem by defining MEV as a game
where honest players try to minimize the damage, while                                   IX. C ONCLUSIONS
adversaries try to maximize their gain. A token redistribution         We present a Lean framework for reasoning about MEV
mechanism ensures that the adversaries have enough wealth           in smart contracts. The framework is blockchain-agnostic and
to execute their extraction strategy. The token redistribution is   can be instantiated to model different smart contract languages,
making it applicable to a wide range of real-world scenarios.                  [14] K. Babel, P. Daian, M. Kelkar, and A. Juels, “Clockwork finance:
Unlike prior tools that are focussed on under- or over- ap-                         Automated analysis of economic security in smart contracts,” in IEEE
                                                                                    Symposium on Security and Privacy. IEEE Computer Society, 2023,
proximations, our proof technique can establish exact MEV                           pp. 622–639.
bounds, by identifying attacks that are realistically executable               [15] A. Salles, “On the formalization of MEV,” 2021, https://writings.
by an adversary and proving their optimality (no strictly                           flashbots.net/research/formalization-mev.
                                                                               [16] B. Mazorra, M. Reynolds, and V. Daza, “Price of MEV: towards a game
more profitable attacks exist). We validate the framework by                        theoretical approach to MEV,” in ACM CCS Workshop on Decentralized
formalising representative DeFi protocols and mechanising                           Finance and Security. ACM, 2022, pp. 15–22.
their analysis in Lean. In particular, we provide the first                    [17] M. Bartoletti and R. Zunino, “A theoretical basis for MEV,” in Financial
                                                                                    Cryptography and Data Security, ser. LNCS. Springer, 2025.
machine-checked proof of the optimality of sandwich attacks                    [18] L. d. Moura and S. Ullrich, “The Lean 4 Theorem Prover and Program-
on Uniswap v2-based Automated Market Makers, demonstrat-                            ming Language,” in Automated Deduction (CADE). Springer-Verlag,
ing the effectiveness of our approach.                                              2021, p. 625–635.
                                                                               [19] The mathlib Community, “The Lean Mathematical Library,” in Certified
                                                                                    Programs and Proofs (CPP). ACM, 2020, p. 367–381.
                        ACKNOWLEDGMENT                                         [20] G. Angeris and T. Chitra, “Improved price oracles: Constant Function
                                                                                    Market Makers,” in ACM Conference on Advances in Financial Tech-
  Work partially supported by project SERICS (PE00000014)                           nologies (AFT). ACM, 2020, pp. 80–91.
under the MUR National Recovery and Resilience Plan funded                     [21] S. Werner, D. Perez, L. Gudgeon, A. Klages-Mundt, D. Harz, and W. J.
by the European Union – NextGenerationEU, and by PRIN                               Knottenbelt, “SoK: Decentralized Finance (DeFi),” in ACM Conference
                                                                                    on Advances in Financial Technologies, (AFT). ACM, 2022, pp. 30–46.
2022 PNRR project DeLiCE (F53D23009130001).                                    [22] L. Zhou, K. Qin, C. F. Torres, D. V. Le, and A. Gervais, “High-
                                                                                    Frequency Trading on Decentralized On-Chain Exchanges,” in IEEE
                             R EFERENCES                                            Symp. on Security and Privacy. IEEE, 2021, pp. 428–445.
                                                                               [23] M. Bartoletti, J. H. Chiang, and A. Lluch-Lafuente, “Maximizing
 [1] B. Weintraub, C. F. Torres, C. Nita-Rotaru, and R. State, “A Flash(Bot)        extractable value from Automated Market Makers,” in Financial Cryp-
     in the pan: Measuring maximal extractable value in private pools,” in          tography, ser. LNCS, vol. 13411. Springer, 2022, pp. 3–19.
     ACM Internet Measurement Conference. ACM, 2022, p. 458–471.               [24] J. Xu, K. Paruch, S. Cousaert, and Y. Feng, “SoK: Decentralized
 [2] C. F. Torres, R. Camino, and R. State, “Frontrunner Jones and the              Exchanges (DEX) with Automated Market Maker (AMM) Protocols,”
     Raiders of the Dark Forest: An empirical study of frontrunning on the          ACM Comput. Surv., vol. 55, no. 11, 2023. [Online]. Available:
     Ethereum blockchain,” in USENIX Security Symposium, 2021, pp. 1343–            https://doi.org/10.1145/3570639
     1359.                                                                     [25] K. Kulkarni, T. Diamandis, and T. Chitra, “Routing MEV in Constant
 [3] K. Qin, L. Zhou, and A. Gervais, “Quantifying blockchain extractable           Function Market Makers,” in Web and Internet Economics (WINE), ser.
     value: How dark is the forest?” in IEEE Symp. on Security and Privacy.         LNCS, vol. 14413. Springer, 2023, pp. 456–473.
     IEEE, 2022, pp. 198–214.                                                  [26] “MEV Lean formalization,” 2025. [Online]. Available: https://github.
 [4] K. Qin, L. Zhou, B. Livshits, and A. Gervais, “Attacking the DeFi              com/r-marche/MEV-formal
     ecosystem with Flash Loans for fun and profit,” in Financial Cryptog-     [27] S. Eskandari, S. Moosavi, and J. Clark, “SoK: Transparent Dishonesty:
     raphy, ser. LNCS, vol. 12674. Springer, 2021, pp. 3–32.                        Front-Running Attacks on Blockchain,” in Financial Cryptography.
 [5] P. Daian, S. Goldfeder, T. Kell, Y. Li, X. Zhao, I. Bentov, L. Brei-           Springer, 2020, pp. 170–189.
     denbach, and A. Juels, “Flash boys 2.0: Frontrunning in decentralized     [28] G. Angeris, H.-T. Kao, R. Chiang, C. Noyes, and T. Chitra, “An analysis
     exchanges, miner extractable value, and consensus instability,” in IEEE        of Uniswap markets,” Cryptoeconomic Systems, vol. 1, no. 1, 2021.
     Symp. on Security and Privacy. IEEE, 2020, pp. 910–927.                   [29] M. Bartoletti, J. H. Chiang, and A. Lluch-Lafuente, “A theory of
 [6] Z. Li, J. Li, Z. He, X. Luo, T. Wang, X. Ni, W. Yang, X. Chen, and             Automated Market Makers in DeFi,” Logical Methods in Computer
     T. Chen, “Demystifying DeFi MEV Activities in Flashbots Bundle,” in            Science, vol. 18, no. 4, 2022.
     ACM SIGSAC Conference on Computer and Communications Security             [30] “Uniswap           token       pair       implementation,”         2021,
     (CCS). ACM, 2023, pp. 165–179.                                                 https://github.com/Uniswap/uniswap-v2-core/blob/
 [7] K. Babel, M. Javaheripi, Y. Ji, M. Kelkar, F. Koushanfar, and A. Juels,        4dd59067c76dea4a0e8e4bfdda41877a6b16dedc/contracts/
     “Lanturn: Measuring economic security of smart contracts through               UniswapV2Pair.sol.
     adaptive learning,” in ACM SIGSAC Conference on Computer and              [31] M. Bartoletti, R. Marchesin, and R. Zunino, “DeFi composability as
     Communications Security (CCS). ACM, 2023, pp. 1212–1226.                       MEV non-interference,” in Financial Cryptography, ser. LNCS, vol.
 [8] E. Hildenbrandt, M. Saxena, N. Rodrigues, X. Zhu, P. Daian, D. Guth,           14744. Springer, 2024.
     B. M. Moore, D. Park, Y. Zhang, A. Stefanescu, and G. Rosu, “KEVM:        [32] M. Dessalvi, “Automated Market Makers in the Lean 4 Theorem Prover,”
     A Complete Formal Semantics of the Ethereum Virtual Machine,”                  Master’s thesis, DTU Compute, Technical University of Denmark, 2025.
     in IEEE Computer Security Foundations Symposium (CSF).             IEEE        [Online]. Available: https://fulltext-gateway.cvt.dk/oafilestore?oid=
     Computer Society, 2018, pp. 204–217.                                           6865ca59ee615523af43fd05&targetid=6865ca59c998ab10401d3143
 [9] I. Grishchenko, M. Maffei, and C. Schneidewind, “A Semantic Frame-        [33] D. Pusceddu and M. Bartoletti, “Formalizing Automated Market Makers
     work for the Security Analysis of Ethereum Smart Contracts,” in Prin-          in the Lean 4 Theorem Prover,” in Formal Methods for Blockchains
     ciples of Security and Trust (POST), ser. LNCS, vol. 10804. Springer,          (FMBC), ser. OASIcs, vol. 118. Schloss Dagstuhl - Leibniz-Zentrum
     2018, pp. 243–269.                                                             für Informatik, 2024, pp. 5:1–5:13.
[10] F. Cassez, J. Fuller, M. K. Ghale, D. J. Pearce, and H. M. A. Quiles,     [34] J. Wang, J. Li, Z. Li, X. Deng, and B. Xiao, “n-MVTL Attack: Optimal
     “Formal and Executable Semantics of the Ethereum Virtual Machine in            Transaction Reordering Attack on DeFi,” in European Symposium on
     Dafny,” in Formal Methods (FM), ser. LNCS, vol. 14000. Springer,               Research in Computer Security (ESORICS), ser. LNCS, vol. 14346.
     2023, pp. 571–583.                                                             Springer, 2023, pp. 367–386.
[11] S. Crafa, M. D. Pirro, and E. Zucca, “Is Solidity Solid Enough?” in       [35] A. Park, “The conceptual flaws of decentralized automated market
     Workshop on Trusted Smart Contracts (WTSC), ser. LNCS, vol. 11599.             making,” Management Science, vol. 69, no. 11, pp. 6731–6751, 2023.
     Springer, 2019, pp. 138–153.                                              [36] L. Breidenbach, P. Daian, F. Tramèr, and A. Juels, “Enter the Hydra:
[12] J. Jiao, S. Kan, S. Lin, D. Sanán, Y. Liu, and J. Sun, “Semantic               Towards principled bug bounties and exploit-resistant smart contracts,”
     Understanding of Smart Contracts: Executable Operational Semantics             in USENIX Security Symposium. USENIX Association, 2019, pp. 1335–
     of Solidity,” in IEEE Symposium on Security and Privacy (SP). IEEE,            1352.
     2020, pp. 1695–1712.                                                      [37] C. Baum, J. H. Chiang, B. David, T. K. Frederiksen, and L. Gentile,
[13] D. Marmsoler and A. D. Brucker, “Isabelle/Solidity: A deep embedding           “SoK: Mitigation of Front-Running in Decentralized Finance,” in Finan-
     of Solidity in Isabelle/HOL,” Formal Aspects Comput., vol. 37, no. 2,          cial Cryptography Workshops, ser. LNCS, vol. 13412. Springer, 2022,
     pp. 15:1–15:56, 2025.                                                          pp. 250–271.
[38] L. Heimbach and R. Wattenhofer, “Sok: Preventing transaction reorder-        where tr’ and tr’’ are lists of adversarial moves, and id
     ing manipulations in decentralized finance,” in Advances in Financial     is the transaction id associated to tx. Thus we would have
     Technologies, 2022.
[39] A. Canidio and V. Danos, “Commitment against front-running attacks,”        gainMoves σ tr = gainMoves σ tr’
     Manag. Sci., vol. 70, no. 7, pp. 4429–4440, 2024.
[40] K. Babel, N. Jean-Louis, Y. Ji, U. Misra, M. Kelkar, K. Y. Mudiyanse-                               + gainMove σ ′ (mempool id) (1)
     lage, A. Miller, and A. Juels, “PROF: protected order flow in a profit-                             + gainMoves σ ′′ tr”
     seeking world,” CoRR, vol. abs/2408.02303, 2024.
[41] M. Ciampi, M. Ishaq, M. Magdon-Ismail, R. Ostrovsky, and V. Zikas,                                          tr’              tx
     “FairMM: A fast and frontrunning-resistant crypto market-maker,” in       where σ ′ and σ ′′ are such that −−→ σ ′ and σ ′ −→ σ ′′ .
     Cyber Security, Cryptology, and Machine Learning (CSCML), ser.              Now, let b0 (respectively b′0 ) be equal to the balance of
     LNCS, vol. 13301. Springer, 2022, pp. 428–446.                            σ (respectively σ ′ ) in τ0 and b1 , b′1 be the balance of those
[42] C. Baum, B. David, and T. K. Frederiksen, “P2DEX: privacy-preserving
     decentralized cryptocurrency exchange,” in Applied Cryptography and       contract states in τ1 . From this point onward we will also
     Network Security (ACNS), ser. LNCS, vol. 12726. Springer, 2021, pp.       denote tx.v as v. Finally pr0 and pr1 are the prices of tokens.
     163–194.                                                                  The adversarial gain can be calculated from the contract
                            A PPENDIX                                          balances as follows:
A. Non existence of MEV in the general case                                            gainMoves σ tr’ = pr0 (b0 − b′0 ) + pr1 (b1 − b′1 )
   In this appendix we consider the corner case in which MEV                               tx
                                                                               Since σ ′ −→ σ ′′ we can calculate the balance of σ ′′ . In τ0 this
fails to exist for an AMM contract.                                                                                          b′ b′
   Specifically, we consider an AMM contract, starting in a                    balance is equal to b′0 + v, and in τ1 it is ′ 0 1 .
                                                                                                                            b0 + v
state σ such that the mempool in σ contains a single transaction                 To give a bound on gainMoves σ’’ tr’’ we notice that
tx with tx.vmin = 0 and tx.inputValue = τ 0 . In such a                        tr” only contains adversarial moves. Therefore we can use
scenario we can prove that MEV σ does not exist, and that                      the results on the MEV of AMMs with an empty mempool to
MEVSup σ is equal to extractable σ + tx.v * pr0 .                              conclude that
   We prove the existence of MEVSup σ with two propositions:
the first one establishes that the gain of the adversary is strictly            gainMoves σ ′′ tr” ≤ extractable σ ′′ =
bounded from above, while the second one establishes that the                                                   b′ b′
                                                                                          = pr0 (b′0 + v) + pr1 ′ 0 1 − 2 b′0 b′1 pr0 pr1
                                                                                                                         p
adversary can extract a value that is arbitrarily close to that                                                b0 + v
upper bound.
                                                                                 Finally remembering that tx itself gains no token for the
Proposition 1. The value that the adversary can gain                           adversary, and that b0 b1 = b′0 b′1 , we can use Equation (1) to
by performing a sequence of transactions in σ is strictly                      obtain that gainMoves σ tr must be smaller than
less than extractable σ + tx.v * pr0 . In short, we have                                            b′ b′
                                                                                pr0 (b0 + v) + pr1 ′ 0 1 + pr1 (b1 − b′1 ) − 2 b0 b1 pr0 pr1
                                                                                                                                p
  ∀ tr, gainMoves σ tr < extractable σ + tx.v * pr0                                                b0 + v
                                                                               which in turn can be rewritten as
Proof. Since the mempool contains a single transaction, we
                                                                                                                    b′ b′
can assume that tr either includes a single mempool move or                             extractable σ + pr0 v + pr1 ′ 0 1 − pr1 b′1
none at all. Indeed, although theoretically tr could include                                                       b0 + v
more than one mempool move, at most one of them can                                      b′0
                                                                               Since          < 1 we have shown that every trace extracts a
be executed succesfully, since the contract semantics would                           b′0 + v
remove the transaction from the mempool after executing it.                    value that is below extractable σ + pr0 v.
An unsuccessful move leaves the contract state unaltered, so                   Proposition 2. There exists a sequence moves tr that the
we can prune these failing moves from tr.                                      adversary can perform in σ order to gain an amount of value
   The case in which tr features no mempool transactions
                                                                               that is arbitrarily close to extractable σ + tx.v * pr0 . In
is simple: indeed this is akin to working in a contract
                                                                               short, we have:
with an empty mempool. From our results on AMMs with
empty mempool (MEV_empty_mempool, AMM_MEV_guess and                               ∀ (ε : R+), ∃ tr,
exact_gain_simple) we know that such a contract would have                        gainMoves σ tr + ε ≥ extractable σ + tx.v * pr0
MEV equal to extractable σ , and since both tx.v and pr0
are positive, we have:                                                         Proof. To prove this proposition we will calculate the gain of
          gainMoves σ tr ≤ extractable σ                                       a trace parametrized by the positive real value x ∈ R+ .
                          < extractable σ + tx.v * pr0                            First, we name some contract states and transactions.
                                                                                  • σ is the state in which the AMM is balanced, i.e. the state
  which proves our proposition.
                                                                                    in which
  Instead, if tr contains the mempool move that executes tx,                                             b0 · pr0 = b1 · pr1
we can write it as follows:
          tr = tr’ :: mempool id :: tr’’                                            where b0 (respectively b1 ) is the balance of σ in τ0
                                                                                    (respectively τ1 ).
  •   mσ is the transaction that balances the AMM when                       gainMoves σ tr(x) + ε ≥ extractable σ + tx.v * pr0
      applied in σ, i.e. the transaction such that
                                                                      proving our proposition.
                                   σm
                               σ −−→ σ
  • adv(x) is an adversarial transaction that sends x tokens
    of type τ0 to the contract.
     ′       ′′
  • σ and σ are states such that
                             adv(x)     tx
                          σ −−−−→ σ ′ −→ σ ′′
      It easily follows from the definition of adv(tx) that the
      balance of σ ′ in τ0 is b0 + x, and that its balance in τ1 is
       b0 b1
      b +x
             . Similarly, from the definition of tx, we have that
       0
                                                      b0 b1
    the balance of σ ′′ is b0 + x + tx.v in τ0 and b +x+tx.v
                                                    0
    in τ1 .
  • mσ is the transaction that balances the AMM when
    applied in σ ′′
  We define tr(x) as the following list of moves:
              tr(x) := mσ :: adv(x) :: tx :: mσ′′
  We will now calculate the amount of tokens that the
adversary gains from appending tr(x) to the blockchain.
  • mσ yields

                   pr0 (b0 − b0 ) + pr1 (b1 − b1 )
                                    
                               b b
  • adv(x) yields pr1 b1 − 0 1 − pr0 x (a negative quan-
                               b0 +x
    tity).
  • tx is a mempool transaction, so it doesn’t yield any gain
    for the adversary.
                                            ′′
  • Finally, mσ ′′ yields extractable σ for the adversary
    which is equal to
                                   b0 b1
                                               q
       pr0 (b0 + x + v) + pr1               − 2 b0 b1 pr0 pr1
                               b0 + x + v
The gain of tr(x), which is the sum of all the above gains,
amounts to:
      pr0 (b0 − b0 ) + pr1 (b1 − b1 )
                  b0 b1
   + pr1 (b1 −          ) − pr0 x
                 b0 + x
                                  b0 b1
                                             q
   + pr0 (b0 + x + v) + pr1               − 2 b0 b1 pr0 pr1
                               b0 + x + v
Since we are working with a constant product AMM, we
have that b0 b1 = b0 b1 , meaning that expression above can
be simplified as
                              p
         pr0 b0 + pr1 b1 − 2 b0 b1 pr0 pr1 + pr0 v
                                                  
                                    1          1
                 + pr1 b0 b1              −
                               b0 + x + v b0 + x
which is equal to
                                                 1
 extractable σ + pr0 v − pr1 b0 b1 v
                                        (b0 + x + v)(b0 + x)
which gets arbitrarily close to extractable σ + pr0 v for
large values of x. Therefore, for all ϵ one can find a value of
x such that
