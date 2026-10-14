                                         Foundational Verification of Smart Contracts through
                                         Verified Compilation
                                         VILHELM SJÖBERG, CertiK, USA
arXiv:2405.08348v1 [cs.PL] 14 May 2024




                                         KINNARI DAVE, CertiK, USA
                                         DANIEL BRITTEN, University of Waikato, New Zealand
                                         MARIA A SCHETT, University College London, England
                                         XINYUAN SUN, CertiK, USA
                                         QINSHI WANG, Princeton University, USA
                                         SEAN NOBLE ANDERSON, Portland State University, USA
                                         STEVE REEVES, University of Waikato, New Zealand
                                         ZHONG SHAO, Yale University, USA
                                         Programs executed on a blockchain—smart contracts—have high financial stakes; their correctness is crucial.
                                         We argue, that this correctness needs to be foundational: correctness needs to be based on the operational
                                         semantics of their execution environment. In this work we present a foundational system—the DeepSEA
                                         system—targeting the Ethereum blockchain as the largest smart contract platform. The DeepSEA system
                                         has a small but sufficiently rich programming language amenable for verification, the DeepSEA language,
                                         and a verified DeepSEA compiler. Together they enable true end-to-end verification for smart contracts. We
                                         demonstrate usability through two case studies: a realistic contract for Decentralized Finance and contract for
                                         crowdfunding.
                                         Additional Key Words and Phrases: Verification, Verified compilation, Blockchain, Smart Contracts

                                         1   INTRODUCTION
                                         Blockchains are distributed systems for recording and processing data. They are public, i.e., not
                                         subject to permissions or visibility-controls, decentralized, i.e., not controlled by any single party,
                                         and use a consensus mechanism to ensure consistency and immutability of the widely and openly
                                         distributed data. Blockchains were spearheaded by Bitcoin [Nakamoto 2008] for simple transactions
                                         of passing bitcoins between accounts. The Ethereum blockchain generalized these transactions:
                                         users can execute arbitrary programs. These programs are compiled to bytecode for the Ethereum
                                         Virtual Machine (EVM). This bytecode is then uploaded on the Ethereum blockchain and therefore
                                         immutable. Users can now call the bytecode of a program and such a transaction can change a
                                         range of state variables—also stored on the blockchain—by executing the Turing complete program.
                                         These programs are known as smart contracts. Smart contracts programmatically transfer money
                                         following this immutable bytecode. In the last few years, their promise and problems have become
                                         apparent. On the one hand Ethereum is widely used, in particular in decentralized finance (DeFi).
                                         Cryptocurrencies trading has moved from centralized brokers to smart contracts and process a
                                         yearly trading volume of tens of billions of dollars. On the other hand these smart contracts have
                                         security flaws. Each year there are dozens of hacks resulting in losses of hundreds of thousands, or
                                         even millions of dollars.
                                            Stakes as high as these attracted verification efforts. Many tools leverage automatic theorem
                                         proving by annotating smart contracts with pre- and post-conditions. These are translated into
                                         Authors’ addresses: Vilhelm Sjöberg, CertiK, USA, vilhelm.sjoberg@certik.io; Kinnari Dave, CertiK, USA, kinnari.dave@
                                         certik.io; Daniel Britten, University of Waikato, New Zealand, db130@students.waikato.ac.nz; Maria A Schett, University
                                         College London, England, mail@maria-a-schett.net; Xinyuan Sun, CertiK, USA, sxysun@certik.io; Qinshi Wang, Princeton
                                         University, USA, qinshiw@cs.princeton.edu; Sean Noble Anderson, Portland State University, USA, ander28@pdx.edu;
                                         Steve Reeves, University of Waikato, New Zealand, stever@waikato.ac.nz; Zhong Shao, Yale University, USA, zhong.shao@
                                         yale.edu.
    Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
2                                                                                               Reeves, and Zhong Shao

verification conditions (VCs) for an SMT solver. However, the theories that can be automatically
handled by SMT solvers are limited. So while these tools worked well for the simple “token”
contracts that dominated the landscape a few years ago, we believe more complex applications such
as DeFi necessitate interactive proof assistants. Even tools that can generate VCs for interactive
proof (e.g. via intermediate languages like Why3) have weaknesses: the VC generation is not
itself verified, so the verification tool itself could have correctness-critical bugs. This leads to the
demand of foundational systems, which are based on a formal semantics for the EVM machine
itself [Hildenbrandt et al. 2018; Hirai 2018]. Proving correctness with respect to an operational
semantics gives much higher confidence than proving VCs which were generated in an ad-hoc
way. Some of the most critical and high-value contracts, e.g. the staking contract for Ethereum 2.0,
have been foundationally verified [Park 2020; Ryan 2020]. However, working directly on bytecode
without the benefit of data abstraction is very laborious, which makes it hard to use these tools for
large contracts.
   In this work, we introduce the DeepSEA system, which provides the best of both worlds. We define
a programming language, small but sufficiently rich to write realistic programs, and implement a
verified compiler for it. The compiler compiles the source program into (1) EVM bytecode, and (2) a
formal model which can be loaded into the Coq proof assistant to prove correctness properties. The
DeepSEA language is designed to make programs amenable to verification. Programs are structured
to enable modular verification, inspired by previous work on large program verification. It also tries
to shield the user as much as possible from data representation concerns, by making the Coq model
use idealized “mathematical” data types like unbounded integers and finite maps, and separate out
concerns about finite word-size and array bounds into a side-condition that can be verified before
dealing with the main proof. We have tried the system on realistic smart contracts, and find it both:
powerful and user-friendly. The DeepSEA compiler is implemented and verified in Coq, and the
correctness theorem is internalized so one can check a theorem inside Coq that a particular smart
contract specification is implemented by a given bytecode.
   Writing a verified compiler for a blockchain language also revealed some interesting points that
do not come up in more traditional verified compilers. The EVM tracks gas cost and charges money
for each step of execution and each byte stored on the blockchain. So the compiler correctness
proof must take gas cost into account at each phase, and when phrasing the correctness theorem
we must be careful to make sure it is still informative even if the compiler optimizes the gas cost.
Gas costs for storing the bytecode on the blockchain also means that a slightly different set of
optimizations are relevant: we want to minimize program size. Finally, unlike a compiler for C, we
must be careful to distinguish undefined behavior which should be avoided by the programmer, e.g.
an integer overflow, versus erroneous behavior that can always be triggered by an attacker, e.g. an
out-of-gas exception.
   Specifically we make the following contributions:

        • an integrated system for proving smart contract correctness, consisting of a programming
          language (Section 2), tools for producing a Coq model of a contract (Section 2.2) and set of
          Coq tactics for reasoning about that model (Section 3.2.1),
        • two case studies: a realistic DeFi contract (Section 3.1) and a crowdfunding contract (Sec-
          tion 3.2). We evaluate the proof effort of the crowdfunding contract by comparing it to a
          similar proof by a non-foundational tool, and find that DeepSEA is similarly user-friendly
          (Section 3.2.4).
        • a verified compiler from the DeepSEA language to EVM with several interesting features:
          we compile via a general-purpose intermediate language (Section 4.2) with a novel memory
Foundational Verification of Smart Contracts through Verified Compilation                            3


        model (Section 4.2.1) and we use an extensible way to abstract away from datatype represen-
        tation (Section 4.2.2). Our correctness statement distinguishes datatype-related undefined
        behavior from genuinely unavoidable errors (Section 4.2.3). The compiler correctness proofs
        track gas cost through all the phases (Section 4.3.1). We describe how to apply a large
        collection of automatically proven peephole optimization rules, which is particularly helpful
        in the EVM setting (Section 4.4).

2     THE DEEPSEA PROGRAMMING LANGUAGE
At the center of the DeepSEA system is a small programming language. Each program is written
as a set of objects with methods and state variables, corresponding to contract methods and data
which is persistently stored on the blockchain. We base this work on an earlier version of the
DeepSEA language [Sjöberg et al. 2019] which aims to support verified operating system kernels
and compiles into C and Coq. We now target the EVM and Coq. As such, we inherit a set of
language features to support modular proofs. Each program is divided into a set of objects, which
are further grouped into “layers”, and one can further use “abstraction refinement” to ascribe a
simpler, manually written, specification to part of a program. We have not used these features
extensively in our current blockchain case studies, but we expect them to become relevant when
verifying even larger smart contract applications.
   DeepSEA supports primitive built-in datatypes like int or bool, and allows users to define
datatypes using the keyword type. It also supports arrays, hashmappings, and structs which are
defined as a collection of fields. However, complex data is currently only used for persistent storage,
while method arguments and local variables are word-sized.
   Our compilation target is the Ethereum Virtual Machine (EVM). Each node in the Ethereum
network has a bytecode interpreter which executes EVM bytecode as part of processing transactions.
The EVM is quasi-Turing complete: termination is guaranteed by executing code using a fuel called
gas. Each time you submit a transaction you pay for a certain number of units of gas, and the
system can execute bytecode only as long as there is gas available to run it, with the gas cost for
each instruction execution defined by the EVM specification [Wood 2021].
   The EVM is a stack based machine, which departs from the standard von Neumann architecture,
in the way it handles storage of programs. Instead of storing the code of the program in a memory
location which is generally accessible, it stores it in a virtual ROM-like memory, which can only
be accessed by a special construct for EVM programs called the constructor. The EVM model has
three different types of regions to store data during program execution: stack, memory and storage.
The stack stores data which can be popped off or pushed on during program execution through
special instructions designed exclusively for stack manipulation. The memory is a volatile word
addressable byte array. The storage on the other hand is a persistent word addressable word array,
which is a part of the VM state description. The standard implementation of hashmappings in
Ethereum programming languages just writes directly to a storage address, which will be backed
by a real hashtable in the bytecode interpreter.

2.1    DeepSEA language by example: a token contract
We now demonstrate the DeepSEA language by showing a small program: a “token contract”.
Tokens are fungible units of exchange, and the contract maintains a database of how many tokens
each user owns. In effect, a token contract creates a new cryptocurrency which can be transferred
between users, and token contracts are by far the most common type of contracts on Ethereum
currently. In order to maintain uniformity and aid ease of conversion, the Ethereum foundation
has created a standard known as ERC-20 which specifies what methods a token contract shall
implement.
         Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
     4                                                                                               Reeves, and Zhong Shao

        The implementation of an ERC-20 compliant token in DeepSEA is laid out in the token.ds file
     which we will describe in this section. It initially assigns a balance of 100000 token units to the
     owner of the contract. The interface of this contract allows transfer of tokens, querying the balance
     of this particular token in an account and gives the constructor which initializes the owner’s
     account with a fixed supply of the tokens. The entire DeepSEA program in token.ds consists of a
     single object and layer. Because the layer does not depend on any layer below it is declared in the
     following manner:
1    layer TOK : [{}] TOKSig = {
2      tok = Tok
3    } assert "Invariant.inv"
        Here, the square brackets followed by the layer declaration enclose layer dependencies—in our
     case the empty list of signatures {} indicates a low-level layer with no dependencies beneath.
        Invariants for objects (or layers) are declared with assert. The user must prove that invariants
     are preserved by all methods declared inside objects. The DeepSEA compiler generates a set of
     verification side-conditions, and the invariant is also available when proving those.
        In our example, the Invariant.inv condition requires that the balance of the token being
     implemented in all accounts is non-negative and that the sum of the balances must add up to the
     total supply of the token. Finally, tok is the object enclosed within this layer. Its signature is given
     as follows:
1    object signature ERC20Interface = {
2      constructor : unit -> unit;                               transfer : address * int -> bool;
3      const totalSupply : unit -> int;                          approve : address * int -> bool;
4      const balanceOf : address -> int;                         transferFrom : address * address * int -> bool
5    }
       The Tok object is an instance of an object with the above signature and highlights various
     important features of DeepSEA:
1    object Tok : ERC20Interface {
2      let balances : mapping[address] int := mapping_init
3      let allowances : mapping[address] mapping[address] int := mapping_init
4      let constructor () = balances[msg_sender] := 100000
5      let balanceOf tokenOwner = let bal = balances[tokenOwner] in bal
6      let transfer(toA, tokens) =
7        let fromA = msg_sender in let from_bal = balances[fromA] in let to_bal = balances[toA] in
8        assert (fromA <> toA /\ from_bal >= tokens);
9        balances[fromA] := from_bal-tokens;
10       balances[toA] := to_bal+tokens;
11       true
12       ...
13     }
        We can see that DeepSEA does not use dynamic memory allocation, and the balances and
     allowances mappings are initialized using the placeholder initializer mapping_init which initial-
     izes them with zeros (a no-op on the EVM).

     2.2      Verifying smart contracts
     Now we discuss the Coq specifications which DeepSEA generates, and the choice of datatype
     representation in these specifications. The DeepSEA compiler dsc generates a directory token
     as a part of the compilation process of the DeepSEA source file token.ds. As a result the token
     directory is populated with the files LayerTOK.v and ObjTokCodeProofs.v among others. The
     file LayerTOK.v is where the Coq specifications of the methods in various objects defined in the
     layer are written. Since the token.ds contract consists of exactly one layer TOK and one object Tok
         Foundational Verification of Smart Contracts through Verified Compilation                                      5


         inside, with no dependency on any underlying layer, it is considered to be in kernel mode. The
         data types used to represent the variables balances and allowances are declared as fields of the
         record global_abstract_data_type:
1        Record global_abstract_data_type : Type := Build_global_abstract_data_type
2          { Tok_balances : Int256Tree.t Z32;
3            Tok_allowances : Int256Tree.t (Int256Tree.t Z32) }
      Every Gallina1 specification generated for the methods defined in this object uses this data repre-
      sentation in its definition, as is evident from the Tok_transfer_opt definition below. Since the
      program is defined as a single layer, and is not a vertical composition of two layers, the instance
      generated for the _overlay_spec is the empty record and the _underlay_spec is simply the in-
      stance GlobalLayerSpec declared for the entire program. Similarly, the object variables balances,
      allowances are represented by the definitions ending with _var as defined in the LayerTOK.v.
     The constructor is represented by the definition ending with _constructor.
         We now illustrate the specification generation mechanism of DeepSEA and the proof generation
      of its equivalence to the code through its treatment of the transfer function defined as a part of the
      object definition above. The generated Tok_transfer definition has type function_constr which
      is a record type parametrized by an element of type LayerSpecClass. The Gallina specification is
      the definition Tok_transfer_opt which is of type int256 -> Z32 -> machine_env GetHighData
     -> DS bool. Also generated by dsc are automatic proofs of the fact that the ASTs that it generates
      for all the methods are well-typed:
1        Lemma Tok_transfer_wf : synth_func_wellformed Tok_transfer.
2          Proof. solve_wellformed. Defined.
         The dsc generated specification for the transfer method is given as follows. Note that address is a
         type alias for int256.
     1      Tok_transfer_opt memModelOps f f0 me : DS bool :=               (* Corresponding .ds file: *)
     2      spec1 <- ret (me_caller me);;                                   (* let fromA = msg_sender *)
     3      spec2 <- gets                                                   (* let from_bal = balances[fromA] *)
     4        (fun s => get_default 0 f (Tok_balances s));;
     5      (v <- ret (negb (eq spec1 f) && (spec2 >=? f0));;               (* assert (fromA<>toA               *)
     6        guard v);;                                                    (*        /\ from_bal>=tokens)      *)
     7      modify
     8        (fun s => update_Tok_balances
     9        (set spec1 (spec2 - f0) (Tok_balances s)) s);;                (* balances[fromA] := from_bal-tokens *)
    10      modify
    11        (fun s => update_Tok_balances
    12        (set f (spec3 + f0) (Tok_balances s)) s);;                    (* balances[toA] := to_bal+tokens      *)
    13        ret true.
            The _opt suffix in the name of the generated specification refers to the use of the option monad
         to capture the effect of assertion failures. The effects of commands are captured in the specification
         using the monadic type:
         Definition DS := stateT GetHighData option. (* DS a = GetHighData -> option(a*GetHighData) *)
            Since the specification is what the user will reason about in the proofs, we want it to correspond
         in an obvious way to the input program, and it mostly does except apart from being written in Coq
         syntax instead of DeepSEA syntax and using monadic combinators for the imperative operations.
            If we look at the details, in some ways the Coq representation is actually more high-level and
         easier to reason about than the input program. While compiled Ethereum hash tables do not keep
         track of which keys are stored in them, in the Coq version we represent the balances table with a
         Int256Tree data type which does remember its keys. The executable code still cannot make use
         1 Gallina is the specification language of Coq.
        Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
    6                                                                                               Reeves, and Zhong Shao

    of the keys, but theorems about the code can talk about them. Similarly, while the executable
    program uses bounded 256-bit integers, the representation uses unbounded mathematical integers
    so that theorems about ordinary arithmetic applies. Instead, the DeepSEA system generates a set of
    separate side conditions for the user to prove there is no overflow.
       We can then write theorems about the generated specifications just as we would for any monadic
    Coq function. Consider, for example this lemma about the tok_transfer_opt satisfying the in-
    variant that the sum of the balances of the token in all accounts remains constant after a transfer:
1   Theorem transfer_constant_balances_sum : forall toA n d d' me b,
2   runStateT (Tok_transfer_opt toA n me) d = Some (b, d') -> balances_sum d' = balances_sum d.
       Let us consider the above theorem statement. Note that the variables characterizing the data
    needed for the contract to execute any of its methods are the maps balances and allowances.
    Hence, the state in this case is represented by global_abstract_data_type as defined above. The
    monadic evaluator runStateT evaluates the effect of calling the transfer method in state 𝑑 and
    returns a value of type DS bool which is an option on the bool * state pair. In case of a successful
    run (i.e no assertion failure was reported) the theorem states that the sum of the balances in the
    new state 𝑑 ′ is the same as that in the state 𝑑. DeepSEA defines a few custom tactics to help proving
    such results by simplifying monadic computations in the context.

    3      CASE STUDIES
    The small token contract discussed above is easy to verify using many methods. In this section we
    discuss two larger case studies, where the power of reasoning about high-level semantics in an
    interactive proof assistant is crucial.

    3.1      Uniswap-style market maker
    An example that highlights the importance of having a language which enables reasoning about
    code at “all levels” is the automated market maker smart contract prototype. Constant-product
    automated market makers is one of the most important and popular smart contract types in
    decentralized finance (DeFi). They support exchange of tokens on blockchain-based platforms
    without a centralized party keeping track of such transactions. This is accomplished by maintaining
    liquidity reserves of two tokens, and determining the exchange rate using a mathematical formula
    which is a function of the token reserves. Various users can provide liquidity of tokens in return
    for receiving the transaction fees charged by the contract to the traders.
       These contracts also serve as oracles which can be queried for the current market rate for
    particular exchanges. Other contracts, e.g. for lending and margin trading, use this price information
    to value token deposits used as collaterals. Hence, manipulating such oracles can prove to be very
    beneficial to hackers.
    3.1.1 Contract implementation. The smart contract written in DeepSEA uses the Uniswap v2
    protocol as a blueprint. In the DeepSEA setup, the entire contract is defined as a layer AMM on top
    of an underlay layer called the AMMLIB. The AMMLIB layer consists of three objects: two ERC20
    tokens which are to be swapped and a liquidity token. The AMM layer acts as the interface for the
    contract. This layer consists of an object of type AMMInterface, which defines the methods that
    provide all the functionalities of the protocol. The methods in this object signature are given as
    follows:

            • simpleSwap0 allows the transfer of one token to the contract to be exchanged for the other,
              and returns the amount of the second token to be received in return;
            • mint allows the transfer of liquidity to a liquidity pool for a liquidity provider;
     Foundational Verification of Smart Contracts through Verified Compilation                          7


          • burn allows a liquidity provider to withdraw liquidity from a pool;
          • sync is a recovery mechanism method to prevent the market for the given pair from being
            stuck in case of low reserves;
          • skim prevents any user from depositing more tokens in any reserve than the maximum
            limit, to prevent overflow;
          • k tracks the product of the reserves;
          • quote0 returns the equivalent amount of the second token, given an amount of the first
            token and current reserves in the contract;
          • getAmountOut0 returns the maximum possible amount of a token than can be gained in
            exchange for a particular input amount of the other token and that of the reserves;
          • getAmountIn0 returns the amount of a given token that must be input in order to obtain
            the desired amount of the other token under the given reserves.
     Compared to the Uniswap protocol, we have made a few simplifications. Unlike Uniswap, which
     offers the option of switching on/off the protocol fee, the DeepSEA contract does not model protocol
     fees. Moroever, instead of using the above mentioned square root formula to calculate the share of
     minted liquidity tokens for a liquidity provider, the DeepSEA contract uses the product and burns
     the first 1000 coins, as in Uniswap v2. The price oracle mechanism is based on Uniswap v1, and
     the DeepSEA contract does not support flash swaps. In order to make our contract completely
     ABI-compatible with the original we may add these features. However, the DeepSEA AMM contract
     already offers all the core functionality offered by the Uniswap protocol, and it contains everything
     that is relevant to the specification that we are verifying. As such, our proof is an example of
     verifying a realistic contract.
        The exchange of two tokens is enabled by the simple swap function declared as a part of the
     AMMInterface signature above. The method definition is given as follows:
1    let simpleSwap0 (toA) =
2        let reserve0 = _reserve0 in
3        let reserve1 = _reserve1 in
4        let balance0 = erc20Token0.balanceOf(this_address) in
5        let balance1 = erc20Token1.balanceOf(this_address) in
6        let amount0In = balance0 - reserve0 in
7        let token0 = _token0 in
8        let token1 = _token1 in
9        assert (toA <> token0 /\ toA <> token1);
10       assert (amount0In > 0);
11       assert (reserve0 > 0 /\ reserve1 > 0);
12       let amountInWithFee = amount0In * 997 in
13       let numerator = amountInWithFee * reserve1 in
14       let denominator = reserve0 * 1000 + amountInWithFee in
15       let result = numerator / denominator in
16       let success = erc20Token1.transfer(toA, result) in
17       assert (success);
18       let balance0 = erc20Token0.balanceOf(this_address) in
19       let balance1 = erc20Token1.balanceOf(this_address) in
20       _reserve0 := balance0;
21       _reserve1 := balance1;
22       let resultU = result in
23       resultU

        The main object of the contract is 144 lines, to be compared with 200 lines of the original
     UniswapV2Pair.sol contract which we are imitating. Although these are not very large by conven-
     tional software development terms, it is big enough to show practical issues with the development
        Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
    8                                                                                               Reeves, and Zhong Shao

    system, for example we had to add a live-variable analysis phase to the DeepSEA compiler to fit all
    the local variables on the EVM stack.
    3.1.2 Proof. Recent work [Angeris et al. 2019] develop a mathematical analysis of this style of
    AMMs. One of their theorems is was a lower bound on the cost of trades to move the reported price
    of the contract by a certain amount. This theorem provides measures of the various parameters
    that needed to be controlled in order to prevent oracle-manipulation attacks.
       Using DeepSEA we formally proved this theorem in the Coq, connecting the parameters involved
    directly to the generated bytecode, while being rigorous about integers versus real numbers. We
    state and prove the cost_of_manipulation_min result under the assumption that a swap operation
    was successful (as indicated by the hypothesis del_alp):
1   Hypothesis del_alp : runStateT (AutomatedMarketMaker_simplSwap0_opt
2         toA (make_machine_env a)) s = Some (r , s').
3
4   Theorem cost_of_manipulation_min : eps >= 0 ->
5         cost_of_manipulation_val >= (IZR (reserve_beta s)) * (5/100) * sqrt (eps) \/
6         cost_of_manipulation_val >= (IZR (reserve_beta s)) * (1/48) * (eps^2).
       The DeepSEA system generated specification of the simpleSwap0 method enables us to establish
    a lower bound for this cost and connect it directly to the bytecode generated for this contract. The
    details of the proof have been published as a workshop paper [Anonymised 2021]. Here, we just
    note that it requires some nontrivial mathematical results, e.g. the the Taylor series approximation
    twice differentiable functions. We rely on existing libraries like Coq-interval [Martin-Dorel et al.
    2013] and Coquelicot [Boldo et al. 2015] for these. This highlights the benefit of using an interactive
    theorem prover which can handle arbitrary mathematical reasoning.

    3.2      Crowdfunding
    The automated market maker example shows that DeepSEA can verify a complex smart contract.
    We next consider the usability when writing interactive proofs in DeepSEA. Two other Coq-based
    systems for reasoning about smart contracts, Scilla [Sergey et al. 2019] and ConCert [Annenkov
    et al. 2020], both use a Crowdfunding contract to evaluate their system. In this section we use the
    same benchmark, and consider a DeepSEA Crowdfunding smart contract based upon the Scilla
    version [Zilliqa 2020]. The correctness proof is roughly as complex as for the Scilla version. Scilla
    and ConCert do not have verified backends and define the Coq representation of the contract in a
    way which is convenient to reason about, so we consider this a sign that DeepSEA’s representation
    is adequate.
       The Crowdfunding smart contract decentralises fundraising for a project by setting a funding
    goal and time limit, and letting users make donations. If the goal is met within the time limit, the
    project receives the funds and if not, then all backers can reclaim their funds. Listing 1 shows the
    donate function in the DeepSEA version of the Crowdfunding contract.
    3.2.1 Reasoning about monadic programs in Coq. One difference between our proofs and the Scilla
    proofs is that our Coq model of the contract is specified as a function in the state monad rather than
    an inductively defined relation. This makes the connection between the DeepSEA source program
    and the Coq model more obvious, and one can extract code from specifications which could be
    helpful for QuickChick-style automated testing [Dénès et al. 2014]. From a practical perspective,
    this means we need some changes to the proof tactics we use, particularly inversion.
       If the semantics of a programming language is given by an inductively defined step relation,
    then the inversion tactic can take e.g. an assumption about a sequenced command steps st1
    (c1;;c2) st2 and conclude that there exists some intermediate state st such that steps st1 c1
     Foundational Verification of Smart Contracts through Verified Compilation                                  9


1    let donate () =
2      assert(msg_sender <> this_address);
3      assert(msg_value >= 0);
4      let bs = backers in
5      let blk = block_number in
6      let _max_block = max_block in
7      if (blk > _max_block) then
8        begin
9          emit Message(_deadlinePassed_msg);
10         assert(false) (* Revert: do not accept funds *)
11       end
12     else
13       begin
14         let backed_amount = backers[msg_sender] in
15         if (backed_amount = 0) then
16              backers[msg_sender] := msg_value
17         else
18           begin
19              emit Message(_alreadyDonated_msg);
20              assert(false) (* Revert: do not accept funds *)
21           end
22       end


                   Listing 1. The donate function of the Crowdfunding smart contract in DeepSEA


     st and steps st c2 st2. Similarly, if the step rules specify how the state is updated, the tactic
     introduces equalities into the context. Contract correctness theorems have the form “if a state
     is reachable by a sequence of steps, then . . . ”, so their proofs heavily rely on using inversion to
     decompose the sequence.
        In our case, the semantics of code sequencing c1;;c2 is specified by the bind function for the
     state monad, so the built-in inversion tactic does not do anything, and instead we prove lemmas
     saying e.g. “if runStateT (c1;;c2) st1 = Some (return_value, st2) then there exists an
     intermediate state st such that . . . ”, and similarly for equations, and then provide a custom-written
     tactic inv_runStateT to apply them.
        While this is simple in theory, we found that it required some care in practice because some of
     Coq’s built-in methods take more than linear time in the size of the terms they work on. For small
     examples there are no issues, but for the large method specifications from e.g. the market maker
     example, they get intolerably slow. For the subst tactic, which exploits equalities, we needed to
     turn off Coq’s Regular Subst Tactic flag. And the destruct tactic, which uses “there exists”
     assumptions, seems to take at least quadratic time, so we can not use a literal existential statement
     in the above lemma. Instead we use a Church-encoded version.
        With inv_runStateT, reasoning about inversion of monadic functions is just as convenient as
     inversion of inductive relations. We also define the tactic inv_runStateT_branching which also
     branches at every conditional statement.
     3.2.2 Proofs. The correctness property we aimed to prove was that if a backer made a donation
     but the goal was not met, then the backer is able to get their donation back. As first discussed
     in [Sergey et al. 2018], the following three properties taken together provide this guarantee.
         (1) The contract’s balance is not less than the recorded sum of all the backers’ contributions.
         (2) If the goal is not met and the time expires, it is possible for backers to withdraw their funds.
         (3) The recorded balances are not altered except when depositing and valid withdrawals.
     Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
    10                                                                                           Reeves, and Zhong Shao

       DeepSEA does not include a model of blockchain interactions, i.e. what sequences of method
    calls are possible. Currently, the user must manually define that as part of the statement of the
    correctness theorem. In the case of the Crowdfunding contract we define a step relation which
    makes method calls while keeping track of blockchain parameters like user balances and block
    numbers. We then define a reachability predicate ReachableFromBy in terms of the step relation.
    This predicate describes which states are reachable from a starting state by a list of intermediate
    steps and actions.

      Lemma 3.1. The contract’s balance is not less than the recorded sum of all the backers’ contributions.

       As part of the user defined model of blockchain interactions the predicate Safe is defined, which
    is True when the given predicate defined over an individual state of the blockchain model is true for
    all reachable states. This is useful for defining the lemma. We can state that the contract’s balance
    is not less than the recorded sum of all the backers’ contributions in Coq as follows:
1   Definition balance_backed state := (Crowdfunding_funded (contract_state state)) = false
2     -> sum (Crowdfunding_backers (contract_state state)) <= (balance state (contract_address))
3        /\ (forall k v,
4              get k (Crowdfunding_backers (contract_state state)) = Some v
5              -> ((v >= 0) /\ (v < Int256.modulus))).
6   Lemma sufficient_funds_safe : Safe balance_backed.

      The proof uses induction on ReachableFromBy. After proving that the initial state satisfies the
    invariant balance_backed, each of the cases representing different possible blockchain actions are
    considered.
      When reasoning about the donate function, lemmas about the datatype used for the backers
    mapping are required. At one point a lemma stating that if an item 𝑘 in a mapping initially has the
    value zero, then setting 𝑘 to the value 𝑣 means the sum now is the original sum plus 𝑣. The proof
    heavily uses the inv_runStateT_branching tactic mentioned earlier. While completing these
    proofs it also became clear how useful it is that DeepSEA enables a quick workflow for switching
    between proving and improving the contract’s implementation (after finding the occasional bug in
    the contract during the proof process).

      Lemma 3.2. If the goal is not met and the time expires, it is possible for backers to withdraw their
    funds.

       This lemma is proved in a similar manner, with the exception that it is also necessary here to
    prove that the contract does not revert in certain circumstances, which helps guarantee that it is
    possible for backers to withdraw their funds. The proof makes use of the previous lemma in order
    to guarantee that the smart contract has sufficient funds to refund the backer. This distinguishes
    our proof from the Scilla version which is not structured in a way which makes this link between
    the lemmas in Coq.

      Lemma 3.3. The recorded balances are not altered except when depositing and valid withdrawals.

       The final lemma is stated using a temporal predicate, claiming the following: in all states since
    a donation is recorded, that donation remains recorded as long as all intermediate states do not
    involve a claim from the donor. In other words, a donation is recorded since that donation was
    recorded, as long as there were no claims from the donor in the meantime. This lemma is expressed
    formally in Coq as shown here.
1   Lemma donation_preserved : forall (a : addr) (d : Z),
2     (donation_recorded a d) `since` (donation_recorded a d) `as-long-as` (no_claims_from a).
Foundational Verification of Smart Contracts through Verified Compilation                                        11


   The ability to state lemmas such as this, which involve reachability and properties about traces
of smart contract execution, highlights the expressivity that is a strength of DeepSEA coupled with
the user-defined blockchain model used for the Crowdfunding contract.
   The proof proceeds similarly to Lemma 3.1, by induction on the reachability predicate. The
inductive hypothesis as well as the assumption about the intermediate states having no claim from
the donor is sufficient to establish that the second to last state of the trace has the donation recorded.
The proof then shows that this final step also preserves the record of the donation.
3.2.3 Proofs of side conditions. As mentioned earlier, for a DeepSEA proof to be valid it is necessary
to also prove certain automatically generated goals, for example relating to the absence of overflows.
In the case of the Crowdfunding contract all the side conditions can be trivially discharged.
3.2.4 Evaluation. The proof of Lemma 3.1 uses about 260 Coq tactic invocations. The equivalent
proof in Scilla uses about 100 (though is written in the terser mathcomp proof style). In ConCert, it
is about 55. The proofs all follow a similar overall structure.

  These proofs about the Crowdfunding smart contract and the associated user-defined blockchain
model are available at: https://github.com/Coda-Coda/Crowdfunding/tree/foundational-verification-
paper.

4   VERIFIED COMPILATION
The DeepSEA compiler consists of an unverified
frontend called dsc and a verified compiler. The fron-            DeepSea source file
tend dsc is implemented in OCaml. It typechecks the
DeepSEA source code and also generates a directory               dsc                □     frontend compilation
of Coq files containing the AST of the program and
proofs connecting each layer declared in the source              MiniC           □
code. The generated Coq files then import the ver-                  explicit pointer dereferencing
ified compiler, which translates the AST into EVM                Clike           □
bytecode via an intermediate language called MiniC.                 control flow graph construction
   The dsc part is 11,000 lines of OCaml, while the              Clocal          □
verified part is 34,000 lines of Coq excluding com-
ments (as counted by coqwc there are 4847 lines spec             Cintptr
+ 6320 proof for AST to MiniC, and 15714 spec + 6993
proof for MiniC to EVM). Figure 1 gives an overview              Cgraph          □      WebAssembly
on the 12 phases of the compiler.                                   block construction
                                                                 Cbasic          □
4.1 Typechecking                                                    blocks linearized to statement lists
and elaboration into core language                               Clinear         □
The DeepSEA compiler frontend works in two steps.                   labeled entry points into program
In the first step the dsc tool typechecks the program.           Clabeled        □
In the second step it writes out a term in the core                 stack layout of arguments
language—desugared into a functional specification               Stacked         □
in Coq. The core language is defined as a datatype in               expressions no longer part of syntax
Coq, and the desugaring function serves as a deno-               Expressionless □
tational semantics which interprets the core terms                  establish single entry point
as simply typed lambda terms.                                    Methodical      □
   The core language syntax consists of typed expres-               EVM semantics
sions and commands. Expressions are typed with                   EVM_lem         □

                                                                            Fig. 1. Phases of the Compiler.
 Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
12                                                                                           Reeves, and Zhong Shao

respect to variable environments and commands are
typed with respect to variable environments as well
as layer signatures. Note that the distinction between expressions and commands makes it re-
dundant to define the formal semantics for expressions. Expressions are pure and do not have
side-effects, and are just a subset of the lambda calculus. Hence the semantics for desugaring them
just involve an embedding. Since DeepSEA only supports for loops, it is possible to translate them
into a functional specification using a total function (forM). The formal semantics for the commands
are defined denotationally with the help of monadic combinators ret, bind, get, set:

                synth_spec (val(𝑒))       =    ret 𝑒 (an embedding of an expression)
                     synth_spec (v)       =    gets (𝜆 𝑡 .𝑡) (gets (𝑓 : 𝑇 → 𝑈 ) := bind get (fun 𝑥 ⇒ ret (𝑓 𝑥)))
               synth_spec (v ← e)         =    modify (𝜆 t.set {t with 𝑣 = 𝑒 })
             (modify (𝑓 : 𝑇 → 𝑇 )         =    bind get (fun 𝑥 ⇒ put (𝑓 𝑥)))
      synth_spec (let 𝑥 = 𝑐 1 in 𝑐 2 )    =    bind synth_spec(𝑐 1 ) (𝜆 x. synth_spec(𝑐 2 ))
   synth_spec (if 𝑒 then 𝑐 1 else 𝑐 2 )   =    if 𝑒 thensynth_spec(𝑐 1 ) else synth_spec(𝑐 2 )
 synth_spec (for 𝑥 = 𝑒 1 to 𝑒 2 do 𝑐)     =    forM 𝑒 1 𝑒 2 synth_spec(𝑐)
            synth_spec (assert(𝑐))        =    guard synth_spec(𝑐)
   When we load a DeepSEA-generated file into Coq, we are evaluating the desugaring function
to generate the functional specification for the contract methods. The user proofs are done with
respect to that specification, and dsc generates a proof that the specification is refined by the
bytecode, so although the dsc tool is not itself verified it is not in the trusted computing base.

4.2   Translation into MiniC intermediate language
Rather than translating the core AST directly into EVM bytecode, we first translate it to an
intermediate language which we call MiniC. The syntax is shown in Figure 2. As the name suggests
it is similar to a subset of C, with the main differences being on the one hand a more limited support
for pointers, and on the other a set of primitive command for accessing blockchain features such as
transmitting money or querying the blockchain state.
    The DeepSEA source language was designed to be quite constrained in order to make it easy to
desugar it into Coq functions. For example it does not have mutable local variables, and loops are
restricted to a few terminating patterns. By contrast, MiniC is general-purpose, and we believe our
backend to be reusable for creating verified compilers for other blockchain languages.

4.2.1 Memory Model. In MiniC, most addresses (that is, L-values) are represented as extended
identifiers—recursively defined paths from a root identifier through its data structure (Figure 3).
For instance, if the identifier 𝑖 refers to an array of structs containing a field identified by 𝑖 ′ , then
Index(𝑖, 0) points to the first struct in the array, and Field(Index(𝑖, 0), 𝑖 ′ ) refers to the field 𝑖 ′ in
the first array. The root of an extended identifier is either Global(𝑖), indicating a persistent global
variable, or Local(𝑖), which will be allocated and deallocated at function calls and returns. The set
of L-values also contains raw hashes. A memory 𝑚 is a map from L-values to values.
   Using extended identifiers in place of a more typical block-offset model gives us some advantages.
First, the structure of an extended identifier corresponds directly to that of the sequences of hashes
that we use to access EVM storage at lower-level IRs, making compilation and proofs simpler.
Second, there is a clear distinction between addresses that would be aliased in the block-offset
model: a pointer to an array is different from the pointer to its first value. A pointer to an object’s
substructure, when passed as an argument, gives access only to that substructure, not the object as
a whole as is typical in C-like languages.
Foundational Verification of Smart Contracts through Verified Compilation                                       13


⟨type⟩ ::= Tvoid (the [void]            ⟨expr⟩ ::= Eint (𝑖, 𝑡) (integer           ⟨statements⟩ ::= skip
     type)                                   literal)                               | assign(𝑒 1, 𝑒 2 )
  | Tint(𝑖, 𝑠) (integer types)            | Eint256 (𝑖 256, 𝑡) (256-bit             | set(𝑖, 𝑒)
  | Tpointer(𝑝, 𝑡) (pointer                  integer literal)                       | call(𝑜, 𝑙, list 𝑒)
     types)                               | Evar (𝑖, 𝑡) (variable)                  | sequence (𝑠 1, 𝑠 2 )
  | Tarray(𝑡, 𝑧)         (array           | Eglob (𝑖, 𝑡) (global                    | ifte (𝑒, 𝑠 1, 𝑠 2 )
     types)                                 variable)                               | loop (𝑠)
  | Thashmap(𝑡 1, 𝑡 2 ) ( key             | Etemp (𝑖, 𝑡) (temporary                 | break
     type, elem type )                      variable)                               | return (𝑜)
  | Tfunction(𝑡𝑦_𝑙𝑖𝑠𝑡 , 𝑡)                | Ederef (𝑒, 𝑡) (pointer                  | transfer (𝑒 1, 𝑒 2 )
     (function types )                       dereference)                           | callmethod (𝑒, list 𝑖, 𝑖 1 )
  | Tstruct(𝑖, 𝑓 _𝑙𝑖𝑠𝑡)                   | Eaddr (𝑒, 𝑡) (address of                | log (list 𝑒 1, list 𝑒 2 )
     (struct types)                          an lvalue converted to                 | revert
  | Tunion(𝑖, 𝑓 )       (union               an rvalue pointer)
                                                                                           (c) Statements
     types)                               | Eunop (𝑜𝑝, 𝑒, 𝑡) (unary
  | Tcomp_ptr(𝑖) (pointer to                 operation)
     named struct or union)               | Ebinop (𝑜𝑝, 𝑒 1, 𝑒 2, 𝑡 1, 𝑡 2 )
                                            (binary operation)
⟨ty_list⟩ ::= Tnil
                                          | Efield (𝑒, 𝑖, 𝑡) (struct
  | Tcons (𝑡, 𝑡𝑙 )
                                             member access)
⟨f_list⟩ ::= Fnil                         | Eindex (𝑒 1, 𝑒 2, 𝑡)
  | Fcons(𝑖, 𝑡, 𝑓𝑙 )                      | Ecall0 (𝑏 0 )
                                          | Ecall1 (𝑏 1 )
    (a) Type representation
                                                  (b) Expressions

                                               Fig. 2. MiniC syntax

⟨𝑙 ∈ L-values⟩ ::= Eid (𝑝)                                      ⟨𝑝 ∈ extended identifiers⟩ ::= Global
  | Lhash1 (𝑖 256 )                                               | Local (𝑖 256 )
  | Lhash2 (𝑙, 𝑖 256 )                                            | Field (𝑝, 𝑖)
                                                                  | Index (𝑝, 𝑖 256 )
                  (a) Left Values
                                                                               (b) Extended identifiers

                                    Fig. 3. Extended identifiers as addresses


4.2.2 Datatype representation relation. One of the design decisions that makes reasoning about
DeepSEA generated specifications user-friendly is the choice of data representation in these func-
tional counterparts of the source code. We use mathematical types available in Coq such as 𝑍 ,
finite maps etc. to represent datatypes in the theorems that reason about specifications. While that
makes reasoning easier, the compiler must maintain a correspondence between these types and the
conventional C types used in the MiniC AST and ensure that this relation is preserved by any data
manipulation.
   The state representation for the execution context model used to reason about the specifications,
is given by a record in Coq (recall the token contract example in section 2) with a field for each
object in the DeepSEA source code containing a mathematical value. The state representation in
the MiniC IR consists of the memory model, described below, which is further parametrized by a
value 𝑑 of an abstract data type, representing trusted primitives. Defining a relation between these
 Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
14                                                                                           Reeves, and Zhong Shao

        tp(int) = Tint                       R𝑖𝑛𝑡 𝑛 Vint n ⇐⇒
       tp(unit) = Tvoid                            0 ≤ 𝑛 ≤ 232                                           𝑚,𝑡𝑝 (𝑇𝑖 )
                                                                                  R𝑇𝑖 𝑡 .𝑓𝑖 𝑣𝑖         𝑝𝑖 ↦−−−−−−→ 𝑣𝑖
                                             R𝑢𝑛𝑖𝑡 () Vint n ⇐⇒
                                                      (𝑛 = 0)                                    𝑡 R (𝑚, 𝑎)

                                Fig. 4. Data representation and State relations


two state representations involves defining a correspondence between the types of values used in
both the contexts and then a relation between the memory locations and the MiniC representation
of these values. We describe both these relations here.
                                 𝑚,𝑡 𝑦
   A relation of the form 𝑝 ↦−−−→ 𝑣 holds when upon loading from the memory 𝑚 at position 𝑝
yields the value 𝑣 which has type 𝑡𝑦. This defines the base case for simple values, for complex
values like structs and arrays the relation is defined recursively point-wise.
   With this relation defined, we now define the relation between type representations and then
the corresponding value representations in the specification and the MiniC implementation. The
mathematical types used in specifications are mapped to a corresponding C type via the inductively
definition type_pair. This relation can be thought of as a map from mathematical types to C types,
say 𝑡𝑝 (.) Finally, the relation between the specification values and the MiniC values is parametrized
by the mathematical type representing the value as illustrated by a few base cases in the figure
below.
   Once we have these two relations in place, they are composed for each object field 𝑓𝑖 in the
record representing a layer state for the specification and a corresponding extended identifier 𝑝𝑖 in
the MiniC program, to define the relation R for the entire layer.
4.2.3 Compilation correctness theorem. The command synthesis rules for this phase are fairly
standard, and we omit them here while making one remark. Note that because object fields behave
differently when loading values and assigning them respectively, expressions are further classified
as L-values and R-values respectively, and have distinct translation rules for both.
   Finally, there is a correctness theorem proved in Coq which states that the command translation
is correct with respect to desugaring if the verification conditions regarding data representation
generated by dsc hold. For each command 𝑐 the DeepSEA system defines a condition VC(𝑐, 𝑡) that
states 𝑐 can be correctly executed in state 𝑡. This is a large conjunction generated based on the
datatypes involved which the user must prove (with the aid of some provided tactics); for example
each time an integer variable is assigned the user must prove that it is in the range 0 ≤ 𝑥 < 2256 .
For a detailed exposition on the definition of such verification conditions, and the tactic mechanism
designed to solve them, we refer the reader to a previous publication [Sjöberg et al. 2019].
   With the verification condition aspect of this compiler duly noted, we have the compiler correct-
ness theorem stated as a simulation:
   Theorem 4.1. For every DeepSEA command 𝑐, its MiniC implementation 𝑚(𝑐), its specification 𝑠 (𝑐) ,
a state 𝑡 such that VC(𝑐, 𝑡) holds and a state 𝑡 ′ reached from 𝑡 upon the execution of runStateT 𝑠 (𝑐) 𝑡 =
Some(𝑡 ′ ), if we have 𝑡 R (𝑚, 𝑎) for some memory state 𝑚, then there exists some amount of gas 𝑔 and
a memory 𝑚 ′ reachable from 𝑚 by execution of 𝑚(𝑐) such that 𝑡 ′ R (𝑚 ′, 𝑎) holds.
  It’s worth noting that this correctness theorem neatly separates out three different source of
undefined behavior. First, runtime errors or assertion failures cause a transaction to revert; this is
represented by the high-level specification returning None instead of the Some. An attacker can
always set up situations where a contract reverts, so the compiler will ensure that the compiled
bytecode faithfully follows the source program semantics in this case.
    Foundational Verification of Smart Contracts through Verified Compilation                           15


       Second, it is the programmer’s responsibility to avoid integer overflows and similar sources of
    overflow: DeepSEA will the make the user prove that there are none in the VC(⌋, ⊔) condition, and
    then the compiler can assume that no such behavior is present. In this way, a DeepSEA program
    can be compiled more efficiently than a Solidity program using the “safe math” library, because the
    latter will insert a runtime check after every arithmetic operation, while the DeepSEA programmer
    only needs to insert as many checks as needed for the VC-proofs to go through.
       Third, out-of-gas errors are treated separately. When proving safety properties gas cost can be
    ignored, and indeed it is not part of the current generated specifications 𝑠 (𝑐). In future work, we
    may extend the system to also generate a second set of specifications which exactly tracks the gas
    usage of each command.

    4.3   Verified compiler backend
    The backend for the MiniC language has two compilation paths, compiling to either EVM or
    “Ethereum-flavored Web Assembly” (eWasm), but the eWasm path does not yet have a correctness
    proof. The EVM path consists of a series of intermediate representations, ending with a final phase
    that connects this IRs to a formalization of the EVM written in Lem and extracted into Coq. This
    formalization [Hirai 2017] of the EVM has been tested against the VM test suites provided by the
    Ethereum Foundation.
       The source language MiniC and the first few phases of the compiler are inspired by Comp-
    Cert [Leroy et al. 2016], but the later phases are quite different because we target a stack machine.
    Similar to CompCert, the correctness of compilation theorem for each pass is a forward simulation
    diagram, which is in the form of a lock-step, plus or star simulation. The proofs can then be
    composed into a simulation for the entire compiler. Because the source language is deterministic,
    the forward simulation proof also implies a bisimulation relation.

    4.3.1 General Framework. In order to define the semantics of all the intermediate languages, all
    phases of the backend share certain data. First, a global environment which maps function names to
    function definitions and global variable names to the corresponding locations. Second, to support
    EVM operations such as querying current account balances there is a machine environment, a
    record which contains information about the contract and state of the VM. Finally, following
    CompCertX [Gu et al. 2015], the backend and the machine environment are further parametrized by
    an abstract data type called adata. This is a way to support separate compilation: in addition to the
    concrete memory each program state also contains an abstract data value, and when compiling a
    particular function this value is instantiated to a record which describes the state of other functions
    and contracts. A global environment along with an initial memory and abstract state are constructed
    at the beginning of the program execution.
       The syntax for the first seven intermediate languages consists of statements and expressions. The
    distinction being that expressions do not have side-effects while statements might. Expressionless is
    the last IR which deals with expressions.
       Each compilation pass manipulates values which are represented throughout the backend by the
    following type:
1   Inductive val: Type := (* defined in LowValues.v *)
2   | Vunit: val
3   | Vint: int256 -> val
4   | Vhash: val -> val
5   | Vhash2: val -> val -> val.

    Programs for the EVM make very frequent use of 256-bit hash operations, and generally assume
    that there are never any hash collisions; for example all hash mappings are stored directly with no
 Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
16                                                                                           Reeves, and Zhong Shao

attempt to detect collisions. Therefore we use this symbolic representation of constructing a hash
value from one key and constructing a hash value from two keys respectively, which implicitly
ensures that all hash operations are injective. In the final compiler phase we need an axiom (which
is actually false, but “true enough”) stating that the concrete Keccack hash function is injective.
   The operational semantics for each intermediate representation are defined as labeled transition
                                                                s
systems. The transition relation takes the form 𝐺 ⊢ 𝑆 1 →       − 𝑆 2 . Here 𝐺 represents the general
environment on which each compilation pass is parametrized (the global environment genv and
the machine environment machine_env), 𝑆 1, 𝑆 2 represent the states of the transition system and 𝑠
represents one step of execution from state 𝑆 1 to 𝑆 2 . The semantics of each such step corresponding
to an instruction in the code is defined for each compilation pass by the inductively defined relation
step. What constitutes the program state varies for each intermediate language, but for most of
the passes they come in four different kinds:
     • regular states (State) represent the states of the program during execution of steps which
       do not require control to transfer to another function;
     • call states (Callstate) represent the state of the program when it performs a call to another
       function within the contract;
     • initial states (Initialstate) represent the state of the transition system before contract
       execution begins;
     • return states (Returnstate) represent the state of the transition system when a function is
       about to return.

   Handling gas. Because we are compiling to EVM, each state type also contains a natural number
which is the amount of gas the program has consumed, and which is incremented as each instruction
is executed. The simulation relation for each phase specifies that the target code consumes at most
as much gas as the sources. The amount consumed may go down, either because the compiler
optimizes the code, or because we deliberately overapproximated e.g. the gas cost of a function call
(by assuming the maximal number of arguments) to make the source language semantics simpler
for the end user.
   This convention for gas handling is the opposite of the actual EVM, and the EVM formalization
we target: there the state counts the remaining gas, which is decremented by each instruction,
and the program becomes stuck/reverts if the count hits zero. In early versions of the backend we
tried the same, but the counting-down convention does not let allow a strong enough correctness
theorem. We want to say that, if the source program computes a value using some amount 𝑔 gas,
then running the target program will either compute the same value or run out of gas (and if you
submit at least 𝑔′ > 𝑔 gas it will successfully compute). An attacker can force a program to run
out by paying for too little gas, so we want to know that the compiled contract will still end up in
a safe state in that case. But because of optimization, the compiled program may not run out of
gas even if the source semantics claims it will, so we do not want a source semantic that claims
that programs will always abort if the gas reaches zero; we want the source program to continue
executing to know what it would have computed. At the final EVM generation compiler phase
there are no further optimizations so we can prove an exact relation between the “gas used” and
“gas remaining” counts.
   Next we give a brief description of some of the important phases of the Ethereum backend of the
compiler.

4.3.2 Clike. The Clike phase models persistent storage separately from memory, instead of keep-
ing it as part of the extended environment. In particular, when compiling accesses a[k] to a
hashmapping in storage, this phase generates the actual hash operation.
    Foundational Verification of Smart Contracts through Verified Compilation                            17


       The Clike IR shares the same syntax as MiniC, but the semantic evaluation rules for expressions
    differ. Left-expressions are no longer implicitly dereferenced, and instead evaluate to pointers
    which must be explicitly dereferenced. Furthermore, the storage environment is not the same as the
    extended environment. It corresponds to the EVM’s storage and hence the keys are represented by
    an inductive type 𝐻𝑎𝑠ℎ𝐾𝑒𝑦 which represents an abstraction of hash values as opposed to extended
    identifiers:
1   Inductive HashKey :=
2   | singleton : int256 -> HashKey
3   | pair : HashKey -> int256 -> HashKey.
       The phase leaves statements the same but changes the expressions embedded in them. Since
    the storage is modeled explicitly in this pass, the 𝐸𝑔𝑙𝑜𝑏 expressions are also translated to first
    evaluate the identifiers as hash values. Other expressions dealing with extended identifiers, such as
    𝐸𝑖𝑛𝑑𝑒𝑥 and 𝐸 𝑓 𝑖𝑒𝑙𝑑, are treated based on the type of the left expression: if it is a memory pointer
    it is unmodified while if it is a storage pointer it is evaluated as a hash value using the 𝐸𝑏𝑖𝑛𝑜𝑝
    expression type.
       In order to define a simulation relation between the states of the two IRs, we first define relations
    to match the storage and the extended environment, ensure that no additional gas is consumed
    in this translation and match every other component in the state representation in MiniC to its
    translation.
    4.3.3 Cgraph. The Cgraph IR represents functions as control-flow graphs, where each statement
    is a node with an edge to its successor. Immediately after constructing a CFG-representation of the
    program, we carry out a live variable analysis of all the temporary variables, and use a standard
    graph-coloring register assignment algorithm to rename temporary variables into a smaller set.
    This is important because temporaries will eventually be mapped to items on the EVM argument
    stack, and only the top 15 variables can be accessed. Other EVM compilers, such as Solidity, give
    an error if a function has more than 15 local variables, but we can accommodate more if their live
    ranges do not overlap.
    4.3.4 Cbasic. The Cbasic IR groups lists of statements into blocks. Program execution happening
    within such a block is represented by an additional execution context constructor called Block. The
    list of statements enclosed within the block are syntactically the same as the statements in Cgraph.
    This intermediate language and phase is similar to the similarly named phase in CompCert, except
    that blocks can end with Srevert (which aborts the entire transaction) as well as Sdone.
       The Block constructor represents the execution context when the control is within a block of
    statements. The transition step semantics for this IR are given by the inductively defined proposition
    step, like in the previous IRs. However, due to the additional state description given by the Block
    constructor, the step semantics are worth mentioning. Except for the semantics for control-flow
    statements where the execution context transitions from a Block to a State, any execution of
    other statement only causes transition within the Block state, where the change is that a statement
    is consumed. The execution of the Scall statement on the other hand, causes the state to transition
    from a Block to a Callstate.
       The translation of statements from the Cgraph IR to a block in the Cbasic IR is done by appending
    a Sjump node statement at the end of each statement from Cgraph except Srevert and Sdone, to
    obtain a bblock.
    4.3.5 Clinear. This pass linearizes the CFG generated from the Cbasic IR. The code in a program
    execution is now a list of statements instead of a DAG. The CFG structure aids controlflow analysis,
    but we eventually need to print out a linear list of assembly instructions. The syntax for the
 Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
18                                                                                           Reeves, and Zhong Shao

expressions remains the same, and the statements in this IR largely remain the same, except for two
new additions Sfetchargs, Sintro. These statements push data onto the call stack corresponding
to the arguments for the EVM calldata operation and adding fresh temporaries respectively.
   The code linearization process begins with an enumeration of all the labels that appear in the
body of the function we are compiling. There is a heuristic that generates them using a depth-first
traversal of the CFG, in order to avoid inserting unnecessary jump instructions between basic
blocks. Once we have a list of nodes, the code for this phase is generated from the code in Cbasic
by concatenating the blocks in Cbasic in the order of the enumeration of the labels.
   The match_states relation is defined using a match_stackframes relation between the calling
context in the source and target languages, and mapping function representations to their translated
counterparts. Certain subtleties of this relation come through while defining it for the execution
contexts for the custom Ethereum statements. We state the case for the Stransfer statement failing
here. The cases for conditional jumps (Sjumpi) and method calls (Scallmethod) failing are treated
similarly and so we omit them for brevity.
     • match_states_transfer_fail : This constructor is defined to relate execution of the
        Stransfer statement which is an EVM specific statement. It models the case when the
        execution fails. Similar to the constructor to model successful conditional jumps, the state
        reached in the Cgraph execution context once the transfer fails is matched to the state in
        the Clinear execution context where the condition for the transfer to fail holds, but the step
        is yet to be executed. The condition expressing this failure is stated as:
        DOJUMP: (MachineModelLow.me_transfer me) a' v' lg' lg Int256.zero)
        Hence, the state
        (State s f pc (TempsL le) se lg g)
        is matched to the state
        (State ts tf (Stransfer a v pc :: c) (TempsL le) se lg' (g' + gas_transfer_cintptr a v 0)).
The simulation diagram for the correctness proof for this translation is a star simulation, and hence
we need a notion of measure to prevent the problem of stuttering. After much experimentation, the
measure on the Cbasic state representations is defined over non-negative integers with all states
except the Block (which has measure 1) state having measure 0.
4.3.6 Stacked. This is the first IR where the syntax for the expressions is different from the MiniC
expressions. The syntax for this IR is given in Figure 5b. The code is represented as a list of
statements and functions are again record types, but this time with only one field fn_code. The
function stacked_expr converts expressions from Clabeled to a list of statements in Stacked. The
semantics of expressions from the previous phase on whether they are to be treated as R-values or
L-values is conveyed through a boolean which is passed as an argument to stacked_expr. This value
is true if the expression is to be evaluated in a right handed context and false otherwise. The state of
the execution context is represented in a similar way as the previous pass. One notable change is that
instead of having a callstack and a local environment, every state now has stack_entries. These
stack_entries are represented as a list of the tagged type LowValue.val + generic_label.
Values pushed as stack_entries represent the values that expressions are evaluated to and the
generic_label data type represents typed labels which are annotated with the function from
which they were pushed. This is done so that the function to be returned to can be looked up
from the general environment. The value of the expression that it evaluates to and how it modifies
stack_entries is dictated by the eval_rvalue function, whose excerpt we give here:
     Foundational Verification of Smart Contracts through Verified Compilation                             19


1    Inductive eval_rvalue: expr -> stack_entries -> stack_entries -> Prop :=
2        | eval_Econst_int256: forall i st,
3            eval_rvalue (Econst_int256 i) st (inl (LowValues.Vint i) :: st)
4        | eval_Etempvar: forall i v st,
5            stack_get st i = Some v ->
6            eval_rvalue (Etempvar i) st (inl v :: st)
7        | eval_Esload: forall ptr i st,
8            HashEnv.read ptr he = Some i ->
9            (*read' ptr he = Some (OfLow i) ->*)
10           eval_rvalue Esload (inl ptr :: st) (inl i :: st).



     ⟨expression⟩ :: = const256(𝑖)                                         ⟨statement⟩ :: = skip
       | global(𝑖)                                                           | rvalue(𝑒)
       | temp(𝑛)                                                             | pushvoid
       | sload                                                               | pop
       | unop(𝑜𝑝)                                                            | assign
       | binop(𝑜𝑝, 𝑏)                                                        | set(𝑛)
       | call0(𝑏0)                                                           | done(𝑛, 𝑟𝑡 )
       | call1(𝑏1)                                                           | pushlabel(𝑡)
                                                                             | label(𝑙)
                    (a) Expressions
                                                                             | jump_call
                                                                             | jump_internal
                                                                             | jumpi
                                                                             | transfer
                                                                             | callmethod(𝑖, 𝑛 1, 𝑛 2 )
                                                                             | log(𝑛 1, 𝑛 2 )
                                                                             | revert
                                                                             | fetchargs
                                                                                        (b) Statements

                                                   Fig. 5. Stacked syntax


     The state of the execution context is parametrized by the arguments to be passed to the Scallmethod
     statement. They are no longer a part of the arguments that the statement takes. Instead, the statement
     is passed the number of arguments that it needs. Since these arguments do not change throughout
     the program execution, they are declared as a parameter instead of being passed around in the state.
     The translation from Clableled to Stacked is parametrized by a map of temporary variables mapped
     to their values. This map is initialized by the temporaries declared as a part of the function definition
     in Clabeled using the allocate_fn_temps function. Once this map is initialized, it is passed as
     the parameter for translating Clabeled code to Stacked code, which is then used to construct a
     Stacked function from a Clabeled function. Finally, the stacked_genv function converts the global
     environment from Clabeled to the global environment for Stacked using the functions listed above
     to translate the corresponding parts. The whole program is converted from its representation in
     Clabeled to that in Stacked after performing a check that the function and method labels do not
     repeat. The semantic preservation of the translation is proved using a plus simulation diagram.
     4.3.7 Expressionless. As is evident from the name, this is the first IR where expressions are no
     longer a part of its syntax. The syntax for statements in this IR is given in Figure 6.
 Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
20                                                                                           Reeves, and Zhong Shao

⟨statement⟩ ::= push(𝑣 + 𝑙) | dup(𝑛) | sload | unop(𝑜𝑝) | binop(𝑜𝑝, 𝑏)
  | call0(𝑏 0 ) | call1(𝑏 1 ) | skip | pop | sstore | swap(𝑛) | done(𝑟𝑡 )
  | label(𝑙) | jump | jumpi | transfer | callmethod(𝑖, 𝑛 1, 𝑛 2 )
  | log(𝑛 1, 𝑛 2 ) | revert | calldataload | constructordataload(𝑛)

                                          Fig. 6. Expressionless syntax


   The code, function, global environment and program representation are the same as in the
Stacked IR. It is from this pass where the transition from the CompCert style backend to an IR
written to match the execution context of the EVM becomes clear. Since the EVM has a special
function called the constructor, which compiles differently than other methods in the contract, it
is compiled in a different manner than normal methods/functions. In order to indicate whether a
particular function is a constructor a datatype function_kind is defined and is passed around as
the type of the function. The compilation of a constructor differs from that of a normal function in
two primary ways. Firstly, function calls from the constructor are prohibited and second is that
the callmethod arguments which parametrize the execution context of this IR (similar to Stacked)
are loaded in a different way for constructors. The state representation for this IR is the same
as that for Stacked except that there is no separate Callstate for function calls. The function
expressionless_stm takes a stacked statement, a function_kind argument to indicate the type
of function for which the compilation is going on (needed to determine what Sjump_call gets
compiled to) and returns an option type on list of expressionless statements. Every translation
function takes an argument of the type function_kind to determine what type of function is being
compiled and returns a translation accordingly. Finally, the expressionless_genv function is used
to construct the global environment, and to convert the program representation from Stacked after
performing the check that labels in the program do not repeat and each function begins with it’s
own label.
4.3.8 Methodical. The syntax for this IR is the same as that for Expressionless. The only and major
difference is in the semantics where this IR instead of providing separate entry points into the
contract for each method, streamlines the contract code into one list of statements with a single
entry point into the contract that “multiplexes” into the correct method. This is reflected as expected
in the function that translates the Expressionless program to return the code for execution in the
Methodical IR. This is done by the methodical_main function which uses the helper function
methodical_multiplexer_body. methodical_multiplexer_body is a recursively defined func-
tion that takes the list of methods and a map which takes a method to its definition as arguments,
and returns an option type on code. For each method in the list, it looks for its definition in the
map and returns a list of statements which are semantically equivalent to performing a conditional
jump to the method definition if the signature of the function that is to be executed matches the
method label. This is the main step for this compilation pass which achieves the effect described in
the paragraph above.
4.3.9 EVM_lem. This is the final pass of the DeepSEA compiler backend. The methodical IR is
translated to the syntax for the execution of code in this EVM formalization as defined in [Hirai
2017]. This formalization acts as an interpreter for a single smart contract execution. This is
achieved by providing a formal definition of the EVM which is widely portable. Since all smart
contract executions on the EVM happen within a block of various transactions clumped together
by the miner, the execution context here is a block which is defined using a Coq record data
type block_account. The execution context for this phase is completely characterized by two
    Foundational Verification of Smart Contracts through Verified Compilation                          21


    record types, the constant_ctx and variable_ctx. The constant_ctx consists of fields which
    represent relatively stable data, unaffected by the execution of instructions but needed to access
    the information required to successfully execute bytecode. The variable_ctx on the other hand
    constitutes of fields which represent data susceptible to change with instruction execution. The
    program is also represented using a record type:
1   Record program : Type := {
2     program_content : Z -> option inst ; (* a way to look up instructions from positions *)
3     program_length : Z (* the length of the program in bytes *)
4   }.
    The equivalent of the statement datatype from the previous passes is the inst datatype which is
    an inductively defined wrapper type used to represent EVM opcodes. The possible outcomes of
    executing an opcode are captured by the instruction_result datatype defined as follows:
1   Inductive instruction_result : Type :=
2   | InstructionContinue: variable_ctx -> instruction_result (* the execution should continue. *)
3   | InstructionToEnvironment:
4     (* the execution has stopped; either for the moment just calling out another account, or *)
5     (* finally finishing the current invocation *)
6       contract_action    (* the contract's move *)
7     -> variable_ctx        (* the last venv *)
8     -> option ((Z * Z) % type) -> instruction_result .
    A total function instruction_sem defines the semantics of all the opcodes and their effect on
    the state of the EVM. A helper function meter_gas computes the amount of gas required for the
    execution of the opcode and then subtract_gas subtracts it from the gas balance of the contract.
    Finally, the execution of the entire program and its effects on the state of the EVM is defined using
    a recursive function program_sem:
1   Program Fixpoint program_sem (stopper : instruction_result -> unit) (c : constant_ctx) (fuel :
    ↩→  nat) (net : network) (pr : instruction_result) : instruction_result :=
2   match ( fuel) with
3    | 0%nat => pr
4    | S (fuel_pred) => program_sem stopper c fuel_pred net (next_state stopper c net pr)
5   end.
       Here the function next_state is a helper function which acts on the EVM state in the same
    way as the fold function does on lists. The program execution for this pass is modeled in the form
    of a game between the environment and the contract. The possible moves of both the players
    are defined via the inductive types environment_action and contract_action respectively. The
    operational step semantics are defined by the step definition which takes a global_state as an
    argument and returns the modified global_state obtained upon execution of an operation. The
    record type global completely characterizes the VM state including a list of ongoing calls and their
    respective execution states. For a detailed exposition of the model used in this formalization, we
    refer the reader to [Hirai 2017]. The translation of statements from the Methodical IR to the syntax
    in the EVM formalization is done via a total function s_t_opcodes which takes as arguments a
    statement, and a map from labels to integers (this is needed in order to convert labels being pushed
    onto the stack into bytes) and returns a list of instructions.
       In order to prove semantic preservation for this pass, we set up the correspondence between differ-
    ent components of the execution context in the following way: the block_account corresponding to
    the execution context in the Methodical phase is constructed through the initial_state_account
    definition which takes the account address and the storage (which is defined to be a function that
    takes a word of size 256 and returns the corresponding word in the storage of that size) as arguments
    and returns the corresponding block_account. Similarly, the initial variable and constant context
     Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
    22                                                                                           Reeves, and Zhong Shao

    (variable_ctx, constant_ctx respectively) are constructed as functions of the account address,
    storage and the amount of gas available for program execution. The definitions constant_ctx_init
    and variable_ctx_init are defined for this purpose. The definition initial_arguments initial-
    izes the environment with the appropriate calldata arguments and the constructor code used
    to deploy the runtime code for the contract. Using these definitions, initial_global takes the
    account address, the storage and the remaining gas as arguments and constructs an instance of
    the global record type described above. Once the environment has been initialized with the ap-
    propriate data, we further setup the variables to correspond to the entry point to the code of the
    methodical pass. This is done via the enter_code_account, enter_code_cctx, enter_code_vctx,
    enter_code_state and the enter_code_global definitions respectively. Similar helper defini-
    tions are defined to relate the final states in both the languages. In order to set up the simulation
    relation to prove the semantic preservation, we define a wrapper proposition to mimic the step
    semantics in the methodical pass:
1   Inductive lem_step (n : network) : option global_state -> option global_state -> Prop :=
2    | Init_state : forall addr he l g,
3      lem_step n None (Some (Continue (enter_code_global addr (hash_env_to_store he) g l)))
4    | Take_step : forall g1 g2,
5      block.step n g1 = g2 ->
6      lem_step n (Some g1) (Some g2).
    Since the code is represented as a map as opposed to a list of statements, in order to define a relation
    between the respective state representations, we need to relate the corresponding elements of the
    states. The characterizing elements are the code in the account, the storage, the memory and the
    stack. Here we present the correspondence for each of these in order:
         • Code representation: we first define an inductive relation to match the program counter in
            the Lem formalization to the corresponding statement being executed in the methodical IR:
        1     Inductive code_from_counter : Z -> evm.program -> list inst -> Prop :=
        2     | N : forall (pc : Z) (p : evm.program), code_from_counter pc p nil
        3     | L : forall (l : list inst) (i : inst) (p : evm.program) (pc : Z) ,
        4           (program_content p) pc = Some i ->
        5           code_from_counter (pc + (inst_size i)) p l ->
        6           code_from_counter pc p (i :: l).
              The above relation is simply a recursive way of relating valid program counter positions to
              the instructions that can be read from them. Once we have this relation, we use it to define
              a relation between the respective code representations as follows:
        1     Definition rel_code (l_map:PMap.t Z) (p:evm.program) (code:list statement) (pc:Z) : Prop :=
        2       code_from_counter pc p (flatmap (fun s1 => s_t_opcodes s1 l_map) code).
              The above relation simply states that the entire code in the methodical state is related to
              the beginning position of the program counter for that code.
            • Memory representation: this relation is defined so as to compare the values read from the
              memory representations in the two passes from the same address. Since the datatypes used
              to represent corresponding values is different, we use appropriate conversion functions to
              be able to compare them.
        1     Definition rel_mem (l_map : PMap.t Z) (stk :stack_env ) (m :memory ) :Prop :=
        2     forall (i : LowValues.val) (b1 : LowValues.val),
        3     StackEnv.read_from_base i stk = Some b1 ->
        4     cut_memory_aux_alt (entries_to_w256 (inl i) l_map) 32 m = val_to_list_bytes b1.
            • Storage representation: the relation to match corresponding storage models is defined in a
              similar manner as the memory representation relation.
     Foundational Verification of Smart Contracts through Verified Compilation                             23


           1     Definition rel_store (l_map : PMap.t Z) (he :hash_env) (s:storage) : Prop :=
           2     forall (v : val) (b1: LowValues.val),
           3     HashEnv.read v he = Some b1 ->
           4     s (entries_to_w256 (inl v) l_map) = entries_to_w256 (inl b1) l_map.
               • Stack representation: in both the languages the stack representations are related by a recur-
                 sively defined relation, which relates empty stacks as the base case, and relates two stacks
                 if the top elements represent the same value and the tail stacks are related.
           1     Inductive rel_stk (l_map : PMap.t Z): stack_entries -> lem_stack -> Prop :=
           2     | Empty : rel_stk l_map ([]) ([])
           3     | Push_elem : forall s1 s2 v1 v2 ,
           4             rel_stk l_map s1 s2 ->
           5             entries_to_w256 v1 l_map = v2 ->
           6             rel_stk l_map (v1 :: s1) (v2 :: s2).
               • Gas relation: the Lem defined EVM model semantics subtract gas upon execution of each
                 instruction, whereas the Methodical IR accumulates the amount of gas required for the
                 successful execution of the whole program. To relate the two ways of accounting for gas,
                 we require that after each instruction execution the sum of the gas components in both the
                 state representations does not change. This is because the amount that gets added in the
                 Methodical semantics is the exact amount that gets removed in the EVM semantics, thus
                 keeping the total constant.
     Now we finally define a relation for the corresponding state representations using the above
     relations:
1    Inductive rel (gas_limit : Z) (l_map : PMap.t Z) : state -> option global_state -> Prop :=
2     | I : forall s g d,
3           rel gas_limit l_map (Initialstate empty_stack s d g) None
4     | E : forall s g ,
5           rel_stk l_map (state_to_stack s) (vctx_stack (ext_vctx_state g)) ->
6           rel_mem l_map (state_to_senv s) (vctx_memory (ext_vctx_state g)) ->
7           rel_store l_map (state_to_henv s) (vctx_storage (ext_vctx_state g)) ->
8           rel_code l_map (cctx_program (g_cctx g)) (state_code s) (vctx_pc (ext_vctx_state g)) ->
9           vctx_gas (ext_vctx_state g) + Z.of_nat (state_gas s) = gas_limit ->
10          rel gas_limit l_map s (Some (Continue g)).
     The correctness of the above relation is proved using a plus step simulation.

     4.4       Optimizations
     The Expressionless phase has machinery for performing peephole optimizations. Optimization is
     paramount: the cost for execution is directly derived from the executed instructions and access to
     storage/memory and for every inefficiency the caller looses money—for every call: [Albert et al.
     2020] super-optimize a function within the AirdropToken smart contract, which is called more
     than half a million times. In total they estimate savings of $2815. [Brandstätter et al. 2020] analyzed
     optimizations of 3000 Solidity contracts from etherscan.io with respect to well-known compiler
     optimization strategies and found that around 7 % of contracts could be improved.
        In peephole optimizations, we replace small sequences of EVM bytecode by cheaper, observation-
     ally equivalent code using rewrite rules. They are local, closed under context, and modular, as well
     as adjustable by adding or removing rewrite rules. To obtain rewrite rules, we leverage the tool
     ppltr [Schett and Nagele 2020], which generates peephole optimization rules from optimizations
     found by the EVM bytecode superoptimizer ebso [Nagele and Schett 2019], which encodes the
     search for cheaper, observationally equivalent, EVM bytecode into an SMT problem. While these
     optimizations are found by an automated theorem prover and correct by construction with respect
     to the model encoded in SMT, the correctness argument needs to be proved within the compiler.
 Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
24                                                                                           Reeves, and Zhong Shao

Reproving the correctness also widens the scope: the state modeled in SMT does not capture all of
the EVM state, e.g., it does not model memory, which can then be shown as unaffected. Our first
approach to extract SMT proofs to Coq failed due to uncertainty on how to relate the encodings
of the EVM semantics in the two settings. The practical solution is to extend the tool ppltr to
generate Coq proofs with tactics. In our formalization, peephole optimization rules have two com-
ponents: (1) the definition rule_rewrite of the rule, and (2) a proof rule_correct showing that
if there is an optimization p to po then after executing p and po the global environments coincide
apart the from the gas costs. The proofs employ tactics to execute the original instructions p,
and the optimized instructions po and observe that the state is equivalent. One key lemma is to
show that gas consumption grows monotonically when executing a program. For stack-based
optimization rules, such as optimizing DUP SWAP to DUP, equivalence of the states follows directly
from the execution. Optimization rules targeting the algebraic properties of instructions, e.g.,
zero is the neutral element in addition, need a lemma data base. The peephole optimization rules
can be applied to any program exhaustively. The (strict) gas decrease in every rule immediately
gives a reduction order. Then correctness of applying peephole optimizations follows by induc-
tion from rule_correct of the individual rules. The current state of the work can be found at:
https://github.com/mariaschett/ppltr/tree/ace6324916534fc37290c870da47171fdbe4a98c.

5   RELATED WORK
   Verified compilers. In the last decade, several large and mature verified compilers, such as Com-
pCert [Leroy et al. 2016] (which the DeepSEA compiler is partly based upon) and CakeML [Tan
et al. 2016], have been developed. However, the only verified compiler for smart contracts, which
we are aware of, is Elle [Alvarez 2019]. While Elle targets the same Lem formalization of EVM as
us, the Elle source language is less ambitious than DeepSEA: it compiles a version of the LLL (“low
level language”) programming language. LLL is similar to a macro assembler or an intermediate
language such as Yul: it provides structured control flow like while-loops and if-statements, but
apart from that all commands are raw EVM assembly instructions directly affecting storage and
memory; there are no higher-level data types as in DeepSEA. Elle does not distinguish undefined
behavior such as overflows in DeepSEA, and the compiler does no optimizations.
   SMT-based smart contract verification. Various tools exist for smart contract verification that
rely on SMT solvers to discharge proof obligations. These include Mythril [ConsenSys 2021],
Oyente [Luu et al. 2016], Solc-verify [Hajdu and Jovanović 2019], Solidity’s SMTChecker [Alt and
Reitwiessner 2018], Verisol [Born et al. 2020] and Verx [Permenev et al. 2020]. A key difference
between these tools and our approach is that the DeepSEA is foundationally verified. In addition, our
use of Coq allows the full power of interactive theorem proving which is critical for the verification
of complex properties of smart contracts such as the Automated Market Maker. While SMT solvers
will typically solve the goals they are able to solve more quickly than an equivalent DeepSEA proof,
we believe that the trade-off for more expressiveness is worthwhile in many cases.
   Low-level language formalizations. The low-level stack based smart contract language Michelson
of the Tezos blockchain is formally specified in Coq. This formalization, Mi-Cho-Coq [Bernardo
et al. 2020a], enables verification of Tezos smart contracts at a low-level. Their work differs from
DeepSEA firstly in that it does not target Ethereum, which at the time of writing is by a large
margin the most popular blockchain with fully-featured smart contracts. Secondly, DeepSEA works
with a high-level functional representation of a smart contract rather than the low-level stack-based
language Michelson. There does appear to be ongoing work in the Tezos community to facilitate
proofs about higher level representations of Tezos smart contracts such as a step towards that with
the intermediate language Albert [Bernardo et al. 2020b]. Another formalization, Eth-isabelle [Hirai
Foundational Verification of Smart Contracts through Verified Compilation                                                 25


2018] makes use of the same Lem model [Hirai 2017] as used in DeepSEA. While this theoretically
means Eth-isabelle’s capabilities are like those of DeepSEA, Eth-isabelle operates at a much lower
level—typically reasoning about low-level EVM instructions which limits its expressiveness and
usability, similarly to Mi-Cho-Coq. The KEVM [Hildenbrandt et al. 2018] is a well validated formal
semantics of the EVM which has been used along with the K-framework to enable formal verification
of a range of real-world smart contracts. The KEVM also relies upon an SMT solver to solve goals
which would constrain its ability to prove some complex lemmas compared with a proof assistant
such as Coq. To the best of our knowledge, the KEVM with the K framework is also only able to
specify and prove reachability-related properties and so its specifications are less expressive than
our approach allows.
   Other Coq-based systems. Scilla [Sergey et al. 2019] is the smart contract language of the Zilliqa
blockchain. Their work on delivering a fully-functional proof system in Coq for Scilla has ceased
(to the best of our knowledge). Nevertheless their work is helpful in demonstrating some key ideas
about a smart contract proof system. ConCert [Annenkov et al. 2020] is a smart contract verification
framework which enables the embedding of functional languages into Coq using a novel technique.
Unlike DeepSEA, both approaches are not foundational.

6   CONCLUSIONS AND FUTURE WORK
Using the DeepSEA system, users can verify blockchain contracts inside the Coq proof assistant.
The generated model of the contract is a collection of Coq functions, which can be verified as easily
as any other Coq program. At the same time, by using a verified compiler, the system can offer as
strong foundational guarantees as if we were proving things directly about the compiled bytecode.
We have applied DeepSEA to verify useful realistic programs, including a Uniswap-style market
maker contract.
   There are many directions for future work. First, although the language is already complete
enough for useful contracts we would like to add more feautures, e.g. by completing the backend
proofs about pointers and adding stack-allocated data to the surface language. Second, the verified
compiler currently only deals with individual method calls, but we would like to extend the language
semantics with a model of the full blockchain rather than leaving that model to the user as in
Section 3.2. Third, it will be interesting to explore more compiler optimizations, particularly because
existing EVM compilers do not optimize very agressively. Most importantly, we will want to verify
larger and more important blockchain applications, e.g. the many interacting contracts of a modern
DeFi exchange.

REFERENCES
Elvira Albert, Pablo Gordillo, Albert Rubio, and Maria A. Schett. 2020. Synthesis of Super-Optimized Smart Contracts Using
   Max-SMT. In Computer Aided Verification (Lecture Notes in Computer Science), Shuvendu K. Lahiri and Chao Wang (Eds.).
   Springer International Publishing, Cham, 177–200. https://doi.org/10.1007/978-3-030-53288-8_10
Leonardo Alt and Christian Reitwiessner. 2018. SMT-based verification of solidity smart contracts. In International Symposium
   on Leveraging Applications of Formal Methods. Springer, 376–388.
Mario M Alvarez. 2019. Elle: Foundationally Verified Compilation for Ethereum. (2019).
Guillermo Angeris, Hsien-Tang Kao, Rei Chiang, Charlie Noyes, and Tarun Chitra. 2019. An analysis of Uniswap markets.
   arXiv preprint arXiv:1911.03380 (2019).
Danil Annenkov, Jakob Botsch Nielsen, and Bas Spitters. 2020. ConCert: A smart contract certification framework in Coq.
   In Proceedings of the 9th ACM SIGPLAN International Conference on Certified Programs and Proofs. 215–228.
Anonymised. 2021. Towards Verified Price Oracles for Decentralized Exchange Protocols. (2021). In press, accepted at the
   3rd International Workshop on Formal Methods for Blockchains.
Bruno Bernardo, Raphaël Cauderlier, Zhenlei Hu, Basile Pesin, and Julien Tesson. 2020a. Mi-Cho-Coq, a Framework for
   Certifying Tezos Smart Contracts. In Formal Methods. FM 2019 International Workshops, Emil Sekerinski, Nelma Moreira,
   José N. Oliveira, Daniel Ratiu, Riccardo Guidotti, Marie Farrell, Matt Luckcuck, Diego Marmsoler, José Campos, Troy
 Vilhelm Sjöberg, Kinnari Dave, Daniel Britten, Maria A Schett, Xinyuan Sun, Qinshi Wang, Sean Noble Anderson, Steve
26                                                                                           Reeves, and Zhong Shao

   Astarte, Laure Gonnord, Antonio Cerone, Luis Couto, Brijesh Dongol, Martin Kutrib, Pedro Monteiro, and David Delmas
   (Eds.). Springer International Publishing, Cham, 368–379.
Bruno Bernardo, Raphaël Cauderlier, Basile Pesin, and Julien Tesson. 2020b. Albert, an intermediate smart-contract language
    for the Tezos blockchain. In International Conference on Financial Cryptography and Data Security. Springer, 584–598.
Sylvie Boldo, Catherine Lelay, and Guillaume Melquiond. 2015. Coquelicot: A user-friendly library of real analysis for Coq.
    Mathematics in Computer Science 9, 1 (2015), 41–62.
Cody Born, Immad Naseer, and Kostas Ferles. 2020. Formal verification of workflow policies for smart contracts in azure
    blockchain. In Verified Software. Theories, Tools, and Experiments: 11th International Conference, VSTTE 2019, New York
    City, NY, USA, July 13–14, 2019, Revised Selected Papers, Vol. 12031. Springer Nature, 87.
T. Brandstätter, S. Schulte, J. Cito, and M. Borkowski. 2020. Characterizing Efficiency Optimizations in Solidity Smart Con-
    tracts. In 2020 IEEE International Conference on Blockchain (Blockchain). 281–290. https://doi.org/10.1109/Blockchain50366.
    2020.00042
ConsenSys. 2021. Mythril. https://github.com/ConsenSys/mythril-classic. Accessed: 6 July 2021.
Maxime Dénès, Catalin Hritcu, Leonidas Lampropoulos, Zoe Paraskevopoulou, and Benjamin C Pierce. 2014. QuickChick:
    Property-based testing for Coq. In The Coq Workshop, Vol. 125. 126.
Ronghui Gu, Jérémie Koenig, Tahina Ramananandro, Zhong Shao, Xiongnan (Newman) Wu, Shu-Chun Weng, Haozhong
    Zhang, and Yu Guo. 2015. Deep Specifications and Certified Abstraction Layers. SIGPLAN Not. 50, 1 (Jan. 2015), 595–608.
    https://doi.org/10.1145/2775051.2676975
Ákos Hajdu and Dejan Jovanović. 2019. solc-verify: A modular verifier for Solidity smart contracts. arXiv preprint
    arXiv:1907.04262 (2019).
Everett Hildenbrandt, Manasvi Saxena, Nishant Rodrigues, Xiaoran Zhu, Philip Daian, Dwight Guth, Brandon Moore,
    Daejun Park, Yi Zhang, Andrei Stefanescu, et al. 2018. Kevm: A complete formal semantics of the ethereum virtual
    machine. In 2018 IEEE 31st Computer Security Foundations Symposium (CSF). IEEE, 204–217.
Yoichi Hirai. 2017. Defining the Ethereum Virtual Machine for Interactive Theorem Provers. In Financial Cryptography and
    Data Security, Michael Brenner, Kurt Rohloff, Joseph Bonneau, Andrew Miller, Peter Y.A. Ryan, Vanessa Teague, Andrea
    Bracciali, Massimiliano Sala, Federico Pintore, and Markus Jakobsson (Eds.). Springer International Publishing, Cham,
    520–535.
Yoichi Hirai. 2018. A Lem formalization of EVM and some Isabelle/HOL proofs. https://github.com/pirapira/eth-isabelle
   Accessed: 6 July 2021.
Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus Pister, and Christian Ferdinand. 2016. CompCert-a
    formally verified optimizing compiler. In ERTS 2016: Embedded Real Time Software and Systems, 8th European Congress.
Loi Luu, Duc-Hiep Chu, Hrishi Olickel, Prateek Saxena, and Aquinas Hobor. 2016. Making smart contracts smarter. In
    Proceedings of the 2016 ACM SIGSAC conference on computer and communications security. 254–269.
Érik Martin-Dorel, Laurence Rideau, Laurent Théry, Micaela Mayero, and Ioana Pasca. 2013. Certified, efficient and sharp
    univariate Taylor models in Coq. In 2013 15th International Symposium on Symbolic and Numeric Algorithms for Scientific
    Computing. IEEE, 193–200.
Julian Nagele and Maria A. Schett. 2019. Blockchain Superoptimizer. In Preproceedings of the 29th International Symposium
    on Logic-Based Program Synthesis and Transformation (LOPSTR 2019). arXiv:2005.05912
Satoshi Nakamoto. 2008. Bitcoin: A peer-to-peer electronic cash system. Decentralized Business Review (2008), 21260.
Daejun Park. 2020. deposit-spec.ini (GitHub). https://github.com/runtimeverification/verified-smart-contracts/blob/master/
    deposit/bytecode-verification/deposit-spec.ini. Accessed: 9/7/2021.
Anton Permenev, Dimitar Dimitrov, Petar Tsankov, Dana Drachsler-Cohen, and Martin T. Vechev. 2020. VerX: Safety
   Verification of Smart Contracts. In IEEE S&P 2020.
Danny Ryan. 2020. Runtime Verification audit and verification of deposit contract. https://blog.ethereum.org/2020/02/04/eth2-
    quick-update-no-8/. Accessed: 9 July 2021.
Maria A. Schett and Julian Nagele. 2020. Populating the Peephole Optimizer of a Smart Contract Compiler. In 2nd Workshop
    on Formal Methods for Blockchains (FMBC 2020) (OpenAccess Series in Informatics (OASIcs), Vol. 84), Bruno Bernardo and
    Diego Marmsoler (Eds.). Schloss Dagstuhl–Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 3:1–3:15.
Ilya Sergey, Amrit Kumar, and Aquinas Hobor. 2018. Scilla: a Smart Contract Intermediate-Level LAnguage. arXiv:1801.00687
    [cs] (Jan. 2018). arXiv: 1801.00687.
Ilya Sergey, Vaivaswatha Nagaraj, Jacob Johannsen, Amrit Kumar, Anton Trunov, and Ken Chan Guan Hao. 2019. Safer
    smart contract programming with Scilla. Proceedings of the ACM on Programming Languages 3, OOPSLA (2019), 1–30.
Vilhelm Sjöberg, Yuyang Sang, Shu-chun Weng, and Zhong Shao. 2019. DeepSEA: A Language for Certified System Software.
    Proc. ACM Program. Lang. 3, OOPSLA, Article 136 (Oct. 2019), 27 pages. https://doi.org/10.1145/3360562
Yong Kiam Tan, Magnus O Myreen, Ramana Kumar, Anthony Fox, Scott Owens, and Michael Norrish. 2016. A new
   verified compiler backend for CakeML. In Proceedings of the 21st ACM SIGPLAN International Conference on Functional
    Programming. 60–73.
Foundational Verification of Smart Contracts through Verified Compilation                                        27


Gavin Wood. 2021. Ethereum: A Secure Decentralised Generalised Transaction Ledger. Technical Report Istanbul Version
   cfa3f42. 40 pages. https://ethereum.github.io/yellowpaper/paper.pdf
Zilliqa. 2020. scilla-coq. https://github.com/Zilliqa/scilla-coq/. Accessed: 28 April 2020.
